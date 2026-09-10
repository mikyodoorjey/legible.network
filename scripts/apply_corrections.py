#!/usr/bin/env python3
"""Apply pending rows from data/corrections.csv to data/scores.csv and rebuild.

Usage: python3 scripts/apply_corrections.py

data/corrections.csv columns:
  date, netuid, audience, q, old_score, new_score, new_status, url, note, requested_by, reason, applied
The file is created with just the header when missing. Every row whose `applied` is
blank is applied once: the matching evidence entry gets the new score, the new status
and URL when given, and a note that keeps the old one as "was: ...". The row is
stamped "corrected <date>: ...", scores are recomputed, `applied` is set to today, both
CSVs are written, and build.py runs. Whether a row is a factual fix or a score dispute
is decided before it goes in the file; this script applies what is there.
"""
import subprocess
import sys
from pathlib import Path

from common import AUDIENCES, DATA, QUESTIONS, TODAY, load_csv, set_verified, stamp, write_csv
from merge_scores import recompute
from review import clean_note, edit_entry
from verify_links import norm_url

CORRECTION_COLUMNS = ["date", "netuid", "audience", "q", "old_score", "new_score", "new_status", "url", "note",
                      "requested_by", "reason", "applied"]


def load_corrections(path=None):
    path = path or DATA / "corrections.csv"
    if not path.exists():
        write_csv(path, [], CORRECTION_COLUMNS)
        print(f"created empty {path.name}", file=sys.stderr)
        return []
    return load_csv(path, CORRECTION_COLUMNS)


def apply_one(row, c):
    """Rewrite one entry from a correction row. Returns (old_score, new_score) or None."""
    a, q = c["audience"].strip().lower(), c["q"].strip().lower()
    if a not in AUDIENCES or q not in QUESTIONS:
        print(f"  SN{c['netuid']}: bad cell {a}.{q}", file=sys.stderr)
        return None
    try:
        new = int(c["new_score"])
        assert 0 <= new <= 5
    except (ValueError, AssertionError):
        print(f"  SN{c['netuid']} {a}.{q}: new_score {c['new_score']!r} is not 0 to 5", file=sys.stderr)
        return None
    cur = edit_entry(row, a, q)
    old_note = cur["note"] if cur else ""
    note = f"was: {old_note}" if old_note else "was: (no note)"
    if c["note"].strip():
        note = f"{note}, {clean_note(c['note'])}"
    kw = {"score": new, "note": note}
    status = c["new_status"].strip().lower()
    if status in ("verified", "inferred", "unknown"):
        kw["status"] = status
    url = norm_url(c["url"])
    if url:
        kw["url"] = url
    old = edit_entry(row, a, q, **kw)
    old_score = old["score"] if old else (c["old_score"] or "?")
    return old_score, new


def main():
    corrections = load_corrections()
    pending = [c for c in corrections if not c["applied"].strip()]
    if not pending:
        print("no pending corrections", file=sys.stderr)
        return
    rows = load_csv(DATA / "scores.csv")
    by_nid = {r["netuid"]: r for r in rows}
    applied = 0
    for c in pending:
        row = by_nid.get(c["netuid"].strip())
        if not row:
            print(f"  SN{c['netuid']}: not in scores.csv, left pending", file=sys.stderr)
            continue
        res = apply_one(row, c)
        if res is None:
            continue
        old, new = res
        if not c["old_score"].strip():
            c["old_score"] = str(old)
        who = c["requested_by"].strip() or "unattributed"
        stamp(row, f"corrected {TODAY}: {c['audience']}.{c['q']} {old}->{new}, requested by {who}: {clean_note(c['reason'])}")
        set_verified(row)
        for w in recompute(row):
            if "malformed" in w:
                print(f"  SN{row['netuid']}: {w}", file=sys.stderr)
        c["applied"] = TODAY
        c["date"] = c["date"].strip() or TODAY
        applied += 1
        print(f"  SN{row['netuid']} {c['audience']}.{c['q']} {old}->{new} ({who})", file=sys.stderr)

    write_csv(DATA / "corrections.csv", corrections, CORRECTION_COLUMNS)
    write_csv(DATA / "scores.csv", rows)
    print(f"applied {applied} of {len(pending)} pending corrections; wrote corrections.csv and scores.csv", file=sys.stderr)
    if not applied:
        return
    build = Path(__file__).resolve().parent / "build.py"
    rc = subprocess.call([sys.executable, str(build)])
    if rc:
        print(f"build.py exited {rc}; scores.csv and corrections.csv are written, index.json is not", file=sys.stderr)
        sys.exit(rc)


if __name__ == "__main__":
    main()
