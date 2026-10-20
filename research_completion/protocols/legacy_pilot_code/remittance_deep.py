from common import *
import pandas as pd,numpy as np,re
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import brier_score_loss,log_loss,roc_auc_score,average_precision_score
T=time.monotonic();rng=np.random.default_rng(20261017);O=ROOT/'runs/N2';O.mkdir(parents=True,exist_ok=True)
source=LAB/'discovery_round3/data/rpw_post2016.parquet'
cols=['id','period','corridor','firm','firm_type','payment instrument','access point','speed actual','cc1 lcu amount','cc1 total cost %','cc1 lcu fee','cc1 fx margin','transparent','receiving network coverage','pickup location','pickup method','source_income','destination_income']
d=pd.read_parquet(source,columns=cols);d.columns=[re.sub('[^a-z0-9]+','_',x.lower()).strip('_') for x in d.columns]
d['origin']=np.arange(len(d));d['year']=d.period.str.extract('(20[0-9]{2})')[0].astype(int);d['quarter']=d.period.str.extract('_([1-4])Q')[0].astype(int);d['t']=4*d.year+d.quarter
for c in ['cc1_lcu_amount','cc1_total_cost','cc1_lcu_fee','cc1_fx_margin']:d[c]=pd.to_numeric(d[c],errors='coerce')
d['cost']=d.cc1_total_cost
core=['corridor','firm','payment_instrument','access_point','pickup_method','pickup_location','cc1_lcu_amount'];strict=core+['speed_actual','receiving_network_coverage']
for k in strict:d[k]=d[k].fillna('UNSPECIFIED').astype(str).str.strip()
ok=d.transparent.str.strip().str.lower().eq('yes')&d.cost.notna()&d.cost.ge(0)
v=d[ok].copy();views={};audit=[];present=set(zip(d.corridor,d.t))
for label,key in [('core',core),('strict',strict)]:
 dup=v.duplicated(key+['t'],keep=False);x=v[~dup].copy();x['next_t']=x.t+1
 rhs=x[key+['t','cost','speed_actual','receiving_network_coverage']].copy()
 # Only add outcome attributes not already used as join keys.
 rhs=rhs.loc[:,~rhs.columns.duplicated()].rename(columns={'t':'next_t','cost':'next_cost',**{c:'next_'+c for c in ['speed_actual','receiving_network_coverage'] if c not in key}})
 p=x.merge(rhs,on=key+['next_t'],how='left',validate='many_to_one',suffixes=('','_nextattr'))
 p=p[[((c,t) in present) for c,t in zip(p.corridor,p.next_t)]];p['observed_next']=p.next_cost.notna();views[label]=p
 audit.append(dict(definition=label,valid_source_rows=len(v),duplicate_source_rows_excluded=int(dup.sum()),adjacent_origins=len(p)))
c=views['core'];s=views['strict'];common=c.merge(s[['origin','observed_next','next_cost']],on='origin',suffixes=('_core','_strict'),validate='one_to_one')
rows=[]
for period,base in [('all',common),('2023_on',common[common.year.ge(2023)])]:
 for threshold in [3,5]:
  g=base[base.cost.le(threshold)];lost=~g.observed_next_strict & g.observed_next_core
  sc=g.speed_actual.ne(g.next_speed_actual);nc=g.receiving_network_coverage.ne(g.next_receiving_network_coverage)
  rows.append(dict(period=period,threshold=threshold,common_origins=len(g),core_observed=int(g.observed_next_core.sum()),strict_observed=int(g.observed_next_strict.sum()),strict_missing_but_core_observed=int(lost.sum()),speed_changed_among_recovered=int((lost&sc).sum()),network_changed_among_recovered=int((lost&nc).sum()),either_attribute_changed=int((lost&(sc|nc)).sum()),core_missing=int((~g.observed_next_core).sum())))
pd.DataFrame(rows).to_csv(O/'common_support_mechanism.csv',index=False)
long=[]
for (year,q),g in c.groupby(['year','quarter']):
 for threshold in [3,5]:
  z=g[g.cost.le(threshold)];n=len(z);seen=z.observed_next;stay=z.next_cost.le(threshold)&seen
  if n:long.append(dict(year=int(year),quarter=int(q),threshold=threshold,n=n,reobserved=int(seen.sum()),still_cheap=int(stay.sum()),conditional=float(stay[seen].mean()),lower=float(stay.mean()),upper=float((stay|~seen).mean())))
