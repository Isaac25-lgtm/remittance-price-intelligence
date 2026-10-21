# Git integration and downloadable handoff

Scientific source **merged into main** through [PR 3](https://github.com/Isaac25-lgtm/remittance-price-intelligence/pull/3). Starting main was `d4ccbf91c3adac56418f60ad63afc9e85a07ca82`; verified scientific integration commit is **`ae7c977d87c7cf03d54f3e499ba3ef25beffbe5c`**, fetched and fast-forwarded locally on 21 October 2026 (Africa/Kampala).

Reviewed source head: `c9f8e5063785ff3afd31cba100dcbbbff0a1d71f`. [GitHub CI run39532272698](https://github.com/Isaac25-lgtm/remittance-price-intelligence/actions/runs/39532272698), Python3.11, completed **SUCCESS**:140 passed,1 pre-package ZIP skip. Local full suite:139 passed,1 pre-package skip; the subsequent newline/package regression adds another passing test. These are software/integrity tests, not scientific gate passes.

**One-file handoff:** [download the ZIP](https://raw.githubusercontent.com/Isaac25-lgtm/remittance-price-intelligence/main/research_completion/deliverables/REMITTANCE_R01_PUBLICATION_HANDOFF_20261021_ae7c977.zip). Local relative path: `research_completion/deliverables/REMITTANCE_R01_PUBLICATION_HANDOFF_20261021_ae7c977.zip`.

The ZIP is an immutable snapshot of the integrated scientific source plus the reviewed packaging/verification metadata. Its source commit is the scientific integration above; its input tree records metadata changes as dirty rather than claiming an identical clean checkout. Every archive member has a SHA256 manifest; the ZIP's own hash and open/member safety checks are in [zip_verification.json](zip_verification.json) beside the archive. UTF8 text is canonicalised to LF for Windows/Linux consistency. Rebuild with `python scripts/build_publication_handoff.py`; verify with its `--audit <ZIP>` option.

The final packaging commit/CI is a subsequent integration checkpoint; the live file history and final investigator response identify that integration. This snapshot records the already-verified scientific main commit, avoiding a self-referential claim about its own future packaging merge. No formal release or DOI was minted.

The assembled archive passed all5 local package-safety/integrity tests with no skips. Final member hashes, repeat-build determinism and the downloadable GitHub bytes are checked after this metadata is frozen. The latest exact verification record lives beside the immutable ZIP.

Hosted dashboard: https://isaac-remittance-research.streamlit.app/ . Local aggregate-only AppTest passes. The browser inventory returned no available browsers, and the web reader could not access this URL on 20 October UTC /21 October Kampala. Actual hosted redeployment of the new completion section is **UNVERIFIED**; a source commit is not proof of redeployment.

Raw/row files, provider quote records, private caches, predictions, fitted binaries, source literature PDFs and credentials are excluded. No journal submission or preprint posting was performed.
