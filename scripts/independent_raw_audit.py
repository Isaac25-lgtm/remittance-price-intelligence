"""Separate streaming implementation of E1/E2 counts, independent of rpi linkage code.

This is a second implementation audit, not external peer review. Reads the official
workbook in read-only mode; exports only pooled counts and discrepancies.
"""
from collections import Counter,defaultdict
import hashlib
import json
import math
from pathlib import Path
import re
import unicodedata
import openpyxl
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def normal(x):
    if x is None:return ''
    s=unicodedata.normalize('NFKC',str(x)).casefold().strip()
    return re.sub(r'\s+',' ',re.sub(r'\s*,\s*',',',s))

def number(x):
    try:return float(x)
    except (TypeError,ValueError):return math.nan

def main():
    raw=ROOT/'data/raw/rpw_dataset_2011_2025_q3.xlsx'
    with raw.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
    assert digest=='f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8'
    wb=openpyxl.load_workbook(raw,read_only=True,data_only=True)
    it=wb['Dataset (from Q2 2016)'].iter_rows(values_only=True);header=next(it)
    ix={str(v):i for i,v in enumerate(header) if v is not None}
    waves=defaultdict(lambda:defaultdict(list));corridors=set();n=0
    attrs=['firm','payment instrument','access point','pickup method','pickup location']
    for row in it:
        if row[ix['period']] is None:continue
        year,quarter=re.fullmatch(r'(\d{4})_([1-4])Q',str(row[ix['period']]).strip()).groups()
        q=int(year)*4+int(quarter)-1
        corridor=str(row[ix['source_code']])+'>'+str(row[ix['destination_code']])
        key=(corridor,*(normal(row[ix[c]]) for c in attrs),number(row[ix['cc1 denomination amount']]))
        waves[q][key].append(number(row[ix['cc1 total cost %']]))
        corridors.add(corridor);n+=1
    wb.close();last=max(waves);flow=Counter();cheap=0
    for q,keys in waves.items():
        nextcorr={k[0] for k in waves.get(q+1,{})}
        for key,prices in keys.items():
            for price in prices:
                if not (0<=price<=3):continue
                cheap+=1
                if q==last:flow['right_censored_last_quarter']+=1;continue
                if len(prices)>1:flow['origin_key_ambiguous']+=1;continue
                if key[0] not in nextcorr:flow['corridor_not_surveyed_next_quarter']+=1;continue
                targets=waves[q+1].get(key,[])
                if len(targets)>1:flow['target_key_ambiguous']+=1
                elif not targets:flow['core_unobserved_corridor_surveyed']+=1
                elif not (targets[0]>=0):flow['reobserved_invalid_target']+=1
                elif targets[0]<=3:flow['observed_stay']+=1
                else:flow['observed_fail']+=1
    public=pd.read_csv(ROOT/'research_completion/data/inclusion_exclusion_flow.csv').groupby('state')['count'].sum().to_dict()
    mismatches={k:dict(independent=flow.get(k,0),pipeline=public.get(k,0)) for k in set(flow)|set(public) if flow.get(k,0)!=public.get(k,0)}
    result=dict(method='independently coded streaming Python dictionary; no rpi linkage imports',source_sha256=digest,n_quotes=n,n_corridors=len(corridors),n_cheap=cheap,n_eligible=cheap-flow['right_censored_last_quarter'],n_valid_pairs=flow['observed_stay']+flow['observed_fail'],flow=dict(flow),mismatches=mismatches,status='PASS' if not mismatches else 'FAIL',caveat='Implementation independence; same stated identity specification. Not external scientific peer review.')
    path=ROOT/'research_completion/audits/independent_raw_audit.json';path.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
    return bool(mismatches)

if __name__=='__main__':raise SystemExit(main())
