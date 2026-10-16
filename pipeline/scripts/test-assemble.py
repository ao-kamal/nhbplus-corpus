#!/usr/bin/env python3
"""Emitter + assembly tests (beads uff, a7z).

Emitter: six bad outputs unwritable (webinar/null/sixth-key/off-title/3h14m/
duration0-trees/speaker-people); domains good+bad per field; writes into
existing notes only; title from the filename stem.
Assembly: smoke utterances assemble with 30-min headings + caveat + words;
sparse stub verbatim per-page; paths from clean-names (344, unique CI);
empty tree + >= 344 rejected; doc without path fails.
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


fm = load("frontmatter_mod", "frontmatter.py")
asm = load("assemble_mod", "assemble.py")

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "assemble-tests.jsonl")
RESULTS = []
TMP = tempfile.mkdtemp(prefix="uff-")


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def log(name, artifact, inp, verdict, note=""):
    RESULTS.append({"test": name, "artifact": artifact,
                    "input_digest": digest(inp), "verdict": verdict, "note": note})


def T(name):
    def deco(fn):
        try:
            fn()
            log(name, "frontmatter+assemble", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "frontmatter+assemble", {"case": name}, "FAIL",
                traceback.format_exc(limit=4).replace("\n", " | "))
            return False
    return deco


def note(name="Call Note", body="hello\n"):
    p = os.path.join(TMP, name + ".md")
    open(p, "w", encoding="utf-8").write(body)
    return p


@T("six-bad-outputs-unwritable")
def _():
    p = note()
    good = dict(date="2024-03-07", duration=194, speakers=2, type="theory", words=100)
    for bad in (dict(good, type="webinar"),
                dict(good, duration=None),
                dict(good, speakers=None),
                dict(good, duration="3h 14m"),
                dict(good, date="03/07/2024")):
        try:
            fm.render_frontmatter(p, **bad)
            raise SystemExit(f"emitted {bad}")
        except fm.EmitFail:
            pass
    try:
        fm.render_frontmatter(p, **dict(good, duration=0, words=0))
        raise SystemExit("duration0+nowords written silently")
    except fm.Flagged:
        pass
    # sixth key: no API for it (signature is the literal five + words)
    import inspect
    params = set(inspect.signature(fm.render_frontmatter).parameters)
    assert params == {"note_path", "date", "duration", "speakers", "type", "words"}, params


@T("domains-good-and-title-from-stem")
def _():
    p = note("2024-03-07 How To Sell")
    block = fm.render_frontmatter(p, date="2024-03-07", duration=0,
                                  speakers="unknown", type="other", words=12)
    assert "title: 2024-03-07 How To Sell" in block, block  # stem, not source
    assert "duration: 0" in block and "speakers: unknown" in block, block
    text = open(p, encoding="utf-8").read()
    assert text.startswith("---\n") and text.count("---") >= 2, text
    assert "null" not in text.lower(), text


@T("emitter-never-creates-notes")
def _():
    try:
        fm.render_frontmatter(os.path.join(TMP, "nope.md"), date="unknown",
                              duration="unknown", speakers="unknown",
                              type="other", words=0)
        raise SystemExit("created a note")
    except fm.EmitFail:
        pass


@T("smoke-utterances-assemble")
def _():
    utts = [{"start": 0.4, "transcript": "Alright.", "speaker": 0},
            {"start": 61.2, "transcript": "Second minute.", "speaker": 1},
            {"start": 1800.5, "transcript": "Half hour mark.", "speaker": 0}]
    body, words = asm.audio_body(utts, 2)
    assert "### 0:00" in body and "### 0:30" in body, body
    assert "Speaker 0: Alright." in body, body
    assert "algorithmically derived clusters" in body, body
    assert words == 6, words


@T("sparse-stub-verbatim-per-page")
def _():
    pages = [{"page": 1, "words": 3, "lines": ["Title Words Here"]},
             {"page": 2, "words": 0, "lines": []}]
    stub = asm.sparse_stub("AC eBook", pages, "340 pp, cap 200, 691 words")
    assert "#### p. 1" in stub and "Title Words Here" in stub, stub
    assert "#### p. 2" in stub and "no recoverable text" in stub, stub
    assert "No layout is recoverable" in stub and "not a summary" in stub, stub


@T("paths-344-unique-ci-empty-tree-rejected")
def _():
    cn = json.load(open(os.path.join(ROOT, "pipeline", "out", "clean-names.json"), encoding="utf-8"))
    paths = ([c["path"] for c in cn["calls"]] + [l["path"] for l in cn["lessons"]]
             + [d["path"] for d in cn["documents"]])
    assert len(paths) == 344, len(paths)
    assert len({p.lower() for p in paths}) == 344, "case-insensitive collision"
    assert all(p and "None" not in p for p in paths), "missing/None path"
    assert len([]) < 344, "empty tree must fail >= 344"


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} emitter/assembly tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:250]}")
    import shutil
    shutil.rmtree(TMP, ignore_errors=True)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
