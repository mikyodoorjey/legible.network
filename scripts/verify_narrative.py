#!/usr/bin/env python3
"""Check every source URL in the narrator files. Writes data/narrative/links-<date>.json.

Usage: python3 scripts/verify_narrative.py [--timeout 12] [--workers 8]
The merge step reads the newest links file and stamps each statement's source with
link: live | redirected | unreachable | manual (hosts that cannot be checked by machine).
Standard library only.
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import get, DATA, TODAY  # noqa: E402

RAW = DATA / "narrative" / "raw"
MANUAL_HOSTS = ("x.com", "twitter.com", "discord.com", "discord.gg", "t.me", "medium.com", "web.archive.org")


def classify(url, timeout):
    host = urlparse(url).netloc.replace("www.", "")
    if any(host == h or host.endswith("." + h) for h in MANUAL_HOSTS):
        return "manual"
    status, _, final = get(url, timeout=timeout, ttl_hours=24)
    if isinstance(status, int) and 200 <= status < 300:
        return "redirected" if final.rstrip("/") != url.rstrip("/") else "live"
    if isinstance(status, int) and status in (401, 402, 403, 429):
        return "manual"  # blocks machines, not necessarily dead
    return "unreachable"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=int, default=12)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    urls = set()
    for f in sorted(RAW.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            print(f"  {f.name}: not valid JSON yet, skipped", file=sys.stderr)
            continue
        for s in d.get("statements", []):
            u = (s.get("source") or {}).get("url", "")
            if u.startswith("http"):
                urls.add(u)
            au = (s.get("source") or {}).get("archive_url", "")
            if au.startswith("http"):
                urls.add(au)
    urls = sorted(urls)
    print(f"checking {len(urls)} urls", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        results = dict(zip(urls, ex.map(lambda u: classify(u, a.timeout), urls)))
    out = DATA / "narrative" / f"links-{TODAY}.json"
    out.write_text(json.dumps({"checked": TODAY, "results": results}, indent=1, sort_keys=True), encoding="utf-8")
    from collections import Counter
    c = Counter(results.values())
    print(f"wrote {out.name}: " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())), file=sys.stderr)


if __name__ == "__main__":
    main()
