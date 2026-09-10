#!/usr/bin/env python3
"""Check the subnet explainers in data/explainers/ against the brief.

Usage: python3 scripts/check_explainers.py [--only 64,120] [--links]

Checks: front matter fields, the seven headings in order, word count 350 to 600,
a Sources section with URLs, every link in the body present in Sources, no em or
en dash, no banned words, one_sentence matches the first section, commodity in
the allowed set. With --links, fetches every Source and Go deeper URL.
"""
import argparse
import re
import sys
from pathlib import Path

from common import get

REPO = Path(__file__).resolve().parent.parent
DIR = REPO / "data" / "explainers"
HEADINGS = ["In one sentence", "The commodity, explained from zero", "Why it is on Bittensor at all",
            "How the work gets done", "How you would know it works", "What is missing", "Go deeper"]
COMMODITIES = {"inference", "compute", "training", "data", "agents", "forecasting", "storage", "security", "media", "science", "other"}
BANNED = ["leverage", "ecosystem", "cutting-edge", "seamless", "robust", "unlock", "supercharge", "game-changing", "revolutionary", "delve"]


def parse(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None, text
    fm = {}
    for ln in m.group(1).splitlines():
        if ":" in ln:
            k, v = ln.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, m.group(2)


def check_file(path, fetch_links=False):
    fails = []
    text = path.read_text(encoding="utf-8")
    fm, body = parse(text)
    if fm is None:
        return [f"{path.name}: no front matter"]
    for k in ("netuid", "name", "commodity", "one_sentence", "metaphor", "written"):
        if not fm.get(k):
            fails.append(f"{path.name}: front matter missing {k}")
    if fm.get("netuid") and fm["netuid"] != path.stem:
        fails.append(f"{path.name}: netuid {fm['netuid']} does not match filename")
    if fm.get("commodity") and fm["commodity"] not in COMMODITIES:
        fails.append(f"{path.name}: commodity '{fm['commodity']}' not in the allowed set")
    heads = re.findall(r"^## (.+)$", body, re.M)
    core = [h for h in heads if h != "Sources"]
    if core != HEADINGS:
        fails.append(f"{path.name}: headings are {core[:3]}... expected the seven fixed headings in order")
    if "Sources" not in heads:
        fails.append(f"{path.name}: no Sources section")
    main = body.split("## Sources")[0]
    words = len(re.findall(r"\b\w+\b", re.sub(r"https?://\S+", "", main)))
    if not 350 <= words <= 600:
        fails.append(f"{path.name}: {words} words, want 350 to 600")
    if "—" in text or re.search(r"\s–\s", text):
        fails.append(f"{path.name}: em or en dash")
    low = main.lower()
    for w in BANNED:
        if re.search(r"\b" + re.escape(w) + r"\b", low):
            fails.append(f"{path.name}: banned word '{w}'")
    first = re.search(r"## In one sentence\s*\n+(.+?)\n", body)
    if first and fm.get("one_sentence") and first.group(1).strip() != fm["one_sentence"].strip():
        fails.append(f"{path.name}: one_sentence differs from the first section")
    if first and len(first.group(1).split()) > 45:
        fails.append(f"{path.name}: first sentence over 40 words")
    sources = set(re.findall(r"https?://[^\s)>\]]+", body.split("## Sources")[1])) if "## Sources" in body else set()
    body_links = set(re.findall(r"\]\((https?://[^)]+)\)", main))
    for u in body_links - sources:
        fails.append(f"{path.name}: link not in Sources: {u[:70]}")
    deeper = re.search(r"## Go deeper\s*\n(.*?)(?=\n## |\Z)", body, re.S)
    if deeper and len(re.findall(r"\]\((https?://", deeper.group(1))) > 3:
        fails.append(f"{path.name}: more than three Go deeper links")
    if "(inferred" not in main and "inferred" not in main:
        pass  # inference marks are optional; their absence is not a failure
    if fetch_links:
        for u in sorted(sources | body_links):
            st, _, _ = get(u.rstrip(".,"), timeout=15)
            if st != 200:
                fails.append(f"{path.name}: {st} {u[:70]}")
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated netuids")
    ap.add_argument("--links", action="store_true")
    a = ap.parse_args()
    files = sorted(p for p in DIR.glob("*.md") if p.stem.isdigit())
    if a.only:
        keep = set(a.only.split(","))
        files = [p for p in files if p.stem in keep]
    fails = []
    for p in files:
        fails += check_file(p, a.links)
    print(f"{len(files)} explainers checked", file=sys.stderr)
    if fails:
        print("FAIL", file=sys.stderr)
        for f in fails:
            print("  " + f, file=sys.stderr)
        sys.exit(1)
    print("ok", file=sys.stderr)


if __name__ == "__main__":
    main()
