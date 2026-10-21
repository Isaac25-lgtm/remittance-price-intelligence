"""R01 research dashboard: World Bank RPW service-level quote continuity.

Reads ONLY committed aggregate files listed in ALLOWLIST (legacy results and COMPLETION_FILES),
plus fixed source/run/notice metadata. No row-level quotes, services, provider names or predictions; no
model training or source download at startup. Run: streamlit run dashboard/app.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ui  # noqa: E402
from ui import AQUA, BLUE, BLUE_TINT, GREY, INK2, LIGHT, MUTED, ORANGE, ORANGE_TINT, VIOLET, YELLOW  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
REPO_URL = "https://github.com/Isaac25-lgtm/remittance-price-intelligence"
COMPLETION_FILES = {
    "model_comparison.csv": "models/model_comparison.csv",
    "joint_dependence_sensitivity.csv": "models/joint_dependence_sensitivity.csv",
    "all_origin_capacity_bounds.csv": "models/all_origin_capacity_bounds.csv",
    "sensitivity_grid.csv": "models/sensitivity_grid.csv",
    "publication_gates.csv": "assessment/publication_gates.csv",
    "recent_history_reference.csv": "models/recent_history_reference.csv",
    "conventional_reference_comparisons.csv": "models/conventional_reference_comparisons.csv",
    "LINKAGE_SCENARIO_RESULTS.csv": "phase3/identity/LINKAGE_SCENARIO_RESULTS.csv",
    "PAIRED_MEASUREMENT_EFFECTS.csv": "phase3/inference/PAIRED_MEASUREMENT_EFFECTS.csv",
    "PUBLICATION_GATE_MATRIX.csv": "phase3/assessment/PUBLICATION_GATE_MATRIX.csv",
    "wave_measurement.csv": "phase3/tables/wave_measurement.csv",
    "paired_wave_identity.csv": "phase3/tables/paired_wave_identity.csv",
    "unknown_flow.csv": "phase3/tables/unknown_flow.csv",
    "core_strict_transition.csv": "phase3/tables/core_strict_transition.csv",
    "measurement_sensitivities.csv": "phase3/tables/measurement_sensitivities.csv",
    "corridor_monitoring.csv": "phase3/tables/corridor_monitoring.csv",
    "independent_unit_support.csv": "phase3/tables/independent_unit_support.csv",
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
    "LINKAGE_SCENARIO_RESULTS.csv", "PAIRED_MEASUREMENT_EFFECTS.csv", "PUBLICATION_GATE_MATRIX.csv",
    "wave_measurement.csv", "paired_wave_identity.csv", "unknown_flow.csv", "core_strict_transition.csv",
    "measurement_sensitivities.csv", "corridor_monitoring.csv", "independent_unit_support.csv",
}
SECTIONS = ["Overview", "Background & question", "Data & provenance", "Linkage & identity",
            "Continuity & bounds", "Measurement audit (Phase 3)", "Model comparison",
            "Time-forward & lag sensitivity", "Calibration", "Review capacity", "Reobservation (negative result)",
            "Geography & support", "Verdict & publication gates", "Reproducibility & limits"]
MODELS = ["B0_always_stay", "B1_prevalence", "B2_history", "B3_cost_logistic", "L1_ridge_logistic",
          "L2_spline_logistic", "M1_hist_gbm", "M2_random_forest"]
NAMES = {"B0_always_stay": "B0 Always stays ≤3%", "B1_prevalence": "B1 Training prevalence",
         "B2_history": "B2 Shrunk provider/corridor history", "B3_cost_logistic": "B3 Current-cost logistic",
         "B4_recent_history": "B4 Recent rolling history",
         "L1_ridge_logistic": "L1 Ridge logistic", "L2_spline_logistic": "L2 Spline logistic",
         "M1_hist_gbm": "M1 HistGradientBoosting", "M2_random_forest": "M2 Random forest",
         "L1_ridge_logistic__cal": "L1 Ridge logistic, calibrated",
         "L2_spline_logistic__cal": "L2 Spline logistic, calibrated",
         "M1_hist_gbm__cal": "M1 HistGradientBoosting, calibrated",
         "M2_random_forest__cal": "M2 Random forest, calibrated",
         "S_selected": "S Selected research policy",
         "R_highest_cost_rule": "R Highest current cost rule"}
# Fixed colour per entity (never re-assigned by filtering); categorical slots from a validated palette.
COLORS = {"B0_always_stay": "#9a9893", "B1_prevalence": "#6f6d68", "B2_history": "#1baf7a",
          "B3_cost_logistic": "#eda100", "L1_ridge_logistic": "#6250d6", "L2_spline_logistic": "#eb6834",
          "M1_hist_gbm": "#2a78d6", "M2_random_forest": "#e87ba4", "R_highest_cost_rule": "#52514e",
          "S_selected": "#0d366b"}
FAMILY = {"B0_always_stay": "Baseline rule", "B1_prevalence": "Baseline rule", "B2_history": "Baseline rule",
          "B3_cost_logistic": "Baseline rule", "B4_recent_history": "Baseline rule",
          "L1_ridge_logistic": "Conventional statistical", "L2_spline_logistic": "Conventional statistical",
          "M1_hist_gbm": "Machine learning", "M2_random_forest": "Machine learning",
          "S_selected": "Selected research policy"}
FAMILY_COLORS = {"Baseline rule": GREY, "Conventional statistical": BLUE, "Machine learning": ORANGE,
                 "Selected research policy": AQUA}
SUBSETS = {"pooled_2022_2025": "Pooled targets 2022–2025Q1", "pooled_2022_2024": "Pooled targets 2022–2024",
           "year_2022": "Target year 2022", "year_2023": "Target year 2023", "year_2024": "Target year 2024",
           "year_2025": "Target year 2025 (2025Q1 only)"}
LAGS = {"lag0": "History lag 0 (primary)", "lag1": "History lag 1 (sensitivity)"}
DEFAULT_MODELS = ["B2_history", "L2_spline_logistic", "M1_hist_gbm"]
PRODUCTS = {"cc1_3pct": "USD 200 · 3% threshold (primary)", "cc1_5pct": "USD 200 · 5% threshold",
            "cc2_3pct": "USD 500 · 3% threshold", "cc2_5pct": "USD 500 · 5% threshold"}
FIELDS = {"region": "Receiving region", "provider_type": "Provider type", "fixed_sensitivity": "Period and exclusions",
          "dominance": "Dominant-group removal", "weighting": "Re-weighting (changes the target)"}
UNKNOWN_LABELS = {"stay": "Stays ≤3%", "fail": "Rises above 3%", "service_not_observed": "Service not observed",
                  "origin_key_ambiguous": "Ambiguous origin key", "corridor_not_surveyed": "Corridor not surveyed",
                  "invalid_target_cost": "Invalid target cost", "target_key_ambiguous": "Ambiguous target key",
                  "strict_attributes_changed": "Speed/network changed",
                  "other_unknown": "Invalid cost or ambiguous target"}
STRATA = {"..": "Region not given in source", "pre_2022Q3": "Before 2022Q3", "post_2022Q3": "2022Q3 onwards",
          "exclude_Russia": "Excluding Russia corridors", "exclude_largest_corridor_group": "Excluding largest corridor group",
          "exclude_largest_provider_group": "Excluding largest provider group",
          "equal_corridor_group": "Equal weight per corridor", "equal_provider_group": "Equal weight per provider"}


def stratum_label(field: str, stratum: str) -> str:
    if stratum in STRATA:
        return STRATA[stratum]
    if field == "region":
        return stratum.title().replace("&", "and")
    return stratum[:1].upper() + stratum[1:]


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


def data_panel(names: list[str], key: str, label: str = "Data behind this view", frame: pd.DataFrame | None = None):
    """Collapsible table view plus exact-byte downloads of the committed aggregates."""
    with st.expander(label, icon=":material/table_view:"):
        st.dataframe(frame if frame is not None else table(names[0]), hide_index=True, width="stretch")
        cols = st.columns(min(len(names), 3))
        for i, n in enumerate(names):
            with cols[i % len(cols)]:
                download(n, f"{key}_{i}")


def pct(x: float, d: int = 1) -> str:
    return f"{100 * x:.{d}f}%"


def qlabel(qidx: int) -> str:
    return f"{qidx // 4}Q{qidx % 4 + 1}"


def scenario_row(scenario: str) -> pd.Series:
    s = table("LINKAGE_SCENARIO_RESULTS.csv")
    return s[s.scenario == scenario].iloc[0]


def ribbon():
    m = run_meta()
    st.markdown(
        f"""<div class="ribbon"><span><b>Stage</b> R01 · Phase 3 · decision <b>CONDITIONAL_HOLD</b></span>
        <span><b>Status</b> RETROSPECTIVE, EXPLORATORY analysis of previously inspected years</span>
        <span><b>Observed data</b> survey quarters 2016Q2–2025Q3 (2025Q2 absent)</span>
        <span><b>Operational model</b> none</span>
        <span><b>Run</b> <code>{m['run_id']}</code> · source sha256 <code>{m['source_sha256'][:8]}…</code></span></div>""",
        unsafe_allow_html=True)


def caveats():
    st.caption("Outcome = the same surveyed service, reobserved in the exactly-next calendar quarter, still costs "
               "≤3% of a USD 200 transfer. Surveyed quotes are not prices paid, provider exit or consumer advice; "
               "no savings are observed or implied. Publication timing of RPW waves is UNVERIFIED: the history-lag-1 "
               "run does not prove a quote was available before the next survey. Data: The World Bank, Remittance "
               "Prices Worldwide (CC BY 4.0), http://remittanceprices.worldbank.org — no endorsement implied.")


# --------------------------------------------------------------------------------------------- charts
def identity_bounds_figure(products: list[str]) -> go.Figure:
    fig = go.Figure()
    for i, p in enumerate(products[::-1]):
        for rule, off, col, tint in [("core", 0.17, BLUE, "rgba(42,120,214,0.35)"),
                                     ("strict", -0.17, ORANGE, "rgba(235,104,52,0.35)")]:
            r = scenario_row(f"{p}_{rule}")
            tip = (f"<b>{PRODUCTS[p]}</b><br>{rule.title()} identity<br>Conditional: {pct(r.conditional)}"
                   f"<br>Bounds: {pct(r.lower)} – {pct(r.upper)}<br>Eligible origins: {int(r.n_eligible):,}"
                   f"<br>Valid pairs: {int(r.n_valid):,}<br>Unknown: {int(r.n_unknown):,}<extra></extra>")
            fig.add_trace(go.Scatter(x=[r.lower, r.upper], y=[i + off] * 2, mode="lines",
                                     line=dict(color=tint, width=12), hovertemplate=tip,
                                     name=f"{rule.title()} bounds", legendgroup=f"{rule}b", showlegend=i == 0))
            fig.add_trace(go.Scatter(x=[r.conditional], y=[i + off], mode="markers",
                                     marker=dict(color=col, size=12, line=dict(color="#fff", width=2)),
                                     hovertemplate=tip, name=f"{rule.title()} conditional",
                                     legendgroup=f"{rule}c", showlegend=i == 0))
    fig.update_yaxes(tickvals=list(range(len(products))), ticktext=[PRODUCTS[p] for p in products[::-1]],
                     showgrid=False)
    fig.update_xaxes(range=[0.4, 1.0], tickformat=".0%", title="Share of initially cheap quotes still cheap next quarter")
    return ui.style(fig, height=130 + 95 * len(products))


def range_dot_figure(df: pd.DataFrame, label_col: str, groups: list[tuple[str, str, str, str]],
                     x_title: str, height: int | None = None) -> go.Figure:
    """groups: (column prefix tag, display name, colour, tint) where df has conditional_/lower_/upper_ + tag."""
    fig = go.Figure()
    labels = df[label_col].tolist()
    n_g = len(groups)
    for gi, (tag, gname, col, tint) in enumerate(groups):
        off = (n_g - 1) / 2 * 0.3 - gi * 0.3
        for i, lab in enumerate(labels[::-1]):
            r = df[df[label_col] == lab].iloc[0]
            tip = (f"<b>{lab}</b><br>{gname}<br>Conditional: {pct(r['conditional_' + tag])}<br>Bounds: "
                   f"{pct(r['lower_' + tag])} – {pct(r['upper_' + tag])}<extra></extra>")
            fig.add_trace(go.Scatter(x=[r["lower_" + tag], r["upper_" + tag]], y=[i + off] * 2, mode="lines",
                                     line=dict(color=tint, width=9), hovertemplate=tip, name=f"{gname} bounds",
                                     legendgroup=tag + "b", showlegend=i == 0))
            fig.add_trace(go.Scatter(x=[r["conditional_" + tag]], y=[i + off], mode="markers",
                                     marker=dict(color=col, size=10, line=dict(color="#fff", width=2)),
                                     hovertemplate=tip, name=f"{gname} conditional", legendgroup=tag + "c",
                                     showlegend=i == 0))
    fig.update_yaxes(tickvals=list(range(len(labels))), ticktext=labels[::-1], showgrid=False)
    fig.update_xaxes(tickformat=".0%", title=x_title)
    return ui.style(fig, height=height or 120 + 62 * len(labels))


def unknown_sankey() -> go.Figure:
    u = table("unknown_flow.csv").set_index("state")["count"]
    u = pd.concat([u.drop(["invalid_target_cost", "target_key_ambiguous"]),
                   pd.Series({"other_unknown": u["invalid_target_cost"] + u["target_key_ambiguous"]})])
    unknown_states = ["service_not_observed", "origin_key_ambiguous", "corridor_not_surveyed", "other_unknown"]
    n_valid, n_unknown = int(u["stay"] + u["fail"]), int(u[unknown_states].sum())
    total = n_valid + n_unknown
    nodes = [f"Eligible cheap quotes<br>{total:,}", f"Valid successor pair<br>{n_valid:,}",
             f"Unknown successor<br>{n_unknown:,}", f"Stays ≤3%<br>{int(u['stay']):,}",
             f"Rises above 3%<br>{int(u['fail']):,}"] + [f"{UNKNOWN_LABELS[s]}<br>{int(u[s]):,}" for s in unknown_states]
    node_col = [ui.NAVY, BLUE, GREY, AQUA, ORANGE] + ["#b5b3ad"] * len(unknown_states)
    src = [0, 0, 1, 1] + [2] * len(unknown_states)
    tgt = [1, 2, 3, 4] + list(range(5, 5 + len(unknown_states)))
    val = [n_valid, n_unknown, int(u["stay"]), int(u["fail"])] + [int(u[s]) for s in unknown_states]
    link_col = ["rgba(42,120,214,0.28)", "rgba(154,152,147,0.32)", "rgba(27,175,122,0.30)",
                "rgba(235,104,52,0.32)"] + ["rgba(154,152,147,0.25)"] * len(unknown_states)
    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(label=nodes, color=node_col, pad=18, thickness=16, line=dict(width=0),
                  hovertemplate="%{label}<extra></extra>"),
        link=dict(source=src, target=tgt, value=val, color=link_col,
                  hovertemplate="%{source.label} → %{target.label}<br>%{value:,} quotes<extra></extra>")))
    fig.update_layout(font=dict(family=ui.FONT, size=12.5, color=ui.INK))
    return ui.style(fig, height=430, legend=False)


# --------------------------------------------------------------------------------------------- pages
def overview():
    core, strict = scenario_row("cc1_3pct_core"), scenario_row("cc1_3pct_strict")
    e3 = scenario_row("cc1_3pct_core_E3")
    sel = table("model_comparison.csv").set_index("model").loc["S_selected"]
    widen = (strict.upper - strict.lower) - (core.upper - core.lower)
    ui.hero("R01 · World Bank Remittance Prices Worldwide · 2016–2025",
            "When a remittance quote is cheap, does it stay cheap?",
            "A retrospective measurement study of 204,469 surveyed money-transfer quotes across 368 corridors. "
            "We follow every quote costing ≤3% of a USD 200 transfer (the SDG 10.c reference level) into the next "
            "survey quarter, and ask how much the answer depends on how a “same service” is defined and on the "
            "quotes that are never seen again.",
            [("Phase 3 · CONDITIONAL_HOLD", YELLOW), ("Retrospective, not a forecast", "#9ec5f4"),
             ("No operational model", ui.RED), ("Public data · CC BY 4.0", AQUA)])
    ribbon()
    ui.stats([
        ("Matched quotes still ≤3% next quarter", pct(core.conditional),
         f"{int(core.n_stay):,} of {int(core.n_valid):,} valid successor pairs (core identity)", BLUE),
        ("All eligible quotes: identified range", f"{pct(core.lower, 0)}–{pct(core.upper, 0)}",
         f"{int(core.n_unknown):,} of {int(core.n_eligible):,} cheap quotes have no observed successor", GREY),
        ("Extra width under strict identity", f"+{100 * widen:.1f} pp",
         f"Strict bounds {pct(strict.lower, 0)}–{pct(strict.upper, 0)}; conditional point almost unchanged", ORANGE),
        ("Corridors keeping ≥1 cheap quote", pct(e3.conditional),
         f"{int(e3.n_stay):,} of {int(e3.n_valid):,} resurveyed corridor-quarters", AQUA),
    ])
    st.subheader("The headline in one chart")
    ui.plot(identity_bounds_figure(list(PRODUCTS)), key="ov_bounds")
    st.caption("Dots: continuity among quotes with a valid successor. Bars: the range the true all-quote share "
               "must lie in when every unknown successor is counted as failing (left end) or staying (right end). "
               "These are identification bounds, not confidence intervals. Each row is a separate basket/threshold cohort.")
    ui.cards([
        ("What we measured", "Same-service price continuity",
         "<p>For each surveyed quote costing ≤3% in quarter <i>t</i>, we look for the identical service "
         "(corridor, provider, payment, access and pickup bundle, basket) in quarter <i>t+1</i> and check whether "
         "it still costs ≤3%.</p>"),
        ("What we found", "Four in five, if you can find it",
         f"<p>{pct(core.conditional)} of matched quotes stay cheap. But {pct(core.n_unknown / core.n_eligible, 0)} "
         "of cheap quotes have no observable successor, so the all-quote share is only identified within a "
         f"{100 * (core.upper - core.lower):.0f}-point range, which widens sharply under a stricter identity rule.</p>"),
        ("What it is not", "Not prices paid, not a forecast",
         "<p>Quotes are survey offers, not transactions. Missing quotes are not provider exits. Release dates "
         "of past survey waves cannot be verified, so no prediction lead time or operational model is claimed.</p>"),
    ])
    st.subheader("Key findings")
    st.markdown(f"""
