#!/usr/bin/env python3
"""
DESIGN THE CLEAN NAMES from the data, and verify them.

Operator decision 2026-10-15: "we should rename them to be much cleaner and
better." This REVERSES the earlier locked decision to use MEGA filenames
verbatim. The cost of the reversal is traceability by filename, mitigated by
_meta/manifest.json carrying verbatim <-> clean for every unit.

Measured junk in the 230 audio names (this is the justification, not taste):
  ordinal prefix        65  (28.3%)
  underscores           28  (12.2%)
  'on <Topic>' suffix   14  ( 6.1%)
  _watermarked           5  ( 2.2%)
  '#N' part marker       5  ( 2.2%)
  ampersand             11  ( 4.8%)

Redundant on most files, because the VAULT is the NHB+ archive and the folder is
already calls/:
  'Call'               177/230  (77.0%)
  'NHB'/'NHB+'         165/230  (71.7%)
  'Theory'             108/230  (47.0%)

Date formats, unusable as-is: MM-DD-YYYY 114, M-D-YYYY 71, none 44, YYYY-MM-DD 1.

Run:  python design-names.py
"""
import json, os, re, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")
MN = ["January","February","March","April","May","June","July","August",
      "September","October","November","December"]
WINDOWS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
RESERVED = {"CON","PRN","AUX","NUL",*[f"COM{i}" for i in range(1,10)],
            *[f"LPT{i}" for i in range(1,10)]}

man = json.load(open(os.path.join(OUT, "manifest-v3.json"), encoding="utf-8"))
sc  = json.load(open(os.path.join(OUT, "scope-final.json"), encoding="utf-8"))

calls   = [u for u in man["units"] if u["kind"] == "calls"]
lessons = [u for u in man["units"] if u["kind"] == "lessons"]

# ------------------------------------------------------------------ cleaning
def strip_junk(s):
    s = re.sub(r"\s*_water\s?mark(ed)?\b", "", s, flags=re.I)   # 5 files
    s = re.sub(r"\s+\d{3,4}x\d{3,4}\b.*$", "", s)              # res+size tail
    s = re.sub(r"\s+\b\d{2,5}k\b", "", s)
    s = re.sub(r"[\[\]]", "", s)                                # stray brackets
    return s

def drop_lead(s):
    """Ordinal prefix, redundant brand, and the word 'Call'."""
    s = re.sub(r"^\s*\d{1,2}\s*[.)]\s*", "", s)                 # 65 files
    s = s.replace("FF_NHB+", "").replace("NHB+", "").replace("FF ", "")
    # `Mindstream` must NOT be in this alternation. With it, the regex ate the
    # whole phrase "NHB+ Mindstream Call" down to an empty stem, call_path
    # returned None, and the unit was dropped silently - fetched and transcribed
    # with no note. Only the generic word Call is removed.
    s = re.sub(r"\b(?:Theory|Coaching|Guest|Training|Mastermind)\s*Call\b", "", s, flags=re.I)
    s = re.sub(r"^\s*[-–—:]\s*", "", s)
    return s

def tidy(s):
    s = WINDOWS.sub("", s)
    # Normalise dash STYLES only. Adding a space where none existed turned
    # Ron-Lynch into "Ron - Lynch" across 50 of 229 paths. An ASCII hyphen
    # between word characters is left exactly as it is.
    s = re.sub(r"\s*[–—]\s*", " - ", s)                          # en/em -> spaced
    s = re.sub(r"\s+-\s+", " - ", s)                            # spaced hyphen
    s = re.sub(r"\s*&\s*", " & ", s)
    s = re.sub(r"\s+", " ", s).strip(" -.")
    s = re.sub(r"^(the|The)\s+", "", s)                         # 3 names start 'the'
    return s.strip()

def safe(name):
    stem = name.rsplit(".", 1)[0] if re.search(r"\.[A-Za-z0-9]{1,5}$", name) else name
    if stem.upper() in RESERVED: return False
    if name != name.strip(" .") or name.endswith((" ", ".")): return False
    return bool(name) and len(name) <= 180

