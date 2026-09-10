# Calibration set: three hand-scored subnets

Rubric v1.0. Scored 2026-09-09 by the calibration agent. Chain identities read directly from Finney at block 9033581 with the Bittensor SDK on 2026-09-09, because Taostats pages are JS rendered and show no identity block to a fetcher.

These three are the anchors for the scoring agents. Each cell is in the exact CSV entry format, so a line can be pasted into a scores CSV. The same data is in `data/scores-calibration.csv`.

Composites: SN64 Chutes 4.0, SN1 Apex 3.1, SN120 Affine 1.9. No unknown cells.


## SN64 Chutes (scored 2026-09-09)

What a reader finds first: A product site: headline, model catalog with per-token prices, pricing page, docs and a status page, each one click from the front page.


### Stakers and validators

```
stakers_evidence: q1 | 5 | verified | https://chutes.ai | "Chutes is the leading open-source, decentralized compute provider for deploying, scaling and running open-source models in production." Per token and per GPU hour prices on the pricing page, matches the chain description; q2 | 3 | verified | https://chutes.ai | "Powering Trillions of Tokens per Month" on the front page, no date, no named customers, no usage dashboard (the app stats route returns Model Not Found); q3 | 3 | verified | https://chutes.ai/docs/miner-resources/scoring | scoring page with four weighted metrics, a 7 day window and one rewarded hotkey per coldkey, three clicks from the front page, written for miners, no failure modes stated; q4 | 4 | verified | https://raw.githubusercontent.com/rayonlabs/chutes-api/main/README.md | identity 7 of 7 read on chain, github and url resolve, no staker or validator page on the site, the chutes-api README tells validators to use a child hotkey instead of running one
```

stakers_score: 3.8


### Miners

```
miners_evidence: q1 | 3 | verified | https://chutes.ai/docs/miner-resources/overview | "The goal of mining on chutes is to provide as much compute as possible, optimizing for cold start times" Miners host GPU nodes that run chutes, no request or response schema for the miner, needs Kubernetes and Bittensor knowledge; q2 | 3 | verified | https://chutes.ai/docs/miner-resources/overview | "if you are using a server with 4x a40 GPUs (48GB VRAM), the server must have >= 192 GB of RAM" Bare metal and TDX required, supported GPU list only in gpu.py, registration cost not stated (chain burn 0.0005 TAO today); q3 | 4 | verified | https://chutes.ai/docs/miner-resources/scoring | weights in prose: compute units 55%, invocations 25%, unique chutes 15%, bounties 5%, 7 day window, one hotkey per coldkey rewarded, no example numbers, no immunity or deregistration policy; q4 | 4 | verified | https://raw.githubusercontent.com/rayonlabs/chutes-miner/main/README.md | step by step Ansible and sek8s guide, repo pushed 2026-08-30, no tagged releases or changelog
```

miners_score: 3.5


### Buyers and enterprises

```
buyers_evidence: q1 | 5 | verified | https://chutes.ai/docs/getting-started/quickstart | "Get your first chute deployed in under 10 minutes!" with a curl example against a chutes.ai v1/chat/completions endpoint, 31 models listed at chutes.ai/models; q2 | 5 | verified | https://chutes.ai/pricing | "No subscription, no minimum, no markup." Per 1M token prices per model, Plus $10/mo, Pro $20/mo, Enterprise custom with dedicated support; q3 | 4 | verified | https://status.chutes.ai | Better Stack status page with 90 day uptime history for website and API, help page lists docs, Discord, support@chutes.ai and a sales form, no SLA and no response time stated; q4 | 5 | verified | https://chutes.ai/docs/getting-started/authentication | API reference index at chutes.ai/docs/api-reference/overview, base URL https://api.chutes.ai, support@chutes.ai on the help page matches the chain subnet_contact
```

buyers_score: 4.8


### Newcomers

