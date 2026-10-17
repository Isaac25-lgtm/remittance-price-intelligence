"""Aggregate-only presentation tables from the CACHED frozen-spec test predictions.

No model is fitted here. Inputs: data/processed/test_predictions_lag{0,1}.parquet (gitignored).
Outputs (results/tables/presentation_*.csv) contain no quote, service, or provider identifiers.

Support gate (pre-specified before computing): a group's metrics are shown only if it has
n >= 100 test rows AND >= 20 observed failures; otherwise the row is kept with supported=False
and blank metrics. Provider-level results are released only as an anonymous distribution
(no provider names), because the model card excludes provider assessment.

Bootstrap intervals resample corridors (or providers) within the SAME time-forward test rows;
they are NOT held-out-corridor or held-out-provider validation (none was performed).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from rpi import config
from rpi.evaluate import capture_at_capacity, reliability_bins
from rpi.models import MODELS

T = config.TABLES_DIR
MIN_N, MIN_FAIL, N_BOOT = 100, 20, 1000
MODEL_NAMES = list(MODELS)
SUBSETS = {"pooled_2022_2025": lambda d: np.ones(len(d), bool),
           "pooled_2022_2024": lambda d: d["target_year"].isin([2022, 2023, 2024]).to_numpy(),
           **{f"year_{y}": (lambda y: lambda d: (d["target_year"] == y).to_numpy())(y)
              for y in [2022, 2023, 2024, 2025]}}


def cluster_ci(loss: np.ndarray, clusters: np.ndarray, seed: int) -> tuple[float, float]:
    g = pd.DataFrame({"l": loss, "c": clusters}).groupby("c")["l"].agg(["sum", "size"])
    s, n = g["sum"].to_numpy(), g["size"].to_numpy()
    idx = np.random.default_rng(seed).integers(0, len(g), size=(N_BOOT, len(g)))
    b = s[idx].sum(1) / n[idx].sum(1)
    return float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def model_brier_ci(P: pd.DataFrame, tag: str) -> pd.DataFrame:
    y = P["y"].astype(float).to_numpy()
    rows = []
    for sub, f in SUBSETS.items():
        m = f(P)
        for name in MODEL_NAMES:
            loss = (P[name].to_numpy() - y) ** 2
            lc = cluster_ci(loss[m], P["corridor_key"].to_numpy()[m], config.SEED)
            lp = cluster_ci(loss[m], P["firm__n"].to_numpy()[m], config.SEED)
            rows.append({"release_lag": tag, "subset": sub, "model": name, "n": int(m.sum()),
                         "brier": float(loss[m].mean()),
                         "corridor_boot_lo": lc[0], "corridor_boot_hi": lc[1],
                         "provider_boot_lo": lp[0], "provider_boot_hi": lp[1],
                         "n_corridors": int(P.loc[m, "corridor_key"].nunique()),
                         "n_providers": int(P.loc[m, "firm__n"].nunique())})
    return pd.DataFrame(rows)


def group_metrics(P: pd.DataFrame, col: str, label: str) -> pd.DataFrame:
    rows = []
    for g, d in P.groupby(col):
        y = d["y"].astype(float).to_numpy()
        n, fails = len(d), int((1 - y).sum())
        r = {label: g, "n": n, "observed_failures": fails, "observed_stay_rate": float(y.mean()),
             "supported": bool(n >= MIN_N and fails >= MIN_FAIL)}
        if r["supported"]:
            for name in MODEL_NAMES:
                r[f"brier_{name}"] = float(((d[name] - y) ** 2).mean())
            r["gbm_minus_spline"] = r["brier_M1_hist_gbm"] - r["brier_L2_spline_logistic"]
        rows.append(r)
    return pd.DataFrame(rows)


def provider_distribution(P: pd.DataFrame) -> pd.DataFrame:
    g = group_metrics(P, "firm__n", "provider")
    sup = g[g["supported"]]
    rows = [{"statistic": "providers_in_test", "value": float(len(g))},
            {"statistic": "providers_meeting_gate", "value": float(len(sup))},
            {"statistic": "test_rows_in_gated_providers", "value": float(sup["n"].sum())}]
    for name in MODEL_NAMES:
        q = sup[f"brier_{name}"].quantile([0.25, 0.5, 0.75])
        rows += [{"statistic": f"brier_{name}_p25", "value": float(q.loc[0.25])},
                 {"statistic": f"brier_{name}_median", "value": float(q.loc[0.5])},
                 {"statistic": f"brier_{name}_p75", "value": float(q.loc[0.75])}]
    rows.append({"statistic": "share_gated_providers_gbm_better_than_spline",
                 "value": float((sup["gbm_minus_spline"] < 0).mean())})
    return pd.DataFrame(rows)


def capacity_by_year(P: pd.DataFrame) -> pd.DataFrame:
    y = P["y"].astype(int).to_numpy()
    scores = {n: 1 - P[n].to_numpy() for n in MODEL_NAMES if n not in ("B0_always_stay", "B1_prevalence")}
    scores["R_highest_cost_rule"] = P["cost"].to_numpy()
    rows = []
    for yr in sorted(P["target_year"].unique()):
        m = (P["target_year"] == yr).to_numpy()
        for n, s in scores.items():
            got, k, tot = capture_at_capacity(P[m], s[m], y[m], 0.20)
            rows.append({"target_year": int(yr), "rule": n, "capacity": 0.20, "reviewed": k,
                         "failures_captured": got, "failures_total": tot, "recall": got / tot})
    return pd.DataFrame(rows)


def reliability_all(P: pd.DataFrame, tag: str) -> pd.DataFrame:
    """Decile reliability for ALL eight families (the frozen run stored only four), using the same
    rpi.evaluate.reliability_bins on the same pooled test rows."""
    y = P["y"].astype(int).to_numpy()
    return pd.concat([reliability_bins(y, P[n].to_numpy()).assign(model=n, release_lag=tag)
                      for n in MODEL_NAMES if P[n].nunique() > 1])


def main():
    out, rel = [], []
    for tag in ["lag0", "lag1"]:
        P = pd.read_parquet(config.PROCESSED_DIR / f"test_predictions_{tag}.parquet")
        out.append(model_brier_ci(P, tag))
        rel.append(reliability_all(P, tag))
        if tag == "lag0":
            group_metrics(P, "destination_region", "destination_region").to_csv(
                T / "presentation_region_metrics_lag0.csv", index=False)
            c = group_metrics(P, "corridor_key", "corridor")
            c.to_csv(T / "presentation_corridor_metrics_lag0.csv", index=False)
            provider_distribution(P).to_csv(T / "presentation_provider_distribution_lag0.csv", index=False)
            capacity_by_year(P).to_csv(T / "presentation_capacity_by_year_lag0.csv", index=False)
            print("corridors gated:", int(c.supported.sum()), "of", len(c))
    pd.concat(out).to_csv(T / "presentation_model_brier_ci.csv", index=False)
    pd.concat(rel).to_csv(T / "presentation_reliability_all_families.csv", index=False)
    print("done")


if __name__ == "__main__":
    main()
