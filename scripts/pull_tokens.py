#!/usr/bin/env python3
"""Alpha token data and trading venues for the frozen subnet set.

Usage: python3 scripts/pull_tokens.py [--fresh]

Sources:
  Taostats  /api/dtao/pool/latest/v1      symbol, price in TAO, market cap, liquidity, volume, changes, staked vs in pool
  Taostats  /api/price/latest/v1?asset=tao TAO in USD
  Kraken    /0/public/AssetPairs           spot pairs named SN<netuid>/USD, SN<netuid>/EUR
  MEXC      /api/v3/exchangeInfo           spot symbols named SN<netuid>USDT
  CoinGecko /api/v3/search and /coins/<id>/tickers   any other listed market, when the token is on CoinGecko

Writes data/tokens-<date>.json. Every venue carries a source and a fetched URL;
the on-chain venues (tao.app, Taostats, TaoMarketCap) are listed for every subnet
because every alpha token trades there by construction.
"""
import argparse
import json
import sys
import time
import urllib.parse
from datetime import datetime, timezone

from common import DATA, TODAY, get, load_csv, require_env

RAO = 1e9


def taostats(path, params, key, fresh):
    url = f"https://api.taostats.io{path}?{urllib.parse.urlencode(params)}"
    st, body, _ = get(url, headers={"Authorization": key, "Accept": "application/json"}, ttl_hours=None if fresh else 6, use_cache=not fresh)
    if st != 200:
        raise SystemExit(f"taostats {path}: {st}")
    return json.loads(body)


def public_json(url, fresh, ttl=6):
    st, body, _ = get(url, headers={"Accept": "application/json"}, ttl_hours=None if fresh else ttl, use_cache=not fresh)
    if st != 200 or not body:
        return None
    try:
        return json.loads(body)
    except ValueError:
        return None


