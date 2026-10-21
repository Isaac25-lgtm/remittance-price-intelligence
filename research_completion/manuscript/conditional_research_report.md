# The persistence of affordable international remittance quotes

**Conditional scientific evidence report - NOT FOR SUBMISSION.** Investigator: Isaac Omoding. Generated: 2026-10-21T02:15:34+00:00. Code at report generation:`aa42965775d5c3ce57c3752f2996b8eebb764282`. Decision:**CONDITIONAL_MORE_EVIDENCE; NOT YET PUBLICATION-READY**.

## Structured evidence summary

The study measures whether a World Bank RPW service quote costing 0-3% remains at or below 3% in exactly the next calendar quarter when a uniquely matching valid quote is observed. This is an offer-level retrospective endpoint, not a transaction price, provider exit, consumer saving or official aggregate SDG 10.c statistic. Across45,343 eligible initially cheap records,36,429 have valid unique successors and 29,546 stay cheap. Conditional continuity is 0.8111 (corridor-bootstrap 95%[0.7960,0.8256]); unknown successors produce extreme population bounds[0.6516,0.8482]. Strict identity gives conditional continuity 0.8105 but bounds[0.5464,0.8722]. These are quote-record populations, not transaction-weighted markets.

The new chronological selection/calibration policy scores Brier0.130763 on 19,667 retrospective outer records. Every tested period was already inspected. No operational model is selected: historical full-feature availability and genuinely new confirmation data are unavailable. A 13-work competitor matrix includes newly identified service-level2026 studies, with Lim 2026 full text blocked. Substantial novelty remains unresolved.

## Motivation and closest evidence

Affordable quotes can be intermittent even when corridor averages fall. The distinct question is how recorded service identity and selection into reobservation affect measured affordability continuity. Beck and Martinez Peria's2009 working paper/2011 article, Beck et al.2022, Lim 2026, Borra and Saritha2026, official RPW/SmaRT reporting and existing analytical products constrain originality. The IMF paper includes firm-level regressions, correcting the old corridor-only description. The full head-to-head assessment and access locators are in[the literature matrix](../literature/closest_work_matrix.md) and [scientific delta](../literature/head_to_head_scientific_delta.md). No model here is claimed to beat a published study on a different target.

## Data, estimands and service identity

The independently downloaded official workbook exactly matches the frozen source hash, covering204469 post-2016 quotes across 368 ordered corridors,699 normalised provider labels and 37 observed waves through 2025Q3.2025Q2 is absent; 181 collection dates conflict with assigned quarters. Core linkage uses ordered corridor, provider, payment instrument, access point, pickup method/location and basket. Strict also requires speed/network equality. Matching is deterministic; no fuzzy links are promoted. Duplicate origins/targets are explicitly unknown. A separately coded streaming audit reproduces the full flow.

E1 conditions on unique valid reobservation. E2 allocates every unknown successor to fail/stay for lower/upper bounds. E3 describes persistence of any surveyed cheap quote among resurveyed corridor-quarters. E4 models quote reobservation separately, within the declared corridor-surveyed/unambiguous scope. Ambiguous origin duplicates remain quote-record uncertainty in E2, not independently identified economic services. Secondary thresholds, basket/horizon and selection scenarios have their own denominators.

## Information clocks and validation design

Survey collection, public availability and decision time are distinct.125 archived official-report URLs were recovered, but report capture times are only public-by bounds, not first release dates or quote-level vintage availability. Issue 54 has a nominal 2025 publication statement, April 2026 PDF creation metadata and a September 2026 present blob timestamp; these cannot be silently equated. No full-feature `available_by <= decision < target_collection_start` condition is verified. Lag1 changes history, not current-quote availability. All modelling is consequently retrospective.

Annual outer targets are2022-2025Q1 (13 target waves). Training labels precede the first outer origin. Phase2 reserves six available earlier target quarters: two tune finite hyperparameter candidates,two fit sigmoid/isotonic calibrators,two select methods/families. Base models refit on proper+tuning records and remain fixed through calibration, selection and outer scoring. The legacy full-training design is preserved separately. Deterministic20% provider/corridor holdouts rebuild all target-dependent histories without heldout groups; unknown-group rates fall back to admissible training histories. They are historical transfer sensitivities, not a future holdout.

Provider holdouts are based on normalised source labels. Without an externally validated alias/legal-entity crosswalk, they cannot guarantee that every renamed form of the same firm is unseen. No independent legal-entity transportability claim is made.

## Probability models and calibration

| model | n | brier | log_loss | auroc | auprc_failure | cal_intercept | cal_slope |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M2_random_forest | 19667 | 0.128059 | 0.408764 | 0.767631 | 0.424477 | 0.122956 | 1.20721 |
| M1_hist_gbm | 19667 | 0.128106 | 0.408471 | 0.76329 | 0.425084 | -0.0322571 | 0.939006 |
| M2_random_forest__cal | 19667 | 0.128224 | 0.410475 | 0.761452 | 0.420504 | 0.0642783 | 0.996372 |
| M1_hist_gbm__cal | 19667 | 0.128338 | 0.410617 | 0.759338 | 0.423962 | -0.0237273 | 0.959571 |
| S_selected | 19667 | 0.130763 | 0.419527 | 0.749077 | 0.401859 | -0.0430757 | 0.89813 |
| L1_ridge_logistic__cal | 19667 | 0.134707 | 0.433051 | 0.724356 | 0.373128 | -0.158781 | 0.831853 |
| L2_spline_logistic__cal | 19667 | 0.134912 | 0.439538 | 0.725016 | 0.371557 | -0.180543 | 0.710613 |
| L1_ridge_logistic | 19667 | 0.135969 | 0.440285 | 0.726434 | 0.375261 | -0.242623 | 0.681333 |
| L2_spline_logistic | 19667 | 0.136151 | 0.440208 | 0.728266 | 0.375056 | -0.267777 | 0.668126 |
| B4_recent_history | 19667 | 0.13887 | 0.44265 | 0.69239 | 0.336411 | -0.14418 | 0.851887 |
| B2_history | 19667 | 0.138967 | 0.443091 | 0.693953 | 0.3363 | -0.0637355 | 0.777435 |
| B3_cost_logistic | 19667 | 0.146096 | 0.4672 | 0.64166 | 0.270096 | 0.197812 | 0.679632 |
| B1_prevalence | 19667 | 0.149854 | 0.476854 | 0.520065 | 0.191841 | 0.0956189 | 4.75603 |
| B0_always_stay | 19667 | 0.183302 | 2.53241 |  |  | -12.3214 |  |

