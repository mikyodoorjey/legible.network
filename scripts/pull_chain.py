#!/usr/bin/env python3
"""Step 1 collector: rank the top subnets by emission and capture their chain identity.

Usage: python3 scripts/pull_chain.py [--limit 32] [--fresh] [--no-sdk] [--deep] [--refreeze]

Sources:
  Taostats  /api/subnet/latest/v1?order=emission_desc   ranking, emission share, counts, burn, owner
  Taostats  /api/subnet/identity/v1                       identity fields (fallback when the SDK is absent)
  Bittensor SDK (optional)                                identity, burn, alpha price; --deep adds metagraph counts

Writes data/chain-<date>.json. The first successful run freezes data/subnets.csv,
agents/slices/slice-<x>.md and data/scores-<x>.csv stubs. Later runs refresh figures
and print a diff but keep membership unless --refreeze is passed.
"""
import argparse
import json
import sys
import time
import urllib.parse
from datetime import datetime, timezone

from common import (AGENTS, DATA, IDENTITY_FIELDS, SCORE_COLUMNS, TODAY, get, latest, require_env,
                    write_csv)

TAOSTATS = "https://api.taostats.io"
MIN_GAP_SECONDS = 13  # free tier is reportedly 5 calls per minute
_last_call = 0.0

# Our name -> candidate keys in the Taostats payload, tried in order. The keys
# actually used are recorded in the snapshot so the choice is auditable.
FIELD_MAP = {
    "netuid": ["netuid", "net_uid", "subnet_id"],
    "name": ["name", "subnet_name", "subnet_identity.subnet_name"],
    "emission_share": ["emission", "emission_share", "tao_emission_share", "emissions"],
    "active_miners": ["active_miners", "miners", "active_miner_count"],
    "active_validators": ["active_validators", "validators", "active_validator_count"],
    "registration_cost_tao": ["registration_cost", "neuron_registration_cost", "burn"],
    "owner": ["owner", "owner_coldkey", "owner_ss58", "owner.ss58"],
    "alpha_price_tao": ["price", "alpha_price", "pool_price"],
}


def dig(record, dotted):
    cur = record
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def pick(record, name):
    for k in FIELD_MAP[name]:
        v = dig(record, k)
        if v not in (None, ""):
            return v, k
    return None, None


def to_float(v):
    try:
        if isinstance(v, dict):
            return None
        return float(v)
    except (TypeError, ValueError):
        return None


def to_int(v):
    f = to_float(v)
    return int(f) if f is not None else None


def taostats_get(path, params, key, fresh=False, ttl_hours=6):
    """GET a Taostats endpoint with spacing, backoff, and the on-disk cache."""
    global _last_call
    url = f"{TAOSTATS}{path}?{urllib.parse.urlencode(params)}"
    delays = [15, 30, 60, 120, 240]
    for attempt in range(len(delays) + 1):
        wait = MIN_GAP_SECONDS - (time.time() - _last_call)
        if wait > 0 and (fresh or attempt > 0):
            time.sleep(wait)
        st, body, _ = get(url, headers={"Authorization": key, "Accept": "application/json"},
                          ttl_hours=None if fresh else ttl_hours, use_cache=not fresh or attempt > 0)
        if st != 200 or not body:
            _last_call = time.time()
        if st == 200 and body:
            try:
                return json.loads(body)
            except ValueError:
                print(f"  taostats {path}: unparseable body", file=sys.stderr)
                return None
        if st in (429, 500, 502, 503, 504) and attempt < len(delays):
            print(f"  taostats {path}: {st}, retry in {delays[attempt]}s", file=sys.stderr)
            time.sleep(delays[attempt])
            continue
        print(f"  taostats {path}: {st}", file=sys.stderr)
        return None
    return None


