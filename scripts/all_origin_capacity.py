"""Correct monitoring denominator: score all eligible origins, retain unknown outcomes.

The E1-trained score is extrapolated as a ranking scenario, not a joint availability
probability. Unknown selected/unselected failures yield explicit recall bounds.
"""
from pathlib import Path
import pickle
import pandas as pd
import numpy as np
from completion_models import calibrated

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_completion';PRIVATE=OUT/'private_runtime/processed'

def main():
    X=pd.read_parquet(PRIVATE/'features_core.parquet');X=X[X.target_year.isin([2022,2023,2024,2025])].copy()
    choice=pd.read_csv(OUT/'models/annual_selection.csv').set_index('year').chosen_model
    frames=[]
    for year,d in X.groupby('target_year'):
        d=d.copy()
        with (OUT/'private_runtime/fit_models'/f'{choice.loc[year]}_{year}.pkl').open('rb') as f:m,method,cal=pickle.load(f)
        d['S_selected_risk']=1-calibrated(m.predict_proba(d)[:,1],method,cal)
        with (OUT/'private_runtime/fit_models'/f'L2_spline_logistic_{year}.pkl').open('rb') as f:m,_,_=pickle.load(f)
        d['spline_risk']=1-m.predict_proba(d)[:,1]
        d['history_risk']=1-d.h_corrfirm;d['cost_risk']=d.cost
        frames.append(d)
    P=pd.concat(frames,ignore_index=True);rows=[]
    known=P.primary.astype(bool).to_numpy();fail=known&~P.y.astype(bool).to_numpy();unknown=~known
    total_fail=int(fail.sum())
    for rule,col in [('S_selected','S_selected_risk'),('L2_spline_logistic','spline_risk'),('B2_history','history_risk'),('R_highest_cost_rule','cost_risk')]:
        for cap in [.05,.1,.2,.3]:
            selected=np.zeros(len(P),bool)
            for _,part in P.groupby('qidx'):
                k=int(np.floor(cap*len(part)))
                ranked=part.assign(_tie=part.source_row).sort_values([col,'_tie'],ascending=[False,True]).head(k)
                selected[ranked.index]=True
            cf=int((selected&fail).sum());ur=int((selected&unknown).sum());unr=int((~selected&unknown).sum());reviews=int(selected.sum())
            rows.append(dict(rule=rule,capacity=cap,n_all_eligible=len(P),n_known_valid=int(known.sum()),n_unknown=int(unknown.sum()),reviewed=reviews,known_failures_total=total_fail,known_failures_captured=cf,unknown_reviewed=ur,known_stays_reviewed=reviews-cf-ur,recall_of_known_failures=cf/total_fail,all_failure_recall_lower=cf/(total_fail+unr),all_failure_recall_upper=(cf+ur)/(total_fail+ur),interpretation='all-origin budget; E1 score extrapolation scenario; unknown states not assumed failures or exits'))
    result=pd.DataFrame(rows);result.to_csv(OUT/'models/all_origin_capacity_bounds.csv',index=False)
    print(result[result.capacity==.2].to_string(index=False))

if __name__=='__main__':main()
