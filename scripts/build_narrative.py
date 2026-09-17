#!/usr/bin/env python3
"""The narrative map: merge the per-narrator raw files into one dataset and render its pages.

Imported by build_site.py. Standard library only, except Pillow for the OG cards (optional).

- data/narrative/raw/<id>.json  ->  data/narrative.json (published, CC BY 4.0)
- narrative/<id>/index.html      one page per narrator
- narrative/frames/index.html   the frames
- narrative/index.html           the map (hand-written; the build injects partials and stats)
- a block per subnet page and a block for the home page
"""
import html
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "data" / "narrative" / "raw"
TEMPLATE = REPO / "scripts" / "templates" / "narrator.html"
OG_DIR = REPO / "assets" / "og"
FONTS = REPO / "scripts" / "fonts"
sys.path.insert(0, str(REPO / "scripts"))
from narrative_check import check as check_raw, SLOTS, ERAS  # noqa: E402

VERSION = "2.0"

ERA_META = [
    ("pre", "Whitepaper", "to 2020", "Before mainnet"),
    ("nakamoto", "Nakamoto", "2021 to early 2023", "Mainnet, no subnets"),
    ("finney", "Finney", "2023", "Finney network, the first subnets"),
    ("revolution", "Revolution", "late 2023 to early 2025", "Subnet expansion, root network"),
    ("dtao", "Dynamic TAO", "2025 to mid 2026", "Alpha tokens, emission follows price"),
    ("current", "Current", "mid 2026 on", "Emission follows the price moving average"),
]
ERA_LABEL = {e[0]: e[1] for e in ERA_META}
ERA_START = {"pre": "2019-01", "nakamoto": "2021-01", "finney": "2023-03", "revolution": "2023-10", "dtao": "2025-02", "current": "2026-06"}

SECTIONS = [  # the brand strategy skeleton, turned on the narrator
    ("foundation", "1. Foundation", "What they say it is for, the world it builds, what it stands for.",
     [("foundation.mission", "Mission"), ("foundation.vision", "Vision"), ("foundation.values", "Values")]),
    ("problem", "2. The problem", "What is broken that Bittensor answers, in their telling.",
     [("problem.cultural", "Cultural"), ("problem.market", "Market"), ("problem.institutional", "Institutional")]),
    ("opportunity", "3. The opportunity", "The tailwinds they cite.", [("opportunity", "Tailwinds")]),
    ("audience", "4. Audience", "Who they talk to and what they tell them.", [("audience", "Audiences")]),
    ("against", "5. Competitive positioning", "What they set it against.", [("positioning.against", "Against")]),
    ("positioning", "6. Positioning statement", "Category frame, differentiator, reason to believe.",
     [("positioning.category", "Category frame"), ("positioning.differentiator", "Differentiator"), ("positioning.reason", "Reason to believe")]),
    ("value", "7. Value proposition", "The benefit they claim, the feeling they sell, what joining says about you.",
     [("value.functional", "Functional"), ("value.emotional", "Emotional"), ("value.self_expressive", "Self-expressive")]),
    ("messaging", "8. Messaging hierarchy", "The line they repeat and the proof they point to.",
     [("messaging.h1", "The line"), ("messaging.proof", "Proof")]),
    ("voice", "9. Voice", "Register more than claim.", [("voice", "Voice")]),
    ("relationship", "10. Narrator and network", "How they describe their own relation to it.", [("relationship", "Relationship")]),
    ("language", "11. Language conventions", "What they call things, and refuse to call them.", [("language.term", "Terms")]),
    ("subnet", "12. Subnet frames", "How a subnet team describes itself, and the network it lives in.",
     [("subnet.self", "Their subnet"), ("subnet.network", "The network")]),
]
SLOT_LABEL = {
    "foundation.mission": "What it is for", "foundation.vision": "The world it builds", "foundation.values": "What it stands for",
    "problem.cultural": "What is broken", "problem.market": "What is missing", "problem.institutional": "What is at risk",
    "opportunity": "Why now", "audience": "Who they address",
    "positioning.category": "What they call it", "positioning.differentiator": "What makes it different", "positioning.reason": "Why believe them",
    "positioning.against": "What it is against",
    "value.functional": "What you get", "value.emotional": "How it feels", "value.self_expressive": "What joining says about you",
    "messaging.h1": "The line they repeat", "messaging.proof": "The proof they point to", "voice": "How they sound",
    "relationship": "Their stake in it", "language.term": "Their words for things",
    "subnet.self": "Their subnet, in their words", "subnet.network": "Bittensor, in their words",
}
SLOT_SECTION = {sid: key for key, _, _, slots in SECTIONS for sid, _ in slots}

KIND_LABEL = {"person": "Person", "institution": "Institution", "subnet": "Subnet"}
CONF_LABEL = {"verified": "verified", "probable": "secondhand", "unverified": "unconfirmed"}


