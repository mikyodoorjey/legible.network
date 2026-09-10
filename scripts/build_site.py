#!/usr/bin/env python3
"""Site build for legible.network.

Usage: python3 scripts/build_site.py [--data data/index.json] [--launch]

- Renders rubric.md, methodology.md, about.md into <page>/index.html with the doc template.
- Injects the shared topbar, nav, and footer partials into hand-written pages between
  <!-- topbar:start --> ... <!-- topbar:end --> style markers (anchored, early exit if unchanged).
- Writes sitemap.xml. Subnet pages, summary.json, OG images, and the chart are added by
  later steps in this file as the data pipeline lands.

No dependencies beyond the standard library.
"""
import argparse
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PARTIALS = REPO / "scripts" / "templates" / "partials"
SITE = "https://legible.network"
TODAY = date.today().isoformat()

DOCS = [  # (source markdown, output dir, nav key)
    ("rubric.md", "rubric", "rubric"),
    ("methodology.md", "methodology", "methodology"),
    ("about.md", "about", "about"),
]
HAND_PAGES = ["index.html", "404.html"]  # pages that carry partial markers


# ---------------- tiny markdown
def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\w)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+|/[^)]*|#[^)]*)\)", r'<a href="\2">\1</a>', s)
    return s


def render_table(lines, data_table=False):
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines if not re.match(r"^\s*\|?\s*-{3,}", ln)]
    if not rows:
        return ""
    head, body = rows[0], rows[1:]
    out = [f'<div class="table-wrap{" data-table" if data_table else ""}"><table><thead><tr>']
    out += [f"<th>{inline(c)}</th>" for c in head]
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def md_to_sections(md):
    """Parse a constrained Markdown subset. Returns (title, meta dict, [(id, h2, html)])."""
    lines = md.splitlines()
    title, meta, i = "", {}, 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("# ") and not title:
            title = ln[2:].strip()
        elif re.match(r"^[A-Z][A-Za-z ]+: .+$", ln) and not any(s.startswith("## ") for s in lines[:i]):
            k, v = ln.split(":", 1)
            meta[k.strip().lower().replace(" ", "_")] = v.strip()
        elif ln.startswith("## "):
            break
        i += 1
    sections, cur, buf = [], None, []

    def flush_buf():
        nonlocal buf
        out, j = [], 0
        while j < len(buf):
            ln = buf[j]
            if not ln.strip():
                j += 1
                continue
            if ln.startswith("### "):
                out.append(f"<h3>{inline(ln[4:].strip())}</h3>")
                j += 1
            elif ln.lstrip().startswith("|"):
                k = j
                while k < len(buf) and buf[k].lstrip().startswith("|"):
                    k += 1
                block = buf[j:k]
                out.append(render_table(block, data_table=(len(block[0].split("|")) > 5)))
                j = k
            elif re.match(r"^\s*[-*] ", ln):
                k = j
                items = []
                while k < len(buf) and re.match(r"^\s*[-*] ", buf[k]):
                    items.append(re.sub(r"^\s*[-*] ", "", buf[k]))
                    k += 1
                out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
                j = k
            elif re.match(r"^\s*\d+\. ", ln):
                k = j
                items = []
                while k < len(buf) and re.match(r"^\s*\d+\. ", buf[k]):
                    items.append(re.sub(r"^\s*\d+\. ", "", buf[k]))
                    k += 1
                out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
                j = k
            elif ln.startswith("```"):
                k = j + 1
                code = []
                while k < len(buf) and not buf[k].startswith("```"):
                    code.append(buf[k])
                    k += 1
                out.append("<pre>" + html.escape("\n".join(code)) + "</pre>")
                j = k + 1
            else:
                k = j
                para = []
                while k < len(buf) and buf[k].strip() and not re.match(r"^(### |\s*[-*] |\s*\d+\. |\||```)", buf[k]):
                    para.append(buf[k].strip())
                    k += 1
                out.append(f"<p>{inline(' '.join(para))}</p>")
                j = k
        buf = []
        return "".join(out)

    for ln in lines[i:]:
        if ln.startswith("## "):
            if cur is not None:
                sections.append((cur[0], cur[1], flush_buf()))
            h = ln[3:].strip()
            cur = (slug(h), h)
        else:
            buf.append(ln)
    if cur is not None:
        sections.append((cur[0], cur[1], flush_buf()))
    return title, meta, sections


# ---------------- partials and templates
def partial(name, ctx):
    t = (PARTIALS / f"{name}.html").read_text(encoding="utf-8")
    def sub(m):
        k = m.group(1)
        v = str(ctx.get(k, ""))
        return v if k.startswith("cur_") else html.escape(v)
    return re.sub(r"\{\{(\w+)\}\}", sub, t)


def nav_ctx(active, ctx):
    c = dict(ctx)
    for k in ("index", "rubric", "methodology", "about"):
        c[f"cur_{k}"] = ' aria-current="page"' if k == active else ""
    return c


def inject(page_html, name, body):
    start, end = f"<!-- {name}:start -->", f"<!-- {name}:end -->"
    if start not in page_html or end not in page_html:
        return page_html
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    return pat.sub(lambda m: f"{start}\n{body}\n{end}", page_html, count=1)


