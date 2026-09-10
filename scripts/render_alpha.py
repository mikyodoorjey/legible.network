#!/usr/bin/env python3
"""Alpha token pages: /alpha/<netuid>/ and the /alpha/ list. Imported by build_site.py."""
import html
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def e(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def money(v, unit="", digits=2):
    if v is None:
        return "n/a"
    if unit == "$":
        return f"${v:,.{digits}f}" if v >= 1 else f"${v:.4f}"
    return f"{v:,.{digits}f} {unit}".strip()


def tao(v, digits=4):
    return "n/a" if v is None else f"{v:,.{digits}f} τ"


def pct(v):
    if v is None:
        return '<span class="sm">n/a</span>'
    cls = "up" if v > 0 else ("down" if v < 0 else "")
    return f'<span class="chg {cls}">{v:+.1f}%</span>'


def head(title, description, canonical, partials, site, extra_css=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · Subnet Legibility Index</title>
{partials.get("robots", "")}
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{site}{canonical}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:url" content="{site}{canonical}">
<meta property="og:title" content="{e(title)} · Subnet Legibility Index">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{site}/assets/og/default.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@9..144,300..700,30..100,0..1&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<style>
.alpha{{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:40px;align-items:start;padding-top:32px}}
.sym{{font-family:var(--serif);font-size:72px;line-height:1;font-variation-settings:"opsz" 144,"SOFT" 60}}
.price{{font-family:var(--mono);font-size:30px;margin:8px 0 2px}}
.price small{{font-size:14px;color:var(--soft);margin-left:8px}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:22px 0}}
.stat{{border:1px solid var(--rule);border-radius:6px;padding:10px 12px;background:var(--paper)}}
.stat .k{{font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--softer)}}
.stat .v{{font-family:var(--mono);font-size:16px;margin-top:4px}}
.chg.up{{color:var(--b4)}}.chg.down{{color:var(--b0)}}
.venues{{margin:10px 0 0}}
.venue{{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:10px 0;border-top:1px solid var(--rule)}}
.venue:first-child{{border-top:0}}
.venue .n{{font-weight:500}}
.venue .n small{{font-family:var(--mono);font-size:11px;color:var(--softer);margin-left:8px}}
.venue a.go{{padding:6px 10px;border:1px solid var(--rule-strong);border-radius:6px;font-size:12.5px;white-space:nowrap}}
.venue a.go:hover{{border-color:var(--teal);text-decoration:none}}
.card{{position:sticky;top:20px;border:1px solid var(--rule);border-radius:8px;background:var(--paper);padding:18px 20px}}
.card .row{{display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-top:1px solid var(--rule);font-size:13.5px}}
.card .row:first-of-type{{border-top:0}}
.card .actions{{display:flex;flex-direction:column;gap:8px;margin-top:14px}}
.card .actions a{{display:block;text-align:center;padding:8px 10px;border:1px solid var(--rule-strong);border-radius:6px;font-size:13px;color:var(--ink-soft)}}
.card .actions a.primary{{border-color:var(--teal);color:var(--teal)}}
.note{{font-size:13px;color:var(--soft);max-width:70ch}}
.list{{padding:0;list-style:none;margin:16px 0 0}}
.list li{{display:grid;grid-template-columns:70px minmax(0,1fr) 120px 140px 1fr;gap:12px;align-items:baseline;padding:9px 0;border-top:1px solid var(--rule);font-size:14px}}
.list li.h{{font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--softer);border-top:0}}
.list .mono{{letter-spacing:0;text-transform:none;font-size:13px;color:var(--ink)}}
@media (max-width:820px){{.alpha{{grid-template-columns:1fr}}.card{{position:static}}.list li{{grid-template-columns:60px 1fr 100px}}.list li span:nth-child(n+4){{display:none}}}}
{extra_css}
</style>
</head>
<body>
{partials["topbar"]}
{partials["nav"]}
"""


def render_alpha(sub, data, partials, site):
    t = sub.get("alpha") or {}
    nid = sub["netuid"]
    name = sub["name"]
    sym = t.get("symbol") or "α"
    venues = t.get("venues") or []
    onchain = [v for v in venues if v["kind"] == "on-chain"]
    exch = [v for v in venues if v["kind"] == "exchange"]
    def vrow(v):
        pair = f"<small>{e(v.get('pair', ''))}</small>" if v.get("pair") else ""
        return (f'<div class="venue"><div><span class="n">{e(v["name"])}{pair}</span><div class="sm">{e(v.get("note", ""))} · <span class="badge {e(v.get("source", "stated"))}">{e(v.get("source", "stated"))}</span></div></div>'
                f'<a class="go" href="{e(v["url"])}" target="_blank" rel="noopener">Open</a></div>')
    staked = t.get("alpha_staked") or 0
    in_pool = t.get("alpha_in_pool") or 0
    total = t.get("total_alpha") or (staked + in_pool)
    staked_pct = (staked / total * 100) if total else None
    description = (f"SN{nid} {name} alpha token: {tao(t.get('price_tao'))} ({money(t.get('price_usd'), '$')}), market cap {tao(t.get('market_cap_tao'), 0)}, "
                   f"{len(exch)} exchange listing{'s' if len(exch) != 1 else ''}. Where it trades and what the subnet says about itself.")
    out = [head(f"{sym} {name} alpha token", description, f"/alpha/{nid}/", partials, site)]
    out.append(f"""<main class="wrap alpha">
  <div>
    <span class="mono">SN {nid} · alpha token · pool rank {e(t.get('pool_rank', '?'))} by market cap</span>
    <div style="display:flex;gap:18px;align-items:baseline;flex-wrap:wrap"><span class="sym">{e(sym)}</span><h1>{e(name)}</h1></div>
    <div class="price">{tao(t.get('price_tao'))}<small>{money(t.get('price_usd'), '$')} at TAO {money(data.get('tao_usd'), '$')}</small></div>
    <div class="sm">{pct(t.get('change_1d'))} 24h · {pct(t.get('change_1w'))} 7d · {pct(t.get('change_1m'))} 30d · as of {e((t.get('as_of') or '')[:16].replace('T', ' '))} UTC</div>
    <div class="stats">
      <div class="stat"><div class="k">Market cap</div><div class="v">{tao(t.get('market_cap_tao'), 0)}</div><div class="sm">{money(t.get('market_cap_usd'), '$', 0)}</div></div>
      <div class="stat"><div class="k">Pool liquidity</div><div class="v">{tao(t.get('liquidity_tao'), 0)}</div></div>
      <div class="stat"><div class="k">24h volume</div><div class="v">{tao(t.get('volume_24h_tao'), 0)}</div></div>
      <div class="stat"><div class="k">Staked vs in pool</div><div class="v">{f"{staked_pct:.0f}%" if staked_pct is not None else 'n/a'}</div><div class="sm">of {total:,.0f} alpha staked</div></div>
      <div class="stat"><div class="k">Emission share</div><div class="v">{e(sub.get('emission_pct'))}</div><div class="sm">rank {sub['rank']} of {len(data['subnets'])}</div></div>
      <div class="stat"><div class="k">Legibility</div><div class="v band-{int(float(sub['composite']))}">{float(sub['composite']):.1f} / 5</div><div class="sm">rank {sub.get('composite_rank', '?')} of {len(data['subnets'])}</div></div>
    </div>

    <h2>Where it trades</h2>
    <p class="note">Every alpha token is minted by staking TAO into its subnet's pool, so the on-chain venues below work for all of them. Exchange listings are read from the exchanges' own market lists on the snapshot date; absence here means no listing was found, not that none exists.</p>
    <h3 style="margin-top:18px">Exchanges</h3>
    <div class="venues">{"".join(vrow(v) for v in exch) if exch else '<p class="sm">No exchange listing found for SN' + str(nid) + ' on Kraken, MEXC, or CoinGecko on the snapshot date.</p>'}</div>
    <h3 style="margin-top:22px">On-chain</h3>
    <div class="venues">{"".join(vrow(v) for v in onchain)}</div>

    <h2 style="margin-top:32px">What the subnet says it is</h2>
    {('<p class="quote">' + e(sub["own_words"]["quote"]) + '</p><span class="sm">In their own words · <a href="' + e(sub["own_words"]["url"]) + '" target="_blank" rel="noopener">source</a></span>') if (sub.get("own_words") or {}).get("quote") else '<p class="sm">No self-description found.</p>'}
    <p class="note" style="margin-top:14px">Prices and pool figures are from Taostats; this page is not investment advice and the index does not score token quality. The legibility score measures what a reader can find, not what the token is worth.</p>
  </div>
  <aside class="card">
    <div class="row"><span>Subnet</span><a href="/sn/{nid}/">SN{nid} {e(name)}</a></div>
    <div class="row"><span>Symbol</span><b class="mono" style="letter-spacing:0;font-size:16px;color:var(--ink)">{e(sym)}</b></div>
    <div class="row"><span>Price</span><b class="mono" style="letter-spacing:0;color:var(--ink)">{tao(t.get('price_tao'))}</b></div>
    <div class="row"><span>Listings</span><b class="mono" style="letter-spacing:0;color:var(--ink)">{len(exch)} exchange{'s' if len(exch) != 1 else ''}</b></div>
    <div class="actions">
      <a class="primary" href="/sn/{nid}/">Legibility evidence</a>
      <a href="https://tao.app/subnets/{nid}" target="_blank" rel="noopener">Stake on tao.app</a>
      <a href="/alpha/">All alpha tokens</a>
    </div>
  </aside>