Brier is primary; log loss, discrimination, failure AUPRC, calibration and within-quarter capacity are secondary. Calibration-in-the-large previously used a +/-10 root bracket that truncated the near-certain constant baseline; phase2 uses corrected bracketing and returns undefined calibration for single-class samples. Model artifacts remain private, with save/reload parity checked. The selected policy is a research comparison; no deployable winner is declared.

Annual choices:

| year | chosen_model | selection_brier | minimum_selection_brier | tolerance | operationally_selected |
| --- | --- | --- | --- | --- | --- |
| 2022 | L1_ridge_logistic | 0.133974 | 0.133974 | 0.002 | False |
| 2023 | M1_hist_gbm | 0.141962 | 0.141615 | 0.002 | False |
| 2024 | M1_hist_gbm | 0.138376 | 0.138308 | 0.002 | False |
| 2025 | L2_spline_logistic | 0.138545 | 0.13799 | 0.002 | False |

## Paired uncertainty and heterogeneity

| analysis | model_a | model_b | resampling | brier_diff | ci95_lo | ci95_hi |
| --- | --- | --- | --- | --- | --- | --- |
| legacy | M1_hist_gbm | L2_spline_logistic | corridor | -0.00345641 | -0.00554356 | -0.00138557 |
| legacy | M2_random_forest | L2_spline_logistic | corridor | -0.00564033 | -0.00761939 | -0.00368612 |
| legacy | M2_random_forest | M1_hist_gbm | corridor | -0.00218392 | -0.0036207 | -0.000665997 |
| legacy | M1_hist_gbm | L2_spline_logistic | provider | -0.00345641 | -0.00593636 | -0.000929859 |
| legacy | M2_random_forest | L2_spline_logistic | provider | -0.00564033 | -0.0078149 | -0.00339053 |
| legacy | M2_random_forest | M1_hist_gbm | provider | -0.00218392 | -0.00343885 | -0.000801011 |
| legacy | M1_hist_gbm | L2_spline_logistic | time_block_4 | -0.00345641 | -0.00676767 | -0.000648713 |
| legacy | M2_random_forest | L2_spline_logistic | time_block_4 | -0.00564033 | -0.00876774 | -0.0025215 |
| legacy | M2_random_forest | M1_hist_gbm | time_block_4 | -0.00218392 | -0.00295886 | -0.00132013 |
| legacy | M1_hist_gbm | L2_spline_logistic | crossed_corridor_provider | -0.00345641 | -0.00730288 | 3.85838e-05 |
| legacy | M2_random_forest | L2_spline_logistic | crossed_corridor_provider | -0.00564033 | -0.00955488 | -0.00244171 |
| legacy | M2_random_forest | M1_hist_gbm | crossed_corridor_provider | -0.00218392 | -0.00462251 | 0.000190079 |
| phase2 | M1_hist_gbm | L2_spline_logistic | corridor | -0.00804564 | -0.0104598 | -0.00594762 |
| phase2 | M2_random_forest | L2_spline_logistic | corridor | -0.0080924 | -0.0107011 | -0.00556389 |
| phase2 | M2_random_forest | M1_hist_gbm | corridor | -4.67616e-05 | -0.00158123 | 0.00134407 |
| phase2 | S_selected | L2_spline_logistic | corridor | -0.00538823 | -0.00739817 | -0.00368263 |
| phase2 | S_selected | B2_history | corridor | -0.00820405 | -0.0107908 | -0.00574511 |
| phase2 | L1_ridge_logistic__cal | L1_ridge_logistic | corridor | -0.00126201 | -0.00274698 | -0.000162617 |
| phase2 | L2_spline_logistic__cal | L2_spline_logistic | corridor | -0.0012396 | -0.00210022 | -0.000502335 |
| phase2 | M1_hist_gbm__cal | M1_hist_gbm | corridor | 0.000232486 | -9.0055e-05 | 0.000536434 |
| phase2 | M2_random_forest__cal | M2_random_forest | corridor | 0.000165083 | -0.000241699 | 0.00056916 |
| phase2 | S_selected | B4_recent_history | corridor | -0.008107 | -0.0111294 | -0.00531996 |
| phase2 | M2_random_forest | B4_recent_history | corridor | -0.0108112 | -0.0136037 | -0.00823996 |
| phase2 | M1_hist_gbm | L2_spline_logistic | provider | -0.00804564 | -0.0111925 | -0.00423256 |
| phase2 | M2_random_forest | L2_spline_logistic | provider | -0.0080924 | -0.0110131 | -0.00484984 |
| phase2 | M2_random_forest | M1_hist_gbm | provider | -4.67616e-05 | -0.00128793 | 0.00110555 |
| phase2 | S_selected | L2_spline_logistic | provider | -0.00538823 | -0.007725 | -0.00261053 |
| phase2 | S_selected | B2_history | provider | -0.00820405 | -0.0120101 | -0.00434512 |
| phase2 | L1_ridge_logistic__cal | L1_ridge_logistic | provider | -0.00126201 | -0.00230986 | -0.00030912 |
| phase2 | L2_spline_logistic__cal | L2_spline_logistic | provider | -0.0012396 | -0.00212476 | -0.000503087 |
| phase2 | M1_hist_gbm__cal | M1_hist_gbm | provider | 0.000232486 | -5.18615e-05 | 0.000508229 |
| phase2 | M2_random_forest__cal | M2_random_forest | provider | 0.000165083 | -0.000356009 | 0.000643656 |
| phase2 | S_selected | B4_recent_history | provider | -0.008107 | -0.0125889 | -0.00353793 |
| phase2 | M2_random_forest | B4_recent_history | provider | -0.0108112 | -0.014741 | -0.00577166 |
| phase2 | M1_hist_gbm | L2_spline_logistic | time_block_4 | -0.00804564 | -0.0110733 | -0.00506163 |
| phase2 | M2_random_forest | L2_spline_logistic | time_block_4 | -0.0080924 | -0.0116804 | -0.0046978 |
| phase2 | M2_random_forest | M1_hist_gbm | time_block_4 | -4.67616e-05 | -0.0010924 | 0.000798401 |
| phase2 | S_selected | L2_spline_logistic | time_block_4 | -0.00538823 | -0.00941577 | -0.00115645 |
| phase2 | S_selected | B2_history | time_block_4 | -0.00820405 | -0.0104088 | -0.00611851 |
| phase2 | L1_ridge_logistic__cal | L1_ridge_logistic | time_block_4 | -0.00126201 | -0.00270962 | 6.06904e-06 |
| phase2 | L2_spline_logistic__cal | L2_spline_logistic | time_block_4 | -0.0012396 | -0.00292434 | 0.000249459 |
| phase2 | M1_hist_gbm__cal | M1_hist_gbm | time_block_4 | 0.000232486 | -0.000139495 | 0.000704391 |
| phase2 | M2_random_forest__cal | M2_random_forest | time_block_4 | 0.000165083 | -0.000619827 | 0.00113727 |
| phase2 | S_selected | B4_recent_history | time_block_4 | -0.008107 | -0.011221 | -0.0052853 |
| phase2 | M2_random_forest | B4_recent_history | time_block_4 | -0.0108112 | -0.0138195 | -0.007642 |
| phase2 | M1_hist_gbm | L2_spline_logistic | crossed_corridor_provider | -0.00804564 | -0.0127828 | -0.00365191 |
| phase2 | M2_random_forest | L2_spline_logistic | crossed_corridor_provider | -0.0080924 | -0.0129628 | -0.00360698 |
| phase2 | M2_random_forest | M1_hist_gbm | crossed_corridor_provider | -4.67616e-05 | -0.00220039 | 0.00192614 |
| phase2 | S_selected | L2_spline_logistic | crossed_corridor_provider | -0.00538823 | -0.00933545 | -0.00178326 |
| phase2 | S_selected | B2_history | crossed_corridor_provider | -0.00820405 | -0.013325 | -0.00297347 |
| phase2 | L1_ridge_logistic__cal | L1_ridge_logistic | crossed_corridor_provider | -0.00126201 | -0.0039248 | 0.000390788 |
| phase2 | L2_spline_logistic__cal | L2_spline_logistic | crossed_corridor_provider | -0.0012396 | -0.00296893 | -5.4955e-05 |
| phase2 | M1_hist_gbm__cal | M1_hist_gbm | crossed_corridor_provider | 0.000232486 | -0.000253253 | 0.000742017 |
| phase2 | M2_random_forest__cal | M2_random_forest | crossed_corridor_provider | 0.000165083 | -0.000566991 | 0.00100522 |
| phase2 | S_selected | B4_recent_history | crossed_corridor_provider | -0.008107 | -0.0138592 | -0.00192382 |
| phase2 | M2_random_forest | B4_recent_history | crossed_corridor_provider | -0.0108112 | -0.0169181 | -0.00435984 |
| legacy | M1_hist_gbm | L2_spline_logistic | crossed_corridor_provider_time_block | -0.00345641 | -0.00916869 | 0.00196994 |
| legacy | M2_random_forest | L2_spline_logistic | crossed_corridor_provider_time_block | -0.00564033 | -0.0113163 | -0.000716289 |
| phase2 | M1_hist_gbm | L2_spline_logistic | crossed_corridor_provider_time_block | -0.00804564 | -0.013715 | -0.00219081 |
| phase2 | M2_random_forest | L2_spline_logistic | crossed_corridor_provider_time_block | -0.0080924 | -0.0144393 | -0.0015487 |
| phase2 | S_selected | L2_spline_logistic | crossed_corridor_provider_time_block | -0.00538823 | -0.0117298 | 0.000456998 |
| phase2 | S_selected | B2_history | crossed_corridor_provider_time_block | -0.00820405 | -0.0140961 | -0.0019427 |

