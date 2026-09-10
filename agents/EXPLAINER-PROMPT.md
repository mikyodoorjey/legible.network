# Explainer brief: Subnet Legibility Index

You are writing agent `<SLICE>`. Write one plain-language explainer for each of the eight subnets in `agents/slices/slice-<SLICE>.md`. Work in `/Users/mikyoclark/Sites/legible.network`. Each explainer is a Markdown file at `data/explainers/<netuid>.md`.

## The reader

A smart person with no crypto or machine learning background: a journalist, a founder's parent, an enterprise buyer's lawyer, a curious staker. They have five minutes and one question: what is this thing, and why would anyone pay for it? Write for them, never for the subnet's own community. The reader may open the glossary at `data/explainers/glossary.md`; assume they have not.

## Sources, and nothing from memory

Every factual claim comes from one of two places:

1. The evidence already collected for this subnet in `data/index.json`: find the object with your `netuid`; use `own_words`, `identity`, `identity_check`, `artifacts`, and the sixteen cells under `audiences` (each has a `url`, a `note` with a quote, a `status`, and a `link` result). These were verified on 2026-09-09.
2. The subnet's own materials, re-fetched by you now: the README, the docs, the site, the paper. Prefer raw.githubusercontent.com when a page will not render.

If neither source says it, you do not say it. Where the sources disagree, say so in the entry. Where you conclude something rather than read it, mark it inline with the word "inferred" in parentheses, like this: "(inferred from the validator code)". Do not soften a gap and do not editorialize about the team. The explainer earns trust by being the first honest account, not the kindest one.

Budget: 25 minutes and 15 web searches per subnet. No em dashes anywhere. No AI-isms. No hype words. No sentence you would be embarrassed to read aloud to the subnet's founder.

## Metaphor

Every entry has one governing everyday comparison, introduced in the first sentence and carried through the whole entry. A cloud provider whose machines belong to strangers. A stock exchange for forecasts. A spelling bee where the dictionary changes daily. Choose the comparison that a reader would reach for themselves, keep it concrete (a place, a job, a market a person has stood in), and state, in one sentence somewhere in section 2 or 4, where the comparison breaks. A metaphor that never breaks is a slogan. Use a second comparison only when the mechanism section needs one, and never more than two in an entry. Gloss every specialist term on first use, in the sentence itself.

## The fixed structure

Write exactly these seven sections with these exact headings, in this order. The front matter is required.

```
---
netuid: 64
name: Chutes
commodity: inference
one_sentence: SN64 Chutes rents out AI model computing power by the request, the way a cloud provider does, except the machines belong to strangers who are paid in the subnet's token.
metaphor: a cloud provider whose machines belong to strangers
written: 2026-09-10
---

## In one sentence
## The commodity, explained from zero
## Why it is on Bittensor at all
## How the work gets done
## How you would know it works
## What is missing
## Go deeper
```

`commodity` is one of: `inference`, `compute`, `training`, `data`, `agents`, `forecasting`, `storage`, `security`, `media`, `science`, `other`. Pick the one the subnet's own output fits, not what its marketing says.

**In one sentence.** What the subnet produces, in a unit a person can picture, with the metaphor. One sentence, under 40 words, identical to `one_sentence` in the front matter.

**The commodity, explained from zero.** Two to four short paragraphs. What the digital commodity is. Why it has a price. Who buys it today, or, if nobody does yet, what would have to be true for someone to. Name customers only when the subnet's own materials name them.

**Why it is on Bittensor at all.** What decentralization changes for this commodity, concretely: cost, censorship, ownership, coverage, or nothing yet. If the honest answer is "nothing yet," say so in those words.

**How the work gets done.** Miners do X, validators check Y, the reward flows Z. Three to five sentences. Every protocol word glossed in the sentence.

**How you would know it works.** The one artifact a reader can check: a demo, a dashboard, a benchmark, a customer, a live endpoint. Name it and link it. Or the statement that no such artifact exists, in those words.

**What is missing.** The gaps the legibility score found, translated for this reader. Use the low-scoring cells in `data/index.json` for this subnet: "there is no price list", "the miner guide is a year old", "the only documentation is written for AI agents", "the on-chain contact address appears nowhere on the site". Two to five short sentences. Facts, not judgments.

**Go deeper.** At most three links, as a bulleted list, each with a five-word label: the front door, the best explainer, the mechanism document. Every link must be one you fetched in this session or one that appears in `data/index.json` for this subnet with a `link` result of `live`.

End the file with a `## Sources` section: a bulleted list of every URL you drew on, one per line, nothing else. The checker verifies each is live.

Length: 350 to 600 words from "In one sentence" through "Go deeper", not counting the front matter and Sources. No entry longer than the subnet deserves.

## Voice

Build the idea from zero. Say the most in the fewest beats. Plain sentences, one idea each. No borrowed vocabulary: not "leverage", not "ecosystem", not "cutting-edge", not "seamless", not "robust". Present tense. Say "the subnet" and "miners" and "validators"; never "we" or "you should". When you do not know, write "the materials do not say".

## Test before you finish

For each entry, ask: could a newcomer who read only this entry explain to a friend what the subnet makes, who would pay, and how they would check, in their own words, without opening another tab? If not, the entry is not done.

## Deliverables

1. Eight files `data/explainers/<netuid>.md` in the exact structure above.
2. `agents/summaries/explainers-<SLICE>.md`: one line per subnet with the metaphor you chose and the hardest thing to explain, then a paragraph on where the sources were thinnest.
3. Run from the repo root: `python3 scripts/check_explainers.py --only <netuid list>` if it exists, else `python3 -c "import re,glob; [print(f, len(re.sub(r'^---.*?---','',open(f).read(),flags=re.S).split('## Sources')[0].split())) for f in glob.glob('data/explainers/*.md')]"` and bring any entry outside 350 to 600 words into range.

Final report to me: the eight metaphors in one line each, any entry where the sources were too thin to write a section honestly, and the word count of each. Do not paste the entries.
