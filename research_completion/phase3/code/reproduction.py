"""Bounded deterministic fixture/selected-fold audit; original comparator stays strict."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import sys
import numpy as np
import pandas as pd
import scipy
import sklearn
from threadpoolctl import threadpool_info
from rpi.models import ridge_logistic,spline_logistic
from rpi.features import NUMERIC,CATEGORICAL

ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'research_completion/phase3'
PRIVATE=OUT/'private_runtime/reproduction'

def arrayhash(a):
    return hashlib.sha256(np.asarray(a,dtype='<f8').tobytes()).hexdigest()

def framehash(frame):
    # pandas hashing may change across versions; file SHA is the cross-environment input anchor.
    return hashlib.sha256(pd.util.hash_pandas_object(frame,index=True).to_numpy().tobytes()).hexdigest()

def main(label,fixture=False,tight=False):
    PRIVATE.mkdir(parents=True,exist_ok=True);(OUT/'reproducibility').mkdir(exist_ok=True)
    rows=[]
    if fixture:
        rng=np.random.default_rng(20261021);n=360
        X=pd.DataFrame({col:rng.normal(size=n) for col in NUMERIC})
        for col in CATEGORICAL:X[col]=np.where(np.arange(n)%3==0,'cash','online')
        X.loc[X.index%7==0,'lag_cost']=np.nan
        y=(rng.uniform(size=n)<1/(1+np.exp(-X.cost))).astype(int)
        train=X.iloc[:280];test=X.iloc[280:];yt=y[:280];ys=y[280:]
    else:
        path=ROOT/'research_completion/private_runtime/processed/features_core.parquet'
        cols=list(dict.fromkeys(NUMERIC+CATEGORICAL+['source_row','qidx','target_qidx','target_year','primary','y']))
        X=pd.read_parquet(path,columns=cols);prim=X[X.primary].copy();del X
        test=prim[prim.target_year==2022].copy();first=int(test.qidx.min());train=prim[prim.target_qidx<first].copy()
        assert int(train.target_qidx.max())<first
        yt=train.y.astype(int).to_numpy();ys=test.y.astype(int).to_numpy()
        # Existing independent legacy regeneration is only a comparison reference.
        old=pd.read_parquet(ROOT/'data/processed/test_predictions_lag0.parquet')
        old=old[old.target_year==2022].set_index('source_row').loc[test.source_row]
    for name,maker in [('ridge',ridge_logistic),('spline',spline_logistic)]:
        model=maker()
        if tight:model.set_params(clf__tol=1e-10,clf__max_iter=10000)
        model.fit(train,yt);p=model.predict_proba(test)[:,1]
        z=model.named_steps['pre'].transform(train)
        ztest=model.named_steps['pre'].transform(test)
        row=dict(run=label,scope='synthetic_fixture' if fixture else 'real_2022_legacy_fold',model=name,n_train=len(train),n_test=len(test),
                 train_input_hash=framehash(train),test_input_hash=framehash(test),train_y_hash=arrayhash(yt),
                 transformed_train_hash=arrayhash(z),transformed_test_hash=arrayhash(ztest),prediction_hash=arrayhash(p),
                 brier=float(np.mean((p-ys)**2)),solver=model.named_steps['clf'].solver,tol=model.named_steps['clf'].tol,
                 n_iter=int(model.named_steps['clf'].n_iter_.max()),transformed_columns=z.shape[1])
        clf=model.named_steps['clf'];trainp=model.predict_proba(train)[:,1]
        grad=z.T@(trainp-yt)/len(yt)+clf.coef_[0]/(clf.C*len(yt))
        row['max_abs_objective_gradient']=float(max(abs(grad).max(),abs((trainp-yt).mean())))
        if not fixture:
            col='L1_ridge_logistic' if name=='ridge' else 'L2_spline_logistic'
            row['max_prediction_difference_phase2_legacy_rerun']=float(np.abs(p-old[col].to_numpy()).max())
        np.save(PRIVATE/f'{label}_{name}.npy',p)
        rows.append(row)
    env=dict(python=platform.python_version(),platform=platform.platform(),processor=platform.processor(),numpy=np.__version__,pandas=pd.__version__,scipy=scipy.__version__,sklearn=sklearn.__version__,executable=sys.executable,thread_settings={k:os.environ.get(k) for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','PYTHONHASHSEED']},threadpools=threadpool_info())
    (OUT/f'reproducibility/{label}.json').write_text(json.dumps(dict(environment=env,results=rows),indent=2),encoding='utf-8')
    print(json.dumps(dict(environment=env,results=rows),indent=2))

def compare():
    spec=importlib.util.spec_from_file_location('strict_compare',ROOT/'scripts/reproduce_from_cache.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    comps=module.compare_all();pd.DataFrame(comps).to_csv(OUT/'reproducibility/STRICT_LEGACY_COMPARISON.csv',index=False)
    fields=[];causes=[]
    for row in comps:
        name=row['file'];p=ROOT/'data/processed/frozen_tables_snapshot'/name;q=ROOT/'data/processed/repro_outputs'/name
        if name.endswith('.csv'):
            a=pd.read_csv(p);b=pd.read_csv(q)
            for col in a.columns:
                if pd.api.types.is_numeric_dtype(a[col]) and pd.api.types.is_numeric_dtype(b[col]):
                    aa=a[col].to_numpy(float);bb=b[col].to_numpy(float)
                    bad=~np.isclose(aa,bb,atol=1e-9,rtol=1e-9,equal_nan=True)
                    if bad.any():fields.append(dict(file=name,field=col,n_different=int(bad.sum()),max_abs_diff=float(np.nanmax(np.abs(aa-bb))),category='volatile_runtime' if col=='fit_seconds' else 'numeric_or_rank_propagation'))
        status=row['status']
        if status=='MATCH':category='source_cohort_linkage_exact';evidence='Strict original comparator; no divergent source/count field.'
        elif status=='MATCH_EXCEPT_TIMING':category='volatile_runtime';evidence='Only fit_seconds differs; not a scientific difference.'
        elif name.startswith('run_meta'):category='python_platform_metadata';evidence='Python3.13.16 Linux vs3.12.10 Windows; not silently ignored.'
        else:category='numeric_solver_and_derived_rank';evidence='Logistic/spline-associated probability differences propagate into diagnostics, rank ties and resampling. Platform/BLAS causality not isolated; no source/cohort difference demonstrated.'
        causes.append(dict(file=name,strict_status=status,category=category,source_cohort='EXACT_COUNTS',feature_input='current selected-fold fingerprints only; no Linux row fingerprints',fold_order='current fixed input verified; historical Linux order unproven',seed_threads='same declared seed20261017 and2 threads; BLAS differences unisolated',calibration='legacy diagnostics preserved; phase2 corrected offset bracket is separate',evidence=evidence,cause_status='UNRESOLVED_ROOT_NUMERIC_CAUSE' if status=='DIFFERS' and not name.startswith('run_meta') else 'EXPLAINED'))
    pd.DataFrame(fields).to_csv(OUT/'reproducibility/LEGACY_FIELD_DIFFERENCES.csv',index=False)
    pd.DataFrame(causes).to_csv(OUT/'reproducibility/LEGACY_DIFFERENCE_CAUSES.csv',index=False)
    runs=[]
    for prefix in ['locked_real','locked_fixture','base_fixture']:
        for model in ['ridge','spline']:
            a=OUT/f'reproducibility/{prefix}_1.json';b=OUT/f'reproducibility/{prefix}_2.json'
            if not (a.exists() and b.exists()):continue
            ra=next(r for r in json.loads(a.read_text())['results'] if r['model']==model);rb=next(r for r in json.loads(b.read_text())['results'] if r['model']==model)
            pa=np.load(PRIVATE/f'{prefix}_1_{model}.npy');pb=np.load(PRIVATE/f'{prefix}_2_{model}.npy')
            runs.append(dict(comparison=prefix,model=model,n=ra['n_test'],same_input=ra['train_input_hash']==rb['train_input_hash'],same_transformed_input=ra['transformed_train_hash']==rb['transformed_train_hash'],exact_predictions=np.array_equal(pa,pb),max_abs_probability_difference=float(abs(pa-pb).max()),brier_difference=ra['brier']-rb['brier'],strict_atol=0,strict_rtol=0))
    a=OUT/'reproducibility/locked_fixture_1.json';b=OUT/'reproducibility/base_fixture_1.json'
    if a.exists() and b.exists():
        for model in ['ridge','spline']:
            pa=np.load(PRIVATE/f'locked_fixture_1_{model}.npy');pb=np.load(PRIVATE/f'base_fixture_1_{model}.npy')
            runs.append(dict(comparison='cross_dependency_fixture_only',model=model,n=len(pa),exact_predictions=np.array_equal(pa,pb),max_abs_probability_difference=float(abs(pa-pb).max()),brier_difference=math_brier(a,model)-math_brier(b,model),strict_atol=1e-9,strict_rtol=1e-9))
    ci1=OUT/'reproducibility/ci_fixture_1.json';ci2=OUT/'reproducibility/ci_fixture_2.json'
    if ci1.exists() and ci2.exists():
        aa=json.loads(ci1.read_text())['results'];bb=json.loads(ci2.read_text())['results']
        ww=json.loads((OUT/'reproducibility/locked_fixture_1.json').read_text())['results']
        for model in ['ridge','spline']:
            a=next(x for x in aa if x['model']==model);b=next(x for x in bb if x['model']==model);w=next(x for x in ww if x['model']==model)
            for label,ref in [('ci_linux_repeat',b),('windows_vs_ci_linux_fixture',w)]:
                exact=a['prediction_hash']==ref['prediction_hash']
                runs.append(dict(comparison=label,model=model,n=a['n_test'],same_input=a['train_input_hash']==ref['train_input_hash'],same_transformed_input=a['transformed_train_hash']==ref['transformed_train_hash'],exact_predictions=exact,max_abs_probability_difference=0 if exact else np.nan,brier_difference=a['brier']-ref['brier'],strict_atol=0,strict_rtol=0))
    pd.DataFrame(runs).to_csv(OUT/'reproducibility/RUN_COMPARISONS.csv',index=False)
    print(json.dumps(dict(strict_counts=CounterLike(comps),repeated_fits=runs),indent=2))
    return module.comparison_exit_code(comps)

def CounterLike(rows):
    return {s:sum(r['status']==s for r in rows) for s in sorted({r['status'] for r in rows})}

def math_brier(path,model):return next(r['brier'] for r in json.loads(path.read_text())['results'] if r['model']==model)

if __name__=='__main__':
    if sys.argv[1]=='compare':raise SystemExit(compare())
    else:main(sys.argv[1],fixture='--fixture' in sys.argv,tight='--tight' in sys.argv)
