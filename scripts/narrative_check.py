#!/usr/bin/env python3
"""Validate a narrative raw file against the contract in agents/NARRATIVE-PROMPT.md.

Usage: python3 scripts/narrative_check.py data/narrative/raw/<id>.json [...]
Exit 1 on any failure. Standard library only.
"""
import json
import re
import sys
from pathlib import Path

SLOTS = {
    "foundation.mission", "foundation.vision", "foundation.values",
    "problem.cultural", "problem.market", "problem.institutional",
    "opportunity", "audience",
    "positioning.category", "positioning.differentiator", "positioning.reason", "positioning.against",
    "value.functional", "value.emotional", "value.self_expressive",
    "messaging.h1", "messaging.proof", "voice", "relationship", "language.term",
    "subnet.self", "subnet.network",
}
ERAS = ["pre", "nakamoto", "finney", "revolution", "dtao", "current"]
ERA_BOUNDS = [("pre", "0000-00", "2020-12"), ("nakamoto", "2021-01", "2023-02"), ("finney", "2023-03", "2023-09"),
              ("revolution", "2023-10", "2025-01"), ("dtao", "2025-02", "2026-05"), ("current", "2026-06", "9999-99")]
MEDIA = {"podcast", "youtube", "x", "blog", "whitepaper", "docs", "article", "talk", "discord", "forum", "other"}
CONF = {"verified", "probable", "unverified"}
TRANSCRIPT = {"primary", "auto", "show-notes", "secondary", "none"}
KINDS = {"person", "institution", "subnet"}
REL = {"agrees", "borrows", "argues", "responds", "introduces"}
DASHES = ("—", "–")


def era_for(date):
    ym = (date or "")[:7]
    for era, lo, hi in ERA_BOUNDS:
        if lo <= ym <= hi:
            return era
    return None


