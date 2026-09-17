#!/usr/bin/env python3
"""Per-subnet pages, the subnet list, OpenGraph images, and the says-versus-shows chart.

Imported by build_site.py. Standard library only, except Pillow for the PNGs
(optional: without it every page falls back to the default card).
"""
import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "scripts" / "templates" / "subnet.html"
FONTS = REPO / "scripts" / "fonts"
OG_DIR = REPO / "assets" / "og"

AUD = ["stakers", "miners", "buyers", "newcomers"]
AUD_LABEL = {"stakers": "Stakers and validators", "miners": "Miners", "buyers": "Buyers and enterprises", "newcomers": "Newcomers"}
AUD_Q = {"stakers": "Should I allocate here?", "miners": "Can I compete, and what wins?",
         "buyers": "Can I use this today?", "newcomers": "What is this and why does it matter?"}
BAND_WORD = ["sparse", "thin", "partial", "workable", "clear", "exemplary"]
BAND_DEF = ["nobody can tell you", "only other people can tell you; the subnet itself doesn't say", "it's in there somewhere, but scattered, out of date, or buried in code", "you'd find it, but you'd need to already know Bittensor or dig for a while", "you'd get your answer on your own in about five minutes", "you'd have everything, with proof you can check, in a couple of clicks"]
CONF_LABEL = {"verified": "verified", "inferred": "secondhand", "unknown": "unconfirmed"}
IDENTITY_FIELDS = ["subnet_name", "github_repo", "subnet_contact", "subnet_url", "discord", "description", "additional"]
LIGHT = {"bg": (247, 246, 243), "paper": (239, 237, 232), "ink": (26, 26, 26), "soft": (107, 107, 107), "softer": (138, 138, 138),
         "teal": (231, 38, 48), "rule": (228, 226, 221),
         "bands": [(231, 38, 48), (138, 138, 138), (107, 107, 107), (74, 74, 74), (42, 42, 42), (26, 26, 26)],
         "aud": {"stakers": (26, 26, 26), "miners": (26, 26, 26), "buyers": (26, 26, 26), "newcomers": (26, 26, 26)}}


