#!/usr/bin/env python3
"""V0 worklist integrity gate (bead nhbplus-corpus-ost).

Implements the bead formula verbatim: 344 rows, 344 unique handles, TWO
separate equalities (235 audio == manifest units, 109 docs == clean-names
documents), plus the targets.csv cross-check: the verdict follows the CSV,
never the disk. A tree where disk enumeration and targets.csv disagree must
still verdict on the CSV - otherwise the population was discovered.

NON_VACUOUS iff rows==344 and audio==235==manifest units and docs==109==
clean-names documents. A V0 that returns PASS on zero rows is the V9
failure with a different formula.
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))


class V0Fail(Exception):
    pass


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def check(scope=None, manifest=None, cleannames=None, csv_rows=None):
    """Returns (verdict, non_vacuous, detail). Raises V0Fail on any breach."""
    scope = scope if scope is not None else load(os.path.join("pipeline", "out", "scope-final.json"))
    manifest = manifest if manifest is not None else load(os.path.join("pipeline", "out", "manifest-v3.json"))
    cleannames = cleannames if cleannames is not None else load(os.path.join("pipeline", "out", "clean-names.json"))
    if csv_rows is None:
        with open(os.path.join(ROOT, "worklist", "targets.csv"), encoding="utf-8") as f:
            csv_rows = list(csv.DictReader(f))

    rows = scope["targets"]
    if len(rows) != 344:
        raise V0Fail(f"row count {len(rows)} != 344")
    handles = [r["handle"] for r in rows]
    if len(set(handles)) != 344:
        dupes = sorted({h for h in handles if handles.count(h) > 1})
        raise V0Fail(f"handle uniqueness: {len(set(handles))} unique, dupes {dupes[:5]}")

    audio = [r for r in rows if r["kind"] == "audio"]
    docs = [r for r in rows if r["kind"] in ("written_hand", "course_doc", "orphan_doc")]
    if len(audio) != 235:
        raise V0Fail(f"audio rows {len(audio)} != 235")
    units = {u["media"]["handle"] for u in manifest["units"]}
    if {r["handle"] for r in audio} != units:
        missing = units - {r["handle"] for r in audio}
        extra = {r["handle"] for r in audio} - units
        raise V0Fail(f"audio != manifest units: missing {sorted(missing)[:5]}, extra {sorted(extra)[:5]}")
    if len(docs) != 109:
        raise V0Fail(f"doc rows {len(docs)} != 109")
    cn_docs = {d["handle"] for d in cleannames["documents"]}
    if {r["handle"] for r in docs} != cn_docs:
        raise V0Fail("docs != clean-names documents")

    # The CSV cross-check: verdict follows the CSV.
    if len(csv_rows) != 344:
        raise V0Fail(f"targets.csv rows {len(csv_rows)} != 344")
    if {r["handle"] for r in csv_rows} != set(handles):
        raise V0Fail("targets.csv handle set != scope handle set")

    non_vacuous = (len(rows) == 344
                   and len(audio) == 235 == len(manifest["units"])
                   and len(docs) == 109 == len(cleannames["documents"]))
    if not non_vacuous:
        raise V0Fail("vacuous PASS refused: non-vacuity clause false")
    return ("PASS", True, "344 rows, sets equal, csv agrees, non-vacuous")


if __name__ == "__main__":
    try:
        print(json.dumps(check()))
    except V0Fail as e:
        print(json.dumps({"verdict": "FAIL", "reason": str(e)}))
        raise SystemExit(1)