- **Identity choice barely moves the matched estimate but greatly changes what is identified.** Strict matching keeps
  the same {int(strict.n_eligible):,} origins, loses {int(core.n_valid - strict.n_valid):,} valid pairs, and widens the
  all-origin bounds by **{100 * widen:.1f} percentage points**; the conditional point moves by
  {100 * (strict.conditional - core.conditional):+.2f} points. In 35 of 36 origin waves the strict bounds are wider.
- **Machine learning ranks slightly better, but not robustly.** Random forest and gradient boosting record the lowest
  retrospective Brier scores (≈0.128). The pre-specified selected policy scores {sel.brier:.4f}; its joint
  corridor/provider/time interval against the spline includes zero, so no superiority claim is made.
- **Review queues look useful only among matched quotes.** Once unknown outcomes are kept, the selected policy's
  recall at a 20% review budget is bounded between 21.7% and 57.3%.
- **Negative results are kept.** A model of whether a quote is reobserved did not beat simple prevalence in 2022 or
  2023, and Uganda-receiving corridors fall below the pre-specified support gate.
""")
    ui.callout("<b>How to use this site.</b> Start with <b>Background &amp; question</b> for the concepts, then "
               "<b>Measurement audit</b> for the main result. Model pages document the secondary prediction work. "
               "Every chart has a <i>Data behind this view</i> panel with the exact committed aggregate CSV.", "note")


def background():
    cov = table("audit_quarter_coverage.csv")
    present = cov[cov.present_in_source]
    cheap_share = present.cc1_cost_le3_share.mean()
    ui.page_head("Background", "Why remittance quote continuity matters",
                 "Remittances are money sent home by migrants. For many households they pay for food, school fees "
                 "and health care, so every percentage point lost to fees and exchange-rate margins matters.")
    ui.cards([
        ("The policy target", "SDG 10.c: below 3%",
         "<p>The Sustainable Development Goals ask countries to reduce the transaction cost of migrant "
         "remittances to less than 3% by 2030, and to eliminate corridors costing more than 5%.</p>"),
        ("The evidence base", "Remittance Prices Worldwide",
         f"<p>The World Bank surveys the total cost (fee plus exchange-rate margin) of sending USD 200 and USD 500 "
         f"through named services in each corridor. The post-2016 file used here has {int(present.rows.sum()):,} "
         f"quotes from {int(present.sending_countries.max())} sending and {int(present.receiving_countries.max())} "
         "receiving countries.</p>"),
        ("The gap", "Cheap today, cheap tomorrow?",
         f"<p>On average only {pct(cheap_share, 0)} of surveyed USD 200 quotes cost ≤3%. Official indicators "
         "describe corridor averages. They do not say whether a specific cheap service stays cheap, or how "
         "often it simply cannot be found again.</p>"),
    ])
    st.subheader("The research questions")
    ui.steps([
        ("Continuity", "If a surveyed quote costs ≤3% in quarter <i>t</i>, does the same service still cost ≤3% "
                       "in the exactly-next quarter?"),
        ("Identity", "How much does the answer depend on what counts as the “same service” (core vs strict)?"),
        ("Missingness", "What can be said about quotes that are never reobserved, without assuming why?"),
        ("Prediction", "Do statistical or ML models rank quotes for analyst re-checking better than simple rules?"),
    ])
    st.subheader("Where the 45,343 cheap quotes went")
    st.markdown("Every eligible quote ends in exactly one state. Only valid successor pairs have an observed outcome; "
                "the rest are **unknown**, which is not the same as the service disappearing or getting more expensive.")
    ui.plot(unknown_sankey(), key="bg_sankey")
    data_panel(["unknown_flow.csv"], "bg_flow", frame=table("unknown_flow.csv").assign(
        label=lambda d: d.state.map(UNKNOWN_LABELS)))
    st.subheader("Four estimands, kept separate")
    ui.cards([
        ("E1 · primary", "Conditional continuity",
         "<p>Share still ≤3% among quotes with a unique, valid successor in <i>t+1</i>. Precise, but only about "
         "quotes that could be matched.</p>"),
        ("E2 · bounds", "All-origin identification range",
         "<p>Allocate every unknown successor to fail (lower) or stay (upper). Honest about missingness and "
         "assumption-free, but wide.</p>"),
        ("E3 · corridor", "At least one cheap quote",
         "<p>Share of resurveyed corridors that still show ≥1 surveyed quote at ≤3%. A monitoring quantity, "
         "not the same offer.</p>"),
        ("E4 · coverage", "Reobservation",
         "<p>Share of cheap quotes whose service is uniquely found again at all. Reported separately, never "
         "folded into E1.</p>"),
    ], accent=VIOLET)
    st.subheader("Two definitions of the “same service”")
    st.markdown("""
