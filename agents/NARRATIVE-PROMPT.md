# Research brief: the Bittensor narrative map

You are a research agent building one entry in a person-centered ontology of how Bittensor is talked about. The core object is a **narrator**: a person, a foundation, or a subnet team. Your job is to collect what that narrator has actually said about Bittensor, verbatim and sourced, then fill a fixed narrative framework from those words and trace how the words changed over time.

You are assigned one narrator (or one small group). Write your result to `data/narrative/raw/<id>.json` in the format below, then run `python3 scripts/narrative_check.py data/narrative/raw/<id>.json` and fix anything it reports. Return a short coverage note, not the data.

## The one rule

Nothing without a source. Every quote is the narrator's own words, copied from a page, transcript, post, or video you reached in this session, with the URL you reached it at. If you cannot reach the source, the quote is not `verified`. Do not reconstruct a quote from memory. Do not smooth a quote. Do not invent a URL. A gap is recorded as a gap.

## Sources, in order

1. The narrator's own writing: blog, Substack, Medium, Mirror, docs, whitepaper, GitHub READMEs they authored, the bittensor.com pages if the narrator is the foundation.
2. Long-form interviews and podcasts with a public transcript or a YouTube page. Read the transcript or the description and chapters. If only a video exists and you cannot read a transcript, record the appearance in `appearances` with what you can verify (title, host, date, URL) and mark any quote from it `probable`, naming where the wording came from (a show-notes page, a clipping, a secondary article).
3. X posts. Try the direct URL, then archive.org, then threadreader or a quoting article. A post reachable only through a third party's quotation is `probable`.
4. Conference talks, press interviews, and articles that quote the narrator directly. A quote in a reputable article is `probable`, unless you can reach the primary.
5. Community writeups and paraphrases are `unverified`. Record them only when the wording is distinctive and there is no primary; they never enter the map without the flag.

Search budget: up to 40 web searches and 60 fetches. When you hit the budget, stop, write what you have, and list what you did not get to under `coverage.gaps`.

## Quote rules

- Verbatim, in the narrator's language, at most 60 words. Cut with an ellipsis inside the quote when the source runs long; never rewrite.
- Include enough context in `context` (your words, one sentence) to say what was being asked or discussed.
- Date every quote. `date_precision` is `day`, `month`, or `year`. If a post is undated but the page shows a year, use `year`.
- Never editorialise inside `quote` or `context`. Editorial reading goes in the framework slots, and there it must cite statement ids.
- Distinguish what the narrator said from what others said about them. Only the narrator's own words go in `statements`.
- Criticism, retractions, and reversals count as much as promotion. If the narrator disagreed with someone, record it with the `positioning.against` slot and, in `relations`, who they argued with.

## The framework (the slots)

Every statement is tagged with one or more slots. These are the sections of a brand strategy, turned on the narrator: not what Bittensor's brand is, but what this narrator's Bittensor is.

| Slot id | What it captures |
|---|---|
| `foundation.mission` | What they say Bittensor is for, what it does |
| `foundation.vision` | The world they say it builds |
| `foundation.values` | What they say it stands for or refuses |
| `problem.cultural` | What is broken in the world that Bittensor answers |
| `problem.market` | What is missing from current AI or crypto |
| `problem.institutional` | What is at risk if it fails, or who it is against |
| `opportunity` | Tailwinds they cite: timing, tech, market, regulation |
| `audience` | Who they are talking to and what they tell them (miners, validators, stakers, investors, developers, enterprises, newcomers) |
| `positioning.category` | The category frame: "a market for intelligence", "the Bitcoin of AI", "a language for markets" |
| `positioning.differentiator` | What makes it different in their telling |
| `positioning.reason` | The reason to believe they offer |
| `positioning.against` | What they set it against: OpenAI, hyperscalers, Ethereum, VC-backed AI, other subnets |
| `value.functional` | The concrete benefit they claim |
| `value.emotional` | The feeling they sell |
| `value.self_expressive` | What it says about the person who joins |
| `messaging.h1` | Their one-line vision, the sentence they repeat |
| `messaging.proof` | The evidence they point to |
| `voice` | A statement that shows their register more than their claim |
| `relationship` | How they talk about their own relation to the network: founder, steward, investor, critic, builder on it |
| `language.term` | A coinage or a naming decision: what they call things, or refuse to call them |
| `subnet.self` | Only for subnet narrators: how they describe their own subnet |
| `subnet.network` | Only for subnet narrators: how they describe Bittensor as a whole |

## Eras

Every statement gets an `era` from its date:

| Era id | Dates | Marker |
|---|---|---|
| `nakamoto` | 2021-01 to 2023-03 | mainnet, Kusanagi and Nakamoto networks, no subnets |
| `finney` | 2023-03 to 2023-10 | Finney network, single-subnet then the first subnets |
| `revolution` | 2023-10 to 2025-02 | Revolution upgrade, subnet expansion, root network |
| `dtao` | 2025-02 to 2026-06 | Dynamic TAO, alpha tokens, emission follows price |
| `current` | 2026-06 onward | emission follows the price moving average |

