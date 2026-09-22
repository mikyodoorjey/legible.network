#!/usr/bin/env python3
"""Validate a mining program manifest against the contract in agents/PROGRAM-PROMPT.md.

Usage: python3 scripts/program_check.py data/programs/raw/<netuid>.json [...]
       python3 scripts/program_check.py            (every file in data/programs/raw)
Exit 1 on any failure. Standard library only.

A manifest is the subnet's puzzle written as a spec: seven fields, each with
a source and a trust level naming what kind of thing the claim rests on.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
RAW = DATA / "programs" / "raw"

FIELDS = ["work", "scoring", "split", "judges", "cadence", "buyer", "exploits"]
TRUST = ["chain", "code", "docs", "said", "read", "unknown"]
COMMODITIES = {"inference", "compute", "training", "data", "agents", "forecasting",
               "storage", "security", "media", "science", "other"}
DASHES = ("—", "–")
BANNED = ("leverage", "ecosystem", "cutting-edge", "seamless", "robust", "unlock", "supercharge", "game-changing", "revolutionary", "delve")
MAX_QUOTE_WORDS = 25
MAX_TEXT_WORDS = 70
URL_RE = re.compile(r"^https?://\S+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")


def words(s):
    return len((s or "").split())


def load_statement_ids():
    p = DATA / "narrative.json"
    if not p.exists():
        return None
    ids = set()

    def walk(o):
        if isinstance(o, dict):
            if "id" in o and "quote" in o:
                ids.add(o["id"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(json.loads(p.read_text(encoding="utf-8")))
    return ids


def check_field(name, f, d, fails, statement_ids):
    if not isinstance(f, dict):
        fails.append(f"fields.{name}: not an object")
        return
    trust = f.get("trust")
    if trust not in TRUST:
        fails.append(f"fields.{name}: trust must be one of {', '.join(TRUST)}")
        return
    text = f.get("text", "")
    if not text or not text.strip():
        fails.append(f"fields.{name}: text missing (an unknown field still says what was looked for)")
    if words(text) > MAX_TEXT_WORDS:
        fails.append(f"fields.{name}: text is {words(text)} words, cap is {MAX_TEXT_WORDS}")
    for s in (text, f.get("quote", ""), f.get("disagrees", "")):
        if any(ch in (s or "") for ch in DASHES):
            fails.append(f"fields.{name}: em or en dash")
        low = (s or "").lower()
        for w in BANNED:
            if re.search(r"\b" + re.escape(w) + r"\b", low):
                fails.append(f"fields.{name}: banned word '{w}'")
    if trust == "unknown":
        if f.get("url") or f.get("quote"):
            fails.append(f"fields.{name}: unknown carries a url or quote; either it is known or it is not")
        return
    url = f.get("url", "")
    if trust == "chain":
        snap = f.get("snapshot", "")
        if not snap or not (REPO / snap).exists():
            fails.append(f"fields.{name}: chain trust needs a snapshot path that exists (got '{snap}')")
    elif not URL_RE.match(url or ""):
        fails.append(f"fields.{name}: {trust} trust needs a fetched url")
    quote = f.get("quote", "")
    if not quote:
        fails.append(f"fields.{name}: quote missing (the words on the page, or the value read from code or chain)")
    elif words(quote) > MAX_QUOTE_WORDS:
        fails.append(f"fields.{name}: quote is {words(quote)} words, cap is {MAX_QUOTE_WORDS}")
    if trust == "code":
        if not f.get("path"):
            fails.append(f"fields.{name}: code trust needs a path inside the repo")
        if not SHA_RE.match((d.get("repo") or {}).get("commit", "")):
            fails.append(f"fields.{name}: code trust needs repo.commit pinned")
    if trust == "said":
        sid = f.get("statement", "")
        if not sid:
            fails.append(f"fields.{name}: said trust needs a statement id from the map")
        elif statement_ids is not None and sid not in statement_ids:
            fails.append(f"fields.{name}: statement {sid} is not in data/narrative.json")
    if url and url not in (d.get("sources") or []):
        fails.append(f"fields.{name}: url not in sources: {url[:70]}")


def check(path):
    fails = []
    try:
        d = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as ex:  # noqa
        return [f"{path}: not valid JSON: {ex}"]
    netuid = d.get("netuid")
    if not isinstance(netuid, int):
        fails.append("netuid missing or not an integer")
    elif Path(path).stem != str(netuid):
        fails.append(f"file name {Path(path).stem} does not match netuid {netuid}")
    for k in ("name", "version", "read_on", "commodity"):
        if not d.get(k):
            fails.append(f"{k} missing")
    if d.get("read_on") and not DATE_RE.match(str(d["read_on"])):
        fails.append("read_on must be YYYY-MM-DD")
    if d.get("commodity") and d["commodity"] not in COMMODITIES:
        fails.append(f"commodity '{d['commodity']}' not in the allowed set")
    repo = d.get("repo")
    if repo is not None:
        if not URL_RE.match(repo.get("url", "") or ""):
            fails.append("repo.url missing or not a url")
        if repo.get("commit") and not SHA_RE.match(repo["commit"]):
            fails.append("repo.commit is not a git sha")
        if repo.get("commit") and not DATE_RE.match(repo.get("committed", "") or ""):
            fails.append("repo.committed (the pinned commit's date) must be YYYY-MM-DD")
    fields = d.get("fields") or {}
    missing = [f for f in FIELDS if f not in fields]
    if missing:
        fails.append(f"fields missing: {', '.join(missing)}")
    extra = [f for f in fields if f not in FIELDS]
    if extra:
        fails.append(f"fields not in the schema: {', '.join(extra)}")
    sources = d.get("sources")
    if not isinstance(sources, list):
        fails.append("sources must be a list of fetched urls")
        d["sources"] = []
    else:
        for u in sources:
            if not URL_RE.match(u or ""):
                fails.append(f"sources: not a url: {str(u)[:70]}")
    statement_ids = load_statement_ids()
    for name in FIELDS:
        if name in fields:
            check_field(name, fields[name], d, fails, statement_ids)
    return [f"{Path(path).name}: {f}" for f in fails]


def main():
    args = sys.argv[1:]
    files = [Path(a) for a in args] if args else sorted(RAW.glob("*.json"))
    if not files:
        print("no manifests found", file=sys.stderr)
        sys.exit(1)
    fails = []
    for p in files:
        fails += check(p)
    print(f"{len(files)} manifests checked", file=sys.stderr)
    if fails:
        for f in fails:
            print(f)
        sys.exit(1)
    print("ok", file=sys.stderr)


if __name__ == "__main__":
    main()
