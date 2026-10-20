"""Bounded chronological model/calibration selection; private predictions and artifacts."""
from __future__ import annotations
import argparse
import gc
import json
import pickle
import time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression,Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error,mean_squared_error
from rpi import config,features as F,linkage as L
from rpi.models import MODELS
from rpi.evaluate import brier,metric_row,reliability_bins,capture_at_capacity
from rpi.completion_stats import stable_holdout,expected_calibration_error
from rpi.preprocess import load_clean,qlabel
from completion_data import linked_variant,write

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_completion';PRIVATE=OUT/'private_runtime/processed'
FAMILIES=['L1_ridge_logistic','L2_spline_logistic','M1_hist_gbm','M2_random_forest']
PREF=['L2_spline_logistic','L1_ridge_logistic','M1_hist_gbm','M2_random_forest']

def params_for(name):
    if name=='L1_ridge_logistic':return [{'clf__C':v} for v in [.1,1.,10.]]
    if name=='M1_hist_gbm':return [{'clf__max_leaf_nodes':7,'clf__max_iter':150},{'clf__max_leaf_nodes':15,'clf__max_iter':300}]
    if name=='M2_random_forest':return [{'clf__min_samples_leaf':20},{'clf__min_samples_leaf':50}]
    return [{}]

def logit(p):
    p=np.clip(p,1e-6,1-1e-6);return np.log(p/(1-p))[:,None]

def calibrated(p,method,calibrator):
    if method=='none':return p
    if method=='sigmoid':return calibrator.predict_proba(logit(p))[:,1]
    return np.clip(calibrator.predict(p),1e-6,1-1e-6)

def metrics(P,names,scenario):
    rows=[]
    for scope,d in [('pooled',P)]+[(str(q),g) for q,g in P.groupby('qidx')]:
        y=d.y.astype(int).to_numpy()
        if len(np.unique(y))<2:
            for name in names:rows.append(dict(scenario=scenario,scope=scope,model=name,n=len(d),status='NOT_ESTIMABLE_SINGLE_CLASS'))
            continue
        for name in names:
            p=d[name].to_numpy()
            rows.append(dict(scenario=scenario,scope=scope,model=name,status='ESTIMABLE',failures=int((1-y).sum()),ece=expected_calibration_error(y,p),**metric_row(y,p)))
    return pd.DataFrame(rows)

def base_output(d):
    cols=['source_row','qidx','target_qidx','target_year','corridor_key','firm__n','destination_region','destination_income','destination_code','source_code','cost','y','access point__n','n_firm_hist','n_corr_hist','lag_available']
    return d[[c for c in cols if c in d]].copy()

