# Explainers, slice c

Written 2026-09-10 by agent c. Eight entries in data/explainers/: 15, 4, 3, 93, 110, 56, 83, 62. All pass scripts/check_explainers.py with --links (every Source and Go deeper URL returned 200).

## Metaphor and the hardest thing to explain

- SN15 ORO: a daily talent contest for robot personal shoppers. Hardest: that the product for sale is not the agents but the recorded footage (trajectories) and a model trained on it, while the shopping assistant a buyer would pay for is still on the roadmap.
- SN4 Targon: a hotel of sealed rooms owned by strangers. Hardest: a trusted execution environment, and why a guest would trust a chip's proof rather than the hotel; also that a public price list exists while every machine reads Out of Stock.
- SN3 Teutonic: a boxing title for language models. Hardest: the paired bootstrap acceptance test, and that the champion's weights are public so every challenger starts from the incumbent.
- SN93 Bitcast: a sponsored-video job board with no agency. Hardest: that pay is anchored in dollars read from YouTube's own analytics, then paid in a token, with 62 percent of revenue recycled into that token rather than to creators.
- SN110 Green Compute: a green electricity tariff for AI computing. Hardest: that the sales site is complete (prices, endpoint, sales address) while the subnet mechanism has no code, no formula and, on the day of checking, one active miner.
- SN56 Gradients: a tailoring service with a weekly cutting contest. Hardest: that miners submit training code rather than compute, the validators' own GPUs do the work, and the winning code is open-sourced.
- SN83 CliqueAI: a timed puzzle league with no sponsor. Hardest: saying plainly that the puzzles are written by the validators and nobody outside the subnet has asked for the answers, without editorialising.
- SN62 Ridges: an open tournament for robot software mechanics. Hardest: two routes to emission (3 percent better or 6 percent cheaper), a stall multiplier and a 14 day half-life, in three sentences a newcomer can follow.

## Where the sources were thinnest

CliqueAI is the thinnest: one mechanism document, a one-line README, a site that is an empty shell to anything but a browser, and no statement anywhere of what the answers are for or what decentralization changes; the "Why it is on Bittensor" section had to say the materials do not say. Green Compute is a full sales site with no technical material at all: no repository, no incentive document, no scoring formula, so the mechanism section rests on two sentences from the providers page and a calculator. Teutonic's only prose is llms.txt, written for AI agents, and its evaluation numbers disagree with the live dashboard data on two successive days (0.025 then 0.1 against the file's 0.5), which the entry reports as a disagreement rather than resolving. Bitcast's mechanism lives in code, a CLAUDE.md file and an August 2025 substack post; the dated dashboard is excellent but explains nothing. Gradients' site returned 403 to WebFetch (200 to curl), so the pricing page was read from SKILL.md in the repository and the news page from curl output; the README and miner guide disagree on entry fees. Ridges' front page returns a Vercel security checkpoint to fetchers, so everything came from docs.ridges.ai and the index notes taken in a browser. Targon and ORO were well documented; the gaps there are demand (no usage figure for Targon, no product for ORO) rather than sources.

## Note for the maintainer

scripts/check_explainers.py line 77 has an unterminated regex group, `r"\]\((https?://"`, which raises re.PatternError before any file is checked. I ran a patched copy from the scratchpad (pattern `r"\]\(https?://"`) rather than edit the shared script. The repo copy is unchanged.
