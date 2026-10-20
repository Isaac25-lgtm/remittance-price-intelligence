"""Logged, thread-bounded local execution. Logs stay below research_completion/."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research_completion"


def run(command, stage, evidence_type="REAL-DATA EXECUTION"):
    def code_hashes():
        return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                for folder in ['src','scripts','configs'] for p in sorted((ROOT/folder).rglob('*'))
                if p.is_file() and p.suffix in {'.py','.yaml'} and '__pycache__' not in p.parts}
    before=code_hashes()
    env = dict(os.environ)
    env.update({k: "2" for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]})
    env.update(PYTHONHASHSEED="0", PYTHONUTF8="1", PYTHONPATH=str(ROOT / "src"), PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
    logs = OUT / "reproducibility"
    logs.mkdir(parents=True, exist_ok=True)
    private = OUT / "private_runtime" / "logs"
    private.mkdir(parents=True, exist_ok=True)
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    t0 = time.monotonic()
    with (private / f"{stage}.log").open("w", encoding="utf-8") as f:
        proc = subprocess.Popen(command, cwd=ROOT, env=env, stdout=f, stderr=subprocess.STDOUT)
        peak_rss = 0
        try:
            import psutil
            p = psutil.Process(proc.pid)
            while proc.poll() is None:
                try:
                    peak_rss = max(peak_rss, sum(x.memory_info().rss for x in [p] + p.children(recursive=True)))
                except psutil.Error:
                    pass
                time.sleep(1)
        except ImportError:
            proc.wait()
    record = dict(stage=stage, evidence_type=evidence_type, command=command, started_utc=started,
                  ended_utc=dt.datetime.now(dt.timezone.utc).isoformat(), exit_code=proc.returncode,
                  seconds=round(time.monotonic()-t0, 2), peak_rss_mb=round(peak_rss/2**20, 1),
                  code_sha=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip())
    after=code_hashes()
    record['code_files_changed_during_run']=[p for p in set(before)|set(after) if before.get(p)!=after.get(p)]
    record['code_fingerprint_start']=hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest()
    record['code_fingerprint_end']=hashlib.sha256(json.dumps(after,sort_keys=True).encode()).hexdigest()
    with (logs / "commands_executed.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    progress_path = logs / "progress.json"
    progress = json.loads(progress_path.read_text(encoding="utf-8")) if progress_path.exists() else {}
    progress.setdefault("stages", {})[stage] = record
    progress["last_stage"] = stage
    progress_path.write_text(json.dumps(progress, indent=2), encoding="utf-8")
    print(json.dumps(record, indent=2), flush=True)
    print((private / f"{stage}.log").read_text(encoding="utf-8", errors="replace")[-2400:], flush=True)
    return proc.returncode


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True)
    ap.add_argument("--type", default="REAL-DATA EXECUTION")
    ap.add_argument("command", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = a.command[1:] if a.command[:1] == ["--"] else a.command
    sys.exit(run(cmd, a.stage, a.type))