def e(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def host(url):
    try:
        return urlparse(url).netloc.replace("www.", "") or url
    except Exception:
        return url


def nurl(n):
    """Where a narrator's page lives: subnet teams speak on their subnet page."""
    return f"/sn/{n['subnets'][0]}/#says" if n["kind"] == "subnet" and n.get("subnets") else f"/narrative/{n['id']}/"


def glyph(n):
    if n["kind"] == "subnet":
        return f"SN{n['subnets'][0]}"
    words = [w for w in re.split(r"[\s-]+", n["name"]) if w]
    return "".join(w[0] for w in words[:3]).upper()


def date_key(d):
    return (d + "-01-01")[:10] if len(d) == 4 else ((d + "-01")[:10] if len(d) == 7 else d)


def fmt_date(d, prec):
    try:
        if prec == "day":
            return datetime.strptime(d, "%Y-%m-%d").strftime("%-d %b %Y")
        if prec == "month":
            return datetime.strptime(d, "%Y-%m").strftime("%b %Y")
    except ValueError:
        pass
    return d[:4]


def fill(template, ctx):
    def raw(m):
        k = m.group(1)
        if k not in ctx:
            raise KeyError(f"template key missing: {k}")
        return str(ctx[k])

    def escaped(m):
        k = m.group(1)
        if k not in ctx:
            raise KeyError(f"template key missing: {k}")
        return e(ctx[k])
    out = re.sub(r"\{\{\{(\w+)\}\}\}", raw, template)
    return re.sub(r"\{\{(\w+)\}\}", escaped, out)


# ---------------- load and merge
def load_raw(raw_dir=RAW):
    files = sorted(Path(raw_dir).glob("*.json"))
    fails = []
    for f in files:
        fails += check_raw(f)
    if fails:
        for f in fails:
            print("  " + f, file=sys.stderr)
        raise SystemExit(f"narrative: {len(fails)} problem(s) in raw files")
    return [json.loads(f.read_text(encoding="utf-8")) for f in files]


def load_links():
    files = sorted((REPO / "data" / "narrative").glob("links-*.json"))
    if not files:
        return {}, ""
    d = json.loads(files[-1].read_text(encoding="utf-8"))
    return d.get("results", {}), d.get("checked", "")


def merge(raws):
    narrators, statements, metaphor_uses, relations = [], [], defaultdict(list), []
    by_id = {}
    links, links_date = load_links()
    for r in raws:
        n = dict(r["narrator"])
        n["glyph"] = glyph(n)
        n["url"] = nurl(n)
        n["aka"] = n.get("aka") or []
        n["handles"] = n.get("handles") or {}
        n["subnets"] = n.get("subnets") or []
        sts = sorted(r["statements"], key=lambda s: (date_key(s["date"]), s["id"]))
        for s in sts:
            s = dict(s)
            s["narrator"] = n["id"]
            s["date_label"] = fmt_date(s["date"], s["date_precision"])
            s["sort"] = date_key(s["date"])
            s["metaphors"] = [m.strip().lower() for m in (s.get("metaphors") or []) if m.strip()]
            s["themes"] = [t.strip().lower() for t in (s.get("themes") or []) if t.strip()]
            s["source"] = {**{"url": "", "medium": "other", "title": "", "outlet": "", "timestamp": "", "archive_url": "", "transcript": "none"}, **(s.get("source") or {})}
            s["source"]["host"] = host(s["source"]["url"])
            s["source"]["link"] = links.get(s["source"]["url"], "unchecked")
            statements.append(s)
            for m in s["metaphors"]:
                metaphor_uses[m].append(s)
        conf = Counter(s["confidence"] for s in sts)
        wordings = {m["label"].strip().lower(): m for m in (r.get("metaphors") or [])}
        n.update({
            "statement_count": len(sts),
            "confidence": {k: conf.get(k, 0) for k in ("verified", "probable", "unverified")},
            "eras": [era for era in ERAS if any(s["era"] == era for s in sts)],
            "media": sorted({s["source"]["medium"] for s in sts if s.get("source")}),
            "first_date": sts[0]["date"] if sts else "", "last_date": sts[-1]["date"] if sts else "",
            "framework": r.get("framework") or {},
            "language": r.get("language") or {"words_used": [], "words_avoided": [], "coinages": []},
            "genealogy": sorted(r.get("genealogy") or [], key=lambda g: ERAS.index(g["era"])),
            "appearances": sorted(r.get("appearances") or [], key=lambda a: a.get("date", "")),
            "metaphor_wordings": wordings,
            "coverage": r.get("coverage") or {},
            "themes": [t for t, _ in Counter(t for s in sts for t in (s.get("themes") or [])).most_common()],
        })
        for rel in r.get("relations") or []:
            relations.append({"from": n["id"], **rel})
        narrators.append(n)
        by_id[n["id"]] = n
    statements.sort(key=lambda s: (s["sort"], s["id"]))
    kind_order = {"person": 0, "institution": 1, "subnet": 2}
    narrators.sort(key=lambda n: (kind_order[n["kind"]], -n["statement_count"], n["name"]))

    metaphors = []
    for label, uses in metaphor_uses.items():
        uses = sorted(uses, key=lambda s: (s["sort"], s["id"]))
        first = uses[0]
        users = []
        for nid in dict.fromkeys(s["narrator"] for s in uses):
            mine = [s for s in uses if s["narrator"] == nid]
            w = (by_id[nid].get("metaphor_wordings") or {}).get(label) or {}
            users.append({"narrator": nid, "first": mine[0]["id"], "first_date": mine[0]["date"], "last_date": mine[-1]["date"],
                          "count": len(mine), "origin": w.get("origin", "unknown"), "wording": w.get("wording", ""), "lineage_notes": w.get("lineage_notes", "")})
        metaphors.append({
            "label": label,
            "wording": (by_id[first["narrator"]].get("metaphor_wordings") or {}).get(label, {}).get("wording") or "",
            "first": {"narrator": first["narrator"], "statement": first["id"], "date": first["date"]},
            "users": users, "count": len(uses),
            "eras": [era for era in ERAS if any(s["era"] == era for s in uses)],
            "status": "active" if any(s["era"] in ("dtao", "current") for s in uses) else "dormant",
            "statements": [s["id"] for s in uses],
        })
    metaphors.sort(key=lambda m: (-len(m["users"]), -m["count"], m["label"]))
    themes = [{"label": t, "count": c, "narrators": sorted({s["narrator"] for s in statements if t in s["themes"]})}
              for t, c in Counter(t for s in statements for t in s["themes"]).most_common()]
    for n in narrators:
        n.pop("metaphor_wordings", None)
        n["metaphors"] = [m["label"] for m in metaphors if any(u["narrator"] == n["id"] for u in m["users"])]
    sources = Counter(s["source"]["medium"] for s in statements)
    conf = Counter(s["confidence"] for s in statements)
    return {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "links_checked": links_date,
        "license": "CC BY 4.0, attribution: Bittensor Narrative Map by Mikyö Clark, legible.network",
        "eras": [{"id": i, "label": l, "span": sp, "note": nt, "start": ERA_START[i]} for i, l, sp, nt in ERA_META],
        "slots": [{"id": sid, "label": SLOT_LABEL[sid], "section": SLOT_SECTION[sid]} for sid in SLOT_LABEL],
        "sections": [{"id": k, "title": t, "note": nt, "slots": [s for s, _ in sl]} for k, t, nt, sl in SECTIONS],
        "summary": {"narrators": len(narrators), "statements": len(statements), "metaphors": len(metaphors),
                    "sources": len({s["source"]["url"] for s in statements}),
                    "confidence": {k: conf.get(k, 0) for k in ("verified", "probable", "unverified")},
                    "links": dict(Counter(s["source"]["link"] for s in statements)),
                    "media": dict(sources.most_common())},
        "narrators": narrators, "statements": statements, "metaphors": metaphors, "themes": themes, "relations": relations,
    }


# ---------------- html pieces
def badge(conf):
    return f'<span class="badge {e(conf)}">{e(CONF_LABEL.get(conf, conf))}</span>'


def quote_card(s, by_id, show_narrator=False, compact=False):
    src = s["source"]
    n = by_id.get(s["narrator"])
    who = f'<a class="who" href="{e(n["url"]) if n else "/narrative/"}">{e(n["name"]) if n else e(s["narrator"])}</a> · ' if show_narrator else ""
    ts = f' · {e(src["timestamp"])}' if src.get("timestamp") else ""
    arch = f' · <a href="{e(src["archive_url"])}" target="_blank" rel="noopener">archive</a>' if src.get("archive_url") else ""
    about = f'<a class="pill" href="/sn/{e(s["about"].split(":")[1])}/">SN{e(s["about"].split(":")[1])}</a>' if s["about"].startswith("subnet:") else ""
    slots = "".join(f'<span class="pill slot" data-slot="{e(sl)}">{e(SLOT_LABEL.get(sl, sl))}</span>' for sl in s["slots"])
    mets = "".join(f'<a class="pill met" href="/narrative/frames/#{e(m)}">{e(m)}</a>' for m in s["metaphors"])
    body = "" if compact else f'<p class="ctx">{e(s["context"])}</p>'
    return (f'<article class="st" id="{e(s["id"])}" data-era="{e(s["era"])}" data-conf="{e(s["confidence"])}">'
            f'<span class="when">{e(s["date_label"])}</span><div class="body"><p class="quote">{e(s["quote"])}</p>{body}'
            f'<div class="src">{who}<span class="d">{e(s["date_label"])}</span> · <a href="{e(src["url"])}" target="_blank" rel="noopener">{e(src["outlet"] or src["host"])}</a>'
            f'<span class="m">{e(src["medium"])}{ts}</span>{arch}{badge(s["confidence"])}{(f'<span class="badge {e(src["link"])}">{e(src["link"])}</span>') if src.get("link") and src["link"] != "unchecked" else ""}</div>'
            f'<div class="tags">{about}{slots}{mets}</div></div></article>')


def narrator_pills(n):
    pills = [f'<span class="pill">{e(KIND_LABEL[n["kind"]])}</span>']
    if n.get("role"):
        pills.append(f'<span class="pill">{e(n["role"])}</span>')
    if n.get("affiliation") and n["affiliation"] != n.get("role"):
        pills.append(f'<span class="pill">{e(n["affiliation"])}</span>')
    if n.get("active_from"):
        pills.append(f'<span class="pill">active since {e(n["active_from"])}</span>')
    for k, v in (n.get("handles") or {}).items():
        if not v:
            continue
        if k == "x":
            pills.append(f'<a class="pill" href="https://x.com/{e(v.lstrip("@"))}" target="_blank" rel="noopener">{e(v if v.startswith("@") else "@" + v)}</a>')
        elif k == "github":
            pills.append(f'<a class="pill" href="https://github.com/{e(v)}" target="_blank" rel="noopener">github {e(v)}</a>')
        elif str(v).startswith("http"):
            pills.append(f'<a class="pill" href="{e(v)}" target="_blank" rel="noopener">{e(k)}</a>')
    for sn in n.get("subnets") or []:
        pills.append(f'<a class="pill" href="/sn/{sn}/">SN{sn} in the index</a>')
    return "".join(pills)


def render_narrator(n, data, partials, site, og_name, prev_n, next_n, subnet_names=None):
    by_id = {x["id"]: x for x in data["narrators"]}
    st_by_id = {s["id"]: s for s in data["statements"]}
    mine = [s for s in data["statements"] if s["narrator"] == n["id"]]
    # genealogy by era
    gen_by_era = {g["era"]: g for g in n["genealogy"]}
    eras_html = []
    for era in ERAS:
        sts = [s for s in mine if s["era"] == era]
        g = gen_by_era.get(era)
        if not sts and not g:
            continue
        meta = next(x for x in ERA_META if x[0] == era)
        summ = ""
        if g:
            text = re.sub(r"\[([a-z0-9-]+-\d{3,})\]", lambda m: f'<a class="ref" href="#{m.group(1)}">{m.group(1).rsplit("-", 1)[1]}</a>', e(g["summary"]))
            dom = f'<span class="pill met">{e(g["dominant_metaphor"])}</span>' if g.get("dominant_metaphor") else ""
            shift = f'<p class="shift"><span class="mono">Shift</span> {e(g["shift"])}</p>' if g.get("shift") else ""
            summ = f'<div class="gen"><p>{text}</p>{dom}{shift}</div>'
        eras_html.append(f'<section class="era" id="era-{era}"><h3><span>{e(meta[1])}</span><span class="mono">{e(meta[2])} · {len(sts)} quote{"s" if len(sts) != 1 else ""}</span></h3>{summ}'
                         + "".join(quote_card(s, by_id) for s in sts) + "</section>")
    # framework
    fw_html = []
    for key, title, note, slots in SECTIONS:
        if key == "subnet" and n["kind"] != "subnet":
            continue
        blocks = []
        for sid, lab in slots:
            f = n["framework"].get(sid)
            cited = [st_by_id[c] for c in (f or {}).get("statements", []) if c in st_by_id]
            tagged = [s for s in mine if sid in s["slots"]]
            if not f and not tagged:
                continue
            summary = f'<p class="fsum">{e(f["summary"])}</p>' if f else '<p class="fsum none">No synthesis written; statements tagged to this slot are below.</p>'
            shown = cited or tagged
            extra = [s for s in tagged if s not in shown]
            more = (f'<details class="more"><summary>{len(extra)} more tagged statement{"s" if len(extra) != 1 else ""}</summary>' + "".join(quote_card(s, by_id, compact=True) for s in extra) + "</details>") if extra else ""
            blocks.append(f'<div class="slot" id="slot-{e(sid)}"><h4>{e(lab)}</h4>{summary}' + "".join(quote_card(s, by_id, compact=True) for s in shown) + more + "</div>")
        if key == "voice":
            lang = n["language"]
            wu = "".join(f'<span class="pill">{e(w)}</span>' for w in lang.get("words_used") or [])
            wa = "".join(f'<span class="pill off">{e(w)}</span>' for w in lang.get("words_avoided") or [])
            if wu or wa:
                blocks.append(f'<div class="slot"><h4>Words they use</h4><div class="pills">{wu or "<span class=sm>none recorded</span>"}</div><h4>Words they avoid</h4><div class="pills">{wa or "<span class=sm>none recorded</span>"}</div></div>')
        if key == "language":
            co = n["language"].get("coinages") or []
            if co:
                blocks.append('<div class="slot"><h4>Coinages</h4><dl class="coin">' + "".join(
                    f'<dt>{e(c["term"])}</dt><dd>{e(c.get("meaning", ""))}{(" <a class=ref href=#" + e(c["statement"]) + ">" + e(c["statement"].rsplit("-", 1)[1]) + "</a>") if c.get("statement") else ""}</dd>' for c in co) + "</dl></div>")
        if blocks:
            fw_html.append(f'<section class="fsec" id="fw-{key}"><h3>{e(title)}</h3><p class="sm">{e(note)}</p>{"".join(blocks)}</section>')
    # relations
    rel_html = []
    def who(nid):
        return f'<a href="{e(by_id[nid]["url"])}">{e(by_id[nid]["name"])}</a>' if nid in by_id else f'<span title="not yet a voice in the map">{e(nid.replace("-", " ").title())}</span>'
    for r in data["relations"]:
        if r["from"] == n["id"]:
            rel_html.append(f'<li><span class="mono">{e(r["kind"])}</span> {who(r["to"])}{(" · " + e(r.get("note", ""))) if r.get("note") else ""}{(" <a class=ref href=#" + e(r["statement"]) + ">" + e(r["statement"].rsplit("-", 1)[1]) + "</a>") if r.get("statement") else ""}</li>')
        elif r["to"] == n["id"] and r["from"] in by_id:
            rel_html.append(f'<li><a href="{e(by_id[r["from"]]["url"])}">{e(by_id[r["from"]]["name"])}</a> <span class="mono">{e(r["kind"])}</span> this voice{(" · " + e(r.get("note", ""))) if r.get("note") else ""}</li>')
    shared = []
    for m in data["metaphors"]:
        users = [u["narrator"] for u in m["users"]]
        if n["id"] in users and len(users) > 1:
            others = [by_id[u]["name"] for u in users if u != n["id"] and u in by_id]
            shared.append(f'<li><a class="pill met" href="/narrative/frames/#{e(m["label"])}">{e(m["label"])}</a> shared with {e(", ".join(others))}</li>')
    relations = ("<ul>" + "".join(rel_html) + "</ul>") if rel_html else '<p class="sm">No explicit relations recorded.</p>'
    # subnets they speak for or about
    counts = Counter(int(s["about"].split(":")[1]) for s in mine if s["about"].startswith("subnet:"))
    for sn in n.get("subnets") or []:
        counts[sn] += 0
    sub_rows = "".join(
        f'<li><a href="/sn/{sn}/#{"says" if sn in (n.get("subnets") or []) else "said"}">SN{sn} {e((subnet_names or {}).get(sn, ""))}</a> '
        f'<span class="mono">{"speaks for it · " if sn in (n.get("subnets") or []) else ""}{c} quote{"s" if c != 1 else ""}</span></li>'
        for sn, c in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))
    subnets_html = ("<ul>" + sub_rows + "</ul>") if sub_rows else '<p class="sm">No quote about a particular subnet on record.</p>'
    shared_html = ("<ul>" + "".join(shared) + "</ul>") if shared else '<p class="sm">No metaphor shared with another narrator yet.</p>'
    # appearances
    app = n.get("appearances") or []
    app_html = ("<ul class=\"apps\">" + "".join(f'<li><span class="d">{e(a.get("date", ""))}</span> <a href="{e(a.get("url", ""))}" target="_blank" rel="noopener">{e(a.get("title", ""))}</a> <span class="sm">{e(a.get("outlet", ""))} · {e(a.get("medium", ""))}{(" · " + e(a["note"])) if a.get("note") else ""}</span></li>' for a in app) + "</ul>") if app else ""
    # card
    conf = n["confidence"]
    total = max(1, n["statement_count"])
    bars = "".join(f'<div class="row"><span>{CONF_LABEL.get(k, k)}</span><span><i class="bar"><b style="width:{100 * v / total:.0f}%"></b></i> <b class="n">{v}</b></span></div>' for k, v in conf.items())
    era_pills = "".join(f'<a class="pill" href="#era-{era}">{e(ERA_LABEL[era])}</a>' for era in n["eras"])
    mine_mets = [m for m in data["metaphors"] if any(u["narrator"] == n["id"] for u in m["users"])]
    met_rows = "".join(f'<li><a href="/narrative/frames/#{e(m["label"])}">{e(m["label"])}</a> <span class="n">{sum(u["count"] for u in m["users"] if u["narrator"] == n["id"])}</span></li>'
                       for m in mine_mets[:10])
    if len(mine_mets) > 10:
        met_rows += f'<li><a href="/narrative/#view=metaphors&n={e(n["id"])}">and {len(mine_mets) - 10} more, in the map</a><span class="n"></span></li>'
    cov = n["coverage"]
    cov_html = ""
    for k, lab in (("well_covered", "Well covered"), ("thin", "Thin"), ("gaps", "Gaps")):
        items = cov.get(k) or []
        if items:
            cov_html += f'<h4>{lab}</h4><ul>' + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>"
    prevnext = (f'<a href="{e(prev_n["url"])}">← {e(prev_n["name"])}</a>' if prev_n else "<span></span>") + \
               (f'<a href="{e(next_n["url"])}">{e(next_n["name"])} →</a>' if next_n else "<span></span>")
    first_h1 = next((s for s in mine if "messaging.h1" in s["slots"]), None) or (mine[0] if mine else None)
    desc = f'{n["one_line"]} {n["statement_count"]} quotes on record, {conf["verified"]} verified, across {len(n["eras"])} era{"s" if len(n["eras"]) != 1 else ""}.'
    ctx = {
        "id": n["id"], "name": n["name"], "kind": KIND_LABEL[n["kind"]], "one_line": n["one_line"], "site": site, "og_image": og_name,
        "description": desc, "glyph": n["glyph"], "pills": narrator_pills(n),
        "lead_quote": (f'<p class="quote big">{e(first_h1["quote"])}</p><span class="qsrc">{e(first_h1["date_label"])} · <a href="#{e(first_h1["id"])}">in context</a></span>' if first_h1 else ""),
        "eras": "".join(eras_html), "framework": "".join(fw_html), "relations": relations, "shared": shared_html, "subnets": subnets_html,
        "appearances": (f'<section class="fsec"><h3>Appearances</h3><p class="sm">Public appearances on the record, whether or not a quote was taken.</p>{app_html}</section>' if app_html else ""),
        "count": n["statement_count"], "bars": bars, "era_pills": era_pills, "met_rows": met_rows or "<li class=sm>none tagged</li>",
        "coverage": cov_html or '<p class="sm">No coverage notes.</p>', "prevnext": prevnext,
        "aka": (" · ".join(n["aka"])) if n["aka"] else "",
        "issue_url": f"https://github.com/mikyodoorjey/legible.network/issues/new?template=correction.yml&title=%5BCorrection%5D%20{e(n['name']).replace(' ', '%20')}",
        "topbar": partials["topbar"], "nav": partials["nav"], "footer": partials["footer"], "robots": partials.get("robots", ""),
        "json": json.dumps({k: v for k, v in n.items()}, ensure_ascii=False).replace("</", "<\\/"),
    }
    return fill(TEMPLATE.read_text(encoding="utf-8"), ctx)


