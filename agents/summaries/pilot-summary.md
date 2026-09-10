# Pilot summary: SN64 Chutes and SN120 Affine

Scored 2026-09-09 by the pilot agent under rubric v1.0, without sight of the hand scores for these two subnets. Rows are in `data/scores-pilot.csv`.

## SN64 Chutes

Composite 4.1 (stakers 4.3, miners 3.3, buyers 5.0, newcomers 3.8). Chutes is legible because the front page does the work: the chain description is the site headline, a Python example posts to a named endpoint, the pricing page carries per-token and per-second prices, and the status page, the API reference and a support address that matches the chain contact are each one click away. Buyers are the best served audience; miners are the least, because the miner overview and ansible pages on the docs site still describe GraVal and Wireguard while the chutes-miner README says the network is TEE-exclusive and GraVal is no longer supported, and no page on the site is written for stakers or validators.

## SN120 Affine

Composite 2.7 (stakers 2.5, miners 4.0, buyers 1.8, newcomers 2.5). Affine is legible to exactly one audience through exactly one file: `www.affine.io/llms.txt`, one click from a live dashboard, holds the submit checklist, the hardware line, where to read the registration cost, the full scoring contract and dated fork notices, and the repo has no README at all (START_HERE.txt points to an internal handoff file). Miners are the best served audience; buyers and newcomers meet a JS-rendered dashboard with a chat box, a two word chain description (Reason Mining) that appears nowhere on the site, no contact address anywhere on the site, no about page and no plain paragraph saying what the subnet is.

## Gaps

Unknown cells: none. Every cell in both rows is scored.

JS-rendered or partly rendered pages:

- https://taostats.io/subnets/64 and https://taostats.io/subnets/120 render name, price and navigation only, no description or identity block. Identity was taken from the slice files as the brief instructs.
- https://www.affine.io is a dashboard whose charts, reign, queue, history and audits panels all read "loading" to a fetcher. The static shell, the meta description and the inline chat text were readable, and the data behind the panels was fetched from https://affine.io/api/v1/snapshot and https://affine.io/api/v1/history?limit=3, which are plain JSON.
- https://chutes.ai and its docs pages are server rendered and fetched cleanly.

Identity links that pointed somewhere wrong or malformed:

- SN120 `discord` is the text `consttt`, not a URL. Recorded as absent and marked `dead` in identity_check.
- SN120 `subnet_url` is `www.affine.io` with no scheme. It resolves (http redirects 301 to https://www.affine.io/), so it was marked `resolves` with the missing scheme noted.
- SN120 `subnet_contact` hello@affine.io appears nowhere on the site, in llms.txt, or in the repo handoff files. Not wrong, but unconfirmable from the subnet's own materials.
- SN120 `github_repo` resolves but the repository has no README on main or master (both raw fetches returned 404). The repo root holds START_HERE.txt, LAYOUT.txt and AGENTS.md instead.
- SN120 `description` Reason Mining is not used on the site; the site calls itself a king-of-the-hill subnet.
- SN64: all seven fields agree with the site. The README at github_repo is the SDK README and links the miner and validator repos under the older rayonlabs org, which redirect to chutesai.
- The affine.ai domain was not visited; Affine's site is affine.io.

Failed fetches: https://raw.githubusercontent.com/AffineFoundation/affine/main/README.md and the master branch equivalent, both 404 (no README exists). GitHub releases API returned Not Found for chutesai/chutes, chutesai/chutes-miner and AffineFoundation/affine (no releases published). No fetch had to be retried.

Searches and time:

- SN64 Chutes: 3 searches, about 12 minutes.
- SN120 Affine: 3 searches, about 11 minutes.
- Neither cap was reached. Wall clock for fetching was short because pages were fetched in parallel; the minutes recorded are the attention spent per subnet including reading and scoring.

## Ambiguities met while scoring

The rubric's 4 anchor says "within two clicks of the README, the docs root, or the site front page", and the Chutes scoring page is one click from the docs root and three from the front page, so I counted it as within reach and gave S3 a 4; the brief's own restatement of the ladder drops the docs root, so a scorer reading only the brief would count three clicks and give 3. The 5 anchors for B3 and M2 are met literally by Chutes and Affine (a status page plus an escalation path, hardware plus where to read the registration cost) while missing things a reader would want (no SLA or response time, a one line hardware statement in a file named llms.txt), and "take the lower when torn" pulled Affine M2 down to 4 but not Chutes B3, which shows how much that rule depends on whether the scorer admits to being torn. The identity_check tokens do not cover a URL field that holds a non-URL (Affine's discord), so I used `dead` and said why. For B2 and B3 the ladder's 1 is defined as "third-party only", which does not describe Affine, where no third party covers pricing or support either, but 0 ("nothing findable") felt too strong for B2 because the site does offer the dataset and chat free of charge; a rung for "own materials mention it in passing with no answer" would fit. Finally, Affine's llms.txt is the subnet's real documentation but its name and register are for agents, and the rubric does not say whether a file written for machines counts as plain for a human reader; I treated it as own material in one place and let the jargon decide between 3 and 4 in each cell.
