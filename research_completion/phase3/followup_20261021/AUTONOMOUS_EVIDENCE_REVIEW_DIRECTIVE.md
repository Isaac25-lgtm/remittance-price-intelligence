# R01 — Autonomous evidence review and final publication decision

**Updated investigator instruction: 21 October 2026.** The investigator cannot personally adjudicate the 60 blinded cases or recruit a reviewer for this phase. **Proceed autonomously through every scientifically feasible research step. Do not pause to request a human review.** No AI assessment may be represented as human, independent expert, or externally validated ground truth.

Repository: https://github.com/Isaac25-lgtm/remittance-price-intelligence  
Local Windows repo: \`F:\MY FILES\DATA SCIENCE\PUBLISHING\Remittance AI\remittance-price-intelligence\`  
Starting point: committed Phase 3 and subsequent \`followup_20261021/\` files, not a new project.  
Existing scientific decision: \`CONDITIONAL_HOLD\`; no operational remittance prediction service is validated.

## 0. Non-negotiable outcomes

1. **Run, do not merely propose, a privacy-preserving automated evidence investigation** for all 60 blinded historical identity cases, obtaining legal, dated, specific historical documents wherever feasible.
2. Freeze a machine-only review ledger with granular citations, source temporal scope, uncertainty and failures. **Do not write anything into fields named \`human_identity_decision\` or \`reviewer\` that would falsely indicate a person reviewed the cases.**
3. Execute sensitivity analyses that use the evidentiary grades and cannot confuse an AI-proposed bundle match with a verified real-world product match.
4. Make a bounded, documented originality/publication decision. Write a complete, carefully delimited manuscript **only if the evidence really supports one**, otherwise issue an explicit \`NO_GO_ORIGINAL_ARTICLE\` or \`CONDITIONAL_HOLD_EXTERNAL_VALIDATION\`, explain the limitation, and preserve the research as a quality GitHub project.
5. Update the aesthetically improved public README and dashboard **only where necessary to reflect verified new scientific findings or the final verdict**; do not redesign them again or turn a speculative study into a sales demo.
6. Produce a clean, tested public aggregate handoff and a **separate private local-only package** with all case-by-case data. Preserve every prior completed research phase and its immutable handoff. Push safe verified materials to \`main\` using conflict-aware, test-verified Git operations.
7. Give the investigator an end-state report with exact status, Git SHA, test/CI result, local handoff paths, public links, unresolved items, and the candid publication verdict. The investigator must not be asked to classify 60 rows.

## 1. Repository and permission preflight

- Determine \`git status\`, \`git remote -v\`, recent commits, default branch and read \`AGENTS.md\`, \`CLAUDE.md\`, \`README.md\`, \`research_completion/phase3/START_HERE_PHASE3.md\`, \`research_completion/phase3/assessment/FINAL_SCIENTIFIC_VERDICT.md\`, and current \`followup_20261021/PUBLICATION_VERDICT.md\`.
- Consult \`followup_20261021/LIM_OVERLAP_REVIEW.md\`, \`SURVEY_CHANGE_REVIEW.md\`, \`CRITIQUE_RECONCILIATION.md\`, \`REVIEWER_INSTRUCTIONS.md\`, and the source acquisition ledger. Lim author v1.1 has **already been read**. Historical methodology changes are **already documented**. Do not redo this work without a specific scientific reason.
- Keep \`OMP_NUM_THREADS=2\`, \`OPENBLAS_NUM_THREADS=2\`, \`MKL_NUM_THREADS=2\`, \`NUMEXPR_NUM_THREADS=2\`; avoid competing high-memory processes. Reuse caches and frozen results. Do not run new classifier searches.
- Find the **existing ignored private** case file in \`research_completion/phase3/private_runtime/\`. First look for \`BLINDED_IDENTITY_REVIEW.csv\` or \`followup_20261021\`. If absent, look in the investigator's local Downloads for \`REMITTANCE_R01_IDENTITY_REVIEW_LOCAL_ONLY_20261021.zip\`, validate the source, and extract privately. NEVER commit original case records, reviewer HTML, price/outcome columns, alternative candidate lists or the stratum key.
- Verify that the casebook contains exactly 60 unique IDs, and that the public review template is not mistaken for completed evidence. Keep the \`IDENTITY_REVIEW_KEY.csv\` and outcome prices inaccessible to the evidence-review process until after its machine decisions are frozen.
- Do not call an empty form completed. Do not require \`Reviewer_B\` to exist. **The investigator has now withdrawn availability for manual review**; prior "I will review the cases" was a planning statement, not a completed validation.
- No purchasing, paywall bypass, CAPTCHA bypass, credential disclosure, provider/author outreach, journal submission, manuscript upload, or new paid billing. Apply bounded normal requests and cache/hash fetched source documents. Network restrictions count as evidence barriers, not permissions to fabricate a reference.

## 2. Automated 60-case documentary investigation

Create a maintainable, checkpointed pipeline under \`research_completion/phase3/followup_20261021/autonomous_review/\`, keeping case-identifiable generated files under the ignored \`research_completion/phase3/private_runtime/followup_20261021/autonomous_review/\`. Use existing private data and no external upload of its rows.

### 2.1 Blindness and review order

- Retain the seeded randomized case order, \`case_id\`, origin quarter, exactly next quarter, corridor direction, provider, instrument, access point, payout/pickup, speed, network, target candidate multiplicity and alternatives.
- No exposure to the original sampled stratum, threshold outcome, cost, model probabilities, or whether any match currently agrees with the selected rule.
- Do **not** use case-by-case commercial identifiers in public logs, README, Streamlit or GitHub Actions.

### 2.2 Lawful historical evidence search

For each case or shared provider/corridor group, automatically attempt:
- dated provider product schedules, archival product terms, service feature pages with contemporaneous effective dates;
- regulator notices, payments-network product documentation, publicly accessible provider reports with exact effective dates;
- period-correct World Bank RPW methodology and survey change notices;
- lawfully accessible page archives or PDF captures, where access is permitted.

Batch/reuse provider/quarter source retrieval to minimise redundant network requests. Record which sources were actually opened, whether the document mentions **this exact corridor and full service bundle**, whether it explicitly covers **both** origin and successor periods, and any material contradictions. Archive publication dates alone do not prove historic product terms. A 2026 current home page does not validate a 2019 service.

For each attempted source record:
\`case_id,source_id,url,title,publisher,document_date,effective_from,effective_to,corridor_scope,provider_scope,bundle_scope,origin_coverage,target_coverage,section_or_page,quoted_support_or_paraphrase,source_sha256,access_status,checked_at_utc,limitations\`.

Avoid false precision. If all available sources are generic or modern, document them as **context only**. No source URL or page number may be invented. Prefer short paraphrase with attribution over copied long passages.

### 2.3 Two machine passes, explicitly NOT independent human review

- Run a first AI-assisted extraction/assessment from the blinded case and documentary evidence.
- Run a second **adversarial machine audit** that can challenge evidentiary scope, missing alternative candidates, timing mismatch, identical label fallacy and the 2021/2022 source classification shifts.
- The second pass is a *software error-check*, **not** an independent researcher, inter-rater agreement, or external expert. Do not calculate or title its agreement as human validation.
- Frozen machine-only outcomes: \`EVIDENCE_SUPPORTS_SAME\`, \`EVIDENCE_SUPPORTS_DIFFERENT\`, \`UNRESOLVED_INSUFFICIENT_HISTORICAL_EVIDENCE\`, \`NOT_REVIEWABLE\`. These are **documentary plausibility conclusions, not gold-standard service identity labels**.
- Require strong evidence for \`EVIDENCE_SUPPORTS_SAME\`: contemporaneous source coverage of both relevant periods, the same corridor/provider/payment and delivery bundle, and no unresolved competing successor. Identical RPW text labels alone cannot meet that threshold.
- Require strong evidence for \`EVIDENCE_SUPPORTS_DIFFERENT\`: specific historical evidence of materially different products, and not merely changed RPW speed/network vocabulary. Merely failing a match is not evidence that the product exited.
- Source support grade: \`A\` exact dated bundle/document applying to both quarters; \`B\` dated near-period provider/corridor support but partial product specificity; \`C\` generic or one-sided evidence; \`D\` none. An automated status must be \`UNRESOLVED\` where there is no sufficiently case-specific support. Do not force an A from several Bs or an arbitrary confidence cutoff.
- Record separately the source-based reasoning, counterargument, best alternative and why it is rejected (if rejected). Machine conclusions may be revised after the blinded phase, but original decisions and revision audit must remain.
- Save a timestamped, tamper-evident \`machine_review_frozen.json\` containing script commit, source-manifest checksums, review-prompt version, seed, case count, all machine statuses, and SHA256 digest of the frozen machine evidence table. **Never assert a human reviewed it.**

### 2.4 Preserve unknown outcomes honestly

- \`UNRESOLVED\` is a legitimate output even if all 60 remain unresolved.
- Failed HTTP access, missing archived bundle-level information, undated web pages or incompatible service descriptions are reasons for uncertainty, not default SAME/DIFFERENT labels.
- Respect the original 12×5 **stratified** sample design and exclusion of unresurveyed corridors. Do not extrapolate 60 case decisions into a universal matching-error rate, a new gold standard or a reweighted population estimate without design weights and support.
- Compute the proportion of cases with evidence support at grades A/B/C/D and category-specific documentation gaps for honest feasibility assessment; it is not a validation accuracy estimate.

## 3. Scientific inference using documentary evidence

Use only *after* freezing machine-only adjudications to unblind the sample strata and compare to existing algorithmic core/strict classifications. Produce a transparent cross-tab by true sampled stratum, with all UNRESOLVED cases retained, and a clear distinction between:
- quote-record linkage **under an explicit mechanical rule**;
- machine reading of limited historical documents;
- **verified** product identity (generally not attainable absent qualified human corroboration).

Do not replace original reported E1/E2 with AI decisions as if they were observed truth. Keep frozen measurements, including:
- 45,343 eligible cheap USD200 origins;
- 36,429 core valid pairs; 81.1057% conditional continuity;
- core all-origin identification bounds 65.1611%–84.8201%;
- 30,570 strict valid pairs; 81.0468% conditional continuity;
- strict bounds 54.6413%–87.2218%, **12.9215 percentage points wider**.

These are exact *under their specified record identity definitions* and are not estimates of true economic-service survival. Numerator/denominator identities must reconcile for each reported scenario. Do not treat the wider interval as a newly invented missing-data statistical method; the arithmetic follows from added unknowns.

Extend only meaningful sensitivity work:
- source-era before/after Q2 2021 and Q4 2022, without claiming causal attribution;
- breakdown of records that strict identity makes newly unknown, and observed continuity in those records under core identity, clearly labelled a cross-definition descriptive result;
- regions, providers, instrument/payout groups, quarter composition, alternative weighting, and supported vs unsupported history evidence where sample size permits;
- optional **illustrative** scenarios around linkage false positives/negatives, explicitly assumptions not empirical error rates;
- final audit of the known 14 strict cross-platform table mismatches; do not disguise them as resolved by CI fixture tests, and do not refit models just to make their ranking appear stronger.

Keep the original adverse model inference: no prospective validation or real release-time lead, policy-vs-spline uncertainty includes zero, no operational model. A future-wave requirement should not automatically veto a strictly retrospective finite-panel measurement paper, but cannot be ignored for forecasting claims.

## 4. Publication novelty and decision logic

The full Lim author manuscript **v1.1**, repository commit \`c370a619edac2545291a5a30b8d2d035f7c79f3a\`, was reviewed in the prior follow-up. Exact-next-quarter identity-based outcome and bounds were not found in that **specific inspected version**, while substantial novelty remains **unconfirmed**. Reuse the full-text/citation/hashes from \`LIM_OVERLAP_REVIEW.md\`; do not call it the latest SSRN byte-identical publication.

Ask two *different* scientific questions:
1. Is there a real previously unreported empirical phenomenon whose measurement would matter to public RPW monitoring **beyond** the arithmetic of treating extra rows as unknown?
2. Is this phenomenon interpretable from RPW sampled quote records **without pretending** to have verified stable true economic service identity?

Compare exactly against the same-data literature, existing RPW official reports, provider/corridor studies, matched-item replacement/missing data prior art, and the already inspected Lim and Borra manuscripts. Name a precise delta; originality is not conferred merely by running AI or showing an attractive dashboard. An AI literature audit is provisional; say so.

Decision tree:
- **MEASUREMENT_NOTE_READY_FOR_AUTHOR_REVIEW** only if a genuinely consequential, clearly delimited *record-based* measurement finding with adequate novelty, integrity and permissions survives, and every inference is compatible with **no independent human product-validation**. Prepare a complete manuscript appropriate to a statistics/measurement journal or a technical note, with author-approval items still outstanding. Do **not** call it submission-ready or formally externally validated.
- **CONDITIONAL_HOLD_EXTERNAL_VALIDATION** if adequate originality or economic-product interpretation still depends on missing historical documents or qualified human product review. Fully prepare the dossier and objective missing-information list without waiting for the user to review 60 cases.
- **NO_GO_ORIGINAL_ARTICLE** if evidence shows only standard mechanical bounding on ill-defined identity, substantial closest-work overlap or an unfixable estimand. Preserve code/data audits and consider a narrow reproducibility/technical repository output.
- Do not upgrade to GO due to completion of tasks, number of sources fetched, beautiful figures, high classification confidence, peer-reviewed-sounding prose, or model performance.

One last human step remains inherently unavoidable: **the investigator's approval of authorship, declarations and actual journal submission**. Do not ask for this during the execution; finish all other work first and present a simple final GO/NO-GO recommendation.

## 5. Deliverables, tests, privacy and pushes

Create these files (names may expand, not shrink):
- Public safe: \`autonomous_review/README.md\`, \`EVIDENCE_METHODS.md\`, \`REVIEW_FEASIBILITY.md\`, \`AUTOMATED_FINDINGS_AGGREGATED.csv\`, \`SOURCE_SCOPE_SUMMARY.csv\`, \`IDENTITY_SENSITIVITY.md\`, \`NOVELTY_AND_CONTRIBUTION.md\`, \`FINAL_PUBLICATION_DECISION.md\`, \`RUN_LOG.md\`, tests and any manuscript that survives the gate.
- Private ignored: \`phase3/private_runtime/followup_20261021/autonomous_review/case_evidence.csv\`, \`machine_review_frozen.json\`, \`case_source_log.csv\`, locally cached permissible historical reading copies, code-produced case-level review reports, private ZIP.
- Public ZIP: safe aggregate-only science, figures, code, revised conditional manuscript, exact package SHA256 and README.
- Private ZIP: case-by-case review bundle and full machine evidence ledger, stored locally only.
- No \`BLINDED_CASES.csv\`, provider-specific case rows, alternatives, outcome prices, saved HTML cases, source reading copies, confidential tokens or user-private files may enter GitHub, public website or public ZIP.
- Test URL capture metadata and CSV schemas; test 60 unique cases and no dropped review classifications; test conservation of historical outcome denominators and result text vs source CSV; test the public artifact allowlist, synthetic fixtures and dashboard. Do not claim that passed fixture tests reproduce 50 MB source analysis.
- Run existing \`pytest -q tests research_completion/phase3/code/test_science.py research_completion/phase3/followup_20261021/test_followup.py\` and your new unit/integration tests. Respect runtime resource limits.
- Commit at meaningful milestones with unchanged frozen prior raw/model artifacts, reconcile upstream commits, push reviewed safe changes to the existing \`main\` after tests, and verify CI where accessible. If CI not viewable, report unverified. Do not push generated raw data and do not break production Streamlit.
- Finish in one screen of decision-first summary plus exact private/public artifact paths; preserve durable run checkpoints and explicit blockers. Never end with a question asking the investigator to do 60 reviews.

## 6. Execution order (do not stall for human input)

1. Audit local repo, caches, privacy and source files; set clean output boundaries.
2. Implement and test the evidence-only blind review runner; create automatic checkpointing.
3. Search/read historical documents in bounded batches; prioritise relevant primary sources and log failures.
4. Run machine assessment and adversarial evidence audit; freeze complete 60-row machine findings without human labels.
5. Unblind for case-stratum comparison and evaluate documentary support/limitations; do not manufacture agreement.
6. Recompute only justified measurement robustness; no generic additional classifier searches.
7. Make a scientific novelty/measurement GO-HOLD-NO-GO decision; prepare defensible journal-style text only to that level.
8. Run tests, inspect privacy allowlist, package public/private separately, push safe material and provide SHA/status.

**Important:** You can automate research work, not guarantee historical evidence exists. The success condition is a finished and honest evidentiary decision with reproducible artifacts, **not** an invented independent human validation. Execute all feasible phases without waiting for manual reviews.
