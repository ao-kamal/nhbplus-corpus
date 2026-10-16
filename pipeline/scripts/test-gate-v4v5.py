#!/usr/bin/env python3
"""V4/V5 gate tests (beads pcp, 724).

V4: pjFQiLQQ -> 0.0871 WARN (not header-relative 0.0954); sentinel manifest
excluded with PASS (polarity defect recorded); 0 manifest + no decoded FAIL;
12% divergence FAILS; 1 ms agreement PASSES; ledger writes decoded value.
V5: smoke edges 0.40/0.94 PASS; 55 s edge FAILS; negative tail PASSES;
empty FAILS named EMPTY; span_ratio UNSET recorded, never 0.
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
    "gate_v4v5", os.path.join(HERE, "gate-v4v5.py"))
g = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "gate-v4v5-tests.jsonl")
RESULTS = []


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def log(name, artifact, inp, verdict, note=""):
    RESULTS.append({"test": name, "artifact": artifact,
                    "input_digest": digest(inp), "verdict": verdict, "note": note})


def T(name):
    def deco(fn):
        try:
            fn()
            log(name, "gate-v4v5.py", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "gate-v4v5.py", {"case": name}, "FAIL",
                traceback.format_exc(limit=4).replace("\n", " | "))
            return False
    return deco


@T("pjfqilqq-00871-warn-not-00954")
def _():
    out = g.v4(4958.7, 5431.8 - 473.1 + 0, 5431.8)  # header ~ decoded here
    out = g.v4(4958.7, 5431.8, 5431.8)
    assert out["ratio"] == 0.0871, out
    assert out["warn"] is True, out
    assert out["authoritative"] == 5431.8, out  # ledger writes decoded


@T("string-manifest-zero-excluded-live-shape")
def _():
    # Live 2026-10-16: gate-inputs carries CSV strings. "0" must coerce and
    # exclude (else ratio 1.0000 FAIL); "10663" must coerce and include.
    out = g.v4("0", 5431.8, 5431.8)
    assert out["manifest_excluded"] is True and out["ratio"] == 0.0, out
    out = g.v4("10663", 10663.188, 10663.211)
    assert out["manifest_excluded"] is False, out
    assert g.is_sentinel_manifest("0") is True
    assert g.is_sentinel_manifest("10663") is False


@T("sentinel-manifest-excluded-pass-with-note")
def _():
    out = g.v4(2 * 1024 ** 3, 1436.9, 1436.885)
    assert out["manifest_excluded"] is True, out
    assert out["ratio"] < 0.02, out  # spread from header+decoded only


@T("zero-manifest-no-decoded-fails-12pct-fails-1ms-passes")
def _():
    try:
        g.v4(0, 100.0, None)
        raise SystemExit("no-decoded passed")
    except g.V4Fail:
        pass
    try:
        g.v4(100.0, 100.0, 112.0)  # spread 12/112 = 0.107
        raise SystemExit("12% passed")
    except g.V4Fail:
        pass
    out = g.v4(16556.207, 16556.208, 16556.207)  # wiUyTRZb 1 ms
    assert out["warn"] is False and out["ratio"] == 0.0, out


@T("smoke-edges-pass-55s-fails-negative-passes")
def _():
    out = g.v5(0.40, 1435.945, 1436.885, 5531)  # smoke: head 0.40 tail 0.94
    assert out == {"head_gap": 0.4, "tail_gap": 0.94, "basis": "wall-clock",
                   "span_ratio": "UNSET (MIN_SPAN_RATIO unsourced)"}, out
    try:
        g.v5(55.0, 1400.0, 1436.0, 5000)
        raise SystemExit("55 s head passed")
    except g.V5Fail as e:
        assert "EDGE" in str(e), e
    out2 = g.v5(0.5, 1437.885, 1436.885, 5000)  # negative tail: NOT failure
    assert out2["tail_gap"] == -1.0, out2
    try:
        g.v5(0.0, 0.0, 1436.0, 0)
        raise SystemExit("empty passed")
    except g.V5Fail as e:
        assert "EMPTY" in str(e), e


@T("silence-edges-pass-live-hnU2dCxTzb")
def _():
    # Live 2026-10-16: leader/trailer silence matching transcript edges.
    out = g.v5(24.735, 6476.505, 6478.272, 22084,
               speech_start=24.7041, speech_end=6476.6)
    assert out["basis"] == "speech" and out["head_gap"] == 0.03, out
    out = g.v5(2.32, 14280.555, 14301.461, 47896,
               speech_start=0.0, speech_end=14280.6)
    assert out["basis"] == "speech" and out["tail_gap"] == 0.05, out
    # 9zUSRTpC: trailing music bed, re-probe last word == transcript last word.
    out = g.v5(0.32, 10653.195, 10663.211, 33038,
               speech_start=0.0, speech_end=10653.2, speech_basis="re-probe")
    assert out["basis"] == "re-probe" and out["tail_gap"] == 0.01, out
    # Same inputs WITHOUT speech edges still FAIL wall-clock (strict default).
    try:
        g.v5(24.735, 6476.505, 6478.272, 22084)
        raise SystemExit("wall-clock lax without speech data")
    except g.V5Fail as e:
        assert "wall-clock" in str(e), e


@T("span-ratio-unset-never-zero")
def _():
    assert g.MIN_SPAN_RATIO is None
    import re
    src = open(os.path.join(HERE, "gate-v4v5.py"), encoding="utf-8").read()
    assert "MIN_SPAN_RATIO = None" in src
    assert "span_ratio < 0" not in src and "or 0" not in src.split("MIN_SPAN_RATIO = None")[1][:400]


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} V4/V5 tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:250]}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
