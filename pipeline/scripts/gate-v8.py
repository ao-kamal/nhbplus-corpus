#!/usr/bin/env python3
"""V8 frontmatter validator: value DOMAINS, not a field count (bead 7w7).

The GATE (uff is the emitter; neither bead's evidence satisfies the other's
claim, deliberately). parse_frontmatter reads REAL --- delimiters from
emitted notes and nothing else: it never parses a design document, and a note
with no --- block returns None (which FAILS the non-vacuity clause rather
than passing silently).

Shared fixture with uff (six bad inputs): the emitter asserts it cannot
WRITE them; this validator asserts it REJECTS them. Same six, opposite claim.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

TYPES = ("theory", "guest", "coaching", "training", "mastermind", "other")
KEYS = {"title", "date", "type", "duration", "speakers"}


class V8Fail(Exception):
    pass


def parse_frontmatter(note_path):
    """Real --- delimiters only. No block -> None (fails non-vacuity)."""
    with open(note_path, encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fm = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            raise V8Fail(f"{note_path}: malformed frontmatter line {line!r}")
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip()
    return fm


def check_note(note_path, word_count=1):
    fm = parse_frontmatter(note_path)
    if fm is None:
        raise V8Fail(f"{note_path}: no frontmatter block")
    if set(fm) != KEYS:
        raise V8Fail(f"{note_path}: keys {sorted(fm)} != five")
    if not (re.fullmatch(r"\d{4}-\d{2}-\d{2}", fm["date"]) or fm["date"] == "unknown"):
        raise V8Fail(f"{note_path}: date {fm['date']!r}")
    if not (fm["duration"].isdigit() and int(fm["duration"]) >= 0) and fm["duration"] != "unknown":
        raise V8Fail(f"{note_path}: duration {fm['duration']!r}")
    if not (fm["speakers"].isdigit() and int(fm["speakers"]) >= 1) and fm["speakers"] != "unknown":
        raise V8Fail(f"{note_path}: speakers {fm['speakers']!r}")
    if fm["type"] not in TYPES:
        raise V8Fail(f"{note_path}: type {fm['type']!r}")
    stem = os.path.splitext(os.path.basename(note_path))[0]
    if fm["title"] != stem:
        raise V8Fail(f"{note_path}: title != stem")
    if fm["duration"] == "0" and word_count == 0:
        raise V8Fail(f"{note_path}: duration 0 with zero words (flagged)")
    if "None" in os.path.basename(note_path):
        raise V8Fail(f"{note_path}: None in filename")
    return True


def v8(note_paths, word_counts=None, expect_n=344):
    fronts = [parse_frontmatter(n) for n in note_paths]
    if not (all(f is not None for f in fronts) and len(note_paths) >= expect_n):
        raise V8Fail(f"NON_VACUOUS false: {len(note_paths)} notes, "
                     f"{sum(1 for f in fronts if f is not None)} parsed")
    for n in note_paths:
        wc = (word_counts or {}).get(n, 1)
        check_note(n, word_count=wc)
    return {"notes": len(note_paths), "verdict": "PASS"}


if __name__ == "__main__":
    print(json.dumps({"keys": sorted(KEYS), "types": list(TYPES)}))
