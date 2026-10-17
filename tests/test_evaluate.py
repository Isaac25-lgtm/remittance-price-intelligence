import numpy as np
import pandas as pd

from rpi.evaluate import brier, capture_at_capacity, cluster_bootstrap_diff, log_loss, metric_row


def test_brier_and_logloss():
    y = np.array([1, 0, 1, 1])
    p = np.array([0.9, 0.2, 0.6, 1.0])
    assert np.isclose(brier(y, p), np.mean((p - y) ** 2))
    assert log_loss(y, np.full(4, 0.5)) > log_loss(y, p)


def test_calibration_perfect_model():
    rng = np.random.default_rng(0)
    p = rng.uniform(0.05, 0.95, 20000)
    y = (rng.uniform(size=p.size) < p).astype(int)
    r = metric_row(y, p)
    assert abs(r["cal_slope"] - 1) < 0.1 and abs(r["cal_intercept"]) < 0.1


def test_cluster_bootstrap_zero_difference():
    est, lo, hi, k = cluster_bootstrap_diff(np.ones(10), np.ones(10), list("aabbccddee"), n_boot=50)
    assert est == lo == hi == 0 and k == 5


def test_capacity_counts():
    df = pd.DataFrame({"qidx": [1] * 10})
    y = np.array([0, 0, 1, 1, 1, 1, 1, 1, 1, 1])  # two failures
    score = np.array([0.9, 0.8] + [0.1] * 8)
    got, k, tot = capture_at_capacity(df, score, y, 0.2)
    assert (got, k, tot) == (2, 2, 2)