def render_metaphors(data, partials, site):
    by_id = {x["id"]: x for x in data["narrators"]}
    st_by_id = {s["id"]: s for s in data["statements"]}
    rows = []
    for m in data["metaphors"]:
        first = m["first"]
        fs = st_by_id.get(first["statement"])
        users = "".join(
            f'<a class="pill{" on" if u["narrator"] == first["narrator"] else ""}" href="{e(by_id[u["narrator"]]["url"].split("#")[0])}#{e(u["first"])}" title="{e(u.get("wording") or "")}">'
            f'{e(by_id[u["narrator"]]["glyph"])} <span class="n">{e(fmt_date(u["first_date"], "month" if len(u["first_date"]) >= 7 else "year"))}</span></a>'
            for u in m["users"] if u["narrator"] in by_id)
        eras = "".join(f'<i class="{"on" if era in m["eras"] else ""}" title="{e(ERA_LABEL[era])}"></i>' for era in ERAS)
        rows.append(
            f'<article class="met" id="{e(m["label"])}"><div class="mh"><h3><a href="#{e(m["label"])}">{e(m["label"])}</a></h3>'
            f'<span class="badge {e(m["status"])}">{e(m["status"])}</span><span class="mono">{m["count"]} use{"s" if m["count"] != 1 else ""} · {len(m["users"])} voice{"s" if len(m["users"]) != 1 else ""}</span><span class="eras" title="Eras in use">{eras}</span></div>'
            + (f'<p class="quote">{e(fs["quote"])}</p><p class="src">First on record: <a href="{e(by_id[first["narrator"]]["url"].split("#")[0])}#{e(first["statement"])}">{e(by_id[first["narrator"]]["name"])}</a>, {e(fs["date_label"])} · <a href="{e(fs["source"]["url"])}" target="_blank" rel="noopener">{e(fs["source"]["outlet"] or fs["source"]["host"])}</a> {badge(fs["confidence"])}</p>' if fs else "")
            + f'<div class="users"><span class="mono">Used by, in order of first use</span><div class="pills">{users}</div></div></article>')
    active = sum(1 for m in data["metaphors"] if m["status"] == "active")
    shared = sum(1 for m in data["metaphors"] if len(m["users"]) > 1)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The frames · Legible</title>
{partials.get("robots", "")}
<meta name="description" content="Every figurative frame used for Bittensor on the record: who said it first, who picked it up, and whether it is still in use.">
<link rel="canonical" href="{site}/narrative/frames/">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website"><meta property="og:url" content="{site}/narrative/frames/">
<meta property="og:title" content="The frames · Legible">
<meta property="og:description" content="Who said it first, who picked it up, whether it is still in use.">
<meta property="og:image" content="{site}/assets/og/narrative.png"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&family=Geist:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/narrative.css">
</head>
<body>
{partials["nav"]}
<main class="wrap" style="padding-top:32px">
  <h1>The frames, <em>and who reached for them first.</em></h1>
  <p class="lede" style="max-width:62ch">A frame is a figurative way of saying what the network or a subnet is: a brain, a market, a language, a Bitcoin. Each one below is dated to its earliest sourced use and followed through every voice that picked it up. Active means used since dynamic TAO.</p>
  <div class="stats"><div><b>{len(data["metaphors"])}</b><span>frames</span></div><div><b>{shared}</b><span>shared by two or more</span></div><div><b>{active}</b><span>still active</span></div></div>
  <div class="metgrid">{"".join(rows)}</div>