Corridor/provider bootstraps and crossed pigeonhole/time-block sensitivities preserve paired comparisons. The latter are not exact arbitrary multiway inference, and 13 waves give only about three four-quarter blocks. Quote, corridor, provider and quarter weighting target different populations. All comparisons are exploratory, without multiplicity-adjusted confirmation. Per-wave, regional and income results are retained; Uganda's20 test failures across 3 corridors fail the 100-event reporting gate.

Limited synthetic coverage stress (not RPW evidence):

| method | n_simulations | empirical_coverage | mean_width | evidence_type | bootstrap_reps | dgp |
| --- | --- | --- | --- | --- | --- | --- |
| corridor | 50 | 0.38 | 0.00249788 | SYNTHETIC UNIT TEST; not observed RPW data | 200 | 20x20 sparse crossed groups; 13 AR(0.6) quarters; fixed loss-gap mean -0.003 |
| crossed_corridor_provider | 50 | 0.6 | 0.00452366 | SYNTHETIC UNIT TEST; not observed RPW data | 200 | 20x20 sparse crossed groups; 13 AR(0.6) quarters; fixed loss-gap mean -0.003 |
| crossed_corridor_provider_time_block | 50 | 0.86 | 0.00702627 | SYNTHETIC UNIT TEST; not observed RPW data | 200 | 20x20 sparse crossed groups; 13 AR(0.6) quarters; fixed loss-gap mean -0.003 |
| provider | 50 | 0.48 | 0.0031971 | SYNTHETIC UNIT TEST; not observed RPW data | 200 | 20x20 sparse crossed groups; 13 AR(0.6) quarters; fixed loss-gap mean -0.003 |
| time_block_4 | 50 | 0.58 | 0.00450555 | SYNTHETIC UNIT TEST; not observed RPW data | 200 | 20x20 sparse crossed groups; 13 AR(0.6) quarters; fixed loss-gap mean -0.003 |

