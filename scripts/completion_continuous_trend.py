"""Past-only shrunk provider/corridor cost-change reference, secondary endpoint."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error,mean_squared_error
from completion_data import write

ROOT=Path(__file__).resolve().parents[1]
PRIVATE=ROOT/'research_completion/private_runtime/processed'

def main():
    X=pd.read_parquet(PRIVATE/'features_core.parquet');X=X[X.primary].copy();X['change']=X.cost_next-X.cost
    rows=[]
    for year in [2022,2023,2024,2025]:
        test=X[X.target_year==year].copy();train=X[X.target_qidx<test.qidx.min()]
        global_change=train.change.mean();cg=train.groupby('corridor_key').change.agg(['sum','count'])
        corr=(cg['sum']+10*global_change)/(cg['count']+10)
        pg=train.groupby(['corridor_key','firm__n']).change.agg(['sum','count'])
        prior=pg.index.get_level_values(0).map(corr).to_numpy();pg['mean']=(pg['sum']+10*prior)/(pg['count']+10)
        own=pd.MultiIndex.from_frame(test[['corridor_key','firm__n']]).map(pg['mean']).to_numpy(dtype=float)
        fallback=test.corridor_key.map(corr).fillna(global_change).to_numpy()
        p=test.cost.to_numpy()+np.where(np.isfinite(own),own,fallback)
        rows.append(dict(year=year,model='shrunk_past_provider_corridor_cost_change',n=len(test),mae=mean_absolute_error(test.cost_next,p),rmse=float(np.sqrt(mean_squared_error(test.cost_next,p))),endpoint='continuous_next_cost_conditional_reobservation',scope='Annual past-only labels before first origin; shrink10; no within-year refit'))
    write(pd.DataFrame(rows),'models/continuous_group_trend.csv')
    print('Secondary continuous-cost group trend reference completed')

if __name__=='__main__':main()
