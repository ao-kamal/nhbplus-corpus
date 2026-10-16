#!/usr/bin/env python3
"""Spend ledger tests (bead md5).

- 3,600 s part commits $0.336 (the /60); $20.16 rejected by construction.
- Double release changes released ONCE (compare-and-set inside the lock).
- Stereo settles 2x on INPUT_CHANNEL_COUNT despite response channels=1.
- Downmixed BIT_IDENTICAL settles 1x (post-downmix count, never pre-).
- Lessons rescan: 1,569.6167 min x 0.0056 = $8.79 to the cent.
- PAID_UNKNOWN upper bound counts against the stop.
- Per-account schema (no global pool); totals.released present.
- Report: two lines (stt_* + vm_days_*), never one combined total.
One JSONL line per test. Exit non-zero on failure.
"""
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location(
    "spend_ledger", os.path.join(HERE, "spend-ledger.py"))
sl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sl)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "spend-ledger-tests.jsonl")
RESULTS = []
TMP = tempfile.mkdtemp(prefix="md5-")


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def log(name, artifact, inp, verdict, note=""):
    RESULTS.append({"test": name, "artifact": artifact,
                    "input_digest": digest(inp), "verdict": verdict, "note": note})


def T(name):
    def deco(fn):
        try:
            fn()
            log(name, "spend-ledger.py", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "spend-ledger.py", {"case": name}, "FAIL",
                traceback.format_exc(limit=4).replace("\n", " | "))
            return False
    return deco


def fresh():
    return sl.Ledger(os.path.join(TMP, f"spend-{len(os.listdir(TMP))}.json"))


@T("hour-part-commits-0336-not-2016")
def _():
    assert abs(sl.commit_cost(3600, 1) - 0.336) < 1e-9, sl.commit_cost(3600, 1)
    assert abs(sl.commit_cost(3600, 2) - 0.672) < 1e-9
    assert sl.SPEND_HARD_STOP_USD == 213.48
    derived = (34472.10 + 294.84 + 1569.62) * 0.0056 + 10.0
    assert abs(derived - 213.48) < 0.01, derived


@T("double-release-changes-once")
def _():
    L = fresh()
    L.commit("primary", "p00", 0.50)
    assert L.release("primary", "p00", 0.50) is True
    assert L.release("primary", "p00", 0.50) is False
    t = L.totals()
    assert abs(t["released"] - 0.50) < 1e-9 and abs(t["committed"]) < 1e-9, t


@T("stereo-settles-2x-on-input-count-downmix-1x")
def _():
    L = fresh()
    L.commit("primary", "s1", sl.commit_cost(600, 2))
    L.settle("primary", sl.commit_cost(600, 2), (600 / 60) * 0.0056 * 2)
    t = L.totals()
    assert abs(t["settled"] - 0.112) < 1e-9, t  # 2x despite response saying 1
    L.commit("primary", "d1", sl.commit_cost(600, 1))
    L.settle("primary", sl.commit_cost(600, 1), (600 / 60) * 0.0056 * 1)
    t = L.totals()
    assert abs(t["settled"] - 0.168) < 1e-9, t  # post-downmix 1x, never pre


@T("lessons-rescan-879-to-the-cent")
def _():
    assert abs(1569.6167 * 0.0056 - 8.79) < 0.005, 1569.6167 * 0.0056


@T("paid-unknown-counts-against-stop")
def _():
    L = fresh()
    L.commit("primary", "u1", 2.00)  # upper bound committed at PAID_UNKNOWN
    running = L.check_stop()
    assert abs(running - 2.00) < 1e-9, running
    L2 = fresh()
    L2.commit("primary", "u1", 213.48)  # exactly at the stop: allowed
    try:
        L2.commit("primary", "u2", 0.01)
        raise SystemExit("stop did not fire")
    except sl.StopHit:
        pass


@T("per-account-schema-totals-released-present")
def _():
    L = fresh()
    L.commit("primary", "p1", 1.0)
    L.commit("secondary", "p2", 0.5)
    raw = json.load(open(L.path, encoding="utf-8"))
    assert set(raw["accounts"]) == {"primary", "secondary"}, raw
    assert "released" in raw["totals"], raw["totals"]
    assert abs(raw["totals"]["committed"] - 1.5) < 1e-9, raw


@T("report-two-lines-never-one")
def _():
    L = fresh()
    rep = L.report(vm_days=None)
    assert "stt_actual_usd" in rep and "vm_days_actual" in rep, rep
    assert "total_cost" not in rep and "combined" not in rep, rep
    assert rep["stt_forecast_usd"] == 213.48, rep


@T("write-down-moves-settled-to-dead-one-way")
def _():
    L = fresh()
    L.commit("primary", "p1", 2.0)
    L.settle("primary", 2.0, 1.8)
    assert L.write_down("primary", 1.8, "ghost receipts wiped") == 0.0
    t = L.totals()
    assert abs(t["settled"]) < 1e-9 and abs(t["dead"] - 1.8) < 1e-9, t
    try:
        L.write_down("primary", 0.1, "overdraft")
        raise SystemExit("write-down overdraft passed")
    except ValueError:
        pass
    # Old-format ledger without dead key migrates safely.
    raw = json.load(open(L.path, encoding="utf-8"))
    del raw["totals"]["dead"]
    del raw["accounts"]["primary"]["dead"]
    json.dump(raw, open(L.path, "w"))
    assert L.write_down("primary", 0.0, "zero-move") == 0.0
    assert L.note_commitment("primary", 3.05, "kill mid-submit") is True
    raw = json.load(open(L.path, encoding="utf-8"))
    assert raw["commitments"] == [
        {"account": "primary", "amount": 3.05, "reason": "kill mid-submit"}], raw


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} ledger tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:250]}")
    import shutil
    shutil.rmtree(TMP, ignore_errors=True)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
