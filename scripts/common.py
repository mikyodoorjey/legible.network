#!/usr/bin/env python3
"""Shared contract and helpers for the Subnet Legibility Index pipeline.

Every script imports from here so there is one column contract, one evidence
parser, one HTTP getter, and one way to stamp provenance.
"""
import csv
import hashlib
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import date, datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
AGENTS = REPO / "agents"
CACHE = REPO / "scripts" / "cache"
TODAY = date.today().isoformat()

AUDIENCES = ["stakers", "miners", "buyers", "newcomers"]
QUESTIONS = ["q1", "q2", "q3", "q4"]
Q_LABELS = {
    "q1": "What it is",
    "q2": "Who it is for",
    "q3": "How it resists gaming or fails",
    "q4": "Identity and documentation",
}
AUDIENCE_LABELS = {
    "stakers": "Stakers and validators",
    "miners": "Miners",
    "buyers": "Buyers and enterprises",
    "newcomers": "Newcomers",
}
AUDIENCE_QUESTION = {
    "stakers": "Should I allocate here?",
    "miners": "Can I compete, and what wins?",
    "buyers": "Can I use this today?",
    "newcomers": "What is this and why does it matter?",
}
IDENTITY_FIELDS = ["subnet_name", "github_repo", "subnet_contact", "subnet_url", "discord", "description", "additional"]
STATUS_TOKENS = ("verified", "inferred", "unknown")

SCORE_COLUMNS = [
    "netuid", "name", "rank", "slice",
    "stakers_score", "stakers_evidence",
    "miners_score", "miners_evidence",
    "buyers_score", "buyers_evidence",
    "newcomers_score", "newcomers_evidence",
    "composite",
    "own_words", "identity_check", "artifacts",
    "sources", "searches_used", "minutes_spent",
    "last_verified", "claim_labels", "notes",
]
ARTIFACT_KEYS = ["github", "docs", "whitepaper", "x", "discord", "api", "dashboard"]


# ---------------- environment
def read_env(path=None):
    """Load KEY=VALUE lines from .env into os.environ without overriding existing vars."""
    path = path or (REPO / ".env")
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def require_env(name):
    read_env()
    v = os.environ.get(name, "").strip()
    if not v:
        raise SystemExit(f"set {name} in .env or the environment")
    return v


# ---------------- CSV
def load_csv(path, columns=SCORE_COLUMNS):
    """Read a CSV under the exact column contract. Ragged rows are skipped with a note."""
    path = Path(path)
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != columns:
            print(f"column mismatch in {path.name}:\n  got      {reader.fieldnames}\n  expected {columns}", file=sys.stderr)
            raise SystemExit(2)
        rows = []
        for i, row in enumerate(reader, start=2):
            if None in row or any(v is None for v in row.values()):
                print(f"  {path.name}:{i} ragged row, skipped", file=sys.stderr)
                continue
            rows.append({k: (v or "").strip() for k, v in row.items()})
    return rows


def write_csv(path, rows, columns=SCORE_COLUMNS):
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columns, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in columns})


# ---------------- evidence cells
ENTRY_START = re.compile(r"^\s*q[1-4]\s*\|", re.IGNORECASE)


def rejoin_entries(text):
    """Split an evidence cell on semicolons and glue back fragments that are not entries."""
    parts = [p.strip() for p in text.split(";")]
    out = []
    for p in parts:
        if not p:
            continue
        if out and not ENTRY_START.match(p):
            out[-1] = out[-1] + ", " + p
        else:
            out.append(p)
    return out


def parse_evidence(text):
    """Turn an audience evidence cell into a structured envelope.

    Entry format: q1 | score | verified|inferred|unknown | url | note
    Returns {"status": unchecked|skipped|scored, "note": str, "entries": [...]}
    where each entry is {"q", "score" (int or None), "status", "url", "note"}.
    Entries with fewer than five fields are kept with status "malformed".
    """
    t = (text or "").strip()
    if not t:
        return {"status": "unchecked", "note": "", "entries": []}
    if t.lower().startswith("not scored"):
        return {"status": "skipped", "note": t, "entries": []}
    entries = []
    for raw in rejoin_entries(t):
        parts = [p.strip() for p in raw.split("|")]
        if len(parts) < 5:
            entries.append({"q": parts[0].lower() if parts else "", "score": None, "status": "malformed", "url": "", "note": raw})
            continue
        q = parts[0].lower()
        score_txt = parts[1].lower()
        score = int(score_txt) if score_txt.isdigit() and 0 <= int(score_txt) <= 5 else None
        status = parts[2].lower()
        if status not in STATUS_TOKENS:
            status = "malformed"
        url = parts[3] if parts[3].lower() not in ("none", "n/a", "-", "") else ""
        note = " | ".join(parts[4:]).strip()
        if score is None and status != "unknown":
            status = "malformed"
        entries.append({"q": q, "score": score, "status": status, "url": url, "note": note})
    return {"status": "scored", "entries": entries}


