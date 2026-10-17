# Data access log (phase 1, 17 Oct 2026)

| # | Route | Result | Attempts |
|---|---|---|---|
| 1 | `datacatalogapi.worldbank.org/ddhxext/DatasetView?dataset_unique_id=0037898` | HTTP 429 rate-limited | 3, spaced; stopped |
| 2 | `remittanceprices.worldbank.org/data-download` (curl and WebFetch) | HTTP 403 Cloudflare challenge | 1 each; stopped, no bypass |
| 3 | `ddh-openapi.worldbank.org/dataset/view?...` | HTTP 404 | 1 |
| 4 | `datacatalogfiles.worldbank.org/ddh-published/0037898/DR0095523/rpw_dataset_2011_2025_q3.xlsx` | **HTTP 200**, 50,780,339 bytes | 1 |

Route 4 is the catalogue's own "Complete Dataset" link. The investigator's coordinator relayed it after reading the official catalogue page. It is the official file host, not a mirror.

**Genuinely fetched:** the workbook above. **Catalogued only (not fetched):** the catalogue metadata (48.4 MB, updated 23 Sep 2026; the blob header says Last-Modified 28 Sep 2026), the methodology web page, and any historical release archive.

**Not available:** publication/release dates of each quarterly RPW wave.
