"""Adversarial scientific tests; fixtures are synthetic, never claimed real quotes."""
import importlib.util
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import pytest

HERE=Path(__file__).parent
sys.path.insert(0,str(HERE))
import measurement as audit
from inference import hac_effect
from rpi.completion_stats import resample_weights
from rpi.preprocess import norm_text

def quote(q=100,cost=2,speed='fast',provider='synthetic firm',corridor='AAA>BBB',row=1):
    original=(provider,'cash','agent','cash','nationwide',speed,'wide')
    return (q,(corridor,*[audit.norm(v) for v in original[:5]]),speed,'wide',cost,cost,200.,500.,'synthetic region','synthetic provider type',row,original)

def frame(records,strict=False):
    # Non-cheap sentinel separates follow-up existence from final-quarter censoring.
    d,_,_,_=audit.construct(records+[quote(q=104,cost=8,provider='sentinel',row=999)],strict=strict)
    return d[d.qidx==100]

def test_missing_calendar_wave_is_not_next_observation():
    d=frame([quote(),quote(q=102,row=2)])
    assert d.iloc[0].state=='corridor_not_surveyed' and d.iloc[0].valid==0

def test_identity_drift_is_unknown_and_not_exit():
    d=frame([quote(),quote(q=101,provider='synthetic renamed firm',row=2)])
    assert d.iloc[0].state=='service_not_observed' and d.iloc[0].unknown==1

@pytest.mark.parametrize('where',['origin','target'])
def test_duplicate_key_never_promoted(where):
    r=[quote(),quote(q=101,row=2)];r.append(quote(q=100 if where=='origin' else 101,row=3))
    d=frame(r)
    assert set(d.state)=={where+'_key_ambiguous'} and d.valid.sum()==0

@pytest.mark.parametrize('bad',[float('nan'),-1,float('inf')])
def test_invalid_target_remains_unknown(bad):
    d=frame([quote(),quote(q=101,cost=bad,row=2)])
    assert d.iloc[0].state=='invalid_target_cost' and d.iloc[0].unknown==1

@pytest.mark.parametrize('bad',[float('nan'),-1,float('inf')])
def test_primary_pipeline_invalid_target_matches_independent(bad):
    from rpi.linkage import primary_outcome_rows,bounds_table
    d=pd.DataFrame(dict(cost=[2.],cost_next=[bad],status=['core_reobserved'],core_reobserved=[True],strict_reobserved=[True]))
    assert not primary_outcome_rows(d).iloc[0]
    b=bounds_table(d).iloc[0]
    assert b.n_unknown==1 and b.n_fail==0 and b.n_stay==0

def test_speed_change_widens_bounds_on_same_origin():
    records=[quote(),quote(q=101,speed='slow',row=2)]
    a=frame(records);b=frame(records,True)
    assert len(a)==len(b)==1 and a.valid.sum()==1 and b.unknown.sum()==1
    assert audit.estimate(a,'a')['conditional']==1
    assert audit.estimate(b,'b')['lower']==0 and audit.estimate(b,'b')['upper']==1

def test_two_transfer_baskets_are_different():
    r=list(quote(q=101,row=2));r[6]=500.
    d=frame([quote(),tuple(r)])
    assert d.iloc[0].state=='service_not_observed'

@pytest.mark.parametrize('value',[None,'  Cash ,  AGENT ','ＫＥＮＹＡ','Synthetic|Provider','nan'])
def test_canonicalisation_roundtrip(value):
    assert audit.norm(audit.norm(value))==audit.norm(value)==norm_text(value)

def test_future_availability_boundary_is_strict():
    from datetime import datetime,timezone
    available=datetime(2026,1,2,tzinfo=timezone.utc);decision=available;target=available
    assert not (available<=decision<target)
    # Same-day collection is not a positive lead-time decision, even when available then.

def test_brier_direction_and_unknown_not_zero_failure():
    y=np.array([1,0]);good=np.array([.9,.1]);bad=1-good
    assert np.mean((good-y)**2)<np.mean((bad-y)**2)
    d=frame([quote(),quote(q=101,cost=float('nan'),row=2)])
    r=audit.estimate(d,'unknown');assert r['n_fail']==0 and r['n_unknown']==1

