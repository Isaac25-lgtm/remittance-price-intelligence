# Model card: R01 phase-1 retrospective benchmark

- **Task:** for a surveyed RPW quote with cost ≤3% (USD 200 basket), predict P(the same core service, reobserved in exactly the next quarter, still costs ≤3%).
- **Intended use:** research benchmark and hypothetical analyst re-check triage. **Not for** consumer advice, price guarantees or provider assessment.
- **Training data:** RPW post-Q2-2016 transitions with target quarter < first test origin. Examples: 2022 models train on targets through 2021Q3; the 2025 model trains on targets through 2024Q3.
- **Models:** see `configs/experiment.yaml` (fixed hyperparameters). Fit times are in `results/tables/model_registry_lag0.csv`; every model fits in under 10 s on 2 threads.
- **Evaluation:** 19,667 pooled test rows, 329 corridors, 284 providers. Previously inspected years.
- **Results:** see `docs/STATUS.md`.
  - Random forest: Brier 0.1265, calibration slope 1.19 (under-confident).
  - HistGBM: 0.1286, slope 0.82.
  - Spline logistic: 0.1321.
  - History baseline: 0.1390.
- **Known failure modes:**
  - Performance is worse for Sub-Saharan Africa receiving corridors (GBM Brier 0.162 vs 0.123 elsewhere).
  - Year-to-year ranking changes (the spline beat GBM in 2024).
  - The models depend on reobservation, which they do not predict.
- **Timing caveat:** RPW release dates are unverified. The lag-1 sensitivity delays history features only; it does not establish that predictions could precede the next survey.
- **Presentation:** aggregate results are viewable in the local dashboard (`dashboard/app.py`). No model artefacts are served.
- **Explainability:** not yet produced. Any importance analysis would be associational, not causal.
- **Licence of the training data:** CC BY 4.0 per the catalogue, with the attribution and restricted-data terms in the workbook. No model artefacts are published.
