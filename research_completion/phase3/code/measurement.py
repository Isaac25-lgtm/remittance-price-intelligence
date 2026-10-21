"""Independent raw-workbook measurement audit: no rpi or model/report imports.

Private cache stores original fields for blinded human review, never exported.
All public results are counts/rates grouped over waves or broad strata.
"""
from collections import Counter, defaultdict
import csv
import gc
import hashlib
import json
import math
from pathlib import Path
import pickle
import random
import re
import sys
import unicodedata
import numpy as np
import openpyxl
import pandas as pd
from scipy.stats import t as student_t

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'research_completion/phase3'
PRIVATE=OUT/'private_runtime'
EXPECTED='f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8'
FIELDS=['firm','payment instrument','access point','pickup method','pickup location']

def norm(value):
    if value is None: return ''
    return sys.intern(re.sub(r'\s+',' ',re.sub(r'\s*,\s*',',',unicodedata.normalize('NFKC',str(value)).casefold().strip())))

def number(value):
    try:return float(value)
    except (ValueError,TypeError):return math.nan

def write(rows,path):
    p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(p,index=False)

def load_source():
    raw=ROOT/'data/raw/rpw_dataset_2011_2025_q3.xlsx'
    with raw.open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
    assert digest==EXPECTED
    cache=PRIVATE/'independent_source.pkl'
    if cache.exists():
        value=pickle.loads(cache.read_bytes())
        assert value['source_sha256']==digest
        return value['records']
    wb=openpyxl.load_workbook(raw,read_only=True,data_only=True)
    it=wb['Dataset (from Q2 2016)'].iter_rows(values_only=True)
    ix={v:i for i,v in enumerate(next(it)) if v is not None}
    records=[]
    for rownum,row in enumerate(it,2):
        if row[ix['period']] is None:continue
        y,q=map(int,re.fullmatch(r'(\d{4})_([1-4])Q',str(row[ix['period']]).strip()).groups())
        corr=sys.intern(str(row[ix['source_code']])+'>'+str(row[ix['destination_code']]))
        original=tuple(sys.intern('' if row[ix[c]] is None else str(row[ix[c]])) for c in FIELDS+['speed actual','receiving network coverage'])
        key=(corr,*(norm(x) for x in original[:5]))
        rec=(y*4+q-1,key,norm(original[5]),norm(original[6]),
             number(row[ix['cc1 total cost %']]),number(row[ix['cc2 total cost %']]),
             number(row[ix['cc1 denomination amount']]),number(row[ix['cc2 denomination amount']]),
             norm(row[ix['destination_region']]),norm(row[ix['firm_type']]),rownum,original)
        records.append(rec)
    wb.close()
    PRIVATE.mkdir(parents=True,exist_ok=True)
    cache.write_bytes(pickle.dumps(dict(source_sha256=digest,records=records),protocol=5))
    print(json.dumps(dict(raw_quotes=len(records),raw_sha256=digest,private_cache_created=True)),flush=True)
    return records

def construct(records,basket=0,threshold=3,strict=False):
    """Explicit state precedence matches the frozen definition; absent wave never bridged."""
    waves=defaultdict(lambda:defaultdict(list))
    surveyed=set()
    for i,r in enumerate(records):
        waves[r[0]][r[1]+(r[6+basket],)].append(i)
        surveyed.add((r[0],r[1][0]))
    last=max(waves);rows=[];censored=0;review=[]
    for q,keys in sorted(waves.items()):
        for key,indices in keys.items():
            for i in indices:
                r=records[i];price=r[4+basket]
                if not 0<=price<=threshold:continue
                if q==last:censored+=1;continue
                target=waves.get(q+1,{}).get(key,[])
                chosen=None;changed=False;valid=False;unique=False
                if len(indices)>1:state='origin_key_ambiguous'
                elif (q+1,key[0]) not in surveyed:state='corridor_not_surveyed'
                elif len(target)>1:state='target_key_ambiguous'
                elif not target:state='service_not_observed'
                else:
                    chosen=records[target[0]];unique=True
                    changed=(r[2:4]!=chosen[2:4])
                    if strict and changed:state='strict_attributes_changed';unique=False
                    elif not math.isfinite(chosen[4+basket]) or chosen[4+basket]<0:state='invalid_target_cost'
                    else:
                        valid=True
                        state='stay' if chosen[4+basket]<=threshold else 'fail'
                rows.append((q,key[0],key[1],r[8],r[9],state,int(unique),int(valid),int(changed),i))
                if basket==0 and threshold==3 and not strict:
                    if state in ['origin_key_ambiguous','target_key_ambiguous']:stratum='ambiguous'
                    elif state=='service_not_observed':
                        # Candidate drift: same corridor/provider/payment with changed remaining metadata.
                        candidates=[k for k in waves.get(q+1,{}) if k[:3]==key[:3]]
                        stratum='potential_metadata_drift' if candidates else 'nonmatch'
                    elif unique:stratum='changed_attributes' if changed else 'unchanged_match'
                    else:stratum=None
                    alternatives=[]
                    if stratum=='potential_metadata_drift':
                        alternatives=[j for k in candidates[:3] for j in waves[q+1][k]][:3]
                    if stratum:review.append((stratum,i,target,alternatives))
    d=pd.DataFrame(rows,columns=['qidx','corridor_group','provider_group','region','provider_type','state','unique','valid','changed','private_index'])
    d['stay']=(d.state=='stay').astype(int);d['fail']=(d.state=='fail').astype(int);d['unknown']=1-d['valid']
    cq={}
    for q,keys in waves.items():
        for key,indices in keys.items():
            ck=(q,key[0]);cq[ck]=cq.get(ck,False) or any(0<=records[i][4+basket]<=threshold for i in indices)
    e3=[]
    for (q,c),cheap in cq.items():
        if cheap and q<last:
            seen=(q+1,c) in cq
            e3.append(dict(qidx=q,surveyed=int(seen),cheap_next=int(cq.get((q+1,c),False))))
    return d,pd.DataFrame(e3),censored,review

