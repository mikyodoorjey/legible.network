#!/usr/bin/env python3
"""Apply pending rows from data/program-corrections.csv to the raw mining program manifests.

Usage: python3 scripts/apply_program_corrections.py

data/program-corrections.csv columns:
  date, netuid, field, new_text, new_trust, url, quote, path, statement, requested_by, reason, applied
The file is created with just the header when missing. Every row whose `applied` is blank
is applied once: the field's text, trust and evidence are replaced by what the row gives
(blank cells keep the current value), the previous reading is kept under the manifest's
`corrections` list with the date, who asked and why, `read_on` is left alone (the reading
date is the reading date), and the check script runs on the file. Rows that fail the check
are rolled back and left pending. Rebuild with scripts/build_site.py afterwards.

Whether a row is a factual fix or a dispute about the reading is decided before it goes
in the file; this script applies what is there.
"""
import csv
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
RAW = DATA / "programs" / "raw"
TODAY = date.today().isoformat()
COLUMNS = ["date", "netuid", "field", "new_text", "new_trust", "url", "quote", "path", "statement",
           "requested_by", "reason", "applied"]
FIELDS = ["work", "scoring", "split", "judges", "cadence", "buyer", "exploits"]
TRUST = ["chain", "code", "docs", "said", "read", "unknown"]


def load(path):
    if not path.exists():
        with path.open("w", encoding="utf-8", newline="") as fh:
            csv.DictWriter(fh, fieldnames=COLUMNS).writeheader()
        print(f"created empty {path.name}", file=sys.stderr)
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return [dict(r) for r in csv.DictReader(fh)]


def save(path, rows):
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in COLUMNS})


def apply_one(c):
    field = c["field"].strip().lower()
    if field not in FIELDS:
        print(f"  SN{c['netuid']}: bad field {field!r}", file=sys.stderr)
        return False
    p = RAW / f"{c['netuid'].strip()}.json"
    if not p.exists():
        print(f"  SN{c['netuid']}: no manifest", file=sys.stderr)
        return False
    m = json.loads(p.read_text(encoding="utf-8"))
    f = dict(m["fields"].get(field) or {})
    old = dict(f)
    trust = c["new_trust"].strip().lower()
    if trust:
        if trust not in TRUST:
            print(f"  SN{c['netuid']} {field}: bad trust {trust!r}", file=sys.stderr)
            return False
        f["trust"] = trust
    if c["new_text"].strip():
        f["text"] = c["new_text"].strip()
    for k in ("url", "quote", "path", "statement"):
        if c.get(k, "").strip():
            f[k] = c[k].strip()
    if f.get("trust") == "unknown":
        for k in ("url", "quote", "path", "statement", "snapshot"):
            f.pop(k, None)
    f.pop("disagrees", None) if c["reason"].strip().lower().startswith("resolves:") else None
    if f.get("url") and f["url"] not in m.get("sources", []):
        m.setdefault("sources", []).append(f["url"])
    m["fields"][field] = f
    who = c["requested_by"].strip() or "unattributed"
    m.setdefault("corrections", []).append({
        "date": c["date"].strip() or TODAY, "field": field,
        "old_trust": old.get("trust", ""), "new_trust": f.get("trust", ""),
        "old_text": old.get("text", ""), "requested_by": who, "reason": c["reason"].strip(),
    })
    backup = p.with_suffix(".json.bak")
    shutil.copy(p, backup)
    p.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rc = subprocess.call([sys.executable, str(REPO / "scripts" / "program_check.py"), str(p)])
    if rc:
        shutil.move(backup, p)
        print(f"  SN{c['netuid']} {field}: check failed, rolled back, left pending", file=sys.stderr)
        return False
    backup.unlink()
    print(f"  SN{c['netuid']} {field}: {old.get('trust', '?')} -> {f.get('trust', '?')} ({who})", file=sys.stderr)
    return True


def main():
    path = DATA / "program-corrections.csv"
    rows = load(path)
    pending = [c for c in rows if not c.get("applied", "").strip()]
    if not pending:
        print("no pending program corrections", file=sys.stderr)
        return
    n = 0
    for c in pending:
        if apply_one(c):
            c["applied"] = TODAY
            c["date"] = c.get("date", "").strip() or TODAY
            n += 1
    save(path, rows)
    print(f"applied {n} of {len(pending)} pending; wrote {path.name}. Rebuild with scripts/build_site.py.", file=sys.stderr)


if __name__ == "__main__":
    main()
