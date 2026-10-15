#!/usr/bin/env python3
"""
SELECTION INVENTORY. The operator picks the files; this is what they pick from.

Scoped by an operator instruction 2026-10-15: "I need to actually pick the files
that we make it into... we need to know exactly what files we are getting before
we proceed."

So this does NOT decide. It presents every file grouped into DECISION UNITS, with
what each choice costs in hours, bytes and dollars. A 709-row file list is not a
reviewable artefact; four decisions are.

Decisions surfaced here:
  A  audio scope      - which calls / lessons
  B  encoding         - existing MP3 vs remuxed MP4, per call
  C  bonuses          - which of the lesson courses, and which FORMAT where a
                        module exists in more than one
  D  companion PDFs  - in-corpus pairings and the orphans with no call
"""
import glob, json, os, re, sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
OD   = os.path.join(HERE, "..", "out")

# reuse the verified normaliser rather than re-deriving it a second time
import normalize as N

rows = N.rows
seednames = N.seednames
media = [r for r in rows if not r["isfolder"] and r["ext"] in ("mp3", "mp4")]
docs  = [r for r in rows if not r["isfolder"] and r["ext"] not in ("mp3", "mp4")]

hrs = lambda s: (s or 0) / 3600
gb  = lambda b: (b or 0) / 1073741824

print("=" * 74)
print("INVENTORY - what is in the share, grouped by what you have to decide")
print("=" * 74)

# ---------------------------------------------------------------- inventory
byext = defaultdict(lambda: [0, 0, 0])          # count, bytes, seconds
for r in rows:
    if r["isfolder"]: continue
    e = r["ext"] or "(none)"
    byext[e][0] += 1
    byext[e][1] += r["bytes"] or 0
    byext[e][2] += r["dur_s"] or 0
print(f"\nrows captured {len(rows)}   media {len(media)}   documents {len(docs)}\n")
print(f"  {'ext':<10} {'files':>6} {'GB':>9} {'hours':>8}")
for e in sorted(byext, key=lambda x: -byext[x][1]):
    c, b, s = byext[e]
    print(f"  {e:<10} {c:>6} {gb(b):>9.2f} {hrs(s):>8.2f}")

# ------------------------------------------------- DECISION B: encoding pairs
print("\n" + "=" * 74)
print("DECISION B - the 88 calls that exist as BOTH an MP3 and an MP4")
print("=" * 74)
pairs = defaultdict(lambda: {"mp3": None, "mp4": None})
for r in media:
    k = (r["folder_handle"], N.call_date(r["name"]), N.topic_key(r["name"]))
    pairs[k]["mp3" if r["ext"] == "mp3" else "mp4"] = r
both = [p for p in pairs.values() if p["mp3"] and p["mp4"]]
h_mp3 = sum(p["mp3"]["dur_s"] or 0 for p in both) / 3600
b_mp3 = sum(p["mp3"]["bytes"] or 0 for p in both)
b_mp4 = sum(p["mp4"]["bytes"] or 0 for p in both)
print(f"  {len(both)} calls have both encodings.")
print(f"\n  {'choose':<26} {'audio h':>8} {'fetch GB':>9} {'STT $':>8} {'quality':>22}")
print(f"  {'MP3 (recommended)':<26} {h_mp3:>8.2f} {gb(b_mp3):>9.2f} "
      f"{h_mp3*60*0.0043:>8.2f} {'lower bitrate':>22}")
print(f"  {'MP4 remuxed to .m4a':<26} {h_mp3:>8.2f} {gb(b_mp4):>9.2f} "
      f"{h_mp3*60*0.0043:>8.2f} {'higher bitrate':>22}")
print(f"\n  STT cost is IDENTICAL either way - Deepgram bills audio minutes, not bytes.")
print(f"  You are choosing source quality vs {gb(b_mp4)-gb(b_mp3):.1f} GB of download.")
print(f"  Verified: transcribing the same call from each gives near-identical text")
print(f"  (37027w/22spk from mp3 vs 36963w/21spk from mp4).")

# ------------------------------------------- DECISION C: multi-format modules
print("\n" + "=" * 74)
print("DECISION C - documents that exist in MORE THAN ONE FORMAT")
print("=" * 74)
OFFICE = {"docx", "pptx", "xlsx", "doc", "ppt", "xls"}
by_stem = defaultdict(list)
for r in docs:
    stem = re.sub(r"[\s_]+", " ", re.sub(r"\.[A-Za-z0-9]{1,5}$", "", r["name"])).strip().casefold()
    by_stem[(r["folder_handle"], stem)].append(r)
multi = {k: v for k, v in by_stem.items() if len({r["ext"] for r in v}) > 1}
print(f"  document groups: {len(by_stem)}")
print(f"  groups spanning >1 FORMAT: {len(multi)}   <- these need your pick\n")
fmt_pairs = defaultdict(int)
for k, v in multi.items():
    fmt_pairs[tuple(sorted({r["ext"] for r in v}))] += 1