def e(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def band(v):
    try:
        return max(0, min(5, int(float(v))))
    except (TypeError, ValueError):
        return 0


def dots(n):
    k = round(float(n or 0))
    return '<span class="dots" title="%.1f">' % float(n or 0) + "".join(
        f'<span class="band-{band(n)}">●</span>' if i <= k else '<span class="off">●</span>' for i in range(1, 6)) + "</span>"


def meter(sub):
    c = sub["identity_completeness"]
    return f'<span class="meter" title="{c["filled"]} of {c["of"]} identity fields set">' + "".join(
        f'<i class="{"on" if i < c["filled"] else ""}"></i>' for i in range(c["of"])) + f'</span> <span class="mono" style="letter-spacing:0">{c["filled"]}/{c["of"]}</span>'


def host(url):
    try:
        return urlparse(url).netloc.replace("www.", "") or url
    except Exception:
        return url


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


def description(sub):
    scores = {a: float(sub["audiences"][a]["score"]) for a in AUD}
    hi = max(scores, key=scores.get)
    lo = min(scores, key=scores.get)
    return (f"Legibility {float(sub['composite']):.1f} of 5. Most legible to {hi} ({scores[hi]:.1f}), least to {lo} ({scores[lo]:.1f}). "
            f"What a first-time reader can find in five minutes, snapshot {sub.get('last_verified', '')}.")


WHO = {"stakers": "staker", "miners": "miner", "buyers": "buyer", "newcomers": "newcomer"}


def verdict_block(sub, comp):
    v = sub.get("verdict")
    if not isinstance(v, dict) or not v.get("summary"):
        return ""
    items = "".join(
        f'<li><b>If you were a {WHO[a]}</b> <span class="band-{band(sub["audiences"][a]["score"])}" style="font-family:var(--pix)">{float(sub["audiences"][a]["score"]):.1f}</span> {e(v[a])}</li>'
        for a in AUD if v.get(a))
    return f'<div class="verdict"><span class="mono">What {comp:.1f} means</span><p>{e(v["summary"])}</p><ul>{items}</ul></div>'


def first_sentences(text, n=2):
    parts = re.split(r"(?<=[.!?])\s+", (text or "").strip())
    return " ".join(parts[:n]).strip()


def program_card(sub, ent):
    """The subnet as a mining program: the work, how it is scored, what it emits."""
    fm = (ent or {}).get("fm", {})
    secs = dict((ent or {}).get("sections", []))
    work = fm.get("one_sentence") or (sub.get("own_words") or {}).get("quote") or ""
    scored = first_sentences(secs.get("How the work gets done", ""), 2)
    t = sub.get("alpha") or {}
    emits = f'{e(sub["emission_pct"])} of the block reward'
    if t.get("symbol"):
        emits += f' · paid in {e(t["symbol"])}, its own token'
    rows = [f'<div><span class="mono">The work</span><p>{e(work)}</p></div>']
    if scored:
        rows.append(f'<div><span class="mono">How it is scored</span><p>{e(scored)}</p></div>')
    rows.append(f'<div><span class="mono">What it emits</span><p>{emits}</p></div>')
    return f'<section class="program" id="program"><div class="pg-head"><span class="mono">The program</span><span class="sm">{e(fm.get("commodity", ""))}</span></div>{"".join(rows)}</section>'


def says_sections(sub, nv):
    """What it says (own words, the team's quotes) and what is said about it (others' quotes)."""
    ow = sub.get("own_words") or {}
    own = (f'<article class="st"><p class="quote">{e(ow.get("quote", ""))}</p><div class="src"><span class="d">In their own words</span> · '
           f'<a href="{e(ow.get("url", ""))}" target="_blank" rel="noopener">{e(host(ow.get("url", "")))}</a><span class="badge verified">verified</span></div></article>') if ow.get("quote") else ""
    nv = nv or {}
    says = [f'<section class="says" id="says"><h2 class="sec-h">What it says</h2>']
    says.append(f'<p class="sm">The subnet in its own words: the line the index took from its front door, and what the team has said on the record. {("<a href=\"" + nv["map"] + "\">All " + str(nv["count"]) + " quotes in the map</a>.") if nv.get("map") else ""}</p>')
    says.append(own)
    if nv.get("self"):
        says.append(f'<h3>Their subnet</h3>{("<p class=fsum>" + nv["summary_self"] + "</p>") if nv.get("summary_self") else ""}{nv["self"]}')
    if nv.get("network"):
        says.append(f'<h3>Bittensor, in their words</h3>{("<p class=fsum>" + nv["summary_network"] + "</p>") if nv.get("summary_network") else ""}{nv["network"]}')
    if nv.get("frames"):
        says.append(f'<p class="frames"><span class="mono">Frames</span> {nv["frames"]}</p>')
    says.append("</section>")
    said = ""
    if nv.get("said"):
        said = f'<section class="said" id="said"><h2 class="sec-h">What is said about it</h2><p class="sm">By other voices in the map, verbatim and dated.</p>{nv["said"]}</section>'
    return "".join(says), said


def render_subnet(sub, data, partials, site, prev_sub, next_sub, og_name, explainer_html="", explainer_css="", narrative=None, narrative_css="", entry=None):
    ident = sub["identity"]
    check = {c["field"]: c for c in sub.get("identity_check", [])}
    rows = []
    for f in IDENTITY_FIELDS:
        v = ident.get(f) or ""
        chk = check.get(f, {})
        res = chk.get("result", "")
        if not v:
            rows.append(f"<dt>{e(f)}</dt><dd class=\"unset\">not set</dd>")
            continue
        if v.startswith("http"):
            val = f'<a href="{e(v)}" target="_blank" rel="noopener">{e(host(v))}</a>'
        else:
            val = e(v)
        flag = f' <span class="badge mismatch">{e(res)}</span>' if res in ("mismatch", "dead") else ""
        rows.append(f"<dt>{e(f)}</dt><dd>{val}{flag}</dd>")

    panels = []
    for a in AUD:
        au = sub["audiences"][a]
        cells = []
        for c in au["cells"]:
            url = c.get("url") or ""
            src = f'<a href="{e(url)}" target="_blank" rel="noopener">{e(host(url))}</a>' if url else '<span>no source</span>'
            note = c.get("note") or ""
            quote = ""
            m = re.search(r'"([^"]{4,})"', note)
            if m:
                quote = f'<p class="quote">{e(m.group(1))}</p>'
                note = (note[:m.start()] + note[m.end():]).strip(" ,;.")
            link = c.get("link") or "unchecked"
            cells.append(
                f'<details open><summary><span class="qn">{e(c["q"].upper())}</span><span class="ql">{e(c["label"])}</span>'
                f'<span class="qs">{dots(c["score"])} <b class="band-{band(c["score"])}" style="font-family:var(--mono);font-weight:500">{c["score"] if c["score"] is not None else "?"}</b></span></summary>'
                f'<div class="ev">{quote}<div class="src">{src}<span class="badge {e(c["status"])}">{e(CONF_LABEL.get(c["status"], c["status"]))}</span><span class="badge {e(link)}">{e(link)}</span></div>'
                f'{("<p class=note>" + e(note) + "</p>") if note else ""}</div></details>')
        panels.append(
            f'<section class="panel" style="--accent:var(--a-{a})"><h3><span class="aud-{a}">{AUD_LABEL[a]}</span>'
            f'<span>{dots(au["score"])} <b class="band-{band(au["score"])}" style="font-family:var(--mono);font-weight:500">{float(au["score"]):.1f}</b></span></h3>'
            f'<p class="who">{AUD_Q[a]} · rank {au.get("rank", "?")} of {len(data["subnets"])} for this audience</p>{"".join(cells)}</section>')

    score_rows = "".join(
        f'<div class="srow" title="{e(AUD_LABEL[a])} {float(sub["audiences"][a]["score"]):.1f} of 5: {BAND_WORD[band(sub["audiences"][a]["score"])]}, {BAND_DEF[band(sub["audiences"][a]["score"])]}"><span class="k aud-{a}">{AUD_LABEL[a].split(" and ")[0]}</span>'
        f'<span class="v"><b>{float(sub["audiences"][a]["score"]):.1f}</b><span>{BAND_WORD[band(sub["audiences"][a]["score"])]} · rank {sub["audiences"][a].get("rank", "?")} of {len(data["subnets"])}</span></span></div>'
        for a in AUD)
    chain_rows = [
        f'<div class="srow"><span class="k">Emission</span><span class="v"><b>{e(sub["emission_pct"])}</b><span>of the block reward · rank {e(sub["rank"])} of {len(data["subnets"])}</span></span></div>',
        f'<div class="srow"><span class="k">Participants</span><span class="v"><b>{e(sub.get("active_miners", "?"))} miners · {e(sub.get("active_validators", "?"))} validators</b></span></div>',
    ]
    if sub.get("registration_cost_tao") is not None:
        chain_rows.append(f'<div class="srow"><span class="k">Registration</span><span class="v"><b>{float(sub["registration_cost_tao"]):.4g} TAO</b></span></div>')
    chain_rows.append(f'<div class="srow"><span class="k">Verified</span><span class="v"><b>{e(sub.get("last_verified", ""))}</b><span>links checked and scores merged</span></span></div>')
    prov = "".join(f'<span class="pill">{e(p.strip())}</span>' for p in (sub.get("claim_labels") or "").split(";") if p.strip())
    corrections = sub.get("corrections") or []
    if corrections:
        prov += "".join(f'<span class="pill">corrected {e(c["date"])}: {e(c["audience"])}.{e(c["q"])} {e(c["old"])} to {e(c["new"])}</span>' for c in corrections)
    pills = [f'<span class="pill">{e(sub["emission_pct"])} of emission</span>',
             f'<span class="pill">{e(sub.get("active_miners", "?"))} miners · {e(sub.get("active_validators", "?"))} validators</span>']
    if sub.get("registration_cost_tao") is not None:
        pills.append(f'<span class="pill">registration {float(sub["registration_cost_tao"]):.4g} TAO</span>')
    pills.append(f'<span class="pill">verified {e(sub.get("last_verified", ""))}</span>')
    ow = sub.get("own_words") or {}
    own = (f'<p class="quote">{e(ow.get("quote", ""))}</p><span class="qsrc">In their own words · '
           f'<a href="{e(ow.get("url", ""))}" target="_blank" rel="noopener">{e(host(ow.get("url", "")))}</a></span>') if ow.get("quote") else ""
    prevnext = (f'<a href="/sn/{prev_sub["netuid"]}/">← SN{prev_sub["netuid"]} {e(prev_sub["name"])}</a>' if prev_sub else "<span></span>") + \
               (f'<a href="/sn/{next_sub["netuid"]}/">SN{next_sub["netuid"]} {e(next_sub["name"])} →</a>' if next_sub else "<span></span>")
    comp = float(sub["composite"])
    ctx = {
        "netuid": sub["netuid"], "name": sub["name"], "rank": sub["rank"], "site": site,
        "description": description(sub), "composite": f"{comp:.1f}", "band": band(comp), "band_word": BAND_WORD[band(comp)],
        "band_def": f"{BAND_WORD[band(comp)]}: {BAND_DEF[band(comp)]}.",
        "verdict_block": verdict_block(sub, comp),
        "og_image": og_name, "pills": "".join(pills), "own_words": own, "meter": meter(sub), "identity_rows": "".join(rows),
        "panels": "".join(panels), "provenance": prov or '<span class="pill">no provenance recorded</span>',
        "score_rows": score_rows, "chain_rows": "".join(chain_rows), "prevnext": prevnext,
        "issue_url": f"https://github.com/mikyodoorjey/legible.network/issues/new?template=correction.yml&title=%5BCorrection%5D%20SN{sub['netuid']}%20{e(sub['name']).replace(' ', '%20')}",
        "mail_subject": f"[SLI] Correction: SN{sub['netuid']} {sub['name']}".replace(" ", "%20"),
        "alpha_row": (lambda t: f'<div class="srow" id="token"><span class="k">Token</span><span class="v"><a href="https://taostats.io/subnets/{sub["netuid"]}" target="_blank" rel="noopener"><b>{e(t.get("symbol") or "α")} {(t.get("price_tao") or 0):.4f} τ</b></a><span>{", ".join(sorted({v["name"] for v in (t.get("venues") or []) if v["kind"] == "exchange"})) or "on-chain only"}</span></span></div>' if t else "")(sub.get("alpha") or {}),
        "json": json.dumps({k: v for k, v in sub.items() if k != "alpha"}, ensure_ascii=False).replace("</", "<\\/"),
        "topbar": partials["topbar"], "nav": partials["nav"], "footer": partials["footer"], "robots": partials.get("robots", ""),
        "explainer": explainer_html, "explainer_css": explainer_css,
        "program": program_card(sub, entry), "says": says_sections(sub, narrative)[0], "said": says_sections(sub, narrative)[1],
        "narrative_css": narrative_css,
    }
    return fill(TEMPLATE.read_text(encoding="utf-8"), ctx)




# ---------------- OpenGraph images
def _font(name, size):
    from PIL import ImageFont
    for cand in ([name] if isinstance(name, str) else name):
        p = FONTS / cand
        if p.exists():
            try:
                f = ImageFont.truetype(str(p), size)
                if cand.startswith("InterTight"):
                    try:
                        f.set_variation_by_axes([600])  # wght
                    except Exception:
                        pass
                elif cand.startswith("IBMPlexSans"):
                    try:
                        f.set_variation_by_axes([100, 400])  # wdth, wght
                    except Exception:
                        pass
                return f
            except Exception:
                continue
    return ImageFont.load_default()


def og_canvas(kicker):
    """One card family for the whole site: header kicker, footer strip, shared palette and faces."""
    from PIL import Image, ImageDraw
    P = LIGHT
    img = Image.new("RGB", (1200, 630), P["bg"])
    d = ImageDraw.Draw(img)
    F = {"mono": _font(["IBMPlexMono-Medium.ttf", "IBMPlexMono-Regular.ttf"], 22), "mono_s": _font(["IBMPlexMono-Regular.ttf"], 18),
         "mono_xs": _font(["IBMPlexMono-Regular.ttf"], 14), "sans": _font(["IBMPlexSans.ttf"], 24), "pix": _font(["InterTight.ttf"], 26)}
    d.text((70, 60), kicker, font=F["mono"], fill=P["soft"])
    d.line([70, 566, 1130, 566], fill=P["rule"], width=2)
    d.text((70, 578), "Legible", font=_font(["InterTight.ttf"], 26), fill=P["ink"])
    d.text((1130 - d.textlength("Built by Mikyö Clark", font=F["sans"]), 578), "Built by Mikyö Clark", font=F["sans"], fill=P["soft"])
    return img, d, F, P


def _save(img, out_path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG", optimize=True)
    return True


def render_og(sub, out_path):
    """A subnet: name, legibility in its band colour, four audience bars."""
    try:
        img, d, F, P = og_canvas("LEGIBLE  ·  SUBNETS")
    except ImportError:
        return False
    d.text((70, 100), f"SN {sub['netuid']}  ·  RANK {sub['rank']} BY EMISSION  ·  {sub['emission_pct']} OF THE BLOCK REWARD", font=F["mono_s"], fill=P["softer"])
    name = sub["name"]
    size = 78
    while size > 40 and d.textlength(name, font=_font(["InterTight.ttf"], size)) > 640:
        size -= 6
    d.text((66, 150), name, font=_font(["InterTight.ttf"], size), fill=P["ink"])
    comp = float(sub["composite"])
    col = P["bands"][band(comp)]
    d.text((770, 100), f"{comp:.1f}", font=_font(["InterTight.ttf"], 190), fill=col)
    d.text((780, 300), f"/ 5  ·  LEGIBILITY  ·  {BAND_WORD[band(comp)].upper()}", font=F["mono_s"], fill=P["softer"])
    y = 360
    for a in AUD:
        v = float(sub["audiences"][a]["score"])
        d.text((70, y), AUD_LABEL[a].split(" and ")[0].upper(), font=F["mono_s"], fill=P["aud"][a])
        d.rectangle([260, y + 6, 1130, y + 16], fill=P["rule"])
        d.rectangle([260, y + 6, 260 + int(870 * v / 5), y + 16], fill=P["aud"][a])
        d.text((1140 - d.textlength(f"{v:.1f}", font=F["mono_s"]), y - 2), f"{v:.1f}", font=F["mono_s"], fill=P["ink"])
        y += 46
    return _save(img, out_path)


def render_index_og(data, out_path):
    """The index page: the question, and the five most legible subnets."""
    try:
        img, d, F, P = og_canvas("LEGIBLE  ·  SUBNETS")
    except ImportError:
        return False
    big = _font(["InterTight.ttf"], 74)
    d.text((66, 110), "Can a first-time reader", font=big, fill=P["ink"])
    d.text((66, 190), "understand this subnet", font=big, fill=P["ink"])
    d.text((66, 270), "in five minutes?", font=big, fill=P["teal"])
    top = sorted(data["subnets"], key=lambda s: -float(s["composite"]))[:5]
    y = 380
    for s in top:
        d.text((70, y), f"SN{s['netuid']:<4} {s['name'][:28]}", font=F["mono_s"], fill=P["soft"])
        d.text((640, y), f"{float(s['composite']):.1f}", font=F["mono_s"], fill=P["bands"][band(s["composite"])])
        y += 30
    d.text((760, 380), f"{len(data['subnets'])} subnets", font=F["mono_s"], fill=P["softer"])
    d.text((760, 410), f"snapshot {data.get('chain_snapshot', '')}", font=F["mono_s"], fill=P["softer"])
    d.text((760, 440), f"scale v{data.get('rubric_version', '')}", font=F["mono_s"], fill=P["softer"])
    return _save(img, out_path)


def render_default_og(data, out_path):
    """The site card: the argument, with the sealed-and-open grid."""
    try:
        img, d, F, P = og_canvas("LEGIBLE")
    except ImportError:
        return False
    big = _font(["InterTight.ttf"], 62)
    d.text((66, 108), "Ethereum made Bitcoin's", font=big, fill=P["ink"])
    d.text((66, 176), "money programmable.", font=big, fill=P["ink"])
    d.text((66, 244), "Bittensor makes the", font=big, fill=P["ink"])
    d.text((66, 312), "mining programmable.", font=big, fill=P["teal"])
    # the grid, across the lower band: three networks, two rows, sealed or open
    x0, y0, cw, rh, gap = 210, 426, 290, 44, 12
    heads = ["Bitcoin", "Ethereum", "Bittensor"]
    rows = [("The money", ["sealed", "open", "same as bitcoin"]), ("The mining", ["sealed", "sealed", "open"])]
    for j, h in enumerate(heads):
        d.text((x0 + j * (cw + gap) + 12, y0 - 24), h.upper(), font=F["mono_xs"], fill=P["ink"] if h == "Bittensor" else P["softer"])
    for i, (lab, cells) in enumerate(rows):
        y = y0 + i * (rh + gap)
        d.text((70, y + rh / 2 - 8), lab.upper(), font=F["mono_xs"], fill=P["softer"])
        for j, c in enumerate(cells):
            x = x0 + j * (cw + gap)
            if c == "open":
                d.rectangle([x, y, x + cw, y + rh], outline=P["teal"], width=3)
                d.text((x + 12, y + rh / 2 - 8), "OPEN", font=F["mono_xs"], fill=P["teal"])
            else:
                d.rectangle([x, y, x + cw, y + rh], fill=P["paper"], outline=P["rule"], width=2)
                d.text((x + 12, y + rh / 2 - 8), c.upper(), font=F["mono_xs"], fill=P["softer"])
    return _save(img, out_path)


# ---------------- chart
def render_chart(data):
    subs = data["subnets"]
    W, H, L, R, T, B = 960, 560, 60, 24, 24, 60
    xmax = max(float(s["emission_share"]) for s in subs) * 100
    xmax = (int(xmax) // 2 + 1) * 2 if xmax > 2 else 2
    def X(v): return L + (W - L - R) * (v / xmax)
    def Y(v): return T + (H - T - B) * (1 - v / 5)
    ems = sorted(float(s["emission_share"]) * 100 for s in subs)
    med_x = ems[len(ems) // 2]
    comps = sorted(float(s["composite"]) for s in subs)
    med_y = comps[len(comps) // 2]
    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="height:auto;display:block" role="img" aria-label="Legibility against emission share" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" font-family="var(--mono)" font-size="11">']
    for v in range(0, 6):
        out.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{W - R}" y2="{Y(v):.1f}" stroke="var(--rule)" stroke-width="1"/><text x="{L - 10}" y="{Y(v) + 4:.1f}" text-anchor="end" fill="var(--softer)">{v}</text>')
    step = max(1, int(xmax / 6))
    for v in range(0, int(xmax) + 1, step):
        out.append(f'<text x="{X(v):.1f}" y="{H - B + 20}" text-anchor="middle" fill="var(--softer)">{v}%</text>')
    out.append(f'<text x="{(L + W - R) / 2:.1f}" y="{H - 14}" text-anchor="middle" fill="var(--soft)">share of TAO emission</text>')
    out.append(f'<text transform="translate(14 {(T + H - B) / 2:.1f}) rotate(-90)" text-anchor="middle" fill="var(--soft)">legibility score</text>')
    out.append(f'<line x1="{X(med_x):.1f}" y1="{T}" x2="{X(med_x):.1f}" y2="{H - B}" stroke="var(--rule-strong)" stroke-dasharray="4 4"/>')
    out.append(f'<line x1="{L}" y1="{Y(med_y):.1f}" x2="{W - R}" y2="{Y(med_y):.1f}" stroke="var(--rule-strong)" stroke-dasharray="4 4"/>')
    out.append(f'<text x="{W - R - 6}" y="{T + 14}" text-anchor="end" fill="var(--softer)" class="quad">high emission, high legibility</text>')
    out.append(f'<text x="{W - R - 6}" y="{H - B - 8}" text-anchor="end" fill="var(--softer)" class="quad">high emission, low legibility</text>')
    out.append(f'<text x="{L + 6}" y="{T + 14}" fill="var(--softer)" class="quad">low emission, high legibility</text>')
    for series, key, color in (("composite", None, "var(--teal)"), ("buyers", "buyers", "var(--a-buyers)")):
        out.append(f'<g data-series="{series}">')
        for s in subs:
            y = float(s["composite"]) if key is None else float(s["audiences"][key]["score"])
            x = float(s["emission_share"]) * 100
            out.append(f'<a xlink:href="/sn/{s["netuid"]}/" href="/sn/{s["netuid"]}/"><g class="pt"><circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="6" fill="{color}" fill-opacity=".85" stroke="var(--bg)" stroke-width="1.5"/>'
                       f'<text x="{X(x) + 8:.1f}" y="{Y(y) + 4:.1f}" fill="var(--soft)">{s["netuid"]}</text><title>SN{s["netuid"]} {html.escape(s["name"])}: {series} {y:.1f}, emission {x:.1f}%</title></g></a>')
        out.append("</g>")
    out.append("</svg>")
    # gaps lists
    by_comp = sorted(subs, key=lambda s: -float(s["composite"]))
    crank = {s["netuid"]: i + 1 for i, s in enumerate(by_comp)}
    gaps = sorted(subs, key=lambda s: s["rank"] - crank[s["netuid"]])
    def li(s):
        return f'<li><a href="/sn/{s["netuid"]}/">SN{s["netuid"]} {e(s["name"])}</a> <span class="mono" style="letter-spacing:0">emission #{s["rank"]} · legibility #{crank[s["netuid"]]}</span></li>'
    high_em_low_leg = [s for s in gaps if s["rank"] - crank[s["netuid"]] < 0][:8]
    low_em_high_leg = [s for s in reversed(gaps) if s["rank"] - crank[s["netuid"]] > 0][:8]
    lists = (f'<div class="gaps"><div><span class="mono">Paid more than they explain</span><ol>{"".join(li(s) for s in high_em_low_leg)}</ol></div>'
             f'<div><span class="mono">Explain more than they are paid</span><ol>{"".join(li(s) for s in low_em_high_leg)}</ol></div></div>')
    controls = ('<div class="seg chart-seg" role="group" aria-label="Series"><button data-series="composite" class="on">Composite</button>'
                '<button data-series="buyers">Buyers</button><button data-series="both">Both</button></div>')
    style = ('<style>figure.chart{margin:16px 0}figure.chart[data-show=composite] g[data-series=buyers]{display:none}figure.chart[data-show=buyers] g[data-series=composite]{display:none}'
             '.gaps{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:10px}.gaps ol{padding-left:22px;line-height:1.8;font-size:13.5px}'
             '@media (max-width:600px){.gaps{grid-template-columns:1fr}svg .pt text,svg .quad{display:none}svg circle{r:8}}</style>')
    script = ('<script>(function(){const f=document.querySelector("figure.chart");document.querySelectorAll(".chart-seg button").forEach(b=>b.onclick=()=>{'
              'document.querySelectorAll(".chart-seg button").forEach(x=>x.classList.toggle("on",x===b));f.dataset.show=b.dataset.series;});})();</script>')
    return style + controls + f'<figure class="chart" data-show="composite">{"".join(out)}</figure>' + lists + script


def build_all(data, partials, site, write_if_changed, explainers=None, narrative_blocks=None, narrative_css="", entries=None):
    """Render subnet pages, the list, OG images, and return (changed list, chart html)."""
    changed = []
    subs = sorted(data["subnets"], key=lambda s: s["rank"])
    og_ok = None
    for i, sub in enumerate(subs):
        og_name = f"{sub['netuid']}.png"
        if og_ok is not False:
            ok = render_og(sub, OG_DIR / og_name)
            og_ok = ok if og_ok is None else (og_ok and ok)
            if not ok:
                og_name = "default.png"
        else:
            og_name = "default.png"
        ex_html, ex_css = (explainers or {}).get(sub["netuid"], ("", ""))
        nb = (narrative_blocks or {}).get(sub["netuid"])
        page = render_subnet(sub, data, partials, site, subs[i - 1] if i > 0 else None, subs[i + 1] if i + 1 < len(subs) else None, og_name, ex_html, ex_css, nb, narrative_css, (entries or {}).get(sub["netuid"]))
        if write_if_changed(REPO / "sn" / str(sub["netuid"]) / "index.html", page):
            changed.append(f"sn/{sub['netuid']}/")
    if render_default_og(data, OG_DIR / "default.png"):
        changed.append("assets/og/default.png")
    if render_index_og(data, OG_DIR / "subnets.png"):
        changed.append("assets/og/subnets.png")
    if og_ok is False:
        print("  Pillow missing or font error: subnet OG images skipped, default card used", file=__import__("sys").stderr)
    return changed, render_chart(data)
