# Deployment readiness: R01 research dashboard

## Local completion update — 21 October 2026 (Kampala)

The local app adds a Publication completion section with verified aggregate model scores, all named ridge/spline references, joint dependence sensitivity, all-origin capacity bounds and publication gates. The CSV allowlist in dashboard/app.py maps seven additional filenames into research_completion/models or assessment; tests verify the exact committed download bytes and every section/control. No raw data, training, predictions, provider input or secrets at startup. Analysis date/cutoff and no-operational-model/confirmation notices remain visible. Local Python3.12 tests use Streamlit1.66 and Altair6.3; GitHub CI checks Python3.11.

Hosted new-page verification is **UNVERIFIED**: the browser tool has no browser and the web reader failed. This differs from the verified historical deployment below. See the [current integration ledger](../research_completion/deliverables/git_and_download_links.md) for actual CI/main/ZIP state. A commit does not prove hosted redeployment.

## Verified deployment — 17 October 2026

Live app: https://isaac-remittance-research.streamlit.app/ . Deployed by the coordinator from reviewed `main` after PR #2 merged (`7dd7281`), using Python 3.11 and no secrets. Browser verification confirmed the overview, retrospective context ribbon, World Bank attribution, all-eight-family model chart and aggregate download controls. CI at the reviewed head passed 96 tests. Source/row-level files were not uploaded. Scientific limitations remain unchanged.


**Status: TECHNICALLY READY. Licence for aggregate display: CLEARED (CC BY 4.0, sources below).** Nothing has been deployed from this session. Deployment and merge are handled by the investigator/coordinator after review.

## App
| Item | Value |
|---|---|
| Entry point | `dashboard/app.py` |
| Requirements | `dashboard/requirements.txt`: `streamlit==1.66.0`, `altair==6.3.0`, `pandas==3.0.6`, `numpy>=1.26,<3`, `pyarrow>=15,<27,!=25.0.0`. All support Python 3.11; numpy is a range because numpy 2.5.x requires Python ≥3.12. |
| Python | 3.11 (CI), 3.13 (tested in the cloud session) |
| Config | `.streamlit/config.toml`: headless, XSRF protection on, usage stats off, error details hidden, viewer toolbar, light accessible theme |
| Startup behaviour | Reads committed CSV/JSON aggregates only. **No training, no source download, no `data/raw` or `data/processed` access, no `rpi` package import** (enforced by `tests/test_results_integrity.py::test_app_reads_no_row_level_sources`). |
| Secrets | None required; there is no `secrets.toml`. |
| Tests | `pytest tests/test_dashboard.py tests/test_results_integrity.py`: AppTest covers every section, every selectbox option, every radio option, multiselects (including empty), and every download. Integrity checks run against the real committed files. |

## Licence audit (sources read 17 Oct 2026)
1. **World Bank Data Catalog page for dataset 0037898** — https://datacatalog.worldbank.org/search/dataset/0037898/remittance-prices-worldwide (read directly in this session):
   - "This dataset is licensed under Creative Commons Attribution 4.0".
   - Classified **Public** under the Access to Information Classification Policy.
   - "Complete Dataset" (`rpw_dataset_2011_2025_q3.xlsx`) last updated **23 Sep 2026**; metadata last updated 28 Sep 2026.
   - The catalogue lists no dataset-specific restriction.
2. **World Bank restricted-data page** — https://data.worldbank.org/restricted-data. This is where https://www.worldbank.org/terms-datasets-restricted now redirects; the coordinator resolved it.
   - The page states that restrictions, where applicable, are now recorded in each dataset's or indicator's metadata.
   - The old restricted-data page is legacy only.
   - The workbook's `go.worldbank.org/R6942GMMH0` shortlink points at that legacy list. The shortlink does not resolve from this environment, but a dead shortener is not itself a restriction.
3. **RPW data-download terms** — https://remittanceprices.worldbank.org/data-download (verified by the coordinator; this session received a 403 bot challenge there):
   - Copying, distributing, adapting and displaying the data are permitted.
   - Required attribution: *"The World Bank, Remittance Prices Worldwide, available at http://remittanceprices.worldbank.org"*.
   - No implied World Bank endorsement.
   - All of this is subject to restrictions recorded in the metadata, and the catalogue metadata (item 1) records none.
4. **Workbook "Terms of Use" sheet** (text extracted from the fetched file, sha256 `f1d7265b…`): the same attribution and no-endorsement terms. It references the legacy restricted-data list covered in item 2.
5. **World Bank Terms and Conditions** (amended 25 Jul 2025): Data Catalog datasets carry their own specific terms (item 1). Public representation of World Bank endorsement is prohibited.

## Licence decision
- **Aggregate derived statistics** (the allowlist below): **CLEARED** for public display under CC BY 4.0. This rests on items 1–3. Attribution and no-endorsement notices are required, and both are present in the app's context ribbon.
- **No residual HOLD from the legacy list.** Restrictions now live in dataset metadata, and RPW's metadata is Public / CC BY 4.0.
- **Still excluded regardless of licence:** raw workbook, quote/service rows, provider-level quote rows, row-level predictions and model binaries. They are never committed or deployed. This follows the project's publication boundary and the model card's exclusion of provider assessment, not a licence restriction.

## Safe public aggregate allowlist
The app may read or offer for download **only** these files. This is the `ALLOWLIST` in `dashboard/app.py`, and tests check it against what the app actually offers.

| Group | Files |
|---|---|
| Source audit | `audit_quarter_coverage.csv`, `audit_cost_anomalies.csv`, `audit_missingness.csv`, `record_flow.csv` |
| Linkage | `linkage_core_vs_strict_by_year.csv`, `linkage_core_only_attribute_changes.csv`, `linkage_status_by_origin_quarter.csv` |
| Estimands | `estimand_bounds_by_year.csv`, `estimand_bounds_by_year_5pct.csv`, `estimand_bounds_overall.csv`, `estimand3_corridor_level_by_year.csv` |
| Models (lag0/lag1) | `model_metrics_*`, `model_paired_diffs_*`, `model_capacity_*`, `model_capacity_diff_*`, `model_reliability_*`, `model_registry_*`, `reobservation_metrics_*` |
| Subgroups | `subgroup_support.csv`, `subgroup_model_metrics_lag0.csv` |
| Presentation aggregates | `presentation_model_brier_ci.csv`, `presentation_region_metrics_lag0.csv`, `presentation_corridor_metrics_lag0.csv` (ISO3 corridor pairs, gated n≥100 and ≥20 failures), `presentation_provider_distribution_lag0.csv` (anonymous quantiles only), `presentation_capacity_by_year_lag0.csv` |
| Reproduction | `results/reproduction/table_comparison.csv` |

**Excluded by design:**
- `data/raw/*`, `data/processed/*` (parquet caches, row-level predictions);
- any table with `source_row`, `id`, `firm`, `firm__n`, `key`, `provider`, `cost_next` or `y` columns (a test enforces this);
- provider names.

## Pre-deployment checklist (coordinator)
- [ ] Confirm the licence evidence above is still current (catalogue metadata Public / CC BY 4.0).
- [ ] `pip install -r dashboard/requirements.txt && pytest -q` is green.
- [ ] Deploy `dashboard/app.py` from a reviewed commit; the app needs no secrets.
- [ ] Open the live URL and verify the context ribbon, attribution and caveats before recording the URL anywhere.
