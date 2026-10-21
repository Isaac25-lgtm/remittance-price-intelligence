# Affordable surveyed remittance quotes: identity-sensitive continuity and unknown-successor bounds

**Complete conditional research dossier for investigator review. Decision: CONDITIONAL_HOLD. This is not a submission-ready original manuscript.** Created 2026-10-21 T03:34:40.828257+00:00. Scientific code/source fingerprints are in the locked manifest. Keywords: remittance prices; longitudinal measurement; record linkage; partial identification; survey attrition.

## Scientific question and strongest supported statement

How persistently do recorded affordable RPW quotes reappear below the same threshold in the exactly next calendar quarter, and how much does inference change with identity and missing successors? The surviving statement is about the recorded source panel under explicit linkage rules. It is not a claim about actual transactions, provider exits or guaranteed access.

Among 36,429 uniquely valid core successor pairs, continuity is 0.81105712 (81.11%). Among all eligible origin records, its missing-outcome identification interval is [0.65161105, 0.84820149]. These are different targets. [M03]

Strict matching keeps the same 45,343 origins, retains 30,570 valid pairs, and gives conditional continuity 0.81046778. Its bounds are [0.54641290, 0.87221842]. The width increases by 12.9215 percentage points, although the conditional point changes by -0.0589 points. [M04]

The practically meaningful distinction is between a conditional statement about matched records and a statement about every initially affordable recorded offer. The evidence does not identify the true missing-outcome persistence or prove the conditional estimate overstates it. Under both rules, the finite-panel lower bound exceeds a majority of eligible records; an 80% all-origin claim is not identified. With unrestricted false links, even those latent-economic-service bounds would not follow.

## Position relative to closest work

Same-source firm/service price analysis is already established in Beck 2022 and Borra 2026. Matched-item replacement selection is established conceptually by Nakamura and Steinsson. Lim 2026 exact-method overlap remains unverified because its lawful full text was not obtained. No claim is SUBSTANTIAL_CONFIRMED. [L01]

Beck and Martinez Peria's foundational 2011 journal article is distinguished from the separately read 2009 World Bank working paper. Beck 2022's full local PDF includes firm-level models and appendix covariate definitions. Borra 2026's full methods already address provider/channel composition and expansion. Bersch 2021's recovered annex uses its own operator data and a different pricing endpoint. Nakamura and Steinsson's replacement-bias work supplies the closest conceptual comparison, not a commensurate predictive benchmark. The complete claim-by-claim matrix and access limitations are in literature/closest_work_matrix_v3.csv and fulltext_access_ledger.csv. A generic bibliography, absent search hit or new algorithm cannot establish originality.

## Data, permissions and methods

The verified source contains 204,469 post-2016 quote records across 37 observed waves, 2016Q2-2025Q3; 2025Q2 is absent. The current official download has 50,780,339 bytes and the frozen SHA256 f 1 d 7265 b 1856 d 61812 c 158 d 3 d 03 fae 686 dbff 58735 deabe 016 a 6 bfe 23482 d 2 a 8. [M01]

Attribution: The World Bank, Remittance Prices Worldwide, available at http://remittanceprices.worldbank.org. Official catalogue classification is public CC BY4.0 with attribution and no endorsement. This package uses public-safe aggregates and reproducible code; raw workbooks, provider/service rows, reading-copy PDFs, identity cases and predictions are excluded.

Eligibility uses nonnegative cost at most 3% of the USD200 basket, with a target calendar quarter no later than the final observed wave. Ambiguous origin/target keys, absent services, unresurveyed corridors and invalid target costs remain unknown. Core identity includes direction, provider, payment/access/pickup bundle and basket; strict additionally requires speed/network equality. There is no fuzzy match promotion. USD500 and 5% are separate fixed secondary products/thresholds. The independent implementation streams the original workbook and uses tuple dictionaries without importing the primary model/report code.

The primary source-record cohort has 45,343 eligible affordable origins: 29,546 recorded stays, 6,883 observed threshold failures and 8,914 unknown successors. The last observed wave contributes 2,083 separately right-censored affordable origins. [M02]

Eligible primary origins span 359 corridors and 474 provider labels, of which 444 labels have valid pairs. The quote-weighted conditional result must not be called an average-provider or average-corridor probability. [M08]

