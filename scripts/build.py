#!/usr/bin/env python3
"""Assemble data/index.json, the public dataset, from the snapshot and the reviewed scores.

Usage: python3 scripts/build.py [--chain data/chain-YYYY-MM-DD.json]
                                [--allow-unknown] [--allow-unreviewed] [--allow-unreachable]

Inputs: the named or newest data/chain-*.json, data/scores.csv, data/corrections.csv
(optional), the "Version:" line of rubric.md, and the newest data/verify-*.csv (optional).
Outputs: data/index.json in the shape of scripts/fixtures/sample.json, data/index.md
(a readable ranking plus one section per subnet), and data/CHANGELOG.md (applied
corrections, newest first).

Publication gate, checked before anything is written. The build exits 1 and lists
the offenders when: a cell is unknown, malformed, or missing (--allow-unknown skips);
a row carries neither a "reviewed by" nor a "spot-checked" stamp (--allow-unreviewed);
a verified entry's link is unreachable (--allow-unreachable); or the Taostats key name
or value, or anything that looks like an API key, appears under data/ or agents/
(never skipped).
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from common import (AGENTS, ARTIFACT_KEYS, AUDIENCES, DATA, IDENTITY_FIELDS, Q_LABELS, QUESTIONS, REPO,
                    audience_score, composite_score, latest, load_csv, parse_evidence, parse_pairs, read_env)
from verify_links import VERIFY_COLUMNS, norm_url

PUBLISHED_AT = "2026-09-21"
KEY_NAME = "TAOSTATS_API_KEY"
KEY_SHAPE = re.compile(r"(?i)(api[_-]?key|secret|token|authorization|bearer)\W{0,6}[A-Za-z0-9_\-]{32,}")
CORRECTION_COLUMNS = ["date", "netuid", "audience", "q", "old_score", "new_score", "new_status", "url", "note",
                      "requested_by", "reason", "applied"]


# ---------------- inputs
def rubric_version():
    for line in (REPO / "rubric.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*Version:\s*([0-9][0-9.]*)", line)
        if m:
            return m.group(1)
    raise SystemExit("rubric.md has no 'Version:' line")


def load_snapshot(path):
    p = Path(path) if path else latest("chain-*.json")
    if not p or not p.exists():
        raise SystemExit("no chain snapshot; run pull_chain.py first")
    snap = json.loads(p.read_text(encoding="utf-8"))
    m = re.search(r"chain-(\d{4}-\d{2}-\d{2})", p.name)
    snap["_date"] = m.group(1) if m else (snap.get("pulled_at") or "")[:10]
    snap["_file"] = p.name
    return snap


def load_links():
    p = latest("verify-*.csv")
    if not p:
        return {}
    return {norm_url(r["url"]): r["result"] for r in load_csv(p, VERIFY_COLUMNS)}


def load_corrections():
    p = DATA / "corrections.csv"
    if not p.exists():
        return []
    rows = [c for c in load_csv(p, CORRECTION_COLUMNS) if c["applied"].strip()]
    return sorted(rows, key=lambda c: (c["date"], c["applied"]), reverse=True)


# ---------------- per-subnet assembly
def parse_identity_check(text):
    out = []
    for parts in parse_pairs(text):
        field = parts[0].lower()
        value = parts[1] if len(parts) > 1 else ""
        if value.lower() in ("none", "n/a", "-"):
            value = ""
        result = parts[2].lower() if len(parts) > 2 else ""
        note = " | ".join(parts[3:]).strip()
        if note.lower() == "not set" and not value:
            result = result or "none"
        out.append({"field": field, "value": value, "result": result, "note": note})
    return out


def parse_artifacts(text):
    art = {k: None for k in ARTIFACT_KEYS}
    for parts in parse_pairs(text):
        k = parts[0].lower()
        if k not in art or len(parts) < 2:
            continue
        v = parts[1].strip()
        art[k] = None if v.lower() in ("none", "n/a", "-", "") else v
    return art


def parse_own_words(text):
    quote, sep, url = (text or "").rpartition(" | ")
    if not sep:
        quote, url = text or "", ""
    return {"quote": quote.strip().strip('"').strip(), "url": norm_url(url)}


def build_audiences(row, links, problems, nid):
    auds = {}
    for a in AUDIENCES:
        parsed = parse_evidence(row.get(f"{a}_evidence", ""))
        by_q = {}
        for e in parsed["entries"]:
            if e["q"] in QUESTIONS and e["q"] not in by_q:
                by_q[e["q"]] = e
            elif e["q"] not in QUESTIONS:
                problems["unknown"].append(f"SN{nid} {a}: malformed entry {e['note'][:50]!r}")
        cells = []
        for q in QUESTIONS:
            e = by_q.get(q)
            if e is None:
                problems["unknown"].append(f"SN{nid} {a}.{q}: missing")
                cells.append({"q": q, "label": Q_LABELS[q], "score": None, "status": "unknown", "url": "",
                              "note": "missing", "link": "unchecked"})
                continue
            url = norm_url(e["url"])
            link = links.get(url, "unchecked") if url else "unchecked"
            if e["status"] in ("unknown", "malformed"):
                problems["unknown"].append(f"SN{nid} {a}.{q}: {e['status']}")
            if e["status"] == "verified" and link == "unreachable":
                problems["unreachable"].append(f"SN{nid} {a}.{q}: verified but {url} unreachable")
            cells.append({"q": q, "label": Q_LABELS[q], "score": e["score"], "status": e["status"], "url": url,
                          "note": e["note"], "link": link})
        score, partial, _ = audience_score(parsed)
        auds[a] = {"score": score, "rank": None, "partial": partial, "cells": cells}
    return auds


def build_subnet(s, row, links, corrections, problems):
    nid = s["netuid"]
    share = float(s.get("emission_share") or 0.0)
    ident = s.get("identity") or {}
    identity = {f: (ident.get(f) or "") for f in IDENTITY_FIELDS}
    comp_block = s.get("identity_completeness") or {
        "filled": sum(1 for f in IDENTITY_FIELDS if identity[f]), "of": len(IDENTITY_FIELDS),
        "missing": [f for f in IDENTITY_FIELDS if not identity[f]]}
    artifacts = parse_artifacts(row.get("artifacts", ""))
    auds = build_audiences(row, links, problems, nid)
    composite, partial = composite_score({a: auds[a]["score"] for a in AUDIENCES})
    labels = row.get("claim_labels", "")
    if "reviewed by" not in labels and "spot-checked" not in labels:
        problems["unreviewed"].append(f"SN{nid} {row['name']}: no review or spot-check stamp")
    return {
        "netuid": nid, "name": s.get("name") or row["name"], "rank": s.get("rank"),
        "emission_share": share, "emission_pct": f"{share * 100:.1f}%",
        "active_miners": s.get("active_miners"), "active_validators": s.get("active_validators"),
        "registration_cost_tao": s.get("registration_cost_tao"), "alpha_price_tao": s.get("alpha_price_tao"),
        "owner": s.get("owner"),
        "identity": identity,
        "identity_completeness": {"filled": comp_block.get("filled", 0), "of": comp_block.get("of", 7),
                                  "missing": comp_block.get("missing", [])},
        "identity_check": parse_identity_check(row.get("identity_check", "")),
        "artifacts": artifacts,
        "flags": {"has_docs": artifacts["docs"] is not None, "has_paper": artifacts["whitepaper"] is not None},
        "own_words": parse_own_words(row.get("own_words", "")),
        "audiences": auds,
        "composite": composite, "composite_rank": None, "partial": partial,
        "corrections": [{"date": c["date"], "audience": c["audience"], "q": c["q"], "old": c["old_score"],
                         "new": c["new_score"], "reason": c["reason"], "requested_by": c["requested_by"]}
                        for c in corrections if c["netuid"].strip() == str(nid)],
        "claim_labels": labels, "last_verified": row.get("last_verified", ""), "notes": row.get("notes", ""),
    }


def rank(subnets):
    """Shared ranks on ties, like make_fixture.rank; unscored subnets get null."""
    for key in ["composite"] + AUDIENCES:
        def val(s):
            return s["composite"] if key == "composite" else s["audiences"][key]["score"]
        scored = sorted([s for s in subnets if val(s) is not None], key=lambda s: -val(s))
        r, prev = 0, None
        for i, s in enumerate(scored):
            if val(s) != prev:
                r, prev = i + 1, val(s)
            if key == "composite":
                s["composite_rank"] = r
            else:
                s["audiences"][key]["rank"] = r


# ---------------- gate
def key_leak():
    read_env()
    value = os.environ.get(KEY_NAME, "").strip()
    hits = []
    for root in (DATA, AGENTS):
        if not root.exists():
            continue
        for p in sorted(root.rglob("*")):
            if not p.is_file() or p.suffix.lower() in (".png", ".jpg", ".gif", ".ttf", ".woff", ".woff2"):
                continue
            try:
                text = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            rel = p.relative_to(REPO)
            if KEY_NAME in text:
                hits.append(f"{rel}: contains {KEY_NAME}")
            if value and len(value) >= 8 and value in text:
                hits.append(f"{rel}: contains the {KEY_NAME} value")
            m = KEY_SHAPE.search(text)
            if m:
                hits.append(f"{rel}: '{m.group(0)[:20]}...' looks like an API key")
    return hits


# ---------------- outputs
def band(v):
    if v is None:
        return "unscored"
    return ["sparse", "thin", "partial", "workable", "clear", "exemplary"][min(5, int(v + 0.5))]


def fmt(v):
    return "n/a" if v is None else f"{v:.1f}"


def write_index_md(data, path):
    subs = data["subnets"]
    L = [f"# Subnet Legibility Index, rubric v{data['rubric_version']}", "",
         f"Chain snapshot {data['chain_snapshot']}, scores as of {data['scores_date']}, generated {data['generated_at']}.",
         f"{len(subs)} subnets of {data['total_subnets']}. Mean composite {data['summary']['mean_composite']}.", "",
         "| # | SN | Name | Emission | Composite | Stakers | Miners | Buyers | Newcomers | Identity |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for s in sorted(subs, key=lambda x: (x["composite_rank"] is None, x["composite_rank"] or 0, x["rank"] or 0)):
        L.append(f"| {s['composite_rank'] or '-'} | {s['netuid']} | {s['name']} | {s['emission_pct']} | {fmt(s['composite'])} | "
                 + " | ".join(fmt(s["audiences"][a]["score"]) for a in AUDIENCES)
                 + f" | {s['identity_completeness']['filled']}/{s['identity_completeness']['of']} |")
    L.append("")
    for s in sorted(subs, key=lambda x: x["rank"] or 999):
        L += [f"## SN{s['netuid']} {s['name']}", "",
              f"Emission rank {s['rank']} ({s['emission_pct']}), composite {fmt(s['composite'])} ({band(s['composite'])}), "
              f"composite rank {s['composite_rank'] or '-'}, identity {s['identity_completeness']['filled']} of {s['identity_completeness']['of']}.",
              ""]
        ow = s["own_words"]
        if ow["quote"]:
            L.append(f"> {ow['quote']}" + (f" ({ow['url']})" if ow["url"] else ""))
            L.append("")
        arts = ", ".join(f"{k}: {v}" for k, v in s["artifacts"].items() if v) or "none recorded"
        L += [f"Artifacts: {arts}", "",
              "| Audience | " + " | ".join(f"{q} {Q_LABELS[q]}" for q in QUESTIONS) + " | Score |",
              "|---|---|---|---|---|---|"]
        for a in AUDIENCES:
            cells = []
            for c in s["audiences"][a]["cells"]:
                sc = "?" if c["score"] is None else c["score"]
                cells.append(f"{sc} {c['status']}" + (f" {c['url']}" if c["url"] else "") + (f" [{c['link']}]" if c["link"] != "unchecked" else ""))
            L.append(f"| {a} | " + " | ".join(cells) + f" | {fmt(s['audiences'][a]['score'])} |")
        if s["corrections"]:
            L += ["", "Corrections: " + "; ".join(f"{c['date']} {c['audience']}.{c['q']} {c['old']}->{c['new']} ({c['requested_by']})" for c in s["corrections"])]
        if s["notes"]:
            L += ["", s["notes"]]
        L += ["", f"Provenance: {s['claim_labels']}", ""]
    path.write_text("\n".join(L), encoding="utf-8")


def write_changelog(data, path):
    L = ["# Changelog", "",
         f"Corrections applied to the Subnet Legibility Index, newest first. Rubric v{data['rubric_version']}.", ""]
    rows = [c for c in data["changelog"] if c["kind"] == "correction"]
    if not rows:
        L.append("No corrections yet.")
    else:
        L += ["| Date | Subnet | Cell | Old | New | Reason | Requested by |", "|---|---|---|---|---|---|---|"]
        for c in rows:
            L.append(f"| {c['date']} | SN{c['netuid']} {c['name']} | {c['audience']}.{c['q']} | {c['old']} | {c['new']} | "
                     f"{c['reason'].replace('|', '/')} | {c['requested_by']} |")
    L.append("")
    path.write_text("\n".join(L), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chain", help="snapshot to build from (default: newest data/chain-*.json)")
    ap.add_argument("--allow-unknown", action="store_true")
    ap.add_argument("--allow-unreviewed", action="store_true")
    ap.add_argument("--allow-unreachable", action="store_true")
    a = ap.parse_args()

    snap = load_snapshot(a.chain)
    rows = {r["netuid"]: r for r in load_csv(DATA / "scores.csv")}
    links = load_links()
    corrections = load_corrections()
    version = rubric_version()
    problems = {"unknown": [], "unreviewed": [], "unreachable": []}

    subnets = []
    for s in sorted(snap["subnets"], key=lambda x: x.get("rank") or 999):
        row = rows.get(str(s["netuid"]))
        if not row:
            problems["unknown"].append(f"SN{s['netuid']} {s.get('name')}: no row in scores.csv")
            continue
        subnets.append(build_subnet(s, row, links, corrections, problems))
    rank(subnets)

    leaks = key_leak()
    failed = False
    for kind, allowed in (("unknown", a.allow_unknown), ("unreviewed", a.allow_unreviewed), ("unreachable", a.allow_unreachable)):
        if problems[kind]:
            flag = "allowed by flag" if allowed else "blocking"
            print(f"gate {kind}: {len(problems[kind])} ({flag})", file=sys.stderr)
            for x in problems[kind][:40]:
                print("   ", x, file=sys.stderr)
            if len(problems[kind]) > 40:
                print(f"    ... {len(problems[kind]) - 40} more", file=sys.stderr)
            failed = failed or not allowed
    if leaks:
        print(f"gate key: {len(leaks)} hits (blocking, no override)", file=sys.stderr)
        for x in leaks:
            print("   ", x, file=sys.stderr)
        failed = True
    if failed:
        print("build refused; nothing written", file=sys.stderr)
        sys.exit(1)

    scored = [s for s in subnets if s["composite"] is not None]
    by_nid = {s["netuid"]: s for s in subnets}
    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rubric_version": version,
        "chain_snapshot": snap["_date"],
        "scores_date": max([r.get("last_verified", "") for r in rows.values()] + [""]),
        "published_at": PUBLISHED_AT,
        "total_subnets": snap.get("total_subnets", 128),
        "weights": {x: 1 for x in AUDIENCES},
        "question_labels": dict(Q_LABELS),
        "summary": {
            "mean_composite": round(sum(s["composite"] for s in scored) / len(scored), 2) if scored else None,
            "audience_means": {
                x: (round(sum(s["audiences"][x]["score"] for s in subnets if s["audiences"][x]["score"] is not None)
                          / max(1, sum(1 for s in subnets if s["audiences"][x]["score"] is not None)), 2)
                    if any(s["audiences"][x]["score"] is not None for s in subnets) else None)
                for x in AUDIENCES},
            "identity_full": sum(1 for s in subnets if s["identity_completeness"]["filled"] == s["identity_completeness"]["of"]),
            "identity_empty": sum(1 for s in subnets if s["identity_completeness"]["filled"] == 0),
        },
        "subnets": subnets,
        "changelog": [{"date": c["date"], "kind": "correction", "netuid": int(c["netuid"]) if c["netuid"].strip().isdigit() else None,
                       "name": by_nid.get(int(c["netuid"]), {}).get("name", "") if c["netuid"].strip().isdigit() else "",
                       "audience": c["audience"], "q": c["q"], "old": c["old_score"], "new": c["new_score"],
                       "reason": c["reason"], "requested_by": c["requested_by"]} for c in corrections],
    }
    tokens_path = latest("tokens-*.json")
    if tokens_path:
        tok = json.loads(tokens_path.read_text(encoding="utf-8"))
        data["tao_usd"] = tok.get("tao_usd")
        data["tokens_snapshot"] = tokens_path.name.replace("tokens-", "").replace(".json", "")
        for s in data["subnets"]:
            s["alpha"] = tok["tokens"].get(str(s["netuid"]))
    else:
        data["tao_usd"] = None
        data["tokens_snapshot"] = None
        for s in data["subnets"]:
            s["alpha"] = None
    vpath = DATA / "verdicts.csv"
    if vpath.exists():
        import csv as _csv
        with vpath.open(newline="", encoding="utf-8") as fh:
            verdicts = {r["netuid"].strip(): {k: (r.get(k) or "").strip() for k in ("stakers", "miners", "buyers", "newcomers", "summary")} for r in _csv.DictReader(fh)}
        for sub in data["subnets"]:
            sub["verdict"] = verdicts.get(str(sub["netuid"]))
        missing_v = [s["netuid"] for s in data["subnets"] if not (s.get("verdict") or {}).get("summary")]
        if missing_v:
            print(f"  verdicts missing for {len(missing_v)} subnets: {missing_v[:8]}", file=sys.stderr)
    (DATA / "index.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    write_index_md(data, DATA / "index.md")
    write_changelog(data, DATA / "CHANGELOG.md")
    print(f"wrote data/index.json ({len(subnets)} subnets from {snap['_file']}, {len(links)} links, "
          f"{len(corrections)} corrections), data/index.md, data/CHANGELOG.md", file=sys.stderr)


if __name__ == "__main__":
    main()
