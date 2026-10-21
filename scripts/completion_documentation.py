"""Dossier navigation and execution metadata; no analytic refits."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import pandas as pd

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_completion'

def put(rel,text):
    (ROOT/rel).write_text(text.strip()+'\n',encoding='utf-8')

def main():
    p=ROOT/'README.md';old=p.read_text(encoding='utf-8')
    marker='<!-- COMPLETION CURRENT END -->'
    if marker in old:old=old.split(marker,1)[1].lstrip()
    prefix='''# Remittance AI: affordable quote continuity

**Current decision: CONDITIONAL GO / CONDITIONAL_MORE_EVIDENCE — NOT YET PUBLICATION-READY.** Local investigation completed in October 2026; no operational model selected.

We study whether a surveyed remittance quote costing 0–3% remains affordable in the exactly next calendar quarter, and how service identity and missing successors change that measurement. The independently reacquired World Bank RPW workbook contains 204,469 quotes, 368 corridors and 699 normalised provider labels, 2016Q2–2025Q3; 2025Q2 is absent. Quotes are offers, not transactions or market exits.

- Conditional continuity: **81.11%** among 36,429 uniquely valid successor pairs; corridor interval 79.60%–82.56%.
- Among all 45,343 eligible origins, missing-outcome bounds are **65.16%–84.82%**. Strict identity widens them to **54.64%–87.22%**, despite a similar conditional point estimate.
- Chronological tuning/calibration/selection was executed. The selected research policy Brier is **0.130763** on 19,667 previously inspected outer records; raw spline is 0.136151 and history 0.138967. Raw RF/GBM score about 0.1281, but are not operationally promoted.
- Selected policy minus spline: **−0.005388**, amended joint corridor/provider/time interval **[−0.011730,+0.000457]**. Only 13 target waves; simulation coverage does not validate nominal 95%. Superiority remains uncertain.
- A corrected all-origin 20% review budget includes 4,889 unknown outcomes; policy recall bounds **21.67%–57.26%**. Conditional matched-sample gains do not establish monitoring benefit.
- Independent source/cohort audits pass. Strict numerical legacy reproduction has small logistic/spline mismatches; recovered pilot counts/GBM match, spline retains a residual. All negative results remain available.

Historical report captures do not establish quote-level public lead time. No untouched new temporal wave was found. The expanded 13-work literature assessment includes firm/service-level competitors; Lim 2026 full text remains inaccessible, so substantial novelty is unresolved. The original corridor-only/abstract-only description below is archived history, not the current literature verdict.

Start with the [scientific verdict](research_completion/assessment/PUBLICATION_VERDICT.md), [complete conditional report and outline](research_completion/manuscript/conditional_research_report.md), [figures](research_completion/figures/figure_inventory.csv), [tables](research_completion/manuscript/table_legends.md), [blockers](research_completion/assessment/REMAINING_BLOCKERS.md), [audit](research_completion/audits/final_independent_audit.md) and [one-file ZIP / Git state](research_completion/deliverables/git_and_download_links.md). A submission manuscript is not justified by the unresolved gates.

Reproduce using the [recorded environment and commands](research_completion/reproducibility/README.md); original experiments remain frozen under results/. Raw rows, private predictions, fitted models and copyrighted source PDFs are excluded from Git and the handoff. Public data attribution: The World Bank, Remittance Prices Worldwide, http://remittanceprices.worldbank.org (CC BY 4.0); no endorsement.

[Aggregate-only dashboard](https://isaac-remittance-research.streamlit.app/) includes a Publication completion section. Hosted redeployment is verified separately in the Git/download ledger; local tests are not proof of redeployment.

<!-- COMPLETION CURRENT END -->

'''
    p.write_text(prefix+'## Archived phase 1 report (17 October 2026)\n\n'+old.removeprefix('## Archived phase 1 report (17 October 2026)\n\n'),encoding='utf-8')
    note='''> Current local completion: **CONDITIONAL_MORE_EVIDENCE / NOT YET PUBLICATION-READY**. The analyses, pilot recovery, calibration, transfers and dependence sensitivities have been executed. See [the scientific verdict](../research_completion/assessment/PUBLICATION_VERDICT.md) and [conditional report](../research_completion/manuscript/conditional_research_report.md). The text below preserves the 17 October phase-1 history; references to future work or unavailable local inputs there are historical.

'''
    for name in ['docs/STATUS.md','docs/MODEL_CARD.md','docs/LIMITATIONS.md','docs/REPRODUCIBILITY.md','docs/PRIOR_ART.md','manuscript/README.md']:
        p=ROOT/name
        if p.exists() and not p.read_text(encoding='utf-8').startswith('> Current local completion:'):p.write_text(note+p.read_text(encoding='utf-8'),encoding='utf-8')
    for name in ['AGENTS.md','CLAUDE.md']:
        p=ROOT/name;s=p.read_text(encoding='utf-8')
        if 'Completion evidence is now available' not in s:
            p.write_text('Completion evidence is now available in research_completion/assessment/PUBLICATION_VERDICT.md and the conditional report. Read these and progress.json before resuming; do not refit completed checkpoints automatically. Decision remains conditional, with no operational model. Local calendar completion date:21 October2026 (Africa/Kampala).\n\n'+s,encoding='utf-8')
    fig=pd.read_csv(OUT/'figures/figure_inventory.csv')
    lines=['# Figure legends','', 'All figures use World Bank RPW aggregates, generated from the stated tables. PNG files are 300 dpi; SVG text remains editable. No source microdata are distributed.','']
    for r in fig.itertuples():lines += [f'## {r.title}',f'![{r.title}](../figures/{r.figure}.png)',f'Source: `{r.source}`. {r.note}','']
    put('research_completion/manuscript/figure_legends.md','\n'.join(lines))
    tables=[]
    for p in sorted((OUT/'tables').glob('*.csv')):
        if p.name=='table_inventory.csv':continue
        d=pd.read_csv(p);tables.append(dict(table=p.stem,rows=len(d),source=p.relative_to(OUT).as_posix(),units='See field names and canonical report; probabilities/percentage points/counts as labelled'))
    pd.DataFrame(tables).to_csv(OUT/'tables/table_inventory.csv',index=False)
    lines=['# Table legends and provenance','', 'Tables are deterministic exports of independently checked measurement or executed model aggregates. Legacy versus phase2 is explicit in analysis fields. All intervals are exploratory and conditional on fitted predictions; see the dependence methods and simulation caveats.','']
    for t in tables:lines += [f"- [{t['table']}](../tables/{t['table']}.md): {t['rows']} aggregate rows. {t['units']}."]
    lines += ['', 'Table 1: exclusive initially-cheap origin flow by assigned calendar quarter, 2016Q2–2025Q3; counts include final-wave right censoring. Table 2: all post-2016 source quote records by wave; costs are percent of the USD200 transfer, dates are collection dates, shares are survey-record proportions. Table 3: exact-next-quarter E1 conditional stay and E2 all-origin bounds; corridor intervals are nominal95%, not missing-data bounds. Table 4: annual2022–2025Q1 outer target periods and strictly earlier training/tuning/calibration/selection windows, row/event/group counts.', '', 'Table 5 reports absolute Brier/log-loss with resampling labels; paired differences are in models/paired_dependence.csv and joint_dependence_sensitivity.csv. Table 6 is the future-reobserved E1 benchmark at5/10/20/30% per-quarter budget; the corrected all-origin queue and unknown-state recall bounds are in models/all_origin_capacity_bounds.csv. Table 7 applies the100-failure/cluster support gates; true group transfer is separately in transfer_sensitivity_metrics.csv. Table 8 reports distinct scenario denominators, not paired causal effects. The final fitted source/dominance stresses are in models/final_stress_metrics.csv.', '', 'S1–S6 are mapped in supplementary_material.md. No individual-provider assessments or restricted rows are included.']
    put('research_completion/manuscript/table_legends.md','\n'.join(lines))
    stages=json.loads((OUT/'reproducibility/progress.json').read_text(encoding='utf-8'))['stages']
    manifest=dict(run_id='r01-local-completion-2026-10-20',generated_utc=dt.datetime.now(dt.timezone.utc).isoformat(),code_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),source_sha256='f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8',threads=2,peak_logged_rss_mb=max(x.get('peak_rss_mb',0) for x in stages.values()),stages=len(stages),status='CONDITIONAL_MORE_EVIDENCE',execution='LOCAL WINDOWS AUTHORISED',evidence_labels=['REAL-DATA EXECUTION','SYNTHETIC UNIT TEST','PUBLIC SOURCE INVESTIGATION','REUSED PRIOR OUTPUT'],limitations=['All old outcomes inspected; no untouched temporal confirmation','Strict legacy numerical comparison failed; immutable prior outputs preserved','Command logs record end-of-run commit and broad code fingerprints; unrelated files changed during some stages','One roughly seven-second overlap of exiting pilot driver and small joint-inference process; no concurrent memory-intensive fits'])
    for folder in ['reproducibility','validation']:(OUT/folder/'run_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    put('research_completion/reproducibility/README.md','''# Reproduction and checkpoints

Use Python 3.12 with environment_lock.txt / version_manifest.json; the dashboard CI uses Python 3.11. Commands below are run from the repository root. Windows uses .venv/Scripts/python.exe; other systems use their environment's python. Limit OMP_NUM_THREADS, OPENBLAS_NUM_THREADS, MKL_NUM_THREADS and NUMEXPR_NUM_THREADS to 2. Run one heavy stage at a time.

1. Install the locked analysis dependencies. Acquire the official public workbook privately with scripts/completion_fetch.py and expected SHA256 f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8 (source_manifest.json records URL/bytes).
2. Run scripts/completion_reproduce.py to execute the legacy comparator; it deliberately exits nonzero on retained scientific numerical differences and restores immutable results in finally. Do not interpret that exit as successful strict reproduction.
3. Run scripts/completion_data.py, then scripts/completion_pipeline.py (serial checkpointed models/inference). Completed checkpoints are skipped; nested code signatures prevent silently reusing changed-model checkpoints. Preserve/version incompatible caches rather than overwriting them. For the evidence ledgers, reacquire private reading copies with scripts/completion_sources.py beck2009.pdf borra2026.pdf rpw2025q3_catalogue.pdf archive_directory.json before scripts/completion_evidence.py; CDX responses can change, so compare acquisition hashes with the shipped capture ledger.
4. Run scripts/joint_dependence.py, scripts/completion_score_supplement.py, scripts/all_origin_capacity.py, scripts/completion_final_stress.py, scripts/completion_no_identity_history.py, scripts/completion_continuous_trend.py and scripts/completion_metric_references.py serially; see commands_executed.jsonl for exact historical ordering. Run scripts/recover_pilot.py --rebuild-original-encoding with the optional original cache path for comparison. Its legacy numerical environment is separately recorded in the pilot audit.
5. Run scripts/completion_report.py, scripts/completion_figures.py, scripts/completion_documentation.py, scripts/completion_requirements.py and pytest -q with JUnit output at research_completion/private_runtime/final_pytest.xml, then scripts/completion_test_report.py and scripts/final_scientific_audit.py. Review public files, run scripts/completion_public_review.py and inspect its explicit allowlist/schema inventory before scripts/build_publication_handoff.py. Run the packager's --audit on the resulting ZIP.

Raw rows, checkpoint parquet, fitted pickles and source literature PDFs are not shipped. The official workbook is publicly reacquirable; caches save interruption cost locally. Exact commands, evidence types, failures, timestamps, RSS and fingerprints are retained. This is not a claim of byte-identical numerical models across operating systems/dependency versions. Synthetic tests do not substitute for real-data execution. No new wave was fabricated.
''')
    print('Current documentation, figure/table legends and execution manifest updated')

if __name__=='__main__':main()
