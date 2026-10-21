"""Bounded source retrieval and aggregate-only follow-up; no fitting or key access."""
import argparse
import csv
import hashlib
import html
import json
from pathlib import Path
import shutil
import time
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent
PHASE3 = HERE.parent
PRIVATE = PHASE3 / "private_runtime" / "followup_20261021"

SOURCES = {
    "lim_author": "https://singapore.to/research/ssrn-6830281/",
    "author_public_repositories": "https://api.github.com/users/boonchuan/repos?per_page=100",
    "rpw_methodology": "https://remittanceprices.worldbank.org/methodology",
    "rpw_2020q4": "https://remittanceprices.worldbank.org/sites/default/files/rpw_main_report_and_annex_q42020.pdf",
    "rpw_2021q1": "https://remittanceprices.worldbank.org/sites/default/files/rpw_main_report_and_annex_q121_final.pdf",
    "rpw_2021q2": "https://remittanceprices.worldbank.org/sites/default/files/rpw_main_report_and_annex_q221.pdf",
    "rpw_2022q4": "https://remittanceprices.worldbank.org/sites/default/files/rpw_main_report_and_annex_q422_final.pdf",
    "rpw_2021q2_academic_mirror": "https://courseapps.studyonline.unsw.edu.au/media/unsw/course/ZZBU8508/pdfs/WorldBank_Remittance_Prices_Worldwide-main_report_and_annex_q221.pdf",
}

# Author-linked public GitHub account, ordinary API tree discovery on 21 October.
# Fix the reading copy to its observed commit rather than mutable main.
LIM_COMMIT = "c370a619edac2545291a5a30b8d2d035f7c79f3a"
LIM_FILES = {
    "lim_fulltext": "paper/digital-discount-v1_1.md",
    "lim_replication_code": "code/replicate.py",
    "lim_regression_results": "output/regression_results.json",
    "lim_robustness_results": "output/robustness_results.json",
    "lim_repository_readme": "README.md",
    "lim_data_readme": "data/README.md",
    "lim_citation": "CITATION.cff",
    "lim_license": "LICENSE",
}
SOURCES.update({name: f"https://raw.githubusercontent.com/boonchuan/digital-channel-discount/{LIM_COMMIT}/{path}"
                for name, path in LIM_FILES.items()})


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def acquire():
    """One ordinary request per listed source; cached bytes are not fetched again."""
    PRIVATE.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, url in SOURCES.items():
        path = PRIVATE / (name + (".pdf" if url.endswith(".pdf") else ".source"))
        meta = path.with_suffix(path.suffix + ".json")
        if meta.exists():
            cached = json.loads(meta.read_text(encoding="utf-8"))
            if cached["status"] == "RETRIEVED_PRIVATE_COPY":
                if not path.exists() or digest(path.read_bytes()) != cached["sha256"]:
                    raise ValueError(f"Cached reading-copy hash differs: {name}; no automatic replacement")
            rows.append(cached)
            continue
        started = time.perf_counter()
        row = dict(source_id=name, url=url, retrieved_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   status="", http_status="", bytes=0, sha256="", elapsed_s=0, note="")
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "R01-public-research-audit/1.0"})
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read(20_000_001)
                row["http_status"] = response.status
            if len(data) > 20_000_000:
                raise ValueError("Source exceeds this bounded review's 20MB limit")
            if url.endswith(".pdf") and not data.startswith(b"%PDF"):
                raise ValueError("Response is not a PDF")
            path.write_bytes(data)
            row.update(status="RETRIEVED_PRIVATE_COPY", bytes=len(data), sha256=digest(data))
        except (urllib.error.URLError, TimeoutError, ValueError) as error:
            row.update(status="UNAVAILABLE_NO_RETRY", http_status=getattr(error, "code", ""), note=str(error))
        row["elapsed_s"] = round(time.perf_counter() - started, 3)
        meta.write_text(json.dumps(row, indent=2), encoding="utf-8")
        rows.append(row)
    write_csv(HERE / "source_acquisition.csv", rows)
    print(json.dumps(rows, indent=2))


