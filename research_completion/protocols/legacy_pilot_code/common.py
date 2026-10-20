"""Minimal safe I/O adapter for unchanged recovered pilot programs.

No prior common.py is executed. All source rows, diagnostics and predictions stay private.
These are reruns of archived exploratory protocols, not newly frozen hypotheses.
"""
from pathlib import Path
import hashlib
import json
import time
import datetime

ROOT=Path(__file__).resolve().parents[2]/'private_runtime/pilot_reproduction'
LAB=ROOT/'lab'

def save(name,value):
    p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,indent=2),encoding='utf-8')

def protocol(name,text):
    p=ROOT/'rerun_protocol_calls';p.mkdir(parents=True,exist_ok=True)
    (p/(name+'.md')).write_text('Archived protocol rerun; not a new prespecification.\n\n'+text,encoding='utf-8')

def record(project,stage,sources,seconds,result):
    p=ROOT/'execution.jsonl';p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a',encoding='utf-8') as f:f.write(json.dumps(dict(project=project,stage=stage,seconds=seconds,executed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),result=result))+'\n')
