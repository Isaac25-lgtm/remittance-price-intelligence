import numpy as np

from rpi import linkage as L


def _linked(toy):
    return L.link_next_quarter(L.service_table(toy))


def status_of(lk, firm, q, dest="BBB"):
    r = lk[(lk["firm__n"] == firm) & (lk["qtr"] == q) & (lk["destination_code"] == dest)]
    return r["status"].tolist()


def test_statuses(toy):
    lk = _linked(toy)
    assert status_of(lk, "firm a", 1) == ["core_reobserved"]
    assert status_of(lk, "firm b", 1) == ["core_unobserved_corridor_surveyed"]
    assert set(status_of(lk, "firm c", 1)) == {"origin_key_ambiguous"}
    assert status_of(lk, "firm a", 3) == ["right_censored_last_quarter"]


def test_exactly_adjacent_quarter_only(toy):
    lk = _linked(toy)
    s = status_of(lk, "firm a", 1, dest="CCC")
    assert s == ["corridor_not_surveyed_next_quarter"]  # Q1 never links to Q3


def test_strict_is_subset_of_core_on_same_cohort(toy):
    lk = _linked(toy)
    d = lk[(lk["firm__n"] == "firm d") & (lk["qtr"] == 1)].iloc[0]
    assert d["core_reobserved"] and not d["strict_reobserved"]
    assert (lk["strict_reobserved"] <= lk["core_reobserved"]).all()


def test_eligibility_and_negative_costs(toy):
    lk = _linked(toy)
    e = L.eligible_origin(lk)
    assert not e[(lk["firm__n"] == "firm e") & (lk["qtr"] == 1)].any()  # negative origin excluded
    assert not e[lk["status"] == "right_censored_last_quarter"].any()
    prim = L.primary_outcome_rows(lk)
    # firm a Q1->Q2 (stays), firm a Q2->Q3 (2.0 -> 4.0, observed failure), firm d Q1->Q2
    assert prim.sum() == 3


def test_bounds_contain_conditional(toy):
    lk = _linked(toy)
    b = L.bounds_table(lk).iloc[0]
    assert b["lower_bound"] <= b["upper_bound"]
    assert b["n_eligible"] == b["n_stay"] + b["n_fail"] + b["n_unknown"]
    # cost_next = 3.0 counts as <= 3
    d = lk[(lk["firm__n"] == "firm d") & (lk["qtr"] == 1)].iloc[0]
    assert d["cost_next"] == 3.0