def aggregate():
    with (PHASE3 / "tables" / "wave_measurement.csv").open(encoding="utf-8-sig", newline="") as stream:
        waves = list(csv.DictReader(stream))
    grouped = {}
    for row in waves:
        if row["scenario"] in {"cc1_3pct_core", "cc1_3pct_strict"}:
            grouped.setdefault(row["quarter"], {})[row["scenario"]] = row
    output = []
    for quarter, scenarios in sorted(grouped.items()):
        core = scenarios["cc1_3pct_core"]
        strict = scenarios["cc1_3pct_strict"]
        n, nc, ns, sc, ss = (int(float(x)) for x in
                             [core["n"], core["valid"], strict["valid"], core["s"], strict["s"]])
        assert n == int(float(strict["n"])) and 0 <= ss <= sc and 0 <= ns <= nc <= n
        changed, changed_stay = nc - ns, sc - ss
        assert 0 <= changed_stay <= changed
        output.append(dict(quarter=quarter, n_eligible=n, n_core_valid=nc, n_unchanged_valid=ns,
                           n_changed_valid=changed, unchanged_stay=ss, changed_stay=changed_stay,
                           unchanged_continuity=ss / ns if ns else "",
                           changed_continuity=changed_stay / changed if changed else "",
                           core_unknown_share=(n - nc) / n,
                           strict_unknown_share=(n - ns) / n, width_difference=changed / n))
    write_csv(HERE / "attribute_change_by_wave.csv", output)
    totals = {key: sum(row[key] for row in output) for key in
              ["n_eligible", "n_core_valid", "n_unchanged_valid", "n_changed_valid", "unchanged_stay", "changed_stay"]}
    assert totals == dict(n_eligible=45343, n_core_valid=36429, n_unchanged_valid=30570,
                          n_changed_valid=5859, unchanged_stay=24776, changed_stay=4770)
    totals.update(unchanged_continuity=totals["unchanged_stay"] / totals["n_unchanged_valid"],
                  changed_continuity=totals["changed_stay"] / totals["n_changed_valid"],
                  changed_share_all_origins=totals["n_changed_valid"] / totals["n_eligible"],
                  changed_share_core_valid=totals["n_changed_valid"] / totals["n_core_valid"])
    write_csv(HERE / "attribute_change_pooled.csv", [totals])
    print(json.dumps(totals, indent=2))


REVIEW_FIELDS = ["case_id", "human_identity_decision", "supporting_document", "document_locator",
                 "evidence_origin_date", "evidence_target_date", "historical_evidence_scope",
                 "reviewer", "review_date", "reason"]
DECISIONS = {"SAME_BUNDLE", "DIFFERENT_BUNDLE", "UNRESOLVED", "NOT_REVIEWABLE"}


def validate_decisions(rows, expected_ids):
    """Internal completeness only; source contents still need human adjudication."""
    ids = [row.get("case_id", "") for row in rows]
    if len(ids) != len(set(ids)) or set(ids) != set(expected_ids):
        raise ValueError("Missing, unexpected or duplicate case IDs")
    counts = {decision: 0 for decision in sorted(DECISIONS)}
    counts["PENDING"] = 0
    import datetime
    for row in rows:
        decision = row.get("human_identity_decision", "").strip()
        if not decision:
            counts["PENDING"] += 1
            continue
        if decision not in DECISIONS:
            raise ValueError("Invalid identity decision")
        if not all(row.get(field, "").strip() for field in ["reviewer", "review_date", "reason"]):
            raise ValueError("Decision requires reviewer, review date and reason")
        datetime.date.fromisoformat(row["review_date"])
        if decision in {"SAME_BUNDLE", "DIFFERENT_BUNDLE"}:
            required = ["supporting_document", "document_locator", "evidence_origin_date",
                        "evidence_target_date", "historical_evidence_scope"]
            if not all(row.get(field, "").strip() for field in required):
                raise ValueError("A resolved decision requires documented historical evidence for both periods")
        counts[decision] += 1
    return dict(counts=counts, complete=counts["PENDING"] == 0,
                external_evidence_verified_by_code=False, population_error_rate_identified=False)