The simulation deliberately includes crossed-group and serially correlated time shocks. Separate resampling axes cannot be assumed to capture every dependence component; the measured coverage rates have substantial Monte Carlo uncertainty and do not validate a universal95% coverage claim. Real-data intervals condition on fitted predictions and do not include full retraining/selection uncertainty.

The amended joint corridor/provider/time sensitivity gives selected policy minus spline Brier difference -0.005388 with interval[-0.011730,+0.000457]. Thus even retrospective superiority of the predeclared selection policy is not robust across dependence assumptions. The joint method achieved0.86 coverage in the limited stress simulation, still below nominal 0.95; no exact inferential guarantee is claimed.

## Hypothetical monitoring utility

| rule | reviewed | failures_total | failures_captured | recall | precision | false_alerts |
| --- | --- | --- | --- | --- | --- | --- |
| B2_history | 3928 | 3605 | 1387 | 0.384743 | 0.353106 | 2541 |
| B3_cost_logistic | 3928 | 3605 | 1217 | 0.337587 | 0.309827 | 2711 |
| L1_ridge_logistic | 3928 | 3605 | 1563 | 0.433564 | 0.397912 | 2365 |
| L1_ridge_logistic__cal | 3928 | 3605 | 1560 | 0.432732 | 0.397149 | 2368 |
| L2_spline_logistic | 3928 | 3605 | 1543 | 0.428017 | 0.392821 | 2385 |
| L2_spline_logistic__cal | 3928 | 3605 | 1540 | 0.427184 | 0.392057 | 2388 |
| M1_hist_gbm | 3928 | 3605 | 1688 | 0.468239 | 0.429735 | 2240 |
| M1_hist_gbm__cal | 3928 | 3605 | 1688 | 0.468239 | 0.429735 | 2240 |
| M2_random_forest | 3928 | 3605 | 1711 | 0.474619 | 0.435591 | 2217 |
| M2_random_forest__cal | 3928 | 3605 | 1711 | 0.474619 | 0.435591 | 2217 |
| S_selected | 3928 | 3605 | 1635 | 0.453537 | 0.416242 | 2293 |
| B4_recent_history | 3928 | 3605 | 1414 | 0.392233 | 0.35998 | 2514 |
| R_highest_cost_rule | 3928 | 3605 | 1217 | 0.337587 | 0.309827 | 2711 |

Policies select equal numbers within each origin quarter at5/10/20/30% capacity. Capacity uncertainty reranks in300 corridor resamples. False alerts are observed stays selected for review, not harm measured in practice. Relative cost scenarios assume a review identifies an observed failure and cannot establish monetary saving, intervention effectiveness or consumer availability.

The preceding E1 queue uses future valid-reobservation membership, which would be unavailable at an origin decision. The following correction scores **all eligible origin quotes**, preserving unknown outcomes instead of selecting the queue using future membership. These are E1-score extrapolation scenarios with partial-identification bounds, not validated joint observation/price forecasts:

| rule | n_all_eligible | n_known_valid | n_unknown | reviewed | known_failures_captured | unknown_reviewed | all_failure_recall_lower | all_failure_recall_upper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S_selected | 24556 | 19667 | 4889 | 4905 | 1611 | 1060 | 0.216707 | 0.572562 |
| L2_spline_logistic | 24556 | 19667 | 4889 | 4905 | 1502 | 1118 | 0.203633 | 0.554732 |
| B2_history | 24556 | 19667 | 4889 | 4905 | 1378 | 1022 | 0.184422 | 0.518695 |
| R_highest_cost_rule | 24556 | 19667 | 4889 | 4905 | 1193 | 1043 | 0.160113 | 0.481067 |

Among24556 origins,4889 outcomes are unknown. At20% capacity the selected policy reviews4905 quotes, captures1611 known failures, and reviews1060 unknowns; all-failure recall can range from 0.2167 to0.5726 under extreme allocations. Overlapping bounds prevent an identified population ranking of policies. Conditional matched-sample gains cannot be sold as operational benefit.

## Identity, source and missingness sensitivity

