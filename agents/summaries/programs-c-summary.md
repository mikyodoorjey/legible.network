# Programs slice c: summary

Read on 2026-09-19. Eight manifests in `data/programs/raw/`: 15, 4, 3, 93, 110, 56, 83, 62. All eight pass `scripts/program_check.py`. Every URL in every `sources` list answered 200 on 2026-09-19 (82 URLs).

Trust levels across the 56 fields: code 21, chain 16, docs 13, read 2, said 1, unknown 3.

## Lowest-trust field per subnet

- SN15 ORO: `buyer` at `read`. The front page names no customer, no price and no product; the trajectories feed the team's own model. Inferred from the front page line that every run becomes training data.
- SN4 Targon: `exploits` at `said` (sn4-010, the May 2025 No Free Gas post). The docs have no anti-gaming section; the guard in code is attestation and the burn of unallocated weight, which the text names.
- SN3 Teutonic: `buyer` at `read`. Crowned checkpoints are published free; llms.txt describes the income loop as emission sold for TAO to buy GPU time. No price or customer anywhere.
- SN93 Bitcast: `work` and `buyer` at `docs`. Everything else is code. The buyer is unnamed brands behind a revenue dashboard; the work reading rests on the README because the docs site does not exist.
- SN110 Green Compute: `scoring` and `split` at `unknown`. There is no repository, no incentive document and no endpoint; the site gives one sentence on what validators score and a 1.5x multiplier in a calculator.
- SN56 Gradients: all fields at `code` or `chain`; the lowest is `buyer` at `code`, read from SKILL.md in the repository because the pricing page renders only with JavaScript.
- SN83 CliqueAI: `buyer` at `unknown`. The site is a title and an empty shell to a fetcher; no API, no price, no customer in any material.
- SN62 Ridges: `work`, `scoring`, `buyer` and `exploits` at `docs`. The weight code is in the repository but the scoring and screening thresholds live only on docs.ridges.ai; the validator submits a weight mapping fetched from the platform.

## Disagreements recorded

- SN15 `scoring`: the docs scoring page describes per-family verifier rewards averaged into run and race scores with no reasoning coefficient; `src/agent/scoring.py` at the pinned commit still multiplies success rate by a 0.3 to 1.0 reasoning coefficient.
- SN15 `split`: the architecture page says the top agent receives the large majority of emissions with an optional burn; `weight_setter.py` at the pinned commit defaults the burn rate to 0.75, so the top slot is 25 percent of the vector and most of the rest burns.
- SN3 `scoring`: llms.txt (last verified 2026-08-24) states delta 0.5 nats and n 2000; `chain.toml` at the 2026-09-19 commit sets delta_threshold 0.0095 and n 20000, and dashboard.json lists seven configs stepping from 0.5 to 0.0095, the current king crowned under 0.0125.
- SN93 `work`: the chain identity names only the bitcast repository and the explainer treats YouTube as the subnet's work; the README says this code is mechanism 0 at about 2 percent of emission, with mechanism 1 for X at 98 percent in bitcast-network/bitcast-x.
- SN56 `split`: docs/miner.md says nothing is burned; `validator/scoring/constants.py` at the same commit defines EMISSION_BURN_HOTKEY on its first line, whose use this reading did not trace.
- SN83 `scoring`: docs/mechanism.md gives three problem classes at difficulty 0.2, 0.4 and 1; `problem_selector.py` at the same commit ships four classes at 0.7, 0.8, 0.9 and 1.0, the fourth at 890 to 900 vertices.
- SN62 `split`: the incentive page says the time multiplier doubles after a 6-hour stall; `api/config.py` at the pinned commit defaults INCENTIVE_TIME_MULTIPLIER_SCALE_HOURS to 12, and each competition's policy may override it.

## Unknowns recorded

- SN110 `scoring`: looked for a scoring formula, validator code or an incentive document on the front page, about, providers, enterprise and apply pages, in the chain identity (github_repo unset) and in the index. Found one sentence (validators score performance, reliability and proof integrity) and a calculator's 1.5x green multiplier. No repository, no endpoint, no document.
- SN110 `split`: looked for how the miner share divides on every site page, in the chain identity and the index. The providers page says validators route demand by performance, reliability and attestation and pay every epoch; nothing says proportional, winner-heavy or floored. One active miner on the 2026-09-09 snapshot.
- SN83 `buyer`: looked for a customer, a price or a way to submit a graph on cliqueai.toptensor.ai (empty shell to a fetcher), the README, docs/mechanism.md, min_compute.yml, the wandb table link, the chain identity and the narrative map. Found none.

## Notes for the next reader

- ORO's repository uses Git LFS for `data/local-test/env-pack.tar.gz`; a plain shallow clone leaves the working tree half checked out on a machine without git-lfs. Disabling the LFS filters and resetting restores the source tree.
- Targon's live auction endpoint (`tower.targon.com/api/v2/auctions`) returned Bad Gateway on 2026-09-19; the auction targets in the manifest come from the docs example in the repository, not from a live read.
- Bitcast-x (mechanism 1, 98 percent of SN93 emission) was not cloned; the manifest pins the bitcast repository the chain identity names and records the split in `disagrees`. A second manifest for bitcast-x would be the natural follow-up.
- Ridges validators do not compute weights; they fetch `/scoring/weights` from the platform and submit it after checking it sums to one. The manifest says so in `judges`.
- Narrative statements for SN62 (sn62-006, sn62-010, sn62-012) were considered for `work`, `split` and `exploits` and outranked by docs pages fetched this session that carry the same content at higher trust.
