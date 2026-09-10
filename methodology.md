# Methodology

Version: 1.0
Scores dated: 2026-09-21
Corrections window: 48 hours from publication

## What the index is

The Subnet Legibility Index scores the 32 Bittensor subnets with the largest share of TAO emissions on one question: what can a first-time reader in a given audience find out about this subnet in five minutes from public sources? Four audiences, four questions each, sixteen cells per subnet, scored 0 to 5. The rules are in the [rubric](/rubric/). This page is how the rules were applied.

## Which subnets

The set is the top 32 by share of TAO emission on the snapshot date, read from Taostats. Membership was frozen at the first snapshot so that the scores, the essay, and every conversation refer to one set. Later snapshots refresh emission share, counts, and identities but do not change membership; a subnet that leaves the top 32 after the freeze stays in the index with a note. Since June 2026 a subnet's share of emission follows the moving average of its token price, so the ranking is a ranking of what the market currently pays for, not of quality.

## Sources, in the order a scorer looks

1. The on-chain subnet identity: seven fields the owner sets. Read directly from the chain through the Bittensor SDK on the snapshot date.
2. The GitHub README and docs at the repository the identity names, and the docs site they link.
3. The site the identity names: front page, about, docs, pricing, status.
4. A whitepaper or litepaper linked from the repository or the site.
5. The subnet's own X account or blog, when linked from the repository or the site.
6. The Taostats subnet page, as a cross-check on the description only.
7. At most three web searches per subnet.

Discord is recorded as present or absent and never read. A link to the shared Opentensor server counts as absent.

## Scoring

Scores were drafted by four research agents working in parallel, each on eight subnets interleaved by rank so that no agent had only large or only small subnets. Every agent worked from the same brief, the same rubric, and the same three hand-scored calibration subnets. Each agent had a cap of 25 minutes and 20 web searches per subnet; when the cap ran out, the remaining cells were marked unknown rather than guessed.

Every cell was then reviewed by a person before publication. Cells were queued for close review when they were unknown, scored 0 or 5, inferred with a score of 3 or more, in the top or bottom five subnets by composite, or backed by a link that did not resolve. The reviewer could keep, change, or send a cell back for a second look. Every change is recorded in the subnet's provenance line with the date. Nothing was published with an unknown cell.

## Evidence

Each cell carries one piece of evidence: a score, a status, a URL, and a quote or observation. The status is the scorer's provenance:

| Status | Meaning |
|---|---|
| verified | The scorer fetched the URL and the quote or observation is on that page |
| inferred | Concluded from code, from absence, or from a third-party page |
| unknown | The check could not be completed before publication; resolved by hand or scored 0 with a dated note |

Every URL was then checked by a script before publication, and each cell also carries the result of that check: live, redirected, unreachable, or manual for pages that cannot be checked by machine (X, Discord). A verified cell whose URL was unreachable at publication is shown as inferred.

Quotes are the subnet's own words, at most 25 words, taken from the page at the URL. The scorer never evaluates the mechanism; the evidence says what is on the page and where.

## Identity

The seven on-chain identity fields are `subnet_name`, `github_repo`, `subnet_contact`, `subnet_url`, `discord`, `description`, and `additional`. Completeness is the count of fields that are set. Each set field was also checked for whether it resolves to the claimed subnet. The identity is the subnet's own words and the first thing a wallet or explorer shows, which is why it anchors the fourth question in every audience.

## Provenance

Every subnet carries a provenance line that every step appends to: the agent and date that scored it, the merge, the review decisions, the link check, and any corrections. It is shown on the subnet's page so that a reader can see how a score came to be.

## Composite

Each audience score is the mean of its four cells. The composite is the mean of the four audience scores with equal weights. The composite is a summary; the per-audience view is the finding. Ranks with equal scores share a rank.

## Corrections

Corrections are welcome and expected. Two routes:

- A [GitHub issue](https://github.com/mikyodoorjey/legible.network/issues/new?template=correction.yml) using the correction form.
- Email to the address on the [about](/about/) page with the subnet number, the cell, what is wrong, and the public URL a first-time reader would find it on.

During the 48-hour window after publication, corrections of fact (a dead link, a wrong repository, a page the scorer missed) are applied as they arrive. Score disputes are collected and applied together at the close of the window with a public note, so that no subnet gets a quiet edit. After the window, corrections still apply and are dated; a subnet that adds documentation is rescored in the next version.

What qualifies: a public page that a first-time reader would find within the sources above, which the scorer missed or misread. What does not: a page created after the snapshot date (that is a rescore, not a correction), a page only reachable through Discord, or an argument that the mechanism deserves a higher score than its documentation earns.

## Changelog

<!-- changelog:start -->
No corrections yet.
<!-- changelog:end -->

## Snapshots

The chain snapshot, the scores, and the link check each carry a date, shown in the top strip of every page. Old snapshots are kept in the repository. The index will be re-run at intervals; each run is a new dated version and the changelog records rescores.

## Known limits

Web search during scoring was capped, so some subnets were scored with fewer searches than others; the number of searches used is recorded per subnet. Some documentation sites render only in a browser and fetch as empty pages; those cells were checked by hand or marked unknown before review. X pages often fail to fetch. Headcount, funding, and team are not scored and not recorded. The index measures what can be found, not what is true.