def estimate(d,label):
    n=len(d);s=int(d.stay.sum());f=int(d.fail.sum());u=n-s-f
    return dict(scenario=label,n_eligible=n,n_valid=s+f,n_stay=s,n_fail=f,n_unknown=u,
                conditional=s/(s+f) if s+f else math.nan,lower=s/n,upper=(s+u)/n,
                unknown_share=u/n,e4_unique=d.unique.mean(),e4_valid=d.valid.mean())

def hac_ratio(wave,num,den,lag):
    n=wave[num].to_numpy(float);d=wave[den].to_numpy(float);T=len(n);p=n.sum()/d.sum()
    influence=(n-p*d)/d.mean()
    v=float(influence@influence/T)
    for k in range(1,min(lag,T-1)+1):v+=2*(1-k/(lag+1))*float(influence[k:]@influence[:-k]/T)
    se=math.sqrt(max(v,0)/T)
    delta=student_t.ppf(.975,T-1)*se
    return p,max(0,p-delta),min(1,p+delta),se

def main():
    records=load_source();scenarios=[];wave_outputs=[];strata=[];primary=[];checks=[]
    n_quotes=len(records);assert n_quotes==204469
    for basket in [0,1]:
        for threshold in [3,5]:
            core=None
            for strict in [False,True]:
                label=f'cc{basket+1}_{threshold}pct_'+('strict' if strict else 'core')
                d,e3,censored,review=construct(records,basket,threshold,strict)
                est=estimate(d,label);est['right_censored']=censored;scenarios.append(est)
                wave=d.groupby('qidx').agg(n=('stay','size'),s=('stay','sum'),f=('fail','sum'),u=('unknown','sum'),valid=('valid','sum'),unique=('unique','sum')).reset_index()
                wave['conditional']=wave.s/wave.valid;wave['lower']=wave.s/wave.n;wave['upper']=(wave.s+wave.u)/wave.n
                wave['width']=wave.u/wave.n;wave['scenario']=label
                wave['quarter']=wave.qidx.map(lambda q:f'{q//4}Q{q%4+1}')
                wave_outputs.append(wave)
                for metric,num,den in [('E1','s','valid'),('E2_lower','s','n'),('E2_upper','upper_count','n'),('E2_width','u','n'),('E4_unique','unique','n'),('E4_valid','valid','n')]:
                    wave['upper_count']=wave.s+wave.u
                    for lag in [0,1,4]:
                        p,lo,hi,se=hac_ratio(wave,num,den,lag)
                        primary.append(dict(scenario=label,estimand=metric,estimate=p,sensitivity_lower=lo,sensitivity_upper=hi,se=se,hac_lag=lag,n_origin_waves=len(wave),nonzero_denominator_waves=int((wave[den]>0).sum()),inference_status='ASSUMPTION_DEPENDENT_HAC_NOT_COVERAGE_VALIDATED'))
                scenarios.append(dict(scenario=label+'_E3',n_eligible=len(e3),n_valid=int(e3.surveyed.sum()),n_stay=int(e3.cheap_next.sum()),conditional=e3.cheap_next.sum()/e3.surveyed.sum()))
                if basket==0 and threshold==3:
                    for field in ['region','provider_type']:
                        for group,g in d.groupby(field):
                            if len(g)>=30:strata.append(dict(stratum_field=field,stratum=group,**estimate(g,label)))
                    for group,g in [('pre_2022Q3',d[d.qidx<2022*4+2]),('post_2022Q3',d[d.qidx>=2022*4+2]),('exclude_Russia',d[~d.corridor_group.str.startswith('RUS>')])]:
                        strata.append(dict(stratum_field='fixed_sensitivity',stratum=group,**estimate(g,label)))
                    for field in ['corridor_group','provider_group']:
                        largest=d.groupby(field).size().idxmax()
                        strata.append(dict(stratum_field='dominance',stratum='exclude_largest_'+field,**estimate(d[d[field]!=largest],label)))
                        groupstats=d.groupby(field).agg(n=('stay','size'),s=('stay','sum'),v=('valid','sum'),u=('unknown','sum'))
                        strata.append(dict(stratum_field='weighting',stratum='equal_'+field,scenario=label,n_eligible=len(d),conditional=(groupstats.s/groupstats.v.replace(0,np.nan)).mean(),lower=(groupstats.s/groupstats.n).mean(),upper=((groupstats.s+groupstats.u)/groupstats.n).mean()))
                    if not strict:
                        core=d;make_review(records,review)
                        flow=d.groupby('state').size().rename('count').reset_index();write(flow,'tables/unknown_flow.csv')
                        write(e3.groupby('qidx').sum().reset_index(),'tables/corridor_monitoring.csv')
                        write([dict(source_sha256=EXPECTED,n_quotes=n_quotes,n_observed_waves=len({r[0] for r in records}),n_eligible=len(d),raw_parser='openpyxl stream and independent tuple dictionary',imports_primary_pipeline=False)],'tables/source_audit.csv')
                    else:
                        merged=core[['private_index','state']].merge(d[['private_index','state']],on='private_index',suffixes=('_core','_strict'),validate='one_to_one')
                        write(merged.groupby(['state_core','state_strict']).size().rename('n').reset_index(),'tables/core_strict_transition.csv')
                del d;gc.collect()
    write(scenarios,'identity/LINKAGE_SCENARIO_RESULTS.csv');write(pd.concat(wave_outputs),'tables/wave_measurement.csv')
    write(primary,'inference/PRIMARY_CLAIM_ESTIMATES.csv');write(strata,'tables/measurement_sensitivities.csv')
    frozen=pd.read_csv(ROOT/'research_completion/models/sensitivity_grid.csv')
    for label,oldlabel in [('cc1_3pct_core','core'),('cc1_3pct_strict','strict'),('cc1_5pct_core','threshold_5'),('cc2_3pct_core','cc2')]:
        new=next(x for x in scenarios if x['scenario']==label);old=frozen[frozen.scenario==oldlabel].iloc[0]
        for key,prior in [('n_eligible','n_eligible'),('n_valid','n_valid_pairs'),('n_stay','n_stay'),('n_fail','n_fail'),('n_unknown','n_unknown')]:
            checks.append(dict(scenario=label,field=key,independent=new[key],phase2=int(old[prior]),pass_check=new[key]==int(old[prior])))
    write(checks,'assessment/independent_count_comparison.csv')
    assert all(x['pass_check'] for x in checks)
    print(json.dumps(dict(status='PASS',count_checks=len(checks),scenarios=scenarios[:4]),indent=2),flush=True)

