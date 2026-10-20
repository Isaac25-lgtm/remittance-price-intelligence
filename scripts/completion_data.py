"""Real-data measurement extensions. Private linkage; public aggregates only."""
from __future__ import annotations
import gc
import json
from pathlib import Path
import numpy as np
import pandas as pd
from rpi import config,features as F,linkage as L
from rpi.acquire import sha256
from rpi.preprocess import load_clean,qlabel
from rpi.completion_stats import dependence_ci

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research_completion'
PRIVATE=OUT/'private_runtime/processed'

def write(frame,name):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);frame.to_csv(p,index=False)

def linked_variant(df,name):
    d=df
    if name=='cc2':return L.link_next_quarter(L.service_table(d,'cc2'))
    if name=='transparent_only':d=df[df['transparent__n']=='yes'].copy()
    if name=='no_negative_fx':d=df[df['cc1 fx margin']>=0].copy()
    if name=='exclude_russia':d=df[df.source_code!='RUS'].copy()
    if name=='exclude_2021_date_anomaly':d=df[(df.collection_date.dt.year*4+df.collection_date.dt.quarter-1)==df.qidx].copy()
    if name=='date_quarter':
        d=df[df.collection_date.notna()].copy()
        d['qidx']=d.collection_date.dt.year*4+d.collection_date.dt.quarter-1
        d['year']=d.collection_date.dt.year;d['qtr']=d.collection_date.dt.quarter
    s=L.service_table(d)
    if name=='reduced_metadata_unique':
        key=[c for c in L.CORE_KEY if c not in ['access point__n','pickup location__n']]
        s['key']=s[key].astype(str).agg('|'.join,axis=1)
        s['key_n_in_quarter']=s.groupby(['qidx','key'])['key'].transform('size')
    lk=L.link_next_quarter(s,horizon=2 if name=='horizon_2' else 1)
    if name=='strict':
        changed=lk.core_reobserved & ~lk.strict_reobserved
        lk.loc[changed,'status']='core_unobserved_corridor_surveyed'
        lk.loc[changed,'core_reobserved']=False
    return lk

def state_frame(lk,threshold=3):
    e=L.eligible_origin(lk,threshold)
    cheap=(lk.cost>=0)&(lk.cost<=threshold)
    state=lk.status.astype(str).copy()
    obs=L.primary_outcome_rows(lk,threshold)
    state.loc[cheap&lk.core_reobserved&~obs]='reobserved_invalid_target'
    state.loc[obs&(lk.cost_next<=threshold)]='observed_stay'
    state.loc[obs&(lk.cost_next>threshold)]='observed_fail'
    d=lk[cheap].copy();d['state']=state[cheap]
    return d

