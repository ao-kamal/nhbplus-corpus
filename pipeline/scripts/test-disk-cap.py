#!/usr/bin/env python3
"""Acceptance tests for the sentinel-aware disk cap (bead nhbplus-corpus-06k).

- sentinel(2**30) True; sentinel(2**30+512) True; non-KiB-exact False.
- All 335 declared sizes through sentinel() -> 335 hits, zero kills.
- GiB-exact sub-population 77 (38 x 1 GiB, 39 x 2 GiB), 116.00/153.81 = 75.4%.
- max(1.10*declared, ...) present in disk-cap.py -> reject.
- else arm reported as exercised -> reject (recorded never-taken).
- A kill derived from a declared size -> reject, all 335.
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
    "disk_cap", os.path.join(HERE, "disk-cap.py"))
dc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dc)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "disk-cap-tests.jsonl")
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
            log(name, "disk-cap.py", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "disk-cap.py", {"case": name}, "FAIL",
                traceback.format_exc(limit=4).replace("\n", " | "))
            return False
    return deco


@T("sentinel-predicate-kib-not-gib")
def _():
    assert dc.sentinel(2 ** 30) is True
    # CORRECTED 2026-10-16: the bead text asserted sentinel(2**30 + 512) True,
    # but (2**30 + 512) % 1024 == 512, so it is NOT KiB-exact and the spec's
    # own predicate (b % 1024) == 0 returns False for it. The spec wins over
    # the bead: the True case needs a KiB-exact offset (+512 KiB), and the
    # literal bead example is recorded here as False, not True.
    assert dc.sentinel(2 ** 30 + 512) is False
    assert dc.sentinel(2 ** 30 + 512 * 1024) is True
    assert dc.sentinel(2 ** 30 + 1) is False
    assert dc.sentinel(0) is True
    # The wrong predicate: GiB granularity finds 77 and mislabels 258.
    mf = dc.load_manifest()
    prim = [u["media"]["bytes"] for u in mf["units"]]
    gib_granularity = sum(1 for b in prim if b % 2 ** 30 == 0)
    assert gib_granularity == 77, gib_granularity
    assert sum(1 for b in prim if dc.sentinel(b)) == 235


@T("census-335-kib-exact-zero-kills")
def _():
    c = dc.census()
    assert c["n_decl"] == 335, c
    assert c["kib_exact"] == 335, c
    assert c["scope_mismatches"] == [], c["scope_mismatches"]
    mf = dc.load_manifest()
    sizes = ([u["media"]["bytes"] for u in mf["units"]]
             + [a["bytes"] for u in mf["units"] for a in u["media"].get("alternates", [])])
    kills = [b for b in sizes if dc.kill_threshold(b) is not None]
    assert kills == [], f"kills fired on declared sizes: {kills[:5]}"


@T("gib-subpopulation-77-38-39-75pct")
def _():
    c = dc.census()
    assert c["gib_exact_primaries"] == 77, c
    assert c["gib1"] == 38, c
    assert c["gib2"] == 39, c
    assert abs(c["sent_gib"] - 116.0) < 1e-9, c
    assert abs(c["sent_pct"] - 75.4) < 0.05, c


@T("no-max-threshold-arm")
def _():
    # Strip prose before checking: the docstring NAMES the deleted arm so a
    # naive substring check fails on correct code (same trap as the glob
    # check in T7 of test-worklist.py). Only code counts.
    import re
    src = open(os.path.join(HERE, "disk-cap.py"), encoding="utf-8").read()
    code = re.sub(r'"""[\s\S]*?"""', "", src)
    code = "\n".join(l.split("#")[0] for l in code.splitlines())
    assert "1.10" not in code, "max(1.10*declared, ...) arm present: reject"
    assert "max(" not in code, "a max() threshold is present: reject"


@T("else-arm-never-taken-recorded")
def _():
    c = dc.census()
    mf = dc.load_manifest()
    sizes = ([u["media"]["bytes"] for u in mf["units"]]
             + [a["bytes"] for u in mf["units"] for a in u["media"].get("alternates", [])])
    nonsentinel = [b for b in sizes if not dc.sentinel(b)]
    assert nonsentinel == [], f"else arm reachable for {len(nonsentinel)} units"
    # The reachable quantum bands still exist as code, for a future corpus.
    assert dc.quantum_for(2 ** 30) == 512 * 1024 ** 2
    assert dc.quantum_for(2 * 2 ** 30) == 1024 ** 3
    assert dc.kill_threshold(2 ** 30 + 1) == 2 ** 30 + 1 + 0.5 * 512 * 1024 ** 2


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} disk-cap tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:250]}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
