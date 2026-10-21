"""Streamlit AppTest: every section, widget option and download renders from committed aggregates.
These are presentation tests, not a real-data reproduction."""
import ast
from pathlib import Path

import pytest

st_testing = pytest.importorskip("streamlit.testing.v1")
ROOT = Path(__file__).resolve().parents[1]
APP = str(ROOT / "dashboard" / "app.py")


def _consts():
    tree = ast.parse(Path(APP).read_text(encoding="utf-8"))
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", None) in {
                "SECTIONS", "ALLOWLIST", "LAGS", "SUBSETS"}:
            out[node.targets[0].id] = ast.literal_eval(node.value)
    return out


C = _consts()
LAG_VALUES = list(C["LAGS"])
SUBSET_VALUES = list(C["SUBSETS"])
ALT_STATES = {  # widget states that reveal the alternative downloads (lag 1, 5% threshold)
    "Model comparison": [("selectbox", "mc_lag", "lag1")],
    "Calibration": [("selectbox", "cal_lag", "lag1")],
    "Review capacity": [("selectbox", "cap_lag", "lag1")],
    "Reobservation (negative result)": [("selectbox", "reob_lag", "lag1")],
    "Continuity & bounds": [("radio", "thr", "5% (secondary)")],
}


def _app(section=None):
    at = st_testing.AppTest.from_file(APP, default_timeout=90)
    at.run()
    if section:
        at.sidebar.radio(key="section").set_value(section).run()
    assert not at.exception, [e.value for e in at.exception]
    return at


def _offered(at):
    return {d.proto.label.replace("Download ", "") for d in at.get("download_button")}


def test_context_ribbon_and_caveats():
    at = _app()
    html = " ".join(m.value for m in at.markdown)
    assert "RETROSPECTIVE" in html and "EXPLORATORY" in html and "CONDITIONAL" in html
    cap = " ".join(c.value for c in at.caption)
    assert "no savings are observed" in cap and "UNVERIFIED" in cap and "does not prove" in cap


@pytest.mark.parametrize("section", C["SECTIONS"])
def test_section_renders_with_allowlisted_downloads(section):
    at = _app(section)
    if section == "Overview":  # the landing page opens with an HTML hero instead of st.header
        assert any("does it stay cheap?" in m.value for m in at.markdown)
    else:
        assert at.header[0].value
    offered = _offered(at)
    if section != "Overview":
        assert offered, section
    assert offered <= C["ALLOWLIST"]


def test_all_allowlisted_tables_are_downloadable_somewhere():
    offered = set()
    for s in C["SECTIONS"]:
        at = _app(s)
        offered |= _offered(at)
        for kind, key, val in ALT_STATES.get(s, []):
            getattr(at, kind)(key=key).set_value(val).run()
            assert not at.exception
            offered |= _offered(at)
    assert offered == C["ALLOWLIST"]


def test_download_payload_is_the_committed_file():
    at = _app("Model comparison")
    names = _offered(at)
    assert "presentation_model_brier_ci.csv" in names
    # the button serves exactly the committed aggregate bytes (no row-level content generated at runtime)
    committed = (ROOT / "results" / "tables" / "presentation_model_brier_ci.csv").read_bytes()
    assert committed.splitlines()[0].startswith(b"release_lag,subset,model,n,brier")


@pytest.mark.parametrize("section,key,values", [
    ("Model comparison", "mc_lag", LAG_VALUES), ("Model comparison", "mc_subset", SUBSET_VALUES),
    ("Calibration", "cal_lag", LAG_VALUES), ("Review capacity", "cap_lag", LAG_VALUES),
    ("Review capacity", "cap_subset", ["pooled_2022_2025", "pooled_2022_2024"]),
    ("Reobservation (negative result)", "reob_lag", LAG_VALUES),
    ("Measurement audit (Phase 3)", "ms_field", ["region", "provider_type", "fixed_sensitivity", "dominance",
                                                  "weighting"])])
def test_every_formatted_selectbox_value(section, key, values):
    at = _app(section)
    for v in values:  # raw values: displayed options are format_func labels
        at.selectbox(key=key).set_value(v).run()
        assert not at.exception, (section, key, v)


@pytest.mark.parametrize("section,key", [("Data & provenance", "flow_spec"), ("Geography & support", "sg_group")])
def test_every_plain_selectbox_option(section, key):
    at = _app(section)
    n_options = len(at.selectbox(key=key).options)
    assert n_options >= 2
    for i in range(n_options):
        at.selectbox(key=key).select_index(i).run()
        assert not at.exception, (section, key, i)


@pytest.mark.parametrize("section,key,values", [
    ("Continuity & bounds", "thr", ["3% (primary)", "5% (secondary)"]),
    ("Measurement audit (Phase 3)", "ms_product", ["cc1_3pct", "cc1_5pct", "cc2_3pct", "cc2_5pct"]),
    ("Model comparison", "mc_cluster", ["corridor", "provider"]),
    ("Geography & support", "sg_scope", ["all years", "test targets 2022-2025"])])
def test_every_radio_option(section, key, values):
    at = _app(section)
    for v in values:
        at.radio(key=key).set_value(v).run()
        assert not at.exception, (section, key, v)


@pytest.mark.parametrize("section,key,value", [
    ("Time-forward & lag sensitivity", "tf_models", ["M2_random_forest", "B0_always_stay", "L1_ridge_logistic"]),
    ("Time-forward & lag sensitivity", "tf_models", []),
    ("Calibration", "cal_models", ["B2_history", "L1_ridge_logistic", "B3_cost_logistic"]),
    ("Calibration", "cal_models", []),
    ("Review capacity", "cap_rules", ["B3_cost_logistic", "M2_random_forest"]),
    ("Review capacity", "cap_rules", [])])
def test_multiselects_including_empty(section, key, value):
    at = _app(section)
    at.multiselect(key=key).set_value(value).run()
    assert not at.exception
