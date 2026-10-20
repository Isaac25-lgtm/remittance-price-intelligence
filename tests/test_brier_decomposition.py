import importlib.util
from pathlib import Path
import numpy as np
spec=importlib.util.spec_from_file_location('supp',Path(__file__).resolve().parents[1]/'scripts/completion_score_supplement.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_binned_identity_and_unbinned_residual_are_distinct():
    y=np.array([0.,1.,1.,0.]);p=np.array([.11,.19,.81,.89])
    r=m.decomposition(y,p)
    assert np.isclose(r['raw_brier'],np.mean((p-y)**2))
    assert np.isclose(r['binned_brier'],r['uncertainty']-r['resolution']+r['reliability'])
    assert np.isclose(r['raw_brier'],r['binned_brier']+r['binning_residual'])
    assert abs(r['binning_residual'])>0
