"""SYNTHETIC fixtures only. Nothing here is RPW data or used as a finding."""
import numpy as np
import pandas as pd
import pytest

from rpi.preprocess import IDENTITY_TEXT, norm_text, quarter_index


def make_clean(rows):
    """Build a minimal 'clean' frame as produced by preprocess.clean from dict rows."""
    base = {"id": 0, "source_code": "AAA", "destination_code": "BBB", "source_region": "R1",
            "destination_region": "Sub-Saharan Africa", "source_income": "High income",
            "destination_income": "Low income", "firm": "Firm A", "firm_type": "Money Transfer Operator",
            "payment instrument": "Cash", "access point": "Agent", "speed actual": "Same day",
            "receiving network coverage": "High", "pickup location": "Agent", "pickup method": "Cash",
            "transparent": "yes", "cc1 denomination amount": 200.0, "cc2 denomination amount": 500.0,
            "cc1 lcu amount": 200.0, "cc1 lcu fee": 2.0, "cc1 fx margin": 0.0,
            "cc2 lcu amount": 500.0, "cc2 lcu fee": 2.0, "cc2 fx margin": 0.0, "cc2 total cost %": 0.4}
    out = []
    for i, r in enumerate(rows):
        d = {**base, **r}
        d["id"] = i
        d["source_row"] = i + 2
        d["qidx"] = quarter_index(d["year"], d["qtr"])
        d["period"] = f"{d['year']}_{d['qtr']}Q"
        d["collection_date"] = pd.Timestamp(d["year"], 3 * d["qtr"] - 1, 1)
        d["corridor_key"] = d["source_code"] + ">" + d["destination_code"]
        for c in IDENTITY_TEXT:
            d[c + "__n"] = norm_text(d[c])
        out.append(d)
    return pd.DataFrame(out)


@pytest.fixture
def toy():
    rows = []
    # Firm A: cheap in 2020Q1, reobserved 2020Q2 still cheap, 2020Q3 expensive
    for q, cost in [(1, 1.0), (2, 2.0), (3, 4.0)]:
        rows.append({"year": 2020, "qtr": q, "cc1 total cost %": cost})
    # Firm B: cheap in Q1, absent in Q2 although corridor surveyed (unobserved)
    rows.append({"year": 2020, "qtr": 1, "firm": "Firm B", "cc1 total cost %": 2.5})
    # Firm C: duplicated key in Q1 (ambiguous origin)
    rows.append({"year": 2020, "qtr": 1, "firm": "Firm C", "cc1 total cost %": 1.0})
    rows.append({"year": 2020, "qtr": 1, "firm": "FIRM  c", "cc1 total cost %": 1.5})
    # Firm D: speed changes between Q1 and Q2 -> core but not strict
    rows.append({"year": 2020, "qtr": 1, "firm": "Firm D", "cc1 total cost %": 2.9})
    rows.append({"year": 2020, "qtr": 2, "firm": "Firm D", "speed actual": "Next day", "cc1 total cost %": 3.0})
    # Other corridor surveyed only in Q1 and Q3 (gap): Q1 must NOT link to Q3
    rows.append({"year": 2020, "qtr": 1, "destination_code": "CCC", "cc1 total cost %": 1.0})
    rows.append({"year": 2020, "qtr": 3, "destination_code": "CCC", "cc1 total cost %": 1.0})
    # Negative quote retained but not eligible
    rows.append({"year": 2020, "qtr": 1, "firm": "Firm E", "cc1 total cost %": -0.5})
    rows.append({"year": 2020, "qtr": 2, "firm": "Firm E", "cc1 total cost %": 1.0})
    return make_clean(rows)
