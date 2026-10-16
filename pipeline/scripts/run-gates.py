#!/usr/bin/env python3
"""Gate runner - real services, no mocks, detailed logging (bead emn).

Runs every registered gate script to completion (never stops at the first
failure: two planted defects means two receipts), writes one JSONL verdict
line per gate plus a run summary, and exits mechanically:

  0               all registered gates passed
  10 * (i + 1)    gate i (0-based registry order) failed. NOT i * 10: that
                  form returns 0 for V0, and 0 is success, so V0 could never
                  report failure.
  1               crash: an exception escaped, no gate reached a verdict
  2               usage error, before any gate ran

Every gate failure writes its receipt (pipeline/out/gate-receipts/<ID>.json)
and increments its count. A killed run leaves STARTED lines without verdicts;
audit-run detects that shape and reports INTERRUPTED rather than green.

Child processes always get stdin closed (DEVNULL): ffmpeg, ffprobe and
mega-get read stdin by default and will consume the loop's input stream.
Equality between artifacts goes through check_eq(), which demands a FLOOR
(bytes decoded > 0 on both sides) before any hash comparison - SHA-256 of
nothing equalled SHA-256 of nothing once.
"""
import atexit
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "pipeline", "out")
RUN_LOG = os.path.join(OUT, "gate-run.jsonl")
RECEIPT_DIR = os.path.join(OUT, "gate-receipts")

# Registry order IS the gate index. Only implemented gates are listed;
# a registered gate whose script is missing FAILS (it does not go quiet).
GATES = [
    {"id": "V-0em", "script": "test-worklist.py",
     "subject": "worklist/targets.csv",
     "log": "worklist-tests.jsonl"},
    {"id": "V0", "script": "test-gate-v0.py",
     "subject": "worklist/targets.csv",
     "log": "gate-v0-tests.jsonl"},
    {"id": "V1", "script": "test-gate-v1.py",
     "subject": "disk-cap.py",
     "log": "gate-v1-tests.jsonl"},
    {"id": "V-zyg", "script": "test-fetch-pool.py",
     "subject": "fetch-pool.py",
     "log": "fetch-pool-tests.jsonl"},
    {"id": "V-geo", "script": "test-channels.py",
     "subject": "channels.py",
     "log": "channels-tests.jsonl"},
    {"id": "V-md5", "script": "test-spend-ledger.py",
     "subject": "spend-ledger.py",
     "log": "spend-ledger-tests.jsonl"},
    {"id": "V-z72", "script": "test-submit.py",
     "subject": "submit.py",
     "log": "submit-tests.jsonl"},
    {"id": "V4", "script": "test-gate-v4v5.py",
     "subject": "gate-v4v5.py",
     "log": "gate-v4v5-tests.jsonl"},
    {"id": "V5", "script": "test-gate-v4v5.py",
     "subject": "gate-v4v5.py",
     "log": "gate-v4v5-tests.jsonl"},
    {"id": "V-kgb", "script": "test-part-state.py",
     "subject": "part-state.py",
     "log": "part-state-tests.jsonl"},
    {"id": "V-06k", "script": "test-disk-cap.py",
     "subject": "disk-cap.py",
     "log": "disk-cap-tests.jsonl"},
    {"id": "V-dqh", "script": "test-extract-pdf.py",
     "subject": "extract-pdf.py",
     "log": "extract-pdf-tests.jsonl"},
    {"id": "V-5zb", "script": "test-extract-ooxml.py",
     "subject": "extract-ooxml.py",
     "log": "extract-ooxml-tests.jsonl"},
    {"id": "V-8pt", "script": "test-extract-misc.py",
     "subject": "extract-misc.py",
     "log": "extract-misc-tests.jsonl"},
    {"id": "V-emn", "script": "test-harness.py",
     "subject": "run-gates.py",
     "log": "harness-tests.jsonl"},
]