pd.DataFrame(long).to_csv(O/'long_panel_continuity.csv',index=False)
# A source-field sample for direct human inspection, not validation against unobserved real services.
common['link_stratum']=np.where(common.observed_next_strict,'strict_reobserved',np.where(common.observed_next_core,'attribute_changed_reobserved','not_reobserved'))
sample=common.groupby('link_stratum',group_keys=False).apply(lambda g:g.sample(min(10,len(g)),random_state=20261017),include_groups=False)
sample[['origin','period','corridor','firm','payment_instrument','access_point','pickup_method','pickup_location','speed_actual','next_speed_actual','receiving_network_coverage','next_receiving_network_coverage','cost','next_cost_core','observed_next_strict']].to_csv(O/'stratified_source_review_30.csv',index=False)
# Corridor-level: observed survey presence, not actual consumer accessibility.
cov=d[ok].groupby(['corridor','t']).agg(min_cost=('cost','min'),firms=('firm','nunique')).reset_index();cov['next_t']=cov.t+1
co=cov.merge(cov[['corridor','t','min_cost','firms']].rename(columns={'t':'next_t','min_cost':'next_min','firms':'next_firms'}),on=['corridor','next_t'],how='inner')
g=co[co.min_cost.le(3)];corr=dict(initial_cheap_corridor_periods=len(g),next_has_surveyed_cheap=int(g.next_min.le(3).sum()),conditional=float(g.next_min.le(3).mean()),not_population_availability=True)
save('runs/N2/data_audit.json',dict(raw_rows=len(d),views=audit,common_support=rows,corridor_availability=corr,source_fields_reviewed='30 stratified records exported for inspection; no stable-identity/market-exit truth available',asof_release_limitation='Historical public RPW release dates not reconstructed; model is a quote-information exploratory backtest.'))
record('N2','new_identity_common_support_audit',[source],time.monotonic()-T,dict(common_support=rows,corridor_availability=corr));print('N2_COMMON',json.dumps(rows),flush=True)

