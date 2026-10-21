"""Presentation figures for the README, drawn from committed public aggregates only.

No modelling, no raw data. Re-run after any change to the aggregate tables:
    python scripts/readme_figures.py
Writes PNG files to docs/figures/.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.ticker import FuncFormatter, PercentFormatter  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RC = ROOT / "research_completion"
P3 = RC / "phase3"
OUT = ROOT / "docs" / "figures"

INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW, VIOLET, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#6250d6", "#9a9893"
NAVY = "#0d2240"
PRODUCTS = {"cc1_3pct": "USD 200 · 3% threshold\n(primary)", "cc1_5pct": "USD 200 · 5% threshold",
            "cc2_3pct": "USD 500 · 3% threshold", "cc2_5pct": "USD 500 · 5% threshold"}

plt.rcParams.update({
    "font.family": ["Segoe UI", "Arial", "DejaVu Sans"], "font.size": 11,
    "axes.edgecolor": "#c3c2b7", "axes.labelcolor": INK2, "axes.titlesize": 14, "axes.titleweight": "bold",
    "axes.titlecolor": INK, "axes.titlelocation": "left", "axes.titlepad": 30, "xtick.color": INK2,
    "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False, "figure.facecolor": "white",
    "savefig.facecolor": "white", "savefig.dpi": 170, "savefig.bbox": "tight", "savefig.pad_inches": 0.25,
})
PCT = PercentFormatter(1.0, decimals=0)


def note(fig, text: str, y: float = -0.02):
    fig.text(0.01, y, text, ha="left", va="top", fontsize=9.2, color=MUTED, wrap=True)


def subtitle(ax, text: str):
    ax.text(0, 1.025, text, transform=ax.transAxes, fontsize=10.5, color=INK2, va="bottom")


def save(fig, name: str):
    fig.savefig(OUT / name)
    plt.close(fig)
    print("wrote", name)


def headline_bounds():
    s = pd.read_csv(P3 / "identity" / "LINKAGE_SCENARIO_RESULTS.csv").set_index("scenario")
    fig, ax = plt.subplots(figsize=(11, 5.2))
    for i, p in enumerate(list(PRODUCTS)[::-1]):
        for rule, off, col in [("core", 0.16, BLUE), ("strict", -0.16, ORANGE)]:
            r = s.loc[f"{p}_{rule}"]
            ax.plot([r.lower, r.upper], [i + off] * 2, color=col, alpha=0.32, lw=10, solid_capstyle="round")
            ax.scatter(r.conditional, i + off, s=90, color=col, edgecolor="white", linewidth=2, zorder=3)
            if p == "cc1_3pct":
                ax.annotate(f"{r.lower:.0%}–{r.upper:.0%}", (r.upper, i + off), xytext=(10, 0),
                            textcoords="offset points", va="center", fontsize=10, color=INK2)
    ax.set_yticks(range(4), list(PRODUCTS.values())[::-1])
    ax.set_xlim(0.45, 1.0)
    ax.xaxis.set_major_formatter(PCT)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Share of initially cheap quotes still under the threshold next quarter")
    ax.set_title("Same matched estimate, very different certainty")
    subtitle(ax, "Dots: continuity among matched quotes · Bars: range for all eligible quotes when unknown "
                 "successors are counted as fail or stay")
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], color=BLUE, lw=8, alpha=0.4, label="Core identity bounds"),
               Line2D([], [], marker="o", color=BLUE, lw=0, ms=9, label="Core conditional"),
               Line2D([], [], color=ORANGE, lw=8, alpha=0.4, label="Strict identity bounds"),
               Line2D([], [], marker="o", color=ORANGE, lw=0, ms=9, label="Strict conditional")]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0, -0.13), ncol=4, fontsize=9.5)
    note(fig, "Bounds are identification ranges, not confidence intervals. Each row is a separate basket/threshold "
              "cohort. Source: World Bank RPW 2016Q2–2025Q3; aggregates in research_completion/phase3/identity.", y=-0.06)
    save(fig, "fig1_identity_bounds.png")


def wave_series():
    w = pd.read_csv(P3 / "tables" / "wave_measurement.csv")
    fig, ax = plt.subplots(figsize=(12, 5.2))
    for rule, col in [("strict", ORANGE), ("core", BLUE)]:
        d = w[(w.scenario == f"cc1_3pct_{rule}") & (w.valid > 0)].sort_values("qidx")
        x = range(len(d))
        ax.fill_between(x, d.lower, d.upper, color=col, alpha=0.16, lw=0, label=f"{rule.title()} bounds")
        ax.plot(x, d.conditional, color=col, lw=2, marker="o", ms=4.5, mec="white", mew=1,
                label=f"{rule.title()} conditional")
        labels = d.quarter.tolist()
    ax.set_xticks(range(0, len(labels), 2), labels[::2], rotation=45, ha="right")
    ax.set_xlim(-0.5, len(labels) - 0.5)
    ax.set_ylim(0.2, 1.0)
    ax.yaxis.set_major_formatter(PCT)
    ax.grid(axis="x", visible=False)
    ax.set_ylabel("Still ≤3% next quarter")
    ax.set_title("Continuity is stable; what we can say about all quotes is not")
    subtitle(ax, "USD 200 basket, 3% threshold, every origin survey wave with an observable successor")
    ax.legend(loc="lower left", ncol=4, fontsize=9.5)
    note(fig, "From 2021 the strict rule loses many links (changed speed/network attributes), so its bounds widen "
              "sharply while the matched estimate tracks the core rule. 2025Q1 is omitted: 2025Q2 is absent from the source.")
    save(fig, "fig2_wave_series.png")


def quote_flow():
    u = pd.read_csv(P3 / "tables" / "unknown_flow.csv").set_index("state")["count"]
    parts = [("Stays ≤3%", u["stay"], AQUA), ("Rises above 3%", u["fail"], ORANGE),
             ("Service not observed", u["service_not_observed"], "#8f8d87"),
             ("Ambiguous origin key", u["origin_key_ambiguous"], "#b0aea8"),
             ("Corridor not surveyed", u["corridor_not_surveyed"], "#c9c7c1"),
             ("Other unknown", u["invalid_target_cost"] + u["target_key_ambiguous"], "#dedcd6")]
    total = sum(v for _, v, _ in parts)
    fig, ax = plt.subplots(figsize=(12, 2.9))
    left = 0
    for i, (lab, v, col) in enumerate(parts):
        ax.barh(0, v, left=left, color=col, height=0.5, edgecolor="white", linewidth=2)
        cx = left + v / 2
        if i < 2:
            ax.text(cx, 0, f"{lab}\n{v:,} · {v / total:.0%}", ha="center", va="center", fontsize=10.5,
                    color="white", fontweight="semibold")
        left += v
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=c, label=f"{lab}: {v:,}") for lab, v, c in parts[2:]], loc="lower right",
              bbox_to_anchor=(1, 0.62), ncol=2, fontsize=9.5, alignment="left", title_fontsize=10,
              title=f"Unknown successor: {total - u['stay'] - u['fail']:,} · {(total - u['stay'] - u['fail']) / total:.0%}")
    ax.axvline(u["stay"] + u["fail"], color=INK, lw=1.2, ls=(0, (3, 3)))
    ax.text(u["stay"] + u["fail"], -0.42, "  ← observed outcome  |  unknown successor →", fontsize=9.5, color=INK2,
            ha="center", va="top")
    ax.set_xlim(0, total)
    ax.set_ylim(-0.6, 1.25)
    ax.axis("off")
    ax.set_title(f"Where the {total:,} cheap quotes went in the next quarter", pad=8)
    save(fig, "fig3_quote_flow.png")


def models():
    names = {"B0_always_stay": "Always stays ≤3%", "B1_prevalence": "Training prevalence",
             "B2_history": "Shrunk provider/corridor history", "B3_cost_logistic": "Current-cost logistic",
             "B4_recent_history": "Recent rolling history", "L1_ridge_logistic": "Ridge logistic",
             "L2_spline_logistic": "Spline logistic", "M1_hist_gbm": "HistGradientBoosting",
             "M2_random_forest": "Random forest", "S_selected": "Selected research policy"}
    fam = {"B": ("Baseline rule", GREY), "L": ("Conventional statistical", BLUE), "M": ("Machine learning", ORANGE),
           "S": ("Selected research policy", AQUA)}
    sc = pd.concat([pd.read_csv(RC / "models" / "model_comparison.csv"),
                    pd.read_csv(RC / "models" / "recent_history_reference.csv")])
    sc = sc[~sc.model.str.endswith("__cal")].sort_values("brier", ascending=False)
    j = pd.read_csv(RC / "models" / "joint_dependence_sensitivity.csv")
    j = j[j.analysis == "phase2"].iloc[::-1]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.4), gridspec_kw={"width_ratios": [1.25, 1], "wspace": 0.55})
    for i, r in enumerate(sc.itertuples()):
        lab, col = fam[r.model[0]]
        a1.barh(i, r.brier - 0.12, left=0.12, color=col, height=0.62)
        a1.text(r.brier + 0.0007, i, f"{r.brier:.4f}", va="center", fontsize=9, color=INK2)
    a1.set_yticks(range(len(sc)), [names[m] for m in sc.model])
    a1.set_xlim(0.12, 0.192)
    a1.grid(axis="y", visible=False)
    a1.set_xlabel("Brier score, 19,667 test records (lower is better; axis starts at 0.12)")
    a1.set_title("Retrospective scores")
    from matplotlib.patches import Patch
    a1.legend(handles=[Patch(color=c, label=l) for l, c in fam.values()], loc="upper right", fontsize=9)
    short = {"M1_hist_gbm": "HistGBM", "M2_random_forest": "Random forest", "S_selected": "Selected policy",
             "L2_spline_logistic": "spline", "B2_history": "history"}
    for i, r in enumerate(j.itertuples()):
        cross = r.ci95_lo <= 0 <= r.ci95_hi
        col = GREY if cross else BLUE
        a2.plot([r.ci95_lo, r.ci95_hi], [i, i], color=col, lw=2.2, solid_capstyle="round")
        a2.scatter(r.brier_diff, i, s=70, color=col, edgecolor="white", linewidth=1.8, zorder=3)
    a2.set_yticks(range(len(j)), [f"{short[a]} − {short[b]}" for a, b in zip(j.model_a, j.model_b)])
    a2.axvline(0, color="#d03b3b", lw=1.2, ls=(0, (3, 3)))
    a2.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:+.3f}"))
    a2.grid(axis="y", visible=False)
    a2.set_xlabel("Paired Brier difference (negative favours the first)")
    a2.set_title("Joint corridor × provider × time sensitivity")
    note(fig, "Grey: interval includes zero. Only 13 target quarters; a small simulation gave 0.86 coverage, so these "
              "are exploratory sensitivities, not validated 95% intervals. All test years were inspected before selection.")
    save(fig, "fig4_models.png")


def capacity():
    a = pd.read_csv(RC / "models" / "all_origin_capacity_bounds.csv")
    rules = [("S_selected", "Selected policy", "#0d366b"), ("L2_spline_logistic", "Spline logistic", ORANGE),
             ("B2_history", "History baseline", AQUA), ("R_highest_cost_rule", "Highest current cost", "#52514e")]
    fig, ax = plt.subplots(figsize=(11, 5))
    for i, (rule, lab, col) in enumerate(rules):
        d = a[a.rule == rule]
        x = d.capacity * 100 + (i - 1.5) * 1.1
        ax.vlines(x, d.all_failure_recall_lower, d.all_failure_recall_upper, color=col, lw=4, alpha=0.45)
        ax.scatter(x, d.recall_of_known_failures, color=col, s=60, edgecolor="white", linewidth=1.8, zorder=3, label=lab)
    ax.set_xticks([5, 10, 20, 30], ["5%", "10%", "20%", "30%"])
    ax.yaxis.set_major_formatter(PCT)
    ax.set_ylim(0, 0.8)
    ax.grid(axis="x", visible=False)
    ax.set_xlabel("Review budget (share of all eligible origins re-checked)")
    ax.set_ylabel("Share of failures caught")
    ax.set_title("Review queues: gains shrink once unknown outcomes are kept")
    subtitle(ax, "Dots: recall among quotes with an observed outcome · Bars: bounds on recall of all failures "
                 "(4,889 unknown outcomes)")
    ax.legend(loc="upper left", fontsize=9.5)
    save(fig, "fig5_review_capacity.png")


def regions():
    s = pd.read_csv(P3 / "tables" / "measurement_sensitivities.csv")
    s = s[s.stratum_field == "region"].copy()
    s["label"] = s.stratum.str.title().str.replace("&", "and").replace({"..": "Region not given in source"})
    core = s[s.scenario.str.endswith("core")].set_index("label")
    strict = s[s.scenario.str.endswith("strict")].set_index("label")
    order = core.sort_values("conditional").index
    fig, ax = plt.subplots(figsize=(11, 5.4))
    for i, lab in enumerate(order):
        for df, off, col in [(core, 0.15, BLUE), (strict, -0.15, ORANGE)]:
            r = df.loc[lab]
            ax.plot([r.lower, r.upper], [i + off] * 2, color=col, alpha=0.32, lw=8, solid_capstyle="round")
            ax.scatter(r.conditional, i + off, s=60, color=col, edgecolor="white", linewidth=1.6, zorder=3)
        ax.text(1.012, i, f"{int(core.loc[lab].n_eligible):,} quotes", va="center", ha="left", fontsize=9.5,
                color=MUTED, transform=ax.get_yaxis_transform(), clip_on=False)
    ax.set_yticks(range(len(order)), order)
    ax.set_xlim(0.4, 1.0)
    ax.xaxis.set_major_formatter(PCT)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Share still ≤3% next quarter (blue: core identity · orange: strict identity)")
    ax.set_title("Continuity by receiving region")
    subtitle(ax, "Sub-Saharan Africa has the lowest matched continuity and among the widest bounds")
    save(fig, "fig6_regions.png")


def coverage():
    cov = pd.read_csv(ROOT / "results" / "tables" / "audit_quarter_coverage.csv")
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 5.6), sharex=True, gridspec_kw={"hspace": 0.28,
                                                                                    "height_ratios": [1.3, 1]})
    x = range(len(cov))
    a1.bar(x, cov.rows.fillna(0), color=[BLUE if p else "white" for p in cov.present_in_source], width=0.72)
    for i, p in enumerate(cov.present_in_source):
        if not p:
            for a in (a1, a2):
                a.axvline(i, color="#d03b3b", ls=(0, (3, 3)), lw=1.4)
            a1.text(i, cov.rows.max() * 1.07, f"{cov.quarter[i]} absent", color="#d03b3b", ha="center", fontsize=9.5)
    a1.set_ylim(0, cov.rows.max() * 1.16)
    a1.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v / 1000:.0f}K"))
    a1.set_ylabel("Quotes")
    share = cov.cc1_cost_le3_share.dropna()
    a1.set_title(f"The survey: {cov.rows.min() / 1000:.1f}K–{cov.rows.max() / 1000:.1f}K quotes a quarter, and only "
                 f"{share.min():.0%}–{share.max():.0%} of USD 200 quotes cost ≤3%")
    a1.grid(axis="x", visible=False)
    present = cov[cov.present_in_source]
    a2.plot([i for i, p in zip(x, cov.present_in_source) if p], present.cc1_cost_le3_share, color=AQUA, lw=2,
            marker="o", ms=4, mec="white", mew=1)
    a2.yaxis.set_major_formatter(PCT)
    a2.set_ylim(0, None)
    a2.set_ylabel("USD 200 quotes ≤3%")
    a2.grid(axis="x", visible=False)
    a2.set_xticks(range(0, len(cov), 2), cov.quarter[::2], rotation=45, ha="right")
    save(fig, "fig0_survey_coverage.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    coverage()
    headline_bounds()
    wave_series()
    quote_flow()
    models()
    capacity()
    regions()
