"""R01 phase-1 pipeline: linkage -> features -> frozen model ladder -> metrics/uncertainty.

Usage: OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 python scripts/run_phase1.py [--release-lag 0]
Row-level predictions go to data/processed (gitignored); only aggregates go to results/.
"""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import time

import numpy as np
import pandas as pd
import sklearn
import yaml

from rpi import config, features as F, linkage as L
from rpi.evaluate import (capture_at_capacity, capture_pooled, cluster_bootstrap_diff, metric_row,
                          reliability_bins)
from rpi.models import MODELS
from rpi.preprocess import load_clean, qlabel

SPEC = yaml.safe_load((config.ROOT / "configs" / "experiment.yaml").read_text())
TEST_YEARS = SPEC["splits"]["test_target_years"]
CAPACITIES = [0.10, 0.20, 0.30]


def fit_predict(X: pd.DataFrame, release_lag: int):
    prim = X[X["primary"]].copy()
    preds, registry = [], []
    for year in TEST_YEARS:
        test = prim[prim["target_year"] == year]
        if test.empty:
            continue
        first_origin = int(test["qidx"].min())
        train = prim[prim["target_qidx"] < first_origin]
        assert train["target_qidx"].max() < test["qidx"].min()  # time-forward guard
        out = test[["source_row", "qidx", "target_qidx", "target_year", "corridor_key", "firm__n",
                    "source_code", "destination_code", "destination_region", "cost", "y"]].copy()
        for name, make in MODELS.items():
            t0 = time.time()
            m = make().fit(train, train["y"].astype(int))
            out[name] = m.predict_proba(test)[:, 1]
            registry.append({"model": name, "test_target_year": year, "release_lag": release_lag,
                             "n_train": len(train), "train_first_origin": qlabel(int(train["qidx"].min())),
                             "train_last_target": qlabel(int(train["target_qidx"].max())),
                             "n_test": len(test), "test_first_origin": qlabel(first_origin),
                             "fit_seconds": round(time.time() - t0, 2)})
            print(year, name, f"{time.time() - t0:.1f}s", flush=True)
        preds.append(out)
    return pd.concat(preds, ignore_index=True), pd.DataFrame(registry)


def summarise(P: pd.DataFrame, tag: str):
    names = list(MODELS)
    y = P["y"].astype(int).to_numpy()
    rows = []
    for subset, mask in [("pooled_2022_2025", np.ones(len(P), bool)),
                         ("pooled_2022_2024", P["target_year"].isin([2022, 2023, 2024]).to_numpy())] + \
                        [(f"year_{yr}", (P["target_year"] == yr).to_numpy()) for yr in TEST_YEARS]:
        for n in names:
            r = metric_row(y[mask], P.loc[mask, n].to_numpy())
            rows.append({"subset": subset, "model": n, **r})
    metrics = pd.DataFrame(rows)

    # paired differences vs strongest-simple and spline, clustered by corridor / provider
    diffs = []
    for subset, mask in [("pooled_2022_2025", np.ones(len(P), bool)),
                         ("pooled_2022_2024", P["target_year"].isin([2022, 2023, 2024]).to_numpy())]:
        sub = P[mask]
        ys = sub["y"].astype(int).to_numpy()
        for a, b in [("M1_hist_gbm", "L2_spline_logistic"), ("M1_hist_gbm", "B2_history"),
                     ("M1_hist_gbm", "L1_ridge_logistic"), ("L2_spline_logistic", "B2_history"),
                     ("M2_random_forest", "M1_hist_gbm"), ("L1_ridge_logistic", "B2_history"),
                     ("B2_history", "B1_prevalence")]:
            la, lb = (sub[a] - ys) ** 2, (sub[b] - ys) ** 2
            for cl in ["corridor_key", "firm__n"]:
                est, lo, hi, k = cluster_bootstrap_diff(la, lb, sub[cl], n_boot=1000, seed=config.SEED)
                diffs.append({"subset": subset, "model_a": a, "model_b": b, "cluster": cl,
                              "n_clusters": k, "brier_diff_a_minus_b": est, "ci95_lo": lo, "ci95_hi": hi})
    diffs = pd.DataFrame(diffs)

    cap = []
    rank_scores = {n: 1 - P[n].to_numpy() for n in names if n not in ("B0_always_stay", "B1_prevalence")}
    rank_scores["R_highest_cost_rule"] = P["cost"].to_numpy()
    for subset, mask in [("pooled_2022_2025", np.ones(len(P), bool)),
                         ("pooled_2022_2024", P["target_year"].isin([2022, 2023, 2024]).to_numpy())]:
        for n, s in rank_scores.items():
            for c in CAPACITIES:
                got, k, tot = capture_at_capacity(P[mask], s[mask], y[mask], c)
                gp, kp = capture_pooled(s[mask], y[mask], c)
                cap.append({"subset": subset, "rule": n, "capacity": c, "reviewed_per_quarter_sum": k,
                            "failures_captured_per_quarter": got, "failures_total": tot,
                            "recall_per_quarter": got / tot, "reviewed_pooled": kp,
                            "failures_captured_pooled": gp})
    cap = pd.DataFrame(cap)
    # bootstrap the capture difference GBM vs best simple rule, clustered by corridor
    capd = []
    for a, b in [("M1_hist_gbm", "L2_spline_logistic"), ("M1_hist_gbm", "R_highest_cost_rule"),
                 ("M1_hist_gbm", "B2_history")]:
        rng = np.random.default_rng(config.SEED)
        cors = P["corridor_key"].unique()
        grp = {c: np.flatnonzero(P["corridor_key"].to_numpy() == c) for c in cors}
        vals = []
        for _ in range(300):
            pick = rng.choice(cors, size=len(cors), replace=True)
            idx = np.concatenate([grp[c] for c in pick])
            ga, _, _ = capture_at_capacity(P.iloc[idx], rank_scores[a][idx], y[idx], 0.20)
            gb, _, _ = capture_at_capacity(P.iloc[idx], rank_scores[b][idx], y[idx], 0.20)
            vals.append(ga - gb)
        ga, _, _ = capture_at_capacity(P, rank_scores[a], y, 0.20)
        gb, _, _ = capture_at_capacity(P, rank_scores[b], y, 0.20)
        capd.append({"subset": "pooled_2022_2025", "capacity": 0.20, "rule_a": a, "rule_b": b,
                     "captured_diff": ga - gb, "ci95_lo": float(np.percentile(vals, 2.5)),
                     "ci95_hi": float(np.percentile(vals, 97.5)), "cluster": "corridor_key", "n_boot": 300})
    capd = pd.DataFrame(capd)
    rel = pd.concat([reliability_bins(y, P[n].to_numpy()).assign(model=n)
                     for n in ["B2_history", "L2_spline_logistic", "M1_hist_gbm", "L1_ridge_logistic"]])
    for name, t in [("metrics", metrics), ("paired_diffs", diffs), ("capacity", cap),
                    ("capacity_diff", capd), ("reliability", rel)]:
        t.to_csv(config.TABLES_DIR / f"model_{name}_{tag}.csv", index=False)
    return metrics, diffs, cap, capd


