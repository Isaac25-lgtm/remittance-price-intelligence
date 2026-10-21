# REMITTANCE R01 — CODEX SCIENTIFIC PUBLICATION DECISION & COMPLETION HANDOFF

**Version:** 2026-10-21 / phase 3 / execution directive  
**Project:** The persistence of affordable international remittance quotes  
**GitHub:** https://github.com/Isaac25-lgtm/remittance-price-intelligence  
**Local Windows repository:** `F:\MY FILES\DATA SCIENCE\PUBLISHING\Remittance AI`  
**Owner/investigator:** Isaac Omoding  
**Starting evidence:** merged publication-completion PR #3, main integration commit `ae7c977d87c7cf03d54f3e499ba3ef25beffbe5c` (verified 21 Oct 2026).  
**Current scientific verdict:** `CONDITIONAL GO / CONDITIONAL_MORE_EVIDENCE — NOT YET PUBLICATION-READY`.  
**Execution environment:** Codex operating **locally in VS Code/Windows**, with managed memory; **not** Claude Code and **not** Codex Cloud unless the investigator explicitly changes that setting.  
**Objective:** Resolve every *resolvable* remaining scientific and reproducibility problem, then make an evidence-backed choice among (A) a defensible **retrospective measurement paper**, (B) a fully validated predictive paper *only if independently supported*, or (C) a rigorous **NO-GO/STOP**. Finish author-reviewable publication materials if and only if a substantive contribution survives. Preserve the research and publish safe files to GitHub irrespective of the verdict.

> **READ THIS ENTIRE FILE AND THEN EXECUTE.** Do not stop at a plan, a status summary, a README rewrite, or superficial dashboard edits. Do not pretend a blocked evidence gate was completed. The goal is a trustworthy scientific result, not a mandated positive model or a preordained acceptance claim.

---

## 0. Instructions, precedence, autonomy, permissions

1. Operate only in the cloned R01 repository. Confirm `pwd`, `git remote -v`, current branch, `git status`, recent commits, Python versions, available RAM/free disk, and whether user edits are present. **Never overwrite unrelated uncommitted work**; create a new worktree/branch if needed.
2. First read `README.md`, `AGENTS.md`, `CLAUDE.md`, `START_HERE.md`, `configs/experiment.yaml`, `configs/r01_phase2_publication.yaml`, and **all** `research_completion` protocols, status/assessment, reproduction, literature, source and manuscript files listed below. Read existing source/test code before altering it. GitHub main and checked-in artifacts are the source of truth; the handoff ZIP is a snapshot, not a reason to overwrite a newer checkout.
3. Earlier `AGENTS.md` text may say *cloud only*, *stop at 25 minutes*, *leave pull requests unmerged* or reference outdated $64 of Claude credit. Those instructions were for a **superseded 17-Oct Claude session**. The investigator NOW explicitly authorises **local Windows execution and safe, tested pushes/merges to `main`**. This handoff overrides only those older environment/timebox/branch restrictions. It does **not** override scientific protocol freezing, data protection, ethical restrictions, honest reporting or any requirement to avoid paid purchases.
4. Execute scientific work independently, sequentially, and efficiently. Do not ask permission for routine legitimate analysis, documented software fixes, tests, free public-source retrieval, writing safe outputs, or pushing reviewed changes. Ask only when an actual user-only authentication, purchase, licence/ethics agreement, legally restricted data, publication to an external journal/preprint, or serious unresolved destructive action requires a decision.
5. Never purchase credits, enable paid billing, use paywalled bypasses, defeat a 403, secretly use commercial scraping services, or send manuscripts to journals/authors without the investigator's approval. Already available authorised usage may be used, but distinguish local resources from paid cloud services.
6. **No invented results, sources, dates, sample sizes, confidence intervals, external confirmation, performance gains, or publication verdict.** Cite actual computations; maintain negative findings. Do not keep searching dozens of model families merely to engineer a win.
7. If a source cannot be obtained, record the **exact URL, response/error, date, lawful attempts and impact on claims**; progress with feasible independent tasks. Three controlled retries per host maximum for transient errors; do not repeatedly retry authorization-denied responses.
8. Leave **no important finished artifact only in a temporary session**. Commit safe files at meaningful checkpoints and push. Never push private/raw quote rows, firm-level quote histories, model binaries containing sensitive row-level representations, provider-named predictions, credentials or unlicensed paper PDFs.
9. Before finalizing, compare the checkout's current actual scientific state to the baseline recorded below. If later work supersedes any number, do not silently carry the old number forward.

## 1. Verified starting position: what is DONE and must be protected

The previous phase **was a real analysis**. Do not invalidate or erase it merely because its final verdict was conditional:

- Public World Bank *Remittance Prices Worldwide* (RPW) source workbook `rpw_dataset_2011_2025_q3.xlsx`, 50,780,339 bytes, SHA-256 `f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8`, post-2016 sheet. The raw workbook is **not** versioned in Git.
- **204,469** quotes; **368** ordered corridors; **699** normalized provider labels; **37 observed quarters** from 2016Q2–2025Q3 with **2025Q2 absent**. Do not infer data exist for the missing wave.
- **45,343** initially-cheap eligible quote origins; **36,429** uniquely matched next-quarter successors with valid cost; **29,546** stayed at ≤3%; **6,883** observed failures; **8,914** successors unknown.
- Conditional same-core-bundle continuation ≈ **0.811057**. Worst/best possible all-origin bounds ≈ **[0.651611, 0.848201]**. Strict identity changes the conditional point estimate little (≈0.810468) but widens missing-outcome bounds to about **[0.546413, 0.872218]**. These are *measured quote-survey quantities*, not provider exit, consumer availability, transactions or savings.
- Phase-2 retrospective model evaluation **n=19,667** in already inspected target periods. Phase-2 raw random forest Brier **0.128059**, HistGradientBoosting **0.128106**, spline logistic **0.136151**, historical shrunk provider/corridor history **0.138967**, selected chronological research policy **0.130763**. These differ from some phase-1 frozen values; **never mix metrics from different runs/selection rules without explicitly identifying the run**.
- `S_selected` versus spline joint corridor/provider/time sensitivity: point ≈ **−0.005388** Brier; interval **[−0.011730, +0.000457]** includes zero. The stress-test nominal-95%-CI coverage was ≈ **0.86**, not validated 95% coverage. Only **13 distinct target waves** underpin some time-dependent precision estimates.
- **No operational model selected.** The data establish retrospective research associations and hypothetical monitoring scenarios; public availability of full predictor feature sets before the successor survey is unverified.
- The latest research-completion package contained 16 scientific figure designs, detailed audit/result tables, literature matrix (~13 sources), roughly 5,700-word conditional research report, software/integrity tests, and a safe handoff archive. Existing main publication-completion PR #3 was merged as `ae7c977...`. See its handoff report. The previous automated audit checked internal consistency, not external human peer review.
- **Cross-platform strict reproduction is NOT solved**: initial Windows-vs-Linux comparison identified substantive diagnostic/model differences in **14 of 30** legacy tables, though source/cohort/measurement counts reproduce and certain headline tree results agree. A programmatic audit must not mark these as exact strict reproduction.
- A live aggregate-only dashboard exists, https://isaac-remittance-research.streamlit.app/ , but the previous package did **not** independently confirm that the latest scientific changes were redeployed.

### Primary baseline files — inspect, do not overwrite wholesale

`research_completion/assessment/PUBLICATION_VERDICT.md`  
`research_completion/assessment/REMAINING_BLOCKERS.md`  
`research_completion/assessment/reviewer_challenges.md`  
`research_completion/assessment/publication_gates.csv`  
`research_completion/assessment/claim_evidence_ledger.csv`  
`research_completion/manuscript/conditional_research_report.md`  
`research_completion/manuscript/supplementary_material.md`  
`research_completion/manuscript/investigator_signoff_checklist.md`  
`research_completion/literature/closest_work_matrix.md`  
`research_completion/literature/head_to_head_scientific_delta.md`  
`research_completion/literature/search_log.csv`  
`research_completion/data/historical_publication_timing.md`  
`research_completion/data/release_availability_registry.csv`  
`research_completion/data/manual_identity_feasibility.md`  
`research_completion/models/model_comparison.csv`  
`research_completion/models/model_selection.md`  
`research_completion/models/joint_dependence_sensitivity.csv`  
`research_completion/models/all_origin_capacity_bounds.csv`  
`research_completion/reproducibility/local_table_comparison.csv`  
`research_completion/reproducibility/environment_lock.txt`  
`research_completion/validation/split_registry.csv`  
`research_completion/validation/holdout_status.md`  
`research_completion/audits/final_independent_audit.md`  
`research_completion/deliverables/git_and_download_links.md`  

Start with `scripts/completion_fetch.py`, `completion_data.py`, `completion_pipeline.py`, `completion_report.py`, `final_scientific_audit.py`, `build_publication_handoff.py`, and `evaluate_future_wave.py`. Do not replace existing experimental structures without documenting a scientifically defensible amendment and run comparison.

---

## 2. What constitutes success? Choose a *defensible manuscript*, not an ML trophy

There are THREE distinct endpoints for this assignment:

**Track A — retrospective measurement paper (preferred if defensible):** Quantify persistence of **surveyed** ≤3%-cost remittance offers when exact service bundles reappear, and how service identity definitions, selective non-reobservation, survey changes and missing-outcome scenarios alter what can be inferred about affordability persistence. Include calibrated historical/predictive modelling as *secondary comparative evidence* only; no forward lead-time claims. **A real-time timestamped prediction system and a new untouched future wave are not automatically prerequisites for this narrower paper**. Instead, prove novelty, measurement validity, robustness and consequential insight on the actual observational target.

**Track B — operational predictive paper:** Only if authentic contemporaneous quote snapshots and documented `available_by` dates establish that every predictor could be known by a **real decision date strictly before target collection**, and genuinely uninspected future waves exist. Prove strong base-model comparison, calibration, clustered uncertainty and useful decision value. If unavailable, this branch must finish as *NOT SUPPORTED* without compromising Track A.

**Track C — NO-GO / preservation:** If the closest work already establishes the exact measurement contribution, valid linkage cannot be defended, or missingness makes all substantive claims vacuous, stop expansion. Produce a complete transparent negative/reproducibility record rather than an artificially publishable article.

**STOP RULE:** Not enough evidence for Track B does **not** automatically invalidate Track A. Conversely, a beautiful descriptive dashboard or a small retrospective model gain does not establish Track A originality. Explicitly decide which scientific claim is actually supportable.

---

## 3. Gate A — closest-prior-work / NOVELTY: highest priority

### A1. Extend the head-to-head literature assessment, using lawful sources

Start with the sources already registered in `closest_work_matrix.csv`, especially:

1. **Beck, Janfils & Kpodar (2022), *What Explains Remittance Fees? Panel Evidence* (IMF Working Paper 2022/063)** — prior R01 narrative incorrectly implied this was corridor-only; it includes firm-level analysis. Read its full sections, tables, appendices and dataset/identifier definitions, not only abstracts.
2. **Borra & Saritha (2026)**, already reviewed in the previous phase — service-level prices, fixed effects, fee/foreign-exchange decomposition and survey-expansion sensitivities; do not claim those features are new.
3. **Boon Chuan Lim (2026)** provider/corridor/quarter digital-channel pricing study, reported as a same-source competitor with ~188,700 observations — previously blocked full text. Search lawful author/institution repositories, working-paper series, SSRN/RePEc/eprint and supplementary files using precise titles/identifiers; do not bypass access controls. If full text remains unavailable, label findings `ABSTRACT-ONLY/UNVERIFIED OVERLAP`, with publication implication.
4. **Beck & Martínez Pería (2011)** foundational World Bank RPW pricing paper; the **official World Bank RPW SmaRT** metric and issue reports; **PlainRemit**; **Remit-Scout** or related real-world price-stability tools. Verify exactly what they measure, who compiled them, and whether their stability claims have auditable methods. Official monitoring can constitute prior art even when not peer reviewed.
5. Search both **exact dataset** studies and **different dataset but same estimand** research: offer/quote persistence, provider switching, attrition of sampled listings, price threshold transition probabilities, incomplete follow-up in market price panels, information sets and decision-theoretic recheck allocation. Include published research, preprints, theses, conference papers, technical reports, GitHub code and institutional working papers.

Do not assume any citation is real merely because the old matrix includes it. Verify authors, title, date, DOI/URL, published/preprint status, data period/unit, actual question and findings. Read full papers wherever possible; document when only abstracts are available. Distinguish **author-stated limitations** from your own critique. Preserve a reproducible dated search log (queries, portals, URLs, full-text availability and depth).

### A2. Produce an actual novelty verdict

Construct a **head-to-head, claim-by-claim overlap matrix** with columns: exact source/dataset, period, quote/service identity, transition outcome, denominators, attrition handling, missingness identification, temporal/publication clock, validation design, baseline models, uncertainty, actionability and substantive result. Quote only short necessary excerpts within copyright limits and cite source/page where available. Include direct evidence where the competing result occupies the proposed claim.

Classify each candidate contribution: `ALREADY_ESTABLISHED`, `NEW_BUT_INCREMENTAL`, `POTENTIALLY_SUBSTANTIAL`, `SUBSTANTIAL_CONFIRMED`, or `UNRESOLVED`, with a falsifiable explanation.

Prepare `research_completion/phase3/literature/NOVELTY_DECISION.md` and updated bibliographic matrix. If the best surviving original claim is narrow, **adjust the proposed title/aims** before adding analysis. If the contribution is not substantial, return NO-GO; don't say “first use of ML” or “first African application.”

### A3. Concrete novelty question that MUST be answered

