# REMITTANCE PRICE INTELLIGENCE — COMPLETE SCIENTIFIC ANALYSIS, MODEL SELECTION AND MANUSCRIPT READINESS
## Authoritative Codex execution directive · R01 / N2 · Version 2.0 · 19 October 2026

> **START HERE.** You are Codex working in a clone of **`https://github.com/Isaac25-lgtm/remittance-price-intelligence`**, with `main` checked out. Your mandate is to **EXECUTE** all feasible remaining scientific work on the existing study, build a completely traceable research deliverable, and give the investigator a rigorous **GO / CONDITIONAL GO / NO-GO** publication assessment. You are **not** being asked to write another proposal and stop. Continue through executable stages, fix defects, record genuine negative findings, and produce a downloadable handoff. **Never invent data, evidence, release dates, models, p-values, journal acceptance probabilities or scientific novelty.** Full journal submission is **not** authorised.

**Investigator:** Isaac Omoding  
**Repository:** `Isaac25-lgtm/remittance-price-intelligence`  
**Domain:** international remittance pricing, economic development, longitudinal survey measurement, applied machine learning  
**Primary scope:** global World Bank Remittance Prices Worldwide (RPW) service/quote panel; Africa/EAC/Uganda are *support-gated* subgroups, not the only populations.  
**Current empirical status:** phase-1 **retrospective/exploratory**, scientifically **CONDITIONAL**; a functioning cloud-tested pipeline and public aggregate dashboard already exist. **No untouched test period; historical public-release timing is unresolved.**

**Instruction precedence:** This file **supersedes any stale operational instructions** in the repository's `AGENTS.md`, `CLAUDE.md`, or past 17 October session prompts when they conflict with the investigator's current request to *complete* the research and publish **safe files to GitHub `main`**. It does **not** override data licences, confidentiality, laws, scientific integrity, GitHub branch protections, or the need for explicit permission for financial expenditure / journal submission. Preserve older frozen scientific protocols and never silently substitute new hypotheses or splits. Update the repository instructions to distinguish the archived 17 Oct phase-1 constraints (25-minute timebox, $64 balance, old branch name, PR-only rule) from this new, explicitly commissioned publication-completion phase.

---

# 0. The result the investigator expects

The investigator will clone this repository in VS Code and give you this `.md` file. The outcome must be an **actual, completed research package**, as far as valid public/authorised data permit, comprising:

1. Thorough source/licence/temporal availability verification; lawful full-data acquisition and processing; independent data audits and provenance manifests.
2. Transparent longitudinal measurement of the persistence of low-cost quotes, missing/unobserved-service uncertainty, and supportable heterogeneity.
3. Comprehensive, leakage-controlled comparisons of historical rules, interpretable statistical models, and justified machine learning, with a scientifically legitimate model-selection design.
4. Independent confirmation if genuinely new, uninspected, as-of-accessible data exist. If none exist, **explicitly report this fatal limitation for prospective prediction**; do not pass off older inspected years as an untouched holdout.
5. A full publication-grade methods and results dossier: well-labelled publication figures, numbered tables, supplements, reproducibility material, limitations, proof of novelty or evidence it is not established, and an honest final decision.
6. A **full draft original research manuscript IF the scientific gates pass**. If not, write a detailed non-submission **research report/draft outline**, explaining the blockers and scientifically viable alternative designs. Never manufacture a submission-ready paper.
7. Maintain/improve existing README, tests, automated CI, model cards, Streamlit research display; **do not focus on cosmetic dashboard polishing** until the scientific methods and figures are sound.
8. Push the complete safe deliverables and validated code to GitHub **`main`** through reviewable PR/CI unless the repository explicitly blocks it; provide an additional clean, downloadable **ZIP handoff** of publishable-safe artifacts. Never push secrets, provider/service row records, restricted datasets, individual predictions, large raw workbooks, or sensitive model artifacts.
9. Final response: exact GO/CONDITIONAL/NO-GO status, model actually selected (or “none”), what was run vs not run, GitHub `main` commit SHA, files/directories, verified link to ZIP or instructions to retrieve it, metrics with uncertainty, data gap ledger, journal submission prerequisites, and the best scientifically responsible next step.

**Do not stop after a plan, a README rewrite, a CI-green check, or a dashboard enhancement.** You are allowed to stop a **scientifically invalid branch** and continue other viable branches. If a required input truly cannot be obtained after bounded legitimate attempts, mark that gate BLOCKED, perform every independent remaining action, and return a complete honest outcome. “Keep working” means persistence and resumable execution, **not** infinite loops, endless hyperparameter searches, cost overages or invented progress.

## 0.1 Resource, safety and action policy

- The human will use VS Code as the interface. **Do not use the human's Windows machine for RAM-intensive processing or model fitting.** Prefer an authorised remote Linux/Codex/cloud compute environment for full downloads, training, bootstrapping and figure generation. Local actions may inspect files, edit text and run tiny unit tests only. If the current Codex session is local, detect that and prepare remote-capable workflows (GitHub Actions, permitted remote container/cloud session) rather than running large jobs locally. **Do not assume VS Code itself provides cloud compute.**
- No paid API, paid server, new service, purchased credits, subscription, paid GitHub runner, or paid usage overage without new user approval. Prior promotional balance information is stale; **do not assume funds or entitlements remain**. Standard permitted GitHub Actions may be used for bounded CI if quota and data terms allow; not as a secret unlimited HPC service.
- One heavy job at a time; initial CPU threads `OMP_NUM_THREADS=2`, `OPENBLAS_NUM_THREADS=2`, `MKL_NUM_THREADS=2`, `NUMEXPR_NUM_THREADS=2`, `PYTHONHASHSEED=0`. Measure actual CPU/RAM/time and scale only on proven evidence. No GPU as a default: tabular RPW data do not justify one without empirical need.
- Ordinary authorised public-data downloads and source literature access are allowed. No CAPTCHA or bot-challenge circumvention. Never disable TLS/security checks, leak cookies, scrape against explicit restrictions, or pretend blocked URLs were accessed. Limit retries (max three per host per acquisition stage with exponential backoff; stop on 401/403), cache source artifacts and record URLs, HTTP statuses, bytes, hashes, observed update dates and UTC access times.
- **GitHub repositories are public.** Do not put raw RPW workbooks, per-service/provider quote rows, per-row predictions, licensing-uncertain material, credentials, personal or private data into Git or ZIP. Aggregate-only public outputs must satisfy `docs/DEPLOYMENT.md` and licence conditions. Treat workbook terms and dataset metadata as authoritative; a dashboard being already public does not automatically approve every new artifact.
- Never submit a manuscript to a journal, post a preprint, message authors, register a DOI, or claim acceptance. Draft submission material is allowed; author confirmation, ethics/permissions and final scientific sign-off remain the investigator's actions.
- **Git:** work on a new `research/r01-publication-completion-2026-10-19` branch (or equivalent), open a PR, enforce tests/source checks, then **merge verified safe work to `main`** because the investigator expressly requested final research files on `main` in this conversation. Use non-force merge and protect existing history. If policy or CI blocks the merge, do not bypass it: leave the PR and report exact blocker. No silent deletion of old results.

---

# 1. Reconstruct the existing repository faithfully before touching any results

## 1.1 Mandatory initial inspection

Run `git status --porcelain`, `git remote -v`, `git branch --show-current`, `git log -8 --oneline`, `git ls-files`, and inspect:

- `README.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `pyproject.toml`, `configs/experiment.yaml`;
- `docs/SCIENTIFIC_PROTOCOL.md`, `docs/STATUS.md`, `docs/PRIOR_ART.md`, `docs/REPRODUCIBILITY.md`, `docs/DEPLOYMENT.md`, `docs/MODEL_CARD.md`, `docs/DATA_ACCESS.md`, `docs/DATA_DICTIONARY.md`, `docs/LIMITATIONS.md`, `docs/DECISION_LOG.md`;
- `src/rpi/{acquire,audit,preprocess,linkage,features,models,evaluate,config,figures}.py`, `scripts/{run_phase1,reproduce_from_cache,presentation_aggregates,run_descriptive,subgroup_metrics}.py`, and all existing tests;
- `results/tables`, `results/figures`, `results/reproduction`, `dashboard/app.py`, `.github/workflows`.

Use actual current file names: versions may have changed since 19 October. Search locally in the clone, but never hallucinate absent files. Save a machine-readable pre-work inventory (`research_completion/audits/initial_repo_inventory.json`) with branch, HEAD, tracked file list/hash, test outcome and all anomalies. Freeze prior outputs and record their hashes before changes. Do not alter `configs/experiment.yaml` for the original phase-1 run; create **new versioned** protocols/configs for new analyses.

## 1.2 Verified history at handoff (CHECK, DO NOT ASSUME IMMUTABLE)

As of the current documented GitHub `main`:

- Official World Bank RPW complete dataset: `rpw_dataset_2011_2025_q3.xlsx`, **50,780,339 bytes**, SHA-256 `f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8`; source `https://datacatalogfiles.worldbank.org/ddh-published/0037898/DR0095523/rpw_dataset_2011_2025_q3.xlsx`.
- Post-Q2-2016 sheet: **204,469 quote rows**, **37 observed quarters**, **368 ordered corridors**, approximately **699 normalised providers**; missing **2025Q2**. Do not bridge this missing wave as a single next-quarter transition.
- Initially cheap primary cohort (USD 200 basket, non-negative cost ≤3%): **45,343 eligible records**; **36,429** uniquely core-reobserved next-quarter valid-cost quotes in descriptive linkage.
- Phase-1 expanding-year evaluation across 2022–2025Q1: **19,667 evaluation rows, 329 corridors**. All tested years were already inspected in earlier work: not an untouched confirmatory sample.
- Pooled Brier: random forest **0.126452**, HistGradientBoosting **0.128636**, spline logistic **0.132093**, ridge logistic **0.133148**, shrunk provider/corridor history **0.138967**, prevalence **0.149848**. **Lower is better**; these are exploratory retrospective results, NOT prospective operational performance.
- Historical phase-1 `GBM - spline` pooled Brier difference approximately **−0.00346** with one-way corridor and provider uncertainty intervals reported in the README. For 2022–24 only, provider-cluster interval includes zero; spline slightly beats GBM in 2024. Do not conceal this heterogeneity.
- The conditional continuity probability among reobserved cheap quotes is approximately **0.811**; extreme overall bounds from unknown successors approximately **0.652–0.848**, much wider for 2025. The reobservation prediction model **did not beat prevalence in 2022–2023**.
- Sub-Saharan Africa: **2,779** test rows, **74** receiving corridors, about **688** observed threshold failures, no statistically established tree-over-spline superiority. EAC: **731** rows, **25** corridors, around **137** failures. Uganda receiving: **140** rows, **3** corridors, **20** failures—**no credible Uganda-specific model claim**.
- Frozen modelling design is `configs/experiment.yaml`, committed before the first recorded model metrics (phase-1 commit `ecc7c49`). Reproduction from cached verified workbook matched **28/30 result tables**, with the remaining two differing only by nondeterministic elapsed fit seconds, not substantive results.
- Existing live aggregate-only Streamlit dashboard: `https://isaac-remittance-research.streamlit.app/`; repository code under `dashboard/`. This is a **research display**, not a consumer product nor operational forecasting service.
- Current `main` had the presentation and reproducibility work merged by 17 October 2026. Do not rely on an old branch-level narrative saying it remains unmerged.

**These baseline counts and scores are provenance anchors**. If new independently downloaded input has a different hash/schema, treat it as a *new source vintage* and produce an explicit comparison rather than replacing original denominators. Distinguish exact numeric reproduction from methodological extensions.

---

# 2. Scientific question and claims policy

## 2.1 Preferred working title — change only on evidence

> **The Persistence of Affordable International Remittance Quotes: Longitudinal Measurement, Selection into Reobservation and Benchmarking of Machine Learning Across Global Payment Corridors**

Alternate (ONLY if true historic lead time is established):

> **Can Machine Learning Anticipate the Loss of Low-Cost Remittance Quotes? Release-Aware Longitudinal Evaluation Across International Corridors**

Do not put “prospective prediction,” “real-time early warning,” “guaranteed affordable transfer,” “consumer savings,” “fraud detection,” “provider survival” or “Uganda-specific AI” in the title/abstract unless the data actually measure those things and the required tests pass.

## 2.2 Scientific aim

Determine how often surveyed services that currently quote a low total cost remain below the same threshold at their next quarterly observation; what can be inferred when comparable quotes are not observed; and whether appropriately timed historical/statistical/ML models improve estimation or triage of subsequent observed threshold crossing over strong simpler rules, conditional on defensible data timing and service identity.

## 2.3 Exact estimands (all must stay separate)

- **E1 (primary observed-sample endpoint):** `P(0 <= C[t+1] <= 3% | 0 <= C[t] <= 3%, same *core* service uniquely and validly reobserved at exactly q[t+1])` for the USD 200 (`cc1`) basket. Model output is a probability of *staying cheap*, with separate failure-risk `1 − p` used for priority ranking. Observe only at exact `qidx+1`.
- **E2 (population uncertainty bounds):** for all eligible cheap origin quotes, `lower = confirmed_stays / all_eligible`; `upper = (confirmed_stays + unknown_next_state) / all_eligible`. Define unknown classes separately: corridor not resurveyed, service missing in surveyed corridor, ambiguous identity, target cost invalid, right censoring. Exclusions and eligible denominators must reconcile. Never equate a missing quote with market exit or unaffordability.
- **E3 (corridor-level availability of *surveyed* cheap quotes):** among origin corridors with ≥1 observed cheap quote and surveyed again in next quarter, share with ≥1 observed cheap quote next time. Not proof of consumer availability.
- **E4 (reobservation process):** estimate and, if feasible, predict probability of a uniquely matchable next-quarter quote. Do not silently treat it as the same event as E1; preserve and report its previously negative baseline comparison.
- **Secondary endpoints**: 5% threshold, USD 500 (`cc2`) basket, two-quarter *true* horizon (explicit handling of middle wave and censoring), continuous next cost/delta, threshold margin bands, and appropriate corridor aggregated outcomes **only when data valid and pre-specified before looking at new metric results**.

## 2.4 Prespecified candidate contributions to test and falsify

A. **Measurement:** a reproducible, conservatively linked service panel quantifies when low-cost quote persistence estimates depend on identity rules, wave omission and non-reobservation; report partial identification rather than one naive number.

B. **Predictive incremental value:** strong and interpretable reference rules are outperformed on a legitimate information set; evaluate whether any tree advantage remains reliable **relative to spline logistic and hierarchical history**, not merely the constant rule.

C. **Monitoring value:** a model genuinely changes detection of observable threshold increases at fixed analyst review capacity compared with historical/cost/logistic rules, subject to explicit review costs and as-of availability.

D. **Transportability/heterogeneity:** identify where and why the pooled result does or does not transfer across later quarters, providers and corridors; use strict independent holdouts only when valid; do not rebrand subgroup analysis as external validation.

Falsifiers: no demonstrable incremental information over well-specified conventional models; no lead time for the claimed forecasting use; selection into reobservation undermines interpretation; competitor literature has already established same result; implausible provider identity matching; unstable advantage under year, provider/corridor/time uncertainty or revised data. A carefully documented null can justify a methodological paper only if it answers an unresolved research question and its own rigor is adequate.

---

# 3. Priority 1: comprehensive up-to-date closest-work novelty audit (execute, don't just list)

**This is a possible publication killer. Do it before large model searches.** Prior repository file `docs/PRIOR_ART.md` contains seven works and explicitly states no full texts read; that is insufficient for a major novelty claim.

## 3.1 Search breadth

Search (within legitimate accessible sources) Crossref, OpenAlex, Semantic Scholar, World Bank Open Knowledge Repository / RPW reports, IMF eLibrary or RePEc, Google Scholar discovery pages if accessible, SSRN, working-paper/preprint repositories, IDEAS/RePEc, university repositories, and open GitHub technical projects. No bypassing paywalls, logins or access controls. Retrieve full texts where public and licensed. For inaccessible works, capture abstract/metadata and state **FULL TEXT NOT READ**. Keep reference URLs, DOIs, dates, datasets, populations, outcomes, predictors/methods, validation schemes and limitations. Verify direct methodological claims against the text, not only search snippets.

Mandatory query families (expand variants): `Remittance Prices Worldwide service level persistence`, `RPW provider corridor quarter longitudinal`, `remittance low cost 3 percent persistence`, `remittance service reobservation`, `money transfer provider pricing stability`, `price dispersion remittances machine learning`, `remittance fee FX margin prediction`, `digital remittance prices panel 2016 2025`, `remittance quote provider matching`, `corridor monitoring remittance price`, `SSRN preprint RPW pricing`, `remittance service comparison cheapest provider consistency`.

## 3.2 Exact competitors and new discovery leads to inspect

1. **Beck & Martínez Pería (2011)**, *What Explains the Price of Remittances? An Examination Across 119 Country Corridors*, *World Bank Economic Review*, DOI `10.1093/wber/lhr017`; working paper variants. Confirm their data unit and estimand.
2. **Beck, Janfils & Kpodar (2022)**, *What Explains Remittance Fees? Panel Evidence*, IMF WP 2022/063, DOI `10.5089/9798400205439.001.a001`; strongest classical corridor-level comparison. Full-text review mandatory if legally available.
3. **Boon Chuan Lim (posted 1 Jun 2026)**, *The Digital Discount in Cross-Border Remittances: Stylised Facts on the Inclusion Gradient, 2016–2025*, SSRN `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6830281`, DOI as presented `10.2139/ssrn.6830281`. Its abstract describes a **188,700-provider–corridor–quarter RPW panel**. **Very important same-dataset/service-level competitor**: distinguish its channel/cost fixed-effects estimand from our same-service continuity and reobservation analysis. Compare identity rules and analyses only if full text accessible. No claim it already answers/doesn't answer ours without examination.
4. 2026 cross-corridor remittance digital/pricing studies, including India-relevant service-level econometric work previously surfaced; verify titles, authors, DOI/URL and exact questions anew, not from memory.
5. **World Bank RPW methodology, data-download licence, quarterly reports/annexes and SmaRT/SDG indicators:** `https://remittanceprices.worldbank.org/methodology`, `https://remittanceprices.worldbank.org/resources`, `https://remittanceprices.worldbank.org/data-download`, `https://datacatalog.worldbank.org/search/dataset/0037898/remittance-prices-worldwide`.
6. **Other non-peer-reviewed analytics competitors:** `https://plainremit.com/research/what-changed-this-release` (as of 2026, corridor-level release differences, not automatically service persistence); `https://plainremit.com/statistics` (corridor-level longitudinal pricing); `https://github.com/xenaxu7/remittance-cost-analysis` (fee/FX analyses); search for provider quote continuity sites. Verify content and methodological overlap. Not equivalent to peer review, but relevant to **originality**.
7. Gurira (2025 online / 2026 issue) RPW transparency valuation study, remittance provider price-consistency products, and relevant demand/competition experiments; identify if any study already performs exact next-quarter service matching or intervention ranking.

