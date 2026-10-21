"""Checkpointed, blinded machine documentary review; no price/key imports before freeze."""
from collections import Counter
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PRIVATE = ROOT / "research_completion/phase3/private_runtime/followup_20261021/autonomous_review"
INPUT = ROOT / "research_completion/phase3/private_runtime/BLINDED_IDENTITY_REVIEW.csv"
PROMPT_VERSION = "R01_AUTONOMOUS_DOCUMENTARY_V1"
STATUSES = {"EVIDENCE_SUPPORTS_SAME", "EVIDENCE_SUPPORTS_DIFFERENT",
            "UNRESOLVED_INSUFFICIENT_HISTORICAL_EVIDENCE", "NOT_REVIEWABLE"}
UNRESOLVED = "UNRESOLVED_INSUFFICIENT_HISTORICAL_EVIDENCE"
SOURCE_FIELDS = ["case_id", "source_id", "url", "title", "publisher", "document_date", "effective_from", "effective_to",
                 "corridor_scope", "provider_scope", "bundle_scope", "origin_coverage", "target_coverage",
                 "section_or_page", "quoted_support_or_paraphrase", "source_sha256", "access_status", "checked_at_utc", "limitations"]


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path, rows, fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_blind(path=INPUT):
    rows = read_csv(path)
    if len(rows) != 60 or len({row["case_id"] for row in rows}) != 60:
        raise ValueError("Expected exactly 60 unique blinded cases")
    if any(any(t in field.lower() for t in ["cost", "price", "stratum", "probability"]) for field in rows[0]):
        raise ValueError("Outcome/stratum field in blind input")
    if any(row.get("human_identity_decision", "") or row.get("reviewer", "") for row in rows):
        raise ValueError("Human decisions must not be overwritten or reinterpreted")
    return rows


def init():
    PRIVATE.mkdir(parents=True, exist_ok=True)
    rows = load_blind()
    summary = dict(blind_input_sha256=sha(INPUT.read_bytes()), cases=len(rows), unique_providers=len({r["origin_firm"].strip() for r in rows}),
                   original_human_decisions=0, key_opened=False, prompt_version=PROMPT_VERSION, seed=20261021,
                   started_utc=now(), baseline_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip())
    path = PRIVATE / "preflight.json"
    if path.exists():
        old = json.loads(path.read_text())
        if old["blind_input_sha256"] != summary["blind_input_sha256"]:
            raise ValueError("Blinded input changed since checkpoint")
    else:
        path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "blind_input_sha256"}, indent=2))


