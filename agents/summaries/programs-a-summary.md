# Programs slice a: summary

Read on 2026-09-19. Six manifests written: SN80, SN9, SN28, SN58, SN124, SN90. SN107 and SN64 were hand-written calibration manifests and were not touched. All six pass `scripts/program_check.py`; all 53 source URLs returned 200 on 2026-09-19.

Trust counts across the six (42 fields): chain 12, code 8, docs 19, read 3, said 0, unknown 0.

## Lowest-trust field per subnet

- SN80 OpenRoboto: `buyer` at `read`. The front page describes a competition whose winner becomes the next base; the competitions API lists miner fees only. No customer, price or usage figure anywhere. Nothing in the repository at `code` above `docs`: validator.py only reads a settled weight vector from the operator's backend, and the ranking and evaluation code live in other repositories.
- SN9 iota: every field is `docs` or higher; the weakest reading is `scoring` at `docs`, because the repository at the pinned commit holds no scoring function (the validator loads validation functions from an orchestrator directory that is not in the repo and fetches finished global scores).
- SN28 SayGM: `work` at `docs`. The index lists the miner repository (taostat/gm-miner); the program itself is in taostat/gm-validator, which was pinned instead, following the Chutes calibration. Scoring, split and exploits are at `code` from that repo.
- SN58 greevils: `buyer` at `read`. The site sells an arena; traders bring their own money; the only fee is a builder fee of about 5 bps stated in the validator README. The incentive document and validator README sit in greevils-ai/greevils-validator, read at `main` and cited at `docs`, since the pinned repo (greevils-cli, last commit 2026-07-06) holds only the participant CLI.
- SN124 Swarm: `buyer` at `read`. The site names sectors and adapters but no customer, price or endpoint; the way in is a contact form.
- SN90 KubeTEE: `work`, `buyer` and `exploits` at `docs`. Scoring and split are at `code` from validator/miner_scoring.py. Note: the pinned commit's `git log --date=short` gives 2026-09-20 (author time 01:31 +03:00, which is 22:31 UTC on 2026-09-19); recorded as the command reported.

## Disagreements recorded

- SN80 `scoring`: the overview at the pinned commit says the round scores six LIBERO suites for a pi0.5 base; the live competitions API on 2026-09-19 names the simulation benchmark libero_pro_custom_1 with a LingBot-VLA 2.0 base and a baseline of 0.285833 over 5 trials.
- SN9 `scoring`: the docs say the exact thresholds live in the code; the repository at the pinned commit holds no scoring function. task_execution.py loads validation functions from an orchestrator directory that is not in the repository, and weight_setting.py fetches finished scores from /validator/global_miner_scores.
- SN58 `scoring`: the incentive document scores agents and humans in one tournament with a separate agent pool; the validator README says the agent classifier is not deployed, so the agent lane is inert and every account is classified human.
- SN90 `scoring`: the README's economics section says emissions are weighted by attested TEE health, job-execution quality and uptime and that no attestation means no emissions; its What Ships Today table and the code at the pinned commit put only Rancher readiness in the weight path, with attestation, Armada metrics and health designed and not yet scored.

## Unknowns

None. Every field found a source at `read` or higher. The three `read` fields (SN80, SN58, SN124 `buyer`) are inferences from absence on the front page, the app and the repository, and each `text` says what was looked for.

## Notes for the next reader

- SN80: the live weights endpoint (`/api/weights`, read key published in control.json) returned 0.425, 0.425, 0.105, 0.03, 0.015 on 2026-09-19, matching the documented 42.5 / 42.5 real tracks and 70 / 20 / 10 of 15 percent for simulation. It needs an API key header, so it is not in `sources`; the observation is in the `split` text.
- SN9: `FALLBACK_BURN_FACTOR = 0.8` is defined in shared/common settings.py and referenced nowhere else in the repository; the burn share arrives from the orchestrator as the owner UID's weight.
- SN28: chain hyperparameters are unusual for the slice: weights_rate_limit 1, immunity_period 3600, bonds_moving_avg 0. The validator's epoch is 361 blocks (tempo + 1). Epochs on the miners page are about 72 minutes apart.
- SN58: the live leaderboard at app.greevils.ai read no competitors on 2026-09-19; the front page leaderboard uses illustrative names.
- SN90: the validator dashboard on 2026-09-20 showed the owner's staging cluster (UID 56, hardcoded as OWNER_MINER_UID in config.py) earning 64 percent of the pool and the one production miner (BTLABS, UID 97) 32 percent, with $31.48 recycled.
- Narrative map: statements exist only for SN9 (sn9-001 to sn9-015, keith-singery-021); none describe an exploit, so no field in the slice uses `said` trust.