protocol('N2_MODEL','Exploratory counterfactual quote-information backtest conditional on exact CORE reobservation, origin cost <=3%. No alias matching. Reobservation is separately assessed with prevalence/logistic. Two expanding temporal evaluations: train origins <=2021 / evaluate2022; train<=2022 / evaluate2023; train<=2023 / evaluate2024. All these periods have been inspected in aggregate: EXPLORATORY_BACKTEST, not untouched confirmation. Predictors current quote cost/FX/fee/quarter and contemporary service types/income bins, no future attributes. Fixed logistic C1 and histogram gradient boosting 60 iterations, 7 leaves, minleaf40, learningrate.07. Comparator current-cheap persistence p1 and shrinkage empirical corridor/provider rates, global training prevalence and logistic. Primary paired Brier vs logistic and best training-only baseline; logloss/calibration/AUROC/PR secondary, corridor-cluster bootstrap1999. Group bootstrap does not fully resolve provider/time cross-dependence. No causal welfare, public-release as-of deployment or claimed first-ever model. Stop AI promotion unless incremental benefit and practical consequence survive these limits.')
T=time.monotonic()
num=['cost','cc1_lcu_fee','cc1_fx_margin','quarter'];cat=['firm_type','payment_instrument','access_point','pickup_method','speed_actual','source_income','destination_income']
for col in cat:c[col]=c[col].fillna('UNSPECIFIED').astype(str)
for col in num:c[col]=pd.to_numeric(c[col],errors='coerce').astype(float)
preds=[];metrics=[];observ_metrics=[]
for testyear in [2022,2023,2024]:
 # Require target quarter before test-origin period starts for training information.
 train=c[c.next_t.lt(testyear*4+1)];test=c[c.year.eq(testyear)]
 cheaptrain=train[train.cost.le(3)&train.observed_next];cheaptest=test[test.cost.le(3)&test.observed_next]
 y=cheaptrain.next_cost.le(3).astype(int);yt=cheaptest.next_cost.le(3).astype(int)
 prep=ColumnTransformer([('n',make_pipeline(SimpleImputer(strategy='median'),StandardScaler()),num),('c',OneHotEncoder(handle_unknown='ignore',sparse_output=False),cat)])
 logistic=make_pipeline(prep,LogisticRegression(C=1,max_iter=400));logistic.fit(cheaptrain[num+cat],y)
 enc=ColumnTransformer([('n',SimpleImputer(strategy='median'),num),('c',OrdinalEncoder(handle_unknown='use_encoded_value',unknown_value=-1),cat)])
 xb=enc.fit_transform(cheaptrain[num+cat]);xt=enc.transform(cheaptest[num+cat])
 model=HistGradientBoostingClassifier(max_iter=60,max_leaf_nodes=7,min_samples_leaf=40,learning_rate=.07,random_state=20261017,categorical_features=list(range(len(num),len(num)+len(cat))))
 model.fit(xb,y)
 prior=float(y.mean());pr={'current_cheap_persistence':np.ones(len(yt)),'training_prevalence':np.full(len(yt),prior),'logistic':logistic.predict_proba(cheaptest[num+cat])[:,1],'hist_boost':model.predict_proba(xt)[:,1]}
 for group in ['corridor','firm']:
  tab=pd.DataFrame({'group':cheaptrain[group],'y':y}).groupby('group').y.agg(['sum','count']);rates=(tab['sum']+20*prior)/(tab['count']+20)
  pr[group+'_historical']=cheaptest[group].map(rates).fillna(prior).to_numpy()
 for name,pred in pr.items():metrics.append(dict(testyear=testyear,model=name,n=len(yt),train_n=len(y),corridors=int(cheaptest.corridor.nunique()),brier=brier_score_loss(yt,pred),logloss=log_loss(yt,np.clip(pred,1e-6,1-1e-6)),observed=float(yt.mean()),predicted=float(np.mean(pred)),roc_auc=roc_auc_score(yt,pred) if len(set(yt))>1 else None,pr_auc=average_precision_score(yt,pred)))
 f=pd.DataFrame({'origin':cheaptest.origin,'year':testyear,'corridor':cheaptest.corridor,'firm':cheaptest.firm,'y':yt,'p_logistic':pr['logistic'],'p_boost':pr['hist_boost']});preds.append(f)
 # Same cheap-origin frame, separate whether next core quote is observed.
 ot=train[train.cost.le(3)];oe=test[test.cost.le(3)];oy=ot.observed_next.astype(int);oyt=oe.observed_next.astype(int)
 obs=make_pipeline(ColumnTransformer([('n',make_pipeline(SimpleImputer(strategy='median'),StandardScaler()),num),('c',OneHotEncoder(handle_unknown='ignore',sparse_output=False),cat)]),LogisticRegression(C=1,max_iter=400));obs.fit(ot[num+cat],oy);op=obs.predict_proba(oe[num+cat])[:,1]
 observ_metrics.append(dict(testyear=testyear,n=len(oe),reobserved=float(oyt.mean()),baseline_brier=brier_score_loss(oyt,np.full(len(oe),oy.mean())),logistic_brier=brier_score_loss(oyt,op),target='survey/key reobservation, not provider exit'))
p=pd.concat(preds,ignore_index=True);p.to_parquet(O/'exploratory_predictions.parquet',index=False)
delta=(p.p_boost-p.y)**2-(p.p_logistic-p.y)**2;group=p.assign(delta=delta).groupby('corridor').agg(total=('delta','sum'),n=('delta','size'));inds=rng.integers(0,len(group),(1999,len(group)));boot=group.total.to_numpy()[inds].sum(1)/group.n.to_numpy()[inds].sum(1)
pd.DataFrame(metrics).to_csv(O/'model_metrics.csv',index=False);pd.DataFrame(observ_metrics).to_csv(O/'reobservation_model.csv',index=False)
bins=pd.cut(p.p_boost,[0,.5,.7,.8,.9,1.00001],include_lowest=True);p.assign(bin=bins.astype(str)).groupby('bin').agg(n=('y','size'),observed=('y','mean'),predicted=('p_boost','mean')).to_csv(O/'boost_calibration.csv')
res=dict(evaluation='EXPLORATORY_BACKTEST; aggregate-inspected periods and unverified public dataset-release chronology',test_origins=len(p),corridors=int(p.corridor.nunique()),paired_boost_minus_logistic_brier=float(delta.mean()),corridor_bootstrap_interval=[float(np.quantile(boot,.025)),float(np.quantile(boot,.975))],operational_utility_demonstrated=False,independent_provider_time_validation=False,scope='Model predicts price among exactly reobserved core service quotes, not market exit or population welfare.')
save('runs/N2/model_result.json',res);record('N2','new_exploratory_models',[source],time.monotonic()-T,res);print('N2_MODEL',json.dumps(res),flush=True)
