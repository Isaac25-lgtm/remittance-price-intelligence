# Associative model diagnostics

Grouped permutation importance was computed on 2024 outer test records separately by origin quarter, for spline, GBM and RF, three permutations per group. Calibrators were fixed from earlier folds. Feature groups preserve cost/distance together and collect correlated histories; residual correlation and implausible permuted combinations can bias importance. partial_response.csv contains descriptive observed-cost bins using actual covariates, with support counts, avoiding counterfactual prices that violate the fee-plus-FX accounting identity. It is not a partial or causal effect or guaranteed recommendation.

No SHAP/causal feature-effect claim is made. Quarterly variation and signed importance are retained, including null/negative permutation effects. The diagnostics do not establish mechanism or new temporal validation.