```
newcomers_evidence: q1 | 4 | verified | https://chutes.ai/docs | "Chutes is a decentralized, serverless inference platform for open-source AI models." One click from the front page, consistent with the chain description, serverless and inference left unexplained; q2 | 2 | verified | https://chutes.ai | "the leading open-source, decentralized compute provider" is the only difference claim, no comparison with a centralized provider on the front, TEE or docs pages; q3 | 4 | verified | https://chutes.ai/models | live catalog of 31 models with prices, chat app at chutes.ai/chat needs sign in, status page shows 90 days of uptime, usage figure undated, no dated benchmark; q4 | 5 | verified | https://chutes.ai/team | subnet_name matches the site, description is a human sentence, subnet_url resolves, team page and docs serve as about and learn pages
```

newcomers_score: 3.8


**Composite: 4.0**


own_words: "Chutes is the leading open-source, decentralized compute provider for deploying, scaling and running open-source models in production." | https://chutes.ai


identity_check: subnet_name | Chutes | resolves | matches the site name; github_repo | https://github.com/chutesai/chutes | resolves | CLI and SDK repo, miner and validator repos linked from its README; subnet_contact | support@chutes.ai | resolves | same address on the help page; subnet_url | https://chutes.ai | resolves | front page fetched; discord | https://discord.gg/chutes | resolves | recorded present, not read; description | Breakthrough Serverless Compute for AI, At Scale. | resolves | same headline on the front page; additional | Chutes Global Corp, Nevis registration C 61974 | resolves | operator statement, not checked against a registry


artifacts: github|https://github.com/chutesai/chutes; docs|https://chutes.ai/docs; whitepaper|none; x|@chutes_ai; discord|https://discord.gg/chutes; api|https://api.chutes.ai; dashboard|https://status.chutes.ai


sources: https://raw.githubusercontent.com/chutesai/chutes/main/README.md; https://chutes.ai; https://taostats.io/subnets/64; https://raw.githubusercontent.com/rayonlabs/chutes-api/main/README.md; https://raw.githubusercontent.com/rayonlabs/chutes-miner/main/README.md; https://api.chutes.ai/pricing; https://chutes.ai/pricing; https://status.chutes.ai; https://docs.chutes.ai; https://chutes.ai/team; https://github.com/chutesai/chutes; https://chutes.ai/help; https://chutes.ai/models; https://chutes.ai/docs/getting-started/quickstart; https://chutes.ai/tee; https://chutes.ai/docs; https://chutes.ai/docs/miner-resources/overview; https://chutes.ai/docs/miner-resources/scoring; https://chutes.ai/docs/api-reference/overview; https://chutes.ai/chat; https://chutes.ai/docs/getting-started/authentication; https://subnetalpha.ai/subnet/chutes/


searches_used: 1


minutes_spent: 9


notes: Chutes is legible to buyers first: product, prices, an endpoint and a status page are each one click from the front page. Stakers and newcomers get a tagline and an undated usage figure, and the incentive design lives three clicks down in the miner docs.


Gaps and failed fetches:

- https://taostats.io/subnets/64 is JS rendered, the fetch returns name and price only, no identity block. Identity was read from the chain with the Bittensor SDK instead and matches the seven fields given in the brief.
- https://chutes.ai/api returns the navigation header only (JS rendered). The API reference was found under /docs/api-reference/overview instead.
- https://chutes.ai/app/stats returns a Model Not Found page, so no usage dashboard was found.
- The chutes-miner README was fetched at the rayonlabs path, which GitHub redirects to chutesai/chutes-miner. The sources list keeps the URL actually fetched.


## SN1 Apex (scored 2026-09-09)

What a reader finds first: A dashboard at apex.macrocosmos.ai headed The general intelligence platform whose every counter reads zero, a README that says anyone can bring a problem, and a docs tree with per-competition specs.


### Stakers and validators

