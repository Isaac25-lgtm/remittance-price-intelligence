# Data access and publication boundary

| Item | Status |
|---|---|
| Source | World Bank Remittance Prices Worldwide, complete dataset (catalogue 0037898, resource DR0095523) |
| URL fetched | https://datacatalogfiles.worldbank.org/ddh-published/0037898/DR0095523/rpw_dataset_2011_2025_q3.xlsx |
| Fetched | 2026-10-17T18:56:49Z, HTTP 200, single attempt; blob Last-Modified 2026-09-28 |
| Bytes / sha256 | 50,780,339 / f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8 |
| Licence | Catalogue: CC BY 4.0. Workbook terms: attribution required; World Bank "restricted data" list referenced |
| Stored | `data/raw/` and `data/processed/` locally only (gitignored); never committed |

Run `python -m rpi.acquire` to fetch and verify. Only aggregate tables and figures (`results/`) and explicitly synthetic test fixtures (`tests/conftest.py`) are public. `data/samples/` is intentionally empty: tests build synthetic rows in code. Failed routes are logged in `results/source_manifest.json`.
