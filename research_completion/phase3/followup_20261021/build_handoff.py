"""Explicit safe overlay, immutable previous snapshot, separate LOCAL ONLY review ZIP."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PRIVATE = HERE.parent / "private_runtime" / "followup_20261021"
OLD = HERE.parent / "deliverables" / "REMITTANCE_R01_PHASE3_PUBLICATION_HANDOFF_20261021_34ba4ca.zip"
OLD_SHA = "a01def0d701aae0b7f19a89d5ebbf28f7b2b683b2d33eb4ae629d5ba59b5665c"
PUBLIC_NAME = "REMITTANCE_R01_PHASE3_FOLLOWUP_HANDOFF_20261021.zip"
PRIVATE_NAME = "REMITTANCE_R01_IDENTITY_REVIEW_LOCAL_ONLY_20261021.zip"
PUBLIC_FILES = ["SCOPE.md", "HANDOFF.md", "PUBLICATION_VERDICT.md", "LIM_OVERLAP_REVIEW.md",
                "SURVEY_CHANGE_REVIEW.md", "CRITIQUE_RECONCILIATION.md", "REVIEWER_INSTRUCTIONS.md",
                "evidence_followup.py", "test_followup.py", "build_handoff.py", "source_acquisition.csv",
                "web_source_checks.csv", "attribute_change_by_wave.csv", "attribute_change_pooled.csv",
                "identity_preparation_status.json", "EXECUTION_LEDGER.md", "SCIENTIFIC_AUDIT.md",
                "validation_summary.json"]
CURRENT_FILES = ["README.md", "AGENTS.md", "CLAUDE.md", "CITATION.cff", "pyproject.toml",
                 ".github/workflows/ci.yml", "dashboard/app.py", "dashboard/ui.py", "dashboard/README.md",
                 "dashboard/requirements.txt", "docs/DEPLOYMENT.md", "docs/archive/README_phase1_phase2_record.md",
                 "scripts/readme_figures.py", "tests/test_dashboard.py", "research_completion/phase3/START_HERE_PHASE3.md"]
CURRENT_FILES += ["docs/figures/" + name for name in ["banner.svg", "fig0_survey_coverage.png",
                  "fig1_identity_bounds.png", "fig2_wave_series.png", "fig3_quote_flow.png", "fig4_models.png",
                  "fig5_review_capacity.png", "fig6_regions.png"]]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(path):
    data = path.read_bytes()
    return data.replace(b"\r\n", b"\n") if path.suffix in {".md", ".py", ".csv", ".json", ".cff", ".toml", ".yml", ".txt", ".svg"} else data


def verify_archive(path):
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        assert len(names) == len(set(names))
        sums = archive.read("SHA256SUMS.txt").decode("utf-8").splitlines()
        listed = []
        for line in sums:
            expected, name = line.split("  ", 1)
            assert sha(archive.read(name)) == expected
            listed.append(name)
        assert set(listed) == set(names) - {"SHA256SUMS.txt"}
        return dict(members=len(names), payload_hashes_verified=len(listed), crc_verified=True)


def write_archive(path, mapped):
    for name in mapped:
        p = PurePosixPath(name)
        if p.is_absolute() or ".." in p.parts or "\\" in name:
            raise ValueError("Unsafe archive path")
    mapped = dict(mapped)
    mapped["SHA256SUMS.txt"] = "".join(sha(data) + "  " + name + "\n" for name, data in sorted(mapped.items())).encode("utf-8")
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(mapped.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    result = verify_archive(path)
    result.update(sha256=sha(path.read_bytes()), bytes=path.stat().st_size)
    return result


def check_public(mapped):
    for name, data in mapped.items():
        p = PurePosixPath(name)
        assert not set(p.parts) & {"private_runtime", "raw", "restricted", ".git", "__pycache__"}, name
        assert p.suffix.lower() not in {".pdf", ".xlsx", ".xls", ".pkl", ".pickle", ".parquet", ".npy", ".joblib"}, name
        if p.suffix == ".zip":
            assert name == OLD.relative_to(ROOT).as_posix() and sha(data) == OLD_SHA
        if p.suffix == ".csv":
            reader = csv.reader(io.StringIO(data.decode("utf-8-sig")))
            header = next(reader, [])
            first_row = next(reader, None)
            # A header-only public review schema is allowed; actual case rows are not.
            if first_row is not None:
                assert not set(header) & {"origin_source_row", "target_source_rows", "origin_firm", "target_firm",
                                          "human_identity_decision", "case_id", "cost_next"}, name


def build_public():
    assert sha(OLD.read_bytes()) == OLD_SHA, "Original Phase 3 archive changed"
    with zipfile.ZipFile(OLD) as previous:
        original_sums = previous.read("research_completion/phase3/deliverables/SHA256SUMS.txt").decode()
        for line in original_sums.splitlines():
            expected, name = line.split("  ", 1)
            assert sha(previous.read(name)) == expected
        mapped = {name: previous.read(name) for name in previous.namelist()}
    for name in CURRENT_FILES:
        mapped[name] = canonical(ROOT / name)
    for name in PUBLIC_FILES:
        path = HERE / name
        mapped[path.relative_to(ROOT).as_posix()] = canonical(path)
    mapped[OLD.relative_to(ROOT).as_posix()] = OLD.read_bytes()
    mapped["START_HERE_FOLLOWUP.md"] = ("# Current handoff - 21 October 2026\n\n"
        "Decision CONDITIONAL_HOLD. Start with [the new handoff](research_completion/phase3/followup_20261021/HANDOFF.md).\n\n"
        "This consolidated ZIP contains safe previous scientific artifacts, the current follow-up and presentation files, "
        "and the immutable original Phase 3 ZIP in research_completion/phase3/deliverables/. "
        "Validate this consolidated archive using root SHA256SUMS.txt. Historical manifests under phase3/deliverables/ "
        "describe the older embedded ZIP, not the updated overlay. No private cases, outcome rows, key or reading-copy papers are included. "
        "Your LOCAL_ONLY reviewer pack is a separate local Downloads delivery.\n").encode("utf-8")
    check_public(mapped)
    target = HERE / "deliverables"
    target.mkdir(exist_ok=True)
    path = target / PUBLIC_NAME
    result = write_archive(path, mapped)
    downloads = Path.home() / "Downloads"
    shutil.copyfile(path, downloads / PUBLIC_NAME)
    assert sha((downloads / PUBLIC_NAME).read_bytes()) == result["sha256"]
    shutil.copyfile(HERE / "HANDOFF.md", downloads / "REMITTANCE_R01_PHASE3_FOLLOWUP_HANDOFF_20261021.md")
    result.update(source_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                  original_phase3_sha256=OLD_SHA, downloads_copy_verified=True, public_private_separation="PASS",
                  snapshot_note="Original archive immutable; overlay payload hashes define this new handoff")
    (target / "zip_verification.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


def build_private():
    pack = PRIVATE / "reviewer_pack"
    names = ["START_HERE.md", "BLINDED_CASES.csv", "Reviewer_A/REVIEWER.html", "Reviewer_A/REVIEW_DECISIONS.csv",
             "Reviewer_B/REVIEWER.html", "Reviewer_B/REVIEW_DECISIONS.csv"]
    mapped = {name: (pack / name).read_bytes() for name in names}
    for name, data in mapped.items():
        assert "KEY" not in name and "stratum" not in name.lower()
        if name.endswith(".csv"):
            text = data.decode("utf-8-sig")
            rows = list(csv.DictReader(io.StringIO(text)))
            assert len(rows) == 60 and len({row["case_id"] for row in rows}) == 60
            assert all(not row.get("human_identity_decision", "") for row in rows)
            assert not any(any(token in field.lower() for token in ["cost", "price", "stratum"]) for field in rows[0])
    path = PRIVATE / PRIVATE_NAME
    result = write_archive(path, mapped)
    downloads = Path.home() / "Downloads" / PRIVATE_NAME
    shutil.copyfile(path, downloads)
    assert sha(downloads.read_bytes()) == result["sha256"]
    result.update(local_only=True, cases=60, human_decisions=0, prices_or_key_included=False, downloads_copy_verified=True)
    (PRIVATE / "reviewer_zip_verification.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["public", "private", "audit"])
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    if args.stage == "audit":
        print(json.dumps(verify_archive(args.archive), indent=2))
    else:
        {"public": build_public, "private": build_private}[args.stage]()