Search through the actual execution date. The titles, dates and links above are **starting leads, not proof of novelty or a literature search already performed by Codex**.

## 3.3 Mandatory outputs

- `research_completion/literature/search_log.csv`: query, engine/source, execution timestamp, hit count where known, screened/selected reasons; record access failure, not false coverage.
- `research_completion/literature/closest_work_matrix.csv` and `...md`: ≥10 genuinely relevant candidate works **if found** (do not fabricate a minimum), with fields: exact DOI/link, author, date, published/preprint/repo, dataset/period, unit, outcome, analyses, validation, sample, paper finding, authors' limitations, independent critique (separate), access depth (`FULL_TEXT`, `ABSTRACT`, `REPOSITORY`, `CATALOGUE_ONLY`, `UNVERIFIED`), and overlap judgment.
- `research_completion/literature/head_to_head_scientific_delta.md`: what each top 3–5 studies already establishes, exactly what R01 adds, falsification cases, and a **substantiated** novelty verdict (`SUBSTANTIAL`, `INCREMENTAL`, `OCCUPIED`, `UNRESOLVED`).
- `research_completion/literature/references.bib` with valid metadata only; use DOI resolution/actual title verification. Provide concise evidence/locators in notes, without republishing copyrighted full papers.

**Stop gate:** If the closest prior work already performs the exact essential investigation or if the only claim is an incremental AUROC/Brier leaderboard, do not force a publishability GO. Continue the data integrity and reproducible results work; consider narrower measurement/replication paper, clearly labelled.

---
# 4. Priority 2: official data audit, source vintage and true information availability

## 4.1 Recover the source properly

1. Determine whether the official RPW workbook is present in the **authorised remote** `data/raw/` cache. A cloned GitHub repository is not expected to contain it. The original cache existed in an earlier Claude cloud session but **cannot be assumed to exist in a new VS Code/Codex session**.
2. If missing, consult the official World Bank catalog and fetch its legitimate source. Verify historical expected bytes/SHA-256 if the exact 2025Q3 blob remains downloadable. A changed file is **not** an error to override: preserve both immutable vintages and run a source-version diff (hash, number of waves, date coverage, row counts, columns, quote keys, changed historical values).
3. The catalogue may be newer than the RPW website download page; the catalog currently describes a 2025Q3 complete dataset, while another RPW site page may have stale display text indicating 2025Q1. Treat **metadata, actual file content, and file-publication timestamps separately**. Do not assume Q4 2025 or 2026 data exist merely because today's date is October 2026. Check official releases carefully.
4. Respect stated provenance/licences: catalogue metadata indicates Public / CC BY 4.0, while the RPW site and workbook contain attribution/restricted-material notices. Verify current metadata. Keep source bytes cached outside Git, encrypted/private storage if needed, with checksum manifest; avoid exposing identifiable quote/provider detail in public outputs.
5. If historical data are available from an archive, store source URLs, archived capture time, wave/issue date, content checksum and proof of when the public could have accessed it. Only use archived *official/legitimate* copies and never bypass an access block.

## 4.2 Data audit: don't mechanically trust old cleaning choices

Regenerate **auditable inclusion-exclusion flows** at each stage, by quarter, sending country, receiving country, corridor, provider, service bundle and basket (private row-level for diagnostics; public aggregate only):

- observed data schema/type/units; codebook crosswalk; actual collection date vs assigned quarter (known 181 anomalous 2021Q3 labels); 2025Q2 absence; right-censoring of newest wave;
- missing/unparseable/negative/zero costs, invalid percentages, outliers, apparent conversion-unit errors, total cost/fee/FX-margin reconciliation (rounding-aware tolerance); exclude invalid negative quotes without claiming they are zero;
- invalid ISO3 geography and `KSV`/`XKX` Kosovo naming conflict (log mapping rule and affected counts); unchanged vs changing corridor universe across waves; sending-versus-receiving direction;
- provider name NFKC normalisation, spacing, punctuation, mergers/rebrands, duplicated provider labels, `firm_type` relabelling (not an identity key); speed/network reclassifications;
- ID cardinality by quarter, duplicate origins/targets, many-to-one linkage traps, basket mixing, survey coverage vs service disappearance, late publication, and calendar/non-adjacent gaps;
- provider/service-frequency concentration and dependence structure; representation changes after 2022Q4; positivity for subgroup/model selection;
- sample selection and non-reobservation as functions of past quoted price, provider, corridor, geography, survey coverage and wave.

Before any cleaning change that alters original metrics: write `research_completion/protocols/phase2_changes_vs_phase1.md` with reason, count affected, predicted direction, exact code change and prespecified sensitivity. Keep `phase1` untouched as a reproducibility benchmark. Add tests around every known source anomaly, 3% rounding/threshold boundaries, and first/last quarterly observations.

## 4.3 The central timing audit: can this *really* forecast?

**Do this rigorously.** The current repository's most serious unclosed scientific question is when RPW wave prices became publicly available. The current `release_lag=1` history sensitivity does **not** answer it because *current* wave quote features may themselves not have been released by the next wave.

Build a `release_availability_registry.csv` with at least:

`wave, sample_start, sample_end, nominal_quarter_end, report_issue_date, report_page_url, report_pdf_hash, website_announcement_date, web_archived_first_public_by_date, databank_available_by_date, downloaded_complete_dataset_first_seen, earliest_proven_public_date, timing_evidence_type, timing_source_url, evidence_grade, caveats`.

Sources to investigate: official RPW report list and PDF publication pages (Issues 40–54 and earlier where useful), document metadata **not as sole proof**, official site releases and news entries, World Bank Data Catalog version history, Wayback captures when permitted, archived public dataset versions, Open Knowledge Repository records, GitHub public mirrors with first-public timestamps, DataBank archives, RPW release calendars. The RPW resources page lists quarterly issues through September 2025; whether publication happened in the same quarter must be proven, not guessed.

Establish three distinct clocks:

1. `collection_date` — quote surveyed from a provider (may never have been public at collection time).
2. `earliest_proven_public_by_date` — evidenced moment that a particular wave/value set could have been known to an external analyst. A PDF issue date or git committer timestamp is **not automatically** a proven public availability timestamp; grade evidence.
3. `decision_date` — pre-specified time at which a hypothetical analyst could act (e.g., a documented quarterly release date), strictly **before** the outcome observation window begins if claiming a forecast.

**MANDATORY FOR A PROSPECTIVE / OUT-OF-SAMPLE EARLY-WARNING CLAIM:** for every origin predictor, verify `available_by <= decision_date < target_collection_start` (or a defensible alternative aligned to the actual target period). For prices sampled throughout a quarter, the decision rule may need to be after origin release and before the next wave's individual observation—**if not possible, explicitly abandon the early-warning claim**.

Produce both analyses only if legitimately meaningful:

- **A. Release-aware prospective-style forecasting:** restrict all origin quote and historical transition features to publication-known values by the decision timestamp; record lead days distribution and excluded rows; compare baseline and ML with legitimate observed outcomes.
- **B. Retrospective quote-transition modelling:** current survey quote values are treated as if observed at the end of survey collection, without claims of availability to the public; legitimate longitudinal statistical analysis even when live forecast is impossible.

Gate verdict must be `TIMING_PASS`, `TIMING_PARTIAL`, or `TIMING_FAIL`, with primary evidence. If publication timing cannot be proven, evaluate plausible lag scenarios and bound what can be said; never claim verified operational lead time from a lagged feature alone. Under timing failure, pivot publication framing to **measurement, reobservation selection and retrospective model comparison**.

## 4.4 Truly new holdout availability: do not create one by renaming old data

A new October 2026 rerun of 2022–2025Q1 cannot be called independent because those periods, raw files and metrics have been examined repeatedly. When an official newer Q4-2025/2026 RPW wave with proper successor data is available:

1. Verify it is actually new to **all prior research phases**, not just new to one Codex chat. Freeze hypotheses/model choices/feature definitions/threshold/calibration rule **before accessing new outcome labels**. Record git SHA and immutable protocol/checksum manifest; maintain evidence of access dates.
2. Evaluate a true chronological holdout with predictors and labels available by correct times. It must be **isolated from all hyperparameter selection, feature engineering, threshold tuning, explanations and post-hoc decisions**.
3. Report the number of independent quarters, distinct providers/corridors and observed failures. One quarter may be insufficient for robust publication claims even if row count is huge. Include time-block uncertainty and disclose limited sample.
4. If no new wave exists, leave an executable frozen **future-wave evaluation script/config** and an independent-evaluation readiness checklist. Mark `CONFIRMATION_NOT_AVAILABLE`; do not pretend a time-forward retrospective set is untouched. An external split of old data also isn't a new chronological wave; it may address geographic transfer but not prospective temporal confirmation.
5. If new data arrive after the analysis, a genuinely future experiment may be completed in a later follow-up; not by indefinitely looping today.

