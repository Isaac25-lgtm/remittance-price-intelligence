"""Paired uncertainty, hypothetical review utility and noncausal diagnostics."""
from __future__ import annotations
import gc
import hashlib
import json
import pickle
from pathlib import Path
import numpy as np
import pandas as pd
from rpi import features as F
from rpi.evaluate import capture_at_capacity,metric_row,brier
from rpi.completion_stats import dependence_ci,expected_calibration_error
from completion_models import calibrated
from completion_data import write

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_completion';PRIVATE=OUT/'private_runtime/processed'
KINDS=['corridor','provider','time_block_4','crossed_corridor_provider']

def inference():
    tables=[];paired=[];weighted=[];capacity=[];subgroups=[];capacity_ci=[];yearly=[];yearly_ci=[]
    for label,path in [('legacy',ROOT/'data/processed/test_predictions_lag0.parquet'),('phase2',PRIVATE/'phase2_predictions.parquet')]:
        P=pd.read_parquet(path);y=P.y.astype(int).to_numpy()
        names=[c for c in P if c.startswith(('B0_','B1_','B2_','B3_','B4_','L1_','L2_','M1_','M2_','S_selected'))]
        loss=np.column_stack([(P[n].to_numpy()-y)**2 for n in names])
        probabilities=np.clip(P[names].to_numpy(float),1e-6,1-1e-6)
        log_losses=-(y[:,None]*np.log(probabilities)+(1-y[:,None])*np.log(1-probabilities))
        for year,part in P.groupby('target_year'):
            ys=part.y.astype(int).to_numpy()
            losses=np.column_stack([(part[n].to_numpy()-ys)**2 for n in names])
            for j,n in enumerate(names):yearly.append(dict(analysis=label,target_year=int(year),model=n,n_quarters=part.qidx.nunique(),**metric_row(ys,part[n].to_numpy())))
            for kind in ['corridor','provider']:
                ci=dependence_ci(losses,part,kind)
                for j,n in enumerate(names):yearly_ci.append(dict(analysis=label,target_year=int(year),model=n,brier=losses[:,j].mean(),resampling=kind,ci95_lo=ci[0,j],ci95_hi=ci[1,j],n_quarters=part.qidx.nunique()))
        for kind in KINDS:
            ci=dependence_ci(np.column_stack([loss,log_losses]),P,kind)
            for j,n in enumerate(names):tables.append(dict(analysis=label,model=n,n=len(P),brier=loss[:,j].mean(),resampling=kind,ci95_lo=ci[0,j],ci95_hi=ci[1,j],log_loss=log_losses[:,j].mean(),log_loss_ci95_lo=ci[0,j+len(names)],log_loss_ci95_hi=ci[1,j+len(names)],n_corridors=P.corridor_key.nunique(),n_providers=P['firm__n'].nunique(),n_quarters=P.qidx.nunique()))
        pairs=[('M1_hist_gbm','L2_spline_logistic'),('M2_random_forest','L2_spline_logistic'),('M2_random_forest','M1_hist_gbm')]
        if label=='phase2':pairs += [('S_selected','L2_spline_logistic'),('S_selected','B2_history')]+[(n+'__cal',n) for n in ['L1_ridge_logistic','L2_spline_logistic','M1_hist_gbm','M2_random_forest']]
        if 'B4_recent_history' in names:pairs += [('S_selected','B4_recent_history'),('M2_random_forest','B4_recent_history')]
        dloss=np.column_stack([loss[:,names.index(a)]-loss[:,names.index(b)] for a,b in pairs])
        for kind in KINDS:
            ci=dependence_ci(dloss,P,kind)
            for j,(a,b) in enumerate(pairs):paired.append(dict(analysis=label,model_a=a,model_b=b,brier_diff=dloss[:,j].mean(),resampling=kind,ci95_lo=ci[0,j],ci95_hi=ci[1,j],n_quarters=P.qidx.nunique(),caveat='13 observed target waves; about three four-quarter blocks; exploratory'))
        for field in ['corridor_key','firm__n','qidx']:
            counts=P.groupby(field)[field].transform('size').to_numpy()
            for j,n in enumerate(names):weighted.append(dict(analysis=label,model=n,equal_weight_unit={'corridor_key':'corridor','firm__n':'provider','qidx':'quarter'}[field],brier=np.average(loss[:,j],weights=1/counts)))
        scores={n:1-P[n].to_numpy() for n in names if not n.startswith(('B0_','B1_'))}
        scores['R_highest_cost_rule']=P.cost.to_numpy()
        for n,s in scores.items():
            for cap in [.05,.1,.2,.3]:
                got,k,total=capture_at_capacity(P,s,y,cap)
                capacity.append(dict(analysis=label,rule=n,capacity=cap,n=len(P),reviewed=k,failures_total=total,failures_captured=got,recall=got/total,precision=got/k,lift=(got/k)/(total/len(P)),false_alerts=k-got,missed_failures=total-got,scope='within origin quarter'))
        # Re-rank policies within each resampled corridor cohort; both share capacity.
        rng=np.random.default_rng(20261020);cors=P.corridor_key.unique();idxs={c:np.flatnonzero(P.corridor_key.to_numpy()==c) for c in cors}
        a='M1_hist_gbm' if label=='legacy' else 'S_selected'
        for b in ['R_highest_cost_rule','L2_spline_logistic','B2_history']:
            draws=[]
            for _ in range(300):
                pick=rng.choice(cors,size=len(cors),replace=True);idx=np.concatenate([idxs[c] for c in pick])
                aa,_,_=capture_at_capacity(P.iloc[idx],scores[a][idx],y[idx],.2)
                bb,_,_=capture_at_capacity(P.iloc[idx],scores[b][idx],y[idx],.2)
                draws.append(aa-bb)
            aa,_,_=capture_at_capacity(P,scores[a],y,.2);bb,_,_=capture_at_capacity(P,scores[b],y,.2)
            capacity_ci.append(dict(analysis=label,rule_a=a,rule_b=b,capacity=.2,captured_difference=aa-bb,ci95_lo=np.quantile(draws,.025),ci95_hi=np.quantile(draws,.975),resampling='corridor reranking',reps=300))
        masks={'SSA':P.destination_region=='Sub-Saharan Africa','EAC':P.destination_code.isin(['BDI','COD','KEN','RWA','SOM','SSD','TZA','UGA']),'Uganda':P.destination_code=='UGA'}
        if 'destination_income' in P:
            masks.update({f'income:{v}':P.destination_income==v for v in P.destination_income.unique()})
            masks.update({'no_provider_history':P.n_firm_hist==0,'provider_history_available':P.n_firm_hist>0,'no_corridor_history':P.n_corr_hist==0})
            masks.update({'remote_initiation':P['access point__n'].isin(['internet','mobile phone']),'other_initiation':~P['access point__n'].isin(['internet','mobile phone'])})
        for group,mask in masks.items():
            d=P[mask];failures=int((~d.y.astype(bool)).sum());supported=failures>=100 and len(d)>0
            for n in names:
                r=dict(analysis=label,group=group,model=n,n=len(d),failures=failures,n_corridors=d.corridor_key.nunique(),supported=supported)
                if supported:r.update(metric_row(d.y.astype(int),d[n]))
                else:r['status']='NOT_ESTIMABLE_SUPPORT_GATE'
                subgroups.append(r)
        print('Inference completed',label,flush=True)
    for frame,path in [(tables,'models/absolute_brier_ci.csv'),(paired,'models/paired_dependence.csv'),(weighted,'models/weighting_sensitivity.csv'),(capacity,'models/decision_capacity.csv'),(capacity_ci,'models/decision_capacity_ci.csv'),(subgroups,'models/subgroups.csv')]:write(pd.DataFrame(frame),path)
    write(pd.DataFrame(yearly),'models/performance_by_year.csv');write(pd.DataFrame(yearly_ci),'models/yearly_brier_ci.csv')
    sensitivity_ci=[]
    for scenario in ['heldout_corridor','heldout_provider','strict','threshold_5','cc2','lag_1','no_provider_history','exclude_2021_date_anomaly','exclude_russia']:
        s=pd.read_parquet(PRIVATE/(scenario+'.parquet'));ys=s.y.astype(int).to_numpy()
        ds=np.column_stack([(s[n].to_numpy()-ys)**2-(s.L2_spline_logistic.to_numpy()-ys)**2 for n in ['M1_hist_gbm','M2_random_forest']])
        for kind in ['corridor','provider','time_block_4']:
            ci=dependence_ci(ds,s,kind)
            for j,n in enumerate(['M1_hist_gbm','M2_random_forest']):sensitivity_ci.append(dict(scenario=scenario,model_a=n,model_b='L2_spline_logistic',brier_diff=ds[:,j].mean(),resampling=kind,ci95_lo=ci[0,j],ci95_hi=ci[1,j],n=len(s)))
    write(pd.DataFrame(sensitivity_ci),'models/transfer_sensitivity_paired_ci.csv')
    # Dominance stress: remove the largest DEVELOPMENT group from outer evaluation.
    # This is a cohort-weight sensitivity; actual no-history refits are the group holdouts.
    X=pd.read_parquet(PRIVATE/'features_core.parquet');dev=X[X.primary & (X.target_year<2022)]
    P=pd.read_parquet(PRIVATE/'phase2_predictions.parquet');stress=[]
    for field,label in [('firm__n','provider'),('corridor_key','corridor')]:
        largest=dev.groupby(field).size().sort_values(ascending=False).index[0]
        s=P[P[field]!=largest]
        for n in ['L2_spline_logistic','M1_hist_gbm','M2_random_forest','S_selected']:
            stress.append(dict(omitted_development_unit=label,n_omitted=len(P)-len(s),model=n,scope='evaluation-cohort dominance; no refit; identifier withheld',**metric_row(s.y.astype(int),s[n])))
    write(pd.DataFrame(stress),'models/major_group_dominance_stress.csv')
    # Normalised cost scenarios: no currency, savings, or intervention effect asserted.
    costs=[]
    for r in capacity:
        for miss_cost in [1,5,10]:
            costs.append(dict(analysis=r['analysis'],rule=r['rule'],capacity=r['capacity'],review_cost=1,miss_cost=miss_cost,total_hypothetical_cost=r['reviewed']+(r['failures_total']-r['failures_captured'])*miss_cost,assumption='review perfectly identifies an observed threshold failure; relative cost units only'))
    write(pd.DataFrame(costs),'models/decision_cost_scenarios.csv')
    pd.DataFrame(tables).to_csv(OUT/'tables/table_05_models.csv',index=False)
    pd.DataFrame(capacity).to_csv(OUT/'tables/table_06_decision_capacity.csv',index=False)
    pd.DataFrame(subgroups).to_csv(OUT/'tables/table_07_transfer_subgroups.csv',index=False)
    manifest=[]
    for p in sorted(PRIVATE.glob('*.parquet')):
        d=pd.read_parquet(p)
        manifest.append(dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rows=len(d),classification='PRIVATE ROW DATA; not distributed'))
    (OUT/'models/test_predictions_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

def explain():
    X=pd.read_parquet(PRIVATE/'features_core.parquet');d=X[X.primary & (X.target_year==2024)].copy()
    groups={'current_price':['cost','fx_margin','fee_pct','cost_other_basket','dist_to_threshold'],'provider_history':['h_firm','h_corrfirm','n_firm_hist'],'corridor_history':['h_global','h_corr','n_corr_hist','reob_corr'],'own_lag':['lag_cost','lag_available','lag_delta'],'corridor_composition':['corr_n_services','corr_share_cheap','corr_min_cost','cost_rank_in_corr'],'geography':['source_region','destination_region','source_income','destination_income'],'channel_and_terms':[c for c in F.CATEGORICAL if c not in ['source_region','destination_region','source_income','destination_income','qtr_cat']]}
    rows=[];curves=[];rng=np.random.default_rng(20261020)
    for name in ['L2_spline_logistic','M1_hist_gbm','M2_random_forest']:
        with (OUT/'private_runtime/fit_models'/f'{name}_2024.pkl').open('rb') as f:m,method,cal=pickle.load(f)
        for q,g in d.groupby('qidx'):
            y=g.y.astype(int).to_numpy();base=brier(y,calibrated(m.predict_proba(g)[:,1],method,cal))
            for group,cols in groups.items():
                vals=[]
                for rep in range(3):
                    v=g.copy();v[cols]=g[cols].to_numpy()[rng.permutation(len(g))]
                    vals.append(brier(y,calibrated(m.predict_proba(v)[:,1],method,cal))-base)
                rows.append(dict(model=name,origin_qidx=q,feature_group=group,n=len(g),mean_brier_increase=np.mean(vals),min_brier_increase=min(vals),max_brier_increase=max(vals),reps=3,interpretation='associative grouped permutation; correlated/off-manifold combinations possible'))
        # Actual observed-price bins preserve the fee+FX accounting identity and
        # corridor composition, avoiding impossible counterfactual price vectors.
        response=d[['cost','y']].copy();response['pred']=calibrated(m.predict_proba(d)[:,1],method,cal)
        response['bin']=pd.cut(response.cost,np.linspace(0,3,13),include_lowest=True)
        for _,g in response.groupby('bin',observed=True):
            curves.append(dict(model=name,current_cost=g.cost.mean(),mean_predicted_stay=g.pred.mean(),observed_stay=g.y.astype(float).mean(),local_observed_n=len(g),caveat='descriptive observed-cost bin; actual covariates; not a partial/causal effect'))
        del m;gc.collect();print('Explainability',name,flush=True)
    write(pd.DataFrame(rows),'models/permutation_importance.csv');write(pd.DataFrame(curves),'models/partial_response.csv')

if __name__=='__main__':
    import sys
    (explain if sys.argv[-1]=='explain' else inference)()
