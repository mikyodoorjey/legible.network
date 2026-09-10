# Slice b summary: SN51, SN97, SN114, SN53, SN91, SN38, SN61, SN34

Scored 2026-09-09 by agent b under rubric v1.0. Rows are in `data/scores-b.csv`. Composites below are computed from the cell scores with the same rule the merge script uses. No cell is unknown.

## SN51 lium.io

Composite 3.8 (stakers 3.3, miners 4.0, buyers 4.3, newcomers 3.5). Lium is legible because the front page is the product: a live list of 83 rentable pods with per GPU-hour prices, a one line pip install quick start, a per second pricing page, an OpenAPI spec and a full provider rewards section with formulas, penalties and a calculator, all one or two clicks from lium.io or docs.lium.io. Buyers are best served; stakers get no page of their own, a single validator run by the team, and a chain identity with no contact, a username in the discord field and a slogan for a description.

## SN97 Albedo

Composite 2.1 (stakers 2.3, miners 2.8, buyers 1.3, newcomers 1.8). Albedo's real documentation is an llms.txt linked from the front page nav and two repo docs (MINING.md, SCORING.md) that a reader only finds by opening a GitHub repo with no README, and the site itself is a leaderboard whose panels all read loading to a fetcher. Miners are best served, though llms.txt says a 3 percent win margin while SCORING.md and MINING.md say 2.5; buyers and newcomers get a Chat with the King link, a two word chain description and nothing else.

## SN114 SOMA

Composite 3.4 (stakers 3.8, miners 3.0, buyers 3.5, newcomers 3.3). SOMA has a plain front page (one live model price with and without SOMA, a token savings chart, three named tools) and a docs site whose incentive page is dated 15 Jul 2026 and whose scoring page carries formulas and a constants table. Stakers are best served; miners get a task that shifts by competition, a compression page dated Feb 2026 that predates the current SWE benchmark mechanism, and a setup guide older than the incentive change; buyers find products named but no API reference.

## SN53 engy

Composite 4.0 (stakers 3.5, miners 3.8, buyers 4.5, newcomers 4.0). engy reads like a product: seven models priced per million tokens on the front page, an OpenAI compatible base URL in the docs, a status page with 90 day uptime per model, and a one pager in the repo that states four scoring gates, an anti wash trading rule and a cheat detection experiment with numbers. Buyers are best served; stakers get no demand figure anywhere and no page of their own, and the chain identity has no Discord field even though the site links one.

## SN91 cascade

Composite 2.0 (stakers 2.0, miners 3.3, buyers 0.5, newcomers 2.3). cascade lives entirely in its repo: a long README, an llms.txt and five deep docs give miners a generator interface with a class signature and output shape, and auditors a replay tool with three verification tiers. The chain URL redirects to a testnet host that renders only its title, the repo homepage field points at an unrelated cipher tool, and no page says who would buy a forecaster, so buyers score almost nothing and stakers have no demand evidence at all.

## SN38 ChronoLLM

Composite 3.3 (stakers 3.3, miners 3.3, buyers 3.0, newcomers 3.5). ChronoLLM's front page explains lookahead bias and point in time vintages in plain words, names three customer tiers, and the README states the emission decay, leak gate, anti copy checks and weekly reset in prose with a live config endpoint. Newcomers are best served; miners get model constraints with no hardware or cost, buyers get tiers with no institutional price and no API reference, and the leaderboard and contact path need a browser and a form.

## SN61 RedTeam

Composite 2.6 (stakers 2.5, miners 3.3, buyers 1.8, newcomers 2.8). RedTeam has a versioned MkDocs site with a current getting started guide, a challenge menu, release notes dated 2026-08-27 and a CHANGELOG dated 2026-09-09, so a miner can start. The scoring story is split across the docs root (14 day decay), a dashboard concept page (days 10 to 15), a generic incentive page and a 2024 whitepaper with point formulas; the landing page is from 2024, the dashboard is a Streamlit app that renders empty, and no buyer path or demand figure exists in own materials.

## SN34 BitMind

Composite 3.5 (stakers 3.0, miners 3.8, buyers 4.3, newcomers 3.0). BitMind is a buyer facing product with a base URL and curl example in the docs, three priced tiers with named customer types, a live detector and an SLA claim, and its repo Incentive.md states the sn34_score formula, lane and king shares and the defending window one click from the README. The chain identity is the weak point: 3 of 7 fields, no url, no description, and a contact address (intern@bitmind.ai) that the site never uses, so a wallet reader has no front door and the front page counters render as zero.

## Where the gap is widest

Across these eight the widest gap is demand. Not one subnet puts a dated usage, revenue or customer figure on its own pages: lium and engy show live supply (pods, providers) and third parties supply the revenue numbers; SOMA shows an undated savings chart; BitMind's counters read 0+ to a fetcher; ChronoLLM, RedTeam, Albedo and cascade show nothing. The second gap is the chain identity as a front door: three of eight urls redirect (Albedo through a hippius page, cascade to a testnet shell, ChronoLLM from crunchdao.com), three discord fields hold usernames or shared server channels, two contacts (Albedo, cascade) appear on no page, BitMind sets neither url nor description, and two descriptions are tags without verbs. The third is that the best mechanism documentation in the slice (cascade, Albedo, engy's one pager) sits in repo docs folders that no site front page points to, so it counts for miners and validators who already know to look there and for no one else.

## Gaps

Unknown cells: none. Every cell in the eight rows is scored, verified or inferred.

JS-rendered or partly rendered pages:

