import pandas as pd
import pytest

from rpi.preprocess import norm_text, parse_date, parse_period, qlabel, quarter_index


def test_parse_period_and_adjacency():
    assert parse_period("2016_2Q") == (2016, 2)
    a = quarter_index(*parse_period("2024_4Q"))
    b = quarter_index(*parse_period("2025_1Q"))
    assert b - a == 1  # year boundary is adjacent
    assert quarter_index(2025, 3) - quarter_index(2025, 1) == 2  # gap is not adjacent
    assert qlabel(a) == "2024Q4"


@pytest.mark.parametrize("bad", ["2016Q2", "2016_5Q", "", "16_2Q"])
def test_parse_period_rejects(bad):
    with pytest.raises(ValueError):
        parse_period(bad)


def test_norm_text_is_conservative():
    assert norm_text("  Western   Union ") == "western union"
    assert norm_text("Bank account transfer, Cash") == norm_text("bank account transfer,cash")
    assert norm_text("WorldRemit") != norm_text("World Remit")  # no fuzzy merging
    assert norm_text(None) == ""


def test_parse_date_both_formats():
    assert parse_date("11/May/2016") == pd.Timestamp("2016-05-11")
    assert parse_date(pd.Timestamp("2025-08-22")) == pd.Timestamp("2025-08-22")
