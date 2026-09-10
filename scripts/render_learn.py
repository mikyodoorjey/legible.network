#!/usr/bin/env python3
"""Explainers and the learn hub. Imported by build_site.py.

Reads data/explainers/<netuid>.md (front matter plus seven fixed sections and Sources)
and data/explainers/glossary.md. Renders:
  - the explainer block placed at the top of each subnet page
  - /learn/ (glossary, entries by commodity, alphabetical list)
  - the glossary auto-links: first use of each term in an entry links to /learn/#term
"""
import html
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DIR = REPO / "data" / "explainers"
COMMODITY_LABEL = {
    "inference": "Inference: answers from trained models", "compute": "Compute: GPU time and machines",
    "training": "Training: making new models", "data": "Data: collected, labeled, or verified",
    "agents": "Agents: software that acts", "forecasting": "Forecasting: predictions with a score",
    "storage": "Storage: files and archives", "security": "Security: testing and defense",
    "media": "Media: images, video, audio", "science": "Science: research outputs", "other": "Other",
}


def e(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse_entry(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None
    fm = {}
    for ln in m.group(1).splitlines():
        if ":" in ln:
            k, v = ln.split(":", 1)
            fm[k.strip()] = v.strip()
    body = m.group(2)
    sections = []
    cur, buf = None, []
    for ln in body.splitlines():
        if ln.startswith("## "):
            if cur is not None:
                sections.append((cur, "\n".join(buf).strip()))
            cur, buf = ln[3:].strip(), []
        else:
            buf.append(ln)
    if cur is not None:
        sections.append((cur, "\n".join(buf).strip()))
    return {"fm": fm, "sections": sections, "netuid": int(fm.get("netuid", path.stem))}


def load_entries():
    out = {}
    for p in sorted(DIR.glob("*.md")):
        if not p.stem.isdigit():
            continue
        ent = parse_entry(p)
        if ent:
            out[ent["netuid"]] = ent
    return out


def load_glossary():
    p = DIR / "glossary.md"
    if not p.exists():
        return []
    terms = []
    cur, buf = None, []
    for ln in p.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            if cur:
                terms.append((cur, "\n".join(buf).strip()))
            cur, buf = ln[3:].strip(), []
        elif cur is not None:
            buf.append(ln)
    if cur:
        terms.append((cur, "\n".join(buf).strip()))
    return terms


def md_inline(s, inline_fn):
    return inline_fn(s)


def md_block(md, inline_fn):
    """Paragraphs and bullet lists only; the explainers use nothing else."""
    out, para = [], []
    lines = md.splitlines()
    i = 0

    def flush():
        nonlocal para
        if para:
            out.append("<p>" + inline_fn(" ".join(x.strip() for x in para)) + "</p>")
            para = []
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            flush()
            i += 1
            continue
        if re.match(r"^\s*[-*] ", ln):
            flush()
            items = []
            while i < len(lines) and re.match(r"^\s*[-*] ", lines[i]):
                items.append(re.sub(r"^\s*[-*] ", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline_fn(x)}</li>" for x in items) + "</ul>")
            continue
        para.append(ln)
        i += 1
    flush()
    return "".join(out)


class Linker:
    """Link the first use of each glossary term in an entry to /learn/#term."""

    def __init__(self, terms, inline_fn):
        self.inline_fn = inline_fn
        # longest first so "alpha token" wins over "TAO"
        self.terms = sorted([t for t, _ in terms], key=len, reverse=True)
        self.used = set()

    def __call__(self, s):
        out = self.inline_fn(s)
        for t in self.terms:
            if t in self.used:
                continue
            # skip if already inside a tag or link
            pat = re.compile(r"(?<![\w/#-])(" + re.escape(t) + r"s?)(?![\w-])(?![^<]*>)(?![^<]*</a>)", re.I)
            m = pat.search(out)
            if m:
                out = out[:m.start()] + f'<a class="term" href="/learn/#{slug(t)}">{m.group(1)}</a>' + out[m.end():]
                self.used.add(t)
        return out


def render_entry_block(ent, terms, inline_fn, sub=None):
    fm = ent["fm"]
    link = Linker(terms, inline_fn)
    parts = [f'<section class="explainer" id="explainer">']
    parts.append(f'<span class="mono">Explained from zero · {e(fm.get("commodity", ""))} · written {e(fm.get("written", ""))}</span>')
    for h, body in ent["sections"]:
        if h == "Sources":
            continue
        if h == "In one sentence":
            parts.append(f'<p class="lede one">{link(body.strip())}</p>')
            continue
        parts.append(f'<h3>{e(h)}</h3>{md_block(body, link)}')
    src = next((b for h, b in ent["sections"] if h == "Sources"), "")
    urls = re.findall(r"https?://[^\s)>\]]+", src)
    if urls:
        parts.append('<details class="srcs"><summary class="mono">Sources for this explainer</summary><ul>' +
                     "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(u[:90])}</a></li>' for u in urls) + "</ul></details>")
    parts.append(f'<p class="sm">Metaphor: {e(fm.get("metaphor", ""))}. Every claim is drawn from the evidence set or the subnet\'s own materials; "(inferred)" marks a conclusion rather than a quote. <a href="/methodology/#corrections">Corrections</a>.</p>')
    parts.append("</section>")
    return "".join(parts)


def render_placeholder(sub):
    return ('<section class="explainer" id="explainer"><span class="mono">Explained from zero</span>'
            f'<p class="sm">The plain-language explainer for SN{sub["netuid"]} {e(sub["name"])} is being written. The scores and evidence below are complete.</p></section>')


def render_learn(data, entries, terms, partials, site, inline_fn, head_fn):
    by_comm = {}
    for nid, ent in entries.items():
        by_comm.setdefault(ent["fm"].get("commodity", "other"), []).append(ent)
    subs = {s["netuid"]: s for s in data["subnets"]}
    def item(ent):
        s = subs.get(ent["netuid"], {})
        return (f'<li><a href="/sn/{ent["netuid"]}/#explainer"><b>SN{ent["netuid"]} {e(ent["fm"].get("name", s.get("name", "")))}</b></a>'
                f'<span class="sm"> · {e(ent["fm"].get("metaphor", ""))}</span><br><span class="one">{e(ent["fm"].get("one_sentence", ""))}</span></li>')
    comm_html = ""
    for c in COMMODITY_LABEL:
        if c in by_comm:
            comm_html += f'<h3 id="{c}">{e(COMMODITY_LABEL[c])}</h3><ul class="entries">' + "".join(item(x) for x in sorted(by_comm[c], key=lambda x: subs.get(x["netuid"], {}).get("rank", 999))) + "</ul>"
    alpha_html = "<ul class=\"entries compact\">" + "".join(
        f'<li><a href="/sn/{ent["netuid"]}/#explainer">{e(ent["fm"].get("name", ""))}</a> <span class="sm">SN{ent["netuid"]} · {e(ent["fm"].get("commodity", ""))}</span></li>'
        for ent in sorted(entries.values(), key=lambda x: x["fm"].get("name", "").lower())) + "</ul>"
    gloss = "".join(f'<section id="{slug(t)}" class="gterm"><h3>{e(t)}</h3>{md_block(b, Linker([x for x in terms if x[0] != t], inline_fn))}</section>' for t, b in terms)
    missing = [s for n, s in subs.items() if n not in entries]
    missing_html = ("<p class=\"sm\">Still being written: " + ", ".join(f'SN{s["netuid"]} {e(s["name"])}' for s in sorted(missing, key=lambda x: x["rank"])) + ".</p>") if missing else ""
    body = f"""<main class="wrap learn">
  <div class="intro">
    <span class="mono">Learn · {len(entries)} of {len(subs)} subnets explained</span>
    <h1>What each subnet makes, <em>explained from zero.</em></h1>
    <p class="lede">One entry per subnet, written for someone who has never heard of Bittensor: what the digital commodity is, why it has a price, who buys it, how the work gets done, and how you would check. Each entry carries one everyday comparison and says where it breaks. Every claim comes from the subnet's own materials or the evidence behind its <a href="/">legibility score</a>.</p>
    <p class="sm">Jump to: <a href="#by-commodity">by commodity</a> · <a href="#alphabetical">alphabetical</a> · <a href="#glossary">glossary</a></p>
  </div>
  <section id="by-commodity"><h2>By commodity</h2>{comm_html}{missing_html}</section>
  <section id="alphabetical"><h2>Alphabetical</h2>{alpha_html}</section>
  <section id="glossary"><h2>Glossary</h2><p class="sm">Every term the entries use, with an everyday comparison. The comparison is a way in, not a definition.</p>{gloss}</section>
</main>"""
    css = """
.learn .intro{padding:36px 0 10px;max-width:74ch}
.learn h2{margin:36px 0 12px;padding-top:18px;border-top:1px solid var(--rule)}
.learn h3{margin:22px 0 8px}
.entries{list-style:none;padding:0;margin:0}
.entries li{padding:10px 0;border-top:1px solid var(--rule);line-height:1.5}
.entries li:first-child{border-top:0}
.entries .one{color:var(--ink-soft);font-size:14px}
.entries.compact li{padding:5px 0;border:0}
.gterm p{max-width:74ch;color:var(--ink-soft)}
.gterm h3{scroll-margin-top:20px}
"""
    return head_fn("Learn", "What each Bittensor subnet makes, explained from zero, with a glossary.", "/learn/", partials, site, css) + body + partials["footer"] + '<script src="/assets/glossary.js"></script><script src="/assets/terms.js"></script>' + "</body></html>\n"


EXPLAINER_CSS = """
.explainer{border:1px solid var(--rule);border-left:3px solid var(--teal);border-radius:8px;background:var(--paper);padding:18px 22px 14px;margin:18px 0 28px}
.explainer .one{font-family:var(--serif);font-size:20px;line-height:1.35;color:var(--ink);margin:8px 0 14px;font-variation-settings:"opsz" 24,"SOFT" 60}
.explainer h3{font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--softer);margin:18px 0 6px;font-weight:500}
.explainer p{margin:0 0 10px;color:var(--ink-soft);max-width:74ch}
.explainer ul{padding-left:20px;color:var(--ink-soft)}
.explainer .srcs{margin-top:10px}
.explainer .srcs ul{font-family:var(--mono);font-size:11px;padding-left:18px}
.scored-head{margin:30px 0 8px;padding-top:18px;border-top:1px solid var(--rule)}
"""