Statements before 2021-01 get `pre` (whitepaper era).

## Metaphors and themes

A **metaphor** is the figurative frame: a brain, a market, a hive, a language, a Bitcoin, a nation, a Cambrian explosion, a race, a garden. Record the exact wording as `wording` and give it a short `label` (lowercase, one to three words). A **theme** is the literal idea: decentralised intelligence, incentive design, permissionless entry, ownership, anti-OpenAI, censorship resistance, commodity markets, token economics, governance, validator power.

For each metaphor you record, say whether the narrator introduced it or is reusing it. If you find the same frame in another narrator's mouth, note the URL in `lineage_notes`; the merge step joins these across narrators.

## Output format

Write valid JSON, UTF-8, to `data/narrative/raw/<id>.json`:

```json
{
  "narrator": {
    "id": "jacob-steeves",
    "name": "Jacob Steeves",
    "aka": ["const", "Const"],
    "kind": "person",
    "role": "Co-founder, Opentensor Foundation",
    "affiliation": "Opentensor Foundation",
    "active_from": "2019",
    "handles": {"x": "@const_reborn", "github": "unconst"},
    "subnets": [],
    "one_line": "Who this is, in one sentence, your words."
  },
  "statements": [
    {
      "id": "jacob-steeves-001",
      "date": "2023-10-02",
      "date_precision": "day",
      "era": "finney",
      "quote": "…",
      "context": "One sentence in your words: where, to whom, in response to what.",
      "about": "network",
      "slots": ["positioning.category", "messaging.h1"],
      "themes": ["decentralised intelligence"],
      "metaphors": ["market"],
      "source": {
        "url": "https://…",
        "medium": "podcast|youtube|x|blog|whitepaper|docs|article|talk|discord|forum|other",
        "title": "…",
        "outlet": "Show or publication name, or the narrator's own channel",
        "timestamp": "00:14:32 or empty",
        "archive_url": "https://web.archive.org/… or empty",
        "transcript": "primary|auto|show-notes|secondary|none"
      },
      "confidence": "verified|probable|unverified"
    }
  ],
  "appearances": [
    {"date": "2024-05-10", "title": "…", "outlet": "…", "url": "https://…", "medium": "podcast", "note": "what it covered, one line; whether a transcript exists"}
  ],
  "metaphors": [
    {"label": "market", "wording": "a market for intelligence", "first_statement": "jacob-steeves-001", "origin": "introduced|reused|unknown", "lineage_notes": "seen also in … at URL"}
  ],
  "framework": {
    "foundation.mission": {"summary": "One or two sentences, your words, built only from the cited statements.", "statements": ["jacob-steeves-001"]},
    "…": {}
  },
  "language": {
    "words_used": ["incentive", "commodity", "…"],
    "words_avoided": ["…"],
    "coinages": [{"term": "…", "meaning": "…", "statement": "jacob-steeves-004"}]
  },
  "genealogy": [
    {"era": "nakamoto", "summary": "How they framed it then, two or three sentences, citing statement ids in brackets like [jacob-steeves-002].", "dominant_metaphor": "brain", "shift": "what changed from the previous era, or empty"}
  ],
  "relations": [
    {"to": "barry-silbert", "kind": "agrees|borrows|argues|responds|introduces", "statement": "jacob-steeves-009", "note": "one line"}
  ],
  "coverage": {
    "searches_used": 0,
    "fetches_used": 0,
    "well_covered": ["eras or media that are solid"],
    "thin": ["eras or media that are thin"],
    "gaps": ["what you did not reach and why: URL, reason"],
    "unreachable": ["URLs that failed"]
  }
}
```

Rules that keep it mergeable: statement ids are `<narrator-id>-NNN`, zero-padded, in date order. Slots come from the table. Era from the table. `about` is `network`, or `subnet:<netuid>` when the statement is about one subnet. Every framework slot you fill cites at least one statement id that exists. Leave a slot out rather than fill it without evidence. No em dashes, no en dashes as dashes, no AI-isms in your own sentences.

Target: 25 to 60 statements for a major narrator, spread across the eras they were active in; 8 to 20 for a smaller one. Breadth across time beats depth in one interview. If a narrator has one famous line they repeat, record its earliest and latest instance so the map can show the span.

For a subnet group: one narrator object per subnet team (id `sn<netuid>`, kind `subnet`, `subnets: [<netuid>]`), each in its own file `data/narrative/raw/sn<netuid>.json`. Founders who speak for the subnet are quoted under the subnet narrator, with the speaker's name in `context`. Split statements between `subnet.self` and `subnet.network`.

## Deliverable

1. `data/narrative/raw/<id>.json`, validated.
2. A reply of at most 200 words: statement count by era and confidence, which media you reached, and the three largest gaps.
