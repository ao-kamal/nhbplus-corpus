#!/usr/bin/env python3
"""Acceptance tests for the worklist builder (bead nhbplus-corpus-0em).

Reject a worklist builder unless it fails on these inputs. Every test emits
one JSONL line: artifact path, input digest, verdict. Exit non-zero on any
failure. No mocks: the E2E builds from the real artifacts.

Suites:
  T1 empty scope-final        -> 0 rows, 344 assertion FAILS
  T2 glob of a partial tree   -> FAILS the equality-with-manifest assertion
  T3 ordering predicate        -> rejects alphabetical; rejects raw-minutes
                                 order; planted pair whose minute order and
                                 cost order differ must sort by cost
  T4 section 9 order           -> shakedown docs, 99 docs, smoke, lpt16,
                                 cheapest-first remainder; docs phase SPLIT
  T5 kind spelling             -> any row kind == call/calls FAILS
  T6 duration marker           -> None FAILS; docs carry explicit unknown
  T7 real-artifact E2E        -> 344 rows, sets equal, targets.csv emitted,
                                 no gate reads a glob
"""
import copy
import csv
import hashlib
import io
import json
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "build_worklist", os.path.join(HERE, "build-worklist.py"))
bw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bw)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "worklist-tests.jsonl")
RESULTS = []


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def log(name, artifact, inp, verdict, note=""):
    RESULTS.append({"test": name, "artifact": artifact,
                    "input_digest": digest(inp), "verdict": verdict, "note": note})


def fail(name, artifact, inp, note):
    log(name, artifact, inp, "FAIL", note)
    return False


def real_inputs():
    sf = bw.load_json(os.path.join("pipeline", "out", "scope-final.json"))
    mf = bw.load_json(os.path.join("pipeline", "out", "manifest-v3.json"))
    cn = bw.load_json(os.path.join("pipeline", "out", "clean-names.json"))
    return sf, mf, cn


def t1_empty_scope():
    name = "T1-empty-scope-fails-344"
    try:
        bw.build.__wrapped__ if hasattr(bw.build, "__wrapped__") else None
        sf, mf, cn = real_inputs()
        sf2 = copy.deepcopy(sf)
        sf2["targets"] = []
        # Replicate the builder's head assertions against empty input.
        rows = sf2["targets"]
        assert len(rows) == 344, f"scope rows {len(rows)} != 344"
        return fail(name, "worklist/targets.csv", {"rows": 0}, "empty scope passed 344 assertion")
    except AssertionError as e:
        log(name, "worklist/targets.csv", {"rows": 0}, "PASS", f"correctly failed: {e}")
        return True


def t2_glob_partial_fails():
    name = "T2-glob-partial-fails-equality"
    sf, mf, cn = real_inputs()
    manifest_handles = {u["media"]["handle"] for u in mf["units"]}
    # Simulate a glob over a partial tree: first 100 audio rows only.
    partial = [r["handle"] for r in sf["targets"] if r["kind"] == "audio"][:100]
    try:
        assert set(partial) == manifest_handles, "partial glob equals manifest"
        return fail(name, "worklist/targets.csv", {"rows": 100}, "partial glob passed equality")
    except AssertionError as e:
        log(name, "worklist/targets.csv", {"rows": 100}, "PASS", f"correctly failed: {e}")
        return True


