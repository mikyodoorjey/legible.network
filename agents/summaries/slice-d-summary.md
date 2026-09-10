# Slice d summary: SN120, SN44, SN8, SN68, SN75, SN118, SN5, SN19

Scored 2026-09-09 by agent d under rubric v1.0. Rows are in `data/scores-d.csv`. Eight rows, no unknown cells, one web search per subnet (eight in total), between 11 and 17 minutes per subnet. Composites below are computed locally from the four audience means; the merge script recomputes them.

## SN120 Affine

Composite 2.4 (stakers 2.3, miners 3.8, buyers 1.3, newcomers 2.0). Affine is legible to miners through exactly one file, `www.affine.io/llms.txt`, one click from a live dashboard: it carries the submit checklist, the hardware line, where to read the registration cost, the min(R, G) scoring contract and dated fork notices, and its machine-facing register is what keeps those cells at 3 and 4 rather than 5. Everyone else meets a repo with no README, a two word chain description (Reason Mining) that appears nowhere on the site, no pricing, no support path and no plain paragraph; miners are the best served audience.

## SN44 Score

Composite 2.5 (stakers 2.3, miners 3.0, buyers 1.5, newcomers 3.0). Score has real documentation (a current miner guide, a scoring note with a worked table, a 173 KB draft whitepaper) but all of it sits in folders the README never links, the README's own link to MINER.md returns 404, and the site's Documentation link goes to the older score-vision repo rather than the chain github_repo. Newcomers are best served, by a plain front page paragraph under the headline that matches the chain description; buyers get a JS-only console shell and a contact form.

## SN8 Vanta

Composite 3.8 (stakers 3.5, miners 4.0, buyers 3.5, newcomers 4.0). Vanta reads much the same to every audience: the README carries the rules and elimination policy in prose, docs/miner.md carries scoring, hardware, collateral and registration on one page, the front page carries a comparison table against traditional prop firms, and Vanta Trading has a pricing page with six tiers. The gaps are demand and support: every dashboard (network, tokenomics, Vanta Trading metrics) is a JS shell to a fetcher, the discord identity field is a username rather than a link, and support is an email address in llms.txt with no status page.

## SN68 NOVA

Composite 3.0 (stakers 2.8, miners 3.3, buyers 2.0, newcomers 3.8). NOVA's company site answers the newcomer in one click (a plain paragraph on the nova page, dated research articles, named partners, counts of molecules and nanobodies found), while the miner task spec, format examples and scoring prose live in a docs folder the README never mentions. Buyers get a partnerships pitch and an email with no price, and the chain identity is 4 of 7 with the site's Discord link pointing at the shared Bittensor server; newcomers are the best served audience.

## SN75 Hippius

Composite 4.0 (stakers 3.8, miners 3.5, buyers 4.5, newcomers 4.3). Hippius is legible to buyers first: an S3 endpoint with AWS CLI, boto3 and rclone examples, per TB prices, a Swagger API and a dated status page are each one click from the front page, and the docs site has a plain What is Hippius page. Stakers and miners get the weight formula only in repo root files (readme_weights.md, incentives.md) that the README never links, the repo's own miner setup still describes a testnet bootnode, and the chain contact hello@hippius.com appears on none of the pages fetched.

## SN118 Ditto

Composite 3.7 (stakers 3.8, miners 4.0, buyers 3.5, newcomers 3.3). Ditto's site is a product site with a numbers page dated Sep 6, 2026 (users, monthly actives, ARR), a dated benchmark, an MCP endpoint with a config example and four mining docs pages that cover the task, the fee, the scoring rule and the king-of-the-hill gate, so miners and buyers are well served. The chain identity works against it: the description Open-Source Claude Cowork and the contact peyton@omniaura.ai appear nowhere on the site, github_repo points at an organisation listing of more than twenty repos, the docs pages still say mining goes live in July 2026, and llms.txt lists subscription tiers the pricing page has dropped.

## SN5 Hone

Composite 1.5 (stakers 1.8, miners 2.5, buyers 0.3, newcomers 1.5). Hone is a validator repository and a JS dashboard: docs/DESIGN.md writes down the trust model and the reward rule (a fully correct submission scores 0.95 to 1.0, anything else zero), but there is no miner guide beyond a demo that calls a hosted GLM model, no product, no contact, no Discord and a two word chain description (Hone training) while the README calls the project RLVR subnet. Miners are the least badly served audience; buyers find nothing at all.

## SN19 blockmachine

Composite 4.3 (stakers 4.3, miners 4.0, buyers 4.5, newcomers 4.3). blockmachine is legible to buyers and stakers alike: endpoints for eleven chains, a plan table, a cost calculator against named competitors, a versioned whitepaper, a dated on-chain buyback ledger and a 64 KB llms.txt that doubles as a full API reference all sit one click from the front page, and the chain contact matches. What holds it back is that the live performance and miner dashboards need a browser, there is no status page or SLA, the miner README registers on a testnet and gives no mainnet cost, and the chain description wording is not used anywhere on the site.

## Where the gap is widest

Across the eight, the widest gap is between what the subnet has written and what a reader can reach from a front door. Four subnets (Score, NOVA, Hippius, Affine) have a real scoring or incentive document, and in every one of them it sits in a folder or file the README never links: Score's notes/documentation, NOVA's docs/, Hippius's repo root, Affine's llms.txt with no README to point at it. The second gap is demand: six of the eight offer a dashboard, and to a fetcher all six read empty or loading, so the only dated usage or revenue figures in the slice are on Ditto's numbers page and blockmachine's buyback ledger. The third is the chain identity itself: three discord fields hold text rather than links or are unset, three contact addresses appear nowhere on the subnet's own pages, two descriptions (Reason Mining, Hone training) are tags rather than sentences, and Ditto's description and github_repo describe something other than what the site shows. Buyers are the audience served worst, with four of eight subnets scoring 2.0 or below; newcomers and miners fare best because a tagline and a setup guide are what most teams write first.

