# Identity and composition sensitivity

All computations below occurred **after** the 60 machine assessments were sealed and the sample key unblinded. They reuse the existing independent-source cache after verifying the workbook SHA256 `f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8`. The 204,469 quotes were not downloaded again. No original case form, model prediction or frozen historical estimate was overwritten.

## Preserved primary measurement

| Identity | Eligible cheap USD200 origins | Valid next-quarter pairs | Stay cheap | Fail | Unknown | Conditional | All-origin bounds |
|---|---:|---:|---:|---:|---:|---:|---|
| Core | 45,343 | 36,429 | 29,546 | 6,883 | 8,914 | 81.1057% | 65.1611%–84.8201% |
| Strict | 45,343 | 30,570 | 24,776 | 5,794 | 14,773 | 81.0468% | 54.6413%–87.2218% |

Under each specified recorded-key rule, conditional continuity is S/V and all-origin bounds are [S/N, (S+U)/N]. These are finite-panel identification bounds, not sampling confidence intervals or proven economic-service survival. Strict makes **5,859** previously valid core outcomes unknown: **4,770** core stays and **1,089** core failures. The extra width is exactly 5,859/45,343 = **12.9215 percentage points**. The earlier 5,956 changed-attribute records include another 97 that were already invalid under core. Those categories must not be conflated.

## Source eras

Era boundaries follow the **target** wave. Q1 2021 origins face the Q2 2021 recording change; Q3 2022 origins face the Q4 2022 change. Full eras and all 36 origin waves are retained. [Official context](../SURVEY_CHANGE_REVIEW.md), [complete new group tables](MEASUREMENT_GROUP_SENSITIVITIES.csv).

| Target-era group | Origins | Core valid | Strict valid | Newly unknown | Extra width |
|---|---:|---:|---:|---:|---:|
| Before Q2 2021 | 16,726 | 14,432 | 14,061 | 371 | 2.22 pp |
| Transition into Q2 2021 | 1,247 | 517 | 244 | 273 | 21.89 pp |
| Between changes | 7,595 | 5,616 | 3,932 | 1,684 | 22.17 pp |
| Transition into Q4 2022 | 1,481 | 763 | 554 | 209 | 14.11 pp |
| After Q4 2022 | 18,294 | 15,101 | 11,779 | 3,322 | 18.16 pp |

The increase is not confined to the boundary quarters. This is a descriptive difference across unequal quote/provider/corridor composition, not an interrupted-time-series treatment effect. Official classification changes are established prior information, and no causal fraction of broken links is identified. [Figure](figures/source_era_width.png).

## Funding, payout, provider type and region

Prespecified text grouping distinguishes bank transfer, card, cash, mobile money and combined funding instruments. Payout groups distinguish bank/account, cash, mobile wallet and other. Combined labels are retained rather than split into fabricated transactions; these broad groupings do not validate historical product identity.

Bank-funded origins lose 2,496 valid core links under strict (16.60% of 15,035 origins); card 1,697/12,955 (13.10%); cash 1,209/10,486 (11.53%); combined instruments 390/6,236 (6.25%); mobile money 67/631 (10.62%). Bank/account payout loses 3,737/22,196 (16.84%), cash 1,792/20,205 (8.87%), wallet 330/2,882 (11.45%). Those differences describe composition under deterministic rules, not financial inclusion effects.

Among six named regions, extra strict width ranges from 12.02 pp in sub-Saharan Africa to 13.66 pp in East Asia & Pacific. Source region `..` (1,425 origins) remains an explicit unspecified group, not a seventh substantive region. Sub-Saharan Africa still has the lowest conditional continuity under core among named regions; geography does not isolate identity validity. Provider-type outputs cover banks, mobile operators, MTOs, post offices and combined categories. A 20-origin bank/post-office group falls below the n=30 reporting floor. [GROUP_SUPPORT.csv](GROUP_SUPPORT.csv) preserves that omitted support for both identities; totals over reported provider-type rows therefore omit 20 origins. Every other grouping fully reconciles to 45,343.

The changed versus unchanged valid-core cohorts do not exhibit one uniform contrast. Changed continuity is 73.26% versus 82.79% for unchanged links at the first boundary, but 78.95% versus 71.66% at the second. These are outcomes under **core** within groups excluded/retained by strict, not observed identities of true products. No hypothesis or independence claim follows from their pooled similarity. [All group decompositions](PAIRED_GROUP_DECOMPOSITION.csv).

## Alternative descriptive weights

Core quote-weighted conditional continuity is 81.11%; equal-corridor 69.54%, equal-provider 63.21%, equal-origin-wave 80.63%. Strict equivalents are 81.05%, 70.04%, 64.54% and 80.75%. These change the descriptive estimand, not correct towards a transaction population. Of 474 provider groups, 444 core and 430 strict groups have valid pairs; conditional means exclude groups with no observed outcome. Bounds average over all 474 groups. Corridors: 359 total, 359 core/355 strict with valid outcomes. Waves: 36 total/35 with valid outcomes. Conditional means and bounds therefore need not summarize the same group subset. [Weighting support and denominators](WEIGHTING_SUPPORT.csv).

## Assumed linkage false positives

With no full-support case labels, evidence-derived false-positive or false-negative rates cannot be estimated. As **illustrations only**, remove floor(f × 36,429) valid core links at f=0%, 1%, 5%, 10%, retain all 45,343 origins, and make removed links unknown. Do not infer these fractions from the 60-case sample. No model-based identity repair is applied.

| Assumed fraction | Assumed incorrect links | Retained valid | Unknown | Conditional range | All-origin envelope |
|---|---:|---:|---:|---|---|
| 0% | 0 | 36,429 | 8,914 | 81.11% | 65.16%–84.82% |
| 1% | 364 | 36,065 | 9,278 | 80.92%–81.92% | 64.36%–85.62% |
| 5% | 1,821 | 34,608 | 10,735 | 80.11%–85.37% | 61.15%–88.84% |
| 10% | 3,642 | 32,787 | 12,556 | 79.01%–90.11% | 57.13%–92.85% |

For k assumed incorrect links, the lowest possible known stays are S−min(S,k); the lowest possible known failures are F−min(F,k). The displayed envelope takes the union over **different possible allocations** of which links are incorrect. When k is less than both S and F it widens by 2k/N, rather than k/N. A particular known subset's interval would widen only k/N. The displayed two extrema are not required to arise from one subset. Synthetic tests enumerate allocations independently; the independent completion audit checks denominator and bound arithmetic. [Full precision scenarios](ILLUSTRATIVE_LINKAGE_SENSITIVITY.csv).

## Inference limits and retained adverse results

New results are finite-panel descriptions. Earlier fixed-lag HAC, equal-wave, leave-group and crossed-resampling outputs remain in the consolidated dossier; they are assumptions about temporal generalization, not externally validated 95% coverage. They were not rerun merely to obtain favourable precision. The model policy-versus-spline interval still includes zero, simulation simultaneous coverage was 0.86, all inspected test waves remain retrospective, and historical release-time lead is unverified. No operational forecasting model or publication improvement follows from this extension.

The strict legacy comparison still has 14 exact tables, two timing-only tables and 14 differing outputs: **12 numerical/rank-derived tables and two platform-metadata files**. The numerical root cause remains unresolved. Source/cohort/count checks agree; Windows repetition agrees within environment, which does not establish cross-platform equality. Small Linux synthetic CI fixtures do not resolve the real-data discrepancies. [Independent retained-file audit](COMPLETION_AUDIT.json), [original causes](../../reproducibility/LEGACY_DIFFERENCE_CAUSES.csv).
