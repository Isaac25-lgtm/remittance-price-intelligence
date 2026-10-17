"""Source-grounded figures from aggregate result tables only (no row-level data)."""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from . import config  # noqa: E402

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e4e3df"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
GRAY = "#9a9893"
T, Fg = config.TABLES_DIR, config.FIGURES_DIR

NAMES = {"B0_always_stay": "Always stays ≤3%", "B1_prevalence": "Training prevalence",
         "B2_history": "Shrunk provider/corridor history", "B3_cost_logistic": "Current-cost logistic",
         "L1_ridge_logistic": "Ridge logistic", "L2_spline_logistic": "Spline logistic",
         "M1_hist_gbm": "HistGradientBoosting", "M2_random_forest": "Random forest",
         "R_highest_cost_rule": "Highest current cost rule"}


def _style(ax, title, xlabel=None, ylabel=None):
    ax.set_facecolor(SURFACE)
    ax.figure.set_facecolor(SURFACE)
    ax.set_title(title, loc="left", color=INK, fontsize=11, fontweight="bold")
    if xlabel:
        ax.set_xlabel(xlabel, color=INK2, fontsize=9)
    if ylabel:
        ax.set_ylabel(ylabel, color=INK2, fontsize=9)
    ax.tick_params(colors=INK2, labelsize=8)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax.spines[s].set_color(GRID)
    ax.grid(axis="y", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def _save(fig, name, note):
    fig.text(0.01, 0.005, note, fontsize=7, color=INK2, ha="left", va="bottom")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    Fg.mkdir(parents=True, exist_ok=True)
    fig.savefig(Fg / f"{name}.png", dpi=160)
    plt.close(fig)


SRC = "Source: World Bank, Remittance Prices Worldwide (rpw_dataset_2011_2025_q3.xlsx, sha256 f1d7265b…)."


def coverage():
    c = pd.read_csv(T / "audit_quarter_coverage.csv")
    fig, ax = plt.subplots(figsize=(9, 3.4))
    x = np.arange(len(c))
    ax.bar(x, c["rows"].fillna(0), color=BLUE, width=0.8)
    miss = c[~c["present_in_source"]]
    for i in miss.index:
        ax.annotate("absent in\nsource", (i, 0), xytext=(i, c["rows"].max() * 0.35), ha="center",
                    fontsize=7, color=INK, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
    ax.set_xticks(x[::4], c["quarter"].iloc[::4])
    _style(ax, "Published quotes per survey quarter (post-Q2 2016 sheet)", ylabel="Quotes (rows)")
    _save(fig, "fig1_quarter_coverage", SRC + " 2025Q2 is not in the file.")


def linkage():
    q = pd.read_csv(T / "linkage_status_by_origin_quarter.csv")
    q = q[q["right_censored_last_quarter"] == 0]
    denom = q["quotes"] - q["origin_key_ambiguous"]
    fig, ax = plt.subplots(figsize=(9, 3.4))
    ax.plot(q["origin_quarter"], q["core_reobserved"] / denom, color=BLUE, lw=2, marker="o", ms=3,
            label="Core service reobserved in t+1")
    ax.plot(q["origin_quarter"], q["corridor_not_surveyed_next_quarter"] / denom, color=ORANGE, lw=2,
            marker="o", ms=3, label="Corridor not surveyed in t+1")
    ax.set_ylim(0, 1)
    ax.set_xticks(range(0, len(q), 4), q["origin_quarter"].iloc[::4])
    _style(ax, "Share of uniquely-keyed quotes linked to the exactly-next quarter (all costs)",
           xlabel="Origin quarter", ylabel="Share of quotes")
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    _save(fig, "fig2_linkage_by_quarter", SRC + " Denominator excludes keys duplicated within a quarter.")


def bounds():
    b = pd.read_csv(T / "estimand_bounds_by_year.csv")
    b = b[b["n_eligible"] >= 100]
    fig, ax = plt.subplots(figsize=(9, 3.6))
    x = b["target_year"].to_numpy()
    ax.vlines(x, b["lower_bound"], b["upper_bound"], color=GRAY, lw=6, alpha=0.6,
              label="Worst/best-case bound (all eligible cheap origins)")
    ax.plot(x, b["conditional_p_stay_core"], "o", color=BLUE, ms=6, label="Conditional on core reobservation")
    ax.plot(x, b["conditional_p_stay_strict"], "s", color=ORANGE, ms=5, label="Conditional on strict reobservation")
    ax.set_ylim(0.3, 1)
    _style(ax, "Next-quarter continuity of a ≤3% quote: conditional estimate vs missing-outcome bounds",
           xlabel="Target year", ylabel="P(cost stays ≤3%)")
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    _save(fig, "fig3_continuity_bounds", SRC + " Missing ≠ exit: bounds allocate every unobserved outcome to fail or stay.")


def models(tag="lag0"):
    m = pd.read_csv(T / f"model_metrics_{tag}.csv")
    m = m[(m["subset"] == "pooled_2022_2025") & (m["model"] != "B0_always_stay")].sort_values("brier")
    d = pd.read_csv(T / f"model_paired_diffs_{tag}.csv")
    fig, ax = plt.subplots(figsize=(8, 3.8))
    y = np.arange(len(m))
    simple = m["model"].str.startswith("B")
    ax.barh(y, m["brier"], color=np.where(simple, GRAY, BLUE), height=0.55)
    for yi, v in zip(y, m["brier"]):
        ax.text(v + 0.0005, yi, f"{v:.4f}", va="center", fontsize=8, color=INK)
    ax.set_yticks(y, [NAMES[n] for n in m["model"]])
    ax.set_xlim(0.12, m["brier"].max() + 0.006)
    ax.invert_yaxis()
    _style(ax, "Brier score on identical pooled test rows, targets 2022–2025Q1 (lower is better)",
           xlabel="Brier score (axis starts at 0.12)")
    ax.grid(axis="x", color=GRID, linewidth=0.6)
    ax.grid(axis="y", visible=False)
    r = d[(d.subset == "pooled_2022_2025") & (d.model_a == "M1_hist_gbm") & (d.model_b == "L2_spline_logistic")]
    txt = "; ".join(f"{c.replace('_key','').replace('__n','')}-clustered 95% CI [{lo:.4f}, {hi:.4f}]"
                    for c, lo, hi in zip(r.cluster, r.ci95_lo, r.ci95_hi))
    _save(fig, f"fig4_model_brier_{tag}", f"HGB − spline = {r.brier_diff_a_minus_b.iloc[0]:.4f} ({txt}).\n"
          "Retrospective backtest; test years previously inspected. Gray = simple baselines.")


def reliability(tag="lag0"):
    r = pd.read_csv(T / f"model_reliability_{tag}.csv")
    fig, ax = plt.subplots(figsize=(5, 4.6))
    ax.plot([0, 1], [0, 1], color=GRAY, lw=1, ls="--", label="Perfect calibration")
    for n, c in [("M1_hist_gbm", BLUE), ("L2_spline_logistic", ORANGE), ("B2_history", AQUA)]:
        s = r[r.model == n]
        ax.plot(s["mean_pred"], s["obs_rate"], color=c, lw=2, marker="o", ms=4, label=NAMES[n])
    ax.set_xlim(0.2, 1)
    ax.set_ylim(0.2, 1)
    _style(ax, "Reliability (deciles), pooled test", xlabel="Mean predicted P(stays ≤3%)",
           ylabel="Observed share staying ≤3%")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _save(fig, f"fig5_reliability_{tag}", "Conditional on core reobservation.")


def capacity(tag="lag0"):
    c = pd.read_csv(T / f"model_capacity_{tag}.csv")
    c = c[c.subset == "pooled_2022_2025"]
    fig, ax = plt.subplots(figsize=(7, 3.8))
    for n, col in [("M1_hist_gbm", BLUE), ("L2_spline_logistic", ORANGE), ("R_highest_cost_rule", GRAY)]:
        s = c[c.rule == n]
        ax.plot(s["capacity"] * 100, s["failures_captured_per_quarter"], color=col, lw=2, marker="o", ms=5,
                label=NAMES[n])
        last = s.iloc[-1]
        ax.text(last["capacity"] * 100 + 0.6, last["failures_captured_per_quarter"],
                f"{int(last['failures_captured_per_quarter'])}", fontsize=8, color=INK, va="center")
    tot = int(c["failures_total"].iloc[0])
    ax.set_xticks([10, 20, 30], ["10%", "20%", "30%"])
    ax.set_xlim(8, 34)
    _style(ax, f"Observed failures captured by a hypothetical review list (of {tot:,})",
           xlabel="Review capacity per origin quarter", ylabel="Failures captured")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _save(fig, f"fig6_review_capacity_{tag}", "Hypothetical triage of reobserved quotes; no consumer savings are observed or implied.")


def main():
    coverage()
    linkage()
    bounds()
    models()
    reliability()
    capacity()


if __name__ == "__main__":
    main()
