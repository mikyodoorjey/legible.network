#!/usr/bin/env python3
"""Merge the per-slice score CSVs into data/scores.csv and recompute scores.

Usage: python3 scripts/merge_scores.py [--only a] [--force]

- Loads data/scores-{a,b,c,d}.csv under the column contract, rejoins split entries,
  recomputes each audience score and the composite from the evidence cells.
- Checks every netuid in data/subnets.csv appears exactly once.
- Lists unknown and malformed cells and per-slice mean and spread.
- Refuses to overwrite rows in scores.csv that carry a "reviewed by" stamp unless --force.
- --only <slice> replaces just that slice's unreviewed rows.
"""
import argparse
import statistics
import sys

from common import (AUDIENCES, DATA, SCORE_COLUMNS, TODAY, audience_score, composite_score, load_csv,
                    parse_evidence, rejoin_entries, stamp, write_csv)


def recompute(row):
    """Recompute audience and composite scores from evidence; return list of warnings."""
    warnings = []
    aud = {}
    for a in AUDIENCES:
        cell = row.get(f"{a}_evidence", "")
        row[f"{a}_evidence"] = "; ".join(rejoin_entries(cell)) if cell.strip() else cell
        parsed = parse_evidence(row[f"{a}_evidence"])
        score, partial, unknown = audience_score(parsed)
        aud[a] = score
        qs = [e["q"] for e in parsed["entries"]]
        for q in ("q1", "q2", "q3", "q4"):
            if q not in qs:
                warnings.append(f"{a}.{q} missing")
        for e in parsed["entries"]:
            if e["status"] == "malformed":
                warnings.append(f"{a}.{e['q'] or '?'} malformed: {e['note'][:60]}")
            elif e["status"] == "unknown":
                warnings.append(f"{a}.{e['q']} unknown")
        old = row.get(f"{a}_score", "").strip()
        new = "" if score is None else f"{score:.1f}"
        if old and new and abs(float(old) - score) > 0.05:
            warnings.append(f"{a}_score agent {old} vs recomputed {new}")
        row[f"{a}_score"] = new
    comp, partial = composite_score(aud)
    row["composite"] = "" if comp is None else f"{comp:.1f}"
    return warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=list("abcd"))
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    targets = {r["netuid"]: r for r in load_csv(DATA / "subnets.csv", ["netuid", "rank", "name", "slice"])}
    existing = {}
    if (DATA / "scores.csv").exists():
        existing = {r["netuid"]: r for r in load_csv(DATA / "scores.csv")}

    slices = [a.only] if a.only else list("abcd")
    merged = dict(existing) if a.only else {}
    per_slice = {}
    problems = []
    for s in slices:
        p = DATA / f"scores-{s}.csv"
        if not p.exists():
            print(f"  missing {p.name}", file=sys.stderr)
            continue
        rows = load_csv(p)
        vals = []
        for r in rows:
            nid = r["netuid"]
            prior = existing.get(nid)
            if prior and "reviewed by" in prior.get("claim_labels", "") and not a.force:
                print(f"  SN{nid}: keeping reviewed row (pass --force to overwrite)", file=sys.stderr)
                merged[nid] = prior
                continue
            if not any(r.get(f"{x}_evidence", "").strip() for x in AUDIENCES):
                continue  # untouched stub
            w = recompute(r)
            stamp(r, f"merged {TODAY}")
            r["last_verified"] = r.get("last_verified") or TODAY
            merged[nid] = r
            if r["composite"]:
                vals.append(float(r["composite"]))
            for x in w:
                problems.append(f"SN{nid} {r['name']}: {x}")
        if vals:
            per_slice[s] = (statistics.mean(vals), statistics.pstdev(vals) if len(vals) > 1 else 0.0, len(vals))

    missing = [nid for nid in targets if nid not in merged]
    extra = [nid for nid in merged if nid not in targets]
    out = sorted(merged.values(), key=lambda r: int(r["rank"] or 999))
    write_csv(DATA / "scores.csv", out)

    print(f"scores.csv: {len(out)} rows ({len(missing)} of {len(targets)} targets unscored{', extra: ' + ','.join(extra) if extra else ''})", file=sys.stderr)
    if missing:
        print("  unscored: " + ", ".join(f"SN{n} {targets[n]['name']}" for n in missing), file=sys.stderr)
    if per_slice:
        means = [m for m, _, _ in per_slice.values()]
        grand = statistics.mean(means)
        for s, (m, sd, n) in sorted(per_slice.items()):
            flag = "  <-- deviates by more than 0.7, review the whole slice" if abs(m - grand) > 0.7 else ""
            print(f"  slice {s}: n={n} mean={m:.2f} sd={sd:.2f}{flag}", file=sys.stderr)
    print(f"  {len(problems)} cell problems", file=sys.stderr)
    for x in problems[:60]:
        print("   ", x, file=sys.stderr)
    if len(problems) > 60:
        print(f"    ... {len(problems) - 60} more", file=sys.stderr)


if __name__ == "__main__":
    main()
