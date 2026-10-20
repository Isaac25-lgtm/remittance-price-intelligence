"""Named conventional references, Brier skill and supported subgroup paired uncertainty."""
from pathlib import Path
import numpy as np
import pandas as pd
from rpi.completion_stats import dependence_ci
from completion_data import write

ROOT=Path(__file__).resolve().parents[1];PRIVATE=ROOT/'research_completion/private_runtime/processed'

def main():
    P=pd.read_parquet(PRIVATE/'phase2_predictions.parquet');y=P.y.astype(int).to_numpy()
    references=['L1_ridge_logistic','L1_ridge_logistic__cal','L2_spline_logistic','L2_spline_logistic__cal']
    candidates=['S_selected','M1_hist_gbm','M1_hist_gbm__cal','M2_random_forest','M2_random_forest__cal','B2_history']
    pairs=[(a,b) for a in candidates for b in references]
    losses={n:(P[n].to_numpy()-y)**2 for n in candidates+references}
    delta=np.column_stack([losses[a]-losses[b] for a,b in pairs]);rows=[]
    for kind in ['corridor','provider','time_block_4','crossed_corridor_provider','crossed_corridor_provider_time_block']:
        ci=dependence_ci(delta,P,kind)
        for j,(a,b) in enumerate(pairs):
            diff=float(delta[:,j].mean());reference=float(losses[b].mean())
            rows.append(dict(model=a,reference=b,n=len(P),brier_model=float(losses[a].mean()),brier_reference=reference,brier_diff=diff,brier_skill=1-float(losses[a].mean())/reference,relative_brier_diff=diff/reference,resampling=kind,ci95_lo=ci[0,j],ci95_hi=ci[1,j],status='RETROSPECTIVE_EXPLORATORY; fixed predictions; joint coverage unverified'))
    write(pd.DataFrame(rows),'models/conventional_reference_comparisons.csv')
    masks={'SSA':P.destination_region=='Sub-Saharan Africa','EAC':P.destination_code.isin(['BDI','COD','KEN','RWA','SOM','SSD','TZA','UGA']),'Uganda':P.destination_code=='UGA'}
    masks.update({f'income:{v}':P.destination_income==v for v in P.destination_income.unique()})
    masks.update({'no_provider_history':P.n_firm_hist==0,'provider_history_available':P.n_firm_hist>0,'no_corridor_history':P.n_corr_hist==0,'remote_initiation':P['access point__n'].isin(['internet','mobile phone']),'other_initiation':~P['access point__n'].isin(['internet','mobile phone'])})
    rows=[]
    for group,mask in masks.items():
        d=P[mask];fail=int((1-d.y.astype(int)).sum());nc=d.corridor_key.nunique()
        names=['S_selected','M1_hist_gbm','M2_random_forest'];ref='L1_ridge_logistic__cal'
        if fail<100 or nc<5:
            rows.append(dict(group=group,n=len(d),failures=fail,n_corridors=nc,status='NOT_ESTIMABLE_SUPPORT_GATE',reference=ref));continue
        yy=d.y.astype(int).to_numpy();delta=np.column_stack([(d[n].to_numpy()-yy)**2-(d[ref].to_numpy()-yy)**2 for n in names])
        for kind in ['corridor','provider','crossed_corridor_provider_time_block']:
            ci=dependence_ci(delta,d,kind)
            for j,n in enumerate(names):rows.append(dict(group=group,n=len(d),failures=fail,n_corridors=nc,model=n,reference=ref,brier_diff=delta[:,j].mean(),resampling=kind,ci95_lo=ci[0,j],ci95_hi=ci[1,j],n_quarters=d.qidx.nunique(),status='EXPLORATORY; conditional fixed predictions; joint coverage unverified'))
    write(pd.DataFrame(rows),'models/subgroup_paired_uncertainty.csv')
    print('Named conventional-reference skill and subgroup paired intervals completed')

if __name__=='__main__':main()
