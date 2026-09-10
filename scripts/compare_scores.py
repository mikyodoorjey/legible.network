#!/usr/bin/env python3
"""Compare two score CSVs cell by cell (for the pilot against the calibration set, or any rerun).

Usage: python3 scripts/compare_scores.py data/scores-calibration.csv data/scores-pilot.csv
Prints per-cell differences, the count of cells within one point, and per-audience means.
"""
import sys

from common import AUDIENCES, QUESTIONS, load_csv, parse_evidence


def cells(row):
    out = {}
    for a in AUDIENCES:
        p = parse_evidence(row.get(f"{a}_evidence", ""))
        for e in p["entries"]:
            if e["q"] in QUESTIONS and (a, e["q"]) not in out:
                out[(a, e["q"])] = e
    return out


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    a_rows = {r["netuid"]: r for r in load_csv(sys.argv[1])}
    b_rows = {r["netuid"]: r for r in load_csv(sys.argv[2])}
    common = sorted(set(a_rows) & set(b_rows), key=int)
    if not common:
        raise SystemExit("no shared netuids")
    total = within1 = exact = 0
    diffs = []
    for nid in common:
        ca, cb = cells(a_rows[nid]), cells(b_rows[nid])
        for a in AUDIENCES:
            for q in QUESTIONS:
                ea, eb = ca.get((a, q)), cb.get((a, q))
                sa = ea["score"] if ea else None
                sb = eb["score"] if eb else None
                if sa is None or sb is None:
                    diffs.append((nid, a, q, sa, sb, "unknown on one side"))
                    continue
                total += 1
                d = abs(sa - sb)
                exact += d == 0
                within1 += d <= 1
                if d >= 2:
                    diffs.append((nid, a, q, sa, sb, f"{ea['status']} vs {eb['status']}: {(ea['note'] or '')[:70]} || {(eb['note'] or '')[:70]}"))
    print(f"shared subnets: {common}")
    print(f"cells compared: {total}; exact {exact} ({100 * exact / max(total, 1):.0f}%); within 1 point {within1} ({100 * within1 / max(total, 1):.0f}%)")
    print("cells differing by 2 or more, or unknown on one side:")
    for nid, a, q, sa, sb, why in diffs:
        print(f"  SN{nid} {a}.{q}: {sys.argv[1].split('/')[-1]}={sa} {sys.argv[2].split('/')[-1]}={sb}  {why}")
    for nid in common:
        ca, cb = cells(a_rows[nid]), cells(b_rows[nid])
        means = []
        for a in AUDIENCES:
            va = [ca[(a, q)]["score"] for q in QUESTIONS if (a, q) in ca and ca[(a, q)]["score"] is not None]
            vb = [cb[(a, q)]["score"] for q in QUESTIONS if (a, q) in cb and cb[(a, q)]["score"] is not None]
            means.append(f"{a} {sum(va) / len(va) if va else 0:.1f} vs {sum(vb) / len(vb) if vb else 0:.1f}")
        print(f"SN{nid} {a_rows[nid]['name']}: " + "; ".join(means))


if __name__ == "__main__":
    main()
