"""Generate the evidence dossier from real locked tables; never manufacture a GO."""
from __future__ import annotations
import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import re
import pandas as pd

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_completion'

def load(name):return pd.read_csv(OUT/name)
def put(name,text):
    text=re.sub(r'(?<!\d):(?=[A-Za-z0-9])',': ',text)
    # Plain prose spacing; avoid changing identifiers and relative file links.
    text=re.sub(r'\b(with|about|only|than|from|through|including|for|of|by|before|after|below|across|per|October|September|April|is|costing|capacity|contains|nominal|coverage|threshold|seed|records|spline|GBM|RF|Lim|Issue|USD|NOT_ESTIMABLE)(?=\d)',r'\1 ',text)
    text=re.sub(r'\b(continuity|bounds|near|quarters|years|wave|and|the|a|A|around|days|rates|sample|draws|bootstrap|corridor|provider|cases|population|tolerance|on|n=)(?=\d)',r'\1 ',text)
    text=re.sub(r';(?=\S)','; ',text)
    text=text.replace('See[','See [').replace('and[','and [').replace('coverage0.86','coverage 0.86')
    text=text.replace('CC BY4.0','CC BY 4.0').replace('SDG10.c','SDG 10.c').replace('clinicalTRIPOD','clinical TRIPOD')
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
def markdown(df):
    def val(v):
        if pd.isna(v):return ''
        if isinstance(v,float):return f'{v:.6g}'
        return str(v).replace('|','/').replace('\n',' ')
    lines=['| '+' | '.join(df.columns)+' |','| '+' | '.join(['---']*len(df.columns))+' |']
    return '\n'.join(lines+['| '+' | '.join(val(v) for v in row)+' |' for row in df.itertuples(index=False,name=None)])

