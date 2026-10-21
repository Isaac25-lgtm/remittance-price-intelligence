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


def sensitivity_module():
    spec = importlib.util.spec_from_file_location("measurement_sensitivity", HERE / "sensitivity.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("origin,expected", [(2021*4-1,"before_target_2021Q2"),
    (2021*4,"transition_target_2021Q2"), (2021*4+1,"between_classification_transitions"),
    (2022*4+1,"between_classification_transitions"), (2022*4+2,"transition_target_2022Q4"),
    (2022*4+3,"after_target_2022Q4")])
def test_classification_era_uses_successor_not_origin_boundary(origin, expected):
    assert sensitivity_module().era(origin) == expected


@pytest.mark.parametrize("removed", [0,1,3,7,10])
def test_false_positive_envelope_by_enumerating_allocations(removed):
    # Enumerate possible removal allocations: an independent arithmetic check.
    s = sensitivity_module()
    result = s.adversarial_false_positive(14,7,3,removed)
    possible = [(7-a,3-(removed-a)) for a in range(8) if 0 <= removed-a <= 3]
    assert result["retained_valid"] + result["unknown"] == 14
    assert result["all_origin_lower"] == min(stays/14 for stays, fails in possible)
    assert result["all_origin_upper"] == max(1-fails/14 for stays, fails in possible)


def test_false_positive_impossible_counts_rejected():
    with pytest.raises(ValueError):
        sensitivity_module().adversarial_false_positive(9,7,3,1)


def test_partial_near_period_can_be_b_but_not_same():
    source = exact_source(); source.update(bundle_scope="PARTIAL", target_coverage="NOT_ESTABLISHED", origin_coverage="PARTIAL_NEAR_PERIOD")
    p = proposal(); p["proposed_grade"] = "B"
    result = r.audit_proposal(dict(target_multiplicity="1"), p, [source])
    assert result["support_grade"] == "B" and result["machine_status"] == r.UNRESOLVED


def test_reader_hash_never_implies_full_period_coverage():
    source = exact_source(); source.update(access_status="BROWSER_PARSED_SOURCE_TEXT", origin_coverage="NOT_ESTABLISHED")
    result = r.audit_proposal(dict(target_multiplicity="1"), proposal(), [source])
    assert result["machine_status"] == r.UNRESOLVED


def test_public_completion_audit_has_independent_conservation_path():
    spec = importlib.util.spec_from_file_location("completion_audit", HERE / "audit_completion.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    assert module.public_checks()["denominator_checks"] == "PASS"
    legacy = module.legacy_checks()
    assert legacy["differs"] == 14 and legacy["numeric_or_rank_tables"] == 12


def test_reported_documentary_counts_match_frozen_aggregate():
    import csv
    from collections import Counter
    with (HERE/"AUTOMATED_FINDINGS_AGGREGATED.csv").open(encoding="utf8") as f:
        rows = list(csv.DictReader(f))
    grades = Counter()
    for row in rows: grades[row["support_grade"]] += int(row["cases"])
    assert grades == Counter(B=2,C=47,D=11)
    text = (HERE/"REVIEW_FEASIBILITY.md").read_text(encoding="utf8")
    for phrase in ["0/60 (0%)", "2/60 (3.33%)", "47/60 (78.33%)", "11/60 (18.33%)"]:
        assert phrase in text


@pytest.mark.parametrize("name,data", [
    ("public/cases.csv", b"case_id,origin_firm\nSYNTHETIC-1,Example\n"),
    ("research_completion/phase3/private_runtime/evidence.txt", b"private"),
    ("public/reading_copy.pdf", b"%PDF-test"),
    ("public/summary.md", b"R01P3-999 confidential association"),
    ("../outside.txt", b"unsafe path")])
def test_new_public_package_rejects_confidential_payloads(name, data):
    spec=importlib.util.spec_from_file_location("autonomous_package", HERE/"build_handoff.py")
    package=importlib.util.module_from_spec(spec);spec.loader.exec_module(package)
    with pytest.raises(AssertionError):package.check_public({name:data})
