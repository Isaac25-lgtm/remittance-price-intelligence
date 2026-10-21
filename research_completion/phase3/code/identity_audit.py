"""Original-to-canonical field, label turnover and blinded-form integrity audit."""
from collections import defaultdict
import json
from pathlib import Path
import numpy as np
import pandas as pd
import measurement as m

def main():
    records=m.load_source();rows=[];labelrows=[]
    names=m.FIELDS+['speed actual','receiving network coverage']
    for j,field in enumerate(names):
        groups=defaultdict(set);nonidempotent=0;separator=0;missing=0;byq=defaultdict(set)
        for r in records:
            raw=r[11][j];n=m.norm(raw);groups[n].add(raw)
            nonidempotent+=int(m.norm(n)!=n);separator+=int('|' in n);missing+=int(n=='');byq[r[0]].add(n)
        rows.append(dict(field=field,n_raw_distinct=len({v for values in groups.values() for v in values}),n_canonical_distinct=len(groups),n_canonical_multiple_raw=sum(len(v)>1 for v in groups.values()),missing_rows=missing,pipe_separator_rows=separator,non_idempotent_rows=nonidempotent))
        for q,labels in sorted(byq.items()):
            prior=byq.get(q-1)
            labelrows.append(dict(field=field,quarter=f'{q//4}Q{q%4+1}',n_labels=len(labels),n_labels_absent_previous_calendar_wave=len(labels-prior) if prior is not None else np.nan,previous_calendar_wave_present=prior is not None))
    m.write(rows,'identity/canonicalisation_audit.csv');m.write(labelrows,'identity/label_turnover_by_wave.csv')
    assert sum(x['non_idempotent_rows']+x['pipe_separator_rows'] for x in rows)==0
    d,e,c,review=m.construct(records)
    sizes=[]
    for label,g in [('all',d),*list(d.groupby('region'))]:
        group=g.groupby('provider_group').agg(n=('stay','size'),valid=('valid','sum'))
        sizes.append(dict(scope=label,n_origins=len(g),n_corridors=g.corridor_group.nunique(),n_provider_labels=len(group),provider_labels_with_valid_pairs=int((group.valid>0).sum()),corridors_with_valid_pairs=g.loc[g.valid==1,'corridor_group'].nunique()))
    m.write(sizes,'tables/independent_unit_support.csv')
    form=pd.read_csv(m.PRIVATE/'BLINDED_IDENTITY_REVIEW.csv',keep_default_na=False)
    key=pd.read_csv(m.PRIVATE/'IDENTITY_REVIEW_KEY.csv')
    assert len(form)==len(key)==60 and form.case_id.is_unique
    assert not any('cost' in name or name in ['state','stay','fail','stratum'] for name in form.columns)
    assert (form.human_identity_decision=='').all()
    assert form.filter(regex='alternative_.*source_row').astype(str).ne('').any().any()
    result=dict(external_adjudications=0,private_blinded_cases=len(form),stratum_key_separate=True,costs_and_automated_verdict_hidden=True,canonicalisation_idempotent=True,no_observed_separator_collision=True,implementation_audit_only=True)
    (m.OUT/'identity/identity_audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(result)

if __name__=='__main__':main()
