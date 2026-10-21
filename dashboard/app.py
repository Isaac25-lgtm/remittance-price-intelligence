"""R01 research dashboard: World Bank RPW service-level quote continuity.

Reads ONLY committed aggregate files listed in ALLOWLIST (legacy results and COMPLETION_FILES),
plus fixed source/run/notice metadata. No row-level quotes, services, provider names or predictions; no
model training or source download at startup. Run: streamlit run dashboard/app.py
"""
from __future__ import annotations

import json
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
COMPLETION_FILES = {
    "model_comparison.csv": "models/model_comparison.csv",
    "joint_dependence_sensitivity.csv": "models/joint_dependence_sensitivity.csv",
    "all_origin_capacity_bounds.csv": "models/all_origin_capacity_bounds.csv",
    "sensitivity_grid.csv": "models/sensitivity_grid.csv",
    "publication_gates.csv": "assessment/publication_gates.csv",
    "recent_history_reference.csv": "models/recent_history_reference.csv",
    "conventional_reference_comparisons.csv": "models/conventional_reference_comparisons.csv",
}

# Every file the app may read or offer for download (aggregate, public-safe; see docs/DEPLOYMENT.md).
ALLOWLIST = {
    "audit_quarter_coverage.csv", "audit_cost_anomalies.csv", "audit_missingness.csv",
    "record_flow.csv", "linkage_core_vs_strict_by_year.csv", "linkage_core_only_attribute_changes.csv",
    "linkage_status_by_origin_quarter.csv", "estimand_bounds_by_year.csv", "estimand_bounds_by_year_5pct.csv",
    "estimand_bounds_overall.csv", "estimand3_corridor_level_by_year.csv",
    "model_metrics_lag0.csv", "model_metrics_lag1.csv", "model_paired_diffs_lag0.csv",
    "model_paired_diffs_lag1.csv", "model_capacity_lag0.csv", "model_capacity_lag1.csv",
    "model_capacity_diff_lag0.csv", "model_capacity_diff_lag1.csv", "model_reliability_lag0.csv",
    "model_reliability_lag1.csv", "model_registry_lag0.csv", "model_registry_lag1.csv",
    "reobservation_metrics_lag0.csv", "reobservation_metrics_lag1.csv",
    "subgroup_support.csv", "subgroup_model_metrics_lag0.csv",
    "presentation_model_brier_ci.csv", "presentation_region_metrics_lag0.csv",
    "presentation_corridor_metrics_lag0.csv", "presentation_provider_distribution_lag0.csv",
    "presentation_capacity_by_year_lag0.csv", "presentation_reliability_all_families.csv",
    "table_comparison.csv",
    "model_comparison.csv", "joint_dependence_sensitivity.csv", "all_origin_capacity_bounds.csv",
    "sensitivity_grid.csv", "publication_gates.csv",
    "recent_history_reference.csv",
    "conventional_reference_comparisons.csv",
}
SECTIONS = ["Overview", "Data & provenance", "Linkage & identity", "Continuity & bounds",
            "Model comparison", "Time-forward & lag sensitivity", "Calibration", "Review capacity",
            "Reobservation (negative result)", "Geography & support", "Reproducibility & limits",
            "Publication completion"]
MODELS = ["B0_always_stay", "B1_prevalence", "B2_history", "B3_cost_logistic", "L1_ridge_logistic",
          "L2_spline_logistic", "M1_hist_gbm", "M2_random_forest"]
NAMES = {"B0_always_stay": "B0 Always stays ≤3%", "B1_prevalence": "B1 Training prevalence",
         "B2_history": "B2 Shrunk provider/corridor history", "B3_cost_logistic": "B3 Current-cost logistic",
         "L1_ridge_logistic": "L1 Ridge logistic", "L2_spline_logistic": "L2 Spline logistic",
         "M1_hist_gbm": "M1 HistGradientBoosting", "M2_random_forest": "M2 Random forest",
         "R_highest_cost_rule": "R Highest current cost rule"}
# Fixed colour per entity (never re-assigned by filtering); categorical slots from a validated palette.
COLORS = {"B0_always_stay": "#9a9893", "B1_prevalence": "#6f6d68", "B2_history": "#1baf7a",
          "B3_cost_logistic": "#eda100", "L1_ridge_logistic": "#6250d6", "L2_spline_logistic": "#eb6834",
          "M1_hist_gbm": "#2a78d6", "M2_random_forest": "#e87ba4", "R_highest_cost_rule": "#52514e"}
SUBSETS = {"pooled_2022_2025": "Pooled targets 2022–2025Q1", "pooled_2022_2024": "Pooled targets 2022–2024",
           "year_2022": "Target year 2022", "year_2023": "Target year 2023", "year_2024": "Target year 2024",
           "year_2025": "Target year 2025 (2025Q1 only)"}
LAGS = {"lag0": "History lag 0 (primary)", "lag1": "History lag 1 (sensitivity)"}
DEFAULT_MODELS = ["B2_history", "L2_spline_logistic", "M1_hist_gbm"]