def fetch_ranking(limit, key, fresh):
    """Fetch every subnet (paginated) so emission share is over the whole network, then keep the top N."""
    data, page, total_items = [], 1, None
    while True:
        j = taostats_get("/api/subnet/latest/v1", {"order": "emission_desc", "limit": 200, "page": page}, key, fresh)
        if not j:
            raise SystemExit("ranking call failed; see stderr")
        rows = j.get("data") if isinstance(j, dict) else j
        if not isinstance(rows, list) or not rows:
            break
        data.extend(rows)
        pg = j.get("pagination") or {}
        total_items = pg.get("total_items", total_items)
        if not pg.get("next_page"):
            break
        page = pg["next_page"]
    if not data:
        raise SystemExit("ranking returned no rows")
    print(f"  ranking: {len(data)} subnets fetched (total_items {total_items}); keys: {sorted(data[0].keys())[:12]}...", file=sys.stderr)
    data.sort(key=lambda r: -(to_float(pick(r, "emission_share")[0]) or 0.0))
    return data, total_items or len(data)


def fetch_identities_taostats(key, fresh):
    out = {}
    page = 1
    while True:
        j = taostats_get("/api/subnet/identity/v1", {"limit": 200, "page": page}, key, fresh)
        if not j:
            break
        data = j.get("data") if isinstance(j, dict) else j
        if not data:
            break
        for rec in data:
            nid = to_int(pick(rec, "netuid")[0])
            if nid is None:
                continue
            ident = rec.get("subnet_identity") if isinstance(rec.get("subnet_identity"), dict) else rec
            out[nid] = {f: (ident.get(f) or "") for f in IDENTITY_FIELDS}
        nxt = (j.get("pagination") or {}).get("next_page") if isinstance(j, dict) else None
        if not nxt:
            break
        page = nxt
    print(f"  identities (taostats): {len(out)} subnets", file=sys.stderr)
    return out


# ---------------- optional SDK path
def sdk_available():
    try:
        import bittensor  # noqa
        return getattr(bittensor, "__version__", "unknown")
    except Exception:
        return None


def sdk_connect():
    import bittensor
    return bittensor.Subtensor(network="finney")


def sdk_identity(sub, netuid):
    try:
        ident = sub.subnets.subnet_identity(netuid=netuid)
    except Exception as e:  # noqa
        print(f"  sdk identity {netuid}: {str(e)[:60]}", file=sys.stderr)
        return None
    if ident is None:
        return {f: "" for f in IDENTITY_FIELDS}
    out = {}
    for f in IDENTITY_FIELDS + ["logo_url"]:
        v = getattr(ident, f, None)
        if v is None and isinstance(ident, dict):
            v = ident.get(f)
        out[f] = (v or "")
    return out


def sdk_extras(sub, netuid, deep):
    extra = {}
    try:
        b = sub.subnets.burn(netuid=netuid)
        extra["registration_cost_tao"] = float(getattr(b, "tao", b))
    except Exception as e:  # noqa
        print(f"  sdk burn {netuid}: {str(e)[:60]}", file=sys.stderr)
    try:
        p = sub.prices.alpha_price(netuid=netuid)
        if isinstance(p, dict):
            p = p.get("tao_per_alpha", p.get("price"))
        extra["alpha_price_tao"] = float(getattr(p, "tao", p))
    except Exception as e:  # noqa
        print(f"  sdk price {netuid}: {str(e)[:60]}", file=sys.stderr)
    if deep:
        try:
            mg = sub.subnets.metagraph(netuid=netuid)
            permits = list(getattr(mg, "validator_permit", []))
            stakes = list(getattr(mg, "S", getattr(mg, "stake", [])))
            v = sum(1 for i, p in enumerate(permits) if p and (i >= len(stakes) or float(stakes[i]) > 0))
            extra["active_validators"] = v
            extra["active_miners"] = int(getattr(mg, "n", len(permits))) - v
        except Exception as e:  # noqa
            print(f"  sdk metagraph {netuid}: {str(e)[:60]}", file=sys.stderr)
    return extra


