#!/usr/bin/env python3
"""Read-only checks on the built site. Exit 1 on any failure.

Usage: python3 scripts/check_site.py [--data data/index.json]
"""
import argparse
import json
import re
import struct
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = "https://www.legible.network"


def png_size(path):
    with path.open("rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/index.json")
    a = ap.parse_args()
    fails = []
    data_path = REPO / a.data
    if not data_path.exists():
        print(f"no data at {a.data}; checking static pages only", file=sys.stderr)
        data = None
    else:
        data = json.loads(data_path.read_text(encoding="utf-8"))

    rubric_md = (REPO / "rubric.md").read_text(encoding="utf-8")
    md_ver = next((ln.split(":", 1)[1].strip() for ln in rubric_md.splitlines() if ln.startswith("Version:")), None)
    rubric_page = (REPO / "rubric" / "index.html").read_text(encoding="utf-8") if (REPO / "rubric" / "index.html").exists() else ""
    if not rubric_page:
        fails.append("rubric/index.html missing")
    elif f"version: {md_ver}" not in rubric_page.lower() and f"rubric v{md_ver}" not in rubric_page.lower():
        fails.append(f"rubric page does not show version {md_ver}")
    if data and data.get("rubric_version") != md_ver:
        fails.append(f"index.json rubric_version {data.get('rubric_version')} != rubric.md {md_ver}")

    pages = ["index.html", "rubric/index.html", "methodology/index.html", "about/index.html", "404.html"]
    if data:
        pages += ["sn/index.html"] + [f"sn/{s['netuid']}/index.html" for s in data["subnets"]]
    for rel in pages:
        p = REPO / rel
        if not p.exists():
            fails.append(f"missing page {rel}")
            continue
        t = p.read_text(encoding="utf-8")
        if "{{" in t:
            fails.append(f"{rel}: unfilled template placeholder")
        if "mikyo.one/landscape" in t or "JOB-SEARCH" in t:
            fails.append(f"{rel}: leftover reference to the landscape project")
        for m in re.finditer(r'(?:property="og:image"|rel="canonical") (?:content|href)="([^"]+)"', t):
            if not m.group(1).startswith(SITE + "/"):
                fails.append(f"{rel}: non-absolute og/canonical url {m.group(1)}")
        if "topbar:start" in t and "class=\"topbar\"" not in t:
            fails.append(f"{rel}: topbar partial not injected")
        if rel.startswith("sn/") and rel != "sn/index.html" and t.count("<details") != 16:
            fails.append(f"{rel}: expected 16 evidence cells, found {t.count('<details')}")

    if data:
        for s in data["subnets"]:
            og = REPO / "assets" / "og" / f"{s['netuid']}.png"
            if not og.exists():
                fails.append(f"missing OG image for SN{s['netuid']}")
            elif png_size(og) != (1200, 630):
                fails.append(f"OG image for SN{s['netuid']} is {png_size(og)}, not 1200x630")
        default = REPO / "assets" / "og" / "default.png"
        if not default.exists() or png_size(default) != (1200, 630):
            fails.append("assets/og/default.png missing or wrong size")
        summary = REPO / "data" / "summary.json"
        if not summary.exists():
            fails.append("data/summary.json missing")
        else:
            sj = json.loads(summary.read_text(encoding="utf-8"))
            for s in sj.get("subnets", []):
                if "claim_labels" in s or "identity_check" in s:
                    fails.append(f"summary.json carries provenance for SN{s['netuid']}")
        sm = (REPO / "sitemap.xml").read_text(encoding="utf-8") if (REPO / "sitemap.xml").exists() else ""
        want = {f"{SITE}/sn/{s['netuid']}/" for s in data["subnets"]} | {f"{SITE}/", f"{SITE}/rubric/", f"{SITE}/methodology/", f"{SITE}/about/", f"{SITE}/sn/"}
        have = set(re.findall(r"<loc>([^<]+)</loc>", sm))
        if want != have:
            fails.append(f"sitemap mismatch: missing {sorted(want - have)[:3]} extra {sorted(have - want)[:3]}")
        for c in data.get("changelog", []):
            if not c.get("date") or not c.get("kind"):
                fails.append("changelog entry without date or kind")
        leak = re.compile(r"TAOSTATS_API_KEY=\S|[A-Za-z0-9_\-]{40,}")
        for p in list((REPO / "data").glob("*")) + list((REPO / "agents").rglob("*.md")):
            if p.is_file() and p.suffix in (".json", ".csv", ".md") and p.name != "index.json":
                for ln in p.read_text(encoding="utf-8", errors="ignore").splitlines():
                    if "TAOSTATS_API_KEY=" in ln and len(ln.split("=", 1)[1].strip()) > 0:
                        fails.append(f"{p.relative_to(REPO)}: API key literal")
                        break

    if fails:
        print("FAIL", file=sys.stderr)
        for f in fails:
            print("  " + f, file=sys.stderr)
        sys.exit(1)
    print(f"ok: {len(pages)} pages checked", file=sys.stderr)


if __name__ == "__main__":
    main()
