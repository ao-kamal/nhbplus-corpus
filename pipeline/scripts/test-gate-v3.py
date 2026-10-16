#!/usr/bin/env python3
"""V3 gate tests (bead d5p). Synthetic receipts; kill-branch covered by kgb
tests against the real state machine. One JSONL line per test."""
import hashlib
import importlib.util
import json
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location(
    "gate_v3", os.path.join(HERE, "gate-v3.py"))
v3m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v3m)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "gate-v3-tests.jsonl")
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
            log(name, "gate-v3.py", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "gate-v3.py", {"case": name}, "FAIL",
                traceback.format_exc(limit=4).replace("\n", " | "))
            return False
    return deco


def good(**kw):
    r = {"part": "p00", "transport": "sync", "sent_ts": 100.0,
         "socket_open_ts": 100.5, "http_status": 200, "response_complete": True}
    r.update(kw)
    return r


@T("async-inverted-equal-truncated-missing-all-fail")
def _():
    for bad in (good(transport="async"),
                good(sent_ts=101.0, socket_open_ts=100.5),
                good(sent_ts=100.5, socket_open_ts=100.5),
                good(response_complete=False)):
        try:
            v3m.v3([bad])
            raise SystemExit(f"passed on {bad}")
        except v3m.V3Fail:
            pass
    r = good()
    del r["http_status"]
    try:
        v3m.v3([r])
        raise SystemExit("missing http_status passed")
    except v3m.V3Fail:
        pass


@T("empty-receipts-never-pass")
def _():
    try:
        v3m.v3([])
        raise SystemExit("empty passed")
    except v3m.V3Fail:
        pass


@T("good-receipts-pass")
def _():
    out = v3m.v3([good(), good(part="p01")])
    assert out == {"receipts": 2, "verdict": "PASS"}, out


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} V3 tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:250]}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
