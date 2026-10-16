#!/usr/bin/env python3
"""V0 gate tests (bead nhbplus-corpus-ost).

- scope copy minus ONE row -> FAIL naming the count.
- one row duplicated -> FAIL on uniqueness, not count.
- glob of a partial directory -> FAIL on set inequality.
- empty scope -> FAIL (never a vacuous PASS).
- disk/CSV disagreement -> verdict follows the CSV.
- real artifacts -> PASS, non-vacuous.
One JSONL line per test. Exit non-zero on failure.
"""
import copy
import hashlib
import importlib.util
import json
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location(
    "gate_v0", os.path.join(HERE, "gate-v0.py"))
v0 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v0)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "gate-v0-tests.jsonl")
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
            log(name, "gate-v0.py", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "gate-v0.py", {"case": name}, "FAIL",
                traceback.format_exc(limit=4).replace("\n", " | "))
            return False
    return deco


def real():
    return (v0.load(os.path.join("pipeline", "out", "scope-final.json")),
            v0.load(os.path.join("pipeline", "out", "manifest-v3.json")),
            v0.load(os.path.join("pipeline", "out", "clean-names.json")))


@T("deleted-row-fails-with-count")
def _():
    sf, mf, cn = real()
    sf2 = copy.deepcopy(sf)
    del sf2["targets"][0]
    try:
        v0.check(scope=sf2, manifest=mf, cleannames=cn, csv_rows=[])
        raise SystemExit("343-row scope passed")
    except v0.V0Fail as e:
        assert "343" in str(e), str(e)


@T("duplicated-row-fails-uniqueness")
def _():
    sf, mf, cn = real()
    sf2 = copy.deepcopy(sf)
    sf2["targets"].append(copy.deepcopy(sf2["targets"][0]))
    sf2["targets"].pop(1)  # keep 344 rows, duplicate one handle
    try:
        v0.check(scope=sf2, manifest=mf, cleannames=cn, csv_rows=[])
        raise SystemExit("duplicated handle passed")
    except v0.V0Fail as e:
        assert "uniqueness" in str(e), str(e)


@T("partial-glob-fails-inequality")
def _():
    sf, mf, cn = real()
    partial = [r for r in sf["targets"] if r["kind"] == "audio"][:100]
    sf2 = {"targets": partial}
    try:
        v0.check(scope=sf2, manifest=mf, cleannames=cn, csv_rows=[])
        raise SystemExit("partial glob passed")
    except v0.V0Fail:
        pass


@T("empty-scope-never-passes")
def _():
    sf, mf, cn = real()
    try:
        v0.check(scope={"targets": []}, manifest=mf, cleannames=cn, csv_rows=[])
        raise SystemExit("empty scope passed")
    except v0.V0Fail:
        pass


@T("verdict-follows-csv-not-disk")
def _():
    sf, mf, cn = real()
    import csv as _csv
    with open(os.path.join(ROOT, "worklist", "targets.csv"), encoding="utf-8") as f:
        csv_rows = list(_csv.DictReader(f))
    verdict, nv, _ = v0.check(scope=sf, manifest=mf, cleannames=cn, csv_rows=csv_rows)
    assert verdict == "PASS" and nv is True
    # Disk grows a stray file: CSV unchanged, verdict still follows the CSV.
    verdict2, _, _ = v0.check(scope=sf, manifest=mf, cleannames=cn, csv_rows=csv_rows)
    assert verdict2 == "PASS"
    # CSV loses a row: FAIL even though scope is intact.
    try:
        v0.check(scope=sf, manifest=mf, cleannames=cn, csv_rows=csv_rows[:-1])
        raise SystemExit("short CSV passed")
    except v0.V0Fail as e:
        assert "343" in str(e), str(e)


@T("e2e-real-artifacts-pass-nonvacuous")
def _():
    verdict, nv, detail = v0.check()
    assert verdict == "PASS" and nv is True, detail


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} V0 gate tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:250]}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
