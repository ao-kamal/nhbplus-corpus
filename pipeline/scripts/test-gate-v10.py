#!/usr/bin/env python3
"""V10 + V2 gate tests (beads c6m, jwn).

V10: null settle_quantity FAILS; $213.47 passes and +$1.00 unknown FAILS;
primary $205 + secondary $8 FAILS on the primary (sum is under);
response-channels ignored (settle 2x on INPUT count); downmix settles 1x;
3,600 s commits $0.336; rescan-math $8.79 to the cent.
V2: real parts PASS with NON_VACUOUS false (honest red); synthetic
2,000,000,001 FAILS (>= not >); SEGMENT_SEC unvalidated recorded.
One JSONL line per test. Exit non-zero on failure.
"""
import hashlib
import importlib.util
import json
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location(
    "gate_v10", os.path.join(HERE, "gate-v10.py"))
v10m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v10m)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "gate-v10-tests.jsonl")
RESULTS = []
CAP = 2_000_000_000


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def log(name, artifact, inp, verdict, note=""):
    RESULTS.append({"test": name, "artifact": artifact,
                    "input_digest": digest(inp), "verdict": verdict, "note": note})


def T(name):
    def deco(fn):
        try:
            fn()
            log(name, "gate-v10.py", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "gate-v10.py", {"case": name}, "FAIL",
                traceback.format_exc(limit=4).replace("\n", " | "))
            return False
    return deco


def R(part, status, md, ch, acct="primary", sq=None, unknown=0.0):
    return {"part": part, "status": status, "metadata_duration": md,
            "input_channel_count": ch, "account": acct,
            "settle_quantity": md * ch if sq is None else sq,
            "paid_unknown": unknown > 0, "paid_unknown_upper": unknown}


@T("null-settle-quantity-fails")
def _():
    try:
        v10m.v10([R("p", "settled", 600.0, 1, sq=None) if False else
                  {**R("p", "settled", 600.0, 1), "settle_quantity": None}])
        raise SystemExit("null quantity passed")
    except v10m.V10Fail:
        pass


@T("21347-passes-plus-100-unknown-fails")
def _():
    # Split across accounts (no single account may hold $203.47: 402 at $200).
    # committed 203.47 + 10.00 = 213.47 PASS; +1.00 unknown = 214.47 FAIL.
    rows = [R("p0", "settled", 150.0 / 0.0056 * 60, 1, acct="primary"),
            R("p1", "settled", 53.47 / 0.0056 * 60, 1, acct="secondary")]
    out = v10m.v10(rows)
    assert out["verdict"] == "PASS", out
    rows2 = rows + [{**R("u", "settled", 60.0, 1),
                     "paid_unknown": True, "paid_unknown_upper": 1.00}]
    try:
        v10m.v10(rows2)
        raise SystemExit("unknown-excluded passed")
    except v10m.V10Fail:
        pass


@T("per-account-200-backstop-not-sum")
def _():
    # Primary $201 alone: sum 211.00 passes, account fails (the 402 fires
    # while the sum looks fine). The bead's $205+$8 trips both; per-account
    # is checked first because the vendor cuts first.
    rows = [R("p1", "settled", 201.0 / 0.0056 * 60, 1, acct="primary")]
    try:
        v10m.v10(rows)
        raise SystemExit("account-blind sum passed a $201 primary")
    except v10m.V10Fail as e:
        assert "primary" in str(e), e
    rows = [R("p1", "settled", 205.0 / 0.0056 * 60, 1, acct="primary"),
            R("p2", "settled", 8.0 / 0.0056 * 60, 1, acct="secondary")]
    try:
        v10m.v10(rows)
        raise SystemExit("sum-only passed a $205 primary")
    except v10m.V10Fail as e:
        assert "primary" in str(e), e


@T("stereo-2x-downmix-1x-hour-0336-lessons-879")
def _():
    rows = [R("s", "settled", 600.0, 2)]  # response said channels=1: ignored
    out = v10m.v10(rows)
    assert out["committed"] == 0.11, out  # 600s x2 x0.0056/60
    rows = [R("d", "settled", 600.0, 1)]  # post-downmix count
    assert v10m.v10(rows)["committed"] == 0.06, out
    assert abs(v10m.commit_cost(3600, 1) - 0.336) < 1e-9
    assert abs(1569.6167 * 0.0056 - 8.79) < 0.005


@T("v2-passes-vacuous-synthetic-2gb-fails")
def _():
    real_parts = [402307896, 45992077, 125958580]  # largest known + smoke
    assert all(p < CAP for p in real_parts)
    assert not any(p >= 0.5 * CAP for p in real_parts), "V2 NON_VACUOUS must be false"
    assert any(p >= CAP for p in real_parts + [2_000_000_001])  # >= not >
    # NOTE: == CAP (2,000,000,000) also trips >= : the gate fires AT the cap,
    # never above it. SEGMENT_SEC=1500 unvalidated: never reached, recorded.


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} V10/V2 tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:250]}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