def doc_page(title, meta, sections, active, ctx, description):
    toc_ctx = nav_ctx(active, ctx)
    meta_pills = "".join(f'<span class="pill">{html.escape(k.replace("_", " "))}: {html.escape(v)}</span>' for k, v in meta.items())
    body = "".join(f'<section id="{sid}"><h2>{html.escape(h)}</h2>{content}</section>' for sid, h, content in sections)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · Subnet Legibility Index</title>
{ctx.get("robots", "")}
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{SITE}/{active}/">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}/{active}/">
<meta property="og:title" content="{html.escape(title)} · Subnet Legibility Index">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:image" content="{SITE}/assets/og/default.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@9..144,300..700,30..100,0..1&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/doc.css">
</head>
<body>
<div id="progress"></div>
{partial("topbar", toc_ctx)}
{partial("nav", toc_ctx)}
<main class="wrap doc">
  <nav class="toc" aria-label="Contents"><span class="mono">Contents</span></nav>
  <article class="prose">
    <span class="mono kicker">Subnet Legibility Index</span>
    <h1>{html.escape(title)}</h1>
    <div class="meta">{meta_pills}</div>
    {body}
  </article>
</main>
{partial("footer", toc_ctx)}
<script src="/assets/doc.js"></script>
</body>
</html>
"""


def write_if_changed(path, text):
    path = Path(path)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def rubric_version():
    for ln in (REPO / "rubric.md").read_text(encoding="utf-8").splitlines():
        if ln.startswith("Version:"):
            return ln.split(":", 1)[1].strip()
    return "unknown"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/index.json")
    ap.add_argument("--launch", action="store_true", help="drop pre-launch notes")
    a = ap.parse_args()

    data_path = REPO / a.data
    data = json.loads(data_path.read_text(encoding="utf-8")) if data_path.exists() else None
    ctx = {
        "robots": "" if a.launch else '<meta name="robots" content="noindex">',
        "snapshot": (data or {}).get("chain_snapshot", "pending"),
        "rubric_version": rubric_version(),
        "year": TODAY[:4],
        "site": SITE,
        "byline": "Built by Mikyö Clark",
    }
    changed = []
    descriptions = {
        "rubric": "How the Subnet Legibility Index scores what a first-time reader can find about a Bittensor subnet in five minutes.",
        "methodology": "Sources, scoring, evidence, corrections, and the changelog for the Subnet Legibility Index.",
        "about": "Who built the Subnet Legibility Index and why.",
    }
    for src, outdir, active in DOCS:
        p = REPO / src
        if not p.exists():
            print(f"  missing {src}, skipped", file=sys.stderr)
            continue
        title, meta, sections = md_to_sections(p.read_text(encoding="utf-8"))
        page = doc_page(title, meta, sections, active, ctx, descriptions.get(active, ""))
        if data and active == "methodology" and data.get("changelog") is not None:
            items = "".join(
                f'<li><span class="mono">{html.escape(c.get("date",""))} · {html.escape(c.get("kind",""))}</span> '
                f'{("<a href=/sn/" + str(c["netuid"]) + "/>SN" + str(c["netuid"]) + " " + html.escape(c.get("name","")) + "</a> ") if c.get("netuid") else ""}'
                f'{html.escape(c.get("audience",""))} {html.escape(c.get("q",""))}: {html.escape(str(c.get("old","")))} to {html.escape(str(c.get("new","")))}. {html.escape(c.get("reason",""))}'
                f'{(" Requested by " + html.escape(c["requested_by"]) + ".") if c.get("requested_by") else ""}</li>'
                for c in data["changelog"]) or "<li>No corrections yet.</li>"
            page = inject(page, "changelog", f"<ul>{items}</ul>")
        if write_if_changed(REPO / outdir / "index.html", page):
            changed.append(f"{outdir}/index.html")

    if data:
        summary = {k: v for k, v in data.items() if k != "subnets"}
        summary["subnets"] = []
        for sub in data["subnets"]:
            lite = {k: v for k, v in sub.items() if k not in ("audiences", "identity_check", "corrections", "claim_labels", "notes", "owner")}
            lite["audiences"] = {a: {"score": v["score"], "rank": v.get("rank"), "partial": v.get("partial", False),
                                     "cells": [{"q": c["q"], "score": c["score"]} for c in v["cells"]]}
                                 for a, v in sub["audiences"].items()}
            summary["subnets"].append(lite)
        if write_if_changed(REPO / "data" / "summary.json", json.dumps(summary, ensure_ascii=False, separators=(",", ":"))):
            changed.append("data/summary.json")

    for name in HAND_PAGES:
        p = REPO / name
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        active = "index" if name == "index.html" else ""
        c = nav_ctx(active, ctx)
        s2 = inject(inject(inject(s, "topbar", partial("topbar", c)), "nav", partial("nav", c)), "footer", partial("footer", c))
        s2 = inject(s2, "robots", ctx["robots"])
        if name == "index.html":
            s2 = re.sub(r"<body[^>]*>", f'<body data-snapshot="{html.escape(ctx["snapshot"])}">', s2, count=1)
        if s2 != s:
            p.write_text(s2, encoding="utf-8")
            changed.append(name)

    if data:
        from render_subnets import build_all
        parts = {k: partial(k, nav_ctx("", ctx)) for k in ("topbar", "nav", "footer")}
        parts["robots"] = ctx["robots"]
        sub_changed, chart_html = build_all(data, parts, SITE, write_if_changed)
        changed += sub_changed
        p = REPO / "index.html"
        s = p.read_text(encoding="utf-8")
        s2 = inject(s, "chart", chart_html)
        if s2 != s:
            p.write_text(s2, encoding="utf-8")
            changed.append("index.html chart")

    urls = ["/", "/rubric/", "/methodology/", "/about/"]
    if data:
        urls += ["/sn/"] + [f"/sn/{s['netuid']}/" for s in data.get("subnets", [])]
    lastmod = ctx["snapshot"] if ctx["snapshot"] != "pending" else TODAY
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{SITE}{u}</loc><lastmod>{lastmod}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    if write_if_changed(REPO / "sitemap.xml", sm):
        changed.append("sitemap.xml")
    print("changed: " + (", ".join(changed) if changed else "nothing"), file=sys.stderr)


if __name__ == "__main__":
    main()
