#!/usr/bin/env python3
"""V10 spend gate (bead c6m): same settle quantity as the submission path.

V10(receipts): committed = Σ COMMIT_COST over settled; total = committed +
LOSS_ALLOWANCE_USD (10.00). FAIL if total > 213.48. FAIL if any
settle_quantity is None. PAID_UNKNOWN counts at upper bound. Per-account:
any account > $200 FAILS (the 402 backstop fires before our gate; a sum-only
check is blind to the account about to be cut off).

SETTLE_FROM(r) = metadata.duration × INPUT_CHANNEL_COUNT, recomputed fresh
per receipt and compared to the stored settle_quantity: divergence FAILS.
Never the response's channel array (bills 2x while reporting 1), never the
pre-downmix count (double-counts the saving). NON_VACUOUS iff receipts
non-empty AND committed > 0 AND every stored quantity == fresh recompute.
Ceilings held, never re-derived: $193.04 all-dated-stereo, $201.83 all-235.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

HARD_STOP = 213.48
ACCOUNT_STOP = 200.0
LOSS_ALLOWANCE = 10.00
MIN_RATE = 0.0056


class V10Fail(Exception):
    pass


def commit_cost(billed_seconds, channels=1):
    return (billed_seconds * channels / 60.0) * MIN_RATE


def settle_from(receipt):
    return receipt["metadata_duration"] * receipt["input_channel_count"]


def v10(receipts, loss_allowance=LOSS_ALLOWANCE):
    if len(receipts) == 0:
        raise V10Fail("zero receipts: refusing vacuous PASS")
    for r in receipts:
        if r.get("settle_quantity") is None:
            raise V10Fail(f"{r.get('part')}: settle_quantity None (defaults to 0 rejected)")
        if r.get("metadata_duration") is None:
            raise V10Fail(f"{r.get('part')}: metadata_duration missing: nothing to recompute from")
        # Tolerance 1e-3 s: settle_quantity is stored at 3 dp. A ms is
        # $0.0000000933 of billing: asserting tighter manufactures findings.
        if abs(r["settle_quantity"] - settle_from(r)) > 1e-3:
            raise V10Fail(f"{r.get('part')}: stored {r['settle_quantity']} != fresh {settle_from(r)}")
    committed = sum(commit_cost(r["metadata_duration"], r["input_channel_count"])
                    for r in receipts if r.get("status") == "settled")
    unknown = sum(r.get("paid_unknown_upper", 0.0) for r in receipts
                  if r.get("paid_unknown"))
    # Per-account FIRST: the vendor's 402 backstop fires at $200 while the sum
    # can still look fine. A sum-first order reports the wrong gate.
    per_acct = {}
    for r in receipts:
        if r.get("status") == "settled":
            a = r.get("account", "primary")
            per_acct[a] = per_acct.get(a, 0.0) + commit_cost(r["metadata_duration"], r["input_channel_count"])
    for a, c in per_acct.items():
        if c > ACCOUNT_STOP:
            raise V10Fail(f"account {a} ${c:.2f} > ${ACCOUNT_STOP}: 402 backstop first")
    total = committed + loss_allowance + unknown
    if total > HARD_STOP:
        raise V10Fail(f"total ${total:.2f} > stop ${HARD_STOP}")
    non_vacuous = committed > 0
    if not non_vacuous:
        raise V10Fail("committed == 0: nothing evaluated")
    return {"committed": round(committed, 2), "total": round(total, 2),
            "per_account": {a: round(c, 2) for a, c in per_acct.items()},
            "verdict": "PASS"}


if __name__ == "__main__":
    print(json.dumps({"hard_stop": HARD_STOP, "account_stop": ACCOUNT_STOP}))
