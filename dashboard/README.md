# R01 research dashboard (local, not deployed)

`app.py` is a Streamlit research dashboard. It is **not** a consumer service.

- **Inputs:** only the committed aggregate tables in `results/tables/` and `results/source_manifest.json`. It does not read row-level RPW data or `data/raw`/`data/processed`, and it does no model training or live prices.
- **Sections:** Overview → Data provenance → Study cohort & linkage → Missing-outcome bounds → Baselines and models → Calibration → Hypothetical review capacity → African subgroup support → Limitations & reproducibility.
- **Labels:**
  - A context ribbon on every page states the stage (CONDITIONAL), the data cutoff (2025Q3, with 2025Q2 absent), that results are RETROSPECTIVE and EXPLORATORY, and the run ID, commit and source hash.
  - A caveat states that the outcome is conditional on reobservation and that no savings are observed.
  - Missing quarters display as empty, not zero.
- **Run:** `pip install -e ".[dashboard]" && streamlit run dashboard/app.py`
- **Tests:** `pytest tests/test_dashboard.py` uses Streamlit AppTest to render every section and change its selectors (information scenario, test subset, threshold, capacity subset, subgroup, calibration models, record-flow spec).
- **Deployment:** none. Public deployment needs separate investigator approval and a review of public-safe contents.
