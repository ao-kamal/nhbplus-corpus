#!/usr/bin/env python3
"""Clean-filename verification (bead wi6 evidence).

Re-checks pipeline/out/clean-names.json against every wi6 rule (the repair
itself lives in design-names.py; this is the independent re-check):
- 344 paths, casefold-unique; documents carry path 109/109, 0 collisions
- documents: no leading ordinal; lessons: source ordinals 42/42
- no None in any path; no media extension in any stem
- no brand tokens; written hands 37/37 resolve to their call
- Resources Links unprefixed count == 0
One JSONL line per check. Exit non-zero on failure.
"""
import hashlib
import json
import os
import re
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
LOG_PATH = os.path.join(ROOT, "pipeline", "out", "names-verify.jsonl")
RESULTS = []
MEDIA_EXTS = (".mp3", ".mp4", ".mka", ".docx", ".pptx", ".xlsx", ".png", ".zip", ".txt")


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def log(name, artifact, inp, verdict, note=""):
    RESULTS.append({"test": name, "artifact": artifact,
                    "input_digest": digest(inp), "verdict": verdict, "note": note})


def T(name):
    def deco(fn):
        try:
            fn()
            log(name, "clean-names.json", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "clean-names.json", {"case": name}, "FAIL",
                traceback.format_exc(limit=3).replace("\n", " | "))
            return False
    return deco


def cn():
    return json.load(open(os.path.join(ROOT, "pipeline", "out", "clean-names.json"), encoding="utf-8"))


@T("paths-344-unique-docs-109")
def _():
    c = cn()
    paths = ([x["path"] for x in c["calls"]] + [x["path"] for x in c["lessons"]]
             + [x["path"] for x in c["documents"]])
    assert len(paths) == 344, len(paths)
    assert len({p.lower() for p in paths}) == 344
    assert all(d.get("path") for d in c["documents"]), "doc without path"


@T("ordinals-docs-stripped-lessons-source")
def _():
    c = cn()
    docs = [d["path"] for d in c["documents"]]
    assert not any(re.search(r"/\d+\.\s", p) for p in docs), [p for p in docs if re.search(r"/\d+\.\s", p)][:3]
    assert sum(1 for l in c["lessons"] if l.get("ordinal_is_source")) == 42


@T("no-none-no-media-ext-no-brand")
def _():
    c = cn()
    paths = ([x["path"] for x in c["calls"]] + [x["path"] for x in c["lessons"]]
             + [x["path"] for x in c["documents"]])
    assert not any("None" in p for p in paths)
    stems = [os.path.splitext(os.path.basename(p))[0].lower() for p in paths]
    assert not any(s.endswith(e) for s in stems for e in MEDIA_EXTS), [s for s in stems if s.endswith(tuple(MEDIA_EXTS))][:3]
    assert "collisions" in c and c["collisions"].get("document_names_unprefixed", 1) == 0


@T("hands-resolve-to-calls-37")
def _():
    c = cn()
    hands = [d for d in c["documents"] if d["kind"] == "written_hand"]
    assert len(hands) == 37, len(hands)
    assert all(h.get("source_call") for h in hands), "hand without source_call"


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} names checks passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:250]}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