Outputs: `research_completion/data/source_manifest.json`, `raw_data_audit.md`, `release_availability_registry.csv`, `historical_publication_timing.md`, `inclusion_exclusion_flow.csv`, `cohort_by_wave.csv`, `source_vintage_diff.csv` when applicable, and `data_integrity_tests.md`. Include exact download commands, environment, byte counts and SHA-256 hashes.

---

# 5. Priority 3: service identity, selection into observation and robust estimands

## 5.1 Model the *observation process* as a scientific object

RPW does not observe every provider, every corridor and every service every quarter. Absence at `t+1` can be a survey omission, catalogue change, rebranding, unsupported bundle, provider exit, or unknown cause. Do not equate these. Separate the **survey design** from the price outcome and count disjoint attrition/censoring classes.

For each origin quarter, report: eligible; right-censored; corridor absent; corridor observed but service not; duplicate/ambiguous key; reobserved with invalid price; reobserved with valid price staying ≤3%; valid price moving >3%. The totals must reconcile without overlapping classes. Build sankey/inclusion figures based on true counts, not illustrative animation.

## 5.2 Identity and selection sensitivity ladder

Keep the original core and strict identity as **frozen benchmarks**. Then, if empirical audits motivate it, add separately named preregistered sensitivities:

- **Strict:** all core features plus unchanged speed/network coverage.
- **Core (primary legacy):** corridor+provider+instrument+access+pickup+location+basket.
- **Conservative alternative:** provider+ordered corridor+instrument+pickup+basket with selected metadata fields removed *only if audit shows relabelling* and collision rates remain bounded; quantitatively assess false merges.
- **High-confidence manual validation sample** of changes/rebrands: adjudicate a **small** random stratified sample of ambiguous/changed labels using only public metadata and logged rules, never fuzzy-link unverified rows by default. Keep adjudication audit trail and uncertainty bounds; no made-up provider histories.
- Matched vs unmatched provider/corridor distributions; collision/duplicate counts; stability of direction and magnitude of E1/E2 for each rule.

Do not choose the identity producing the most favourable AI result. Missingness must remain explicit. If the link is not defensible, halt that sensitivity and report failure.

## 5.3 Additional principled missing-outcome analyses

Beyond worst/best E2 bounds, evaluate **clearly assumption-labelled** approaches where feasible, and test identifiability:

- Reobservation model on all eligible origins (when corridor survey coverage is known), comparing baseline prevalence, historical observation rates, logistic and suitable regularised/tree model; report the negative earlier results.
- Inverse probability weighting (IPW) under conditional exchangeability and positivity, fitted on proper training folds, stabilized/clipped weights with effective sample size and overlap diagnostics. Do not market IPW as eliminating MNAR uncertainty.
- Augmented/standardized risk estimates or doubly robust correction **only if appropriate** to the outcome-observation model and identifiable data, with honest assumptions; avoid causal claims.
- Pattern-mixture/MNAR sensitivity: shift assumed price-failure probabilities for unreobserved services across defensible ranges, including extreme bounds, by corridor/region/wave. Report tipping points at which the headline finding changes.
- Logistic/survival competing risks only if a genuine service-exit event is externally observed; otherwise **do not use survival terminology** for missing survey records.
- Threshold robustness: near-3.00% rounding, ±0.05/0.1 percentage point buffers, 5% threshold, USD 500 basket and fee versus FX components, with correction for alternative estimands where outcome meaning changes.

Keep the selection model separate from price model. A two-stage decision score `P(reobserved) × P(stays cheap | reobserved)` is a **scenario-based observed-quote composite**, not a verified market availability probability; publish it only with correct interpretation and positive supporting evidence.

## 5.4 Panel dependence and descriptive targets

Generate publication tables by year, region, destination income group, channel type where reliably coded, corridor-provider lifetime, cost proximity to 3%, price volatility, sample selection rates, provider/corridor sizes, and structural changes in measurement. Weighting can be performed at quote, provider, corridor and *wave* levels, but identify which population each weighting scheme represents. RPW is not a random sample of worldwide remittance transactions; do not generalise weighted quote averages to consumer welfare or market shares.

---
# 6. Priority 4: full modelling and rigorous selection of the best defensible method

## 6.1 Preserve the frozen 2026 phase-1 benchmark

Never delete/overwrite the old model comparisons. Run the exact old pipeline from a verified source as a **baseline reproduction**. Save before/after SHA/metrics comparisons. The previously tested set was already inspected; it is *development evidence*, not new independent verification. Include an audit of features in `src/rpi/features.py` (current cost, fee, FX margin, within-quarter corridor composition, historical continuity, prior cost) and verify that every feature is available at the *declared decision time*, not merely present in a retrospective workbook.

Check the following potential sources of target/temporal leakage using executable adversarial tests:

1. E1 label at `q+1` never enters features at `q` through cumulative history or the same-quarter aggregate.
2. History `target_qidx <= q−lag` is only used when the whole source wave is publicly available by the declared decision date. **A purely numeric lag is insufficient.**
3. Features like `corr_share_cheap`, `corr_min_cost` and `cost_rank_in_corr` use all *survey quotes in quarter q*, and thus are unavailable until the quarter/wave is accessible; remove them in any early-decision scenario that precedes availability.
4. Preprocessing (scalers, encoders, imputation, splines, target encoders, calibration, feature selection and tuning) is trained only on training folds, never pooled across future test rows.
5. Repeated service/provider/corridor records do not cross a supposedly held-out-provider/corridor boundary via history or grouped target statistics. For zero-shot geographic validation, all target-dependent history features for held-out groups must be correctly unseen/missing (use appropriate global fallback).
6. No aggregation uses `cost_next`, `status` (which contains outcome-informed future observability), or future survey coverage to predict the next-quarter event.
7. Selection of matched E1 observations is fully acknowledged and cannot be avoided via outcome-conditioned exclusion without changing the estimand.
8. Reordering data, replacing future values with sentinels, shifting release timestamps and dropping outcome columns should produce invariant admissible feature values. Add unit and integration tests that fail if this property breaks.

Write `research_completion/validation/feature_asof_registry.csv` (feature, input source wave, known-after date, theoretical availability rule, leakage finding, retained vs rejected by scenario) and a feature DAG for the main research report.

## 6.2 Predefine model-evaluation decision and split architecture *before new outcomes*

Create `configs/r01_phase2_publication.yaml` and `research_completion/protocols/phase2_frozen_protocol.md` on a committed branch before viewing any new-wave labels or new performance table. The config should include explicit hypothesis, unit, endpoint, populations, split dates/quarters, model families, tuning bounds, metrics, selection criterion, subgroup gates, uncertainty resampling, primary information scenario, sensitivity families, stopping criteria and random seeds. Never silently rewrite the frozen config; amendments have timestamps and must precede affected metrics. Keep separate `DEVELOPMENT` vs `CONFIRMATORY` result namespaces.

**If no genuinely new wave is available**: use historical expanding-origin evaluation as honestly retrospective. You may apply nested/rolling temporal tuning with an inner chronological validation to compare families, but do not relabel any prior inspected period as untouched or run unrestricted repeated tuning against the final test leaderboard. Create an evaluation plan for future waves and grade confirmation `NOT_AVAILABLE`.

For a credible independent setting with sufficient data, evaluate:

- **Rolling chronological origin**: consecutive non-overlapping target waves and explicit *embargo* on outcomes not known by the decision date; retrain models per predeclared schedule.
- **Geography/provider transfer sensitivity**: grouped held-out corridors and providers with no leakage of their outcome history into predictors; use group-aware splits and careful treatment of within-group service identity. This is transfer evaluation, **not** prospective time validation.
- **Within-period stability**: per-quarter/per-year confidence intervals and temporal blocks; more quote rows in one quarter do not create additional independent quarters.
- **Nested selection**: training window → chronological validation/tuning → frozen final scoring on genuinely untouched holdout if one exists. Primary ranking must not be learned from the holdout itself.

Record the entire split registry with origin quarter, target quarter, decision date, training start/end, tuning windows, test date, row/service/provider/corridor counts, failure counts and whether previously inspected.

## 6.3 Model ladder — fit what data justify, not everything just because available

**Tier 0: operational references (mandatory)**

- Always-stays-cheap rule; training prevalence; last observed binary state;
- Current quote cost / distance to 3% monotone risk ranking;
- Hierarchically smoothed provider-in-corridor → corridor → global historical persistence with past-only observations;
- Rolling last-k continuity rate and provider/corridor cost-change rule, if data sufficiently dense and available as of decision.

**Tier 1: strong interpretable statistical comparators (mandatory)**

- Cost-only logistic; regularised logistic with full permissible predictors (ridge/elastic-net if justified);
- Logistic with splines / generalized additive terms for near-threshold effects;
- Hierarchical/partial-pooling binomial model (random/fixed provider/corridor effects) or proxy shrunk-empirical-Bayes model **if numerically/data feasible and stable**; record extrapolation to unseen groups;
- Monotonic additive spline/GAM if appropriate, evaluating identically to other candidates.

**Tier 2: established ML (mandatory if timing/label gate passes; otherwise honest retrospective benchmark only)**

- Existing frozen `HistGradientBoostingClassifier` and `RandomForestClassifier`, identical hyperparameters for reproduction;
- Calibrated variants trained on strictly earlier valid calibration folds, with Platt/sigmoid/isotonic methods compared without leakage;
- CatBoost, LightGBM or XGBoost **only where obtainable without new paid dependencies** and justified by clear unmet modelling needs (categoricals, calibration, underfitting). Install at most 1–2 justified added families after a cheap controlled benchmark and document compute. Do not run all libraries uncritically.

