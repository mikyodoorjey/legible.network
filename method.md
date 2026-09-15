# Method

Version: 2.0
Scale version: 1.0
Scores dated: 2026-09-21
Corrections window: 48 hours from publication
Data: /data/

## What Legible measures

Bittensor pays on perception: since June 2026 a subnet's share of emission follows the market price of its token, and the price follows what people can see. Legible records what there is to perceive, from two sides. The index reads a subnet's own public materials for what the subnet **shows** a first-time reader in five minutes. The map reads the words of the people around the network, founders, the foundation, investors, analysts, and subnet teams, for what is **said** the network is. The two are the same measurement from two sides, and the chart on the index page, says versus shows, is where they meet.

Neither side judges a mechanism. The index scores findability, not quality. The map records words, not truth. Both carry their evidence on every page: a URL, a date, and a confidence status on every quote.

Two vocabularies are kept apart on purpose. **Scoring** belongs to the puzzle: a subnet's incentive mechanism scores miners. The index's number is **legibility**, out of five, and is never called a score on the site; the method keeps the word composite for the arithmetic.

## The argument

The home page opens with one argument: Ethereum made Bitcoin's money programmable, and Bittensor makes the mining programmable. It is one person's reading of the network, and the instruments do not depend on it. The index would score the same subnets the same way if the argument were wrong, and the map records what narrators say whether or not it agrees with them.

What the argument takes from the record is its lineage. The phrase has four sourced uses in the map: Jacob Steeves in October 2025 as the antecedent, Mark Jeffrey on 19 February 2026 as the first exact use on record, Ala Shaabana on 25 March 2026 as the shorthand, and the foundation's own about page on 15 September 2026 for the Ethereum comparison, which the foundation lands on markets and the argument lands on mining. The home page links each. The choice of word, and the line that Bittensor programs work that can only be verified by judging it, are the argument's own, and are credited to nobody in the record.

## The index: what it scores

### What this measures

Every cell in this rubric scores one thing: what a first-time reader in a given audience can find in five minutes from public sources, weighted toward the subnet's own materials.

It does not score whether the mechanism is good, whether the token is a good buy, whether the team is competent, or whether the subnet will exist next year. A subnet whose front page says plainly "there is no product yet, and here is why" scores well with buyers, because the buyer got their answer in one click. A brilliant mechanism documented only in validator code scores low with stakers, because the staker could not find it.

Legibility is not marketing. It is whether the subnet has told the people who fund it, work for it, buy from it, and encounter it what it is, in a place they will look.

### Who is reading

Four audiences, each with one question. Four is the ceiling.

| Audience | Their question | What they need to find |
|---|---|---|
| Stakers and validators | Should I allocate here? | The commodity, the demand, the anti-gaming design, the emissions logic |
| Miners | Can I compete, and what wins? | The task spec, the scoring, the hardware, the entry cost, the churn |
| Buyers and enterprises | Can I use this today? | The product, the API, the pricing, the reliability, who to call |
| Newcomers | What is this and why does it matter? | A plain-language account, what is novel, proof it works |

Regulators, the foundation, and the press read the buyer and newcomer accounts. They are not separate audiences here.

### Sources that count, in order

1. The on-chain subnet identity: the seven fields the owner sets (`subnet_name`, `github_repo`, `subnet_contact`, `subnet_url`, `discord`, `description`, `additional`). These are the subnet's own words and the first thing a wallet or explorer shows.
2. The GitHub README and docs folder at `github_repo`, and any docs site they link.
3. The site at `subnet_url`: its front page and its about, docs, pricing, and status links.
4. A whitepaper or litepaper linked from 2 or 3.
5. The subnet's own X account and blog, when linked from 2 or 3.
6. Third-party pages: the Taostats description, community explainers, posts by others.

Third-party evidence alone caps a cell at 1. Discord is recorded as present or absent and never read; a link to the shared Opentensor server counts as absent.

### The scale, applied in every cell