| scenario | n_eligible | n_valid_pairs | conditional_p_stay_core | lower_bound | upper_bound | origin_collision_rows |
| --- | --- | --- | --- | --- | --- | --- |
| core | 45343 | 36429 | 0.811057 | 0.651611 | 0.848201 | 2290 |
| strict | 45343 | 30570 | 0.810468 | 0.546413 | 0.872218 | 2290 |
| reduced_metadata_unique | 45343 | 33883 | 0.81079 | 0.605871 | 0.858611 | 5870 |
| threshold_2.9 | 41849 | 33673 | 0.800166 | 0.643839 | 0.839208 | 2035 |
| threshold_2.95 | 43171 | 34734 | 0.804831 | 0.647541 | 0.842973 | 2109 |
| threshold_3.05 | 46481 | 37365 | 0.813729 | 0.654138 | 0.850261 | 2348 |
| threshold_3.1 | 47729 | 38384 | 0.817737 | 0.65763 | 0.853422 | 2398 |
| threshold_5 | 96418 | 77399 | 0.902996 | 0.724875 | 0.922131 | 5741 |
| cc2 | 84751 | 67822 | 0.877488 | 0.70221 | 0.90196 | 5056 |
| horizon_2 | 45343 | 34214 | 0.781025 | 0.58933 | 0.834771 | 2290 |
| date_quarter | 45343 | 36270 | 0.810835 | 0.64859 | 0.848687 | 2442 |
| transparent_only | 44639 | 35763 | 0.80916 | 0.648267 | 0.847107 | 2276 |
| no_negative_fx | 41040 | 31561 | 0.818859 | 0.629727 | 0.860697 | 2135 |
| exclude_russia | 44004 | 35306 | 0.805189 | 0.646032 | 0.843696 | 2268 |
| exclude_2021_date_anomaly | 45259 | 36296 | 0.810916 | 0.650324 | 0.848362 | 2290 |

Core and strict conditional point estimates are close while the strict bounds are wider. Reduced metadata increases duplicate ambiguity and is not promoted. Thresholds around 3% alter the population as well as crossing classification; USD 500 and a true two-quarter horizon are separate products/estimands. A two-quarter2025Q1-to-Q3 link explicitly spans a missing intermediate wave, never a one-quarter transition. Date-quarter/transparency/Russia/negative-FX alternatives are sensitivities rather than silent data repairs.

Separate reobservation comparisons:

| year | model | n | brier | log_loss | cal_slope |
| --- | --- | --- | --- | --- | --- |
| 2022 | B1_prevalence | 5900 | 0.176615 | 0.553455 |  |
| 2022 | L1_ridge_logistic | 5900 | 0.227518 | 0.810982 | 0.182296 |
| 2022 | M1_hist_gbm | 5900 | 0.234276 | 0.892281 | 0.179342 |
| 2022 | corridor_history | 5900 | 0.169022 | 0.52705 | 0.660553 |
| 2023 | B1_prevalence | 7226 | 0.0346127 | 0.18587 |  |
| 2023 | L1_ridge_logistic | 7226 | 0.069314 | 0.2691 | -0.0603956 |
| 2023 | M1_hist_gbm | 7226 | 0.0624691 | 0.242965 | 0.0748025 |
| 2023 | corridor_history | 7226 | 0.0444938 | 0.212953 | -0.0242781 |
| 2024 | B1_prevalence | 6907 | 0.0492836 | 0.2219 |  |
| 2024 | L1_ridge_logistic | 6907 | 0.0491179 | 0.210904 | 0.223843 |
| 2024 | M1_hist_gbm | 6907 | 0.0446685 | 0.189768 | 0.445075 |
| 2024 | corridor_history | 6907 | 0.0486957 | 0.213055 | 0.770057 |
| 2025 | B1_prevalence | 1702 | 0.0308492 | 0.167784 |  |
| 2025 | L1_ridge_logistic | 1702 | 0.0224994 | 0.107606 | 1.2866 |
| 2025 | M1_hist_gbm | 1702 | 0.0247342 | 0.116875 | 0.416797 |
| 2025 | corridor_history | 1702 | 0.0324054 | 0.168152 | 0.149687 |

The earlier negative2022-2023 ridge-versus-prevalence finding is preserved in the legacy outputs. New tree comparisons do not identify why a quote is absent. MAR/IPW is an assumption-labelled valid-price observation scenario within the corridor-surveyed scope:

| year | n_eligible | n_observed | observed_stay | ipw_mar_p_stay | effective_sample_size | share_clipped |
| --- | --- | --- | --- | --- | --- | --- |
| 2022 | 5900 | 4566 | 0.792378 | 0.780677 | 1189.57 | 0.204237 |
| 2023 | 7226 | 6993 | 0.824253 | 0.82058 | 6554.76 | 0.0716856 |
| 2024 | 6907 | 6489 | 0.826938 | 0.824843 | 6447.63 | 0.209498 |
| 2025 | 1702 | 1619 | 0.811612 | 0.810021 | 1617.9 | 0.753231 |

Clipping does not repair MNAR selection. Pattern-mixture log-odds shifts and extreme bounds remain explicit. No causal doubly robust correction or service-exit survival model is identified. Price-component, continuous-cost and shift summaries are supplementary; observed quote-label concentration is not market concentration.

## Historical transfer and fitted sensitivities

