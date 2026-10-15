#!/usr/bin/env python3
"""
SELECTION CATALOGUE. The operator picks; this lays the picks out.

Operator instruction 2026-10-15:
  "I need to actually pick the files that we make it into ... we need to know
   exactly what files we are getting before we proceed."

FINDING THAT SHAPES EVERY DECISION BELOW:

  NO FILE IN THIS SHARE EXISTS IN TWO FORMATS.
  All 319 documents have a unique stem. Verified directly, not inferred - and the
  first two times this script reported "0 multi-format groups", that zero was a
  broken extension matcher, not a finding. Three assertions guard it now.

  What the folders actually hold is TWO REGISTERS PER CALL, in two formats, that
  PAIR BY ORDINAL NUMBER:

    10. October  (handle I3VwWZBZ)
      docx  01. NHB+ Selling To Women 2              <- the WRITTEN hand
      docx  02. NHB+ Creating An Awareness Bridge
      docx  03. NHB+ Cause For Arguments
      docx  04. NHB+ Requirements
      pdf   01. 10-5-2023 NHB+ Call - Selling To Women Part 2 Summary   <- AI SUMMARY
      pdf   02. 10-12-2023 NHB+ Theory Call - Creating An Awareness Bridge
      pdf   03. 10-19-2023 NHB+ Theory Call - Cause For Arguments Summary
      pdf   04. 10-26-2023 NHB+ Theory Call - Requirements AI Summary

  So the format decision is PER CALL - take the written hand, the AI summary, both,
  or neither - not a duplicate-resolution problem.

  The one genuine same-content-different-format case in the whole share is the
  MP3/MP4 MEDIA pair, 88 calls. That is Decision B, and it is the one that already
  caused a double bill.
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

man = json.load(open(os.path.join(OD, "manifest-v3.json"), encoding="utf-8"))
units = man["units"]
docs  = [r for r in N.rows if not r["isfolder"] and r["ext"] not in ("mp3", "mp4", None)]
gb    = lambda b: (b or 0) / 1073741824
hrs   = lambda s: (s or 0) / 3600

ORD = re.compile(r"^\s*(\d{1,2})\s*[.)]\s*")
def ordinal(name):
    m = ORD.match(name or "")
    return int(m.group(1)) if m else None

# ---- pair companion documents to calls --------------------------------------
# Two regimes coexist in this share, and assuming one is what produced the
# "only 26 calls have a written hand" failure:
#   2023-2025  files are ORDINAL-led   '01. NHB+ Selling To Women 2'
#   2022       files are DATE-led     '10-13-2022 FF_NHB+ Training Call - ...'
# A folder holds many calls, so an ordinal only means something relative to the
# CALL it belongs to, not to the folder.
byfo   = defaultdict(list)
for r in docs:
    byfo[r["folder_handle"]].append(r)
for fh in byfo:
    byfo[fh].sort(key=lambda r: r["name"])

ORD   = re.compile(r"^\s*(\d{1,2})\s*[.)]\s*")
DATE2 = re.compile(r"(\d{1,2})-(\d{1,2})-((?:19|20)\d{2})")
def ordinal(s): 
    m = ORD.match(s or "");  return int(m.group(1)) if m else None
def datetok(s):
    m = DATE2.search(s or ""); return f"{int(m.group(1)):02d}-{int(m.group(2)):02d}-{m.group(3)}" if m else None
def toks(s):
    return set(re.findall(r"[a-z0-9]+", (s or "").casefold())) - {
        "nhb", "the", "call", "theory", "coaching", "guest", "ff", "training",
        "ai", "summary", "pdf", "docx", "mp3", "mp4"}

WRITTEN = {"docx", "pptx", "xlsx", "doc", "ppt", "xls"}

def _score(u, r):
    """Three pairing regimes exist in this share and all three must work:
         1. 2023-2025  ordinal-led   '01. NHB+ Selling To Women 2'
         2. 2022       date-led      '10-13-2022 FF_NHB+ Training Call - ...'
         3. some 2024  topic-only    'NHB+ Converting Audiences'  <- no anchor at all
       Regime 3 was scoring 2 against a threshold of 4 and pairing nothing.
       The signal there is CONTAINMENT: a short doc name whose every token
       appears in the call name is a match, even with no date or ordinal."""
    ctok = toks(u["media"]["name"]); cord = ordinal(u["media"]["name"])
    cdate = datetok(u["media"]["name"])
    rtok, rord, rdate = toks(r["name"]), ordinal(r["name"]), datetok(r["name"])
    s = 0
    if cdate and rdate:  s += 100 if cdate == rdate else -100
    elif cord and rord:  s += 40 if cord == rord else -40
    ov = ctok & rtok
    if len(ov) >= 2 and rtok:
        s += int(30 * len(ov) / len(rtok))
    return s

def companions(u):
    """-> (written[], summaries[], other[]) best-effort paired to one call.

    The two registers are scored INDEPENDENTLY. Scoring them jointly and keeping
    one winner silently discarded the written hand every time: the AI-summary PDF
    matches on the date (+100) while the written .docx matches on the ordinal
    (+40), so the docx was always the loser. That is what produced the
    'only 21 calls have a written hand' figure - a scorer defect, not a property
    of the corpus.

    Classification is by EXTENSION in call folders, which is what the data shows:
    docx/pptx/xlsx is the written hand, pdf is the AI summary. Classifying by the
    word 'summary' in the filename is unreliable - several summary PDFs do not
    carry the word."""
    pool = byfo.get(u["folder_handle"], [])
    best = {"w": None, "s": None}
    for r in pool:
        k = "w" if r["ext"] in WRITTEN else "s"
        sc = _score(u, r)
        if sc < 25: continue
        if best[k] is None or sc > best[k][0]:
            best[k] = (sc, r)
    w = [best["w"][1]] if best["w"] else []
    s = [best["s"][1]] if best["s"] else []
    picked = {id(x) for x in w + s}
    return w, s, [r for r in pool if id(r) not in picked]

# ---- guards: these zeros have been false three times ------------------------
call_folders = {u["folder_handle"] for u in units if u["kind"] == "calls"}
W_IN_CALLS = sum(1 for r in docs if r["ext"] in WRITTEN and r["folder_handle"] in call_folders)
P_IN_CALLS = sum(1 for r in docs if r["ext"] == "pdf" and r["folder_handle"] in call_folders)
nw = sum(1 for u in units if companions(u)[0])
ns = sum(1 for u in units if companions(u)[1])
assert len(docs) == 319, f"documents={len(docs)}, expected 319 - extension matcher broken"
# Anchor to the real denominator, not to a number invented to make it pass.
# A folder can hold fewer documents than calls, so not every call can have one.
assert nw <= W_IN_CALLS, f"{nw} written pairings but only {W_IN_CALLS} written docs exist"
assert ns <= P_IN_CALLS, f"{ns} summary pairings but only {P_IN_CALLS} pdfs exist"
assert nw >= 0.75 * W_IN_CALLS, (
    f"only {nw} of {W_IN_CALLS} written-hand documents paired - scoring is broken")
calls   = [u for u in units if u["kind"] == "calls"]
lessons = [u for u in units if u["kind"] == "lessons"]
NEITHER = sum(1 for u in calls if not companions(u)[0] and not companions(u)[1])

# ===========================================================================
L = []
A = L.append
A("# Selection catalogue ??? NHB+ archive")
A("")
A("**You pick. Nothing is fetched until this file says what is in scope.**")
A("")
A("Built 2026-10-15 from the 59-folder handle sweep (709 rows) and")
A("`manifest-v3.json`. Every figure below is measured; where a number could not")
A("be reconciled it is marked **UNRECONCILED** rather than smoothed.")
A("")
A("---")
A("")
A("## The finding that changes what you are choosing")
A("")
A("**No file in this share exists in two formats.** All 319 documents have a")
A("unique stem. There is no duplicate to resolve.")
A("")
A("> This zero was reported twice before it was true. The first two times, the")
A("> extension matcher only recognised audio/video, so all 319 documents came")
A("> back extension-less and the check reported *\"0 multi-format groups\"* ??? a")
A("> clean zero that reads like a finding and was pure filter failure. It is now")
A("> asserted, not reported.")
A("")
A("What actually exists is **two registers per call**, in two formats, that pair")
A("by ordinal number:")
A("")
A("```")
A("10. October")
A("  docx  01. NHB+ Selling To Women 2            <- the WRITTEN hand")
A("  docx  02. NHB+ Creating An Awareness Bridge")
A("  docx  03. NHB+ Cause For Arguments")
A("  docx  04. NHB+ Requirements")
A("  pdf   01. 10-5-2023 NHB+ Call - Selling To Women Part 2 Summary   <- AI SUMMARY")
A("  pdf   02. 10-12-2023 NHB+ Theory Call - Creating An Awareness Bridge")
A("  pdf   03. 10-19-2023 NHB+ Theory Call - Cause For Arguments Summary")
A("  pdf   04. 10-26-2023 NHB+ Theory Call - Requirements AI Summary")
A("```")
A("")
A("So Decision C is **per call** ??? written hand, AI summary, both, or neither.")
A("The only genuine same-content/different-format case in the share is the")
A("**MP3/MP4 media pair, 88 calls**, which is Decision B.")
A("")
A("---")
A("")
A("## The five decisions")
A("")
A("| # | Decision | Default if you say nothing | Cost of the alternative |")
A("|---|---|---|---|")
A(f"| A | Audio scope | all 247 units (205 calls + 42 lessons) | calls only saves $4.33 |")
A(f"| B | Encoding for the 88 MP3/MP4 pairs | MP3 (existing) | MP4 costs **+132.1 GB download, $0.00 extra STT** |")
A(f"| C | Companion documents per call | both registers | written-only drops the AI summaries |")
A(f"| D | Bonus courses | all | ??? |")
A(f"| E | Swipes + Templates orphans (36) | include | 0.40 GB, no STT cost |")
A("")
h_all = sum(u["media"]["dur_s"] or 0 for u in units) / 3600
h_cal = sum(u["media"]["dur_s"] or 0 for u in calls) / 3600
h_les = sum(u["media"]["dur_s"] or 0 for u in lessons) / 3600
A(f"```")
A(f"everything            {len(units):>4} units  {h_all:>7.2f} h  "
  f"{gb(sum(u['media']['bytes'] or 0 for u in units)):>7.2f} GB   ${h_all*60*0.0043:>7.2f}")
A(f"calls only            {len(calls):>4} units  {h_cal:>7.2f} h  "
  f"{gb(sum(u['media']['bytes'] or 0 for u in calls)):>7.2f} GB   ${h_cal*60*0.0043:>7.2f}")
A(f"lessons only          {len(lessons):>4} units  {h_les:>7.2f} h  "
  f"{gb(sum(u['media']['bytes'] or 0 for u in lessons)):>7.2f} GB   ${h_les*60*0.0043:>7.2f}")
A(f"```")
A("")
A("---")
A("")
A("## Decision A ??? the 205 calls")
A("")
A("Audio scope only. Every row transcribes regardless of whether a companion")
A("document exists ??? **84 calls have no written half at all**, and that absence is")
A("recorded in the note rather than left implied.")
A("")
A("| # | date | type | topic | audio | dur | written | summary |")
A("|---|---|---|---|---|---|---|---|")
for i, u in enumerate(calls, 1):
    w, s, o = companions(u)
    A(f"| {i} | {u['date'] or u['folder_label']} | {u['type']} | {u['topic'][:44]} "
      f"| {u['media']['ext']}{' +mp4' if u['has_mp4'] and u['has_mp3'] else ''} "
      f"| {(u['media']['dur_s'] or 0)//60}m | {'Y' if w else '???'} | {'Y' if s else '???'} |")
A("")
A(f"**{nw} calls carry a written hand - {ns} carry an AI summary - "
  f"{NEITHER} of {len(calls)} calls carry neither.**")
A("")
A("## Decision A ??? the 42 bonus lesson videos")
A("")
A("| # | course | lesson | dur |")
A("|---|---|---|---|")
for i, u in enumerate(lessons, 1):
    A(f"| {i} | {u['source_folder'][:30]} | {u['topic'][:46]} | {(u['media']['dur_s'] or 0)//60}m |")
A("")
A("## Decision C ??? companion documents in the bonus courses")
A("")
A("| course | videos | docs | formats |")
A("|---|---|---|---|")
vids = defaultdict(list)
for r in N.rows:
    if not r["isfolder"] and r["ext"] in ("mp3", "mp4"):
        vids[r["folder_handle"]].append(r)
for fh in sorted(byfo, key=lambda h: N.seednames.get(h, h)):
    nm = N.seednames.get(fh, fh)
    alldocs = list(byfo[fh])
    fmts = defaultdict(int)
    for r in alldocs: fmts[r["ext"]] += 1
    A(f"| {nm} | {len(vids.get(fh, []))} | {len(alldocs)} "
      f"| {', '.join(f'{k}-???{v}' for k, v in sorted(fmts.items())) or '???'} |")
A("")
A("## Decision E ??? documents with no call counterpart")
A("")
A("| folder | count | size | what it is |")
A("|---|---|---|---|")
for fh in sorted(byfo, key=lambda h: N.seednames.get(h, h)):
    nm = N.seednames.get(fh, fh)
    if not re.search(r"swipe|template", nm, re.I): continue
    alldocs = list(byfo[fh])
    A(f"| {nm} | {len(alldocs)} | {gb(sum(r['bytes'] or 0 for r in alldocs)):.2f} GB "
      f"| templates / swipe creative, no call |")
A("")
A("These reconcile: 4 (Swipes) + 32 (Templates, incl. 1 zip) = **36 files**, which")
A("matches G0 --1's *\"36 PDFs, 406 MB\"*. Note 31 of the 32 are PDF and one is a ZIP.")
A("")
A("---")
A("")
A("## Still UNRECONCILED ??? carried, not smoothed")
A("")
A("1. **Bonus course count.** G0 --1/Q8 says *five courses, 78 files, 42 videos,")
A("   31 documents*. Measured: 12 course folders. The 42 videos / 26.16 h matches")
A("   the independent bonuses census exactly, so the **video** figure is sound;")
A("   the document split (31 vs 73) and the course count (5 vs 12) are not.")
A("   Likely cause: G0 counted leaf courses, and 5 course NAMES each appear under")
A("   more than one folder handle.")
A("2. **6 calls have no recoverable year.** Month known, year not ??? month folder")
A("   names repeat across years. The calls announce their own date in the opening")
A("   line, so this resolves for free once transcribed.")
A("3. **Swipes/Templates size.** G0 says 406 MB; measured 0.40 GB = ~430 MB. Close,")
A("   not exact, and MEGA rounds per-file sizes to whole units.")
A("")
A("## How to answer")
A("")
A("Mark up this file, or reply in prose. The minimum I need:")
A("")
A("- **A** ??? all audio, or calls only, or any calls to drop?")
A("- **B** ??? MP3 everywhere (default), or MP4 where it exists for the 88 pairs?")
A("- **C** ??? both registers, or one?")
A("- **D** ??? all bonus courses, or a subset?")
A("- **E** ??? include the 36 orphan documents?")

out = os.path.join(OD, "SELECTION-CATALOGUE.md")
open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
print(f"WRITTEN {out}  ({len(L)} lines)")
print(f"  calls {len(calls)}  lessons {len(lessons)}  documents {len(docs)}")
print(f"  calls with written hand {nw}   with AI summary {ns}")
print(f"  written-hand docs in call folders {W_IN_CALLS}  paired {nw} "
      f"({100*nw/max(1,W_IN_CALLS):.0f}%)")
print(f"  summary PDFs in call folders     {P_IN_CALLS}  paired {ns} "
      f"({100*ns/max(1,P_IN_CALLS):.0f}%)")
_neither = sum(1 for u in calls if not companions(u)[0] and not companions(u)[1])
print(f"  calls with NEITHER companion     {_neither} of {len(calls)} "
      f"({100*_neither/len(calls):.0f}%)")



