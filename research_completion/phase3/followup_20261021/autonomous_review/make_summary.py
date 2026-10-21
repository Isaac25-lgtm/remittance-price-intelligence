"""Aggregate evidence-acquisition metadata and plot existing descriptive outputs."""
from collections import Counter
import csv
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PRIVATE=ROOT/'research_completion/phase3/private_runtime/followup_20261021/autonomous_review'


def source_summary():
    # Imports the freeze verifier only; never opens raw outcomes or the key.
    sys.path.insert(0,str(HERE))
    import review
    review.verify_freeze()
    source=json.loads((PRIVATE/'source_manifest.json').read_text(encoding='utf8'))
    originals=[r for r in source if not r['source_id'].startswith('b')]
    readers=[r for r in source if r['source_id'].startswith('b')]
    rows=[]
    for status,n in sorted(Counter(r['access_status'] for r in originals).items()):
        rows.append(dict(denominator='56_DISCOVERED_SOURCE_URLS',category=status,count=n,
            interpretation='ACCESS_RESULT_NOT_DOCUMENT_PERTINENCE_OR_HISTORICAL_VALIDITY'))
    rows.append(dict(denominator='56_DISCOVERED_SOURCE_URLS',category='ADDITIONAL_USABLE_READER_TEXT',count=len(readers),
        interpretation='SUBSET_OF_FAILED_ORIGINAL_DOWNLOADS; TEXT_HASH_NOT_ORIGINAL_DOCUMENT_HASH'))
    grades=json.loads((HERE/'freeze_integrity_summary.json').read_text())['grade_counts']
    for grade in 'ABCD':
        rows.append(dict(denominator='60_STRATIFIED_CASES',category='GRADE_'+grade,count=grades.get(grade,0),
                        interpretation='DOCUMENTATION_FEASIBILITY_NOT_IDENTITY_ACCURACY'))
    rows.extend([dict(denominator='DISCOVERY_PROCESS',category=k,count=n,interpretation=meaning) for k,n,meaning in [
        ('QUERY_BATCHES',18,'FOUR_QUERIES_PER_LOGGED_BATCH'),('DISCOVERY_QUERIES',72,'SHARED_PROVIDER_SEARCHES_NOT_60_INDEPENDENT_SEARCHES'),
        ('UNIQUE_PROVIDER_LABELS_INVESTIGATED',39,'ALIASES_AND_AFFILIATES_NOT_SILENTLY_MERGED'),('CASE_SOURCE_LEDGER_ROWS',185,'SHARED_DOCUMENTS_REUSED'),
        ('ARCHIVE_API_PROBE',1,'HTTP429; REQUESTS_STOPPED; NOT_EVIDENCE_OF_ABSENCE'),
        ('UNRESOLVED_CASES',60,'NO_DOCUMENTARY_SAME_OR_DIFFERENT_STATUS_SUPPORTED'),('HUMAN_ADJUDICATIONS',0,'SOFTWARE_AUDIT_IS_NOT_HUMAN_VALIDATION')]])
    with (HERE/'SOURCE_SCOPE_SUMMARY.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def figures():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import pandas as pd
    out=HERE/'figures';out.mkdir(exist_ok=True)
    d=pd.read_csv(HERE/'PAIRED_GROUP_DECOMPOSITION.csv')
    order=['before_target_2021Q2','transition_target_2021Q2','between_classification_transitions','transition_target_2022Q4','after_target_2022Q4']
    x=d[d.group_field=='source_era'].set_index('group').loc[order]
    labels=['Before Q2 2021 target','Transition into Q2 2021','Between transitions','Transition into Q4 2022','After Q4 2022 target']
    fig,ax=plt.subplots(figsize=(9,4.8),layout='constrained')
    ax.barh(labels[::-1],(100*x.width_difference).to_numpy()[::-1],color='#315d88')
    for i,(_,row) in enumerate(x.iloc[::-1].iterrows()):
        ax.text(100*row.width_difference+.3,i,f'{100*row.width_difference:.2f} pp  ({int(row.newly_unknown):,}/{int(row.n_eligible):,})',va='center',fontsize=9)
    ax.set_xlim(0,31);ax.set_xlabel('Extra unknown share / identification-bound width (percentage points)')
    ax.set_title('Strict identity excludes core-valid links throughout source eras',loc='left',fontsize=13)
    ax.spines[['top','right']].set_visible(False)
    fig.text(.01,-.04,'Eligible cheap USD200 origins; full periods retained. Source-era alignment is descriptive, not causal.',fontsize=9)
    for ext in ['png','pdf']:fig.savefig(out/('source_era_width.'+ext),dpi=180,bbox_inches='tight')
    plt.close(fig)
    fig,ax=plt.subplots(figsize=(7.4,4.1),layout='constrained')
    ax.bar(['A: full both-period\nbundle','B: near-period\npartial','C: context\nonly','D: no pertinent\naccessible support'],[0,2,47,11],color=['#27715b','#5b809c','#9aa9b4','#b8bdc3'])
    ax.set_ylim(0,60);ax.set_ylabel('Cases (deliberate stratified sample, n=60)')
    ax.set_title('No case establishes the historical full bundle in both quarters',loc='left',fontsize=12)
    for i,n in enumerate([0,2,47,11]):ax.text(i,n+1,str(n),ha='center')
    ax.spines[['top','right']].set_visible(False)
    fig.text(.01,-.04,'All 60 machine statuses unresolved. Grades measure documentation, not matching accuracy or human validation.',fontsize=8.5)
    for ext in ['png','pdf']:fig.savefig(out/('documentary_support.'+ext),dpi=180,bbox_inches='tight')
    plt.close(fig)


if __name__=='__main__':
    source_summary();figures()
