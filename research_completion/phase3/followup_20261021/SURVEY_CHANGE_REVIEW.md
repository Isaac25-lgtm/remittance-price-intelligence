# Official classification changes and the observed discontinuity

## Documentary finding

The [World Bank June 2021 RPW report](https://remittanceprices.worldbank.org/sites/default/files/rpw_main_report_and_annex_q221.pdf), **printed page 5, Changes in Q2 2021**, documents splitting previously combined payment/access arrangements when different combinations had different prices. It reports more products per corridor after classification, especially among digital services. This is explicit historical source evidence, not a conjecture from our graph. The full relevant page and footnote were read and the academic-mirror page was rendered and visually inspected.

Local ordinary requests to the World Bank endpoints returned 403 and were not retried. The same World Bank-authored report was available through the browser source reader; an [academic teaching copy](https://courseapps.studyonline.unsw.edu.au/media/unsw/course/ZZBU8508/pdfs/WorldBank_Remittance_Prices_Worldwide-main_report_and_annex_q221.pdf) downloaded lawfully (2,195,426 bytes; SHA256 `b7cb3380f88273211dda29477f2517c559935aad149b7d39b2e4ddef71d8d83d`). The report's authorship, issue and page content agree with the official parsed source. Identical bytes to the denied official download were not verified. Reading copies/render remain private.

The [December 2022 RPW report](https://remittanceprices.worldbank.org/sites/default/files/rpw_main_report_and_annex_q422_final.pdf), **printed page 4, Changes in Q4 2022**, documents recording payment/access combinations separately more generally. It explains that previously equivalent price/speed combinations could change between quarters. This further classification change is already public prior information. The same page separately documents Azimo's closure and survey treatment of Russia; those are distinct mechanisms, not a universal explanation for nonobservation. This source was browser-parsed; no complete local byte copy/hash was obtained.

## Correct time alignment

An origin labeled **2021Q1** links to **2021Q2**, when the first documented change applied. Likewise an origin labeled **2022Q3** links to the Q4 2022 classification change. A change in a target wave can therefore appear in our plot at the preceding origin quarter. Describing the first break as a documented Q1 2021 policy change would be incorrect.

From existing, independently reproduced Phase 3 aggregates:

| Origin -> target | Eligible origins | Core valid | Strict valid | Core unknown share | Strict unknown share | Extra width |
|---|---:|---:|---:|---:|---:|---:|
| 2020Q4 -> 2021Q1 | 1,166 | 965 | 952 | 17.24% | 18.35% | 1.11 pp |
| 2021Q1 -> 2021Q2 | 1,247 | 517 | 244 | 58.54% | 80.43% | 21.89 pp |
| 2021Q2 -> 2021Q3 | 1,408 | 865 | 584 | 38.57% | 58.52% | 19.96 pp |
| 2022Q3 -> 2022Q4 | 1,481 | 763 | 554 | 48.48% | 62.59% | 14.11 pp |
| 2022Q4 -> 2023Q1 | 1,848 | 1,682 | 1,353 | 8.98% | 26.79% | 17.80 pp |

`attribute_change_by_wave.csv` preserves all 36 eligible origin waves, not only these illustrative boundaries. Values are exploratory descriptive reconstructions from existing public counts; no data were refitted or new source outcomes loaded. Eligible cheap-origin counts here are not total quote volumes. Existing source-date/quarter anomalies remain documented; nominal wave labels do not establish actual release times.

## Scientific consequence

There is a documented recording change aligned with the first discontinuity. It supplies a plausible measurement mechanism and strengthens the case for caution about longitudinal links. It does **not** identify how many of our broken core keys or changed speed/network attributes were caused by classification, and it does not prove stable economic identity for the reclassified cases. Multiple instruments/access categories are part of the core key, whereas strict additionally restricts speed/network; their mechanisms cannot be conflated.

We cannot infer a causal fraction, treat all discontinuity as market behaviour, or claim that this study discovered the survey change. Nor should we arbitrarily delete boundary quarters to improve the headline. Retain full-wave results, label the institutional explanation and require case-level historical evidence where comparable-product claims are made. The publication route remains conditional.