**Tier 3: only if justified by robust evidence**

- Multilevel/hierarchical gradient boosting, time-aware models or discrete-time transition models where the data structure supports them. Do **not** use LSTMs, transformers, large language models or GPU deep learning by default for these tabular/quarterly snapshots.
- Continuous price forecasting as a separate clearly labelled estimand only if price definition is coherent; compare last-cost, group trend, robust regression and simple tree regressors. Do not force this into the E1 threshold-classification evaluation.

## 6.4 Controlled hyperparameter selection

If sufficient valid training observations and an inner temporal validation exist, perform **bounded** tuning for only a few justified top families. Example feasible grids (adapt to actual data and log choices):

- Ridge/elastic-net `C` from `{0.1, 1, 10}`, elastic-net `l1_ratio` limited to `{0.0,0.5}` where supported;
- HistGBM learning rate `{0.03,0.07}`, max leaves `{7,15,31}`, min leaf `{30,75}`, iterations `{150,300}` with pruning/early stopping **inside train-only folds**;
- RF trees `{200,400}`, min leaf `{10,25,50}`, depth `{None,12,24}`, with compute short-circuiting when gain plateaus;
- Calibration `none`, sigmoid, isotonic only with adequate independent calibration sample and no use of the final test outcomes.

Do **not** execute Cartesian products blindly. Prefer a compact successive-halving/randomized search where valid, seed recorded, ≤~20–30 fits per family by default, at most 2 CPU threads, with early abort when reasonable improvements vanish. The real workload and quota govern final limits. Record tried, failed and skipped candidates; no post-hoc inventing a predeclared search.

## 6.5 Primary and supplementary performance metrics

**Primary metric for E1:** Brier score (probability-of-staying-cheap) on identical eligible, reobserved test rows. Compare to **the best prespecified strong conventional reference**, not just the simplest naive model. Also report Brier skill score (`1 − Brier_model/Brier_reference`) clearly naming the reference, paired absolute Brier difference and relative difference; include model-versus-model *paired* uncertainty.

**Mandatory:** log loss; AUROC; AUPRC for observed threshold failure with failure positive; calibration-in-the-large/intercept, slope, ECE with caveats, decile reliability diagrams (sample and event counts), recalibration effects; stability over time and provider/corridor. Brier decomposition where numerically interpretable.

**Ranking and triage:** recall of observed threshold failures in top 5/10/20/30% review capacity **by origin quarter**, precision/lift, false-alert burden, and comparison with cost rule, history, spline logistic and best ML. Pooling all rows over years as one ranking is a secondary legacy comparison, not an actual within-quarter review policy. Show hypothetically avoided misses, not monetized savings. Never claim that monitoring causes lower prices; no intervention or transaction outcomes exist.

**Inference:**

- Estimate uncertainty for paired score differences by **corridor** and **provider**, separately (reproducible legacy), plus a defensible dependence sensitivity involving *time blocks* and *crossed/multiway cluster structure* where enough clusters exist. Explain exactly which bootstrap procedure approximates which sampling population; a naive cluster-within-cluster procedure is not automatically a valid two-way bootstrap. If few independent periods, report that uncertainty is weak rather than creating spurious narrow intervals.
- Consider a hierarchical bootstrap or multiway cluster-robust variance appropriate to the dependence graph, validated on simulation/fixtures, and report paired estimates rather than comparing overlapping marginal intervals. If unavailable, retain clear one-way bootstrap plus block sensitivity and downgrade inference strength.
- Secondary sensitivity for corridor equal weighting, provider equal weighting, quarter equal weighting and high-frequency quote dominance. Show how target changes with weighting.
- Confidence intervals for absolute metrics, Brier deltas, ranking/capacity deltas, subgroup differences and E1/E2. State resampling seed, reps, unit and interval method. Mark exploratory multiplicity and avoid cherry-picking intervals.

**Model selection rule:** Prefer the **simplest stable and calibrated model that achieves a reproducible, decision-relevant improvement** on strong baselines, under legitimate release timing and acceptable dependence uncertainty. If RF has the lowest pooled Brier but unstable yearly calibration, prefer a calibrated RF or a more robust spline/GBM **only if objectively supported by valid tuning/validation**. If there is no robust incremental benefit, say the model does not justify a predictive paper. The correct “best model” may be a historical rule or “no deployable model”.

## 6.6 Explainability, shift, robustness and subgroup work

- Use held-out/cross-fitted **permutation importance** on admissible features, repeated by quarter/region; document correlated feature bias. SHAP optional only if dependencies available and results stable; never claim SHAP proves causation.
- Partial dependence/ICE or model-agnostic descriptive response curves for important cost/fee/history variables, with observed-data support masks. Check monotonicity near 3%; label associative.
- Drift of total cost distributions, provider/corridor inclusion, channel mix, market concentration, missingness, selection and model calibration across years and pre/post-2022 design changes. Plot, test and interpret shifts without causal claims.
- Subgroups: SSA receiving, East Africa/EAC, Uganda receiving, other income/region groups, digital vs traditional channel if classification verifiable, low/medium/high number of historical observations, and provider/corridor novelty. Enforce appropriate support gates; **do not produce unsupported Uganda-specific AUC/ML advantage** from 20 observed failures.
- Check model sensitivity to source anomalies, core vs strict identity, 5% threshold, USD 500 basket, date corrections, 2025Q2 missingness, one-lag historical features, current-data-vs-released-data assumptions, no historical provider identity, high-overlap/low-overlap observations and leave-one-major-provider/corridor-out stress.
- Where metrics are not estimable (single class, too few clusters/events), output `NOT_ESTIMABLE` with reason; never silently omit difficult years.

## 6.7 Final model and artifact integrity

A selected model may be useful only for **research-only reproducibility**. If a fitted artifact is created:

- Record immutable input hash, code SHA, training periods, preprocessing transformer, dependencies, random seeds, fitted classes and checksum; train-only calibrator, versioned schema.
- Test save/reload parity, expected probability range, Brier reproduction and the absence of lookahead; detect train/test contamination.
- Keep model binaries **private or omitted from public Git** unless licensing, data leakage, disclosure and security checks approve them. A serialized model trained on public quotes can still expose provider-specific information or introduce unsafe unpickling if served.
- The **public Streamlit app remains aggregate-only**. No user-entered provider forecasts/live pricing if timing validity has not been established.

Outputs: `research_completion/models/model_comparison.csv`, `model_selection.md`, `model_registry.json`, `calibration.csv`, `performance_by_wave.csv`, `test_predictions_manifest.json` (NO prediction rows in Git), `subgroups.csv`, `sensitivity_grid.csv`, `decision_capacity.csv`, `model_explainability.md`, `inference_spec.md`, `leakage_audit.md`, `split_registry.csv` and publication-ready figures.

---

# 7. Priority 5: decisive falsification, future-wave and publishability tests

Create one **scientific claim ledger** in `research_completion/assessment/claim_evidence_ledger.csv`:

`claim_id,claim,estimand,required_evidence,source_file_or_paper,method,test_population,observed_result,uncertainty,alternative_explanation,caveat,pass_fail_unresolved,figure_or_table,eligible_manuscript_language`.

The ledger must include at least:

- “Low-cost quotes persist 81.1% conditional on reobservation” — clarify dataset, cohort, percent threshold and confidence/selection limitations.
- “Missing-quote uncertainty materially changes continuity conclusions” — E2 bounds and reasons.
- “ML outperforms a strong interpretable model” — paired Brier and within-quarter decision capture with valid as-of release timing, calibrated models and temporal/time/crossed-dependence uncertainty; both confirming and contradicting years.
- “ML improves independent unseen corridor/provider generalization” — only if grouped out-of-group training/evaluation was actually conducted and leakage-protected.
- “ML predicts in advance of survey outcomes” — only if availability registry supports strictly positive lead time for the input information used; **otherwise FAIL**.
- “Results generalize to Uganda” — **FAIL/not supported** under current observed event counts; do not exaggerate.
- “The paper significantly advances closest prior studies” — only when full-text head-to-head matrix establishes the specific new contribution, not just a new algorithm.

## 7.1 Formal publication gates (binary reasoning, not fake publication probabilities)

Gate | PASS requires | FAIL/UNRESOLVED means
:---|:---|:---
G1 Scientific estimand | E1/E2/E3/E4 distinguished and matched to real data | redesign outcome
G2 Source integrity | official sources with auditable hashes, licensing, schema & coverage | cannot substantiate results
G3 Linkage/attrition | identity collision audit, matching sensitivity and E2 bounds | limit claims or redesign
G4 Availability/timing | release-aware lead time if predictive claim is central | no “prospective” claim; consider measurement paper
G5 Validation | independent confirmation if available, or transparent high-quality nonconfirmatory observational design | downgrade model claim
G6 Strong comparator | all reasonable historical/spline/statistical references, objective selection, no leakage | rerun comparative models
G7 Statistical precision | appropriate dependence aware uncertainty, calibration, drift and stable benefits | limit or reject incremental ML claim
G8 Major novelty | closest same-source and same-question competitors read/compared; material delta | do not recommend full original paper
G9 Practical contribution | actionability or meaningful new measurement knowledge shown, not assumed | narrow interpretation
G10 Reproducibility & transparent reporting | exact recipes, hashes, frozen specs, tests, audit records and safe outputs | research not reviewable
G11 Manuscript/report accuracy | claims supported by corresponding tables/figures; no unsupported cause/benefit | not submit-ready
G12 Permissions/investigator approval | lawful analysis/figures and author verification; any institutional requirements clarified | no submission / restricted deployment

