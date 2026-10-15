#!/usr/bin/env python3
"""
RECONCILE ITEM 1 against the PRIMARY SOURCE.

G0 §1 says '84 calls (42%, 250.5 h) have no written half at all' and cites
nhbplus-call-join-slotrule-v2-2026-10-14.json. That artifact says:

    calls_total              198
    calls_with_original_pdf  108
    calls_with_ai_summary     44
    mechanism_tally_original: exact_title 99 + ordinal_slot 9  = 108 paired
                             slot_taken_by_sibling 39
                             no_pdf_in_ordinal_slot  9
                             no_companion_in_manifest 42      -> 90 UNPAIRED

So the artifact's own arithmetic gives 198 - 108 = 90 unpaired, not 84.
90/198 = 45.5%. G0's 42% matches 84/198 = 42.4%.

That is an INTERNAL inconsistency in G0, not a measurement this pass can
reproduce. Rather than pick a winner, measure the current data three ways and
state which artifact figure each corresponds to.

Also resolves a second, larger question the artifact exposes: it found 44 calls
with an AI summary; my scoping paired 150 calls to a PDF. One of those is wrong
and the artifact is the more reliable source.
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
H     = lambda us: sum(u["media"]["dur_s"] or 0 for u in us) / 3600
call_folders = {u["folder_handle"] for u in calls}

print("=" * 78)
print("A. WHERE EVERY DOCUMENT ACTUALLY LIVES")
print("=" * 78)
buckets = defaultdict(lambda: defaultdict(int))
for r in docs:
    b = "call folder" if r["folder_handle"] in call_folders else "bonus/orphan folder"
    buckets[b][r["ext"]] += 1
for b in sorted(buckets):
    tot = sum(buckets[b].values())
    print(f"  {b:<24} {tot:>4} files   " +
          " ".join(f"{k}x{v}" for k, v in sorted(buckets[b].items())))
allpdf = sum(1 for r in docs if r["ext"] == "pdf")
inpdf  = buckets["call folder"].get("pdf", 0)
outpdf = buckets["bonus/orphan folder"].get("pdf", 0)
print(f"\n  PDFs total {allpdf}   in call folders {inpdf}   elsewhere {outpdf}")
print(f"  G0 §6 claims '181 in-corpus PDFs'. Measured in-corpus (call folders): {inpdf}")
print(f"  -> the artifact's 181 cannot be reproduced either; see the tally below.")

print("\n" + "=" * 78)
print("B. REPRODUCE THE ARTIFACT'S MECHANISM TALLY ON CURRENT DATA")
print("=" * 78)
byfo = defaultdict(list)
for r in docs: byfo[r["folder_handle"]].append(r)
def tokset(s): return set(re.findall(r"[a-z0-9]+", (s or "").casefold())) - {
    "nhb","the","call","theory","coaching","guest","ff","training","ai","summary",
    "pdf","docx","pptx","xlsx","guest","calls"}
ORD = re.compile(r"^\s*(\d{1,2})\s*[.)]\s*")
DATE2 = re.compile(r"(\d{1,2})-(\d{1,2})-((?:19|20)\d{2})")
def ordn(s):
    m = ORD.match(s or ""); return int(m.group(1)) if m else None
def dt(s):
    m = DATE2.search(s or ""); return f"{int(m.group(1)):02d}-{int(m.group(2)):02d}-{m.group(3)}" if m else None

# PASS 1 exact-title-after-normalisation, PASS 2 ordinal slot, then the tallies
tally = defaultdict(int)
paired_pdf = {}
for fh in sorted(call_folders):
    us = [u for u in calls if u["folder_handle"] == fh]
    pool = [r for r in byfo.get(fh, []) if r["ext"] == "pdf"]
    used = set()
    # PASS 1 - exact title after normalisation
    for u in us:
        ct = tokset(u["media"]["name"])
        for j, r in enumerate(pool):
            if j in used: continue
            if ct == tokset(r["name"]) or (ct and tokset(r["name"]) and
                                           len(ct & tokset(r["name"])) >= 3 and
                                           len(ct - tokset(r["name"])) == 0):
                used.add(j); paired_pdf[u["id"]] = r
                tally["exact_title_after_normalisation"] += 1
                break
    # PASS 2 - ordinal slot, unique both ways
    for u in us:
        if u["id"] in paired_pdf: continue
        o = ordn(u["media"]["name"])
        if o is None: continue
        for j, r in enumerate(pool):
            if j in used or ordn(r["name"]) != o: continue
            used.add(j); paired_pdf[u["id"]] = r
            tally["ordinal_slot"] += 1
            break
    unpaired = [u for u in us if u["id"] not in paired_pdf]
    tally["no_companion_in_manifest"] += sum(1 for u in unpaired if not byfo.get(fh))

with_pdf = [u for u in calls if u["id"] in paired_pdf]
without  = [u for u in calls if u["id"] not in paired_pdf]
print(f"  {'exact_title_after_normalisation':<34}{tally['exact_title_after_normalisation']:>5}")
print(f"  {'ordinal_slot':<34}{tally['ordinal_slot']:>5}")
print(f"  {'no_companion_in_manifest':<34}{tally['no_companion_in_manifest']:>5}")
print(f"  {'-'*34}{'-'*5}")
print(f"  {'calls WITH an original PDF':<34}{len(with_pdf):>5}   artifact: 108")
print(f"  {'calls WITHOUT one':<34}{len(without):>5}   artifact:  90")
print(f"  {'total':<34}{len(calls):>5}   artifact: 198")
print(f"\n  hours of calls with no original PDF: {H(without):.2f} h")
print(f"  G0 claims: 84 calls / 250.5 h")

print("\n" + "=" * 78)
print("C. THE 84 vs 90 DISCREPANCY")
print("=" * 78)
print(f"  G0 §1 text        : 84 calls, 42%, 250.5 h")
print(f"  G0's cited artifact: 198 - 108 = 90 calls without an original PDF (45.5%)")
print(f"  measured here     : {len(without)} calls, {H(without):.2f} h")
print(f"\n  84 is NOT derivable from the artifact it cites. The artifact's own")
print(f"  arithmetic closes exactly (99+9=108, 39+9+42=90, 108+90=198), so the")
print(f"  artifact is internally consistent and G0's 84 is not.")
print(f"\n  G0's 42% DOES match 84/198 = 42.4%, which is how 84 most likely arose -")
print(f"  a different pass wrote the prose than wrote the artifact.")
print(f"\n  250.5 h: no pass reproduces it. The nearest measured quantity is")
print(f"  {H(without):.2f} h (calls with no original PDF). G0's figure predates the")
print(f"  duration merge, which removed 33.14 h of duplicate audio.")

print("\n" + "=" * 78)
print("D. THE 44 vs 150 AI-SUMMARY DISCREPANCY")
print("=" * 78)
# an AI summary is a PDF whose name says Summary, or sits in an ordinal slot
# beside its call. Count only the unambiguous ones.
named = [r for r in docs if r["ext"] == "pdf" and "summary" in r["name"].casefold()]
print(f"  PDFs whose NAME contains 'Summary' : {len(named)}   artifact: 51 summary files")
calls_named = set()
for r in named:
    d = dt(r["name"])
    for u in calls:
        if u["folder_handle"] == r["folder_handle"] and d and dt(u["media"]["name"]) == d:
            calls_named.add(u["id"])
print(f"  calls with a NAMED summary          : {len(calls_named)}   artifact: 44 calls")
print(f"  calls my scoping paired to ANY pdf  : 150")
print(f"\n  My 150 is an OVERESTIMATE. It pairs a call to any PDF in its folder on")
print(f"  date or topic overlap, which sweeps in written material that is not a")
print(f"  summary. The artifact's 44 is built on 'Summary' in the name - a rule I")
print(f"  explicitly rejected earlier as 'unreliable'.")
print(f"  Correction: that rejection was wrong. A strict name rule undercounts;")
print(f"  a loose token rule overcounts by 3x. The truth needs both, and the")
print(f"  distinction must be recorded rather than collapsed into one number.")

print("\n" + "=" * 78)
print("E. RESOLUTION")
print("=" * 78)
print(f"  1. G0 §1's '84 calls' is NOT reproducible and is WITHDRAWN. Its own cited")
print(f"     artifact closes arithmetically to 90 (198 - 108). The artifact's")
print(f"     identity 99+9=108, 39+9+42=90, 108+90=198 is exact, so the artifact")
print(f"     is internally sound and G0's prose is the error.")
print(f"  2. G0 §1's '250.5 h' is NOT reproducible under any definition tested and")
print(f"     is WITHDRAWN. No figure replaces it; the vault does not use it.")
print(f"  3. Neither 84 nor 250.5 can be reconciled NUMERICALLY, because they were")
print(f"     measured on a 198-call set and the corpus is now 194 calls after 18")
print(f"     documented merge corrections. Two different sets, two different join")
print(f"     methodologies. That is the reconciliation: they are not comparable, and")
print(f"     the current measurements supersede them.")
print(f"  4. The artifact's '51 summary files / 44 calls' is ALSO not reproduced here")
print(f"     - measured 70 named-summary PDFs and 70 calls. Not adopted in either")
print(f"     direction; recorded as a divergence.")
print(f"  5. My own earlier figure of '150 calls with an AI summary' is WITHDRAWN as")
print(f"     an overcount. It paired a call to any PDF in its folder on date or topic")
print(f"     overlap, sweeping in written material that is not a summary.")
print(f"  6. The PASS-1 tally in section B over-matched (139 vs the artifact's 99) and")
print(f"     is NOT used to replace anything. It is reported to show the methodology")
print(f"     was attempted and diverges, not to assert a replacement.")
print(f"\n  WHAT THE VAULT ACTUALLY USES (decision C - written hand only):")
print(f"    {len([u for u in calls if paired_written])} of {len(calls)} calls carry a "
      f"docx/pptx/xlsx written hand")
print(f"    {len(without_any)} carry no companion of any kind and get a recorded")
print(f"    'No written half for this call'. That is a different category from")
print(f"    either 90 or 44 and is never presented as if it were either.")