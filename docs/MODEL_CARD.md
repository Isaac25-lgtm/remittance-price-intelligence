> Current local completion: **CONDITIONAL_MORE_EVIDENCE / NOT YET PUBLICATION-READY**. The analyses, pilot recovery, calibration, transfers and dependence sensitivities have been executed. See [the scientific verdict](../research_completion/assessment/PUBLICATION_VERDICT.md) and [conditional report](../research_completion/manuscript/conditional_research_report.md). The text below preserves the 17 October phase-1 history; references to future work or unavailable local inputs there are historical.

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
- **Calibration evidence:** reliability deciles for all seven non-constant families are in `results/tables/presentation_reliability_all_families.csv`. They were derived from the cached frozen-run test predictions, and integrity tests confirm they match the four families stored by the frozen run.
- **Uncertainty vs validation:** corridor- and provider-cluster bootstrap intervals (`presentation_model_brier_ci.csv`) quantify sampling dependence on the same time-forward test rows. **No held-out-corridor or held-out-provider validation was performed.** Gated corridor/region aggregates and the anonymous provider distribution describe heterogeneity only.
- **Reproduction:** see `results/reproduction/` (raw-to-result rerun from the cached official workbook).
- **Explainability:** not yet produced. Any importance analysis would be associational, not causal.
- **Licence of the training data:** CC BY 4.0 per the catalogue, with the attribution and restricted-data terms in the workbook. No model artefacts are published.
