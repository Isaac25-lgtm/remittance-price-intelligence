"""Rebuild the original string cache directly from the verified workbook.

Run with the recorded pilot pandas/pyarrow versions. Keeps openpyxl blank-string versus
missing-cell distinctions; pandas.read_excel's default NA conversion collapses them.
"""
from pathlib import Path
import argparse
import hashlib
import json
import openpyxl
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    raw=ROOT/'data/raw/rpw_dataset_2011_2025_q3.xlsx'
    with raw.open('rb') as f:source_hash=hashlib.file_digest(f,'sha256').hexdigest()
    assert source_hash=='f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8'
    dest=a.output.resolve();private=(ROOT/'research_completion/private_runtime').resolve()
    if not dest.is_relative_to(private):raise ValueError('cache output must stay private')
    wb=openpyxl.load_workbook(raw,read_only=True,data_only=True)
    it=wb['Dataset (from Q2 2016)'].iter_rows(values_only=True)
    headers=[str(x).strip() if x is not None else '' for x in next(it)]
    keep=[i for i,h in enumerate(headers) if h and h not in ['note1','note2']]
    data=[[r[i] for i in keep] for r in it if r[0] is not None];wb.close()
    d=pd.DataFrame(data,columns=[headers[i] for i in keep]).astype('string')
    dest.parent.mkdir(parents=True,exist_ok=True);d.to_parquet(dest,index=False)
    with dest.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
    result=dict(source_sha256=source_hash,cache_sha256=digest,n_rows=len(d),n_columns=len(d.columns),matches_original_cache_sha256=digest=='d371c8b2e09b3f7698803dbfc20b85550f6206e4d30a4974b7a6051060c3493f',method='unchanged original openpyxl rows -> pandas string -> parquet; no quote rows distributed')
    (ROOT/'research_completion/audits/pilot_cache_rebuild.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
