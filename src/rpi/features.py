"""Split-safe features. Every history feature for an origin quarter q uses only linked
transitions whose TARGET quarter is <= q - release_lag (information available at q under
the stated release scenario). Cross-sectional features use only quarter-q quotes."""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import config
from .linkage import eligible_origin, primary_outcome_rows

NUMERIC = ["cost", "fx_margin", "fee_pct", "cost_other_basket", "dist_to_threshold",
           "lag_cost", "lag_available", "lag_delta", "transparent",
           "h_global", "h_corr", "h_firm", "h_corrfirm", "n_corr_hist", "n_firm_hist",
           "reob_corr", "corr_n_services", "corr_share_cheap", "corr_min_cost", "cost_rank_in_corr"]
CATEGORICAL = ["firm_type__n", "payment instrument__n", "access point__n", "pickup method__n",
               "speed actual__n", "receiving network coverage__n", "source_region",
               "destination_region", "source_income", "destination_income", "qtr_cat"]
SPLINE_NUMERIC = ["cost", "fx_margin", "fee_pct", "h_corr", "h_firm", "corr_share_cheap"]
SHRINK_M = 10.0


def _asof(events: pd.DataFrame, by: list[str], value: str, origins: pd.DataFrame, lag: int,
          prefix: str) -> pd.DataFrame:
    """Cumulative sum/count of `value` over events with target_qidx <= origin qidx - lag."""
    agg = events.groupby(by + ["target_qidx"])[value].agg(["sum", "count"]).reset_index()
    agg = agg.sort_values(by + ["target_qidx"])
    agg[["sum", "count"]] = agg.groupby(by)[["sum", "count"]].cumsum() if by else agg[["sum", "count"]].cumsum()
    left = origins[by + ["qidx"]].copy()
    left["_row"] = np.arange(len(left))
    left["_t"] = left["qidx"] - lag
    left = left.sort_values("_t")
    agg = agg.rename(columns={"target_qidx": "_t"}).sort_values("_t")
    m = pd.merge_asof(left, agg, on="_t", by=by or None, direction="backward")
    m = m.sort_values("_row")
    return pd.DataFrame({f"{prefix}_sum": m["sum"].fillna(0).to_numpy(),
                         f"{prefix}_n": m["count"].fillna(0).to_numpy()}, index=origins.index)


def build(linked: pd.DataFrame, release_lag: int = 0, threshold: float = config.THRESHOLD) -> pd.DataFrame:
    """Return the modelling frame (eligible origins) with features and labels."""
    lk = linked.copy()
    lk["y"] = (lk["cost_next"] >= 0) & (lk["cost_next"] <= threshold)
    prim = primary_outcome_rows(lk, threshold)
    elig = eligible_origin(lk, threshold)
    events = lk[prim].assign(y=lambda d: d["y"].astype(float))
    reob_events = lk[elig & lk["status"].isin(["core_reobserved", "core_unobserved_corridor_surveyed"])]
    reob_events = reob_events.assign(r=reob_events["core_reobserved"].astype(float))

    o = lk[elig].copy()
    g = _asof(events.assign(_k=1), ["_k"], "y", o.assign(_k=1), release_lag, "glob")
    c = _asof(events, ["corridor_key"], "y", o, release_lag, "corr")
    f = _asof(events, ["firm__n"], "y", o, release_lag, "firm")
    cf = _asof(events, ["corridor_key", "firm__n"], "y", o, release_lag, "cf")
    rc = _asof(reob_events, ["corridor_key"], "r", o, release_lag, "reob")
    rg = _asof(reob_events.assign(_k=1), ["_k"], "r", o.assign(_k=1), release_lag, "reobg")

    p0 = (g["glob_sum"] + 1.0) / (g["glob_n"] + 2.0)  # weak prior before any history exists
    o["h_global"] = p0
    o["h_corr"] = (c["corr_sum"] + SHRINK_M * p0) / (c["corr_n"] + SHRINK_M)
    o["h_firm"] = (f["firm_sum"] + SHRINK_M * p0) / (f["firm_n"] + SHRINK_M)
    o["h_corrfirm"] = (cf["cf_sum"] + SHRINK_M * o["h_corr"]) / (cf["cf_n"] + SHRINK_M)
    o["n_corr_hist"] = c["corr_n"]
    o["n_firm_hist"] = f["firm_n"]
    r0 = (rg["reobg_sum"] + 1.0) / (rg["reobg_n"] + 2.0)
    o["reob_corr"] = (rc["reob_sum"] + SHRINK_M * r0) / (rc["reob_n"] + SHRINK_M)

    # lagged own cost: unique same core key exactly one quarter earlier (known at q)
    uniq = linked[linked["key_n_in_quarter"] == 1][["key", "qidx", "cost"]]
    prev = uniq.assign(qidx=uniq["qidx"] + 1).rename(columns={"cost": "lag_cost"})
    o = o.merge(prev, on=["key", "qidx"], how="left", validate="many_to_one")
    o["lag_available"] = o["lag_cost"].notna().astype(float)
    o["lag_delta"] = o["cost"] - o["lag_cost"]

    # cross-section of the corridor at q (all quotes, same basket)
    cs = linked[["corridor_key", "qidx", "cost"]]
    agg = cs.groupby(["corridor_key", "qidx"])["cost"].agg(
        corr_n_services="size",
        corr_share_cheap=lambda v: float(((v >= 0) & (v <= threshold)).mean()),
        corr_min_cost="min").reset_index()
    o = o.merge(agg, on=["corridor_key", "qidx"], how="left", validate="many_to_one")
    rank = linked.assign(r=linked.groupby(["corridor_key", "qidx"])["cost"].rank(pct=True))
    o = o.merge(rank[["source_row", "r"]].rename(columns={"r": "cost_rank_in_corr"}),
                on="source_row", how="left", validate="one_to_one")

    o["dist_to_threshold"] = threshold - o["cost"]
    o["transparent"] = (o["transparent__n"] == "yes").astype(float)
    o["qtr_cat"] = "q" + o["qtr"].astype(str)
    o["primary"] = primary_outcome_rows(o, threshold).to_numpy()
    o["target_year"] = o["target_qidx"] // 4
    for col in CATEGORICAL:
        o[col] = o[col].fillna("").astype(str)
    return o