# ---------------- snapshot
def completeness(identity):
    filled = [f for f in IDENTITY_FIELDS if (identity or {}).get(f)]
    return {"filled": len(filled), "of": len(IDENTITY_FIELDS),
            "missing": [f for f in IDENTITY_FIELDS if f not in filled]}


def build_rows(ranking, identities, identity_source, sdk=None, deep=False, limit=32):
    rows, used = [], {}
    raw_em = []
    for rec in ranking:
        vals = {}
        for name in FIELD_MAP:
            v, k = pick(rec, name)
            vals[name] = v
            if k and name not in used:
                used[name] = k
        raw_em.append(to_float(vals["emission_share"]) or 0.0)
    total = sum(raw_em)
    method = "api_share" if total <= 1.05 else "normalized_over_network"
    for i, rec in enumerate(ranking[:limit]):
        vals = {name: pick(rec, name)[0] for name in FIELD_MAP}
        nid = to_int(vals["netuid"])
        em = to_float(vals["emission_share"]) or 0.0
        if method == "normalized_over_network" and total:
            em = em / total
        ident = identities.get(nid) or {f: "" for f in IDENTITY_FIELDS}
        row = {
            "netuid": nid, "rank": i + 1,
            "name": (vals["name"] if isinstance(vals["name"], str) else None) or ident.get("subnet_name") or f"SN{nid}",
            "emission_share": round(em, 6),
            "active_miners": to_int(vals["active_miners"]),
            "active_validators": to_int(vals["active_validators"]),
            "registration_cost_tao": to_float(vals["registration_cost_tao"]),
            "alpha_price_tao": to_float(vals["alpha_price_tao"]),
            "owner": vals["owner"] if isinstance(vals["owner"], str) else None,
            "identity": ident, "identity_source": identity_source,
        }
        if sdk is not None:
            row.update({k: v for k, v in sdk_extras(sdk, nid, deep).items() if v is not None})
        row["identity_completeness"] = completeness(ident)
        rows.append(row)
    return rows, used, method


def diff_previous(new_rows, prev_path):
    if not prev_path:
        return
    try:
        old = {r["netuid"]: r for r in json.loads(prev_path.read_text(encoding="utf-8"))["subnets"]}
    except Exception:
        return
    new = {r["netuid"]: r for r in new_rows}
    print(f"== diff against {prev_path.name}", file=sys.stderr)
    for nid in sorted(set(old) - set(new)):
        print(f"  left top set: SN{nid} {old[nid]['name']}", file=sys.stderr)
    for nid in sorted(set(new) - set(old)):
        print(f"  entered top set: SN{nid} {new[nid]['name']} at rank {new[nid]['rank']}", file=sys.stderr)
    for nid in sorted(set(new) & set(old)):
        a, b = old[nid], new[nid]
        if a["rank"] != b["rank"]:
            print(f"  SN{nid} rank {a['rank']} -> {b['rank']}", file=sys.stderr)
        if a["name"] != b["name"]:
            print(f"  SN{nid} renamed {a['name']!r} -> {b['name']!r}", file=sys.stderr)
        for f in IDENTITY_FIELDS:
            if (a["identity"].get(f) or "") != (b["identity"].get(f) or ""):
                print(f"  SN{nid} identity.{f} changed", file=sys.stderr)


