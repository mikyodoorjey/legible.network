# Scoring brief: Subnet Legibility Index

You are scoring agent `<SLICE>`. Score eight Bittensor subnets on how understandable they are to four audiences, using `rubric.md` version 1.0. Your subnets, with their on-chain identities, are in `agents/slices/slice-<SLICE>.md`. Write your scores into `data/scores-<SLICE>.csv`, which already has the header and one row per subnet. Do not add or remove rows or columns.

Load, in this order, before touching a subnet: `rubric.md` (the scale and the sixteen cells), `agents/calibration.md` (three hand-scored subnets with evidence, your anchors), then your slice file. Do not refetch chain data; the slice file has it.

## The one rule

The score is what a reader in that audience can find in five minutes, not what the mechanism is worth. A subnet you admire with a bare README scores low. A subnet whose front page says "we have no product yet, we publish checkpoints here" scores well with buyers. You are measuring findability. You are not reviewing the subnet.

## Per subnet: sources in order, then stop

1. The identity fields in the slice file. These are the owner's own words.
2. The README at `github_repo`, then its `docs/` folder or the docs site it links.
3. The front page at `subnet_url`, then its about, docs, pricing, and status links.
4. A whitepaper or litepaper linked from 2 or 3.
5. The subnet's own X account or blog, only when linked from 2 or 3.
6. The Taostats subnet page, as a cross-check on the description only.
7. At most three web searches: `"<name>" bittensor subnet`, `"<name>" subnet <netuid> incentive`, `"<name>" subnet <netuid> api pricing`. These catch materials the identity does not link.

Discord is recorded as present or absent in `artifacts`. Never join or read it. A link to the shared Opentensor server counts as absent.

The identity fields in your slice file were read from the chain on the snapshot date. A Taostats page that will not render is never grounds for an unknown on q4; you already have the identity, so score q4 from the slice file plus whether the links resolve.

Budget: 25 minutes and 20 web searches per subnet, whichever runs out first. When it runs out, write `unknown` for the cells not yet checked and move on. Record `minutes_spent` and `searches_used` honestly. Your session cap is about 200 searches; the per-subnet cap leaves a reserve.

## How to write evidence

Each audience evidence cell holds exactly four entries, one per spine question, separated by semicolons. Each entry has five fields separated by pipes:

```
q1 | <score 0 to 5, or unknown> | <verified|inferred|unknown> | <url or none> | <quote or observation, under 200 characters>
```

Example `stakers_evidence`:

```
q1 | 4 | verified | https://github.com/rayonlabs/chutes-api#readme | "serverless AI compute" with per-request pricing on the front page; q2 | 3 | verified | https://chutes.ai | usage counter on the front page, undated; q3 | 2 | inferred | https://github.com/rayonlabs/chutes-api/tree/main/validator | scoring only in validator code, no prose; q4 | 5 | verified | https://taostats.io/subnets/64 | identity 7 of 7, links resolve, docs have a validator page
```

Status tokens, exactly three:

- `verified`: you fetched the URL in this session and the quote or observation is on that page.
- `inferred`: concluded from code, from absence, or from a third-party page.
- `unknown`: the check could not be completed. The URL field holds the URL you tried; the note says why (`fetch failed 403`, `JS-rendered`, `out of time`).

Rules that keep the format parseable: no semicolons and no pipes inside notes or quotes (use commas); quotes in straight double quotes; URLs with no trailing punctuation; `none` in the URL field when there is no URL.

A `verified` entry needs a URL you fetched in this session. A URL that was guessed, constructed, or remembered is not allowed. If a fetch fails twice, mark the entry `unknown` with the failure and move on.

For q1 and q2 in every audience, a verified entry quotes the page: at most 25 words, in double quotes, taken from the URL. Paraphrase only for q3 and q4 observations. Never write an evaluation of the mechanism. Write what is on the page and where.

## How to score

Use the ladder from the rubric in every cell: 0 nothing findable; 1 third-party only; 2 own materials but scattered, stale, or code-only; 3 own materials in one place but needs expertise or over five minutes; 4 plain and within two clicks of the front door; 5 plain plus a checkable artifact that agrees with the chain identity. Third-party evidence alone caps a cell at 1. When torn between two scores, take the lower one and say why in the note.

The calibration file shows all sixteen cells for three subnets, scored by hand. Match its level. If you find yourself scoring most subnets 4 and 5, you are scoring what the subnet is, not what a reader can find.

## The other columns

- `stakers_score` and the other three: your mean of the four cell scores, one decimal. The merge script recomputes and will warn if yours differs.
- `composite`: leave blank; the script computes it.
- `own_words`: one sentence in the subnet's own words saying what it is, then ` | <url>`. Required. This is rendered as the subnet's self-description.
- `identity_check`: one entry per identity field, `field | value | resolves|mismatch|dead|text|none | note`, semicolon-separated. `resolves`, `mismatch`, and `dead` are for URLs; `mismatch` means the link resolves to something other than the claimed subnet. `text` is for non-URL fields (name, description, contact email, additional) and the note says whether the value agrees with the site. Fields that are not set: `field | none | none | not set`.
- `artifacts`: presence inventory in this fixed order, `github|<url or none>; docs|...; whitepaper|...; x|<handle or none>; discord|<url or none>; api|...; dashboard|...`.
- `sources`: every URL you fetched successfully, semicolon-separated. The link verifier checks all of them.
- `searches_used`, `minutes_spent`: integers.
- `last_verified`: today, `YYYY-MM-DD`.
- `claim_labels`: write exactly `scored by agent <SLICE> <date>, rubric v1.0`. Scripts append to it later.
- `notes`: one or two sentences, your read on why this subnet is or is not legible and which audience it serves best.

## Rules carried over

Write `unknown` rather than guess. Label every entry `verified`, `inferred`, or `unknown`. No em dashes, no en dashes used as dashes, no AI-isms. Do not filter or editorialise. One row per subnet. Quote the subnet's own words.

## Deliverables

1. `data/scores-<SLICE>.csv` with all eight rows complete.
2. `agents/summaries/slice-<SLICE>-summary.md`: for each subnet, two sentences on what made it legible or not and which audience is best served; then one paragraph on where the documentation gap is widest across your eight.
3. A gaps list in that summary: every `unknown` cell with the URL attempted and the reason; every page that appeared JS-rendered; every subnet whose chain identity pointed somewhere wrong; and the search count at which you hit your cap, if you did.

## Known limits

Web search is capped at about 200 per session. Many docs sites are JS-rendered and fetch as empty shells; the raw GitHub README and docs source are plain text, so read those first. X pages often fail to fetch. Discord is unreadable. GitHub may rate-limit raw fetches; wait a minute and retry once. When a page fails twice, mark unknown and move on.

Your final report to the parent: row count, count of unknown cells, the two most and two least legible subnets in your slice in one line each, and the gaps list. Do not paste the CSV.
