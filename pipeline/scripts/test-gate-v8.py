#!/usr/bin/env python3
"""V8 validator tests (bead 7w7): the shared six are REJECTED here.

Shared fixture with uff (files, since the validator reads notes):
webinar type, null duration, sixth key, off-stem title, 3h14m duration,
duration0+0words flagged. Plus: design doc without --- parsed as None and
fails non-vacuity; 343 notes fail the 344 floor; good notes pass.
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
    "gate_v8", os.path.join(HERE, "gate-v8.py"))
v8m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v8m)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "gate-v8-tests.jsonl")
RESULTS = []
TMP = tempfile.mkdtemp(prefix="7w7-")


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def log(name, artifact, inp, verdict, note=""):
    RESULTS.append({"test": name, "artifact": artifact,
                    "input_digest": digest(inp), "verdict": verdict, "note": note})


def T(name):
    def deco(fn):
        try:
            fn()
            log(name, "gate-v8.py", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "gate-v8.py", {"case": name}, "FAIL",
                traceback.format_exc(limit=4).replace("\n", " | "))
            return False
    return deco


def note(name, fm_lines, body="words here\n"):
    p = os.path.join(TMP, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write("---\n" + "".join(fm_lines) + "---\n" + body)
    return p


GOOD = ["title: Note\n", "date: 2024-03-07\n", "type: theory\n",
        "duration: 194\n", "speakers: 2\n"]


@T("shared-six-rejected")
def _():
    bads = [
        ["title: Note\n", "date: 2024-03-07\n", "type: webinar\n",
         "duration: 194\n", "speakers: 2\n"],
        ["title: Note\n", "date: 2024-03-07\n", "type: theory\n",
         "duration: null\n", "speakers: 2\n"],
        GOOD + ["speaker_labels: [0, 1]\n"],
        ["title: Other\n", "date: 2024-03-07\n", "type: theory\n",
         "duration: 194\n", "speakers: 2\n"],
        ["title: Note\n", "date: 2024-03-07\n", "type: theory\n",
         "duration: 3h 14m\n", "speakers: 2\n"],
        ["title: Note\n", "date: 2024-03-07\n", "type: theory\n",
         "duration: 0\n", "speakers: 1\n"],
    ]
    for i, fm in enumerate(bads):
        p = note(f"Note{i}.md" if i != 3 else "Note.md", fm,
                 body="" if i == 5 else "words here\n")
        wc = 0 if i == 5 else 2
        try:
            v8m.check_note(p, word_count=wc)
            raise SystemExit(f"bad fixture {i} passed")
        except v8m.V8Fail:
            pass


@T("design-doc-parses-None-floor-344")
def _():
    p = os.path.join(TMP, "design.md")
    open(p, "w").write("# Design\n\nNo delimiters here.\n")
    assert v8m.parse_frontmatter(p) is None
    try:
        v8m.v8([p] * 344)
        raise SystemExit("design docs passed")
    except v8m.V8Fail:
        pass
    good = [note(f"G{i}.md", [l.replace("Note", f"G{i}") for l in GOOD]) for i in range(344)]
    out = v8m.v8(good)
    assert out == {"notes": 344, "verdict": "PASS"}, out
    try:
        v8m.v8(good[:-1])
        raise SystemExit("343 passed the 344 floor")
    except v8m.V8Fail:
        pass


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} V8 tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:250]}")
    import shutil
    shutil.rmtree(TMP, ignore_errors=True)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
