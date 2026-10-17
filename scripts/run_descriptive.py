"""Descriptive (non-model) outputs: record flow, core vs strict, bounds, corridor-level
estimand, secondary threshold/basket/horizon, African subgroup support. Aggregates only."""
from __future__ import annotations

import pandas as pd

from rpi import config, linkage as L
from rpi.preprocess import load_clean, qlabel

T = config.TABLES_DIR


def flow(lk: pd.DataFrame, label: str) -> pd.DataFrame:
    e = L.eligible_origin(lk)
    rows = [("all published quotes (post-2016 sheet)", len(lk)),
            ("missing basket cost", int(lk["cost"].isna().sum())),
            ("negative cost (retained, excluded from primary)", int((lk["cost"] < 0).sum())),
            ("cost <= 3% and >= 0", int(((lk["cost"] >= 0) & (lk["cost"] <= 3)).sum())),
            ("  of which origin in last quarter (right-censored)",
             int((((lk["cost"] >= 0) & (lk["cost"] <= 3)) & (lk["status"] == "right_censored_last_quarter")).sum())),
            ("eligible initially-cheap origins", int(e.sum()))]
    for s in L.STATUS_ORDER[:-1]:
        rows.append((f"  status: {s}", int((e & (lk["status"] == s)).sum())))
    rows += [("  core reobserved with invalid/negative target cost",
              int((e & lk["core_reobserved"] & ~(lk["cost_next"] >= 0)).sum())),
             ("primary E1 rows (core reobserved, valid target)", int(L.primary_outcome_rows(lk).sum())),
             ("  of which strict-bundle reobserved", int((L.primary_outcome_rows(lk) & lk["strict_reobserved"]).sum()))]
    return pd.DataFrame(rows, columns=["step", "count"]).assign(spec=label)


def main():
    df = load_clean()
    s1 = L.service_table(df, "cc1")
    lk = L.link_next_quarter(s1)
    lk["target_year"] = lk["target_qidx"] // 4
    lk["origin_quarter"] = lk["qidx"].map(qlabel)

    flows = [flow(lk, "primary: cc1 USD200, 3%, h=1")]
    flows.append(flow(L.link_next_quarter(L.service_table(df, "cc2")), "secondary: cc2 USD500, 3%, h=1"))
    lk2 = L.link_next_quarter(s1, horizon=2)
    flows.append(flow(lk2, "secondary: cc1 USD200, 3%, h=2"))
    pd.concat(flows).to_csv(T / "record_flow.csv", index=False)

    # core vs strict on identical eligible cohort, per target year
    e = lk[L.eligible_origin(lk)]
    cs = e.groupby("target_year").agg(
        eligible=("status", "size"), core_reobserved=("core_reobserved", "sum"),
        strict_reobserved=("strict_reobserved", "sum"),
        core_unobserved_corridor_surveyed=("status", lambda s: int((s == "core_unobserved_corridor_surveyed").sum())),
        corridor_not_surveyed=("status", lambda s: int((s == "corridor_not_surveyed_next_quarter").sum())),
        ambiguous=("status", lambda s: int(s.str.contains("ambiguous").sum()))).reset_index()
    core_only = e[e["core_reobserved"] & ~e["strict_reobserved"]]
    cs.to_csv(T / "linkage_core_vs_strict_by_year.csv", index=False)
    chg = pd.DataFrame({
        "core_only_records": [len(core_only)],
        "speed_changed": [int((core_only["speed actual__n"] != core_only["speed_next"]).sum())],
        "coverage_changed": [int((core_only["receiving network coverage__n"] != core_only["coverage_next"]).sum())]})
    chg.to_csv(T / "linkage_core_only_attribute_changes.csv", index=False)

    # E1 conditional rate under core and strict, and E2 bounds, by target year
    b = L.bounds_table(lk, by="target_year")
    prim = lk[L.primary_outcome_rows(lk)]
    strict = prim[prim["strict_reobserved"]]
    b = b.merge(strict.groupby("target_year").apply(
        lambda d: ((d["cost_next"] >= 0) & (d["cost_next"] <= 3)).mean(), include_groups=False)
        .rename("conditional_p_stay_strict").reset_index(), on="target_year", how="left")
    b.to_csv(T / "estimand_bounds_by_year.csv", index=False)
    L.bounds_table(lk).to_csv(T / "estimand_bounds_overall.csv", index=False)

    # secondary threshold 5%
    L.bounds_table(lk, threshold=5.0, by="target_year").to_csv(T / "estimand_bounds_by_year_5pct.csv", index=False)

    # E3 corridor-level
    c = L.corridor_level(lk)
    c["target_year"] = (c["qidx"] + 1) // 4
    c3 = c.groupby("target_year").agg(corridor_quarters_with_cheap=("cheap", "size"),
                                      surveyed_next=("surveyed_next", "sum"),
                                      still_cheap_next=("cheap_next", lambda v: int((v == True).sum())))  # noqa: E712
    c3["p_still_cheap_given_surveyed"] = c3["still_cheap_next"] / c3["surveyed_next"]
    c3.reset_index().to_csv(T / "estimand3_corridor_level_by_year.csv", index=False)

    # African subgroup support (receiving side; Uganda both directions separately)
    groups = {
        "global": pd.Series(True, index=lk.index),
        "receiving Sub-Saharan Africa": lk["destination_region"] == "Sub-Saharan Africa",
        "receiving East African Community (8)": lk["destination_code"].isin(config.EAST_AFRICA),
        "receiving Uganda": lk["destination_code"] == "UGA",
        "sending Uganda": lk["source_code"] == "UGA",
    }
    rows = []
    elig = L.eligible_origin(lk)
    primm = L.primary_outcome_rows(lk)
    for g, m in groups.items():
        for scope, ym in [("all years", pd.Series(True, index=lk.index)),
                          ("test targets 2022-2025", lk["target_year"].between(2022, 2025))]:
            mm = m & ym
            p = lk[mm & primm]
            rows.append({"group": g, "scope": scope, "corridors": int(lk.loc[mm, "corridor_key"].nunique()),
                         "providers": int(lk.loc[mm, "firm__n"].nunique()),
                         "all_quotes": int(mm.sum()), "eligible_cheap_origins": int((mm & elig).sum()),
                         "primary_rows": len(p), "primary_corridors": int(p["corridor_key"].nunique()),
                         "primary_providers": int(p["firm__n"].nunique()),
                         "observed_failures": int((p["cost_next"] > 3).sum()),
                         "conditional_p_stay": float(((p["cost_next"] <= 3)).mean()) if len(p) else float("nan")})
    pd.DataFrame(rows).to_csv(T / "subgroup_support.csv", index=False)

    # quote-observation flow per origin quarter (for figure)
    q = lk.groupby("origin_quarter").agg(qidx=("qidx", "first"), quotes=("status", "size"),
                                         **{s: ("status", (lambda s_: (lambda v: int((v == s_).sum())))(s))
                                            for s in L.STATUS_ORDER}).sort_values("qidx")
    q.to_csv(T / "linkage_status_by_origin_quarter.csv")
    print(pd.concat(flows).to_string(index=False))
    print(cs.to_string(index=False)); print(chg.to_string(index=False))
    print(b.round(4).to_string(index=False))
    print(c3.round(4).to_string())
    print(pd.DataFrame(rows).round(4).to_string(index=False))


if __name__ == "__main__":
    main()
