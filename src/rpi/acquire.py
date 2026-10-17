"""Lawful fetch of the official RPW workbook with checksum + manifest.

Usage: python -m rpi.acquire [--force]
The workbook is stored under data/raw/ (gitignored) and is never committed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone

from . import config

MANIFEST = config.RESULTS_DIR / "source_manifest.json"


def sha256(path, chunk=1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def fetch(url: str = config.SOURCE_URL, dest=config.RAW_FILE, timeout: int = 300) -> dict:
    """Single bounded attempt (no retry storm). Returns response metadata."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".part")
    req = urllib.request.Request(url, headers={"User-Agent": "rpi-research/0.1 (academic, non-commercial)"})
    with urllib.request.urlopen(req, timeout=timeout) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(r, f)
        headers = {k.lower(): v for k, v in r.headers.items()}
        status = r.status
    tmp.replace(dest)
    return {"http_status": status, "last_modified": headers.get("last-modified"),
            "etag": headers.get("etag"), "content_length": headers.get("content-length"),
            "x_ms_version_id": headers.get("x-ms-version-id")}


def git_head() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=config.ROOT, text=True).strip()
    except Exception:
        return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)
    meta = {}
    if args.force or not config.RAW_FILE.exists():
        meta = fetch()
    digest = sha256(config.RAW_FILE)
    size = config.RAW_FILE.stat().st_size
    ok = digest == config.EXPECTED_SHA256 and size == config.EXPECTED_BYTES
    prev = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    manifest = {
        **prev,
        "source_url": config.SOURCE_URL,
        "catalogue_url": config.CATALOGUE_URL,
        "license_catalogue": "CC BY 4.0 (as stated on the World Bank Data Catalog page)",
        "license_workbook_terms": (
            "Workbook 'Terms of Use' sheet: free reuse with attribution 'The World Bank, Remittance "
            "Prices Worldwide, available at http://remittanceprices.worldbank.org'; links to a World Bank "
            "'Restricted Data' list. Row-level data are therefore not redistributed in this repository."),
        "bytes": size,
        "sha256": digest,
        "matches_frozen_checksum": ok,
        "verified_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "code_commit": git_head(),
    }
    if meta:
        manifest["http"] = meta
    config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
