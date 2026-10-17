# Reproducibility

Two different kinds of evidence exist. They are kept separate:

| Kind | What it proves | Where |
|---|---|---|
| **A. Raw-to-result reproduction (real data)** | Re-running the full pipeline on the cached official workbook regenerates the frozen result tables | `scripts/reproduce_from_cache.py` → `results/reproduction/` |
| **B. Committed-table consistency checks** | Internal identities across the committed aggregates, plus a dashboard that renders and downloads only allowlisted aggregates | `tests/test_results_integrity.py`, `tests/test_dashboard.py` (Streamlit AppTest) |

Neither B nor the synthetic fixtures in `tests/test_linkage.py` and similar files are a data reproduction.

## A. Raw-to-result reproduction from the cached workbook

- **Run:** 2026-10-17T20:37:17+00:00 at code commit `a818ca6f840b8561022db7ffe74fd0672e04a65f`. Source/script/config changes uncommitted at run time: False.
- **Input:** `data/raw/rpw_dataset_2011_2025_q3.xlsx`, sha256 `f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8`, verified before running. **Not re-downloaded:** `source_downloaded_in_this_run` = False.
- **Environment:** Python 3.13.16, pandas 3.0.6, numpy 2.5.4, scikit-learn 1.9.1. Seed 20261017, OMP/BLAS threads 2, PYTHONHASHSEED=0.
- **Procedure:**
  1. Snapshot the committed tables.
  2. Run the steps below.
  3. Compare each regenerated table with its frozen counterpart.
  4. **Restore the frozen tables.** Committed results are never overwritten; the regenerated copies stay in gitignored `data/processed/repro_outputs/`.
- **Tolerance:** numeric |Δ| ≤ atol 1e-09 + rtol 1e-09·|x|. Text must match exactly. In JSON files the volatile keys code_commit, verified_at_utc, wall_seconds are ignored.

| Step | Exit | Seconds |
|---|---|---|
| `python -c from rpi.preprocess import load_clean; load_clean(rebuild=True)` | 0 | 78.6 |
| `python -m rpi.audit` | 0 | 6.3 |
| `python scripts/run_phase1.py --release-lag 0` | 0 | 133.6 |
| `python scripts/run_phase1.py --release-lag 1` | 0 | 124.9 |
| `python scripts/run_descriptive.py` | 0 | 58.7 |
| `python scripts/subgroup_metrics.py` | 0 | 2.5 |

**Outcome:**
- **28 of 30 frozen tables matched.**
- Largest numeric |Δ| across CSV tables: 1.1.
- Non-matching tables: `model_registry_lag0.csv` (MATCH_EXCEPT_TIMING: max |Δ| 0.5, text mismatches 0.0); `model_registry_lag1.csv` (MATCH_EXCEPT_TIMING: max |Δ| 1.1, text mismatches 0.0)

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
