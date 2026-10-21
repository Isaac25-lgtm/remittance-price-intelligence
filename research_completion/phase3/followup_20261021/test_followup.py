"""Offline safeguards for the blinded review and aggregate reconciliation."""
import csv
import importlib.util
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("bounded_followup", HERE / "evidence_followup.py")
followup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(followup)
package_spec = importlib.util.spec_from_file_location("followup_package", HERE / "build_handoff.py")
package = importlib.util.module_from_spec(package_spec)
package_spec.loader.exec_module(package)


def decision(value=""):
    row = {field: "" for field in followup.REVIEW_FIELDS}
    row.update(case_id="SYNTHETIC-1", human_identity_decision=value)
    return row


def test_pending_is_not_adjudication():
    result = followup.validate_decisions([decision()], ["SYNTHETIC-1"])
    assert result["counts"]["PENDING"] == 1
    assert not result["complete"] and not result["external_evidence_verified_by_code"]


@pytest.mark.parametrize("value", ["SAME_BUNDLE", "DIFFERENT_BUNDLE"])
def test_resolved_requires_historical_evidence(value):
    row = decision(value)
    row.update(reviewer="Synthetic reviewer", review_date="2026-10-21", reason="Synthetic example")
    with pytest.raises(ValueError, match="historical evidence"):
        followup.validate_decisions([row], ["SYNTHETIC-1"])


@pytest.mark.parametrize("value", ["UNRESOLVED", "NOT_REVIEWABLE"])
def test_uncertainty_is_valid_and_not_truth(value):
    row = decision(value)
    row.update(reviewer="Synthetic reviewer", review_date="2026-10-21", reason="No sufficient historical source")
    result = followup.validate_decisions([row], ["SYNTHETIC-1"])
    assert result["complete"] and not result["population_error_rate_identified"]


@pytest.mark.parametrize("rows,expected", [([decision(), decision()], ["SYNTHETIC-1"]),
                                        ([decision()], ["OTHER"]), ([], ["SYNTHETIC-1"])])
def test_missing_duplicate_or_unexpected_cases_fail(rows, expected):
    with pytest.raises(ValueError, match="case IDs"):
        followup.validate_decisions(rows, expected)


def test_invalid_label_and_date_rejected():
    with pytest.raises(ValueError, match="Invalid identity"):
        followup.validate_decisions([decision("probably same")], ["SYNTHETIC-1"])
    row = decision("UNRESOLVED")
    row.update(reviewer="Synthetic", review_date="2026-99-99", reason="No source")
    with pytest.raises(ValueError):
        followup.validate_decisions([row], ["SYNTHETIC-1"])


def test_html_escapes_source_text_and_has_no_key_or_network():
    row = {"case_id": "SYNTHETIC-1", "origin_quarter": "2020Q4", "corridor": "AAA>BBB",
           "origin_firm": "<script>unsafe</script>", "target_multiplicity": "1"}
    result = followup.reviewer_html([row], "Reviewer_A")
    assert "&lt;script&gt;unsafe&lt;/script&gt;" in result
    assert "2020Q4 to 2021Q1" in result
    assert "IDENTITY_REVIEW_KEY.csv" not in result
    assert "fetch(" not in result and "XMLHttpRequest" not in result
    assert 'value="">Pending' in result


def test_every_wave_and_pooled_counts_reconcile():
    with (HERE / "attribute_change_by_wave.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == len({row["quarter"] for row in rows}) == 36
    assert sum(int(row["n_changed_valid"]) for row in rows) == 5859
    assert sum(int(row["changed_stay"]) for row in rows) == 4770
    assert sum(int(row["unchanged_stay"]) for row in rows) == 24776
    for row in rows:
        assert int(row["n_core_valid"]) == int(row["n_changed_valid"]) + int(row["n_unchanged_valid"])
        assert float(row["width_difference"]) == pytest.approx(int(row["n_changed_valid"]) / int(row["n_eligible"]))


@pytest.mark.parametrize("path,data", [
    ("research_completion/phase3/private_runtime/cases.csv", b"case_id\nSYNTHETIC\n"),
    ("public/cases.csv", b"case_id,human_identity_decision\nSYNTHETIC,UNRESOLVED\n"),
    ("public/manuscript.pdf", b"%PDF")])
def test_public_archive_rejects_case_rows_and_reading_copies(path, data):
    with pytest.raises(AssertionError):
        package.check_public({path: data})


def test_archive_detects_corrupt_payload(tmp_path):
    path = tmp_path / "synthetic.zip"
    package.write_archive(path, {"synthetic.txt": b"safe synthetic fixture"})
    import zipfile
    with zipfile.ZipFile(path, "r") as archive:
        payload = {name: archive.read(name) for name in archive.namelist()}
    payload["synthetic.txt"] = b"changed"
    with zipfile.ZipFile(path, "w") as archive:
        for name, data in payload.items():
            archive.writestr(name, data)
    with pytest.raises(AssertionError):
        package.verify_archive(path)
