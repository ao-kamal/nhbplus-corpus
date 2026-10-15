#!/usr/bin/env python3
"""
RECONCILIATION 3, COMPLETED - close the 5 year-less calls by ELIMINATION.

The folder-ordering inference was falsified (32/34) and correctly rejected. But
elimination is a different argument and it does close this.

Facts, each independently checkable:

  1. Exactly THREE folder handles are named '5. May':
         B2FEmJjC  RyV0FDpI  liVUnbAT
  2. Two of them carry DATED calls inside, which dates them outright:
         B2FEmJjC -> 5-30-2022        (2022)
         RyV0FDpI -> 5-4-2023 ... 5-25-2023   (2023)
  3. The share is 'Up to 02.2025' and begins mid-2021, so May exists in only
     THREE years: 2022, 2023, 2024.
         2021 -> first call is June 2021, no May
         2025 -> last call is February 2025, no May
  4. Two of the three May folders are taken. The third is 2024. QED.

Every step is checked against the data rather than asserted, and the script
REFUSES to conclude if any step fails.
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
calls = [u for u in units if u["kind"] == "calls"]

LEAD = re.compile(r"^\s*\d{1,2}\s*[.)]\s*")
YEARRE = re.compile(r"^\s*((?:19|20)\d{2})\s*$")
MONTHNUM = {m.lower(): i for i, m in enumerate(
    ["january","february","march","april","may","june","july","august",
     "september","october","november","december"], 1)}
def month_of(name):
    for w in re.split(r"[^a-z]+", LEAD.sub("", (name or "").lower())):
        if w in MONTHNUM: return MONTHNUM[w]
    return None

print("=" * 76)
print("STEP 1 - how many handles are named '5. May'?")
print("=" * 76)
may_handles = sorted(h for h, n in N.seednames.items()
                     if month_of(n) == 5 and YEARRE.match(n.strip()) is None)
print(f"  {len(may_handles)}  ->  {may_handles}")
assert len(may_handles) == 3, f"expected 3 May folders, found {len(may_handles)}"
print(f"  OK: exactly three, so each corresponds to one year.")

print("\n" + "=" * 76)
print("STEP 2 - which are dated from inside?")
print("=" * 76)
dated = {}
for h in may_handles:
    us = [u for u in calls if u["folder_handle"] == h and u["year"]]
    ys = sorted({u["year"] for u in us})
    dated[h] = ys
    print(f"  {h}  dated calls: {len(us):>2}  years: {ys}")
resolved = {h: ys[0] for h, ys in dated.items() if len(ys) == 1}
assert len(resolved) == 2, f"expected 2 self-dating May folders, got {len(resolved)}"
print(f"  OK: {resolved} are dated by their own contents.")

print("\n" + "=" * 76)
print("STEP 3 - in how many years does MAY occur in this corpus?")
print("=" * 76)
# Derive each year's span from the CALL DATES, not from the year folder's own
# handle - a year folder does not contain its month folders, so asking it for its
# month range returns nothing and every year looks equally possible.
ym = defaultdict(set)
for u in calls:
    if u["year"]: ym[u["year"]].add(u["month"])
span = {}
for y in sorted(ym):
    ms = sorted(ym[y])
    span[y] = (ms[0], ms[-1])
    print(f"  {y}:  months {ms[0]}..{ms[-1]}   ({len(ms)} distinct)")
candidates = [y for y, (a, b) in span.items() if a <= 5 <= b]
print(f"\n  years whose call span INCLUDES May: {sorted(candidates)}")
print(f"  excluded: {sorted(set(span) - set(candidates))}")
assert len(candidates) == 3, f"expected 3 May-capable years, got {sorted(candidates)}"
assert 2021 not in candidates, "2021 should be excluded - the corpus starts in June"
assert 2025 not in candidates, "2025 should be excluded - the share ends at 02.2025"
print(f"  OK: exactly three. 2021 starts in June, 2025 ends in February.")

print("\n" + "=" * 76)
print("STEP 4 - elimination")
print("=" * 76)
taken = set(resolved.values())
remaining_handles = [h for h in may_handles if h not in resolved]
remaining_years   = [y for y in candidates if y not in taken]
print(f"  taken by dated folders : {sorted(taken)}")
print(f"  unassigned folders     : {remaining_handles}")
print(f"  unassigned years       : {remaining_years}")
if len(remaining_handles) == 1 and len(remaining_years) == 1:
    h, y = remaining_handles[0], remaining_years[0]
    print(f"\n  => {h} = May {y}.  Exactly one folder, exactly one year left.")
    print(f"\n  CORROBORATING ARGUMENT - seed ordering, tested on the MAY subset only.")
    print(f"  The global ordering test failed 2/34, so it is not used alone. But on")
    print(f"  the two May folders whose contents can date them, does it agree?")
    order = re.findall(r'"([A-Za-z0-9_-]+)=([^"]*)"',
                       open(os.path.join(OD, "seednames.txt"), encoding="utf-8").read())
    names = dict(order)
    cur, pred = None, {}
    for hh, nm2 in order:
        ymatch = YEARRE.match(nm2.strip())
        if ymatch: cur = int(ymatch.group(1))
        elif hh in may_handles and cur: pred[hh] = cur
    for hh in may_handles:
        actual = resolved.get(hh)
        p = pred.get(hh)
        if actual:
            print(f"    {hh}: order predicts {p}, contents say {actual}  "
                  f"{'MATCH' if p == actual else 'MISMATCH'}")
        else:
            print(f"    {hh}: order predicts {p}, contents say (undated)  -> "
                  f"unverifiable, but the elimination above is independent")
    print(f"\n  PROPOSED PATCH (year {y}, month 5) for the undated calls in {h}:")
    for u in calls:
        if u["folder_handle"] != h or u["year"]: continue
        print(f"    {u['media']['handle']}  {y}-05  {u['media']['name'][:52]}")
    print(f"\n  LABEL becomes '{y}-05 May' instead of '05 May year-unknown'")
else:
    print(f"\n  ELIMINATION FAILS - {len(remaining_handles)} folders and "
          f"{len(remaining_years)} years remain. NOT RESOLVED.")

print("\n" + "=" * 76)
print("SEPARATE DEFECT FOUND WHILE DOING THIS")
print("=" * 76)
h = remaining_handles[0] if len(remaining_handles) == 1 else None
if h:
    us = [u for u in calls if u["folder_handle"] == h and not u["date"]]
    for i in range(len(us)):
        for j in range(i + 1, len(us)):
            a, b = us[i], us[j]
            if not a["media"]["dur_s"] or not b["media"]["dur_s"]: continue
            d1, d2 = a["media"]["dur_s"], b["media"]["dur_s"]
            if abs(d1 - d2) / max(d1, d2) <= 0.02:
                print(f"  UNMERGED DUPLICATE in {h}:")
                print(f"    {a['media']['ext']}  {d1}s  {a['media']['name']}")
                print(f"    {b['media']['ext']}  {d2}s  {b['media']['name']}")
                print(f"  cause: the duration merge requires a DATE on both units,")
                print(f"  so undated calls are exempt from it. That is a gap.")