def make_review(records,candidates):
    rng=random.Random(20261021);groups=defaultdict(list)
    for c in candidates:groups[c[0]].append(c)
    private=[];selection=[]
    for stratum,values in sorted(groups.items()):
        chosen=rng.sample(values,min(12,len(values)))
        selection.append(dict(stratum=stratum,eligible_cases=len(values),sampled=len(chosen),seed=20261021,externally_adjudicated=0))
        for _,i,targets,alternatives in chosen:
            r=records[i];target=records[targets[0]] if len(targets)==1 else None
            case_id=f'R01P3-{len(private)+1:03}'
            row=dict(case_id=case_id,origin_quarter=f'{r[0]//4}Q{r[0]%4+1}',corridor=r[1][0],origin_source_row=r[10],target_source_rows=';'.join(str(records[t][10]) for t in targets),target_multiplicity=len(targets))
            for j,field in enumerate(FIELDS+['speed actual','receiving network coverage']):
                row['origin_'+field]=r[11][j];row['target_'+field]=target[11][j] if target else ''
            row.update(human_identity_decision='',supporting_document='',reviewer='',review_date='',reason='')
            row['_private_stratum']=stratum
            for a,j in enumerate(alternatives,1):
                candidate=records[j]
                row[f'alternative_{a}_source_row']=candidate[10]
                for k,field in enumerate(FIELDS+['speed actual','receiving network coverage']):row[f'alternative_{a}_'+field]=candidate[11][k]
            private.append(row)
    PRIVATE.mkdir(parents=True,exist_ok=True)
    # Shuffle case order and replace sequential IDs so stratum/order is blinded.
    rng.shuffle(private)
    review_key=[]
    for i,r in enumerate(private):
        r['case_id']=f'R01P3-{i+1:03}'
        review_key.append(dict(case_id=r['case_id'],stratum=r.pop('_private_stratum')))
    pd.DataFrame(private).to_csv(PRIVATE/'BLINDED_IDENTITY_REVIEW.csv',index=False)
    pd.DataFrame(review_key).to_csv(PRIVATE/'IDENTITY_REVIEW_KEY.csv',index=False)
    write(selection,'identity/review_sample_design.csv')
    template=OUT/'identity/PRIVATE_REVIEW_TEMPLATE.csv';template.parent.mkdir(parents=True,exist_ok=True)
    with template.open('w',newline='',encoding='utf-8') as f:csv.writer(f).writerow(['case_id','human_identity_decision','supporting_document','reviewer','review_date','reason'])

if __name__=='__main__':main()