| scenario | model | n | brier | log_loss | cal_slope |
| --- | --- | --- | --- | --- | --- |
| heldout_corridor | B2_history | 4217 | 0.157224 | 0.493979 | 0.664481 |
| heldout_corridor | L2_spline_logistic | 4217 | 0.153208 | 0.476091 | 0.700436 |
| heldout_corridor | M1_hist_gbm | 4217 | 0.140102 | 0.438713 | 0.842202 |
| heldout_corridor | M2_random_forest | 4217 | 0.141446 | 0.444964 | 1.21789 |
| heldout_provider | B2_history | 3719 | 0.122253 | 0.401836 | 0.999757 |
| heldout_provider | L2_spline_logistic | 3719 | 0.118354 | 0.386314 | 0.989277 |
| heldout_provider | M1_hist_gbm | 3719 | 0.116973 | 0.382153 | 0.867732 |
| heldout_provider | M2_random_forest | 3719 | 0.115132 | 0.380754 | 1.41875 |
| strict | B2_history | 14969 | 0.142574 | 0.454645 | 0.706321 |
| strict | L2_spline_logistic | 14969 | 0.135011 | 0.433865 | 0.742431 |
| strict | M1_hist_gbm | 14969 | 0.130598 | 0.418715 | 0.795338 |
| strict | M2_random_forest | 14969 | 0.128392 | 0.409953 | 1.19294 |
| threshold_5 | B2_history | 40438 | 0.0775884 | 0.281119 | 0.716957 |
| threshold_5 | L2_spline_logistic | 40438 | 0.0730119 | 0.259451 | 0.82451 |
| threshold_5 | M1_hist_gbm | 40438 | 0.070162 | 0.248012 | 0.854649 |
| threshold_5 | M2_random_forest | 40438 | 0.0691941 | 0.243717 | 1.15747 |
| cc2 | B2_history | 33547 | 0.0955914 | 0.326524 | 0.795115 |
| cc2 | L2_spline_logistic | 33547 | 0.0890631 | 0.303021 | 0.873869 |
| cc2 | M1_hist_gbm | 33547 | 0.0864835 | 0.293527 | 0.880888 |
| cc2 | M2_random_forest | 33547 | 0.0855559 | 0.289483 | 1.20614 |
| lag_1 | B2_history | 19667 | 0.140636 | 0.44727 | 0.734706 |
| lag_1 | L2_spline_logistic | 19667 | 0.13271 | 0.425756 | 0.766581 |
| lag_1 | M1_hist_gbm | 19667 | 0.128207 | 0.410657 | 0.826351 |
| lag_1 | M2_random_forest | 19667 | 0.126565 | 0.404471 | 1.18605 |
| no_provider_history | B2_history | 19667 | 0.143586 | 0.456419 | 0.836934 |
| no_provider_history | L2_spline_logistic | 19667 | 0.133426 | 0.427268 | 0.788597 |
| no_provider_history | M1_hist_gbm | 19667 | 0.129092 | 0.411629 | 0.851045 |
| no_provider_history | M2_random_forest | 19667 | 0.127031 | 0.405696 | 1.24157 |
| exclude_2021_date_anomaly | B2_history | 19667 | 0.138947 | 0.443091 | 0.775391 |
| exclude_2021_date_anomaly | L2_spline_logistic | 19667 | 0.132064 | 0.423178 | 0.777846 |
| exclude_2021_date_anomaly | M1_hist_gbm | 19667 | 0.128196 | 0.410444 | 0.820822 |
| exclude_2021_date_anomaly | M2_random_forest | 19667 | 0.126208 | 0.403151 | 1.19564 |
| exclude_russia | B2_history | 19667 | 0.138914 | 0.442835 | 0.779848 |
| exclude_russia | L2_spline_logistic | 19667 | 0.132104 | 0.423723 | 0.777541 |
| exclude_russia | M1_hist_gbm | 19667 | 0.129114 | 0.413732 | 0.786636 |
| exclude_russia | M2_random_forest | 19667 | 0.126238 | 0.403341 | 1.20392 |

Different scenarios may select different test records, so cross-scenario score differences are not automatically paired treatment effects. Main families within each scenario use identical eligible records. Group holdouts exclude heldout target histories; current surveyed covariates remain an explicitly retrospective information scenario.

## Final audit-driven robustness checks

| scenario | model | n | brier | log_loss | cal_slope |
| --- | --- | --- | --- | --- | --- |
| exclude_largest_development_provider | B2_history | 17245 | 0.133972 | 0.430389 | 0.764568 |
| exclude_largest_development_provider | L2_spline_logistic | 17245 | 0.127571 | 0.412163 | 0.789538 |
| exclude_largest_development_provider | M1_hist_gbm | 17245 | 0.124707 | 0.403542 | 0.784384 |
| exclude_largest_development_provider | M2_random_forest | 17245 | 0.122456 | 0.394467 | 1.1883 |
| exclude_largest_development_corridor | B2_history | 19341 | 0.139678 | 0.444481 | 0.786443 |
| exclude_largest_development_corridor | L2_spline_logistic | 19341 | 0.13262 | 0.424195 | 0.787416 |
| exclude_largest_development_corridor | M1_hist_gbm | 19341 | 0.129667 | 0.413333 | 0.799551 |
| exclude_largest_development_corridor | M2_random_forest | 19341 | 0.127026 | 0.405778 | 1.19659 |
| transparent_only | B2_history | 19667 | 0.138823 | 0.442438 | 0.78413 |
| transparent_only | L2_spline_logistic | 19667 | 0.132264 | 0.424336 | 0.767865 |
| transparent_only | M1_hist_gbm | 19667 | 0.129443 | 0.414292 | 0.787777 |
| transparent_only | M2_random_forest | 19667 | 0.126347 | 0.403554 | 1.17099 |
| no_negative_fx | B2_history | 17111 | 0.13666 | 0.439021 | 0.738705 |
| no_negative_fx | L2_spline_logistic | 17111 | 0.128553 | 0.413412 | 0.788845 |
| no_negative_fx | M1_hist_gbm | 17111 | 0.126599 | 0.405336 | 0.819736 |
| no_negative_fx | M2_random_forest | 17111 | 0.124304 | 0.399167 | 1.16353 |
| date_quarter | B2_history | 19667 | 0.138967 | 0.443141 | 0.774037 |
| date_quarter | L2_spline_logistic | 19667 | 0.132172 | 0.423478 | 0.774697 |
| date_quarter | M1_hist_gbm | 19667 | 0.127509 | 0.407909 | 0.833127 |
| date_quarter | M2_random_forest | 19667 | 0.12618 | 0.403195 | 1.18922 |

