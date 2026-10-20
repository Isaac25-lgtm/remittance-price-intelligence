import numpy as np
import pandas as pd
import pytest
from rpi.completion_stats import dependence_ci,resample_weights,stable_holdout

@pytest.mark.parametrize('kind',['corridor','provider','crossed_corridor_provider','time_block_4'])
def test_whole_cells_and_zero_paired_loss(kind):
    f=pd.DataFrame({'corridor_key':np.tile(np.repeat(['a','a','b','b'],2),4),'firm__n':np.tile(np.repeat(['x','y','x','y'],2),4),'qidx':np.repeat(np.arange(4),8)})
    w=resample_weights(f.corridor_key,f['firm__n'],f.qidx,kind,np.random.default_rng(3))
    assert np.all(w>=0) and np.all(w[::2]==w[1::2])
    assert np.array_equal(dependence_ci(np.zeros(len(f)),f,kind,reps=30),np.zeros((2,1)))

def test_crossed_weights_factor_into_cluster_counts():
    c=np.repeat(['a','b','c'],3);p=np.tile(['x','y','z'],3);q=np.ones(9)
    w=resample_weights(c,p,q,'crossed_corridor_provider',np.random.default_rng(5)).reshape(3,3)
    assert np.linalg.matrix_rank(w)<=1

def test_block_resamples_all_quotes_of_quarter():
    q=np.repeat(np.arange(13),3)
    w=resample_weights(q,q,q,'time_block_4',np.random.default_rng(4))
    assert all(len(set(w[q==i]))==1 for i in range(13))
    assert w.sum()==len(q)

def test_holdout_independent_of_row_order():
    a=['a','b','c','d']
    assert np.array_equal(stable_holdout(a),stable_holdout(a[::-1])[::-1])
