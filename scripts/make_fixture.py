#!/usr/bin/env python3
"""Write scripts/fixtures/sample.json: 32 fabricated subnets under the index.json contract.

For building and testing the site before real scores exist. Every name is
obviously fake and every URL points at example.com so nothing can be mistaken
for a result.
"""
import json
import random
from pathlib import Path

from common import AUDIENCES, IDENTITY_FIELDS, Q_LABELS, QUESTIONS

REPO = Path(__file__).resolve().parent.parent
random.seed(7)

WORDS = ["Cinder", "Harbor", "Quill", "Basalt", "Lantern", "Moss", "Tallow", "Gable", "Orrery", "Sable", "Fennel", "Kestrel",
         "Umber", "Vellum", "Wicket", "Alder", "Brine", "Cobble", "Dune", "Ember", "Flint", "Gorse", "Heath", "Ingot",
         "Juniper", "Kiln", "Loam", "Marl", "Nettle", "Ochre", "Pewter", "Reed"]
CATS = ["inference", "GPU compute", "model checkpoints", "forecasts", "datasets", "agents", "search", "storage"]


def subnet(i):
    name = f"{WORDS[i]} (fixture)"
    netuid = [64, 120, 3, 44, 75, 1, 9, 13, 18, 19, 21, 22, 27, 30, 34, 36, 39, 41, 43, 45, 47, 51, 52, 56, 59, 61, 68, 72, 81, 85, 90, 96][i]
    share = round(0.09 * (0.87 ** i) + random.uniform(0, 0.002), 5)
    filled = random.choice([7, 7, 6, 5, 4, 3, 2, 0])
    ident = {f: (f"https://example.com/{netuid}/{f}" if f in ("github_repo", "subnet_url", "discord") else f"{name} {f}") for f in IDENTITY_FIELDS}
    for f in IDENTITY_FIELDS[filled:]:
        ident[f] = ""
    auds = {}
    for a in AUDIENCES:
        base = random.uniform(0.5, 4.8)
        cells = []
        for q in QUESTIONS:
            sc = max(0, min(5, round(base + random.uniform(-1.2, 1.2))))
            cells.append({"q": q, "label": Q_LABELS[q], "score": sc,
                          "status": random.choice(["verified", "verified", "verified", "inferred"]),
                          "url": f"https://example.com/{netuid}/{a}/{q}",
                          "note": f'"{name} {a} {q} fixture evidence, not a real quote"',
                          "link": random.choice(["live", "live", "live", "redirected", "manual"])})
        score = round(sum(c["score"] for c in cells) / 4, 1)
        auds[a] = {"score": score, "rank": 0, "partial": False, "cells": cells}
    comp = round(sum(v["score"] for v in auds.values()) / 4, 1)
    return {
        "netuid": netuid, "name": name, "rank": i + 1, "emission_share": share, "emission_pct": f"{share * 100:.1f}%",
        "active_miners": random.randint(20, 250), "active_validators": random.randint(8, 64),
        "registration_cost_tao": round(random.uniform(0.0005, 2.5), 4), "alpha_price_tao": round(random.uniform(0.001, 0.1), 5),
        "owner": "5Fixture" + "x" * 40,
        "identity": ident, "identity_completeness": {"filled": filled, "of": 7, "missing": IDENTITY_FIELDS[filled:]},
        "identity_check": [{"field": f, "value": ident[f], "result": "resolves" if ident[f] else "none", "note": ""} for f in IDENTITY_FIELDS],
        "artifacts": {"github": ident["github_repo"] or None, "docs": f"https://example.com/{netuid}/docs" if filled > 3 else None,
                      "whitepaper": f"https://example.com/{netuid}/paper.pdf" if filled > 5 else None, "x": None,
                      "discord": ident["discord"] or None, "api": None, "dashboard": None},
        "flags": {"has_docs": filled > 3, "has_paper": filled > 5},
        "own_words": {"quote": f"{name} is a fixture subnet producing {random.choice(CATS)}.", "url": f"https://example.com/{netuid}"},
        "audiences": auds, "composite": comp, "composite_rank": 0, "partial": False,
        "corrections": [],
        "claim_labels": f"scored by agent {'abcd'[i % 4]} 2026-09-14, rubric v1.0; merged 2026-09-15; reviewed by MC 2026-09-16",
        "last_verified": "2026-09-16", "notes": "Fixture row. Not a real subnet score.",
    }


def rank(subnets):
    for key in ["composite"] + AUDIENCES:
        vals = sorted(subnets, key=lambda s: -(s["composite"] if key == "composite" else s["audiences"][key]["score"]))
        r, prev = 0, None
        for i, s in enumerate(vals):
            v = s["composite"] if key == "composite" else s["audiences"][key]["score"]
            if v != prev:
                r, prev = i + 1, v
            if key == "composite":
                s["composite_rank"] = r
            else:
                s["audiences"][key]["rank"] = r


def main():
    subs = [subnet(i) for i in range(32)]
    rank(subs)
    data = {
        "generated_at": "2026-09-16T00:00:00+00:00", "rubric_version": "1.0", "chain_snapshot": "2026-09-09",
        "scores_date": "2026-09-16", "published_at": "2026-09-21", "total_subnets": 128,
        "weights": {a: 1 for a in AUDIENCES}, "question_labels": Q_LABELS,
        "summary": {"mean_composite": round(sum(s["composite"] for s in subs) / 32, 2),
                    "audience_means": {a: round(sum(s["audiences"][a]["score"] for s in subs) / 32, 2) for a in AUDIENCES},
                    "identity_full": sum(1 for s in subs if s["identity_completeness"]["filled"] == 7),
                    "identity_empty": sum(1 for s in subs if s["identity_completeness"]["filled"] == 0)},
        "subnets": subs,
        "changelog": [{"date": "2026-09-16", "kind": "note", "netuid": None, "name": "", "audience": "", "q": "", "old": "", "new": "",
                       "reason": "Fixture dataset for site development.", "requested_by": "self"}],
    }
    out = REPO / "scripts" / "fixtures" / "sample.json"
    out.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {out.relative_to(REPO)}: {len(subs)} subnets")


if __name__ == "__main__":
    main()
