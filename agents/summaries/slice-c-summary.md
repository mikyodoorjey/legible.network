# Slice c summary: SN15, SN4, SN3, SN93, SN110, SN56, SN83, SN62

Scored 2026-09-09 by agent c under rubric v1.0. Rows are in `data/scores-c.csv`. Eight rows, 128 cells, no unknown cells. Audience means (stakers, miners, buyers, newcomers) and the unweighted mean of the four, which the merge script will recompute as the composite:

| netuid | name | stakers | miners | buyers | newcomers | mean |
|---|---|---|---|---|---|---|
| 15 | ORO | 4.0 | 4.0 | 2.5 | 4.5 | 3.8 |
| 62 | Ridges | 3.5 | 4.5 | 3.3 | 3.8 | 3.8 |
| 56 | Gradients | 3.0 | 4.0 | 3.8 | 3.5 | 3.6 |
| 4 | Targon | 3.0 | 3.3 | 3.5 | 4.0 | 3.5 |
| 110 | Green Compute | 3.3 | 1.8 | 3.8 | 3.8 | 3.2 |
| 3 | Teutonic | 2.8 | 3.8 | 1.5 | 3.0 | 2.8 |
| 93 | Bitcast | 3.3 | 2.3 | 1.8 | 3.5 | 2.7 |
| 83 | CliqueAI | 2.3 | 2.8 | 0.5 | 2.0 | 1.9 |

## Per subnet

### SN15 ORO

ORO's front page says what it is and why in plain words (an open arena where shopping agents are scored daily and every run becomes training data), and the docs tree behind it carries an agent interface spec, a scoring page, an architecture page with anti gaming rules, a staking guide and a dated changelog. Newcomers and miners are best served; buyers find a roadmap saying the shopping product comes later, no price, and a chain contact (team@oroagents.com) that appears nowhere on the site, whose privacy page lists support@oroagents.com instead.

### SN4 Targon

Targon reads as a cloud product: rentals and confidential VMs, a public inventory API that returns hourly prices without a key, and a full REST reference at docs.targon.com. Buyers are best served, though every inventory SKU read Out of Stock today; stakers and newcomers get a tagline, an Intel co authored whitepaper and counters that only render in a browser, while the emission auction lives in the miner docs and the chain contact devs@manifold.inc is not on the site.

### SN3 Teutonic

Teutonic documents itself for miners through one file, `teutonic.ai/llms.txt`, one click from a live dashboard, with the submission contract, hardware line, where to read the registration burn, the acceptance math and a known exploits section; the README covers the miner CLI. Miners are best served, but the file's eval parameters (delta 0.5 nats, n 2000, FineWeb-Edu) already disagree with the live dataset manifest (delta 0.025, n 20000, five datasets), the discord field on chain is a handle rather than a link, the contact address appears nowhere, and nothing speaks to stakers, buyers or newcomers.

### SN93 Bitcast

Bitcast shows its numbers and hides its words: a dated dashboard (updated 2026-09-09) with creators, views, rewards, revenue, buybacks and a transaction audit whose rows link to taostats, etherscan and solscan. Stakers and newcomers are best served; the mechanism lives in validator code, a CLAUDE.md machine file and an August 2025 substack post that nothing on the site links, the brand and creator portals (outfold.ai, stitch3.ai) render as empty JS shells, and the chain identity has no contact and no discord.

### SN110 Green Compute

Green Compute is a sales site: per GPU hour prices, an OpenAI compatible endpoint with a curl example that answers, a sales address with a 24 hour reply promise, and a plain about page explaining what subnet 110 is and why it is on Bittensor. Buyers and newcomers are best served; miners get an application form and a paragraph, stakers get a commitment to buybacks with a treasury wallet, and there is no repository, no incentive document and only three identity fields on chain (github, contact, discord and additional all unset).

### SN56 Gradients

Gradients is legible to miners through one long guide in the repo (`docs/miner.md`, called the single source of truth, with the repository contract, fees and the emission split in prose) and to buyers through a front page curl example, a Swagger reference and hourly prices. Miners and buyers are best served; the pricing page loads only with JS, the README fee table (0.35, 0.20, 0.30 TAO) is stale against the guide and the fees API (0.7, 0.4, 0.6 TAO), the news feed stops in 2025, and the chain identity's discord and additional fields hold the literal text None.

### SN83 CliqueAI

