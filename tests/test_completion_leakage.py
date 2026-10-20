import numpy as np
import pandas as pd
from rpi import features as F,linkage as L
from tests.conftest import make_clean

def test_holdout_outcomes_cannot_enter_histories():
    rows=[dict(year=2020,qtr=q,firm=firm,**{'cc1 total cost %':1. if q%2 else 4.}) for q in range(1,5) for firm in ['Train','Holdout']]
    lk=L.link_next_quarter(L.service_table(make_clean(rows)))
    allowed=lk['firm__n']=='train'
    a=F.build(lk,history_allowed=allowed)
    b=lk.copy();b.loc[~allowed,'cost_next']=100.
    b=F.build(b,history_allowed=allowed)
    hist=['h_global','h_corr','h_firm','h_corrfirm','n_corr_hist','n_firm_hist','reob_corr']
    pd.testing.assert_frame_equal(a[hist],b[hist])
    held=a[a['firm__n']=='holdout']
    assert (held.n_firm_hist==0).all()
    assert np.allclose(held.h_firm,held.h_global)

def test_all_feature_values_ignore_target_replacement_for_fixed_origins():
    rows=[dict(year=2020,qtr=q,firm=f'F{j}',**{'cc1 total cost %':1.}) for q in range(1,5) for j in range(3)]
    lk=L.link_next_quarter(L.service_table(make_clean(rows)))
    a=F.build(lk)
    q=lk.qidx.min()+1
    b=lk.copy();b.loc[b.target_qidx>q,'cost_next']=999.
    b=F.build(b)
    cols=F.NUMERIC+F.CATEGORICAL
    pd.testing.assert_frame_equal(a.loc[a.qidx==q,cols].reset_index(drop=True),b.loc[b.qidx==q,cols].reset_index(drop=True))
