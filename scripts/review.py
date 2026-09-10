#!/usr/bin/env python3
"""Build the human review queue from data/scores.csv and apply the reviewer's decisions.

Usage: python3 scripts/review.py [--apply] [--all]

Without --apply, writes data/review-<date>.csv (one line per queued cell with blank
decision and reviewer_note columns) and a phone-readable data/review-<date>.md.
A cell is queued when any of these hold: status unknown or malformed or missing;
score 0 or 5; status inferred with score 3 or more; the agent's audience score differs
from the recomputed one by more than 0.05; the subnet is in the top 5 or bottom 5 by
composite; own_words has no URL; the newest verify CSV says the cell's link is anything
but live or manual. --all queues every cell.

Decisions, filled in the CSV by the reviewer:
  keep          leave the cell as it is
  set:<0-5>     rewrite the score (reviewer_note starting "verified" also sets the status)
  unknown->0    score 0, status inferred, note "nothing found by hand <date>"
  recheck       collect into agents/recheck-<date>.md for another agent pass
A reviewer-edited note replaces the entry note with an "MC: " prefix.

--apply reads the newest data/review-*.csv, applies MANUAL first, then the decisions,
recomputes scores, stamps each change as "reviewed by MC <date>: ..." and rows with
no queued cells as "spot-checked MC <date>", and writes data/scores.csv. Idempotent.
"""
import argparse
import statistics
import sys

from common import (AGENTS, AUDIENCES, DATA, QUESTIONS, TODAY, audience_score, composite_score, load_csv,
                    parse_evidence, rejoin_entries, set_verified, stamp, write_csv)
from merge_scores import recompute
from verify_links import VERIFY_COLUMNS, norm_url

REVIEW_COLUMNS = ["netuid", "name", "audience", "q", "agent_score", "status", "url", "note", "link_result",
                  "why_queued", "decision", "reviewer_note"]

# Cells fixed by hand outside the CSV round trip. (netuid, audience, q) -> (score, reason).
# Applied on every --apply before the CSV decisions, so a rerun cannot lose them.
MANUAL = {
    # ("64", "buyers", "q2"): (3, "pricing page found at chutes.ai/pricing, agent missed it"),
}


# ---------------- entry editing (shared with apply_corrections.py)
def edit_entry(row, audience, q, **changes):
    """Rewrite one evidence entry in place. changes may set score, status, url, note.

    Returns the old entry as a dict, or None when the entry did not exist (in which
    case a new entry is appended when a score was given).
    """
    col = f"{audience}_evidence"
    raws = rejoin_entries(row.get(col, ""))
    for i, raw in enumerate(raws):
        parts = [p.strip() for p in raw.split("|")]
        if not parts or parts[0].lower() != q:
            continue
        while len(parts) < 5:
            parts.append("")
        old = {"score": parts[1], "status": parts[2], "url": parts[3], "note": " | ".join(parts[4:])}
        new = dict(old)
        new.update({k: str(v) for k, v in changes.items() if v is not None})
        raws[i] = " | ".join([q, new["score"], new["status"], new["url"] or "none", new["note"]])
        row[col] = "; ".join(raws)
        return old
    if "score" in changes:
        new = {"score": str(changes["score"]), "status": changes.get("status", "inferred"),
               "url": changes.get("url") or "none", "note": changes.get("note", "")}
        raws.append(" | ".join([q, new["score"], new["status"], new["url"], new["note"]]))
        row[col] = "; ".join(raws)
    return None


def clean_note(text):
    """Notes may not carry the two separators the cell format uses."""
    return (text or "").replace(";", ",").replace("|", "/").strip()


# ---------------- queue
def link_results():
    p = sorted(DATA.glob("verify-*.csv"))
    if not p:
        return {}, None
    return {norm_url(r["url"]): r["result"] for r in load_csv(p[-1], VERIFY_COLUMNS)}, p[-1].name


