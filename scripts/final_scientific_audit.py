"""Read-only second-pass audit of requirements, claims, immutable legacy files and package safety."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import pandas as pd

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_completion'
REQUIRED={
 'P0':['audits/initial_repo_inventory.json'],
 'P1':['literature/closest_work_matrix.csv','literature/search_log.csv','literature/head_to_head_scientific_delta.md','literature/references.bib'],
 'P2':['data/source_manifest.json','data/release_availability_registry.csv','data/historical_publication_timing.md'],
 'P3':['data/inclusion_exclusion_flow.csv','data/identity_collision_audit.csv','models/mnar_sensitivity.csv','models/ipw_mar_scenario.csv','audits/independent_raw_audit.json'],
 'P4':['protocols/phase2_frozen_protocol.md','validation/feature_asof_registry.csv','validation/leakage_audit.md','validation/split_registry.csv'],
 'P5':['models/model_registry.json','models/model_comparison.csv','models/calibration.csv','models/annual_selection.csv'],
 'P6':['models/paired_dependence.csv','models/transfer_sensitivity_metrics.csv','models/decision_capacity.csv','models/subgroups.csv','models/permutation_importance.csv'],
 'P7':['validation/holdout_status.md'],
 'P8':['assessment/publication_gates.csv','assessment/claim_evidence_ledger.csv','assessment/PUBLICATION_VERDICT.md','manuscript/conditional_research_report.md'],
 'P9':['figures/figure_inventory.csv','manuscript/figure_legends.md','manuscript/table_legends.md','reproducibility/test_report.md'],
}

def audit():
    checks=[]
    def check(name,ok,detail=''):
        checks.append(dict(check=name,status='PASS' if bool(ok) else 'FAIL',detail=detail))
    inv=json.loads((OUT/'audits/initial_repo_inventory.json').read_text(encoding='utf-8'))
    for rel,digest in inv['tracked_sha256'].items():
        if rel.startswith('results/') or rel=='configs/experiment.yaml':
            check('legacy_immutable:'+rel,hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest)
    for phase,names in REQUIRED.items():
        for name in names:check('requirement:'+phase+':'+name,(OUT/name).is_file() and (OUT/name).stat().st_size>0)
    flow=pd.read_csv(OUT/'data/inclusion_exclusion_flow.csv').groupby('state')['count'].sum()
    b=pd.read_csv(OUT/'tables/supplementary_overall_bounds.csv').iloc[0]
    check('flow_denominator',int(flow.sum()-flow['right_censored_last_quarter'])==int(b.n_eligible))
    check('outcome_denominator',int(flow.observed_stay+flow.observed_fail)==int(b.n_stay+b.n_fail))
    check('unknown_denominator',int(b.n_stay+b.n_fail+b.n_unknown)==int(b.n_eligible))
    check('bounds_order',0<=b.lower_bound<=b.conditional_p_stay_core<=b.upper_bound<=1)
    raw=json.loads((OUT/'audits/independent_raw_audit.json').read_text(encoding='utf-8'))
    check('separate_implementation',raw['status']=='PASS' and not raw['mismatches'])
    m=pd.read_csv(OUT/'models/model_comparison.csv');check('same_outer_rows',m.n.nunique()==1 and int(m.n.iloc[0])==19667)
    check('probability_metrics_valid',m.brier.between(0,1).all() and (m.log_loss>=0).all())
    splits=pd.read_csv(OUT/'validation/split_registry.csv')
    for year,d in splits.groupby('year'):
        x=d.set_index('role');check('chronology:'+str(year),str(x.loc['base_refit','target_end'])<str(x.loc['calibration','target_start'])<str(x.loc['selection','target_start'])<str(x.loc['outer_test','target_start']))
    cap=pd.read_csv(OUT/'models/decision_capacity.csv')
    check('within_quarter_capacity',cap.groupby(['analysis','capacity']).reviewed.nunique().eq(1).all())
    check('capacity_counts',(cap.failures_captured<=cap.failures_total).all() and (cap.false_alerts+cap.failures_captured==cap.reviewed).all())
    sg=pd.read_csv(OUT/'models/subgroups.csv');u=sg[sg.group=='Uganda']
    check('uganda_gate',(~u.supported).all() and u.brier.isna().all())
    report=(OUT/'manuscript/conditional_research_report.md').read_text(encoding='utf-8')
    verdict=(OUT/'assessment/PUBLICATION_VERDICT.md').read_text(encoding='utf-8')
    check('no_forced_go','CONDITIONAL_MORE_EVIDENCE' in verdict and 'NOT YET PUBLICATION-READY' in verdict and not (OUT/'manuscript/candidate_article.md').exists())
    check('headline_conditional_rate',f'{b.conditional_p_stay_core:.4f}' in report and f'{b.conditional_p_stay_core:.6f}' in verdict)
    check('headline_bounds',f'{b.lower_bound:.4f}' in report and f'{b.upper_bound:.4f}' in report)
    selected=m[m.model=='S_selected'].iloc[0]
    check('headline_selected_brier',f'{selected.brier:.6f}' in report and f'{selected.brier:.6f}' in verdict)
    claims=pd.read_csv(OUT/'assessment/claim_evidence_ledger.csv')
    for r in claims.to_dict('records'):check('claim_source:'+r['claim_id'],(OUT/r['source_file_or_paper']).is_file())
    check('forecast_claim_rejected',claims.set_index('claim_id').loc['C5','pass_fail_unresolved']=='FAIL')
    gates=pd.read_csv(OUT/'assessment/publication_gates.csv')
    check('all_twelve_gates',set(gates.gate)=={f'G{i}' for i in range(1,13)})
    check('novelty_unresolved',gates.set_index('gate').loc['G8','status']=='UNRESOLVED')
    check('all_science_statuses',gates.status.isin(['PASS','FAIL','UNRESOLVED']).all())
    for name in ['assessment/PUBLICATION_VERDICT.md','manuscript/conditional_research_report.md','README.md']:
        p=OUT/name
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if '://' not in link:check('link:'+name+':'+link,(p.parent/link.split('#')[0]).exists())
    fig=pd.read_csv(OUT/'figures/figure_inventory.csv')
    for n in fig.figure:
        for ext in ['png','svg']:check('figure:'+n+'.'+ext,(OUT/'figures'/f'{n}.{ext}').stat().st_size>1000)
    check('figure_count',len(fig)>=12)
    # Public CSV exports reviewed independently from model code.
    forbidden={'source_row','source_row_next','id','firm','firm__n','key','provider','cost_next','y'}
    for p in OUT.rglob('*.csv'):
        if 'private_runtime' in p.parts:continue
        check('no_quote_columns:'+str(p.relative_to(OUT)),not (set(pd.read_csv(p,nrows=0).columns)&forbidden))
    source=json.loads((OUT/'data/source_manifest.json').read_text(encoding='utf-8'))
    check('source_hash',source['sha256']=='f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8' and source['bytes']==50780339)
    result=pd.DataFrame(checks);result.to_csv(OUT/'audits/final_independent_audit.csv',index=False)
    failed=result[result.status=='FAIL']
    text='# Final independent implementation and scientific-claims audit\n\nThis is a separate second-pass programmatic/claims audit, not external human peer review.\n\n'
    text+=f'{len(result)} checks; {len(failed)} failed. Scientific gates are not converted into an acceptance probability.\n\n'
    text+='Every master-directive phase is mapped to real artifacts in this audit; blocked scientific evidence remains explicitly unresolved in publication_gates.csv.\n\n'
    text+='Major challenges:unverified row-level release clocks; no untouched temporal confirmation; unresolved full-text competitor and true bundle identity; only13 independent target waves; strict cross-platform numerical mismatch. A conditional report is the appropriate deliverable.\n\n'
    if len(failed):text+=failed.to_string(index=False)
    else:text+='All artifact/cohort/claim consistency checks pass; this does not turn unresolved scientific gates into PASS.'
    (OUT/'audits/final_independent_audit.md').write_text(text+'\n',encoding='utf-8')
    print(f'Audit:{len(result)} checks;{len(failed)} failures')
    if len(failed):print(failed.to_string(index=False))
    return bool(len(failed))

if __name__=='__main__':raise SystemExit(audit())
