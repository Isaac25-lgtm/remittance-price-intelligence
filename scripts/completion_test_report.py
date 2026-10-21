"""Summarise actual JUnit results; never infer a scientific pass from software tests."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_completion'

def main():
    root=ET.parse(OUT/'private_runtime/final_pytest.xml').getroot();suites=root.findall('testsuite')
    total=sum(int(s.get('tests',0)) for s in suites);skipped=sum(int(s.get('skipped',0)) for s in suites)
    failures=sum(int(s.get('failures',0))+int(s.get('errors',0)) for s in suites)
    stage=json.loads((OUT/'reproducibility/progress.json').read_text(encoding='utf-8'))['stages']['final_full_tests']
    rows=[]
    for case in root.iter('testcase'):
        rows.append(dict(module=case.get('classname'),status='FAIL' if case.find('failure') is not None or case.find('error') is not None else 'SKIP' if case.find('skipped') is not None else 'PASS'))
    summary=pd.DataFrame(rows).groupby(['module','status']).size().rename('count').reset_index()
    summary.to_csv(OUT/'reproducibility/test_summary.csv',index=False)
    text=f'''# Actual software / integrity test report

Evidence type: SYNTHETIC UNIT TEST AND PUBLIC AGGREGATE INTEGRITY / STREAMLIT APPTEST.
Full local suite: **{total-failures-skipped} passed, {skipped} skipped, {failures} failures/errors**. Executed {stage['started_utc']} to {stage['ended_utc']}; exit {stage['exit_code']}; peak logged RSS {stage['peak_rss_mb']} MB. Python3.12 / Streamlit1.66 / Altair6.3. Exact command and fingerprints: commands_executed.jsonl. The original source/cohort real-data reproduction is separate.

The one pre-package skip is the ZIP open/hash test, which runs after assembly and in the packaging CI. A dateutil utcfromtimestamp deprecation warning is unrelated to scientific results. The full suite exercises every dashboard section/control and aggregate download, source/quarter/identity/leakage guards, fold transformers with unseen covariates/outcome columns, calibration limits, bootstrap structures, decomposition and file safety. Tests do not rerun large model fits or download raw data.

Initial baseline dependency failures, one bootstrap test correction, the strict legacy numeric comparison failure, final fee-column reporting failure and all-NaN ablation histogram failure remain in the command history. Corrected/resumed stages passed; model checkpoints were preserved. Strict legacy numerical reproduction itself remains failed (14 exact /2 timing-only /14 different); software test success does not erase that scientific limitation.

Additional final supplement tests and ZIP verification are logged separately after this full run. GitHub Python3.11 CI outcome is recorded in deliverables/git_and_download_links.md. The hosted browser inventory was empty and web reader failed, so deployed new pages were not verified. No assertion of public redeployment follows from local tests or a commit.

Scientific interpretation: all pre-existing periods were inspected, public predictor release clocks are not verified, novelty/true identity remain unresolved, and joint inference undercovered the stress simulation. **NOT YET PUBLICATION-READY.**
'''
    for folder in ['reproducibility','validation']:(OUT/folder/'test_report.md').write_text(text,encoding='utf-8')
    print(f'{total-failures-skipped} passed; {skipped} skipped; {failures} failed/error in actual local full suite')
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
