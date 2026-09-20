# Programs slice b: summary

Read on 2026-09-19. Eight manifests in `data/programs/raw/`: 51, 97, 114, 53, 91, 38, 61, 34. All pass `scripts/program_check.py`. Trust counts across the 56 fields: docs 19, code 18, chain 16, read 3, said 0, unknown 0.

## Lowest-trust field per subnet

- SN51 lium.io: `work` and `buyer` at docs. The scoring and split are in the validator code; what is produced and who pays are only stated in the subnet's own prose (llms.txt, pricing page). No customer is named anywhere.
- SN97 Albedo: `buyer` at read. The front page offers only a Chat with the King link; the absence of a price, API or customer is the site's own inference from that page.
- SN114 SOMA: `work` and `buyer` at docs. The compression task is defined in the README; the only price is one model's per-million-token rate on the front page.
- SN53 engy: every non-chain field at docs. The repository holds only a light validator that relays a master-signed weight vector; the scoring formula, gates, split and cheat experiment live in docs/SN53_ONE_PAGER.md, and the audit box that verifies proofs is not in the repository.
- SN91 cascade: `buyer` at read. cascadesub.net did not resolve; testnet.cascadesub.net is a scoreboard with no product, price or customer.
- SN38 ChronoLLM: `work` and `buyer` at docs. The vintage-model task is README prose; the three pricing tiers on chronollm.com carry no figure.
- SN61 RedTeam: `buyer` at read. The front page promises enterprise access but has no product page, API or price and a 2024 copyright. `scoring` is also only docs: the per-challenge managers that apply the similarity penalty and the decay run inside challenge Docker images, and the set_weights loop is not in the repository.
- SN34 BitMind: `scoring` and `exploits` at docs. sn34_score (MCC plus Brier) and the 0.01 dethrone margin are computed on the platform and described in docs/Incentive.md; only the lane split and the 85/10/5 residual are in the validator code.

## Disagreements recorded

- SN51 `split`: the docs emission page says the rented pool is a fixed 13 percent and the burn ceiling moved from 91 to 87 percent in mid-2026; lium.io/api/v1/shared-config returned total_burn_emission 0.9 on 2026-09-19; the packaged default at the pinned commit is 0.91.
- SN114 `scoring`: docs/miner/scoring.md at the pinned commit (mirrored on thesoma.ai) gives a bonus cap of 3.0, a penalty floor of -4.0 and floor(0.8x); mcp_platform/app/api/routes/scoring.py at the same commit caps the bonus at 0.1, starts the penalty at -2 and uses ceil(0.8x).
- SN53 `judges`: the one-pager says a validator samples requests, verifies the proof and sets weights; validator/sync.py says the provider owns scoring and the validator checks only the master hotkey's signature, and VALIDATOR.md calls the GPU audit box a different component.
- SN53 `cadence`: the one-pager says epochs are weekly in production and 4 hours on staging; the validator/sync.py docstring says the code once pinned 604800 seconds while production ran 86400 and staging 3600.
- SN91 `split`: docs/ARCHITECTURE.md says an equal share across the king plus up to reward_prior_kings prior kings; chain.toml sets king_decay 0.5, loop.py passes it to decayed_share_vector, and the README and llms.txt give about 52/26/13/6/3 percent.
- SN38 `scoring`: code defaults at the pinned commit are leak_weight 0.7, quality_weight 0.3, top_n_for_quality 10; api.chronollm.com/config on 2026-09-19 returned 0.0, 1.0 and 30, so the README's final_score = quality_win_rate is what runs.
- SN61 `scoring`: the docs root and repo docs/README.md say points decay linearly over 14 days; the dashboard concept page says decay starts at 10 days and runs over approximately 10 to 15 days; the managers that apply it are not in the repository.

## Unknowns

None recorded. Every field found a source at docs trust or above, or a page from which an absence could be read (the three `read` fields for buyer on SN97, SN91 and SN61).

## Notes for the next reader

- SN53 immunity_period is 1 block; SN38 tempo is 1440 and immunity 50400; SN61 immunity is 14400. All stated plainly in `cadence`.
- SN91's head commit is dated 2026-09-20 in git (committer timezone); recorded as-is.
- The narrative statement keith-singery-012 is tagged subnet:53 but describes the earlier Efficient Frontier subnet at that netuid, not engy; it was not used.
- No `said` field was used: the SN34 statements (sn34-003, sn34-006) are older and less specific than docs/Incentive.md at the pinned commit.
