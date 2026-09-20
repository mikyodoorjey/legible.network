# Program brief: Mining Programs

You are reading agent `<SLICE>`. Write one mining program manifest for each of the eight subnets in `agents/slices/slice-<SLICE>.md`. Work in `/Users/mikyoclark/Sites/legible.network`. Each manifest is a JSON file at `data/programs/raw/<netuid>.json`. Run `python3 scripts/program_check.py data/programs/raw/<netuid>.json` after each one and fix what it reports before moving on.

Load, in this order, before touching a subnet: this brief, then the three calibration manifests in `data/programs/raw/` for SN120, SN64 and SN107 (hand-written, your anchors for depth and tone), then your slice file.

## What a manifest is

The site's argument is that a subnet is a mining program: what Bitcoin hard-coded, a subnet writes. The manifest is that program read aloud. Seven fields, each answering one question a validator, a miner, or a buyer asks first, each with a source and a trust level that names what kind of thing the claim rests on. The index measures whether a reader can find the puzzle. The manifest records what the puzzle is.

You are not reviewing the subnet. You are not scoring it. You are writing down what its program says, where it says it, and how far a reader can trust the reading.

## The seven fields

| Field | The question | Where it usually lives |
|---|---|---|
| `work` | What is a miner paid to produce? | The README, the docs, the explainer's one sentence |
| `scoring` | How does a validator judge it, against what, with what formula? | Validator code, a scoring doc, a scoring endpoint |
| `split` | How does the subnet's miner share divide between miners? Winner takes all, equal shares, proportional, decaying? | Weight-setting code, a network config |
| `judges` | Who validates, how many, and what may they do: set weights, commit-reveal, re-run the work, sample it? | The chain hyperparameters, validator code, the metagraph |
| `cadence` | How often does the puzzle turn: tempo, rounds, windows, challenges? | The chain tempo, a round interval in code or config |
| `buyer` | Who pays for the output today, and how? | A pricing page, a customer statement, or nothing |
| `exploits` | What have miners optimized instead of the work, and what did the program do about it? | Anti-gaming docs, guardrails in code, a statement in the map, an audit log |

The protocol's default split of emission between miners, validators and the owner is not the `split` field. The field is how the miner share divides among miners, because that is what the program decides.

## Trust, six values

`trust` says what kind of thing the claim rests on, in descending order of what a reader can check for themselves.

| Trust | Means | Needs |
|---|---|---|
| `chain` | A value read from the chain: a hyperparameter, a metagraph count | `snapshot`, the path of the data file it was read from |
| `code` | Read in the subnet's repository at the pinned commit | `path` inside the repo, `url` to the file at that commit, `quote` of the line or value |
| `docs` | The subnet's own prose: README, docs site, front page, paper, llms.txt | `url` fetched this session, `quote` under 25 words from that page |
| `said` | A statement in the narrative map | `statement`, the id in `data/narrative.json`, plus its `url` and `quote` |
| `read` | The site's own inference from code, absence, or a third party | `url` of what you inferred from, `quote` of what it shows |
| `unknown` | Looked for and not found | `text` saying what you looked for and where; no `url`, no `quote` |

Prefer the highest trust you can earn. A scoring formula that is in the code at `code` beats the same formula in the docs at `docs`. Do not claim `code` for a file you did not open. Do not claim `docs` for a page you did not fetch this session.

When the sources disagree, and they often do, the field carries the highest-trust reading in `text` and the disagreement in `disagrees`, one sentence naming both readings and both sources. Three calibration manifests each carry one. A manifest that finds a disagreement is doing its job.

## The shape