```
stakers_evidence: q1 | 3 | verified | https://raw.githubusercontent.com/macrocosm-os/apex/main/README.md | "Apex is a platform for outsourcing intelligence. Anyone can bring a problem." Output is solutions to competitions, no unit or price named, chain description reads The general intelligence platform; q2 | 2 | verified | https://apex.macrocosmos.ai/ | "Explore the terrain, discover active competitions, and watch agents climb in real time as they submit new versions of their code." Live dashboard reads 0 active competitions, 0 all time submissions and 0.00 paid out while the docs list two current competitions, no customers named; q3 | 4 | verified | https://docs.macrocosmos.ai/subnets/subnet-1-apex/incentive-mechanism.md | named incentive page: winner takes all per competition, winning code hidden until rewards are paid, burn rate rises while a solution goes unchallenged, disclaimer on malicious miner code, no subnet failure modes stated; q4 | 4 | verified | https://macrocosmos.ai/delegation-guide | identity 6 of 7 (additional empty), github and url resolve, contact matches the docs, the delegation guide names SN1 and a validator hotkey, no tokenomics page
```

stakers_score: 3.3


### Miners

```
miners_evidence: q1 | 4 | verified | https://docs.macrocosmos.ai/subnets/subnet-1-apex/subnet-1-current-competitions/text-clustering-competition.md | "Build fast, CPU-only clustering algorithms that approximate industry-standard NLP pipelines" with 5,000 texts per subset in, a POST /cluster endpoint returning cluster_ids out, a scoring formula and a baseline, three clicks from the docs root, dashboard says 0 active competitions; q2 | 2 | verified | https://docs.macrocosmos.ai/subnets/subnet-1-apex/apex-support-and-faqs.md | "Text Clustering: $20 USD" per submission in the FAQ, 4 submissions per day per hotkey on the CLI page, no hardware statement, registration cost not mentioned, scattered across three pages; q3 | 3 | verified | https://docs.macrocosmos.ai/subnets/subnet-1-apex/incentive-mechanism.md | highest score takes the full reward, raw_score must beat the top scorer by at least 1% (FAQ page), per competition formula on the competition page, no example numbers, no immunity or deregistration policy; q4 | 4 | verified | https://docs.macrocosmos.ai/subnets/subnet-1-apex/subnet-1-base-miner-setup.md | miner guide plus Apex CLI page and SOLVERS.md match the current CLI, repo pushed 2026-09-09, last GitHub release v3.0.6 dated 2025-09-11, docs pages undated
```

miners_score: 3.3


### Buyers and enterprises

```
buyers_evidence: q1 | 3 | verified | https://docs.macrocosmos.ai/subnets/subnet-1-apex.md | "You provide a problem. Apex provides research, iteration, improvement, and real results." The way in is email or the dashboard Builder link, which returns 404 at macrocosmos.ai/builder; q2 | 3 | verified | https://docs.macrocosmos.ai/subnets/subnet-1-apex.md | "Apex is built for organizations that have a measurable challenge but don't want to staff or wait on an internal research team" Enterprises, research labs and product teams named, no price for launching a competition; q3 | 3 | verified | https://docs.macrocosmos.ai/subnets/subnet-1-apex/apex-support-and-faqs.md | support@macrocosmos.ai and two Discord servers on the FAQ page, no status page, no SLA, no response time; q4 | 3 | verified | https://apex.macrocosmos.ai/ | hello@macrocosmos.ai on the dashboard and docs matches the chain subnet_contact, no Apex API reference in the docs sitemap, the search results for an Apex API page and a pricing page both return 404
```

buyers_score: 3.0


### Newcomers

