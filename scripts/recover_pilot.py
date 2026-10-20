"""Rerun recovered archived pilot code, compare its original source and current cohort."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_completion';CODE=OUT/'protocols/legacy_pilot_code';PRIVATE=OUT/'private_runtime/pilot_reproduction'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prior-parquet',type=Path);ap.add_argument('--python',type=Path);a=ap.parse_args()
    source=ROOT/'data/processed/rpw_post2016.parquet'
    cached=PRIVATE/'lab/discovery_round3/data/rpw_post2016.parquet';cached.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,cached)
    old=pd.read_parquet(a.prior_parquet) if a.prior_parquet else None
    fresh=pd.read_parquet(source)
    differences=[]
    if old is not None:
        for col in ['id','period','corridor','firm','cc1 total cost %','cc1 lcu amount','payment instrument','access point','pickup method','pickup location']:
            if 'cost' in col or 'amount' in col or col=='id':
                x=pd.to_numeric(old[col],errors='coerce').to_numpy(float);y=pd.to_numeric(fresh[col],errors='coerce').to_numpy(float)
                mismatch=int((~np.isclose(x,y,equal_nan=True,rtol=0,atol=1e-12)).sum())
            else:
                x=old[col].fillna('').astype(str);y=fresh[col].fillna('').astype(str);mismatch=int((x.to_numpy()!=y.to_numpy()).sum())
            differences.append(dict(variable=col,n_mismatches=mismatch))
        pd.DataFrame(differences).to_csv(OUT/'audits/pilot_source_content_comparison.csv',index=False)
        if any(x['n_mismatches'] for x in differences):raise ValueError('pilot source content differs; do not claim same-source replication')
    py=str(a.python or Path(sys.base_prefix)/('python.exe' if os.name=='nt' else 'bin/python3'))
    for name in ['remittance_deep.py','remittance_spline_baseline.py','remittance_group_holdout.py']:
        p=subprocess.run([py,str(CODE/name)],cwd=ROOT)
        if p.returncode:return p.returncode
    results={}
    for name in ['model_result.json','spline_results.json','corridor_holdout_results.json','data_audit.json']:
        results[name]=json.loads((PRIVATE/'runs/N2'/name).read_text(encoding='utf-8'))
    results['source_code_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in CODE.glob('*.py')}
    results['input_processed_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    results['source_comparison']=differences;results['evidence_type']='REAL-DATA EXECUTION; unchanged archived pilot programs with private I/O adapter'
    results['python_runtime']=subprocess.check_output([py,'-c','import json,platform,numpy,pandas,sklearn;print(json.dumps(dict(python=platform.python_version(),numpy=numpy.__version__,pandas=pandas.__version__,sklearn=sklearn.__version__)))'],text=True).strip()
    oldpred=pd.read_parquet(PRIVATE/'runs/N2/spline_matched_predictions.parquet');newpred=pd.read_parquet(ROOT/'data/processed/test_predictions_lag0.parquet');newpred=newpred[newpred.target_year<=2024]
    # Row order/content comparison above validates original origin index -> Excel source row.
    oldset=set(oldpred.origin+2);newset=set(newpred.source_row)
    results['cohort_overlap']=dict(pilot_origin_years='2022-2024',phase1_target_years='2022-2024',pilot_n=len(oldset),phase1_n=len(newset),shared=len(oldset&newset),pilot_only=len(oldset-newset),phase1_only=len(newset-oldset),warning='Different calendar windows, transparency/source filters, local-amount vs USD-basket identity, text normalisation, features and model hyperparameters; the net18 difference is not a single-row cleaning discrepancy.')
    results['spline_brier_matches_reported']=abs(results['spline_results.json']['spline_brier']-.144145)<.000001
    results['gbm_brier_matches_reported']=abs(results['spline_results.json']['boost_brier']-.136037)<.000001
    (OUT/'audits/recovered_pilot_reproduction.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results['cohort_overlap'],indent=2));print(json.dumps(results['spline_results.json'],indent=2))
    return 0

if __name__=='__main__':raise SystemExit(main())
