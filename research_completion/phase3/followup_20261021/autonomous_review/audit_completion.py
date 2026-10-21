"""Independent arithmetic/file audit: no imports of linkage or modelling code.

Public mode runs on aggregates in CI. --private additionally verifies the sealed
60-case ledger and reading-copy bytes locally; it never emits case identifiers.
This is a software audit, not external scientific or human identity validation.
"""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import urllib.parse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PRIVATE = ROOT / "research_completion/phase3/private_runtime/followup_20261021/autonomous_review"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def check_close(a, b):
    assert abs(float(a)-float(b)) < 1e-12, (a, b)


def public_checks():
    findings = read(HERE / "AUTOMATED_FINDINGS_AGGREGATED.csv")
    assert sum(int(r["cases"]) for r in findings) == 60
    strata = Counter()
    grades = Counter()
    for row in findings:
        strata[row["sampled_stratum"]] += int(row["cases"])
        grades[row["support_grade"]] += int(row["cases"])
        assert row["machine_status"] == "UNRESOLVED_INSUFFICIENT_HISTORICAL_EVIDENCE"
    assert len(strata) == 5 and set(strata.values()) == {12}
    assert grades == Counter(B=2, C=47, D=11)
    freeze = json.loads((HERE / "freeze_integrity_summary.json").read_text())
    assert freeze["case_count"] == 60 and freeze["human_adjudications"] == 0 and not freeze["external_validation"]
    assert dict(grades) == freeze["grade_counts"]
    grouped = read(HERE / "MEASUREMENT_GROUP_SENSITIVITIES.csv")
    support = read(HERE / "GROUP_SUPPORT.csv")
    assert len(grouped) == sum(r["reported"] == "True" for r in support)
    for identity in ["core", "strict"]:
        for field in {r["group_field"] for r in support}:
            rows = [r for r in support if r["identity_rule"] == identity and r["group_field"] == field]
            assert sum(int(r["n_eligible"]) for r in rows) == 45343
    for row in grouped:
        n, v, stay, fail, unknown = (int(row[k]) for k in ["n_eligible", "n_valid", "n_stay", "n_fail", "n_unknown"])
        assert stay+fail == v and v+unknown == n
        check_close(row["lower"], stay/n)
        check_close(row["upper"], (stay+unknown)/n)
        if v:
            check_close(row["conditional"], stay/v)
    paired = read(HERE / "PAIRED_GROUP_DECOMPOSITION.csv")
    for row in paired:
        assert int(row["core_valid"])-int(row["strict_valid"]) == int(row["newly_unknown"])
        assert int(row["changed_core_stay"])+int(row["changed_core_fail"]) == int(row["newly_unknown"])
        check_close(row["width_difference"], int(row["newly_unknown"])/int(row["n_eligible"]))
    for field in ["source_era", "funding_group", "payout_group", "region"]:
        rows = [r for r in paired if r["group_field"] == field]
        assert sum(int(r["newly_unknown"]) for r in rows) == 5859
        assert sum(int(r["changed_core_stay"]) for r in rows) == 4770
    for row in read(HERE / "ILLUSTRATIVE_LINKAGE_SENSITIVITY.csv"):
        k = int(row["assumed_false_positive_links"])
        assert int(row["n_eligible"]) == 45343
        assert int(row["retained_valid"])+int(row["unknown"]) == 45343
        assert int(row["retained_valid"]) == 36429-k
        check_close(row["all_origin_lower"], (29546-min(29546,k))/45343)
        check_close(row["all_origin_upper"], 1-(6883-min(6883,k))/45343)
    return dict(sample_cases=60, strata=5, grades=dict(grades), denominator_checks="PASS",
                source_era_and_group_reconciliation="PASS", human_validation=False)


