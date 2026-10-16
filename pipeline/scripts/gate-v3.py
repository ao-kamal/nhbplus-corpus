#!/usr/bin/env python3
"""V3 STT contracts gate (bead d5p): ordering is the contract.

V3(receipts): every receipt names transport sync (no async path exists);
sent_ts < socket_open_ts STRICT (equal timestamps prove nothing: 1 s clock
granularity records both in the same second); http_status == 200 AND
response_complete (a 200 with complete=false is a truncated file, not a
transcript); NON_VACUOUS iff len(receipts) > 0 (green over zero receipts
evaluated nothing).

The kill/recovery branch (sent-then-die reads PAID_UNKNOWN, never queued,
never resubmitted) is implemented and tested in part-state.py (kgb); V3
asserts the receipt fields that make the branch decidable.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))


class V3Fail(Exception):
    pass


def check_receipt(r):
    if r.get("transport", "sync") != "sync":
        raise V3Fail(f"async transport on {r.get('part')}: plan no longer exists")
    if "sent_ts" not in r or "socket_open_ts" not in r:
        raise V3Fail(f"{r.get('part')}: sent/socket timestamps missing")
    if not r["sent_ts"] < r["socket_open_ts"]:
        raise V3Fail(f"{r.get('part')}: sent_ts {r['sent_ts']} >= socket_open_ts {r['socket_open_ts']}")
    if "http_status" not in r:
        raise V3Fail(f"{r.get('part')}: http_status absent (504/429/402 all 'a response')")
    if r["http_status"] != 200:
        raise V3Fail(f"{r.get('part')}: http {r['http_status']} != 200")
    if not r.get("response_complete"):
        raise V3Fail(f"{r.get('part')}: 200 but response_complete false (truncated)")
    return True


def v3(receipts):
    if len(receipts) == 0:
        raise V3Fail("zero receipts: V3 evaluates nothing, refusing vacuous PASS")
    for r in receipts:
        check_receipt(r)
    return {"receipts": len(receipts), "verdict": "PASS"}


if __name__ == "__main__":
    print(json.dumps({"gate": "V3", "non_vacuous": "len(receipts) > 0"}))