for combo, n in sorted(fmt_pairs.items(), key=lambda x: -x[1]):
    print(f"    {' + '.join(combo):<24} {n:>4} groups")
print("\n  sample groups (folder / stem / formats / sizes):")
shown = 0
for k, v in sorted(multi.items(), key=lambda x: seednames.get(x[0][0], "")):
    if shown >= 10: break
    shown += 1
    print(f"    {seednames.get(k[0], k[0])[:26]:<26} {k[1][:40]}")
    for r in v:
        print(f"        {r['ext']:<6} {gb(r['bytes']):>8.3f} GB  {r['name'][:52]}")
print(f"\n  NOTE: extraction is FREE for all of these. Q9 proved .docx/.xlsx/.pptx")
print(f"  are ZIP+XML and unpack with the Python stdlib alone - no ffmpeg, no office,")
print(f"  no converter, no dependency. So format choice costs nothing in tooling.")
print(f"  It may still cost fidelity: a .docx carries structure a .pdf flattens.")

# -------------------------------------- DECISION D: documents with no pairing
print("\n" + "=" * 74)
print("DECISION D - companion documents, and which have no call counterpart")
print("=" * 74)
man = json.load(open(os.path.join(OD, "manifest-v3.json"), encoding="utf-8"))
call_keys = {u["topic"] for u in man["units"]}
call_folders = {u["folder_handle"] for u in man["units"] if u["kind"] == "calls"}

def is_orphan(r):
    """A document whose folder is a CALL month folder but whose name matches no
    call topic - i.e. written material with nothing to pair to."""
    if r["folder_handle"] not in call_folders: return False
    stem = re.sub(r"\.[A-Za-z0-9]{1,5}$", "", r["name"]).strip().casefold()
    stem = re.sub(r"^[\s\d.()\-]+", "", stem)
    stem = re.sub(r"\s+", " ", stem.replace("nhb+", "nhb"))
    return not any(stem and (stem in k or k in stem) for k in call_keys)

orph = [r for r in docs if is_orphan(r)]
res  = [r for r in docs if not is_orphan(r)
        and re.search(r"swipe|template", seednames.get(r["folder_handle"], ""), re.I)]
print(f"  documents total            : {len(docs)}")
print(f"  in a bonus-course folder    : {sum(1 for r in docs if 'bonus' in seednames.get(r['folder_handle'],'').lower() or re.match(r'^[1-9]\\. ', seednames.get(r['folder_handle'],'')))}")
print(f"  in Swipes / Templates      : {len(res)}   ({gb(sum(r['bytes'] or 0 for r in res)):.1f} GB)")
print(f"  no call counterpart        : {len(orph)}   ({gb(sum(r['bytes'] or 0 for r in orph)):.1f} GB)")
print(f"\n  Swipes + Templates are named in G0 §1 as 36 PDFs / 406 MB of orphaned text.")
print(f"  Measured here: {len(res)}. The two disagree and are NOT reconciled here.")

# --------------------------------------------------------------- summary
print("\n" + "=" * 74)
print("WHAT THE FOUR DECISIONS ADD UP TO")
print("=" * 74)
calls   = [u for u in man["units"] if u["kind"] == "calls"]
lessons = [u for u in man["units"] if u["kind"] == "lessons"]
h_all   = sum(u["media"]["dur_s"] or 0 for u in man["units"]) / 3600
b_all   = sum(u["media"]["bytes"] or 0 for u in man["units"])
print(f"  A  all calls + all lessons   {len(man['units']):>4} units  {h_all:>7.2f} h  "
      f"{gb(b_all):>7.2f} GB   ${h_all*60*0.0043:>7.2f}")
print(f"     calls only                {len(calls):>4} units  "
      f"{sum(u['media']['dur_s'] or 0 for u in calls)/3600:>7.2f} h")
print(f"     lessons only              {len(lessons):>4} units  "
      f"{sum(u['media']['dur_s'] or 0 for u in lessons)/3600:>7.2f} h")
print(f"  B  encoding: no effect on STT cost, {gb(b_mp4)-gb(b_mp3):+.1f} GB on download")
print(f"  C  {len(multi)} multi-format document groups need a pick")
print(f"  D  {len(res)} Swipes/Templates PDFs, {len(orph)} unpaired documents")

json.dump({"decisions": {"B_encoding_pairs": len(both),
                         "B_mp3_GB": round(gb(b_mp3), 2), "B_mp4_GB": round(gb(b_mp4), 2),
                         "C_multiformat_groups": len(multi),
                         "C_fmt_combos": {" + ".join(k): v for k, v in fmt_pairs.items()},
                         "D_swipe_template": len(res), "D_unpaired": len(orph)},
           "units": len(man["units"]), "hours": round(h_all, 2)},
          open(os.path.join(OD, "selection-inventory.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print(f"\nWRITTEN {os.path.join(OD, 'selection-inventory.json')}")