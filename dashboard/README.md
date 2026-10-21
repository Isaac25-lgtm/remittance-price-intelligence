# R01 research dashboard

A Streamlit + Plotly research dashboard (not a consumer service) for the R01 remittance quote continuity study.
Hosted at **https://isaac-remittance-research.streamlit.app/** (Streamlit Community Cloud, redeploys from `main`).

## Stack

| Layer | Choice |
|---|---|
| App framework | Streamlit 1.66 (`app.py`): navigation, widgets, cached aggregate reads, downloads |
| Charts | Plotly 6.3: interactive SVG/JS charts with hover tooltips, PNG export from the chart toolbar |
| Design layer | `ui.py`: design tokens (validated categorical palette), injected CSS, HTML hero, stat cards, callouts, gate rows |
| Data | Only the committed aggregate CSV/JSON files named in `ALLOWLIST` |

## Pages

1. **Overview**: hero, headline numbers, the core-vs-strict bounds chart and key findings
2. **Background & question**: SDG 10.c, the RPW survey, research questions, quote-flow Sankey, estimands E1–E4, identity rules
3. **Data & provenance**: source checksum, quotes per quarter (2025Q2 shown as absent), cheap-quote share, record flow, anomalies
4. **Linkage & identity**: reobservation by identity rule, core→strict reclassification Sankey, linkage status by quarter
5. **Continuity & bounds**: yearly bounds (3% / 5%), corridor-level E3 series
6. **Measurement audit (Phase 3)**: per-wave continuity and bounds for four products, paired width difference, group/period/weighting sensitivity
7. **Model comparison**: Phase 2 scores by family, joint corridor × provider × time sensitivity, Phase 1 cluster-bootstrap comparison, paired differences
8. **Time-forward & lag sensitivity**
9. **Calibration**: reliability curves for all non-constant families
10. **Review capacity**: corrected all-origin recall bounds; Phase 1 matched-sample queues kept for transparency
11. **Reobservation (negative result)**
12. **Geography & support**: regional continuity, support gates, African subgroups, gated region/corridor metrics, anonymous provider distribution
13. **Verdict & publication gates**: Phase 3 gate matrix, next steps, Phase 2 completion record
14. **Reproducibility & limits**

## Data rules

- The app reads only the files in `ALLOWLIST`: committed aggregates in `results/tables`, `results/reproduction/table_comparison.csv`,
  and the `research_completion` files mapped in `COMPLETION_FILES` (Phase 2 models/assessment and Phase 3 public tables),
  plus the source manifest, run metadata and dashboard notice.
- Every allowlisted table is downloadable byte-for-byte from a "Data behind this view" panel or a download button.
- No row-level quotes, services, provider names or predictions; no model training or source download at startup.
- Unsupported filters (provider names, sending-Uganda, per-year paired differences) are labelled as such.
- Bootstrap and HAC intervals are sensitivities, not held-out validation.

## Run

```bash
pip install -r dashboard/requirements.txt     # Python 3.11+
streamlit run dashboard/app.py
```

## Tests

`pytest tests/test_dashboard.py tests/test_results_integrity.py`. AppTest renders every page and exercises every
selectbox, radio, multiselect (including empty) and download; integrity checks run on the real committed tables
and confirm the app source never references raw or processed row-level data.
