"""Second-pass artifact/arithmetic/source-claim audit; not external scientific peer review."""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import pandas as pd
from literature import md

ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'research_completion/phase3'

def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    checks=[]
    def check(name,ok,detail):checks.append(dict(check=name,pass_check=bool(ok),detail=detail))
    s=pd.read_csv(OUT/'identity/LINKAGE_SCENARIO_RESULTS.csv').set_index('scenario')
    for basket in ['cc1','cc2']:
        for threshold in [3,5]:
            a=s.loc[f'{basket}_{threshold}pct_core'];b=s.loc[f'{basket}_{threshold}pct_strict']
            for rule,r in [('core',a),('strict',b)]:
                check(f'{basket}_{threshold}_{rule}_flow',r.n_eligible==r.n_stay+r.n_fail+r.n_unknown,'exact integer reconciliation')
                check(f'{basket}_{threshold}_{rule}_bounds',abs(r.lower-r.n_stay/r.n_eligible)<1e-14 and abs(r.upper-(r.n_stay+r.n_unknown)/r.n_eligible)<1e-14,'independent arithmetic from integer aggregates')
            check(f'{basket}_{threshold}_same_origins',a.n_eligible==b.n_eligible,'core/strict cohort identical')
            check(f'{basket}_{threshold}_monotone',b.lower<=a.lower and b.upper>=a.upper,'restriction increases unknown allocation')
    paired=pd.read_csv(OUT/'tables/paired_wave_identity.csv')
    check('paired_width_count',(paired.additional_unknown>=0).all() and paired.additional_unknown.sum()==5859,'same-origin paired unknown increment')
    check('origin_waves',len(paired)==36 and paired.conditional_core.notna().sum()==35,'source37 observed waves, not model13 or36 independent IID seasons')
    flow=pd.read_csv(OUT/'tables/unknown_flow.csv').set_index('state')['count']
    check('unknown_subtypes',sum(flow.drop(['stay','fail']))==8914,'unknowns partition without last-wave censoring')
    check('independent_count_comparison',pd.read_csv(OUT/'assessment/independent_count_comparison.csv').pass_check.all(),'all20 comparisons to unchanged Phase2')
    check('e3_rate',s.loc['cc1_3pct_core_E3','n_stay']==8189 and s.loc['cc1_3pct_core_E3','n_valid']==8879,'corridor survey denominator preserved; final censor separately excluded')
    strict=pd.read_csv(OUT/'reproducibility/STRICT_LEGACY_COMPARISON.csv')
    check('strict_failure_retained',(strict.status=='DIFFERS').sum()==14,'not disguised by rounding/tolerance widening')
    repeats=pd.read_csv(OUT/'reproducibility/RUN_COMPARISONS.csv')
    check('locked_repeatability',repeats.loc[repeats.comparison=='locked_real','exact_predictions'].all(),'selected2022 real ridge/spline, two separate processes')
    check('source_nonfinite_zero',json.loads((OUT/'identity/source_nonfinite_audit.json').read_text())['infinite_cost_cells']==0,'zero actual source result changes after finite-cost guard')
    review=json.loads((OUT/'identity/identity_audit.json').read_text())
    check('external_review_not_invented',review['external_adjudications']==0 and review['private_blinded_cases']==60,'human task pending')
    with (OUT/'identity/PRIVATE_REVIEW_TEMPLATE.csv').open(newline='',encoding='utf-8') as f: template=list(csv.reader(f))
    check('public_template_schema_only',len(template)==1,'explicit empty review schema, no source/provider cases')
    verdict=(OUT/'assessment/FINAL_SCIENTIFIC_VERDICT.md').read_text(encoding='utf-8')
    check('verdict_consistency','CONDITIONAL_HOLD' in verdict and 'NONE' in verdict,'no deployable model or submission readiness')
    check('no_fake_manuscript',not (OUT/'manuscript/manuscript_for_author_review.md').exists(),'conditional branch supplies a complete dossier instead')
    claims=pd.read_csv(OUT/'assessment/claim_evidence_ledger.csv')
    report=(OUT/'manuscript/conditional_research_dossier.md').read_text(encoding='utf-8')
    check('report_source_hash_literal','f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8' in report,'formatting must preserve exact provenance tokens')
    check('verdict_baseline_hash_literal','c0ef4fddbef78a47f9f274df78ab68d622da8d8e' in verdict,'baseline SHA must not be split by prose formatting')
    generation=json.loads((OUT/'reproducibility/LOCKED_RUN_MANIFEST.json').read_text())['source_commit']
    check('verdict_generation_commit_literal',generation in verdict,'exact generation SHA is preserved, not prose-spaced')
    for _,r in claims.iterrows():
        check('claim_'+r.claim_id,('['+r.claim_id+']') in report,'label present in canonical dossier')
        for name in r.evidence_artifact.split(';'):
            check('claim_source_'+r.claim_id+'_'+name,(OUT/name).exists(),'exact cited evidence path exists')
    baseline=json.loads((OUT/'reproducibility/BASELINE_INVENTORY.json').read_text())
    allowed={'README.md','AGENTS.md','CLAUDE.md','.gitignore','.github/workflows/ci.yml','docs/STATUS.md','research_completion/README.md','src/rpi/linkage.py'}
    changes=[]
    for item in baseline['files']:
        name=item['path'];p=ROOT/name
        if p.exists() and digest(p)!=item['sha256']:changes.append(name)
    check('baseline_preservation',set(changes)<=allowed,'intentional current pointers/CI/ignore/finite-cost source fix only: '+repr(changes))
    check('frozen_results_unchanged',not any(n.startswith(('results/','configs/','research_completion/')) and n!='research_completion/README.md' for n in changes),'Phase1/2 numerical/config/package artifacts preserved')
    spec=importlib.util.spec_from_file_location('safe_package',ROOT/'scripts/build_publication_handoff.py');package=importlib.util.module_from_spec(spec);spec.loader.exec_module(package)
    public=[]
    for p in sorted(OUT.rglob('*')):
        if not p.is_file() or set(p.parts)&package.FORBIDDEN_PARTS or p.suffix=='.zip':continue
        try:package.inspect_public_file(p);check('safe_'+str(p.relative_to(OUT)),True,'approved suffix/size/schema/credential scan')
        except ValueError as e:check('safe_'+str(p.relative_to(OUT)),False,str(e))
        public.append(p.relative_to(ROOT).as_posix())
    allow=OUT/'assessment/public_artifact_allowlist.json'
    public.append(allow.relative_to(ROOT).as_posix())
    allow.write_text(json.dumps(dict(paths=sorted(set(public)),review='aggregate schema and content/source boundary review; no private cases or PDFs'),indent=2),encoding='utf-8')
    for p in sorted((OUT/'figures').glob('*.png')):
        from PIL import Image
        with Image.open(p) as im:check('image_'+p.stem,min(im.size)>=1000 and im.info.get('dpi',(0,0))[0]>=299,'high-resolution source figure; visual QA separately recorded')
    # Requirement-by-requirement ledger, including conditional branches and explicit external blockers.
    text=(OUT/'MASTER_DIRECTIVE.md').read_text(encoding='utf-8');heading='initial';requirements=[]
    anchors={
      '3.':('literature/NOVELTY_DECISION.md','ASSESSED_NOVELTY_UNRESOLVED'),
      '4.':('reproducibility/ENVIRONMENT_MATRIX.md','EXECUTED_STRICT_FAILURE_RETAINED'),
      '5.':('identity/IDENTITY_VALIDITY.md','EXECUTED_EXTERNAL_IDENTITY_UNRESOLVED'),
      '6.':('timing/INFORMATION_SET_AUDIT.md','EXECUTED_NO_NEW_WAVE_OR_ASOF_CLOCK'),
      '7.':('inference/INFERENCE_ROBUSTNESS.md','EXECUTED_WITH_EXPLICIT_INFERENCE_LIMITS'),
      '8.':('assessment/SCIENTIFIC_AUDIT.md','EXECUTED_IMPLEMENTATION_INDEPENDENT_NOT_PEER_REVIEW'),
      '9.':('manuscript/conditional_research_dossier.md','CONDITIONAL_DOSSIER_BRANCH_EXECUTED'),
      '10.':('START_HERE_PHASE3.md','DELIVERABLES_AND_INTEGRATION_VERIFIED_SEPARATELY'),
      '11.':('EXECUTION_LEDGER.md','EXECUTED_WITH_EXTERNAL_STOP_RULES'),
    }
    for line_no,line in enumerate(text.splitlines(),1):
        if line.startswith('## '):heading=line[3:]
        if not (re.match(r'^\d+\.\s',line) or line.startswith('- ')):continue
        artifact,status='PROTOCOL.md','FOLLOWED_OR_EXPLICIT_SCOPE_NOTE'
        for prefix,(path,st) in anchors.items():
            if heading.startswith(prefix):artifact,status=path,st;break
        if 'If and only if' in heading or ('9.' in heading and any(x in line for x in ['Research title','Introduction:','Methods:','Results:','Discussion:','Declarations:','Accurate bibliography','Supplementary methods'])):status='NOT_APPLICABLE_NO_SCIENTIFIC_GO; CONDITIONAL_DOSSIER_SUPPLIED'
        if 'Lim' in line:status='LAWFUL_SEARCH_EXECUTED_FULLTEXT_BLOCKED'
        requirements.append(dict(requirement_id=f'DIRECTIVE-L{line_no}',heading=heading,requirement=line.lstrip('- '),disposition=status,evidence=artifact))
    pd.DataFrame(requirements).to_csv(OUT/'assessment/MASTER_REQUIREMENT_LEDGER.csv',index=False)
    md('assessment/SCIENTIFIC_AUDIT.md','''# Independent scientific audit and hostile-review assessment

This is a second implementation and second-pass claim/artifact audit, not an external human peer review. The raw-workbook parser does not import the primary linkage/model/report code. It rederives the prescribed recorded-key target, so agreement cannot validate the underlying economic identity assumption. Adversarial fixtures include missing calendar wave, changed identity/speed, duplicate origins/targets, nonfinite/negative target cost, separate baskets, strict availability boundary, unknown-state allocation, Brier direction, ratio-of-totals inference and asymmetric crossed groups. A deliberately introduced missing-wave bridge is detected by the scientific test oracle.

Every numbered/bulleted master requirement is indexed in MASTER_REQUIREMENT_LEDGER.csv with disposition and evidence, including conditional branches and unresolved external requirements. artifact_checks.csv contains machine checks, not a vote to pass substantive novelty/identity gates. The source and final package include exact fingerprints. Root exceptions preserve old scientific outputs and only change pointers, CI, safety ignore and the tested finite-cost boundary fix.

## Hostile reviewer grounds and actual disposition

1. **A service-row/ML application is not novel.** Resolved in wording only: those claims withdrawn. Exact RPW contribution still UNRESOLVED against blocked Lim full text and established selection theory.
2. **Recorded strings need not identify the same economic service.** UNRESOLVED_EXTERNAL. Sixty blinded cases and original-field/collision audits exist; zero ground-truth adjudications are claimed.
3. **A conditional81% result is presented as all-origin continuity.** RESOLVED_SCOPE: distinct E1/E2 denominators, exact bounds, no signed bias claim, no80% guarantee.
4. **Duplicate origins inflate a count of unique latent products.** RESOLVED_SCOPE: denominator explicitly quote records, ambiguous keys remain unknown; no latent-service count asserted.
5. **Missing is interpreted as provider exit.** RESOLVED_SCOPE: separate recorded states, no observed exit label or survival inference.
6. **Dominant providers or alternative weights reverse interpretation.** PARTLY_RESOLVED: deletion checks survive; equal-group means differ substantially and are reported, not suppressed or called population corrections.
7. **Corridor monitoring or SmaRT is incorrectly criticised.** RESOLVED_SCOPE: E3/SmaRT/same-record endpoints distinguished; old E3 right-censor display reconciled; no claim official statistics are wrong.
8. **Thousands of correlated quotes create spurious precision.** RESOLVED_SCOPE: finite-panel arithmetic separated from assumption-dependent wave-HAC; no validated robust95% claim. Broad temporal generalisation remains limited.
9. **ML superiority rests on failed coverage or favourable uncertainty selection.** NOT_ESTABLISHED: adverse joint interval and0.86 stress coverage retained; HAC does not promote a model.
10. **Conditional recheck evaluation uses future sample membership.** RESOLVED_SCOPE: all-origin capacity bounds retained; no efficacy/saving or unique policy ranking asserted.
11. **Linux reproduction mismatch is hidden as a passing run.** RESOLVED_TRANSPARENCY, not numeric identity: strict exit1 and14 differing tables retained; real Windows repeats exact; root platform cause unresolved. Solver probe adds adverse individual-probability sensitivity.
12. **Synthetic tests masquerade as independent outcomes or human validation.** RESOLVED_SCOPE: synthetic/observed distinction explicit; no new wave or human truth fabricated.
13. **An update date is presented as a new survey or positive lead time.** RESOLVED_SCOPE: identical source bytes and absent new waves recorded; operational TrackB rejected. Measurement TrackA judged separately.
14. **Author declarations or journal readiness are invented.** RESOLVED_SCOPE: conditional dossier and specific investigator checklist, no submission-ready paper or acceptance estimate. External scientific gates still prevent GO.

Final auditor judgement: CONDITIONAL_HOLD is consistent with evidence. The software/artifact checks can pass while originality, product comparability and operational predictive validity do not. No additional classifier experiment can settle the remaining external items. One bounded lawful overlap/identity review is rational; stop expansion if it establishes only routine incremental application or invalid identities.
''')
    # Resolve links only after this audit's own report has been materialised.
    for p in OUT.rglob('*.md'):
        if 'private_runtime' in p.parts:continue
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            target=link.split('#')[0]
            if not target or '://' in target:continue
            check('link_'+str(p.relative_to(OUT))+'_'+link,(p.parent/target).exists(),'relative link resolves')
    pd.DataFrame(checks).to_csv(OUT/'assessment/artifact_checks.csv',index=False)
    failed=[r for r in checks if not r['pass_check']]
    summary=dict(checks=len(checks),failed=len(failed),failures=failed,master_requirements=len(requirements),scientific_verdict='CONDITIONAL_HOLD',external_peer_review=False)
    (OUT/'assessment/audit_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2));return bool(failed)

if __name__=='__main__':raise SystemExit(main())
