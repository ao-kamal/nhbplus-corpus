#!/usr/bin/env python3
"""Acceptance tests for the per-part state machine (bead nhbplus-corpus-kgb).

Reject a state machine unless it fails on these inputs. Real filesystem in a
temp dir, no mocks. One JSONL line per test: artifact, input digest, verdict.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location(
    "part_state", os.path.join(HERE, "part-state.py"))
ps = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ps)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "part-state-tests.jsonl")
RESULTS = []
TMP = tempfile.mkdtemp(prefix="kgb-")


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def log(name, artifact, inp, verdict, note=""):
    RESULTS.append({"test": name, "artifact": artifact,
                    "input_digest": digest(inp), "verdict": verdict, "note": note})


def unit(name):
    d = os.path.join(TMP, name)
    os.makedirs(d, exist_ok=True)
    return d


def T(name):
    def deco(fn):
        try:
            fn()
            log(name, "part-state.py", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "part-state.py", {"case": name}, "FAIL",
                traceback.format_exc(limit=4).replace("\n", " | "))
            return False
    return deco


@T("kill-between-sent-and-socket-reads-paid-unknown")
def _():
    d = unit("kill")
    ps.admit(d, "p00")
    ps.reserve(d, "p00", 0.34, "abc", {"model": "nova-3"}, 1)
    ps.mark_sent(d)  # durable BEFORE the socket opens...
    # ...then the process dies before any byte leaves. Fresh instance:
    verdict, action = ps.recover(d)
    assert verdict == ps.PAID_UNKNOWN, verdict
    assert action == "operator_decides", action
    try:
        ps.submit(d)
        raise SystemExit("submit on PAID_UNKNOWN did not raise")
    except ps.PaidUnknown:
        pass
    st = ps.read_json(os.path.join(d, "state.json"))
    assert st["status"] != ps.QUEUED, "restart read queued after sent"


@T("interrupted-receipt-write-is-old-or-new-never-mixed")
def _():
    d = unit("torn")
    ps.admit(d, "p00")
    v1 = ps.reserve(d, "p00", 0.10, "h1", {"m": 1}, 1)
    # Kill between tmp write and replace: old receipt must survive intact.
    rp = os.path.join(d, "receipt.json")
    v2 = dict(v1, committed_usd=0.20)
    with open(rp + ".tmp", "wb") as f:
        f.write(json.dumps(v2, sort_keys=True).encode())
    got = ps.read_json(rp)  # replace never ran: still v1, fully parseable
    assert got["committed_usd"] == 0.10, got
    os.replace(rp + ".tmp", rp)
    got2 = ps.read_json(rp)
    assert got2["committed_usd"] == 0.20, got2


@T("deleted-response-complete-fails-the-machine")
def _():
    d = unit("schema")
    ps.admit(d, "p00")
    r = ps.reserve(d, "p00", 0.10, "h1", {"m": 1}, 1)
    bad = {k: v for k, v in r.items() if k != "response_complete"}
    ps.atomic_write_json(os.path.join(d, "receipt.json"), bad)
    try:
        ps.settle(d, 200, True)
        raise SystemExit("settle without response_complete did not fail")
    except ps.Refused:
        pass


@T("429-retries-with-backoff-never-lost")
def _():
    d = unit("r429")
    ps.admit(d, "p00")
    ps.reserve(d, "p00", 0.50, "h", {"m": 1}, 1)
    ps.mark_sent(d)
    st, action = ps.settle(d, 429, False)
    assert action == "retry_backoff", action
    assert st != ps.LOST, "429 recorded as lost"
    delays = [ps.backoff_delay_s(i) for i in range(8)]
    assert delays == [2, 4, 8, 16, 32, 60, 60, 60], delays


@T("402-routes-whole-part-to-secondary-lost-untouched")
def _():
    d = unit("r402")
    ps.admit(d, "p00")
    ps.reserve(d, "p00", 1.50, "h", {"m": 1}, 1)
    ps.mark_sent(d)
    st, action = ps.settle(d, 402, False)
    assert action == "reroute_secondary", action
    assert st != ps.LOST, "402 touched lost"
    s = ps.read_json(os.path.join(d, "state.json"))
    assert s["committed_usd"] == 0.0, s
    assert s.get("rerouted_to_secondary") is True, s
    # No part of one part split across accounts: single reroute flag.


@T("400-reprepares-and-resubmits-not-lost")
def _():
    d = unit("r400")
    ps.admit(d, "p00")
    ps.reserve(d, "p00", 0.30, "h", {"m": 1}, 1)
    ps.mark_sent(d)
    st, action = ps.settle(d, 400, False)
    assert action == "reprepare_resubmit", action
    assert st == ps.RESERVED, st
    # Resubmission path works from the re-prepared receipt.
    ps.mark_sent(d)
    st2, a2 = ps.settle(d, 200, True)
    assert st2 == ps.SETTLED, (st2, a2)


@T("504-timeout-truncated-is-paid-then-lost")
def _():
    for case, http, complete in [("504", 504, False), ("timeout", None, False),
                                 ("truncated", 200, False)]:
        d = unit(f"paid-{case}")
        ps.admit(d, "p00")
        ps.reserve(d, "p00", 0.40, "h", {"m": 1}, 1)
        ps.mark_sent(d)
        st, action = ps.settle(d, http, complete)
        assert st == ps.LOST, (case, st)
        assert action == "paid_unknown_then_lost", (case, action)
        s = ps.read_json(os.path.join(d, "state.json"))
        assert s.get("paid_unknown") is True, (case, s)


@T("unit-with-queued-part-emits-no-note")
def _():
    assert ps.unit_complete([ps.SETTLED, ps.SETTLED, ps.QUEUED], True) is False
    assert ps.unit_complete([ps.SETTLED, ps.SETTLED, ps.SETTLED], True) is True
    assert ps.unit_complete([ps.SETTLED, ps.LOST], True) is True
    assert ps.unit_complete([ps.SETTLED, ps.SETTLED], False) is False
    assert ps.unit_complete([], True) is False


@T("queued-replay-idempotent-no-commit-never-paid-unknown")
def _():
    d = unit("replay")
    s1 = ps.admit(d, "p00")
    s2 = ps.admit(d, "p00")  # crash replay: re-admit every queued part
    assert s1 == s2, (s1, s2)
    assert s2["committed_usd"] == 0.0, s2
    assert s2.get("paid_unknown", False) is False, s2
    verdict, action = ps.recover(d)
    assert verdict == ps.QUEUED and action == "replay_idempotent_no_commit"


@T("extras-merge-but-never-overwrite-load-bearing")
def _():
    import importlib.util as iu
    d = unit("extras")
    ps.admit(d, "p00")
    ps.reserve(d, "p00", 0.1, "h", {"m": 1}, 1)
    ps.mark_sent(d, extras={"sent_ts": 100.0, "transport": "sync"})
    r = ps.read_json(os.path.join(d, "receipt.json"))
    assert r["sent_ts"] == 100.0 and r["transport"] == "sync", r
    try:
        ps.mark_sent(d, extras={"status": "settled"})
        raise SystemExit("extras overwrote status")
    except ps.Refused:
        pass


@T("illegal-transitions-refused")
def _():
    d = unit("illegal")
    ps.admit(d, "p00")
    try:
        ps.mark_sent(d)
        raise SystemExit("mark_sent from queued did not refuse")
    except ps.Refused:
        pass
    try:
        ps.settle(d, 200, True)
        raise SystemExit("settle from queued did not refuse")
    except ps.Refused:
        pass
    ps.reserve(d, "p00", 0.1, "h", {"m": 1}, 1)
    try:
        ps.reserve(d, "p00", 0.1, "h", {"m": 1}, 1)
        raise SystemExit("double reserve did not refuse")
    except ps.Refused:
        pass


@T("402-stops-run-committed-intact-for-secondary")
def _():
    # E2E: two parts admitted; first hits 402. Run stops, its commit is
    # released for the secondary ledger (not charged, not lost), second part
    # stays queued with zero commit.
    bills = []
    for pid in ("p00", "p01"):
        d = unit(f"e2e-{pid}")
        ps.admit(d, pid)
    d0 = os.path.join(TMP, "e2e-p00")
    ps.reserve(d0, "p00", 1.10, "h", {"m": 1}, 1)
    ps.mark_sent(d0)
    st, action = ps.settle(d0, 402, False)
    assert action == "reroute_secondary", action
    r = ps.read_json(os.path.join(d0, "receipt.json"))
    assert r["status"] != ps.LOST and r["http_status"] == 402, r
    d1 = os.path.join(TMP, "e2e-p01")
    v, a = ps.recover(d1)
    assert (v, a) == (ps.QUEUED, "replay_idempotent_no_commit"), (v, a)
    bills.append(r["committed_usd"])
    assert bills == [1.10], bills  # receipt still names the amount rerouted


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} state-machine tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:200]}")
    shutil.rmtree(TMP, ignore_errors=True)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