| Rule | Matching key | Why it matters |
|---|---|---|
| **Core** (primary) | corridor · provider (normalised text) · payment instrument · access point · pickup method · pickup location · USD basket | Treats speed or network changes as the same service |
| **Strict** (sensitivity) | core **+** unchanged transfer speed **+** unchanged receiving-network coverage | A changed attribute breaks the link, so the outcome becomes unknown |

Matching is exact after deterministic text normalisation. There is no fuzzy matching, keys duplicated within a
quarter are excluded, and only the exactly-next calendar quarter is linked.
""")
    ui.callout("<b>What is not claimed.</b> Quotes are survey offers, not transactions. A missing quote is not a market "
               "exit. Continuity is not consumer access or savings. The study is retrospective: all test years were "
               "inspected before Phase 2, and historical release dates are unverified.", "caution")


def provenance():
    ui.page_head("Data", "Data & provenance",
                 "One official World Bank workbook, fetched and checksum-verified. Nothing is scraped and no row-level "
                 "data is published here.")
    m = manifest()
    ui.cards([
        ("Source file", m['source_url'].rsplit('/', 1)[-1],
         f"<p>{m['bytes']:,} bytes<br><code>{m['sha256'][:16]}…</code></p>"),
        ("Observation window", "2016Q2 – 2025Q3",
         "<p>Collection dates 2016-05-09 to 2025-09-10. <b>2025Q2 is absent</b> from the source.</p>"),
        ("Fetched", m['http']['fetched_at_utc'][:10],
         f"<p>Blob Last-Modified {ui.esc(m['http']['last_modified'])}. Catalogue update ≠ observation date ≠ "
         "wave release date (unverified).</p>"),
        ("Licence", "CC BY 4.0 · Public",
         "<p>The World Bank, Remittance Prices Worldwide. Attribution required; no endorsement implied.</p>"),
    ])
    cov = table("audit_quarter_coverage.csv")
    st.subheader("Published quotes per survey quarter")
    present = cov[cov.present_in_source]
    fig = go.Figure(go.Bar(x=present.quarter, y=present.rows, marker=dict(color=BLUE, cornerradius=4),
                           customdata=present[["corridors", "firms_normalised", "collection_date_min",
                                               "collection_date_max"]],
                           hovertemplate="<b>%{x}</b><br>%{y:,} quotes<br>%{customdata[0]:.0f} corridors · "
                                         "%{customdata[1]:.0f} providers<br>Collected %{customdata[2]} → "
                                         "%{customdata[3]}<extra></extra>", name="Quotes"))
    for q in cov[~cov.present_in_source].quarter:
        fig.add_vline(x=q, line=dict(color=ui.RED, dash="dash", width=2))
        fig.add_annotation(x=q, y=present.rows.max() * 1.04, text=f"{q} absent", showarrow=False,
                           font=dict(color=ui.RED, size=12), xanchor="right")
    fig.update_xaxes(categoryorder="array", categoryarray=cov.quarter.tolist(), tickangle=-45, showgrid=False)
    fig.update_yaxes(title="Published quotes", tickformat=",")
    ui.plot(ui.style(fig, height=360, legend=False), key="prov_cov")
    st.subheader("Share of USD 200 quotes costing ≤3%")
    fig = go.Figure(go.Scatter(x=present.quarter, y=present.cc1_cost_le3_share, mode="lines+markers",
                               line=dict(color=AQUA, width=2), marker=dict(size=7, line=dict(color="#fff", width=1.5)),
                               fill="tozeroy", fillcolor="rgba(27,175,122,0.10)",
                               hovertemplate="<b>%{x}</b><br>%{y:.1%} of USD 200 quotes ≤3%<extra></extra>"))
    fig.update_xaxes(categoryorder="array", categoryarray=cov.quarter.tolist(), tickangle=-45, showgrid=False)
    fig.update_yaxes(tickformat=".0%", title="Share ≤3%", rangemode="tozero")
    ui.plot(ui.style(fig, height=300, legend=False), key="prov_share")
    st.caption("The quarter absent from the source is shown as missing, never as zero.")
    data_panel(["audit_quarter_coverage.csv"], "cov")
    st.subheader("Record flow (inclusion / exclusion)")
    flow = table("record_flow.csv")
    spec = st.selectbox("Specification", flow["spec"].unique().tolist(), key="flow_spec")
    st.dataframe(flow[flow.spec == spec][["step", "count"]], hide_index=True, width="stretch")
    download("record_flow.csv", "flow")
    st.subheader("Cost anomalies and missingness")
    st.markdown("Negative and missing costs are counted and kept out of the primary cohort, never silently dropped.")
    c1, c2 = st.columns(2)
    with c1:
        st.dataframe(table("audit_cost_anomalies.csv"), hide_index=True, width="stretch")
        download("audit_cost_anomalies.csv", "anom")
    with c2:
        st.dataframe(table("audit_missingness.csv"), hide_index=True, width="stretch")
        download("audit_missingness.csv", "miss")


def linkage():
    ui.page_head("Identity", "Linkage & identity",
                 "Whether a cheap quote can be followed depends on the matching key. Core identity ignores changes "
                 "in speed and network coverage; strict identity treats them as a different service.")
    cs = table("linkage_core_vs_strict_by_year.csv")
    fig = go.Figure()
    for col, name, colour in [("core_reobserved", "Core identity", BLUE), ("strict_reobserved", "Strict identity", ORANGE)]:
        share = cs[col] / cs.eligible
        fig.add_trace(go.Scatter(x=cs.target_year, y=share, mode="lines+markers", name=name,
                                 line=dict(color=colour, width=2), marker=dict(size=9, line=dict(color="#fff", width=2)),
                                 customdata=cs[[col, "eligible"]],
                                 hovertemplate=f"<b>{name}</b> · %{{x}}<br>%{{y:.1%}} reobserved<br>%{{customdata[0]:,}}"
                                               " of %{customdata[1]:,} eligible<extra></extra>"))
    fig.update_yaxes(tickformat=".0%", title="Eligible cheap quotes reobserved")
    fig.update_xaxes(title="Target year", dtick=1, showgrid=False)
    ui.plot(ui.style(fig, height=360), key="lk_years")
    data_panel(["linkage_core_vs_strict_by_year.csv", "linkage_core_only_attribute_changes.csv"], "cs")
    st.subheader("How strict identity reclassifies core outcomes")
    t = table("core_strict_transition.csv")
    states = list(dict.fromkeys(t.state_core.tolist() + t.state_strict.tolist()))
    left = [f"Core: {UNKNOWN_LABELS[s]}" for s in states]
    right = [f"Strict: {UNKNOWN_LABELS[s]}" for s in states]
    colour = {"stay": AQUA, "fail": ORANGE, "strict_attributes_changed": VIOLET}
    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(label=left + right, pad=12, thickness=14, line=dict(width=0),
                  color=[colour.get(s, "#b5b3ad") for s in states] * 2),
        link=dict(source=[states.index(s) for s in t.state_core],
                  target=[len(states) + states.index(s) for s in t.state_strict], value=t.n,
                  color=["rgba(98,80,214,0.35)" if a != b else "rgba(154,152,147,0.22)"
                         for a, b in zip(t.state_core, t.state_strict)],
                  hovertemplate="%{source.label} → %{target.label}<br>%{value:,} quotes<extra></extra>")))
    ui.plot(ui.style(fig, height=430, legend=False), key="lk_sankey")
    st.caption("Violet flows are quotes whose core successor changed speed or network coverage. Under strict identity "
               "their outcome becomes unknown; most of them were stays, which is why the strict lower bound falls.")
    data_panel(["core_strict_transition.csv"], "trans")
    st.subheader("Linkage status by origin quarter (all quotes, all costs)")
    q = table("linkage_status_by_origin_quarter.csv").sort_values("qidx")
    cols = ["core_reobserved", "core_unobserved_corridor_surveyed", "corridor_not_surveyed_next_quarter",
            "origin_key_ambiguous", "target_key_ambiguous", "right_censored_last_quarter"]
    names = ["Reobserved (core)", "Not reobserved, corridor surveyed", "Corridor not surveyed next quarter",
             "Ambiguous origin key", "Ambiguous target key", "Right-censored (last quarter)"]
    palette = [BLUE, ORANGE, YELLOW, VIOLET, ui.MAGENTA, GREY]
    fig = go.Figure()
    for c, n, p in zip(cols, names, palette):
        fig.add_trace(go.Bar(x=q.origin_quarter, y=q[c] / q.quotes, name=n, marker=dict(color=p),
                             customdata=q[[c, "quotes"]],
                             hovertemplate=f"<b>{n}</b> · %{{x}}<br>%{{y:.1%}} (%{{customdata[0]:,}} of "
                                           "%{customdata[1]:,})<extra></extra>"))
    fig.update_layout(barmode="stack", bargap=0.12)
    fig.update_yaxes(tickformat=".0%", title="Share of quotes", range=[0, 1])
    fig.update_xaxes(tickangle=-45, showgrid=False)
    ui.plot(ui.style(fig, height=420), key="lk_status")
    data_panel(["linkage_status_by_origin_quarter.csv"], "status")


def bounds():
    ui.page_head("Estimands", "Continuity & missing-outcome bounds",
                 "Points show continuity among matched quotes. Bars show the worst-to-best range over all eligible "
                 "cheap quotes when unknown successors are allocated to fail or stay. Missing ≠ exit or price rise.")
    thr = st.radio("Threshold", ["3% (primary)", "5% (secondary)"], horizontal=True, key="thr")
    name = "estimand_bounds_by_year.csv" if thr.startswith("3") else "estimand_bounds_by_year_5pct.csv"
    b = table(name)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=b.target_year, y=b.upper_bound - b.lower_bound, base=b.lower_bound, name="All-origin bounds",
                         marker=dict(color=LIGHT, cornerradius=4), width=0.42,
                         customdata=b[["lower_bound", "upper_bound", "n_eligible", "n_unknown"]],
                         hovertemplate="<b>%{x}</b><br>Bounds %{customdata[0]:.1%} – %{customdata[1]:.1%}<br>"
                                       "%{customdata[2]:,} eligible · %{customdata[3]:,} unknown<extra></extra>"))
    fig.add_trace(go.Scatter(x=b.target_year, y=b.conditional_p_stay_core, mode="markers+lines", name="Core conditional",
                             line=dict(color=BLUE, width=2), marker=dict(size=10, line=dict(color="#fff", width=2)),
                             hovertemplate="<b>%{x}</b> core<br>%{y:.1%}<extra></extra>"))
    if "conditional_p_stay_strict" in b.columns:
        fig.add_trace(go.Scatter(x=b.target_year, y=b.conditional_p_stay_strict, mode="markers", name="Strict conditional",
                                 marker=dict(size=9, symbol="square", color=ORANGE, line=dict(color="#fff", width=2)),
                                 hovertemplate="<b>%{x}</b> strict<br>%{y:.1%}<extra></extra>"))
        st.caption("Blue circles = core identity; orange squares = strict identity (same eligible cohort).")
    else:
        st.caption("Strict-identity estimate is computed for the 3% threshold only (not available for 5%).")
    fig.update_yaxes(tickformat=".0%", title="P(stays ≤ threshold)", range=[0.3, 1])
    fig.update_xaxes(title="Target year", dtick=1, showgrid=False)
    ui.plot(ui.style(fig, height=420), key="bd_years")
    data_panel([name, "estimand_bounds_overall.csv"], "bounds")
    st.subheader("Corridor level: ≥1 surveyed cheap quote next quarter (E3)")
    cm = table("corridor_monitoring.csv").assign(quarter=lambda d: d.qidx.map(qlabel),
                                                 share=lambda d: d.cheap_next / d.surveyed)
    fig = go.Figure(go.Scatter(x=cm.quarter, y=cm.share, mode="lines+markers", line=dict(color=AQUA, width=2),
                               marker=dict(size=7, line=dict(color="#fff", width=1.5)), customdata=cm[["cheap_next", "surveyed"]],
                               hovertemplate="<b>%{x}</b> origin<br>%{y:.1%}: %{customdata[0]} of %{customdata[1]} "
                                             "resurveyed corridors<extra></extra>"))
    fig.update_yaxes(tickformat=".0%", title="Corridors with ≥1 cheap quote next quarter", range=[0.7, 1])
    fig.update_xaxes(tickangle=-45, showgrid=False, title="Origin quarter")
    ui.plot(ui.style(fig, height=330, legend=False), key="bd_e3")
    st.caption("Conditional on the corridor being surveyed next quarter: a surveillance quantity, not consumer access, "
               "and not persistence of the same offer.")
    data_panel(["estimand3_corridor_level_by_year.csv", "corridor_monitoring.csv"], "e3")


def measurement():
    core, strict = scenario_row("cc1_3pct_core"), scenario_row("cc1_3pct_strict")
    ui.page_head("Phase 3 · main result", "Measurement audit: identity-sensitive continuity",
                 "Phase 3 re-derived every count with an independent parser and asked one question: how robust is the "
                 "measured continuity to the identity rule, the survey wave, the product definition and the weighting?")
    ui.stats([
        ("Core conditional / strict conditional", f"{pct(core.conditional)} / {pct(strict.conditional)}",
         "Almost identical point estimates", BLUE),
        ("Core bounds width", f"{100 * (core.upper - core.lower):.1f} pp", f"{pct(core.lower)} – {pct(core.upper)}", GREY),
        ("Strict bounds width", f"{100 * (strict.upper - strict.lower):.1f} pp",
         f"{pct(strict.lower)} – {pct(strict.upper)}", ORANGE),
        ("Waves with wider strict bounds", "35 of 36", "None narrows; lag-4 HAC sensitivity 6.6–19.2 pp", VIOLET),
    ])
    st.subheader("Every survey wave")
    prod = st.radio("Product and threshold", list(PRODUCTS), format_func=PRODUCTS.get, horizontal=True, key="ms_product")
    w = table("wave_measurement.csv")
    fig = go.Figure()
    for rule, col, tint in [("strict", ORANGE, ORANGE_TINT), ("core", BLUE, BLUE_TINT)]:
        d = w[(w.scenario == f"{prod}_{rule}") & (w.valid > 0)].sort_values("qidx")
        fig.add_trace(go.Scatter(x=d.quarter, y=d.upper, mode="lines", line=dict(width=0), showlegend=False,
                                 hoverinfo="skip", legendgroup=rule))
        fig.add_trace(go.Scatter(x=d.quarter, y=d.lower, mode="lines", line=dict(width=0), fill="tonexty",
                                 fillcolor=tint, name=f"{rule.title()} bounds", legendgroup=rule,
                                 customdata=d[["lower", "upper", "n", "u"]],
                                 hovertemplate=f"<b>%{{x}}</b> {rule}<br>Bounds %{{customdata[0]:.1%}} – "
                                               "%{customdata[1]:.1%}<br>%{customdata[2]:,} eligible · "
                                               "%{customdata[3]:,} unknown<extra></extra>"))
        fig.add_trace(go.Scatter(x=d.quarter, y=d.conditional, mode="lines+markers", name=f"{rule.title()} conditional",
                                 line=dict(color=col, width=2), marker=dict(size=6, line=dict(color="#fff", width=1.5)),
                                 hovertemplate=f"<b>%{{x}}</b> {rule}<br>Conditional %{{y:.1%}}<extra></extra>"))
    fig.update_yaxes(tickformat=".0%", title="Share still under threshold next quarter", range=[0.2, 1])
    fig.update_xaxes(tickangle=-45, showgrid=False, title="Origin quarter")
    ui.plot(ui.style(fig, height=440), key="ms_waves")
    st.caption("Bands are per-wave identification bounds; lines are per-wave conditional continuity. Quarters are origin "
               "waves. The 2025Q1 origin wave is not drawn: 2025Q2 is absent from the source, so none of its quotes has "
               "an exactly-next successor and its bounds are uninformative (0–100%).")
    data_panel(["wave_measurement.csv"], "waves", frame=w[w.scenario.str.startswith(prod)])
    st.subheader("Paired width difference by wave (USD 200, 3%)")
    p = table("paired_wave_identity.csv").sort_values("qidx")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=p.quarter_core, y=p.width_strict - p.width_core, name="Strict − core width",
                         marker=dict(color=VIOLET, cornerradius=4), customdata=p[["width_core", "width_strict",
                                                                                 "additional_unknown"]],
                         hovertemplate="<b>%{x}</b><br>Core width %{customdata[0]:.1%}<br>Strict width "
                                       "%{customdata[1]:.1%}<br>+%{customdata[2]:,} unknown under strict<extra></extra>"))
    fig.add_hline(y=strict.upper - strict.lower - (core.upper - core.lower), line=dict(color=INK2, dash="dot", width=1.5),
                  annotation_text="pooled difference", annotation_position="top left",
                  annotation_font=dict(size=11, color=INK2))
    fig.update_yaxes(tickformat=".0%", title="Extra bound width (percentage points)")
    fig.update_xaxes(tickangle=-45, showgrid=False)
    ui.plot(ui.style(fig, height=360, legend=False), key="ms_width")
    data_panel(["paired_wave_identity.csv", "PAIRED_MEASUREMENT_EFFECTS.csv"], "paired")
    ui.callout("<b>Uncertainty.</b> Wave-level HAC intervals are reported as assumption-dependent sensitivities: "
               "36 origin waves and changing survey composition mean nominal 95% coverage is not validated. "
               "The counts and bounds themselves are exact descriptions of the recorded panel.", "caution")
    st.subheader("Sensitivity by group, period and weighting")
    field = st.selectbox("Breakdown", list(FIELDS), format_func=FIELDS.get, key="ms_field")
    s = table("measurement_sensitivities.csv")
    s = s[s.stratum_field == field].copy()
    s["label"] = [stratum_label(field, x) for x in s.stratum]
    wide = s.pivot_table(index="label", columns=s.scenario.str.split("_").str[-1],
                         values=["conditional", "lower", "upper"]).reset_index()
    wide.columns = [c if not t else f"{c}_{t}" for c, t in wide.columns]
    wide = wide.sort_values("conditional_core", ascending=False)
    ui.plot(range_dot_figure(wide, "label", [("core", "Core", BLUE, "rgba(42,120,214,0.30)"),
                                             ("strict", "Strict", ORANGE, "rgba(235,104,52,0.30)")],
                             "Share still ≤3% next quarter"), key="ms_sens")
    if field == "weighting":
        ui.callout("Equal-corridor and equal-provider weighting gives every group the same weight. This changes the "
                   "estimand (to an average corridor or provider). It does not correct survey selection.", "note")
    data_panel(["measurement_sensitivities.csv", "independent_unit_support.csv", "LINKAGE_SCENARIO_RESULTS.csv"], "sens",
               frame=s.drop(columns=["label"]))


def model_comparison():
    ui.page_head("Secondary analysis", "Model comparison",
                 "Can a model rank quotes by risk of losing affordability better than simple rules? All scores are "
                 "retrospective, on 19,667 previously inspected test records, with identical rows for every model.")
    st.subheader("Phase 2: chronological selection and calibration")
    sc = pd.concat([table("model_comparison.csv"), table("recent_history_reference.csv")], ignore_index=True)
    sc["base"] = sc.model.str.replace("__cal", "", regex=False)
    sc["family"] = sc.base.map(FAMILY)
    sc["label"] = sc.model.map(NAMES)
    sc = sc.sort_values("brier", ascending=False)
    fig = go.Figure()
    for fam, colour in FAMILY_COLORS.items():
        d = sc[sc.family == fam]
        fig.add_trace(go.Bar(y=d.label, x=d.brier, orientation="h", name=fam, marker=dict(color=colour, cornerradius=4),
                             width=0.62, customdata=d[["log_loss", "auroc", "cal_slope"]],
                             hovertemplate="<b>%{y}</b><br>Brier %{x:.4f}<br>Log loss %{customdata[0]:.4f}<br>"
                                           "AUROC %{customdata[1]:.3f}<br>Calibration slope %{customdata[2]:.2f}"
                                           "<extra></extra>"))
    fig.update_xaxes(range=[0.12, sc.brier.max() + 0.004], title="Brier score (lower is better)")
    fig.update_yaxes(categoryorder="array", categoryarray=sc.label.tolist(), showgrid=False)
    fig.update_layout(barmode="overlay")
    ui.plot(ui.style(fig, height=520), key="mc_phase2")
    st.caption("Axis starts at 0.12 to separate close scores; read differences from the paired intervals below, not from "
               "bar length. Calibrated variants were fitted on a reserved chronological calibration window.")
    data_panel(["model_comparison.csv", "recent_history_reference.csv"], "p2")
    st.subheader("Is any difference robust? Joint corridor × provider × time sensitivity")
    j = table("joint_dependence_sensitivity.csv").copy()
    short = {"M1_hist_gbm": "HistGBM", "M2_random_forest": "Random forest", "S_selected": "Selected policy",
             "L2_spline_logistic": "spline", "B2_history": "history baseline"}
    j["label"] = (j.analysis.map({"phase2": "Phase 2", "legacy": "Phase 1"}) + " · " + j.model_a.map(short) + " − "
                  + j.model_b.map(short))
    j = j.iloc[::-1]
    crosses = (j.ci95_lo <= 0) & (j.ci95_hi >= 0)
    fig = go.Figure(go.Scatter(
        x=j.brier_diff, y=j.label, mode="markers",
        marker=dict(size=11, color=[GREY if c else BLUE for c in crosses], line=dict(color="#fff", width=2)),
        error_x=dict(type="data", symmetric=False, array=j.ci95_hi - j.brier_diff, arrayminus=j.brier_diff - j.ci95_lo,
                     color=INK2, thickness=1.6, width=5),
        customdata=j[["ci95_lo", "ci95_hi", "n_quarters"]],
        hovertemplate="<b>%{y}</b><br>Δ Brier %{x:+.4f}<br>Interval %{customdata[0]:+.4f} to %{customdata[1]:+.4f}"
                      "<br>%{customdata[2]} target quarters<extra></extra>"))
    fig.add_vline(x=0, line=dict(color=ui.RED, width=1.5, dash="dot"))
    fig.update_xaxes(title="Difference in Brier score (negative favours the first model)", tickformat="+.3f")
    fig.update_yaxes(showgrid=False)
    ui.plot(ui.style(fig, height=330, legend=False), key="mc_joint")
    st.caption("Grey = interval includes zero. Only 13 target quarters are available and a small simulation gave 0.86 "
               "coverage, so these intervals are exploratory sensitivities rather than validated 95% intervals.")
    data_panel(["joint_dependence_sensitivity.csv", "conventional_reference_comparisons.csv"], "joint")

    st.subheader("Phase 1: all eight frozen families with cluster bootstrap")
    c1, c2, c3 = st.columns(3)
    lag = c1.selectbox("History information scenario", list(LAGS), format_func=LAGS.get, key="mc_lag")
    sub = c2.selectbox("Test subset", list(SUBSETS), format_func=SUBSETS.get, key="mc_subset")
    clus = c3.radio("Bootstrap clusters", ["corridor", "provider"], horizontal=True, key="mc_cluster")
    ci = table("presentation_model_brier_ci.csv")
    ci = ci[(ci.release_lag == lag) & (ci.subset == sub)].copy()
    ci["label"] = ci.model.map(NAMES)
    ci["lo"], ci["hi"] = ci[f"{clus}_boot_lo"], ci[f"{clus}_boot_hi"]
    ci = ci.sort_values("brier", ascending=False)
    fig = go.Figure(go.Scatter(
        x=ci.brier, y=ci.label, mode="markers",
        marker=dict(size=12, color=[COLORS[m] for m in ci.model], line=dict(color="#fff", width=2)),
        error_x=dict(type="data", symmetric=False, array=ci.hi - ci.brier, arrayminus=ci.brier - ci.lo, color=INK2,
                     thickness=1.6, width=5),
        customdata=ci[["lo", "hi", "n", "n_corridors", "n_providers"]],
        hovertemplate="<b>%{y}</b><br>Brier %{x:.4f}<br>95% %{customdata[0]:.4f} – %{customdata[1]:.4f}<br>"
                      "%{customdata[2]:,} test rows · %{customdata[3]} corridors · %{customdata[4]} providers"
                      "<extra></extra>"))
    fig.update_xaxes(title="Brier score (lower is better)")
    fig.update_yaxes(showgrid=False)
    ui.plot(ui.style(fig, height=380, legend=False), key="mc_legacy")
    st.caption(f"Bars: 95% percentile interval from {clus}-cluster bootstrap (1,000 reps) of the mean Brier on the "
               "same time-forward test rows. This quantifies sampling dependence; it is NOT held-out-"
               f"{clus} validation, which was not performed. Overlapping marginal intervals do NOT imply no difference: "
               "models are compared on the same rows, so use the paired differences below.")
    m = table(f"model_metrics_{lag}.csv")
    m = m[m.subset == sub].assign(label=lambda x: x.model.map(NAMES)).sort_values("brier")
    with st.expander("Full metric table", icon=":material/table_view:"):
        st.dataframe(m[["label", "n", "prevalence_stay", "brier", "log_loss", "auroc", "auprc_failure",
                        "cal_intercept", "cal_slope", "mean_pred"]], hide_index=True, width="stretch")
        download("presentation_model_brier_ci.csv", "ci")
        download(f"model_metrics_{lag}.csv", "metrics")
    st.subheader("Paired differences (A − B, cluster bootstrap)")
    d = table(f"model_paired_diffs_{lag}.csv")
    if sub in set(d.subset):
        st.dataframe(d[d.subset == sub], hide_index=True, width="stretch")
    else:
        st.warning("Paired differences were pre-computed for the pooled subsets only; per-year paired intervals are "
                   "not available (filter unsupported for this table).")
    download(f"model_paired_diffs_{lag}.csv", "diffs")


def time_forward():
    ui.page_head("Secondary analysis", "Time-forward performance & history-lag sensitivity",
                 "Expanding window, refit once per target year; training targets strictly precede the first test origin. "
                 "2025 contains only 2025Q1 targets because 2025Q2 is absent from the source.")
    sel = st.multiselect("Models", MODELS, default=DEFAULT_MODELS, format_func=NAMES.get, key="tf_models")
    ci = table("presentation_model_brier_ci.csv")
    yr = ci[(ci.release_lag == "lag0") & ci.subset.str.startswith("year_") & ci.model.isin(sel)].copy()
    yr["target_year"] = yr.subset.str[-4:]
    if yr.empty:
        st.warning("Select at least one model.")
    else:
        fig = go.Figure()
        for mdl in [m for m in MODELS if m in sel]:
            d = yr[yr.model == mdl].sort_values("target_year")
            fig.add_trace(go.Scatter(
                x=d.target_year, y=d.brier, mode="lines+markers", name=NAMES[mdl], line=dict(color=COLORS[mdl], width=2),
                marker=dict(size=9, line=dict(color="#fff", width=2)),
                error_y=dict(type="data", symmetric=False, array=d.corridor_boot_hi - d.brier,
                             arrayminus=d.brier - d.corridor_boot_lo, color=COLORS[mdl], thickness=1.2, width=4),
                customdata=d[["corridor_boot_lo", "corridor_boot_hi", "n"]],
                hovertemplate=f"<b>{NAMES[mdl]}</b> · %{{x}}<br>Brier %{{y:.4f}}<br>95% %{{customdata[0]:.4f}} – "
                              "%{customdata[1]:.4f}<br>%{customdata[2]:,} test rows<extra></extra>"))
        fig.update_yaxes(title="Brier score (lower is better)")
        fig.update_xaxes(title="Target year", showgrid=False, type="category")
        ui.plot(ui.style(fig, height=400), key="tf_years")
    st.caption("Error bars: corridor-cluster bootstrap 95% intervals within each test year (sampling uncertainty only).")
    st.subheader("History lag 0 vs lag 1 (pooled 2022–2025Q1)")
    lg = ci[(ci.subset == "pooled_2022_2025") & ci.model.isin(sel)].copy()
    if not lg.empty:
        fig = go.Figure()
        for lag_key, symbol, name in [("lag0", "circle", "Lag 0"), ("lag1", "diamond", "Lag 1")]:
            d = lg[lg.release_lag == lag_key]
            fig.add_trace(go.Scatter(x=d.brier, y=d.model.map(NAMES), mode="markers", name=name,
                                     marker=dict(size=12, symbol=symbol, color=[COLORS[m] for m in d.model],
                                                 line=dict(color="#fff", width=2)),
                                     hovertemplate=f"<b>%{{y}}</b> · {name}<br>Brier %{{x:.4f}}<extra></extra>"))
        fig.update_xaxes(title="Brier score")
        fig.update_yaxes(showgrid=False)
        ui.plot(ui.style(fig, height=110 + 48 * lg.model.nunique()), key="tf_lag")
    st.warning("Lag 1 only delays the history features by one quarter. It does not establish that RPW quotes were "
               "publicly available before the next survey; operational lead time remains unverified.")
    with st.expander("Data behind this view", icon=":material/table_view:"):
        download("presentation_model_brier_ci.csv", "ci_tf")
        download("model_registry_lag0.csv", "reg0")
        download("model_registry_lag1.csv", "reg1")


def calibration():
    ui.page_head("Secondary analysis", "Calibration",
                 "Do predicted probabilities match observed rates? Pooled test rows are split into prediction deciles; "
                 "the dotted diagonal is perfect calibration.")
    lag = st.selectbox("History information scenario", list(LAGS), format_func=LAGS.get, key="cal_lag")
    r = table("presentation_reliability_all_families.csv")
    r = r[r.release_lag == lag]
    avail = [m for m in MODELS if m in set(r.model)]
    sel = st.multiselect("Models", avail, default=["M1_hist_gbm", "L2_spline_logistic", "M2_random_forest"],
                         format_func=NAMES.get, key="cal_models")
    rr = r[r.model.isin(sel)]
    if not rr.empty:
        fig = go.Figure(go.Scatter(x=[0.2, 1], y=[0.2, 1], mode="lines", line=dict(color=MUTED, dash="dot", width=1.5),
                                   name="Perfect calibration", hoverinfo="skip"))
        for mdl in [m for m in MODELS if m in sel]:
            d = rr[rr.model == mdl].sort_values("bin")
            fig.add_trace(go.Scatter(x=d.mean_pred, y=d.obs_rate, mode="lines+markers", name=NAMES[mdl],
                                     line=dict(color=COLORS[mdl], width=2),
                                     marker=dict(size=8, line=dict(color="#fff", width=2)), customdata=d[["bin", "n"]],
                                     hovertemplate=f"<b>{NAMES[mdl]}</b><br>Decile %{{customdata[0]}} · "
                                                   "%{customdata[1]:,} rows<br>Predicted %{x:.3f} · observed %{y:.3f}"
                                                   "<extra></extra>"))
        fig.update_xaxes(range=[0.2, 1], title="Mean predicted P(stays ≤3%)", tickformat=".0%")
        fig.update_yaxes(range=[0.2, 1], title="Observed share staying ≤3%", tickformat=".0%")
        ui.plot(ui.style(fig, height=520), key="cal_curve")
    st.caption("Deciles for all seven non-constant families are derived from the cached frozen-run test predictions (the "
               "frozen run stored deciles for four families only). B0 is constant and has no reliability curve.")
    st.subheader("Calibration intercept and slope, all eight families (pooled 2022–2025Q1)")
    m = table(f"model_metrics_{lag}.csv")
    m = m[m.subset == "pooled_2022_2025"].assign(label=lambda x: x.model.map(NAMES))
    st.dataframe(m[["label", "cal_intercept", "cal_slope", "mean_pred", "prevalence_stay"]], hide_index=True,
                 width="stretch")
    st.caption("Slope < 1 = over-confident spread; > 1 = under-confident (e.g. random forest 1.19). B0 is constant, "
               "so its slope is undefined.")
    with st.expander("Data behind this view", icon=":material/table_view:"):
        download("presentation_reliability_all_families.csv", "rel_all")
        download(f"model_reliability_{lag}.csv", "rel")


def capacity():
    ui.page_head("Secondary analysis", "Hypothetical review capacity",
                 "If an analyst could re-check only a fixed share of cheap quotes each quarter, which ranking finds the "
                 "most quotes that later lose affordability? Counts are observed threshold crossings, not savings.")
    st.subheader("Correction: score every eligible origin, keep unknowns unknown")
    a = table("all_origin_capacity_bounds.csv")
    rules = ["S_selected", "L2_spline_logistic", "B2_history", "R_highest_cost_rule"]
    fig = go.Figure()
    for i, rule in enumerate(rules):
        d = a[a.rule == rule]
        x = d.capacity * 100 + (i - 1.5) * 1.1
        fig.add_trace(go.Scatter(
            x=x, y=d.recall_of_known_failures, mode="markers", name=NAMES[rule],
            marker=dict(size=10, color=COLORS[rule], line=dict(color="#fff", width=2)),
            error_y=dict(type="data", symmetric=False, array=d.all_failure_recall_upper - d.recall_of_known_failures,
                         arrayminus=d.recall_of_known_failures - d.all_failure_recall_lower, color=COLORS[rule],
                         thickness=2.5, width=0),
            customdata=d[["capacity", "all_failure_recall_lower", "all_failure_recall_upper", "reviewed", "unknown_reviewed"]],
            hovertemplate=f"<b>{NAMES[rule]}</b> · %{{customdata[0]:.0%}} budget<br>Recall of known failures %{{y:.1%}}"
                          "<br>All-failure recall bounds %{customdata[1]:.1%} – %{customdata[2]:.1%}<br>"
                          "%{customdata[3]:,} reviewed, %{customdata[4]:,} with unknown outcome<extra></extra>"))
    fig.update_xaxes(tickvals=[5, 10, 20, 30], ticktext=["5%", "10%", "20%", "30%"], title="Review budget (share of all "
                     "eligible origins)", showgrid=False)
    fig.update_yaxes(tickformat=".0%", title="Share of failures caught", range=[0, 0.8])
    ui.plot(ui.style(fig, height=420), key="cap_all")
    st.caption("Dots: recall among quotes with an observed outcome. Vertical bars: extreme bounds on recall of all "
               "failures when the 4,889 unknown outcomes are allocated adversely or favourably. Bounds, not confidence "
               "intervals; they overlap heavily across rules.")
    data_panel(["all_origin_capacity_bounds.csv"], "allcap")

    st.subheader("Phase 1: matched-sample queues")
    ui.callout("These queues rank only quotes that were later reobserved, so they condition on the future. They are "
               "kept for transparency; the corrected all-origin view above is the one to interpret.", "caution")
    c1, c2 = st.columns(2)
    lag = c1.selectbox("History information scenario", list(LAGS), format_func=LAGS.get, key="cap_lag")
    c = table(f"model_capacity_{lag}.csv")
    sub = c2.selectbox("Test subset", c.subset.unique().tolist(), format_func=SUBSETS.get, key="cap_subset")
    rule_opts = MODELS[2:] + ["R_highest_cost_rule"]
    sel = st.multiselect("Rules", rule_opts, default=["M1_hist_gbm", "L2_spline_logistic", "B2_history",
                                                      "R_highest_cost_rule"], format_func=NAMES.get, key="cap_rules")
    cc = c[(c.subset == sub) & c.rule.isin(sel)]
    if not cc.empty:
        fig = go.Figure()
        for rule in [r for r in rule_opts if r in sel]:
            d = cc[cc.rule == rule].sort_values("capacity")
            fig.add_trace(go.Scatter(x=d.capacity, y=d.failures_captured_per_quarter, mode="lines+markers",
                                     name=NAMES[rule], line=dict(color=COLORS[rule], width=2),
                                     marker=dict(size=9, line=dict(color="#fff", width=2)),
                                     customdata=d[["failures_total", "recall_per_quarter"]],
                                     hovertemplate=f"<b>{NAMES[rule]}</b> · %{{x:.0%}}<br>%{{y:,}} of "
                                                   "%{customdata[0]:,} failures (%{customdata[1]:.1%})<extra></extra>"))
        fig.update_xaxes(tickvals=[0.1, 0.2, 0.3], tickformat=".0%", title="Review capacity (share of quotes per "
                         "origin quarter)", showgrid=False)
        fig.update_yaxes(title="Observed failures captured", tickformat=",")
        ui.plot(ui.style(fig, height=400), key="cap_curve")
    st.caption("B0 and B1 are constant and cannot rank quotes, so they are omitted from capacity rankings.")
    download(f"model_capacity_{lag}.csv", "cap")
    st.subheader("Difference at 20% capacity (corridor bootstrap, 300 reps)")
    st.dataframe(table(f"model_capacity_diff_{lag}.csv"), hide_index=True, width="stretch")
    download(f"model_capacity_diff_{lag}.csv", "capd")
    st.subheader("20% capacity by target year (history lag 0)")
    cy = table("presentation_capacity_by_year_lag0.csv")
    cy = cy[cy.rule.isin(sel)]
    if not cy.empty:
        fig = go.Figure()
        for rule in [r for r in rule_opts if r in sel]:
            d = cy[cy.rule == rule]
            fig.add_trace(go.Bar(x=d.target_year.astype(str), y=d.recall, name=NAMES[rule],
                                 marker=dict(color=COLORS[rule], cornerradius=4),
                                 customdata=d[["failures_captured", "failures_total"]],
                                 hovertemplate=f"<b>{NAMES[rule]}</b> · %{{x}}<br>%{{y:.1%}} (%{{customdata[0]:,}} of "
                                               "%{customdata[1]:,})<extra></extra>"))
        fig.update_layout(barmode="group", bargap=0.25, bargroupgap=0.08)
        fig.update_yaxes(tickformat=".0%", title="Share of observed failures captured")
        fig.update_xaxes(title="Target year", showgrid=False)
        ui.plot(ui.style(fig, height=380), key="cap_year")
    download("presentation_capacity_by_year_lag0.csv", "capy")


def reobservation():
    ui.page_head("Negative result", "Reobservation model: a negative result",
                 "A separate question: is an eligible cheap quote reobserved at all, given its corridor is surveyed next "
                 "quarter? A ridge logistic model did not beat training prevalence in 2022 or 2023, was roughly tied in "
                 "2024, and won only in 2025 (a single transition, 2024Q4→2025Q1).")
    lag = st.selectbox("History information scenario", list(LAGS), format_func=LAGS.get, key="reob_lag")
    r = table(f"reobservation_metrics_{lag}.csv")
    fig = go.Figure()
    for mdl, colour, name in [("prevalence", GREY, "Training prevalence"), ("corridor_history", AQUA, "Corridor history"),
                              ("ridge_logistic", VIOLET, "Ridge logistic")]:
        d = r[r.model == mdl].sort_values("test_target_year")
        fig.add_trace(go.Scatter(x=d.test_target_year.astype(str), y=d.brier, mode="lines+markers", name=name,
                                 line=dict(color=colour, width=2), marker=dict(size=9, line=dict(color="#fff", width=2)),
                                 customdata=d[["n", "prevalence_stay", "auroc"]],
                                 hovertemplate=f"<b>{name}</b> · %{{x}}<br>Brier %{{y:.4f}}<br>%{{customdata[0]:,}} rows · "
                                               "reobserved share %{customdata[1]:.3f}<br>AUROC %{customdata[2]:.3f}"
                                               "<extra></extra>"))
    fig.update_yaxes(title="Brier score (lower is better)")
    fig.update_xaxes(title="Target year", showgrid=False)
    ui.plot(ui.style(fig, height=400), key="reob")
    ui.callout("A better price-conditional model therefore does not imply useful prediction of service availability. "
               "The negative result is preserved deliberately.", "note")
    data_panel([f"reobservation_metrics_{lag}.csv"], "reob")


def geography():
    ui.page_head("Subgroups", "Geography & support gates",
                 "Models were trained globally. Subgroup metrics require ≥100 observed failures; region and corridor "
                 "aggregates require ≥100 test rows and ≥20 failures. Unsupported groups are shown as unsupported, never as zero.")
    st.subheader("Continuity by receiving region (Phase 3, all years)")
    s = table("measurement_sensitivities.csv")
    s = s[s.stratum_field == "region"].copy()
    s["label"] = [stratum_label("region", x) for x in s.stratum]
    wide = s.pivot_table(index="label", columns=s.scenario.str.split("_").str[-1],
                         values=["conditional", "lower", "upper"]).reset_index()
    wide.columns = [c if not t else f"{c}_{t}" for c, t in wide.columns]
    wide = wide.sort_values("conditional_core", ascending=False)
    ui.plot(range_dot_figure(wide, "label", [("core", "Core", BLUE, "rgba(42,120,214,0.30)"),
                                             ("strict", "Strict", ORANGE, "rgba(235,104,52,0.30)")],
                             "Share still ≤3% next quarter"), key="geo_region_meas")
    st.caption("Sub-Saharan Africa has the lowest matched continuity and among the widest bounds. Regions are the World "
               "Bank region of the receiving country as published in the source.")
    s_sup = table("subgroup_support.csv")
    scope = st.radio("Support table scope", s_sup.scope.unique().tolist(), horizontal=True, key="sg_scope")
    st.dataframe(s_sup[s_sup.scope == scope], hide_index=True, width="stretch")
    st.caption("Uganda: 3 receiving corridors; **no corridors send from Uganda** in the source (sending-Uganda "
               "filter unsupported).")
    download("subgroup_support.csv", "sg")
    st.subheader("Globally trained model metrics within African subgroups (pooled test, lag 0)")
    sm = table("subgroup_model_metrics_lag0.csv")
    g = st.selectbox("Group", sm.group.unique().tolist(), key="sg_group")
    sg = sm[sm.group == g].dropna(axis=1, how="all")
    if (sg.model == "(not reported)").any():
        st.warning(f"{g}: support gate not met — {sg.iloc[0].get('note', '')}")
    st.dataframe(sg, hide_index=True, width="stretch")
    download("subgroup_model_metrics_lag0.csv", "sgm")
    st.subheader("Receiving-region model performance (gated)")
    rg = table("presentation_region_metrics_lag0.csv")
    sup = rg[rg.supported].copy()
    sup["label"] = [stratum_label("region", x) for x in sup.destination_region]
    fig = go.Figure()
    for mdl in DEFAULT_MODELS:
        fig.add_trace(go.Scatter(x=sup[f"brier_{mdl}"], y=sup.label, mode="markers", name=NAMES[mdl],
                                 marker=dict(size=11, color=COLORS[mdl], line=dict(color="#fff", width=2)),
                                 customdata=sup[["n", "observed_failures"]],
                                 hovertemplate=f"<b>%{{y}}</b><br>{NAMES[mdl]}: %{{x:.4f}}<br>%{{customdata[0]:,}} rows · "
                                               "%{customdata[1]:,} failures<extra></extra>"))
    fig.update_xaxes(title="Brier score (lower is better)")
    fig.update_yaxes(showgrid=False)
    ui.plot(ui.style(fig, height=140 + 46 * len(sup)), key="geo_region")
    data_panel(["presentation_region_metrics_lag0.csv"], "region", frame=rg)
    st.subheader("Corridor-level performance (gated; ISO3 sending>receiving)")
    co = table("presentation_corridor_metrics_lag0.csv")
    cs = co[co.supported]
    st.caption(f"{int(co.supported.sum())} of {len(co)} test corridors meet the gate. Points: HistGBM minus spline "
               "Brier per corridor (negative favours HistGBM). Not a held-out-corridor validation.")
    fig = go.Figure(go.Scatter(x=cs.n, y=cs.gbm_minus_spline, mode="markers",
                               marker=dict(size=9, color=[BLUE if v < 0 else ORANGE for v in cs.gbm_minus_spline],
                                           opacity=0.8, line=dict(color="#fff", width=1)),
                               customdata=cs[["corridor", "observed_failures", "observed_stay_rate"]],
                               hovertemplate="<b>%{customdata[0]}</b><br>%{x:,} test rows · %{customdata[1]} failures<br>"
                                             "Stay rate %{customdata[2]:.3f}<br>GBM − spline %{y:+.4f}<extra></extra>"))
    fig.add_hline(y=0, line=dict(color=MUTED, dash="dot", width=1.5))
    fig.update_xaxes(type="log", title="Test rows in corridor (log scale)")
    fig.update_yaxes(title="Brier: HistGBM − spline", tickformat="+.3f")
    ui.plot(ui.style(fig, height=380, legend=False), key="geo_corr")
    data_panel(["presentation_corridor_metrics_lag0.csv"], "corr", frame=co)
    st.subheader("Provider-level distribution (anonymous)")
    st.caption("Provider names are deliberately not shown (no provider assessment); filter by provider is "
               "unsupported. Statistics summarise providers meeting the gate.")
    st.dataframe(table("presentation_provider_distribution_lag0.csv"), hide_index=True, width="stretch")
    download("presentation_provider_distribution_lag0.csv", "prov")


def verdict():
    notice = json.loads((ROOT / "research_completion/assessment/dashboard_notice.json").read_text(encoding="utf-8"))
    ui.page_head("Decision", "Verdict & publication gates",
                 "The project is judged against explicit publication gates. Passing code and attractive charts do not "
                 "change a gate; only new evidence can.")
    ui.callout("<b>CONDITIONAL_HOLD.</b> A careful retrospective measurement result is demonstrated: identity rules "
               "substantially widen all-origin bounds while leaving matched continuity almost unchanged. Substantial "
               "novelty and externally validated service identity are not yet demonstrated. No operational model is "
               "selected and no submission-ready manuscript is claimed. "
               f"<a href='{REPO_URL}/blob/main/research_completion/phase3/followup_20261021/autonomous_review/FINAL_PUBLICATION_DECISION.md'>"
               "Read the current follow-up verdict</a>.", "caution")
    ui.callout("<b>External-evidence update, 21 October:</b> Lim's complete author v1.1 manuscript and code "
               "have now been reviewed; the exact continuity/bounds contrast was not found. Official Q2 2021 and "
               "Q4 2022 classification changes were verified. The autonomous historical investigation is complete: "
               "all 60 cases remain unresolved (grades A/B/C/D: 0/2/47/11). No human validation occurred. "
               "Substantial novelty remains unconfirmed; no manual case review is requested.", "info")
    st.subheader("Original Phase 3 gate snapshot (before external-evidence follow-up)")
    ui.gate_rows(table("PUBLICATION_GATE_MATRIX.csv"))
    download("PUBLICATION_GATE_MATRIX.csv", "gates3")
    st.subheader("Evidence and remaining limits")
    ui.cards([
        ("Evidence obtained", "Author v1.1 reviewed",
         "<p>Lim's full manuscript, replication code and reported outputs were read. Exact endpoint overlap was "
         "not found in that version; this does not establish substantial novelty.</p>"),
        ("Investigation complete", "60 unresolved cases",
         "<p>Historical documents give partial or contextual support. None establishes the full bundle in both "
         "quarters. Machine consistency checks are not independent human validation.</p>"),
        ("Publication decision", "Conditional hold",
         "<p>Do not submit the original article now. Product interpretation and substantial originality remain "
         "unconfirmed. The completed conditional dossier preserves the defensible record-based findings.</p>"),
    ], accent=YELLOW)
    st.subheader("Phase 2 completion record")
    st.caption(f"Analysis: {notice['analysis_date']} UTC; source cutoff: 2025Q3 (2025Q2 absent). "
               f"Model status: {notice['operational_model']}; independent confirmation: {notice['confirmation']}. "
               "Downloads serve committed aggregate files exactly; World Bank RPW, CC BY 4.0, no endorsement.")
    with st.expander("Phase 2 publication gates", icon=":material/fact_check:"):
        ui.gate_rows(table("publication_gates.csv"))
    with st.expander("Identity and missingness sensitivity grid", icon=":material/table_view:"):
        st.dataframe(table("sensitivity_grid.csv"), hide_index=True, width="stretch")
    with st.expander("Conventional reference comparisons (selected policy, crossed resampling)",
                     icon=":material/table_view:"):
        references = table("conventional_reference_comparisons.csv")
        st.dataframe(references[(references.model == "S_selected") &
                                (references.resampling == "crossed_corridor_provider_time_block")],
                     hide_index=True, width="stretch")
    cols = st.columns(3)
    for i, name in enumerate(list(COMPLETION_FILES)[:7]):
        with cols[i % 3]:
            download(name, "completion_" + name)


def reproducibility():
    ui.page_head("Reproducibility", "Reproducibility & limitations",
                 "Every number on this site comes from a committed aggregate file produced by versioned code from one "
                 "checksum-verified source file.")
    rep = RESULTS / "reproduction" / "reproduction_report.json"
    if rep.exists():
        r = json.loads(rep.read_text(encoding="utf-8"))
        ui.stats([
            ("Phase 1 raw-to-result tables matched", f"{r['n_match']} / {r['n_tables']}",
             f"Within atol/rtol {r['tolerance']['atol']:g}; others differ only in wall-clock fit time", AQUA),
            ("Phase 3 independent count checks", "20 / 20", "Separate parser, no shared modelling code", AQUA),
            ("Strict 1e-9 legacy comparator", "14 differ", "14 exact, 2 timing-only; retained as a documented failure",
             ui.RED),
            ("Seed / scikit-learn", f"{r['seed']} / {r['sklearn']}", f"Python {r['python']} · commit "
                                                                     f"<code>{r['code_commit'][:7]}</code>", BLUE),
        ])
        st.markdown(f"**Raw-to-result reproduction from the cached official workbook** (real data): "
                    f"{r['n_match']} of {r['n_tables']} frozen tables matched within atol/rtol "
                    f"{r['tolerance']['atol']:g}; run {r['run_at_utc']} at commit `{r['code_commit'][:7]}`. "
                    f"Non-matching: {', '.join(r['non_matching']) or 'none'}.")
        data_panel(["table_comparison.csv"], "repro", label="Table-by-table comparison")
    else:
        st.warning("No reproduction report found.")
    st.caption("The dashboard's own automated tests (AppTest) check rendering and table consistency on the committed "
               "aggregates; they are not a data reproduction.")
    st.subheader("Limitations")
    ui.cards([
        ("Timing", "No verified lead time",
         "<p>Historical RPW wave release dates could not be reconstructed, so no forecasting or operational claim is "
         "made. All test years were inspected before Phase 2.</p>"),
        ("Identity", "Exact keys only",
         "<p>Normalised exact matching probably under-links renamed services and may merge distinct offerings. No "
         "human adjudication occurred; all 60 autonomous documentary assessments remain unresolved.</p>"),
        ("Missingness", "Unknown ≠ exit",
         "<p>Bounds are wide because missing successors can reflect coverage, metadata changes or price availability. "
         "None is assumed.</p>"),
        ("Inference", "Few independent waves",
         "<p>13 target quarters for model comparisons and 36 origin waves for measurement limit precision; reported "
         "intervals are sensitivities.</p>"),
        ("Scope", "Survey offers",
         "<p>Quotes are not transactions; quote weights are not volumes; Uganda subgroups are below support gates.</p>"),
        ("Novelty", "Unresolved",
         "<p>Same-source firm/service analyses exist. Lim's author v1.1 is now reviewed; exact endpoint overlap "
         "was not found, but substantial contribution remains unconfirmed.</p>"),
    ], accent=ui.RED)
    st.subheader("Run it locally")
    st.code("pip install -r dashboard/requirements.txt\nstreamlit run dashboard/app.py", language="bash")


PAGES = dict(zip(SECTIONS, [overview, background, provenance, linkage, bounds, measurement, model_comparison,
                            time_forward, calibration, capacity, reobservation, geography, verdict, reproducibility]))


def sidebar() -> str:
    with st.sidebar:
        st.markdown(
            "<div style='padding:0.2rem 0 0.9rem'><div style='font-size:0.7rem;letter-spacing:0.14em;font-weight:700;"
            "color:#6da7ec;text-transform:uppercase'>Research programme R01</div><div style='font-size:1.15rem;"
            "font-weight:750;color:#fff;line-height:1.3;margin-top:0.2rem'>Remittance quote continuity</div></div>",
            unsafe_allow_html=True)
        section = st.radio("Explore", SECTIONS, key="section")
        st.markdown(f"<div style='margin-top:1.2rem;font-size:0.84rem;line-height:1.7'>"
                    f"<a href='{REPO_URL}'>Source code &amp; protocol ↗</a><br>"
                    f"<a href='{REPO_URL}/blob/main/research_completion/phase3/START_HERE_PHASE3.md'>"
                    "Phase 3 dossier ↗</a><br>"
                    "<a href='https://remittanceprices.worldbank.org'>World Bank RPW ↗</a></div>",
                    unsafe_allow_html=True)
        st.caption("Research dashboard, not a consumer service. Aggregates only.")
    return section


def main():
    st.set_page_config(page_title="Remittance Quote Continuity · R01", page_icon=":material/currency_exchange:",
                       layout="wide", initial_sidebar_state="expanded")
    ui.inject_css()
    section = sidebar()
    if section != "Overview":
        ribbon()
    PAGES[section]()
    caveats()
    ui.footer("Isaac Omoding · R01 research programme · Data: The World Bank, Remittance Prices Worldwide (CC BY 4.0). "
              "The World Bank does not endorse this analysis. Built with Streamlit and Plotly; code and documents "
              "produced with AI assistance (Claude Code) under investigator direction.")


main()