def legacy_checks():
    folder = ROOT / "research_completion/phase3/reproducibility"
    strict = read(folder / "STRICT_LEGACY_COMPARISON.csv")
    causes = read(folder / "LEGACY_DIFFERENCE_CAUSES.csv")
    fields = read(folder / "LEGACY_FIELD_DIFFERENCES.csv")
    assert Counter(r["status"] for r in strict) == Counter(MATCH=14, DIFFERS=14, MATCH_EXCEPT_TIMING=2)
    assert {r["file"]: r["status"] for r in strict} == {r["file"]: r["strict_status"] for r in causes}
    assert Counter(r["category"] for r in causes) == Counter(source_cohort_linkage_exact=14,
              numeric_solver_and_derived_rank=12, python_platform_metadata=2, volatile_runtime=2)
    assert len({r["file"] for r in fields if r["category"] == "numeric_or_rank_propagation"}) == 12
    return dict(tables=30, exact=14, timing_only=2, differs=14, numeric_or_rank_tables=12,
                metadata_tables=2, root_numeric_cause="UNRESOLVED", refits=0,
                files={f:digest(folder/f) for f in ["STRICT_LEGACY_COMPARISON.csv","LEGACY_DIFFERENCE_CAUSES.csv","LEGACY_FIELD_DIFFERENCES.csv"]})


def private_checks():
    frozen_path = PRIVATE / "machine_review_frozen.json"
    assert digest(frozen_path) == (PRIVATE / "machine_review_frozen.sha256").read_text().strip()
    freeze = json.loads(frozen_path.read_text())
    for name, field in [("case_evidence.csv","evidence_table_sha256"),("case_source_log.csv","case_source_log_sha256"),
        ("pass1_proposals.json","pass1_proposals_sha256"),("source_manifest.json","source_manifest_sha256"),
        ("annotation_provenance.json","annotation_provenance_sha256"),("prepare_private.py","private_annotation_script_sha256")]:
        assert digest(PRIVATE/name) == freeze[field]
    blind = read(ROOT / "research_completion/phase3/private_runtime/BLINDED_IDENTITY_REVIEW.csv")
    assert digest(ROOT / "research_completion/phase3/private_runtime/BLINDED_IDENTITY_REVIEW.csv") == freeze["blind_input_sha256"]
    cases = read(PRIVATE / "case_evidence.csv")
    proposals = json.loads((PRIVATE / "pass1_proposals.json").read_text(encoding="utf8"))
    ids = {r["case_id"] for r in blind}
    assert len(ids) == len(cases) == len(proposals) == 60
    assert ids == {r["case_id"] for r in cases} == {r["case_id"] for r in proposals}
    assert all(not r["human_identity_decision"] and not r["reviewer"] for r in blind)
    sources = json.loads((PRIVATE / "source_manifest.json").read_text(encoding="utf8"))
    ledger = read(PRIVATE / "case_source_log.csv")
    assert ids == {r["case_id"] for r in ledger}
    assert len({(r["case_id"],r["source_id"]) for r in ledger}) == len(ledger)
    for source in sources:
        url = urllib.parse.urlparse(source["url"])
        assert url.scheme in {"http","https"} and url.hostname and not url.username and not url.password
        assert source["checked_at_utc"]
        if source.get("source_sha256"):
            file = PRIVATE / source["reading_copy"] if source.get("reading_copy") else PRIVATE / "sources" / (source["source_id"]+".bin")
            assert digest(file) == source["source_sha256"]
    assert all(p["source_based_reasoning"] and p["counterargument"] and p["best_alternative"] and not p["human_adjudication"] for p in proposals)
    return dict(case_ids_conserved=60, case_source_rows=len(ledger), source_records=len(sources),
                sealed_file_and_reading_copy_hashes="PASS", human_fields_untouched=True)


def main(private=False):
    report = dict(audit_type="INDEPENDENT_CODE_PATH_NOT_INDEPENDENT_HUMAN_REVIEW", public=public_checks(), legacy=legacy_checks())
    if private:
        report["private"] = private_checks()
    (HERE / "COMPLETION_AUDIT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("--private", action="store_true")
    main(p.parse_args().private)