> Do the *same provider-service quote bundles* in RPW show important ≤3% threshold persistence, and does their **conditional 81.1% persistence** fail to represent all initially-affordable observed offers because of identity ambiguities and unknown successors? Are the changes between core and strict bounds **not previously quantified** and practically meaningful beyond ordinary published corridor-level cost monitoring?

No author should have to infer the paper's significant contribution from a model scoreboard. Quantify the substantive implication with uncertainty, compare it to what official RPW corridor statistics would tell a decision maker, and test whether the result persists across periods/regions/thresholds without selecting only favourable subgroups.

---

## 4. Gate B — reproduce, trace and repair the Windows/Linux numerical discrepancies

This is a **quality-control requirement**, not a request to make all models agree by rounding.

1. Run `python --version`, record OS/CPU/thread settings, Python/scikit-learn/pandas/numpy/scipy versions and relevant BLAS info. Compare environment lock files with the original Linux runs and test Python 3.11/3.12-compatible controlled environments if feasible on the machine without damaging other installations.
2. Verify the **raw workbook hash and exactly reconstructed row/identity/outcome counts** against frozen manifests before any model refit. Preserve copies of original legacy result tables under immutable comparison paths.
3. Execute the built-in strict comparator and capture all file-level/field-level differences, including the 14/30 legacy-table mismatch finding. Partition differences into (a) source/cohort or linkage, (b) feature values/leakage, (c) fold or training-order changes, (d) stochastic seeds/threading, (e) dependency/solver/dtype changes, (f) calibration and time-selection changes, (g) formatting and intentionally variable run-time fields.
4. Trace differences using controlled small deterministic fixtures and selected real-data row **fingerprints**, feature and split hashes; keep raw row outputs/private identifiers out of Git. Check as-of transition boundaries, stable group sorting, scikit-learn estimators' solver/preprocessing versions, missing/nullable dtypes, one-hot category ordering, probabilities, clipping, ties in top-capacity ranking and bootstrap seed/RNG choices.
5. Add regression tests specifically reproducing each genuine defect discovered. Repair code only when the science warrants it; write a changelog linking old/new results. **Never widen an arbitrary numerical tolerance to disguise a scientifically consequential difference**. Some numerical disagreement may remain legitimate and must be stated with separate environment-dependent results.
6. Run a stable environment twice in succession; compare deterministic outputs using a declared substantive tolerance justified by model semantics, plus exact table/schema count checks. Distinguish *within-environment reproducibility* from *cross-platform numeric identity*. If substantive results change, regenerate all affected tables, text, figures and dashboard notices from the same locked run.

Artifacts: `phase3/reproducibility/ENVIRONMENT_MATRIX.md`, `LEGACY_DIFFERENCE_CAUSES.csv`, `FIXES_AND_REGRESSIONS.md`, `LOCKED_RUN_MANIFEST.json`, `RUN_COMPARISONS.csv`. Do not mark the strict legacy check PASS if it still fails.

---

## 5. Gate C — service identity, coverage and selection validity

1. Audit exactly how core bundle identity is constructed (corridor, normalised provider, payment instrument, access point, pickup method, pickup location, basket) and how strict identity adds speed and receiving-network coverage. Confirm variable units and survey-collection periods. Preserve original/source values and round-trip canonicalisation tests.
2. Examine potential **false links, under-links after renaming, collisions, duplicated offerings, relabelled payment instruments, changing network coverage, abrupt 2021/2022 composition changes and 2025 missing wave**. Stratify by origin quarter, region, provider type, speed-change indicators and survey expansion. Do not treat unknown services as confirmed provider exits.
3. Implement **a reproducible private manual review protocol** for a seeded, pre-specified stratified sample (match vs non-match, ambiguous keys, label drift). Show the user what source fields and cases need human judgement and create a blinded review form/decision guide. The investigator's or another qualified human's adjudications must be recorded **before** calling false-link/true-link rates externally validated. Agent-only inspection is *not* external identity ground truth.
4. If no external truth source or human adjudication exists, use explicit rule-based **identification intervals** and plausible-linkage scenarios. Report sensitivity of the primary claims without implying a statistically identified mislinkage rate. Do not use provider reputation or commercial availability as ground truth.
5. Confirm that every numerator/denominator aligns to its estimand. Recompute E1 conditional observed continuity, E2 all-origin bounds, E3 corridor-level survey monitoring, and any E4 variant. Check the 3% and 5% thresholds and USD200/USD500 basket distinctions. Run 2022-era schema/subpopulation shift sensitivities.
6. Review the 8,914 unknown successors, their subtypes and plausible missingness mechanisms. Show primary nonparametric worst/best bounds first; then separately explain any MAR/IPW assumptions, pattern-mixture/MNAR scenarios and tipping points. IPW and MNAR sensitivity analyses **do not identify truth** without assumptions.
7. Connect the measurement finding to a real substantive policy question: **what would a World Bank/SDG monitoring analyst conclude under conditional matched-service continuity versus source-population bounds?** Quantify difference clearly; avoid consumer savings, causal benefit or observed provider exit.

