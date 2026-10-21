"""Single-attempt, TLS-verified source acquisition; immutable bytes and public manifest."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def fetch(url, dest, expected=None):
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    result = dict(url=url, accessed_utc=dt.datetime.now(dt.timezone.utc).isoformat(), destination=str(dest.relative_to(ROOT)))
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "R01-academic-research/0.2"})
        with urllib.request.urlopen(req, timeout=90) as resp, dest.with_suffix(".part").open("wb") as f:
            result.update(http_status=resp.status, headers={k.lower():v for k,v in resp.headers.items() if k.lower() in ['last-modified','content-type','etag','content-length']})
            while chunk := resp.read(1024*1024):
                f.write(chunk)
        part = dest.with_suffix(".part")
        result.update(bytes=part.stat().st_size, sha256=hashlib.file_digest(part.open("rb"), "sha256").hexdigest())
        result["matches_expected"] = result["sha256"] == expected if expected else None
        if expected and not result["matches_expected"]:
            dest = dest.with_name(dest.stem + "_new_vintage" + dest.suffix)
        part.replace(dest)
        result["destination"] = str(dest.relative_to(ROOT))
    except Exception as exc:
        result.update(error=str(exc), http_status=getattr(exc,"code",None))
    log = ROOT / 'research_completion/data/acquisition_log.jsonl'
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(result) + "\n")
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('url'); ap.add_argument('dest'); ap.add_argument('--expected')
    a=ap.parse_args()
    result=fetch(a.url, ROOT/a.dest, a.expected)
    raise SystemExit(1 if 'error' in result else 0)
