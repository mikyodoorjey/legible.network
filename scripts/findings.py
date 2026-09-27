"""Findings: counts computed from the three datasets, and the allocator table.

Nothing here is a reading. Every sentence is a count over data/index.json, data/programs.json,
and data/narrative.json, with the rule written next to it and a link to the rows it was counted from.
build_site.py calls compute() once and injects home_block(), page_list(), page_stats(), and page_rows().
"""
import json
import re
import statistics

from programs import FIELDS, FIELD_LABEL, TRUST_LABEL, disagreements, e, first_sentence, strength, trust_badge, trust_dots, trust_of

NO_BUYER = re.compile(r"^(Nobody|No paying|Unknown)\b")
DELTA_OPEN = 10  # places between emission rank and legibility rank that count as a delta worth questioning


def buyer_named(m):
    """The rule: a buyer is named unless the field starts Nobody, No paying, or Unknown, or was not found."""
    f = (m.get("fields") or {}).get("buyer") or {}
    if f.get("trust", "unknown") == "unknown":
        return False
    return not NO_BUYER.match((f.get("text") or "").strip())


def band(v):
    try:
        return max(0, min(5, int(float(v))))
    except (TypeError, ValueError):
        return 0


def compute(data, pmerged, ndata):
    subs = sorted(data["subnets"], key=lambda s: s["rank"])
    total = len(subs)
    programs = {m["netuid"]: m for m in (pmerged or {}).get("programs", [])}
    rows = []
    for s in subs:
        m = programs.get(s["netuid"]) or {}
        f = (m.get("fields") or {})
        buyers = s["audiences"].get("buyers", {})
        ident = s.get("identity_completeness") or {}
        rows.append({
            "netuid": s["netuid"], "name": s["name"], "commodity": m.get("commodity", ""),
            "emission_rank": s["rank"], "emission_pct": s.get("emission_pct", ""),
            "legibility": s["composite"], "legibility_rank": s.get("composite_rank"),
            "delta": (s.get("composite_rank") or s["rank"]) - s["rank"],
            "buyers_score": buyers.get("score"), "buyers_rank": buyers.get("rank"),
            "buyer_named": buyer_named(m) if m else None,
            "buyer_text": first_sentence((f.get("buyer") or {}).get("text", "")) if m else "",
            "buyer_trust": trust_of(m, "buyer") if m else "unknown",
            "disagreements": len(disagreements(m)) if m else 0,
            "fields_from_chain_or_code": strength(m) if m else 0,
            "identity_filled": ident.get("filled"), "identity_of": ident.get("of"),
            "read_on": m.get("read_on", ""),
            "trust_html": trust_dots(m) if m else "",
        })
    read = [r for r in rows if r["buyer_named"] is not None]
    no_buyer = [r for r in read if not r["buyer_named"]]
    top10 = [r for r in read if r["emission_rank"] <= 10]
    top10_no_buyer = [r for r in top10 if not r["buyer_named"]]
    dis_total = sum(r["disagreements"] for r in rows)
    dis_subnets = sum(1 for r in rows if r["disagreements"])
    nfields = len(programs) * len(FIELDS) or 1
    from_cc = sum(r["fields_from_chain_or_code"] for r in rows)
    unknown_fields = sum(1 for m in programs.values() for k in FIELDS if trust_of(m, k) == "unknown")
    means = data["summary"]["audience_means"]
    lo, hi = min(subs, key=lambda s: s["composite"]), max(subs, key=lambda s: s["composite"])
    median = statistics.median(s["composite"] for s in subs)
    big_delta = [r for r in rows if r["delta"] >= DELTA_OPEN]
    ident_full = sum(1 for r in rows if r["identity_filled"] is not None and r["identity_filled"] == r["identity_of"])
    exploits_code = sum(1 for m in programs.values() if trust_of(m, "exploits") == "code")
    exploits_any = sum(1 for m in programs.values() if trust_of(m, "exploits") != "unknown")
    nsum = (ndata or {}).get("summary") or {}
    verified = (nsum.get("confidence") or {}).get("verified", 0)
    statements = nsum.get("statements", 0)
    read_dates = sorted({r["read_on"] for r in rows if r["read_on"]})
    when = " and ".join(read_dates[:1] + read_dates[-1:]) if len(read_dates) > 1 else "".join(read_dates)

    findings = [
        {"id": "no-buyer", "n": len(no_buyer), "of": len(read),
         "text": f"{len(no_buyer)} of {len(read)} name no paying buyer today.",
         "rule": f"the buyer field of each program, read from the subnet's own materials on {when}; counted when it starts Nobody, No paying, or Unknown, or was not found",
         "href": "/findings/#table"},
        {"id": "top-ten-no-buyer", "n": len(top10_no_buyer), "of": len(top10),
         "text": f"{len(top10_no_buyer)} of the ten largest by emission name no buyer.",
         "rule": "the same buyer rule, over the ten subnets with the largest share of the block reward",
         "href": "/findings/#table"},
        {"id": "disagreements", "n": dis_total, "of": None,
         "text": f"{dis_total} places where a subnet's own sources disagree about its program, across {dis_subnets} subnets.",
         "rule": "fields where the docs, the code, and the chain did not say the same thing; each is quoted on the subnet page",
         "href": "/programs/"},
        {"id": "big-delta", "n": len(big_delta), "of": total,
         "text": f"{len(big_delta)} sit {DELTA_OPEN} or more places lower on legibility than on emission.",
         "rule": "legibility rank minus emission rank, over the index; the table below carries every delta",
         "href": "/findings/#table"},
        {"id": "buyers-least", "n": f'{means["buyers"]:.1f}', "of": None,
         "text": f'Buyers are the audience subnets explain least: {means["buyers"]:.1f} of 5 on average, against {means["miners"]:.1f} for miners.',
         "rule": "mean legibility per audience across the index, four questions each, scale version " + str(data.get("rubric_version", "")),
         "href": "/sn/"},
        {"id": "spread", "n": f"{median:.1f}", "of": None,
         "text": f'The median legibility is {median:.1f}; the range runs from {lo["composite"]:.1f} ({lo["name"]}) to {hi["composite"]:.1f} ({hi["name"]}).',
         "rule": "the composite over four audiences, 0 to 5, scored " + str(data.get("scores_date", "")),
         "href": "/sn/"},
        {"id": "chain-or-code", "n": f"{round(100 * from_cc / nfields)}%", "of": None,
         "text": f"{round(100 * from_cc / nfields)}% of program fields rest on the chain or the code; {unknown_fields} could not be found.",
         "rule": f"{from_cc} of {nfields} fields, seven per program, by the trust mark on each",
         "href": "/programs/"},
        {"id": "identity", "n": ident_full, "of": total,
         "text": f"{ident_full} of {total} have filled every field of their on-chain identity.",
         "rule": "the seven identity fields a subnet owner can set on chain, from the chain snapshot of " + str(data.get("chain_snapshot", "")),
         "href": "/sn/"},
        {"id": "exploits", "n": exploits_any, "of": len(programs),
         "text": f"All {exploits_any} programs record something miners optimized instead of the work; {exploits_code} were read from the code.",
         "rule": "the exploits field of each program and its trust mark",
         "href": "/programs/"},
        {"id": "verified-quotes", "n": verified, "of": statements,
         "text": f"{verified} of {statements} quotes on record are verified against a live primary source.",
         "rule": "the confidence mark on each statement in the map; the rest are probable or unverified and say so",
         "href": "/narrative/"},
    ]
    return {
        "generated_at": data.get("generated_at"), "scores_date": data.get("scores_date"), "programs_read": read_dates,
        "license": "CC BY 4.0", "attribution": "Findings by Mikyö Clark, legible.network",
        "rules": {"buyer_named": "false when the buyer field starts Nobody, No paying, or Unknown, or its trust is unknown", "delta": "legibility_rank minus emission_rank", "delta_open": DELTA_OPEN},
        "findings": findings, "rows": rows,
    }