def retrieve(source):
    """One ordinary request; do not retry denied access. All payloads remain ignored."""
    PRIVATE.mkdir(parents=True, exist_ok=True)
    folder = PRIVATE / "sources"
    folder.mkdir(exist_ok=True)
    source_id = source["source_id"]
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", source_id):
        raise ValueError("Unsafe source identifier")
    parsed = urllib.parse.urlparse(source["url"])
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Source URL must be a public HTTP(S) URL without credentials")
    meta = folder / (source_id + ".json")
    payload = folder / (source_id + ".bin")
    if meta.exists():
        cached = json.loads(meta.read_text(encoding="utf-8"))
        if cached.get("source_sha256") and sha(payload.read_bytes()) != cached["source_sha256"]:
            raise ValueError("Cached source hash changed")
        return cached
    result = dict(source, checked_at_utc=now(), access_status="", http_status="", bytes=0, source_sha256="")
    if source.get("cached_reading_copy"):
        old = ROOT / source["cached_reading_copy"]
        old.resolve().relative_to((ROOT / "research_completion/phase3/private_runtime").resolve())
        data = old.read_bytes()
        if source.get("expected_sha256") and sha(data) != source["expected_sha256"]:
            raise ValueError("Existing reading-copy checksum differs")
        payload.write_bytes(data)
        result.update(access_status="CACHED_ORIGINAL_BYTES", bytes=len(data), source_sha256=sha(data), checksum_kind="ORIGINAL_BYTES")
        meta.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result
    try:
        req = urllib.request.Request(source["url"], headers={"User-Agent": "R01-historical-documentary-research/1.0"})
        with urllib.request.urlopen(req, timeout=25) as response:
            data = response.read(25_000_001)
            result["http_status"] = response.status
            result["resolved_url"] = response.url
            result["content_type"] = response.headers.get("Content-Type", "")
        if len(data) > 25_000_000:
            raise ValueError("Document exceeds bounded 25MB reading-copy limit")
        payload.write_bytes(data)
        result.update(access_status="RETRIEVED_ORIGINAL_BYTES", bytes=len(data), source_sha256=sha(data), checksum_kind="ORIGINAL_BYTES")
    except (urllib.error.URLError, TimeoutError, ValueError, ConnectionError) as error:
        result.update(access_status="FAILED_NO_BYPASS", http_status=getattr(error, "code", ""), error=str(error))
    meta.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def audit_proposal(case, proposal, source_rows):
    """Adversarial machine audit; never an independent human/rater assessment."""
    reasons = []
    grade = proposal["proposed_grade"]
    status = proposal["proposed_status"]
    if grade not in {"A", "B", "C", "D"} or status not in STATUSES:
        raise ValueError("Invalid machine proposal")
    if not source_rows and grade != "D":
        reasons.append("No cited documentary evidence; grade downgraded")
        grade = "D"
    evidence = [r for r in source_rows if r.get("access_status", "").startswith(("RETRIEVED", "BROWSER_PARSED", "CACHED"))]
    if not evidence and grade != "D":
        reasons.append("No accessible source supports the proposed grade")
        grade = "D"
    partial = any(r.get("provider_scope") == "EXACT_PROVIDER" and r.get("corridor_scope") == "EXACT_ORDERED_CORRIDOR"
                  and r.get("document_date") and (r.get("origin_coverage") in {"EXPLICIT_FULL_PERIOD", "PARTIAL_NEAR_PERIOD"}
                  or r.get("target_coverage") in {"EXPLICIT_FULL_PERIOD", "PARTIAL_NEAR_PERIOD"}) for r in evidence)
    if grade == "B" and not partial:
        reasons.append("B lacks dated near-period provider and ordered-corridor support")
        grade = "C" if evidence else "D"
    full = any(r.get("origin_coverage") == "EXPLICIT_FULL_PERIOD" and r.get("target_coverage") == "EXPLICIT_FULL_PERIOD"
               and r.get("corridor_scope") == "EXACT_ORDERED_CORRIDOR" and r.get("provider_scope") == "EXACT_PROVIDER"
               and r.get("bundle_scope") == "FULL_BUNDLE" for r in evidence)
    if grade == "A" and not full:
        reasons.append("A requires exact bundle, provider, corridor and both-period coverage")
        grade = "C" if evidence else "D"
    if status == "EVIDENCE_SUPPORTS_SAME":
        if grade != "A" or not full or int(case["target_multiplicity"]) != 1 or proposal.get("unresolved_alternative", True):
            reasons.append("Same-product support fails specificity, temporal or uniqueness requirements")
            status = UNRESOLVED
    if status == "EVIDENCE_SUPPORTS_DIFFERENT":
        direct = proposal.get("direct_dated_distinct_products", False)
        if not direct or not full:
            reasons.append("Missing key, vocabulary change or corporate event is not direct distinct-product evidence")
            status = UNRESOLVED
    if status.startswith("EVIDENCE_SUPPORTS") and proposal.get("material_contradiction", False):
        reasons.append("Material documentary contradiction remains unresolved")
        status = UNRESOLVED
    if not reasons:
        reasons.append("Scope/temporal/alternative checks retain proposal; this does not validate identity")
    return dict(machine_status=status, support_grade=grade, adversarial_machine_audit="; ".join(reasons),
                independent_human_validation=False)