def reobservation(X: pd.DataFrame, tag: str):
    """Separate model of P(core reobserved | eligible, corridor surveyed next quarter)."""
    from rpi.models import ConstantModel, ColumnProbability, ridge_logistic
    R = X[X["status"].isin(["core_reobserved", "core_unobserved_corridor_surveyed"])].copy()
    R["r"] = (R["status"] == "core_reobserved").astype(int)
    rows = []
    for year in TEST_YEARS:
        test = R[R["target_year"] == year]
        if test.empty:
            continue
        train = R[R["target_qidx"] < test["qidx"].min()]
        for n, m in [("prevalence", ConstantModel()), ("corridor_history", ColumnProbability("reob_corr")),
                     ("ridge_logistic", ridge_logistic())]:
            p = m.fit(train, train["r"]).predict_proba(test)[:, 1]
            rows.append({"test_target_year": year, "model": n, **metric_row(test["r"].to_numpy(), p)})
    t = pd.DataFrame(rows)
    t.to_csv(config.TABLES_DIR / f"reobservation_metrics_{tag}.csv", index=False)
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--release-lag", type=int, default=0)
    args = ap.parse_args()
    tag = f"lag{args.release_lag}"
    t0 = time.time()
    lk = L.link_next_quarter(L.service_table(load_clean()))
    X = F.build(lk, release_lag=args.release_lag)
    P, reg = fit_predict(X, args.release_lag)
    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    P.to_parquet(config.PROCESSED_DIR / f"test_predictions_{tag}.parquet", index=False)
    reg.to_csv(config.TABLES_DIR / f"model_registry_{tag}.csv", index=False)
    metrics, diffs, cap, capd = summarise(P, tag)
    reob = reobservation(X, tag)
    meta = {"run_id": SPEC["run_id"], "release_lag": args.release_lag,
            "code_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
            "python": platform.python_version(), "sklearn": sklearn.__version__,
            "source_sha256": config.EXPECTED_SHA256, "n_test_rows": len(P),
            "n_test_corridors": int(P["corridor_key"].nunique()),
            "n_test_providers": int(P["firm__n"].nunique()), "wall_seconds": round(time.time() - t0, 1)}
    (config.TABLES_DIR / f"run_meta_{tag}.json").write_text(json.dumps(meta, indent=2) + "\n")
    pd.set_option("display.width", 200)
    print(json.dumps(meta, indent=2))
    print(metrics[metrics.subset.str.startswith("pooled")].round(5).to_string(index=False))
    print(diffs.round(5).to_string(index=False))
    print(cap[(cap.capacity == 0.2)].to_string(index=False))
    print(capd.to_string(index=False))
    print(reob.round(5).to_string(index=False))


if __name__ == "__main__":
    main()
