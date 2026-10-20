"""Prespecified rolling history reference, without tuning or future outcomes."""
from pathlib import Path
import pandas as pd
import numpy as np
from rpi import features as F,linkage as L
from rpi.evaluate import metric_row,capture_at_capacity
from completion_data import write

ROOT=Path(__file__).resolve().parents[1];PRIVATE=ROOT/'research_completion/private_runtime/processed'

def main():
    lk=pd.read_parquet(PRIVATE/'linked_core.parquet')
    X=pd.read_parquet(PRIVATE/'features_core.parquet')
    events=lk[L.primary_outcome_rows(lk)].copy();events['y']=(events.cost_next<=3).astype(float)
    by=['corridor_key','firm__n']
    now=F._asof(events,by,'y',X,0,'r')
    earlier=F._asof(events,by,'y',X.assign(qidx=X.qidx-4),0,'r')
    count=now.r_n-earlier.r_n;success=now.r_sum-earlier.r_sum
    X['B4_recent_history']=(success+10*X.h_corr)/(count+10)
    P=pd.read_parquet(PRIVATE/'phase2_predictions.parquet')
    P=P.drop(columns=['B4_recent_history','lag_delta'],errors='ignore')
    P=P.merge(X[['source_row','B4_recent_history','lag_delta']],on='source_row',validate='one_to_one')
    P.to_parquet(PRIVATE/'phase2_predictions.parquet',index=False)
    rows=[dict(model='B4_recent_history',scope='pooled',**metric_row(P.y.astype(int),P.B4_recent_history))]
    write(pd.DataFrame(rows),'models/recent_history_reference.csv')
    capacity=[]
    for name,score in [('B4_recent_history',1-P.B4_recent_history),('R_positive_last_cost_change',P.lag_delta.fillna(0))]:
        for c in [.05,.1,.2,.3]:
            got,k,total=capture_at_capacity(P,score,P.y.astype(int),c)
            capacity.append(dict(rule=name,capacity=c,reviewed=k,failures_captured=got,failures_total=total,recall=got/total,precision=got/k))
    write(pd.DataFrame(capacity),'models/recent_change_capacity.csv')
    print('Recent history reference complete',flush=True)

if __name__=='__main__':main()
