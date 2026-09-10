#!/usr/bin/env python3
"""Check every URL the scores cite and record what came back.

Usage: python3 scripts/verify_links.py [--apply] [--only-evidence]

Collects URLs from data/scores.csv (evidence cells, sources, artifacts, own_words)
and from the newest data/chain-*.json (github_repo, subnet_url, discord), fetches
each unique URL once, and writes data/verify-<date>.csv with one line per reference:
  live               2xx and, when a quote was given, its first six words are on the page
  live_unconfirmed   2xx but the quoted text is absent (JS-rendered, moved, or paraphrased)
  redirected         2xx after a redirect to a different host; detail carries the final URL
  unreachable        anything else (4xx, 5xx, timeout, DNS)
  manual             x.com, twitter.com, discord, t.me: not fetched, check by hand
GitHub repository URLs go through api.github.com/repos and record pushed_at and archived.
With --apply, verified entries whose URL is unreachable become inferred with a dated
note, redirected entries get a dated note, no URL is ever deleted or replaced, and
each touched row is stamped with its counts.
"""
import argparse
import json
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlsplit

from common import (ARTIFACT_KEYS, AUDIENCES, DATA, TODAY, get, latest, load_csv, parse_pairs, rejoin_entries,
                    set_verified, stamp, strip_tags, write_csv)

VERIFY_COLUMNS = ["netuid", "name", "field", "url", "expected_text", "result", "detail", "final_url"]
MANUAL_HOSTS = {"x.com", "twitter.com", "discord.gg", "discord.com", "t.me"}
GITHUB_REPO = re.compile(r"^https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?/?$")
QUOTE = re.compile(r'"([^"]{3,})"')

# Pages that are JS-rendered, rate-limited, or behind a bot wall, checked in a browser
# on the date given. url -> (result, reason). Applied before any fetch.
MANUAL = {
    # "https://example.org/docs": ("live", "docs render client-side, checked in Safari 2026-09-17"),
}


# ---------------- URL handling
def norm_url(u):
    """Add a scheme when missing and strip trailing punctuation; return "" for non-URLs."""
    u = (u or "").strip().strip("<>")
    if not u or u.lower() in ("none", "n/a", "-"):
        return ""
    if not re.match(r"^[a-z][a-z0-9+.-]*://", u, re.I):
        if not re.match(r"^[a-z0-9.-]+\.[a-z]{2,}(/|$)", u, re.I):
            return ""
        u = "https://" + u
    return u.rstrip(").,;:'\"")


def host_of(u):
    try:
        h = (urlsplit(u).hostname or "").lower()
    except ValueError:
        return ""
    return h[4:] if h.startswith("www.") else h


def words(text, n=None):
    w = re.findall(r"[a-z0-9]+", (text or "").lower())
    return w[:n] if n else w


# ---------------- collection
def collect_urls(rows, snapshot, only_evidence=False):
    """Yield (netuid, name, field, url, expected_text) for every URL reference."""
    ident = {}
    if snapshot:
        for s in snapshot.get("subnets", []):
            ident[str(s.get("netuid"))] = s.get("identity") or {}
    for r in rows:
        nid, name = r["netuid"], r["name"]
        for a in AUDIENCES:
            for raw in rejoin_entries(r.get(f"{a}_evidence", "")):
                parts = [p.strip() for p in raw.split("|")]
                if len(parts) < 5:
                    continue
                url = norm_url(parts[3])
                if not url:
                    continue
                note = " | ".join(parts[4:])
                m = QUOTE.search(note)
                yield nid, name, f"{a}.{parts[0].lower()}", url, (m.group(1) if m else "")
        if only_evidence:
            continue
        for src in r.get("sources", "").split(";"):
            url = norm_url(src)
            if url:
                yield nid, name, "sources", url, ""
        for parts in parse_pairs(r.get("artifacts", "")):
            if len(parts) < 2 or parts[0].lower() not in ARTIFACT_KEYS:
                continue
            url = norm_url(parts[1])
            if url:
                yield nid, name, f"artifacts.{parts[0].lower()}", url, ""
        ow = r.get("own_words", "")
        if " | " in ow:
            quote, _, u = ow.rpartition(" | ")
            url = norm_url(u)
            if url:
                yield nid, name, "own_words", url, quote.strip().strip('"')
        for f in ("github_repo", "subnet_url", "discord"):
            url = norm_url(ident.get(nid, {}).get(f, ""))
            if url:
                yield nid, name, f"identity.{f}", url, ""


# ---------------- checking
def text_present(expected, body):
    want = " ".join(words(expected, 6))
    if not want:
        return True
    have = " ".join(words(strip_tags(body)))
    return want in have


def check_github(url, expected_text):
    m = GITHUB_REPO.match(url)
    owner, repo = m.group(1), m.group(2)
    st, body, _ = get(f"https://api.github.com/repos/{owner}/{repo}", headers={"Accept": "application/vnd.github+json"})
    if st == 200:
        try:
            j = json.loads(body)
        except ValueError:
            j = {}
        pushed = str(j.get("pushed_at") or "")[:10]
        archived = bool(j.get("archived"))
        final = j.get("html_url") or url
        detail = f"archived, pushed_at {pushed}" if archived else f"pushed_at {pushed}, archived=false"
        if expected_text:
            st2, body2, _ = get(url)
            if st2 == 200 and not text_present(expected_text, body2):
                return "live_unconfirmed", detail + ", quote absent from repo page", final
        return "live", detail, final
    if st in (403, 429):
        return check_page(url, expected_text, prefix="github api rate-limited, page ")
    if st == 404:
        return "unreachable", "github api 404 (repo missing, renamed, or private)", url
    return "unreachable", f"github api {st}", url