```
newcomers_evidence: q1 | 3 | verified | https://docs.macrocosmos.ai/subnets/subnet-1-apex.md | "A routing layer for intelligence. You provide a problem. Apex provides research, iteration, improvement, and real results." One place, abstract, the chain description matches the dashboard headline; q2 | 2 | verified | https://macrocosmos.ai/about | "AGI won't be built in a single lab" is the company level claim, no concrete cost, ownership or coverage comparison for Apex; q3 | 2 | verified | https://apex.macrocosmos.ai/ | dashboard is live but every metric reads zero, five ended competitions are listed in the docs sitemap with no dated results or benchmarks on the site; q4 | 4 | verified | https://apex.macrocosmos.ai/ | subnet_name Apex matches the dashboard, description The general intelligence platform is the dashboard headline, url resolves, the about page is on the parent site macrocosmos.ai/about rather than the subnet site
```

newcomers_score: 2.8


**Composite: 3.1**


own_words: "Apex is a platform for outsourcing intelligence." | https://raw.githubusercontent.com/macrocosm-os/apex/main/README.md


identity_check: subnet_name | Apex | resolves | matches the dashboard headline APEX; github_repo | https://github.com/macrocosm-os/apex | resolves | README fetched, the macrocosmos.ai footer still links the older prompting repo; subnet_contact | hello@macrocosmos.ai | resolves | same address on the dashboard and the docs page; subnet_url | https://apex.macrocosmos.ai | resolves | dashboard fetched; discord | https://discord.gg/bvBDat3Gy | resolves | recorded present, not read; description | The general intelligence platform | resolves | same phrase as the dashboard headline; additional | none | none | not set


artifacts: github|https://github.com/macrocosm-os/apex; docs|https://docs.macrocosmos.ai/subnets/subnet-1-apex; whitepaper|none; x|@macrocosmosai; discord|https://discord.gg/bvBDat3Gy; api|none; dashboard|https://apex.macrocosmos.ai


sources: https://raw.githubusercontent.com/macrocosm-os/apex/main/README.md; https://taostats.io/subnets/1; https://docs.macrocosmos.ai/subnets/subnet-1-apex; https://raw.githubusercontent.com/macrocosm-os/apex/main/SOLVERS.md; https://raw.githubusercontent.com/macrocosm-os/apex/main/VALIDATORS.md; https://macrocosmos.ai; https://docs.macrocosmos.ai/llms.txt; https://docs.macrocosmos.ai/subnets/subnet-1-apex.md; https://docs.macrocosmos.ai/subnets/subnet-1-apex/subnet-1-current-competitions.md; https://docs.macrocosmos.ai/subnets/subnet-1-apex/subnet-1-base-miner-setup.md; https://docs.macrocosmos.ai/subnets/subnet-1-apex/incentive-mechanism.md; https://subnetalpha.ai/subnet/apex/; https://apex.macrocosmos.ai/; https://docs.macrocosmos.ai/subnets/subnet-1-apex/apex-support-and-faqs.md; https://docs.macrocosmos.ai/subnets/subnet-1-apex/validating.md; https://docs.macrocosmos.ai/subnets/subnet-1-apex/subnet-1-base-miner-setup/apex-cli.md; https://macrocosmos.ai/delegation-guide; https://docs.macrocosmos.ai/subnets/subnet-1-apex/subnet-1-current-competitions/text-clustering-competition.md; https://docs.macrocosmos.ai/sitemap.md; https://macrocosmos.ai/about


searches_used: 1


minutes_spent: 10


notes: Apex is most legible to miners: each competition page carries a spec, a schema, a scoring formula and a fee. Buyers and stakers get a clear pitch but no price, no API page any more, and a live dashboard that reads zero against docs that list two open competitions.


Gaps and failed fetches:

