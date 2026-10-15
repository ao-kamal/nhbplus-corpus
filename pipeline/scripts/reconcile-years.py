#!/usr/bin/env python3
"""
RECONCILIATION 3b - resolve the 5 remaining year-less calls from the FOLDER TREE,
without waiting for the transcripts.

The hypothesis: seednames.txt is in traversal order, so each year folder is
immediately followed by its own month folders.

    2022 -> 4. April, 5. May, 6. June ...
    2023 -> 1. January, 2. February ...
    2024 -> 1. January, 2. February ...

If that holds, a month folder's year is known even when its files carry no date.

This is an INFERENCE, so it is tested before it is used: every month folder that
DOES hold dated calls is checked against the year the ordering assigns it. If the
ordering is wrong anywhere, it is rejected and the 5 stay unresolved.
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

MONTHS = ["january","february","march","april","may","june","july","august",
          "september","october","november","december"]
ABBR   = {"jan","feb","mar","apr","may","jun","jul","aug","sep","sept","oct","nov","dec"}
LEAD   = re.compile(r"^\s*\d{1,2}\s*[.)]\s*")
YEARRE = re.compile(r"^\s*((?:19|20)\d{2})\s*$")

LOWER = [m.lower() for m in MONTHS]
FULL  = {m: i for i, m in enumerate(MONTHS, 1)}
def month_of(name):
    n = LEAD.sub("", (name or "").lower())
    for w in re.split(r"[^a-z]+", n):
        if w in FULL: return FULL[w]
        hits = [FULL[m] for m in MONTHS if m.startswith(w)]   # MONTHS is capitalised
        if len(hits) == 1: return hits[0]
    return None

# ---- 1. segment the seed list into year blocks ----------------------------
raw = open(os.path.join(OD, "seednames.txt"), encoding="utf-8").read()
order = re.findall(r'"([A-Za-z0-9_-]+)=([^"]*)"', raw)
print("=" * 76)
print("TEST - does seed ordering actually encode year -> month?")
print("=" * 76)
order_names = dict(order)
print(f"  seed entries: {len(order)}")

# A year folder is followed by its own month folders; the next year folder closes
# the block. A month folder BEFORE the first year folder gets no year.
assign, cur_year, block = {}, None, []
def flush(yr, handles):
    if yr is None: return
    for x in handles:
        m = month_of(order_names.get(x, ""))
        if m: assign[x] = (yr, m)
for h, nm in order:
    ym = YEARRE.match(nm.strip())
    if ym:
        flush(cur_year, block)
        cur_year, block = int(ym.group(1)), []
    else:
        block.append(h)
flush(cur_year, block)
print(f"  month folders assigned a year by ordering: {len(assign)}")

# ---- 2. validate against folders that DO carry dated calls ----------------
ok = bad = 0
mismatch = []
for fh, (yr, mo) in sorted(assign.items(), key=lambda x: order_names.get(x[0], "")):
    us = [u for u in calls if u["folder_handle"] == fh and u["year"]]
    if not us: continue
    actual = sorted({u["year"] for u in us})
    if actual == [yr]:
        ok += 1
    else:
        bad += 1
        mismatch.append((order_names.get(fh, fh), yr, actual,
                         sorted(u["date"] for u in us)[:3]))
print(f"\n  month folders WITH dated calls, used as the test set:")
print(f"    year from ordering CORRECT : {ok}")
print(f"    year from ordering WRONG   : {bad}")
for nm, pred, actual, dates in mismatch:
    print(f"      {nm!r:<34} predicted {pred}, actual {actual}  {dates}")

# ---- 3. apply only if validated -------------------------------------------
noy = [u for u in calls if not u["year"]]
print(f"\n  the {len(noy)} unresolved calls:")
if bad == 0 and ok >= 10:
    print(f"  ordering validated on {ok}/{ok+bad} dated folders -> APPLYING it\n")
    resolved = []
    for u in noy:
        a = assign.get(u["folder_handle"])
        if not a:
            print(f"    {u['media']['name'][:56]:<56} no year folder precedes it - STILL OPEN")
            continue
        yr, mo = a
        resolved.append((u, f"{yr:04d}-{mo:02d}"))
        print(f"    {u['media']['name'][:56]:<56} -> {yr}-{mo:02d}  "
              f"(from folder {u['source_folder']!r} following {yr})")
    print(f"\n  resolved {len(resolved)} of {len(noy)}")
    print(f"\n  PROPOSED PATCH to manifest-v3 (year + month for these calls):")
    for u, ym in resolved:
        print(f"    {u['media']['handle']}  {ym}  {u['media']['name'][:50]}")
else:
    print(f"  ordering NOT validated (ok={ok} bad={bad}) -> NOT APPLIED")
    print(f"  these stay unresolved and are recorded as such in the vault")