"""Model metrics within African receiving subgroups on the pooled test rows (descriptive;
models were trained globally, nothing was tuned for subgroups). Aggregates only."""
import numpy as np
import pandas as pd

from rpi import config
from rpi.evaluate import cluster_bootstrap_diff, metric_row
from rpi.models import MODELS

MIN_FAILURES = 100  # below this, subgroup model metrics are not reported (support gate)


def main(tag="lag0"):
    P = pd.read_parquet(config.PROCESSED_DIR / f"test_predictions_{tag}.parquet")
    groups = {"receiving Sub-Saharan Africa": P["destination_region"] == "Sub-Saharan Africa",
              "receiving East African Community (8)": P["destination_code"].isin(config.EAST_AFRICA),
              "receiving Uganda": P["destination_code"] == "UGA",
              "all other receiving": P["destination_region"] != "Sub-Saharan Africa"}
    rows = []
    for g, m in groups.items():
        sub = P[m]
        y = sub["y"].astype(int).to_numpy()
        nfail = int((1 - y).sum())
        if nfail < MIN_FAILURES:
            rows.append({"group": g, "model": "(not reported)", "n": len(sub), "failures": nfail,
                         "corridors": sub["corridor_key"].nunique(),
                         "note": f"fewer than {MIN_FAILURES} observed failures: support gate not met"})
            continue
        for n in MODELS:
            r = metric_row(y, sub[n].to_numpy())
            rows.append({"group": g, "model": n, "failures": nfail,
                         "corridors": sub["corridor_key"].nunique(), **r})
        est, lo, hi, k = cluster_bootstrap_diff((sub["M1_hist_gbm"] - y) ** 2, (sub["L2_spline_logistic"] - y) ** 2,
                                                sub["corridor_key"], 1000, config.SEED)
        rows.append({"group": g, "model": "diff M1_hist_gbm - L2_spline_logistic (corridor CI)",
                     "brier": est, "ci95_lo": lo, "ci95_hi": hi, "corridors": k})
    t = pd.DataFrame(rows)
    t.to_csv(config.TABLES_DIR / f"subgroup_model_metrics_{tag}.csv", index=False)
    print(t[["group", "model", "n", "failures", "corridors", "brier", "auroc", "cal_slope", "ci95_lo", "ci95_hi"]]
          .round(4).to_string(index=False))


if __name__ == "__main__":
    main()