def reviewer_html(cases, role):
    """Offline casebook: no prices, key, automatic match judgment or network code."""
    cards = []
    fields = ["firm", "payment instrument", "access point", "pickup method", "pickup location",
              "speed actual", "receiving network coverage"]
    for row in cases:
        q = row["origin_quarter"]
        y, quarter = int(q[:4]), int(q[-1])
        target_q = f"{y + (quarter == 4)}Q{quarter % 4 + 1}"
        attributes = "".join("<tr><th>" + html.escape(field) + "</th><td>" +
                             html.escape(row.get("origin_" + field, "")) + "</td><td>" +
                             html.escape(row.get("target_" + field, "")) + "</td></tr>" for field in fields)
        alternatives = ""
        for i in range(1, 4):
            prefix = f"alternative_{i}_"
            if row.get(prefix + "source_row", ""):
                alternatives += "<p><b>Candidate " + str(i) + "</b>: " + " | ".join(
                    html.escape(field + ": " + row.get(prefix + field, "")) for field in fields) + "</p>"
        inputs = []
        for field in REVIEW_FIELDS[1:]:
            label = html.escape(field.replace("_", " "))
            if field == "human_identity_decision":
                control = '<select data-field="' + field + '"><option value="">Pending</option>' + "".join(
                    '<option>' + decision + '</option>' for decision in sorted(DECISIONS)) + '</select>'
            else:
                control = '<textarea rows="2" data-field="' + field + '"></textarea>'
            inputs.append('<label>' + label + control + '</label>')
        cards.append('<details data-case="' + html.escape(row["case_id"]) + '"><summary>' +
                     html.escape(row["case_id"] + " | " + q + " to " + target_q + " | " + row["corridor"]) +
                     '</summary><table><thead><tr><th>Attribute</th><th>Origin</th><th>Recorded target</th></tr></thead><tbody>' +
                     attributes + '</tbody></table><p>Target multiplicity: ' + html.escape(row["target_multiplicity"]) +
                     '. Blank fields mean missing information.</p>' + alternatives + '<div class="inputs">' +
                     ''.join(inputs) + '</div></details>')
    template = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>R01 blinded identity review - ROLE</title><style>