def cells_of(row):
    """Return {audience: {q: entry}} plus recomputed audience scores, without touching the row."""
    out, scores = {}, {}
    for a in AUDIENCES:
        parsed = parse_evidence(row.get(f"{a}_evidence", ""))
        by_q = {}
        for e in parsed["entries"]:
            by_q.setdefault(e["q"] if e["q"] in QUESTIONS else f"?{len(by_q)}", e)
        out[a] = by_q
        scores[a] = audience_score(parsed)[0]
    return out, scores


def build_queue(rows, links, queue_all=False):
    comps = []
    for r in rows:
        _, scores = cells_of(r)
        comp = composite_score(scores)[0]
        comps.append((comp if comp is not None else -1, r["netuid"]))
    ranked = [nid for _, nid in sorted(comps, key=lambda x: -x[0])]
    edge = set(ranked[:5]) | set(ranked[-5:])

    queue = []
    for r in rows:
        nid, name = r["netuid"], r["name"]
        cells, scores = cells_of(r)
        for a in AUDIENCES:
            agent = r.get(f"{a}_score", "").strip()
            mismatch = ""
            if agent and scores[a] is not None:
                try:
                    if abs(float(agent) - scores[a]) > 0.05:
                        mismatch = f"agent {a}_score {agent} vs recomputed {scores[a]:.1f}"
                except ValueError:
                    mismatch = f"agent {a}_score {agent!r} unparseable"
            for q in QUESTIONS:
                e = cells[a].get(q)
                why = []
                if e is None:
                    e = {"score": None, "status": "missing", "url": "", "note": ""}
                    why.append("missing")
                if e["status"] in ("unknown", "malformed"):
                    why.append(e["status"])
                if e["score"] in (0, 5):
                    why.append(f"score {e['score']}")
                if e["status"] == "inferred" and e["score"] is not None and e["score"] >= 3:
                    why.append("inferred at 3 or more")
                if mismatch:
                    why.append(mismatch)
                if nid in edge:
                    why.append("top or bottom 5 by composite")
                lr = links.get(norm_url(e["url"]), "") if e["url"] else ""
                if lr and lr not in ("live", "manual"):
                    why.append(f"link {lr}")
                if queue_all and not why:
                    why.append("all")
                if not why:
                    continue
                queue.append({"netuid": nid, "name": name, "audience": a, "q": q,
                              "agent_score": "" if e["score"] is None else str(e["score"]),
                              "status": e["status"], "url": e["url"], "note": e["note"], "link_result": lr,
                              "why_queued": "; ".join(why), "decision": "", "reviewer_note": ""})
            for k, e in cells[a].items():
                if k.startswith("?"):
                    queue.append({"netuid": nid, "name": name, "audience": a, "q": e["q"] or "?",
                                  "agent_score": "", "status": "malformed", "url": e["url"], "note": e["note"],
                                  "link_result": "", "why_queued": "malformed (unrecognised q)", "decision": "",
                                  "reviewer_note": ""})
        ow = r.get("own_words", "")
        quote, _, u = ow.rpartition(" | ")
        if not ow.strip() or not norm_url(u):
            queue.append({"netuid": nid, "name": name, "audience": "own_words", "q": "", "agent_score": "",
                          "status": "", "url": "", "note": ow[:200], "link_result": "",
                          "why_queued": "own_words has no URL" if ow.strip() else "own_words empty",
                          "decision": "", "reviewer_note": ""})
        elif queue_all:
            lr = links.get(norm_url(u), "")
            queue.append({"netuid": nid, "name": name, "audience": "own_words", "q": "", "agent_score": "",
                          "status": "", "url": norm_url(u), "note": quote[:200], "link_result": lr,
                          "why_queued": "all", "decision": "", "reviewer_note": ""})
    return queue


