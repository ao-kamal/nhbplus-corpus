#!/usr/bin/env python3
"""
SCOPE DECISION + BONUS TRIAGE.

Operator decisions 2026-10-15:
  A  all CALLS. "i wanna triage bonus video first" -> the 42 bonus lesson videos
     and the orphan documents are NOT yet in scope. They are held open.
  B  MP3 where one exists.
  C  written hand only - the docx/pptx/xlsx written material, NOT the 165
     AI-summary PDFs.

So the call run is DECIDED and the bonus material is PENDING. This writes both
records: the locked scope as a machine-readable manifest the runner will read,
and a triage sheet for the 42 videos that are still open.
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
gb    = lambda b: (b or 0) / 1073741824
hrs   = lambda s: (s or 0) / 3600
WRITTEN = {"docx", "pptx", "xlsx", "doc", "ppt", "xls"}

calls   = [u for u in units if u["kind"] == "calls"]
lessons = [u for u in units if u["kind"] == "lessons"]

# --------------------------------------------------------------- locked scope
h_c  = sum(u["media"]["dur_s"] or 0 for u in calls) / 3600
b_c  = sum(u["media"]["bytes"] or 0 for u in calls)
# the written-hand companion for each call, under decision C
from collections import defaultdict as _dd
byfo = _dd(list)
for r in docs: byfo[r["folder_handle"]].append(r)
def tokset(s): return set(re.findall(r"[a-z0-9]+", (s or "").casefold())) - {
    "nhb","the","call","theory","coaching","guest","ff","training","ai","summary"}
def wpick(u):
    return written_for.get(u["id"])

# The assignment must be ONE-TO-ONE. A per-call best-pick happily handed the same
# .docx to several calls - it reported 63 calls holding a written hand when only
# 44 written-hand documents exist in call folders. Greedy global assignment per
# folder instead: best score first, each document consumed exactly once.
written_for = {}
for fh in sorted({u["folder_handle"] for u in calls}):
    pool = [r for r in byfo.get(fh, []) if r["ext"] in WRITTEN]
    us   = [u for u in calls if u["folder_handle"] == fh]
    pairs = []
    for i, u in enumerate(us):
        for j, r in enumerate(pool):
            ct = tokset(u["media"]["name"]); rt = tokset(r["name"])
            ov = ct & rt
            if len(ov) < 2 or not rt: continue
            s = 30.0 * len(ov) / len(rt)
            if s >= 25: pairs.append((s, i, j))
    pairs.sort(reverse=True)
    du, dd = set(), set()
    for s, i, j in pairs:
        if i in du or j in dd: continue
        du.add(i); dd.add(j); written_for[us[i]["id"]] = pool[j]
    for u in us:
        written_for.setdefault(u["id"], None)

scope_units = []
for u in calls:
    w = wpick(u)
    scope_units.append({
        "id": u["id"], "date": u["date"], "folder_label": u["folder_label"],
        "type": u["type"], "topic": u["topic"],
        "audio": {"handle": u["media"]["handle"], "url": u["media"]["url"],
                  "ext": u["media"]["ext"], "bytes": u["media"]["bytes"],
                  "dur_s": u["media"]["dur_s"]},
        "mp4_available": u["has_mp4"] and u["has_mp3"],
        "written_hand": ({"handle": w["handle"], "name": w["name"], "ext": w["ext"],
                          "bytes": w["bytes"],
                          "url": "https://mega.nz/folder/EzMk0Z4K#CrnHbM7tWaNtcByX0Ry_-Q/file/" + w["handle"]}
                         if w else None),
    })

n_w = sum(1 for s in scope_units if s["written_hand"])
scope = {
    "decided": "2026-10-15 by operator",
    "A_audio_scope": "205 CALLS. The 42 bonus lesson videos and the 36 orphan documents are HELD OPEN pending operator triage of the bonus material.",
    "B_encoding": "MP3 wherever an MP3 exists. The 88 MP4 siblings are recorded as alternates and are NEVER fetched. STT cost is identical either way; this saves 132.1 GB.",
    "C_companion_documents": "WRITTEN HAND ONLY - docx/pptx/xlsx. The 165 AI-summary PDFs are OUT OF SCOPE.",
    "D_bonus_courses": "PENDING - operator is triaging",
    "E_orphans": "PENDING - operator is triaging",
    "counts": {"calls": len(scope_units), "with_written_hand": n_w,
               "without_written_hand": len(scope_units) - n_w,
               "mp4_alternates_not_fetched": sum(1 for s in scope_units if s["mp4_available"])},
    "totals": {"hours": round(h_c, 2), "fetch_GB": round(gb(b_c), 2),
               "written_hand_GB": round(gb(sum(s["written_hand"]["bytes"]
                                     for s in scope_units if s["written_hand"])), 3),
               "stt_forecast_usd": round(h_c * 60 * 0.0043, 2)},
    "held_open": {"bonus_lesson_videos": len(lessons),
                  "orphan_documents": 36,
                  "ai_summary_pdfs_excluded": 165},
    "units": scope_units,
}
p = os.path.join(OD, "scope-decision.json")
json.dump(scope, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

print("=" * 74)
print("SCOPE — DECIDED")
print("=" * 74)
c = scope["counts"]; t = scope["totals"]
print(f"  calls in scope          : {c['calls']}")
print(f"  with a written hand     : {c['with_written_hand']}")
print(f"  with no written hand    : {c['without_written_hand']}")
print(f"  mp4 alternates NOT fetched : {c['mp4_alternates_not_fetched']}")
print(f"  audio                   : {t['hours']:.2f} h")
print(f"  fetch                   : {t['fetch_GB']:.2f} GB")
print(f"  written-hand documents  : {t['written_hand_GB']:.3f} GB")
print(f"  STT forecast            : ${t['stt_forecast_usd']:.2f}")
print(f"\n  HELD OPEN               : {scope['held_open']['bonus_lesson_videos']} bonus videos, "
      f"{scope['held_open']['orphan_documents']} orphan documents")
print(f"  EXCLUDED by choice C    : {scope['held_open']['ai_summary_pdfs_excluded']} AI-summary PDFs")
print(f"\nWRITTEN {p}")

# --------------------------------------------------------------- bonus triage
print("\n" + "=" * 74)
print("BONUS TRIAGE — 42 lesson videos across 12 folders. Not yet in scope.")
print("=" * 74)
course = defaultdict(list)
for u in lessons:
    course[u["folder_handle"]].append(u)
docs_by_fo = _dd(list)
for r in docs: docs_by_fo[r["folder_handle"]].append(r)

L = []
A = L.append
A("# Bonus material triage - held open pending your decision")
A("")
A("Nothing here is fetched. This is the pick list for decisions **D** and **E**.")
A("")
rows = []
for fh, us in course.items():
    nm = N.seednames.get(fh, fh)
    h = sum(u["media"]["dur_s"] or 0 for u in us) / 3600
    b = sum(u["media"]["bytes"] or 0 for u in us)
    nd = len(docs_by_fo.get(fh, []))
    rows.append((nm, len(us), h, gb(b), nd, fh, us))
rows.sort(key=lambda x: -x[2])

A(f"**{len(rows)} courses carry all {len(lessons)} lesson videos.** Three further")
A("folders hold documents and no video at all (`1. NHB+ Calls & Playlists`,")
A("`2. NHB+ Swipes`, `3. Templates`) - those are decision E, and cannot be judged")
A("from this sheet.")
A("")
A("| # | course | videos | audio | video GB | docs | STT |")
A("|---|---|---|---|---|---|---|")
for i, (nm, n, h, b, nd, fh, us) in enumerate(rows, 1):
    A(f"| {i} | {nm} | {n} | {h:.2f} h | {b:.2f} | {nd} | ${h*60*0.0043:.2f} |")
A("")
A(f"**all {len(rows)} courses: {len(lessons)} videos, "
  f"{sum(u['media']['dur_s'] or 0 for u in lessons)/3600:.2f} h, "
  f"${sum(u['media']['dur_s'] or 0 for u in lessons)/3600*60*0.0043:.2f} STT**")
A("")
A("Every course carries at least one video, so this list is judgeable by video.")
A("")
for i, (nm, n, h, b, nd, fh, us) in enumerate(rows, 1):
    A(f"### {i}. {nm}")
    A(f"")
    A(f"{n} video{'s' if n != 1 else ''} · {h:.2f} h · {b:.2f} GB · "
      f"${h*60*0.0043:.2f} STT · {nd} companion document{'s' if nd != 1 else ''}")
    A("")
    for u in sorted(us, key=lambda x: x["topic"]):
        m = re.match(r"(\d+(?:\.\d+)?)\s+(.*)", u["topic"])
        num, ti = (m.group(1), m.group(2)) if m else ("", u["topic"])
        A(f"- `{num}` **{ti}** — {(u['media']['dur_s'] or 0)//60} min, "
          f"{u['media']['ext']}, has written hand: {'yes' if any(d['ext'] in WRITTEN for d in docs_by_fo.get(fh,[])) else 'no'}")
    A("")

A("## Documents with no video and no call counterpart")
A("")
A("These cannot be triaged by video. They are decision E.")
A("")
A("| folder | files | size | contents |")
A("|---|---|---|---|")
for fh in sorted(docs_by_fo, key=lambda x: N.seednames.get(x, x)):
    nm = N.seednames.get(fh, fh)
    if not re.search(r"swipe|template", nm, re.I): continue
    rs = docs_by_fo[fh]
    A(f"| {nm} | {len(rs)} | {gb(sum(r['bytes'] or 0 for r in rs)):.2f} GB | "
      f"{', '.join(sorted({r['ext'] for r in rs}))} |")
A("")
A("4 (Swipes) + 32 (Templates) = **36 files**, which reconciles exactly with")
A("G0 §1's *\"36 PDFs, 406 MB\"*. Note 31 of the 32 Templates files are PDF and one")
A("is a ZIP. Extraction costs nothing: Q9 proved docx/xlsx/pptx unpack with the")
A("Python standard library alone — no converter, no office, no dependency.")
A("")
A("## How to answer")
A("")
A("Name the courses you want by number, and say yes or no on the 36 orphans.")
A("Everything not named stays out, and the call run does not wait on it.")

pt = os.path.join(OD, "BONUS-TRIAGE.md")
open(pt, "w", encoding="utf-8").write("\n".join(L) + "\n")
print(f"WRITTEN {pt}  ({len(L)} lines)")