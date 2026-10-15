#!/usr/bin/env python3
"""
FINAL SCOPE. Every decision the operator made on 2026-10-15, resolved into one
work list of fetch targets. Nothing is fetched here; this is the contract the
runner reads and the plan is written against.

  A  audio scope      all 205 calls + all 42 bonus lesson videos   (single run)
  B  encoding         MP3 wherever an MP3 exists; the 88 MP4 siblings are
                      recorded as alternates and NEVER fetched
  C  companion docs   WRITTEN HAND ONLY - docx/pptx/xlsx. The 165 AI-summary
                      PDFs are OUT OF SCOPE.
  D  bonus courses    all 11
  E  orphans          both folders - Swipes + Templates, 36 files

One run. 247 audio units plus every in-scope document.
"""
import json, os, re, sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
OD   = os.path.join(HERE, "..", "out")
import os as _o
_s = _o.dup(1); _n = _o.open(_o.devnull, _o.O_WRONLY); _o.dup2(_n, 1)
try:
    import normalize as N
finally:
    _o.dup2(_s, 1); _o.close(_n); _o.close(_s)

man   = json.load(open(os.path.join(OD, "manifest-v3.json"), encoding="utf-8"))
units = man["units"]
docs  = [r for r in N.rows if not r["isfolder"] and r["ext"] not in ("mp3", "mp4", None)]
PH    = "https://mega.nz/folder/EzMk0Z4K#CrnHbM7tWaNtcByX0Ry_-Q"
url   = lambda h: f"{PH}/file/{h}"
gb    = lambda b: (b or 0) / 1073741824
hrs   = lambda s: (s or 0) / 3600
WRITTEN = {"docx", "pptx", "xlsx", "doc", "ppt", "xls"}

calls   = [u for u in units if u["kind"] == "calls"]
lessons = [u for u in units if u["kind"] == "lessons"]

# ---------------------------------------------------- call <-> written hand
byfo = defaultdict(list)
for r in docs: byfo[r["folder_handle"]].append(r)
def tokset(s): return set(re.findall(r"[a-z0-9]+", (s or "").casefold())) - {
    "nhb","the","call","theory","coaching","guest","ff","training","ai","summary"}

# ONE-TO-ONE greedy assignment per folder. A per-call best-pick handed the same
# .docx to several calls and reported 63 calls holding a written hand when only 44
# written-hand documents exist in call folders.
written_for = {}
for fh in sorted({u["folder_handle"] for u in calls}):
    pool = [r for r in byfo.get(fh, []) if r["ext"] in WRITTEN]
    us   = [u for u in calls if u["folder_handle"] == fh]
    pairs = []
    for i, u in enumerate(us):
        for j, r in enumerate(pool):
            ov = tokset(u["media"]["name"]) & tokset(r["name"])
            if len(ov) < 2 or not tokset(r["name"]): continue
            s = 30.0 * len(ov) / len(tokset(r["name"]))
            if s >= 25: pairs.append((s, i, j))
    pairs.sort(reverse=True)
    du, dd = set(), set()
    for s, i, j in pairs:
        if i in du or j in dd: continue
        du.add(i); dd.add(j); written_for[us[i]["id"]] = pool[j]
    for u in us: written_for.setdefault(u["id"], None)

# ------------------------------------------------------------- work targets
targets = []
for u in units:
    m = u["media"]
    targets.append({
        "kind": "audio", "unit": u["id"], "date": u["date"],
        "label": u["folder_label"], "type": u["type"], "topic": u["topic"],
        "handle": m["handle"], "url": m["url"], "ext": m["ext"],
        "bytes": m["bytes"], "dur_s": m["dur_s"],
        "alternates_not_fetched": [a["handle"] for a in m["alternates"]],
    })
    w = written_for.get(u["id"]) if u["kind"] == "calls" else None
    if w:
        targets.append({"kind": "written_hand", "unit": u["id"],
                        "label": u["folder_label"], "handle": w["handle"],
                        "url": url(w["handle"]), "name": w["name"],
                        "ext": w["ext"], "bytes": w["bytes"]})

# bonus-course companion documents (all of them - decision D takes all 11 courses)
lesson_fhs = {u["folder_handle"] for u in lessons}
for fh in sorted(lesson_fhs, key=lambda x: N.seednames.get(x, x)):
    nm = N.seednames.get(fh, fh)
    for r in byfo.get(fh, []):
        targets.append({"kind": "course_doc", "course": nm, "handle": r["handle"],
                        "url": url(r["handle"]), "name": r["name"],
                        "ext": r["ext"], "bytes": r["bytes"]})

# orphan folders - Swipes + Templates (decision E)
for fh in sorted(byfo, key=lambda x: N.seednames.get(x, x)):
    nm = N.seednames.get(fh, fh)
    if not re.search(r"swipe|template", nm, re.I): continue
    for r in byfo[fh]:
        targets.append({"kind": "orphan_doc", "folder": nm, "handle": r["handle"],
                        "url": url(r["handle"]), "name": r["name"],
                        "ext": r["ext"], "bytes": r["bytes"]})

