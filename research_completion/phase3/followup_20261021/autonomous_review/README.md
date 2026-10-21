# Autonomous historical-evidence review: completed

**21 October 2026. `CONDITIONAL_HOLD_EXTERNAL_VALIDATION`. Recommendation: do not submit the original article now.** [Final decision](FINAL_PUBLICATION_DECISION.md), [handoff](HANDOFF.md), [conditional research dossier](conditional_research_dossier.md).

All 60 blinded cases were investigated through shared provider/corridor searches, actual source requests and AI documentary assessment, followed by adversarial software checks. Every case remains `UNRESOLVED_INSUFFICIENT_HISTORICAL_EVIDENCE`. Support grades: **A 0, B 2, C 47, D 11**. These are documentation findings from a deliberate stratified sample, not matching accuracy. Human adjudications: **0**. This completes the bounded autonomous investigation; it does not establish economic-product identity or require the investigator to complete a case form.

The original 45,343 cheap USD200 origins, 36,429 valid core pairs, 30,570 valid strict pairs and adverse model findings are preserved. New source-era, funding, payout, region/provider-type and weighting analyses reproduce the existing counts. No classifier was fitted and no outcome was replaced by an AI label.

## Read the evidence

- [Frozen methods](EVIDENCE_METHODS.md) and [actual feasibility/limitations](REVIEW_FEASIBILITY.md).
- [Anonymous stratum cross-tab](AUTOMATED_FINDINGS_AGGREGATED.csv), [aggregate source scope](SOURCE_SCOPE_SUMMARY.csv), [freeze hashes](freeze_integrity_summary.json).
- [Identity sensitivity and interpretation](IDENTITY_SENSITIVITY.md), [paired group decomposition](PAIRED_GROUP_DECOMPOSITION.csv), [complete group support](GROUP_SUPPORT.csv), [measurement groups](MEASUREMENT_GROUP_SENSITIVITIES.csv), [weighting support](WEIGHTING_SUPPORT.csv), [illustrative assumed errors](ILLUSTRATIVE_LINKAGE_SENSITIVITY.csv).
- [Novelty assessment](NOVELTY_AND_CONTRIBUTION.md), [independent code-path audit](COMPLETION_AUDIT.json), [requirements audit](PUBLICATION_READINESS_AUDIT.md), [execution log](RUN_LOG.md).
- Scientific figures: [documentary support](figures/documentary_support.png), [source-era widening](figures/source_era_width.png); vector PDF exports accompany them.

## Reproduce without restarting the project

Use the existing Windows environment, two library threads and one analysis process. `review.py freeze` intentionally refuses to overwrite the sealed record. Its source/decision stages need ignored local files, which are supplied only in the private package. Do not rerun the old casebook-generation or model-search entry points.

```powershell
$env:OMP_NUM_THREADS='2'; $env:OPENBLAS_NUM_THREADS='2'
$env:MKL_NUM_THREADS='2'; $env:NUMEXPR_NUM_THREADS='2'
.\.venv\Scripts\python.exe research_completion/phase3/followup_20261021/autonomous_review/audit_completion.py --private
# Optional: recompute the same post-freeze aggregates from the verified existing cache
.\.venv\Scripts\python.exe research_completion/phase3/followup_20261021/autonomous_review/sensitivity.py
.\.venv\Scripts\python.exe -m pytest -q tests research_completion/phase3/code/test_science.py research_completion/phase3/followup_20261021/test_followup.py research_completion/phase3/followup_20261021/autonomous_review/test_autonomous.py
```

Public CI uses synthetic fixtures and public aggregates; it cannot reproduce the private historical source investigation or full workbook/model analysis. `audit_completion.py` independently recomputes arithmetic from outputs without importing the linkage/model implementation. It is not an independent human scientist.

Observed Windows/Python and package versions are in [environment.json](environment.json). Historical source extraction additionally needs `pypdf` and `beautifulsoup4`; PDF visual inspection used PyMuPDF. These optional reading dependencies are not needed by aggregate-only CI.

Private source/case associations, alternatives, transcripts, reading copies and all 60 sealed assessments remain in ignored `research_completion/phase3/private_runtime/followup_20261021/autonomous_review/`. Prior archives remain immutable. The new public package consolidates the prior safe payload plus this extension; the separate private ZIP is local only. See [handoff](HANDOFF.md) for names and verification records.
