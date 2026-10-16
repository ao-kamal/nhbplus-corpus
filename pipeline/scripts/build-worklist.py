#!/usr/bin/env python3
"""Build worklist/targets.csv - the ONLY work list. NEVER a glob.

Bead: nhbplus-corpus-0em. Spec: stage-1/stage-1-spec.md section 9.

Reads (declared population, then checked - never discovered from disk):
  pipeline/out/scope-final.json   344 targets
  pipeline/out/manifest-v3.json   235 units (audio truth)
  pipeline/out/clean-names.json   344 paths (calls 193 + lessons 42 + docs 109)

Emits:
  worklist/targets.csv            344 rows in spec section 9 order

Order (load-bearing, not cosmetic):
  1. shakedown   - 10 documents through egress first (free debugging front)
  2. docs_rest   - remaining 99 documents, alongside the audio lanes
  3. smoke       - one lesson-sized STT smoke test (~$0.16) before paid bulk
  4. lpt16       - 16 longest audio head-of-line (LPT fill, minimises makespan)
  5. remainder   - cheapest-first by COMMIT_COST mono estimate

COMMIT_COST (spec section 2.2):
  COMMIT_COST = (billed_seconds / 60) * (RATE + KEYTERM_RATE)
              = (dur_s * INPUT_CHANNEL_COUNT / 60) * (0.0043 + 0.0013)
At worklist time channels are unmeasured, so ordering uses the mono estimate
(channels=1). Ordering cost is NOT billed cost: the predicate orders on cost,
never on raw minutes, and never alphabetically. The acceptance test plants two
units whose minute order and cost order differ to prove it.
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))  # pipeline/scripts -> project root

RATE = 0.0043
KEYTERM_RATE = 0.0013
MIN_RATE = RATE + KEYTERM_RATE  # 0.0056 USD per billed minute

N_ROWS = 344
N_AUDIO = 235
N_DOCS = 109

# Shakedown subset: ~10 documents covering PDF text + PDF sparse (raster is
# proven empty: 0 documents, recorded not worked around), both sparse books,
# the ZIP, plus one docx / txt / png / pptx so every extractor route runs
# through egress before the paid bulk.
SHAKEDOWN_HANDLES = [
    "snViEZ6C",  # 2. AC eBook          - sparse book 1 (340pp, page_cap 200)
    "52c22T5D",  # AC_Book              - sparse book 2 (340pp, page_cap 200)
    "xyUQhDAa",  # Lazy Loading Code    - the 296 MiB ZIP (ElementTree exposure)
    "g2U0UDLb",  # 500-page-swipe-file  - page_cap text PDF, largest doc by words
    "46cEGZpD",  # 6. 7-Figure VSL      - least sparse doc; the one v1 dropped
    "1mcEVBLS",  # 5. $200,000 Ad Tmpl  - text PDF
    "s2MGiDJb",  # NHB+ Conv Audiences  - written_hand docx
    "YvNyGbqS",  # Sales Funnel Tmpl    - txt (Resources Links need s10.2 prefix)
    "guNkBLaZ",  # Pick Primary Color   - png: manifest entry only, 0 bytes
    "A2Mk1DQC",  # Background Graphics  - pptx: OOXML non-docx route
]

SMOKE_TARGET_USD = 0.16


def commit_cost_mono(dur_s):
    """Ordering-cost estimate pre-segmentation: mono channels."""
    return (dur_s / 60.0) * MIN_RATE


def commit_cost(dur_s, channels):
    """Billed-cost ordering predicate: cost, never raw minutes."""
    return (dur_s * channels / 60.0) * MIN_RATE


def load_json(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def build():
    sf = load_json(os.path.join("pipeline", "out", "scope-final.json"))
    mf = load_json(os.path.join("pipeline", "out", "manifest-v3.json"))
    cn = load_json(os.path.join("pipeline", "out", "clean-names.json"))

    rows = sf["targets"]
    assert len(rows) == N_ROWS, f"scope rows {len(rows)} != {N_ROWS}"
    handles = [r["handle"] for r in rows]
    assert len(set(handles)) == N_ROWS, "handles are not unique"

    # The spelling tripwire: scope-final has no kind called call/calls.
    bad_kinds = [r["handle"] for r in rows if r.get("kind") in ("call", "calls")]
    assert not bad_kinds, f"kind call/calls present: {bad_kinds}"

    audio_rows = [r for r in rows if r["kind"] == "audio"]
    doc_rows = [r for r in rows if r["kind"] in ("written_hand", "course_doc", "orphan_doc")]
    assert len(audio_rows) == N_AUDIO, f"audio {len(audio_rows)} != {N_AUDIO}"
    assert len(doc_rows) == N_DOCS, f"docs {len(doc_rows)} != {N_DOCS}"

    # Two separate equalities (V0 correction 2026-10-16): manifest units are
    # the 235 audio handles; clean-names documents are the 109 doc handles.
    manifest_handles = {u["media"]["handle"] for u in mf["units"]}
    assert {r["handle"] for r in audio_rows} == manifest_handles, "audio != manifest units"
    cn_doc_handles = {d["handle"] for d in cn["documents"]}
    assert {r["handle"] for r in doc_rows} == cn_doc_handles, "docs != clean-names documents"

    # Paths: every row gets one from clean-names; docs never carried a path.
    path_by_handle = {}
    for d in cn["documents"]:
        path_by_handle[d["handle"]] = d["path"]
    for c in cn["calls"]:
        path_by_handle[c["handle"]] = c["path"]
    for les in cn["lessons"]:
        path_by_handle[les["handle"]] = les["path"]
    missing_path = [h for h in handles if h not in path_by_handle]
    assert not missing_path, f"handles without path: {missing_path}"

    # Duration: a number for audio, explicit unknown for docs, never None.
    # MEASURED 2026-10-16: one audio row (dvcEDToK, mp4, 2 GiB sentinel bytes)
    # carries dur_s None, and doc rows carry no dur_s key at all. Per the bead,
    # every row gets either a duration or an explicit unknown marker - so None
    # and missing both map to unknown, LOUDLY (returned in the build report).
    # An unknown-cost audio unit cannot claim a cheapest-first position, so it
    # sorts after every known cost: unknown cost is treated as unbounded.
    unknown_dur_audio = sorted(
        r["handle"] for r in audio_rows if not isinstance(r.get("dur_s"), (int, float)))
    for r in rows:
        if r["kind"] == "audio":
            if not isinstance(r.get("dur_s"), (int, float)):
                r["dur_s"] = "unknown"
        else:
            r.setdefault("dur_s", "unknown")
            if r["dur_s"] is None:
                r["dur_s"] = "unknown"
    assert all(r["dur_s"] != "None" and r["dur_s"] is not None for r in rows)

    lesson_handles = {les["handle"] for les in cn["lessons"]}
    assert len(lesson_handles) == 42

    # Shakedown split: the docs phase must be SPLIT, not serialised in front
    # of the paid lanes while the VM burns.
    by_handle = {r["handle"]: r for r in rows}
    assert all(h in by_handle for h in SHAKEDOWN_HANDLES), "shakedown handle not in scope"
    shakedown = [by_handle[h] for h in SHAKEDOWN_HANDLES]
    rest_docs = [r for r in doc_rows if r["handle"] not in set(SHAKEDOWN_HANDLES)]
    assert len(rest_docs) == 99, f"rest docs {len(rest_docs)} != 99"

    # Smoke: the lesson minimizing |cost - $0.16|, over known durations only.
    lessons = [r for r in audio_rows
               if r["handle"] in lesson_handles and isinstance(r["dur_s"], (int, float))]
    assert lessons, "no lesson with known duration for smoke test"
    smoke = min(lessons, key=lambda r: abs(commit_cost_mono(r["dur_s"]) - SMOKE_TARGET_USD))

    # LPT16: 16 longest audio excluding the smoke unit, known durations only.
    pool = [r for r in audio_rows
            if r["handle"] != smoke["handle"] and isinstance(r["dur_s"], (int, float))]
    lpt16 = sorted(pool, key=lambda r: r["dur_s"], reverse=True)[:16]

    # Remainder: cheapest-first by COMMIT_COST mono estimate. Unknown-cost
    # units sort last - they cannot prove cheap, so they claim nothing.
    lpt_handles = {r["handle"] for r in lpt16}
    known_rest = [r for r in pool if r["handle"] not in lpt_handles]
    known_rest.sort(key=lambda r: commit_cost_mono(r["dur_s"]))
    unknown_rest = [r for r in audio_rows if not isinstance(r["dur_s"], (int, float))]
    remainder = known_rest + unknown_rest

    ordered = (
        [("shakedown", r) for r in shakedown]
        + [("docs_rest", r) for r in rest_docs]
        + [("smoke", smoke)]
        + [("lpt16", r) for r in lpt16]
        + [("remainder", r) for r in remainder]
    )
    assert len(ordered) == N_ROWS, f"ordered {len(ordered)} != {N_ROWS}"
    assert len({h for _, r in ordered for h in [r["handle"]]}) == N_ROWS

    out_dir = os.path.join(ROOT, "worklist")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "targets.csv")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["seq", "block", "handle", "kind", "unit", "path", "dur_s",
                    "commit_cost_usd_mono", "ext", "bytes"])
        for i, (block, r) in enumerate(ordered):
            dur = r["dur_s"]
            cost = (f"{commit_cost_mono(dur):.4f}"
                    if isinstance(dur, (int, float)) else "")
            by = r.get("bytes")
            w.writerow([i, block, r["handle"], r["kind"], r.get("unit", ""),
                        path_by_handle[r["handle"]], dur, cost,
                        r.get("ext", ""), "" if by is None else by])
    return {
        "rows": N_ROWS,
        "shakedown": len(shakedown),
        "docs_rest": len(rest_docs),
        "smoke": smoke["handle"],
        "smoke_usd": round(commit_cost_mono(smoke["dur_s"]), 4),
        "lpt16": len(lpt16),
        "remainder": len(remainder),
        "remainder_known": len(known_rest),
        "unknown_dur_audio": unknown_dur_audio,
        "out": out_path,
    }


if __name__ == "__main__":
    info = build()
    print(json.dumps(info))
