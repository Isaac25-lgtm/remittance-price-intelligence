# Verification record

**Local full suite: 236 passed in 321.29 seconds (5m21s), exit 0, 21 October 2026.** Command, with two library threads and PYTHONHASHSEED=0:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests research_completion/phase3/code/test_science.py research_completion/phase3/followup_20261021/test_followup.py research_completion/phase3/followup_20261021/autonomous_review/test_autonomous.py
```

The suite includes 36 autonomous-review tests plus the 200 existing tests. It exercises all dashboard sections/download allowlists, synthetic temporal/provider/corridor/uniqueness rejection cases, assumed-error allocation arithmetic, public denominator reconciliation, retained legacy classifications, reported documentation counts and public-package privacy rejection. The installed pytest-asyncio plugin emitted an unset fixture-loop-scope deprecation warning; it did not fail the suite. The test process used roughly 280–290MB working set in observed snapshots; no competing new analysis job was launched.

**Independent code-path audit: PASS**, public and local-private modes, recorded in COMPLETION_AUDIT.json. It verifies all 60 IDs/human fields, 185 case-source associations, sealed inputs/reading-copy hashes, 45,343-origin group totals, 5,859 newly unknown outcomes/4,770 stays, illustrative bound arithmetic, and all 30 original strict comparator classifications/52 field records. Primary post-freeze cache reconstruction also passed with the original raw SHA256 and 204,469 records. Neither test suite nor audit establishes external product truth or resolves the 14 differing legacy outputs.

**Publication integrity:** frozen evidence before key/cache access; public rows contain aggregate strata/groups only; original human fields unchanged. No new classifier fits, no raw workbook download, no original result replacement. Two scientific figures were exported as PNG/PDF and the PNGs visually inspected. Optional source-parser/environment versions are recorded in environment.json; CI does not require those reading dependencies.

**Public package dry run: PASS** for the explicit overlay; three historical archive hashes unchanged. Final member checksums/CRC, public/private separation and Downloads-copy digests are recorded by build_handoff.py in deliverable verification JSONs. Those exact archive checks occur after the source commit; they are not inferred from fixture tests.

GitHub CI is verified after the scientific checkpoint is pushed; its actual run URL/result will be added before sealing the public package. The final delivery also reports the final main commit's CI result. A Linux synthetic numerical fixture is not the 50MB real-data reproduction and cannot resolve historical numerical discrepancies.
