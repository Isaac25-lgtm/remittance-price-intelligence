"""Deterministic, allowlisted public research handoff; no quote rows or model binaries."""
from __future__ import annotations
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path,PurePosixPath
import re
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research_completion'
ALLOWED_SUFFIXES={'.md','.csv','.json','.jsonl','.bib','.txt','.yaml','.yml','.toml','.py','.png','.svg'}
FORBIDDEN_COLUMNS={'source_row','source_row_next','id','firm','firm__n','key','provider','cost_next','y'}
FORBIDDEN_PARTS={'private_runtime','raw','processed','row_predictions','fit_models','provider_level_diagnostics','.git','.venv','__pycache__'}
ROOT_FILES={'README.md','AGENTS.md','CLAUDE.md','pyproject.toml','.python-version','.gitignore'}
PREFIXES=('src/','scripts/','tests/','configs/','docs/','results/','dashboard/','research_completion/','.github/workflows/','.streamlit/')
OMIT={'research_completion/reproducibility/file_hash_manifest.csv','research_completion/deliverables/SHA256SUMS.txt','research_completion/deliverables/zip_verification.json'}

def inspect_public_file(path):
    rel=path.relative_to(ROOT)
    if set(rel.parts)&FORBIDDEN_PARTS:raise ValueError(f'forbidden path: {rel}')
    if path.suffix.lower() not in ALLOWED_SUFFIXES and str(rel).replace('\\','/') not in ROOT_FILES:raise ValueError(f'forbidden type: {rel}')
    if path.stat().st_size>15_000_000:raise ValueError(f'oversize public file: {rel}')
    if path.suffix=='.csv':
        with path.open(encoding='utf-8-sig',newline='') as f:
            reader=csv.reader(f);columns=set(next(reader,[]))
        if columns&FORBIDDEN_COLUMNS:raise ValueError(f'row/provider identifiers in CSV: {rel}')
    if path.suffix in {'.md','.py','.json','.jsonl','.txt','.yaml','.yml','.toml'}:
        text=path.read_text(encoding='utf-8')
        if re.search(r'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',text):
            raise ValueError(f'credential-like content: {rel}')


def public_bytes(path):
    data=path.read_bytes()
    if path.suffix.lower()=='.png':return data
    # Match Git's canonical text content across Windows CRLF/Linux LF checkouts.
    return data.decode('utf-8').replace('\r\n','\n').replace('\r','\n').encode('utf-8')

def payload():
    approved=ROOT/'research_completion/audits/public_artifact_allowlist.json'
    if not approved.exists():raise ValueError('missing reviewed explicit public artifact allowlist')
    allowed=set(json.loads(approved.read_text(encoding='utf-8'))['paths'])
    files=[]
    candidates=[]
    for base,dirs,names in os.walk(ROOT):
        dirs[:]=sorted(d for d in dirs if d not in FORBIDDEN_PARTS and not d.endswith('.egg-info') and not (Path(base)/d).is_symlink())
        candidates.extend(Path(base)/n for n in names)
    for p in sorted(candidates):
        if not p.is_file() or p.is_symlink():continue
        rel=p.relative_to(ROOT);name=rel.as_posix()
        if set(rel.parts)&FORBIDDEN_PARTS or name in OMIT or p.suffix=='.zip':continue
        if name not in ROOT_FILES and not name.startswith(PREFIXES):continue
        if p.suffix.lower() not in ALLOWED_SUFFIXES and name not in ROOT_FILES:continue
        if name.endswith('/zip_verification.json'):continue
        if name not in allowed:raise ValueError(f'file not explicitly approved: {name}')
        inspect_public_file(p);files.append(p)
    return files

def audit_zip(path):
    with zipfile.ZipFile(path) as z:
        if z.testzip():raise ValueError('corrupt ZIP member')
        names=set(z.namelist())
        if 'START_HERE.md' not in names:raise ValueError('missing START_HERE')
        for name in names:
            parts=PurePosixPath(name).parts
            if '..' in parts or set(parts)&FORBIDDEN_PARTS or '\\' in name or PurePosixPath(name).is_absolute():raise ValueError('unsafe archive path')
            if PurePosixPath(name).suffix not in ALLOWED_SUFFIXES and name not in ROOT_FILES:raise ValueError('forbidden archive type')
            if name.endswith('.csv'):
                header=set(next(csv.reader(io.StringIO(z.read(name).decode('utf-8-sig'))),[]))
                if header&FORBIDDEN_COLUMNS:raise ValueError('forbidden archive identifiers')
        sums=z.read('research_completion/deliverables/SHA256SUMS.txt').decode()
        checked=0
        for line in sums.splitlines():
            digest,name=line.split('  ',1)
            if hashlib.sha256(z.read(name)).hexdigest()!=digest:raise ValueError('member hash mismatch: '+name)
            checked+=1
        start=z.read('START_HERE.md').decode()
        for link in re.findall(r'\]\(([^)]+)\)',start):
            if '://' not in link and link.split('#')[0] not in names:raise ValueError('broken start link: '+link)
        return dict(status='PASS',members=len(names),member_hashes_verified=checked,start_links='PASS',forbidden_paths='PASS')

def build():
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    dirty_before=subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip()
    files=payload();mapped={p.relative_to(ROOT).as_posix():public_bytes(p) for p in files}
    start='research_completion/deliverables/START_HERE.md'
    if start not in mapped:raise ValueError('create verified START_HERE content first')
    mapped['START_HERE.md']=mapped.pop(start).decode('utf-8').replace('](../../README.md)','](README.md)').replace('](../','](research_completion/').encode('utf-8')
    rows=[]
    for name,data in sorted(mapped.items()):rows.append(dict(archive_path=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
    buf=io.StringIO();w=csv.DictWriter(buf,fieldnames=['archive_path','bytes','sha256'],lineterminator='\n');w.writeheader();w.writerows(rows)
    manifest=buf.getvalue().encode();mp='research_completion/reproducibility/file_hash_manifest.csv';mapped[mp]=manifest
    (ROOT/mp).write_bytes(manifest)
    sums='\n'.join(hashlib.sha256(data).hexdigest()+'  '+name for name,data in sorted(mapped.items()))+'\n'
    sp='research_completion/deliverables/SHA256SUMS.txt';mapped[sp]=sums.encode();(ROOT/sp).write_bytes(sums.encode())
    # Investigator's Africa/Kampala calendar date (UTC+3, no DST).
    date=dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).strftime('%Y%m%d')
    path=OUT/'deliverables'/f'REMITTANCE_R01_PUBLICATION_HANDOFF_{date}_{sha[:7]}.zip'
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(mapped.items()):
            info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,data)
    result=audit_zip(path)
    result.update(source_commit=sha,source_tree_dirty_at_start=bool(dirty_before),built_utc=dt.datetime.now(dt.timezone.utc).isoformat(),zip=path.relative_to(ROOT).as_posix(),zip_bytes=path.stat().st_size,zip_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    (OUT/'deliverables/zip_verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2));return path

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--audit',type=Path);a=ap.parse_args()
    if a.audit:print(json.dumps(audit_zip(a.audit),indent=2))
    else:build()