</main>
{partials["footer"]}
<script type="application/json" id="alpha-data">{json.dumps(t, ensure_ascii=False).replace("</", "<\\/")}</script>
</body>
</html>
""")
    return "".join(out)


def render_alpha_list(data, partials, site):
    subs = sorted(data["subnets"], key=lambda s: -((s.get("alpha") or {}).get("market_cap_tao") or 0))
    rows = []
    for s in subs:
        t = s.get("alpha") or {}
        exch = [v["name"] for v in (t.get("venues") or []) if v["kind"] == "exchange"]
        rows.append(f'<li><span class="mono">{e(t.get("symbol") or "α")}</span><span><a href="/alpha/{s["netuid"]}/">{e(s["name"])}</a> <span class="sm">SN{s["netuid"]}</span></span>'
                    f'<span class="mono">{tao(t.get("price_tao"))}</span><span class="mono">{tao(t.get("market_cap_tao"), 0)}</span><span class="sm">{e(", ".join(sorted(set(exch))) or "on-chain only")}</span></li>')
    body = (head("Alpha tokens", "Every alpha token in the index: price, market cap, and where it trades.", "/alpha/", partials, site) +
            f'<main class="wrap" style="padding-top:32px"><span class="mono">By pool market cap · TAO {money(data.get("tao_usd"), "$")}</span><h1>Alpha tokens</h1>'
            f'<p class="note">One token per subnet, minted by staking TAO into the subnet pool. Exchange listings are read from Kraken, MEXC, and CoinGecko on the snapshot date.</p>'
            f'<ul class="list"><li class="h"><span>Symbol</span><span>Subnet</span><span>Price</span><span>Market cap</span><span>Listed on</span></li>{"".join(rows)}</ul></main>'
            f'{partials["footer"]}</body></html>\n')
    return body


def build_alpha(data, partials, site, write_if_changed):
    changed = []
    if not any(s.get("alpha") for s in data["subnets"]):
        return changed
    for s in data["subnets"]:
        if write_if_changed(REPO / "alpha" / str(s["netuid"]) / "index.html", render_alpha(s, data, partials, site)):
            changed.append(f"alpha/{s['netuid']}/")
    if write_if_changed(REPO / "alpha" / "index.html", render_alpha_list(data, partials, site)):
        changed.append("alpha/index.html")
    return changed