def audience_score(parsed):
    """Return (score or None, partial, unknown_count) per the rubric's unknown rule.

    Unknown cells are excluded from the mean while at least three cells are scored;
    with two or more unknown or missing cells the audience is unscored (None).
    """
    by_q = {}
    for e in parsed.get("entries", []):
        if e["q"] in QUESTIONS and e["q"] not in by_q:
            by_q[e["q"]] = e
    scored = [e["score"] for e in by_q.values() if e["score"] is not None and e["status"] != "malformed"]
    unknown = 4 - len(scored)
    if len(scored) < 3:
        return None, True, unknown
    return round(sum(scored) / len(scored) + 1e-9, 1), unknown > 0, unknown


def composite_score(audience_scores):
    """Mean of the scored audiences, one decimal; partial if any audience is unscored."""
    vals = [v for v in audience_scores.values() if v is not None]
    if not vals:
        return None, True
    return round(sum(vals) / len(vals) + 1e-9, 1), len(vals) < len(audience_scores)


def parse_pairs(text, keys=None):
    """Parse 'key | value | ...' entries separated by semicolons into a list of field lists."""
    out = []
    for raw in (text or "").split(";"):
        raw = raw.strip()
        if not raw:
            continue
        out.append([p.strip() for p in raw.split("|")])
    return out


# ---------------- provenance
def stamp(row, text):
    """Append a dated provenance note to claim_labels once."""
    cur = (row.get("claim_labels") or "").strip()
    if text in cur:
        return
    row["claim_labels"] = (cur.rstrip(". ") + "; " + text) if cur else text


def set_verified(row):
    row["last_verified"] = TODAY


def key(name):
    return re.sub(r"[^a-z0-9]", "", (name or "").lower().split("(")[0])


def is_unknown(v):
    v = (v or "").strip().lower()
    return v == "" or v.startswith("unknown")


# ---------------- HTTP with cache
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) legible-network/1.0 (+https://legible.network)"}
_mem = {}


def _cache_path(url):
    return CACHE / (hashlib.sha1(url.encode("utf-8")).hexdigest() + ".json")


def get(url, timeout=20, headers=None, ttl_hours=None, use_cache=True):
    """GET a URL. Returns (status, body, final_url). Never raises.

    On-disk cache under scripts/cache keyed by sha1(url); ttl_hours=None means
    reuse any cached copy within the process lifetime, a number expires it.
    Secret headers are never written to the cache.
    """
    if use_cache and url in _mem:
        return _mem[url]
    CACHE.mkdir(parents=True, exist_ok=True)
    cp = _cache_path(url)
    if use_cache and cp.exists():
        try:
            c = json.loads(cp.read_text(encoding="utf-8"))
            fresh = True
            if ttl_hours is not None:
                age = (datetime.now(timezone.utc) - datetime.fromisoformat(c["fetched_at"])).total_seconds() / 3600
                fresh = age <= ttl_hours
            if fresh:
                res = (c["status"], c["body"], c.get("final_url", url))
                _mem[url] = res
                return res
        except (ValueError, KeyError):
            pass
    h = dict(UA)
    if headers:
        h.update(headers)
    try:
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            res = (r.status, r.read().decode("utf-8", "ignore"), r.geturl())
    except urllib.error.HTTPError as e:
        res = (e.code, "", url)
    except Exception as e:  # noqa
        res = (str(e)[:80], "", url)
    if use_cache and isinstance(res[0], int):
        cp.write_text(json.dumps({"url": url, "status": res[0], "final_url": res[2],
                                  "fetched_at": datetime.now(timezone.utc).isoformat(), "body": res[1]}),
                      encoding="utf-8")
    _mem[url] = res
    return res


def latest(pattern):
    """Newest file matching a glob under data/, by name (dates sort)."""
    files = sorted(DATA.glob(pattern))
    return files[-1] if files else None


def strip_tags(html_text):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html_text, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)
