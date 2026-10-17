# Reproducibility

- **Environment used:** Claude Code cloud container, Linux, 4 vCPU, 15 GB RAM, Python 3.13.16. Packages: pandas 3.0.6, numpy 2.5.4, scikit-learn 1.9.1, scipy 1.18.1, matplotlib 3.11.2, openpyxl 3.1.5, plus pyarrow. Threads capped at OMP/BLAS = 2.
- **Seed:** 20261017. Random forest uses n_jobs = 2; repeated runs agree to ~1e-16 (floating-point summation order only).

Commands, in order:

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e ".[dev]"
python -m rpi.acquire                     # fetch + sha256 check -> results/source_manifest.json
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
python -c "from rpi.preprocess import load_clean; load_clean(rebuild=True)"   # 62 s
python -m rpi.audit
python scripts/run_phase1.py --release-lag 0   # 123 s
python scripts/run_phase1.py --release-lag 1
python scripts/run_descriptive.py
python scripts/subgroup_metrics.py             # needs data/processed/test_predictions_lag0.parquet
python -m rpi.figures
pytest -q                                      # 32 tests (19 synthetic-fixture + 13 dashboard AppTest), ~11 s
streamlit run dashboard/app.py                 # local research dashboard (aggregates only)
```

`results/tables/run_meta_lag*.json` records the code commit, source hash and versions for each model run. CI (`.github/workflows/ci.yml`) runs only the synthetic tests. It never downloads data or trains models. CI installs `.[dev,dashboard]` so the AppTest checks run on the committed aggregate tables.
