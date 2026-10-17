"""R01 research dashboard: precomputed aggregate tables only (results/tables).

Run locally: streamlit run dashboard/app.py
No row-level RPW data, no model training, no live prices, no consumer recommendations.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

TABLES = Path(__file__).resolve().parents[1] / "results" / "tables"
SECTIONS = ["Overview", "Data provenance", "Study cohort & linkage", "Missing-outcome bounds",
            "Baselines and models", "Calibration", "Hypothetical review capacity",
            "African subgroup support", "Limitations & reproducibility"]
NAMES = {"B0_always_stay": "Always stays ≤3%", "B1_prevalence": "Training prevalence",
         "B2_history": "Shrunk provider/corridor history", "B3_cost_logistic": "Current-cost logistic",
         "L1_ridge_logistic": "Ridge logistic", "L2_spline_logistic": "Spline logistic",
         "M1_hist_gbm": "HistGradientBoosting", "M2_random_forest": "Random forest",
         "R_highest_cost_rule": "Highest current cost rule"}
SUBSETS = {"pooled_2022_2025": "Pooled targets 2022–2025Q1", "pooled_2022_2024": "Pooled targets 2022–2024",
           "year_2022": "Target year 2022", "year_2023": "Target year 2023", "year_2024": "Target year 2024",
           "year_2025": "Target year 2025 (2025Q1 only)"}
LAGS = {"lag0": "Release lag 0 (primary)", "lag1": "Release lag 1 (history sensitivity)"}


@st.cache_data
def table(name: str) -> pd.DataFrame:
    return pd.read_csv(TABLES / name)


@st.cache_data
def meta(name: str) -> dict:
    return json.loads((TABLES / name).read_text())


def ribbon():
    m = meta("run_meta_lag0.json")
    st.info(
        f"**Stage:** phase-1 research, decision **CONDITIONAL** · **Data cutoff:** 2025Q3 survey "
        f"(2025Q2 absent from source) · **All values are observed aggregates from a RETROSPECTIVE, "
        f"EXPLORATORY backtest** on previously inspected years, not a prospective forecast · "
        f"**Run:** `{m['run_id']}` @ `{m['code_commit'][:7]}` · source sha256 `{m['source_sha256'][:8]}…`")
    st.caption("Outcome is conditional on the same surveyed service being reobserved in the exactly-next "
               "calendar quarter. A surveyed quote is not a price paid, a provider exit or a consumer "
               "recommendation. No savings are observed or implied. Data: The World Bank, Remittance Prices "
               "Worldwide, http://remittanceprices.worldbank.org (no endorsement implied).")


def overview():
    st.header("Overview")
    st.markdown(
        "**Question.** If a surveyed money-transfer quote costs ≤3% of a USD 200 transfer in quarter *t*, "
        "does the same service, when surveyed again in quarter *t+1*, still cost ≤3%? How do service "
        "identity rules and quotes that are not reobserved change the answer? Do models rank quotes for "
        "analyst re-checking better than simple rules?")
    b = table("estimand_bounds_overall.csv").iloc[0]
    m = table("model_metrics_lag0.csv")
    p = m[m.subset == "pooled_2022_2025"].set_index("model")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Eligible initially-cheap quotes", f"{int(b.n_eligible):,}")
    c2.metric("P(stays ≤3%) | core reobserved", f"{b.conditional_p_stay_core:.3f}")
    c3.metric("Bounds over all eligible", f"[{b.lower_bound:.2f}, {b.upper_bound:.2f}]")
    c4.metric("Brier: HGB vs spline (pooled)",
              f"{p.loc['M1_hist_gbm', 'brier']:.4f}",
              f"{p.loc['M1_hist_gbm', 'brier'] - p.loc['L2_spline_logistic', 'brier']:+.4f} vs spline",
              delta_color="inverse")
    st.warning("Release dates of RPW waves are **unverified**. The release-lag-1 run only shifts history "
               "features; it does not show that a quote was publicly available before the next survey, so no "
               "lead time or operational forecasting value is claimed.")


def provenance():
    st.header("Data provenance")
    src = json.loads((TABLES.parent / "source_manifest.json").read_text())
    st.write({k: src[k] for k in ["source_url", "bytes", "sha256", "matches_frozen_checksum",
                                  "license_catalogue"]})
    st.caption(src["license_workbook_terms"])
    st.subheader("Failed routes (logged, not retried)")
    st.dataframe(pd.DataFrame(src["earlier_failed_routes"]), hide_index=True)
    st.subheader("Quotes per survey quarter")
    cov = table("audit_quarter_coverage.csv")
    st.caption("Missing quarters appear as empty (None), not zero.")
    st.dataframe(cov[["quarter", "present_in_source", "rows", "corridors", "firms_normalised",
                      "collection_date_min", "collection_date_max", "cc1_cost_le3_share"]],
                 hide_index=True)
    st.bar_chart(cov.set_index("quarter")["rows"], y_label="Published quotes", x_label="Survey quarter")
    st.subheader("Cost anomalies")
    st.dataframe(table("audit_cost_anomalies.csv"), hide_index=True)


def cohort():
    st.header("Study cohort & linkage")
    flow = table("record_flow.csv")
    spec = st.selectbox("Specification", flow["spec"].unique().tolist(), key="flow_spec")
    st.dataframe(flow[flow.spec == spec][["step", "count"]], hide_index=True)
    st.subheader("Core vs strict identity on the same eligible cohort")
    st.markdown("**Core:** corridor + provider + payment instrument + access point + pickup method/location "
                "+ USD basket. **Strict:** core + unchanged speed and receiving-network coverage. Exact keys "
                "only; duplicated keys are excluded.")
    st.dataframe(table("linkage_core_vs_strict_by_year.csv"), hide_index=True)
    st.dataframe(table("linkage_core_only_attribute_changes.csv"), hide_index=True)
    st.subheader("Linkage status by origin quarter (all costs)")
    q = table("linkage_status_by_origin_quarter.csv").set_index("origin_quarter")
    shares = q[["core_reobserved", "core_unobserved_corridor_surveyed",
                "corridor_not_surveyed_next_quarter"]].div(q["quotes"], axis=0)
    st.line_chart(shares, y_label="Share of quotes", x_label="Origin quarter")


def bounds():
    st.header("Missing-outcome bounds")
    thr = st.radio("Threshold", ["3% (primary)", "5% (secondary)"], horizontal=True, key="thr")
    b = table("estimand_bounds_by_year.csv" if thr.startswith("3") else "estimand_bounds_by_year_5pct.csv")
    st.markdown("Lower bound counts every non-reobserved or invalid outcome as a failure; upper bound as "
                "staying low-cost. **Missing ≠ exit or price rise.**")
    cols = [c for c in ["target_year", "n_eligible", "n_stay", "n_fail", "n_unknown",
                        "conditional_p_stay_core", "conditional_p_stay_strict", "lower_bound",
                        "upper_bound"] if c in b.columns]
    st.dataframe(b[cols], hide_index=True)
    st.line_chart(b.set_index("target_year")[["lower_bound", "conditional_p_stay_core", "upper_bound"]],
                  y_label="P(stays ≤ threshold)", x_label="Target year")
    st.subheader("Corridor level: ≥1 surveyed low-cost quote next quarter (surveillance, not access)")
    st.dataframe(table("estimand3_corridor_level_by_year.csv"), hide_index=True)


def models():
    st.header("Baselines and models")
    lag = st.selectbox("Information scenario", list(LAGS), format_func=LAGS.get, key="model_lag")
    sub = st.selectbox("Test subset", list(SUBSETS), format_func=SUBSETS.get, key="model_subset")
    m = table(f"model_metrics_{lag}.csv")
    m = m[m.subset == sub].copy()
    m.insert(0, "label", m["model"].map(NAMES))
    st.caption("Identical test rows for every model. Brier is the primary metric (lower is better). "
               "Fixed hyperparameters; no tuning. Retrospective exploratory evaluation.")
    st.dataframe(m.drop(columns=["subset"]).sort_values("brier"), hide_index=True)
    st.bar_chart(m.set_index("label")["brier"], y_label="Brier score", horizontal=True)
    st.subheader("Paired Brier differences (cluster bootstrap, 1,000 reps)")
    d = table(f"model_paired_diffs_{lag}.csv")
    st.dataframe(d[d.subset == sub] if sub in d.subset.unique() else d, hide_index=True)
    st.subheader("Separate model: is the service reobserved at all?")
    st.dataframe(table(f"reobservation_metrics_{lag}.csv"), hide_index=True)


def calibration():
    st.header("Calibration (pooled test, deciles)")
    lag = st.selectbox("Information scenario", list(LAGS), format_func=LAGS.get, key="cal_lag")
    r = table(f"model_reliability_{lag}.csv")
    chosen = st.multiselect("Models", r.model.unique().tolist(),
                            default=["M1_hist_gbm", "L2_spline_logistic"], format_func=NAMES.get,
                            key="cal_models")
    r = r[r.model.isin(chosen)]
    st.scatter_chart(r.assign(model=r.model.map(NAMES)), x="mean_pred", y="obs_rate", color="model",
                     x_label="Mean predicted P(stays ≤3%)", y_label="Observed share staying ≤3%")
    st.dataframe(r, hide_index=True)


def capacity():
    st.header("Hypothetical review capacity")
    st.warning("Hypothetical analyst re-check list among reobserved quotes. Counts are observed threshold "
               "crossings captured, **not** consumer savings, transactions or market effects.")
    lag = st.selectbox("Information scenario", list(LAGS), format_func=LAGS.get, key="cap_lag")
    c = table(f"model_capacity_{lag}.csv")
    sub = st.selectbox("Test subset", c.subset.unique().tolist(), format_func=SUBSETS.get, key="cap_subset")
    c = c[c.subset == sub].copy()
    c["rule_label"] = c.rule.map(NAMES)
    piv = c.pivot(index="capacity", columns="rule_label", values="failures_captured_per_quarter")
    st.line_chart(piv, x_label="Review capacity per origin quarter", y_label="Failures captured")
    st.dataframe(c.drop(columns=["rule"]), hide_index=True)
    st.subheader("Difference at 20% capacity (corridor bootstrap, 300 reps)")
    st.dataframe(table(f"model_capacity_diff_{lag}.csv"), hide_index=True)


def subgroups():
    st.header("African subgroup support")
    st.caption("Models were trained globally; subgroup metrics are descriptive. Model metrics are reported "
               "only where ≥100 observed failures exist (pre-set gate). Uganda: receiving direction only; no "
               "Uganda-sending corridors in the source.")
    s = table("subgroup_support.csv")
    scope = st.radio("Scope", s.scope.unique().tolist(), horizontal=True, key="sg_scope")
    st.dataframe(s[s.scope == scope], hide_index=True)
    st.subheader("Globally-trained model metrics within subgroups (pooled test)")
    sm = table("subgroup_model_metrics_lag0.csv")
    g = st.selectbox("Group", sm.group.unique().tolist(), key="sg_group")
    st.dataframe(sm[sm.group == g].dropna(axis=1, how="all"), hide_index=True)


def limits():
    st.header("Limitations & reproducibility")
    st.markdown("""
- Quotes, not transactions; target conditional on reobservation; bounds are wide in 2021 and 2025.
- RPW release dates are unverified, so no lead time is established; the lag-1 history run is not evidence of availability.
- No untouched test period: 2022–24 inspected in the pilot; 2025Q2 missing from source.
- Exact-label identity probably under-links renamed services; one-way (not crossed) cluster bootstraps.
- Competitor overlap: see `docs/PRIOR_ART.md`.
""")
    reg = table("model_registry_lag0.csv")
    st.dataframe(reg, hide_index=True)
    st.code("pip install -e '.[dev,dashboard]'\nstreamlit run dashboard/app.py", language="bash")


PAGES = dict(zip(SECTIONS, [overview, provenance, cohort, bounds, models, calibration, capacity,
                            subgroups, limits]))


def main():
    st.set_page_config(page_title="R01 Remittance Quote Continuity", layout="wide")
    st.title("R01 · Remittance quote continuity — research dashboard")
    ribbon()
    section = st.sidebar.radio("Section", SECTIONS, key="section")
    PAGES[section]()


main()
