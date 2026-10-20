"""Final bounded source/major-group refits and descriptive shift diagnostics."""
import gc
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from rpi import features as F
from rpi.preprocess import load_clean
from rpi.evaluate import metric_row
from completion_models import fixed_annual,metrics
from completion_data import linked_variant,write

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_completion';PRIVATE=OUT/'private_runtime/processed'

def main():
    lk=pd.read_parquet(PRIVATE/'linked_core.parquet');X=pd.read_parquet(PRIVATE/'features_core.parquet')
    dev=X[X.primary & (X.target_year<2022)]
    frames=[];registry=[]
    for label,field in [('provider','firm__n'),('corridor','corridor_key')]:
        largest=dev.groupby(field).size().idxmax();scenario='exclude_largest_development_'+label
        cache=PRIVATE/(scenario+'.parquet')
        if cache.exists():P=pd.read_parquet(cache)
        else:
            # Keep current cross-section; exclude this group's outcomes from every history and fit.
            a=F.build(lk,history_allowed=lk[field]!=largest);a=a[a[field]!=largest]
            P,reg=fixed_annual(a,scenario);registry+=reg;P.to_parquet(cache,index=False);del a;gc.collect()
        frames.append(metrics(P,['B2_history','L2_spline_logistic','M1_hist_gbm','M2_random_forest'],scenario))
    df=load_clean()
    for scenario in ['transparent_only','no_negative_fx','date_quarter']:
        cache=PRIVATE/('fitted_'+scenario+'.parquet')
        if cache.exists():P=pd.read_parquet(cache)
        else:
            a=F.build(linked_variant(df,scenario));P,reg=fixed_annual(a,scenario);registry+=reg;P.to_parquet(cache,index=False);del a;gc.collect()
        frames.append(metrics(P,['B2_history','L2_spline_logistic','M1_hist_gbm','M2_random_forest'],scenario))
    write(pd.concat(frames,ignore_index=True),'models/final_stress_metrics.csv')
    (OUT/'models/final_stress_registry.json').write_text(json.dumps(registry,indent=2),encoding='utf-8')
    P=pd.read_parquet(PRIVATE/'phase2_predictions.parquet');P=P.merge(X[['source_row','n_firm_hist','lag_available']],on='source_row',suffixes=('','_source'),validate='one_to_one')
    rows=[]
    # Fixed support bands; do not tune cutpoints on performance. Prior own quote is an overlap proxy.
    masks={'prior_own_quote':P.lag_available==1,'no_prior_own_quote':P.lag_available==0,
           'provider_history_0_to_99':P.n_firm_hist<100,'provider_history_100_plus':P.n_firm_hist>=100}
    for group,mask in masks.items():
        d=P[mask];fail=int((1-d.y.astype(int)).sum());supported=fail>=100 and d.corridor_key.nunique()>=5
        for name in ['B2_history','L2_spline_logistic','M1_hist_gbm','M2_random_forest','S_selected']:
            row=dict(group=group,model=name,n=len(d),failures=fail,n_corridors=d.corridor_key.nunique(),supported=supported)
            if supported:row.update(metric_row(d.y.astype(int),d[name]))
            else:row['status']='NOT_ESTIMABLE_SUPPORT_GATE'
            rows.append(row)
    write(pd.DataFrame(rows),'models/history_overlap_support.csv')
    # Distribution tests are descriptive; IID p-values are invalid under this panel dependence.
    before=df[df.qidx<2022*4+2];after=df[df.qidx>=2022*4+2];shifts=[]
    for col in ['cc1 total cost %','cc1 fee %','cc1 fx margin']:
        a=before[col].dropna();b=after[col].dropna()
        shifts.append(dict(variable=col,n_before=len(a),n_after=len(b),median_before=a.median(),median_after=b.median(),ks_statistic=ks_2samp(a,b).statistic,p_value_status='NOT_REPORTED_IID_INVALID',interpretation='survey composition and time change; no causal design-change attribution'))
    write(pd.DataFrame(shifts),'data/pre_post2022_distribution_shift.csv')
    composition=[]
    for period,d in [('before_2022Q3',before),('2022Q3_onward',after)]:
        for col in ['destination_region','access point__n','firm_type__n']:
            for group,n in d.groupby(col).size().items():
                if n>=30:composition.append(dict(period=period,field=col,group=group,n=n,share=n/len(d)))
    write(pd.DataFrame(composition),'data/pre_post2022_composition.csv')
    print('Final bounded refits, history support and descriptive shift diagnostics completed',flush=True)

if __name__=='__main__':main()