</main>
{partials["footer"]}
</body>
</html>
"""


def subnet_narrative(data, netuid):
    """Fragments for a subnet page: what the team says (self, network), what others say, frames, and the map link."""
    by_id = {x["id"]: x for x in data["narrators"]}
    own = next((n for n in data["narrators"] if n["kind"] == "subnet" and netuid in n["subnets"]), None)
    about = [s for s in data["statements"] if s["about"] == f"subnet:{netuid}" and (not own or s["narrator"] != own["id"])]
    out = {"count": 0, "self": "", "network": "", "said": "", "frames": "", "map": "", "summary_self": "", "summary_network": ""}
    if own:
        selfs = [s for s in data["statements"] if s["narrator"] == own["id"] and "subnet.self" in s["slots"]]
        nets = [s for s in data["statements"] if s["narrator"] == own["id"] and "subnet.network" in s["slots"]]
        fw = own["framework"]
        out["count"] = own["statement_count"]
        out["summary_self"] = e((fw.get("subnet.self") or {}).get("summary", ""))
        out["summary_network"] = e((fw.get("subnet.network") or {}).get("summary", ""))
        out["self"] = "".join(quote_card(s, by_id, compact=True) for s in selfs[:5])
        out["network"] = "".join(quote_card(s, by_id, compact=True) for s in nets[:4])
        mets = [m for m in data["metaphors"] if any(u["narrator"] == own["id"] for u in m["users"])]
        out["frames"] = " ".join(f'<a class="pill met" href="/narrative/frames/#{e(m["label"])}">{e(m["label"])}</a>' for m in mets)
        out["map"] = f'/narrative/#n={e(own["id"])}'
    out["said"] = "".join(quote_card(s, by_id, show_narrator=True, compact=True) for s in about[:6])
    return out


SUBNET_BLOCK_CSS = """
.narr-block{border-top:1px solid var(--rule);padding:16px 0;margin:0 0 26px}
.narr-block .nb-head{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
.narr-block .nb-link{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--soft)}
.narr-block .nb-h2{font-size:22px;margin:10px 0 4px}
.narr-block .nb-col{margin-top:12px}.narr-block .nb-col h3{font-size:15px;margin-bottom:4px}.narr-block .nb-col>p{margin:0 0 8px;color:var(--ink-soft);font-size:14px}
.narr-block .nb-mets{margin:12px 0 0;display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.st{border-top:1px solid var(--rule);padding:10px 0}
.st .quote{font-size:15px;margin:0 0 4px}
.st .ctx{font-size:13px;color:var(--soft);margin:0 0 6px}
.st .src{font-family:var(--mono);font-size:10.5px;letter-spacing:.04em;color:var(--softer);display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.st .src .m{text-transform:uppercase;letter-spacing:.08em}
.st .src .who{color:var(--ink)}
.st .tags{display:flex;gap:4px;flex-wrap:wrap;margin-top:6px}
.st .tags .pill{font-size:9.5px;padding:2px 7px}

"""


def home_block(data):
    """A section for the home page: the map in one paragraph, the narrators as a strip, three live metaphors."""
    persons = [n for n in data["narrators"] if n["kind"] != "subnet"][:8]
    strip = "".join(f'<a class="nstrip" href="/narrative/{e(n["id"])}/"><b>{e(n["glyph"])}</b><span>{e(n["name"])}</span><small>{n["statement_count"]} quotes</small></a>' for n in persons)
    mets = data["metaphors"][:6]
    met_html = "".join(f'<a class="pill met" href="/narrative/frames/#{e(m["label"])}">{e(m["label"])} <span class="n">{len(m["users"])}</span></a>' for m in mets)
    sm = data["summary"]
    return (f'<div class="nhome"><div class="nhome-strip">{strip}</div>'

            f'<p class="demo"><a href="/narrative/">Open the map</a><a href="/narrative/#view=metaphors">Frame lineage</a><a href="/narrative/#view=framework">Voice by voice</a><a href="/method/#the-map-what-it-records">Method</a></p></div>')


# ---------------- OG cards, in the site's one family
def render_og_narrator(n, data, out_path):
    try:
        from render_subnets import og_canvas, _font, _save
        img, d, F, P = og_canvas("LEGIBLE  ·  VOICES")
    except ImportError:
        return False
    ink, soft, softer, rule = P["ink"], P["soft"], P["softer"], P["rule"]
    d.text((70, 100), f"{KIND_LABEL[n['kind']].upper()}  ·  {n['statement_count']} QUOTES ON RECORD  ·  {n['confidence']['verified']} VERIFIED", font=F["mono_s"], fill=softer)
    size = 72
    while size > 40 and d.textlength(n["name"], font=_font(["InterTight.ttf"], size)) > 1060:
        size -= 6
    d.text((66, 150), n["name"], font=_font(["InterTight.ttf"], size), fill=ink)
    mine = [s for s in data["statements"] if s["narrator"] == n["id"]]
    q = next((s for s in mine if "messaging.h1" in s["slots"]), mine[0] if mine else None)
    y = 250
    if q:
        qf = _font(["InterTight.ttf"], 34)
        words, lines, cur = ("\u201c" + q["quote"] + "\u201d").split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=qf) <= 1060:
                cur = t
            else:
                lines.append(cur); cur = w
        if cur:
            lines.append(cur)
        for ln in lines[:4]:
            d.text((70, y), ln, font=qf, fill=soft)
            y += 44
        d.text((70, y + 10), f"{q['date_label'].upper()}  ·  {(q['source']['outlet'] or q['source']['host']).upper()[:60]}", font=F["mono_s"], fill=softer)
    ex = 70
    for era in ERAS:
        on = era in n["eras"]
        d.rectangle([ex, 500, ex + 160, 512], fill=ink if on else rule)
        d.text((ex, 520), ERA_LABEL[era].upper(), font=F["mono_xs"], fill=ink if on else softer)
        ex += 176
    return _save(img, out_path)


def render_og_default(data, out_path):
    try:
        from render_subnets import og_canvas, _font, _save
        img, d, F, P = og_canvas("LEGIBLE  ·  VOICES")
    except ImportError:
        return False
    big = _font(["InterTight.ttf"], 70)
    d.text((66, 110), "Who says what Bittensor is,", font=big, fill=P["ink"])
    d.text((66, 186), "and when they started", font=big, fill=P["ink"])
    d.text((66, 262), "saying it.", font=big, fill=P["teal"])
    sm = data["summary"]
    y = 380
    for lab, v in (("voices", sm["narrators"]), ("quotes on record", sm["statements"]), ("frames traced", sm["metaphors"])):
        d.text((70, y), f"{v:<6}{lab}", font=F["mono_s"], fill=P["soft"])
        y += 30
    x = 640
    for n in [x for x in data["narrators"] if x["kind"] != "subnet"][:6]:
        d.text((x, 380), n["glyph"], font=F["mono"], fill=P["ink"])
        d.text((x, 410), n["name"][:18], font=F["mono_xs"], fill=P["softer"])
        x += 170
        if x > 1100:
            break
    return _save(img, out_path)


# ---------------- coverage report (for the method page)
def coverage_report(data):
    rows = []
    for n in data["narrators"]:
        c = n["confidence"]
        rows.append(f'<tr><td><a href="{e(n["url"])}">{e(n["name"])}</a></td><td>{e(KIND_LABEL[n["kind"]])}</td><td>{n["statement_count"]}</td>'
                    f'<td>{c["verified"]}</td><td>{c["probable"]}</td><td>{c["unverified"]}</td>'
                    f'<td>{e(", ".join(ERA_LABEL[x] for x in n["eras"]))}</td><td>{e(", ".join(n["media"]))}</td>'
                    f'<td>{e("; ".join((n["coverage"].get("gaps") or [])[:3]))}</td></tr>')
    return ('<div class="table-wrap data-table"><table><thead><tr><th>Voice</th><th>Kind</th><th>Quotes</th><th>Verified</th><th>Secondhand</th><th>Unconfirmed</th><th>Eras</th><th>Media</th><th>Largest gaps</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


# ---------------- entry point
def build(partials, site, write_if_changed, raw_dir=RAW, subnet_names=None):
    changed = []
    raws = load_raw(raw_dir)
    if not raws:
        print("  narrative: no raw files, skipped", file=sys.stderr)
        return changed, None
    data = merge(raws)
    if write_if_changed(REPO / "data" / "narrative.json", json.dumps(data, ensure_ascii=False, separators=(",", ":"))):
        changed.append("data/narrative.json")
    if write_if_changed(REPO / "data" / "narrative-pretty.json", json.dumps(data, ensure_ascii=False, indent=1)):
        changed.append("data/narrative-pretty.json")
    og_ok = None
    ns = [n for n in data["narrators"] if n["kind"] != "subnet"]  # subnet teams speak on their subnet page
    for i, n in enumerate(ns):
        og_name = f"narrative-{n['id']}.png"
        if og_ok is not False:
            ok = render_og_narrator(n, data, OG_DIR / og_name)
            og_ok = ok if og_ok is None else (og_ok and ok)
            if not ok:
                og_name = "narrative.png"
        else:
            og_name = "narrative.png"
        page = render_narrator(n, data, partials, site, og_name, ns[i - 1] if i > 0 else None, ns[i + 1] if i + 1 < len(ns) else None, subnet_names)
        if write_if_changed(REPO / "narrative" / n["id"] / "index.html", page):
            changed.append(f"narrative/{n['id']}/")
    if render_og_default(data, OG_DIR / "narrative.png"):
        changed.append("assets/og/narrative.png")
    if write_if_changed(REPO / "narrative" / "frames" / "index.html", render_metaphors(data, partials, site)):
        changed.append("narrative/frames/")
    return changed, data
