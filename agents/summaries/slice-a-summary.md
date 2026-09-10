# Slice a summary: SN107, SN64, SN80, SN9, SN28, SN58, SN124, SN90

Scored 2026-09-09 by agent a under rubric v1.0. Rows are in `data/scores-a.csv`. Composites as the merge script will compute them: SayGM 4.1, Chutes 4.1, KubeTEE 3.5, Minos 3.4, OpenRoboto 3.3, Swarm 3.3, greevils 2.9, iota 2.5. No unknown cells. Seven web searches used in total, one per subnet except Chutes, which needed none.

## SN107 Minos

Composite 3.4 (stakers 3.3, miners 4.0, buyers 2.3, newcomers 4.0). Minos is legible because the about page says in one plain paragraph what variant calling is and what the competition does, and the README, docs/scoring.md, the tuning guide and min_compute.yml give miners the task, the hardware and the scoring formula with numbers. Miners are best served; buyers find a roadmap that marks the production service as a phase 5 vision, no price, and a chain contact that appears nowhere on the site, while the about page still says the winner takes 100 percent although the live network config pays a winner share of 0.8 plus dust.

## SN64 Chutes

Composite 4.1 (stakers 4.3, miners 3.3, buyers 4.8, newcomers 3.8). Chutes is legible because the chain description is the site headline and the endpoint, per token prices, API reference, status page and a support address matching the chain contact are each one click from the front page. Buyers are best served; miners are least, because the docs site overview still describes GraVal and Wireguard while the chutes-miner README says the network is TEE-only and GraVal is unsupported, and the only comparison with centralized providers lives in the machine facing llms.txt.

## SN80 OpenRoboto

Composite 3.3 (stakers 3.3, miners 4.0, buyers 2.0, newcomers 3.8). OpenRoboto is legible to miners because a dated guide, a stated fee, a checkpoint spec and challenge rules with numbers sit one click from the README, and the site's docs page repeats the miner path in plain prose. Buyers get open models and data but no product, price or contact; the site is an empty shell without JavaScript, the chain github_repo points at a toolkit its own README calls deprecated, and the benchmark page's telemetry panel reads zero above a leaderboard with three ranked rows.

## SN9 iota

Composite 2.5 (stakers 3.0, miners 2.5, buyers 1.8, newcomers 2.8). IOTA has one good page, Scoring, Rewards and Kicking, which explains scoring, the weight formula and the kick policy in prose, and that page is what keeps stakers at 3.0. Everything else is stale or missing: the README links miner and validator docs that return Page Not Found, the primer PDF is gone from both macrocosmos.ai hosts, the dashboard counters all read zero under a banner saying Project Orion is live, the chain description appears nowhere on the site, and the chain Discord invite resolves to no server.

## SN28 SayGM

Composite 4.1 (stakers 4.0, miners 3.5, buyers 4.5, newcomers 4.5). SayGM is legible because the chain description and additional field are the front page headline, and the same page carries the base URL, per model prices, a live attestation block and a link to a miners page with epoch totals dated to the hour. Buyers and newcomers are best served; the gap is that nothing in prose says how miners are scored or how emissions are set, so stakers and miners read the economics off a table with share, reliability and discount columns.

## SN58 greevils

Composite 2.9 (stakers 2.8, miners 3.5, buyers 2.3, newcomers 3.0). Greevils has a plain front page and an unusually complete incentive document, but the document lives in the validator repo three clicks from the front door, and the live leaderboard says no competitors yet while the front page shows a mock leaderboard with illustrative names. Miners are best served; the chain identity is 4 of 7 with no description, the Discord link is an Opentensor channel, and buyers get a trading terminal without a stated product or price.

## SN124 Swarm

Composite 3.3 (stakers 3.0, miners 4.3, buyers 2.0, newcomers 3.8). Swarm is written for miners: each family document carries observation and action tables with shapes and ranges, the miner guide gives the scoring formula with numbers, and the King of the Hill document explains emissions and why winner take all was dropped. The chain identity is half empty (no description, no discord, a url without a scheme), the site is a JavaScript-only services pitch with no contact, price or API, and the README and the site describe two different things, an open arena and a drone lab.

## SN90 KubeTEE

Composite 3.5 (stakers 4.3, miners 3.3, buyers 2.8, newcomers 3.5). KubeTEE is legible to stakers because the README separates what is live from what is designed in one table, the revenue dashboard lists dated swaps with extrinsic ids, and the validator dashboard shows the price card and per miner payout with a timestamp. Miners cannot onboard without the operator and the README says so, buyers find a Swagger page and a first name rather than a price list or contact, and the README is 86 KB, which puts most answers past the five minute mark.

## Where the gap is widest

Across the eight, the widest gap is on the buyer side and on the identity fields. Five of eight subnets (Minos, OpenRoboto, iota, greevils, Swarm) have no product a buyer can reach, and none of those five says so plainly with an expected date; the roadmaps that exist are undated phase lists. Five of eight chain contacts (Minos, OpenRoboto, greevils, Swarm, KubeTEE) appear nowhere on the subnet's own site, and only iota, Chutes and SayGM show theirs, so B4 fell to 2 or below for most of the slice on that count alone. Three subnets (greevils, Swarm, and by omission KubeTEE's tag string) have no human sentence in the chain description, and two Discord fields point at channels on the shared Opentensor server. The second widest gap is the incentive mechanism for stakers: the two inference gateways that serve buyers best (Chutes and SayGM) either bury scoring in miner docs or do not describe it in prose at all, while the competition subnets (Minos, OpenRoboto, Swarm, greevils) each have a real incentive document that a staker only reaches through the README or a second repo.

## Gaps list

