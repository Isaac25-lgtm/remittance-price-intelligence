"""Explicit public allowlist; immutable prior archives; separate local-only evidence."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PRIVATE=ROOT/'research_completion/phase3/private_runtime/followup_20261021/autonomous_review'
BASE=HERE.parent/'deliverables/REMITTANCE_R01_PHASE3_FOLLOWUP_HANDOFF_20261021.zip'
BASE_SHA='6a7b7d0cfd837634ce3cda1906ab55c55c9804a1cd928dc4d9cca0682021c4fe'
PUBLIC_NAME='REMITTANCE_R01_AUTONOMOUS_PUBLIC_HANDOFF_20261021.zip'
PRIVATE_NAME='REMITTANCE_R01_AUTONOMOUS_EVIDENCE_LOCAL_ONLY_20261021.zip'
PUBLIC_FILES=[
 'README.md','EVIDENCE_METHODS.md','REVIEW_FEASIBILITY.md','AUTOMATED_FINDINGS_AGGREGATED.csv',
 'SOURCE_SCOPE_SUMMARY.csv','IDENTITY_SENSITIVITY.md','NOVELTY_AND_CONTRIBUTION.md','FINAL_PUBLICATION_DECISION.md',
 'PUBLICATION_VERDICT.md','RUN_LOG.md','HANDOFF.md','PUBLICATION_READINESS_AUDIT.md','VALIDATION.md',
 'conditional_research_dossier.md','freeze_integrity_summary.json','measurement_check.json','COMPLETION_AUDIT.json','environment.json',
 'GROUP_SUPPORT.csv','MEASUREMENT_GROUP_SENSITIVITIES.csv','PAIRED_GROUP_DECOMPOSITION.csv','WEIGHTING_SUPPORT.csv',
 'ILLUSTRATIVE_LINKAGE_SENSITIVITY.csv','review.py','extract_sources.py','sensitivity.py','audit_completion.py',
 'make_summary.py','build_handoff.py','test_autonomous.py',
 'figures/documentary_support.png','figures/documentary_support.pdf',
 'figures/source_era_width.png','figures/source_era_width.pdf']
CURRENT_FILES=['README.md','AGENTS.md','CLAUDE.md','dashboard/app.py','.github/workflows/ci.yml',
 'research_completion/phase3/START_HERE_PHASE3.md',
 'research_completion/phase3/followup_20261021/HANDOFF.md',
 'research_completion/phase3/followup_20261021/PUBLICATION_VERDICT.md',
 'research_completion/phase3/followup_20261021/AUTONOMOUS_EVIDENCE_REVIEW_DIRECTIVE.md']

spec=importlib.util.spec_from_file_location('prior_package',HERE.parent/'build_handoff.py')
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)


def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def check_public(mapped):
    approved_pdfs={(HERE/f).relative_to(ROOT).as_posix() for f in PUBLIC_FILES if f.endswith('.pdf')}
    for name,data in mapped.items():
        p=PurePosixPath(name)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in name
        if p.suffix=='.pdf':
            assert name in approved_pdfs and data.startswith(b'%PDF'), name
        if p.suffix in {'.md','.json','.csv','.txt','.html'}:
            assert b'R01P3-' not in data, 'Confidential case identifier in '+name
    prior.check_public({name:data for name,data in mapped.items() if name not in approved_pdfs})


def immutable_write(path,mapped):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        prior.verify_archive(path)
        with zipfile.ZipFile(path) as a:
            assert set(a.namelist())-{ 'SHA256SUMS.txt' }==set(mapped), 'Existing immutable archive has different members'
            for name,data in mapped.items():assert a.read(name)==data, 'Existing archive differs; create an explicit revision'
        result=prior.verify_archive(path);result.update(sha256=sha(path),bytes=path.stat().st_size)
        return result
    return prior.write_archive(path,mapped)


def downloads_copy(path):
    target=Path.home()/'Downloads'/path.name
    if target.exists():assert sha(target)==sha(path), 'Different Downloads file already exists; preserve it'
    else:shutil.copyfile(path,target)
    assert sha(target)==sha(path)
    target.with_suffix(target.suffix+'.sha256').write_text(sha(path)+'  '+path.name+'\n',encoding='ascii')


def check_older():
    assert sha(BASE)==BASE_SHA
    assert sha(prior.OLD)==prior.OLD_SHA
    old_private=PRIVATE.parent/'REMITTANCE_R01_IDENTITY_REVIEW_LOCAL_ONLY_20261021.zip'
    assert sha(old_private)=='f5a670e19c1e86e5f16e63d1a2679039dd66f8586162ed86ee93a921ab1e78f2'
    prior.verify_archive(BASE)


def public():
    check_older()
    with zipfile.ZipFile(BASE) as a:
        mapped={n:a.read(n) for n in a.namelist() if n!='SHA256SUMS.txt'}
    for name in CURRENT_FILES:mapped[name]=(ROOT/name).read_bytes()
    for name in PUBLIC_FILES:mapped[(HERE/name).relative_to(ROOT).as_posix()]=(HERE/name).read_bytes()
    mapped['START_HERE_AUTONOMOUS.md']=(
        '# Completed autonomous investigation\n\nCONDITIONAL_HOLD_EXTERNAL_VALIDATION; do not submit the original article now. '
        'Start with research_completion/phase3/followup_20261021/autonomous_review/HANDOFF.md. '
        'All 60 documentary assessments unresolved; no human validation. No manual case review is requested. '
        'This root SHA256SUMS.txt validates the current overlay. Older snapshots/manifests and the embedded immutable '
        'Phase 3 ZIP are historical; their earlier human-review requests are superseded. No confidential cases/source '
        'reading copies are included. The local-only evidence ZIP is a separate private delivery.\n').encode()
    check_public(mapped)
    path=HERE/'deliverables'/PUBLIC_NAME
    result=immutable_write(path,mapped);downloads_copy(path)
    result.update(source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                  prior_followup_sha256=BASE_SHA,original_phase3_sha256=prior.OLD_SHA,
                  public_private_separation='PASS',downloads_copy_verified=True,older_archives_unchanged=True)
    (path.parent/'zip_verification.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    path.with_suffix('.zip.sha256').write_text(result['sha256']+'  '+path.name+'\n',encoding='ascii')
    target=Path.home()/'Downloads/REMITTANCE_R01_AUTONOMOUS_HANDOFF_20261021.md'
    if target.exists():assert target.read_bytes()==(HERE/'HANDOFF.md').read_bytes()
    else:shutil.copyfile(HERE/'HANDOFF.md',target)
    print(json.dumps(result,indent=2))


def private():
    check_older()
    spec=importlib.util.spec_from_file_location('private_audit',HERE/'audit_completion.py')
    audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
    audit.private_checks()
    allowed_suffixes={'.json','.csv','.txt','.py','.sha256','.png'}
    mapped={}
    for path in sorted(PRIVATE.iterdir()):
        if path.is_file() and path.suffix in allowed_suffixes and path.name not in {'private_zip_verification.json'} and not path.name.startswith(PRIVATE_NAME):
            mapped[path.relative_to(ROOT).as_posix()]=path.read_bytes()
    for folder in ['sources','extracted']:
        for path in sorted((PRIVATE/folder).iterdir()):
            assert path.suffix in {'.json','.bin','.txt'}
            mapped[path.relative_to(ROOT).as_posix()]=path.read_bytes()
    blind=ROOT/'research_completion/phase3/private_runtime/BLINDED_IDENTITY_REVIEW.csv'
    mapped[blind.relative_to(ROOT).as_posix()]=blind.read_bytes()
    for name in ['review.py','audit_completion.py','extract_sources.py','sensitivity.py','EVIDENCE_METHODS.md']:
        mapped[(HERE/name).relative_to(ROOT).as_posix()]=(HERE/name).read_bytes()
    mapped['START_HERE_PRIVATE.md']=(
        '# LOCAL ONLY historical evidence\n\nDo not upload this archive. It contains confidential case/source associations, '
        'alternatives, frozen AI assessments, post-freeze strata, query logs and private reading copies. Human decisions remain blank. '
        'No manual review is requested. This is not independent human validation. '
        'The original stratum key, outcomes, raw workbook and model cache are excluded; post-freeze sampled strata are retained in the joined ledger. '
        'Paths mirror the repository for local recovery. Copy into a separate local recovery folder first; never overwrite sealed originals. '
        'SHA256SUMS.txt verifies every payload; source manifest distinguishes original bytes from mixed-source reader transcript hashes.\n').encode()
    assert not any(PurePosixPath(n).suffix in {'.pkl','.xlsx','.joblib'} or PurePosixPath(n).name=='IDENTITY_REVIEW_KEY.csv' for n in mapped)
    path=PRIVATE/PRIVATE_NAME
    result=immutable_write(path,mapped);downloads_copy(path)
    result.update(local_only=True,cases=60,human_adjudications=0,downloads_copy_verified=True,
                  original_key_and_outcome_cache_included=False,postfreeze_strata_included=True,older_archives_unchanged=True)
    (PRIVATE/'private_zip_verification.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['public','private']);args=p.parse_args()
    {'public':public,'private':private}[args.stage]()
