#!/usr/bin/env python3
"""R3 T4: recompute every number in §10.2 / §15 from clean-names.json."""
import json, os, re, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def jload(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)

cn = jload(os.path.join(OD, "clean-names.json"))
man = jload(os.path.join(OD, "manifest-v3.json"))
sc  = jload(os.path.join(OD, "scope-final.json"))
units = man["units"]

calls = cn["calls"]
lessons = cn["lessons"]
docs = cn["documents"]
print("clean-names.json keys :", list(cn.keys()))
print("calls / lessons / docs :", len(calls), len(lessons), len(docs))
print("collisions            :", cn["collisions"])
print("keys, call row        :", sorted(calls[0].keys()))
print("keys, doc row         :", sorted(docs[0].keys()))
print("keys, lesson row      :", sorted(lessons[0].keys()))

print()
print("=" * 78)
print("1. ' - ' IN NAMES  (spec: 67/296, 23%)")
print("=" * 78)
def stem(name):
    return name.rsplit(".", 1)[0] if re.search(r"\.[A-Za-z0-9]{1,5}$", name) else name

call_dash = [c for c in calls if " - " in stem(c["verbatim"])]
les_dash  = [l for l in lessons if " - " in stem(l["verbatim"])]
doc_dash  = [d for d in docs if " - " in stem(d["verbatim"])]
tot_names = len(calls) + len(lessons) + len(docs)
print(f"  verbatim names total        : {tot_names}  (spec says 296)")
print(f"  verbatim ' - ' calls        : {len(call_dash)}")
print(f"  verbatim ' - ' lessons      : {len(les_dash)}")
print(f"  verbatim ' - ' documents    : {len(doc_dash)}")
print(f"  TOTAL ' - '                 : {len(call_dash)+len(les_dash)+len(doc_dash)} "
      f"= {100*(len(call_dash)+len(les_dash)+len(doc_dash))/tot_names:.1f}%")
print(f"  CLEAN names still ' - '     : "
      f"{sum(1 for c in calls if ' - ' in c['path'])} calls, "
      f"{sum(1 for l in lessons if ' - ' in l['path'])} lessons, "
      f"{sum(1 for d in docs if ' - ' in d['clean'])} docs")
dbl = [c for c in calls if re.search(r"\s-\s-\s", c["verbatim"])]
print(f"  double-hyphen ' - - ' artifacts: {len(dbl)}")
for c in dbl[:5]:
    print(f"     {c['verbatim'][:70]!r} -> {c['path'].rsplit('/',1)[-1][:70]!r}")
intra = [c for c in calls if re.search(r"[A-Za-z]-[A-Za-z]", stem(c["verbatim"]))]
print(f"  intra-word hyphen names (must NOT be split): {len(intra)}")
for c in intra[:8]:
    print(f"     {c['verbatim'][:66]!r} -> {c['path'].rsplit('/',1)[-1][:66]!r}")
# how many clean paths actually contain a mangled ' - - ' or ' -  - '
mangled = [c for c in calls
           if re.search(r"\s-\s(-\s|-\s*-)", c["path"].rsplit('/',1)[-1])]
print(f"  clean filenames containing ' - ' twice adjacent (mangled): {len(mangled)}")

print()
print("=" * 78)
print("2. 'None' IN NAMES  (spec: 3 filenames)")
print("=" * 78)
for label, rows, key in [("calls", calls, "path"), ("lessons", lessons, "path"),
                         ("documents", docs, "clean")]:
    hits = [r for r in rows if re.search(r"\bNone\b", r[key])]
    print(f"  {label:<10} 'None' in emitted name: {len(hits)}")
    for r in hits[:6]:
        print(f"     {r['verbatim'][:64]!r} -> {r[key][:64]!r}")
# and in the vault path (date prefix)
none_date = [c for c in calls if re.search(r"\bNone\b", c["path"])]
print(f"  calls whose PATH contains 'None' (date=None leaked): {len(none_date)}")
for c in none_date[:8]:
    print(f"     date={c['date']!r} {c['path']}")