def write_markdown(rows, queue, path, verify_name):
    by_nid = {}
    for item in queue:
        by_nid.setdefault(item["netuid"], []).append(item)
    order = sorted(rows, key=lambda r: int(r["rank"] or 999))
    lines = [f"# Review queue {TODAY}", "",
             f"{len(queue)} cells across {len(by_nid)} subnets. Links from {verify_name or 'no verify CSV yet'}.",
             "Decisions go in the CSV: keep, set:<0-5>, unknown->0, recheck.", ""]
    def comp_of(r):
        c = composite_score(cells_of(r)[1])[0]
        return "?" if c is None else f"{c:.1f}"

    for r in order:
        items = by_nid.get(r["netuid"])
        if not items:
            continue
        lines.append(f"## SN{r['netuid']} {r['name']} (rank {r['rank']}, composite {comp_of(r)})")
        lines.append("")
        cur = None
        for it in items:
            if it["audience"] != cur:
                cur = it["audience"]
                lines.append(f"### {cur}")
            tag = f"{it['audience']}.{it['q']}" if it["q"] else it["audience"]
            head = f"agent {it['agent_score'] or '?'} {it['status']}".strip() if it["q"] else "quote"
            link = f" [{it['link_result']}]" if it["link_result"] else ""
            lines.append(f"- [ ] {tag} {head}: {it['note']} {it['url']}{link} (why: {it['why_queued']})")
        lines.append("")
    quiet = [r for r in order if r["netuid"] not in by_nid]
    lines.append("## Not queued (spot check)")
    lines.append("")
    if quiet:
        for r in quiet:
            lines.append(f"- SN{r['netuid']} {r['name']} composite {comp_of(r)}")
    else:
        lines.append("- every subnet has at least one queued cell")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def slice_report(rows):
    per = {}
    for r in rows:
        _, scores = cells_of(r)
        comp = composite_score(scores)[0]
        if comp is not None:
            per.setdefault(r.get("slice") or "?", []).append(comp)
    if not per:
        return
    means = {s: statistics.mean(v) for s, v in per.items()}
    grand = statistics.mean(means.values())
    for s, vals in sorted(per.items()):
        sd = statistics.pstdev(vals) if len(vals) > 1 else 0.0
        flag = "  <-- deviates by more than 0.7 from the other slices" if abs(means[s] - grand) > 0.7 else ""
        print(f"  slice {s}: n={len(vals)} mean={means[s]:.2f} sd={sd:.2f}{flag}", file=sys.stderr)


