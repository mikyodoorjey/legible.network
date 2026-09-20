#!/usr/bin/env python3
"""Mining Programs: load the raw manifests, merge them into data/programs.json, render the blocks.

A manifest is a subnet's puzzle written as a spec (see agents/PROGRAM-PROMPT.md):
seven fields, each with a source and a trust level naming what kind of thing the
claim rests on. This module is imported by build_site.py and render_subnets.py.

Usage as a script: python3 scripts/programs.py   (merge only; prints the summary)
"""
import html
import json
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
RAW = DATA / "programs" / "raw"
TODAY = date.today().isoformat()

FIELDS = ["work", "scoring", "split", "judges", "cadence", "buyer", "exploits"]
FIELD_LABEL = {
    "work": "The work",
    "scoring": "How it is scored",
    "split": "How the pay splits",
    "judges": "Who judges",
    "cadence": "How often it turns",
    "buyer": "Who buys",
    "exploits": "What has been gamed",
}
FIELD_QUESTION = {
    "work": "What is a miner paid to produce?",
    "scoring": "How does a validator judge it, and against what?",
    "split": "How does the miner share divide between miners?",
    "judges": "Who validates, how many, and what may they do?",
    "cadence": "How often does the puzzle turn?",
    "buyer": "Who pays for the output today?",
    "exploits": "What have miners optimized instead of the work?",
}
TRUST = ["chain", "code", "docs", "said", "read", "unknown"]
TRUST_LABEL = {
    "chain": "chain",
    "code": "code",
    "docs": "own docs",
    "said": "on record",
    "read": "our reading",
    "unknown": "not found",
}
TRUST_DEF = {
    "chain": "a value read from the chain",
    "code": "read in the subnet's repository at the pinned commit",
    "docs": "the subnet's own prose: README, docs, site, paper",
    "said": "a statement in the narrative map",
    "read": "the site's own inference from code, absence, or a third party",
    "unknown": "looked for and not found",
}
STRONG = ("chain", "code")
LICENSE = "CC BY 4.0"
ATTRIBUTION = "Mining Programs by Mikyö Clark, legible.network"