- https://taostats.io/subnets/51, /97, /114, /53, /91, /38, /61 and /34 render name, price and navigation only, no description or identity block. Identity was taken from the slice file as the brief instructs.
- https://albedo.tech is a leaderboard whose benchmarks, reign, dataset mix, queue, history and fails panels read loading to a fetcher. The static shell, the nav (llms.txt, GitHub, Chat with the King) and the llms.txt were readable.
- https://testnet.cascadesub.net/ (the redirect target of cascadesub.net) renders only the title cascade SN91.
- https://app.thesoma.ai renders only the title SOMA - Dashboard.
- https://leaderboard.chronollm.com/ renders only the heading ChronoLLM Leaderboard.
- https://dashboard.theredteam.io is a Streamlit app that renders only the word Streamlit.
- https://app.bitmind.ai renders only the title BitMind. https://bitmind.ai renders its copy but the usage, user and uptime counters show 0+ and 0%.
- https://docs.lium.io root renders only the title; the content was read from https://docs.lium.io/llms.txt and the .md pages it lists.
- https://chat.albedo.tech/ renders an Open WebUI splash only.

Identity links that pointed somewhere wrong or malformed:

- SN51 `subnet_url` lium.io has no scheme; it resolves. `discord` is the text p383_54249, not a URL, recorded as absent. `subnet_contact` and `additional` are not set. `description` is a slogan not used on the site.
- SN97 `subnet_url` https://us-east-1.hippius.com/albedo/index.html is a one line page that redirects to albedo.tech (an llms.txt is also served at that hippius path). `discord` is the handle @arbos, recorded as absent. `subnet_contact` arbos@bittensor.com appears on no page. `github_repo` resolves to a repo with no README. `description` Alchemical intelligence is not used on the site.
- SN114: all six set fields agree with the site. `subnet_contact` is an X URL rather than an email; the contact page lists the same account.
- SN53 `discord` and `additional` are not set although the site links a Discord invite. The site contact email is Cloudflare obfuscated; the match to ning@engy.ai was confirmed from the README.
- SN91 `subnet_url` cascadesub.net has no scheme and 307 redirects to testnet.cascadesub.net, which renders empty. The GitHub repo homepage field is https://cascade-woad.vercel.app, which is a rail fence cipher tool unrelated to the subnet. `discord` is the text christensor_49068, recorded as absent. `subnet_contact` chris@tensor-link.com appears on no page. `description` is a tag with no verb.
- SN38 `subnet_url` https://chronollm.crunchdao.com/ 301 redirects to https://chronollm.com/. `discord` is a channel in the shared Opentensor server, recorded as absent. `subnet_contact` crew@crunchdao.com appears on no page; the site uses forms.
- SN61 `discord` is a channel in the shared Opentensor server, recorded as absent. The other five set fields agree with the site. The site footer reads copyright 2024.
- SN34 `subnet_url`, `discord`, `description` and `additional` are not set; the site bitmind.ai was reached through the repo homepage field and README. `subnet_contact` intern@bitmind.ai differs from hello@bitmind.ai on the docs and pricing pages. The docs nav link labelled API Reference is a broken gitbook page reference.

Failed fetches (each tried once unless noted, all recorded before moving on):

- 404: https://lium.io/docs, https://albedo.tech/docs, https://thesoma.ai/llms.txt, https://engy.ai/llms.txt, https://testnet.cascadesub.net/llms.txt, https://testnet.cascadesub.net/docs, https://chronollm.com/llms.txt, https://chronollm.com/docs, https://chronollm.com/pricing, https://chronollm.com/faq, https://chronollm.com/research (pricing, FAQ and research are anchors on the front page), https://www.theredteam.io/llms.txt.
- DNS failure: https://status.lium.io, https://status.thesoma.ai, https://status.bitmind.ai.
- 403: https://medium.com/@TheRedTeam (the blog linked from the RedTeam front page).
- The RedTeam whitepaper PDF fetched but as binary; its text was extracted locally with pypdf and is in the sources list.
- GitHub REST API rate limited after the first sweep, so folder listings for Albedo, SOMA, engy, ChronoLLM and BitMind were read from github.com tree pages instead.
- No fetch had to be retried twice, so no cell is unknown for a fetch failure.

Searches and time:

- SN51 lium.io: 1 search, about 12 minutes.
- SN97 Albedo: 1 search, about 12 minutes.
- SN114 SOMA: 1 search, about 13 minutes.
- SN53 engy: 1 search, about 11 minutes.
- SN91 cascade: 1 search, about 11 minutes.
- SN38 ChronoLLM: 1 search, about 11 minutes.
- SN61 RedTeam: 1 search, about 13 minutes.
- SN34 BitMind: 1 search, about 12 minutes.
- 8 searches in total, no cap reached. Fetches for several subnets ran in parallel, so minutes are attention per subnet including reading and scoring, not wall clock.

## Ambiguities met while scoring

S1 when the front page names the product and the price but the chain description is a slogan (lium) or absent (BitMind): the 5 anchor asks for a match with the on-chain description, so both took 4 despite being the clearest commodity statements in the slice. S2 when the only live artifact is supply (pods, providers) rather than demand: lium took 3 and engy 2 because lium also has an earnings example page and per pod reliability, but the rubric could say whether a live supply dashboard counts toward demand. Contradictions between a machine facing file and the human docs (Albedo 3 versus 2.5 percent margin, cascade geometric decay versus equal share for prior kings) were scored as stale under the 2 to 3 rungs and noted. RedTeam's decay period differs between three of its own pages, which I treated as scattered rather than stale. Click counting from the docs root versus the front page again decided S3 for lium (3) and SOMA (4). For BitMind N4 the rubric's 2 anchor is a name mismatch or no site, and BitMind has a site the chain does not point to; I scored 2 because the wallet reader has no front door, which is the question N4 asks.
