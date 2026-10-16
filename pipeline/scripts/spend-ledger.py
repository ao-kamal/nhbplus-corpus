#!/usr/bin/env python3
"""Single global spend ledger, per-account, one lock (bead md5).

LEDGER (VM): /data/nhb/_meta/spend.json, per account:
  {"accounts": {aid: {"committed","settled","lost","released"}}, "totals": {...}}
LOCK: spend.lock, flock held across READ-CHECK-WRITE. One writer: 16 workers
reading a stale total jointly overshoot, so every mutation below holds the
lock across the whole read-check-write.

  commit:  committed += cost
  settle:  committed -= cost; settled += actual
  release: committed -= cost; released += cost, compare-and-set INSIDE the
           flock on part_id: a reserved part released twice changes released
           ONCE, or the hard stop goes soft with no code appearing to change.
  lost:    committed -= cost; lost += actual

COMMIT_COST = (billed_seconds / 60) * (0.0043 + 0.0013). The /60 is load
bearing: without it a 3,600 s part commits $20.16 not $0.336 (60x).
SPEND_HARD_STOP_USD = $213.48 = (34472.10 + 294.84 + 1569.62) x 0.0056 + 10.00.
Quote ONE value: $213.48. PAID_UNKNOWN contributes its UPPER BOUND to the
running total: unknown money is spent money.

SETTLE_FROM = metadata.duration x INPUT_CHANNEL_COUNT (the AS-SUBMITTED
count in the same atomic write as sent; never the response array, never the
pre-downmix count). Billing uses DECODED duration, never a header.

Reports carry TWO lines, never one: stt_* from the ledger, vm_days_* from the
box. The VM-day VALUE is unmeasured (s15) and never asserted; its PRESENCE
as a separate field is. pipeline/bin/rescan.py rebuilds from receipts;
receipts win every conflict (single authority, named home for the sum).
"""
import json
import os
import time

try:
    import fcntl as _flock_mod
except ImportError:
    _flock_mod = None
try:
    import msvcrt as _msvcrt_mod
except ImportError:
    _msvcrt_mod = None

RATE = 0.0043
KEYTERM_RATE = 0.0013
MIN_RATE = RATE + KEYTERM_RATE
SPEND_HARD_STOP_USD = 213.48
DEFAULT_LEDGER = "/data/nhb/_meta/spend.json"

ZERO = {"committed": 0.0, "settled": 0.0, "lost": 0.0, "released": 0.0, "dead": 0.0}


class StopHit(Exception):
    pass


def commit_cost(billed_seconds, channels=1):
    return (billed_seconds * channels / 60.0) * MIN_RATE


def _blank():
    return {"accounts": {}, "totals": dict(ZERO), "released_parts": []}


def _load(path):
    if not os.path.exists(path):
        return _blank()
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _save(path, ledger):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(ledger, f, sort_keys=True)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