def e(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def host(url):
    try:
        return url.split("/")[2].replace("www.", "")
    except Exception:  # noqa
        return url


def load_programs(raw_dir=None):
    """netuid -> manifest, from data/programs/raw/*.json. Files that are not valid JSON are skipped with a warning."""
    raw_dir = Path(raw_dir) if raw_dir else RAW
    out = {}
    if not raw_dir.exists():
        return out
    for p in sorted(raw_dir.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            out[int(d["netuid"])] = d
        except Exception as ex:  # noqa
            print(f"  programs: skipped {p.name}: {ex}", file=sys.stderr)
    return out


def trust_of(m, field):
    return ((m.get("fields") or {}).get(field) or {}).get("trust", "unknown")


def strength(m):
    """How many of the seven fields rest on chain or code."""
    return sum(1 for f in FIELDS if trust_of(m, f) in STRONG)


def disagreements(m):
    return [(f, m["fields"][f]["disagrees"]) for f in FIELDS if (m.get("fields") or {}).get(f, {}).get("disagrees")]


def unknowns(m):
    return [f for f in FIELDS if trust_of(m, f) == "unknown"]


def first_sentence(text):
    t = (text or "").strip()
    for i, ch in enumerate(t):
        if ch in ".!?" and (i + 1 == len(t) or t[i + 1] == " "):
            return t[: i + 1]
    return t


def merge(programs, subnets=None):
    """The published dataset. `subnets` (from index.json) adds name, emission and rank when present."""
    by_uid = {s["netuid"]: s for s in (subnets or [])}
    items = []
    counts = {t: 0 for t in TRUST}
    n_dis = n_unk = 0
    for uid in sorted(programs, key=lambda u: by_uid.get(u, {}).get("rank", 999)):
        m = programs[uid]
        s = by_uid.get(uid, {})
        for f in FIELDS:
            counts[trust_of(m, f)] += 1
        n_dis += len(disagreements(m))
        n_unk += len(unknowns(m))
        item = dict(m)
        item["rank"] = s.get("rank")
        item["emission_pct"] = s.get("emission_pct")
        item["strength"] = strength(m)
        items.append(item)
    return {
        "generated_at": TODAY,
        "version": "1.0",
        "license": LICENSE,
        "attribution": ATTRIBUTION,
        "fields": FIELDS,
        "field_labels": FIELD_LABEL,
        "trust": TRUST,
        "trust_labels": TRUST_LABEL,
        "total": len(items),
        "summary": {"fields": counts, "disagreements": n_dis, "unknowns": n_unk,
                    "from_chain_or_code": counts["chain"] + counts["code"]},
        "programs": items,
    }


def write_merged(programs, subnets, write_if_changed):
    out = merge(programs, subnets)
    text = json.dumps(out, ensure_ascii=False, indent=1)
    changed = write_if_changed(DATA / "programs.json", text)
    return out, changed


# ---------------- rendering

def trust_badge(t):
    return f'<span class="badge trust-{e(t)}" title="{e(TRUST_DEF.get(t, ""))}">{e(TRUST_LABEL.get(t, t))}</span>'


def trust_dots(m):
    """Seven dots, one per field in order, coloured by trust. Title carries the field and trust."""
    dots = "".join(
        f'<i class="tdot trust-{e(trust_of(m, f))}" title="{e(FIELD_LABEL[f])}: {e(TRUST_LABEL.get(trust_of(m, f), ""))}"></i>'
        for f in FIELDS)
    return f'<span class="tdots" aria-label="{strength(m)} of 7 fields from chain or code">{dots}</span>'


def source_line(f, m):
    """The evidence under a field: trust badge, the source, the quote."""
    t = f.get("trust", "unknown")
    parts = [trust_badge(t)]
    if t == "chain":
        snap = f.get("snapshot", "")
        parts.append(f'<a href="/{e(snap)}">{e(Path(snap).name)}</a>')
    elif f.get("url"):
        parts.append(f'<a href="{e(f["url"])}" target="_blank" rel="noopener">{e(host(f["url"]))}</a>')
    if t == "code" and f.get("path"):
        parts.append(f'<code>{e(f["path"])}</code>')
    if t == "said" and f.get("statement"):
        sid = f["statement"]
        nid = sid.rsplit("-", 1)[0]
        href = f"/sn/{m['netuid']}/#{e(sid)}" if nid.startswith("sn") else f"/narrative/{e(nid)}/#{e(sid)}"
        parts.append(f'<a href="{href}">{e(sid)}</a>')
    line = '<p class="src">' + " · ".join(parts) + "</p>"
    if f.get("quote"):
        line += f'<p class="quote">{e(f["quote"])}</p>'
    if f.get("disagrees"):
        line += f'<p class="dis"><span class="mono">Sources disagree</span> {e(f["disagrees"])}</p>'
    return line


def issue_url(m):
    name = e(m.get("name", "")).replace(" ", "%20")
    return f"https://github.com/mikyodoorjey/legible.network/issues/new?template=correction.yml&title=%5BCorrection%5D%20SN{m['netuid']}%20{name}%20program"


def changelog_items(programs):
    """Method-page changelog lines for program corrections, newest first."""
    items = []
    for uid, m in programs.items():
        for c in m.get("corrections") or []:
            items.append((c.get("date", ""), f'<li><span class="mono">{e(c.get("date", ""))} · program</span> '
                          f'<a href="/sn/{uid}/#program">SN{uid} {e(m.get("name", ""))}</a> {e(c.get("field", ""))}: '
                          f'{e(c.get("old_trust", ""))} to {e(c.get("new_trust", ""))}. {e(c.get("reason", ""))}'
                          f'{(" Requested by " + e(c["requested_by"]) + ".") if c.get("requested_by") else ""}</li>'))
    return "".join(h for _, h in sorted(items, reverse=True))


def program_card(m, sub=None):
    """The subnet page block: seven rows from the manifest."""
    repo = m.get("repo") or {}
    head = [f'<span class="mono">The program</span>']
    meta = [e(m.get("commodity", ""))]
    if repo.get("commit"):
        meta.append(f'<a href="{e(repo["url"])}/tree/{e(repo["commit"])}" target="_blank" rel="noopener" title="read at this commit, dated {e(repo.get("committed", ""))}">{e(host(repo["url"]))}@{e(repo["commit"][:7])}</a>')
    meta.append(f'read {e(m.get("read_on", ""))}')
    head.append('<span class="sm">' + " · ".join(meta) + "</span>")
    rows = []
    for name in FIELDS:
        f = (m.get("fields") or {}).get(name) or {"text": "", "trust": "unknown"}
        rows.append(
            f'<div class="pf trust-{e(f.get("trust", "unknown"))}" data-f="{name}"><span class="mono" title="{e(FIELD_QUESTION[name])}">{e(FIELD_LABEL[name])}</span>'
            f'<div><p>{e(f.get("text", ""))}</p>{source_line(f, m)}</div></div>')
    foot = (f'<p class="sm pfoot">{strength(m)} of 7 fields rest on the chain or the code. '
            f'A manifest is the site\'s reading of the subnet\'s program, not a review; each field links its source. '
            f'<a href="/programs/">All programs</a> · <a href="/method/#the-programs-what-they-record">What a field means</a> · '
            f'<a href="{issue_url(m)}">Correct a field</a></p>')
    drift = DRIFT_JS.replace("__UID__", str(m["netuid"])) if repo.get("commit") else ""
    return (f'<section class="program" id="program"><div class="pg-head">{"".join(head)}</div>'
            f'{"".join(rows)}{foot}{drift}</section>')


DRIFT_JS = """<script>
(function(){
  var el=document.getElementById('program');if(!el)return;
  fetch('/data/programs-drift.json').then(function(r){return r.ok?r.json():null}).then(function(d){
    if(!d||!d.programs)return;var p=d.programs['__UID__'];if(!p||p.error||!p.ahead_by)return;
    var f=el.querySelector('.pfoot');
    var msg='Code moved '+p.ahead_by+' commit'+(p.ahead_by===1?'':'s')+' since this reading, checked '+d.checked_at+
      (p.stale_fields&&p.stale_fields.length?'; the file behind '+p.stale_fields.join(', ')+' changed, so that field may be stale.':'; the cited files are unchanged.');
    if(f)f.insertAdjacentHTML('afterbegin','<span class="drift">'+msg+'</span> ');
    (p.stale_fields||[]).forEach(function(k){var row=el.querySelector('.pf[data-f="'+k+'"] .src');if(row)row.insertAdjacentHTML('beforeend','<span class="badge stale">stale</span>')});
  }).catch(function(){});
})();
</script>"""


PROGRAM_CSS = """
.program .pf>div{min-width:0}
.program .pf p{margin:0;font-size:16px;color:var(--ink);line-height:1.5}
.program .pf .src{margin-top:6px;font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;color:var(--soft);display:flex;gap:8px;flex-wrap:wrap;align-items:baseline}
.program .pf .src code{font-family:var(--mono);font-size:10.5px;letter-spacing:0;color:var(--soft)}
.program .pf .quote{margin-top:4px;font-size:13.5px;color:var(--ink-soft);font-style:italic;line-height:1.45}
.program .pf .quote::before{content:"\\201C"}.program .pf .quote::after{content:"\\201D"}
.program .pf .dis{margin-top:6px;font-size:13.5px;color:var(--ink-soft);line-height:1.45;border-left:2px solid var(--rule-strong);padding-left:10px}
.program .pf .dis .mono{display:block;margin-bottom:2px;color:var(--ink)}
.program .pfoot{padding:12px 0 0;max-width:70ch}
"""


def home_cards(programs, subnets, entries=None, n=6):
    """Six cards for the home page close: the work as the program reads it, block reward, legibility, trust."""
    cards = []
    for sub in sorted(subnets, key=lambda s: s["rank"]):
        m = programs.get(sub["netuid"])
        ent = (entries or {}).get(sub["netuid"])
        if not m and not ent:
            continue
        commodity = (m or {}).get("commodity") or ((ent or {}).get("fm") or {}).get("commodity", "")
        work = (m or {}).get("fields", {}).get("work", {}).get("text") if m else ((ent or {}).get("fm") or {}).get("one_sentence", "")
        row = f'<span>block reward <b>{e(sub["emission_pct"])}</b></span><span>legibility <b>{float(sub["composite"]):.1f}</b> of 5</span>'
        if m:
            row += f'<span>program {trust_dots(m)} <b>{strength(m)}</b> of 7 from chain or code</span>'
        cards.append(
            f'<a class="prog" href="/sn/{sub["netuid"]}/#program"><div class="h"><b>{e(sub["name"])}</b><span>SN{sub["netuid"]} · {e(commodity)}</span></div>'
            f'<p class="work">{e(work)}</p><div class="row">{row}</div></a>')
        if len(cards) >= n:
            break
    return '<div class="programs">' + "".join(cards) + "</div>"


def list_rows(merged):
    """Rows for /programs/: one per subnet, the four fields a buyer or validator reads first, then the trust strip."""
    rows = []
    for m in merged["programs"]:
        f = m.get("fields") or {}
        cells = "".join(
            f'<td class="f trust-{e(trust_of(m, k))}"><p data-l="{e(FIELD_LABEL[k])}">{e(first_sentence(f.get(k, {}).get("text", "")))}</p>{trust_badge(trust_of(m, k))}</td>'
            for k in ("work", "scoring", "split", "buyer"))
        ndis = len(disagreements(m))
        rows.append(
            f'<tr class="row" data-uid="{m["netuid"]}">'
            f'<td class="rank">{e(m.get("rank") or "")}</td>'
            f'<td class="name"><span class="nm"><a href="/sn/{m["netuid"]}/#program">{e(m["name"])}</a><span class="sn">SN{m["netuid"]} · {e(m.get("commodity", ""))}</span></span>'
            f'<span class="em">{e(m.get("emission_pct") or "")} of emission</span></td>'
            f'{cells}'
            f'<td class="trust">{trust_dots(m)}<span class="k">{strength(m)} of 7</span>'
            f'{("<span class=\"k dis\">" + str(ndis) + (" disagreement" if ndis == 1 else " disagreements") + "</span>") if ndis else ""}'
            f'<span class="k">read {e(m.get("read_on", ""))}</span></td></tr>')
    return "".join(rows)


def list_stats(merged):
    s = merged["summary"]
    total_fields = merged["total"] * len(FIELDS) or 1
    return (f'<div><b>{merged["total"]}</b><span>programs read</span></div>'
            f'<div><b>{round(100 * s["from_chain_or_code"] / total_fields)}%</b><span>of fields from chain or code</span></div>'
            f'<div><b>{s["disagreements"]}</b><span>places the sources disagree</span></div>'
            f'<div><b>{s["unknowns"]}</b><span>fields not found</span></div>')


def main():
    programs = load_programs()
    idx = DATA / "index.json"
    subs = json.loads(idx.read_text(encoding="utf-8"))["subnets"] if idx.exists() else []
    out = merge(programs, subs)
    (DATA / "programs.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out["summary"]), file=sys.stderr)
    print(f"wrote data/programs.json: {out['total']} programs", file=sys.stderr)


if __name__ == "__main__":
    main()
