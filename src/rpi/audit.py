"""Source audit: schema, quarter coverage, missingness, duplicates, negative/zero/outlier costs.

Writes only aggregate tables to results/tables (safe to publish).
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from . import config
from .preprocess import NUMERIC, qlabel


def quarter_coverage(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("qidx")
    t = pd.DataFrame({
        "period": g["period"].first(),
        "rows": g.size(),
        "corridors": g["corridor_key"].nunique(),
        "sending_countries": g["source_code"].nunique(),
        "receiving_countries": g["destination_code"].nunique(),
        "firms_normalised": g["firm__n"].nunique(),
        "collection_date_min": g["collection_date"].min().dt.date.astype(str),
        "collection_date_max": g["collection_date"].max().dt.date.astype(str),
        "cc1_cost_le3_share": g["cc1 total cost %"].apply(lambda c: float(((c >= 0) & (c <= 3)).mean())),
    })
    full = pd.RangeIndex(t.index.min(), t.index.max() + 1)
    t = t.reindex(full)
    t["quarter"] = [qlabel(q) for q in t.index]
    t["present_in_source"] = t["rows"].notna()
    return t.reset_index(names="qidx")


def missingness(df: pd.DataFrame, cols) -> pd.DataFrame:
    rows = []
    for c in cols:
        v = df[c]
        blank = v.isna() | (v.astype(str).str.strip().isin(["", "None", "nan"]))
        rows.append({"variable": c, "n": len(v), "n_missing_or_blank": int(blank.sum()),
                     "share_missing": float(blank.mean())})
    return pd.DataFrame(rows)


def cost_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for b in ["cc1", "cc2"]:
        c = df[f"{b} total cost %"]
        fee = df[f"{b} lcu fee"]
        fx = df[f"{b} fx margin"]
        amt = df[f"{b} lcu amount"]
        recomposed = 100 * fee / amt + fx
        rows.append({
            "basket": b,
            "n": len(c), "missing": int(c.isna().sum()), "negative": int((c < 0).sum()),
            "zero": int((c == 0).sum()), "gt_20pct": int((c > 20).sum()), "gt_50pct": int((c > 50).sum()),
            "le_3pct": int(((c >= 0) & (c <= 3)).sum()),
            "fx_margin_negative": int((fx < 0).sum()),
            "fee_negative": int((fee < 0).sum()),
            "denomination_values": json.dumps(sorted(df[f"{b} denomination amount"].dropna().unique().tolist())[:10]),
            "abs_diff_total_vs_fee_plus_fx_gt_0.05": int(((recomposed - c).abs() > 0.05).sum()),
            "abs_diff_total_vs_fee_plus_fx_median": float((recomposed - c).abs().median()),
        })
    return pd.DataFrame(rows)


def run(df: pd.DataFrame) -> dict:
    config.TABLES_DIR.mkdir(parents=True, exist_ok=True)
    cov = quarter_coverage(df)
    cov.to_csv(config.TABLES_DIR / "audit_quarter_coverage.csv", index=False)
    miss = missingness(df, [c for c in df.columns if not c.endswith("__nonnumeric") and not c.endswith("__n")
                            and c not in ("source_row", "year", "qtr", "qidx")])
    miss.to_csv(config.TABLES_DIR / "audit_missingness.csv", index=False)
    anom = cost_anomalies(df)
    anom.to_csv(config.TABLES_DIR / "audit_cost_anomalies.csv", index=False)
    nonnum = {c: int(df[c + "__nonnumeric"].sum()) for c in NUMERIC}
    dup_id = int(df["id"].duplicated().sum())
    full_dup = int(df.drop(columns=["source_row", "id"]).astype(str).duplicated().sum())
    # provider names that differ only by normalisation (case/whitespace/separator)
    raw_names = df.groupby("firm__n")["firm"].nunique()
    summary = {
        "rows": int(len(df)),
        "periods_present": int(cov["present_in_source"].sum()),
        "first_quarter": cov["quarter"].iloc[0], "last_quarter": cov["quarter"].iloc[-1],
        "quarters_missing_in_span": cov.loc[~cov["present_in_source"], "quarter"].tolist(),
        "corridors": int(df["corridor_key"].nunique()),
        "corridor_field_mismatch": int((df["corridor"] != df["source_code"] + df["destination_code"]).sum()),
        "firms_raw": int(df["firm"].nunique()), "firms_normalised": int(df["firm__n"].nunique()),
        "normalised_firm_names_with_multiple_raw_spellings": int((raw_names > 1).sum()),
        "duplicate_id": dup_id,
        "exact_duplicate_rows_excluding_id": full_dup,
        "nonnumeric_cells_in_numeric_columns": nonnum,
        "collection_date_missing": int(df["collection_date"].isna().sum()),
        "collection_date_outside_period_quarter": int(
            ((df["collection_date"].dt.year * 4 + df["collection_date"].dt.quarter - 1) != df["qidx"]).sum()),
    }
    (config.TABLES_DIR / "audit_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    from .preprocess import load_clean
    print(json.dumps(run(load_clean()), indent=2))
