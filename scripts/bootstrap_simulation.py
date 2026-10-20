"""Synthetic inference stress test, explicitly not RPW evidence or formal coverage proof."""
from pathlib import Path
import numpy as np
import pandas as pd
from rpi.completion_stats import dependence_ci

def main():
    rng=np.random.default_rng(20261020)
    # Sparse crossed provider/corridor cells with 13 shared AR(1) quarter shocks.
    cells=np.argwhere(rng.uniform(size=(20,20))<.3)
    rows=[(c,p,q) for c,p in cells for q in range(13)]
    frame=pd.DataFrame(rows,columns=['corridor_key','firm__n','qidx'])
    kinds=['corridor','provider','time_block_4','crossed_corridor_provider'];records=[]
    for sim in range(50):
        c=rng.normal(0,.002,20);p=rng.normal(0,.003,20);t=np.empty(13);t[0]=rng.normal(0,.004)
        for q in range(1,13):t[q]=.6*t[q-1]+rng.normal(0,.004*np.sqrt(1-.6**2))
        true=-.003
        d=true+c[frame.corridor_key]+p[frame['firm__n']]+t[frame.qidx]+rng.normal(0,.02,len(frame))
        for kind in kinds:
            ci=dependence_ci(d,frame,kind,reps=200,seed=20261020+sim)
            records.append(dict(simulation=sim,method=kind,covered=bool(ci[0,0]<=true<=ci[1,0]),width=ci[1,0]-ci[0,0]))
    result=pd.DataFrame(records).groupby('method').agg(n_simulations=('covered','size'),empirical_coverage=('covered','mean'),mean_width=('width','mean')).reset_index()
    result['evidence_type']='SYNTHETIC UNIT TEST; not observed RPW data';result['bootstrap_reps']=200;result['dgp']='20x20 sparse crossed groups;13 AR(0.6) quarters;fixed loss-gap mean -0.003'
    path=Path(__file__).resolve().parents[1]/'research_completion/validation/bootstrap_simulation.csv'
    result.to_csv(path,index=False);print(result.to_string(index=False))

if __name__=='__main__':main()
