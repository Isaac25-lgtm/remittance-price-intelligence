"""Paired wave sensitivities of the primary measurement and existing model losses."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t

ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'research_completion/phase3'

def hac_effect(wave,num,den,lag):
    n=wave[num].to_numpy(float);d=wave[den].to_numpy(float);T=len(n);theta=n.sum()/d.sum()
    influence=(n-theta*d)/d.mean()
    variance=float(influence@influence/T)
    for k in range(1,min(lag,T-1)+1):variance+=2*(1-k/(lag+1))*float(influence[k:]@influence[:-k]/T)
    se=np.sqrt(max(variance,0)/T);radius=t.ppf(.975,T-1)*se
    return dict(estimate=theta,sensitivity_lower=theta-radius,sensitivity_upper=theta+radius,se=se,hac_lag=lag,n_waves=T,status='EXPLORATORY_ASSUMPTION_DEPENDENT_NOT_ROBUST_95')

def main():
    wave=pd.read_csv(OUT/'tables/wave_measurement.csv')
    core=wave[wave.scenario=='cc1_3pct_core'];strict=wave[wave.scenario=='cc1_3pct_strict']
    paired=core.merge(strict,on='qidx',suffixes=('_core','_strict'),validate='one_to_one')
    assert (paired.n_core==paired.n_strict).all()
    paired['additional_unknown']=paired.u_strict-paired.u_core
    paired['lower_count_change']=paired.s_strict-paired.s_core
    paired['upper_count_change']=paired.s_strict+paired.u_strict-paired.s_core-paired.u_core
    rows=[]
    for name,num in [('strict_minus_core_width','additional_unknown'),('strict_minus_core_lower','lower_count_change'),('strict_minus_core_upper','upper_count_change')]:
        for lag in [0,1,4]:rows.append(dict(contrast=name,**hac_effect(paired,num,'n_core',lag)))
    pd.DataFrame(rows).to_csv(OUT/'inference/PAIRED_MEASUREMENT_EFFECTS.csv',index=False)
    paired[['qidx','quarter_core','n_core','conditional_core','conditional_strict','width_core','width_strict','additional_unknown']].to_csv(OUT/'tables/paired_wave_identity.csv',index=False)
    cols=['qidx','y','S_selected','L1_ridge_logistic','L1_ridge_logistic__cal','L2_spline_logistic','L2_spline_logistic__cal']
    preds=pd.read_parquet(ROOT/'research_completion/private_runtime/processed/phase2_predictions.parquet',columns=cols)
    modelrows=[]
    for reference in cols[3:]:
        delta=(preds.S_selected-preds.y.astype(int))**2-(preds[reference]-preds.y.astype(int))**2
        d=pd.DataFrame(dict(qidx=preds.qidx,delta=delta))
        grouped=d.groupby('qidx').agg(total=('delta','sum'),n=('delta','size')).reset_index()
        for lag in [0,1,4]:modelrows.append(dict(model_a='S_selected',model_b=reference,**hac_effect(grouped,'total','n',lag)))
    pd.DataFrame(modelrows).to_csv(OUT/'inference/MODEL_WAVE_HAC_SENSITIVITY.csv',index=False)
    old=ROOT/'research_completion/models/model_comparison.csv'
    pd.read_csv(old).to_csv(OUT/'inference/DEFINITIVE_MODEL_COMPARISONS.csv',index=False)
    inherited=['conventional_reference_comparisons.csv','joint_dependence_sensitivity.csv','performance_by_year.csv','all_origin_capacity_bounds.csv','decision_capacity.csv','recent_history_reference.csv','reobservation_models.csv','ipw_mar_scenario.csv','mnar_tipping_points.csv','weighting_sensitivity.csv']
    for name in inherited:
        # Exact copies of approved safe aggregates, labelled as inherited, no model refit.
        source=ROOT/'research_completion/models'/name
        (OUT/'tables'/('phase2_'+name)).write_bytes(source.read_bytes())
    print(json.dumps(dict(paired_measurement=rows,model_sensitivities=modelrows),indent=2))

if __name__=='__main__':main()
