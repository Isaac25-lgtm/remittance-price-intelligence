# Global remittance quote continuity (R01)

[![ci](https://github.com/Isaac25-lgtm/remittance-price-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/Isaac25-lgtm/remittance-price-intelligence/actions/workflows/ci.yml)

Investigator: Isaac Omoding · Research programme R01 · Stage: **phase-1 retrospective, exploratory analysis; decision CONDITIONAL**

A surveyed money-transfer quote can cost ≤3% of the amount sent, the SDG 10.c reference level. This project asks:

- Does the **same surveyed service** still cost ≤3% when the World Bank's *Remittance Prices Worldwide* (RPW) survey observes it again in the **exactly-next calendar quarter**?
- How much does the answer depend on how "same service" is defined, and on quotes that are never observed again?
- Do models rank quotes for analyst re-checking better than strong simple rules?

The unit of analysis is a surveyed offer. It is not a price paid, not a provider exit, and not consumer welfare.

## Gap and prior art (provisional)
The closest same-data studies explain corridor-average fees:

- Beck, Janfils & Kpodar, IMF WP 2022/063, [doi:10.5089/9798400205439.001.a001](https://doi.org/10.5089/9798400205439.001.a001);
- Beck & Martínez Pería, *World Bank Economic Review* 25(1), 2011, [doi:10.1093/wber/lhr017](https://doi.org/10.1093/wber/lhr017).

**Reading depth:** abstracts only (World Bank repository, RePEc/IDEAS, Emerald); **no full text was read**. A limited Crossref search found no study of service-level quote continuity with predictive validation, which is not proof of absence. The full matrix of 7 works, with depth labels, is in [docs/PRIOR_ART.md](docs/PRIOR_ART.md).

## Data
| | |
|---|---|
| Source | World Bank RPW Complete Dataset, `rpw_dataset_2011_2025_q3.xlsx` ([catalogue 0037898](https://datacatalog.worldbank.org/search/dataset/0037898/remittance-prices-worldwide)), CC BY 4.0, classified Public |
| Fetched | 17 Oct 2026, 50,780,339 bytes, sha256 `f1d7265b…82d2a8` ([manifest](results/source_manifest.json)). Raw data is never committed. |
| **Observation dates** | survey collection dates 2016-05-09 → 2025-09-10 (post-Q2-2016 sheet, 37 quarters). **2025Q2 is absent from the source.** |
| **Upload dates** | catalogue "Complete Dataset" last updated 23 Sep 2026; file blob Last-Modified 28 Sep 2026 |
| **Wave publication dates** | **unverified.** No historical release record was obtained, so the date an analyst could first know each quote is unknown. |
| Cohort | 204,469 quotes, 368 corridors, 699 normalised providers |
| Primary cohort | 45,343 eligible initially-cheap quotes (USD 200 basket, 0 ≤ cost ≤ 3%) → 36,429 with a unique core match next quarter and a valid cost |
| Exclusions (counted, not dropped silently) | 1,308 negative costs; 18 missing costs; 2,290 ambiguous origin keys; 66 ambiguous target keys; 4,337 not reobserved though their corridor was surveyed; 1,759 in corridors not surveyed next quarter. See [record flow](results/tables/record_flow.csv). |

**Preprocessing:**
- deterministic text normalisation (NFKC, casefold, whitespace), with no fuzzy matching;
- quarter index parsed so that adjacency is exact;
- total cost verified as fee% + FX margin;
- full audit in [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md).

## Design (frozen before any metric: [configs/experiment.yaml](configs/experiment.yaml), commit `ecc7c49`)
- **Identity:**
  - *core* = corridor, provider, payment instrument, access point, pickup method, pickup location, basket;
  - *strict* = core plus unchanged speed and receiving-network coverage, compared on the same cohort.
- **Splits:** expanding window, refit per target year 2022, 2023, 2024 and 2025 (2025Q1 only). Training targets fall strictly before the first test origin.
- **History features:** use only transitions with target ≤ origin − lag. Lag 0 is primary; lag 1 is a sensitivity analysis.
- **Eight fixed families, no tuning:**

  | Code | Family |
  |---|---|
  | B0 | always stays ≤3% |
  | B1 | training prevalence |
  | B2 | shrunk provider/corridor history |
  | B3 | current-cost logistic |
  | L1 | ridge logistic |
  | L2 | spline logistic |
  | M1 | HistGradientBoosting |
  | M2 | random forest |

  A highest-current-cost rule is also used as a review-ranking comparator.
- **Metrics:**
  - primary: Brier score on identical test rows;
  - also: log loss, calibration, AUROC/AUPRC, and failures captured at 10/20/30% review capacity.
- **Uncertainty:** cluster bootstrap by corridor and, separately, by provider (one-way). This measures sampling dependence within the time-forward test. **Held-out-corridor or held-out-provider validation was not performed.**

## Results (retrospective; all test years were previously inspected)
| Pooled targets 2022–2025Q1 (n = 19,667; 329 corridors) | Brier | Corridor-bootstrap 95% | Provider-bootstrap 95% | AUROC | Cal. slope | Failures caught at 20% (of 3,605) |
|---|---|---|---|---|---|---|
| B0 Always stays ≤3% | 0.1833 | [0.1650, 0.2021] | [0.1557, 0.2112] | – | – | – |
| B1 Training prevalence | 0.1498 | [0.1387, 0.1613] | [0.1330, 0.1668] | 0.515 | 0.70 | – |
| R Highest current cost | – | | | – | – | 1,217 |
| B3 Current-cost logistic | 0.1456 | [0.1355, 0.1568] | [0.1283, 0.1621] | 0.641 | 0.71 | 1,217 |
| B2 Shrunk history | 0.1390 | [0.1282, 0.1499] | [0.1219, 0.1558] | 0.694 | 0.78 | 1,387 |
| L1 Ridge logistic | 0.1331 | [0.1226, 0.1437] | [0.1178, 0.1490] | 0.736 | 0.78 | 1,620 |
| L2 Spline logistic | 0.1321 | [0.1218, 0.1425] | [0.1172, 0.1475] | 0.743 | 0.78 | 1,618 |
| M1 HistGradientBoosting | 0.1286 | [0.1188, 0.1387] | [0.1144, 0.1429] | 0.761 | 0.82 | 1,740 |
| M2 Random forest | **0.1265** | [0.1171, 0.1359] | [0.1125, 0.1401] | 0.773 | 1.19 | 1,758 |

- **Paired difference:** HistGBM − spline = −0.0035 (corridor 95% [−0.0054, −0.0014]; provider 95% [−0.0060, −0.0010]).
- **By year:** the spline beat HistGBM in 2024 (0.1209 vs 0.1216).
- **Review capacity:** at 20%, HistGBM catches 523 more failures than the highest-cost rule (corridor 95% [408, 638]).
- **Lag-1 sensitivity:** same ranking. Lag 1 delays history only; it **does not show quotes were available before the next survey**.
- **Reobservation (negative result):** a ridge logistic model of whether a quote is reobserved did **not** beat prevalence in 2022 or 2023.
- **Continuity:** P(stays ≤3% | core reobserved) = 0.811. Worst/best bounds over all eligible quotes are [0.652, 0.848]; in 2025 they are [0.375, 0.913]. Strict-identity estimates are within ±0.02 of core.
- **Africa:**
  - Sub-Saharan Africa receiving (2,779 test rows, 74 corridors): HistGBM vs spline not distinguishable.
  - East African Community (731 rows): logistic models ≈ HistGBM.
  - Uganda receiving (3 corridors, 20 failures): **below the support gate**.
  - No corridors send from Uganda.

**Historical pilot comparison (not an exact replication).** The pilot code and inputs were unavailable, and the specifications differ.

| | Pilot | This study |
|---|---|---|
| Rows | 204,469 | 204,469 (identical) |
| 2022–24 test rows | 18,030 | 18,048 |
| GBM Brier | 0.136037 | 0.130172 |
| Spline Brier | 0.144145 | 0.132738 |
| GBM − spline | −0.0081 | −0.0026 (provider CI includes 0) |

Marginal intervals overlap even where paired differences are clear; compare models with the paired intervals.

Details: [docs/STATUS.md](docs/STATUS.md) · [model card](docs/MODEL_CARD.md) · [figures](results/figures).

## Reproduction
- **Raw-to-result:** from the cached official workbook (checksum-verified, no re-download), [`scripts/reproduce_from_cache.py`](scripts/reproduce_from_cache.py) re-ran the whole pipeline and compared every frozen table: **28 of 30 matched** within 1e-9 (largest numeric difference ~2e-16). The other 2 differ **only in wall-clock `fit_seconds`**. No scientific differences were found. See [results/reproduction](results/reproduction) and [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md).
- **Presentation consistency:** the dashboard tests and result-integrity tests are separate from that reproduction. They check internal consistency of the committed aggregates and do **not** reproduce anything from data.

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e ".[dev,dashboard]"
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
python -m rpi.acquire                      # fetch + sha256 check (skips download if cached)
python scripts/reproduce_from_cache.py     # full pipeline from cache, compares and restores frozen tables (~7 min)
python scripts/presentation_aggregates.py  # dashboard aggregates from cached frozen-run predictions
pytest -q                                  # fixtures + integrity + dashboard AppTest
streamlit run dashboard/app.py             # research dashboard (aggregates only)
```

## Dashboard
`dashboard/app.py` is a research dashboard, not a consumer service. It covers:

- provenance;
- linkage and identity;
- continuity bounds;
- all eight model families with cluster intervals;
- time-forward and lag sensitivity;
- calibration for all families;
- review capacity;
- the negative reobservation result;
- Africa/EAC/Uganda support gates, plus gated region and corridor aggregates and an anonymous provider distribution;
- reproducibility.

It reads only allowlisted aggregate CSVs. Deployment readiness and licence evidence are in [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md). No live URL is recorded until a deployment has been verified.

## Limits and next gates
- No untouched test period exists.
- Wave release dates are unverified, so there is no lead-time claim.
- The outcome is conditional on reobservation.
- Exact-label identity probably under-links renamed services.
- Bootstraps are one-way only.
- Prior art has been read at abstract level only.

**Next gates:**
1. Full-text competitor reading.
2. Release-timing evidence.
3. A prospective test on future RPW waves using the frozen specification.

## Citation and acknowledgements
Data: *The World Bank, Remittance Prices Worldwide, available at http://remittanceprices.worldbank.org* (CC BY 4.0). The World Bank does not endorse this analysis.

**AI assistance:** code and documents were produced with Claude Code (Anthropic) under investigator direction, and must be disclosed in any manuscript.