**Decision categories:**

- **`GO_FULL_ORIGINAL_RESEARCH_DRAFT`**: full-text novelty review supports substantial original scientific delta, valid outcome/source/selection/splits, reliable results and inference, reproducible analyses, useful contribution, and claims framed to match actual timing. When no untouched new wave exists, this category is possible only for a **clearly retrospective measurement/validation study** if the independent contribution is already substantial and uncertainty is candid; **not** a paper claiming prospective forecast validation.
- **`GO_METHODS_OR_MEASUREMENT_DRAFT`**: strong original measurement/selection result but operational forecasting remains unestablished; scientifically narrower article (not fake “AI predicts in real time”).
- **`CONDITIONAL_MORE_EVIDENCE`**: good analytical result but unresolved novelty, release timing, attrition identification or independent confirmation blocks the central claim. Prepare report, a draft outline or conditional draft clearly marked NOT SUBMISSION READY.
- **`NO_GO_ORIGINAL_RESEARCH`**: closest prior work already covers the main contribution, or essential outcome/timing/identity invalid, or repeated robust tests eliminate worthwhile contribution. Preserve code/results and recommend abandonment or fundamentally new question. Negative result can be considered only if it is an original, rigorous answer to a clear scientific question.

**No automated journal-acceptance prediction.** The investigator must independently review and choose a journal, confirm authorship, methods, licences, ethics/institutional conditions and final manuscript.

## 7.2 Stop conditions that prevent science-by-endless-search

Stop *algorithm development* and pivot to evidence reporting when: release timing invalidates early prediction, latest independent data unavailable, prospective decision relevance cannot be demonstrated, repeated strong interpretable models tie ML within practical tolerance, or strongest novelty disappears in full-text comparison. Continue required remaining analyses, figures, reproducibility and honest final dossier. Do not keep adding neural nets, searching thresholds or tuning until a p-value is below 0.05.

---
# 8. Publication-ready tables, scientific figures, supplementary material and drafting

**The manuscript presentation must be at the standard of a careful applied economics / development finance paper**, not a software demo or marketing dashboard. No invented charts, synthetic result illustrations or unsupported significance stars. Every figure/table is generated programmatically from a traceable analytic table or model output and includes captions, units, denominator, method, uncertainty, dates and provenance.

## 8.1 Required figures (produce if estimable; else placeholder in figure inventory with explicit `NOT_ESTIMABLE` reason)

| Figure | Content / scientific purpose | Essential cautions |
|---|---|---|
| Figure 1 | Source/eligible quote flow, matched/unmatched/ambiguous/right-censored by quarter | Use exclusive denominators, distinguish unobserved from exit |
| Figure 2 | Global/region sample coverage by quarter, corridor/provider mix and changes in survey composition | Do not call survey data a market census |
| Figure 3 | E1 quarterly cheap-quote persistence with uncertainty and E2 worst/best missing-outcome bounds | Same origin cohort; mark wave missing/censoring |
| Figure 4 | Cost transition distribution, near-3% movements and persistence by baseline distance | 3% rounding and selection acknowledged |
| Figure 5 | All prespecified model families: paired Brier/log loss, by year, calibrated vs raw when valid, historical benchmark visible | Retrospective vs independent-confirmation panels unmistakably labelled |
| Figure 6 | Reliability/calibration curves for top baselines/models with event/count rug or bin sizes | Not just smooth lines; state recalibration sample |
| Figure 7 | At 5/10/20/30% within-quarter monitoring capacity: failure capture and unnecessary review burden vs simple rules | Hypothetical review, not saved money or provider harm |
| Figure 8 | Regional/SSA/EAC/Uganda **support** and performance; show unsupported subgroups as muted `insufficient events` | No Uganda claim from 20 failures |
| Figure 9 | Impact of service identity definitions, attrition assumptions and wave exclusions on E1/E2 | Missing labels not exits |
| Figure 10 | Performance/selection sensitivity to timing/availability assumptions and provider/corridor/time dependence | Do not conflate lag proxy with known release dates |
| Figure 11 | Validated feature importance/associative relationships across time and model families | No causal language; skip if unstable |
| Figure 12 | Headline scientific decision and supported scope diagram (measurement vs forecasting) | A graphical abstract is optional, not evidence |

Generate publication-quality PNG (≥300 dpi) and vector SVG or PDF per figure where feasible, with readable typography, accessible contrasts and consistent plots. Do not hard-code numeric scores in figure drawing: load the final locked results file. Inspect generated figures for blank axes, swapped labels, spurious bars and misleading scales. A separate, explicitly timestamped **legacy-versus-phase2 comparison figure** should reveal any revised conclusions.

## 8.2 Required tables and manuscript supplements

| Table | Required content |
|---|---|
| Table 1 | Data source, survey structure, RPW scope, exact periods and exclusions |
| Table 2 | Descriptive origin/basket/provider/corridor profile and cost/missingness by wave |
| Table 3 | E1/E2/E3/E4, strict/core identity comparisons, bounds and support |
| Table 4 | Training/test splits, model feature registry and preprocessing comparison |
| Table 5 | Primary conventional vs ML Brier/log loss/calibration results with paired uncertainty |
| Table 6 | Within-quarter top-k monitoring sensitivity and decision-cost assumptions |
| Table 7 | Time/region/provider/corridor stability and generalisation with support warnings |
| Table 8 | Prespecified source/identity/threshold/basket/missingness/release timing sensitivity |
| Supplement S1 | Full variable dictionary with types, units, wave availability and as-of dates |
| Supplement S2 | Complete data cleaning/exclusion and linkage reproducibility log |
| Supplement S3 | All models including negative results, hyperparameter registry, calibration and error analysis |
| Supplement S4 | Statistical uncertainty/bootstrap methods and robustness |
| Supplement S5 | Full competitor study matrix, systematic search provenance and novelty argument |
| Supplement S6 | Licence/attribution, data access, software versions, code hashes and explicit use limits |

Tables in `csv` plus manuscript-friendly `md`/`tex` (and optionally XLSX, if easily supported). Number every table and preserve the source dataframe provenance. No provider-identifying small cells in public exports unless deliberate licence/ethical publication review approves them; prefer suppressed/aggregated details.

## 8.3 Manuscript preparation only after passing scientific gates

If and only if `GO_FULL_ORIGINAL_RESEARCH_DRAFT` or `GO_METHODS_OR_MEASUREMENT_DRAFT`, create a complete, coherent **candidate original research manuscript**, clearly labelled **DRAFT — INVESTIGATOR REVIEW REQUIRED**, with:

- **Title** accurately signalling global, retrospective/methodological vs validated forecasting scope;
- **Structured abstract**: background, exact aim/estimand, source geography and time, sampling, methods, major numerical results with uncertainty and calibrated limitations, conclusions that do not overstate impact;
- **Introduction**: size/importance of remittance fees, SDG 10.c context without equating individual 3% offer threshold to aggregate SDG metric, policy relevance, verified closest literature, *exact gap* and a priori contributions;
- **Methods**: source and licence, snapshot sampling, design, units, analytic sample, clock definitions, price measure/fees/FX margin, identity, attrition, E1–E4, model features, historical availability, training/evaluation, baselines, tuned models, metrics, clustering, bounds, calibration, subgroups, retrospective decision simulation, reproducibility;
- **Results**: all denominators from verified outputs; flow, persistence/bounds, model performance by period and region, selected model and strong alternative, operational review simulation with appropriate caveats, robustness and negative findings;
- **Discussion**: accurate comparison against the closest full-text literature, practical value *if supported*, uncertainty due to observation and temporal availability, generalisation limits, strengths, limitations, next empirical studies;
- **Conclusion** that answers the original question and is conservative;
- **References** with valid, checked bibliographic metadata and in-text source links; no fabricated DOI, citation, table or article;
- **Statements** on data availability, code availability, source attribution/no World Bank endorsement, AI assistance disclosures, funding, competing interests, ethics status, author contributions with all unspecified personal facts marked `INVESTIGATOR TO CONFIRM` rather than invented;
- **Supplementary methods/tables/figure legends** and an appropriate reporting checklist (TRIPOD+AI may offer useful general transparency principles but is **clinical prediction guidance**, not a compulsory financial-economics standard; do not falsely claim compliance or force its clinical terminology onto remittance economics).

Provide `.md` and `.docx` if rendering tooling is available (pandoc/docx libraries), plus a reader-friendly `.pdf` only if generated correctly. Validate formatting and cross-reference integrity programmatically or by rendering inspection; the Markdown must remain the canonical editable text. If a format cannot be built without new paid services, deliver the supported ones and record the limitation. Do not let document conversion block core scientific work.

If `CONDITIONAL` or `NO_GO`: create a **complete scientific evidence report and conditional manuscript outline**, plus optionally a labelled *not-for-submission* discussion draft, but do **not** pretend journal submission is warranted. Include the manuscript structure and statements of what must change; explain whether a narrower measurement article can still be publishable with existing evidence.

## 8.4 Source and authorship integrity