def check(path):
    fails = []
    try:
        d = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as ex:  # noqa
        return [f"{path}: not valid JSON: {ex}"]
    n = d.get("narrator") or {}
    nid = n.get("id", "")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", nid or ""):
        fails.append("narrator.id missing or not kebab-case")
    if Path(path).stem != nid:
        fails.append(f"file name {Path(path).stem} does not match narrator.id {nid}")
    if n.get("kind") not in KINDS:
        fails.append("narrator.kind must be person, institution, or subnet")
    for k in ("name", "one_line"):
        if not n.get(k):
            fails.append(f"narrator.{k} missing")
    if n.get("kind") == "subnet" and not n.get("subnets"):
        fails.append("subnet narrator has no subnets list")
    sts = d.get("statements") or []
    if not sts:
        fails.append("no statements")
    ids = set()
    seen_seq = []
    for s in sts:
        sid = s.get("id", "")
        m = re.fullmatch(rf"{re.escape(nid)}-(\d{{3,}})", sid or "")
        if not m:
            fails.append(f"statement id {sid!r} must be {nid}-NNN")
        elif sid in ids:
            fails.append(f"duplicate statement id {sid}")
        else:
            seen_seq.append(int(m.group(1)))
        ids.add(sid)
        q = (s.get("quote") or "").strip()
        if not q:
            fails.append(f"{sid}: empty quote")
        elif len(q.split()) > 60:
            fails.append(f"{sid}: quote over 60 words ({len(q.split())})")
        if not s.get("context"):
            fails.append(f"{sid}: missing context")
        date = s.get("date") or ""
        if not re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?", date):
            fails.append(f"{sid}: date {date!r} not YYYY, YYYY-MM, or YYYY-MM-DD")
        prec = s.get("date_precision")
        if prec not in ("day", "month", "year"):
            fails.append(f"{sid}: date_precision must be day, month, or year")
        elif (prec == "day" and len(date) != 10) or (prec == "month" and len(date) != 7) or (prec == "year" and len(date) != 4):
            fails.append(f"{sid}: date {date} does not match precision {prec}")
        if s.get("era") not in ERAS:
            fails.append(f"{sid}: era {s.get('era')!r} not in {ERAS}")
        elif len(date) >= 7 and era_for(date) != s.get("era"):
            fails.append(f"{sid}: era {s.get('era')} does not match date {date} (expected {era_for(date)})")
        about = s.get("about") or ""
        if not (about == "network" or re.fullmatch(r"subnet:\d+", about)):
            fails.append(f"{sid}: about must be 'network' or 'subnet:<netuid>'")
        slots = s.get("slots") or []
        if not slots:
            fails.append(f"{sid}: no slots")
        for sl in slots:
            if sl not in SLOTS:
                fails.append(f"{sid}: unknown slot {sl!r}")
        src = s.get("source") or {}
        if not (src.get("url") or "").startswith("http"):
            fails.append(f"{sid}: source.url missing")
        if src.get("medium") not in MEDIA:
            fails.append(f"{sid}: source.medium {src.get('medium')!r} not allowed")
        if src.get("transcript", "none") not in TRANSCRIPT:
            fails.append(f"{sid}: source.transcript {src.get('transcript')!r} not allowed")
        if s.get("confidence") not in CONF:
            fails.append(f"{sid}: confidence must be verified, probable, or unverified")
        for field in ("quote", "context"):
            if any(ch in (s.get(field) or "") for ch in DASHES) and field == "context":
                fails.append(f"{sid}: {field} uses a dash; rewrite")
        for m_ in s.get("metaphors") or []:
            if not re.fullmatch(r"[a-z][a-z0-9 -]{0,30}", m_):
                fails.append(f"{sid}: metaphor label {m_!r} must be lowercase, short")
    if seen_seq and seen_seq != sorted(seen_seq):
        fails.append("statement ids are not in ascending order")
    dates = [s.get("date", "") for s in sts]
    if dates != sorted(dates):
        fails.append("statements are not in date order")
    for m_ in d.get("metaphors") or []:
        if not m_.get("label") or not m_.get("wording"):
            fails.append("metaphor entry missing label or wording")
        if m_.get("first_statement") and m_["first_statement"] not in ids:
            fails.append(f"metaphor {m_.get('label')}: first_statement {m_['first_statement']} not found")
        if m_.get("origin") not in ("introduced", "reused", "unknown"):
            fails.append(f"metaphor {m_.get('label')}: origin must be introduced, reused, or unknown")
    fw = d.get("framework") or {}
    for slot, v in fw.items():
        if slot not in SLOTS:
            fails.append(f"framework slot {slot!r} unknown")
        if not (v or {}).get("summary"):
            fails.append(f"framework.{slot}: missing summary")
        cited = (v or {}).get("statements") or []
        if not cited:
            fails.append(f"framework.{slot}: cites no statements")
        for c in cited:
            if c not in ids:
                fails.append(f"framework.{slot}: cites unknown statement {c}")
        if any(ch in (v or {}).get("summary", "") for ch in DASHES):
            fails.append(f"framework.{slot}: summary uses a dash; rewrite")
    for g in d.get("genealogy") or []:
        if g.get("era") not in ERAS:
            fails.append(f"genealogy era {g.get('era')!r} unknown")
        for c in re.findall(r"\[([a-z0-9-]+-\d{3,})\]", g.get("summary", "")):
            if c not in ids:
                fails.append(f"genealogy {g.get('era')}: cites unknown statement {c}")
        if any(ch in g.get("summary", "") for ch in DASHES):
            fails.append(f"genealogy {g.get('era')}: summary uses a dash; rewrite")
    for r in d.get("relations") or []:
        if r.get("kind") not in REL:
            fails.append(f"relation to {r.get('to')}: kind must be one of {sorted(REL)}")
        if r.get("statement") and r["statement"] not in ids:
            fails.append(f"relation to {r.get('to')}: statement {r['statement']} not found")
    for c in (d.get("language") or {}).get("coinages") or []:
        if c.get("statement") and c["statement"] not in ids:
            fails.append(f"coinage {c.get('term')}: statement {c['statement']} not found")
    cov = d.get("coverage") or {}
    for k in ("searches_used", "fetches_used"):
        if not isinstance(cov.get(k), int):
            fails.append(f"coverage.{k} must be an integer")
    return [f"{path}: {f}" for f in fails]


def main():
    paths = sys.argv[1:] or sorted(Path("data/narrative/raw").glob("*.json"))
    fails = []
    for p in paths:
        fails += check(p)
    for f in fails:
        print(f, file=sys.stderr)
    if fails:
        print(f"{len(fails)} problem(s)", file=sys.stderr)
        sys.exit(1)
    tot = sum(len(json.loads(Path(p).read_text()).get("statements", [])) for p in paths)
    print(f"ok: {len(paths)} file(s), {tot} statements")


if __name__ == "__main__":
    main()
