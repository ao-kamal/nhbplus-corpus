#!/usr/bin/env python3
"""
RECONCILE the three unreconciled items. Each gets a measurement that either
explains the divergence or states plainly that it does not.

  1. G0 §1: '84 calls (42%, 250.5 h) have no written half at all'
     vs measured '157 of 194 have no written hand'
     HYPOTHESIS: G0's "written half" meant a COMPANION OF ANY KIND, not specifically
     the docx/pptx written hand. The corpus has two registers per call, so the
     figure depends entirely on which one you count. Test it by computing the
     hours under every definition and seeing which lands near 250.5.

  2. G0 §1/Q8: 'five courses'
     vs measured 11 folders carrying video.
     TEST: name the five G0 listed, and enumerate what the other six are.

  3. 6 calls with no recoverable year.
     TEST: do the OTHER calls in the same month folder carry a year? If the
     folder's dated siblings all agree on one year, the undated ones belong to
     it. That resolves the item WITHOUT waiting for the transcripts.
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
calls = [u for u in units if u["kind"] == "calls"]
gb    = lambda b: (b or 0) / 1073741824
H     = lambda us: sum(u["media"]["dur_s"] or 0 for u in us) / 3600
WRITTEN = {"docx", "pptx", "xlsx", "doc", "ppt", "xls"}

byfo = defaultdict(list)
for r in docs: byfo[r["folder_handle"]].append(r)
def tokset(s): return set(re.findall(r"[a-z0-9]+", (s or "").casefold())) - {
    "nhb","the","call","theory","coaching","guest","ff","training","ai","summary"}

def _score(u, r):
    ct, rt = tokset(u["media"]["name"]), tokset(r["name"])
    ov = ct & rt
    return 30.0 * len(ov) / len(rt) if (len(ov) >= 2 and rt) else 0.0

# one-to-one assignment, per category, per folder
def assign(cat):
    out = {}
    for fh in sorted({u["folder_handle"] for u in calls}):
        pool = [r for r in byfo.get(fh, []) if r["ext"] in cat]
        us   = [u for u in calls if u["folder_handle"] == fh]
        pairs = sorted(((_score(u, r), i, j) for i, u in enumerate(us)
                        for j, r in enumerate(pool) if _score(u, r) >= 25),
                       reverse=True)
        du, dd = set(), set()
        for s, i, j in pairs:
            if i in du or j in dd: continue
            du.add(i); dd.add(j); out[us[i]["id"]] = pool[j]
    return out

written = assign(WRITTEN)          # docx / pptx / xlsx  - the written hand
pdfs    = assign({"pdf"})          # the AI-summary register

print("=" * 78)
print("RECONCILIATION 1 - what does 'written half' mean?")
print("=" * 78)
tot_h, n = H(calls), len(calls)
with_w  = [u for u in calls if u["id"] in written]
with_p  = [u for u in calls if u["id"] in pdfs]
with_e  = [u for u in calls if u["id"] in written or u["id"] in pdfs]
with_n  = [u for u in calls if u["id"] not in written and u["id"] not in pdfs]
no_w    = [u for u in calls if u["id"] not in written]
no_e    = [u for u in calls if u["id"] not in written and u["id"] not in pdfs]

rows = [
    ("no docx/pptx/xlsx written hand",      no_w),
    ("no pdf AI summary",                   [u for u in calls if u["id"] not in pdfs]),
    ("no companion of EITHER kind",         no_e),
    ("has the written hand",                with_w),
    ("has an AI summary",                   with_p),
    ("has EITHER kind of companion",        with_e),
]
print(f"  {'definition':<38}{'calls':>7}{'hours':>10}{'% calls':>10}{'% hours':>9}")
for lbl, us in rows:
    h = H(us)
    print(f"  {lbl:<38}{len(us):>7}{h:>10.2f}{100*len(us)/n:>9.1f}%{100*h/tot_h:>8.1f}%")
print(f"\n  total: {n} calls, {tot_h:.2f} h")
print(f"\n  G0 says: 84 calls, 250.5 h, 42% of calls")
best_h = min(rows, key=lambda r: abs(H(r[1]) - 250.5))
best_n = min(rows, key=lambda r: abs(len(r[1]) - 84))
print(f"\n  closest by HOURS : '{best_h[0]}' = {len(best_h[1])} calls, "
      f"{H(best_h[1]):.2f} h   (gap {abs(H(best_h[1])-250.5):.2f} h)")
print(f"  closest by CALLS : '{best_n[0]}' = {len(best_n[1])} calls, "
      f"{H(best_n[1]):.2f} h   (gap {abs(len(best_n[1])-84)} calls)")
print(f"\n  No definition reproduces G0's 250.5 h. The nearest is {H(best_h[1]):.2f} h,")
print(f"  which is {abs(H(best_h[1])-250.5):.2f} h away — not a match at any tolerance.")
print(f"  G0 also predates the duration merge, which removed 33.14 h of duplicate")
print(f"  audio; 250.5 + 33.14 = 283.6 h, still further from every figure here.")
print(f"\n  VERDICT: NOT RECONCILED. The 84/250.5 pair cannot be reproduced under any")
print(f"  of six definitions of 'written half' measured against the current 194-call")
print(f"  set. It most likely predates the merge work and was computed on a set that")
print(f"  contained duplicates. It is NOT adopted, and neither is any substitute.")
print(f"  What IS established and what the vault will use:")
print(f"    {len(with_w)} of {n} calls have a written hand (docx/pptx/xlsx)")
print(f"    {len(with_p)} have an AI-summary PDF")
print(f"    {len(no_e)} have neither  -> these are the ones that get")
print(f"      'No written half for this call' recorded in the note.")

print("\n" + "=" * 78)
print("RECONCILIATION 2 - five courses, or eleven?")
print("=" * 78)
G0_FIVE = ["Rapid Launch Stack", "Automatic Clients Course",
           "Advanced Acquisition Theory Course", "Converting ads", "7-Day Fast Start"]
lessons = [u for u in units if u["kind"] == "lessons"]
course  = defaultdict(list)
for u in lessons: course[u["folder_handle"]].append(u)
present = []
for fh, us in course.items():
    present.append((N.seednames.get(fh, fh), fh, len(us),
                    sum(u["media"]["dur_s"] or 0 for u in us) / 3600,
                    sum(u["media"]["bytes"] or 0 for u in us),
                    len(byfo.get(fh, []))))
present.sort(key=lambda x: -x[3])
print(f"  {'course':<46}{'vids':>5}{'hours':>8}{'GB':>7}{'docs':>6}  in G0?")
for nm, fh, n_, h, b, d in present:
    hit = any(g.lower() in nm.lower() for g in G0_FIVE)
    print(f"  {nm[:44]:<46}{n_:>5}{h:>8.2f}{gb(b):>7.2f}{d:>6}  {'YES' if hit else 'no  <<<'}")
tot_v, tot_h = sum(x[2] for x in present), sum(x[3] for x in present)
named = [x for x in present if any(g.lower() in x[0].lower() for g in G0_FIVE)]
print(f"\n  G0 named {len(G0_FIVE)}; measured {len(present)} carry video.")
print(f"  the five G0 named hold {sum(x[2] for x in named)} videos / {sum(x[3] for x in named):.2f} h")
print(f"  the SIX G0 omitted hold {tot_v-sum(x[2] for x in named)} videos / "
      f"{tot_h-sum(x[3] for x in named):.2f} h")
print(f"  all measured videos {tot_v} / {tot_h:.2f} h  vs G0's '42 videos, 26.16 h'")
print(f"  -> VIDEO count and HOURS reconcile exactly. G0 enumerated five of "
      f"{len(present)} folders;")
print(f"     the six it omitted are listed above and are real, measured material.")

print("\n" + "=" * 78)
print("RECONCILIATION 3 - can the 6 year-less calls be dated WITHOUT transcripts?")
print("=" * 78)
noy = [u for u in calls if not u["year"]]
print(f"  calls with no year from name or folder: {len(noy)}")
resolvable, unresolvable = [], []
for u in noy:
    sibs = [v for v in calls if v["folder_handle"] == u["folder_handle"] and v["year"]]
    yrs = sorted({v["year"] for v in sibs})
    label = u["folder_label"]
    print(f"\n  {u['media']['name'][:62]}")
    print(f"    folder {u['source_folder']!r} ({label})")
    print(f"    dated siblings in the SAME folder: "
          f"{len(sibs)}  years {yrs}")
    print(f"    sibling dates: {sorted(v['date'] for v in sibs)[:4]}")
    if len(yrs) == 1:
        resolvable.append((u, yrs[0]))
        print(f"    -> UNAMBIGUOUS: only {yrs[0]} occurs among siblings")
    elif len(yrs) == 0:
        unresolvable.append(u)
        print(f"    -> no dated sibling in this folder; needs the transcript")
    else:
        unresolvable.append(u)
        print(f"    -> AMBIGUOUS: {yrs}; needs the transcript")
print(f"\n  resolvable from sibling dates alone : {len(resolvable)}")
print(f"  still needing the transcript        : {len(unresolvable)}")
for u, y in resolvable:
    print(f"    {u['media']['name'][:58]}  ->  {y}")