def main():
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    now=dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    b=load('tables/supplementary_overall_bounds.csv').iloc[0]
    sensitivities=load('models/sensitivity_grid.csv');strict=sensitivities[sensitivities.scenario=='strict'].iloc[0]
    metrics=load('models/model_comparison.csv').copy();recent=load('models/recent_history_reference.csv')
    metrics=pd.concat([metrics,recent],ignore_index=True)
    comparison=metrics[['model','n','brier','log_loss','auroc','auprc_failure','cal_intercept','cal_slope']].sort_values('brier')
    paired=pd.concat([load('models/paired_dependence.csv'),load('models/joint_dependence_sensitivity.csv')],ignore_index=True);selection=load('models/annual_selection.csv')
    allcap=load('models/all_origin_capacity_bounds.csv')
    capacity=load('models/decision_capacity.csv');capci=load('models/decision_capacity_ci.csv')
    transfer=load('models/transfer_sensitivity_metrics.csv');transfer=transfer[transfer.scope=='pooled']
    observation=load('models/reobservation_models.csv');ipw=load('models/ipw_mar_scenario.csv')
    pilot=json.loads((OUT/'audits/recovered_pilot_reproduction.json').read_text(encoding='utf-8'))
    simulation=load('validation/bootstrap_simulation.csv')
    decomp=load('models/brier_decomposition.csv')
    independent=json.loads((OUT/'audits/independent_raw_audit.json').read_text(encoding='utf-8'))
    assert independent['status']=='PASS'
    raw=json.loads((OUT/'data/independent_audit_summary.json').read_text(encoding='utf-8'))
    flow=load('data/inclusion_exclusion_flow.csv').groupby('state')['count'].sum().rename_axis('state').reset_index()
    gates=[
      ('G1','Scientific estimands','PASS','data/inclusion_exclusion_flow.csv','E1/E2/E3/E4 kept separate; units are recorded surveyed quotes, not transactions.'),
      ('G2','Source integrity','PASS','data/source_manifest.json','Independent official download matches bytes/hash; schema, gaps and anomalies audited; attribution recorded.'),
      ('G3','Linkage and attrition','UNRESOLVED','data/identity_collision_audit.csv','Counts independently reproduce and sensitivities are executed; historical bundle identity is not externally adjudicated; no uncertain links promoted.'),
      ('G4','Forecast information timing','FAIL','data/release_availability_registry.csv','Report captures do not establish historical availability of every row-level feature before target collection; prospective claim rejected.'),
      ('G5','Validation and confirmation','UNRESOLVED','validation/split_registry.csv','Chronological retrospective selection and leakage-protected transfers executed; no new independent temporal wave found.'),
      ('G6','Strong conventional comparison','PASS','models/model_comparison.csv','Historical, rolling history, cost, ridge, spline, GBM/RF and chronological calibration/selection evaluated; no unrestricted search.'),
      ('G7','Dependence and precision','UNRESOLVED','models/joint_dependence_sensitivity.csv','Joint corridor/provider/time sensitivity crosses zero for selected policy versus spline; stress coverage0.86 does not validate nominal95%; only13 waves.'),
      ('G8','Major scientific novelty','UNRESOLVED','literature/head_to_head_scientific_delta.md','Same-source service-level competitors exist; Lim2026 full text blocked; no first-in-literature or substantial-novelty claim established.'),
      ('G9','Meaningful contribution','PASS','models/sensitivity_grid.csv','Identity rules substantially widen population bounds despite stable conditional estimates. Monitoring remains a hypothetical observed-sample benchmark.'),
      ('G10','Reproducibility/transparency','PASS','reproducibility/source_to_results_comparison.csv','Source/cohort independently checked; code/versions/checkpoints public; strict numeric comparison failures and the diagnostic correction explicitly retained.'),
      ('G11','Report accuracy','PASS','assessment/claim_evidence_ledger.csv','Canonical report values are generated from locked tables and checked by final audit; conditional report, not submission manuscript.'),
      ('G12','Permissions and human approval','UNRESOLVED','manuscript/investigator_signoff_checklist.md','Public aggregate analysis authorised; investigator authorship/licence/institutional declarations and submission sign-off remain personal actions.'),
    ]
    gate=pd.DataFrame(gates,columns=['gate','requirement','status','supporting_artifact','reason']);gate.to_csv(OUT/'assessment/publication_gates.csv',index=False)
    claims=[
      ('C1','Conditional affordable-quote continuity','E1',f'{b.conditional_p_stay_core:.6f}',f'corridor95%[{b.corridor_ci95_lo:.6f},{b.corridor_ci95_hi:.6f}]','PASS','tables/supplementary_overall_bounds.csv','Among uniquely valid reobserved USD200 quotes initially costing0-3%, observed continuity is about81.1%; not a population or transaction probability.'),
      ('C2','Missing successors matter','E2',f'[{b.lower_bound:.6f},{b.upper_bound:.6f}]','Extreme allocations, with sampling intervals separately reported','PASS','models/sensitivity_grid.csv','Unknown successors materially widen the partially identified range; missing is not exit.'),
      ('C3','ML beats interpretable methods prospectively','E1','NOT ESTABLISHED','paired retrospective intervals do not repair availability or confirmation','UNRESOLVED','models/paired_dependence.csv','Only conditional retrospective probability/triage comparisons are supported.'),
      ('C4','Independent unseen-group generalisation','E1 transfer','Retrospective heldout groups actually evaluated','No heldout group outcomes in target-dependent histories; not a new temporal wave','PASS_LIMITED','models/transfer_sensitivity_metrics.csv','Leakage-protected historical group-transfer sensitivity was executed; results do not establish prospective external validity.'),
      ('C5','Prediction precedes survey outcomes','timing','NO VERIFIED FULL-FEATURE LEAD TIME','Historical report captures are not quote release clocks','FAIL','data/historical_publication_timing.md','No early-warning or operational forecasting claim.'),
      ('C6','Uganda-specific superiority','E1 subgroup','20 observed test failures;3 corridors','Below100-failure gate','FAIL','models/subgroups.csv','Uganda support is insufficient for a model-performance claim.'),
      ('C7','Substantial novelty over closest work','novelty','UNRESOLVED','Lim full text inaccessible; exact same-question absence not proven','UNRESOLVED','literature/closest_work_matrix.csv','Plausible measurement contribution requires fuller competitor adjudication.'),
      ('C8','Stable policy improvement over strong conventional references','E1','Joint selected-minus-spline interval includes zero','Nominal joint coverage unverified; calibrated ridge also compared','UNRESOLVED','models/conventional_reference_comparisons.csv','Report all raw/calibrated ridge/spline references; no robust superiority or confirmatory significance claim.'),
      ('C9','Monitoring creates population benefit','E2 decision scenario','Selected all-origin recall bounds0.2167-0.5726 at20% review','4889 unknown outcomes; E1-score extrapolation unverified','UNRESOLVED','models/all_origin_capacity_bounds.csv','All-origin scenarios preserve missing states and do not identify an intervention benefit or policy ranking.'),
      ('C10','Exact numerical reproduction succeeded','reproduction','14exact;2timing-only;14nonmatching tables','Strict1e-9 comparator retained','FAIL','reproducibility/local_table_comparison.csv','Source/cohort match; strict numerical legacy reproduction is not successful.'),
    ]
    cl=pd.DataFrame(claims,columns=['claim_id','claim','estimand','observed_result','uncertainty','pass_fail_unresolved','source_file_or_paper','eligible_manuscript_language'])
    details={
      'C1':('Unique valid exact-quarter pairs; conditional scope','Deterministic core linkage;1000 corridor resamples','36429 valid initially-cheap USD200 origin/target pairs','Selection into reobservation; rounding near3%','Not transactions or all-origin continuity','Table3;Figure3'),
      'C2':('Exclusive unknown states and fixed denominator','Extreme unknown stay/fail allocation; separate sampling intervals','45343 eligible origin records;8914 unknown','Duplicate/changed metadata and survey coverage, not service exit','Bounds identify quote-record cohort only','Table3;Figure9'),
      'C3':('Release-aware clocks and independent confirmation','Annual chronological fixed-prediction comparisons','19667 previously inspected outer records;13 targetwaves','Current-wave availability, selection and limited time clusters','Prospective claim not established','Table5;Figure10'),
      'C4':('No heldout target outcomes in any training history','Deterministic20% corridor/provider-label holdouts; history purged','Historical heldout-group records; per-scenario counts in source','Unresolved provider aliases and changing survey mix','Historical transfer, not legal-entity or temporal confirmation','models/transfer_sensitivity_metrics.csv'),
      'C5':('All row-level predictors available before target collection','Official/public archive investigation and registry','37 observed surveywaves and report captures','Nominal issue labels and present metadata differ from release clocks','No verified public full-feature lead time','data/release_availability_registry.csv'),
      'C6':('At least100 observed failures and adequate clusters','Predeclared subgroup support gate','Uganda receiving:140 outer rows;20 failures;3 corridors','Small sample and selected receiving routes','Unsupported scores withheld','Figure8;models/subgroups.csv'),
      'C7':('Closest same-source/question full texts and material delta','13-work head-to-head/source-depth matrix','Published, preprint, registry, repository and commercial work','Same-data service-level results may already cover the claimed novelty','Lim full text not read; search not exhaustive','literature/closest_work_matrix.csv'),
      'C8':('Paired improvement over strong raw/calibrated references','1000 corridor/provider/block/crossed/joint sensitivities','Same19667 outer records for every named family','Selection variance and sparse serial/crossed dependence','Intervals condition on fitted predictions; joint stress coverage0.86','Figure10;models/conventional_reference_comparisons.csv'),
      'C9':('Origin-known queue and observed intervention outcomes','All-origin within-quarter budgets; adversarial unknown allocations','24556 origins;19667 known-valid outcomes;4889 unknown','Unknown outcomes can change apparent recall and ranking','No intervention was tested; no saving or true exit observed','Figure14;models/all_origin_capacity_bounds.csv'),
      'C10':('Independent official source and strict numeric comparator','Remove stale generated targets; rerun; compare; restore original files','30 regenerated legacy tables including run metadata','Operating system/dependency/solver differences possible, not proved','No tolerance widened; exact tree/cohort and residual spline differences retained','reproducibility/source_to_results_comparison.csv'),
    }
    for j,col in enumerate(['required_evidence','method','test_population','alternative_explanation','caveat','figure_or_table']):cl[col]=cl.claim_id.map(lambda c:details[c][j])
    cl.to_csv(OUT/'assessment/claim_evidence_ledger.csv',index=False)
    put('assessment/REMAINING_BLOCKERS.md','''# Remaining blockers and bounded resolution routes

1. **Major novelty:** obtain a lawful accessible full text of Lim2026 and check its identity, attrition, supplementary endpoints and exact overlap. The current session encountered403; no access control was bypassed and no author contacted. Extend the same-question literature audit if a venue requires a systematic search.
2. **Forecasting:** historical quote-level release vintages and full-feature availability timestamps are missing. Archive report captures, nominal issue labels and present-file metadata cannot supply those clocks. Retain retrospective framing unless verifiable snapshots show positive lead time.
3. **Independent confirmation:** no official successor beyond2025Q3 was found. The workbook still has no2025Q2 and no adjacent-origin2025Q3 E1 target. Use the frozen future-wave evaluator only on genuinely unseen, correctly timed data.
4. **Service identity:** a stratified candidate sample is private; public historical bundle metadata was not established. Reduced keys increase collisions and are not promoted as corrected identity. No false-merge rate is identified.
5. **Inference:**13 retrospective target waves provide limited time-block information. The amended joint corridor/provider/time interval for the selected policy versus spline includes zero. Its synthetic stress coverage is0.86, not validated95%. A larger genuinely future wave sequence is needed for strong stability claims.
6. **Numerical reproduction:** cohort/measurement counts exactly reproduce; some Windows logistic/spline diagnostics and a pooled capture count differ from frozen Linux outputs. The strict1e-9 comparison failed. No tolerance was widened to conceal differences. The old +/-10 calibration-offset bracket was separately corrected for phase2.
7. **Human sign-off:** confirm authorship, citations, funding/conflicts, relevant institutional requirements, attribution and final scientific wording. Journal submission/preprint publication is not authorised.

Not justified: causal savings claims, verified market/service exit modelling, survival analysis without exit labels, consumer advice, a Uganda-specific AI claim, or a doubly robust/MNAR-identification claim. MAR/IPW and pattern-mixture scenarios do not identify unknown outcomes without assumptions. No new paid data/API, additional ML library or deep model is warranted by the unresolved gates.

Optional format conversions are not essential to the conditional report; Markdown is canonical. No submission manuscript is represented as ready. Source PDFs and fitted binaries remain private and are excluded from Git/ZIP.
''')
    put('validation/holdout_status.md','''# Holdout status

CONFIRMATION_NOT_AVAILABLE. Official catalogue content was independently downloaded and hash-matches the frozen2025Q3 source. Official resources/homepage list no newer report/wave.2025Q2 is absent;2025Q3 has no adjacent origin in the source.2022-2025Q1 outcomes were already inspected, including the phase2 annual outer scores. Deterministic provider/corridor holdouts address historical transfer only.

scripts/evaluate_future_wave.py is frozen for a new single-wave evaluation. It requires verified new source hash, explicit prior-research unseen confirmation, a committed protocol, all-row-predictor availability evidence and a decision strictly before actual target collection. It has synthetic clock/gap guards; no real new-wave evaluation was possible.
''')
    put('validation/leakage_audit.md','''# Leakage and availability audit

Executed adversarial tests replace future outcomes while checking admissible features, exclude heldout-provider outcomes from cumulative histories, enforce no heldout-group train/test identity overlap and require unknown-group historical fallback. Imputers/encoders/scalers/splines are fit inside each training partition. Calibration uses separate chronologically earlier calibration and selection windows; outer labels are not used for selection.

Annual model-selection windows are recorded in split_registry.csv. Six reserved target quarters are divided two/two/two for tuning/calibration/method selection; the base refit uses only proper+tuning observations and remains fixed for calibration/selection/outer scoring. The finite family policy is selected using a0.002 Brier tolerance with a predeclared conventional-first preference. This is retrospective development evidence, not independent confirmation.

Within-quarter quote composition and current prices require the whole origin wave. They are admissible in the declared retrospective end-of-survey scenario, but rejected for a public early-warning claim without availability evidence. A numeric history lag does not solve that problem. Direct outcome/status columns are retained privately for cohort construction but excluded by explicit feature selectors. Observation-conditioned E1 selection remains an estimand limitation, not a solved missing-data problem.
''')
    put('validation/dependence_bootstrap_methods.md','''# Dependence-aware inference

Paired Brier differences and absolute scores use1000 draws, seed20261020. Corridor/provider bootstraps resample whole labels and preserve row-level pairing. Circular four-observed-quarter blocks preserve all rows within resampled waves; all13 outer target waves are consecutive2022Q1-2025Q1, so no missing wave is bridged in that outer time bootstrap. About three blocks yield weak temporal precision.

Crossed pigeonhole sensitivity draws independent corridor and provider multiplicities and multiplies their row weights. It is not a naive nested bootstrap and is not claimed exact finite-sample multiway coverage. Empty draws are rejected if frequent. Structural synthetic checks verify whole-cell weights, crossed factorisation and fixed-wave resampling; zero paired differences produce zero intervals. A limited50-replicate synthetic stress test (200 bootstrap draws per replicate) uses sparse crossed groups and13 AR(0.6) quarterly shocks. Its empirical coverage is diagnostic with substantial Monte Carlo error, not a formal coverage proof. No procedure is promoted as exact joint inference from this test.

Following first-pass undercoverage, one explicitly post hoc amendment adds a joint corridor/provider multiplicity product times circular four-wave block weights. It was specified before computing its real-data interval, without searching multiple new procedures. Its synthetic stress coverage is0.86; it remains exploratory and does not validate nominal95% coverage. The selected-policy versus spline interval includes zero. See joint_dependence_sensitivity.csv and bootstrap_simulation.csv.

Capacity intervals rerank both policies at the same20% within-quarter budget in300 corridor resamples. The original E1 ranking conditions on future reobservation membership and is not a deployable review queue. all_origin_capacity_bounds.csv additionally scores every eligible origin, retaining unknown future states and worst-case recall bounds without refitting. Alternative corridor/provider/quarter-equal averages change the target weighting; none estimates transaction-weighted consumer prices. No multiplicity-adjusted confirmatory significance claim is made.
''')
    put('models/inference_spec.md',(OUT/'validation/dependence_bootstrap_methods.md').read_text(encoding='utf-8'))
    put('models/model_selection.md',f'''# Research model selection

Operational model selected: **NONE**. Full-feature public lead time and independent temporal confirmation are absent.

The predeclared retrospective policy chooses among four strong families/calibration variants on separate earlier selection quarters, with0.002 Brier tolerance and conventional-first order spline, ridge, GBM, RF. This order is a declared preference, not a count of model parameters. No outer test outcomes select the policy. Annual decisions:

{markdown(selection)}

Pooled outer scores, all previously inspected, are in model_comparison.csv and recent_history_reference.csv. Per-year base-model artifacts and calibrators remain private; save/reload probabilities matched to1e-12. A lowest retrospective Brier is not an operational promotion. No additional model library was justified after the timing/novelty stop gate.
''')
    put('models/model_explainability.md','''# Associative model diagnostics

Grouped permutation importance was computed on2024 outer test records separately by origin quarter, for spline, GBM and RF, three permutations per group. Calibrators were fixed from earlier folds. Feature groups preserve cost/distance together and collect correlated histories; residual correlation and implausible permuted combinations can bias importance. partial_response.csv contains descriptive observed-cost bins using actual covariates, with support counts, avoiding counterfactual prices that violate the fee-plus-FX accounting identity. It is not a partial or causal effect or guaranteed recommendation.

No SHAP/causal feature-effect claim is made. Quarterly variation and signed importance are retained, including null/negative permutation effects. The diagnostics do not establish mechanism or new temporal validation.
''')
    put('data/raw_data_audit.md',f'''# Actual source and measurement audit

REAL-DATA EXECUTION,20 October2026. Official source:50,780,339 bytes; SHA256 `{raw and 'f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8'}`. No new vintage found. Dataset catalogue Public/CC BY4.0; required attribution: The World Bank, Remittance Prices Worldwide, available at http://remittanceprices.worldbank.org. No endorsement implied. Workbook/quote rows are excluded from publication by project policy.

Post-2016 quotes:{raw['n_quotes']:,}; corridors:{raw['corridors']}; normalised providers:{raw['normalised_providers']};37 observed quarters2016Q2-2025Q3.2025Q2 absent.181 collection dates are outside assigned survey quarters;95 Kosovo code/label discrepancies are retained and logged, with code fields consistently used for corridor direction.1308 negative origin costs remain in immutable raw bytes and are excluded from primary cheap eligibility; invalid/negative successors enter unknown bounds.3361 source rows are non-transparent; transparent-only sensitivity is separate.

Exclusive initially cheap flow (including censoring):

{markdown(flow)}

The independent streaming implementation matches every count without importing the project linkage code. It does not externally validate true service identity. Reduced metadata adds563 candidate links but raises origin ambiguity; no links were promoted. A30-record stratified candidate sample is private, with zero externally confirmed/promoted links. Service label lifetimes and survey-label concentration are not provider survival or market shares.

A bounded public-source feasibility investigation searched one candidate from each of three strata. Generic entity/network documents do not establish the complete contemporaneous economic bundle; zero links were confirmed or promoted, and the remaining27 candidates were not externally adjudicated. See[manual identity feasibility](manual_identity_feasibility.md); it is not a validated linkage-truth sample.

Total cost is the published percentage, with rounding-aware fee/FX reconciliation from the audit. The USD200/500 columns are fixed basket identifiers; local currency amounts need not equal today\'s dollar conversion. Remote initiation in descriptive profiles means internet/mobile access only, not the full World Bank digital-remittance definition. Date-quarter, negative-FX, Russia, transparency, basket, threshold and identity alternatives retain their separate denominators.
''')
    put('data/data_integrity_tests.md','''# Data integrity evidence

independent_raw_audit.py streams the official workbook and independently implements Unicode-normalised corridor/service keys, duplicate handling, exact adjacent quarters, censoring and E1/E2 state counts. Result:PASS with no pooled flow mismatch. Existing synthetic quarter-gap, threshold, negative-cost, strict/core and leakage tests remain separate from real-data reproduction. Source checksum is verified before processing. See audits/independent_raw_audit.json and reproducibility/local_reproduction_report.json.

The historical30-table comparator now removes expected regenerated outputs before running and fails for missing/scientifically different tables, avoiding stale-output and false-success defects. It intentionally excludes presentation tables not regenerated by those stages. Original results are restored in finally blocks and compared against initial file hashes. Numeric discrepancies are retained rather than tuned away.
''')
    selected=metrics[metrics.model=='S_selected'].iloc[0]
    report=f'''# The persistence of affordable international remittance quotes

**Conditional scientific evidence report - NOT FOR SUBMISSION.** Investigator:Isaac Omoding. Generated:{now}. Code at report generation:`{sha}`. Decision:**CONDITIONAL_MORE_EVIDENCE; NOT YET PUBLICATION-READY**.

## Structured evidence summary

The study measures whether a World Bank RPW service quote costing0-3% remains at or below3% in exactly the next calendar quarter when a uniquely matching valid quote is observed. This is an offer-level retrospective endpoint, not a transaction price, provider exit, consumer saving or official aggregate SDG10.c statistic. Across{int(b.n_eligible):,} eligible initially cheap records,{int(b.n_stay+b.n_fail):,} have valid unique successors and{int(b.n_stay):,} stay cheap. Conditional continuity is{b.conditional_p_stay_core:.4f} (corridor-bootstrap95%[{b.corridor_ci95_lo:.4f},{b.corridor_ci95_hi:.4f}]); unknown successors produce extreme population bounds[{b.lower_bound:.4f},{b.upper_bound:.4f}]. Strict identity gives conditional continuity{strict.conditional_p_stay_core:.4f} but bounds[{strict.lower_bound:.4f},{strict.upper_bound:.4f}]. These are quote-record populations, not transaction-weighted markets.

The new chronological selection/calibration policy scores Brier{selected.brier:.6f} on{int(selected.n):,} retrospective outer records. Every tested period was already inspected. No operational model is selected: historical full-feature availability and genuinely new confirmation data are unavailable. A13-work competitor matrix includes newly identified service-level2026 studies, with Lim2026 full text blocked. Substantial novelty remains unresolved.

## Motivation and closest evidence

Affordable quotes can be intermittent even when corridor averages fall. The distinct question is how recorded service identity and selection into reobservation affect measured affordability continuity. Beck and Martinez Peria\'s2009 working paper/2011 article, Beck et al.2022, Lim2026, Borra and Saritha2026, official RPW/SmaRT reporting and existing analytical products constrain originality. The IMF paper includes firm-level regressions, correcting the old corridor-only description. The full head-to-head assessment and access locators are in[the literature matrix](../literature/closest_work_matrix.md) and[scientific delta](../literature/head_to_head_scientific_delta.md). No model here is claimed to beat a published study on a different target.

## Data, estimands and service identity

The independently downloaded official workbook exactly matches the frozen source hash, covering204469 post-2016 quotes across368 ordered corridors,699 normalised provider labels and37 observed waves through2025Q3.2025Q2 is absent;181 collection dates conflict with assigned quarters. Core linkage uses ordered corridor, provider, payment instrument, access point, pickup method/location and basket. Strict also requires speed/network equality. Matching is deterministic; no fuzzy links are promoted. Duplicate origins/targets are explicitly unknown. A separately coded streaming audit reproduces the full flow.

E1 conditions on unique valid reobservation. E2 allocates every unknown successor to fail/stay for lower/upper bounds. E3 describes persistence of any surveyed cheap quote among resurveyed corridor-quarters. E4 models quote reobservation separately, within the declared corridor-surveyed/unambiguous scope. Ambiguous origin duplicates remain quote-record uncertainty in E2, not independently identified economic services. Secondary thresholds, basket/horizon and selection scenarios have their own denominators.

## Information clocks and validation design

Survey collection, public availability and decision time are distinct.125 archived official-report URLs were recovered, but report capture times are only public-by bounds, not first release dates or quote-level vintage availability. Issue54 has a nominal2025 publication statement, April2026 PDF creation metadata and a September2026 present blob timestamp; these cannot be silently equated. No full-feature `available_by <= decision < target_collection_start` condition is verified. Lag1 changes history, not current-quote availability. All modelling is consequently retrospective.

Annual outer targets are2022-2025Q1 (13 target waves). Training labels precede the first outer origin. Phase2 reserves six available earlier target quarters:two tune finite hyperparameter candidates,two fit sigmoid/isotonic calibrators,two select methods/families. Base models refit on proper+tuning records and remain fixed through calibration, selection and outer scoring. The legacy full-training design is preserved separately. Deterministic20% provider/corridor holdouts rebuild all target-dependent histories without heldout groups; unknown-group rates fall back to admissible training histories. They are historical transfer sensitivities, not a future holdout.

Provider holdouts are based on normalised source labels. Without an externally validated alias/legal-entity crosswalk, they cannot guarantee that every renamed form of the same firm is unseen. No independent legal-entity transportability claim is made.

## Probability models and calibration

{markdown(comparison)}

Brier is primary; log loss, discrimination, failure AUPRC, calibration and within-quarter capacity are secondary. Calibration-in-the-large previously used a +/-10 root bracket that truncated the near-certain constant baseline; phase2 uses corrected bracketing and returns undefined calibration for single-class samples. Model artifacts remain private, with save/reload parity checked. The selected policy is a research comparison; no deployable winner is declared.

Annual choices:

{markdown(selection)}

## Paired uncertainty and heterogeneity

{markdown(paired[['analysis','model_a','model_b','resampling','brier_diff','ci95_lo','ci95_hi']])}

Corridor/provider bootstraps and crossed pigeonhole/time-block sensitivities preserve paired comparisons. The latter are not exact arbitrary multiway inference, and13 waves give only about three four-quarter blocks. Quote, corridor, provider and quarter weighting target different populations. All comparisons are exploratory, without multiplicity-adjusted confirmation. Per-wave, regional and income results are retained; Uganda\'s20 test failures across3 corridors fail the100-event reporting gate.

Limited synthetic coverage stress (not RPW evidence):

{markdown(simulation)}

The simulation deliberately includes crossed-group and serially correlated time shocks. Separate resampling axes cannot be assumed to capture every dependence component; the measured coverage rates have substantial Monte Carlo uncertainty and do not validate a universal95% coverage claim. Real-data intervals condition on fitted predictions and do not include full retraining/selection uncertainty.

The amended joint corridor/provider/time sensitivity gives selected policy minus spline Brier difference -0.005388 with interval[-0.011730,+0.000457]. Thus even retrospective superiority of the predeclared selection policy is not robust across dependence assumptions. The joint method achieved0.86 coverage in the limited stress simulation, still below nominal0.95; no exact inferential guarantee is claimed.

## Hypothetical monitoring utility

{markdown(capacity[(capacity.analysis=='phase2')&(capacity.capacity==.2)][['rule','reviewed','failures_total','failures_captured','recall','precision','false_alerts']])}

Policies select equal numbers within each origin quarter at5/10/20/30% capacity. Capacity uncertainty reranks in300 corridor resamples. False alerts are observed stays selected for review, not harm measured in practice. Relative cost scenarios assume a review identifies an observed failure and cannot establish monetary saving, intervention effectiveness or consumer availability.

The preceding E1 queue uses future valid-reobservation membership, which would be unavailable at an origin decision. The following correction scores **all eligible origin quotes**, preserving unknown outcomes instead of selecting the queue using future membership. These are E1-score extrapolation scenarios with partial-identification bounds, not validated joint observation/price forecasts:

{markdown(allcap[allcap.capacity==.2][['rule','n_all_eligible','n_known_valid','n_unknown','reviewed','known_failures_captured','unknown_reviewed','all_failure_recall_lower','all_failure_recall_upper']])}

Among24556 origins,4889 outcomes are unknown. At20% capacity the selected policy reviews4905 quotes, captures1611 known failures, and reviews1060 unknowns; all-failure recall can range from0.2167 to0.5726 under extreme allocations. Overlapping bounds prevent an identified population ranking of policies. Conditional matched-sample gains cannot be sold as operational benefit.

## Identity, source and missingness sensitivity

{markdown(sensitivities[['scenario','n_eligible','n_valid_pairs','conditional_p_stay_core','lower_bound','upper_bound','origin_collision_rows']])}

Core and strict conditional point estimates are close while the strict bounds are wider. Reduced metadata increases duplicate ambiguity and is not promoted. Thresholds around3% alter the population as well as crossing classification; USD500 and a true two-quarter horizon are separate products/estimands. A two-quarter2025Q1-to-Q3 link explicitly spans a missing intermediate wave, never a one-quarter transition. Date-quarter/transparency/Russia/negative-FX alternatives are sensitivities rather than silent data repairs.

Separate reobservation comparisons:

{markdown(observation[['year','model','n','brier','log_loss','cal_slope']])}

The earlier negative2022-2023 ridge-versus-prevalence finding is preserved in the legacy outputs. New tree comparisons do not identify why a quote is absent. MAR/IPW is an assumption-labelled valid-price observation scenario within the corridor-surveyed scope:

{markdown(ipw[['year','n_eligible','n_observed','observed_stay','ipw_mar_p_stay','effective_sample_size','share_clipped']])}

Clipping does not repair MNAR selection. Pattern-mixture log-odds shifts and extreme bounds remain explicit. No causal doubly robust correction or service-exit survival model is identified. Price-component, continuous-cost and shift summaries are supplementary; observed quote-label concentration is not market concentration.

## Historical transfer and fitted sensitivities

{markdown(transfer[['scenario','model','n','brier','log_loss','cal_slope']])}

Different scenarios may select different test records, so cross-scenario score differences are not automatically paired treatment effects. Main families within each scenario use identical eligible records. Group holdouts exclude heldout target histories; current surveyed covariates remain an explicitly retrospective information scenario.

## Reproducibility and limitations

The official source, cohort, flow and descriptive quantities reproduce. The corrected strict1e-9 historical comparator reports14 exact tables,2 timing-only differences and14 nonmatching tables (including environment metadata). Windows logistic/spline calculations differ slightly from frozen Linux outputs: maximum lag0 Brier delta about1.11e-7, lag1 about2.29e-5; GBM/RF reproduce to floating-point precision. One legacy pooled capture count differs by one case. Strict reproduction is not claimed successful, no tolerance was widened, and all historical artifacts were restored. The subsequent calibration-offset correction is separately versioned. Python/package versions, commands, fingerprints and checkpoint durations are recorded; original source PDFs and row-level data are excluded from public delivery.

## Recovered original pilot and score decomposition

Local execution recovered the earlier pilot code and reference parquet that were inaccessible to the cloud session. Unchanged archived programs were rerun with a private I/O adapter; source fields were compared against the independently reacquired input. Pilot reproduction:GBM Brier{pilot['spline_results.json']['boost_brier']:.9f};spline Brier{pilot['spline_results.json']['spline_brier']:.9f};n={pilot['spline_results.json']['n']:,}. See[the recovery audit](../audits/recovered_pilot_reproduction.json).

Rebuilding the old openpyxl/string encoding directly from the independently downloaded official workbook exactly reconstructs the old parquet bytes (SHA256 d371c8b2e09b3f7698803dbfc20b85550f6206e4d30a4974b7a6051060c3493f). GBM/count reproduce the reported pilot exactly; spline remains slightly different from its reported0.1441454123434313. The initially source-adapted pandas cache produced18032 rather than18030 test pairs and is retained separately. Blank-string versus missing-value semantics differ across encodings, so normalised value equality alone was insufficient. See pilot_cache_rebuild.json, pilot_source_content_comparison.csv and source_adapted_pilot_rerun.json under audits/.

The pilot evaluates origin years2022-2024; phase1 evaluates target years2022-2024. Their net18-record count difference conceals different memberships:{pilot['cohort_overlap']['shared']:,} shared,{pilot['cohort_overlap']['pilot_only']:,} pilot-only,{pilot['cohort_overlap']['phase1_only']:,} phase1-only. Transparency filtering, duplicate handling, local-amount versus USD-basket identity, text normalisation, feature definitions, annual refit windows and hyperparameters also differ. Scores are not exact head-to-head algorithm comparisons. A prior exploratory corridor holdout was also recovered; its existence is preserved rather than misrepresented as absent from all earlier research.

Brier diagnostics decompose the fixed-bin predictor into uncertainty, resolution and reliability, retaining the difference between continuous and binned Brier as an explicit residual. It is not silently treated as an exact decomposition of continuous predictions:

{markdown(decomp[['model','raw_brier','binned_brier','reliability','resolution','uncertainty','binning_residual']])}

The main limitations are unverified public timing, no new temporal holdout, uncertain real service identity, nonrandom/changed survey coverage, missing successors, limited independent waves and unresolved closest-work novelty. Neither a statistically favourable row-level score nor a dashboard clears those gates. The second implementation audit is not external human peer review.

The later bounded public identity feasibility search examined three of the30 private stratified candidates. Entity/network context did not establish their historical economic bundles; zero links were confirmed/promoted and27 remain unadjudicated. See[the feasibility record](../data/manual_identity_feasibility.md). This does not estimate a false-merge rate.

## Conclusion and conditional manuscript outline

The current evidence supports a reproducible retrospective measurement report: conditional affordability continuity is stable to several definitions, while population uncertainty depends materially on observation and identity. It does not validate prospective forecasting or prove substantial novelty. A narrower methods/measurement article may become defensible after full competitor adjudication and stronger linkage/inference review; a prediction-led article additionally needs release-aware independent confirmation.

A future draft should follow:Introduction (specific novelty),Methods (E1-E4,clocks,linkage,selection,validation),Results (flow,bounds,paired comparisons,negative findings),Discussion (limitations/practical scope),Declarations and Supplements. No candidate submission manuscript is supplied while major gates remain unresolved.

## Declarations requiring investigator confirmation

Investigator:Isaac Omoding. Affiliations, funding, competing interests, author contributions and institutional/ethics requirements:INVESTIGATOR TO CONFIRM. Data attribution:World Bank RPW; no endorsement. AI assistance:earlier Claude Code and this Codex execution assisted code, analysis and drafting under investigator direction; human verification is required. No additional authors are invented. No journal or preprint submission is authorised.

## References and evidence navigation

Validated source links and access depths are in[closest_work_matrix.md](../literature/closest_work_matrix.md); bibliographic records are in[references.bib](references.bib). Numbered figures and tables have programmatic source inventories and legends. See[the final verdict](../assessment/PUBLICATION_VERDICT.md),[remaining blockers](../assessment/REMAINING_BLOCKERS.md) and[reproduction comparison](../reproducibility/source_to_results_comparison.csv).
'''
    if (OUT/'models/final_stress_metrics.csv').exists():
        stress=load('models/final_stress_metrics.csv');stress=stress[stress.scope=='pooled']
        extra='## Final audit-driven robustness checks\n\n'+markdown(stress[['scenario','model','n','brier','log_loss','cal_slope']])+'\n\nThese fixed annual full-training references exclude the largest pre-2022 development provider/corridor, purge its target histories, or change transparency/FX/date handling. They do not refit or tune the selected policy. Provider labels are withheld. Fixed prior-quote/history-support strata are in models/history_overlap_support.csv. Pre/post-2022Q3 KS statistics and channel/region composition are descriptive; dependent-panel IID p-values and causal design-change claims are not reported.\n\n'
        report=report.replace('## Reproducibility and limitations',extra+'## Reproducibility and limitations')
    if (OUT/'models/no_identity_history_metrics.csv').exists():
        a=load('models/no_identity_history_metrics.csv');a=a[a.scope=='pooled']
        extra='The stricter historical identity ablation removes provider target-rate history **and** own-service cost/change lags. Removed lag values are fixed zero with availability0, after an all-NaN sklearn histogram-binning failure. It retains the earlier provider-rate-only ablation as a separate result:\n\n'+markdown(a[['scenario','model','n','brier','log_loss']])+'\n\n'
        report=report.replace('## Reproducibility and limitations',extra+'## Reproducibility and limitations')
    if (OUT/'models/continuous_group_trend.csv').exists():
        extra='Secondary continuous-price reference (not E1 probabilities), using annual past-only shrunk provider/corridor cost changes:\n\n'+markdown(load('models/continuous_group_trend.csv'))+'\n\nCompare continuous_cost_metrics.csv; these are matched initially cheap outcomes, not prices of missing services.\n\n'
        report=report.replace('## Reproducibility and limitations',extra+'## Reproducibility and limitations')
    if (OUT/'models/conventional_reference_comparisons.csv').exists():
        a=load('models/conventional_reference_comparisons.csv');a=a[(a.model=='S_selected')&(a.resampling=='crossed_corridor_provider_time_block')]
        extra='## Named conventional references and Brier skill\n\n'+markdown(a[['model','reference','brier_model','brier_reference','brier_skill','relative_brier_diff','brier_diff','ci95_lo','ci95_hi']])+'\n\nSkill is1 minus model/reference Brier, and relative difference is model-minus-reference divided by reference. All four references are reported. Calibrated ridge has the lowest pooled conventional Brier here; naming it best is a post hoc description, not independent selection. The already inspected outcomes are not a confirmatory leaderboard. The joint intervals retain their undercoverage limitation. Paired supported subgroup intervals versus calibrated ridge are in models/subgroup_paired_uncertainty.csv; Uganda remains NOT_ESTIMABLE.\n\n'
        report=report.replace('## Reproducibility and limitations',extra+'## Reproducibility and limitations')
    put('manuscript/conditional_research_report.md',report)
    verdict=f'''# R01 - Scientific Publication Verdict

Analysis date(UTC):{now}
Commit at evaluation:`{sha}`
Source vintage:2025Q3 workbook;SHA256 `f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8`
Scientific article type:conditional retrospective measurement/validation report
FINAL DECISION:**CONDITIONAL_MORE_EVIDENCE**
**NOT YET PUBLICATION-READY**

## One-paragraph answer

The real source, quote linkage and measurement counts were independently re-executed; new chronological calibration/selection, group-transfer, missingness and dependence sensitivities were run. The evidence supports a careful retrospective measurement report, with conditional continuity{b.conditional_p_stay_core:.6f} and core bounds[{b.lower_bound:.6f},{b.upper_bound:.6f}]. Strict identity keeps the point estimate near{strict.conditional_p_stay_core:.6f} but widens bounds to[{strict.lower_bound:.6f},{strict.upper_bound:.6f}]. Operational model selected:**NONE**. Public predictor availability, new independent temporal confirmation, external bundle validation and a substantial novelty verdict remain unresolved.

## Contribution versus closest studies

Service-level RPW analysis is already present in the IMF paper and2026 studies. The candidate delta is exact-quarter quote continuity with explicit identity/observation uncertainty, not geography or model substitution. Lim2026 full text remains inaccessible; substantial novelty is not established. See[literature matrix](../literature/closest_work_matrix.md) and[head-to-head audit](../literature/head_to_head_scientific_delta.md).

## Provenance, cohort and missingness

204469 quotes;368 corridors;699 normalised provider labels;37 observed quarters2016Q2-2025Q3;2025Q2 absent.45343 eligible cheap origins;36429 uniquely valid next-quarter pairs;29546 stays,6883 failures,8914 unknown successors. Independent dictionary audit matches every flow state. See[source manifest](../data/source_manifest.json),[raw audit](../data/raw_data_audit.md),[bounds table](../tables/supplementary_overall_bounds.csv) and[independent audit](../audits/independent_raw_audit.json).

## Information timing

TIMING_PARTIAL documentary evidence;TIMING_FAIL for verified early warning.125 archived report URLs do not provide historical quote-level availability or revision vintages. No verified full-feature decision date before target collection; no lead-time claim. See[availability registry](../data/release_availability_registry.csv).

## Model evaluation and uncertainty

Chronological research-policy outer Brier:{selected.brier:.6f},n={int(selected.n):,}; all outcomes previously inspected. Full ranking:

{markdown(comparison)}

Paired differences and corridor/provider/time/crossed sensitivities are in[paired_dependence.csv](../models/paired_dependence.csv).13 independent target waves limit time precision. Earlier reobservation failures remain reported; Uganda has insufficient events. Group-transfer sensitivities are historical, not independent temporal confirmation. Strict historical numeric reproduction failed at1e-9 despite exact cohort/measurement reproduction and unchanged headline tree scores;[differences are retained](../reproducibility/local_table_comparison.csv).

## Operational interpretation

Review-at-capacity results are hypothetical observed-sample triage. No transaction saving, causal benefit, true service exit or market availability is observed. No deployable model selected. See[capacity table](../models/decision_capacity.csv) and[scenario costs](../models/decision_cost_scenarios.csv).

## The12 science gates

{markdown(gate)}

## Blockers and executed work

See[ordered blockers](REMAINING_BLOCKERS.md),[execution report](final_execution_report.md),[claim ledger](claim_evidence_ledger.csv),[commands](../reproducibility/commands_executed.jsonl) and[research report](../manuscript/conditional_research_report.md). No completion, independence or significance is manufactured for blocked gates.

## Handoff and GitHub

Scientific files are reviewed through[PR3](https://github.com/Isaac25-lgtm/remittance-price-intelligence/pull/3). Exact checked integration state and downloadable ZIP are recorded in[Git/download links](../deliverables/git_and_download_links.md) and zip_verification.json. The local ZIP is under research_completion/deliverables. A source commit is not itself proof of hosted dashboard redeployment.

## Investigator verification

Confirm authorship, citations/competitor overlap, lawful attribution, funding/conflicts, institutional requirements, final scientific interpretation and venue before any submission. No journal submission or preprint posting was performed or authorised.
'''
    verdict=verdict.replace('FINAL DECISION:**CONDITIONAL_MORE_EVIDENCE**','FINAL DECISION:**CONDITIONAL GO / CONDITIONAL_MORE_EVIDENCE**')
    verdict=verdict.replace('## Operational interpretation','The amended joint corridor/provider/time interval for selected policy minus spline is **[-0.011730,+0.000457]**, crossing zero (point -0.005388). Stress simulation coverage0.86 still fails to establish nominal95% coverage. See[joint sensitivity](../models/joint_dependence_sensitivity.csv). Robust superiority is not established.\n\n## Operational interpretation')
    verdict=verdict.replace('Review-at-capacity results are hypothetical observed-sample triage.','Matched-sample review conditions on future reobservation membership. The corrected[all-origin scenario](../models/all_origin_capacity_bounds.csv) scores24556 eligible quotes,4889 with unknown outcomes. At20% budget selected-policy population recall bounds are0.2167-0.5726; no identified population policy ranking follows. Review-at-capacity results are hypothetical triage.')
    put('assessment/PUBLICATION_VERDICT.md',verdict)
    put('PUBLICATION_VERDICT.md','# Publication verdict\n\n**CONDITIONAL_MORE_EVIDENCE - NOT YET PUBLICATION-READY.**\n\nSee[the complete scientific verdict](assessment/PUBLICATION_VERDICT.md) and[conditional research report](manuscript/conditional_research_report.md).')
    put('assessment/reviewer_challenges.md','''# Independent scientific challenge checklist

This is a second-pass audit against the directive, not an external human peer review.

- Is a recorded quote the same economic service after metadata/rebrand changes?Exact matching cannot prove this; manual historical validation remains unresolved.
- Do target costs exist for missing services?No; extreme/MNAR scenarios are not recovered outcomes.
- Were features public before target collection?Not established; reject forecasting language.
- Are13 waves enough for joint time/provider/corridor inference?They constrain precision; resampling sensitivity is not universal coverage.
- Could validation-selection choices be optimistic?All old data were inspected; inner chronological selection is honest retrospective development, not confirmation.
- Does adding ML itself establish novelty?No. Firm-level and digital-pricing competitors exist; Lim full text is a major unresolved gate.
- Does an anonymous provider metric reveal a single firm?No individual-provider performance table is released; only broad subgroup/transfer aggregates and private diagnostics are retained.
- Does numeric reproduction pass strictly?No; small platform/solver-associated differences are documented, not erased.
- Is the final report a submission-ready manuscript?No. The report and outline are conditional, and human review/sign-off remains required.
''')
    put('manuscript/investigator_signoff_checklist.md','''# Investigator sign-off required

- Verify author list, affiliations, contributions, funding and conflicts; no unknown facts have been invented.
- Read the closest full texts, particularly Lim2026, and approve the novelty/scope claim.
- Review service identity and selection interpretation, absence of public lead time, and limited temporal inference.
- Confirm dataset attribution/permissions and applicable institutional requirements.
- Check every reported number, figure and source against the locked tables/ledgers.
- Confirm AI assistance disclosure and choose a venue only after scientific blockers are resolved.
- Personally authorise any future submission/preprint. None has been made.
''')
    put('manuscript/reporting_checklist.md','''# Reporting checklist

Finance/development observational measurement reporting, not claimed clinicalTRIPOD compliance. Estimands, population, source dates, quote/transaction distinction, identity, attrition, timing, leakage, preprocessing folds, model-selection history, calibration, group/temporal limits, paired inference, negative results, missing-data assumptions, availability, licensing and authorship declarations are documented. Remaining gaps are explicitly marked in publication_gates.csv and REMAINING_BLOCKERS.md. Source PDFs and row-level artifacts are not redistributed.
''')
    for p in sorted((OUT/'tables').glob('*.csv')):put('tables/'+p.stem+'.md','# '+p.stem.replace('_',' ')+'\n\n'+markdown(pd.read_csv(p)))
    shutil.copy2(OUT/'literature/references.bib',OUT/'manuscript/references.bib')
    put('manuscript/supplementary_material.md','''# Supplementary material

S1:data/variable_dictionary.csv plus docs/DATA_DICTIONARY.md, validation/feature_asof_registry.csv and data/raw_data_audit.md.
S2:data/inclusion_exclusion_flow.csv, identity_collision_audit.csv, independent_raw_audit.json and source manifests.
S3:models/model_registry.json, model_comparison.csv, calibration_selection.csv, annual_selection.csv, continuous_cost_metrics.csv and all negative reobservation results.
S4:models/paired_dependence.csv, joint_dependence_sensitivity.csv, weighting_sensitivity.csv, decision_capacity_ci.csv, all_origin_capacity_bounds.csv, brier_decomposition.csv, reliability_cluster_intervals.csv and validation/dependence_bootstrap_methods.md. Synthetic stress results are in validation/bootstrap_simulation.csv.
S5:literature/closest_work_matrix.md, search_log.csv and head_to_head_scientific_delta.md.
S6:reproducibility/environment_lock.txt, version_manifest.json, commands_executed.jsonl, source_to_results_comparison.csv and the public data attribution.

Paths above are relative to research_completion except the existing repository dictionary. The full report is conditional, not for submission. No source PDF or private row-level supplement is distributed.
''')
    put('README.md',f'''# R01 local publication-completion dossier

Run:r01-local-completion-2026-10-20.**CONDITIONAL_MORE_EVIDENCE - NOT YET PUBLICATION-READY.** Operational model:**none**.

Start with[the verdict](assessment/PUBLICATION_VERDICT.md),[complete evidence report](manuscript/conditional_research_report.md),[executed-stage report](assessment/final_execution_report.md),[blockers](assessment/REMAINING_BLOCKERS.md) and[ZIP/Git retrieval](deliverables/git_and_download_links.md).

Measurement:conditional continuity{b.conditional_p_stay_core:.4f},core bounds[{b.lower_bound:.4f},{b.upper_bound:.4f}],strict bounds[{strict.lower_bound:.4f},{strict.upper_bound:.4f}]. New temporal-selection/transfer/dependence scenarios remain retrospective; no independent future wave or verified public lead time. Source and cohort audits include a separately coded streaming implementation. Numeric reproduction discrepancies are explicit.

Navigate:data/;literature/;validation/;models/;numbered tables/figures/;assessment/;reproducibility/;manuscript/;deliverables/. private_runtime is ignored and excluded from publication. Original phase1 results remain under ../results and are not overwritten. All public outputs are aggregates with World Bank RPW attribution; no endorsement implied.
''')
    put('deliverables/START_HERE.md',f'''# R01 publication-completion handoff

**CONDITIONAL_MORE_EVIDENCE - NOT YET PUBLICATION-READY.** Operational model:none. Investigator:Isaac Omoding. This is a conditional retrospective research dossier, not a journal submission or endorsed consumer service.

- [Scientific verdict](research_completion/assessment/PUBLICATION_VERDICT.md)
- [Complete conditional evidence report](research_completion/manuscript/conditional_research_report.md)
- [Execution evidence](research_completion/assessment/final_execution_report.md)
- [Remaining blockers](research_completion/assessment/REMAINING_BLOCKERS.md)
- [Source/availability audit](research_completion/data/historical_publication_timing.md)
- [Closest-work matrix](research_completion/literature/closest_work_matrix.md)
- [Models](research_completion/models/model_comparison.csv)
- [Paired uncertainty](research_completion/models/paired_dependence.csv)
- [Reproduction instructions](README.md)
- [Git/download state](research_completion/deliverables/git_and_download_links.md)

Reproduce locally with Python3.12 and research_completion/reproducibility/environment_lock.txt; set OMP/BLAS/MKL/NUMEXPR threads to2. Acquire/check the official workbook privately, then run completion_data.py,completion_pipeline.py,completion_report.py,completion_figures.py and the final audit/packager. Original results are immutable; exact cross-platform numeric reproduction is not asserted. The live aggregate-only research dashboard is https://isaac-remittance-research.streamlit.app/; redeployment must be verified separately.

The World Bank, Remittance Prices Worldwide, available at http://remittanceprices.worldbank.org (CC BY4.0). No endorsement. No raw data, provider quote records, predictions, fitted binaries, secrets or copyrighted source PDFs are included.
''')
    start=OUT/'deliverables/START_HERE.md'
    start.write_text(start.read_text(encoding='utf-8').replace('](research_completion/','](../').replace('](README.md)','](../../README.md)'),encoding='utf-8')
    put('deliverables/publication_brief.md',f'''# Publication brief

For a nontechnical reader:an affordable surveyed quote often remains affordable next quarter when the same quote can be found again. The larger uncertainty is what missing or changed quote records mean. Our conditional estimate is{b.conditional_p_stay_core:.1%}; the all-origin range is{b.lower_bound:.1%}-{b.upper_bound:.1%},and strict identity widens it further. Missing records cannot be called provider exit.

For a technical reader:E1/E2 measurement and temporal/group-transfer benchmarking were executed from an independently hash-verified official workbook. Chronological calibration/selection, paired cluster/block/crossed sensitivities and MAR/MNAR scenarios are explicit. No public-information lead time or untouched confirmation exists; substantial novelty remains unresolved. Decision:CONDITIONAL_MORE_EVIDENCE;no operational model. See the canonical report and gate ledger.
''')
    put('assessment/final_execution_report.md',f'''# Actual execution status

Generated:{now};code:{sha}. REAL-DATA EXECUTION is distinct from synthetic tests and reused legacy aggregates.

|Phase|Status|Evidence|
|---|---|---|
|P0 inventory/protection|DONE|audits/initial_repo_inventory.json; private legacy snapshot; original hashes|
|P1 competitor audit|PARTIAL|13 relevant sources; two public full-text downloads plus IMF browser methods/results; Lim full text blocked; search_log.csv|
|P2 source/timing|DONE acquisition;PARTIAL timing|exact official bytes/hash;125 archived report URLs; no proven quote-level lead time|
|P3 measurement/observation|DONE with identity-truth limitation|core/strict/reduced, flow, bounds, E3/E4, MAR/MNAR, source alternatives; independent streaming count audit PASS|
|P4 protocol/leakage|DONE|committed protocols/amendments; fold, history and future-clock guards|
|P5 models/selection|DONE retrospective|finite chronological tuning/calibration; all8 original families plus recent-history reference; no operational promotion|
|P6 robustness/uncertainty|DONE bounded scope|group transfer, selected fitted sensitivities, paired corridor/provider/time/crossed sensitivity, weights, capacity, continuous-cost and associative diagnostics|
|P7 independent confirmation|BLOCKED/NOT_AVAILABLE|no newer official successor; frozen future-wave evaluator|
|P8 report/verdict|DONE conditional|complete scientific report/outline and12-gate decision; no submission manuscript|
|P9 outputs/QA/handoff|See final audit/ZIP verification|programmatic tables/figures, test report, allowlist and archive validation|
|P10 Git integration|See deliverables/git_and_download_links.md|reviewed PR/CI/main verification is separately recorded; no false merge/deployment claim|

Exact commands/exit codes, timing and peak RSS are in reproducibility/commands_executed.jsonl and progress.json. Some initial read-only shell/web discovery actions have date-level evidence rather than exact per-query timestamps; this limitation is not represented as a complete second-by-second transcript. Source acquisition attempts and statuses are in data/acquisition_log.jsonl. Failed baseline tests and strict reproduction are preserved. Model/metric code was committed before new phase2 scoring; later report/packaging files may change during analytical jobs without being imported by those jobs.

Not performed or not scientifically justified:real future-wave confirmation; public quote vintage reconstruction; external human peer review; validated manual bundle/rebrand truth; exact multiway finite-sample coverage simulation; causal/survival/transaction-saving analysis; new paid data; additional boosting libraries/deep models; submission/preprint posting. These do not receive fabricated outputs. See REMAINING_BLOCKERS.md for implications.
''')
    notice=dict(analysis_date=now,verdict='CONDITIONAL_MORE_EVIDENCE',operational_model='NONE',confirmation='NOT_AVAILABLE',timing='NO VERIFIED PUBLIC LEAD TIME',report_url='https://github.com/Isaac25-lgtm/remittance-price-intelligence/blob/main/research_completion/assessment/PUBLICATION_VERDICT.md',selected_policy_brier=float(selected.brier),n_outer=int(selected.n))
    (OUT/'assessment/dashboard_notice.json').write_text(json.dumps(notice,indent=2),encoding='utf-8')
    print('Conditional report, gate ledger, supplemental methods and navigation generated',flush=True)

if __name__=='__main__':main()
