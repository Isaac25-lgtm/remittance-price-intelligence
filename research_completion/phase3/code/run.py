"""Serial, logged Phase 3 command runner; does not write Phase 2 checkpoints."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'research_completion/phase3'

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def main():
    stage, *cmd = sys.argv[1:]
    if not cmd:
        raise SystemExit('usage: run.py STAGE COMMAND [ARGS]')
    private = OUT / 'private_runtime/logs'
    private.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update({k: '2' for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']})
    env.update(PYTHONHASHSEED='0', PYTHONUTF8='1', PYTHONPATH=str(ROOT/'src'), PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    code_paths = sorted((OUT/'code').glob('*.py'))
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in code_paths}
    record = dict(stage=stage, command=cmd, start_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                  code_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                  code_hashes=hashes, available_mb=round(psutil.virtual_memory().available/2**20,1))
    start=time.monotonic(); peak=0
    with (private/f'{stage}.log').open('w',encoding='utf-8') as log:
        proc=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
        while proc.poll() is None:
            try:
                parent=psutil.Process(proc.pid)
                peak=max(peak,sum(p.memory_info().rss for p in [parent]+parent.children(recursive=True) if p.is_running()))
            except (psutil.NoSuchProcess,psutil.AccessDenied): pass
            time.sleep(.5)
    record.update(exit_code=proc.returncode,seconds=round(time.monotonic()-start,2),peak_rss_mb=round(peak/2**20,1),
                  end_utc=dt.datetime.now(dt.timezone.utc).isoformat(),code_changed=any(digest(p)!=hashes[str(p.relative_to(ROOT))] for p in code_paths))
    (OUT/'reproducibility').mkdir(exist_ok=True)
    with (OUT/'reproducibility/commands.jsonl').open('a',encoding='utf-8') as stream: stream.write(json.dumps(record)+'\n')
    print(json.dumps(record,indent=2))
    print((private/f'{stage}.log').read_text(encoding='utf-8')[-3500:])
    return proc.returncode

if __name__=='__main__': raise SystemExit(main())
