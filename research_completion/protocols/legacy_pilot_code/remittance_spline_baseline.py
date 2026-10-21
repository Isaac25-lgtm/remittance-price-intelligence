from common import *
import pandas as pd,numpy as np,re
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder,SplineTransformer,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
T=time.monotonic();rng=np.random.default_rng(2026101704)
protocol('N2_SPLINE_BASELINE','Secondary exploratory stronger-simple-baseline challenge AFTER original gains inspected. Add an additive spline logistic model to test whether nonlinear univariate cost/fee/FX response explains boosting advantage. Fixed4knots,cubic degree3, logisticC1; no tuning, same categories, preprocessing trained within temporal train. Identical2022/2023/2024 origins/outcomes matched byorigin to frozen predictions, train target<testyearQ1. Paired Brier boost-minus-spline, corridor bootstrap1999; min useful probability improvement unspecified, monitoring proxy1pp criterion remains secondary. No claim to select model on untouched data. Stop unqualified advancedML advantage if spline matches/beats it.')
source=LAB/'discovery_round3/data/rpw_post2016.parquet';cols=['period','corridor','firm','firm_type','payment instrument','access point','pickup method','pickup location','cc1 lcu amount','cc1 total cost %','cc1 lcu fee','cc1 fx margin','transparent','speed actual','source_income','destination_income']
d=pd.read_parquet(source,columns=cols);d.columns=[re.sub('[^a-z0-9]+','_',x.lower()).strip('_') for x in d.columns];d['origin']=np.arange(len(d));d['year']=d.period.str.extract('(20[0-9]{2})')[0].astype(int);d['quarter']=d.period.str.extract('_([1-4])Q')[0].astype(int);d['t']=4*d.year+d.quarter
for k in ['cc1_lcu_amount','cc1_total_cost','cc1_lcu_fee','cc1_fx_margin']:d[k]=pd.to_numeric(d[k],errors='coerce')
d['cost']=d.cc1_total_cost;key=['corridor','firm','payment_instrument','access_point','pickup_method','pickup_location','cc1_lcu_amount']
for k in key:d[k]=d[k].fillna('UNSPECIFIED').astype(str).str.strip()
v=d[d.transparent.str.strip().str.lower().eq('yes')&d.cost.notna()&d.cost.ge(0)].copy();v=v[~v.duplicated(key+['t'],keep=False)].copy();v['next_t']=v.t+1
c=v.merge(v[key+['t','cost']].rename(columns={'t':'next_t','cost':'next_cost'}),on=key+['next_t'],how='inner',validate='many_to_one');c=c[c.cost.le(3)].copy()
num=['cost','cc1_lcu_fee','cc1_fx_margin'];cat=['quarter','firm_type','payment_instrument','access_point','pickup_method','speed_actual','source_income','destination_income']
for k in cat:c[k]=c[k].fillna('UNSPECIFIED').astype(str)
p=pd.read_parquet(ROOT/'runs/N2/exploratory_predictions.parquet');out=[]
for year in [2022,2023,2024]:
 tr=c[c.next_t.lt(year*4+1)];te=c[c.year.eq(year)];y=tr.next_cost.le(3).astype(int);yt=te.next_cost.le(3).astype(int)
 prep=ColumnTransformer([('n',make_pipeline(SimpleImputer(strategy='median'),SplineTransformer(n_knots=4,degree=3),StandardScaler()),num),('c',OneHotEncoder(handle_unknown='ignore',sparse_output=False),cat)])
 model=make_pipeline(prep,LogisticRegression(C=1,max_iter=600));model.fit(tr[num+cat],y);a=model.predict_proba(te[num+cat])[:,1]
 out.append(pd.DataFrame({'origin':te.origin,'year':year,'y_check':yt,'p_spline':a}))
q=p.merge(pd.concat(out),on=['origin','year'],how='inner',validate='one_to_one');assert len(q)==len(p) and q.y.eq(q.y_check).all()
q['delta']=(q.p_boost-q.y)**2-(q.p_spline-q.y)**2;g=q.groupby('corridor').agg(total=('delta','sum'),n=('delta','size'));ix=rng.integers(0,len(g),(1999,len(g)));b=g.total.to_numpy()[ix].sum(1)/g.n.to_numpy()[ix].sum(1)
metrics=[dict(year=int(year),n=len(g),spline_brier=float(((g.p_spline-g.y)**2).mean()),boost_brier=float(((g.p_boost-g.y)**2).mean()),delta=float(g.delta.mean())) for year,g in q.groupby('year')]
q.to_parquet(ROOT/'runs/N2/spline_matched_predictions.parquet',index=False)
res=dict(evaluation='SECONDARY_EXPLORATORY_STRONGER_BASELINE',n=len(q),spline_brier=float(((q.p_spline-q.y)**2).mean()),boost_brier=float(((q.p_boost-q.y)**2).mean()),boost_minus_spline=float(q.delta.mean()),corridor_interval=[float(np.quantile(b,.025)),float(np.quantile(b,.975))],year_metrics=metrics)
save('runs/N2/spline_results.json',res);record('N2','new_stronger_spline_logistic_challenge',[source],time.monotonic()-T,res);print(json.dumps(res),flush=True)