- https://taostats.io/subnets/1 is JS rendered and shows name and price only. https://api.taostats.io/api/subnet/identity/v1 returns 401 without a key, https://tao.app/subnet/1 returns 403, https://taomarketcap.com/subnets/1 shows no identity fields, https://backprop.finance/dtao/subnets/1-apex returns 403. Identity was read from the chain with the Bittensor SDK in the repo venv at block 9033581.
- The repo README links https://docs.macrocosmos.ai/subnets/new-subnet-1-apex, which returns a not found page. The live path is /subnets/subnet-1-apex.
- https://macrocosmos.ai/builder, linked from the Apex dashboard as the place to create a competition, returns 404.
- https://docs.macrocosmos.ai/pricing, /developers/readme/apex and /developers/api-documentation/sn1-apex all appear in web search results and all return 404. The docs sitemap has no Apex API or pricing page.
- https://docs.macrocosmos.ai/subnets/subnet-1-apex/subnet-1-getting-started (a search result) returns 404.
- https://x.com/MacrocosmosAI was not fetched. Third-party pages (subnetalpha) still describe the older prompting era Apex, so they were used only as a cross check.


## SN120 Affine (scored 2026-09-09)

What a reader finds first: A leaderboard at affine.io with two sentences of prose, a GitHub repo with no README, and a chain description that reads Reason Mining.


### Stakers and validators

```
stakers_evidence: q1 | 2 | verified | https://raw.githubusercontent.com/AffineFoundation/affine/main/AGENTS.md | "Affine is a Bittensor subnet (netuid 120) that crowns miners by a single teacher-anchored distillation score" Output is a crowned model checkpoint, stated only inside a developer handoff file, the repo has no README, chain description reads Reason Mining; q2 | 1 | inferred | https://subnetalpha.ai/subnet/affine/ | nothing on users, revenue or usage in own materials, the third-party page says crowned models are hosted on Chutes for public inference, no numbers anywhere; q3 | 3 | verified | https://raw.githubusercontent.com/AffineFoundation/affine/main/AGENTS.md | named mitigations RT-6, RT-11 and RT-12 and an open failure RT-7 (the live board inverts against SWE benchmarks), plus research/docs/REDTEAM.md, all inside a handoff file that assumes the reader knows the mechanism; q4 | 2 | verified | https://github.com/AffineFoundation/affine | identity 6 of 7 read on chain, the discord field holds the text consttt rather than a link, url lacks a scheme but resolves, github resolves to a repo with no README, no staker page
```

stakers_score: 2.0


### Miners

```
miners_evidence: q1 | 2 | inferred | https://raw.githubusercontent.com/AffineFoundation/affine/main/affine/ARCHITECTURE.md | miner uploads a model checkpoint through a signed mailbox flow at dash.affine.io and a sha256 manifest commit, then duels the current king, described in an architecture note, no spec or worked example for outsiders; q2 | 2 | inferred | https://www.affine.io/ | checkpoint must match the Qwen3.6-35B-A3B genesis shape per AGENTS.md, eval pods are 8x B200 class per ARCHITECTURE.md, registration price shown on the site as tmc burn history (chain burn 0.85 TAO today), no competitiveness statement; q3 | 3 | verified | https://raw.githubusercontent.com/AffineFoundation/affine/main/AGENTS.md | turn score is min(R, G) with a centered reason leg and a grounding band, a crown needs a paired margin above max(2 SE, 0.002) and three gates, no example numbers, no churn or immunity policy; q4 | 2 | verified | https://raw.githubusercontent.com/AffineFoundation/affine/main/START_HERE.txt | no miner guide, START_HERE and setup.sh cover the validator and research harness, repo pushed 2026-09-09, no releases, the submission flow appears only in ARCHITECTURE.md
```

miners_score: 2.3


### Buyers and enterprises

```
buyers_evidence: q1 | 3 | verified | https://www.affine.io/ | "Talk directly to the reigning SN120 king" links to chat.affine.io, which redirects to a sign in sandbox at arbos.life, no product page, no API, no example; q2 | 0 | inferred | none | no pricing and no customer type anywhere in own or third-party materials; q3 | 0 | inferred | none | no status page, SLA, support address or support path on the site or in the repo, the discord identity field is not a link; q4 | 2 | inferred | https://github.com/AffineFoundation/affine | no API reference, subnet_contact hello@affine.io is set on chain but appears nowhere on the site or in the repo
```