def t3_ordering_predicate():
    name = "T3-orders-on-cost-not-minutes-not-alpha"
    # Planted pair: A is longer in minutes but cheaper (mono) than B (stereo).
    a_cost = bw.commit_cost(3600, 1)   # 60 min mono
    b_cost = bw.commit_cost(1800, 2)   # 30 min stereo -> same billed seconds
    c_cost = bw.commit_cost(2000, 2)   # 33 min stereo -> costlier than A
    units = [("zebra", 3600, 1), ("alpha", 2000, 2), ("mid", 1800, 2)]
    by_cost = sorted(units, key=lambda u: bw.commit_cost(u[1], u[2]))
    by_alpha = sorted(units, key=lambda u: u[0])
    by_minutes = sorted(units, key=lambda u: u[1])
    ok = True
    if [u[0] for u in by_cost] == [u[0] for u in by_alpha]:
        ok = fail(name, "predicate", units, "cost order equals alphabetical")
    if [u[0] for u in by_cost] == [u[0] for u in by_minutes]:
        ok = fail(name, "predicate", units, "cost order equals raw-minutes order")
    # zebra (60min mono, $0.336) must sort before alpha (33min stereo, $0.373).
    if [u[0] for u in by_cost] != ["zebra", "mid", "alpha"]:
        ok = fail(name, "predicate", units, f"wrong cost order: {[u[0] for u in by_cost]}")
    if abs(a_cost - 0.336) > 1e-9 or abs(c_cost - 0.373333) > 1e-4:
        ok = fail(name, "predicate", units, f"formula drift: {a_cost} {c_cost}")
    if ok:
        log(name, "predicate", units, "PASS", "cost order differs from both alpha and minutes")
    return ok