def path_of(name: str) -> Path:
    if name not in ALLOWLIST:
        raise ValueError(f"{name} is not on the public aggregate allowlist")
    if name in COMPLETION_FILES:
        return ROOT / "research_completion" / COMPLETION_FILES[name]
    return RESULTS / ("reproduction" if name == "table_comparison.csv" else "tables") / name


@st.cache_data
def table(name: str) -> pd.DataFrame:
    return pd.read_csv(path_of(name))


@st.cache_data
def run_meta() -> dict:
    return json.loads((RESULTS / "tables" / "run_meta_lag0.json").read_text(encoding="utf-8"))


@st.cache_data
def manifest() -> dict:
    return json.loads((RESULTS / "source_manifest.json").read_text(encoding="utf-8"))


def download(name: str, key: str):
    st.download_button(f"Download {name}", path_of(name).read_bytes(), file_name=name, mime="text/csv",
                       key=f"dl_{key}", icon=":material/download:")


def model_color_scale(models):
    return alt.Scale(domain=[NAMES[m] for m in models], range=[COLORS[m] for m in models])


def show(chart):
    st.altair_chart(chart.configure_axis(labelFontSize=12, titleFontSize=12, gridColor="#e4e3df", labelLimit=320)
                    .configure_view(strokeWidth=0), width="stretch")


def ribbon():
    st.warning("Publication completion: CONDITIONAL — NOT YET PUBLICATION-READY. No operational model. "
               "The Publication completion section contains the new local analyses; other sections preserve the phase 1 tables.")
    m = run_meta()
    st.markdown(
        f"""<div style="border-left:6px solid #2a78d6;background:rgba(42,120,214,0.08);padding:0.6rem 0.9rem;
        border-radius:4px;margin-bottom:0.6rem;font-size:0.92rem">
        <b>Stage:</b> R01 phase 1 · decision <b>CONDITIONAL</b> &nbsp;|&nbsp; <b>Status:</b> RETROSPECTIVE,
        EXPLORATORY backtest on previously inspected years (not a prospective forecast) &nbsp;|&nbsp;
        <b>Observed data:</b> survey quarters 2016Q2–2025Q3 (2025Q2 absent) &nbsp;|&nbsp;
        <b>Run:</b> <code>{m['run_id']}</code> @ <code>{m['code_commit'][:7]}</code>, source sha256
        <code>{m['source_sha256'][:8]}…</code></div>""", unsafe_allow_html=True)
    st.caption("Outcome = the same surveyed service, reobserved in the exactly-next calendar quarter, still costs "
               "≤3% of a USD 200 transfer. Surveyed quotes are not prices paid, provider exit or consumer advice; "
               "no savings are observed or implied. Publication timing of RPW waves is UNVERIFIED: the history-lag-1 "
               "run does not prove a quote was available before the next survey. Data: The World Bank, Remittance "
               "Prices Worldwide (CC BY 4.0), http://remittanceprices.worldbank.org — no endorsement implied.")


def overview():
    st.header("Overview")
    st.markdown(
        "**Question.** If a surveyed money-transfer quote costs ≤3% (the SDG 10.c reference level) in quarter *t*, "
        "does the same service still cost ≤3% when surveyed again in *t+1*? How much do identity rules and quotes "
        "that are never reobserved change the answer, and do models rank quotes for analyst re-checking better than "
        "simple rules? **Novelty remains unresolved:** the expanded review includes firm-level IMF analysis and "
        "2026 same-source service-level studies. The earlier abstract-only review was incomplete. See Publication completion.")
    b = table("estimand_bounds_overall.csv").iloc[0]
    ci = table("presentation_model_brier_ci.csv")
    p = ci[(ci.release_lag == "lag0") & (ci.subset == "pooled_2022_2025")].set_index("model")
    d = table("model_paired_diffs_lag0.csv")
    gs = d[(d.subset == "pooled_2022_2025") & (d.model_a == "M1_hist_gbm") & (d.model_b == "L2_spline_logistic")]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Eligible initially-cheap quotes", f"{int(b.n_eligible):,}", help="cc1 basket, 0 ≤ cost ≤ 3%, all years")
    c2.metric("P(stays ≤3%) | core reobserved", f"{b.conditional_p_stay_core:.3f}",
              help=f"{int(b.n_stay):,} of {int(b.n_stay + b.n_fail):,} reobserved quotes")
    c3.metric("Missing-outcome bounds", f"[{b.lower_bound:.2f}, {b.upper_bound:.2f}]",
              help=f"{int(b.n_unknown):,} eligible quotes with unknown outcome")
    c4.metric("Best Brier (pooled test, n=19,667)", f"{p['brier'].min():.4f}", help=NAMES[p['brier'].idxmin()])
    download("estimand_bounds_overall.csv", "overall")
    st.markdown(f"""
- **Simple rules are beaten:** history baseline Brier {p.loc['B2_history','brier']:.4f} vs HistGBM {p.loc['M1_hist_gbm','brier']:.4f}.
- **ML vs well-specified logistic is small:** HistGBM − spline = {gs.brier_diff_a_minus_b.iloc[0]:+.4f}
  (corridor-bootstrap 95% [{gs.ci95_lo.iloc[0]:+.4f}, {gs.ci95_hi.iloc[0]:+.4f}]); about one third of the
  historical pilot's reported gap, and the spline beat HistGBM in 2024.
- **Negative result kept:** a reobservation model did not beat prevalence in 2022 or 2023.
- **Uganda:** below the support gate (3 receiving corridors, 20 failures); no Uganda-sending corridors exist.
""")
    st.info("Navigation: use the sidebar. Every table behind a chart can be downloaded as an aggregate CSV. "
            "Filters only operate on the aggregates shown; no row-level drill-down exists by design.")


