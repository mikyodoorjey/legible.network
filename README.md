# Subnet Legibility Index

What a first-time reader can find out about the 32 Bittensor subnets with the largest share of emission, in five minutes, from the subnet's own public materials. Scored for four audiences (stakers, miners, buyers, newcomers) on a four-question spine, 0 to 5 per cell. Findability, not quality.

Live at [legible.network](https://legible.network). Rubric at [/rubric/](https://legible.network/rubric/). Method at [/methodology/](https://legible.network/methodology/).

## Layout

| Path | What |
|---|---|
| `index.html` | The ranked index. Fetches `/data/summary.json`. |
| `rubric.md`, `methodology.md`, `about.md` | Source of truth for the three document pages, rendered by the build. |
| `sn/<netuid>/` | One page per subnet, generated. |
| `alpha/<netuid>/` | One page per alpha token: price, pool stats, and where it trades, generated. |
| `data/tokens-<date>.json` | Alpha token snapshot: Taostats pool data, Kraken and MEXC pairs, CoinGecko tickers. |
| `data/index.json` | The published dataset (CC BY 4.0). `summary.json` is the same minus evidence. |
| `data/chain-<date>.json` | Raw chain snapshots. `subnets.csv` is the frozen target list. |
| `data/scores-{a,b,c,d}.csv` | Agent output per slice. `scores.csv` is the merged, reviewed source of truth. |
| `agents/` | The scoring brief, per-agent slices, calibration set, summaries. |
| `scripts/` | The pipeline (below) and the site build. |

## Pipeline

```bash
cp .env.example .env            # add TAOSTATS_API_KEY
python3 -m venv .venv && .venv/bin/pip install bittensor   # optional, for chain identities
.venv/bin/python scripts/pull_chain.py            # snapshot, freeze targets, slices, stubs (first run)
python3 scripts/pull_tokens.py                    # alpha token prices, pool stats, exchange listings
# run four scoring agents with agents/PROMPT.md, one per slice
python3 scripts/merge_scores.py                   # scores-*.csv -> scores.csv, recompute
python3 scripts/verify_links.py --apply           # check every URL, downgrade unreachable
python3 scripts/review.py                         # review queue; fill decisions; then --apply
python3 scripts/build.py                          # -> data/index.json (publication gate)
python3 scripts/build_site.py                     # pages, subnet pages, OG images, chart, sitemap
python3 scripts/check_site.py                     # read-only checks
```

Corrections after publication go in `data/corrections.csv` and are applied with `scripts/apply_corrections.py`, which stamps provenance, rebuilds, and adds to the changelog.

## Local preview

`python3 -m http.server 8790` from the repo root, then `http://127.0.0.1:8790/`. To build the site against fixture data before real scores exist: `python3 scripts/build_site.py --data scripts/fixtures/sample.json`.

## Deployment

Static site on Vercel, no build step. `vercel.json` carries redirects, headers, and trailing slashes. `middleware.js` locks the site behind Basic Auth while `SITE_LOCKED=1`, with `PUBLIC_PATHS` for pages opened early.

## Licenses

Code MIT. Data CC BY 4.0, attribution "Subnet Legibility Index by Mikyö Clark, legible.network". Fonts under the SIL Open Font License, in `scripts/fonts/`.
