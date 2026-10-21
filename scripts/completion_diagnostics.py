"""Additional actual-data diagnostics and public-safe identity validation disposition."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from rpi import linkage as L
from rpi.preprocess import load_clean
from completion_data import PRIVATE,OUT,linked_variant,write

def main():
    df=load_clean();lk=pd.read_parquet(PRIVATE/'linked_core.parquet')
    reduced=linked_variant(df,'reduced_metadata_unique')
    old=lk[['source_row','source_row_next','core_reobserved']].rename(columns={'source_row_next':'legacy_target','core_reobserved':'legacy_reobserved'})
    c=reduced.merge(old,on='source_row',validate='one_to_one');e=L.eligible_origin(c);matched=e&c.core_reobserved
    write(pd.DataFrame([dict(scenario='reduced_metadata_unique',eligible=int(e.sum()),matched=int(matched.sum()),newly_linked=int((matched&~c.legacy_reobserved).sum()),changed_target_among_legacy_matches=int((matched&c.legacy_reobserved&(c.source_row_next!=c.legacy_target)).sum()),ambiguous_origins=int((e&(c.key_n_in_quarter>1)).sum()),interpretation='Unique reduced-key matches are not proof against false merges; none promoted')]),'data/identity_collision_audit.csv')
    comp=lk[L.primary_outcome_rows(lk)].copy()
    targets=lk[['source_row','fee_pct','fx_margin']].rename(columns={'source_row':'source_row_next','fee_pct':'fee_next','fx_margin':'fx_next'})
    comp=comp.merge(targets,on='source_row_next',validate='many_to_one')
    comp['endpoint']=np.where(comp.cost_next<=3,'observed_stay','observed_fail')
    comp['fee_delta']=comp.fee_next-comp.fee_pct;comp['fx_delta']=comp.fx_next-comp.fx_margin;comp['total_delta']=comp.cost_next-comp.cost
    write(comp.groupby('endpoint').agg(n=('cost','size'),mean_fee_delta=('fee_delta','mean'),mean_fx_delta=('fx_delta','mean'),mean_total_delta=('total_delta','mean'),median_total_delta=('total_delta','median')).reset_index(),'tables/supplementary_fee_fx_changes.csv')
    # Observation-selection distributions, no provider-specific cells.
    e=lk[L.eligible_origin(lk)].copy();e['observed_valid']=L.primary_outcome_rows(e)
    summaries=[]
    for field in ['destination_region','firm_type__n','access point__n']:
        g=e.groupby([field,'observed_valid']).agg(n=('cost','size'),mean_origin_cost=('cost','mean'),median_origin_cost=('cost','median')).reset_index().rename(columns={field:'group'})
        g['field']=field;summaries.append(g[g.n>=30])
    write(pd.concat(summaries,ignore_index=True),'data/observation_selection_profile.csv')
    concentration=[]
    for q,d in df.groupby('qidx'):
        v=d.groupby('firm__n').size().sort_values(ascending=False)
        concentration.append(dict(qidx=q,n_providers=len(v),largest_label_quote_share=float(v.iloc[0]/v.sum()),top5_label_quote_share=float(v.iloc[:5].sum()/v.sum()),quote_label_hhi=float(((v/v.sum())**2).sum()),interpretation='survey-record concentration; not transaction market share'))
    write(pd.DataFrame(concentration),'data/survey_label_concentration.csv')
    strata={'speed_changed':lk.core_reobserved&(lk['speed actual__n']!=lk.speed_next),'coverage_changed':lk.core_reobserved&(lk['receiving network coverage__n']!=lk.coverage_next),'ambiguous_origin':lk.status=='origin_key_ambiguous'}
    selected=[];dispositions=[]
    for name,mask in strata.items():
        d=lk[mask].sample(min(10,int(mask.sum())),random_state=20261020)
        selected.append(d.assign(adjudication_stratum=name))
        dispositions.append(dict(stratum=name,n_sampled=len(d),public_historical_bundle_confirmation=0,links_promoted=0,status='UNRESOLVED',reason='public historical service-level metadata not established; label difference alone cannot verify same economic bundle'))
    pd.concat(selected,ignore_index=True).to_parquet(PRIVATE/'stratified_identity_adjudication_sample.parquet',index=False)
    write(pd.DataFrame(dispositions),'data/manual_identity_validation_disposition.csv')
    print('Additional diagnostics and identity audit complete',flush=True)

if __name__=='__main__':main()