def provenance():
    st.header("Data & provenance")
    m = manifest()
    st.markdown(f"""
| Item | Value |
|---|---|
| File | `{m['source_url'].rsplit('/', 1)[-1]}` (official World Bank file host) |
| Bytes / sha256 | {m['bytes']:,} / `{m['sha256']}` |
| Fetched | {m['http']['fetched_at_utc']} (blob Last-Modified {m['http']['last_modified']}) |
| Catalogue | "Complete Dataset" last updated 23 Sep 2026; licence CC BY 4.0; classification Public |
| Observation period | collection dates 2016-05-09 to 2025-09-10 (post-2016 sheet) |
| Wave publication dates | **not available / unverified** — upload date ≠ observation date ≠ wave release date |
""")
    cov = table("audit_quarter_coverage.csv")
    cov["status"] = cov["present_in_source"].map({True: "present", False: "absent in source"})
    st.subheader("Published quotes per survey quarter")
    bars = alt.Chart(cov).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3, color="#2a78d6").encode(
        x=alt.X("quarter:N", sort=None, title="Survey quarter"),
        y=alt.Y("rows:Q", title="Published quotes (rows)"),
        tooltip=["quarter", "status", alt.Tooltip("rows:Q", format=","), "corridors", "firms_normalised",
                 "collection_date_min", "collection_date_max",
                 alt.Tooltip("cc1_cost_le3_share:Q", format=".1%", title="share cc1 ≤3%")])
    gap = alt.Chart(cov[~cov.present_in_source]).mark_rule(color="#e34948", strokeDash=[4, 3], size=2).encode(
        x="quarter:N", tooltip=["quarter", "status"])
    show(bars + gap)
    st.caption("Red dashed line = quarter absent from the source file (shown as missing, not zero).")
    download("audit_quarter_coverage.csv", "cov")
    st.subheader("Record flow (inclusion / exclusion)")
    flow = table("record_flow.csv")
    spec = st.selectbox("Specification", flow["spec"].unique().tolist(), key="flow_spec")
    st.dataframe(flow[flow.spec == spec][["step", "count"]], hide_index=True)
    download("record_flow.csv", "flow")
    st.subheader("Cost anomalies and missingness")
    st.dataframe(table("audit_cost_anomalies.csv"), hide_index=True)
    download("audit_cost_anomalies.csv", "anom")
    st.dataframe(table("audit_missingness.csv"), hide_index=True)
    download("audit_missingness.csv", "miss")


def linkage():
    st.header("Linkage & identity")
    st.markdown("**Core identity:** corridor + provider (normalised text) + payment instrument + access point + "
                "pickup method + pickup location + USD basket. **Strict:** core + unchanged speed and receiving-"
                "network coverage, evaluated on the same eligible cohort. Exact keys only; keys duplicated within "
                "a quarter are excluded; only the exactly-next quarter is linked.")
    cs = table("linkage_core_vs_strict_by_year.csv")
    long = cs.melt(id_vars=["target_year", "eligible"], value_vars=["core_reobserved", "strict_reobserved"],
                   var_name="definition", value_name="reobserved")
    long["share"] = long["reobserved"] / long["eligible"]
    show(alt.Chart(long).mark_line(point=alt.OverlayMarkDef(size=60), strokeWidth=2).encode(
        x=alt.X("target_year:O", title="Target year"),
        y=alt.Y("share:Q", title="Share of eligible cheap quotes reobserved", axis=alt.Axis(format="%")),
        color=alt.Color("definition:N", scale=alt.Scale(range=["#2a78d6", "#eb6834"]), title="Identity"),
        tooltip=["target_year", "definition", alt.Tooltip("reobserved:Q", format=","),
                 alt.Tooltip("eligible:Q", format=",", title="denominator"), alt.Tooltip("share:Q", format=".1%")]))
    st.dataframe(cs, hide_index=True)
    download("linkage_core_vs_strict_by_year.csv", "cs")
    st.dataframe(table("linkage_core_only_attribute_changes.csv"), hide_index=True)
    download("linkage_core_only_attribute_changes.csv", "chg")
    st.subheader("Linkage status by origin quarter (all quotes, all costs)")
    q = table("linkage_status_by_origin_quarter.csv")
    cols = ["core_reobserved", "core_unobserved_corridor_surveyed", "corridor_not_surveyed_next_quarter",
            "origin_key_ambiguous", "target_key_ambiguous", "right_censored_last_quarter"]
    ql = q.melt(id_vars=["origin_quarter", "qidx", "quotes"], value_vars=cols, var_name="status", value_name="n")
    ql["share"] = ql["n"] / ql["quotes"]
    show(alt.Chart(ql).mark_bar().encode(
        x=alt.X("origin_quarter:N", sort=alt.SortField("qidx"), title="Origin quarter"),
        y=alt.Y("share:Q", stack="normalize", title="Share of quotes", axis=alt.Axis(format="%")),
        color=alt.Color("status:N", sort=cols, scale=alt.Scale(
            domain=cols, range=["#2a78d6", "#eb6834", "#eda100", "#6250d6", "#e87ba4", "#9a9893"])),
        tooltip=["origin_quarter", "status", alt.Tooltip("n:Q", format=","),
                 alt.Tooltip("quotes:Q", format=",", title="denominator"), alt.Tooltip("share:Q", format=".1%")]))
    download("linkage_status_by_origin_quarter.csv", "status")