Artifacts: `phase3/identity/IDENTITY_VALIDITY.md`, `MATCH_REVIEW_PROTOCOL.md`, `PRIVATE_REVIEW_TEMPLATE.csv` (empty schema or synthetic example only), `LINKAGE_SCENARIO_RESULTS.csv`, `MEASUREMENT_CLAIM_AUDIT.md`, `phase3/figures/` with newly justified plots.

---

## 6. Gate D — historical availability, timing and genuinely new data

1. Audit current official RPW dataset catalog and resource list, legal reuse terms and observed collection dates; compare source bytes/hash against 2025Q3 freeze. Search for **genuinely new** 2025Q4, 2026Q1/Q2/Q3 or later official individual-row survey vintages, without assuming they exist. Verify each resource's true observation period, survey fields and official provenance. The previous phase reported that an “updated” web page still yielded the **identical 2025Q3 workbook**.
2. Revisit archived official report links / Wayback captures only for **evidence the archive actually proves**. The previous effort indexed 125 archived report URLs, but reports/capture timestamps did not identify when every predictor quote became public. Treat archive capture as an *upper bound on first available by*, not precise publication date; distinguish survey collection, report issue label, publication announcement, PDF creation, online capture and file modification.
3. Assemble an `available_by` registry at **feature/vintage** level. An operational test must satisfy `available_by(feature) <= decision_date < target_collection_start`, for all predictor values used. Never treat an inferred one-quarter history lag as enough if the current-wave quote features themselves had not yet been published.
4. If a legitimately untouched future wave is found, freeze the existing candidate family and measurement/linkage rules **before reading its outcome**. Seal dataset identity/hashes/timing protocol and only then compute outcomes. Do not retune on the new holdout. Predefine Brier, calibration, baseline comparisons, capacity and group dependence. If the future-wave time information is not provable, call the run **later-period retrospective confirmation** rather than prospective early-warning validation.
5. If no genuinely new outcome wave is available, retain `NO UNTOUCHED TEST SET`. For a retrospective **measurement-first** paper, determine explicitly whether independent later-wave validation is scientifically essential to the *measurement claim*, rather than inserting a forecasting-only gate that makes any manuscript impossible.
6. Do not manufacture missing 2025Q2, stitch a 2025Q1→2025Q3 “next quarter” transition, use a new upload date as a new observation or inflate effective sample size by treating correlated quotes as independent seasons.

Artifacts: `phase3/timing/UPDATED_SOURCE_INVENTORY.csv`, `INFORMATION_SET_AUDIT.md`, `HOLDOUT_DECISION.md`, and reproducible feature-date verification tests.

---

## 7. Gate E — valid inference, modelling and practical significance

**The question is NOT “can another exotic classifier lower Brier by another decimal?”** Use established Phase-2 models unless a concrete defect demands refitting.

1. Evaluate **the one inferential claim that matters** for the selected paper. For Track A, quantify stability of conditional continuity and widening of observed-population bounds under plausible identity and missingness definitions. Use appropriate clustering/dependence; report wave-level summaries and show that results aren't driven by a few very large providers or highly correlated corridors.
2. Re-evaluate the joint corridor/provider/quarter dependence sensitivity for the *existing* calibrated/model-policy comparisons. Use analytically defensible conservative approaches and sensitivity designs; report the observed small number of independent time waves. The previous attempt's nominal-95% procedure showed **0.86 simulation coverage**. Do not label unvalidated intervals “95% robust” without a verified design/coverage argument.
3. Keep both **probability quality** and **decision value**: Brier/log loss/calibration, AUROC and failure AUPRC, cost/history/ridge/spline/GBM/RF references, per-year estimates, reliable support counts and both fixed-per-quarter vs pooled monitoring capacity. Pooled rankings that rely on future reobserved membership cannot be portrayed as deployable real-world triage.
4. At the all-origin level, treat unknown outcomes as unknown. Report identified recall bounds and plausible assumption scenarios; never convert those into observed savings, verified avoided harm or true capacity effectiveness. The earlier 20%-capacity selected-policy all-origin recall bounds were roughly **0.2167–0.5726** and did not identify a unique deployment policy.
5. If a genuine time-held-out wave exists, perform exactly one sealed confirmation under the predeclared candidate, baseline and comparisons. No reuse of it for tuning/novelty-driven model search.
6. Explicitly separate `MODEL COMPARISON RETROSPECTIVE`, `MEASUREMENT CLAIM`, `SOURCE/TRUTH VALIDITY`, and `OPERATIONAL PREDICTION`. If a simple rule is more reliable under fair robust testing, state it prominently; never retain ML as the flagship merely because the project is branded “AI.”
7. Clarify materially whether the measurement difference offers **new actionable interpretation** that prior corridor-level costs obscure. If it does not, say so. A significant Brier improvement cannot rescue a scientifically trivial estimand.

