"""AppTest smoke tests: every dashboard section renders from committed aggregate tables."""
from pathlib import Path

import pytest

st_testing = pytest.importorskip("streamlit.testing.v1")
APP = str(Path(__file__).resolve().parents[1] / "dashboard" / "app.py")
SECTIONS = ["Overview", "Data provenance", "Study cohort & linkage", "Missing-outcome bounds",
            "Baselines and models", "Calibration", "Hypothetical review capacity",
            "African subgroup support", "Limitations & reproducibility"]


def _run(section=None):
    at = st_testing.AppTest.from_file(APP, default_timeout=60)
    at.run()
    if section:
        at.sidebar.radio(key="section").set_value(section).run()
    assert not at.exception, [e.value for e in at.exception]
    return at


def test_ribbon_labels_retrospective():
    at = _run()
    text = " ".join(i.value for i in at.info)
    assert "RETROSPECTIVE" in text and "EXPLORATORY" in text and "CONDITIONAL" in text
    assert "No savings are observed" in " ".join(c.value for c in at.caption)


@pytest.mark.parametrize("section", SECTIONS)
def test_each_section_renders(section):
    at = _run(section)
    assert at.header[0].value == section.replace(" (pooled test, deciles)", "") or \
        at.header[0].value.startswith(section.split(" ")[0])


def test_model_selectors_and_lag_sensitivity():
    at = _run("Baselines and models")
    for lag in ["lag0", "lag1"]:
        at.selectbox(key="model_lag").set_value(lag).run()
        for sub in ["pooled_2022_2025", "year_2025"]:
            at.selectbox(key="model_subset").set_value(sub).run()
            assert not at.exception


def test_other_interactions():
    at = _run("Missing-outcome bounds")
    at.radio(key="thr").set_value("5% (secondary)").run()
    assert not at.exception
    at = _run("Hypothetical review capacity")
    at.selectbox(key="cap_lag").set_value("lag1").run()
    at.selectbox(key="cap_subset").set_value("pooled_2022_2024").run()
    assert not at.exception
    assert any("not** consumer savings" in w.value for w in at.warning)
    at = _run("African subgroup support")
    at.selectbox(key="sg_group").set_value("receiving Uganda").run()
    assert not at.exception
    at = _run("Calibration")
    at.multiselect(key="cal_models").set_value(["B2_history"]).run()
    assert not at.exception
    at = _run("Study cohort & linkage")
    at.selectbox(key="flow_spec").set_value("secondary: cc1 USD200, 3%, h=2").run()
    assert not at.exception


def test_no_row_level_inputs():
    src = Path(APP).read_text()
    assert "data/raw" not in src and "data/processed" not in src and "parquet" not in src
