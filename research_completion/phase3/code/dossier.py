"""Generate the conditional dossier from executed Phase3 and frozen Phase2 aggregates."""
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import pickle
import subprocess
import numpy as np
import pandas as pd
from literature import md,prose_spacing

ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'research_completion/phase3'

def table(d):
    def fmt(x):
        if pd.isna(x):return ''
        if isinstance(x,(float,np.floating)):return f'{x:.6g}'
        return str(x).replace('|','/')
    lines=['| '+' | '.join(d.columns)+' |','| '+' | '.join('---' for _ in d.columns)+' |']
    lines+=['| '+' | '.join(fmt(x) for x in row)+' |' for row in d.itertuples(index=False,name=None)]
    return '\n'.join(lines)

def main():
    sha=subprocess.check_output(['git','rev-parse','HEAD'],text=True,cwd=ROOT).strip()
    stamp=dt.datetime.now(dt.timezone.utc).isoformat()
    scenarios=pd.read_csv(OUT/'identity/LINKAGE_SCENARIO_RESULTS.csv').set_index('scenario')
    a=scenarios.loc['cc1_3pct_core'];b=scenarios.loc['cc1_3pct_strict'];e3=scenarios.loc['cc1_3pct_core_E3']
    effects=pd.read_csv(OUT/'inference/PAIRED_MEASUREMENT_EFFECTS.csv')
    contrast=effects[(effects.contrast=='strict_minus_core_width')&(effects.hac_lag==4)].iloc[0]
    wave=pd.read_csv(OUT/'tables/paired_wave_identity.csv')
    sensitivities=pd.read_csv(OUT/'tables/measurement_sensitivities.csv')
    infinity=0
    with (OUT/'private_runtime/independent_source.pkl').open('rb') as f: records=pickle.load(f)['records']
    infinity=sum(math.isinf(r[k]) for r in records for k in [4,5])
    (OUT/'identity/source_nonfinite_audit.json').write_text(json.dumps(dict(source_cost_cells=len(records)*2,infinite_cost_cells=infinity,existing_finite_cost_results_affected=False,source_sha256='f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8'),indent=2),encoding='utf-8');del records
    assert infinity==0
    claims=[]
    def claim(cid,text,artifact,locator='',kind='EXECUTED_AGGREGATE',pipeline='code/measurement.py'):
        text=prose_spacing(text)
        claims.append(dict(claim_id=cid,statement=text,claim_type=kind,evidence_artifact=artifact,locator=locator,pipeline=pipeline,source_commit_at_generation=sha,publication_status='conditional dossier; not author-approved manuscript'))
        return text+f' [{cid}]'
    source=claim('M01','The verified source contains 204,469 post-2016 quote records across 37 observed waves, 2016Q2-2025Q3; 2025Q2 is absent. The current official download has 50,780,339 bytes and the frozen SHA256 f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8.','timing/source_acquisition.csv','rpw_current.xlsx',pipeline='code/sources.py')
    flow=claim('M02',f'The primary source-record cohort has {int(a.n_eligible):,} eligible affordable origins: {int(a.n_stay):,} recorded stays, {int(a.n_fail):,} observed threshold failures and {int(a.n_unknown):,} unknown successors. The last observed wave contributes 2,083 separately right-censored affordable origins.','identity/LINKAGE_SCENARIO_RESULTS.csv','cc1_3pct_core')
    conditional=claim('M03',f'Among {int(a.n_valid):,} uniquely valid core successor pairs, continuity is {a.conditional:.8f} ({100*a.conditional:.2f}%). Among all eligible origin records, its missing-outcome identification interval is [{a.lower:.8f}, {a.upper:.8f}]. These are different targets.','identity/LINKAGE_SCENARIO_RESULTS.csv','cc1_3pct_core')
    identity=claim('M04',f'Strict matching keeps the same {int(b.n_eligible):,} origins, retains {int(b.n_valid):,} valid pairs, and gives conditional continuity {b.conditional:.8f}. Its bounds are [{b.lower:.8f}, {b.upper:.8f}]. The width increases by {100*(b.unknown_share-a.unknown_share):.4f} percentage points, although the conditional point changes by {100*(b.conditional-a.conditional):.4f} points.','identity/LINKAGE_SCENARIO_RESULTS.csv','cc1_3pct_core and cc1_3pct_strict')
    paired=claim('M05',f'Of the 36 eligible origin waves, {(wave.additional_unknown>0).sum()} have strictly wider strict bounds; none narrows. There are 35 waves with valid E1 pairs. The prespecified lag4 wave-HAC sensitivity interval for the pooled width difference is [{100*contrast.sensitivity_lower:.2f}, {100*contrast.sensitivity_upper:.2f}] percentage points. This is not a validated robust 95% interval.','inference/PAIRED_MEASUREMENT_EFFECTS.csv;tables/paired_wave_identity.csv','strict_minus_core_width;hac_lag4',pipeline='code/inference.py')
    corridor=claim('M06',f'Corridor survey monitoring gives {int(e3.n_stay):,}/{int(e3.n_valid):,} = {100*e3.conditional:.2f}% continuity of at least one cheap surveyed quote. Its {int(e3.n_eligible):,} eligible origin corridor-quarters include {int(e3.n_eligible-e3.n_valid):,} unknown follow-up corridor surveys. Phase3 excludes270 right-censored final-wave corridor-quarters from the earlier9,438-origin display; the observed follow-up denominator and conditional rate are unchanged. It does not measure persistence of the same offer and is not SmaRT.','identity/LINKAGE_SCENARIO_RESULTS.csv;../tables/supplementary_corridor_estimand.csv','cc1_3pct_core_E3')
    e4=claim('M07',f'E4 over all primary eligible records is {100*a.e4_unique:.4f}% for unique core reobservation and {100*a.e4_valid:.4f}% for unique valid-cost reobservation. This denominator differs from the earlier conditional E4 modelling population.','identity/LINKAGE_SCENARIO_RESULTS.csv','cc1_3pct_core')
    units=claim('M08','Eligible primary origins span359 corridors and474 provider labels, of which444 labels have valid pairs. The quote-weighted conditional result must not be called an average-provider or average-corridor probability.','tables/independent_unit_support.csv','scope all',pipeline='code/identity_audit.py')
    pre=sensitivities[(sensitivities.scenario=='cc1_3pct_core')&(sensitivities.stratum=='pre_2022Q3')].iloc[0]
    post=sensitivities[(sensitivities.scenario=='cc1_3pct_core')&(sensitivities.stratum=='post_2022Q3')].iloc[0]
    shifts=claim('M09',f'Core conditional continuity is {100*pre.conditional:.2f}% before2022Q3 and {100*post.conditional:.2f}% thereafter. Core unknown shares are {100*pre.unknown_share:.2f}% and {100*post.unknown_share:.2f}%. These are composition-sensitive descriptions, not an identified effect of a survey change.','tables/measurement_sensitivities.csv','fixed_sensitivity pre/post2022Q3')
    weighted=sensitivities[(sensitivities.scenario=='cc1_3pct_core')&(sensitivities.stratum_field=='weighting')]
    weights=claim('M10',f'Equal-corridor and equal-provider-label conditional means are {100*weighted.iloc[0].conditional:.2f}% and {100*weighted.iloc[1].conditional:.2f}%, excluding groups without valid pairs for that conditional mean. This weighting change is material; it changes the estimand and does not correct survey selection.','tables/measurement_sensitivities.csv','weighting cc1_3pct_core')
    models=claim('P01','The frozen Phase2 selected research policy has Brier0.130763 on19,667 previously inspected records. Raw RF0.128059 and raw GBM0.128106 have lower observed Brier. Calibrated ridge0.134707, calibrated spline0.134912 and raw spline0.136151 remain reported. No operational model is selected.','inference/DEFINITIVE_MODEL_COMPARISONS.csv','pooled Phase2 comparison',pipeline='Phase2 frozen models; no Phase3 model search')
    precision=claim('P02','The amended joint corridor/provider/time interval for selected-policy minus raw spline is[-0.011730,+0.000457]. The previous small simulation had0.86 coverage across50 replicates, so its nominal95% interpretation is not validated. New wave-HAC intervals are assumption sensitivities and cannot erase that failure.','tables/phase2_joint_dependence_sensitivity.csv;../validation/bootstrap_simulation.csv','selected vs raw spline; simulation joint resampling',pipeline='Phase2 joint_dependence.py; code/inference.py')
    capacity=claim('P03','At the20% all-origin review capacity, the selected policy reviews4,905 of24,556 eligible records;4,889 outcomes are unknown overall. All-failure recall bounds are0.216707-0.572562. No population-wide policy ranking, avoided harm or consumer saving is established.','tables/phase2_all_origin_capacity_bounds.csv','S_selected;capacity0.2',pipeline='Phase2 scripts/all_origin_capacity.py')
    reproduction=claim('R01','The original strict1e-9 comparator still has14 exact matches,2 timing-only matches and14 differing tables. Independent count checks match in all20 fields tested. Separate locked Windows runs give exactly equal ridge and spline predictions on the selected2022 fold; this is not proof of Linux numeric identity.','reproducibility/STRICT_LEGACY_COMPARISON.csv;reproducibility/RUN_COMPARISONS.csv;assessment/independent_count_comparison.csv','all rows',pipeline='code/reproduction.py')
    default=json.loads((OUT/'reproducibility/locked_real_1.json').read_text())['results']
    tight=json.loads((OUT/'reproducibility/tight_real_1.json').read_text())['results']
    numeric=claim('R02',f'On the inspected2022 legacy fold, tightening the fixed diagnostic tolerance from1e-4 to1e-10 changes ridge Brier from{default[0]["brier"]:.9f} to{tight[0]["brier"]:.9f}, and spline from{default[1]["brier"]:.9f} to{tight[1]["brier"]:.9f}. Maximum individual probability changes are{tight[0]["max_prediction_difference_phase2_legacy_rerun"]:.6f} and{tight[1]["max_prediction_difference_phase2_legacy_rerun"]:.6f}. These probes are not new selected candidates.','reproducibility/locked_real_1.json;reproducibility/tight_real_1.json','results ridge and spline',pipeline='code/reproduction.py --tight')
    repaired=claim('R03',f'A genuine invalid-cost boundary defect was fixed: infinite target costs now remain unknown. Across{204469*2:,} source cost cells, there are{infinity} infinite costs, so this repair changes no observed source result.','identity/source_nonfinite_audit.json','all two-basket source costs',pipeline='src/rpi/linkage.py; code/dossier.py')
    human=claim('I01','A private seed20261021 stratified review form contains60 cases:12 each from unchanged matches, changed speed/network, nonmatches, ambiguous keys and potential metadata drift. Prices/automated verdicts are hidden, alternate candidates supplied and stratum key separate. External human adjudications remain0.','identity/review_sample_design.csv;identity/identity_audit.json','all five strata',pipeline='code/measurement.py make_review; code/identity_audit.py')
    lit=claim('L01','Same-source firm/service price analysis is already established in Beck2022 and Borra2026. Matched-item replacement selection is established conceptually by Nakamura and Steinsson. Lim2026 exact-method overlap remains unverified because its lawful full text was not obtained. No claim is SUBSTANTIAL_CONFIRMED.','literature/closest_work_matrix_v3.csv;literature/contribution_classification.csv','beck2022;borra2026;nakamura2012;lim2026',kind='SOURCE_REVIEW_AND_JUDGEMENT',pipeline='code/literature.py')
    md('identity/IDENTITY_VALIDITY.md',f'''# Identity validity: mechanically reproduced, externally unvalidated

{identity}

Core identity: ordered source/destination ISO labels, NFKC/case/space/comma-normalised provider, payment instrument, access point, pickup method/location and basket. Strict requires unchanged speed and receiving-network coverage. It is a restriction of core matching on identical origin records; neither rule is established economic-product ground truth. Canonicalisation is intentionally non-reversible: original strings stay in the private raw/cache, and applying canonicalisation twice is idempotent. Source provider labels reduce713 raw spellings to699 canonical labels; this does not verify common legal entities.

The field audit found no observed pipe separator, so delimiter concatenation in the legacy implementation does not create observed source collisions. The independent implementation uses tuples. Missing pickup-location fields are common and become an explicit empty token, not fabricated known locations. See canonicalisation_audit.csv and label_turnover_by_wave.csv. New or missing labels can reflect sample composition; they are not adjudicated renames or exits.

{human}

There are5,956 unique core links with changed strict attributes, including97 already invalid-cost outcomes; only5,859 previously valid pairs become additionally unknown. This reconciles the apparent difference between changed-link and added-unknown counts. The core-to-strict transition table accounts for every origin. The prior reduced-key sensitivity has563 additional candidate links but5,870 ambiguous origins; uniqueness after metadata collapse is not validation, and no such links were promoted.

Conditional-on-recorded-key E2 bounds account for outcome missingness, not arbitrary false-positive links. If recorded matches may all be wrong with no restriction, true economic-service continuity can range from0 to1. The strict/core scenario envelope is not a validated latent-identity identification set. A human/provider-supported validation of product comparability remains necessary for stronger same-economic-service wording.
''')
    md('identity/MATCH_REVIEW_PROTOCOL.md',f'''# Blinded historical bundle review protocol

{human}

Open the ignored local `research_completion/phase3/private_runtime/BLINDED_IDENTITY_REVIEW.csv`. Keep `IDENTITY_REVIEW_KEY.csv` inaccessible to the reviewer until decisions are sealed. The public PRIVATE_REVIEW_TEMPLATE.csv is header-only by design, not a completed review. Do not upload the private cases.

The sample excludes entirely unresurveyed corridors from adjudicable match strata. Stratum sizes/seed and selection counts are public. Selection is reproducible but deliberately stratified; an unweighted fraction of60 is not a population mislink rate. Candidate alternatives are exact same-provider/corridor/payment candidates with changed remaining metadata, at most three; their inclusion is not endorsement. No fuzzy alias is promoted.

For each case inspect original provider/payment/access/pickup/speed/network fields at both exact calendar quarters; note multiple target candidates and any absent target. Check a historical provider document or official survey definition where lawful evidence exists. Do not use current provider reputation or presence as historical ground truth. Record one of SAME_BUNDLE, DIFFERENT_BUNDLE, UNRESOLVED, NOT_REVIEWABLE, together with evidence URL/page/effective date, reason, reviewer and review date. No outcome-price columns are supplied.

Use a second qualified reviewer or adjudicator where available and document conflicts rather than majority-infer identity. Freeze both decisions and sources before opening the private stratum key or comparing outcome groups. Report nonresponse, unresolved and disagreement counts. Only externally evidenced decisions may be described as identity validation. A reviewer without historical corroboration can provide expert plausibility assessment, not a proven gold standard. Weight only within the actual sampled strata, disclose excluded strata and uncertainty; never infer a universal error rate from convenient cases. No human decisions have yet been supplied.
''')
    md('identity/MEASUREMENT_CLAIM_AUDIT.md',f'''# Measurement claim audit

{conditional}

{corridor}

{e4}

The numerator in E1 excludes unknown successors. E2 retains ambiguous duplicate origin records, so its denominator is recorded offers, not a deduplicated count of latent services. The known-stay lower bound supports a majority of eligible records under either stated rule, but does not establish at least80% continuity for all affordable origins. The conditional estimate is compatible with both all-origin bounds; its actual bias cannot be signed from these data.

SmaRT is a qualifying-service corridor cost indicator including speed/access criteria, not our same-record transition probability ([World Bank Issue54](https://datacatalogfiles.worldbank.org/ddh-published/0037898/DR0095413/RPW_main_report_and_annex_Q325.pdf), pp9-10). Our E3 is an any-cheap-surveyed-quote transition and is also not the official SDG statistic. Do not subtract these rates as if they estimated the same population effect. The new interpretation is a caution about denominator and identity sensitivity, not proof official monitoring is erroneous.
''')
    acq=pd.read_csv(OUT/'timing/source_acquisition.csv')
    inventory=acq.copy();inventory['observation_status']=inventory.get('actual_observations','')
    extra=[]
    for period in ['2025Q4','2026Q1','2026Q2','2026Q3']:
        extra.append(dict(source=period+' row vintage search',url='https://remittanceprices.worldbank.org/resources',status='NO_VERIFIED_RESOURCE_FOUND',observation_status='NOT_AVAILABLE_IN_RETRIEVED_OFFICIAL_INVENTORY',purpose='official catalogue/resources and exact-period search; not proof no unpublished data exist'))
    pd.concat([inventory,pd.DataFrame(extra)],ignore_index=True).to_csv(OUT/'timing/UPDATED_SOURCE_INVENTORY.csv',index=False)
    availability=pd.read_csv(ROOT/'research_completion/validation/feature_asof_registry.csv')
    availability['phase3_available_by']='UNVERIFIED; no recovered historical row-vintage timestamp'
    availability.to_csv(OUT/'timing/FEATURE_AVAILABLE_BY.csv',index=False)
    md('timing/INFORMATION_SET_AUDIT.md',f'''# Information-set audit

{source}

Current catalogue: [official dataset](https://datacatalog.worldbank.org/search/dataset/0037898/remittance-prices-worldwide), public CC BY4.0 classification and temporal coverage2011-2025; source bytes/hash independently rechecked. Download-page text still says2025Q1 while actual verified bytes extend to2025Q3. Catalogue/HTTP modification dates are not new survey observations. Requests and errors are recorded separately from web-reader access. No credentials, login, payment or challenge bypass was used.

The official [resource list](https://remittanceprices.worldbank.org/resources) viewed through the web reader still ends at Issue54/September2025. The ordinary local resource request returned403 and was not retried there. Exact searches for2025Q4/2026Q1/Q2/Q3 yielded no verified official individual-row successor. Unknown unpublished or unindexed material is not ruled out.

The inherited125 successful archived report URLs are an index of report captures, not archived historical quote vintages. A capture proves available BY that capture, not exact first release. The2024Q4 and2025Q3 report public-by captures are later than the respective collection labels; PDF creation, nominal issue month and current Last-Modified disagree for Issue54. We did not redownload125 reports or invent feature dates. FEATURE_AVAILABLE_BY.csv retains every feature as unverified for a prospective clock.

Operational admissibility remains `available_by(feature) <= decision_date < target_collection_start` for every used predictor and vintage. A one-quarter lag to outcome histories does not make current-wave costs/composition public earlier. No full-feature decision time with positive lead time is established. Synthetic boundary guards are tested; no real prospective holdout was evaluated.
''')
    md('timing/HOLDOUT_DECISION.md','''# Holdout decision

NO UNTOUCHED TEST SET. The current official resource is byte-identical to the previously inspected2025Q3 freeze. No new wave was found or evaluated. Do not stitch2025Q1 to2025Q3 across missing2025Q2. The sealed-source amendment rule in PROTOCOL.md remains available if a new source appears.

TrackB operational prediction is NOT_SUPPORTED: both historical public predictor clocks and new outcomes are absent. TrackA finite-panel retrospective measurement does not logically require a new temporal holdout or positive public lead time. Its remaining scientific gates are consequential novelty, economically defensible identity, transparent missingness and limited generalisation. Requiring forecasting clocks as a blanket TrackA gate would be a category error. Later-wave retrospective replication could strengthen external stability but cannot supply missing identity truth or establish first-in-literature status.
''')
    md('inference/UNCERTAINTY_METHODS.md',f'''# Uncertainty targets and assumptions

{paired}

The finite source panel has37 observed waves,36 eligible-origin waves and35 with valid E1 pairs. For that panel, conditional counts and identification bounds are deterministic given identity and valid costs. They do not require an IID binomial sampling interval. RPW is a selected service survey with no row-level selection probabilities/volumes; no design-based global consumer inference is justified.

For hypothetical temporal generalisation, let n_t be a wave numerator, d_t its denominator, theta=sum(n_t)/sum(d_t), and z_t=(n_t-theta*d_t)/mean(d_t). With T eligible-origin waves, the Bartlett HAC sensitivity uses V=(gamma0+2*sum((1-k/(L+1))*gamma_k))/T, gamma_k=sum(z_t*z_(t-k))/T, fixed L in{{0,1,4}}, and t_(T-1) critical values. Source-calendar qidx is retained; no missing wave is compressed into a successor. Eligible-origin waves are consecutive through2025Q1 here; the final missing-target wave contributes to E2 but has zero E1 denominator. Bounds are clipped to[0,1] only for probability displays, not paired effects.

For strict-minus-core width, numerator is additional unknown records and denominator is the identical all-origin count. Entire wave totals absorb arbitrary contemporaneous within-wave provider/corridor dependence; the method still assumes sufficiently regular weak temporal dependence and does not validate that assumption with this small, changing survey panel. Nonstationarity, provider persistence across waves, group imbalance and survey changes limit interpretation. Report all fixed-lag results, not the most favourable interval. No robust95% coverage claim or confirmatory p-value is made.

The secondary model HAC uses13 target waves and the ratio of summed paired loss differences to counts, preserving identical predictions and rows. It does not include model-training/selection uncertainty or validate cross-wave independence. Existing joint bootstrap failures remain part of the evidence. No distribution-free informative confidence interval for arbitrary future dependence is available; absent restrictions, future probabilities and failure-risk ordering remain unidentified.
''')
    md('inference/INFERENCE_ROBUSTNESS.md',f'''# Inference robustness and finite-panel stability

{paired}

{shifts}

{weights}

Deleting the largest origin-count corridor or provider label leaves core conditional continuity close to the pooled estimate; the exact deletion and broad-region/provider-type results are in measurement_sensitivities.csv. No named firm is released. Equal-group summaries differ materially and reveal that record-weighted stability is not universal across provider labels. Small groups are not new independent validation cohorts. Region label `..` is missing classification, not an invented geographic category. Region/provider-type tables are descriptive, not multiplicity-selected discoveries.

{precision}

Selected-policy comparisons against all four raw/calibrated conventional references remain available in the inherited full tables. The new HAC sensitivities may exclude zero under their own assumptions, while the adverse joint interval includes zero. This disagreement is not resolved by choosing HAC. Robust model superiority remains UNRESOLVED. No new bootstrap block/seed search, hyperparameter search or model promotion was performed.
''')
    md('inference/DECISION_VALUE_BOUNDARIES.md',f'''# Decision value boundaries

{capacity}

The original conditional review benchmark ranks a sample defined using future reobservation; it is a retrospective observed-sample diagnostic. The corrected all-origin scenario keeps known failures/stays and unknown reviewed/not-reviewed records separate. Recall bounds allocate unknown failure states adversarially; conditional probabilities do not automatically transport into the unknown subset. Review costs, service availability and consumer transactions are unobserved. Sensitivity costs are scenarios, not money saved.

For a monitoring analyst, the useful result is that an81% matched-record statistic does not establish an80% all-origin guarantee, even when at least one affordable corridor quote often remains surveyed. Rechecking identity/coverage and reporting missing successors is justified as a measurement practice; efficacy of any priority queue is not established. No deployed or operational model is selected.
''')
    envs=[]
    for name in ['locked_real_1','base_real_1','locked_fixture_1','base_fixture_1','tight_real_1']:
        data=json.loads((OUT/f'reproducibility/{name}.json').read_text())
        envs.append(dict(run=name,**{k:data['environment'][k] for k in ['python','platform','numpy','pandas','scipy','sklearn']}))
    md('reproducibility/ENVIRONMENT_MATRIX.md',f'''# Environment matrix

{table(pd.DataFrame(envs))}

The legacy Linux report records Python3.13.16, numpy2.5.4, pandas3.0.6 and sklearn1.9.1. Thus a casual claim that all differences were caused by an sklearn upgrade would be false: the original scientific stack already matches those locked library versions. Windows uses Python3.12.10 and recorded local BLAS DLLs; original Linux transformed rows/probabilities/BLAS fingerprints were not preserved. The base older Windows stack is a controlled alternate, not a reconstruction of original Linux.

All logged fits cap BLAS/OMP/MKL/NumExpr at two threads with PYTHONHASHSEED0. Full threadpool paths/versions and split/transformation/prediction hashes appear in each run JSON. Hashes are fingerprints only; no records or predictions are public. Within-environment repeats are exact, using absolute/relative tolerance zero. The original cross-platform1e-9 comparator is unchanged and still fails. No post hoc substantive tolerance has been introduced. The small cross-dependency synthetic fixture happens to agree exactly; this does not prove real-data identity.

{reproduction}

{numeric}

The older-stack real fold has identical input-row hashes but different transformed-array hashes and tiny Brier/probability differences. Tightening the solver changes individual probabilities substantially more than the original platform differences. This demonstrates preprocessing/termination sensitivity, not an identified causal explanation for the original Linux residual. Larger optimization precision is not uniformly better out of sample in the probe. Frozen scores remain scores of the declared algorithm/tolerance; mathematical optimum and stable individual decisions are not claimed. Reviving a predictive paper would require locked cross-platform row fingerprints and prespecified convergence/refit validation; it is not a reason to repeat the broad model search for TrackA.
''')
    md('reproducibility/FIXES_AND_REGRESSIONS.md',f'''# Repairs and regressions

{repaired}

New primary finite-cost guards affect `primary_outcome_rows` and the observed-failure count in `bounds_table`; regression cases cover NaN, negative and infinite target costs. The independent source parser already used finite validation. Historical source/results/config bytes are preserved; the source implementation change is intentional and listed in the final audit.

The first Phase3 comparison command successfully generated its audit but returned exit0 despite retained DIFFERS statuses. The wrapper now returns the original comparator's failing exit code; the corrected run records exit1 as expected negative evidence. Report-writing success is not strict numeric reproduction success. No tolerance was widened. Every mismatched numeric field is recorded in LEGACY_FIELD_DIFFERENCES.csv; all30 files are partitioned in LEGACY_DIFFERENCE_CAUSES.csv.

The private review aid was repaired to include alternate metadata candidates and a separate blinded stratum key. No identity rule, outcome or external adjudication was changed. Missing-wave mutation detection demonstrates that the adversarial oracle fails under a deliberately wrong bridge. Clock, nonfinite-cost, duplicate, speed-change, weighting and asymmetric-cluster fixtures protect scientific semantics. Successful synthetic tests are not observed human validation.
''')
    md('manuscript/conditional_research_dossier.md',f'''# Affordable surveyed remittance quotes: identity-sensitive continuity and unknown-successor bounds

**Complete conditional research dossier for investigator review. Decision: CONDITIONAL_HOLD. This is not a submission-ready original manuscript.** Created{stamp}. Scientific code/source fingerprints are in the locked manifest. Keywords: remittance prices; longitudinal measurement; record linkage; partial identification; survey attrition.

## Scientific question and strongest supported statement

How persistently do recorded affordable RPW quotes reappear below the same threshold in the exactly next calendar quarter, and how much does inference change with identity and missing successors? The surviving statement is about the recorded source panel under explicit linkage rules. It is not a claim about actual transactions, provider exits or guaranteed access.

{conditional}

{identity}

The practically meaningful distinction is between a conditional statement about matched records and a statement about every initially affordable recorded offer. The evidence does not identify the true missing-outcome persistence or prove the conditional estimate overstates it. Under both rules, the finite-panel lower bound exceeds a majority of eligible records; an80% all-origin claim is not identified. With unrestricted false links, even those latent-economic-service bounds would not follow.

## Position relative to closest work

{lit}

Beck and Martinez Peria's foundational2011 journal article is distinguished from the separately read2009 World Bank working paper. Beck2022's full local PDF includes firm-level models and appendix covariate definitions. Borra2026's full methods already address provider/channel composition and expansion. Bersch2021's recovered annex uses its own operator data and a different pricing endpoint. Nakamura and Steinsson's replacement-bias work supplies the closest conceptual comparison, not a commensurate predictive benchmark. The complete claim-by-claim matrix and access limitations are in literature/closest_work_matrix_v3.csv and fulltext_access_ledger.csv. A generic bibliography, absent search hit or new algorithm cannot establish originality.

## Data, permissions and methods

{source}

Attribution: The World Bank, Remittance Prices Worldwide, available at http://remittanceprices.worldbank.org. Official catalogue classification is public CC BY4.0 with attribution and no endorsement. This package uses public-safe aggregates and reproducible code; raw workbooks, provider/service rows, reading-copy PDFs, identity cases and predictions are excluded.

Eligibility uses nonnegative cost at most3% of the USD200 basket, with a target calendar quarter no later than the final observed wave. Ambiguous origin/target keys, absent services, unresurveyed corridors and invalid target costs remain unknown. Core identity includes direction, provider, payment/access/pickup bundle and basket; strict additionally requires speed/network equality. There is no fuzzy match promotion. USD500 and5% are separate fixed secondary products/thresholds. The independent implementation streams the original workbook and uses tuple dictionaries without importing the primary model/report code.

{flow}

{units}

E1 uses valid matched outcomes. E2 allocates unknown outcomes to fail/stay for lower/upper identification bounds, conditional on recorded identity. E3 describes any cheap surveyed corridor quote, conditional on corridor resurvey. E4 reports reobservation separately. Counts, eligible denominators and state transitions reconcile. Normalisation can underlink label changes or merge economically distinct offerings; deterministic agreement between implementations cannot validate latent identity.

{human}

## Primary measurement results

{table(scenarios.reset_index().loc[lambda d:~d.scenario.str.endswith('_E3'),['scenario','n_eligible','n_valid','n_unknown','conditional','lower','upper']])}

{paired}

{shifts}

{weights}

{corridor}

{e4}

Figures1-5 display the bounds, full wave series, paired width, unknown-state flow and weighting sensitivity. Broad-region/provider-type and fixed pre/post/Russia/deletion analyses are complete in the supplementary CSVs, including adverse results. Neither the strict rule nor equal-group weighting is a validated correction for truth; they test sensitivity of interpretation. The threshold/basket comparisons change eligibility, so cross-scenario differences are not individual treatment effects.

## Statistical precision and secondary modelling

The source-panel counts/bounds are exact descriptive quantities under each rule. Generalisation beyond this selected panel requires assumptions and cannot use raw quote count as the number of independent seasons. The fixed-lag wave-HAC sensitivities include arbitrary contemporaneous dependence through aggregation but assume regular temporal dependence, with limited waves and changing composition. They are not validated robust95% intervals. The full equation and all fixed-lag results are retained in inference/UNCERTAINTY_METHODS.md.

{models}

{precision}

{capacity}

The retrospective model comparison retains Brier/log loss, calibration, AUROC/failure AUPRC, all named conventional references, annual results, historical group transfers and missingness scenarios. No new model family or broad tuning was run. All-origin bounds and MAR/IPW/MNAR assumptions remain separate. Model-selection, release-timing and unknown-successor limitations prevent an operational recommendation.

## Reproducibility and corrections

{reproduction}

{numeric}

{repaired}

Repeated selected-fold determinism is established within Windows, while cross-platform identity remains unresolved. The stricter convergence probe is a diagnostic on inspected data, not a replacement winner. Its probability sensitivity further cautions against individual priority-queue claims. No prior results were silently regenerated with a new tolerance. The Phase3 ledger records expected failures, exact commands, code hashes, CPU limits, time and peak memory.

## Timing, interpretation and limitations

The current official resource has no verified later outcome wave. Archive report captures cannot establish that every current-wave feature was public before target collection. All tested periods were already inspected. This defeats TrackB but is not an automatic barrier to finite-panel TrackA. No forecasting-only gate is imposed on the measurement claim.

Source sampling is not population-representative and quote weights are not transaction volumes. Missingness can reflect survey coverage, metadata or price availability, not actual exit. Identity sensitivities do not identify mislinkage rates. Reweighting changes the target, and temporal stability does not validate product comparability. Negative costs, transparency, date-label anomalies and survey-composition changes have explicit earlier sensitivities; no hidden deletion repairs the source. Uganda's small event count does not support an AI subgroup claim. The all-origin bound width is scientific uncertainty, not uncertainty removed by a better conditional classifier.

## Publication decision and falsification

CONDITIONAL_HOLD for a potential measurement paper; operational predictive paper NOT_SUPPORTED. The large recorded-key contrast is nonvacuous and mechanically reproducible, so immediate whole-project NO_GO is not compelled. Substantial originality and historical economic-product comparability remain unproven. In particular, inaccessible Lim methods could already report the proposed exact endpoint. The new analysis strengthens a careful measurement record but does not clear those external gates.

The next rational action is a bounded human review of the blinded identity cases plus lawful full-text overlap assessment of Lim2026. If those show the exact contribution is already established, or cannot defend comparable services without an arbitrary mislinkage assumption, archive the original-article route. If cleared, author a measurement-focused original manuscript from this dossier with investigator-approved contribution and declarations. Repeating classifiers cannot resolve either gate.

## Declarations requiring investigator confirmation

Author/affiliation/correspondence, individual CRediT contributions, funding, conflicts, institutional determination on secondary public-data research and final licence attribution must be supplied/confirmed by the investigator; no approval, waiver or grant is invented. AI assistance: software execution, source review support, analysis checks and drafting were performed by an AI assistant and require human scientific verification. No submission, preprint posting or author/provider contact occurred. Public software and aggregates are versioned in the repository; private reading copies and provider rows are not redistributed.

## Evidence and references

Every labelled empirical/substantive claim above is linked to a source/table/code path and generation commit in assessment/claim_evidence_ledger.csv. Full bibliography with access depth: literature/references.bib and manuscript/references.bib. Internal dossier paths are relative to phase3; publication-facing citations must be converted to the chosen journal format only after scientific GO.
''')
    md('manuscript/supplementary_methods.md','''# Supplementary replication methods

Clone the repository at the final handoff commit. Use the existing locked Python3.12 analysis environment; the environment lock from Phase2 remains unchanged. Obtain the official workbook lawfully and verify SHA256 before processing. Restore/build Phase2 private features/predictions using the existing frozen protocol only if private caches are absent; do not claim the safe ZIP includes raw inputs. Existing instructions are in research_completion/reproducibility/README.md.

From repository root, serially run `.venv\\Scripts\\python.exe research_completion/phase3/code/run.py independent_measurement .venv\\Scripts\\python.exe research_completion/phase3/code/measurement.py`. This streams the raw workbook once and caches original source fields privately. It enumerates both baskets,3%/5% thresholds and core/strict rules; uses exact calendar adjacency; and computes cohort/region/provider-type/deletion/weighting summaries. E3 is independent of same-service matching. Run identity_audit.py after the private review form is built, inference.py for paired-wave/model-loss sensitivities, and the bounded reproduction.py modes listed in commands.jsonl.

The stricter selected-fold convergence probe is diagnostic, not a new family or policy. Strict legacy comparison expects exit1 while mismatches remain. Counts/repeat tests and CI must pass; that expected audit failure is explicitly separate from software regressions. Newly run commands use the Phase3 runner, never overwrite Phase2 progress. Private identity review CSV and stratum key stay local. Reviewer decisions are not generated by code.

Public-safe outputs are generated from actual aggregates by literature.py, dossier.py and figures.py. Run the independent final audit and full test suite before packaging. A head-only source commit is paired with exact file hashes because the package/its final merge cannot recursively embed its own future commit hash. The final merge/ZIP read-back evidence is recorded outside the immutable ZIP manifest.
''')
    md('manuscript/supplementary_tables.md','# Supplementary numerical tables\n\nAll editable CSVs are under ../tables/ and ../identity/. LINKAGE_SCENARIO_RESULTS.csv contains all eight fixed basket/threshold/identity combinations plus E3 rows. wave_measurement.csv retains every eligible-origin wave. measurement_sensitivities.csv contains every broad stratum and fixed survey/dominance/weighting sensitivity, including adverse differences. paired_wave_identity.csv provides the same-origin paired contrast. Unknown states, canonicalisation and unit-support tables retain denominators. Files prefixed phase2_ are exact safe aggregate copies, not rerun experiments.\n\nModel metrics, calibration, annual comparisons, decision bounds, MAR/IPW, tipping points and all dependence sensitivities remain in the inherited supporting Phase2 dossier. PRIMARY_CLAIM_ESTIMATES.csv and PAIRED_MEASUREMENT_EFFECTS.csv label new HAC sensitivities explicitly. No provider labels, source rows or individual predictions appear in these tables.')
    md('manuscript/JOURNAL_SUITABILITY.md','''# Journal suitability and bounded continuation recommendation

No journal is selected for submission; no cover letter or submission-ready manuscript is supplied. This is an editorial-fit judgement, not a journal acceptance estimate.

The **Statistical Journal of the IAOS** is the most plausible venue category to investigate after validation: the [society's own description](https://iaos-isi.org/statistical-journal/) explicitly covers production and use of official statistics and related public policy. A measured source-panel interpretation/quality note would fit that audience better than an AI-superiority paper. It still needs a consequential original finding, credible identity validation and a clear distinction from the official RPW/SmaRT indicator. Topical fit does not imply editorial suitability or acceptance; current author instructions/charges were not fully verified and no paid action is authorised.

**Economia Politica** links theory, analysis and institutions ([publisher scope](https://link.springer.com/journal/40888/aims-and-scope)). The present descriptive contribution lacks a developed institutional/theoretical inference; it is a weak current fit. **World Development Perspectives** and **Research in International Business and Finance** were considered as topic categories, but their publisher scope pages returned403 in this session; no verified article-format, fee or fit claim is made. No ranking/impact factor is fabricated.

Spend the next effort on one finite external evidence round, not another model. A qualified reviewer can inspect the60 blinded cases and seek historical supporting documents; the full Lim paper/supplements can settle the closest-overlap question. Success is uncertain because neither access nor historical product definitions are controlled by this repository. If that round fails or shows only incremental application of established selection principles, stop the original-research expansion and preserve the reproducibility/measurement note. A bespoke provider-validated panel or prospective snapshot collection would be a new study, not a small remaining software fix.
''')
    md('manuscript/checklist.md','''# Investigator review checklist

- Review the conditional verdict, closest-work access limits and exact surviving recorded-key claim.
- Obtain lawful Lim2026 full text/supplements and document direct endpoint/identity/attrition overlap; no author contact was made.
- Review the private blinded identity form; record evidence-based human decisions before accessing stratum key/outcome summaries.
- Decide whether the application has a substantial domain contribution beyond established matched-panel selection/standard bounds.
- Confirm authors, affiliations, CRediT, funding/conflicts, institutional secondary-data requirements, attribution and AI-assistance disclosure.
- If those scientific gates clear, select an actual journal and convert this dossier into a full manuscript for author review; no current manuscript is labelled ready.
- Preserve all negative model, timing, capacity and reproduction findings. No live deployment or prospective lead-time claim is supported.
- Author approval/submission are separate actions. No journal/preprint submission is authorised or performed.
''')
    (OUT/'manuscript/references.bib').write_bytes((OUT/'literature/references.bib').read_bytes())
    pd.DataFrame(claims).to_csv(OUT/'assessment/claim_evidence_ledger.csv',index=False)
    pd.DataFrame(claims).to_csv(OUT/'manuscript/source_to_claim_audit.csv',index=False)
    gates=[
      ('A','Substantial claim-specific novelty','UNRESOLVED','literature/NOVELTY_DECISION.md','Exact narrow RPW application survives inspected sources; Lim full-text overlap and consequential novelty not cleared.'),
      ('B1','Independent source/count reproduction','PASS','assessment/independent_count_comparison.csv','Twenty independent count comparisons exact.'),
      ('B2','Within-environment numerical repeatability','PASS_SELECTED_FOLDS','reproducibility/RUN_COMPARISONS.csv','Two ridge/spline real2022 repeats and fixtures exact; no universal cross-platform assertion.'),
      ('B3','Strict legacy numeric identity','FAIL_RETAINED','reproducibility/STRICT_LEGACY_COMPARISON.csv','Fourteen differing tables remain, causal platform attribution unresolved.'),
      ('C1','Recorded-key measurement definitions','PASS_CONDITIONAL_ON_RULE','identity/MEASUREMENT_CLAIM_AUDIT.md','E1/E2/E3/E4 separate; finite-cost bug corrected with zero source cells affected.'),
      ('C2','External economic-service identity validation','UNRESOLVED_EXTERNAL','identity/MATCH_REVIEW_PROTOCOL.md','Sixty blinded cases ready; zero human adjudications or validated mislink rates.'),
      ('D1','Historical public information clocks','FAIL_PREDICTIVE_TRACK','timing/INFORMATION_SET_AUDIT.md','No full-feature availability before target; not an automatic TrackA gate.'),
      ('D2','Untouched later outcomes','ABSENT_NOT_AUTOMATIC_TRACK_A_GATE','timing/HOLDOUT_DECISION.md','Current official workbook byte-identical; no new wave evaluated.'),
      ('E1','Finite-panel measurement robustness','PASS_WITH_SCOPE_LIMITS','tables/measurement_sensitivities.csv','Paired identity widening persists; weighting materially changes target.'),
      ('E2','Robust model superiority and operational value','NOT_ESTABLISHED','inference/INFERENCE_ROBUSTNESS.md','Joint interval crosses0, prior stress coverage inadequate, recall bounds overlap.'),
      ('F','Implementation-independent scientific audit','EXECUTED','assessment/SCIENTIFIC_AUDIT.md','Separate parser, adversarial fixtures and claim/file checks; not external peer review.'),
      ('G','Submission-ready original manuscript','NOT_JUSTIFIED','manuscript/conditional_research_dossier.md','Conditional dossier supplied; scientific GO not manufactured.'),
      ('H','Human author/institutional declarations','PENDING_HUMAN','manuscript/checklist.md','Cannot invent declarations or final scientific sign-off.'),
    ]
    pd.DataFrame(gates,columns=['gate','requirement','status','evidence','reason']).to_csv(OUT/'assessment/PUBLICATION_GATE_MATRIX.csv',index=False)
    md('assessment/REMAINING_EXTERNAL_DEPENDENCIES.md','''# Remaining external dependencies and stop rule

1. **Closest-overlap full text:** lawful Lim2026 manuscript/supplements, SSRN6830281. Author catalogue inspected; sole full-work link remains denied. Needed for measurement originality. A human with legitimate access can provide/read the paper; do not infer its contents from the abstract. No author was contacted.
2. **Historical product comparability:** qualified human review with historical documentary evidence of the private60-case form; record unresolved cases, disagreements and exclusions. Needed for economic same-service wording; no universal ground-truth error rate is currently identified. Agent inspection is insufficient.
3. **Independent expert judgement on contribution:** assess whether the measured12.92-point widening and denominator distinction provide consequential original domain insight after those two checks. A positive software audit is not scientific novelty approval.
4. **Author/institutional declarations:** affiliations, contributions, funding/conflicts, appropriate secondary-public-data determination and final attribution/wording. No approval or exemption is assumed.
5. **Only if pursuing TrackB:** authentic historical predictor vintages and positive decision lead time; genuinely new outcomes; independently validated uncertainty and decision value; cross-platform split/transformed-row/prediction fingerprints and convergence precision. These are not automatic barriers to a finite-panel measurement paper and are not resolved by a newer upload date.

Recommendation: do one bounded external overlap/identity round, then decide. Archive the original-article route if exact overlap is found, comparable identities cannot be defended, or only a routine application remains. No further classifier search is recommended. Neither journal acceptance likelihood nor review duration can be inferred from these data.
''')
    verdict=f'''# Final scientific verdict: CONDITIONAL_HOLD

Phase3 decision at{stamp}. Baseline merged main c0ef4fddbef78a47f9f274df78ab68d622da8d8e; generation source commit{sha}, exact run/code hashes in LOCKED_RUN_MANIFEST.json. Publication track: retrospective finite-panel measurement. Operational model selected: NONE. TrackB: NOT_SUPPORTED. This is not peer-reviewed or submission-ready.

{conditional}

{identity}

{corridor}

{reproduction}

What changed: independent eight-scenario raw audit, same-origin paired wave/weighting/dominance/survey-shift estimates, explicit E3/E4 denominator audit, finite target-cost correction, controlled real/fixture repeats and solver probes, recovered IMF2022 and Bersch2021 texts, broader conceptual prior-art assessment, current official-source checksum, blinded60-case review protocol, scoped uncertainty reanalysis and complete conditional dossier/figures/supplements.

The measurement finding is nonvacuous but substantial originality and external historical economic-product identity are not demonstrated. Lim full text remains unavailable. The standard matched-item selection lesson and missing-outcome bounding method are established prior art. These are the scientific reasons for HOLD; absence of real-time clocks/new waves is not used as a blanket measurement-paper rejection.

Preserve the adverse joint-model interval, inadequate simulation coverage, all-origin recall uncertainty, strict legacy mismatch and convergence sensitivity. The narrow supported claim concerns recorded keys under each rule, not true provider survival, consumer savings or a deployable forecast. No new full original manuscript is justified yet. See the conditional_research_dossier.md, source/claim ledger, gate matrix and precise external-dependency list. Next action: one bounded lawful Lim overlap review and evidence-based human identity adjudication, then author decision or archive.
'''
    md('assessment/FINAL_SCIENTIFIC_VERDICT.md',verdict)
    md('PUBLICATION_VERDICT.md',verdict)
    md('START_HERE_PHASE3.md','''# Remittance AI: Phase3 completed conditional dossier

**CONDITIONAL_HOLD. No operational model. No submission-ready original manuscript.** Continue from merged Phase2; no broad model search was repeated.

- [Final scientific verdict](assessment/FINAL_SCIENTIFIC_VERDICT.md)
- [Complete conditional research dossier](manuscript/conditional_research_dossier.md)
- [Novelty decision and precise overlap limits](literature/NOVELTY_DECISION.md)
- [Identity validity and blinded human-review protocol](identity/MATCH_REVIEW_PROTOCOL.md)
- [Actual primary estimates](identity/LINKAGE_SCENARIO_RESULTS.csv) and [paired width inference](inference/PAIRED_MEASUREMENT_EFFECTS.csv)
- [Strict legacy failure and exact within-environment repeats](reproducibility/RUN_COMPARISONS.csv)
- [Scientific audit](assessment/SCIENTIFIC_AUDIT.md), [gate matrix](assessment/PUBLICATION_GATE_MATRIX.csv) and [remaining external dependencies](assessment/REMAINING_EXTERNAL_DEPENDENCIES.md)
- [Execution ledger](EXECUTION_LEDGER.md), [supplementary replication methods](manuscript/supplementary_methods.md), [figure legends](manuscript/figure_legends.md), [claim ledger](assessment/claim_evidence_ledger.csv)
- [Handoff and checksums](deliverables/README.md)

The private60-case identity form is on this Windows computer under ignored phase3/private_runtime/; it is deliberately absent from Git/ZIP. The public review template is schema-only. Raw data, provider rows, predictions, fitted objects and reading-copy PDFs are excluded. Future decision clocks/new temporal holdouts are needed for operational prediction, not automatically for the narrower finite-panel measurement paper. Human source/identity and contribution review remain necessary.
''')
    md('deliverables/README.md','''# Phase3 handoff

The dated REMITTANCE_R01_PHASE3_PUBLICATION_HANDOFF ZIP contains the actual safe repository code, Phase1/2 supporting aggregate evidence and additive Phase3 dossier. START_HERE_PHASE3.md at the archive root opens the new package. Paths inside preserve repository structure, so relative evidence links work. Source workbooks, private reviewer cases, per-service records/predictions, binaries, source PDFs and environment caches are excluded.

SHA256SUMS.txt and file_manifest.csv cover canonical archive bytes (UTF8 text with LF). zip_verification.json outside the archive records actual ZIP hash/member integrity and local Downloads copy read-back; it is excluded from its own payload to prevent self-reference. Final integration is independently verified after build. Preserve the older Phase2 ZIP unchanged.

The scientific outcome is CONDITIONAL_HOLD; the package is a complete conditional dossier, not an accepted/ready manuscript. Replication from raw data requires a lawful separate workbook download and the recorded locked environment. Final ZIP and GitHub paths are recorded in integration.json when actual integration/read-back completes.
''')
    # Runtime summary and immutable source/code fingerprints, including changes outside phase3.
    commands=[json.loads(x) for x in (OUT/'reproducibility/commands.jsonl').read_text().splitlines()]
    code=list((OUT/'code').glob('*.py'))+[ROOT/'src/rpi/linkage.py',ROOT/'configs/experiment.yaml']
    manifests={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in code}
    manifest=dict(generated_utc=stamp,source_commit=sha,baseline_commit='c0ef4fddbef78a47f9f274df78ab68d622da8d8e',source_sha256='f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8',code_hashes=manifests,commands=commands,legacy_strict_status='FAIL_RETAINED_14_DIFFERING_TABLES',within_environment_status='EXACT_SELECTED_2022_FOLDS_AND_FIXTURES',external_peer_review=False)
    (OUT/'reproducibility/LOCKED_RUN_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    ledger=pd.DataFrame([{k:r.get(k) for k in ['stage','exit_code','seconds','peak_rss_mb','start_utc','end_utc','code_changed']} for r in commands])
    md('EXECUTION_LEDGER.md','# Actual Phase3 execution ledger\n\n'+table(ledger)+'\n\nStrict comparator exit1 is preserved expected scientific negative evidence, not a passing legacy reproduction. Source/measurement/model caches were reused only where hashed and specified. One bounded review/aggregate audit overlap is disclosed in AMENDMENTS.md; no heavy model fits overlapped. All scientific runs are local Windows. Further tests/audit/package and Git integration are appended to commands.jsonl and final integration evidence. No author/provider/journal contact or paid usage was performed. Style references were unavailable through the configured writing-style connector; the dossier follows the requested precise scientific English without claiming a retrieved personal style match.')
    print(dict(claims=len(claims),gates=len(gates),verdict='CONDITIONAL_HOLD',infinite_source_cells=infinity))

if __name__=='__main__':main()
