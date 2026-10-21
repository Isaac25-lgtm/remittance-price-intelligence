"""Private text extraction from completed reading-copy checkpoints, one document at a time."""
import argparse
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PRIVATE = ROOT / "research_completion/phase3/private_runtime/followup_20261021/autonomous_review"


def extract():
    from bs4 import BeautifulSoup
    from pypdf import PdfReader
    source_dir = PRIVATE / "sources"
    output = PRIVATE / "extracted"
    output.mkdir(exist_ok=True)
    rows = []
    for meta in sorted(source_dir.glob("s*.json")):
        source = json.loads(meta.read_text(encoding="utf-8"))
        payload = meta.with_suffix(".bin")
        if not payload.exists() or not source.get("source_sha256"):
            continue
        raw = payload.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == source["source_sha256"]
        target = output / (source["source_id"] + ".txt")
        status = "EXTRACTED_TEXT_NOT_INDEPENDENT_FACT_CHECK"
        pages = None
        try:
            if not target.exists():
                if raw.startswith(b"%PDF"):
                    reader = PdfReader(payload)
                    pages = len(reader.pages)
                    text = "\n\n".join(f"[PDF PAGE {i+1}]\n" + (page.extract_text() or "") for i, page in enumerate(reader.pages))
                else:
                    soup = BeautifulSoup(raw, "html.parser")
                    for node in soup(["script", "style", "noscript", "svg"]):
                        node.decompose()
                    text = soup.get_text("\n", strip=True)
                target.write_text(text, encoding="utf-8")
            data = target.read_bytes()
            if len(data.strip()) < 50:
                status = "LITTLE_OR_NO_EXTRACTABLE_TEXT"
            rows.append(dict(source_id=source["source_id"], status=status, text_sha256=hashlib.sha256(data).hexdigest(),
                             text_bytes=len(data), pdf_pages=pages))
        except Exception as error:
            rows.append(dict(source_id=source["source_id"], status="EXTRACTION_FAILED", error=type(error).__name__ + ": " + str(error)))
    (PRIVATE / "text_extraction_manifest.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(json.dumps(dict(completed_source_texts=len(rows), failures=[r for r in rows if r["status"] == "EXTRACTION_FAILED"]), indent=2))


def snippets(ids):
    # Local reading aid only. Do not publish corporate/case-level source excerpts.
    for name in ids:
        path = PRIVATE / "extracted" / (name + ".txt")
        if not path.exists():
            print(name, "NOT_YET_EXTRACTED")
            continue
        text = path.read_text(encoding="utf-8")
        print("\nSOURCE", name, "characters", len(text))
        patterns = {"s018": ["M1 Remit"], "s042": ["25/09/2023", "Egitto", "Carte prepagata", "Carta prepagata"],
                    "s014": ["2017", "BLIZKO"], "s027": ["2017", "India"], "s023": ["29 April 2021", "DBS"],
                    "s031": ["Lebara"], "s048": ["CIBAO"], "s034": ["Myanmar"], "s035": ["Ficohsa Express"],
                    "s033": ["Our mission", "transfer"], "s001": ["Our Business", "Express", "Economy"],
                    "s003": ["Our Business", "Digital Channel"], "s007": ["Services", "Digital money transfer"]}
        found = 0
        for pattern in patterns.get(name, ["remittance", "money transfer", "transfer", "2021", "2024"]):
            hits = list(re.finditer(re.escape(pattern), text, flags=re.IGNORECASE))
            if hits:
                # Last occurrences can be legal boilerplate; use first substantive matches, report page markers.
                for match in hits[:2]:
                    position = match.start()
                    page = text[:position].rsplit("[PDF PAGE ", 1)[-1].split("]", 1)[0] if "[PDF PAGE " in text[:position] else "HTML"
                    print("locator", page, "keyword", pattern)
                    print(text[max(0, position-220):position+850])
                    found += 1
                    if found >= 4:
                        break
            if found >= 4:
                break
        if not found:
            print(text[:1100])


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["extract", "snippets"])
    parser.add_argument("ids", nargs="*")
    args = parser.parse_args()
    extract() if args.stage == "extract" else snippets(args.ids)
