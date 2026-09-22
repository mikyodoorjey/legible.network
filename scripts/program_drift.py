#!/usr/bin/env python3
"""Check every mining program's pinned commit against its repository's current head.

Usage: python3 scripts/program_drift.py [--token $GITHUB_TOKEN]
Writes data/programs-drift.json. Standard library only. Runs weekly from GitHub Actions
and can be run by hand.

For each manifest with a pinned repo commit, asks the GitHub compare API how far the
default branch has moved and which files changed. A field at code trust whose `path`
is among the changed files is marked stale. The pages read the result client-side, so
the static site says what it knows without a rebuild; re-reading a stale program is a
human-triggered run of the brief (agents/PROGRAM-PROMPT.md) against that subnet.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
RAW = DATA / "programs" / "raw"
TODAY = date.today().isoformat()
API = "https://api.github.com"


def gh(url, token=None):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "legible.network drift check",
                                              **({"Authorization": f"Bearer {token}"} if token else {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def org_repo(url):
    m = re.match(r"https?://github\.com/([^/]+)/([^/#?]+)", url or "")
    return (m.group(1), m.group(2).removesuffix(".git")) if m else (None, None)


def check_one(m, token):
    repo = m.get("repo") or {}
    org, name = org_repo(repo.get("url"))
    commit = repo.get("commit")
    out = {"repo": repo.get("url"), "commit": commit, "head": None, "ahead_by": None, "changed_paths": [], "stale_fields": [], "error": None}
    if not (org and name and commit):
        out["error"] = "no pinned repository commit"
        return out
    try:
        info = gh(f"{API}/repos/{org}/{name}", token)
        branch = info.get("default_branch", "main")
        head = gh(f"{API}/repos/{org}/{name}/commits/{branch}", token)["sha"]
        out["head"] = head
        if head.startswith(commit) or commit.startswith(head):
            out["ahead_by"] = 0
            return out
        cmp = gh(f"{API}/repos/{org}/{name}/compare/{commit}...{head}", token)
        out["ahead_by"] = cmp.get("ahead_by")
        # the compare API lists at most 300 files; enough for a week of a subnet repo, and the count says when it is not
        out["changed_paths"] = sorted({f["filename"] for f in cmp.get("files", [])})
        out["files_truncated"] = len(cmp.get("files", [])) >= 300
        cited = {k: v.get("path") for k, v in (m.get("fields") or {}).items() if v.get("trust") == "code" and v.get("path")}
        changed = set(out["changed_paths"])
        out["stale_fields"] = [k for k, p in cited.items() if p in changed]
    except urllib.error.HTTPError as ex:
        out["error"] = f"HTTP {ex.code}"
    except Exception as ex:  # noqa
        out["error"] = str(ex)[:120]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token", default=os.environ.get("GITHUB_TOKEN", ""))
    a = ap.parse_args()
    programs = {}
    for p in sorted(RAW.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            programs[str(d["netuid"])] = d
        except Exception as ex:  # noqa
            print(f"  skipped {p.name}: {ex}", file=sys.stderr)
    out = {"checked_at": TODAY, "programs": {}}
    n_stale = 0
    for uid, m in programs.items():
        r = check_one(m, a.token or None)
        out["programs"][uid] = r
        n_stale += bool(r["stale_fields"])
        print(f"  SN{uid} {m.get('name', '')}: " + (r["error"] or f"ahead {r['ahead_by']}, stale {r['stale_fields'] or 'none'}"), file=sys.stderr)
    out["summary"] = {"programs": len(programs), "with_stale_fields": n_stale,
                      "errors": sum(1 for r in out["programs"].values() if r["error"])}
    (DATA / "programs-drift.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"wrote data/programs-drift.json: {out['summary']}", file=sys.stderr)


if __name__ == "__main__":
    main()
