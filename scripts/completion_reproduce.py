"""Execute corrected legacy reproduction, preserving every historical committed result."""
from pathlib import Path
import json
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research_completion/reproducibility'

def main():
    backup=ROOT/'research_completion/private_runtime/legacy_results'
    try:
        p=subprocess.run([sys.executable,'scripts/reproduce_from_cache.py'],cwd=ROOT)
        for name in ['reproduction_report.json','table_comparison.csv']:
            shutil.copy2(ROOT/'results/reproduction'/name,OUT/('local_'+name))
        report=json.loads((OUT/'local_reproduction_report.json').read_text(encoding='utf-8'))
        report['source_downloaded_in_completion_phase']=True
        (OUT/'local_reproduction_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        shutil.copy2(OUT/'local_table_comparison.csv',OUT/'source_to_results_comparison.csv')
        return p.returncode
    finally:
        for path in backup.rglob('*'):
            if path.is_file():shutil.copy2(path,ROOT/'results'/path.relative_to(backup))

if __name__=='__main__':raise SystemExit(main())