def bounds():
    st.header("Continuity & missing-outcome bounds")
    thr = st.radio("Threshold", ["3% (primary)", "5% (secondary)"], horizontal=True, key="thr")
    name = "estimand_bounds_by_year.csv" if thr.startswith("3") else "estimand_bounds_by_year_5pct.csv"
    b = table(name)
    st.markdown("Grey bar = worst/best case over **all** eligible initially-cheap quotes (unobserved → fail / → "
                "stay). Points = estimate conditional on reobservation. **Missing ≠ exit or price rise.**")
    base = alt.Chart(b).encode(x=alt.X("target_year:O", title="Target year"))
    tip = ["target_year", alt.Tooltip("n_eligible:Q", format=",", title="eligible (denominator)"),
           alt.Tooltip("n_stay:Q", format=","), alt.Tooltip("n_fail:Q", format=","),
           alt.Tooltip("n_unknown:Q", format=","), alt.Tooltip("lower_bound:Q", format=".3f"),
           alt.Tooltip("upper_bound:Q", format=".3f"), alt.Tooltip("conditional_p_stay_core:Q", format=".3f")]
    layers = [base.mark_bar(size=14, color="#c9c7c1", opacity=0.9).encode(
        y=alt.Y("lower_bound:Q", title="P(stays ≤ threshold)", scale=alt.Scale(domain=[0.3, 1])),
        y2="upper_bound:Q", tooltip=tip),
        base.mark_point(filled=True, size=90, color="#2a78d6").encode(y="conditional_p_stay_core:Q", tooltip=tip)]
    if "conditional_p_stay_strict" in b.columns:
        layers.append(base.mark_point(shape="square", filled=True, size=60, color="#eb6834").encode(
            y="conditional_p_stay_strict:Q", tooltip=tip + [alt.Tooltip("conditional_p_stay_strict:Q", format=".3f")]))
        st.caption("Blue circle = core identity; orange square = strict identity (same eligible cohort).")
    else:
        st.caption("Strict-identity estimate is computed for the 3% threshold only (not available for 5%).")
    show(alt.layer(*layers))
    st.dataframe(b, hide_index=True)
    download(name, "bounds")
    st.subheader("Corridor level: ≥1 surveyed ≤3% quote next quarter")
    st.caption("Conditional on the corridor being surveyed next quarter; a surveillance quantity, not consumer access.")
    e3 = table("estimand3_corridor_level_by_year.csv")
    st.dataframe(e3, hide_index=True)
    download("estimand3_corridor_level_by_year.csv", "e3")


def model_comparison():
    st.header("Model comparison — all eight frozen families")
    c1, c2, c3 = st.columns(3)
    lag = c1.selectbox("History information scenario", list(LAGS), format_func=LAGS.get, key="mc_lag")
    sub = c2.selectbox("Test subset", list(SUBSETS), format_func=SUBSETS.get, key="mc_subset")
    clus = c3.radio("Bootstrap clusters", ["corridor", "provider"], horizontal=True, key="mc_cluster")
    ci = table("presentation_model_brier_ci.csv")
    ci = ci[(ci.release_lag == lag) & (ci.subset == sub)].copy()
    ci["label"] = ci.model.map(NAMES)
    ci["lo"], ci["hi"] = ci[f"{clus}_boot_lo"], ci[f"{clus}_boot_hi"]
    order = ci.sort_values("brier")["label"].tolist()
    tip = ["label", alt.Tooltip("brier:Q", format=".4f"), alt.Tooltip("lo:Q", format=".4f", title="95% lo"),
           alt.Tooltip("hi:Q", format=".4f", title="95% hi"), alt.Tooltip("n:Q", format=",", title="test rows"),
           "n_corridors", "n_providers"]
    base = alt.Chart(ci).encode(y=alt.Y("label:N", sort=order, title=None))
    show((base.mark_rule(strokeWidth=2, color="#52514e").encode(
        x=alt.X("lo:Q", title="Brier score (lower is better)", scale=alt.Scale(zero=False)), x2="hi:Q", tooltip=tip)
        + base.mark_point(filled=True, size=110).encode(
            x="brier:Q", color=alt.Color("label:N", scale=model_color_scale(MODELS), legend=None), tooltip=tip)
        ).properties(height=320))
    st.caption(f"Bars: 95% percentile interval from {clus}-cluster bootstrap (1,000 reps) of the mean Brier on the "
               "same time-forward test rows. This quantifies sampling dependence; it is NOT held-out-"
               f"{clus} validation, which was not performed. Identical test rows for every model. Overlapping "
               "marginal intervals do NOT imply no difference: models are compared on the same rows, so use the "
               "paired differences below.")
    download("presentation_model_brier_ci.csv", "ci")
    m = table(f"model_metrics_{lag}.csv")
    m = m[m.subset == sub].assign(label=lambda x: x.model.map(NAMES)).sort_values("brier")
    st.dataframe(m[["label", "n", "prevalence_stay", "brier", "log_loss", "auroc", "auprc_failure",
                    "cal_intercept", "cal_slope", "mean_pred"]], hide_index=True)
    download(f"model_metrics_{lag}.csv", "metrics")
    st.subheader("Paired differences (A − B, cluster bootstrap)")
    d = table(f"model_paired_diffs_{lag}.csv")
    if sub in set(d.subset):
        st.dataframe(d[d.subset == sub], hide_index=True)
    else:
        st.warning("Paired differences were pre-computed for the pooled subsets only; per-year paired intervals are "
                   "not available (filter unsupported for this table).")
    download(f"model_paired_diffs_{lag}.csv", "diffs")


