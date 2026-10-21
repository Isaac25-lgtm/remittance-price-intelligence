import importlib.util
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location('future',Path(__file__).resolve().parents[1]/'scripts/evaluate_future_wave.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_published_after_outcome_is_rejected():
    with pytest.raises(ValueError,match='TIMING_FAIL'):
        m.timing_gate(dict(available_by='2026-01-01',decision_date='2026-01-01',target_collection_start='2025-01-01',evidence_scope='all_row_level_predictors'))

def test_report_only_does_not_prove_quote_availability():
    with pytest.raises(ValueError,match='aggregate report'):
        m.timing_gate(dict(available_by='2024-01-01',decision_date='2024-01-02',target_collection_start='2024-02-01',evidence_scope='aggregate_report'))

def test_positive_lead_requires_all_clocks():
    m.timing_gate(dict(available_by='2024-01-01',decision_date='2024-01-02',target_collection_start='2024-02-01',evidence_scope='all_row_level_predictors'))
    with pytest.raises(ValueError,match='MISSING_INPUT'):m.timing_gate({})