# ------------------------------------------------------------------ totals
aud  = [t for t in targets if t["kind"] == "audio"]
docsT= [t for t in targets if t["kind"] != "audio"]
h    = sum(t["dur_s"] or 0 for t in aud) / 3600
ba   = sum(t["bytes"] or 0 for t in aud)
bd   = sum(t["bytes"] or 0 for t in docsT)

# integrity guards - these zeros have been false before
N_UNITS = len(units)
ids = [u["id"] for u in units]
assert len(set(ids)) == len(ids), (
    f"{len(ids)-len(set(ids))} colliding ids - two calls would share one vault note")
assert len(aud) == N_UNITS, f"{len(aud)} audio targets, expected {N_UNITS}"
assert len({t["handle"] for t in targets}) == len(targets), "a handle was targeted twice"
assert len([t for t in docsT if t["kind"] == "orphan_doc"]) == 36, "orphan count wrong"

by_kind = defaultdict(lambda: [0, 0])
for t in targets:
    by_kind[t["kind"]][0] += 1
    by_kind[t["kind"]][1] += t["bytes"] or 0

scope = {
    "decided": "2026-10-15 by operator. All five decisions. Single run.",
    "decisions": {
        "A_audio": "all 205 calls + all 42 bonus lesson videos, ONE run",
        "B_encoding": "MP3 wherever an MP3 exists; 88 MP4 siblings recorded as alternates, never fetched",
        "C_companion_docs": "WRITTEN HAND ONLY (docx/pptx/xlsx). 165 AI-summary PDFs OUT OF SCOPE.",
        "D_bonus_courses": "all 11",
        "E_orphans": "Swipes + Templates, all 36 files",
    },
    "totals": {
        "audio_units": len(aud), "calls": len(calls), "lessons": len(lessons),
        "audio_hours": round(h, 2), "audio_GB": round(gb(ba), 2),
        "documents": len(docsT), "document_GB": round(gb(bd), 3),
        "total_GB": round(gb(ba + bd), 2),
        "stt_forecast_usd": round(h * 60 * 0.0043, 2),
        "peak_disk_GB": round(max((t["bytes"] or 0) for t in aud) / 1073741824, 2),
    },
    "by_kind": {k: {"count": v[0], "GB": round(gb(v[1]), 3)} for k, v in sorted(by_kind.items())},
    "calls_without_written_hand": sum(1 for u in calls if not written_for.get(u["id"])),
    "mp4_alternates_never_fetched": sum(len(u["media"]["alternates"]) for u in units),
    "unreconciled": [
        "G0 §1 claims '84 calls (42%) have no written half'. Measured: "
        f"{sum(1 for u in calls if not written_for.get(u['id']))} of {len(calls)} "
        "have no written hand under decision C. The two figures are not reconciled "
        "and neither has been adopted over the other.",
        "G0 Q8 says five bonus courses; measured 11 carry video. The 42 videos / "
        "26.16 h figure agrees exactly with the independent bonuses census, so the "
        "video count is sound and the course count is a grouping-level difference.",
        "6 calls have no recoverable year from folder or name. Resolvable from the "
        "transcript once transcribed - flagged, not guessed.",
    ],
    "targets": targets,
}
p = os.path.join(OD, "scope-final.json")
json.dump(scope, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

T = scope["totals"]
print("=" * 70)
print("FINAL SCOPE - locked 2026-10-15")
print("=" * 70)
print(f"  {'AUDIO':<22}{T['audio_units']:>5} units  {T['audio_hours']:>8.2f} h  "
      f"{T['audio_GB']:>8.2f} GB")
print(f"  {'  calls':<22}{T['calls']:>5}")
print(f"  {'  bonus lessons':<22}{T['lessons']:>5}")
print(f"  {'DOCUMENTS':<22}{T['documents']:>5}         {'':>8}   {T['document_GB']:>8.3f} GB")
for k, v in scope["by_kind"].items():
    if k != "audio":
        print(f"    {k:<20}{v['count']:>5}         {'':>8}   {v['GB']:>8.3f} GB")
print(f"  {'TOTAL':<22}{T['audio_units']+T['documents']:>5}         {'':>8}   {T['total_GB']:>8.2f} GB")
print(f"\n  STT forecast            ${T['stt_forecast_usd']:.2f}")
print(f"  peak disk               {T['peak_disk_GB']:.2f} GB   (largest single file)")
print(f"  calls with NO written hand   {scope['calls_without_written_hand']} of {len(calls)}")
print(f"  MP4 alternates never fetched {scope['mp4_alternates_never_fetched']}")
print(f"\nWRITTEN {p}")