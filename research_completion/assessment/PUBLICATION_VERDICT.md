# R01 - Scientific Publication Verdict

Analysis date(UTC): 2026-10-21T02:15:34+00:00
Commit at evaluation:`aa42965775d5c3ce57c3752f2996b8eebb764282`
Source vintage: 2025Q3 workbook; SHA256 `f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8`
Scientific article type: conditional retrospective measurement/validation report
FINAL DECISION:**CONDITIONAL GO / CONDITIONAL_MORE_EVIDENCE**
**NOT YET PUBLICATION-READY**

## One-paragraph answer

The real source, quote linkage and measurement counts were independently re-executed; new chronological calibration/selection, group-transfer, missingness and dependence sensitivities were run. The evidence supports a careful retrospective measurement report, with conditional continuity 0.811057 and core bounds[0.651611,0.848201]. Strict identity keeps the point estimate near 0.810468 but widens bounds to[0.546413,0.872218]. Operational model selected:**NONE**. Public predictor availability, new independent temporal confirmation, external bundle validation and a substantial novelty verdict remain unresolved.

## Contribution versus closest studies

Service-level RPW analysis is already present in the IMF paper and 2026 studies. The candidate delta is exact-quarter quote continuity with explicit identity/observation uncertainty, not geography or model substitution. Lim 2026 full text remains inaccessible; substantial novelty is not established. See [literature matrix](../literature/closest_work_matrix.md) and [head-to-head audit](../literature/head_to_head_scientific_delta.md).

## Provenance, cohort and missingness

204469 quotes; 368 corridors; 699 normalised provider labels; 37 observed quarters 2016Q2-2025Q3; 2025Q2 absent.45343 eligible cheap origins; 36429 uniquely valid next-quarter pairs; 29546 stays,6883 failures,8914 unknown successors. Independent dictionary audit matches every flow state. See [source manifest](../data/source_manifest.json),[raw audit](../data/raw_data_audit.md),[bounds table](../tables/supplementary_overall_bounds.csv) and [independent audit](../audits/independent_raw_audit.json).

## Information timing

TIMING_PARTIAL documentary evidence; TIMING_FAIL for verified early warning.125 archived report URLs do not provide historical quote-level availability or revision vintages. No verified full-feature decision date before target collection; no lead-time claim. See [availability registry](../data/release_availability_registry.csv).

## Model evaluation and uncertainty

Chronological research-policy outer Brier: 0.130763,n= 19,667; all outcomes previously inspected. Full ranking:

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

Paired differences and corridor/provider/time/crossed sensitivities are in[paired_dependence.csv](../models/paired_dependence.csv).13 independent target waves limit time precision. Earlier reobservation failures remain reported; Uganda has insufficient events. Group-transfer sensitivities are historical, not independent temporal confirmation. Strict historical numeric reproduction failed at1e-9 despite exact cohort/measurement reproduction and unchanged headline tree scores; [differences are retained](../reproducibility/local_table_comparison.csv).

The amended joint corridor/provider/time interval for selected policy minus spline is **[-0.011730,+0.000457]**, crossing zero (point -0.005388). Stress simulation coverage 0.86 still fails to establish nominal 95% coverage. See [joint sensitivity](../models/joint_dependence_sensitivity.csv). Robust superiority is not established.

## Operational interpretation

Matched-sample review conditions on future reobservation membership. The corrected[all-origin scenario](../models/all_origin_capacity_bounds.csv) scores24556 eligible quotes,4889 with unknown outcomes. At20% budget selected-policy population recall bounds are0.2167-0.5726; no identified population policy ranking follows. Review-at-capacity results are hypothetical triage. No transaction saving, causal benefit, true service exit or market availability is observed. No deployable model selected. See [capacity table](../models/decision_capacity.csv) and [scenario costs](../models/decision_cost_scenarios.csv).

## The12 science gates

| gate | requirement | status | supporting_artifact | reason |
| --- | --- | --- | --- | --- |
| G1 | Scientific estimands | PASS | data/inclusion_exclusion_flow.csv | E1/E2/E3/E4 kept separate; units are recorded surveyed quotes, not transactions. |
| G2 | Source integrity | PASS | data/source_manifest.json | Independent official download matches bytes/hash; schema, gaps and anomalies audited; attribution recorded. |
| G3 | Linkage and attrition | UNRESOLVED | data/identity_collision_audit.csv | Counts independently reproduce and sensitivities are executed; historical bundle identity is not externally adjudicated; no uncertain links promoted. |
| G4 | Forecast information timing | FAIL | data/release_availability_registry.csv | Report captures do not establish historical availability of every row-level feature before target collection; prospective claim rejected. |
| G5 | Validation and confirmation | UNRESOLVED | validation/split_registry.csv | Chronological retrospective selection and leakage-protected transfers executed; no new independent temporal wave found. |
| G6 | Strong conventional comparison | PASS | models/model_comparison.csv | Historical, rolling history, cost, ridge, spline, GBM/RF and chronological calibration/selection evaluated; no unrestricted search. |
| G7 | Dependence and precision | UNRESOLVED | models/joint_dependence_sensitivity.csv | Joint corridor/provider/time sensitivity crosses zero for selected policy versus spline; stress coverage 0.86 does not validate nominal 95%; only 13 waves. |
| G8 | Major scientific novelty | UNRESOLVED | literature/head_to_head_scientific_delta.md | Same-source service-level competitors exist; Lim 2026 full text blocked; no first-in-literature or substantial-novelty claim established. |
| G9 | Meaningful contribution | PASS | models/sensitivity_grid.csv | Identity rules substantially widen population bounds despite stable conditional estimates. Monitoring remains a hypothetical observed-sample benchmark. |
| G10 | Reproducibility/transparency | PASS | reproducibility/source_to_results_comparison.csv | Source/cohort independently checked; code/versions/checkpoints public; strict numeric comparison failures and the diagnostic correction explicitly retained. |
| G11 | Report accuracy | PASS | assessment/claim_evidence_ledger.csv | Canonical report values are generated from locked tables and checked by final audit; conditional report, not submission manuscript. |
| G12 | Permissions and human approval | UNRESOLVED | manuscript/investigator_signoff_checklist.md | Public aggregate analysis authorised; investigator authorship/licence/institutional declarations and submission sign-off remain personal actions. |

## Blockers and executed work

See [ordered blockers](REMAINING_BLOCKERS.md),[execution report](final_execution_report.md),[claim ledger](claim_evidence_ledger.csv),[commands](../reproducibility/commands_executed.jsonl) and [research report](../manuscript/conditional_research_report.md). No completion, independence or significance is manufactured for blocked gates.

## Handoff and GitHub

Scientific files are reviewed through[PR3](https://github.com/Isaac25-lgtm/remittance-price-intelligence/pull/3). Exact checked integration state and downloadable ZIP are recorded in[Git/download links](../deliverables/git_and_download_links.md) and zip_verification.json. The local ZIP is under research_completion/deliverables. A source commit is not itself proof of hosted dashboard redeployment.

## Investigator verification

Confirm authorship, citations/competitor overlap, lawful attribution, funding/conflicts, institutional requirements, final scientific interpretation and venue before any submission. No journal submission or preprint posting was performed or authorised.
