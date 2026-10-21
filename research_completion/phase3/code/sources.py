"""Bounded official/source verification. All reading copies stay private."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
import pandas as pd

ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'research_completion/phase3'
SOURCES=[
 ('rpw_current.xlsx','https://datacatalogfiles.worldbank.org/ddh-published/0037898/DR0095523/rpw_dataset_2011_2025_q3.xlsx','official known catalogue resource; no outcome inspection if hash differs'),
 ('lim_author.html','https://singapore.to/research/ssrn-6830281/','author catalogue alternate search; bibliographic page only'),
 ('lim_ssrn.html','https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6830281','full text access test; stop on denial'),
 ('rpw_resources.html','https://remittanceprices.worldbank.org/resources','official current resource inventory; latest listed Issue54'),
 ('rpw_catalogue.html','https://datacatalog.worldbank.org/search/dataset/0037898/remittance-prices-worldwide','official current metadata and resource listing'),
 ('fivefacts.pdf','https://eml.berkeley.edu/~enakamura/papers/fivefacts.pdf','lawful author-posted journal article'),
 ('losttransit.pdf','https://www.nber.org/system/files/working_papers/w15359/w15359.pdf','lawful working paper; stop on denial'),
]

def main():
    private=OUT/'private_runtime/sources';private.mkdir(parents=True,exist_ok=True)
    blocked=set();rows=[]
    for name,url,purpose in SOURCES:
        host=urllib.parse.urlsplit(url).netloc
        row=dict(source=name,url=url,access_utc=dt.datetime.now(dt.timezone.utc).isoformat(),purpose=purpose)
        if host in blocked:row.update(status='SKIPPED_HOST_DENIED');rows.append(row);continue
        target=private/name
        if target.exists():
            with target.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
            row.update(status='CACHED_PHASE3',sha256=digest,bytes=target.stat().st_size)
        else:
            try:
                req=urllib.request.Request(url,headers={'User-Agent':'R01-research-source-verification/1.0'})
                with urllib.request.urlopen(req,timeout=45) as response,target.open('wb') as f:
                    digest=hashlib.sha256();n=0
                    while chunk:=response.read(1024*1024):f.write(chunk);digest.update(chunk);n+=len(chunk)
                    row.update(status='FETCHED',http_status=response.status,sha256=digest.hexdigest(),bytes=n,last_modified=response.headers.get('Last-Modified'),content_type=response.headers.get('Content-Type'))
            except urllib.error.HTTPError as e:
                row.update(status='DENIED' if e.code in [401,403] else 'HTTP_ERROR',http_status=e.code,error=str(e))
                if e.code in [401,403]:blocked.add(host)
            except Exception as e:row.update(status='ACCESS_ERROR',error=type(e).__name__+': '+str(e))
        if name=='rpw_current.xlsx' and row.get('sha256'):
            row['matches_frozen_source']=row['sha256']=='f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8'
            row['actual_observations']='2011-2025Q3; post2016 37 waves; 2025Q2 absent' if row['matches_frozen_source'] else 'SEALED_UNINSPECTED_NEW_SOURCE'
        rows.append(row)
        if name.endswith('.pdf') and target.exists() and target.read_bytes()[:4]==b'%PDF':
            import fitz
            doc=fitz.open(target)
            target.with_suffix('.txt').write_text('\n'.join(f'\nPAGE {i+1}\n'+p.get_text() for i,p in enumerate(doc)),encoding='utf-8');doc.close()
    p=OUT/'timing';p.mkdir(exist_ok=True);pd.DataFrame(rows).to_csv(p/'source_acquisition.csv',index=False)
    print(json.dumps(rows,indent=2))

if __name__=='__main__':main()
