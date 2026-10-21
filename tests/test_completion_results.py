"""Cross-file scientific output contracts; no fits or downloads in CI."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

OUT=Path(__file__).resolve().parents[1]/'research_completion'

def test_all_origin_queue_arithmetic_and_unknown_bounds():
    a=pd.read_csv(OUT/'models/all_origin_capacity_bounds.csv')
    assert (a.n_all_eligible==a.n_known_valid+a.n_unknown).all()
    assert a.groupby('capacity').reviewed.nunique().eq(1).all()
    assert (a.reviewed==a.known_failures_captured+a.unknown_reviewed+a.known_stays_reviewed).all()
    assert np.allclose(a.all_failure_recall_lower,a.known_failures_captured/(a.known_failures_total+a.n_unknown-a.unknown_reviewed))
    assert np.allclose(a.all_failure_recall_upper,(a.known_failures_captured+a.unknown_reviewed)/(a.known_failures_total+a.unknown_reviewed))
    assert a.all_failure_recall_lower.le(a.all_failure_recall_upper).all()

def test_joint_inference_and_claim_are_consistent():
    j=pd.read_csv(OUT/'models/joint_dependence_sensitivity.csv')
    row=j[(j.model_a=='S_selected')&(j.model_b=='L2_spline_logistic')].iloc[0]
    verdict=(OUT/'assessment/PUBLICATION_VERDICT.md').read_text(encoding='utf-8')
    assert row.ci95_lo<0<row.ci95_hi
    assert f'{row.ci95_hi:+.6f}' in verdict
    assert 'NOT YET PUBLICATION-READY' in verdict

def test_pilot_cache_rebuilt_and_reproduction_residual_retained():
    p=json.loads((OUT/'audits/pilot_cache_rebuild.json').read_text(encoding='utf-8'))
    assert p['matches_original_cache_sha256']
    report=(OUT/'manuscript/conditional_research_report.md').read_text(encoding='utf-8')
    assert p['cache_sha256'] in report
    assert 'spline remains slightly different' in report

def test_headlines_match_actual_phase2_metrics():
    m=pd.read_csv(OUT/'models/model_comparison.csv').set_index('model')
    report=(OUT/'manuscript/conditional_research_report.md').read_text(encoding='utf-8')
    assert m.n.nunique()==1
    assert f"{m.loc['S_selected','brier']:.6f}" in report
    assert int(m.loc['S_selected','n'])==19667

def test_named_strong_references_and_brier_skill_identities():
    a=pd.read_csv(OUT/'models/conventional_reference_comparisons.csv')
    assert set(a.reference)=={'L1_ridge_logistic','L1_ridge_logistic__cal','L2_spline_logistic','L2_spline_logistic__cal'}
    assert np.allclose(a.brier_skill,1-a.brier_model/a.brier_reference)
    assert np.allclose(a.brier_diff,a.brier_model-a.brier_reference)
    assert np.allclose(a.relative_brier_diff,-a.brier_skill)

def test_unsupported_subgroup_has_no_paired_performance_claim():
    s=pd.read_csv(OUT/'models/subgroup_paired_uncertainty.csv')
    u=s[s.group=='Uganda']
    assert u.status.eq('NOT_ESTIMABLE_SUPPORT_GATE').all()
    assert u.brier_diff.isna().all()
