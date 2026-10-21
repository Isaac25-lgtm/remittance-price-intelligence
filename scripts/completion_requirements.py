"""Explicit master-directive crosswalk, missingness tipping points and feature DAG."""
import pandas as pd
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_completion'

def main():
    # Status describes what was actually achieved, not whether a paper is publishable.
    rows=[]
    def add(section,requirement,status,evidence,limitation='Retrospective evidence; see canonical report'):
        rows.append(dict(requirement_id=f'R{len(rows)+1:02d}',directive_section=section,requirement=requirement,status=status,evidence=evidence,limitation=limitation))
    add('0-1','Local execution overrides cloud restriction; existing research retained','EXECUTED','protocols/phase2_frozen_protocol.md')
    add('1','Inventory original Git, files and outputs before changing','EXECUTED','audits/initial_repo_inventory.json')
    add('2','Distinguish E1 E2 E3 E4, quote/transaction and dates','EXECUTED','manuscript/conditional_research_report.md')
    add('3','Same-data/question literature and preprint/code/commercial searches','EXECUTED','literature/search_log.csv','Search not claimed exhaustive; some web query timestamps only date-level')
    add('3','Full-text closest-work head-to-head and substantial novelty','UNRESOLVED','literature/head_to_head_scientific_delta.md','Lim2026 full text inaccessible; IMF firm-level overlap corrected; no first-ever claim')
    add('3','No citation laundering; evidence depth and metadata','EXECUTED','literature/closest_work_matrix.csv')
    add('4','Official reacquisition, bytes/hash, licence/attribution','EXECUTED','data/source_manifest.json')
    add('4','Source-vintage comparison and latest data search','EXECUTED','data/historical_publication_timing.md','Official source hash unchanged; no newer source or independent wave located')
    add('4','Historical archive/release investigation','EXECUTED','data/archive_report_captures.csv','125 report captures are public-by evidence, not first-release clocks')
    add('4','Historical quote-level positive public lead time','UNRESOLVED','data/release_availability_registry.csv','No public feature-vintage clocks; early-warning claim FAIL')
    add('4-5','Schema, costs, negatives, Kosovo, dates and 2025Q2 gap','EXECUTED','data/raw_data_audit.md')
    add('5.1','Types, units, coverage, variable availability','EXECUTED','data/variable_dictionary.csv','Public release timing explicitly unverified')
    add('5.1','Exclusive flow, censoring, denominators; independent implementation','EXECUTED','audits/independent_raw_audit.json')
    add('5.2','Core/strict/reduced unique identity and collision audit','EXECUTED','data/identity_collision_audit.csv')
    add('5.2','External historical bundle/rebrand adjudication','UNRESOLVED','data/manual_identity_validation_disposition.csv','30 private candidates; zero externally confirmed or promoted; no true false-merge rate')
    add('5.2','Linkage rule stability and threshold/basket/horizon alternatives','EXECUTED','models/sensitivity_grid.csv')
    add('5.3','Separate reobservation comparison, keep old negative years','EXECUTED','models/reobservation_models.csv')
    add('5.3','Train-only MAR IPW, clipping, positivity/ESS scope','EXECUTED','models/ipw_mar_scenario.csv','Corridor-surveyed unambiguous-origin scope; MAR is untestable, not all E2 identified')
    add('5.3','Augmented/doubly robust or survival if identified','NOT_JUSTIFIED','assessment/REMAINING_BLOCKERS.md','No genuine exit label or justified causal/MNAR identification; no false survival analysis')
    add('5.3','MNAR pattern-mixture scenarios and tipping points','EXECUTED','models/mnar_tipping_points.csv','Assumption scenarios, not recovered outcomes; 2025Q1 no-observed wave remains NOT_ESTIMABLE')
    add('5.4','Descriptive groups, fee/FX, margin, lifetime and selection','EXECUTED','tables/supplementary_descriptive_groups.csv','Survey labels not market shares or survival')
    add('5.4','Quote/corridor/provider/wave weighting','EXECUTED','models/weighting_sensitivity.csv')
    add('6.1','Exact legacy rerun and immutable outputs','EXECUTED','reproducibility/local_table_comparison.csv','Strict numeric success NOT achieved:14 exact,2 timing-only,14 nonmatching; no widened tolerance')
    add('6.1','Recover original pilot and explain cohort/specification gap','EXECUTED','audits/recovered_pilot_reproduction.json','Raw cache reconstructed byte-exact; count/GBM match; spline residual retained')
    add('6.1','Feature clocks/DAG; current cross-section only retrospective','EXECUTED','validation/feature_dag.md')
    add('6.1','Adversarial future-label and heldout-history guards','EXECUTED','reproducibility/test_report.md','Synthetic software tests distinct from real-data timing evidence')
    add('6.2','Committed finite protocol/amendments before affected metrics','EXECUTED','protocols/protocol_amendments.md','Joint resampler and all-origin correction explicitly post hoc amendments')
    add('6.2','Chronological train/tune/calibrate/select/test registry','EXECUTED','validation/split_registry.csv','Every outer period previously inspected; retrospective development')
    add('6.2','Heldout corridor/provider zero-outcome-history transfer','EXECUTED','models/transfer_sensitivity_metrics.csv','Provider normalised labels are not verified legal-entity aliases')
    add('6.3','Mandatory constant, history, cost, ridge/spline, tree ladder','EXECUTED','models/model_comparison.csv')
    add('6.3','Last state / shrunk empirical Bayes and recent-k baseline','EXECUTED','models/recent_history_reference.csv','Last cheap binary state duplicates always-stay; history is a partial-pooling proxy')
    add('6.3','Cost-change fixed-capacity ranking','EXECUTED','models/recent_change_capacity.csv')
    add('6.3','Extra ML libraries, deep models or causal models','NOT_JUSTIFIED','assessment/REMAINING_BLOCKERS.md','Timing/novelty stop gate reached; no unmet need warrants extra model search')
    add('6.3','Continuous price secondary baselines and robust regression','EXECUTED','models/continuous_cost_metrics.csv','Conditional next cost; distinct from E1 probability endpoint')
    add('6.4','Bounded nested hyperparameters and train-only calibrators','EXECUTED','models/model_registry.json')
    add('6.5','Brier/logloss/discrimination/calibration incl undefined cases','EXECUTED','models/model_comparison.csv')
    add('6.5','All named raw/calibrated conventional references and Brier skill','EXECUTED','models/conventional_reference_comparisons.csv','Lowest conventional pooled score is post hoc; selected policy joint interval crosses zero versus every named reference')
    add('6.5','Paired supported subgroup differences and event/cluster gates','EXECUTED','models/subgroup_paired_uncertainty.csv','Uganda NOT_ESTIMABLE; nominal joint coverage unverified')
    add('6.5','Reliability support and Brier decomposition','EXECUTED','models/brier_decomposition.csv','Fixed-bin decomposition has explicit continuous-score residual')
    add('6.5','Paired and absolute corridor/provider/time/crossed uncertainty','EXECUTED','models/paired_dependence.csv','Only13 target waves; fitted-prediction uncertainty excludes full retraining')
    add('6.5','Joint dependence coverage validity','UNRESOLVED','validation/bootstrap_simulation.csv','Sparse crossed/time stress undercovers; joint0.86; selected-policy interval crosses0')
    add('6.5','Within-quarter5/10/20/30 capacity and burden/cost assumptions','EXECUTED','models/decision_capacity.csv','Matched E1 queue uses future membership; descriptive conditional benchmark only')
    add('6.5','All-origin review budget, unknown states and recall bounds','EXECUTED','models/all_origin_capacity_bounds.csv','E1 extrapolation scenario; no identified population policy ranking or benefit')
    add('6.6','Associative grouped feature importance/response support','EXECUTED','models/permutation_importance.csv','Three repeats across2024 waves; correlated/off-manifold permutation caveats')
    add('6.6','Pre/post2022 composition/distribution and calibration shifts','EXECUTED','data/pre_post2022_distribution_shift.csv','Descriptive KS effect; IID p-values and causal change attribution withheld')
    add('6.6','SSA/EAC/Uganda/income/channel/new-history support gates','EXECUTED','models/subgroups.csv','Uganda20 failures/3 corridors; no score or superiority claim')
    add('6.6','High/low history, prior-own-quote overlap strata','EXECUTED','models/history_overlap_support.csv','Fixed cutpoints; no performance-optimised strata')
    add('6.6','Source date/transparency/FX/Russia and no-history fitted sensitivity','EXECUTED','models/final_stress_metrics.csv')
    add('6.6','Provider target history plus own-service lag ablation','EXECUTED','models/no_identity_history_metrics.csv','Fixed zero/availability0 removes own-lag information; original rate-only ablation preserved')
    add('6.6','Largest-development provider/corridor refits and evaluation dominance','EXECUTED','models/final_stress_registry.json','Private identifiers withheld; full target histories purged')
    add('6.7','Private models metadata/checksums and save/reload parity','EXECUTED','models/fitted_artifact_manifest.json','No pickles/predictions distributed; hashes supplied for local artifacts')
    add('7','Frozen future evaluator / genuinely unseen new wave','NOT_AVAILABLE','validation/holdout_status.md','Evaluator synthetic clocks tested; no real future data fabricated')
    add('7','Claim falsification and all12 publication gates','EXECUTED','assessment/claim_evidence_ledger.csv','Multiple substantive gates FAIL/UNRESOLVED; conditional verdict')
    add('7.2','Stop unbounded algorithm search when fatal gates persist','EXECUTED','assessment/REMAINING_BLOCKERS.md')
    add('8.1','Numbered300dpiPNG/vector figures, legacy comparison and visual QA','EXECUTED','figures/figure_inventory.csv')
    add('8.2','Eight primary tables, supplements and variable metadata','EXECUTED','manuscript/table_legends.md')
    add('8.3','Conditional evidence report/outline, no submission-ready claim','EXECUTED','manuscript/conditional_research_report.md','No full submission manuscript or format conversions warranted under conditional verdict')
    add('8.4','Authorship/affiliations/funding/ethics/AI statements','UNRESOLVED','manuscript/investigator_signoff_checklist.md','Human declarations explicitly INVESTIGATOR TO CONFIRM; no invented approval')
    add('9.1','README/current instructions and archived historical results','EXECUTED','README.md')
    add('9.2','Aggregate-only dashboard and all-control local tests','EXECUTED','reproducibility/test_report.md','Python3.11 deployed dependency compatibility checked by CI; local analysis Python3.12')
    add('9.2','Verify actual hosted dashboard redeployment','INTEGRATION_RECORDED_SEPARATELY','deliverables/git_and_download_links.md','Local AppTest is not proof of hosted state')
    add('9.3-9.4','Reviewed safe public allowlist, manifests, ZIP and download','INTEGRATION_RECORDED_SEPARATELY','deliverables/git_and_download_links.md','ZIP generated after source lock; excludes private/raw/row files/sourcePDFs/models')
    add('9.5','Safe PR/green CI/main integration and exact SHA','INTEGRATION_RECORDED_SEPARATELY','deliverables/git_and_download_links.md','No force-push, bypass or formal release')
    add('10','Synthetic/integrity/adversarial/Streamlit and scientific audit','EXECUTED','reproducibility/test_report.md','Passing software is not passing scientific gates')
    add('11','Serial memory limits, checkpoints, commands, failures preserved','EXECUTED','reproducibility/run_manifest.json','One brief small-process overlap disclosed; no concurrent heavy fits; peak about1.29GB')
    add('12-13','Clear evidence-based conditional verdict and usable handoff','EXECUTED','assessment/PUBLICATION_VERDICT.md')
    pd.DataFrame(rows).to_csv(OUT/'audits/master_requirement_ledger.csv',index=False)
    b=pd.read_csv(OUT/'tables/supplementary_descriptive_groups.csv')
    overall=pd.read_csv(OUT/'tables/supplementary_overall_bounds.csv').assign(field='all',group='all')
    wave=pd.read_csv(OUT/'tables/table_03_persistence_bounds.csv').assign(field='origin_quarter');wave['group']=wave.origin_quarter
    rows=[]
    for r in pd.concat([overall,b,wave],ignore_index=True).to_dict('records'):
        for threshold in [.5,.8]:
            u=r['n_unknown'];required=(threshold*r['n_eligible']-r['n_stay'])/u if u else float('nan')
            status='NOT_ESTIMABLE_NO_UNKNOWN' if not u else 'GUARANTEED_AT_EXTREME_LOWER' if required<=0 else 'IMPOSSIBLE_AT_EXTREME_UPPER' if required>1 else 'SENSITIVE_TO_UNKNOWN_ALLOCATION'
            rows.append(dict(field=r['field'],group=r['group'],n_eligible=r['n_eligible'],n_unknown=u,stay_target=threshold,required_unknown_stay_fraction=required,status=status,interpretation='Exploratory50% and80% measurement thresholds; unknown stay allocation, not estimated outcome'))
    pd.DataFrame(rows).to_csv(OUT/'models/mnar_tipping_points.csv',index=False)
    (OUT/'validation/feature_dag.md').write_text('''# Feature information graph

```mermaid
flowchart LR
  A[Origin surveyed quotes and collection dates] --> B[Current cost / fee / FX / channel]
  A --> C[Origin corridor composition]
  D[Earlier exact-quarter linked outcomes] --> E[Past-only smoothed histories]
  F[Earlier own unique quote] --> G[Prior cost and change]
  B --> H[Fold-trained imputer / encoder / scaler / spline]
  C --> H
  E --> H
  G --> H
  H --> I[Earlier trained probability model]
  I --> J[Separate chronological calibrator / selector]
  J --> K[Retrospective outer predictions]
  L[Future target quotes and observation status] --> M[E1 cohort / labels / E2 unknown states]
  K --> N[Evaluation conditional on E1 or all-origin bounds]
  M --> N
  O[Historical public release clocks UNVERIFIED] --> P[Operational early-warning claim rejected]
```

No arrow from future outcomes/status into admissible features. Whole-origin-wave composition is only retrospectively available here. All heldout-group target outcomes are removed from historical event pools. E1 membership itself depends on future reobservation and is explicitly an evaluation selection; the corrected all-origin review scenario preserves unknown states. Public release timing remains a separate failed forecasting gate. See feature_asof_registry.csv and the executable leakage/future-clock tests.
''',encoding='utf-8')
    print('Master requirement crosswalk, tipping points and feature graph generated')

if __name__=='__main__':main()
