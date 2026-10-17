"""Raw-to-result reproduction from the CACHED official workbook (no download).

1. Verify cached workbook sha256 against the frozen checksum (abort if absent/mismatch).
2. Snapshot the committed (frozen) result tables.
3. Re-run the full pipeline: workbook -> parquet -> audit -> models lag0/lag1 -> descriptive -> subgroups.
4. Compare every regenerated table with its frozen counterpart (numeric tolerance).
5. Restore the frozen tables (committed results are never silently overwritten); regenerated
   copies are kept under data/processed/repro_outputs/ (gitignored).
Writes results/reproduction/{reproduction_report.json, table_comparison.csv}.

Usage: python scripts/reproduce_from_cache.py
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from rpi import config
from rpi.acquire import sha256

ATOL, RTOL = 1e-9, 1e-9
VOLATILE_JSON_KEYS = {"code_commit", "wall_seconds", "verified_at_utc"}
OUT = config.RESULTS_DIR / "reproduction"
SNAP = config.PROCESSED_DIR / "frozen_tables_snapshot"
REGEN = config.PROCESSED_DIR / "repro_outputs"
STEPS = [
    ["python", "-c", "from rpi.preprocess import load_clean; load_clean(rebuild=True)"],
    ["python", "-m", "rpi.audit"],
    ["python", "scripts/run_phase1.py", "--release-lag", "0"],
    ["python", "scripts/run_phase1.py", "--release-lag", "1"],
    ["python", "scripts/run_descriptive.py"],
    ["python", "scripts/subgroup_metrics.py"],
]


def compare_csv(a: Path, b: Path) -> dict:
    x, y = pd.read_csv(a), pd.read_csv(b)
    r = {"file": a.name, "kind": "csv", "rows_frozen": len(x), "rows_regenerated": len(y),
         "same_columns": list(x.columns) == list(y.columns), "max_abs_diff": 0.0, "text_mismatches": 0}
    if not r["same_columns"] or len(x) != len(y):
        r["status"] = "STRUCTURE_DIFFERS"
        return r
    for c in x.columns:
        if pd.api.types.is_numeric_dtype(x[c]) and pd.api.types.is_numeric_dtype(y[c]):
            xa, ya = x[c].to_numpy(float), y[c].to_numpy(float)
            both_nan = np.isnan(xa) & np.isnan(ya)
            if (np.isnan(xa) != np.isnan(ya)).any():
                r["text_mismatches"] += int((np.isnan(xa) != np.isnan(ya)).sum())
            d = np.abs(xa - ya)[~both_nan & ~np.isnan(xa) & ~np.isnan(ya)]
            if d.size:
                r["max_abs_diff"] = max(r["max_abs_diff"], float(d.max()))
                if not np.allclose(xa[~both_nan], ya[~both_nan], atol=ATOL, rtol=RTOL, equal_nan=True):
                    r.setdefault("numeric_columns_out_of_tolerance", []).append(c)
        else:
            r["text_mismatches"] += int((x[c].astype(str) != y[c].astype(str)).sum())
    r["status"] = "MATCH" if not r.get("numeric_columns_out_of_tolerance") and r["text_mismatches"] == 0 \
        else "DIFFERS"
    return r


def compare_json(a: Path, b: Path) -> dict:
    x, y = json.loads(a.read_text()), json.loads(b.read_text())
    keys = (set(x) | set(y)) - VOLATILE_JSON_KEYS
    diff = sorted(k for k in keys if x.get(k) != y.get(k))
    return {"file": a.name, "kind": "json", "status": "MATCH" if not diff else "DIFFERS",
            "differing_keys": diff, "ignored_volatile_keys": sorted(VOLATILE_JSON_KEYS & (set(x) | set(y)))}


def main() -> int:
    if not config.RAW_FILE.exists():
        print("MISSING INPUT: cached workbook not found; run `python -m rpi.acquire` first.")
        return 3
    digest = sha256(config.RAW_FILE)
    if digest != config.EXPECTED_SHA256:
        print(f"CHECKSUM MISMATCH: {digest}")
        return 2
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "status", "--porcelain", "--", "src", "scripts", "configs"],
                                    text=True).strip()
    shutil.rmtree(SNAP, ignore_errors=True)
    shutil.copytree(config.TABLES_DIR, SNAP)
    env = {**os.environ, "OMP_NUM_THREADS": "2", "OPENBLAS_NUM_THREADS": "2", "MKL_NUM_THREADS": "2",
           "PYTHONHASHSEED": "0"}
    log = []
    try:
        for cmd in STEPS:
            t0 = time.time()
            p = subprocess.run([sys.executable if c == "python" else c for c in cmd], env=env,
                               capture_output=True, text=True)
            log.append({"command": " ".join(cmd), "returncode": p.returncode,
                        "seconds": round(time.time() - t0, 1), "stderr_tail": p.stderr[-400:]})
            print(log[-1]["command"], p.returncode, log[-1]["seconds"], flush=True)
            if p.returncode != 0:
                break
        shutil.rmtree(REGEN, ignore_errors=True)
        shutil.copytree(config.TABLES_DIR, REGEN)
    finally:
        # restore frozen committed tables, whatever happened
        for f in config.TABLES_DIR.iterdir():
            if not (SNAP / f.name).exists():
                f.unlink()
        for f in SNAP.iterdir():
            shutil.copy2(f, config.TABLES_DIR / f.name)
    comps = []
    for f in sorted(SNAP.iterdir()):
        g = REGEN / f.name
        if not g.exists():
            comps.append({"file": f.name, "status": "NOT_REGENERATED"})
        elif f.suffix == ".csv":
            comps.append(compare_csv(f, g))
        elif f.suffix == ".json":
            comps.append(compare_json(f, g))
    import sklearn
    report = {
        "what": "raw-to-result reproduction from cached official workbook (real data, not synthetic)",
        "run_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "code_commit": commit, "code_dirty_in_src_scripts_configs": bool(dirty),
        "source_file": str(config.RAW_FILE.relative_to(config.ROOT)), "source_sha256": digest,
        "source_downloaded_in_this_run": False,
        "python": platform.python_version(), "pandas": pd.__version__, "numpy": np.__version__,
        "sklearn": sklearn.__version__, "seed": config.SEED, "threads": 2,
        "tolerance": {"atol": ATOL, "rtol": RTOL}, "steps": log,
        "n_tables": len(comps), "n_match": sum(c["status"] == "MATCH" for c in comps),
        "non_matching": [c["file"] for c in comps if c["status"] != "MATCH"],
        "frozen_tables_restored": True,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "reproduction_report.json").write_text(json.dumps(report, indent=2) + "\n")
    pd.DataFrame(comps).to_csv(OUT / "table_comparison.csv", index=False)
    print(json.dumps({k: report[k] for k in ["n_tables", "n_match", "non_matching"]}, indent=2))
    return 0 if all(s["returncode"] == 0 for s in log) and len(log) == len(STEPS) else 1


if __name__ == "__main__":
    sys.exit(main())