def time_forward():
    st.header("Time-forward performance & history-lag sensitivity")
    st.markdown("Expanding window, refit once per target year; training targets strictly precede the first test "
                "origin. 2025 contains only 2025Q1 targets because 2025Q2 is absent from the source.")
    sel = st.multiselect("Models", MODELS, default=DEFAULT_MODELS, format_func=NAMES.get, key="tf_models")
    ci = table("presentation_model_brier_ci.csv")
    yr = ci[(ci.release_lag == "lag0") & ci.subset.str.startswith("year_") & ci.model.isin(sel)].copy()
    yr["target_year"] = yr.subset.str[-4:]
    yr["label"] = yr.model.map(NAMES)
    if yr.empty:
        st.warning("Select at least one model.")
    else:
        tip = ["label", "target_year", alt.Tooltip("brier:Q", format=".4f"),
               alt.Tooltip("corridor_boot_lo:Q", format=".4f"), alt.Tooltip("corridor_boot_hi:Q", format=".4f"),
               alt.Tooltip("n:Q", format=",", title="test rows")]
        base = alt.Chart(yr).encode(x=alt.X("target_year:O", title="Target year"),
                                    color=alt.Color("label:N", scale=model_color_scale(sel), title="Model"))
        show(base.mark_line(strokeWidth=2).encode(y=alt.Y("brier:Q", title="Brier score", scale=alt.Scale(zero=False)),
                                                  tooltip=tip)
             + base.mark_errorbar(ticks=True).encode(y="corridor_boot_lo:Q", y2="corridor_boot_hi:Q", tooltip=tip)
             + base.mark_point(filled=True, size=60).encode(y="brier:Q", tooltip=tip))
    st.caption("Error bars: corridor-cluster bootstrap 95% intervals within each test year (sampling uncertainty only).")
    st.subheader("History lag 0 vs lag 1 (pooled 2022–2025Q1)")
    lg = ci[(ci.subset == "pooled_2022_2025") & ci.model.isin(sel)].copy()
    lg["label"] = lg.model.map(NAMES)
    if not lg.empty:
        show(alt.Chart(lg).mark_point(filled=True, size=90).encode(
            x=alt.X("brier:Q", title="Brier score", scale=alt.Scale(zero=False)),
            y=alt.Y("label:N", title=None),
            shape=alt.Shape("release_lag:N", title="History lag"),
            color=alt.Color("label:N", scale=model_color_scale(sel), legend=None),
            tooltip=["label", "release_lag", alt.Tooltip("brier:Q", format=".4f")]))
    st.warning("Lag 1 only delays the history features by one quarter. It does not establish that RPW quotes were "
               "publicly available before the next survey; operational lead time remains unverified.")
    download("presentation_model_brier_ci.csv", "ci_tf")
    download("model_registry_lag0.csv", "reg0")
    download("model_registry_lag1.csv", "reg1")


def calibration():
    st.header("Calibration")
    lag = st.selectbox("History information scenario", list(LAGS), format_func=LAGS.get, key="cal_lag")
    r = table("presentation_reliability_all_families.csv")
    r = r[r.release_lag == lag]
    avail = [m for m in MODELS if m in set(r.model)]
    sel = st.multiselect("Models", avail, default=["M1_hist_gbm", "L2_spline_logistic", "M2_random_forest"],
                         format_func=NAMES.get, key="cal_models")
    rr = r[r.model.isin(sel)].assign(label=lambda x: x.model.map(NAMES))
    diag = alt.Chart(pd.DataFrame({"x": [0.2, 1.0]})).mark_line(color="#9a9893", strokeDash=[5, 4]).encode(
        x="x:Q", y="x:Q")
    if not rr.empty:
        show(diag + alt.Chart(rr).mark_line(point=alt.OverlayMarkDef(size=60), strokeWidth=2).encode(
            x=alt.X("mean_pred:Q", title="Mean predicted P(stays ≤3%)", scale=alt.Scale(domain=[0.2, 1])),
            y=alt.Y("obs_rate:Q", title="Observed share staying ≤3%", scale=alt.Scale(domain=[0.2, 1])),
            color=alt.Color("label:N", scale=model_color_scale(sel), title="Model"),
            tooltip=["label", "bin", alt.Tooltip("n:Q", title="rows in decile"),
                     alt.Tooltip("mean_pred:Q", format=".3f"), alt.Tooltip("obs_rate:Q", format=".3f")]))
    st.caption("Pooled test rows split into prediction deciles; dashed line = perfect calibration. Deciles for all "
               "seven non-constant families are derived from the cached frozen-run test predictions (the frozen "
               "run stored deciles for four families only). B0 is constant and has no reliability curve.")
    download("presentation_reliability_all_families.csv", "rel_all")
    download(f"model_reliability_{lag}.csv", "rel")
    st.subheader("Calibration intercept and slope, all eight families (pooled 2022–2025Q1)")
    m = table(f"model_metrics_{lag}.csv")
    m = m[m.subset == "pooled_2022_2025"].assign(label=lambda x: x.model.map(NAMES))
    st.dataframe(m[["label", "cal_intercept", "cal_slope", "mean_pred", "prevalence_stay"]], hide_index=True)
    st.caption("Slope < 1 = over-confident spread; > 1 = under-confident (e.g. random forest 1.19). B0 is constant, "
               "so its slope is undefined.")


