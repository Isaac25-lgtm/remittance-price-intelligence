"""Serial, resumable heavier stages. Never starts two memory-intensive jobs together."""
import json
from pathlib import Path
import sys
from completion_run import run

ROOT=Path(__file__).resolve().parents[1]
STAGES=[
 ('nested_model_selection',['scripts/completion_models.py','nested']),
 ('recent_history_reference',['scripts/completion_recent.py']),
 ('transfer_and_fitted_sensitivities',['scripts/completion_models.py','transfer']),
 ('observation_and_mar_scenario',['scripts/completion_models.py','observation']),
 ('continuous_price_secondary',['scripts/completion_models.py','continuous']),
 ('paired_dependence_and_capacity',['scripts/completion_inference.py']),
 ('associative_explainability',['scripts/completion_inference.py','explain']),
]

if __name__=='__main__':
    for stage,args in STAGES:
        p=ROOT/'research_completion/reproducibility/progress.json'
        status=json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
        if status.get('stages',{}).get(stage,{}).get('exit_code')==0:
            print('CHECKPOINT already completed:',stage,flush=True);continue
        code=run([sys.executable]+args,stage)
        if code:raise SystemExit(code)
