# Programs slice d: summary

Read on 2026-09-19. Seven manifests written (SN120 was already a calibration manifest and was skipped): `data/programs/raw/44.json`, `8.json`, `68.json`, `75.json`, `118.json`, `5.json`, `19.json`. All seven pass `scripts/program_check.py`.

Trust levels across the 49 fields: code 19, chain 14, docs 14, read 1, unknown 1, said 0. No `said` field: `data/narrative.json` holds statements about SN75 (marketing and a Calacanis aside), one 2024 podcast note about SN8, and one video table of contents for SN19; none of them speaks to a program field better than the code or docs did. SN44, SN68, SN118 and SN5 have no statements at all.

## Lowest-trust field per subnet

- SN44 Score: `buyer` at `read`. The front page is a research-company pitch with a Console link and a contact form; no price, product page, endpoint or named customer in text on the site or in the repository.
- SN8 Vanta: `work` at `docs`. The order-signal contract is prose in the README and docs/miner.md; every other field reached `code` or `chain`, and `buyer` reached `docs` through the Vanta Trading pricing page.
- SN68 NOVA: `work` at `docs`. The submission format is described in docs/MINER.md; scoring, split and exploits all came from `config/config.yaml` and `neurons/validator/weights.py`.
- SN75 Hippius: `work` at `docs`. The storage-miner page describes shards and challenges; the weight formula, pool split and family aggregation are all in the Substrate runtime and pallets at `code`.
- SN118 Ditto: `work`, `scoring`, `buyer` and `exploits` at `docs`. The composite formula lives in the Go scorer under `services/dittobench-api`, which was not opened, so `scoring` rests on the site page; `split` reached `code` through `ditto/validator/config.py`.
- SN5 Hone: `buyer` at `unknown`. Nothing to buy, no price, no customer, no endpoint, on the dashboard or in the repository.
- SN19 blockmachine: `work` at `docs`, from the miner README in a second repository. Note: the chain identity's `github_repo` (taostat/blockmachine) is a one-file link page; the manifest pins taostat/blockmachine-validator at 25ca87c (2026-09-17), where the weight and verification code lives, and cites the miner README at its own head ef5e876 (2026-09-15) at `docs` trust only.

## Disagreements recorded

- SN44 `judges`: the draft whitepaper describes an aggregation service merging every validator's shards with stake-weighted MAD pruning; the code at d6c5529 reads winners from a single `SCOREVISION_CENTRAL_VALIDATOR_HOTKEY` and falls back to local data when it is absent.
- SN8 `exploits`: the README gives one drawdown rule for all miners, 5 percent intraday or 8 percent end-of-day; docs/miner.md in the same repository says challenge-period miners are eliminated at 5 percent end-of-day and only main-competition miners at 8.
- SN68 `split`: docs/MINER.md and the nova page say the winner per type receives the incentive; the code at 623f345, with `config/config.yaml` `payout.enabled: true` and `override_uid: 42`, puts all on-chain weight on UID 42 and pays winners through emission-transfer-api.metanova-labs.ai (`neurons/validator/payouts.py`).
- SN75 `split`: docs.hippius.com/learn/weights and the summary at the top of readme_weights.md say the miner pool grows with stored data relative to emissions; `pallets/execution-unit/src/weight_calculation.rs` at 3187525 and Layer 3 of the same readme fix it at 1 percent to miners and 99 percent to UID 238.
- SN118 `scoring`: the site scoring page (updated 2026-07-13) says the locked model is Qwen3-32B; docs/MINER.md at 2b05b32 says the current contract, Bench v12, is openai/gpt-oss-20b.
- SN118 `split`: the site scoring page says the champion holds about 90 percent with a margin of about 5 percent; `ditto/validator/config.py` at 2b05b32 sets `KOTH_RANK_SHARES = (0.65, 0.14, 0.10, 0.07, 0.04)` and `KOTH_MARGIN = 0.007`, and docs/MINER.md matches the code.
- SN19 `split`: the whitepaper says an emission burn sink removes excess unearned alpha; the comment in `common/scoring/weights.py` at 25ca87c says the pool-over-consumption cap was removed so burn is zero every epoch, with burn only on the sanity bound or an epoch with no gateway activity.
- SN19 `cadence`: the miner README at ef5e876 says validators submit weights each epoch (~72 minutes); the chain hyperparameters (tempo 7200) and the validator README say 7,200 blocks, about 24 hours.

## Unknowns

- SN5 Hone `buyer`: looked for a price, a customer, a product page or an endpoint on honedashboard.com (a miner-performance dashboard that renders "Waiting for aggregate data" to a fetcher) and in README.md, docs/DESIGN.md and docs/DEMO_MINER.md at 34de7f6. None found. The README says problem construction is not part of the repository and names a private problem server; the only hint of an output beyond weights is that partial-credit rewards affect exported dataset labels. No chain contact or discord to ask.

## Notes worth passing on

- SN68: the validator's on-chain vector at the pinned commit is 100 percent UID 42 (the "compound payout UID"); winners are paid off chain by a Metanova API keyed by `WALLET_TRANSFER_API_KEY`. The competition epoch is 361 blocks against a chain tempo of 360.
- SN75: miners as a class receive 1 percent of the weight budget at the pinned commit; the Bittensor validator relays a ranked list computed on the Hippius chain rather than judging anything.
- SN8: burn UID 229 receives whatever emission exceeds the week's debt; the debt scoring docstring also cites two different testnet burn UIDs (5 and 220) within the same file.
- SN44: the repository's `blacklist` file holds 120 hotkeys with no stated reason; weights to them are removed before signing.
- SN118: immunity is 300 blocks, one hour, the shortest in the slice; SN8 is 1,200 blocks, four hours; SN19 tempo is 7,200 blocks, a day.
