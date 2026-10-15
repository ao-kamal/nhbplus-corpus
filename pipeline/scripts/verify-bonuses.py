#!/usr/bin/env python3
"""
VERIFY THE BONUS-COURSE STRUCTURE - the operator's actual question:
"when it comes to stuff like the bonuses, there are some files that have multiple
formats. I need to pick those."

Two prior figures are suspect and must be checked directly rather than inherited:
  * 'multi-format groups: 0'  - was TRUE when the extension matcher was broken,
    and is now claimed again. Both times it was a filter, not a finding.
  * 'in a bonus-course folder: 0' - came from a regex written with a doubled
    backslash, which can never match. Third instance of that mistake this session.

So: list every folder, every document in it, grouped by stem, and say plainly
whether any stem appears under two formats.
"""
import io, json, os, re, sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# normalize.py prints a full report and calls sys.stdout.reconfigure() at import.
# Swallow BOTH: reconfigure onto a StringIO fails, so silence at the file-descriptor
# level with os.dup2, which has no such attribute to break on.
import os as _os
_saved = _os.dup(1)
_null = _os.open(_os.devnull, _os.O_WRONLY)
_os.dup2(_null, 1)
try:
    import normalize as N
finally:
    _os.dup2(_saved, 1); _os.close(_null); _os.close(_saved)

rows, seednames = N.rows, N.seednames
docs = [r for r in rows if not r["isfolder"] and r["ext"] not in ("mp3", "mp4", None)]
gb = lambda b: (b or 0) / 1073741824

def stem_of(name):
    s = re.sub(r"\.[A-Za-z0-9]{1,5}$", "", name or "")
    s = re.sub(r"^[\s\d]+[.)]\s*", "", s)           # leading '1. '
    s = s.replace("NHB+", "NHB")
    return re.sub(r"\s+", " ", s).strip().casefold()

# Which folders are bonus courses? A numbered course name, NOT a month, NOT a year.
MONTHRE = re.compile(r"january|february|march|april|may|june|july|august|september"
                     r"|october|november|december|jan\.|feb\.|mar\.|apr\.|jun\.|jul\."
                     r"|aug\.|sep\.|sept\.|oct\.|nov\.|dec\.")
def folder_role(name):
    n = re.sub(r"^\s*\d{1,2}\s*\.\s*", "", (name or "").strip())
    if re.fullmatch(r"(19|20)\d{2}", n.strip()): return "year"
    if MONTHRE.search(n.lower()):                   return "call-month"
    if re.search(r"[a-z]", n.lower()):               return "COURSE"
    return "other"

byfolder = defaultdict(list)
for r in docs: byfolder[r["folder_handle"]].append(r)

print("=" * 76)
print("DOCUMENT FOLDER MAP - 319 documents, by what the folder actually is")
print("=" * 76)
role_of = {}
for fh in sorted(byfolder, key=lambda h: seednames.get(h, h)):
    name = seednames.get(fh, fh)
    role = folder_role(name)
    role_of[fh] = role
    v = byfolder[fh]
    fmts = defaultdict(int)
    for r in v: fmts[r["ext"]] += 1
    b = sum(r["bytes"] or 0 for r in v)
    print(f"  {name[:44]:<44} {role:<11} {len(v):>3} docs  {gb(b):>7.2f} GB  "
          + " ".join(f"{k}x{n}" for k, n in sorted(fmts.items())))
print()
for role in ("COURSE", "call-month", "year", "other"):
    n = sum(1 for fh in byfolder if role_of.get(fh) == role)
    print(f"  folders classified {role:<11}: {n}")

# ---------------------------------------------------------------- multi-format
print("\n" + "=" * 76)
print("MULTI-FORMAT CHECK - same stem, different extension, same folder")
print("=" * 76)
groups = defaultdict(list)
for r in docs:
    groups[(r["folder_handle"], stem_of(r["name"]))].append(r)
collide_any  = {k: v for k, v in groups.items() if len(v) > 1}
collide_fmt  = {k: v for k, v in groups.items() if len({r["ext"] for r in v}) > 1}
print(f"  document groups (folder+stem): {len(groups)}")
print(f"  groups with >1 file at all    : {len(collide_any)}")
print(f"  groups spanning >1 FORMAT      : {len(collide_fmt)}")
if collide_any:
    print("\n  every group holding more than one file:")
    for k, v in sorted(collide_any.items(), key=lambda x: seednames.get(x[0][0], ""))[:25]:
        tag = "  <<< MULTI-FORMAT" if len({r['ext'] for r in v}) > 1 else ""
        print(f"    {seednames.get(k[0],k[0])[:30]:<30} {k[1][:44]}{tag}")
        for r in v:
            print(f"        {r['ext']:<6} {r['name'][:60]}")

# ------------------------------------------------- per-course full inventory
print("\n" + "=" * 76)
print("PER-COURSE INVENTORY - videos AND companion documents together")
print("=" * 76)
media_by_folder = defaultdict(list)
for r in rows:
    if not r["isfolder"] and r["ext"] in ("mp3", "mp4"):
        media_by_folder[r["folder_handle"]].append(r)

for fh in sorted(role_of, key=lambda h: seednames.get(h, h)):
    if role_of[fh] != "COURSE": continue
    name = seednames.get(fh, fh)
    vids, docs_ = media_by_folder.get(fh, []), byfolder.get(fh, [])
    hrs = sum(r["dur_s"] or 0 for r in vids) / 3600
    vb  = sum(r["bytes"] or 0 for r in vids)
    db  = sum(r["bytes"] or 0 for r in docs_)
    print(f"\n  {name}")
    print(f"    videos : {len(vids):>3}  {hrs:>6.2f} h  {gb(vb):>6.2f} GB")
    print(f"    docs   : {len(docs_):>3}            {gb(db):>6.3f} GB  "
          + (", ".join(f"{k} x{n}" for k, n in sorted(
              (e, sum(1 for r in docs_ if r["ext"] == e))
              for e in {r["ext"] for r in docs_})) or "none"))
    for r in sorted(vids, key=lambda x: x["name"])[:14]:
        print(f"        V {r['dur_s'] or 0:>6}s  {r['name'][:58]}")
    for r in sorted(docs_, key=lambda x: x["name"])[:14]:
        print(f"        D {r['ext']:<5} {r['name'][:56]}")

# ------------------------------------------------------------------- totals
print("\n" + "=" * 76)
courses = [fh for fh in role_of if role_of[fh] == "COURSE"]
cv = sum(len(media_by_folder.get(fh, [])) for fh in courses)
cd = sum(len(byfolder.get(fh, [])) for fh in courses)
print(f"TOTALS across {len(courses)} COURSE folders: {cv} videos, {cd} documents")
print(f"  (G0 §1 / Q8 describe FIVE courses, 78 files, 42 videos, 31 documents)")
print(f"  measured: {len(courses)} folders, {cv+cd} files, {cv} videos, {cd} documents")
print("  DISAGREEMENT IS RECORDED, NOT RECONCILED. Two candidate causes:")
print("    - 'course' here means any non-month, non-year folder, which also catches")
print("      container folders like 'NHB Bonuses' and '2. NHB+ Swipes'")
print("    - G0 counted 5 LEAF courses, not 5 folders")