"""Integrity checks on the REAL committed aggregate result files (not synthetic mirrors).

These verify internal consistency between frozen tables, presentation aggregates and the
reproduction report, and that nothing row-level is exposed. They are not a data reproduction.
"""
import ast
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "results" / "tables"
APP = ROOT / "dashboard" / "app.py"
FORBIDDEN_COLUMNS = {"source_row", "source_row_next", "id", "firm", "firm__n", "key", "provider",
                     "cost_next", "y"}
MODELS = ["B0_always_stay", "B1_prevalence", "B2_history", "B3_cost_logistic", "L1_ridge_logistic",
          "L2_spline_logistic", "M1_hist_gbm", "M2_random_forest"]


def app_allowlist():
    tree = ast.parse(APP.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", None) == "ALLOWLIST":
            return set(ast.literal_eval(node.value))
    raise AssertionError("ALLOWLIST not found")


def allowlisted_paths():
    tree=ast.parse(APP.read_text(encoding="utf-8"))
    completion=next(ast.literal_eval(node.value) for node in ast.walk(tree)
                    if isinstance(node,ast.Assign) and getattr(node.targets[0],"id",None)=="COMPLETION_FILES")
    return [ROOT / "research_completion" / completion[n] if n in completion else
            ROOT / "results" / ("reproduction" if n == "table_comparison.csv" else "tables") / n
            for n in sorted(app_allowlist())]


def test_all_required_results_present_and_small():
    for p in allowlisted_paths():
        assert p.exists(), f"missing required result {p}"
        assert p.stat().st_size < 2_000_000
    for f in ["run_meta_lag0.json", "run_meta_lag1.json"]:
        assert (T / f).exists()
    assert (ROOT / "results" / "reproduction" / "reproduction_report.json").exists()


@pytest.mark.parametrize("path", allowlisted_paths(), ids=lambda p: p.name)
def test_no_row_level_identifiers(path):
    df = pd.read_csv(path)
    assert not (FORBIDDEN_COLUMNS & set(df.columns)), path.name


def test_all_eight_families_evaluated_on_identical_rows():
    for lag in ["lag0", "lag1"]:
        m = pd.read_csv(T / f"model_metrics_{lag}.csv")
        for sub, g in m.groupby("subset"):
            assert set(g.model) == set(MODELS)
            assert g["n"].nunique() == 1 and g["prevalence_stay"].nunique() == 1


def test_metric_identities():
    for lag in ["lag0", "lag1"]:
        m = pd.read_csv(T / f"model_metrics_{lag}.csv")
        b0 = m[m.model == "B0_always_stay"]
        assert np.allclose(b0.brier, 1 - b0.prevalence_stay, atol=1e-5)
        pooled = m[m.subset == "pooled_2022_2025"].set_index("model")["n"]
        years = m[m.subset.str.startswith("year_")].groupby("model")["n"].sum()
        assert (pooled == years.loc[pooled.index]).all()


def test_paired_diffs_match_metrics():
    for lag in ["lag0", "lag1"]:
        m = pd.read_csv(T / f"model_metrics_{lag}.csv").set_index(["subset", "model"])["brier"]
        d = pd.read_csv(T / f"model_paired_diffs_{lag}.csv")
        for r in d.itertuples():
            assert abs(r.brier_diff_a_minus_b - (m[(r.subset, r.model_a)] - m[(r.subset, r.model_b)])) < 1e-12
            assert r.ci95_lo <= r.brier_diff_a_minus_b <= r.ci95_hi


def test_presentation_ci_consistent_with_frozen_metrics():
    ci = pd.read_csv(T / "presentation_model_brier_ci.csv")
    for lag in ["lag0", "lag1"]:
        m = pd.read_csv(T / f"model_metrics_{lag}.csv").set_index(["subset", "model"])
        c = ci[ci.release_lag == lag].set_index(["subset", "model"])
        assert set(c.index) == set(m.index)
        assert np.allclose(c.loc[m.index, "brier"], m["brier"], atol=1e-9)
        assert (c.loc[m.index, "n"].to_numpy() == m["n"].to_numpy()).all()
    for k in ["corridor", "provider"]:
        assert (ci[f"{k}_boot_lo"] <= ci.brier + 1e-12).all() and (ci.brier <= ci[f"{k}_boot_hi"] + 1e-12).all()


def test_capacity_denominators_match_metrics():
    for lag in ["lag0", "lag1"]:
        m = pd.read_csv(T / f"model_metrics_{lag}.csv")
        c = pd.read_csv(T / f"model_capacity_{lag}.csv")
        for sub, g in c.groupby("subset"):
            r = m[(m.subset == sub)].iloc[0]
            assert (g.failures_total == round(r.n * (1 - r.prevalence_stay))).all()
            assert (g.failures_captured_per_quarter <= g.failures_total).all()
    cy = pd.read_csv(T / "presentation_capacity_by_year_lag0.csv")
    m0 = pd.read_csv(T / "model_metrics_lag0.csv")
    for yr, g in cy.groupby("target_year"):
        r = m0[m0.subset == f"year_{yr}"].iloc[0]
        assert (g.failures_total == round(r.n * (1 - r.prevalence_stay))).all()


def test_bounds_and_flow_identities():
    for f in ["estimand_bounds_by_year.csv", "estimand_bounds_by_year_5pct.csv", "estimand_bounds_overall.csv"]:
        b = pd.read_csv(T / f)
        assert (b.n_eligible == b.n_stay + b.n_fail + b.n_unknown).all()
        assert (b.lower_bound <= b.conditional_p_stay_core + 1e-12).all()
        assert (b.conditional_p_stay_core <= b.upper_bound + 1e-12).all()
        assert (b.n_strict <= b.n_core).all()
    fl = pd.read_csv(T / "record_flow.csv")
    for spec, g in fl.groupby("spec"):
        s = g.set_index("step")["count"]
        statuses = s[[i for i in s.index if i.strip().startswith("status:")]].sum()
        assert statuses == s["eligible initially-cheap origins"]


def test_support_gates_respected():
    for f in ["presentation_corridor_metrics_lag0.csv", "presentation_region_metrics_lag0.csv"]:
        c = pd.read_csv(T / f)
        sup = c[c.supported]
        assert ((sup.n >= 100) & (sup.observed_failures >= 20)).all()
        assert c.loc[~c.supported, "brier_M1_hist_gbm"].isna().all()
    sm = pd.read_csv(T / "subgroup_model_metrics_lag0.csv")
    uga = sm[sm.group == "receiving Uganda"]
    assert (uga.model == "(not reported)").all()


def test_negative_reobservation_finding_preserved():
    r = pd.read_csv(T / "reobservation_metrics_lag0.csv").set_index(["test_target_year", "model"])["brier"]
    for yr in [2022, 2023]:
        assert r[(yr, "ridge_logistic")] > r[(yr, "prevalence")]


def test_reproduction_report_consistent():
    rep = json.loads((ROOT / "results" / "reproduction" / "reproduction_report.json").read_text(encoding="utf-8"))
    tc = pd.read_csv(ROOT / "results" / "reproduction" / "table_comparison.csv")
    assert rep["source_sha256"] == "f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8"
    assert rep["source_downloaded_in_this_run"] is False
    assert rep["n_tables"] == len(tc)
    assert sorted(rep["non_matching"]) == sorted(tc.loc[tc.status != "MATCH", "file"])


def test_app_reads_no_row_level_sources():
    src = APP.read_text(encoding="utf-8")
    for bad in ["data/raw", "data/processed", ".parquet", "read_excel", "rpi."]:
        assert bad not in src


def test_all_family_reliability_matches_frozen_four():
    """Derived all-family deciles must reproduce the frozen four-family deciles exactly."""
    allf = pd.read_csv(T / "presentation_reliability_all_families.csv")
    assert set(allf.model) == set(MODELS) - {"B0_always_stay"}
    for lag in ["lag0", "lag1"]:
        fr = pd.read_csv(T / f"model_reliability_{lag}.csv")
        a = allf[allf.release_lag == lag]
        for mdl, g in fr.groupby("model"):
            h = a[a.model == mdl].sort_values("bin")
            assert np.allclose(h[["n", "mean_pred", "obs_rate"]].to_numpy(),
                               g.sort_values("bin")[["n", "mean_pred", "obs_rate"]].to_numpy(), atol=1e-9)
