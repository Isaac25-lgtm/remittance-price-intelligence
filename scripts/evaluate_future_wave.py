"""Frozen future-wave gate/evaluator. Requires a genuinely new official source and clocks.

Usage: python scripts/evaluate_future_wave.py --workbook PRIVATE.xlsx --manifest PRIVATE.json
Manifest must declare sha256, official_url, frozen_protocol_sha, available_by, decision_date,
target_collection_start and prior_research_confirmed_unseen=true. No tuning occurs here.
An available_by date must cover ALL row-level predictors, not just an aggregate report.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np
import pandas as pd
from rpi import config,features as F,linkage as L
from rpi.acquire import sha256
from rpi.preprocess import read_raw_sheet,clean
from rpi.models import MODELS
from rpi.evaluate import metric_row

def timing_gate(manifest):
    required=['available_by','decision_date','target_collection_start']
    if not all(manifest.get(k) for k in required):raise ValueError('MISSING_INPUT: verified full-feature availability clocks required')
    dates=[dt.datetime.fromisoformat(manifest[k].replace('Z','+00:00')) for k in required]
    if not dates[0]<=dates[1]<dates[2]:raise ValueError('TIMING_FAIL: require available_by <= decision < target collection')
    if manifest.get('evidence_scope')!='all_row_level_predictors':raise ValueError('aggregate report is insufficient timing evidence')

def main():
    p=argparse.ArgumentParser();p.add_argument('--workbook',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True);a=p.parse_args()
    m=json.loads(a.manifest.read_text(encoding='utf-8'));timing_gate(m)
    frozen=m.get('frozen_protocol_sha')
    if not frozen:raise ValueError('frozen protocol commit is required')
    committed=subprocess.check_output(['git','show',f'{frozen}:configs/r01_phase2_publication.yaml'],text=True)
    current=(config.ROOT/'configs/r01_phase2_publication.yaml').read_text(encoding='utf-8')
    if committed.replace('\r\n','\n')!=current.replace('\r\n','\n'):raise ValueError('protocol differs from declared frozen commit')
    if not m.get('prior_research_confirmed_unseen'):raise ValueError('new to this runtime is not new to prior research')
    digest=sha256(a.workbook)
    if digest==config.EXPECTED_SHA256 or digest!=m['sha256']:raise ValueError('not an independently verified new vintage')
    if not m.get('official_url','').startswith('https://datacatalogfiles.worldbank.org/'):raise ValueError('official source provenance required')
    source=clean(read_raw_sheet(a.workbook))
    X=F.build(L.link_next_quarter(L.service_table(source)))
    prim=X[X.primary];test=prim[prim.target_qidx>2025*4+2]
    if test.empty:raise ValueError('CONFIRMATION_NOT_AVAILABLE: no exact-adjacent transition into a new target wave')
    test=test[test.target_qidx==test.target_qidx.min()]  # one new wave, no adaptive multiwave scoring
    actual_start=source.loc[source.qidx==test.target_qidx.min(),'collection_date'].min()
    decision=pd.Timestamp(m['decision_date'])
    if decision.tzinfo is not None:decision=decision.tz_convert('UTC').tz_localize(None)
    if pd.isna(actual_start) or decision>=actual_start:raise ValueError('decision does not precede actual target collection')
    train=prim[prim.target_qidx<test.qidx.min()]
    # Fixed families only; reporting benchmark, never score-driven selection on new labels.
    rows=[]
    for n in ['B2_history','L2_spline_logistic','M1_hist_gbm','M2_random_forest']:
        model=MODELS[n]().fit(train,train.y.astype(int))
        rows.append(dict(model=n,**metric_row(test.y.astype(int),model.predict_proba(test)[:,1])))
    out=Path(__file__).resolve().parents[1]/'research_completion/private_runtime/future_wave_metrics.json'
    out.write_text(json.dumps(dict(manifest=m,metrics=rows),indent=2),encoding='utf-8')
    print('PRIVATE evaluation saved; independent scientific review required before public release.')

if __name__=='__main__':main()