| Score | What it means for you | The scoring rule |
|---|---|---|
| 0 | Nobody can tell you | Nothing findable on the question in five minutes from any public source |
| 1 | Only other people can tell you; the subnet itself doesn't say | Findable only in third-party sources, only by asking in Discord, or mentioned in passing in the subnet's own materials without answering the question |
| 2 | It's in there somewhere, but scattered, out of date, or buried in code | The subnet's own materials touch it, but scattered across pages, stale (contradicted by current code or chain state), or readable only in code |
| 3 | You'd find it, but you'd need to already know Bittensor or dig for a while | Stated in the subnet's own materials in one place, but the reader needs Bittensor or domain knowledge, or more than five minutes, to act on it |
| 4 | You'd get your answer on your own in about five minutes | Stated plainly in one place within two clicks of the README, the docs root, or the site front page; a first-time reader gets it in under five minutes |
| 5 | You'd have everything, with proof you can check, in a couple of clicks | As 4, plus a concrete artifact the reader can check (a number with a date, a table, a schema, a live endpoint, a diagram, a worked example), and it agrees with the on-chain identity |

A file written for machines (an `llms.txt`, an `AGENTS.md`, a handoff document) is the subnet's own material and counts as a source. It is scored on what it contains, and its register decides between 3 and 4: a first-time human reader who has to translate it is not getting the answer plainly.

"One place" means one page, or one page plus a link it points to. Plain statements spread across three pages that each answer part of the question are scattered, and score 2, even when each part is clear.

When torn between two scores, take the lower one and say why.

### The sixteen cells

Each audience is scored on the same four-question spine. For every cell: the reader's question, the evidence that counts, and what a 5 and a 2 look like.

**Stakers and validators**

**S1. What it is.** "What does this subnet produce that someone pays for, and in what unit?" Evidence: a commodity statement naming the output (inference tokens, GPU hours, model checkpoints, forecasts, datasets) and its unit. A 5 puts the output and unit on the front page, matching the on-chain description. A 2 is a tagline like "decentralized AI for everyone" with the actual output only inferable from code.

**S2. Who it is for.** "Who is using it today, and how would I see demand?" Evidence: usage figures, named customers, revenue or buyback statements, a dashboard. A 5 is a dated usage or revenue figure, or a live dashboard, on the subnet's own site, and it agrees with the subnet's other pages. A dashboard that reads zero while the docs describe live activity is a 3 at most. A 2 is "used by many" with no number, or numbers only in a months-old post.

**S3. How it resists gaming or fails.** "How do validators score, how do they stop miners cheating, and what would kill this subnet?" Evidence: an incentive mechanism document, a validation description, a known-attacks or limitations section, a statement of how emissions are earned. A 5 is a named incentive document with an anti-gaming section and stated failure modes. A 2 is a mechanism that exists only as validator code.

**S4. Identity and documentation.** "Is the chain identity filled in, do the links resolve, and is there a page written for stakers?" Evidence: the seven identity fields, links resolving to the claimed subnet, a staking, tokenomics, or validator page. A 5 is identity at 7 of 7 with every link resolving, plus a staker-facing page. A 2 is identity at 3 fields or fewer, or links pointing at a dead or renamed project.

**Miners**

**M1. What it is.** "What exactly does a miner do: request in, response out?" Evidence: a task specification with input and output shape. A 5 is a spec with a schema and a worked example. A 2 is a task only inferable from a protocol file.

**M2. Who it is for.** "What kind of miner wins, on what hardware, and what does entry cost?" Evidence: hardware requirements, the registration cost or where to read it, an honest competitiveness statement. A 5 is a hardware table, the current registration cost or where to read it, and a plain statement of what it takes to be competitive. A 2 is "a GPU is recommended" and nothing else.

**M3. How it resists gaming or fails.** "How is my output scored, and what gets me deregistered?" Evidence: the scoring formula in prose, weights, immunity period, churn or deregistration policy. A 5 is scoring described in prose with example numbers and a stated churn or immunity policy. A 2 is scoring only in code, no prose.

**M4. Identity and documentation.** "Can I get a miner running from the docs, and are they current?" Evidence: a step-by-step miner guide, versioned releases or a changelog, a last-updated date consistent with recent commits. A 5 is a guide that matches the current release, updated within 90 days. A 2 is a guide that references removed flags or an older network version.

**Buyers and enterprises**

**B1. What it is.** "What can I buy or call today?" Evidence: a product page, an API endpoint, a hosted app. A 5 is a product page with an endpoint or app and a working example. A plain "no product yet; outputs are X; expected date Y" scores 4. A 2 is a product implied by marketing copy with no way to reach it.

