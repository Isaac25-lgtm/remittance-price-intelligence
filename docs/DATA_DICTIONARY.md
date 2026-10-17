# Data dictionary (observed after audit of sha256 f1d7265b…)

Source sheet: `Dataset (from Q2 2016)`, 204,469 rows, 42 named columns. There are also 5 unnamed helper columns, populated only on 2025Q3 rows (year and ISO3+year keys); they are ignored. Definitions below follow the workbook's `Legend` sheet.

| Column | Type / units | Notes from audit |
|---|---|---|
| id | integer | unique (0 duplicates) |
| period | `YYYY_QQ` | 37 quarters 2016Q2–2025Q3; **2025Q2 absent**; parsed to `qidx = 4*year + q - 1` |
| source_* / destination_* | ISO3, name, WB region, income, lending, G8/G20 | Kosovo is `KSV` in the code fields but `XKX` in `corridor` (95 rows) |
| firm | text | 713 raw → 699 normalised names; 14 normalised names have multiple raw spellings |
| firm_type | text | provider category; treated as an attribute, not identity |
| payment instrument, access point, pickup method, pickup location | text | core identity |
| speed actual | text | strict attribute |
| receiving network coverage | text | strict attribute |
| cc1 / cc2 denomination amount | USD | constant 200 / 500 (basket identifier) |
| cc1 / cc2 lcu amount, lcu fee, lcu fx rate | sending local currency | |
| cc1 / cc2 fx margin | percent | negative values in 9,169 cc1 rows |
| cc1 / cc2 total cost % | percent of amount sent | = 100·fee/amount + FX margin (median abs diff 0.002); cc1: 18 missing, 1,308 negative, 1,155 zero, 293 > 50% |
| inter lcu bank fx | rate | interbank reference |
| transparent | yes/no | non-transparent providers did not disclose the FX rate |
| Standard Note, note2 | text | not used |
| date | collection day | text `dd/Mon/yyyy`, or an Excel datetime for 2025Q3; 181 rows labelled 2021Q3 were collected in May–June 2021 |
| corridor | text | concatenated codes; not used as a key |

Derived (`src/rpi/linkage.py`, `features.py`): `key`, `status`, `cost_next`, `strict_reobserved`, `fee_pct`, history rates `h_*`, `reob_corr`, corridor cross-section features, and `lag_cost`. Coverage, missingness and anomaly tables are in `results/tables/audit_*`.
