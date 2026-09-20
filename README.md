# legible.network

Three instruments for reading the Bittensor ecosystem, one site, under one argument: Ethereum made Bitcoin's money programmable, Bittensor makes the mining programmable.

**The Mining Programs** (v1): each of the 32 indexed subnets as a mining program, written down. Seven fields per subnet (the work, how it is scored, how the pay splits, who judges, how often it turns, who buys, what has been gamed), each with a source and a six-value trust level naming what the claim rests on: the chain, the code at a pinned commit, the subnet's own docs, a statement on record, the site's own reading, or not found. Where the sources disagree, the field says so. Live at [/programs/](https://legible.network/programs/) and on each subnet page as The program. Method at [/method/#the-programs-what-they-record](https://legible.network/method/#the-programs-what-they-record). A weekly drift check marks fields whose cited file has changed since the reading.

**The Subnet Legibility Index** (v1): what a first-time reader can find out about the 32 Bittensor subnets with the largest share of emission, in five minutes, from the subnet's own public materials. Scored for four audiences (stakers, miners, buyers, newcomers) on a four-question spine, 0 to 5 per cell. Findability, not quality. Live at [legible.network](https://legible.network). Rubric at [/method/#the-index-what-it-scores](https://legible.network/method/#the-index-what-it-scores). Method at [/method/#the-index-how-it-was-applied](https://legible.network/method/#the-index-how-it-was-applied).

**The Bittensor Narrative Map** (v2): who says what Bittensor is, in their own words, dated and sourced. The core object is a narrator (a person, the foundation, or a subnet team). Each narrator's entry is built only from verbatim statements with a source URL and a confidence level, read through one framework (a brand strategy skeleton turned on the narrator: mission, problem, opportunity, audience, what it is set against, positioning, value, the line they repeat, voice, their relation to the network, language, and for subnets their own frame) so narrators can be compared slot by slot. Metaphors are traced across narrators from first sourced use. Live at [/narrative/](https://legible.network/narrative/). Method at [/method/#the-map-what-it-records](https://legible.network/method/#the-map-what-it-records).

## Layout

| Path | What |
|---|---|
| `index.html` | The ranked index. Fetches `/data/summary.json`. |
| `about.md` | Source of truth for the about page, rendered by the build. |
| `sn/<netuid>/` | One page per subnet, generated. |
| `data/tokens-<date>.json` | Token snapshot: Taostats pool data, Kraken and MEXC pairs, CoinGecko tickers. Shown as one row on each subnet page. |
| `data/index.json` | The published dataset (CC BY 4.0). `summary.json` is the same minus evidence. |
| `data/chain-<date>.json` | Raw chain snapshots. `subnets.csv` is the frozen target list. |
| `data/scores-{a,b,c,d}.csv` | Agent output per slice. `scores.csv` is the merged, reviewed source of truth. |
| `agents/` | The scoring brief, per-agent slices, calibration set, summaries; `NARRATIVE-PROMPT.md` is the narrative research brief. |
| `scripts/` | The pipeline (below) and the site build. |
| `narrative/index.html` | The narrative map. Fetches `/data/narrative.json`. |
| `narrative/<id>/` | One page per person or institution, generated; subnet teams speak on their subnet page under What it says. `narrative/metaphors/` is the frames index. |
| `method.md` | Source of truth for the single method page at `/method/`: the scale, how the index was applied, what the map records, confidence, coverage, corrections, changelog. |
| `data/narrative/raw/<id>.json` | One file per narrator, written by a research agent against `agents/NARRATIVE-PROMPT.md` and validated by `scripts/narrative_check.py`. |
| `data/narrative.json` | The merged, published narrative dataset (CC BY 4.0). `narrative-pretty.json` is the same, indented. |
| `data/programs/raw/<netuid>.json` | One mining program manifest per subnet: seven sourced fields with a trust level each, written by a reading agent against `agents/PROGRAM-PROMPT.md` (three by hand as calibration) and gated by `scripts/program_check.py`. |
| `data/programs.json` | The merged, published programs dataset (CC BY 4.0). Rendered on each subnet page as The program, on the home close, and at `/programs/`. |
| `data/hyperparams-<date>.json` | Chain hyperparameters per subnet (tempo, immunity, commit-reveal), pulled by `scripts/pull_hyperparams.py`; cited by program fields at chain trust. |

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
# run one research agent per narrator with agents/NARRATIVE-PROMPT.md -> data/narrative/raw/<id>.json
python3 scripts/narrative_check.py                # validate every raw narrator file
.venv/bin/python scripts/pull_hyperparams.py      # chain hyperparameters for the 32, cited by the programs
# run four reading agents with agents/PROGRAM-PROMPT.md -> data/programs/raw/<netuid>.json
python3 scripts/program_check.py                  # validate every manifest (the publication gate)
python3 scripts/apply_program_corrections.py      # pending rows in data/program-corrections.csv -> the raw manifests
python3 scripts/build_site.py                     # narrative dataset and pages, index pages, subnet pages, OG images, chart, sitemap
python3 scripts/check_site.py                     # read-only checks
```

`build_site.py --narrative-raw <dir>` builds the map from a different directory of narrator files (a fixture, or a subset while research is still landing).

Narrative corrections (a misquote, a wrong date, a wrong speaker, a missing primary) are edits to the narrator's raw file, then a rebuild; the [narrative correction form](https://github.com/mikyodoorjey/legible.network/issues/new?template=correction.yml) collects them. Index corrections after publication go in `data/corrections.csv` and are applied with `scripts/apply_corrections.py`, which stamps provenance, rebuilds, and adds to the changelog.

## Local preview

`python3 -m http.server 8790` from the repo root, then `http://127.0.0.1:8790/`. To build the site against fixture data before real scores exist: `python3 scripts/build_site.py --data scripts/fixtures/sample.json`.

## Deployment

Static site on Vercel, no build step. `vercel.json` carries redirects, headers, and trailing slashes. `middleware.js` locks the site behind Basic Auth while `SITE_LOCKED=1`, with `PUBLIC_PATHS` for pages opened early.

## Licenses

Code MIT. Data CC BY 4.0, attribution "Subnet Legibility Index by Mikyö Clark, legible.network" for the index and "Bittensor Narrative Map by Mikyö Clark, legible.network" for the map. Fonts under the SIL Open Font License, in `scripts/fonts/`.