# ------------------------------------------------------------- the two kinds
def call_path(u):
    """calls/<year>/<MM Month>/<YYYY-MM-DD> <Topic>.md
    The date comes from the MANIFEST, not the filename - which means the 44
    units whose MEGA name carries no date still get a sortable one."""
    s = strip_junk(u["media"]["name"])
    s = drop_lead(s)
    # strip a leading date in ANY of the observed formats
    s = re.sub(r"^\s*(?:\d{1,2}[-/.]\d{1,2}[-/.]\d{4}|\d{4}-\d{2}-\d{2})\s*[-–—:]*\s*", "", s)
    # the ISO branch above already existed but the corpus's ONLY ISO-dated name
    # still lost its date, so the ordering here is load-bearing
    s = tidy(s)
    # a trailing media extension in the STEM produced "....mp4.md", which
    # Obsidian renders as a note named "TSL Structures.mp4" - a media extension
    # inside a markdown vault, arriving by a route V6 does not check because the
    # FILE extension is .md. Strip it from the stem, not from the filename.
    s = re.sub(r"\.(mp3|mp4|m4a|mov|wav|flac|mkv|webm)$", "", s, flags=re.I).strip()
    d = u["date"]
    # Three calls carry date=None. Formatting that straight into the path
    # produced the literal filenames "None Selling To Women 3.0.md" and two
    # others - an INVENTED value in a path, which stage-0 forbids. A missing
    # date OMITS the prefix; the year/month folder still carries the sort.
    prefix = f"{d} " if d else ""
    return (f"calls/{u['year']}/{str(u['month']).zfill(2)} {MN[u['month']-1]}/"
            f"{prefix}{s}.md" if s else None), s, d

def lesson_path(u):
    """courses/<Course>/<NN> <Title>.md
    An ordinal prefix is USEFUL here - it is the lesson's position in the
    course, not an archive-listing artefact. That is the distinction the
    call cleaner misses."""
    s = strip_junk(u["media"]["name"])
    s = drop_lead(s)
    s = re.sub(r"^\s*\d{1,2}\s*[.)]\s*", "", s)                 # re-strip for lessons
    s = tidy(s)
    course = re.sub(r"^\s*\d+\.\s*", "", u["source_folder"]).strip()
    return course, s

# ------------------------------------------------------------------ build
print("=" * 78)
print("CLEAN NAMES FOR CALLS")
print("=" * 78)
call_rows, paths = [], defaultdict(list)
for u in sorted(calls, key=lambda x: (x["year"], x["month"], x["date"] or "")):
    p, topic, d = call_path(u)
    if not p:
        # Fall back to the unit's own topic slug. An empty stem must NEVER drop a
        # unit again - a silent `continue` here is how 188 became 187.
        p = f"calls/{u['year']}/{str(u['month']).zfill(2)} {MN[u['month']-1]}/" \
             f"{u['date']} {u.get('topic') or u['id']}.md"
        topic = u.get("topic") or u["id"]
        print(f"  EMPTY STEM, fell back to topic: {u['media']['name']!r} -> {p}")
    if not safe(p.rsplit("/", 1)[-1]):
        print(f"  UNSAFE: {u['media']['name']!r}  (skipped - no writable path)")
        continue
    call_rows.append({"handle": u["media"]["handle"], "verbatim": u["media"]["name"],
                      "path": p, "date": d, "topic": topic, "type": u["type"]})
    paths[p.rsplit("/", 1)[-1].casefold()].append(p)

for r in call_rows[:18]:
    print(f"  {r['verbatim'][:50]:<52} ->  {r['path'].rsplit('/',1)[-1][:52]}")
print(f"  ... {len(call_rows)} calls total")

coll = {k: v for k, v in paths.items() if len(v) > 1}
print(f"\n  COLLISIONS after cleaning: {len(coll)}")
for k, v in coll.items():
    print(f"    {k!r}")
    for p in v: print(f"      {p}")

print("\n" + "=" * 78)
print("CLEAN NAMES FOR COURSE LESSONS")
print("=" * 78)
lesson_rows, lpaths = [], defaultdict(list)
for u in sorted(lessons, key=lambda x: x["source_folder"]):
    course, title = lesson_path(u)
    n = sum(1 for r in lesson_rows if r["course"] == course) + 1
    fn = f"{n:02d} {title}.md"
    p = f"courses/{course}/{fn}"
    lesson_rows.append({"handle": u["media"]["handle"], "verbatim": u["media"]["name"],
                        "course": course, "path": p, "lesson_no": n})
    lpaths[fn.casefold()].append(p)
for r in lesson_rows[:16]:
    print(f"  {r['verbatim'][:44]:<46} ->  {r['path'][:56]}")
print(f"  ... {len(lesson_rows)} lessons total")
lcoll = {k: v for k, v in lpaths.items() if len(v) > 1}
print(f"\n  within-course filename collisions: {len(lcoll)}")

# ------------------------------------------------------------- documents
print("\n" + "=" * 78)
print("DOCUMENTS - collision groups are listed below and each is now prefixed")
print("=" * 78)
drows = []
for t in sc["targets"]:
    if t["kind"] == "audio": continue
    s = tidy(drop_lead(strip_junk(t["name"])))
    s = re.sub(r"\.(docx|xlsx|pptx|pdf|zip|txt|png)$", "", s, flags=re.I)
    drows.append({**t, "clean": s})