def check_page(url, expected_text, prefix=""):
    st, body, final = get(url)
    if isinstance(st, int) and 200 <= st < 300:
        if final and host_of(final) != host_of(url):
            return "redirected", f"{prefix}{st}, host changed to {host_of(final)}: {final}", final
        if expected_text and not text_present(expected_text, body):
            return "live_unconfirmed", f"{prefix}{st}, quoted text absent", final or url
        return "live", f"{prefix}{st}", final or url
    return "unreachable", f"{prefix}{st}", final or url


def check(url, expected_text=""):
    """Return (result, detail, final_url) for one URL. Never raises."""
    if url in MANUAL:
        res, reason = MANUAL[url]
        return res, f"manual: {reason}", url
    host = host_of(url)
    if host in MANUAL_HOSTS or host.endswith(".discord.com"):
        return "manual", f"{host} is not fetched, check by hand", url
    try:
        if GITHUB_REPO.match(url):
            return check_github(url, expected_text)
        return check_page(url, expected_text)
    except Exception as ex:  # noqa
        return "unreachable", f"exception {str(ex)[:100]}", url


# ---------------- apply
def apply_results(rows, by_url):
    """Downgrade and annotate evidence entries in place; return the number of rows stamped."""
    touched = 0
    for r in rows:
        counts = Counter()
        changed = False
        for a in AUDIENCES:
            col = f"{a}_evidence"
            raws = rejoin_entries(r.get(col, ""))
            if not raws:
                continue
            out = []
            for raw in raws:
                parts = [p.strip() for p in raw.split("|")]
                if len(parts) < 5:
                    out.append(raw)
                    continue
                url = norm_url(parts[3])
                hit = by_url.get(url) if url else None
                if not hit:
                    out.append(raw)
                    continue
                res, detail, final = hit
                counts[res] += 1
                note = " | ".join(parts[4:])
                if res == "unreachable":
                    tag = f"(url unreachable {TODAY})"
                    if parts[2].lower() == "verified":
                        parts[2] = "inferred"
                        changed = True
                    if tag not in note:
                        note = (note + " " + tag).strip()
                        changed = True
                elif res == "redirected":
                    tag = f"(redirects to {host_of(final)} {TODAY})"
                    if tag not in note:
                        note = (note + " " + tag).strip()
                        changed = True
                out.append(" | ".join([parts[0], parts[1], parts[2], parts[3], note]))
            new_cell = "; ".join(out)
            if new_cell != r[col]:
                r[col] = new_cell
        # sources, artifacts, own_words, and identity URLs count toward the row stamp too
        for f in ("sources",):
            for src in r.get(f, "").split(";"):
                u = norm_url(src)
                if u and u in by_url:
                    counts[by_url[u][0]] += 1
        for parts in parse_pairs(r.get("artifacts", "")):
            u = norm_url(parts[1]) if len(parts) > 1 else ""
            if u and u in by_url:
                counts[by_url[u][0]] += 1
        if " | " in r.get("own_words", ""):
            u = norm_url(r["own_words"].rpartition(" | ")[2])
            if u and u in by_url:
                counts[by_url[u][0]] += 1
        if not counts and not changed:
            continue
        live = counts["live"] + counts["live_unconfirmed"] + counts["redirected"]
        stamp(r, f"links verified {TODAY}: {live} live, {counts['unreachable']} unreachable, {counts['manual']} manual")
        set_verified(r)
        touched += 1
    return touched


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="rewrite data/scores.csv with downgrades and stamps")
    ap.add_argument("--only-evidence", action="store_true", help="check evidence URLs only")
    a = ap.parse_args()

    rows = load_csv(DATA / "scores.csv")
    snap_path = latest("chain-*.json")
    snapshot = json.loads(snap_path.read_text(encoding="utf-8")) if snap_path else None
    if not snapshot:
        print("  no chain snapshot found, identity URLs skipped", file=sys.stderr)

    tasks = list(collect_urls(rows, snapshot, a.only_evidence))
    unique = {}
    for nid, name, field, url, expected in tasks:
        # keep the longest expected text per URL so the confirmation check is the strictest one
        if url not in unique or len(expected) > len(unique[url]):
            unique[url] = expected
    print(f"verifying {len(unique)} unique URLs across {len(tasks)} references", file=sys.stderr)

    def run(item):
        url, expected = item
        return url, check(url, expected)

    with ThreadPoolExecutor(max_workers=8) as ex:
        by_url = dict(ex.map(run, unique.items()))

    out_rows = []
    for nid, name, field, url, expected in tasks:
        res, detail, final = by_url[url]
        out_rows.append({"netuid": nid, "name": name, "field": field, "url": url, "expected_text": expected,
                         "result": res, "detail": detail, "final_url": final})
    out = DATA / f"verify-{TODAY}.csv"
    write_csv(out, out_rows, VERIFY_COLUMNS)
    c = Counter(r["result"] for r in out_rows)
    print("results:", dict(sorted(c.items())), file=sys.stderr)
    print(f"wrote {out.name}", file=sys.stderr)
    for r in out_rows:
        if r["result"] == "unreachable" and r["field"].split(".")[0] in AUDIENCES:
            print(f"  SN{r['netuid']} {r['field']}: {r['url']} ({r['detail']})", file=sys.stderr)

    if not a.apply:
        return
    touched = apply_results(rows, by_url)
    write_csv(DATA / "scores.csv", rows)
    print(f"applied: {touched} rows stamped, scores.csv written", file=sys.stderr)


if __name__ == "__main__":
    main()