def nested():
    X=pd.read_parquet(PRIVATE/'features_core.parquet');prim=X[X.primary].copy()
    predictions=[];registry=[];splits=[];calibration=[];selection=[]
    modeldir=OUT/'private_runtime/fit_models';modeldir.mkdir(parents=True,exist_ok=True)
    for year in [2022,2023,2024,2025]:
        cache=PRIVATE/f'nested_{year}.parquet'
        meta=PRIVATE/f'nested_{year}.json'
        if cache.exists() and meta.exists():
            predictions.append(pd.read_parquet(cache));m=json.loads(meta.read_text(encoding='utf-8'))
            registry+=m['registry'];splits+=m['splits'];calibration+=m['calibration'];selection+=m['selection'];print('CACHED',year,flush=True);continue
        reg=[];spl=[];ca=[];sel=[]
        test=prim[prim.target_year==year].copy();first=int(test.qidx.min())
        train=prim[prim.target_qidx<first]
        quarters=np.sort(train.target_qidx.unique())
        if len(quarters)<10:raise ValueError('insufficient chronological training')
        six=quarters[-6:];proper=train[train.target_qidx<six[0]]
        tune=train[train.target_qidx.isin(six[:2])];cal=train[train.target_qidx.isin(six[2:4])]
        val=train[train.target_qidx.isin(six[4:])];base=train[train.target_qidx<six[2]]
        assert proper.target_qidx.max()<tune.target_qidx.min()<cal.target_qidx.min()<val.target_qidx.min()<first
        out=base_output(test);selected_scores={}
        for role,d in [('proper',proper),('tuning',tune),('calibration',cal),('selection',val),('base_refit',base),('outer_test',test)]:
            spl.append(dict(year=year,role=role,n=len(d),target_start=qlabel(int(d.target_qidx.min())),target_end=qlabel(int(d.target_qidx.max())),failures=int((~d.y.astype(bool)).sum()),n_corridors=d.corridor_key.nunique(),n_providers=d['firm__n'].nunique(),previously_inspected=True,decision_date='UNVERIFIED; retrospective survey clock'))
        for name in MODELS:
            t0=time.monotonic();best_params={};best=np.inf
            if name in FAMILIES:
                for params in params_for(name):
                    m=MODELS[name]().set_params(**params).fit(proper,proper.y.astype(int))
                    score=brier(tune.y.to_numpy(),m.predict_proba(tune)[:,1])
                    reg.append(dict(year=year,model=name,stage='tune',parameters=params,tuning_brier=score,n_train=len(proper),seconds=round(time.monotonic()-t0,2)))
                    if score<best:best=score;best_params=params
                    del m;gc.collect()
            m=MODELS[name]()
            if best_params:m.set_params(**best_params)
            m.fit(base,base.y.astype(int))
            pt=m.predict_proba(test)[:,1];pv=m.predict_proba(val)[:,1];pc=m.predict_proba(cal)[:,1]
            out[name]=pt
            best_method='none';best_cal=None;best_val=brier(val.y.to_numpy(),pv)
            if name in FAMILIES:
                calibrators={'none':None,'sigmoid':LogisticRegression(C=1e6,max_iter=1000).fit(logit(pc),cal.y.astype(int)), 'isotonic':IsotonicRegression(out_of_bounds='clip').fit(pc,cal.y.astype(int))}
                for method,c in calibrators.items():
                    pred=calibrated(pv,method,c)
                    score=brier(val.y.to_numpy(),pred)
                    ca.append(dict(year=year,model=name,method=method,selection_n=len(val),selection_brier=score,calibration_n=len(cal)))
                    if score<best_val-1e-12:best_val=score;best_method=method;best_cal=c
                out[name+'__cal']=calibrated(pt,best_method,best_cal)
                selected_scores[name]=best_val
                artifact=(m,best_method,best_cal)
                with (modeldir/f'{name}_{year}.pkl').open('wb') as f:pickle.dump(artifact,f)
                with (modeldir/f'{name}_{year}.pkl').open('rb') as f:loaded=pickle.load(f)
                assert np.allclose(calibrated(loaded[0].predict_proba(test)[:,1],loaded[1],loaded[2]),out[name+'__cal'],atol=1e-12)
                ca.append(dict(year=year,model=name,method='CHOSEN_'+best_method,selection_n=len(val),selection_brier=best_val,calibration_n=len(cal)))
            reg.append(dict(year=year,model=name,stage='outer_score',parameters=best_params,calibration=best_method,n_train=len(base),n_test=len(test),seconds=round(time.monotonic()-t0,2)))
            print(year,name,best_params,best_method,flush=True);del m;gc.collect()
        cutoff=min(selected_scores.values())+.002
        chosen=next(n for n in PREF if selected_scores[n]<=cutoff)
        out['S_selected']=out[chosen+'__cal']
        sel.append(dict(year=year,chosen_model=chosen,selection_brier=selected_scores[chosen],minimum_selection_brier=min(selected_scores.values()),tolerance=.002,operationally_selected=False))
        out.to_parquet(cache,index=False)
        meta.write_text(json.dumps(dict(registry=reg,splits=spl,calibration=ca,selection=sel),indent=2),encoding='utf-8')
        predictions.append(out);registry+=reg;splits+=spl;calibration+=ca;selection+=sel
    P=pd.concat(predictions,ignore_index=True);P.to_parquet(PRIVATE/'phase2_predictions.parquet',index=False)
    names=list(MODELS)+[n+'__cal' for n in FAMILIES]+['S_selected']
    mt=metrics(P,names,'nested_retrospective')
    write(mt[mt.scope=='pooled'],'models/model_comparison.csv');write(mt[mt.scope!='pooled'],'models/performance_by_wave.csv')
    write(pd.DataFrame(splits),'validation/split_registry.csv');write(pd.DataFrame(splits),'tables/table_04_split_features.csv')
    write(pd.DataFrame(calibration),'models/calibration_selection.csv');write(pd.DataFrame(selection),'models/annual_selection.csv')
    (OUT/'models/model_registry.json').write_text(json.dumps(registry,indent=2),encoding='utf-8')
    rel=pd.concat([reliability_bins(P.y.astype(int),P[n]).assign(model=n) for n in names if P[n].nunique()>1],ignore_index=True)
    rel['observed_stays']=rel.n*rel.obs_rate;rel['observed_failures']=rel.n-rel.observed_stays
    write(rel,'models/calibration.csv')

