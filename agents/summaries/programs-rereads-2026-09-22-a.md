# Program rereads 2026-09-22, batch a: SN120, SN51, SN56

Three manifests re-read against the repository heads recorded in `data/programs-drift.json`. Each repository was cloned shallow at its head; every `code` field's `url` now points at that head and returned 200. `read_on` is 2026-09-22 on all three. Fields at `docs`, `chain`, `said` and `read` trust were kept unless the new code contradicted them.

## SN120 Affine

Repository moved from `1c3b5999` (2026-09-10) to `d41cca5a` (2026-09-21), 405 commits, weight_version_key 10 to 22. The scoring rule changed: since 2026-09-18 (wvk 22) `[duel].score_mode` is `sd_min_rga`, the turn score is `min(z_R, typ_c, z_A)` in teacher standard-deviation units computed in `affine/evalsrv/sdmeter.py` and applied as the deciding rule in `affine/evalsrv/dueling.py`; `n_turns` fell from 1,300 to 1,000, the crown floor is `min_margin_sd = 0.2` and a forfeited turn scores `forfeit_sd = -12`. Between the two commits the crown rule also went through a 12-hour window-best mode (wvk 15), a confirmation slice (wvk 19) and back to one seeded slice with `max(2 SE, floor)` (wvk 16, wvk 21). The payout rule (one equal share per crown less than 72 hours old, burn when none) is now in the repository as `affine/affine/payout.py`, and `chain.py`'s `set_rolling_weights` delegates to it.

- `scoring`: rewritten at `code`, path now `affine/evalsrv/sdmeter.py`. Old `disagrees` (llms.txt described `min(z_R, typ_c, z_A)` with a 0.2 sd floor while the code had `min(R, G)` and 0.002) is resolved: llms.txt fetched 2026-09-22 and the toml agree. New `disagrees`: the `score.py` module header at this commit still calls `min(R, G)` the live rule and defaults `score_mode` to `reason`, while `affine.toml`, `dueling.py` and llms.txt all say `sd_min_rga`.
- `split`: kept at `docs`. Old `disagrees` (the 72-hour rule postdated the pinned commit and the payout module was only on Hippius) is resolved and removed; `payout.py` at the new head carries the rule and is in `sources`. This field could be upgraded to `code` on a later pass.
- `exploits`: mechanism unchanged in kind; text updated to say the filler-suffix hack led first to `min(R, G)` and then to the sd-meter, and that the copy check compares safetensors digest multisets (`model_store.py`, `check_model_copy`). Quote and path unchanged.
- llms.txt: `www.affine.io/llms.txt` now 301s to `affine.io/llms.txt`; the page's scoring meter, turn count, floor and payout rule match the code.

## SN51 lium.io

Repository moved from `61020313` (2026-09-18) to `606d4a72` (2026-09-22), 15 commits. The two files the stale fields cite changed without changing the mechanism: `shared_config/defaults.py` gained a `NVIDIA B300 SXM6 PC` alias derived from the AC row (`total_burn_emission` is still 0.91), and `services/const.py` gained the same alias in `GPU_MODEL_RATES`, a dind image bump to 0.0.3, and one more TDX compose-hash whitelist entry. `rental_price.py`'s scoring line is unchanged. Texts and quotes kept; URLs repointed.

- `split` `disagrees` updated, not resolved: the live `lium.io/api/v1/shared-config` returned `total_burn_emission` 0.9 again on 2026-09-22 against the packaged 0.91 and the docs' 87 percent.

## SN56 Gradients

Repository moved from `8b673e24` (2026-09-17) to `0791bb6e` (2026-09-22), 8 commits. The bracket changed: text round 1 is now always a single group of every entrant playing three instruct tasks with the top two advancing (it used to depend on field size); the forced pre-boss model `Qwen/Qwen3-32B` is dropped, so the last knockout pair gets an ordinary task; the boss round's large instruct model range is 30B to 72B (was 35B to 71B); and `MAX_NEAR_DUPLICATE_RATE`, a dataset-quality gate on text tasks, fell from 0.20 to 0.10. Per-sample judging, fees, the weekly schedule and the three-tier dedup are unchanged.

- `work`: mechanism unchanged; quote still present in `docs/miner.md`; URL repointed.
- `scoring`: text rewritten for the new round-1 format; quote unchanged.
- `exploits`: mechanism unchanged; quote still present; URL repointed.
- `split` `disagrees` refined: the previous reading left `EMISSION_BURN_HOTKEY` untraced. It is a placeholder written as `winner_hotkey` when a defending champion wins and is resolved back to the real hotkey in `validator/scoring/tournaments.py`. `weights.py` rescales the three pools to fill the whole emission, agreeing with the docs that nothing is burned; `emission_balance.py`'s cap comment at the same commit still says anything above the 0.50 cap falls through to burn.

## Disagreements added, changed or resolved

- SN120 `scoring`: resolved (llms.txt now matches the code); new one recorded on the stale `score.py` header.
- SN120 `split`: resolved and removed.
- SN51 `split`: changed only by the second endpoint reading on 2026-09-22.
- SN56 `split`: changed; the burn hotkey is traced and the two code comments named.