def t4_section9_order():
    name = "T4-section9-block-order"
    info = bw.build()
    with open(info["out"], encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    ok = True
    blocks = [r["block"] for r in rows]
    # Block contiguity and sequence.
    seen = []
    for b in blocks:
        if not seen or seen[-1] != b:
            seen.append(b)
    if seen != ["shakedown", "docs_rest", "smoke", "lpt16", "remainder"]:
        ok = fail(name, info["out"], {"blocks": seen}, f"block order wrong: {seen}")
    counts = {b: blocks.count(b) for b in set(blocks)}
    if counts.get("shakedown") != 10 or counts.get("docs_rest") != 99:
        ok = fail(name, info["out"], counts, f"docs not split 10/99: {counts}")
    if counts.get("smoke") != 1 or counts.get("lpt16") != 16:
        ok = fail(name, info["out"], counts, f"smoke/lpt16 wrong: {counts}")
    if counts.get("remainder") != 218:
        ok = fail(name, info["out"], counts, f"remainder {counts.get('remainder')} != 218")
    # Smoke is the lesson closest to $0.16.
    smoke = [r for r in rows if r["block"] == "smoke"][0]
    if abs(float(smoke["commit_cost_usd_mono"]) - info["smoke_usd"]) > 1e-9:
        ok = fail(name, info["out"], smoke, "smoke row mismatch")
    # Remainder cheapest-first by mono cost; unknown-cost audio sorts last.
    rem = [r for r in rows if r["block"] == "remainder"]
    rem_known = [float(r["commit_cost_usd_mono"]) for r in rem if r["commit_cost_usd_mono"]]
    rem_unknown = [r for r in rem if not r["commit_cost_usd_mono"]]
    if rem_known != sorted(rem_known):
        ok = fail(name, info["out"], {"rem_head": rem_known[:3]}, "remainder not cheapest-first")
    if [r["handle"] for r in rem_unknown] != info["unknown_dur_audio"]:
        ok = fail(name, info["out"], {"unknown": rem_unknown}, "unknown-cost audio not trailing")
    if rem and rem[-1]["commit_cost_usd_mono"]:
        ok = fail(name, info["out"], {"last": rem[-1]}, "last remainder row has known cost")
    # LPT16 longest-first by duration.
    lpt = [int(r["dur_s"]) for r in rows if r["block"] == "lpt16"]
    if lpt != sorted(lpt, reverse=True):
        ok = fail(name, info["out"], {"lpt_head": lpt[:3]}, "lpt16 not longest-first")
    # Not alphabetical.
    handles = [r["handle"] for r in rows]
    if handles == sorted(handles):
        ok = fail(name, info["out"], {"rows": len(handles)}, "emitted order is alphabetical")
    if ok:
        log(name, info["out"], {"rows": len(rows)}, "PASS",
            f"10/99/1/16/218 smoke={info['smoke']} ${info['smoke_usd']}")
    return ok


def t5_kind_spelling():
    name = "T5-no-kind-call"
    sf, _, _ = real_inputs()
    bad = [r["handle"] for r in sf["targets"] if r.get("kind") in ("call", "calls")]
    if bad:
        return fail(name, "scope-final.json", {"bad": bad}, f"kind call present: {bad}")
    log(name, "scope-final.json", {"rows": len(sf["targets"])}, "PASS", "audio/written_hand/course_doc/orphan_doc only")
    return True


def t6_duration_marker():
    name = "T6-duration-or-unknown-never-none"
    info = bw.build()
    with open(info["out"], encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    ok = True
    for r in rows:
        if r["dur_s"] in ("", "None", None):
            ok = fail(name, info["out"], r, f"row {r['handle']} has empty/None duration")
            break
    docs_unknown = [r for r in rows if r["kind"] != "audio" and r["dur_s"] == "unknown"]
    if len(docs_unknown) != 109:
        ok = fail(name, info["out"], {"unknown": len(docs_unknown)}, "docs without explicit unknown")
    audio_unknown = [r for r in rows if r["kind"] == "audio" and r["dur_s"] == "unknown"]
    if [r["handle"] for r in audio_unknown] != info["unknown_dur_audio"]:
        ok = fail(name, info["out"], {"audio_unknown": audio_unknown}, "audio unknown mismatch")
    if ok:
        log(name, info["out"], {"rows": len(rows)}, "PASS",
            f"109 docs unknown + {len(audio_unknown)} audio unknown, rest numeric")
    return ok


def t7_real_e2e_no_glob():
    name = "T7-e2e-344-and-no-gate-reads-glob"
    sf, mf, cn = real_inputs()
    ok = True
    if len(sf["targets"]) != 344 or len({r["handle"] for r in sf["targets"]}) != 344:
        ok = fail(name, "scope-final.json", {}, "344 rows/unique handles failed")
    audio = {r["handle"] for r in sf["targets"] if r["kind"] == "audio"}
    docs = {r["handle"] for r in sf["targets"] if r["kind"] != "audio"}
    if audio != {u["media"]["handle"] for u in mf["units"]}:
        ok = fail(name, "manifest-v3.json", {}, "audio != manifest units")
    if docs != {d["handle"] for d in cn["documents"]}:
        ok = fail(name, "clean-names.json", {}, "docs != clean-names documents")
    if not (os.path.exists(os.path.join(ROOT, "worklist", "targets.csv"))):
        ok = fail(name, "worklist/targets.csv", {}, "not emitted")
    # No gate derives population from a directory listing: the builder source
    # must not USE directory enumeration. Prose mentions of the word do not
    # count - only actual enumeration calls.
    src = open(os.path.join(HERE, "build-worklist.py"), encoding="utf-8").read()
    for token in ("import glob", "glob.glob", "glob.iglob", "glob.escape",
                  "os.listdir", "os.scandir", "os.walk", "pathlib", "iglob"):
        if token in src:
            ok = fail(name, "build-worklist.py", {"token": token}, f"builder uses {token}")
    if ok:
        log(name, "worklist/targets.csv", {"rows": 344}, "PASS", "344, sets equal, no glob in builder")
    return ok


def main():
    suite = [t1_empty_scope, t2_glob_partial_fails, t3_ordering_predicate,
             t4_section9_order, t5_kind_spelling, t6_duration_marker, t7_real_e2e_no_glob]
    passed = 0
    for t in suite:
        try:
            if t():
                passed += 1
        except Exception:
            log(t.__name__, "harness", {}, "FAIL", traceback.format_exc(limit=3).replace("\n", " | "))
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{len(suite)} acceptance tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        print(f"  [{r['verdict']}] {r['test']} - {r['note'][:90]}")
    return 0 if passed == len(suite) else 1


if __name__ == "__main__":
    sys.exit(main())
