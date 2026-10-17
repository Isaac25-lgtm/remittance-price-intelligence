# Results (aggregate only)

Produced by run `r01-phase1-2026-10-17` at code commit `0de853b` on source sha256 `f1d7265b…82d2a8`. Every table is an aggregate. No row-level quotes or predictions are published (predictions stay in `data/processed/`, which is gitignored).

| File | Content |
|---|---|
| `source_manifest.json` | fetch metadata, checksum, licence notes, failed routes |
| `tables/audit_*` | quarter coverage, missingness, cost anomalies, schema summary |
| `tables/record_flow.csv` | inclusion/exclusion flow (primary, cc2 basket, 2-quarter horizon) |
| `tables/linkage_*` | core vs strict on the same cohort, attribute changes, status by origin quarter |
| `tables/estimand_*` | E1 conditional rates, E2 bounds (3% and 5%), E3 corridor-level |
| `tables/model_*_lag0.csv` / `_lag1.csv` | metrics, paired cluster-bootstrap differences, capacity capture, reliability bins, registry |
| `tables/reobservation_metrics_*` | separate reobservation model vs prevalence |
| `tables/subgroup_*` | African subgroup support and globally-trained model metrics |
| `figures/fig1–fig6` | coverage, linkage, bounds, Brier, reliability, review capacity |

All model results are **retrospective backtests on previously inspected years**.