def capacity():
    st.header("Hypothetical review capacity")
    st.warning("A hypothetical analyst re-check list among reobserved quotes. Counts are observed threshold "
               "crossings captured — not consumer savings, transactions or market effects.")
    c1, c2 = st.columns(2)
    lag = c1.selectbox("History information scenario", list(LAGS), format_func=LAGS.get, key="cap_lag")
    c = table(f"model_capacity_{lag}.csv")
    sub = c2.selectbox("Test subset", c.subset.unique().tolist(), format_func=SUBSETS.get, key="cap_subset")
    rules = MODELS[2:] + ["R_highest_cost_rule"]
    sel = st.multiselect("Rules", rules, default=["M1_hist_gbm", "L2_spline_logistic", "B2_history",
                                                  "R_highest_cost_rule"], format_func=NAMES.get, key="cap_rules")
    cc = c[(c.subset == sub) & c.rule.isin(sel)].assign(label=lambda x: x.rule.map(NAMES))
    if not cc.empty:
        show(alt.Chart(cc).mark_line(point=alt.OverlayMarkDef(size=70), strokeWidth=2).encode(
            x=alt.X("capacity:Q", title="Review capacity (share of quotes per origin quarter)",
                    axis=alt.Axis(format="%", values=[0.1, 0.2, 0.3])),
            y=alt.Y("failures_captured_per_quarter:Q", title="Observed failures captured"),
            color=alt.Color("label:N", scale=model_color_scale(sel), title="Rule"),
            tooltip=["label", alt.Tooltip("capacity:Q", format="%"), "failures_captured_per_quarter",
                     alt.Tooltip("failures_total:Q", title="failures (denominator)"),
                     alt.Tooltip("recall_per_quarter:Q", format=".1%"), "reviewed_per_quarter_sum"]))
    st.caption("B0 and B1 are constant and cannot rank quotes, so they are omitted from capacity rankings.")
    download(f"model_capacity_{lag}.csv", "cap")
    st.subheader("Difference at 20% capacity (corridor bootstrap, 300 reps)")
    st.dataframe(table(f"model_capacity_diff_{lag}.csv"), hide_index=True)
    download(f"model_capacity_diff_{lag}.csv", "capd")
    st.subheader("20% capacity by target year (history lag 0)")
    cy = table("presentation_capacity_by_year_lag0.csv")
    cy = cy[cy.rule.isin(sel)].assign(label=lambda x: x.rule.map(NAMES))
    if not cy.empty:
        show(alt.Chart(cy).mark_bar().encode(
            x=alt.X("label:N", title=None, axis=alt.Axis(labelAngle=-30)),
            y=alt.Y("recall:Q", title="Share of observed failures captured", axis=alt.Axis(format="%")),
            color=alt.Color("label:N", scale=model_color_scale(sel), legend=None),
            column=alt.Column("target_year:O", title="Target year"),
            tooltip=["label", "target_year", "failures_captured", "failures_total", alt.Tooltip("recall:Q", format=".1%")]
        ).properties(width=110))
    download("presentation_capacity_by_year_lag0.csv", "capy")


def reobservation():
    st.header("Reobservation model — a negative result")
    st.markdown("Separate question: is an eligible cheap quote reobserved at all (given its corridor is surveyed "
                "next quarter)? A ridge logistic model **did not beat training prevalence** in 2022 or 2023, was "
                "roughly tied in 2024, and won only in 2025 (a single transition, 2024Q4→2025Q1). A better "
                "price-conditional model therefore does not imply useful prediction of service availability.")
    lag = st.selectbox("History information scenario", list(LAGS), format_func=LAGS.get, key="reob_lag")
    r = table(f"reobservation_metrics_{lag}.csv")
    show(alt.Chart(r).mark_line(point=alt.OverlayMarkDef(size=70), strokeWidth=2).encode(
        x=alt.X("test_target_year:O", title="Target year"),
        y=alt.Y("brier:Q", title="Brier score (lower is better)"),
        color=alt.Color("model:N", scale=alt.Scale(domain=["prevalence", "corridor_history", "ridge_logistic"],
                                                    range=["#9a9893", "#1baf7a", "#6250d6"]), title="Model"),
        tooltip=["model", "test_target_year", alt.Tooltip("brier:Q", format=".4f"), alt.Tooltip("n:Q", title="rows"),
                 alt.Tooltip("prevalence_stay:Q", format=".3f", title="reobserved share"), alt.Tooltip("auroc:Q", format=".3f")]))
    st.dataframe(r, hide_index=True)
    download(f"reobservation_metrics_{lag}.csv", "reob")