These fixed annual full-training references exclude the largest pre-2022 development provider/corridor, purge its target histories, or change transparency/FX/date handling. They do not refit or tune the selected policy. Provider labels are withheld. Fixed prior-quote/history-support strata are in models/history_overlap_support.csv. Pre/post-2022Q3 KS statistics and channel/region composition are descriptive; dependent-panel IID p-values and causal design-change claims are not reported.

The stricter historical identity ablation removes provider target-rate history **and** own-service cost/change lags. Removed lag values are fixed zero with availability0, after an all-NaN sklearn histogram-binning failure. It retains the earlier provider-rate-only ablation as a separate result:

| scenario | model | n | brier | log_loss |
| --- | --- | --- | --- | --- |
| no_provider_target_or_own_history | B2_history | 19667 | 0.143586 | 0.456419 |
| no_provider_target_or_own_history | L2_spline_logistic | 19667 | 0.137727 | 0.437723 |
| no_provider_target_or_own_history | M1_hist_gbm | 19667 | 0.135548 | 0.430928 |
| no_provider_target_or_own_history | M2_random_forest | 19667 | 0.133236 | 0.423509 |

Secondary continuous-price reference (not E1 probabilities), using annual past-only shrunk provider/corridor cost changes:

| year | model | n | mae | rmse | endpoint | scope |
| --- | --- | --- | --- | --- | --- | --- |
| 2022 | shrunk_past_provider_corridor_cost_change | 4566 | 0.900648 | 2.01334 | continuous_next_cost_conditional_reobservation | Annual past-only labels before first origin; shrink10; no within-year refit |
| 2023 | shrunk_past_provider_corridor_cost_change | 6993 | 0.761597 | 1.42906 | continuous_next_cost_conditional_reobservation | Annual past-only labels before first origin; shrink10; no within-year refit |
| 2024 | shrunk_past_provider_corridor_cost_change | 6489 | 0.664342 | 1.26177 | continuous_next_cost_conditional_reobservation | Annual past-only labels before first origin; shrink10; no within-year refit |
| 2025 | shrunk_past_provider_corridor_cost_change | 1619 | 0.779451 | 2.34469 | continuous_next_cost_conditional_reobservation | Annual past-only labels before first origin; shrink10; no within-year refit |

Compare continuous_cost_metrics.csv; these are matched initially cheap outcomes, not prices of missing services.

## Named conventional references and Brier skill

| model | reference | brier_model | brier_reference | brier_skill | relative_brier_diff | brier_diff | ci95_lo | ci95_hi |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S_selected | L1_ridge_logistic | 0.130763 | 0.135969 | 0.0382863 | -0.0382863 | -0.00520575 | -0.0123083 | 0.000246953 |
| S_selected | L1_ridge_logistic__cal | 0.130763 | 0.134707 | 0.0292764 | -0.0292764 | -0.00394374 | -0.00901006 | 0.00050458 |
| S_selected | L2_spline_logistic | 0.130763 | 0.136151 | 0.0395753 | -0.0395753 | -0.00538823 | -0.0117298 | 0.000456998 |
| S_selected | L2_spline_logistic__cal | 0.130763 | 0.134912 | 0.0307506 | -0.0307506 | -0.00414863 | -0.00884165 | 0.00048619 |

Skill is 1 minus model/reference Brier, and relative difference is model-minus-reference divided by reference. All four references are reported. Calibrated ridge has the lowest pooled conventional Brier here; naming it best is a post hoc description, not independent selection. The already inspected outcomes are not a confirmatory leaderboard. The joint intervals retain their undercoverage limitation. Paired supported subgroup intervals versus calibrated ridge are in models/subgroup_paired_uncertainty.csv; Uganda remains NOT_ESTIMABLE.

## Reproducibility and limitations

The official source, cohort, flow and descriptive quantities reproduce. The corrected strict1e-9 historical comparator reports14 exact tables,2 timing-only differences and 14 nonmatching tables (including environment metadata). Windows logistic/spline calculations differ slightly from frozen Linux outputs: maximum lag0 Brier delta about 1.11e-7, lag1 about 2.29e-5; GBM/RF reproduce to floating-point precision. One legacy pooled capture count differs by one case. Strict reproduction is not claimed successful, no tolerance was widened, and all historical artifacts were restored. The subsequent calibration-offset correction is separately versioned. Python/package versions, commands, fingerprints and checkpoint durations are recorded; original source PDFs and row-level data are excluded from public delivery.

## Recovered original pilot and score decomposition

Local execution recovered the earlier pilot code and reference parquet that were inaccessible to the cloud session. Unchanged archived programs were rerun with a private I/O adapter; source fields were compared against the independently reacquired input. Pilot reproduction: GBM Brier0.136036872; spline Brier0.144130752; n= 18,030. See [the recovery audit](../audits/recovered_pilot_reproduction.json).