class Ledger:
    def __init__(self, path=None):
        self.path = path or os.environ.get("SPEND_LEDGER", DEFAULT_LEDGER)
        os.makedirs(os.path.dirname(os.path.abspath(self.path)), exist_ok=True)
        self.lock_path = self.path + ".lock"

    def _locked(self, fn):
        with open(self.lock_path, "w") as lock:
            if _flock_mod is not None:
                _flock_mod.flock(lock.fileno(), _flock_mod.LOCK_EX)
            elif _msvcrt_mod is not None:
                lock.seek(0)
                _msvcrt_mod.locking(lock.fileno(), _msvcrt_mod.LK_LOCK, 1)
            else:
                raise RuntimeError("no file locking available on this platform")
            try:
                ledger = _load(self.path)
                out = fn(ledger)
                _save(self.path, ledger)
                return out
            finally:
                if _flock_mod is not None:
                    _flock_mod.flock(lock.fileno(), _flock_mod.LOCK_UN)
                elif _msvcrt_mod is not None:
                    lock.seek(0)
                    _msvcrt_mod.locking(lock.fileno(), _msvcrt_mod.LK_UNLCK, 1)

    def _acct(self, ledger, aid):
        return ledger["accounts"].setdefault(aid, dict(ZERO))

    def totals(self):
        return _load(self.path)["totals"]

    def check_stop(self, ledger=None):
        t = (ledger or _load(self.path))["totals"]
        running = t["committed"] + t["settled"] + t["lost"]
        if running > SPEND_HARD_STOP_USD:
            raise StopHit(f"running ${running:.2f} > stop ${SPEND_HARD_STOP_USD}")
        return running

    def commit(self, aid, part_id, cost):
        def fn(ledger):
            self.check_stop(ledger)
            a = self._acct(ledger, aid)
            a["committed"] = round(a["committed"] + cost, 6)
            t = ledger["totals"]
            t["committed"] = round(t["committed"] + cost, 6)
            return self.check_stop(ledger)
        return self._locked(fn)

    def settle(self, aid, cost, actual):
        def fn(ledger):
            a = self._acct(ledger, aid)
            a["committed"] = round(a["committed"] - cost, 6)
            a["settled"] = round(a["settled"] + actual, 6)
            t = ledger["totals"]
            t["committed"] = round(t["committed"] - cost, 6)
            t["settled"] = round(t["settled"] + actual, 6)
        return self._locked(fn)

    def release(self, aid, part_id, cost):
        """Compare-and-set INSIDE the flock: second release is a no-op."""
        def fn(ledger):
            if part_id in ledger.get("released_parts", []):
                return False
            a = self._acct(ledger, aid)
            a["committed"] = round(a["committed"] - cost, 6)
            a["released"] = round(a["released"] + cost, 6)
            t = ledger["totals"]
            t["committed"] = round(t["committed"] - cost, 6)
            t["released"] = round(t["released"] + cost, 6)
            ledger.setdefault("released_parts", []).append(part_id)
            return True
        return self._locked(fn)

    def mark_lost(self, aid, cost, actual):
        def fn(ledger):
            a = self._acct(ledger, aid)
            a["committed"] = round(a["committed"] - cost, 6)
            a["lost"] = round(a["lost"] + actual, 6)
            t = ledger["totals"]
            t["committed"] = round(t["committed"] - cost, 6)
            t["lost"] = round(t["lost"] + actual, 6)
        return self._locked(fn)

    def write_down(self, aid, amount, reason):
        """Move settled money to dead: spent, no deliverable, never re-counted.
        The stop math (committed+settled+lost) no longer sees it; the dead
        column memorializes it with the reason. One-way: no write-up exists."""
        def fn(ledger):
            a = self._acct(ledger, aid)
            if amount > a["settled"] + 1e-9:
                raise ValueError(f"write_down {amount} > settled {a['settled']}")
            a["settled"] = round(a["settled"] - amount, 6)
            a["dead"] = round(a.get("dead", 0.0) + amount, 6)
            t = ledger["totals"]
            t["settled"] = round(t["settled"] - amount, 6)
            t["dead"] = round(t.get("dead", 0.0) + amount, 6)
            ledger.setdefault("write_downs", []).append(
                {"account": aid, "amount": amount, "reason": reason})
            return t["settled"]
        return self._locked(fn)

    def note_commitment(self, aid, amount, reason):
        """Memorialize committed money with no receipt (kill mid-submit: the
        bytes may have billed, the receipt never landed). It stays inside
        committed (counts against the stop); this entry explains WHY rescan
        cannot rebuild it. Informational: changes no total."""
        def fn(ledger):
            ledger.setdefault("commitments", []).append(
                {"account": aid, "amount": amount, "reason": reason})
            return True
        return self._locked(fn)

    def report(self, vm_days=None):
        t = self.totals()
        return {"stt_actual_usd": round(t["settled"] + t["lost"], 4),
                "stt_committed_usd": round(t["committed"], 4),
                "stt_forecast_usd": SPEND_HARD_STOP_USD,
                "vm_days_actual": vm_days,
                "ledger_totals": t}


if __name__ == "__main__":
    print(json.dumps({"hard_stop": SPEND_HARD_STOP_USD, "rate": MIN_RATE}))