def for_json(F):
    return {**F, "rows": [{k: v for k, v in r.items() if k != "trust_html"} for r in F["rows"]]}


def _item(f, with_rule=True):
    rule = f'<small>{e(f["rule"])}</small>' if with_rule else ""
    return f'<li id="f-{e(f["id"])}"><b>{e(str(f["n"]))}</b><span><a href="{e(f["href"])}">{e(f["text"])}</a>{rule}</span></li>'


def home_block(F, n=8):
    items = "".join(_item(f, with_rule=False) for f in F["findings"][:n])
    return (f'<span class="group">What the record shows</span><ol class="flist">{items}</ol>'
            f'<p class="fcap">Counts, not readings: each is computed from the datasets and links to the rows it was counted from. '
            f'<a href="/findings/">All findings, the rules, and the allocator table</a></p>')


def page_list(F):
    return f'<ol class="flist">{"".join(_item(f) for f in F["findings"])}</ol>'


def page_stats(F):
    by = {f["id"]: f for f in F["findings"]}
    return (f'<div><b>{by["no-buyer"]["n"]}</b><span>of {by["no-buyer"]["of"]} name no buyer</span></div>'
            f'<div><b>{by["disagreements"]["n"]}</b><span>places the sources disagree</span></div>'
            f'<div><b>{by["big-delta"]["n"]}</b><span>funded {DELTA_OPEN}+ places above their legibility</span></div>'
            f'<div><b>{by["buyers-least"]["n"]}</b><span>buyer legibility, mean of 5</span></div>')


