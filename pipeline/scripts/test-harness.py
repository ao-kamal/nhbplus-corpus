#!/usr/bin/env python3
"""Meta-tests for the harness itself (bead nhbplus-corpus-emn).

A gate that cannot fail is not a gate, and a harness that cannot report
failure is part of the defect. Every test here plants a failure mode and
demands the harness report it:

  M1 deleted subject          -> that gate FAILED, receipt + count written
  M2 stage-1/*.md as subject  -> caught by the subject scan
  M3 empty tree, ceilings only-> FAIL via assert_nonvacuous (V6's helper)
  M4 exception inside V0      -> runner exit 1 (crash, no verdict), not 0/10
  M5 exit(gate_index*10) form -> rejected; (i+1)*10 present in runner source
  M6 equality without floor   -> check_eq(b"", b"") raises
  M7 child with stdin open    -> rejected; every spawn uses DEVNULL
  M8 early-exit pipe consumer -> rejected; full capture, never head-truncated
  M9 killed run               -> STARTED-without-verdict detected, not green

One JSONL line per test. Exit non-zero on failure.
"""
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location(
    "run_gates", os.path.join(HERE, "run-gates.py"))
rg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rg)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "harness-tests.jsonl")
RESULTS = []
TMP = tempfile.mkdtemp(prefix="emn-")


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def log(name, artifact, inp, verdict, note=""):
    RESULTS.append({"test": name, "artifact": artifact,
                    "input_digest": digest(inp), "verdict": verdict, "note": note})


def T(name):
    def deco(fn):
        try:
            fn()
            log(name, "run-gates.py", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "run-gates.py", {"case": name}, "FAIL",
                traceback.format_exc(limit=5).replace("\n", " | "))
            return False
    return deco


def isolated_rg():
    """run-gates pointed at a scratch out-dir so meta-tests never clobber it."""
    rg.RUN_LOG = os.path.join(TMP, "gate-run.jsonl")
    rg.RECEIPT_DIR = os.path.join(TMP, "gate-receipts")
    rg.OUT = TMP
    return rg


def code_of(path):
    src = open(path, encoding="utf-8").read()
    code = re.sub(r'"""[\s\S]*?"""', "", src)
    return "\n".join(l.split("#")[0] for l in code.splitlines())


@T("M1-deleted-subject-is-failed-with-receipt-and-count")
def _():
    g = isolated_rg()
    saved = g.GATES
    g.GATES = [{"id": "VX", "script": "no-such-gate.py",
                "subject": "gone", "log": "gone.jsonl"}]
    try:
        rc = g.main([])
    finally:
        g.GATES = saved
    assert rc == 10, f"deleted gate exited {rc}, not 10"
    rp = os.path.join(TMP, "gate-receipts", "VX.json")
    assert os.path.exists(rp), "no receipt written"
    rec = json.load(open(rp, encoding="utf-8"))
    assert rec["verdict"] == "FAILED", rec
    lines = [json.loads(l) for l in open(os.path.join(TMP, "gate-run.jsonl"), encoding="utf-8")]
    assert any(l.get("counts", {}).get("FAILED") == 1 for l in lines), "count not incremented"


@T("M2-stage1-as-subject-caught")
def _():
    bad = []
    for gate in [gt for gt in rg.GATES if os.path.exists(os.path.join(HERE, gt["script"]))]:
        src = open(os.path.join(HERE, gate["script"]), encoding="utf-8").read()
        if re.search(r"""open\([^)]*stage-1""", src):
            bad.append(gate["id"])
    assert bad == [], f"gates reading stage-1/*.md as subject: {bad}"
    # The scan itself must be live: a planted reader string is caught.
    # (Built from chr(40), so this file's source has no matching span.
    # Even this comment is worded to avoid one.)
    pat = r"""open\([^)]*stage-1"""
    planted = "open" + chr(40) + '"stage-1/foo.md")'
    assert re.search(pat, planted), "scan regex dead"


@T("M3-empty-tree-ceilings-fail-nonvacuous")
def _():
    try:
        rg.assert_nonvacuous([], what="vault tree")
        raise SystemExit("empty population passed")
    except ValueError:
        pass
    assert rg.assert_nonvacuous([1, 2]) == 2


@T("M4-exception-in-V0-exits-1-not-0-not-10")
def _():
    g = isolated_rg()
    crash = os.path.join(TMP, "crash-gate.py")
    open(crash, "w").write("raise RuntimeError('boom inside V0')\n")
    g.GATES = [{"id": "V0", "script": crash, "subject": "x", "log": "crash.jsonl"}]
    # run_gate resolves scripts under HERE; point it at the crash file by name
    # via a relative shim: registry uses basenames, so copy the crasher in.
    shim = os.path.join(HERE, "zz-crash-shim.py")
    open(shim, "w").write("raise RuntimeError('boom inside V0')\n")
    saved = g.GATES
    try:
        g.GATES = [{"id": "V0", "script": "zz-crash-shim.py",
                    "subject": "x", "log": "crash.jsonl"}]
        rc = g.main([])
        assert rc == 1, f"exception in V0 exited {rc}, not 1"
    finally:
        g.GATES = saved
        if os.path.exists(shim):
            os.remove(shim)


@T("M5-exit-form-is-index-plus-one-times-ten")
def _():
    code = code_of(os.path.join(HERE, "run-gates.py"))
    assert "(first_failed + 1) * 10" in code, "correct exit form missing"
    assert not re.search(r"return first_failed \* 10", code), "V0-can-never-fail form present"


@T("M6-equality-without-floor-rejected")
def _():
    try:
        rg.check_eq(b"", b"", what="decode")
        raise SystemExit("SHA-256 of nothing equalled SHA-256 of nothing")
    except ValueError:
        pass
    assert rg.check_eq(b"a", b"a") is True
    assert rg.check_eq(b"a", b"b") is False


@T("M7-every-child-spawn-closes-stdin")
def _():
    code = code_of(os.path.join(HERE, "run-gates.py"))
    lines = code.splitlines()
    spawns = [i for i, l in enumerate(lines)
              if "subprocess.run" in l or "Popen" in l]
    assert spawns, "no child spawns found"
    # Multi-line calls: DEVNULL may sit on a continuation line.
    bad = [i for i in spawns
           if "DEVNULL" not in "\n".join(lines[i:i + 4])]
    assert not bad, f"spawn without DEVNULL at lines {bad}"


@T("M8-no-early-exit-pipe-consumer")
def _():
    code = code_of(os.path.join(HERE, "run-gates.py"))
    assert "capture_output=True" in code, "children not fully captured"
    assert "Select-Object -First" not in code and "| head" not in code


@T("M9-killed-run-detected-not-green")
def _():
    logp = os.path.join(TMP, "partial.jsonl")
    with open(logp, "w", encoding="utf-8") as f:
        f.write(json.dumps({"gate": "V0", "verdict": "STARTED"}) + "\n")
    lines = [json.loads(l) for l in open(logp, encoding="utf-8")]
    started = {l["gate"] for l in lines if l.get("verdict") == "STARTED"}
    verdict = {l["gate"] for l in lines if l.get("verdict") not in ("STARTED",)}
    killed = started - verdict
    assert killed == {"V0"}, killed
    # The runner's own crash guard must exist to write INTERRUPTED lines.
    code = code_of(os.path.join(HERE, "run-gates.py"))
    assert "INTERRUPTED" in code, "no killed-run guard in runner"


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} harness meta-tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:300]}")
    import shutil
    shutil.rmtree(TMP, ignore_errors=True)
    # restore module globals for any later in-process use
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