def digest_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def check_eq(a: bytes, b: bytes, what="artifact"):
    """Equality with a FLOOR. No floor -> reject, always."""
    if len(a) == 0 or len(b) == 0:
        raise ValueError(f"{what}: empty side ({len(a)},{len(b)}): refusing equality")
    return hashlib.sha256(a).hexdigest() == hashlib.sha256(b).hexdigest()


def assert_nonvacuous(population, what="population"):
    """A ceiling-only gate over an empty tree must FAIL, never pass vacuous.
    Every gate whose checks are all ceilings calls this on its subject
    population before verdicting. V6 lives or dies by it."""
    n = len(population)
    if n == 0:
        raise ValueError(f"{what}: empty subject population: refusing vacuous PASS")
    return n


def emit(line):
    with open(RUN_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")


_started = []


def _crash_guard():
    for g in _started:
        emit({"gate": g, "verdict": "INTERRUPTED",
              "note": "STARTED without verdict: run killed mid-gate"})


def run_gate(g):
    script = os.path.join(HERE, g["script"])
    _started.append(g["id"])
    emit({"gate": g["id"], "verdict": "STARTED", "script": g["script"],
          "script_digest": digest_file(script) if os.path.exists(script) else None})
    if not os.path.exists(script):
        return ("FAILED", f"registered script missing: {g['script']}", 1)
    log_path = os.path.join(OUT, g["log"])
    before = os.path.getmtime(log_path) if os.path.exists(log_path) else 0
    try:
        p = subprocess.run([sys.executable, script], capture_output=True,
                           stdin=subprocess.DEVNULL, cwd=ROOT, timeout=3600)
    except Exception as e:
        return ("CRASH", f"runner exception: {e}", -1)
    after = os.path.getmtime(log_path) if os.path.exists(log_path) else 0
    verdict_written = after > before
    if p.returncode == 0 and verdict_written:
        return ("PASS", p.stdout.decode()[-500:], 0)
    if p.returncode != 0 and verdict_written:
        return ("FAILED", p.stdout.decode()[-500:], p.returncode)
    return ("CRASH", f"no verdict from {g['script']}: exit={p.returncode} "
                     f"stderr={p.stderr.decode()[-300:]}", p.returncode)


def write_receipt(g, verdict, detail, counts):
    os.makedirs(RECEIPT_DIR, exist_ok=True)
    rp = os.path.join(RECEIPT_DIR, f"{g['id']}.json")
    counts[verdict] = counts.get(verdict, 0) + 1
    with open(rp, "w", encoding="utf-8") as f:
        json.dump({"gate": g["id"], "script": g["script"], "subject": g["subject"],
                   "verdict": verdict, "detail": detail[-800:],
                   "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, f, indent=1)
    return rp


def main(argv):
    if len(argv) > 1:
        print("usage: run-gates.py  (no arguments)", file=sys.stderr)
        return 2
    atexit.register(_crash_guard)
    if os.path.exists(RUN_LOG):
        os.remove(RUN_LOG)
    counts = {}
    first_failed = None
    for i, g in enumerate(GATES):
        verdict, detail, _code = run_gate(g)
        rp = write_receipt(g, verdict, detail, counts)
        emit({"gate": g["id"], "verdict": verdict, "receipt": rp,
              "counts": dict(counts)})
        if verdict == "CRASH":
            atexit.unregister(_crash_guard)
            emit({"gate": g["id"], "verdict": "CRASH", "receipt": rp})
            return 1
        if verdict == "FAILED" and first_failed is None:
            first_failed = i
    atexit.unregister(_crash_guard)
    summary = {"run": "complete", "gates": len(GATES), "counts": counts,
               "verdict": "PASS" if first_failed is None else "FAILED"}
    emit(summary)
    print(json.dumps(summary))
    if first_failed is None:
        return 0
    return (first_failed + 1) * 10


if __name__ == "__main__":
    sys.exit(main(sys.argv))
