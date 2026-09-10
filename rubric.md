# Subnet Legibility Rubric

Version: 1.0
Published: 2026-09-15
Applies to scores dated: 2026-09-21
Author: Mikyö Clark, legible.network

## What this measures

Every cell in this rubric scores one thing: what a first-time reader in a given audience can find in five minutes from public sources, weighted toward the subnet's own materials.

It does not score whether the mechanism is good, whether the token is a good buy, whether the team is competent, or whether the subnet will exist next year. A subnet whose front page says plainly "there is no product yet, and here is why" scores well with buyers, because the buyer got their answer in one click. A brilliant mechanism documented only in validator code scores low with stakers, because the staker could not find it.

Legibility is not marketing. It is whether the subnet has told the people who fund it, work for it, buy from it, and encounter it what it is, in a place they will look.

## Who is reading

Four audiences, each with one question. Four is the ceiling.

| Audience | Their question | What they need to find |
|---|---|---|
| Stakers and validators | Should I allocate here? | The commodity, the demand, the anti-gaming design, the emissions logic |
| Miners | Can I compete, and what wins? | The task spec, the scoring, the hardware, the entry cost, the churn |
| Buyers and enterprises | Can I use this today? | The product, the API, the pricing, the reliability, who to call |
| Newcomers | What is this and why does it matter? | A plain-language account, what is novel, proof it works |

Regulators, the foundation, and the press read the buyer and newcomer accounts. They are not separate audiences here.

## Sources that count, in order

1. The on-chain subnet identity: the seven fields the owner sets (`subnet_name`, `github_repo`, `subnet_contact`, `subnet_url`, `discord`, `description`, `additional`). These are the subnet's own words and the first thing a wallet or explorer shows.
2. The GitHub README and docs folder at `github_repo`, and any docs site they link.
3. The site at `subnet_url`: its front page and its about, docs, pricing, and status links.
4. A whitepaper or litepaper linked from 2 or 3.
5. The subnet's own X account and blog, when linked from 2 or 3.
6. Third-party pages: the Taostats description, community explainers, posts by others.

Third-party evidence alone caps a cell at 1. Discord is recorded as present or absent and never read; a link to the shared Opentensor server counts as absent.

## The scale, applied in every cell

| Score | Meaning |
|---|---|
| 0 | Nothing findable on the question in five minutes from any public source |
| 1 | Findable only in third-party sources, or only by asking in Discord |
| 2 | The subnet's own materials touch it, but scattered across pages, stale (contradicted by current code or chain state), or readable only in code |
| 3 | Stated in the subnet's own materials in one place, but the reader needs Bittensor or domain knowledge, or more than five minutes, to act on it |
| 4 | Stated plainly in one place within two clicks of the README or the site front page; a first-time reader gets it in under five minutes |
| 5 | As 4, plus a concrete artifact the reader can check (a number with a date, a table, a schema, a live endpoint, a diagram, a worked example), and it agrees with the on-chain identity |

When torn between two scores, take the lower one and say why.

## The sixteen cells

Each audience is scored on the same four-question spine. For every cell: the reader's question, the evidence that counts, and what a 5 and a 2 look like.

### Stakers and validators

**S1. What it is.** "What does this subnet produce that someone pays for, and in what unit?" Evidence: a commodity statement naming the output (inference tokens, GPU hours, model checkpoints, forecasts, datasets) and its unit. A 5 puts the output and unit on the front page, matching the on-chain description. A 2 is a tagline like "decentralized AI for everyone" with the actual output only inferable from code.

**S2. Who it is for.** "Who is using it today, and how would I see demand?" Evidence: usage figures, named customers, revenue or buyback statements, a dashboard. A 5 is a dated usage or revenue figure, or a live dashboard, on the subnet's own site. A 2 is "used by many" with no number, or numbers only in a months-old post.

**S3. How it resists gaming or fails.** "How do validators score, how do they stop miners cheating, and what would kill this subnet?" Evidence: an incentive mechanism document, a validation description, a known-attacks or limitations section, a statement of how emissions are earned. A 5 is a named incentive document with an anti-gaming section and stated failure modes. A 2 is a mechanism that exists only as validator code.

**S4. Identity and documentation.** "Is the chain identity filled in, do the links resolve, and is there a page written for stakers?" Evidence: the seven identity fields, links resolving to the claimed subnet, a staking, tokenomics, or validator page. A 5 is identity at 7 of 7 with every link resolving, plus a staker-facing page. A 2 is identity at 3 fields or fewer, or links pointing at a dead or renamed project.

### Miners