Unknown cells: none. Every cell in all eight rows is scored.

JS-rendered or partly rendered pages (all were rendered in a browser during the session and the rendered text used as evidence):

- https://www.openroboto.ai/ and its hash routes /#/docs and /#/benchmark are a React shell to a fetcher; only the meta description is readable without JavaScript.
- https://swarm124.com/ and https://swarm124.com/benchmark are a shell with a noscript notice; /llms.txt and /docs return the same shell rather than 404.
- https://theminos.ai/dashboard and /dashboard/miners fetch as Loading placeholders; the browser view shows live counters and rounds dated 09/09.
- https://iota.macrocosmos.ai/dashboard fetches as a title only; the browser view shows every counter at zero. /dashboard/mainnet, linked from the README, returns 404 in the browser.
- https://app.greevils.ai/leaderboard fetches as a shell; the browser view shows No competitors yet and 158 agent submissions.
- https://taostats.io/subnets/<n> renders name and price only. The identity fields are present in the page's embedded JSON payload, which is how the contact addresses matched, but they are not rendered.
- https://chutes.ai/models notes that filters need JavaScript; the catalog text itself is server rendered.

Chain identity fields that pointed somewhere wrong or were malformed:

- SN9 iota: discord https://discord.gg/adsQPnFRY resolves to a generic Discord page with no server name (marked dead); the docs link a different invite. The description Bringing liquid training to the world appears nowhere on the site or docs. The README links miner and validator docs under /subnets/subnet-9-pre-training/ that return Page Not Found.
- SN80 OpenRoboto: github_repo https://github.com/openroboto-ai/openroboto-subnet resolves, but its README says its own miner flow is deprecated and points to openroboto-ai/openroboto-cli, where the current guides live. subnet_contact riccardo@openroboto.ai is not on the site or in either repo.
- SN124 Swarm: subnet_url is www.swarm124.com with no scheme (resolves, redirects to https://swarm124.com/). description, discord and additional are empty. subnet_contact admin@swarm124.com is not on the site or in the repo docs.
- SN58 greevils: description, discord and additional are empty. subnet_contact atlas@greevils.ai matches only the commit author email. The site's Discord link is a channel on the shared Opentensor server.
- SN107 Minos: discord is a channel on the shared Opentensor server (recorded absent). subnet_contact contact@theminos.ai is not on the site, docs or README.
- SN90 KubeTEE: additional joins an X URL and a slogan with a dash; the value is recorded with a comma in identity_check. subnet_contact pierre@kubetee.ai is not on the site. The site footer Discord link resolves to the Bittensor server while the chain invite resolves to a KubeTEE.AI server.
- SN28 SayGM: discord not set; the docs link discord.gg/ktjRY53Nk. The contact hi@saygm.com is only on the site as a Cloudflare obfuscated mailto, decoded by hand.
- SN64 Chutes: all seven fields agree with the site.

Failed fetches (each tried once unless noted, none retried after a second failure):

- https://theminos.ai/llms.txt 404. https://www.openroboto.ai/llms.txt and /docs 404 (docs live at /#/docs). https://iota.macrocosmos.ai/llms.txt 404. https://saygm.com/docs, /pricing and /product 404 (docs live at docs.saygm.com, pricing is a front page section). https://www.greevils.ai/llms.txt and /docs 404. https://kubetee.ai/llms.txt and /docs 404.
- https://www.macrocosmos.ai/research/iota_primer.pdf and https://macrocosmos.ai/research/iota_primer.pdf 404 (linked from the README and docs as the whitepaper); https://www.macrocosmos.ai/research 404. The arXiv abstract page was used instead.
- https://docs.macrocosmos.ai/subnets/subnet-9-pre-training/subnet-9-iota-mining-setup-guide.md and .../subnet-9-validating.md return Page Not Found (linked from the README).
- https://raw.githubusercontent.com/swarm-subnet/swarm/main/docs/miner_guide.md 404 (guessed path; the guide is at miner/docs/miner.md).
- https://docs.saygm.com/mining/mining-overview/, /platform/billing-and-pricing/ and /api/errors-and-retries/ 404 (guessed paths; the live paths are /mining/overview/ and /platform/billing/). https://saygm.com/blog/introducing-saygm.md 404 (guessed slug).
- api.github.com returned 403 rate limited for the Swarm, KubeTEE and Minos contents and commits calls; push dates and release tags were read with the authenticated gh CLI instead and only the api.github.com URLs that returned 200 are listed in sources.
- No fetch had to be retried; no fetch was marked unknown.

Search count: 7 of a 200 session cap (Minos 1, Chutes 0, OpenRoboto 1, iota 1, SayGM 1, greevils 1, Swarm 1, KubeTEE 1). No per subnet cap was reached. Minutes per subnet are attention estimates; fetches ran in parallel across subnets so the eight numbers add to more than the wall clock.

## Ambiguities met while scoring

S2 when a live dashboard shows supply side activity but no demand (Minos, OpenRoboto, Swarm): I gave 3, reading the rubric's 5 anchor as needing a usage or revenue figure, not miner activity. S2 when the dashboard reads zero against a live claim (iota) got 2 under the contradicted clause, as in the Apex calibration. Chutes N4 and SayGM N4 turn on whether a verbless headline counts as a human sentence; I took 4 both times. Files written for machines (chutes.ai/llms.txt) were scored as own material with the register deciding between 3 and 4, per the pilot notes. KubeTEE M1 is a case the ladder does not name: the task is stated plainly, but onboarding is closed by design and the README says so, and I scored the statement rather than the closure. The docs root was counted as a front door for the two click test, per the rubric wording, which is why Chutes S3 is 4 here and 3 in the calibration.
