# Scientific protocol (phase 1, frozen 2026-10-17)

The machine-readable version is `configs/experiment.yaml`. It was committed in `ecc7c49` before any model metric was computed. At that point the source audit and linkage code existed, but no outcome-by-model results had been seen.

## Unit and population
- **Unit:** ordered corridor × provider × core service bundle × basket × origin quarter.
- **Population:** the RPW post-Q2-2016 sheet.
- **Primary basket:** cc1 (USD 200). cc2 (USD 500) is a separate product and is analysed as secondary.

## Identity
- **Core:** corridor (`source_code>destination_code`) + provider name (NFKC, casefold, whitespace/comma normalisation) + payment instrument + access point + pickup method + pickup location + basket USD amount.
- **Strict:** core + identical `speed actual` + identical `receiving network coverage`. Strict is evaluated only among core matches, so both definitions share the same origin cohort.
- **Duplicates:** a key appearing more than once in a quarter is `origin_key_ambiguous` if it is the origin, and `target_key_ambiguous` if it is the target. Ambiguous keys are never linked.
- **Fuzzy matching:** none.

## Outcome status (each eligible origin gets exactly one)
- `core_reobserved`
- `core_unobserved_corridor_surveyed`: the corridor was surveyed at t+1 but this key was absent.
- `corridor_not_surveyed_next_quarter`
- `target_key_ambiguous`
- `origin_key_ambiguous`
- `right_censored_last_quarter`

Linkage requires `qidx(t+1) = qidx(t) + 1` exactly. 2025Q1 therefore never links to 2025Q3.

## Estimands
- **E1:** P(0 ≤ cost_{t+1} ≤ 3 | 0 ≤ cost_t ≤ 3, unique core service reobserved at t+1 with a valid non-negative cost). This is the primary prediction target.
- **E2:** bounds over all eligible origins:
  - lower = stays / eligible;
  - upper = (stays + unknown) / eligible.
  - "Unknown" covers: not reobserved, corridor not surveyed, ambiguous key, or negative/missing target cost.
- **E3:** among corridor-quarters with at least one surveyed ≤3% quote that are surveyed at t+1, the share that still have at least one ≤3% quote. This is a surveillance quantity, not consumer access.
- **Secondary:** 5% threshold, cc2 basket, horizon 2.
- **Negative quoted costs** (1,308 cc1 rows) are retained in the source but excluded from the primary cohort.

## Information timing
- **Lag 0 (primary):** at origin q we know the quote at q and every linked transition whose target is ≤ q.
- **Lag 1 (sensitivity):** history uses transitions whose target is ≤ q − 1.
- True public release dates are not in the file. Collection dates are in the file and are recorded; release dates are not. No prospective lead-time claim is made.

## Splits
- Expanding window, refit once per test target year Y ∈ {2022, 2023, 2024, 2025}.
- Training rows have target quarter < the first test origin quarter, i.e. ≤ (Y−1)Q3. This is asserted in code.
- All test years are **previously inspected** (2022–24 by the pilot; 2025Q1 was present in the pilot's workbook). No untouched set exists.

## Models (fixed hyperparameters, no search)
- B0: always stays ≤3%.
- B1: training prevalence.
- B2: shrunk history, provider-in-corridor → corridor → global, m = 10.
- B3: logistic on current cost.
- R: highest-current-cost ranking rule.
- L1: ridge logistic, C = 1.
- L2: spline logistic, 5 quantile knots, cubic, on 6 numerics, plus one-hot.
- M1: HistGradientBoosting (lr 0.05, 300 iterations, 15 leaves, min leaf 50, L2 1).
- M2: random forest (300 trees, min leaf 20).

All imputers, encoders, scalers and splines are fitted inside the training fold.

## Metrics
- **Primary:** Brier score on identical pooled test rows.
- **Secondary:**
  - log loss
  - calibration intercept and slope
  - reliability deciles
  - AUROC
  - AUPRC (failure as the positive class)
  - failures captured at 10/20/30% review capacity per origin quarter, plus a pooled-ranking variant for pilot comparability
- **Uncertainty:** paired cluster bootstrap, 1,000 reps, by corridor and separately by provider. Each is a one-way bootstrap, not a crossed-dependence analysis. Capacity differences use 300 corridor bootstrap reps.

## Subgroup support gate
Model metrics are reported for a subgroup only if it has at least 100 observed failures in the test rows. Subgroups:
- receiving Sub-Saharan Africa (World Bank region field);
- East African Community, 8 partner states;
- Uganda, receiving and sending separately.
