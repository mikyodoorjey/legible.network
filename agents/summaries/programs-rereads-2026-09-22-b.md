# Program re-reads, 2026-09-22, batch b

Three manifests re-read at their repository heads. Old-commit raw URLs replaced throughout `sources` and every `code` field; every new raw URL confirmed 200 with curl; `read_on` set to 2026-09-22; each file passes `scripts/program_check.py`.

## SN38 ChronoLLM

`01f596b4` (2026-09-14) to `a1f1aa75` (2026-09-22), 2 commits ahead. Stale fields `scoring`, `split`: both still cite `sn38/neurons/validator.py`, which changed, but the scoring formula (`leak_weight * normalized_leak + quality_weight * win_rates`) and the split line (`np.exp(-0.8 * (np.arange(n) ** 0.9))`) are unchanged, as are the fallback defaults 0.7, 0.3 and top_n 10. Texts kept.

What changed in the mechanism: the quality stage is now async, caches the round's judge prompts and every miner's completions in the validator's SQLite so a restart does not regenerate them, and drops miners whose Hugging Face model cannot be downloaded from the round-robin, so an inaccessible model gets no duel wins. Completion length per prompt went from 50 to 100 new tokens. The validator docker image digest changed.

Live config: `https://api.chronollm.com/config` re-fetched 2026-09-22 still returns leak_weight 0.0, quality_weight 1.0, top_n_for_quality 30, emission_pct 1.0, min_eval_score -3.0, leak_threshold 0.1, known_threshold 0.7. The live values still differ from the code defaults.

Disagrees:
- `scoring` (changed): same disagreement, re-dated to the 2026-09-22 fetch of the config endpoint.

## SN8 Vanta

`3fd1dcfa` (2026-09-18) to `1b758503` (2026-09-20), 1 commit ahead. Stale field `exploits`: cites `vali_objects/vali_config.py`, which changed, but the only edit removed `PRO_TRANSITION_GRACE_PERIOD_DAYS`; the plagiarism threshold 0.75, 10-day lookback, 14-day review and drawdown constants are unchanged. Text kept.

What changed in the mechanism: a miner in the pro-challenge transition bucket used to be promoted after a fixed 7-day grace period; it is now promoted at the start of the next payout week, the first Monday 00:00 UTC after it entered. The testnet-only env override for the grace period is gone.

Disagrees:
- `scoring` (added): the `debt_based_scoring.py` docstring says the payout week starts and ends at midnight Sunday 00:00:00 UTC; the boundary the file computes, `TimeUtil.ms_at_start_of_week`, rounds to Monday 00:00 UTC via `weekday()`, and the head commit's `challengeperiod_manager.py` names the same boundary as Monday 00:00 UTC.
- `cadence` (added): the same conflict, since the cadence text carries the Sunday boundary.
- `exploits` (unchanged): README gives one drawdown rule for all miners, 5 percent intraday or 8 percent end-of-day; `docs/miner.md` at the same commit says challenge-period miners are eliminated at 5 percent end-of-day. Both files still say this at head.

## SN91 cascade

`e745a327` (2026-09-20) to `7ebfc19d` (2026-09-22), 15 commits ahead. Stale fields `scoring` (`cascade/eval/koth.py`) and `split` (`chain.toml`), both changed.

What changed in the mechanism: in `koth.py`, a bootstrap lower bound that comes out NaN (empty resample) is now an inconclusive round, the king holds and the streak is untouched, where before it compared False and read as a challenger loss; the verdict also carries a per-domain breakdown of both geomeans for display. The cohort max-T bound can now be computed in increment units, gated on `cohort_maxt_increment_from_block`, which is 0. `chain.toml` gains the DEC-CA-0043 rollover keys (rolling intake, a 12-hour era king, a 3 hour settlement grid, tenure in blocks, per-leg GPU choice under price caps) and a DEC-CA-0045 `[activation]` section that flips them when 51 percent of permit-holding validator stake has posted a readiness commitment; every typed-in key is 0. The split keys `king_decay 0.5`, `reward_prior_kings 4`, `burn_uid 0` are unchanged. Scoring text rewritten to add the inconclusive rule; split text kept.

README and llms.txt re-fetched at the new commit: both still describe geometric decay, the king plus 4 prior kings at 0.5 to the power of distance, about 52/26/13/6/3 percent, remainder burned to UID 0. That matches `chain.toml`. `docs/ARCHITECTURE.md` at head still says an equal share.

Disagrees:
- `split` (unchanged in substance): ARCHITECTURE.md equal share versus chain.toml, loop.py, README and llms.txt geometric decay.
- `cadence` (added): the README announces rolling intake next, 3 hour settlements against a 12 hour era king, switched on by 51 percent stake signalling; chain.toml keeps `epoch_blocks 3600` with `rolling_from_block` and `era_king_from_block` at 0. Whether the on-chain lock-in has fired was not checked.
- `buyer` (added): cascadesub.net, which did not resolve on 2026-09-19, now redirects to dashboard.cascadesub.net, the mainnet scoreboard; still no product, price, API or customer.

## What the previous readings got wrong

- SN8: the Sunday 00:00 UTC payout boundary in `scoring` and `cadence` was read from a docstring; the code computes Monday 00:00 UTC. Texts left as they were, the conflict recorded in `disagrees`.
- SN91: the `split` text describes the dethrone margin as 0.01 fresh, 0.005 after 8 rounds, the `margin_mode = "level"` rule. At both the pinned and the new commit `increment_from_block = 9046800` schedules the increment rule, under which the margin is a fraction of the per-round improvement over the shared init, floored at `margin_increment_floor 0.01` of the baseline. Whether block 9046800 has passed was not checked. Not a change between the two commits, so the text was not rewritten.