def assess_and_freeze():
    rows = load_blind()
    proposals_path = PRIVATE / "pass1_proposals.json"
    evidence_path = PRIVATE / "case_source_log.csv"
    proposals = json.loads(proposals_path.read_text(encoding="utf-8"))
    evidence = read_csv(evidence_path)
    ids = {row["case_id"] for row in rows}
    if len(proposals) != 60 or {r["case_id"] for r in proposals} != ids:
        raise ValueError("Every blinded case needs exactly one proposal")
    if not evidence or not set(SOURCE_FIELDS).issubset(evidence[0]) or {r["case_id"] for r in evidence} != ids:
        raise ValueError("Case-source ledger schema or IDs invalid")
    source_manifest = json.loads((PRIVATE / "source_manifest.json").read_text(encoding="utf-8"))
    sources_by_id = {s["source_id"]: s for s in source_manifest}
    if len(sources_by_id) != len(source_manifest):
        raise ValueError("Duplicate source identifiers")
    for source in source_manifest:
        if source.get("source_sha256"):
            payload = PRIVATE / source["reading_copy"] if source.get("reading_copy") else PRIVATE / "sources" / (source["source_id"] + ".bin")
            payload.resolve().relative_to(PRIVATE.resolve())
            if sha(payload.read_bytes()) != source["source_sha256"]:
                raise ValueError("Source reading-copy hash differs")
    for row in evidence:
        source = sources_by_id[row["source_id"]]
        if any(row[field] != str(source.get(field, "")) for field in ["url", "source_sha256", "access_status"]):
            raise ValueError("Ledger/source manifest differs")
    lookup = {r["case_id"]: r for r in proposals}
    output = []
    for case in rows:
        proposal = lookup[case["case_id"]]
        sources = [r for r in evidence if r["case_id"] == case["case_id"]]
        decision = audit_proposal(case, proposal, sources)
        output.append(dict(case_id=case["case_id"], **decision, proposed_grade=proposal["proposed_grade"],
                           proposed_status=proposal["proposed_status"], cited_sources=";".join(sorted({r["source_id"] for r in sources})),
                           source_based_reasoning=proposal["source_based_reasoning"], counterargument=proposal["counterargument"],
                           best_alternative=proposal["best_alternative"], alternative_rejection_reason=proposal["alternative_rejection_reason"],
                           evidence_limitations=proposal["evidence_limitations"], assessment_kind="AI_DOCUMENTARY_PLAUSIBILITY_NOT_GROUND_TRUTH"))
    target = PRIVATE / "case_evidence.csv"
    frozen = PRIVATE / "machine_review_frozen.json"
    if frozen.exists():
        raise ValueError("Frozen machine ledger exists; preserve it and use an explicit revision")
    write_csv(target, output)
    manifest = dict(frozen_at_utc=now(), script_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                    script_sha256=sha(Path(__file__).read_bytes()), prompt_version=PROMPT_VERSION, seed=20261021, case_count=60,
                    blind_input_sha256=sha(INPUT.read_bytes()), evidence_table_sha256=sha(target.read_bytes()),
                    case_source_log_sha256=sha(evidence_path.read_bytes()), pass1_proposals_sha256=sha(proposals_path.read_bytes()),
                    statuses=[dict(case_id=r["case_id"], machine_status=r["machine_status"], support_grade=r["support_grade"]) for r in output],
                    source_manifest_sha256=sha((PRIVATE / "source_manifest.json").read_bytes()),
                    key_opened_before_freeze=False, human_adjudications=0, external_validation=False)
    manifest["methods_sha256"] = sha((HERE / "EVIDENCE_METHODS.md").read_bytes())
    manifest["annotation_provenance_sha256"] = sha((PRIVATE / "annotation_provenance.json").read_bytes())
    manifest["private_annotation_script_sha256"] = sha((PRIVATE / "prepare_private.py").read_bytes())
    frozen.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (PRIVATE / "machine_review_frozen.sha256").write_text(sha(frozen.read_bytes()) + "\n", encoding="ascii")
    public = dict(case_count=60, status_counts=dict(Counter(r["machine_status"] for r in output)),
                  grade_counts=dict(Counter(r["support_grade"] for r in output)),
                  frozen_manifest_sha256=sha(frozen.read_bytes()), evidence_table_sha256=manifest["evidence_table_sha256"],
                  script_commit=manifest["script_commit"], human_adjudications=0, external_validation=False)
    (HERE / "freeze_integrity_summary.json").write_text(json.dumps(public, indent=2), encoding="utf-8")
    print(json.dumps(public, indent=2))


def verify_freeze():
    path = PRIVATE / "machine_review_frozen.json"
    if sha(path.read_bytes()) != (PRIVATE / "machine_review_frozen.sha256").read_text().strip():
        raise ValueError("Frozen manifest changed")
    frozen = json.loads(path.read_text())
    if sha(INPUT.read_bytes()) != frozen["blind_input_sha256"]:
        raise ValueError("Original blinded input changed")
    for filename, field in [("case_evidence.csv", "evidence_table_sha256"), ("case_source_log.csv", "case_source_log_sha256"),
                            ("pass1_proposals.json", "pass1_proposals_sha256"), ("source_manifest.json", "source_manifest_sha256")]:
        if sha((PRIVATE / filename).read_bytes()) != frozen[field]:
            raise ValueError("Frozen evidence input changed: " + filename)
    return frozen