**B2. Who it is for.** "Is this for me, and what does it cost?" Evidence: a target-customer statement and pricing. A 5 is a pricing page plus a named customer type. A 2 is "contact us" with no customer type or price.

**B3. How it resists gaming or fails.** "What happens when it breaks: uptime, SLA, status page, support path?" Evidence: a status page, an SLA, uptime history, incident posts, a support channel with a response expectation. A 5 is a status page or SLA and a stated escalation path. A 2 is Discord as the only support path.

**B4. Identity and documentation.** "Where are the API docs, and who do I call?" Evidence: an API reference, `subnet_contact` set on chain and matching the site, a named business contact or form. A 5 is an API reference plus a contact that matches the chain identity. A 2 is docs with no contact anywhere.

**Newcomers**

**N1. What it is.** "In one paragraph, what is this?" Evidence: a plain-language paragraph without unexplained crypto or ML jargon. A 5 is that paragraph on the front page, consistent with the on-chain description. A 2 is a technical README opening, or a chain description that is a full sentence and nothing more. A chain description that is only a tag, like two words with no verb, is a 1.

**N2. Who it is for.** "What does this do that a centralized service does not, and who cares?" Evidence: an explicit statement of the difference decentralization makes here. A 5 is a concrete stated difference (cost, censorship, ownership, coverage) with a comparison. A 2 is a generic "decentralized" claim.

**N3. How it resists gaming or fails.** "How would I know it works?" Evidence: a live demo, dated output samples, benchmarks, a comparison. A 5 is a demo or a dated benchmark on the subnet's own site. A 2 is a claim of results with no artifact.

**N4. Identity and documentation.** "Is there a front door?" Evidence: `subnet_name` matches the site, `description` is a human sentence, `subnet_url` resolves, and the site has an about or learn page. A 5 is all four true. A 2 is a name mismatch between chain and site, or no site.

### Composite, as defined

Each audience score is the mean of its four cell scores, to one decimal. The composite is the mean of the four audience scores, equal weights, to one decimal. The weights are part of version 1.0; changing them is a version bump.

The composite is a summary, not the finding. The finding is the per-audience view: a subnet that stakers can read and buyers cannot is a different subnet from one that reads the same to everyone.

### Unknown

A cell is unknown when the scorer could not check it within the cap: a page that would not load, a site that needs a browser, time that ran out. Unknown is not zero.

Unknown cells are left out of the audience mean while three cells are scored. With two or more unknown cells the audience is unscored, and the composite is computed over the scored audiences and marked partial. Nothing is published with an unknown cell: before publication every unknown is either resolved by hand, with a dated note, or scored 0 with the note "nothing found by hand," also dated. Unknown exists only between the scoring run and publication.

### What is not scored

Mechanism quality. Token price or return. Team reputation. Anything that needs more than five minutes to find. Anything only in Discord. Anything a reader would have to be told by a person.

### Versioning

This is version 1.0. A new version changes the anchors, the weights, the sources that count, or the number of cells. Corrections to individual scores under the same rubric do not change the version; they are logged in the changelog with the date, the cell, the old and new score, and who asked.

### Proposing a change

Before scores publish on 2026-09-21, proposals to change an anchor or a source rule are welcome by GitHub issue or email, and will be answered before scoring begins. After that date, proposals go into version 1.1.

## The index: how it was applied

The index scores the 32 Bittensor subnets with the largest share of TAO emissions on one question: what can a first-time reader in a given audience find out about this subnet in five minutes from public sources? Four audiences, four questions each, sixteen cells per subnet, scored 0 to 5 on the scale above. This part is how the scale was applied.

### Which subnets

The set is the top 32 by share of TAO emission on the snapshot date, read from Taostats. Membership was frozen at the first snapshot so that the scores, the essay, and every conversation refer to one set. Active miner and validator counts and registration cost are Taostats' figures on the snapshot date; alpha price and identity come from the chain through the Bittensor SDK. Later snapshots refresh emission share, counts, and identities but do not change membership; a subnet that leaves the top 32 after the freeze stays in the index with a note. Since June 2026 a subnet's share of emission follows the moving average of its token price, so the ranking is a ranking of what the market currently pays for, not of quality.

