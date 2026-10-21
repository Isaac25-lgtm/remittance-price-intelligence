"""Synthetic machine-review safeguards; no private cases or network in CI."""
import importlib.util
import json
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("machine_documentary_review", HERE / "review.py")
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


def proposal(**overrides):
    return dict(proposed_grade="A", proposed_status="EVIDENCE_SUPPORTS_SAME", unresolved_alternative=False,
                direct_dated_distinct_products=False, material_contradiction=False, **overrides)


def exact_source():
    return dict(access_status="CACHED_ORIGINAL_BYTES", document_date="2020-01-01", origin_coverage="EXPLICIT_FULL_PERIOD",
                target_coverage="EXPLICIT_FULL_PERIOD", corridor_scope="EXACT_ORDERED_CORRIDOR", provider_scope="EXACT_PROVIDER", bundle_scope="FULL_BUNDLE")


def test_label_equality_cannot_replace_documents():
    result = r.audit_proposal(dict(target_multiplicity="1"), proposal(), [])
    assert result["machine_status"] == r.UNRESOLVED and result["support_grade"] == "D"


@pytest.mark.parametrize("field,value", [("target_coverage", "UNKNOWN"), ("bundle_scope", "PARTIAL"),
                                         ("corridor_scope", "GENERIC"), ("provider_scope", "RELATED_BRAND")])
def test_grade_a_requires_all_scopes(field, value):
    source = exact_source(); source[field] = value
    result = r.audit_proposal(dict(target_multiplicity="1"), proposal(), [source])
    assert result["machine_status"] == r.UNRESOLVED and result["support_grade"] != "A"


@pytest.mark.parametrize("multiplicity", ["0", "2", "3"])
def test_unique_successor_is_required(multiplicity):
    assert r.audit_proposal(dict(target_multiplicity=multiplicity), proposal(), [exact_source()])["machine_status"] == r.UNRESOLVED


def test_full_documentary_support_still_not_human_truth():
    result = r.audit_proposal(dict(target_multiplicity="1"), proposal(), [exact_source()])
    assert result["machine_status"] == "EVIDENCE_SUPPORTS_SAME"
    assert result["independent_human_validation"] is False


def test_modern_generic_evidence_not_grade_b():
    source = exact_source(); source.update(origin_coverage="UNKNOWN", target_coverage="UNKNOWN", corridor_scope="GENERIC")
    p = proposal(); p.update(proposed_grade="B", proposed_status=r.UNRESOLVED)
    result = r.audit_proposal(dict(target_multiplicity="1"), p, [source])
    assert result["support_grade"] == "C"


def test_closure_or_vocabulary_alone_not_distinct_products():
    p = proposal(); p.update(proposed_status="EVIDENCE_SUPPORTS_DIFFERENT")
    assert r.audit_proposal(dict(target_multiplicity="0"), p, [exact_source()])["machine_status"] == r.UNRESOLVED


@pytest.mark.parametrize("url", ["file:///secret", "https://name:password@example.org/", "not-a-url"])
def test_bad_source_urls_rejected_without_network(tmp_path, monkeypatch, url):
    monkeypatch.setattr(r, "PRIVATE", tmp_path)
    with pytest.raises(ValueError, match="URL"):
        r.retrieve(dict(source_id="synthetic", url=url))


def test_checkpoint_hash_tampering_detected(tmp_path, monkeypatch):
    monkeypatch.setattr(r, "PRIVATE", tmp_path)
    frozen = tmp_path / "machine_review_frozen.json"
    frozen.write_text('{}', encoding="utf-8")
    (tmp_path / "machine_review_frozen.sha256").write_text(r.sha(b'{}'))
    frozen.write_text('{"altered":true}', encoding="utf-8")
    with pytest.raises(ValueError, match="manifest changed"):
        r.verify_freeze()
