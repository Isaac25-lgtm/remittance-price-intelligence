"""Adversarial reproduction checks, not data reproduction."""
import importlib.util
from pathlib import Path
import pandas as pd

spec=importlib.util.spec_from_file_location('reproducer',Path(__file__).resolve().parents[1]/'scripts/reproduce_from_cache.py')
rep=importlib.util.module_from_spec(spec);spec.loader.exec_module(rep)

def test_different_science_cannot_exit_success():
    assert rep.comparison_exit_code([{'status':'DIFFERS'}])==1
    assert rep.comparison_exit_code([{'status':'NOT_REGENERATED'}])==1
    assert rep.comparison_exit_code([])==1
    assert rep.comparison_exit_code([{'status':'MATCH'},{'status':'MATCH_EXCEPT_TIMING'}])==0

def test_timing_and_scientific_changes_distinguished(tmp_path):
    a,b=tmp_path/'a.csv',tmp_path/'b.csv'
    pd.DataFrame({'brier':[.1],'fit_seconds':[1]}).to_csv(a,index=False)
    pd.DataFrame({'brier':[.1],'fit_seconds':[3]}).to_csv(b,index=False)
    assert rep.compare_csv(a,b)['status']=='MATCH_EXCEPT_TIMING'
    pd.DataFrame({'brier':[.2],'fit_seconds':[1]}).to_csv(b,index=False)
    assert rep.compare_csv(a,b)['status']=='DIFFERS'

def test_presentation_is_not_claimed_regenerated():
    assert len(rep.GENERATED_NAMES)==30
    assert not any(n.startswith('presentation_') for n in rep.GENERATED_NAMES)