### Sources, in the order a scorer looks

1. The on-chain subnet identity: seven fields the owner sets. Read directly from the chain through the Bittensor SDK on the snapshot date.
2. The GitHub README and docs at the repository the identity names, and the docs site they link.
3. The site the identity names: front page, about, docs, pricing, status.
4. A whitepaper or litepaper linked from the repository or the site.
5. The subnet's own X account or blog, when linked from the repository or the site.
6. The Taostats subnet page, as a cross-check on the description only.
7. At most three web searches per subnet.

Discord is recorded as present or absent and never read. A link to the shared Opentensor server counts as absent.

### Scoring

Scores were drafted by four research agents working in parallel, each on eight subnets interleaved by rank so that no agent had only large or only small subnets. Every agent worked from the same brief, the same rubric, and the same three hand-scored calibration subnets. Each agent had a cap of 25 minutes and 20 web searches per subnet; when the cap ran out, the remaining cells were marked unknown rather than guessed.

Every cell was then reviewed by a person before publication. Cells were queued for close review when they were unknown, scored 0 or 5, inferred with a score of 3 or more, in the top or bottom five subnets by composite, or backed by a link that did not resolve. The reviewer could keep, change, or send a cell back for a second look. Every change is recorded in the subnet's provenance line with the date. Nothing was published with an unknown cell.

### Evidence

Each cell carries one piece of evidence: a score, a status, a URL, and a quote or observation. The status is the scorer's provenance:

| Status | Meaning |
|---|---|
| verified | The scorer fetched the URL and the quote or observation is on that page |
| inferred | Concluded from code, from absence, or from a third-party page |
| unknown | The check could not be completed before publication; resolved by hand or scored 0 with a dated note |

Every URL was then checked by a script before publication, and each cell also carries the result of that check: live, redirected, unreachable, or manual for pages that cannot be checked by machine (X, Discord). A verified cell whose URL was unreachable at publication is shown as inferred.

Quotes are the subnet's own words, at most 25 words, taken from the page at the URL. The scorer never evaluates the mechanism; the evidence says what is on the page and where.

### Identity

The seven on-chain identity fields are `subnet_name`, `github_repo`, `subnet_contact`, `subnet_url`, `discord`, `description`, and `additional`. Completeness is the count of fields that are set. Each set field was also checked for whether it resolves to the claimed subnet. The identity is the subnet's own words and the first thing a wallet or explorer shows, which is why it anchors the fourth question in every audience.

### Provenance

Every subnet carries a provenance line that every step appends to: the agent and date that scored it, the merge, the review decisions, the link check, and any corrections. It is shown on the subnet's page so that a reader can see how a score came to be.

### Snapshots

The chain snapshot, the scores, and the link check each carry a date, shown in the top strip of every page. Old snapshots are kept in the repository. The index will be re-run at intervals; each run is a new dated version and the changelog records rescores.

### Known limits

Web search during scoring was capped, so some subnets were scored with fewer searches than others; the number of searches used is recorded per subnet. Some documentation sites render only in a browser and fetch as empty pages; those cells were checked by hand or marked unknown before review. X pages often fail to fetch. Headcount, funding, and team are not scored and not recorded. The index measures what can be found, not what is true.

## The map: what it records

### What the map is

The narrative map records how Bittensor is talked about, by whom, and how the talking changed. The core object is a narrator: a person, a foundation, or a subnet team. Each narrator's entry is built only from their own words on the record, dated and linked to the source, then read through a fixed framework so that narrators can be compared slot by slot. Across narrators the map traces metaphors: which frame appeared first, in whose mouth, who picked it up, and whether it is still in use.

It is a companion to the [index](/sn/). The index asks what a subnet shows a reader. The map asks what the people around the network say it is.

### Objects