- No fake author affiliations, funders, sponsorships, ethics approvals, collaborators, data permits, grants, journal impact factors or citation counts.
- The user is the investigator and scientific decision maker; list other authors only if explicitly confirmed. Follow the target journal's human-authorship rules. AI assistance must be disclosed accurately and does not become authorship.
- Disallow citation laundering: figures and statistics have code/result-file references; external research assertions have bibliographic sources, and speculative statements are labelled hypothesis/inference.
- Compare calculated counts in abstract, tables, README and dashboard automatically. If they disagree, release must fail until corrected or discrepancy fully reconciled.

---

# 9. GitHub outputs, professional README, Streamlit and full handoff bundle

## 9.1 Preserve the functioning repository

Do **not** rebuild from scratch, replace old valid code with a fancy but untested new pipeline, or delete old negative experiments. The new work goes under `research_completion/` and adds reusable tested modules under `src/rpi/` only where necessary. The original phase-1 `results/` remains stable or is versioned explicitly if updated. Distinguish committed safe aggregates, private local processed tables, and frozen source files.

Update README so a first-time reader can see, near its beginning: study question; **current publication verdict**; source/geographic coverage; status of timing/novelty/validation; 4–6 major honest results; strong benchmark comparison; reproducible remote commands; true artifact/data availability; table/figure navigation; manuscript readiness; live safe Streamlit URL (if unchanged); citations and clear limitations. A previous phase-1 README must not continue saying all new work is future if executed. The README is a scientific abstract of actual results, not advertising.

Update `AGENTS.md`/`CLAUDE.md` to (a) preserve historic research rules, (b) identify actual current state and new protocol, (c) remove stale instruction that new merges are forbidden, while maintaining safety/CI/licence safeguards; (d) point directly to this completion directive and the final verdict file. Do not hardwire absolute Windows paths in runnable Linux scripts.

## 9.2 Maintain the existing safe presentation

The live Streamlit app already exists: `https://isaac-remittance-research.streamlit.app/`. Modify it only to show **verified** new aggregate data and publication conclusions. Preserve old links/paths when possible. Add an investigator research-notice ribbon with data cutoff, analysis date, model status, retrospective vs independent confirmation, lead-time caveat, source attribution, and download provenance. All model families, strong historical baselines, E1/E2 and uncertainty must remain visible. The app MUST NOT depend on model training, large raw workbooks, or secrets at startup. Smoke-test against Python 3.11 and the deployed dashboard dependency set. Verify deployed pages if authorised tools permit; a GitHub commit is not proof the hosted app redeployed.

No polished design takes priority over scientific validation. If a chart is conditional, show it as conditional rather than suppressing the limitation.

## 9.3 Exact folder structure to create and fill

```text
research_completion/
  README.md                              # Navigation; verdict and run ID
  protocols/
    phase2_frozen_protocol.md
    phase2_changes_vs_phase1.md
    protocol_amendments.md
  data/
    source_manifest.json
    raw_data_audit.md
    source_vintage_diff.csv              # only if multiple vintages
    release_availability_registry.csv
    historical_publication_timing.md
    inclusion_exclusion_flow.csv
    cohort_by_wave.csv
    data_integrity_tests.md
  literature/
    search_log.csv
    closest_work_matrix.csv
    closest_work_matrix.md
    head_to_head_scientific_delta.md
    references.bib
  validation/
    feature_asof_registry.csv
    leakage_audit.md
    split_registry.csv
    holdout_status.md
    dependence_bootstrap_methods.md
  models/
    model_registry.json
    model_comparison.csv
    model_selection.md
    calibration.csv
    performance_by_wave.csv
    subgroups.csv
    sensitivity_grid.csv
    decision_capacity.csv
    inference_spec.md
    model_explainability.md
    test_predictions_manifest.json       # hashes/counts only, NO rows
  tables/
    table_01_source_flow.csv
    table_02_profile.csv
    table_03_persistence_bounds.csv
    table_04_split_features.csv
    table_05_models.csv
    table_06_decision_capacity.csv
    table_07_transfer_subgroups.csv
    table_08_sensitivities.csv
    supplementary_*.csv
  figures/
    figure_01_*.png
    figure_01_*.svg
    ...                                  # files actually created only
  assessment/
    claim_evidence_ledger.csv
    publication_gates.csv
    PUBLICATION_VERDICT.md
    REMAINING_BLOCKERS.md
    reviewer_challenges.md
    final_execution_report.md
  reproducibility/
    environment_lock.txt
    version_manifest.json
    commands_executed.jsonl
    run_manifest.json
    test_report.md
    source_to_results_comparison.csv
    file_hash_manifest.csv
  manuscript/
    candidate_article.md OR conditional_research_report.md
    candidate_article.docx               # if legitimately generated
    candidate_article.pdf                # if legitimately generated
    supplementary_material.md
    references.bib
    figure_legends.md
    table_legends.md
    reporting_checklist.md
    investigator_signoff_checklist.md
  deliverables/
    handoff_contents.md                  # printable inventory
    publication_brief.md                 # lay + technical summary
    git_and_download_links.md
    SHA256SUMS.txt
  private_runtime/                      # GITIGNORED; never upload
    raw/
    processed/
    row_predictions/
    fit_models/
    provider_level_diagnostics/
```

This tree is a **required logical content map**, not a demand to commit empty files. Generate real files when results are available; for blocked outputs, put a clear reason in `REMAINING_BLOCKERS.md`/inventory rather than generating synthetic CSVs to make the tree appear complete. The final zip should be **flat enough for investigators/reviewers to navigate** and include required audit/report files without raw microdata.

## 9.4 Downloadable package: exact rules

When execution reaches its scientifically honest checkpoint, assemble a **single versioned handoff** from allowlisted safe files:

`dist/REMITTANCE_R01_PUBLICATION_HANDOFF_<YYYYMMDD>_<shortSHA>.zip`

Include: `START_HERE.md` (verdict, evidence scope, reproduction instructions), candidate manuscript OR conditional report, supplements, references, all public publication figures and non-sensitive tables, frozen protocols, current models' metadata/results, as-of/release registry, full closest-work matrix, claim ledger, source and file hashes, `README.md`, reproducibility checklist, link to code commit and live Streamlit. Exclude `data/raw/`, `data/processed/`, caches, quote/provider-level rows, fitted binaries, secrets, cookies, unlicensed source PDFs and private metadata.

1. Run a deterministic packaging script (`scripts/build_publication_handoff.py`) that verifies the allowlist and fails if forbidden filenames/columns/small-cell provider identifiers are present.
2. Compute SHA-256 of every included file and the ZIP. Confirm ZIP opens and `START_HERE.md` references existent files. Validate the README links, all figure captions, citation IDs and table denominators.
3. The code/docs/figures can go on GitHub main; the ZIP may also be uploaded if within acceptable repository size, or attached as a *downloadable GitHub Actions artifact* or draft-release asset that does not misrepresent scientific publication. Do not automatically mint a formal publication release/DOI. If the environment supports direct file attachment to the user, also supply the verified exact path. Do not invent a sandbox URL.
4. **Provide an actual downloadable URL/path** in the final reply, or clearly state exactly where the bundle was built and the authenticated retrieval step if direct linking is unsupported. A GitHub folder alone is not equivalent to a one-file download.
5. Don't assume an Actions artifact persists forever; include a reproducible packaging command and retain public-safe source files in `main`. If a GitHub release or large binary upload would be a consequential publication action, request confirmation instead; use a branch/Actions artifact or direct handoff in the meantime.

## 9.5 Final Git integration sequence

```
1. Record starting `main` HEAD; check uncommitted files and remote.
2. Create versioned completion branch; protect frozen historical results.
3. Commit new protocol/registries before examining new labels/results.
4. Execute stages with atomic commits and resumable checkpoints.
5. Run unit, adversarial, integration, reproducibility and Streamlit tests.
6. Run license/privacy/metadata/file-size checks.
7. Push branch; open PR summarizing scientific changes, results, blocked gates and file manifest.
8. Wait for CI to complete (not just pending); resolve legitimate failures without disabling real checks.
9. Check mergeability and user-authorised merge into `main`; do not force-push or bypass protections.
10. Verify the `main` branch contains required files, not merely a closed PR.
11. Verify hosted dashboard if updated; generate final ZIP and report links.
```

If the GitHub connection lacks permissions, record exact failing operation/response; do not claim merged. If running fully local with no remote cloud compute available, complete the protocol/literature/software work safely, push verified code if authorised, and label all large analyses pending remote execution—not completed.

---

# 10. Scientific and software quality assurance contract

Run relevant tests at every checkpoint. Existing CI green status is a starting point, not proof that publication claims are correct.

**Mandatory test categories:**

