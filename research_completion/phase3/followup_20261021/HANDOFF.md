# Remittance AI: bounded external-evidence handoff

> **Superseded execution instructions:** the investigator withdrew availability for manual reviews. The [completed autonomous handoff](autonomous_review/HANDOFF.md) and [final decision](autonomous_review/FINAL_PUBLICATION_DECISION.md) are current. All 60 machine documentary assessments remain unresolved; no human validation. The manual-review requests below are a historical snapshot, not current instructions. The earlier ZIP remains immutable.

**21 October 2026. Verdict: CONDITIONAL_HOLD.** Continue the completed Phase 3 investigation; do not restart or refit the model searches. [Current evidence-based verdict](PUBLICATION_VERDICT.md).

## What advanced

1. **Lim full text obtained and reviewed.** The complete author v1.1 manuscript, code and reported results are publicly available in the author's replication repository. The exact next-quarter continuity/unknown-successor/core-strict contrast was not found in that version. This resolves the prior access blocker for a specified version, not all originality questions. [Head-to-head review and hashes](LIM_OVERLAP_REVIEW.md).
2. **Historical classification change verified.** Official reports document changes in Q2 2021 and Q4 2022. Their timing aligns with Q1 2021 and Q3 2022 origin transitions. The cause of each broken link remains unverified. [Source passages and interpretation](SURVEY_CHANGE_REVIEW.md).
3. **Review criticisms reconciled against counts.** The changed-attribute cohort is 12.92% of all eligible origins or 16.08% of valid core pairs. Its pooled continuity is similar to unchanged pairs, but that does not establish independence or identity. All 36 origin waves are preserved. [Scientific response](CRITIQUE_RECONCILIATION.md), [wave decomposition](attribute_change_by_wave.csv), [pooled decomposition](attribute_change_pooled.csv).
4. **Your review is ready.** All 60 blinded cases are preserved. You volunteered to review them; two separate blank reviewer forms and an offline casebook are prepared. CSV export, local autosave and JSON checkpoint restore were exercised in a real browser, and synthetic test state was cleared. **Completed human adjudications remain zero.** [Instructions](REVIEWER_INSTRUCTIONS.md).

## Your next action

Extract `REMITTANCE_R01_IDENTITY_REVIEW_LOCAL_ONLY_20261021.zip` from Downloads. Read its `START_HERE.md`, then open `Reviewer_A/REVIEWER.html`. Review in batches, record historical documents and effective periods, and download both decisions CSV and checkpoint JSON. Preserve UNRESOLVED when evidence is insufficient. If possible, give the separate blank Reviewer_B folder to a colleague without your judgments. Do not open the original stratum key or outcome prices before sealing decisions.

Save returned decisions under local ignored `research_completion/phase3/private_runtime/followup_20261021/returned_reviews/` or retain the downloaded CSV for the next session. A single investigator review must be described as author assessment; no independent expert validation is assumed. Automated checks validate form completeness only.

After review, inspect source quality, unresolved/disagreement patterns and whether the measurement insight is substantial. A fully evidenced finding may justify developing a short measurement manuscript. If comparable services cannot be defended or only an established lesson remains, record NO_GO for the original-article route while retaining the reproducible work. No submission or positive novelty decision is implied.

## Deliveries and provenance

- Public consolidated ZIP: `deliverables/REMITTANCE_R01_PHASE3_FOLLOWUP_HANDOFF_20261021.zip`, with a matching Downloads copy. It combines the previous safe scientific payload with the follow-up/current presentation files and embeds the previous immutable Phase 3 ZIP. The root `SHA256SUMS.txt` validates this consolidated package; historical Phase 3 manifests describe the older embedded archive.
- Local reviewer ZIP: under the ignored private follow-up directory and Downloads only. It contains case rows and must remain off GitHub and out of the public package. It excludes prices, stratum key, AI decisions and reading-copy manuscripts/PDFs.
- Standalone copy of this handoff: Downloads `REMITTANCE_R01_PHASE3_FOLLOWUP_HANDOFF_20261021.md`.
- Existing archive unchanged: `../deliverables/REMITTANCE_R01_PHASE3_PUBLICATION_HANDOFF_20261021_34ba4ca.zip`, SHA256 `a01def0d701aae0b7f19a89d5ebbf28f7b2b683b2d33eb4ae629d5ba59b5665c`.
- Baseline `8f29279ae4208a88581c9609a4b91fae544c0141`; scientific follow-up and packaging commits recorded in Git and new package verification. Existing research tables, results, source data, reproduction failures and original archive are preserved. Source acquisitions are hashed in [source_acquisition.csv](source_acquisition.csv); browser-only checks in [web_source_checks.csv](web_source_checks.csv).

## Resume without restarting

From the repository root in Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe research_completion/phase3/followup_20261021/evidence_followup.py aggregate
.\.venv\Scripts\python.exe research_completion/phase3/followup_20261021/evidence_followup.py validate_review --decisions "PATH_TO_RETURNED_CSV"
.\.venv\Scripts\python.exe -m pytest -q tests research_completion/phase3/code/test_science.py research_completion/phase3/followup_20261021/test_followup.py
```

The acquisition command reuses verified cached sources and preserves failed requests rather than retrying denied access. `prepare_review` preserves existing reviewer files and never reads the stratum key. Do not repackage the old immutable handoff or treat prior inspected periods as new validation.