buyers_score: 1.3


### Newcomers

```
newcomers_evidence: q1 | 2 | verified | https://github.com/AffineFoundation/affine | "teacher-anchored distillation subnet (validator, evalsrv, research harness)" is the repo blurb, chain description reads Reason Mining, no plain paragraph on the site or in the repo, third-party explainers exist; q2 | 1 | verified | https://simplytao.ai/blog/your-simple-guide-to-affine-sn120 | "global, permissionless network" where anyone can contribute is a third-party claim, own materials contrast the mechanism with an LLM judge, not with a centralized service; q3 | 3 | verified | https://www.affine.io/ | live leaderboard of king versus challenger duels with margins, sigma bands and an audits section, chat with the king, no explanation of what the numbers mean, no dated benchmark; q4 | 2 | verified | https://www.affine.io/ | subnet_name Affine matches the site header AFFINE, description Reason Mining is not a sentence, url resolves without a scheme, no about or learn page, discord field is not a link
```

newcomers_score: 2.0


**Composite: 1.9**


own_words: "Affine is a Bittensor subnet (netuid 120) that crowns miners by a single teacher-anchored distillation score" | https://raw.githubusercontent.com/AffineFoundation/affine/main/AGENTS.md


identity_check: subnet_name | Affine | resolves | matches the site header; github_repo | https://github.com/AffineFoundation/affine | resolves | repo exists with no README, pushed 2026-09-09; subnet_contact | hello@affine.io | none | not verifiable, the address appears nowhere on the site or in the repo; subnet_url | www.affine.io | resolves | no scheme on chain, https://www.affine.io/ loads a leaderboard; discord | consttt | dead | not a URL; description | Reason Mining | resolves | two words, not a sentence; additional | none | none | not set


artifacts: github|https://github.com/AffineFoundation/affine; docs|none; whitepaper|https://raw.githubusercontent.com/AffineFoundation/affine/main/research/docs/PAPER_DRAFT.md; x|@affine_io; discord|none; api|none; dashboard|https://www.affine.io/


sources: https://taostats.io/subnets/120; https://affine.io; https://subnetalpha.ai/subnet/affine/; https://github.com/AffineFoundation/affine; https://www.affine.io/; https://raw.githubusercontent.com/AffineFoundation/affine/main/START_HERE.txt; https://raw.githubusercontent.com/AffineFoundation/affine/main/LAYOUT.txt; https://raw.githubusercontent.com/AffineFoundation/affine/main/AGENTS.md; https://chat.affine.io/affine; https://simplytao.ai/blog/your-simple-guide-to-affine-sn120; https://raw.githubusercontent.com/AffineFoundation/affine/main/research/docs/PAPER_DRAFT.md; https://raw.githubusercontent.com/AffineFoundation/affine/main/research/docs/MOTIVATION.md; https://raw.githubusercontent.com/AffineFoundation/affine/main/affine/ARCHITECTURE.md


searches_used: 2


minutes_spent: 11


notes: Affine's only prose lives in a developer handoff file and a draft paper inside a repo with no README, and the site is a leaderboard with two sentences of explanation. A reader who already knows the mechanism can verify it in detail, everyone else gets the chain description Reason Mining and third-party explainers.


Gaps and failed fetches:

- https://taostats.io/subnets/120 is JS rendered and shows name and price only. https://tao.app/subnet/120 and https://backprop.finance/dtao/subnets/120-affine return 403, https://taomarketcap.com/subnets/120 shows no identity fields. Identity was read from the chain with the Bittensor SDK at block 9033581.
- https://raw.githubusercontent.com/AffineFoundation/affine/main/README.md returns 404: the repo root has no README on main (files are AGENTS.md, START_HERE.txt, LAYOUT.txt, setup.sh). The gh listing confirmed main is the default branch and the organisation has only this one repo.
- https://raw.githubusercontent.com/AffineFoundation/affine-cortex/main/README.md, the repo named by the simplytao guide, returns 404.
- https://x.com/affine_io returns 402. https://dash.affine.io/, https://docs.affine.io/ and https://models.affine.io/ return 404. https://chat.affine.io/affine redirects to a sign in page at arbos.life.
- The whitepaper listed in artifacts is a draft skeleton dated 2026-08-03 that itself says production has since moved to a later scoring version.
- The brief warned that affine.ai is an unrelated company. It was not fetched. The chain subnet_url is www.affine.io.