def geography():
    st.header("Geography & support gates")
    st.markdown("Models were trained globally. Pre-specified support gates: subgroup model metrics require ≥100 "
                "observed failures; region/corridor/provider aggregates require n ≥ 100 test rows **and** ≥ 20 "
                "observed failures. Unsupported groups are shown as unsupported, never as zero.")
    s = table("subgroup_support.csv")
    scope = st.radio("Scope", s.scope.unique().tolist(), horizontal=True, key="sg_scope")
    st.dataframe(s[s.scope == scope], hide_index=True)
    st.caption("Uganda: 3 receiving corridors; **no corridors send from Uganda** in the source (sending-Uganda "
               "filter unsupported).")
    download("subgroup_support.csv", "sg")
    st.subheader("Globally-trained model metrics within African subgroups (pooled test, lag 0)")
    sm = table("subgroup_model_metrics_lag0.csv")
    g = st.selectbox("Group", sm.group.unique().tolist(), key="sg_group")
    sg = sm[sm.group == g].dropna(axis=1, how="all")
    if (sg.model == "(not reported)").any():
        st.warning(f"{g}: support gate not met — {sg.iloc[0].get('note', '')}")
    st.dataframe(sg, hide_index=True)
    download("subgroup_model_metrics_lag0.csv", "sgm")
    st.subheader("Receiving-region performance (gated)")
    rg = table("presentation_region_metrics_lag0.csv")
    rl = rg[rg.supported].melt(id_vars=["destination_region", "n", "observed_failures"],
                               value_vars=[f"brier_{m}" for m in DEFAULT_MODELS], var_name="model", value_name="brier")
    rl["label"] = rl.model.str.replace("brier_", "", regex=False).map(NAMES)
    show(alt.Chart(rl).mark_point(filled=True, size=90).encode(
        x=alt.X("brier:Q", title="Brier score", scale=alt.Scale(zero=False)),
        y=alt.Y("destination_region:N", title=None),
        color=alt.Color("label:N", scale=model_color_scale(DEFAULT_MODELS), title="Model"),
        tooltip=["destination_region", "label", alt.Tooltip("brier:Q", format=".4f"), alt.Tooltip("n:Q", format=","),
                 "observed_failures"]))
    st.caption("World Bank region of the receiving country as given in the source; '..' = region not given in the "
               "source file (kept as published).")
    st.dataframe(rg, hide_index=True)
    download("presentation_region_metrics_lag0.csv", "region")
    st.subheader("Corridor-level performance (gated; ISO3 sending>receiving)")
    co = table("presentation_corridor_metrics_lag0.csv")
    st.caption(f"{int(co.supported.sum())} of {len(co)} test corridors meet the gate. Points: HistGBM minus spline "
               "Brier per corridor (negative favours HistGBM). Not a held-out-corridor validation.")
    cs = co[co.supported]
    show(alt.Chart(cs).mark_circle(size=70, color="#2a78d6", opacity=0.75).encode(
        x=alt.X("n:Q", title="Test rows in corridor", scale=alt.Scale(type="log")),
        y=alt.Y("gbm_minus_spline:Q", title="Brier: HistGBM − spline"),
        tooltip=["corridor", alt.Tooltip("n:Q", format=","), "observed_failures",
                 alt.Tooltip("observed_stay_rate:Q", format=".3f"), alt.Tooltip("gbm_minus_spline:Q", format="+.4f")])
         + alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="#9a9893", strokeDash=[4, 3]).encode(y="y:Q"))
    st.dataframe(co, hide_index=True)
    download("presentation_corridor_metrics_lag0.csv", "corr")
    st.subheader("Provider-level distribution (anonymous)")
    st.caption("Provider names are deliberately not shown (no provider assessment); filter by provider is "
               "unsupported. Statistics summarise providers meeting the gate.")
    st.dataframe(table("presentation_provider_distribution_lag0.csv"), hide_index=True)
    download("presentation_provider_distribution_lag0.csv", "prov")