CliqueAI has one good document, `docs/mechanism.md`, with the optimality and diversity formulas and the EMA, and almost nothing else: the site is a JS only shell whose rendered copy says miner selection is stake weighted while the mechanism doc says equal probability, the miner README is one command, the last release is from April, the discord is a channel in the shared Opentensor server and the contact domain toptensor.ai does not resolve. Miners with graph theory are the only audience served; buyers score 0.5 because nothing can be bought or called.

### SN62 Ridges

Ridges is legible through docs.ridges.ai: a one function agent contract with example code, dollar costs of entry, a named incentive page with worked numbers and a time multiplier table, a scoring page, and a priced product (Ridgeline, $9.99 a month for 10 credits or credits for locked alpha) for developers. Miners are best served; the site at www.ridges.ai returns a Vercel security checkpoint (429) to every fetcher and animates its headline in a browser, the chain contact hello@ridges.ai appears on no docs page, and Ridgeline demand is stated nowhere.

## Where the gap is widest

Across the eight, the widest gap is on the buyer side and on the identity fields. Only three subnets (Targon, Green Compute, Gradients) put a price and a way to call something within two clicks of the front page, and only Ridges adds a plain customer statement; ORO, Teutonic, Bitcast and CliqueAI have no buyer product at all and say so only by omission. Five of the eight chain contacts do not appear on the subnet's own site (ORO, Targon, Teutonic, CliqueAI, Ridges), two subnets set no contact at all (Bitcast, Green Compute), two discord fields hold non links (Teutonic's handle, Gradients' None) and one points at the shared Opentensor server (CliqueAI). The second pattern is documentation that exists but sits where a five minute reader will not go: Teutonic's whole miner guide is a file named llms.txt, Gradients' is a markdown file two clicks into the repo, Bitcast's eligibility rule is in CLAUDE.md, CliqueAI's hardware table is a YAML file, and in three of those cases (Teutonic, Gradients, CliqueAI) the numbers or copy on the front door already disagree with the file. Stakers are the least addressed audience by name: ORO has a staking guide and Ridges a credits page for locked alpha, and nobody else has a page for them.

## Gaps

Unknown cells: none. Every cell in all eight rows is scored.

JS rendered or partly rendered pages (readable only in a browser, or not at all):

- https://oroagents.com/leaderboard reads 0 agents, 0 validators and network idle to a fetcher while the public API shows race 149 running with 397 qualifiers. The front page counters and docs are server rendered.
- https://targon.com counters (GPUs, uptime, latency, utilization) read 0 to a fetcher; https://targon.com/inventory renders prices only in a browser (B200 $42.80 per hour, every SKU Out of Stock); https://stats.targon.com and /targets render $000.00 and empty tables; https://targon.com/llms.txt redirects to an org access denied page and /docs, /pricing, /about, /models, /blog redirect to sign in.
- https://www.teutonic.ai/ is a dashboard whose panels read loading to a fetcher; the data is plain at https://teutonic.ai/dashboard.json and https://teutonic.ai/datasets/manifest.json, and the page renders fully in a browser.
- https://stats.bitcast.network/ redirects to https://bitcast.network/ and every path on that host (/docs, /brands, /about, /llms.txt) returns the same dashboard page. The dashboard numbers are server rendered. https://outfold.ai/, https://www.stitch3.ai/ and https://creator.outfold.ai/briefs (the redirect target of dashboard.bitcast.network/briefs) render as JS shells.
- https://www.green-compute.com/capacity counters read blank to a fetcher; /models, /rental and /apply redirect to or sit behind login.
- https://www.gradients.io/pricing reads Loading prices to a fetcher and renders the five hourly rates in a browser; /docs, /llms.txt and /team redirect to /auth.
- https://cliqueai.toptensor.ai/ is a 1.9 KB shell to a fetcher; in a browser the copy renders but the MINER SCOREBOARD section still reads Loading after five seconds. All paths (/docs, /llms.txt, /api, /about) return the same shell.
- https://www.ridges.ai/ returns 429 Vercel Security Checkpoint to curl and to WebFetch; in a browser the front page headline is a scrambling text animation that never settled to readable text in two ten second waits, and /agents renders a competitions list. docs.ridges.ai is server rendered and has an llms.txt index.
- Every https://taostats.io/subnets/N page (15, 4, 3, 93, 110, 56, 83, 62) renders name, price and navigation only; the embedded JSON carries the chain identities, which agree with the slice file. Identity was scored from the slice file as the brief instructs.

Chain identity fields that pointed somewhere wrong or malformed:

