import numpy as np
import pandas as pd
import pickle
import pytest
from rpi.models import MODELS
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

@pytest.mark.parametrize('name',['L1_ridge_logistic','L2_spline_logistic','M1_hist_gbm','M2_random_forest'])
def test_fold_transformers_ignore_unseen_test_distribution_and_outcome_columns(name):
    rng=np.random.default_rng(20261020)
    train=pd.DataFrame({c:rng.uniform(.1,2,80) for c in F.NUMERIC})
    for c in F.CATEGORICAL:train[c]=['training_a']*40+['training_b']*40
    train.loc[:5,'cost']=np.nan
    y=np.tile([0,1],40)
    model=MODELS[name]().fit(train,y)
    test=train.iloc[:12].copy();test[F.NUMERIC]=test[F.NUMERIC]+10000
    test[F.CATEGORICAL]='never_seen_test_category'
    before=pickle.dumps(model.named_steps['pre'])
    p=model.predict_proba(test)
    poisoned=test.assign(cost_next=999,status='future_failure',y=0)
    assert np.allclose(p,model.predict_proba(poisoned))
    assert before==pickle.dumps(model.named_steps['pre'])
    assert np.isfinite(p).all() and ((p>=0)&(p<=1)).all()
