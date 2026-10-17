"""Render docs/REPRODUCIBILITY.md from results/reproduction/* (numbers are never typed by hand)."""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
r = json.loads((ROOT / "results/reproduction/reproduction_report.json").read_text())
tc = pd.read_csv(ROOT / "results/reproduction/table_comparison.csv")
steps = "\n".join(f"| `{s['command']}` | {s['returncode']} | {s['seconds']} |" for s in r["steps"])
nonmatch = tc[tc.status != "MATCH"]
nm = "none" if nonmatch.empty else "; ".join(
    f"`{x.file}` ({x.status}: max |Δ| {x.max_abs_diff:.3g}, text mismatches {x.text_mismatches})"
    for x in nonmatch.itertuples())
csv_rows = tc[tc.kind == "csv"]
doc = f"""# Reproducibility

Two different kinds of evidence exist. They are kept separate:

| Kind | What it proves | Where |
|---|---|---|
| **A. Raw-to-result reproduction (real data)** | Re-running the full pipeline on the cached official workbook regenerates the frozen result tables | `scripts/reproduce_from_cache.py` → `results/reproduction/` |
| **B. Committed-table consistency checks** | Internal identities across the committed aggregates, plus a dashboard that renders and downloads only allowlisted aggregates | `tests/test_results_integrity.py`, `tests/test_dashboard.py` (Streamlit AppTest) |

Neither B nor the synthetic fixtures in `tests/test_linkage.py` and similar files are a data reproduction.

## A. Raw-to-result reproduction from the cached workbook

- **Run:** {r['run_at_utc']} at code commit `{r['code_commit']}`. Source/script/config changes uncommitted at run time: {r['code_dirty_in_src_scripts_configs']}.
- **Input:** `{r['source_file']}`, sha256 `{r['source_sha256']}`, verified before running. **Not re-downloaded:** `source_downloaded_in_this_run` = {r['source_downloaded_in_this_run']}.
- **Environment:** Python {r['python']}, pandas {r['pandas']}, numpy {r['numpy']}, scikit-learn {r['sklearn']}. Seed {r['seed']}, OMP/BLAS threads {r['threads']}, PYTHONHASHSEED=0.
- **Procedure:**
  1. Snapshot the committed tables.
  2. Run the steps below.
  3. Compare each regenerated table with its frozen counterpart.
  4. **Restore the frozen tables.** Committed results are never overwritten; the regenerated copies stay in gitignored `data/processed/repro_outputs/`.
- **Tolerance:** numeric |Δ| ≤ atol {r['tolerance']['atol']:g} + rtol {r['tolerance']['rtol']:g}·|x|. Text must match exactly. In JSON files the volatile keys {', '.join(sorted({'code_commit', 'wall_seconds', 'verified_at_utc'}))} are ignored.

| Step | Exit | Seconds |
|---|---|---|
{steps}

**Outcome:**
- **{r['n_match']} of {r['n_tables']} frozen tables matched.**
- Largest numeric |Δ| across CSV tables: {csv_rows['max_abs_diff'].max():.3g}.
- Non-matching tables: {nm}

The per-table comparison is in `results/reproduction/table_comparison.csv`.

**Scope limits:**
- This reproduces this repository's own frozen results. It is **not** an exact replication of the historical pilot, whose code and inputs were unavailable; see `docs/STATUS.md` for that comparison.
- Figures (`results/figures`) are rendered from the tables and were not re-rendered in this check.

## Environment and commands
- **Container:** Claude Code cloud, Linux, 4 vCPU, 15 GB RAM, Python 3.13.16. CI runs Python 3.11.
- **Thread cap:** ≤ 2 for every run.
- **Seed:** 20261017. The 2-thread random forest agrees with earlier runs to ~1e-16.

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e ".[dev,dashboard]"
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
python -m rpi.acquire                      # downloads only if data/raw is missing; verifies sha256
python scripts/reproduce_from_cache.py     # A: full rerun + comparison, frozen tables restored
python scripts/presentation_aggregates.py  # dashboard aggregates from cached frozen-run predictions (no fitting)
python scripts/write_reproducibility_doc.py
pytest -q                                  # synthetic fixtures + B (integrity + AppTest)
streamlit run dashboard/app.py
```

**Individual stages (as originally run):**
- `python -c "from rpi.preprocess import load_clean; load_clean(rebuild=True)"`
- `python -m rpi.audit`
- `python scripts/run_phase1.py --release-lag 0`
- `python scripts/run_phase1.py --release-lag 1`
- `python scripts/run_descriptive.py`
- `python scripts/subgroup_metrics.py`
- `python -m rpi.figures`

**Inputs needed:** only the official workbook. If it is missing, `reproduce_from_cache.py` exits with code 3 ("MISSING INPUT"); if its checksum differs, it exits with code 2.

**CI** (`.github/workflows/ci.yml`) installs `.[dev,dashboard]` and runs `pytest -q`. It never downloads data or trains models.
"""
(ROOT / "docs/REPRODUCIBILITY.md").write_text(doc)
print("written")
