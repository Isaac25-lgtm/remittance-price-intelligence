"""Dependence sensitivities for retrospective paired losses, with explicit sampling units."""
from __future__ import annotations

import numpy as np
import pandas as pd


def resample_weights(corridor, provider, quarter, kind, rng, block=4):
    """Whole-cluster weights; pigeonhole uses independent crossed cluster multiplicities.

    Circular blocks resample ordered *observed* quarters, retaining all rows of each wave.
    Caller must report gaps in observed quarters. This is a sensitivity, not proof of
    precision with few independent time blocks or a design-based survey estimator.
    """
    arrays = [np.asarray(corridor), np.asarray(provider), np.asarray(quarter)]
    codes = [pd.factorize(a, sort=True)[0] for a in arrays]
    sizes = [int(c.max()+1) for c in codes]
    if kind in ('corridor','provider'):
        i=0 if kind=='corridor' else 1
        draws=rng.integers(sizes[i],size=sizes[i])
        return np.bincount(draws,minlength=sizes[i])[codes[i]].astype(float)
    if kind in ('crossed_corridor_provider','crossed_corridor_provider_time_block'):
        w=np.ones(len(arrays[0]))
        for i in (0,1):
            draws=rng.integers(sizes[i],size=sizes[i])
            w*=np.bincount(draws,minlength=sizes[i])[codes[i]]
        if kind=='crossed_corridor_provider_time_block':
            n=sizes[2]
            starts=rng.integers(n,size=int(np.ceil(n/block)))
            draw=np.concatenate([(s+np.arange(block))%n for s in starts])[:n]
            w*=np.bincount(draw,minlength=n)[codes[2]]
        return w
    if kind=='time_block_4':
        n=sizes[2]
        starts=rng.integers(n,size=int(np.ceil(n/block)))
        draw=np.concatenate([(s+np.arange(block))%n for s in starts])[:n]
        return np.bincount(draw,minlength=n)[codes[2]].astype(float)
    raise ValueError(kind)


def dependence_ci(values, frame, kind, reps=1000, seed=20261020):
    v=np.asarray(values,float)
    if v.ndim==1:v=v[:,None]
    if not np.isfinite(v).all():raise ValueError('non-finite losses')
    rng=np.random.default_rng(seed)
    boots=[]
    args=[frame[c].to_numpy() for c in ['corridor_key','firm__n','qidx']]
    for _ in range(reps):
        w=resample_weights(*args,kind,rng)
        if w.sum()>0:boots.append((v*w[:,None]).sum(0)/w.sum())
    if len(boots)<reps*.95:raise ValueError('too few nonempty bootstrap draws')
    b=np.asarray(boots)
    return np.quantile(b,[.025,.975],axis=0)


def stable_holdout(values):
    import hashlib
    return np.array([int(hashlib.sha256(str(x).encode()).hexdigest()[:8],16)%5==0 for x in values])


def expected_calibration_error(y,p,bins=10):
    d=pd.DataFrame({'obs':np.asarray(y,float),'pred':np.asarray(p,float)})
    # Equal-width bins preserve ties; empty bins contribute zero.
    d['bin']=np.minimum((d['pred']*bins).astype(int),bins-1)
    g=d.groupby('bin').agg(n=('obs','size'),obs=('obs','mean'),pred=('pred','mean'))
    return float((g.n*(g.obs-g.pred).abs()).sum()/len(d))