def freeze(rows):
    """Write the frozen target list, per-agent slice files, and score stubs."""
    subs = [{"netuid": r["netuid"], "rank": r["rank"], "name": r["name"], "slice": "abcd"[(r["rank"] - 1) % 4]} for r in rows]
    write_csv(DATA / "subnets.csv", subs, ["netuid", "rank", "name", "slice"])
    (AGENTS / "slices").mkdir(parents=True, exist_ok=True)
    for s in "abcd":
        mine = [r for r in rows if "abcd"[(r["rank"] - 1) % 4] == s]
        lines = [f"# Slice {s}: {len(mine)} subnets", "",
                 f"Chain snapshot {TODAY}. Identity fields are the subnet owner's own words on chain. Do not refetch chain data.", ""]
        for r in mine:
            lines += [f"## SN{r['netuid']} {r['name']}", "",
                      f"- rank by emission: {r['rank']}",
                      f"- emission share: {r['emission_share'] * 100:.2f}%",
                      f"- active miners / validators: {r['active_miners']} / {r['active_validators']}",
                      f"- registration cost (TAO): {r['registration_cost_tao']}",
                      f"- identity filled: {r['identity_completeness']['filled']} of 7"]
            for f in IDENTITY_FIELDS:
                v = r["identity"].get(f) or ""
                lines.append(f"- {f}: {v if v else '(not set)'}")
            lines.append("")
        (AGENTS / "slices" / f"slice-{s}.md").write_text("\n".join(lines), encoding="utf-8")
        stub = [{"netuid": r["netuid"], "name": r["name"], "rank": r["rank"], "slice": s} for r in mine]
        write_csv(DATA / f"scores-{s}.csv", stub, SCORE_COLUMNS)
    print(f"  froze {len(subs)} subnets into subnets.csv, 4 slice files, 4 score stubs", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=32)
    ap.add_argument("--fresh", action="store_true", help="bypass the 6h cache")
    ap.add_argument("--no-sdk", action="store_true", help="identities from Taostats only")
    ap.add_argument("--deep", action="store_true", help="SDK metagraph counts (slow)")
    ap.add_argument("--refreeze", action="store_true", help="rewrite subnets.csv, slices, and stubs")
    a = ap.parse_args()

    key = require_env("TAOSTATS_API_KEY")
    print("pulling ranking", file=sys.stderr)
    ranking, total_subnets = fetch_ranking(a.limit, key, a.fresh)
    top = ranking[:a.limit]

    sdk = None
    version = None if a.no_sdk else sdk_available()
    if version:
        print(f"  bittensor sdk {version}, connecting", file=sys.stderr)
        try:
            sdk = sdk_connect()
        except Exception as e:  # noqa
            print(f"  sdk connect failed ({str(e)[:60]}), falling back to Taostats identities", file=sys.stderr)
            sdk = None
    if sdk is not None:
        identities = {}
        for rec in top:
            nid = to_int(pick(rec, "netuid")[0])
            ident = sdk_identity(sdk, nid)
            if ident is not None:
                identities[nid] = ident
        identity_source = f"sdk {version}"
        if len(identities) < len(top):
            fallback = fetch_identities_taostats(key, a.fresh)
            for rec in top:
                nid = to_int(pick(rec, "netuid")[0])
                identities.setdefault(nid, fallback.get(nid, {f: "" for f in IDENTITY_FIELDS}))
    else:
        identities = fetch_identities_taostats(key, a.fresh)
        identity_source = "taostats /api/subnet/identity/v1"

    rows, used, method = build_rows(ranking, identities, identity_source, sdk, a.deep, a.limit)
    snapshot = {
        "pulled_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sources": {"ranking": "taostats /api/subnet/latest/v1", "identity": identity_source,
                    "counts": "sdk metagraph" if (sdk is not None and a.deep) else "taostats",
                    "emission_share_method": method, "field_map_used": used},
        "total_subnets": total_subnets,
        "subnets": rows,
    }
    prev = latest("chain-*.json")
    out = DATA / f"chain-{TODAY}.json"
    out.write_text(json.dumps(snapshot, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {out.name}: {len(rows)} subnets, identity {sum(1 for r in rows if r['identity_completeness']['filled'])} set, "
          f"emission method {method}", file=sys.stderr)
    if prev and prev != out:
        diff_previous(rows, prev)
    if a.refreeze or not (DATA / "subnets.csv").exists():
        freeze(rows)
    else:
        print("  membership kept (pass --refreeze to rewrite subnets.csv, slices, stubs)", file=sys.stderr)


if __name__ == "__main__":
    main()