def test_asymmetric_crossed_groups_are_not_aliased():
    c=np.array(['a','a','a','b','b']);p=np.array(['x','y','z','x','z']);q=np.array([1,1,2,2,3])
    wc=resample_weights(c,p,q,'corridor',np.random.default_rng(8));wp=resample_weights(c,p,q,'provider',np.random.default_rng(8))
    assert np.array_equal(wc[:3],np.repeat(wc[0],3))
    assert wp[0]==wp[3] and wp[2]==wp[4] and not np.array_equal(wc,wp)

def test_hac_constant_influence_has_zero_variance():
    d=pd.DataFrame({'a':[2,4,6,8],'n':[4,8,12,16]})
    r=hac_effect(d,'a','n',1)
    assert r['estimate']==.5 and r['se']==0

def test_hac_is_ratio_of_totals_not_mean_of_ratios():
    d=pd.DataFrame({'a':[1,0,0],'n':[1,2,7]})
    assert hac_effect(d,'a','n',1)['estimate']==.1

def test_gap_mutation_is_detected(monkeypatch):
    original=audit.construct
    def bad_bridge(records,*args,**kwargs):
        altered=[]
        for r in records:
            t=list(r)
            if t[0]==102:t[0]=101
            altered.append(tuple(t))
        return original(altered,*args,**kwargs)
    monkeypatch.setattr(audit,'construct',bad_bridge)
    with pytest.raises(AssertionError):test_missing_calendar_wave_is_not_next_observation()

def test_public_measurement_counts_exact_and_identity_monotonic():
    p=HERE.parent/'identity/LINKAGE_SCENARIO_RESULTS.csv'
    d=pd.read_csv(p).set_index('scenario')
    for basket in ['cc1','cc2']:
        for threshold in [3,5]:
            a=d.loc[f'{basket}_{threshold}pct_core'];b=d.loc[f'{basket}_{threshold}pct_strict']
            assert a.n_eligible==a.n_stay+a.n_fail+a.n_unknown==b.n_eligible
            assert b.n_valid<=a.n_valid and b.lower<=a.lower and b.upper>=a.upper
    assert d.loc['cc1_3pct_core','n_eligible']==45343

def test_strict_comparator_failures_not_relabelled_pass():
    d=pd.read_csv(HERE.parent/'reproducibility/STRICT_LEGACY_COMPARISON.csv')
    assert len(d)==30 and (d.status=='DIFFERS').sum()==14

def test_independent_parser_does_not_import_primary_pipeline():
    import ast
    tree=ast.parse((HERE/'measurement.py').read_text(encoding='utf-8'))
    imported=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
    assert not any(x and (x.startswith('rpi') or 'report' in x or 'models' in x) for x in imported)

def load_packager():
    spec=importlib.util.spec_from_file_location('phase3_packager',HERE/'package.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def test_archive_rejects_parent_traversal(tmp_path):
    import zipfile
    p=tmp_path/'unsafe.zip'
    with zipfile.ZipFile(p,'w') as z:
        z.writestr('START_HERE_PHASE3.md','safe synthetic entry')
        z.writestr('../escape.csv','x\n1\n')
    with pytest.raises(AssertionError):load_packager().audit(p)

def test_archive_rejects_provider_rows(tmp_path):
    import zipfile
    p=tmp_path/'unsafe.zip'
    with zipfile.ZipFile(p,'w') as z:
        z.writestr('START_HERE_PHASE3.md','safe synthetic entry')
        z.writestr('cases.csv','source_row,firm,cost_next\n1,synthetic,2\n')
    with pytest.raises(AssertionError):load_packager().audit(p)

def test_actual_phase3_zip_integrity():
    paths=list((HERE.parent/'deliverables').glob('REMITTANCE_R01_PHASE3_*.zip'))
    if not paths:pytest.skip('Phase3 science checkpoint precedes immutable ZIP build')
    for p in paths:assert load_packager().audit(p)['status']=='PASS'

def test_report_provenance_tokens_survive_spacing():
    from literature import prose_spacing
    tokens=['c0ef4fddbef78a47f9f274df78ab68d622da8d8e',audit.EXPECTED,'2026-10-21T03:34:40.828257+00:00','https://example.org/phase3/file2.csv','2025Q3','1e-9']
    result=prose_spacing(' '.join(tokens)+' Phase3 has14 tables,2 timing-only matches.')
    assert all(token in result for token in tokens)
    assert 'Phase 3 has 14 tables, 2 timing-only' in result