**M1. What it is.** "What exactly does a miner do: request in, response out?" Evidence: a task specification with input and output shape. A 5 is a spec with a schema and a worked example. A 2 is a task only inferable from a protocol file.

**M2. Who it is for.** "What kind of miner wins, on what hardware, and what does entry cost?" Evidence: hardware requirements, the registration cost or where to read it, an honest competitiveness statement. A 5 is a hardware table, the current registration cost or where to read it, and a plain statement of what it takes to be competitive. A 2 is "a GPU is recommended" and nothing else.

**M3. How it resists gaming or fails.** "How is my output scored, and what gets me deregistered?" Evidence: the scoring formula in prose, weights, immunity period, churn or deregistration policy. A 5 is scoring described in prose with example numbers and a stated churn or immunity policy. A 2 is scoring only in code, no prose.

**M4. Identity and documentation.** "Can I get a miner running from the docs, and are they current?" Evidence: a step-by-step miner guide, versioned releases or a changelog, a last-updated date consistent with recent commits. A 5 is a guide that matches the current release, updated within 90 days. A 2 is a guide that references removed flags or an older network version.

### Buyers and enterprises

**B1. What it is.** "What can I buy or call today?" Evidence: a product page, an API endpoint, a hosted app. A 5 is a product page with an endpoint or app and a working example. A plain "no product yet; outputs are X; expected date Y" scores 4. A 2 is a product implied by marketing copy with no way to reach it.

**B2. Who it is for.** "Is this for me, and what does it cost?" Evidence: a target-customer statement and pricing. A 5 is a pricing page plus a named customer type. A 2 is "contact us" with no customer type or price.

**B3. How it resists gaming or fails.** "What happens when it breaks: uptime, SLA, status page, support path?" Evidence: a status page, an SLA, uptime history, incident posts, a support channel with a response expectation. A 5 is a status page or SLA and a stated escalation path. A 2 is Discord as the only support path.

**B4. Identity and documentation.** "Where are the API docs, and who do I call?" Evidence: an API reference, `subnet_contact` set on chain and matching the site, a named business contact or form. A 5 is an API reference plus a contact that matches the chain identity. A 2 is docs with no contact anywhere.

### Newcomers

**N1. What it is.** "In one paragraph, what is this?" Evidence: a plain-language paragraph without unexplained crypto or ML jargon. A 5 is that paragraph on the front page, consistent with the on-chain description. A 2 is a technical README opening or the chain description alone.

**N2. Who it is for.** "What does this do that a centralized service does not, and who cares?" Evidence: an explicit statement of the difference decentralization makes here. A 5 is a concrete stated difference (cost, censorship, ownership, coverage) with a comparison. A 2 is a generic "decentralized" claim.

**N3. How it resists gaming or fails.** "How would I know it works?" Evidence: a live demo, dated output samples, benchmarks, a comparison. A 5 is a demo or a dated benchmark on the subnet's own site. A 2 is a claim of results with no artifact.

**N4. Identity and documentation.** "Is there a front door?" Evidence: `subnet_name` matches the site, `description` is a human sentence, `subnet_url` resolves, and the site has an about or learn page. A 5 is all four true. A 2 is a name mismatch between chain and site, or no site.

## Composite

Each audience score is the mean of its four cell scores, to one decimal. The composite is the mean of the four audience scores, equal weights, to one decimal. The weights are part of version 1.0; changing them is a version bump.

The composite is a summary, not the finding. The finding is the per-audience view: a subnet that stakers can read and buyers cannot is a different subnet from one that reads the same to everyone.

## Unknown

A cell is unknown when the scorer could not check it within the cap: a page that would not load, a site that needs a browser, time that ran out. Unknown is not zero.

Unknown cells are left out of the audience mean while three cells are scored. With two or more unknown cells the audience is unscored, and the composite is computed over the scored audiences and marked partial. Nothing is published with an unknown cell: before publication every unknown is either resolved by hand, with a dated note, or scored 0 with the note "nothing found by hand," also dated. Unknown exists only between the scoring run and publication.

## What is not scored

Mechanism quality. Token price or return. Team reputation. Anything that needs more than five minutes to find. Anything only in Discord. Anything a reader would have to be told by a person.

## Versioning

This is version 1.0. A new version changes the anchors, the weights, the sources that count, or the number of cells. Corrections to individual scores under the same rubric do not change the version; they are logged in the changelog with the date, the cell, the old and new score, and who asked.

## Proposing a change

Before scores publish on 2026-09-21, proposals to change an anchor or a source rule are welcome by GitHub issue or email, and will be answered before scoring begins. After that date, proposals go into version 1.1.