def fixed_annual(X,scenario,heldout=None):
    prim=X[X.primary].copy();out=[];reg=[]
    for year in [2022,2023,2024,2025]:
        test=prim[prim.target_year==year].copy()
        if heldout is not None:test=test[stable_holdout(test[heldout])]
        if test.empty:continue
        train=prim[prim.target_qidx<test.qidx.min()]
        if heldout is not None:train=train[~stable_holdout(train[heldout])]
        assert train.target_qidx.max()<test.qidx.min()
        if heldout is not None:assert set(train[heldout]).isdisjoint(set(test[heldout]))
        p=base_output(test)
        for n in ['B2_history','L2_spline_logistic','M1_hist_gbm','M2_random_forest']:
            m=MODELS[n]().fit(train,train.y.astype(int));p[n]=m.predict_proba(test)[:,1]
            reg.append(dict(scenario=scenario,year=year,model=n,n_train=len(train),n_test=len(test),train_last_target=qlabel(int(train.target_qidx.max()))))
            del m;gc.collect()
        out.append(p);print(scenario,year,flush=True)
    return pd.concat(out,ignore_index=True),reg

def transfer_and_sensitivity():
    df=load_clean();lk=pd.read_parquet(PRIVATE/'linked_core.parquet');summaries=[];regs=[]
    for field in ['corridor_key','firm__n']:
        scenario='heldout_'+('corridor' if field=='corridor_key' else 'provider')
        cache=PRIVATE/(scenario+'.parquet')
        if cache.exists():P=pd.read_parquet(cache)
        else:
            allowed=~stable_holdout(lk[field]);X=F.build(lk,history_allowed=allowed)
            P,reg=fixed_annual(X,scenario,field);regs+=reg;P.to_parquet(cache,index=False);del X;gc.collect()
        summaries.append(metrics(P,['B2_history','L2_spline_logistic','M1_hist_gbm','M2_random_forest'],scenario))
    for scenario in ['strict','threshold_5','cc2','lag_1','no_provider_history','exclude_2021_date_anomaly','exclude_russia']:
        cache=PRIVATE/(scenario+'.parquet')
        if cache.exists():P=pd.read_parquet(cache)
        else:
            a=linked_variant(df,scenario) if scenario in ['strict','cc2','exclude_2021_date_anomaly','exclude_russia'] else lk
            X=F.build(a,release_lag=1 if scenario=='lag_1' else 0,threshold=5 if scenario=='threshold_5' else 3)
            if scenario=='no_provider_history':
                X['h_firm']=X.h_global;X['h_corrfirm']=X.h_corr;X['n_firm_hist']=0.
            P,reg=fixed_annual(X,scenario);regs+=reg;P.to_parquet(cache,index=False);del X;gc.collect()
        summaries.append(metrics(P,['B2_history','L2_spline_logistic','M1_hist_gbm','M2_random_forest'],scenario))
    write(pd.concat(summaries,ignore_index=True),'models/transfer_sensitivity_metrics.csv')
    (OUT/'models/transfer_sensitivity_registry.json').write_text(json.dumps(regs,indent=2),encoding='utf-8')

