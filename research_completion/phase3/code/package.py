"""Deterministic additive Phase3 ZIP, explicit public allowlists and read-back checks."""
import argparse
import csv
import datetime as dt
import hashlib
import importlib.util
import io
import json
from pathlib import Path,PurePosixPath
import re
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'research_completion/phase3'
spec=importlib.util.spec_from_file_location('old_public_package',ROOT/'scripts/build_publication_handoff.py')
safe=importlib.util.module_from_spec(spec);spec.loader.exec_module(safe)
OMIT={'research_completion/phase3/deliverables/zip_verification.json','research_completion/phase3/deliverables/integration.json','research_completion/phase3/deliverables/SHA256SUMS.txt','research_completion/phase3/deliverables/file_manifest.csv'}

def sha(data):return hashlib.sha256(data).hexdigest()

def audit(path):
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        names=z.namelist();assert len(names)==len(set(names))
        assert 'START_HERE_PHASE3.md' in names
        for name in names:
            p=PurePosixPath(name)
            assert not p.is_absolute() and '..' not in p.parts and '\\' not in name
            assert not set(p.parts)&safe.FORBIDDEN_PARTS
            assert p.suffix.lower() in safe.ALLOWED_SUFFIXES or name in safe.ROOT_FILES
            if p.suffix=='.csv':
                cols=set(next(csv.reader(io.StringIO(z.read(name).decode('utf-8-sig'))),[]))
                assert not cols&safe.FORBIDDEN_COLUMNS
        sums=z.read('research_completion/phase3/deliverables/SHA256SUMS.txt').decode()
        count=0
        for line in sums.splitlines():
            h,name=line.split('  ',1);assert sha(z.read(name))==h;count+=1
        assert count==len(names)-1
        for p in [PurePosixPath('START_HERE_PHASE3.md'),PurePosixPath('research_completion/phase3/START_HERE_PHASE3.md')]:
            text=z.read(str(p)).decode()
            for link in re.findall(r'\]\(([^)]+)\)',text):
                if '://' in link or not link.split('#')[0]:continue
                target=p.parent/link.split('#')[0]
                assert target.as_posix() in names,(str(p),str(target))
    return dict(status='PASS',members=len(names),member_hashes_verified=count,relative_entry_links='PASS',forbidden_paths_and_columns='PASS')

def build():
    (OUT/'deliverables').mkdir(exist_ok=True)
    paths=set(json.loads((ROOT/'research_completion/audits/public_artifact_allowlist.json').read_text())['paths'])
    paths.update(json.loads((OUT/'assessment/public_artifact_allowlist.json').read_text())['paths'])
    mapped={}
    for name in sorted(paths):
        if name in OMIT:continue
        p=ROOT/name
        if not p.is_file() or p.suffix=='.zip' or name.endswith('/zip_verification.json'):continue
        safe.inspect_public_file(p);mapped[name]=safe.public_bytes(p)
    # Entry is an alias; preserve original paths for every other relative link.
    start=mapped['research_completion/phase3/START_HERE_PHASE3.md'].decode()
    start=re.sub(r'\]\((?!https?://)([^)]+)\)',lambda m:'](research_completion/phase3/'+m.group(1)+')',start)
    mapped['START_HERE_PHASE3.md']=start.encode()
    rows=[dict(archive_path=n,bytes=len(b),sha256=sha(b)) for n,b in sorted(mapped.items())]
    buf=io.StringIO();writer=csv.DictWriter(buf,fieldnames=['archive_path','bytes','sha256'],lineterminator='\n');writer.writeheader();writer.writerows(rows)
    manifest=buf.getvalue().encode();mp='research_completion/phase3/deliverables/file_manifest.csv';mapped[mp]=manifest;(ROOT/mp).write_bytes(manifest)
    sums=''.join(sha(data)+'  '+name+'\n' for name,data in sorted(mapped.items())).encode()
    sp='research_completion/phase3/deliverables/SHA256SUMS.txt';mapped[sp]=sums;(ROOT/sp).write_bytes(sums)
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    day=dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).strftime('%Y%m%d')
    path=OUT/'deliverables'/f'REMITTANCE_R01_PHASE3_PUBLICATION_HANDOFF_{day}_{commit[:7]}.zip'
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(mapped.items()):
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,data)
    result=audit(path);result.update(source_commit=commit,zip=str(path.relative_to(ROOT)).replace('\\','/'),zip_sha256=sha(path.read_bytes()),zip_bytes=path.stat().st_size,utc=dt.datetime.now(dt.timezone.utc).isoformat(),source_tree_dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip()))
    (OUT/'deliverables/zip_verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2));return path

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--audit',type=Path);args=parser.parse_args()
    if args.audit:print(json.dumps(audit(args.audit),indent=2))
    else:build()
