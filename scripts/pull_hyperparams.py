#!/usr/bin/env python3
"""Snapshot the chain hyperparameters for every subnet in the frozen target list.

Usage: .venv/bin/python scripts/pull_hyperparams.py [--netuids 120,64,107]
Writes data/hyperparams-<today>.json. Needs the bittensor SDK in .venv.

The mining program manifests cite this file at chain trust for the judges and
cadence fields: tempo, immunity period, commit-reveal, the weights rate limit.
"""
import argparse
import csv
import json
import signal
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
TODAY = date.today().isoformat()
KEYS = ["tempo", "immunity_period", "commit_reveal_weights_enabled", "commit_reveal_period", "weights_rate_limit",
        "max_validators", "min_allowed_weights", "max_weights_limit", "kappa", "bonds_moving_avg", "liquid_alpha_enabled",
        "registration_allowed", "target_regs_per_interval", "max_regs_per_block", "weights_version", "yuma_version",
        "owner_cut_enabled", "subnet_is_active"]


def targets():
    p = DATA / "subnets.csv"
    with p.open(encoding="utf-8") as fh:
        return [int(r["netuid"]) for r in csv.DictReader(fh)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--netuids", default="")
    a = ap.parse_args()
    netuids = [int(x) for x in a.netuids.split(",") if x.strip()] or targets()
    import bittensor as bt  # noqa
    signal.alarm(600)
    sub = bt.Subtensor(network="finney")
    out = {"pulled_at": TODAY, "network": "finney",
           "method": "bittensor SDK, Subtensor.subnets.subnet_hyperparameters(netuid); tempo and periods in blocks, one block is 12 seconds",
           "subnets": {}}
    for n in netuids:
        try:
            h = sub.subnets.subnet_hyperparameters(n)
            d = h.__dict__ if hasattr(h, "__dict__") else dict(h)
            out["subnets"][str(n)] = {k: d.get(k) for k in KEYS if k in d}
            print(f"  {n} tempo {out['subnets'][str(n)].get('tempo')} immunity {out['subnets'][str(n)].get('immunity_period')} "
                  f"commit_reveal {out['subnets'][str(n)].get('commit_reveal_weights_enabled')}", file=sys.stderr)
        except Exception as ex:  # noqa
            out["subnets"][str(n)] = {"error": str(ex)[:160]}
            print(f"  {n} ERR {str(ex)[:120]}", file=sys.stderr)
    path = DATA / f"hyperparams-{TODAY}.json"
    path.write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    print(f"wrote {path.relative_to(REPO)} for {len(netuids)} subnets", file=sys.stderr)


if __name__ == "__main__":
    main()