def unblind():
    frozen = verify_freeze()
    evidence = read_csv(PRIVATE / "case_evidence.csv")
    # This is the first and only stage permitted to read the separate stratum key.
    key = read_csv(ROOT / "research_completion/phase3/private_runtime/IDENTITY_REVIEW_KEY.csv")
    labels = {r["case_id"]: r["stratum"] for r in key}
    if len(labels) != 60 or set(labels) != {r["case_id"] for r in evidence}:
        raise ValueError("Stratum key/case IDs do not reconcile")
    counts = Counter((labels[r["case_id"]], r["machine_status"], r["support_grade"]) for r in evidence)
    output = [dict(sampled_stratum=s, machine_status=status, support_grade=grade, cases=n,
                   interpretation="DOCUMENTATION_FEASIBILITY_NOT_MATCHING_ACCURACY") for (s, status, grade), n in sorted(counts.items())]
    assert sum(r["cases"] for r in output) == frozen["case_count"]
    write_csv(HERE / "AUTOMATED_FINDINGS_AGGREGATED.csv", output)
    write_csv(PRIVATE / "postfreeze_stratum_cases.csv", [dict(row, sampled_stratum=labels[row["case_id"]]) for row in evidence])
    (PRIVATE / "unblinding_event.json").write_text(json.dumps(dict(unblinded_at_utc=now(), freeze_verified=True,
         frozen_manifest_sha256=sha((PRIVATE / "machine_review_frozen.json").read_bytes()), key_sha256=sha((ROOT / "research_completion/phase3/private_runtime/IDENTITY_REVIEW_KEY.csv").read_bytes())), indent=2), encoding="utf-8")
    print(json.dumps(dict(unblinded_cases=60, sampled_strata=len(set(labels.values())), public_cells=len(output))))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["init", "acquire", "freeze", "unblind", "_one_source"])
    parser.add_argument("--source-id")
    args = parser.parse_args()
    if args.stage == "_one_source":
        registry = json.loads((PRIVATE / "source_registry.json").read_text(encoding="utf-8"))
        retrieve(next(source for source in registry if source["source_id"] == args.source_id))
    elif args.stage == "acquire":
        if (PRIVATE / "machine_review_frozen.json").exists():
            raise ValueError("Do not mutate frozen source manifest; use a separate revision")
        registry = json.loads((PRIVATE / "source_registry.json").read_text(encoding="utf-8"))
        manifest = []
        for source in registry:
            meta = PRIVATE / "sources" / (source["source_id"] + ".json")
            if not meta.exists():
                # Socket timeouts alone do not bound slow responses or DNS resolution.
                started = now()
                try:
                    subprocess.run([sys.executable, str(Path(__file__)), "_one_source", "--source-id", source["source_id"]],
                                   check=True, timeout=60)
                except subprocess.TimeoutExpired:
                    meta.write_text(json.dumps(dict(source, checked_at_utc=started, access_status="TIMEOUT_NO_RETRY",
                         http_status="", bytes=0, source_sha256="", error="60-second total acquisition deadline"), indent=2), encoding="utf-8")
                except subprocess.CalledProcessError as error:
                    meta.write_text(json.dumps(dict(source, checked_at_utc=started, access_status="FAILED_SOURCE_PROCESS",
                         http_status="", bytes=0, source_sha256="", error=str(error)), indent=2), encoding="utf-8")
            result = json.loads(meta.read_text(encoding="utf-8"))
            if result.get("source_sha256"):
                assert sha(meta.with_suffix(".bin").read_bytes()) == result["source_sha256"]
            manifest.append(result)
            print(json.dumps(dict(source_id=source["source_id"], access_status=result["access_status"])), flush=True)
        (PRIVATE / "source_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(json.dumps(dict(sources=len(manifest), statuses=dict(Counter(r["access_status"] for r in manifest))), indent=2))
    else:
        {"init": init, "freeze": assess_and_freeze, "unblind": unblind}[args.stage]()