def f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fresh", action="store_true")
    a = ap.parse_args()
    key = require_env("TAOSTATS_API_KEY")
    targets = {int(r["netuid"]): r for r in load_csv(DATA / "subnets.csv", ["netuid", "rank", "name", "slice"])}

    pools = {d["netuid"]: d for d in taostats("/api/dtao/pool/latest/v1", {"limit": 200}, key, a.fresh).get("data", [])}
    tao = taostats("/api/price/latest/v1", {"asset": "tao"}, key, a.fresh)["data"][0]
    tao_usd = f(tao.get("price"))
    print(f"  pools: {len(pools)}; TAO {tao_usd} USD", file=sys.stderr)

    kraken = public_json("https://api.kraken.com/0/public/AssetPairs", a.fresh) or {}
    kpairs = {}
    for k, v in (kraken.get("result") or {}).items():
        ws = (v.get("wsname") or "").upper()
        if ws.startswith("SN") and "/" in ws:
            base, quote = ws.split("/", 1)
            if base[2:].isdigit():
                kpairs.setdefault(int(base[2:]), []).append({"pair": ws, "quote": quote, "url": f"https://pro.kraken.com/app/trade/{base}-{quote}"})
    print(f"  kraken subnet pairs: {sorted(kpairs)}", file=sys.stderr)

    mexc = public_json("https://api.mexc.com/api/v3/exchangeInfo", a.fresh) or {}
    mpairs = {}
    for s in mexc.get("symbols", []):
        sym = s.get("symbol", "")
        base = s.get("baseAsset", "")
        if base.upper().startswith("SN") and base[2:].isdigit() and s.get("status") in ("1", "ENABLED", 1):
            mpairs.setdefault(int(base[2:]), []).append({"pair": f"{base}/{s.get('quoteAsset')}", "quote": s.get("quoteAsset"), "url": f"https://www.mexc.com/exchange/{sym.replace(s.get('quoteAsset'), '_' + s.get('quoteAsset'))}"})
    print(f"  mexc subnet pairs: {sorted(mpairs)}", file=sys.stderr)

    out = {"pulled_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "tao_usd": tao_usd,
           "sources": {"pool": "taostats /api/dtao/pool/latest/v1", "tao_usd": "taostats /api/price/latest/v1",
                       "kraken": "api.kraken.com AssetPairs", "mexc": "api.mexc.com exchangeInfo", "coingecko": "api.coingecko.com search + tickers"},
           "tokens": {}}
    cg_hits = 0
    for nid, t in sorted(targets.items(), key=lambda kv: int(kv[1]["rank"])):
        p = pools.get(nid, {})
        price = f(p.get("price"))
        venues = [
            {"name": "tao.app", "kind": "on-chain", "url": f"https://tao.app/subnets/{nid}", "note": "Stake TAO into the subnet pool; the official Bittensor app", "source": "stated"},
            {"name": "Taostats", "kind": "on-chain", "url": f"https://taostats.io/subnets/{nid}", "note": "Pool stats and staking", "source": "stated"},
            {"name": "TaoMarketCap", "kind": "on-chain", "url": f"https://taomarketcap.com/subnets/{nid}", "note": "Pool stats and staking", "source": "stated"},
        ]
        for kp in kpairs.get(nid, []):
            venues.append({"name": "Kraken", "kind": "exchange", "url": kp["url"], "pair": kp["pair"], "note": "Spot market", "source": "stated"})
        for mp in mpairs.get(nid, []):
            venues.append({"name": "MEXC", "kind": "exchange", "url": mp["url"], "pair": mp["pair"], "note": "Spot market", "source": "stated"})
        # CoinGecko: only when the symbol SN<n> exists there
        cg = public_json(f"https://api.coingecko.com/api/v3/search?query=SN{nid}", a.fresh, ttl=24) or {}
        coin = next((c for c in cg.get("coins", []) if (c.get("symbol") or "").lower() == f"sn{nid}"), None)
        cg_id = None
        if coin:
            cg_id = coin["id"]
            cg_hits += 1
            time.sleep(2.5)
            tk = public_json(f"https://api.coingecko.com/api/v3/coins/{cg_id}/tickers", a.fresh, ttl=24) or {}
            seen = {(v["name"].lower(), v.get("pair", "")) for v in venues}
            for x in tk.get("tickers", []):
                mname = (x.get("market") or {}).get("name", "")
                pair = f"{x.get('base')}/{x.get('target')}"
                if mname.lower() in ("subnet tokens",) or (mname.lower(), pair) in seen or not x.get("trade_url"):
                    continue
                venues.append({"name": mname, "kind": "exchange", "url": x["trade_url"], "pair": pair, "note": "Listed on CoinGecko", "source": "stated"})
        time.sleep(2.5)
        mc_tao = (f(p.get("market_cap")) or 0) / RAO
        liq_tao = (f(p.get("liquidity")) or 0) / RAO
        out["tokens"][str(nid)] = {
            "netuid": nid, "name": p.get("name") or t["name"], "symbol": p.get("symbol") or "",
            "price_tao": price, "price_usd": (price * tao_usd) if (price is not None and tao_usd) else None,
            "market_cap_tao": mc_tao, "market_cap_usd": mc_tao * tao_usd if tao_usd else None,
            "liquidity_tao": liq_tao, "volume_24h_tao": (f(p.get("tao_volume_24_hr")) or 0) / RAO,
            "change_1d": f(p.get("price_change_1_day")), "change_1w": f(p.get("price_change_1_week")), "change_1m": f(p.get("price_change_1_month")),
            "alpha_staked": (f(p.get("alpha_staked")) or 0) / RAO, "alpha_in_pool": (f(p.get("alpha_in_pool")) or 0) / RAO, "total_alpha": (f(p.get("total_alpha")) or 0) / RAO,
            "pool_rank": p.get("rank"), "coingecko_id": cg_id, "venues": venues,
            "as_of": p.get("timestamp"),
        }
    outp = DATA / f"tokens-{TODAY}.json"
    outp.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    ex = sum(1 for t in out["tokens"].values() if any(v["kind"] == "exchange" for v in t["venues"]))
    print(f"wrote {outp.name}: {len(out['tokens'])} tokens, {ex} with an exchange listing, {cg_hits} on CoinGecko", file=sys.stderr)


if __name__ == "__main__":
    main()