- Deterministic source checksum, schema and source-vintage discrepancy detection.
- Exact next-quarter vs gap tests (`2025Q1 -> 2025Q3` MUST NOT count as exactly next quarter); date/time parsing; ordered corridor direction; basket separation; unique identity keys; right censoring; anomalies/negative cost treatment.
- Missing-state exclusivity, origin/target flow arithmetic and E1/E2 denominator identities.
- Leakage canary tests on target quarter and publication availability; null future fields; check that source release-lag changes impact predictors exactly as declared, with no row-level target leakage.
- Fold-safety of all imputers, normalisers, encoders, splines, recalibration and hyperparameter searches.
- Held-out corridor/provider test to prove target history doesn't transfer inadvertently.
- Calibration numeric bounds, Brier/log-loss identities, correct sign of failure risk, tied-score top-k selection and within-quarter capacity.
- Multiway/block-bootstrap resampler structural validity; confidence-interval monotonicity and stratified simulation checks; appropriately limited inference if few periods.
- Reproduction from independently fetched/hash-matching official workbook. Compare numeric tables using relative+absolute tolerances, record nondeterministic timing/metadata separately; retain old phase-1 outputs.
- Robust handling of missing/blocked raw sources with explicit missing-input status, **not** synthetic fallback presented as actual observations.
- Dashboard read-only safe export allowlist and test every section/control with Streamlit AppTest; no per-quote source rows or provider names; deploy from correct Python dependencies.
- Manuscript machine check: headline numbers in abstract/text match locked tables; figure numbering, references, DOI formats, unavailable footnotes, completeness of figure legends, cross references and availability disclosures.
- ZIP safety/integrity: archive open test, hashes, no forbidden paths/columns/credentials/private rows, and correct bundle download link.

**Reproducibility standard:** full executed shell commands with timestamps and exit codes; seed, Python/libs/platform and CPU settings; source URL/byte count/hash; run ID, Git SHA and clean/dirty status; training/test windows, exact cohort sizes, model selection history; metrics with sampling units and CIs. Separate `REAL-DATA EXECUTION` vs `SYNTHETIC UNIT TEST` vs `REUSED PRIOR OUTPUT` explicitly in every log/report.

Add GitHub CI for lightweight tests/integrity, not raw workbook downloads or model fits unless a correctly authorised, quota-bounded remote data source exists. Securely cache any restricted permitted data off Git; do not use public GitHub Actions artifacts as private data stores.

---

# 11. Execution order, checkpoints, automatic recovery and progress integrity

Work through the sequence until **all feasible scientific work is executed** and the final research package is created. The phases below are ordered by what could materially change the paper; **not** by what is easiest to make attractive in GitHub.

| Phase | Mandatory execution | Evidence to show before progressing |
|---|---|---|
| P0 | Reopen current repo; inventory; detect remote compute, permissions, source cache, CI state | verified Git SHA; original results backed up; execution log |
| P1 | Full competitor searches and full-text head-to-head; preliminary novelty decision | sourced matrix, search audit, originality falsifier |
| P2 | Official source/version audit and historic release-timing reconstruction | real source hash; auditable release registry; timing PASS/PARTIAL/FAIL |
| P3 | Clean/validate data and link services; observation-selection and E1/E2/E3/E4 | exclusive flow, data dictionary, identity/attrition robustness |
| P4 | Freeze new protocols and holdout plan; leakage tests | immutable config commit and test evidence |
| P5 | Run full baseline+ML comparisons, nested chronological validation as appropriate | model registry, actual scores, paired/time-aware intervals, negative results |
| P6 | Additional checks: model calibration, missingness scenarios, transportability, 3%/5%, cc1/cc2, decision value | complete sensitivity grid and external support caveats |
| P7 | Independent confirmation if new wave exists; else transparent no-holdout gate | evidence of true new data or explicit `NOT_AVAILABLE` |
| P8 | Locked scientific verdict from gate evidence; manuscript draft if GO, otherwise full research report and rescue plan | completed claim ledger, verdict with exact blockers |
| P9 | Complete tables, figures, supplements, README, dashboard consistency, test suite, handoff ZIP | audited files, successful CI, safe archive integrity |
| P10 | Push, PR review, merge permitted safe work into `main`, verify files and download | exact `main` SHA and handoff link or documented blocker |

**Failure handling:**

- Source download 403/401? Record and use legitimate official alternative; do not bypass. Continue literature, existing aggregate audit and tests.
- Raw file unavailable in current runtime? Do not run large fits on Windows by default; acquire in authorised cloud. If remote compute unavailable, leave working reusable scripts and a clearly blocked real-data gate.
- Public-release date cannot be established? Run only scientifically justified retrospective analyses, change study framing, and list what would unlock prediction.
- No newer holdout? Declare unavailable; build frozen forward holdout evaluator; do not manufacture a new test.
- Package missing optional doc converter? Build Markdown/CSV/PNG and log conversion issue; do not stop package.
- Low memory, timeout, model crash? Make stage idempotent/checkpointed, inspect logs, reduce threads/batch, resume. Do not silently remove a failed model from comparison.
- Git conflict? Rebase/merge conservatively on actual `main`; preserve prior results. No force-push.
- Inconclusive significance or weak novelty? Continue honest report and decision, not indefinite model fishing.

**Resumability:** Maintain `research_completion/reproducibility/progress.json` or a checked-in equivalent listing phase, completed stages, input/output checksums, frozen decisions, last exact command, exit status and next safe action. Commit after meaningful stages. If interrupted by context window, cloud-session expiry or token cap, the next Codex run should **read the progress file and continue** without resetting to the beginning. One Codex session is not guaranteed to run forever; do not falsely promise unattended work beyond platform limits.

**Feedback frequency:** Brief log entries after each phase, not streams of empty status narration. Major irreversible actions and unresolved auth/financial conditions are surfaced honestly. No new paid expenses without approval. The session may perform every reversible legitimate step without asking routine questions.

---

# 12. Exact final reporting template — use this, fill with real evidence

Create `research_completion/assessment/PUBLICATION_VERDICT.md` containing:

```markdown
# R01 — Scientific Publication Verdict
Analysis date (UTC): <actual>
Commit at evaluation: <full SHA>
Latest source vintage / SHA256: <actual>
Scientific article type: <full original / measurement methods / conditional / no-go>
FINAL DECISION: <GO_FULL_ORIGINAL_RESEARCH_DRAFT | GO_METHODS_OR_MEASUREMENT_DRAFT | CONDITIONAL_MORE_EVIDENCE | NO_GO_ORIGINAL_RESEARCH>

## One-paragraph answer
<precisely what has and has not been demonstrated; do not claim journal acceptance>

## Main scientific contribution versus closest published and preprint studies
<explicit comparisons and access depth>

## Provenance, cohort and missingness
<dates, rows, quotes, services, corridors, waves, linkage bounds>

## Information timing
<proven release dates/lead days or why forecasting claim fails>

## Model evaluation and uncertainty
<complete model ranking, selected model or none, Brier/logloss/calibration, paired CI,
 independent holdout status, yearly/region consistency, negative findings>

## Operational interpretation
<review-at-capacity scenario, assumptions and unmeasured costs>

## The 12 science gates
| Gate | PASS / FAIL / UNRESOLVED | Supporting artifact | Why |
...

## Publishability blockers
<ordered fatal/major/minor with bounded resolution routes>

## All work actually executed
<commands, output paths, tests, hashes, failures; no fabricated completions>

## Handoff and GitHub
<verified main commit, clean source tree, PR(s), README and exact ZIP download URL/path>

## What the investigator must personally verify
<authorship, citations, licences, manuscript accuracy, target venue,
 ethical/institutional review if applicable, journal submission choice>
```

Also create `research_completion/assessment/final_execution_report.md` with a compact, honest *done / partial / blocked / not attempted* status for P0–P10 and evidence links. This report is separate from the scientific manuscript. Every key number in `PUBLICATION_VERDICT.md` must point to a table/figure/code/source and be automatically consistency-checked.

# 13. Immediate first actions for Codex (copy/paste run block)

1. **Read this entire directive**, then inspect cloned repository; run `git status`, verify remote `Isaac25-lgtm/remittance-price-intelligence`, current `main`, branch and file inventory.
2. Read `README.md`, `AGENTS.md`, `CLAUDE.md`, `docs/SCIENTIFIC_PROTOCOL.md`, `docs/STATUS.md`, `docs/PRIOR_ART.md`, `docs/REPRODUCIBILITY.md`, `docs/DEPLOYMENT.md`, `configs/experiment.yaml`, and actual pipeline/tests. Resolve operational conflict: this directive governs the new work, frozen prior experiments are not rewritten.
3. Confirm **REMOTE** compute availability; do not fit a 200k-quote model on the investigator's laptop. Verify data source and exact hash or catalogue source vintage. Record whether source files must be reacquired.
4. Create `research/r01-publication-completion-2026-10-19` and a checkpoint/inventory. Preserve initial scientific metrics as frozen legacy evidence.
5. Start the **closest-publication full-text audit and historic release-time investigation immediately**; these are possible fatal gates and take priority over additional hyperparameter tuning.
6. Execute all valid analyses, fixing bugs and writing tests. Compare source-to-result reproductions against prior. Record actual results and uncertainty; if a gate fails, pivot appropriately without faking it.
7. Determine the scientifically justified article scope and verdict. If GO, draft the complete manuscript and supplements. If not, provide complete conditional research report and precise remaining blockers. Do not stop after a successful CI run.
8. Build all credible figures, tables, reports, README updates and the public-safe ZIP. Run consistency, integrity, scientific-claim and licence checks.
9. Push branch, PR, green CI, merge authorised safe outputs to **main**, confirm final commit and files exist, and return an actual working download retrieval route.
10. Final reply to investigator MUST say: **“PUBLISHABLE AS A DRAFT FOR INVESTIGATOR REVIEW”** only if the gates truly pass, or **“NOT YET PUBLICATION-READY”** with the reasons. Neither phrase is a claim of journal acceptance or approval to submit without investigator review.

**END OF DIRECTIVE. The assignment is to carry out the complete scientifically legitimate analysis and publication-readiness work, not to optimise for a favourable verdict.**