## Gaps

Unknown cells: none. Every cell in all eight rows is scored.

JS-rendered or partly rendered pages (the static shell was readable, the data was not):

- https://taostats.io/subnets/120, /44, /8, /68, /75, /118, /5 and /19 all render navigation and footer only, no description or identity block. Identity was taken from the slice file as the brief instructs.
- https://www.affine.io/ renders its chart, reign, queue, history and audit panels as loading. The data behind them was read from https://affine.io/api/v1/snapshot, which is plain JSON.
- https://www.wearescore.com/ renders the headline and one paragraph; the customer logos and demo videos are media files with no text. https://console.scorestudio.ai/ is an empty Score Dashboard shell.
- https://www.vantanetwork.io/tokenomics and /dashboard are shells (Loading dashboard data), https://tokenomics.taoshi.io renders Registrations 0, and the live metrics on https://www.vantatrading.io/ are placeholders.
- https://www.metanova-labs.ai/dashboard renders only the navigation; the front page is a marquee of taglines and the value counters read as animation targets.
- https://hipstats.com renders its Total Storage and node counters empty; the usage calculator on https://hippius.com/ shows a static $6 per month example.
- https://honedashboard.com is a dashboard shell reading Loading and Waiting for aggregate data.
- https://blockmachine.io/performance, /miners and the metric tiles on /bittensor render empty tables to a fetcher.

Chain identity fields that pointed somewhere wrong, were malformed, or disagreed with the site:

- SN120: discord is the text consttt; subnet_url www.affine.io has no scheme (it resolves); subnet_contact hello@affine.io appears nowhere on the site, in llms.txt or in the repo; github_repo resolves to a repository with no README; description Reason Mining is not used on the site.
- SN44: the site's Documentation link goes to https://github.com/score-technologies/score-vision, not the chain github_repo turbovision; the README's MINER.md link is dead (the file is at scorevision/miner/open_source/MINER.md); subnet_contact hello@wearescore.com is not on the site.
- SN8: discord is the text tl_arrash (the README links discord.gg/vantatrading, which resolves); subnet_contact is not set (llms.txt gives support@taoshi.io); description says liquidity and execution engine where the site says funding engine.
- SN68: subnet_contact, discord and additional are not set; the site's Discord link is the shared Bittensor server (recorded absent); the site footer gives contact@metanova-labs.com.
- SN75: subnet_contact hello@hippius.com was not found on any page fetched; discord is not set although the site links discord.hippius.com; https://hippius.com/llms.txt redirects to https://docs.hippius.com/llms.txt.
- SN118: github_repo is an organisation listing (https://github.com/orgs/ditto-assistant/repositories) rather than a repo; description Open-Source Claude Cowork and subnet_contact peyton@omniaura.ai appear nowhere on the site (which gives support@heyditto.ai); llms.txt lists Flex, Plus and Pro subscription plans that the pricing page no longer shows; docs pages dated July 13, 2026 still say mining goes live in July 2026.
- SN5: description Hone training is a two word tag; the README and dashboard call the project RLVR subnet; subnet_contact and discord are not set.
- SN19: subnet_url blockmachine.io has no scheme (http and https both load); discord is not set and the channel linked from llms.txt is on the shared Bittensor server (recorded absent); the chain description wording is not used on the site.

Failed fetches (each tried once unless noted, then recorded and moved past):

- https://raw.githubusercontent.com/AffineFoundation/affine/main/README.md 404 (no README on main; the repo root holds AGENTS.md, START_HERE.txt, LAYOUT.txt).
- https://www.wearescore.com/llms.txt 404 and https://www.wearescore.com/docs 404. https://raw.githubusercontent.com/score-technologies/turbovision/main/MINER.md 404 (linked from the README).
- https://www.vantanetwork.io/docs 404. https://hyperscaled.trade 429 behind a Vercel security checkpoint. https://docs.taoshi.io/request-network/ 404.
- https://www.metanova-labs.ai/docs 404 and https://www.metanova-labs.ai/whitepapers 404 (the latter appeared in search results).
- https://hippius.com/docs 404 (docs live at docs.hippius.com); https://docs.hippius.com/earn and /earn/miner 404 (the miner page is /earn/storage-miner, found from the docs navigation).
- https://honedashboard.com/llms.txt and /docs return a JSON Not found.
- The unauthenticated GitHub REST API rate-limited once while listing the turbovision tree; repo trees and push dates were read through the gh CLI instead. No GitHub raw fetch failed on a second try.
- No X pages were fetched; handles in artifacts come from links on the subnets' own pages.

Searches: one per subnet, eight in total, on the first of the three queries the brief lists. The per-subnet cap of 20 and the session cap were never approached.

## Ambiguities met while scoring

Notes were trimmed to under 200 characters as the brief requires, even though the calibration and pilot rows run longer; a few observations lost a clause in the trim and the longer reasoning is in this summary. The brief's S1 anchor for 5 wants the unit on the front page and the chain description to match: Hippius got 5 because the pricing page is one click away and the tagline restates the chain description, blockmachine got 4 because the chain description wording is absent from the site. For dashboards that exist but render empty (six of eight) I scored S2 and N3 at 3, following the calibration note that an artifact which cannot be read is not a 5. Affine's miner cells were scored at 3 and 4 from llms.txt as the pilot comparison note suggests, letting the machine register decide. For Ditto I treated the org listing in github_repo as resolving but scored S4 and B4 down for it, since a reader has to find the subnet repo among twenty. Discord invites were resolved with a HEAD request where the identity or README gave a link, never read.