Artifacts: `phase3/inference/PRIMARY_CLAIM_ESTIMATES.csv`, `UNCERTAINTY_METHODS.md`, `DEFINITIVE_MODEL_COMPARISONS.csv`, `INFERENCE_ROBUSTNESS.md`, `DECISION_VALUE_BOUNDARIES.md`.

---

## 8. Gate F — independently audit the actual code, results and sources

Run a separate audit path that computes source counts and headline estimates **without importing the primary model evaluation/report-writing implementation** (independent source parser or restricted streaming audit where feasible). Test adversarial source fixtures: missing wave, identity change, duplicate key, invalid cost, non-reobserved corridor, changed speed, target-date boundary, unobserved outcome, wrong direction of Brier and asymmetric provider/corridor clustering. Ensure the scientific tests would actually fail if one known defect were reintroduced.

Produce a claim-level evidence registry with each manuscript's numeric and substantive sentence tied to exact source and table/figure/pipeline/commit. Citation verification must go beyond valid DOI metadata: inspect the cited text or acknowledge the lack of access. Separate external scientific fact from algorithm output and from interpretation.

When needed, run only bounded extra computations to resolve named audit defects; do not run unrestricted hyperparameter searches, redesign the endpoint after seeing holdout results, or quietly change previously frozen choices. Every material change must be dated, justified, testable and shown alongside its predecessor.

---

## 9. Gate G — write the actual paper if science supports it

### G1. Required paper choice and structure

After Gates A–F, publish an internal decision dated by actual execution time:

- `MEASUREMENT_PAPER_GO_FOR_AUTHOR_REVIEW` — novel, valid, consequential measurement finding survives; operational early warning unclaimed.
- `PREDICTIVE_PAPER_GO_FOR_AUTHOR_REVIEW` — genuine prediction information timing, independent validation and material improvement all documented.
- `CONDITIONAL_HOLD` — the study may become publishable, but necessary evidence is unavailable/awaits outside action.
- `NO_GO` — substantive overlap, fatal linkage/identification flaw or lack of meaningful incremental knowledge makes the paper not worth pursuing.

**Never label an AI-written document as peer-reviewed or journal-accepted.** “GO for author review” is not permission to submit.

### G2. If and only if scientific GO survives

Produce a professional full original manuscript in **English** with human-readable scientific prose and real verified citations:

- Research title and 4–6 keywords; structured abstract (study purpose, dataset, time frame, estimand, approach, key numerical findings, honest significance, implications).
- Introduction: practical remittance affordability problem; sharp positioning against closest exact-data and comparable-question work; stated materially new contribution.
- Methods: data origin/licence; true dates; source-vintage limitations; unit/identity/eligibility; transition/attrition; registered estimands; statistical models; timing split; missingness assumptions; clustering/inference; controls against leakage; ethical/data use; sensitivity scope.
- Results: complete record flow; quote-continuity primary estimate and bounds; time/subgroup heterogeneity where credible; strict/core link difference; main statistical uncertainty; carefully interpreted comparative predictive evidence, if justified; figures/tables with accurate denominators.
- Discussion: novel scientific lesson, practical interpretation, comparison with closest prior papers, specific limitations (timing, nonreobservation, identity and selection), honest generalizability, future research.
- Declarations: **explicit placeholders requiring investigator confirmation** for affiliations, author contributions, funding, conflicts and institutional requirements. Do not invent approvals.
- Accurate bibliography with DOI/URL/publisher, access depth and in-text correspondence. No invented references, unsourced sentences or false exclusion/first claims.
- **Supplementary methods** sufficient for replication from lawfully obtained raw data; full sensitivity/robustness tables and figures; transparent research software/data availability statement and AI-assistance disclosure.

Create:

`research_completion/phase3/manuscript/manuscript_for_author_review.md` (canonical),  
`abstract.md`, `supplementary_methods.md`, `supplementary_tables.md`, `figure_legends.md`, `references.bib`, `cover_letter_draft.md` (only after a realistic journal is selected), `checklist.md`, `source_to_claim_audit.csv`.

If format conversion is available **without new paid dependencies**, also produce editable DOCX and a visual-review PDF; conversion is secondary to scientific validity. Do not insert hidden citation placeholders or claim a PDF was rendered if it was not. Inspect figures for legibility; supply 300-dpi or vector figures and actual editable numerical table sources.

