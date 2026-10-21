# Research model selection

Operational model selected: **NONE**. Full-feature public lead time and independent temporal confirmation are absent.

The predeclared retrospective policy chooses among four strong families/calibration variants on separate earlier selection quarters, with 0.002 Brier tolerance and conventional-first order spline, ridge, GBM, RF. This order is a declared preference, not a count of model parameters. No outer test outcomes select the policy. Annual decisions:

| year | chosen_model | selection_brier | minimum_selection_brier | tolerance | operationally_selected |
| --- | --- | --- | --- | --- | --- |
| 2022 | L1_ridge_logistic | 0.133974 | 0.133974 | 0.002 | False |
| 2023 | M1_hist_gbm | 0.141962 | 0.141615 | 0.002 | False |
| 2024 | M1_hist_gbm | 0.138376 | 0.138308 | 0.002 | False |
| 2025 | L2_spline_logistic | 0.138545 | 0.13799 | 0.002 | False |

Pooled outer scores, all previously inspected, are in model_comparison.csv and recent_history_reference.csv. Per-year base-model artifacts and calibrators remain private; save/reload probabilities matched to1e-12. A lowest retrospective Brier is not an operational promotion. No additional model library was justified after the timing/novelty stop gate.
