> Current local completion: **CONDITIONAL_MORE_EVIDENCE / NOT YET PUBLICATION-READY**. The analyses, pilot recovery, calibration, transfers and dependence sensitivities have been executed. See [the scientific verdict](../research_completion/assessment/PUBLICATION_VERDICT.md) and [conditional report](../research_completion/manuscript/conditional_research_report.md). The text below preserves the 17 October phase-1 history; references to future work or unavailable local inputs there are historical.

# Prior art / competitor audit (targeted, phase 1 final checkpoint, 17 Oct 2026)

**Scope.** This is a bounded audit (~5 minutes), not a systematic review.

**Metadata.** Titles, authors, DOIs and venues were verified against Crossref (`api.crossref.org/works/<DOI>`).

**Abstracts.** These were read at, or as close as possible to, the publisher or institutional repository. Abstracts that could not be read are marked.

**Depth labels:** `FULL_TEXT`, `ABSTRACT`, `REPOSITORY`, `CATALOGUE_ONLY`, `UNVERIFIED`. No full texts were read, so every overlap judgement below rests on abstracts or metadata only.

## Matrix

| # | Work (verified metadata) | Depth | Data / unit / period (as stated) | Question & method (as stated) | Overlap with R01 |
|---|---|---|---|---|---|
| 1 | Beck, T., Martínez Pería, M. S. (2011). *What Explains the Price of Remittances? An Examination Across 119 Country Corridors.* **World Bank Economic Review** 25(1):105–131. DOI [10.1093/wber/lhr017](https://doi.org/10.1093/wber/lhr017). Working-paper version: [10.1596/13466](https://doi.org/10.1596/13466) and Policy Research WP [10.1596/1813-9450-5072](https://doi.org/10.1596/1813-9450-5072) (2009). | ABSTRACT (World Bank Open Knowledge Repository record, hdl 10986/13467) | "Newly gathered data across 119 country pairs or corridors"; average prices by provider type | Cross-sectional determinants of remittance prices: migrants, competition, bank access, regulation; Western Union less price-sensitive | **Same question family** (price determinants) and the World Bank price-survey lineage. **No** next-quarter continuity, service-level linkage, missing-outcome bounds or predictive validation. |
| 2 | Beck, T., Janfils, M., Kpodar, K. *What Explains Remittance Fees? Panel Evidence.* IMF Working Paper 2022/063. DOI [10.5089/9798400205439.001.a001](https://doi.org/10.5089/9798400205439.001.a001) | ABSTRACT (via RePEc/IDEAS `imf/imfwpa/2022-063`; IMF eLibrary returned 403) | "data across 365 corridors"; time and country variation over "the past decade" | Panel associations of fees with cost/risk constraints and market structure; notes the 3% goal "has not been met yet in many corridors" | **Closest same-dataset competitor** (365 corridors matches RPW scale; the abstract does not name the dataset). Corridor-level explanatory panel, not service-level continuity prediction. |
| 3 | Gurira, P. *The valuation effects of remittance cost transparency on international money transfer providers.* **International Journal of Emerging Markets** 21(6):1679–1699 (online 14 Oct 2025; issue 2026). DOI [10.1108/IJOEM-04-2024-0691](https://doi.org/10.1108/IJOEM-04-2024-0691). SSRN preprint [10.2139/ssrn.4733674](https://doi.org/10.2139/ssrn.4733674) (2024). | ABSTRACT (Emerald page) | Firms identified in the RPW comparison tool: 3 listed MTOs + 48 banks/financial firms; event window not stated in the abstract | Event study of the RPW tool's effect on provider stock valuations | Uses **RPW as an intervention**, not as a quote panel. Different outcome; no overlap with continuity prediction. |
| 4 | Endo, I., Namaaji, J., Kulathunga, A. (2010). *Uganda's Remittance Corridors from United Kingdom, United States and South Africa.* World Bank Working Papers. DOI [10.1596/978-0-8213-8430-5](https://doi.org/10.1596/978-0-8213-8430-5) | CATALOGUE_ONLY (Crossref metadata) | Uganda receiving corridors (UK, US, South Africa); details unread | Corridor study (content not verified) | **Geographic competitor for the Uganda subgroup.** Our data supports only 3 receiving-Uganda corridors and no sending-Uganda corridors, so this work is not superseded. |
| 5 | World Bank Group (2018). *The Market for Remittance Services in Southern Africa.* DOI [10.1596/30473](https://doi.org/10.1596/30473), hdl 10986/30473 | ABSTRACT (OKR record) | SADC remittance market | Descriptive / policy market study; costs to and within SADC "significantly higher than other regions" | Regional descriptive context for the Sub-Saharan Africa subgroup. Not predictive. |
| 6 | Viceisza, A., Xu, D. *Price dispersion in the remittance industry: The role of fintech, comparison shopping, and other factors.* AEA RCT Registry AEARCTR-0006475, DOI [10.1257/rct.6475](https://doi.org/10.1257/rct.6475), registered 3 Mar 2021 | REPOSITORY (registry page; status "In development"; pre-analysis plan not read) | "existing data" in stage 1, then primary data; sources not named on the page | Whether comparison shopping/websites affect remittance demand and supply; welfare stage | Conceptual neighbour (price dispersion and comparison). Causal/experimental, not quote-continuity prediction. Results unknown. |
| 7 | World Bank, *Remittance Prices Worldwide* quarterly reports (e.g. `rpw_main_report_and_annex_q224.pdf` on remittanceprices.worldbank.org) | UNVERIFIED (seen only in a search-engine index; the site returned a 403 bot challenge to this session) | The RPW survey itself | Official corridor/global averages and SmaRT indicator | Official aggregate monitoring from the same source. Must be read before any novelty claim. |

## Head-to-head competitors (required by AGENTS.md M)

1. **Same data/source:** Beck, Janfils & Kpodar (IMF WP 2022/063), with Beck & Martínez Pería (WBER 2011) as its predecessor.
   - **They establish:** corridor-level *associations* of average fees with market structure, costs and risk.
   - **R01 would add:** a different estimand. Service-level, exactly-adjacent-quarter persistence of ≤3% quotes, explicit identity definitions (core vs strict), missing-outcome bounds, and time-forward predictive validation against strong history baselines.
   - **Falsification:** R01 adds nothing material if well-specified logistic models with corridor history match the tree ensembles. Phase 1 shows the gap is small: 0.0026–0.0035 Brier, with a provider-clustered CI touching zero in 2022–24. R01 also adds nothing if the bounds are too wide to say anything beyond the corridor averages.
2. **Same question elsewhere (conceptual):** no peer-reviewed or preprinted study of *service-level quote continuity or threshold persistence with predictive validation* was found in these targeted Crossref queries:
   - "remittance prices machine learning prediction" (only non-remittance results);
   - "remittance cost persistence digital providers";
   - "price dispersion remittance market competition Africa";
   - "remittance service providers prices panel";
   - "cost of remittances corridor determinants competition".

   **This is not proof of absence.** Google Scholar, SSRN full-text, RePEc full search, theses and GitHub were not searched. The nearest conceptual work found is the Viceisza & Xu registry entry (#6), which is causal and unfinished.

## Novelty implications (provisional)

- **Defensible gap (pending a fuller search):**
  - a measurement contribution: how identity rules and non-reobservation change estimates of whether a low-cost surveyed service stays low-cost;
  - an honest benchmark showing that simple cost/history rules are clearly beaten while tree-model gains over logistic models are small.
- **Not defensible:**
  - "first ML model of remittance prices" (unverified, and model substitution alone is not novelty under gate 3);
  - any operational forecasting claim (release dates unverified);
  - any Uganda-specific advance.
- **Next steps:**
  - read #1–#2 and #7 in full text;
  - run Scholar/SSRN/GitHub searches for RPW service-level panels;
  - check whether the World Bank publishes wave-level persistence statistics.