## Calibration notes

Hardest cells to score.

- S2 (demand) when a live dashboard exists but reads zero, as on Apex. The anchor for 5 is "a live dashboard on the subnet's own site", and Apex has one, but it shows no submissions while the docs list two open competitions with a $20 fee. I scored 2 under the "stale, contradicted" clause. A scorer who reads the anchor literally would give 5. The rubric should say which wins when an artifact exists but disagrees with the subnet's other pages.
- S3 for Chutes. The scoring page is clear and has an anti-gaming section, but it is three clicks from the front page and written for miners. The 4 anchor says "within two clicks of the README or the site front page". Counting clicks is fragile: docs root to Miner Resources to Scoring is three from the front page and two from the docs root. I took 3 and said why. The rubric should say whether the docs root counts as a front door.
- M1 for Apex. The competition page is a real spec with a schema and a baseline (the 5 anchor), but the dashboard says there are no active competitions. I took 4. Same ambiguity as S2: an artifact that may be stale.
- Every Affine cell. The only prose is a developer handoff file (AGENTS.md) inside a repo with no README. It answers S3 and M3 in more detail than either of the other two subnets, but a five minute reader never reaches it. The rubric's 3 anchor ("one place, needs expertise") fits, and I used it, but the rubric could say plainly that a document not linked from any front door is capped at 3 however good it is.
- B4 and N1 for Affine, where the chain identity is the only own material. The rubric's N1 anchor says the chain description alone is a 2, so "Reason Mining" scores 2 even though it is two words. That anchor is generous. I would rephrase it as "a chain description that is a full sentence, alone, is a 2", so that a two word tag falls to 1.
- Attribution of minutes. The three subnets were fetched in parallel over roughly fifteen minutes of wall clock, so minutes_spent per subnet is an estimate of attention per subnet and the three numbers add up to more than the clock. Slice agents working one subnet at a time will have cleaner numbers.

Where the anchors were ambiguous.

- "Stated plainly in one place" versus "scattered across pages". Apex M2 has the fee on the FAQ page, the daily submission cap on the CLI page and the win margin on the FAQ again. Each is plain, together they are scattered. I scored 2. Another scorer might average to 3. The rubric could say: if a reader must open more than two pages to assemble the answer, it is scattered.
- The identity_check status tokens (resolves, mismatch, dead) do not fit text fields such as description or subnet_contact. I used resolves for text that matches the site, dead for a discord field that is not a URL, and none for an email I could not test. The brief should name a token for "text field, consistent with site" and one for "not testable".
- Whether a sign in wall counts against a demo (N3). Chutes Chat needs sign in, Affine's chat redirects to a sign in sandbox. I did not treat sign in as disqualifying but I did not give 5 either.
- Whether the parent company's about page counts for N4 when the subnet has its own site (Apex). I gave 4 not 5.

Anchors I would rephrase.

- S2 5: "A dated usage or revenue figure, or a live dashboard on the subnet's own site, that agrees with the subnet's other pages."
- N1 2: "A technical README opening, or a chain description that is a full sentence and nothing else."
- 4 (general): "within two clicks of the README, the site front page, or the docs root the site links".
- Unknown: the rule says unknown covers "a page that would not load". Taostats did not load for any of the three, but the identity was recoverable from the chain. The brief should say that a JS rendered Taostats page is not by itself grounds for an unknown S4 or N4 cell, since the slice file already carries the identity.
