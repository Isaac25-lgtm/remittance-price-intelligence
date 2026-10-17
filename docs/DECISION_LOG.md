# Decision log

| Date (UTC) | Decision | Reason |
|---|---|---|
| 2026-10-17 18:56 | Use the `datacatalogfiles` official file; stop retrying the catalogue API (429) and the RPW site (403 challenge) | Contract caps attempts per host; challenge pages are not bypassed |
| 2026-10-17 19:00 | Analyse the post-Q2-2016 sheet only | The pre-2016 sheet has a different identity schema (`product`, `sending location`) |
| 2026-10-17 19:03 | Ignore 5 unnamed columns on 2025Q3 rows | Audited as helper lookup keys (year and ISO3+year), not measurements |
| 2026-10-17 19:04 | Freeze protocol (`configs/experiment.yaml`, commit ecc7c49) | Required before metrics |
| 2026-10-17 19:04 | Test years 2022–2025 with 2025 = 2025Q1 targets only | 2025Q2 is absent, so 2025Q3 has no adjacent origin |
| 2026-10-17 19:04 | Firm type treated as an attribute, not identity | Provider categorisation can be relabelled |
| 2026-10-17 19:10 | Corrected two wrong test expectations; production code unchanged | Primary rows include observed failures; a Q2 negative-cost firm's later quote is eligible |
| 2026-10-17 19:18 | Uganda subgroup model metrics withheld | Pre-set gate of ≥100 failures not met (20) |
| 2026-10-17 19:20 | Re-ran lag-0 at committed SHA 0de853b | The first run recorded a parent SHA because model code was uncommitted; results identical to ~1e-16 |
| 2026-10-17 | No model "selected" for deployment | No lead time is established; RF has the best Brier but is under-confident; GBM gains over logistic models are small and unstable by year |
| 2026-10-17 | Dashboard deferred | Phase-1 timebox spent on verified evidence |
| 2026-10-17 (final checkpoint) | Built local Streamlit dashboard on committed aggregates only; no deployment | Investigator authorised a bounded phase; there is no public-safety review for deployment |
| 2026-10-17 (final checkpoint) | Targeted prior-art matrix: Crossref metadata + abstracts; 7 works | Bounded; IMF eLibrary blocked (403), so the abstract was read via RePEc/IDEAS; the RPW site was blocked (403), so its reports are marked UNVERIFIED |
| 2026-10-17 (final checkpoint) | No model refits or data reruns | Investigator instruction; credit preservation |
| 2026-10-17 (final checkpoint) | Cancelled the autonomous PR check-in reminder | Investigator instruction |