```json
{
  "netuid": 120,
  "name": "Affine",
  "version": "1.0",
  "read_on": "2026-09-20",
  "commodity": "training",
  "repo": { "url": "https://github.com/AffineFoundation/affine", "commit": "1c3b5999fbbc10e71fcd7430c018f205ba1980ea", "committed": "2026-09-10" },
  "fields": {
    "work":     { "text": "...", "trust": "docs", "url": "...", "quote": "..." },
    "scoring":  { "text": "...", "trust": "code", "path": "affine/affine/score.py", "url": "...", "quote": "...", "disagrees": "..." },
    "split":    { "text": "...", "trust": "code", "path": "...", "url": "...", "quote": "..." },
    "judges":   { "text": "...", "trust": "chain", "snapshot": "data/hyperparams-2026-09-20.json", "quote": "..." },
    "cadence":  { "text": "...", "trust": "chain", "snapshot": "data/hyperparams-2026-09-20.json", "quote": "..." },
    "buyer":    { "text": "...", "trust": "read", "url": "...", "quote": "..." },
    "exploits": { "text": "...", "trust": "said", "statement": "sn120-002", "url": "...", "quote": "..." }
  },
  "sources": ["..."]
}
```

`commodity` uses the explainer's set: `inference`, `compute`, `training`, `data`, `agents`, `forecasting`, `storage`, `security`, `media`, `science`, `other`. Copy it from the explainer's front matter. `repo` is the subnet's repository from the index's `artifacts.github`; `commit` is the head you read, `committed` is that commit's date. If there is no repository, omit `repo` and no field may claim `code`.

`text` is the reading, under 70 words, in plain sentences a buyer's lawyer could follow. Gloss the protocol word in the sentence. `quote` is the evidence: the words on the page, the line of code, or the value read, under 25 words, no editorial. `sources` lists every URL you fetched successfully; the link verifier checks all of them.

## Sources, in order, then stop

1. `data/index.json`, the object for your netuid: `own_words`, `artifacts`, the sixteen cells under `audiences`. The q3 cells for miners and stakers usually point at the scoring. The buyers cells usually settle `buyer`.
2. `data/explainers/<netuid>.md`: the one sentence is a candidate `work`; the section "How the work gets done" is a candidate `scoring` at `docs` trust, and it names the file to open for `code`.
3. `data/narrative.json`: every statement whose `about` is `subnet:<netuid>` or whose quote names the subnet. These are candidates for `exploits` at `said` trust, and sometimes for `buyer`.
4. `data/hyperparams-<date>.json`, the latest: tempo, immunity period, commit-reveal, weights rate limit, for `judges` and `cadence` at `chain` trust. `data/chain-<date>.json` has the validator and miner counts.
5. The repository at `artifacts.github`: clone shallow into your scratch directory, record the head commit and its date, open the validator, the scoring module, the weight-setting code, and any config file. Prefer raw.githubusercontent.com URLs at the pinned commit for `url`.
6. The subnet's own docs: README, docs site, front page, llms.txt, a scoring or network-config endpoint if the explainer names one.
7. At most three web searches, only for `buyer` and `exploits`: `"<name>" bittensor subnet customers`, `"<name>" subnet <netuid> exploit OR gaming OR sybil`.

Discord is never read. Budget: 25 minutes and 20 web searches per subnet. When it runs out, write `unknown` for the fields not yet settled and move on.

## Rules

- Write `unknown` rather than guess. An `unknown` field says what you looked for, in `text`, so the next reader does not repeat the search.
- Never evaluate the mechanism. "The scoring rewards short answers" is a reading of code and goes in `text` at `read` trust with the line quoted. "The scoring is weak" goes nowhere.
- One repository commit per manifest. Everything at `code` trust was read at that commit.
- Quote the value, not your paraphrase: `SCORING_INTERVAL = "1 day"` is a quote; "the window is a day" is text.
- No em dashes, no en dashes as dashes, no AI-isms, no hype words. Straight double quotes inside JSON strings are escaped.
- Every `url` in a field appears in `sources`. The check script enforces this.

## Deliverables

1. Eight manifests in `data/programs/raw/`, each passing `scripts/program_check.py`.
2. `agents/summaries/programs-<SLICE>-summary.md`: for each subnet, one line naming the lowest-trust field and why; then every `disagrees` you recorded, in one list; then every `unknown`, with what was looked for.

Your final report to the parent: eight file names, the count of fields at each trust level across your slice, the disagreements list, and the unknowns list. Do not paste the JSON.