def observation():
    X=pd.read_parquet(PRIVATE/'features_core.parquet')
    R=X[X.status.isin(['core_reobserved','core_unobserved_corridor_surveyed'])].copy()
    R['r']=(R.status=='core_reobserved').astype(int)
    rows=[];ipw=[];pr=[]
    for year in [2022,2023,2024,2025]:
        test=R[R.target_year==year];train=R[R.target_qidx<test.qidx.min()]
        for name in ['B1_prevalence','L1_ridge_logistic','M1_hist_gbm']:
            m=MODELS[name]().fit(train,train.r)
            p=m.predict_proba(test)[:,1]
            rows.append(dict(year=year,model=name,endpoint='core_reobserved',**metric_row(test.r.to_numpy(),p)))
        rows.append(dict(year=year,model='corridor_history',endpoint='core_reobserved',**metric_row(test.r.to_numpy(),test.reob_corr.to_numpy())))
        # IPW targets valid-price observation, not just a matched quote.
        m=MODELS['L1_ridge_logistic']().fit(train,train.primary.astype(int))
        p=m.predict_proba(test)[:,1];clipped=np.clip(p,.05,.95);obs=test.primary.to_numpy()
        w=1/clipped[obs];y=test.loc[obs,'y'].astype(float).to_numpy()
        ipw.append(dict(year=year,n_eligible=len(test),n_observed=int(obs.sum()),observed_stay=float(y.mean()),ipw_mar_p_stay=float(np.average(y,weights=w)),effective_sample_size=float(w.sum()**2/(w*w).sum()),min_probability=float(p.min()),max_probability=float(p.max()),share_clipped=float(((p<.05)|(p>.95)).mean()),assumption='MAR conditional on measured origin/history; corridor-surveyed unambiguous origin scope'))
    write(pd.DataFrame(rows),'models/reobservation_models.csv');write(pd.DataFrame(ipw),'models/ipw_mar_scenario.csv')

def continuous():
    X=pd.read_parquet(PRIVATE/'features_core.parquet')
    # A distinct estimand: next cost among initially cheap, valid matched records.
    X=X[X.primary].copy()
    rows=[]
    for year in [2022,2023,2024,2025]:
        test=X[X.target_year==year];train=X[X.target_qidx<test.qidx.min()]
        for name,m in [('last_cost',None),('ridge',make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),Ridge(alpha=10))),('hist_absolute_error',make_pipeline(SimpleImputer(strategy='median'),HistGradientBoostingRegressor(loss='absolute_error',max_iter=150,max_leaf_nodes=7,min_samples_leaf=50,random_state=20261020)))]:
            p=test.cost.to_numpy() if m is None else m.fit(train[F.NUMERIC],train.cost_next).predict(test[F.NUMERIC])
            rows.append(dict(year=year,model=name,n=len(test),mae=mean_absolute_error(test.cost_next,p),rmse=float(np.sqrt(mean_squared_error(test.cost_next,p))),endpoint='continuous_next_cost_conditional_reobservation'))
    write(pd.DataFrame(rows),'models/continuous_cost_metrics.csv')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['nested','transfer','observation','continuous']);a=ap.parse_args()
    {'nested':nested,'transfer':transfer_and_sensitivity,'observation':observation,'continuous':continuous}[a.stage]()