print()
print("=" * 78)
print("3. EXTENSION-IN-STEM  (spec: 2 x .mp4.md)")
print("=" * 78)
MEDIA_EXT = r"\.(mp3|mp4|mov|m4a|m4v|wav|flac|mkv|webm|mka|aac|opus|ogg)$"
for label, rows, key in [("calls", calls, "path"), ("lessons", lessons, "path"),
                         ("documents", docs, "clean")]:
    hits = [r for r in rows if re.search(MEDIA_EXT, stem(r[key]), re.I)]
    print(f"  {label:<10} media ext in emitted stem: {len(hits)}")
    for r in hits[:6]:
        print(f"     {r['verbatim'][:60]!r} -> {r[key][:60]!r}")
# what a real emitted path looks like for the mp4 units
mp4rows = [c for c in calls if c.get("verbatim","").lower().endswith(".mp4")]
print(f"  call verbatims ending .mp4: {len(mp4rows)}")
for r in mp4rows[:4]:
    print(f"     {r['verbatim'][:60]!r} -> {r['path'][:70]}")

print()
print("=" * 78)
print("4. COLLISIONS  (spec: 5 'Resources Links' collide; collisions.documents = 1)")
print("=" * 78)
print(f"  clean-names collisions block: {cn['collisions']}")
bystems = defaultdict(list)
for d in docs:
    bystems[d["clean"].casefold()].append(d)
dups = {k: v for k, v in bystems.items() if len(v) > 1}
print(f"  recomputed document collisions: {len(dups)}")
for k, v in dups.items():
    print(f"     {k!r}  n={len(v)}")
    for d in v:
        print(f"        kind={d['kind']:<13} {d['handle']}  {d['verbatim'][:56]}")
print(f"  'Resources Links' documents: "
      f"{sum(1 for d in docs if 'resource' in d['verbatim'].casefold())}")

print()
print("=" * 78)
print("5. THE DROPPED CALL  (spec: 187 paths not 188; Mindstream)")
print("=" * 78)
print(f"  units in manifest: {len(units)}   call_rows emitted: {len(calls)}")
emitted = {c["handle"] for c in calls}
allh    = {u["media"]["handle"] for u in units}
missing = [u for u in units if u["media"]["handle"] not in emitted]
print(f"  manifest units with NO emitted call row: {len(missing)}")
for u in missing:
    print(f"     {u['media']['handle']} kind={u['kind']} {u['media']['name'][:66]!r}")
print(f"  lesson rows: {len(lessons)} ; manifest lessons: "
      f"{sum(1 for u in units if u['kind']=='lessons')}")
miss_l = [u for u in units if u["kind"] == "lessons"
          and u["media"]["handle"] not in {l['handle'] for l in lessons}]
print(f"  lessons with no emitted row: {len(miss_l)}")
for u in miss_l[:10]:
    print(f"     {u['media']['handle']}  {u['media']['name'][:66]!r}")

print()
print("=" * 78)
print("6. UNDATED CALLS  (spec: 3, undated-other-9/-5/-5)")
print("=" * 78)
und = [u for u in units if u["kind"] == "calls" and not u["date"]]
print(f"  manifest calls with date=None: {len(und)}")
for u in und:
    print(f"     {u['date']!r} dated_from={u['dated_from']:<14} year={u['year']} "
          f"month={u['month']} label={u['folder_label']!r}")
    print(f"        {u['media']['name'][:70]}")
callrows_nodate = [c for c in calls if not c.get("date")]
print(f"  call rows with empty date: {len(callrows_nodate)}")
for c in callrows_nodate[:10]:
    print(f"     {c['handle']} {c['path']}")

print()
print("=" * 78)
print("7. CALL STEM vs WRITTEN-HAND STEM COLLISIONS")
print("=" * 78)
wh = [d for d in docs if d["kind"] == "written_hand"]
print(f"  written_hand docs: {len(wh)}")
# derive hand stems from the call the plan links them to
by_unit = {u["id"]: u for u in units}
tgt_by_handle = {t["handle"]: t for t in sc["targets"]}
exact = []
for d in wh:
    t = tgt_by_handle.get(d["handle"])
    if not t or "unit" not in t:
        continue
    u = by_unit.get(t["unit"])
    if not u:
        continue
    # hand's own clean stem vs call's clean path stem
    callrow = next((c for c in calls if c["handle"] == u["media"]["handle"]), None)
    if not callrow:
        continue
    hs = d["clean"].casefold()
    cs = callrow["path"].rsplit("/", 1)[-1][:-3].casefold()
    if hs == cs:
        exact.append((d, callrow))
