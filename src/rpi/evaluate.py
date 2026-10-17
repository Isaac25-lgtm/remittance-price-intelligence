"""Metrics on identical test rows, cluster-bootstrap paired differences, review capacity."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score

EPS = 1e-6


def brier(y, p):
    return float(np.mean((p - y) ** 2))


def log_loss(y, p):
    p = np.clip(p, EPS, 1 - EPS)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def calibration_intercept_slope(y, p):
    """Logistic recalibration: slope = coef on logit(p); intercept from offset-only model."""
    lp = np.log(np.clip(p, EPS, 1 - EPS) / (1 - np.clip(p, EPS, 1 - EPS)))
    if np.std(lp) < 1e-9:
        slope = np.nan
    else:
        slope = float(LogisticRegression(C=1e6, max_iter=1000).fit(lp[:, None], y).coef_[0, 0])
    # calibration-in-the-large: solve mean(sigmoid(a + lp)) = mean(y) by bisection
    lo, hi = -10.0, 10.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if np.mean(1 / (1 + np.exp(-(mid + lp)))) < np.mean(y):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2, slope


def metric_row(y, p):
    y = np.asarray(y, float)
    p = np.asarray(p, float)
    fail = 1 - y
    a, s = calibration_intercept_slope(y, p)
    out = {"n": len(y), "prevalence_stay": float(y.mean()), "brier": brier(y, p),
           "log_loss": log_loss(y, p), "cal_intercept": a, "cal_slope": s,
           "mean_pred": float(p.mean())}
    if 0 < y.sum() < len(y) and np.std(p) > 0:
        out["auroc"] = float(roc_auc_score(y, p))
        out["auprc_failure"] = float(average_precision_score(fail, 1 - p))
    else:
        out["auroc"] = np.nan
        out["auprc_failure"] = np.nan
    return out


def cluster_bootstrap_diff(loss_a, loss_b, clusters, n_boot=1000, seed=0):
    """Paired mean-loss difference (a - b) with percentile CI resampling whole clusters."""
    d = pd.DataFrame({"d": np.asarray(loss_a) - np.asarray(loss_b), "c": np.asarray(clusters)})
    g = d.groupby("c")["d"].agg(["sum", "size"])
    sums, sizes = g["sum"].to_numpy(), g["size"].to_numpy()
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(g), size=(n_boot, len(g)))
    boots = sums[idx].sum(1) / sizes[idx].sum(1)
    est = float(d["d"].mean())
    return est, float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)), len(g)


def capture_at_capacity(df, score_fail, y, capacity, group="qidx"):
    """Review the top `capacity` share of rows by failure score within each origin quarter;
    return observed failures captured. Ties broken deterministically by row order."""
    d = pd.DataFrame({"s": np.asarray(score_fail, float), "fail": 1 - np.asarray(y, int),
                      "g": np.asarray(df[group])})
    d["order"] = np.arange(len(d))
    captured, reviewed = 0, 0
    for _, part in d.groupby("g"):
        k = int(np.floor(capacity * len(part)))
        top = part.sort_values(["s", "order"], ascending=[False, True]).head(k)
        captured += int(top["fail"].sum())
        reviewed += k
    return captured, reviewed, int(d["fail"].sum())


def capture_pooled(score_fail, y, capacity):
    """Pilot-comparable variant: rank all pooled test rows at once."""
    s = np.asarray(score_fail, float)
    k = int(np.floor(capacity * len(s)))
    order = np.argsort(-s, kind="stable")[:k]
    return int((1 - np.asarray(y, int))[order].sum()), k


def reliability_bins(y, p, n_bins=10):
    d = pd.DataFrame({"y": y, "p": p})
    d["bin"] = pd.qcut(d["p"].rank(method="first"), n_bins, labels=False)
    return d.groupby("bin").agg(n=("y", "size"), mean_pred=("p", "mean"), obs_rate=("y", "mean")).reset_index()