| Object | What it is | Where it lives |
|---|---|---|
| Narrator | A person, institution, or subnet team with a public voice on Bittensor | one page each under /narrative/ |
| Statement | A verbatim quote of at most 60 words, dated, with a source URL, medium, and confidence | on the narrator's page and in the map |
| Source | The URL the quote was taken from, the outlet, the medium, a timestamp for audio or video, and an archive link when one exists | inside each statement |
| Slot | The framework position a statement evidences (below) | tags on each statement |
| Metaphor | A figurative frame, recorded in its exact wording and labelled in one to three words | the [frames](/narrative/metaphors/) |
| Theme | A literal idea a statement carries, such as incentive design or permissionless entry | tags on each statement |
| Era | The dated phase of the network a statement falls in | tags on each statement |
| Relation | Agrees, borrows, argues, responds, introduces, from one narrator to another, backed by a statement | on the narrator's page |

### The framework

The framework is a brand strategy skeleton turned on the narrator. It does not describe Bittensor's brand. It describes this narrator's Bittensor: what they say it is for, what problem it answers, who they address, what they set it against, how they position it, what benefit they claim, what line they repeat, in what register, and what they call things.

| Section | Slots |
|---|---|
| 1. Foundation | mission, vision, values |
| 2. The problem | cultural, market, institutional |
| 3. The opportunity | tailwinds |
| 4. Audience | who they address and what they tell them |
| 5. Competitive positioning | what they set it against |
| 6. Positioning statement | category frame, differentiator, reason to believe |
| 7. Value proposition | functional, emotional, self-expressive |
| 8. Messaging hierarchy | the line they repeat, the proof they point to |
| 9. Voice | register; words used and avoided |
| 10. Narrator and network | how they describe their own relation to it |
| 11. Language conventions | terms and coinages |
| 12. Subnet frames | for subnet teams only: their subnet, and the network |

A slot is filled with a short synthesis written from the cited statements only, and every synthesis names the statements it rests on. A slot with no evidence is left out rather than filled.

On screen the slots carry reader names. The data keeps the identifiers.

| On screen | Identifier |
|---|---|
| What it is for · The world it builds · What it stands for | foundation.mission · foundation.vision · foundation.values |
| What is broken · What is missing · What is at risk | problem.cultural · problem.market · problem.institutional |
| Why now | opportunity |
| Who they address | audience |
| What it is against | positioning.against |
| What they call it · What makes it different · Why believe them | positioning.category · positioning.differentiator · positioning.reason |
| What you get · How it feels · What joining says about you | value.functional · value.emotional · value.self_expressive |
| The line they repeat · The proof they point to | messaging.h1 · messaging.proof |
| How they sound | voice |
| Their stake in it | relationship |
| Their words for things | language.term |
| Their subnet, in their words · Bittensor, in their words | subnet.self · subnet.network |

### Eras

| Era | Dates | Marker |
|---|---|---|
| Whitepaper | to 2020 | before mainnet |
| Nakamoto | 2021 to early 2023 | mainnet, the Kusanagi and Nakamoto networks, no subnets |
| Finney | 2023 | the Finney network and the first subnets |
| Revolution | late 2023 to early 2025 | the Revolution upgrade, subnet expansion, the root network |
| Dynamic TAO | 2025 to mid 2026 | alpha tokens; emission follows price |
| Current | mid 2026 on | emission follows the price moving average |

## The map: how it was researched

### Sources, in the order a researcher looks

1. The narrator's own writing: blog, newsletter, docs, whitepaper, repositories they authored, and, for the foundation, bittensor.com and its archived captures.
2. Long-form interviews and podcasts with a transcript or a page. When only a video exists, the appearance is recorded and any quote from it is marked probable with the page the wording came from.
3. Posts on X, reached directly, through an archive, or through a mirror that returns the full primary text (the mirror is recorded as the archive link). A post reachable only through a third party's quotation is probable.
4. Talks, press interviews, and articles that quote the narrator directly. A quote in a reputable article is probable unless the primary source was reached.
5. Community writeups and paraphrases, recorded only when the wording is distinctive and nothing better exists. They never enter the map without the unverified flag.

Discord is not read. Private channels are not read. Nothing a narrator said off the record is recorded.

### Confidence

| Status | Meaning |
|---|---|
| verified | The researcher reached the primary source in the session and the words are on it |
| probable | A secondary source quotes the narrator, or the primary exists but could not be read (a video without a transcript, a post that would not render) |
| unverified | A community paraphrase or a quote with no reachable source; shown only when flagged |

Only verified and probable statements are counted in the map's totals by default. The map has a switch to include unverified statements and shows them with a red badge.

