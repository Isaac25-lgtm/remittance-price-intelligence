"""Conservative exact-key linkage of a surveyed service quote to the next calendar quarter.

Core identity (frozen): ordered corridor, normalised provider name, payment instrument,
access point, pickup method, pickup location and the basket (USD denomination amount).
Strict bundle additionally requires unchanged speed and receiving-network coverage.
Strict is evaluated *only among core matches*, so both definitions share one origin cohort.
No fuzzy matching: any key that is not unique within its quarter is excluded and counted.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import config

CORE_KEY = ["corridor_key", "firm__n", "payment instrument__n", "access point__n",
            "pickup method__n", "pickup location__n", "basket_usd"]
STRICT_ATTRS = ["speed actual__n", "receiving network coverage__n"]

STATUS_ORDER = [
    "core_reobserved",
    "core_unobserved_corridor_surveyed",
    "corridor_not_surveyed_next_quarter",
    "target_key_ambiguous",
    "origin_key_ambiguous",
    "right_censored_last_quarter",
]


def service_table(df: pd.DataFrame, basket: str = config.PRIMARY_BASKET) -> pd.DataFrame:
    """One row per published quote for a basket, with identity key and cost fields."""
    keep = ["source_row", "id", "period", "year", "qtr", "qidx", "collection_date",
            "corridor_key", "source_code", "destination_code", "source_region",
            "destination_region", "source_income", "destination_income",
            "firm", "firm__n", "firm_type__n", "payment instrument__n", "access point__n",
            "pickup method__n", "pickup location__n", "speed actual__n",
            "receiving network coverage__n", "transparent__n"]
    s = df[keep].copy()
    s["basket"] = basket
    s["basket_usd"] = df[f"{basket} denomination amount"].astype(float)
    s["cost"] = df[f"{basket} total cost %"].astype(float)
    s["fx_margin"] = df[f"{basket} fx margin"].astype(float)
    amt = df[f"{basket} lcu amount"].astype(float)
    fee = df[f"{basket} lcu fee"].astype(float)
    s["fee_pct"] = np.where(amt > 0, 100.0 * fee / amt, np.nan)
    other = "cc2" if basket == "cc1" else "cc1"
    s["cost_other_basket"] = df[f"{other} total cost %"].astype(float)
    s["key"] = s[CORE_KEY].astype(str).agg("|".join, axis=1)
    s["key_n_in_quarter"] = s.groupby(["qidx", "key"])["key"].transform("size")
    return s


def link_next_quarter(s: pd.DataFrame, horizon: int = 1) -> pd.DataFrame:
    """Attach status and target-quarter quote (exactly qidx + horizon) to every origin row."""
    last_q = int(s["qidx"].max())
    surveyed = set(zip(s["corridor_key"], s["qidx"]))
    uniq = s[s["key_n_in_quarter"] == 1]
    tgt = uniq[["key", "qidx", "cost", "speed actual__n", "receiving network coverage__n",
                "source_row"]].rename(columns={
                    "cost": "cost_next", "speed actual__n": "speed_next",
                    "receiving network coverage__n": "coverage_next", "source_row": "source_row_next"})
    tgt = tgt.assign(qidx=tgt["qidx"] - horizon)
    multi_next = s.groupby(["qidx", "key"]).size()
    multi_next = set(k for k, v in multi_next.items() if v > 1)

    out = s.merge(tgt, on=["key", "qidx"], how="left", validate="many_to_one")
    out["target_qidx"] = out["qidx"] + horizon
    corr_next = [(c, q + horizon) in surveyed for c, q in zip(out["corridor_key"], out["qidx"])]
    amb_next = [(q + horizon, k) in multi_next for q, k in zip(out["qidx"], out["key"])]
    status = np.select(
        [out["target_qidx"] > last_q,
         out["key_n_in_quarter"] > 1,
         ~np.array(corr_next),
         np.array(amb_next),
         out["source_row_next"].notna()],
        ["right_censored_last_quarter", "origin_key_ambiguous",
         "corridor_not_surveyed_next_quarter", "target_key_ambiguous", "core_reobserved"],
        default="core_unobserved_corridor_surveyed")
    out["status"] = status
    out["core_reobserved"] = out["status"] == "core_reobserved"
    out["strict_reobserved"] = (out["core_reobserved"]
                                & (out["speed actual__n"] == out["speed_next"])
                                & (out["receiving network coverage__n"] == out["coverage_next"]))
    return out


def eligible_origin(linked: pd.DataFrame, threshold: float = config.THRESHOLD) -> pd.Series:
    """Initially low-cost origin quotes: non-missing, non-negative cost <= threshold,
    with a next quarter existing in the data. Negative costs are retained separately."""
    c = linked["cost"]
    return c.notna() & (c >= 0) & (c <= threshold) & (linked["status"] != "right_censored_last_quarter")


def primary_outcome_rows(linked: pd.DataFrame, threshold: float = config.THRESHOLD) -> pd.Series:
    """Rows defining estimand 1: eligible, core-reobserved, unique, valid non-negative target cost."""
    return (eligible_origin(linked, threshold) & linked["core_reobserved"]
            & np.isfinite(linked["cost_next"]) & (linked["cost_next"] >= 0))


def bounds_table(linked: pd.DataFrame, threshold: float = config.THRESHOLD, by=None) -> pd.DataFrame:
    """Estimand 2: worst/best-case bounds on P(stays <= threshold) for all eligible
    initially-cheap origins, allocating every non-reobserved/invalid outcome to fail/success."""
    e = linked[eligible_origin(linked, threshold)].copy()
    e["stay"] = e["core_reobserved"] & (e["cost_next"] >= 0) & (e["cost_next"] <= threshold)
    e["fail_obs"] = e["core_reobserved"] & np.isfinite(e["cost_next"]) & (e["cost_next"] > threshold)
    e["unknown"] = ~(e["stay"] | e["fail_obs"])
    g = e.groupby(by) if by else e.assign(_all="all").groupby("_all")
    t = g.agg(n_eligible=("stay", "size"), n_stay=("stay", "sum"), n_fail=("fail_obs", "sum"),
              n_unknown=("unknown", "sum"),
              n_core=("core_reobserved", "sum"), n_strict=("strict_reobserved", "sum"))
    t["conditional_p_stay_core"] = t["n_stay"] / (t["n_stay"] + t["n_fail"])
    t["lower_bound"] = t["n_stay"] / t["n_eligible"]
    t["upper_bound"] = (t["n_stay"] + t["n_unknown"]) / t["n_eligible"]
    return t.reset_index()


def corridor_level(linked: pd.DataFrame, threshold: float = config.THRESHOLD) -> pd.DataFrame:
    """Estimand 3: among corridor-quarters with >=1 surveyed <=threshold quote and surveyed
    in the next quarter, does the corridor still have >=1 surveyed <=threshold quote?"""
    s = linked[["corridor_key", "qidx", "cost"]]
    cq = s.assign(cheap=(s["cost"] >= 0) & (s["cost"] <= threshold)).groupby(
        ["corridor_key", "qidx"])["cheap"].any().rename("cheap").reset_index()
    nxt = cq.assign(qidx=cq["qidx"] - 1).rename(columns={"cheap": "cheap_next"})
    m = cq.merge(nxt, on=["corridor_key", "qidx"], how="left")
    m["surveyed_next"] = m["cheap_next"].notna()
    return m[m["cheap"]]