# ---------------- apply
def apply_decisions(rows):
    p = sorted(DATA.glob("review-*.csv"))
    if not p:
        raise SystemExit("no data/review-*.csv to apply; run without --apply first")
    decisions = load_csv(p[-1], REVIEW_COLUMNS)
    print(f"applying {p[-1].name}", file=sys.stderr)
    by_nid = {r["netuid"]: r for r in rows}
    queued_nids = {d["netuid"] for d in decisions}
    changes, rechecks, kept = 0, [], {}

    def change(row, a, q, old, new, note):
        if old is not None and str(old.get("score")) == str(new):
            return False
        stamp(row, f"reviewed by MC {TODAY}: {a}.{q} {old['score'] if old else '?'}->{new} ({clean_note(note)})")
        set_verified(row)
        return True

    for (nid, a, q), (score, reason) in MANUAL.items():
        row = by_nid.get(str(nid))
        if not row:
            print(f"  MANUAL SN{nid}: not in scores.csv", file=sys.stderr)
            continue
        old = edit_entry(row, a, q, score=score)
        if change(row, a, q, old, score, "MANUAL: " + reason):
            changes += 1

    for d in decisions:
        dec = d["decision"].strip().lower()
        if not dec:
            continue
        row = by_nid.get(d["netuid"])
        if not row:
            print(f"  SN{d['netuid']}: not in scores.csv", file=sys.stderr)
            continue
        a, q, rnote = d["audience"], d["q"], d["reviewer_note"].strip()
        if dec == "recheck":
            rechecks.append(f"- SN{d['netuid']} {a}{'.' + q if q else ''}: {rnote or d['why_queued']}")
            kept.setdefault(d["netuid"], 0)
            continue
        if a not in AUDIENCES or q not in QUESTIONS:
            if dec != "keep":
                print(f"  SN{d['netuid']} {a}.{q}: decision {dec!r} only applies to evidence cells", file=sys.stderr)
            kept.setdefault(d["netuid"], 0)
            kept[d["netuid"]] += 1
            continue
        cur = edit_entry(row, a, q)  # read without changing
        note_changed = cur is not None and d["note"].strip() and d["note"].strip() != cur["note"].strip()
        new_note = None
        if note_changed:
            n = clean_note(d["note"])
            new_note = n if n.startswith("MC: ") else "MC: " + n
        if dec == "keep":
            if new_note is not None:
                edit_entry(row, a, q, note=new_note)
                stamp(row, f"reviewed by MC {TODAY}: {a}.{q} note edited")
                set_verified(row)
                changes += 1
            kept.setdefault(d["netuid"], 0)
            kept[d["netuid"]] += 1
        elif dec.startswith("set:"):
            try:
                n = int(dec[4:])
                assert 0 <= n <= 5
            except (ValueError, AssertionError):
                print(f"  SN{d['netuid']} {a}.{q}: bad decision {dec!r}", file=sys.stderr)
                continue
            kw = {"score": n}
            if rnote.lower().startswith("verified"):
                kw["status"] = "verified"
            if new_note is not None:
                kw["note"] = new_note
            old = edit_entry(row, a, q, **kw)
            if change(row, a, q, old, n, rnote or "set by reviewer"):
                changes += 1
        elif dec == "unknown->0":
            old = edit_entry(row, a, q, score=0, status="inferred", note=f"nothing found by hand {TODAY}")
            if change(row, a, q, old, 0, rnote or "nothing found by hand"):
                changes += 1
        else:
            print(f"  SN{d['netuid']} {a}.{q}: unrecognised decision {dec!r}", file=sys.stderr)

    for nid, n in kept.items():
        row = by_nid[nid]
        if "reviewed by MC" not in row.get("claim_labels", ""):
            stamp(row, f"reviewed by MC {TODAY}: {n} queued cells kept")
            set_verified(row)
    for row in rows:
        if row["netuid"] not in queued_nids:
            stamp(row, f"spot-checked MC {TODAY}")
            set_verified(row)
        for w in recompute(row):
            if "malformed" in w or "missing" in w:
                print(f"  SN{row['netuid']}: {w}", file=sys.stderr)
    if rechecks:
        AGENTS.mkdir(parents=True, exist_ok=True)
        out = AGENTS / f"recheck-{TODAY}.md"
        out.write_text("\n".join([f"# Recheck {TODAY}", "", "Cells the reviewer could not settle. Fetch, quote, and rescore each one.", ""] + rechecks) + "\n", encoding="utf-8")
        print(f"  {len(rechecks)} rechecks in {out.relative_to(AGENTS.parent)}", file=sys.stderr)
    print(f"  {changes} cells changed, {len(kept)} subnets with kept cells, {len(rows) - len(queued_nids)} spot-checked", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="apply decisions from the newest data/review-*.csv")
    ap.add_argument("--all", action="store_true", help="queue every cell")
    a = ap.parse_args()

    rows = load_csv(DATA / "scores.csv")
    if a.apply:
        apply_decisions(rows)
        write_csv(DATA / "scores.csv", rows)
        print("wrote data/scores.csv", file=sys.stderr)
        return

    links, verify_name = link_results()
    queue = build_queue(rows, links, a.all)
    write_csv(DATA / f"review-{TODAY}.csv", queue, REVIEW_COLUMNS)
    write_markdown(rows, queue, DATA / f"review-{TODAY}.md", verify_name)
    nids = {q["netuid"] for q in queue}
    print(f"queued {len(queue)} cells across {len(nids)} of {len(rows)} subnets "
          f"-> data/review-{TODAY}.csv and .md", file=sys.stderr)
    slice_report(rows)


if __name__ == "__main__":
    main()