by_name = defaultdict(list)
for t in drows: by_name[t["clean"].casefold()].append(t)
dups = {k: v for k, v in by_name.items() if len(v) > 1}

# D4: the course prefix was computed and then DISCARDED - `dpaths` was built and
# never read, which is why five "Resources Links" still collided. Apply it. The
# five carry five distinct course values, so this genuinely disambiguates.
def course_slug(t):
    raw = (t.get("course") or t.get("folder") or "").strip()
    raw = re.sub(r"^\s*\d{1,2}\.\s*", "", raw)          # drop the ordinal
    raw = re.sub(r"\s*[-–—]\s*", " ", raw)
    raw = re.sub(r"\s+", " ", raw).strip()
    return safe(raw) and len(raw) <= 60 and raw or ""

for t in drows:
    n_coll = len(by_name[t["clean"].casefold()])
    slug = course_slug(t)
    if n_coll > 1 and slug:
        t["clean"] = f"{slug} {t['clean']}"

# D3: every document gets a REAL vault path. Without this, gate V8's assertion
# "every document has a path" is unfalsifiable - it can never pass, and the
# section 9 docs shakedown can never complete.
for t in drows:
    stem = re.sub(r"^\s*\d{1,2}\s*[.)]\s*", "", t["clean"]).strip()   # ordinal
    stem = re.sub(r"\s+(V\d+|v\d+)$", "", stem)                        # trailing version
    stem = safe(stem) and stem or f"document {t['handle']}"
    if t["kind"] == "written_hand":
        # written_hand targets in scope-final.json have NO date field. The date
        # is inside `unit`, e.g. "2024-03-07-theory-3-EqN2UTLK". Reading a field
        # that does not exist put all 37 in written-hands/undated/.
        u = t.get("unit") or ""
        iso = re.match(r"(\d{4})-(\d{2})-(\d{2})", u)
        y, mo = (iso.group(1), iso.group(2)) if iso else ("undated", "")
        # zero-padded: month folders ARE the sort mechanism, and `1 January`
        # sorts before `10 January` but after `12 December` without the pad.
        month = (f"{int(mo):02d} {MN[int(mo)-1]}"
                 if mo.isdigit() and 1 <= int(mo) <= 12 else "undated")
        t["path"] = f"written-hands/{y}/{month}/{stem}.md"
    else:
        slug = course_slug(t)
        t["path"] = (f"courses/{slug}/{stem}.md" if slug and t["kind"] == "course_doc"
                     else f"library/{stem}.md")

by_path = defaultdict(list)
for t in drows: by_path[t["path"].casefold()].append(t)
dpdups = {k: v for k, v in by_path.items() if len(v) > 1}
print(f"  documents with a path        : {sum(1 for t in drows if t.get('path'))} of {len(drows)}")
print(f"  document PATH collisions     : {len(dpdups)}")
print(f"  distinct cleaned names: {len(by_name)} of {len(drows)}")
print(f"  COLLISIONS: {len(dups)}")
for k, v in dups.items():
    print(f"\n    {k!r}")
    for t in v:
        print(f"      kind={t['kind']:<13} {t['handle']}  {t['name'][:52]}")

print("\n" + "=" * 78)
print("VERIFY")
print("=" * 78)
allp = ([r["path"] for r in call_rows] + [r["path"] for r in lesson_rows]
        + [t["path"] for t in drows])
print(f"  total clean paths   : {len(allp)}")
print(f"  all casefold-unique : {len({p.casefold() for p in allp}) == len(allp)}")
bad = [p for p in allp if WINDOWS.search(p.rsplit('/',1)[-1]) or not safe(p.rsplit('/',1)[-1])]
print(f"  unwritable on Windows: {len(bad)}")
longest = sorted(allp, key=len, reverse=True)[:3]
print("  longest paths:")
for p in longest: print(f"    {len(p):>3}  {p}")

out = {"calls": call_rows, "lessons": lesson_rows,
       "documents": [{"handle": t["handle"], "verbatim": t["name"],
                      "kind": t["kind"], "clean": t["clean"],
                      "path": t["path"]} for t in drows],
       "collisions": {"calls": len(coll), "lessons": len(lcoll),
                      "documents": len(dups), "document_paths": len(dpdups)},
       "decision": "2026-10-15 operator: clean names, NOT verbatim MEGA filenames. "
                   "Verbatim preserved in _meta/manifest.json for every unit."}
json.dump(out, open(os.path.join(OUT, "clean-names.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print(f"\nWRITTEN {os.path.join(OUT, 'clean-names.json')}")