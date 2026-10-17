# R01 evidence status

Updated 17 October 2026 from Claude Code cloud execution, phase 1 (branch `research/r01-cloud-phase-1`).

| Dimension | Status |
|---|---|
| Data access | **VERIFIED.** Official World Bank file fetched (one attempt), 50,780,339 bytes, sha256 `f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8`. |
| Method validity | **CONDITIONAL.** Linkage, timing and leakage controls implemented and tested. Public release dates are unknown, so no prospective lead-time claim is made. |
| Scientific novelty | **NOT ASSESSED.** The competitor audit (`PRIOR_ART.md`) has not been done yet. |
| AI incremental value | **SMALL, RETROSPECTIVE.** Tree ensembles beat spline/ridge logistic by 0.003–0.006 Brier. This is about a third of the pilot's reported gap. All test years were previously inspected. |
| Readiness | **Not submission-ready.** |
| **Scientific decision** | **CONDITIONAL**, unchanged. The code is now runnable, but that alone does not upgrade the decision. |

## What was actually executed (phase 1)

1. **Environment probe:** Linux; Python 3.13.16 in a venv (`pyproject.toml` declares >=3.11); 4 vCPU, 15 GB RAM. Thread caps were OMP/BLAS=2. Outbound traffic goes through an HTTPS proxy, and package install via pip works.
2. **Source routes:**
   - `datacatalogapi.worldbank.org`: HTTP 429 on 3 attempts. Stopped.
   - `remittanceprices.worldbank.org/data-download`: HTTP 403 Cloudflare challenge. Stopped.
   - `ddh-openapi`: HTTP 404.
   - The official file host link from the catalogue (`datacatalogfiles.worldbank.org/.../DR0095523/rpw_dataset_2011_2025_q3.xlsx`): HTTP 200 on the first attempt.
3. **Audit** (`results/tables/audit_*`):
   - The post-Q2-2016 sheet has **204,469 rows**. This matches the pilot count exactly.
   - 37 quarters run from 2016Q2 to 2025Q3. **2025Q2 is absent from the source.**
   - 368 ordered corridors and 699 normalised provider names.
   - cc1 (USD 200) total cost is missing in 18 rows, negative in 1,308 and zero in 1,155.
   - Total cost equals fee% + FX margin (median absolute difference 0.002 pp).
   - Kosovo is coded `XKX` in `corridor` but `KSV` in the code fields (95 rows).
   - 181 rows labelled 2021Q3 were collected in May–June 2021.
   - Five unnamed helper columns exist only on 2025Q3 rows and were ignored.
4. **Frozen protocol** (`configs/experiment.yaml`) was committed in `ecc7c49` before any model metric was computed.
5. **Linkage, models and evaluation:** code commit `0de853b`, run `r01-phase1-2026-10-17`, about 2 minutes wall time on CPU. 19 synthetic-fixture tests pass.

## Observed results vs reported pilot (retrospective; years already inspected)

All figures are cc1 basket, 3% threshold, exact next quarter, release-lag-0 scenario, identical test rows across models.

| Quantity | Pilot (reported, exploratory) | This run |
|---|---|---|
| Post-2016 rows | 204,469 | **204,469** (exact) |
| 2022–24 test origins / corridors | 18,030 / 326 | **18,048 / 326** (+18 rows; pilot code unavailable, so the difference cannot be attributed) |
| Gradient boosting Brier (2022–24) | 0.136037 | **0.130172** |
| Spline logistic Brier (2022–24) | 0.144145 | **0.132738** |
| History baseline Brier (2022–24) | 0.144422 (corridor history) | **0.139768** (shrunk provider-in-corridor history; a different specification) |
| GBM − spline (2022–24) | −0.008109 [−0.010616, −0.005865] corridor bootstrap | **−0.00257**; corridor CI [−0.00456, −0.00033]; provider CI [−0.00549, +0.00014] |
| Failures captured at top 20% (2022–24, pooled ranking) | 1,351 GBM vs 1,129 spline | **1,555 GBM vs 1,462 spline** (of 3,300 observed failures) |

**Interpretation:**

- The row count reproduces exactly and the test cohort nearly so.
- The *direction* of the pilot result reproduces: boosting beats spline logistic. The *size* does not. The gap is about 3 times smaller, mainly because our spline/ridge logistic models include the same past-only history features.
- Over 2022–24 the provider-clustered interval includes zero.
- Pooled 2022–2025Q1 results:
  - GBM − spline = −0.00346, corridor CI [−0.00543, −0.00145], provider CI [−0.00600, −0.00098].
  - Random forest (one of the frozen families) has the lowest Brier, 0.12645. It is under-confident (calibration slope 1.19), while GBM's slope is 0.82.
- Year-level stability: in 2024 the spline logistic (0.1209) slightly beat GBM (0.1216).

**Simple rules are clearly beaten:**

- The highest-current-cost review rule captures 1,217 failures at 20% capacity, versus 1,740 for GBM. The difference is +523, corridor-bootstrap CI [408, 638].
- Shrunk provider/corridor history scores Brier 0.1390, versus 0.1286 for GBM.

**Reobservation model:** ridge logistic **lost** to training prevalence in 2022 and 2023, was roughly tied in 2024, and won only for 2025 (which has a single transition, 2024Q4→2025Q1). This matches the pilot's negative finding.

## Missing-outcome bounds (estimand 2, all eligible cheap origins)

Overall: 45,343 eligible origins.

| Estimate | Value |
|---|---|
| Conditional P(stay) given core reobservation | 0.811 |
| Worst/best-case bounds | [0.652, 0.848] |
| Bounds for 2021 targets (identity-field changes widen them) | [0.518, 0.888] |
| Bounds for 2025 targets (2025Q2 not published) | [0.375, 0.913] |

Strict-bundle conditional rates are within ±0.02 of core in every year. Of the 5,956 core-only matches, 5,693 have a changed speed label.

## African subgroups

| Subgroup (receiving) | Test rows | Corridors | Observed failures | Result |
|---|---|---|---|---|
| Sub-Saharan Africa | 2,779 | 74 | 688 | GBM − spline = −0.0053, corridor CI [−0.0124, +0.0015]: not distinguishable |
| East African Community | 731 | 25 | 137 | Logistic models ≈ GBM |
| Uganda | 140 | 3 | 20 | Below the pre-set support gate (≥100 failures); **no Uganda model claim** |

There are no corridors sending *from* Uganda.

## Blockers and next decisions

- **Release timing:** the workbook has no publication timestamps. If quarterly releases lag one quarter or more, the next-quarter "forecast" has no lead time. Next step: reconstruct the release history from archives, or keep the work as historical measurement.
- **No untouched test period:** 2025Q2 is missing and 2025Q3 has no adjacent origin quarter. A genuinely prospective test needs future releases (2025Q4 onward), evaluated with the frozen spec.
- **Identity drift:** core-unobserved spikes in 2021 targets (1,676) and 2022 (1,258). Row counts also jump at 2022Q4 while corridor counts stay flat. Both point to survey-scope or label changes; the mechanism is not asserted.
- `PRIOR_ART.md` competitor audit still to do. The dashboard is deferred; see `dashboard/README.md`.