### G3. If conditional hold or NO-GO

Produce the full **scientific negative/conditional research dossier**, including the best supported narrow statement, honest table/figure package, journal-suitability assessment, exact blocker, falsification evidence, what human/official data would unlock it, effort-versus-likelihood and a reasoned stop/continue recommendation. No fake “submission-ready manuscript.”

---

## 10. Required final repository structure and handoff deliverables

Make an additive phase-3 directory; avoid scattering or overwriting unrelated Phase-1/2 results:

```text
research_completion/
  phase3/
    START_HERE_PHASE3.md
    EXECUTION_LEDGER.md
    literature/
      NOVELTY_DECISION.md
      closest_work_matrix_v3.csv
      fulltext_access_ledger.csv
      references.bib
    reproducibility/
      ENVIRONMENT_MATRIX.md
      LEGACY_DIFFERENCE_CAUSES.csv
      FIXES_AND_REGRESSIONS.md
      LOCKED_RUN_MANIFEST.json
      RUN_COMPARISONS.csv
    identity/
      IDENTITY_VALIDITY.md
      MATCH_REVIEW_PROTOCOL.md
      PRIVATE_REVIEW_TEMPLATE.csv
      LINKAGE_SCENARIO_RESULTS.csv
      MEASUREMENT_CLAIM_AUDIT.md
    timing/
      UPDATED_SOURCE_INVENTORY.csv
      INFORMATION_SET_AUDIT.md
      HOLDOUT_DECISION.md
    inference/
      PRIMARY_CLAIM_ESTIMATES.csv
      UNCERTAINTY_METHODS.md
      DEFINITIVE_MODEL_COMPARISONS.csv
      INFERENCE_ROBUSTNESS.md
      DECISION_VALUE_BOUNDARIES.md
    figures/
      [only real publication-quality figures; vector + high-resolution image when warranted]
    tables/
      [versioned final analysis tables, no row-level or firm-identified data]
    manuscript/
      [scientifically warranted author-review manuscript OR conditional/no-go dossier]
    assessment/
      FINAL_SCIENTIFIC_VERDICT.md
      PUBLICATION_GATE_MATRIX.csv
      SCIENTIFIC_AUDIT.md
      claim_evidence_ledger.csv
      REMAINING_EXTERNAL_DEPENDENCIES.md
    deliverables/
      README.md
      SHA256SUMS.txt
      REMITTANCE_R01_PHASE3_PUBLICATION_HANDOFF_<date>_<sha>.zip
```

You may modify names where consistent with existing code, but include a complete index and working relative hyperlinks. Do not generate empty placeholders disguised as completed deliverables. For inapplicable branches, write a truthful `NOT_APPLICABLE` note in the index rather than fabricating tables.

**The ZIP must be generated using the actual repo outputs**, not constructed from invented files, contain a manifest of included files/hashes, and pass integrity checks. Keep the safe ZIP in the repo only if it meets size/licence/security constraints and can be pulled from GitHub. If too large, produce a safe split package or versioned release **without fabricating a URL**. Large private raw inputs never go into it. Verify download/read-back and hashes.

### Git discipline

- Choose a named branch `research/r01-phase3-publication-validation` for work if substantial changes; commit checkpointed phases. The investigator has authorised safe **merging/pushing to `main`** when tests and data-safety checks pass. Prefer PR review workflow when practical, but do not leave all results marooned on an unmerged branch. **Never force-push, alter tags or wipe existing history**.
- Perform `git fetch`, check divergence and rebase/merge prudently without dropping uncommitted user work. If branch protection requires user approval, push a PR and document the exact action needed.
- Prevent committing `data/raw`, `data/processed`, private identity samples, participant/provider-level rows, private PDFs, raw model predictions, serialized models with sensitive memorization risk, API secrets, `.env`, `.venv`, or giant caches. Check `.gitignore`, `git diff --cached --name-only`, file types and safe allowlist before pushing.
- Update `README.md`, `docs/STATUS.md`, manuscript/evidence pointers, and `research_completion/README.md` to reflect the actual new decision; keep older records dated rather than rewriting previous results to look as if the new evidence always existed.
- Run automated tests and data-safety checks before every final integration; record the test count and environment, then verify remote main's commit SHA and success of GitHub Actions where available. Only claim live Streamlit deployment after actually opening the updated deployed app. Keep dashboard as aggregate-only research material; presentation polish has low priority.

### Mandatory final Codex response

Return the following in a compact **completion report**:

1. **Final scientific decision:** one of `MEASUREMENT_PAPER_GO_FOR_AUTHOR_REVIEW`, `PREDICTIVE_PAPER_GO_FOR_AUTHOR_REVIEW`, `CONDITIONAL_HOLD`, `NO_GO`. Give exactly why and what claim survives.
2. **What actually changed:** source/literature/identity/timing/numeric reproduction/inference/validation work; separate tested from untested claims.
3. **Key quantitative findings** tied to versioned tables; identify any revisions to previously reported findings.
4. **Blocking conditions** remaining, and which need investigator intervention; no vague “more research needed.”
5. **Tests and reproduction:** commands, exit codes, input source SHA256, OS/Python/locked libs, CI outcome, disagreements unresolved.
6. **Files:** precise local directory, final ZIP path, safe GitHub links and integrated main SHA (or exact reason integration was not possible).
7. **Publication package:** manuscript filename/status, figures, supplementary material, verified citation registry and sign-off checklist.
8. **The next rational action:** submit for the investigator's author review, obtain one specific external evidence item, or archive the study. No promise that a journal will accept it.

---

## 11. Execution order, gates and non-stall rules

**Phase 0: Inventory + preservation.** Read full prior dossier; check actual checkout and local environment; baseline immutable hashes; set up phase-3 status/progress log. **Do not claim new results yet.**

**Phase 1: Literature/novelty and actual source inventory in parallel where safe.** Verify precise closest work and release/data catalog with bounded lawful requests. If novelty clearly fails, immediately switch to formal NO-GO/negative dossier; do not invest in extensive further tuning.

**Phase 2: Numerical reproduction and identity audit.** Resolve the real discrepancies; independently compute and validate important measurement counts and denominators. Implement human-adjudication protocol without inventing adjudications.

**Phase 3: Inference/source timing and justifiable final analyses.** Focus experiments on decisions that distinguish publication-quality science from inconclusive exploration. If no new wave, explicitly mark it absent and proceed with measurement-track assessment. Preserve weak/negative findings.

**Phase 4: Publication decision and actual files.** Construct the paper only if supported; otherwise create an equally complete conditional/NO-GO dossier. Generate all safe figures and supplementary tables, scientific audit, ZIP, updated README and GitHub integration.

**Phase 5: Independent verification and finish.** Re-read as a hostile journal reviewer. Identify at least ten realistic rejection grounds and confirm whether the evidence actually resolves them. Check every number against source tables, and every reference against legitimate source evidence. Record final verdict and blockages. Give the investigator a single `START_HERE_PHASE3.md` and the final ZIP.

Do not halt after “I will now run analysis.” Do not waste time regenerating existing charts, repeating completed no-change model searches, waiting indefinitely for 403 sources, or asking the user to reauthorise actions already authorised. If a task is impossible, document exactly why, choose the correct narrower scientific scope and continue the other phases. **Do not treat scientific honesty as a license to leave the project unfinished.**

### Local Windows resource controls

- Run one heavy Python job at a time; normally cap `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_NUM_THREADS` at **2**; cap tree model parallelism accordingly. Do not spawn repeated workers or fill the drive with duplicate caches.
- Observe available RAM/disk and actual job peak memory. Use chunked/dtype-aware data processing, Parquet caching, restarts and checkpoints where supported. Stop/repair operations causing destructive memory pressure; avoid OS freezes. Keep the laptop awake during long Codex/local execution; a closed/sleeping laptop cannot keep training.
- Prefer the existing Python 3.12 locked analysis environment and do not unpin/change it casually just to make tests pass; CI currently uses Python 3.11 for dashboard/runtime, which is a different purpose.
- Use portable Windows paths and explicit quoting of the space-containing local path; never assume `F:` is mounted in a remote runner.
- Report actual elapsed time and peak RSS if measurable; do not invent resource metrics. No tight arbitrary timebox overrides scientific validity, but checkpoint often enough to survive session interruptions.

---

## 12. Initial Codex command

When this file is placed in `F:\MY FILES\DATA SCIENCE\PUBLISHING\Remittance AI`, the investigator will send:

> **Read `REMITTANCE_R01_CODEX_PHASE3_SCIENTIFIC_PUBLICATION_HANDOFF_2026-10-21.md` completely. Execute its staged scientific completion assignment in this local Windows repository. Start with the actual existing `research_completion` dossier and merged GitHub main; do not restart from scratch. Resolve novelty, numerical reproducibility, identity/selection validity and inference where genuinely resolvable, select measurement-versus-prediction versus NO-GO honestly, deliver the manuscript or conditional dossier, package safe downloadable outputs, and push/merge tested work to GitHub main. Continue through execution and documented blockers. Provide the exact final scientific verdict and verified file paths/commit hashes.**

**END OF HANDOFF.**
