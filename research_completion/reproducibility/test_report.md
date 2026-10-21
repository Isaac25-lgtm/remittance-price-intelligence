# Actual software / integrity test report

Evidence type: SYNTHETIC UNIT TEST AND PUBLIC AGGREGATE INTEGRITY / STREAMLIT APPTEST.
Full local suite: **139 passed, 1 skipped, 0 failures/errors**. Executed 2026-10-20T21:54:46.828010+00:00 to 2026-10-20T21:56:19.865741+00:00; exit 0; peak logged RSS 247.5 MB. Python3.12 / Streamlit1.66 / Altair6.3. Exact command and fingerprints: commands_executed.jsonl. The original source/cohort real-data reproduction is separate.

The pre-package ZIP test was skipped until assembly; post-build verification is recorded separately. A dateutil utcfromtimestamp deprecation warning is unrelated to scientific results. The full suite exercises every dashboard section/control and aggregate download, source/quarter/identity/leakage guards, fold transformers with unseen covariates/outcome columns, calibration limits, bootstrap structures, decomposition and file safety. Tests do not rerun large model fits or download raw data.

Initial baseline dependency failures, one bootstrap test correction, the strict legacy numeric comparison failure, final fee-column reporting failure and all-NaN ablation histogram failure remain in the command history. Corrected/resumed stages passed; model checkpoints were preserved. Strict legacy numerical reproduction itself remains failed (14 exact /2 timing-only /14 different); software test success does not erase that scientific limitation.

Additional final supplement tests and ZIP verification are logged separately after this full run. GitHub Python3.11 CI outcome is recorded in deliverables/git_and_download_links.md. The hosted browser inventory was empty and web reader failed, so deployed new pages were not verified. No assertion of public redeployment follows from local tests or a commit.

Scientific interpretation: all pre-existing periods were inspected, public predictor release clocks are not verified, novelty/true identity remain unresolved, and joint inference undercovered the stress simulation. **NOT YET PUBLICATION-READY.**

Post-build archive safety/integrity suite:5 passed, no skips, on the assembled archive (command stage postbuild_archive_tests). Scientific source GitHub CI passed140 tests with1 pre-package skip on Python3.11; see github_science_ci.json. The immutable ZIP is audited again after metadata finalization; later integration/verification records live beside it.