def page_rows(F):
    out = []
    for r in F["rows"]:
        d = r["delta"]
        dcls = " open" if d >= DELTA_OPEN else ""
        dtxt = f"+{d}" if d > 0 else str(d)
        if r["buyer_named"] is None:
            buyer = '<td class="buyer" data-sort="2"><span class="yn">not read</span></td>'
        else:
            yn = "yes" if r["buyer_named"] else "no"
            buyer = (f'<td class="buyer" data-sort="{0 if r["buyer_named"] else 1}"><span class="yn{"" if r["buyer_named"] else " open"}">{yn}</span>'
                     f'<p>{e(r["buyer_text"])}</p>{trust_badge(r["buyer_trust"])}</td>')
        out.append(
            f'<tr class="row" data-uid="{r["netuid"]}">'
            f'<td class="rank" data-sort="{r["emission_rank"]}">{r["emission_rank"]}</td>'
            f'<td class="name" data-sort="{e(r["name"].lower())}"><span class="nm"><a href="/sn/{r["netuid"]}/">{e(r["name"])}</a><span class="sn">SN{r["netuid"]} · {e(r["commodity"])}</span></span></td>'
            f'<td class="num" data-sort="{r["emission_rank"]}">{e(r["emission_pct"])}</td>'
            f'<td class="num" data-sort="{r["legibility_rank"] or 99}"><b class="band-{band(r["legibility"])}">{float(r["legibility"]):.1f}</b><span class="k">rank {r["legibility_rank"]} of {len(F["rows"])}</span></td>'
            f'<td class="num delta{dcls}" data-sort="{-d}">{dtxt}</td>'
            f'<td class="num" data-sort="{r["buyers_rank"] or 99}"><b class="band-{band(r["buyers_score"])}">{float(r["buyers_score"] or 0):.1f}</b><span class="k">rank {r["buyers_rank"]}</span></td>'
            f'{buyer}'
            f'<td class="num{" open" if r["disagreements"] else ""}" data-sort="{-r["disagreements"]}">{r["disagreements"] or ""}</td>'
            f'<td class="trust" data-sort="{-r["fields_from_chain_or_code"]}">{r["trust_html"]}<span class="k">{r["fields_from_chain_or_code"]} of 7 from chain or code</span></td>'
            f'</tr>')
    return "".join(out)


if __name__ == "__main__":
    from pathlib import Path
    REPO = Path(__file__).resolve().parent.parent
    data = json.loads((REPO / "data" / "index.json").read_text(encoding="utf-8"))
    pm = json.loads((REPO / "data" / "programs.json").read_text(encoding="utf-8"))
    nd = json.loads((REPO / "data" / "narrative.json").read_text(encoding="utf-8"))
    F = compute(data, pm, nd)
    for f in F["findings"]:
        print(f'{f["id"]:18} {f["text"]}')
