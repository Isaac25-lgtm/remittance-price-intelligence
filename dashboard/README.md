# R01 research dashboard

`app.py` is a Streamlit research dashboard (not a consumer service) that presents the R01 results. It is **not deployed** from the research sessions; see `docs/DEPLOYMENT.md` for readiness, licence evidence and the public aggregate allowlist.

**Sections (sidebar):**
1. Overview
2. Data & provenance (observation vs upload vs unverified release dates; coverage with the missing 2025Q2 marked; record flow)
3. Linkage & identity (core vs strict on the same cohort; status shares by quarter)
4. Continuity & bounds (3% / 5%; corridor-level estimand)
5. Model comparison (all eight frozen families; corridor- or provider-bootstrap intervals; paired differences)
6. Time-forward & lag sensitivity
7. Calibration (all seven non-constant families)
8. Review capacity (all ranking rules incl. baselines; by year)
9. Reobservation (negative result)
10. Geography & support (Africa / EAC / Uganda gates; gated regions and corridors; anonymous provider distribution)
11. Reproducibility & limits

**Data rules:**
- The app reads only the files in `ALLOWLIST`: committed aggregates in `results/tables` and `results/reproduction/table_comparison.csv`, plus the manifest and run metadata.
- Each allowlisted table is downloadable.
- No row-level quotes, services, provider names or predictions; no model training or source download at startup.
- Filters act on aggregates only. Unsupported filters (provider names, sending-Uganda, per-year paired differences) are labelled as such.
- Bootstrap intervals are not held-out validation.

**Run:**

```bash
pip install -r dashboard/requirements.txt     # Python 3.11+
streamlit run dashboard/app.py
```

**Tests:** `pytest tests/test_dashboard.py tests/test_results_integrity.py`. AppTest exercises every section, selectbox value, radio option, multiselect (including empty) and download; integrity checks run on the real committed tables.
