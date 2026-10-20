from common import *
import pandas as pd,numpy as np,re
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder,OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import brier_score_loss
T=time.monotonic();rng=np.random.default_rng(2026101703)
protocol('N2_GROUP_HOLDOUT','Secondary exploratory frozen-hash corridor exclusion sensitivity AFTER temporal metrics inspected. Test2024 origins among corridors with SHA256(code) first8hex modulo5==0; remove these corridors from ALL training. Train only target quarters<2024Q1; same <=3% current-cost and exactly adjacent core-reobserved target. Same fixed logistic/HGB hyperparameters and preprocessing, no tuning. Prevalence/persistence/provider shrinkage20 references. Paired Brier and corridor bootstrap1999. Generalization sensitivity, NOT untouched independent confirmation. Stop promotion if no improvement vs best comparator. Quote-release chronology and conditional observation remain limitations.')
src=LAB/'discovery_round3/data/rpw_post2016.parquet'
cols=['period','corridor','firm','firm_type','payment instrument','access point','pickup method','pickup location','cc1 lcu amount','cc1 total cost %','cc1 lcu fee','cc1 fx margin','transparent','speed actual','source_income','destination_income']
d=pd.read_parquet(src,columns=cols);d.columns=[re.sub('[^a-z0-9]+','_',c.lower()).strip('_') for c in d.columns];d['year']=d.period.str.extract('(20[0-9]{2})')[0].astype(int);d['quarter']=d.period.str.extract('_([1-4])Q')[0].astype(int);d['t']=4*d.year+d.quarter;d['origin']=np.arange(len(d))
for c in ['cc1_lcu_amount','cc1_total_cost','cc1_lcu_fee','cc1_fx_margin']:d[c]=pd.to_numeric(d[c],errors='coerce')
d['cost']=d.cc1_total_cost;key=['corridor','firm','payment_instrument','access_point','pickup_method','pickup_location','cc1_lcu_amount']
for c in key:d[c]=d[c].fillna('UNSPECIFIED').astype(str).str.strip()
v=d[d.transparent.str.strip().str.lower().eq('yes')&d.cost.notna()&d.cost.ge(0)].copy();v=v[~v.duplicated(key+['t'],keep=False)];v['next_t']=v.t+1
p=v.merge(v[key+['t','cost']].rename(columns={'t':'next_t','cost':'next_cost'}),on=key+['next_t'],how='inner',validate='many_to_one');p=p[p.cost.le(3)].copy()
hold={c for c in p.corridor.unique() if int(hashlib.sha256(c.encode()).hexdigest()[:8],16)%5==0}
train=p[p.next_t.lt(2024*4+1)&~p.corridor.isin(hold)].copy();test=p[p.year.eq(2024)&p.corridor.isin(hold)].copy()
num=['cost','cc1_lcu_fee','cc1_fx_margin','quarter'];cat=['firm_type','payment_instrument','access_point','pickup_method','speed_actual','source_income','destination_income']
for frame in [train,test]:
 for c in num:frame[c]=pd.to_numeric(frame[c],errors='coerce').astype(float)
 for c in cat:frame[c]=frame[c].fillna('UNSPECIFIED').astype(str)
y=train.next_cost.le(3).astype(int);yt=test.next_cost.le(3).astype(int)
prep=ColumnTransformer([('n',make_pipeline(SimpleImputer(strategy='median'),StandardScaler()),num),('c',OneHotEncoder(handle_unknown='ignore',sparse_output=False),cat)])
logit=make_pipeline(prep,LogisticRegression(C=1,max_iter=400));logit.fit(train[num+cat],y)
enc=ColumnTransformer([('n',SimpleImputer(strategy='median'),num),('c',OrdinalEncoder(handle_unknown='use_encoded_value',unknown_value=-1),cat)])
xb=enc.fit_transform(train[num+cat]);xt=enc.transform(test[num+cat]);m=HistGradientBoostingClassifier(max_iter=60,max_leaf_nodes=7,min_samples_leaf=40,learning_rate=.07,random_state=20261017,categorical_features=list(range(4,11)));m.fit(xb,y)
prior=float(y.mean());tab=train.assign(y=y).groupby('firm').y.agg(['sum','count']);rates=(tab['sum']+20*prior)/(tab['count']+20)
pred={'persistence':np.ones(len(test)),'prevalence':np.full(len(test),prior),'provider_historical':test.firm.map(rates).fillna(prior).to_numpy(),'logistic':logit.predict_proba(test[num+cat])[:,1],'boost':m.predict_proba(xt)[:,1]}
scores={k:float(brier_score_loss(yt,a)) for k,a in pred.items()};z=pd.DataFrame({'origin':test.origin,'corridor':test.corridor,'y':yt,**pred});z.to_parquet(ROOT/'runs/N2/corridor_holdout_predictions.parquet',index=False)
delta=(z.boost-z.y)**2-(z.logistic-z.y)**2;g=z.assign(delta=delta).groupby('corridor').agg(total=('delta','sum'),n=('delta','size'));ix=rng.integers(0,len(g),(1999,len(g)));b=g.total.to_numpy()[ix].sum(1)/g.n.to_numpy()[ix].sum(1)
res=dict(evaluation='SECONDARY_EXPLORATORY_GROUP_TEMPORAL_SENSITIVITY',train_n=len(train),test_n=len(test),test_corridors=int(test.corridor.nunique()),train_test_corridor_overlap=len(set(train.corridor)&set(test.corridor)),brier=scores,boost_minus_logistic=float(delta.mean()),corridor_interval=[float(np.quantile(b,.025)),float(np.quantile(b,.975))],independent_confirmation=False)
save('runs/N2/corridor_holdout_results.json',res);record('N2','new_unseen_corridor_exploratory_sensitivity',[src],time.monotonic()-T,res);print(json.dumps(res),flush=True)