def reproducibility():
    st.header("Reproducibility & limitations")
    rep = RESULTS / "reproduction" / "reproduction_report.json"
    if rep.exists():
        r = json.loads(rep.read_text(encoding="utf-8"))
        st.markdown(f"**Raw-to-result reproduction from the cached official workbook** (real data): "
                    f"{r['n_match']} of {r['n_tables']} frozen tables matched within atol/rtol "
                    f"{r['tolerance']['atol']:g}; run {r['run_at_utc']} at commit `{r['code_commit'][:7]}`, "
                    f"Python {r['python']}, scikit-learn {r['sklearn']}, seed {r['seed']}. "
                    f"Non-matching: {', '.join(r['non_matching']) or 'none'}.")
        st.dataframe(table("table_comparison.csv"), hide_index=True)
        download("table_comparison.csv", "repro")
    else:
        st.warning("No reproduction report found.")
    st.caption("The dashboard's own automated tests (AppTest) check rendering and table consistency on the committed "
               "aggregates; they are not a data reproduction.")
    st.markdown("""
**Archived phase 1 limitations / next gates**
- Retrospective only; 2022–24 inspected in the pilot; 2025Q2 missing; no untouched test period.
- RPW wave publication dates unverified → no lead time or operational forecasting claim.
- Outcome conditional on reobservation; bounds wide in 2021 and 2025. Missing ≠ exit.
- Exact-label identity probably under-links renamed services; bootstraps are one-way (corridor or provider), not crossed.
- The original review read abstracts; the completion dossier expands full-text assessment and retains a blocked competitor.
- Local completion recovered the original pilot code/cache and independently rebuilt the same cache bytes. Counts/GBM reproduce; spline has a small residual mismatch. Specifications still differ.
""")
    st.info("The new completion section adds chronological selection/calibration, group transfers, joint dependence "
            "sensitivities and all-origin capacity bounds. Historical phase 1 outputs above remain unchanged.")
    st.code("pip install -r dashboard/requirements.txt\nstreamlit run dashboard/app.py", language="bash")


def publication_completion():
    st.header("Publication completion")
    notice=json.loads((ROOT/"research_completion/assessment/dashboard_notice.json").read_text(encoding="utf-8"))
    st.caption(f"Analysis: {notice['analysis_date']} UTC; source cutoff: 2025Q3 (2025Q2 absent). "
               f"Model status: {notice['operational_model']}; independent confirmation: {notice['confirmation']}. "
               "Downloads serve committed aggregate files exactly; World Bank RPW, CC BY 4.0, no endorsement.")
    st.markdown("**CONDITIONAL GO / NOT YET PUBLICATION-READY.** The source was independently reacquired and "
                "the quote counts reproduced. Chronological selection/calibration and sensitivity analyses were executed locally. "
                "No verified public predictor lead time or untouched temporal confirmation exists. "
                "Closest-work novelty and true service identity remain unresolved. "
                "[Read the scientific verdict](https://github.com/Isaac25-lgtm/remittance-price-intelligence/blob/main/research_completion/assessment/PUBLICATION_VERDICT.md).")
    scores=pd.concat([table("model_comparison.csv"),table("recent_history_reference.csv")],ignore_index=True)
    selected=scores[scores.model=="S_selected"].iloc[0]
    st.metric("Retrospective selected-policy Brier",f"{selected.brier:.6f}",help=f"{int(selected.n):,} previously inspected outer test records")
    st.dataframe(scores.sort_values("brier"),hide_index=True)
    joint=table("joint_dependence_sensitivity.csv")
    d=joint[(joint.model_a=="S_selected")&(joint.model_b=="L2_spline_logistic")].iloc[0]
    st.warning(f"Selected policy minus spline Brier: {d.brier_diff:+.6f}; joint corridor/provider/time sensitivity "
               f"[{d.ci95_lo:+.6f}, {d.ci95_hi:+.6f}] includes zero. Limited stress coverage was 0.86, "
               "so nominal 95% coverage is unverified. No robust superiority claim.")
    st.dataframe(joint,hide_index=True)
    references=table("conventional_reference_comparisons.csv")
    st.caption("All raw/calibrated ridge and spline references are retained. Calibrated ridge is the lowest pooled "
               "conventional score, a post hoc description; the selected-policy joint interval versus it also includes zero. "
               "Brier skill is 1 minus model/reference Brier. No confirmatory superiority claim.")
    st.dataframe(references[(references.model=="S_selected")&(references.resampling=="crossed_corridor_provider_time_block")],hide_index=True)
    st.subheader("All-origin review scenarios")
    st.caption("The old matched-sample queue conditions on future reobservation. This correction scores all eligible "
               "origins and preserves unknown outcomes. Recall bounds are extreme allocations, not confidence intervals or measured benefits.")
    st.dataframe(table("all_origin_capacity_bounds.csv"),hide_index=True)
    st.subheader("Identity and missingness sensitivity")
    st.dataframe(table("sensitivity_grid.csv"),hide_index=True)
    st.subheader("Publication gates")
    st.dataframe(table("publication_gates.csv"),hide_index=True)
    for name in COMPLETION_FILES:
        download(name,"completion_"+name)


PAGES = dict(zip(SECTIONS, [overview, provenance, linkage, bounds, model_comparison, time_forward, calibration,
                            capacity, reobservation, geography, reproducibility, publication_completion]))


def main():
    st.set_page_config(page_title="R01 Remittance Quote Continuity", page_icon=":material/insights:", layout="wide")
    st.title("Remittance quote continuity — R01 research dashboard")
    ribbon()
    section = st.sidebar.radio("Section", SECTIONS, key="section")
    st.sidebar.caption("Research dashboard, not a consumer service. Aggregates only.")
    PAGES[section]()


main()