body{font:16px system-ui;max-width:1100px;margin:30px auto;padding:0 20px;color:#173047;background:#f5f7fa}
header,details{background:white;padding:18px;margin:12px 0;border:1px solid #ced8e0;border-radius:8px}
summary{cursor:pointer;font-weight:700}table{border-collapse:collapse;width:100%;margin-top:14px}td,th{border:1px solid #ccd5df;text-align:left;padding:8px;overflow-wrap:anywhere}
.inputs{display:grid;grid-template-columns:1fr 1fr;gap:14px}label{display:block;font-weight:600}textarea,select{display:block;width:100%;box-sizing:border-box;margin-top:5px;font:inherit}button{padding:10px;margin:5px;background:#123c59;color:white;border:0;border-radius:4px;cursor:pointer}
@media(max-width:650px){.inputs{grid-template-columns:1fr}}.toolbar{position:sticky;top:0;background:#f5f7fa;padding:8px;z-index:1}</style>
<header><h1>Blinded identity review - ROLE</h1><p>60 cases. No outcome prices or stratum key. Read START_HERE.md first. The original CSV retains source-row references.</p>
<p>Judge historical comparability of the full offer. SAME_BUNDLE and DIFFERENT_BUNDLE require evidence applying to both periods. With insufficient evidence choose UNRESOLVED; use NOT_REVIEWABLE if the case cannot be assessed and explain why. Matching labels alone are insufficient.</p>
<p>Evidence dates may be ISO dates or documented quarter intervals. Review date must be YYYY-MM-DD. Name the document, URL, exact page or section, and which attributes and periods it supports. Partial documentary support does not establish full identity.</p></header>
<div class="toolbar"><b id="progress"></b><button id="download">Download decisions CSV</button><button id="backup">Download checkpoint JSON</button><label>Restore checkpoint JSON <input id="restore" type="file" accept="application/json,.json"></label><span id="status"></span></div>
CARDS
<script>
const fields=FIELDS, role="ROLE", storageKey="r01-identity-followup-20261021-"+role;
const cards=Array.from(document.querySelectorAll('details[data-case]'));
function rows(){return cards.map(card=>{let r={case_id:card.dataset.case};card.querySelectorAll('[data-field]').forEach(e=>r[e.dataset.field]=e.value);return r})}
function progress(){document.getElementById('progress').textContent=rows().filter(r=>r.human_identity_decision).length+' / 60 decisions recorded';}
function apply(data){if(!Array.isArray(data)||data.length!==cards.length||new Set(data.map(r=>r.case_id)).size!==cards.length||data.some(r=>!cards.some(c=>c.dataset.case===r.case_id)))throw Error('Checkpoint has unexpected case IDs');const byId=new Map(data.map(r=>[r.case_id,r]));cards.forEach(c=>c.querySelectorAll('[data-field]').forEach(e=>e.value=byId.get(c.dataset.case)[e.dataset.field]||''));progress();}
function save(){progress();try{localStorage.setItem(storageKey,JSON.stringify(rows()));document.getElementById('status').textContent='Saved in this browser; also download a checkpoint.'}catch(e){document.getElementById('status').textContent='Browser storage unavailable; download a checkpoint.'}}
function download(text,name,type){let blob=new Blob([text],{type}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);}
document.getElementById('download').onclick=()=>{const quote=v=>'"'+String(v||'').replaceAll('"','""')+'"';let data=[fields,...rows().map(r=>fields.map(f=>r[f]))];download(data.map(r=>r.map(quote).join(',')).join('\\r\\n')+'\\r\\n','R01_'+role+'_DECISIONS.csv','text/csv;charset=utf-8');};
document.getElementById('backup').onclick=()=>download(JSON.stringify(rows(),null,2),'R01_'+role+'_CHECKPOINT.json','application/json');
document.getElementById('restore').onchange=async e=>{try{apply(JSON.parse(await e.target.files[0].text()));save()}catch(err){document.getElementById('status').textContent='Restore failed: '+err.message}};
document.addEventListener('input',save);document.addEventListener('change',save);
try{const stored=localStorage.getItem(storageKey);if(stored)apply(JSON.parse(stored));}catch(e){}progress();
</script></html>'''
    return template.replace("CARDS", "".join(cards)).replace("FIELDS", json.dumps(REVIEW_FIELDS)).replace("ROLE", role)


def prepare_review():
    source = PHASE3 / "private_runtime" / "BLINDED_IDENTITY_REVIEW.csv"
    with source.open(encoding="utf-8-sig", newline="") as stream:
        cases = list(csv.DictReader(stream))
    assert len(cases) == len({r["case_id"] for r in cases}) == 60
    assert not any(any(token in field.lower() for token in ["cost", "price", "stratum"])
                   for field in cases[0])
    assert all(not row["human_identity_decision"] for row in cases)
    pack = PRIVATE / "reviewer_pack"
    pack.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, pack / "BLINDED_CASES.csv")
    shutil.copyfile(HERE / "REVIEWER_INSTRUCTIONS.md", pack / "START_HERE.md")
    for role in ["Reviewer_A", "Reviewer_B"]:
        target = pack / role
        target.mkdir(exist_ok=True)
        decisions = [{field: row["case_id"] if field == "case_id" else "" for field in REVIEW_FIELDS} for row in cases]
        path = target / "REVIEW_DECISIONS.csv"
        # Never overwrite a human's existing decisions or casebook.
        if not path.exists():
            write_csv(path, decisions)
        html_path = target / "REVIEWER.html"
        if not html_path.exists():
            html_path.write_text(reviewer_html(cases, role), encoding="utf-8")
    report = dict(prepared_cases=60, prepared_independent_blank_forms=2, assigned_first_reviewer="Investigator (self-designated)",
                  assigned_second_reviewer=False, original_human_decisions=0, key_opened_by_followup=False,
                  outcome_columns_in_review_pack=False, adjudications_completed=False)
    (HERE / "identity_preparation_status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["acquire", "aggregate", "prepare_review", "validate_review"])
    parser.add_argument("--decisions", type=Path)
    args = parser.parse_args()
    if args.stage == "validate_review":
        if not args.decisions:
            parser.error("--decisions is required")
        with args.decisions.open(encoding="utf-8-sig", newline="") as stream:
            returned = list(csv.DictReader(stream))
        expected = [f"R01P3-{i:03d}" for i in range(1, 61)]
        print(json.dumps(validate_decisions(returned, expected), indent=2))
    else:
        {"acquire": acquire, "aggregate": aggregate, "prepare_review": prepare_review}[args.stage]()
