"""Stricter ablation removes both provider target history and own-quote lags."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from completion_models import fixed_annual,metrics
from completion_data import write

ROOT=Path(__file__).resolve().parents[1];PRIVATE=ROOT/'research_completion/private_runtime/processed'

def main():
    X=pd.read_parquet(PRIVATE/'features_core.parquet')
    X['h_firm']=X.h_global;X['h_corrfirm']=X.h_corr;X['n_firm_hist']=0.
    X['lag_cost']=np.nan;X['lag_delta']=np.nan;X['lag_available']=0.
    P,registry=fixed_annual(X,'no_provider_target_or_own_history')
    P.to_parquet(PRIVATE/'no_provider_target_or_own_history.parquet',index=False)
    write(metrics(P,['B2_history','L2_spline_logistic','M1_hist_gbm','M2_random_forest'],'no_provider_target_or_own_history'),'models/no_identity_history_metrics.csv')
    (ROOT/'research_completion/models/no_identity_history_registry.json').write_text(json.dumps(registry,indent=2),encoding='utf-8')

if __name__=='__main__':main()