Rebuilding the old openpyxl/string encoding directly from the independently downloaded official workbook exactly reconstructs the old parquet bytes (SHA256 d371c8b2e09b3f7698803dbfc20b85550f6206e4d30a4974b7a6051060c3493f). GBM/count reproduce the reported pilot exactly; spline remains slightly different from its reported0.1441454123434313. The initially source-adapted pandas cache produced18032 rather than 18030 test pairs and is retained separately. Blank-string versus missing-value semantics differ across encodings, so normalised value equality alone was insufficient. See pilot_cache_rebuild.json, pilot_source_content_comparison.csv and source_adapted_pilot_rerun.json under audits/.

The pilot evaluates origin years 2022-2024; phase1 evaluates target years 2022-2024. Their net18-record count difference conceals different memberships: 16,709 shared,1,321 pilot-only,1,339 phase1-only. Transparency filtering, duplicate handling, local-amount versus USD-basket identity, text normalisation, feature definitions, annual refit windows and hyperparameters also differ. Scores are not exact head-to-head algorithm comparisons. A prior exploratory corridor holdout was also recovered; its existence is preserved rather than misrepresented as absent from all earlier research.

Brier diagnostics decompose the fixed-bin predictor into uncertainty, resolution and reliability, retaining the difference between continuous and binned Brier as an explicit residual. It is not silently treated as an exact decomposition of continuous predictions:

| model | raw_brier | binned_brier | reliability | resolution | uncertainty | binning_residual |
| --- | --- | --- | --- | --- | --- | --- |
| B0_always_stay | 0.183302 | 0.183302 | 0.0335992 | 0 | 0.149702 | 0 |
| B1_prevalence | 0.149854 | 0.149854 | 0.000330169 | 0.000178831 | 0.149702 | 2.7601e-07 |
| B2_history | 0.138967 | 0.139704 | 0.000512317 | 0.0105106 | 0.149702 | -0.000736769 |
| B3_cost_logistic | 0.146096 | 0.146332 | 0.00202218 | 0.00539247 | 0.149702 | -0.000235699 |
| L1_ridge_logistic | 0.135969 | 0.136773 | 0.00252146 | 0.0154506 | 0.149702 | -0.00080419 |
| L1_ridge_logistic__cal | 0.134707 | 0.135383 | 0.00122385 | 0.0155435 | 0.149702 | -0.000675743 |
| L2_spline_logistic | 0.136151 | 0.137098 | 0.00252956 | 0.0151344 | 0.149702 | -0.000946005 |
| L2_spline_logistic__cal | 0.134912 | 0.135456 | 0.00121278 | 0.0154596 | 0.149702 | -0.000543631 |
| M1_hist_gbm | 0.128106 | 0.128719 | 0.000306873 | 0.0212907 | 0.149702 | -0.000612697 |
| M1_hist_gbm__cal | 0.128338 | 0.128754 | 0.000308727 | 0.021257 | 0.149702 | -0.000415729 |
| M2_random_forest | 0.128059 | 0.128835 | 0.000722279 | 0.02159 | 0.149702 | -0.000775538 |
| M2_random_forest__cal | 0.128224 | 0.128761 | 0.000413037 | 0.0213545 | 0.149702 | -0.000536673 |
| S_selected | 0.130763 | 0.131374 | 0.0009234 | 0.0192518 | 0.149702 | -0.000610678 |
| B4_recent_history | 0.13887 | 0.13957 | 0.000698923 | 0.0108315 | 0.149702 | -0.000699551 |

The main limitations are unverified public timing, no new temporal holdout, uncertain real service identity, nonrandom/changed survey coverage, missing successors, limited independent waves and unresolved closest-work novelty. Neither a statistically favourable row-level score nor a dashboard clears those gates. The second implementation audit is not external human peer review.

The later bounded public identity feasibility search examined three of the 30 private stratified candidates. Entity/network context did not establish their historical economic bundles; zero links were confirmed/promoted and 27 remain unadjudicated. See [the feasibility record](../data/manual_identity_feasibility.md). This does not estimate a false-merge rate.

## Conclusion and conditional manuscript outline

The current evidence supports a reproducible retrospective measurement report: conditional affordability continuity is stable to several definitions, while population uncertainty depends materially on observation and identity. It does not validate prospective forecasting or prove substantial novelty. A narrower methods/measurement article may become defensible after full competitor adjudication and stronger linkage/inference review; a prediction-led article additionally needs release-aware independent confirmation.

A future draft should follow: Introduction (specific novelty),Methods (E1-E4,clocks,linkage,selection,validation),Results (flow,bounds,paired comparisons,negative findings),Discussion (limitations/practical scope),Declarations and Supplements. No candidate submission manuscript is supplied while major gates remain unresolved.

## Declarations requiring investigator confirmation

Investigator: Isaac Omoding. Affiliations, funding, competing interests, author contributions and institutional/ethics requirements: INVESTIGATOR TO CONFIRM. Data attribution: World Bank RPW; no endorsement. AI assistance: earlier Claude Code and this Codex execution assisted code, analysis and drafting under investigator direction; human verification is required. No additional authors are invented. No journal or preprint submission is authorised.

## References and evidence navigation

Validated source links and access depths are in[closest_work_matrix.md](../literature/closest_work_matrix.md); bibliographic records are in[references.bib](references.bib). Numbered figures and tables have programmatic source inventories and legends. See [the final verdict](../assessment/PUBLICATION_VERDICT.md),[remaining blockers](../assessment/REMAINING_BLOCKERS.md) and [reproduction comparison](../reproducibility/source_to_results_comparison.csv).
