"""Binned score decomposition, reliability uncertainty and full observed variable inventory."""
from pathlib import Path
import hashlib
import json
import pandas as pd
import numpy as np
from rpi import config
from rpi import linkage as L
from rpi.preprocess import RAW_COLUMNS,qlabel
from rpi.completion_stats import dependence_ci

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_completion';PRIVATE=OUT/'private_runtime/processed'

def decomposition(y,p):
    y=np.asarray(y,float);p=np.asarray(p,float)
    d=pd.DataFrame({'observed':y,'predicted':p});d['bin']=np.minimum((p*10).astype(int),9)
    g=d.groupby('bin').agg(n=('observed','size'),o=('observed','mean'),p=('predicted','mean'))
    w=g.n/len(d);mu=y.mean();unc=mu*(1-mu)
    rel=float((w*(g.p-g.o)**2).sum());res=float((w*(g.o-mu)**2).sum())
    binned=float(np.mean((d['bin'].map(g.p).to_numpy()-y)**2));raw=float(np.mean((p-y)**2))
    assert np.isclose(binned,unc-res+rel,atol=1e-12)
    return dict(raw_brier=raw,binned_brier=binned,reliability=rel,resolution=res,uncertainty=unc,binning_residual=raw-binned,method='fixed probability deciles; exact identity for binned predictor; continuous-score residual explicit')

def main():
    P=pd.read_parquet(PRIVATE/'phase2_predictions.parquet')
    names=[c for c in P if c.startswith(('B0_','B1_','B2_','B3_','B4_','L1_','L2_','M1_','M2_','S_selected'))]
    rows=[dict(model=n,**decomposition(P.y.astype(int),P[n])) for n in names]
    pd.DataFrame(rows).to_csv(OUT/'models/brier_decomposition.csv',index=False)
    rel=[]
    for name in ['B2_history','L2_spline_logistic','M1_hist_gbm','M2_random_forest','S_selected']:
        d=P.copy();d['bin']=np.minimum((d[name]*10).astype(int),9)
        for b,g in d.groupby('bin'):
            r=dict(model=name,probability_bin=b,n=len(g),observed_stay=float(g.y.astype(float).mean()),mean_pred=float(g[name].mean()),n_corridors=g.corridor_key.nunique(),method='fixed probability width0.1; conditional fixed predictions')
            if len(g)>=100 and g.corridor_key.nunique()>=10:
                ci=dependence_ci(g.y.astype(int).to_numpy(),g,'corridor',reps=300)
                r.update(ci95_lo=ci[0,0],ci95_hi=ci[1,0],status='ESTIMABLE')
            else:r['status']='NOT_ESTIMABLE_SUPPORT_GATE'
            rel.append(r)
    pd.DataFrame(rel).to_csv(OUT/'models/reliability_cluster_intervals.csv',index=False)
    # Explicitly retain all-unknown waves instead of silently skipping MNAR scenarios.
    linked=pd.read_parquet(PRIVATE/'linked_core.parquet');eligible=linked[L.eligible_origin(linked)]
    mnar=pd.read_csv(OUT/'models/mnar_sensitivity.csv');mnar['status']='ASSUMPTION_SCENARIO'
    missing=[]
    for q,g in eligible.groupby('qidx'):
        if qlabel(q) not in set(mnar.origin_quarter):
            for shift in [-2,-1,0,1,2]:missing.append(dict(origin_quarter=qlabel(q),delta_failure_logodds=shift,n_eligible=len(g),n_unknown=len(g),assumed_unknown_failure=np.nan,scenario_p_stay=np.nan,status='NOT_ESTIMABLE_NO_OBSERVED_SUCCESSORS'))
    pd.concat([mnar,pd.DataFrame(missing)],ignore_index=True).to_csv(OUT/'models/mnar_sensitivity.csv',index=False)
    dictionary=[]
    for col in RAW_COLUMNS:
        d=pd.read_parquet(config.CACHE_FILE,columns=[col,'qidx'])
        good=d[col].notna()&~d[col].astype(str).str.strip().isin(['','None','nan'])
        q=d.loc[good,'qidx']
        unit='text/category'
        if 'total cost' in col or 'fx margin' in col:unit='percentage points of transfer value'
        elif 'denomination amount' in col:unit='USD basket identifier'
        elif 'lcu amount' in col or 'lcu fee' in col:unit='sending local currency'
        elif 'rate' in col or col=='inter lcu bank fx':unit='exchange rate; see workbook Legend'
        elif col=='date':unit='collection date'
        elif col=='period':unit='survey-assigned calendar quarter'
        elif col=='id':unit='source identifier; not exported as quote records'
        dictionary.append(dict(variable=col,dtype=str(d[col].dtype),unit=unit,n_source=len(d),n_nonblank=int(good.sum()),n_distinct_nonblank=int(d.loc[good,col].nunique()),first_observed_wave=qlabel(int(q.min())) if len(q) else '',last_observed_wave=qlabel(int(q.max())) if len(q) else '',availability='collection clock observed; historical public availability UNVERIFIED'))
    pd.DataFrame(dictionary).to_csv(OUT/'data/variable_dictionary.csv',index=False)
    artifacts=[]
    for p in (OUT/'private_runtime/fit_models').glob('*.pkl'):
        artifacts.append(dict(file=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),distribution='PRIVATE; omitted from Git and ZIP',save_reload_max_tolerance=1e-12))
    (OUT/'models/fitted_artifact_manifest.json').write_text(json.dumps(dict(source_sha256=config.EXPECTED_SHA256,artifacts=artifacts),indent=2),encoding='utf-8')
    print('Score, reliability, variable and private-artifact metadata supplements complete')

if __name__=='__main__':main()