### How the research was done

Each narrator was researched by an agent working from one brief, with a cap of 40 searches and 60 fetches. The agent wrote statements verbatim with their sources, tagged them, filled the framework from those statements only, and wrote a genealogy by era citing statement ids. A validator rejects any file where a synthesis cites a statement that does not exist, a date does not match its era, a quote runs over 60 words, or a slot, era, or medium is outside the contract. The merge step joins metaphors across narrators by label and dates each one to its earliest sourced use.

Every source URL is then checked by a script before publication, and each statement carries the result: live, redirected, unreachable, or manual for hosts that cannot be checked by machine (X, Discord, Medium, the archive). A verified statement whose URL is unreachable at publication keeps its status, since the researcher reached it, but the badge says it may have moved.

The map is only as good as what could be reached. The coverage table below says, per narrator, what was found and what was not.

### Limits

Transcripts of podcasts and videos are often machine generated, and a quote from one carries that transcript's errors; the transcript kind is recorded on every statement. Posts on X frequently fail to fetch, and much of the early network's talk happened on Discord, which is not read. Statements were collected in English. The map is a sample of what could be reached in a bounded session, not a census of everything said. Absence from the map is not evidence of silence.

## Confidence, on both sides

One vocabulary for both instruments. Verified means the same thing on both sides: the primary source was reached in the session and the words are on it. The other two statuses are defined per side, because the sides read different kinds of source.

| On screen | On the index | On the map |
|---|---|---|
| verified | The scorer fetched the URL and the quote or observation is on that page | The researcher reached the primary source and the words are on it |
| secondhand | Concluded from code, from absence, or from a third-party page (recorded as inferred) | A secondary source quotes the narrator, or the primary exists but could not be read (recorded as probable) |
| unconfirmed | The check could not be completed before publication (recorded as unknown; resolved by hand or scored 0 with a dated note) | A community paraphrase or a quote with no reachable source (recorded as unverified; hidden on the map unless switched on) |

The data files keep the original tokens named in brackets, so nothing published before this version changes meaning.

Every source URL on both sides is also checked by a script before publication, and each quote carries the result: live, redirected, unreachable, or manual for hosts that cannot be checked by machine (X, Discord, Medium, the archive).

## Coverage

<!-- coverage:start -->
Pending.
<!-- coverage:end -->

## Corrections

One route for both instruments. Corrections are welcome and expected.

- A [GitHub issue](https://github.com/mikyodoorjey/legible.network/issues/new?template=correction.yml) using the correction form, which asks first whether it is about a legibility score, a quote in the map, or a link.
- Email to the address on the [about](/about/) page with the subnet or narrator, the cell or statement id, what is wrong, and the public URL.

**For the index.** During the 48-hour window after publication, corrections of fact (a dead link, a wrong repository, a page the scorer missed) are applied as they arrive. Score disputes are collected and applied together at the close of the window with a public note, so that no subnet gets a quiet edit. After the window, corrections still apply and are dated; a subnet that adds documentation is rescored in the next version. What qualifies: a public page that a first-time reader would find within the sources above, which the scorer missed or misread. What does not: a page created after the snapshot date (that is a rescore, not a correction), a page only reachable through Discord, or an argument that the mechanism deserves a higher score than its documentation earns.

**For the map.** A misattributed quote is removed first and argued after. What qualifies: a quote whose wording differs from the source, a wrong date, a wrong speaker, a source that does not say what the entry says it says, a missing primary that would upgrade a secondhand statement, or a public statement the map should carry. What does not: an argument that a narrator meant something other than what they said. The map records the words; the reading is the reader's.

## Changelog

<!-- changelog:start -->
No corrections yet.
<!-- changelog:end -->

## Data and licence

The index is published at /data/index.json with a lighter /data/summary.json; the map at /data/narrative.json. Both are CC BY 4.0. Attribution: "Subnet Legibility Index by Mikyö Clark, legible.network" for the index and "Bittensor Narrative Map by Mikyö Clark, legible.network" for the map. Quotations inside the map remain the words of the people quoted: at most 60 words each, attributed, dated, and linked. The code is MIT.

Cite: Legible, version 2.0, Mikyö Clark, legible.network, 2026.