E1 uses valid matched outcomes. E2 allocates unknown outcomes to fail/stay for lower/upper identification bounds, conditional on recorded identity. E3 describes any cheap surveyed corridor quote, conditional on corridor resurvey. E4 reports reobservation separately. Counts, eligible denominators and state transitions reconcile. Normalisation can underlink label changes or merge economically distinct offerings; deterministic agreement between implementations cannot validate latent identity.

A private seed 20261021 stratified review form contains 60 cases:12 each from unchanged matches, changed speed/network, nonmatches, ambiguous keys and potential metadata drift. Prices/automated verdicts are hidden, alternate candidates supplied and stratum key separate. External human adjudications remain 0. [I01]

## Primary measurement results

| scenario | n_eligible | n_valid | n_unknown | conditional | lower | upper |
| --- | --- | --- | --- | --- | --- | --- |
| cc 1_3 pct_core | 45343 | 36429 | 8914 | 0.811057 | 0.651611 | 0.848201 |
| cc 1_3 pct_strict | 45343 | 30570 | 14773 | 0.810468 | 0.546413 | 0.872218 |
| cc 1_5 pct_core | 96418 | 77399 | 19019 | 0.902996 | 0.724875 | 0.922131 |
| cc 1_5 pct_strict | 96418 | 66135 | 30283 | 0.905285 | 0.620953 | 0.935033 |
| cc 2_3 pct_core | 84751 | 67822 | 16929 | 0.877488 | 0.70221 | 0.90196 |
| cc 2_3 pct_strict | 84751 | 58087 | 26664 | 0.878889 | 0.602376 | 0.916992 |
| cc 2_5 pct_core | 131559 | 104810 | 26749 | 0.934176 | 0.744236 | 0.94756 |
| cc 2_5 pct_strict | 131559 | 90173 | 41386 | 0.935191 | 0.640998 | 0.955579 |

Of the 36 eligible origin waves, 35 have strictly wider strict bounds; none narrows. There are 35 waves with valid E1 pairs. The prespecified lag 4 wave-HAC sensitivity interval for the pooled width difference is [6.64, 19.20] percentage points. This is not a validated robust 95% interval. [M05]

Core conditional continuity is 80.43% before 2022Q3 and 81.98% thereafter. Core unknown shares are 19.57% and 19.78%. These are composition-sensitive descriptions, not an identified effect of a survey change. [M09]

Equal-corridor and equal-provider-label conditional means are 69.54% and 63.21%, excluding groups without valid pairs for that conditional mean. This weighting change is material; it changes the estimand and does not correct survey selection. [M10]

Corridor survey monitoring gives 8,189/8,879 = 92.23% continuity of at least one cheap surveyed quote. Its 9,168 eligible origin corridor-quarters include 289 unknown follow-up corridor surveys. Phase 3 excludes 270 right-censored final-wave corridor-quarters from the earlier 9,438-origin display; the observed follow-up denominator and conditional rate are unchanged. It does not measure persistence of the same offer and is not SmaRT. [M06]

E4 over all primary eligible records is 81.3599% for unique core reobservation and 80.3410% for unique valid-cost reobservation. This denominator differs from the earlier conditional E4 modelling population. [M07]

Figures 1-5 display the bounds, full wave series, paired width, unknown-state flow and weighting sensitivity. Broad-region/provider-type and fixed pre/post/Russia/deletion analyses are complete in the supplementary CSVs, including adverse results. Neither the strict rule nor equal-group weighting is a validated correction for truth; they test sensitivity of interpretation. The threshold/basket comparisons change eligibility, so cross-scenario differences are not individual treatment effects.

## Statistical precision and secondary modelling

The source-panel counts/bounds are exact descriptive quantities under each rule. Generalisation beyond this selected panel requires assumptions and cannot use raw quote count as the number of independent seasons. The fixed-lag wave-HAC sensitivities include arbitrary contemporaneous dependence through aggregation but assume regular temporal dependence, with limited waves and changing composition. They are not validated robust 95% intervals. The full equation and all fixed-lag results are retained in inference/UNCERTAINTY_METHODS.md.

The frozen Phase 2 selected research policy has Brier 0.130763 on 19,667 previously inspected records. Raw RF0.128059 and raw GBM0.128106 have lower observed Brier. Calibrated ridge 0.134707, calibrated spline 0.134912 and raw spline 0.136151 remain reported. No operational model is selected. [P01]