def main():
    PRIVATE.mkdir(parents=True,exist_ok=True)
    assert sha256(config.RAW_FILE)==config.EXPECTED_SHA256
    df=load_clean()
    lk=linked_variant(df,'core')
    lk.to_parquet(PRIVATE/'linked_core.parquet',index=False)
    X=F.build(lk);X.to_parquet(PRIVATE/'features_core.parquet',index=False);del X;gc.collect()
    sf=state_frame(lk)
    flow=sf.groupby(['qidx','state']).size().rename('count').reset_index()
    flow['origin_quarter']=flow.qidx.map(qlabel)
    write(flow,'data/inclusion_exclusion_flow.csv')
    write(flow,'tables/table_01_source_flow.csv')
    profile=df.groupby('qidx').agg(n_quotes=('source_row','size'),n_corridors=('corridor_key','nunique'),n_providers=('firm__n','nunique'),sample_start=('collection_date','min'),sample_end=('collection_date','max'),mean_cost=('cc1 total cost %','mean'),median_cost=('cc1 total cost %','median'),share_transparent=('transparent__n',lambda v:(v=='yes').mean()),negative_cost=('cc1 total cost %',lambda v:(v<0).sum()),negative_fx=('cc1 fx margin',lambda v:(v<0).sum()),digital_access_share=('access point__n',lambda v:v.isin(['internet','mobile phone']).mean())).reset_index()
    profile['quarter']=profile.qidx.map(qlabel)
    profile=profile.merge(sf.groupby('qidx').size().rename('initially_cheap'),on='qidx',how='left')
    write(profile,'data/cohort_by_wave.csv');write(profile,'tables/table_02_profile.csv')
    bounds=L.bounds_table(lk,by='qidx');bounds['origin_quarter']=bounds.qidx.map(qlabel)
    prim=lk[L.primary_outcome_rows(lk)].copy()
    prim['stay']=(prim.cost_next<=3).astype(float)
    cirows=[]
    for q,d in prim.groupby('qidx'):
        ci=dependence_ci(d.stay,d,'corridor',reps=300)
        cirows.append(dict(qidx=q,ci95_lo=ci[0,0],ci95_hi=ci[1,0],n_corridors=d.corridor_key.nunique()))
    bounds=bounds.merge(pd.DataFrame(cirows),on='qidx',how='left')
    write(bounds,'tables/table_03_persistence_bounds.csv')
    overall=L.bounds_table(lk)
    oc=dependence_ci(prim.stay,prim,'corridor',reps=1000)
    overall['corridor_ci95_lo']=oc[0,0];overall['corridor_ci95_hi']=oc[1,0]
    eligible=lk[L.eligible_origin(lk)].copy()
    stay=(eligible.core_reobserved & eligible.cost_next.between(0,3)).astype(float)
    fail=(eligible.core_reobserved & (eligible.cost_next>3)).astype(float)
    for k,values in [('lower',stay),('upper',1-fail)]:
        ci=dependence_ci(values,eligible,'corridor',reps=1000)
        overall[k+'_ci95_lo']=ci[0,0];overall[k+'_ci95_hi']=ci[1,0]
    write(overall,'tables/supplementary_overall_bounds.csv')
    sensitivities=[]
    for name in ['core','strict','reduced_metadata_unique','threshold_2.9','threshold_2.95','threshold_3.05','threshold_3.1','threshold_5','cc2','horizon_2','date_quarter','transparent_only','no_negative_fx','exclude_russia','exclude_2021_date_anomaly']:
        threshold=float(name.removeprefix('threshold_')) if name.startswith('threshold_') else 3.
        a=lk if name=='core' or name.startswith('threshold_') else linked_variant(df,name)
        b=L.bounds_table(a,threshold)
        b['scenario']=name;b['threshold']=threshold
        b['origin_collision_rows']=int((L.eligible_origin(a,threshold)&(a.key_n_in_quarter>1)).sum())
        b['n_valid_pairs']=int(L.primary_outcome_rows(a,threshold).sum())
        sensitivities.append(b)
        if name not in ['core'] and not name.startswith('threshold_'):del a;gc.collect()
    write(pd.concat(sensitivities,ignore_index=True),'models/sensitivity_grid.csv')
    write(pd.concat(sensitivities,ignore_index=True),'tables/table_08_sensitivities.csv')
    reduced=linked_variant(df,'reduced_metadata_unique')
    old=lk[['source_row','source_row_next','core_reobserved']].rename(columns={'source_row_next':'legacy_target','core_reobserved':'legacy_reobserved'})
    compare=reduced.merge(old,on='source_row',validate='one_to_one')
    er=L.eligible_origin(compare)
    candidate=er&compare.core_reobserved
    identity_audit=pd.DataFrame([dict(scenario='reduced_metadata_unique',eligible=int(er.sum()),matched=int(candidate.sum()),newly_linked=int((candidate&~compare.legacy_reobserved).sum()),changed_target_among_legacy_matches=int((candidate&compare.legacy_reobserved&(compare.source_row_next!=compare.legacy_target)).sum()),ambiguous_origins=int((er&(compare.key_n_in_quarter>1)).sum()),interpretation='Exact metadata collapse is a sensitivity; unique linkage does not prove identity or exclude false merges; no links promoted')])
    write(identity_audit,'data/identity_collision_audit.csv')
    del reduced,compare;gc.collect()
    # MNAR pattern-mixture scenarios are assumptions, not recovered missing outcomes.
    mnar=[]
    for q,d in eligible.groupby('qidx'):
        obs=L.primary_outcome_rows(d)
        rate=float((d.loc[obs,'cost_next']>3).mean())
        if not np.isfinite(rate):continue
        rate=np.clip(rate,1e-6,1-1e-6)
        for delta in [-2,-1,0,1,2]:
            unknown_fail=1/(1+np.exp(-(np.log(rate/(1-rate))+delta)))
            observed_stay=int((obs&(d.cost_next<=3)).sum());unknown=int((~obs).sum())
            mnar.append(dict(origin_quarter=qlabel(q),delta_failure_logodds=delta,n_eligible=len(d),n_unknown=unknown,assumed_unknown_failure=unknown_fail,scenario_p_stay=(observed_stay+unknown*(1-unknown_fail))/len(d)))
    write(pd.DataFrame(mnar),'models/mnar_sensitivity.csv')
    # Cost-transition bins do not expose service/provider records.
    edges=[-np.inf,-3,-1,-.1,0,.1,1,3,np.inf]
    prim['delta_band']=pd.cut(prim.cost_next-prim.cost,edges).astype(str)
    trans=prim.groupby('delta_band').size().rename('n').reset_index()
    write(trans,'tables/supplementary_cost_transitions.csv')
    prim['margin_band']=pd.cut(3-prim.cost,[-.001,.05,.1,.5,1,2,3.001]).astype(str)
    margins=prim.groupby('margin_band').agg(n=('stay','size'),stay_rate=('stay','mean'),mean_next_cost=('cost_next','mean')).reset_index()
    write(margins,'tables/supplementary_threshold_margin.csv')
    # Broad descriptive targets retain denominators and no named provider summaries.
    groups=[]
    for field in ['source_region','destination_region','destination_income','access point__n','firm_type__n']:
        for label,d in eligible.groupby(field):
            if len(d)<30:continue
            b=L.bounds_table(d).iloc[0].to_dict();b.update(field=field,group=label)
            groups.append(b)
    write(pd.DataFrame(groups),'tables/supplementary_descriptive_groups.csv')
    e3=L.corridor_level(lk)
    e3['target_year']=(e3.qidx+1)//4
    c=e3.groupby('target_year').agg(n_origin_corridor_quarters=('cheap','size'),n_surveyed_next=('surveyed_next','sum'),n_cheap_next=('cheap_next',lambda v:(v==True).sum())).reset_index()
    c['conditional_p_cheap_next']=c.n_cheap_next/c.n_surveyed_next
    write(c,'tables/supplementary_corridor_estimand.csv')
    anomalies=dict(n_quotes=len(df),rows_outside_label_quarter=int(((df.collection_date.dt.year*4+df.collection_date.dt.quarter-1)!=df.qidx).sum()),kosovo_code_mismatch=int((df.corridor!=df.source_code+df.destination_code).sum()),normalised_providers=df['firm__n'].nunique(),corridors=df.corridor_key.nunique(),missing_2025q2=not (df.qidx==2025*4+1).any(),n_primary=len(prim),n_eligible=len(eligible),n_right_censored=int((sf.state=='right_censored_last_quarter').sum()),negative_origin_costs=int((df['cc1 total cost %']<0).sum()),transparent_no=int((df['transparent__n']!='yes').sum()))
    (OUT/'data/independent_audit_summary.json').write_text(json.dumps(anomalies,indent=2),encoding='utf-8')
    source=json.loads((OUT/'data/acquisition_log.jsonl').read_text(encoding='utf-8').splitlines()[0])
    source.update(license='CC BY 4.0; World Bank attribution/no endorsement; verified catalogue 2026-10-20',observation_start=str(df.collection_date.min()),observation_end=str(df.collection_date.max()),audit=anomalies)
    (OUT/'data/source_manifest.json').write_text(json.dumps(source,indent=2),encoding='utf-8')
    registry=[]
    for f in F.NUMERIC+F.CATEGORICAL:
        history=f.startswith(('h_','n_','reob_'))
        registry.append(dict(feature=f,input_source_wave='target <= origin - lag' if history else 'origin or earlier',known_after_date='UNVERIFIED',theoretical_availability_rule='entire source wave released before decision',retrospective='retained',prospective='rejected until availability verified',finding='no numeric lookahead under lag scenario; public availability unresolved'))
    write(pd.DataFrame(registry),'validation/feature_asof_registry.csv')
    # Private concentration and ambiguous-label sampling, never exported as quote rows.
    diag=eligible.groupby(['corridor_key','firm__n']).size().rename('n')
    diag.to_csv(PRIVATE/'private_corridor_provider_counts.csv')
    changed=lk[L.eligible_origin(lk)&lk.core_reobserved&~lk.strict_reobserved]
    changed.sample(min(30,len(changed)),random_state=20261020).to_parquet(PRIVATE/'manual_validation_sample.parquet',index=False)
    print(json.dumps(anomalies,indent=2),flush=True)

if __name__=='__main__':main()
