"""Leakage guards: history features at origin q must not change when outcomes of
transitions with target quarter > q (or > q - lag) are altered."""
import numpy as np
import pandas as pd

from rpi import features as F, linkage as L
from tests.conftest import make_clean


def _panel(perturb_future=False):
    rows = []
    rng = np.random.default_rng(1)
    for q in range(8):
        y, qt = 2018 + q // 4, q % 4 + 1
        for f in range(6):
            cost = float(rng.uniform(0.5, 2.9))
            if perturb_future and q >= 5:
                cost = 9.0  # every transition with target >= quarter 5 now fails
            rows.append({"year": y, "qtr": qt, "firm": f"F{f}", "cc1 total cost %": cost,
                         "cc1 lcu fee": cost * 2, "cc1 fx margin": 0.0})
    return make_clean(rows)


def _features(df, lag):
    lk = L.link_next_quarter(L.service_table(df))
    return F.build(lk, release_lag=lag)


def test_history_ignores_future_outcomes():
    for lag in (0, 1):
        a = _features(_panel(False), lag)
        b = _features(_panel(True), lag)
        hist = ["h_global", "h_corr", "h_firm", "h_corrfirm", "n_corr_hist", "reob_corr"]
        # origins at quarter index <= 3 (targets <= 4): features must be identical
        qa = a[a["qidx"] - a["qidx"].min() <= 3].sort_values("source_row")
        qb = b[b["qidx"] - b["qidx"].min() <= 3].sort_values("source_row")
        pd.testing.assert_frame_equal(qa[hist].reset_index(drop=True), qb[hist].reset_index(drop=True))


def test_release_lag_shifts_information():
    a0 = _features(_panel(False), 0)
    a1 = _features(_panel(False), 1)
    first = a0["qidx"].min()
    # at the first two origin quarters, lag-1 history count trails lag-0
    n0 = a0[a0["qidx"] == first + 2]["n_corr_hist"].iloc[0]
    n1 = a1[a1["qidx"] == first + 2]["n_corr_hist"].iloc[0]
    assert n1 < n0


def test_label_not_in_features():
    a = _features(_panel(False), 0)
    for c in F.NUMERIC + F.CATEGORICAL:
        assert "next" not in c and c != "y"