print(f"  hand clean stem EXACTLY equal to a call note stem: {len(exact)}")
for d, c in exact[:10]:
    print(f"     {d['verbatim'][:56]!r}  ==  {c['path'].rsplit('/',1)[-1]!r}")
# also: hand stems equal to ANY other hand's stem
hb = defaultdict(list)
for d in wh:
    hb[d["clean"].casefold()].append(d)
print(f"  hand stems duplicated among hands: "
     f"{ {k: len(v) for k, v in hb.items() if len(v) > 1} }")
# hand stems equal to course_doc / orphan doc stems
other = {d["clean"].casefold() for d in docs if d["kind"] != "written_hand"}
cross = [d for d in wh if d["clean"].casefold() in other]
print(f"  hand stems colliding with a non-hand document stem: {len(cross)}")
for d in cross[:6]:
    print(f"     {d['clean']!r}")
# hand stems equal to any call stem (not just its own)
callstems = {c["path"].rsplit("/", 1)[-1][:-3].casefold() for c in calls}
print(f"  hand stems equal to ANY call stem: "
      f"{sum(1 for d in wh if d['clean'].casefold() in callstems)}")

print()
print("=" * 78)
print("8. LESSON ORDINALS / COURSE PREFIX  (spec: 7. AC -> 02; 5 Resources Links)")
print("=" * 78)
lc = cn["collisions"]["lessons"]
print(f"  within-course filename collisions reported by script: {lc}")
bycourse = defaultdict(list)
for l in lessons:
    bycourse[l["course"]].append(l)
print(f"  courses: {len(bycourse)}")
for c in sorted(bycourse):
    rows = bycourse[c]
    nos = [r["lesson_no"] for r in rows]
    print(f"     {c[:44]:<46} n={len(rows):<3} lesson_no={nos if len(nos)<14 else '...'}")
    dupes = [n for n in set(nos) if nos.count(n) > 1]
    if dupes:
        print(f"        DUPLICATE lesson_no {dupes}")
# how many lesson paths have a lesson_no that renumbers the source ordinal
renum = 0
for l in lessons:
    m = re.match(r"^\s*(\d{1,2})\s*[.)]\s*", l["verbatim"])
    if m and int(m.group(1)) != l["lesson_no"]:
        renum += 1
print(f"  lessons where source ordinal != emitted lesson_no: {renum}")

print()
print("=" * 78)
print("9. DATES / ISO  (spec: accept YYYY-MM-DD; the one ISO name lost its date)")
print("=" * 78)
iso = [c for c in calls if re.match(r"^\d{4}-\d{2}-\d{2}", stem(c["verbatim"]))]
print(f"  call verbatims starting YYYY-MM-DD: {len(iso)}")
for c in iso:
    print(f"     {c['verbatim'][:64]!r} -> date={c['date']!r} {c['path']}")

print()
print("=" * 78)
print("10. BRAND TOKENS / UNDERSCORES SURVIVING (spec: 23 brand, 4 underscores)")
print("=" * 78)
brand = [c for c in calls if re.search(r"\b(NHB|FF|Nothing Held Back)\b", c["path"])]
und   = [c for c in calls if "_" in c["path"].rsplit("/",1)[-1]]
print(f"  call paths still carrying NHB/FF: {len(brand)}")
for c in brand[:6]:
    print(f"     {c['path'].rsplit('/',1)[-1][:70]}")
print(f"  call filenames still carrying '_': {len(und)}")
for c in und[:6]:
    print(f"     {c['path'].rsplit('/',1)[-1][:70]}")
amp = [c for c in calls if "&" in c["path"].rsplit("/",1)[-1]]
print(f"  call filenames still carrying '&' (spec says normalise): {len(amp)}")

print()
print("=" * 78)
print("11. PATH KEY ON DOCUMENTS  (V8 / §10 'every documented output location needs a path')")
print("=" * 78)
have_path = sum(1 for d in docs if "path" in d)
print(f"  document rows carrying a 'path' key: {have_path} of {len(docs)}")
print(f"  document row keys: {sorted(docs[0].keys())}")
print(f"  call rows with 'path': {sum(1 for c in calls if 'path' in c)}/{len(calls)}")
print(f"  lesson rows with 'path': {sum(1 for l in lessons if 'path' in l)}/{len(lessons)}")
print("  grep pipeline/scripts for a write of a document 'path': see t3 grep")