- SN15 ORO: subnet_contact team@oroagents.com is not on the site; the privacy page lists support@oroagents.com. description AI commerce agents is a tag, not a sentence.
- SN4 Targon: subnet_contact devs@manifold.inc is not on the site or docs (the site has a contact form only). discord not set although the site links discord.gg/manifold.
- SN3 Teutonic: discord holds the text @unarbos, not a URL (marked dead). subnet_contact arbos@bittensor.com appears nowhere on the site, in llms.txt or in the repo. description Coordinated Learning is a two word tag that the site never uses.
- SN93 Bitcast: subnet_url https://stats.bitcast.network/ redirects to https://bitcast.network/ (marked resolves). subnet_contact and discord not set; a Discord invite exists only in the substack post. Only 4 of 7 fields set.
- SN110 Green Compute: github_repo, subnet_contact, discord and additional not set (3 of 7). The site lists sales@green-compute.com. A web search attributed the code to commune-ai/compute, which is a third party claim not on the site and was not used.
- SN56 Gradients: discord and additional hold the literal text None (discord marked dead; the platform page links a Discord). description Best AutoML plaftorm in the world has a typo and is a slogan. The repo README's clone URL and the miner guide still point at the rayonlabs org, which redirects.
- SN83 CliqueAI: discord is a channel inside the shared Opentensor server (799672011265015819), recorded as absent. subnet_contact CliqueAI@toptensor.ai is on a domain that does not resolve (toptensor.ai returned no response).
- SN62 Ridges: subnet_url returns 429 to fetchers (resolves in a browser). subnet_contact hello@ridges.ai appears on no docs page fetched. The docs site links a different Discord invite (discord.gg/WTsCZpdHQ) from the one on chain (discord.gg/WeDvTnYDad).

Failed or blocked fetches:

- https://www.ridges.ai/ (and /llms.txt, /docs, /about): 429 Vercel Security Checkpoint on curl twice and on WebFetch once; rendered in the browser tool instead.
- https://status.targon.com and https://toptensor.ai: no response (DNS or connection failure).
- https://docs.bitcast.network and https://app.bitcast.network: no response.
- https://docs.gradients.io: no response; api.gradients.io/docs and /openapi.json answered.
- https://api.github.com rate limited unauthenticated calls after the first two subnets; repo metadata for the remaining five was read with the authenticated gh CLI.
- No X pages were fetched. Discord was recorded as present or absent and never read.

Searches and time:

- SN15 ORO: 1 search, about 14 minutes.
- SN4 Targon: 1 search, about 12 minutes.
- SN3 Teutonic: 1 search, about 12 minutes.
- SN93 Bitcast: 2 searches, about 11 minutes.
- SN110 Green Compute: 2 searches, about 11 minutes.
- SN56 Gradients: 1 search, about 11 minutes.
- SN83 CliqueAI: 1 search, about 9 minutes.
- SN62 Ridges: 1 search, about 12 minutes.
- Ten searches in total; neither the per subnet cap nor the session cap was reached. Pages were fetched in parallel across subnets, so the minutes are attention per subnet rather than wall clock.

## Ambiguities met while scoring

The rubric's 4 anchor ("within two clicks of the README, the docs root, or the site front page") was decisive for Ridges, whose site front page is unreadable to fetchers and unreadable in a browser too, so every cell was scored from docs.ridges.ai as the front door; a reader who lands on www.ridges.ai first gets an animation. Machine facing files decided four subnets: Teutonic's llms.txt was scored on content with the register holding cells at 3 or 4, as the pilot notes say, and the same treatment was given to Bitcast's CLAUDE.md, CliqueAI's min_compute.yml and Gradients' SKILL.md (the last was used only as a pointer to the pricing and API endpoints, which were then fetched). The stale clause was applied where a subnet's own front door contradicts its own document: Teutonic's llms.txt versus the live manifest (S3 and M3 held at 3), Gradients' README fee table versus the guide and API (M2 held at 3), CliqueAI's site copy versus mechanism.md (noted in S3, not penalised further because the doc is the more current source). For S2 the calibration note on dashboards that disagree with other pages was applied to Green Compute (dated revenue on the site, one active miner on chain, scored 4 not 5) and to Targon (every SKU out of stock, counters zero to a fetcher, scored 2). Bitcast's S2 and N3 were given 5 because the dashboard is dated, live and links every transaction to a block explorer, which is the strongest artifact in the slice. Two contacts were treated as text fields that could not be confirmed rather than as dead links (ORO, whose site names a different address, and Ridges, whose site could not be read), following the calibration file's use of the text token.