The amended joint corridor/provider/time interval for selected-policy minus raw spline is[-0.011730,+0.000457]. The previous small simulation had 0.86 coverage across 50 replicates, so its nominal 95% interpretation is not validated. New wave-HAC intervals are assumption sensitivities and cannot erase that failure. [P02]

At the 20% all-origin review capacity, the selected policy reviews 4,905 of 24,556 eligible records;4,889 outcomes are unknown overall. All-failure recall bounds are 0.216707-0.572562. No population-wide policy ranking, avoided harm or consumer saving is established. [P03]

The retrospective model comparison retains Brier/log loss, calibration, AUROC/failure AUPRC, all named conventional references, annual results, historical group transfers and missingness scenarios. No new model family or broad tuning was run. All-origin bounds and MAR/IPW/MNAR assumptions remain separate. Model-selection, release-timing and unknown-successor limitations prevent an operational recommendation.

## Reproducibility and corrections

The original strict 1e-9 comparator still has 14 exact matches,2 timing-only matches and 14 differing tables. Independent count checks match in all 20 fields tested. Separate locked Windows runs give exactly equal ridge and spline predictions on the selected 2022 fold; this is not proof of Linux numeric identity. [R01]

On the inspected 2022 legacy fold, tightening the fixed diagnostic tolerance from 1e-4 to 1e-10 changes ridge Brier from 0.156476196 to 0.156857164, and spline from 0.154414433 to 0.154575503. Maximum individual probability changes are 0.081154 and 0.041055. These probes are not new selected candidates. [R02]

A genuine invalid-cost boundary defect was fixed: infinite target costs now remain unknown. Across 408,938 source cost cells, there are 0 infinite costs, so this repair changes no observed source result. [R03]

Repeated selected-fold determinism is established within Windows, while cross-platform identity remains unresolved. The stricter convergence probe is a diagnostic on inspected data, not a replacement winner. Its probability sensitivity further cautions against individual priority-queue claims. No prior results were silently regenerated with a new tolerance. The Phase 3 ledger records expected failures, exact commands, code hashes, CPU limits, time and peak memory.

## Timing, interpretation and limitations

The current official resource has no verified later outcome wave. Archive report captures cannot establish that every current-wave feature was public before target collection. All tested periods were already inspected. This defeats TrackB but is not an automatic barrier to finite-panel TrackA. No forecasting-only gate is imposed on the measurement claim.

Source sampling is not population-representative and quote weights are not transaction volumes. Missingness can reflect survey coverage, metadata or price availability, not actual exit. Identity sensitivities do not identify mislinkage rates. Reweighting changes the target, and temporal stability does not validate product comparability. Negative costs, transparency, date-label anomalies and survey-composition changes have explicit earlier sensitivities; no hidden deletion repairs the source. Uganda's small event count does not support an AI subgroup claim. The all-origin bound width is scientific uncertainty, not uncertainty removed by a better conditional classifier.

## Publication decision and falsification

CONDITIONAL_HOLD for a potential measurement paper; operational predictive paper NOT_SUPPORTED. The large recorded-key contrast is nonvacuous and mechanically reproducible, so immediate whole-project NO_GO is not compelled. Substantial originality and historical economic-product comparability remain unproven. In particular, inaccessible Lim methods could already report the proposed exact endpoint. The new analysis strengthens a careful measurement record but does not clear those external gates.

The next rational action is a bounded human review of the blinded identity cases plus lawful full-text overlap assessment of Lim 2026. If those show the exact contribution is already established, or cannot defend comparable services without an arbitrary mislinkage assumption, archive the original-article route. If cleared, author a measurement-focused original manuscript from this dossier with investigator-approved contribution and declarations. Repeating classifiers cannot resolve either gate.

## Declarations requiring investigator confirmation

Author/affiliation/correspondence, individual CRediT contributions, funding, conflicts, institutional determination on secondary public-data research and final licence attribution must be supplied/confirmed by the investigator; no approval, waiver or grant is invented. AI assistance: software execution, source review support, analysis checks and drafting were performed by an AI assistant and require human scientific verification. No submission, preprint posting or author/provider contact occurred. Public software and aggregates are versioned in the repository; private reading copies and provider rows are not redistributed.

## Evidence and references

Every labelled empirical/substantive claim above is linked to a source/table/code path and generation commit in assessment/claim_evidence_ledger.csv. Full bibliography with access depth: literature/references.bib and manuscript/references.bib. Internal dossier paths are relative to phase 3; publication-facing citations must be converted to the chosen journal format only after scientific GO.
