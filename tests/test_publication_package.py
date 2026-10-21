import importlib.util
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location('pack',Path(__file__).resolve().parents[1]/'scripts/build_publication_handoff.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_provider_rows_cannot_enter_public_csv(tmp_path,monkeypatch):
    monkeypatch.setattr(m,'ROOT',tmp_path)
    p=tmp_path/'research_completion/tables/test.csv';p.parent.mkdir(parents=True)
    p.write_text('provider,cost\nNamed Provider,2\n',encoding='utf-8')
    with pytest.raises(ValueError,match='identifiers'):m.inspect_public_file(p)

def test_private_runtime_is_rejected_even_for_safe_extension(tmp_path,monkeypatch):
    monkeypatch.setattr(m,'ROOT',tmp_path)
    p=tmp_path/'research_completion/private_runtime/test.csv';p.parent.mkdir(parents=True);p.write_text('n\n1\n')
    with pytest.raises(ValueError,match='forbidden path'):m.inspect_public_file(p)

def test_secret_is_rejected(tmp_path,monkeypatch):
    monkeypatch.setattr(m,'ROOT',tmp_path)
    p=tmp_path/'README.md';p.write_text('ghp_'+'a'*36)
    with pytest.raises(ValueError,match='credential'):m.inspect_public_file(p)

def test_archive_text_is_identical_across_windows_and_linux_newlines(tmp_path):
    p=tmp_path/'safe.csv';p.write_bytes(b'count\r\n10\r\n')
    windows=m.public_bytes(p)
    p.write_bytes(b'count\n10\n')
    assert windows==m.public_bytes(p)==b'count\n10\n'

def test_handoff_integrity_when_present():
    root=Path(__file__).resolve().parents[1]
    archives=list((root/'research_completion/deliverables').glob('*.zip'))
    if not archives:pytest.skip('ZIP assembled only after scientific outputs lock')
    assert all(m.audit_zip(p)['status']=='PASS' for p in archives)
