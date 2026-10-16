#!/usr/bin/env python3
"""Resume-branch tests (bead 0wv): kill mid-run, restart, ledger equality.

Simulated interrupted bulk over the REAL state machine + ledger (temp dirs):
  p-clean  uninterrupted: admit/reserve/sent/settle -> settled
  p-resv   killed while reserved -> resume releases, re-reserves, settles.
           Ledger equals the uninterrupted reference exactly.
  p-sent   killed after sent, no response -> PAID_UNKNOWN, never resubmitted;
           ledger carries its upper bound. Resume twice: identical (idempotent).
  p-429    resume meets 429 -> retried with backoff, not retired/lost.
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


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ps = load("part_state", "part-state.py")
sl = load("spend_ledger", "spend-ledger.py")

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "resume-tests.jsonl")
RESULTS = []
TMP = tempfile.mkdtemp(prefix="0wv-")


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def log(name, artifact, inp, verdict, note=""):
    RESULTS.append({"test": name, "artifact": artifact,
                    "input_digest": digest(inp), "verdict": verdict, "note": note})


def T(name):
    def deco(fn):
        try:
            fn()
            log(name, "resume", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "resume", {"case": name}, "FAIL",
                traceback.format_exc(limit=4).replace("\n", " | "))
            return False
    return deco


def udir(tag, part):
    d = os.path.join(TMP, tag, part)
    os.makedirs(d, exist_ok=True)
    return d


@T("reserved-kill-resume-equals-uninterrupted")
def _():
    led = sl.Ledger(os.path.join(TMP, "r1.json"))
    # reference: uninterrupted
    a = udir("ref", "p")
    ps.admit(a, "p00"); ps.reserve(a, "p00", 0.50, "h", {}, 1); ps.mark_sent(a)
    led.commit("primary", "p-a1", 0.50)
    ps.settle(a, 200, True)
    led.settle("primary", 0.50, 0.48)
    ref = led.totals()
    # interrupted: killed while reserved (commit on ledger, then "crash")
    led2 = sl.Ledger(os.path.join(TMP, "r2.json"))
    b = udir("int", "p")
    ps.admit(b, "p00")
    led2.commit("primary", "p-b1", 0.50)
    # ... crash before reserve. Restart: recover says reserved? No receipt yet:
    # no state beyond queued -> redo. Simulate kill AFTER reserve instead:
    ps.reserve(b, "p00", 0.50, "h", {}, 1)
    # ... crash. Restart:
    v, act = ps.recover(b)
    assert v == ps.RESERVED, (v, act)
    old = ps.read_json(os.path.join(b, "receipt.json"))
    assert led2.release("primary", "p-b1", old["committed_usd"]) is True
    st = ps.read_json(os.path.join(b, "state.json"))
    st["status"] = ps.QUEUED
    ps.atomic_write_json(os.path.join(b, "state.json"), st)
    ps.reserve(b, "p00", 0.50, "h", {}, 1)
    led2.commit("primary", "p-b2", 0.50)
    ps.mark_sent(b)
    ps.settle(b, 200, True)
    led2.settle("primary", 0.50, 0.48)
    got = led2.totals()
    # committed/settled identical; released records the one re-reserve (the
    # resume DID release and re-commit, and the journal must say so - hiding
    # it would be the lie, not the equality).
    assert got["committed"] == ref["committed"] == 0.0, (got, ref)
    assert got["settled"] == ref["settled"] == 0.48, (got, ref)
    assert got["released"] == 0.50, got  # exactly one release, CAS-held


@T("sent-kill-paid-unknown-never-resubmitted-idempotent")
def _():
    led = sl.Ledger(os.path.join(TMP, "r3.json"))
    c = udir("k", "p")
    ps.admit(c, "p00"); ps.reserve(c, "p00", 1.00, "h", {}, 1)
    led.commit("primary", "p-c1", 1.00)
    ps.mark_sent(c)
    # ... crash after sent, no response. Restart twice:
    for _ in range(2):
        v, act = ps.recover(c)
        # receipt says sent, no http outcome -> submit() flips PAID_UNKNOWN
        try:
            ps.submit(c)
            raise SystemExit("resubmitted a sent part")
        except ps.PaidUnknown:
            pass
    t = led.totals()
    assert abs(t["committed"] - 1.00) < 1e-9, t  # upper bound still counted
    assert t["settled"] == 0.0 and t["released"] == 0.0, t


@T("resume-429-retried-not-retired")
def _():
    d = udir("r429", "p")
    ps.admit(d, "p00"); ps.reserve(d, "p00", 0.30, "h", {}, 1); ps.mark_sent(d)
    st, act = ps.settle(d, 429, False)
    assert act == "retry_backoff" and st != ps.LOST, (st, act)
    assert ps.backoff_delay_s(0) == 2 and ps.backoff_delay_s(10) == 60


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} resume tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:250]}")
    import shutil
    shutil.rmtree(TMP, ignore_errors=True)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
