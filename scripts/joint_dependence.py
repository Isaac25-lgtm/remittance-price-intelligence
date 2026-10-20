"""One amended exploratory joint crossed-group/time-block sensitivity; fixed predictions."""
from pathlib import Path
import numpy as np
import pandas as pd
from rpi.completion_stats import dependence_ci

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_completion';PRIVATE=OUT/'private_runtime/processed'

def main():
    rows=[]
    for analysis,path in [('legacy',ROOT/'data/processed/test_predictions_lag0.parquet'),('phase2',PRIVATE/'phase2_predictions.parquet')]:
        p=pd.read_parquet(path);y=p.y.astype(float).to_numpy()
        pairs=[('M1_hist_gbm','L2_spline_logistic'),('M2_random_forest','L2_spline_logistic')]
        if analysis=='phase2':pairs += [('S_selected','L2_spline_logistic'),('S_selected','B2_history')]
        d=np.column_stack([(p[a].to_numpy()-y)**2-(p[b].to_numpy()-y)**2 for a,b in pairs])
        kind='crossed_corridor_provider_time_block';ci=dependence_ci(d,p,kind,reps=1000)
        for j,(a,b) in enumerate(pairs):rows.append(dict(analysis=analysis,model_a=a,model_b=b,resampling=kind,brier_diff=d[:,j].mean(),ci95_lo=ci[0,j],ci95_hi=ci[1,j],n_quarters=p.qidx.nunique(),status='AMENDED_EXPLORATORY; limited-period coverage not guaranteed'))
    result=pd.DataFrame(rows);result.to_csv(OUT/'models/joint_dependence_sensitivity.csv',index=False)
    print(result.to_string(index=False))

if __name__=='__main__':main()
