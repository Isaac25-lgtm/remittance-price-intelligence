"""Record a public-safe source/aggregate allowlist after file/schema review."""
import csv
import datetime as dt
import importlib.util
import json
import os
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_completion'
spec=importlib.util.spec_from_file_location('pack',ROOT/'scripts/build_publication_handoff.py');pack=importlib.util.module_from_spec(spec);spec.loader.exec_module(pack)

def main():
    files=[];csvrows=[]
    for base,dirs,names in os.walk(ROOT):
        dirs[:]=sorted(d for d in dirs if d not in pack.FORBIDDEN_PARTS and not d.endswith('.egg-info') and not (Path(base)/d).is_symlink())
        for name in sorted(names):
            p=Path(base)/name;rel=p.relative_to(ROOT).as_posix()
            if p.is_symlink() or rel in pack.OMIT or p.suffix=='.zip':continue
            if rel not in pack.ROOT_FILES and not rel.startswith(pack.PREFIXES):continue
            if p.suffix not in pack.ALLOWED_SUFFIXES and rel not in pack.ROOT_FILES:continue
            pack.inspect_public_file(p);files.append(rel)
            if p.suffix=='.csv':
                with p.open(encoding='utf-8-sig',newline='') as f:
                    reader=csv.reader(f);header=next(reader,[]);n=sum(1 for _ in reader)
                csvrows.append(dict(file=rel,n_aggregate_rows=n,columns=' | '.join(header)))
    path=OUT/'audits/public_artifact_allowlist.json'
    rel=path.relative_to(ROOT).as_posix()
    if rel not in files:files.append(rel)
    review=(OUT/'audits/public_csv_schema_review.csv').relative_to(ROOT).as_posix()
    if review not in files:files.append(review)
    contents=(OUT/'deliverables/handoff_contents.md').relative_to(ROOT).as_posix()
    if contents not in files:files.append(contents)
    with (ROOT/review).open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['file','n_aggregate_rows','columns']);writer.writeheader();writer.writerows(csvrows)
    obj=dict(reviewed_utc=dt.datetime.now(dt.timezone.utc).isoformat(),review='Agent file/source/schema review; not an external human privacy or ethics approval',basis=['Explicit source roots only; private/raw/processed caches pruned before enumeration','CSV schemas and export source reviewed; only broad categories/ISO corridors, no named provider cells','Original public literature/code referenced; source PDFs not redistributed','World Bank RPW Public CC BY4.0 attribution; no endorsement','Credential patterns, file types, size limits and forbidden row columns checked by packager'],paths=sorted(files))
    path.write_text(json.dumps(obj,indent=2),encoding='utf-8')
    counts=Counter(Path(p).suffix or '(no suffix)' for p in files)
    text='# Public handoff contents\n\nThe ZIP contains a frozen conditional research dossier plus safe source code and legacy aggregate results. No data/raw, private_runtime, quote records, provider names, predictions, model binaries, source PDFs or credentials.\n\n'
    text+=f'{len(files)} approved source files before archive aliases/manifests. File hashes are in reproducibility/file_hash_manifest.csv and deliverables/SHA256SUMS.txt; the ZIP hash is in zip_verification.json outside the immutable ZIP.\n\n'
    text+='START_HERE.md is at archive root. The scientific verdict, report, protocols, literature, aggregate models/tables/figures, audit and reproduction material remain under research_completion/. The exact approved paths are in audits/public_artifact_allowlist.json.\n\n'
    text+='\n'.join(f'- {ext}: {n} files' for ext,n in sorted(counts.items()))+'\n'
    (ROOT/contents).write_text(text,encoding='utf-8')
    print(json.dumps(dict(approved_files=len(files),extensions=counts,csv_files=len(csvrows),maximum_csv_rows=max(r['n_aggregate_rows'] for r in csvrows)),indent=2))

if __name__=='__main__':main()
