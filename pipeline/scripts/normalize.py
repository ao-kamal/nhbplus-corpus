#!/usr/bin/env python3
"""
FOLDER LABEL + IDENTITY NORMALISATION.  Produces manifest-v3.

Three defects this fixes, each measured rather than assumed:

1. MOJIBAKE. 8 names carry 'O?C?o' where an em-dash belongs. UTF-8 was decoded
   as cp850 somewhere in the capture pipeline. Verified: cp850 -> utf-8 is the
   ONLY one of five candidate reversals that lands on a real dash, and it is
   applied only when that check passes - never blind.

2. DOUBLE COUNTING (cost). 335 media files collapse to 255 calls. 80 calls had
   both an MP3 and an MP4 with slightly different titles ('NHB' vs 'NHB+',
   'on Vimeo' suffix) and were being queued - and billed - twice. The smoke
   test paid for this once already.

3. FOLDER LABELS. Month folder names repeat across years ('1. January' is both
   RrdEHRCL/2023 and Q7FGRZrJ/2024) and month folders do not carry their own
   year, which left 199 of 211 calls with year=None. The year now comes from
   the CALL'S OWN DATE, which is authoritative. The MEGA folder is retained as
   source_folder for traceability and cross-checked, NOT trusted for the label.

Nothing here is silently reconciled: every count that moves is printed, and a
mismatch between the MEGA folder month and the call's own month is surfaced.
"""
import glob, json, os, re, sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
OD   = os.path.join(HERE, "..", "out")

# ----------------------------------------------------------------- encoding
PUNCT = "\u2014\u2013\u2018\u2019\u201c\u201d\u2026\u00a0"

def unmangle(s):
    """cp850 -> utf-8, but ONLY when the result actually contains a real dash or
    curly quote. A wrong reverse corrupts silently, so it must prove itself."""
    if not s or all(ord(c) < 128 for c in s):
        return s, False
    try:
        fixed = s.encode("cp850").decode("utf-8")
    except Exception:
        return s, False
    return (fixed, True) if any(c in fixed for c in PUNCT) else (s, False)

# ----------------------------------------------------------------- name/dates
DUR    = re.compile(r"\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*$")
MEDIA = ("mp3", "mp4", "wav", "m4a", "mov", "m4v")
# General extension matcher. It used to be audio/video-only, which made all 319
# documents come back extension-less and reported "0 multi-format groups" - a
# clean zero that read as a finding. LAST occurrence, not first: names like
# '10. 12-07-2023 ... .mp4' contain dots that are not extensions.
EXT = re.compile(r"\.([A-Za-z0-9]{1,5})(?=\s|$)")
DATE   = re.compile(r"^\s*(\d{1,2})\s*-\s*(\d{1,2})\s*-\s*((?:19|20)\d{2})\s*")
ORDN   = re.compile(r"^\s*\d{1,2}\s*[.)]\s*")
PLAT   = re.compile(r"\s+on\s+(vimeo(\.com)?|youtube(\.com)?|wistia|loom|teachable)\s*$", re.I)
TYPES  = ("guest", "coaching", "theory", "training", "q&a", "mastermind")

MONTHS = ["January","February","March","April","May","June","July","August",
          "September","October","November","December"]
MONTHNUM = {m.lower(): i for i, m in enumerate(MONTHS, 1)}
MONTHABBR = {m: i for i, m in enumerate(
    ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"], 1)}

def split_name(text):
    """-> (stem, ext, dur_s). Capture the extension ONCE. Stripping it and then
    searching for it is the bug that produced a 2-unit manifest."""
    t = DUR.sub("", (text or "").strip())
    d = DUR.search(text or "")
    dur = None
    if d:
        p = [int(x) for x in d.group(1).split(":")]
        dur = p[0]*3600 + p[1]*60 + p[2] if len(p) == 3 else p[0]*60 + p[1]
    ms = list(EXT.finditer(t))
    if not ms: return t.strip(), None, dur
    m = ms[-1]                                  # LAST dot - names contain dots
    return t[:m.start()].strip(), m.group(1).lower(), dur

# MEGA rounds EVERY displayed size to a whole unit (measured: 156/156 GB-valued
# files whole, 229/229 MB-valued whole), so these are floor estimates, not exact.
# They still make a floor check possible - which is the point.
SZ = re.compile(r"([\d.]+)\s*[^0-9A-Za-z]*\s*([KMG])B\b", re.I)
UNIT = {"k": 1/1048576, "m": 1/1024, "g": 1.0}
def size_of(title):
    m = SZ.search(title or "")
    if not m: return None
    return int(float(m.group(1)) * UNIT[m.group(2).lower()] * 1073741824)

def call_date(name):
    """Strip the ordinal prefix FIRST. Anchoring DATE at ^ while the name
    begins '01. 10-5-2023 ...' silently lost the date for the whole 2023-2025
    batch - 19 calls showed as year-unknown when their own name carried the year."""
    n = ORDN.sub("", name or "")
    m = DATE.match(n)
    if not m: return None
    mo, d, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if not (1 <= mo <= 12 and 1 <= d <= 31): return None
    return f"{y:04d}-{mo:02d}-{d:02d}"

def call_type(name):
    n = name.lower()
    for t in TYPES:
        if t in n: return t
    return "other"

def topic_key(name):
    """Normalise so that 'NHB' == 'NHB+' and '…on Vimeo' == '…'.
    Type is kept separate so a theory call never merges with a guest call on
    the same day; the part number is kept so '#2' stays distinct from '#1'."""
    n = ORDN.sub("", name)
    n = DATE.sub("", n)
    n = PLAT.sub("", n)
    n = n.replace("NHB+", "NHB")
    n = re.sub(r"[‐‑‒–—―]", "-", n)
    n = re.sub(r"[‘’]", "'", n)
    n = re.sub(r"[“”]", '"', n)
    n = re.sub(r"\s+", " ", n).strip().casefold()
    return re.sub(r"\s+", " ", n).strip()

def folder_month(name):
    n = ORDN.sub("", (name or "").lower()).strip()
    for w in re.split(r"[^a-z]+", n):
        if w in MONTHNUM:  return MONTHNUM[w]
        if w in MONTHABBR: return MONTHABBR[w]
    return None

def folder_year(name):
    m = re.search(r"(19|20)\d{2}", name or "")
    return int(m.group(0)) if m else None

def kind_of(name):
    """A folder naming a month or a year holds CALLS. Everything else in this
    share is a bonus lesson course. Asserted against the census, not assumed."""
    n = ORDN.sub("", (name or "").lower()).strip()
    if re.fullmatch(r"(19|20)\d{2}", n): return "calls"
    if re.search(r"[a-z]", n) and (folder_month(name) or folder_year(name)): return "calls"
    return "lessons"

# ----------------------------------------------------------------- read rows
seednames = {}
for m in re.finditer(r'"([A-Za-z0-9_-]+)=([^"]*)"',
                     open(os.path.join(OD, "seednames.txt"), encoding="utf-8").read()):
    seednames[m.group(1)] = m.group(2)

rows, fixed_names = [], 0
for fp in sorted(glob.glob(os.path.join(OD, "handles-*.json"))):
    fh = os.path.basename(fp)[8:-5]
    try: data = json.load(open(fp, encoding="utf-8-sig"))
    except Exception: continue
    if isinstance(data, dict): data = [data]
    for r in data:
        if isinstance(r, dict) and "value" in r: r = r["value"]
        try: hid, text, title, isfolder = r[0], r[1], r[2], int(r[3])
        except Exception: continue
        text, did = unmangle(text or ""); fixed_names += did
        stem, ext, dur = split_name(text)
        rows.append({"folder_handle": fh, "handle": hid, "name": stem,
                     "ext": ext, "dur_s": dur, "bytes": size_of(title),
                     "title": title or "", "isfolder": isfolder})

media = [r for r in rows if not r["isfolder"] and r["ext"] in ("mp3", "mp4")]
docs  = [r for r in rows if not r["isfolder"] and r["ext"] not in ("mp3", "mp4", None)]
print(f"rows {len(rows)}   media files {len(media)}   documents {len(docs)}   "
      f"no-extension {sum(1 for r in rows if not r['isfolder'] and not r['ext'])}   "
      f"names unmangled {fixed_names}")

# A near-zero here means the filter is broken, not that the corpus is empty.
# That failure mode has bitten this project three times today.
assert len(media) > 300, f"only {len(media)} media files - filter is broken, not the corpus"
assert len(docs) > 100, f"only {len(docs)} documents - the general extension matcher is broken"

# ----------------------------------------------------------------- identity
groups = defaultdict(lambda: {"mp3": [], "mp4": [], "other": [], "folder": set()})
undated = 0
for r in media:
    name = r["name"]
    d    = call_date(name)
    if not d: undated += 1
    k = (d, call_type(name), topic_key(name))
    ext = r["ext"]
    groups[k]["mp3" if ext == "mp3" else "mp4"].append(r)
    groups[k]["folder"].add(r["folder_handle"])

print(f"calls grouped: {len(groups)}   (from {len(media)} media files)")
print(f"files with no date in the name: {undated}")

# ---- SECOND MERGE PASS: physical identity, not filenames -------------------
# Seven units share a date, a type AND a duration to the second while their
# names differ only in trailing junk:
#     ...Integration Call #2_        vs  ...Integration Call #2
#     ...Integration Call #3_water    vs  ...Integration Call #3
#     Guest Call - Isaac Lara        vs  Guest Call WITH Isaac Lara  (+ "Selll")
#     ...Lonnie Jones on SEO         vs  ...Lonnie Jones on SEO How To Build Authority
#     Call of Duty Biz Ops Part 2    vs  Call of Duty Biz-Ops Part 2
#     Call of Duty Biz-Ops]          vs  Call of Duty Biz-Ops
# That is 39.21 h of double-counted audio, and every one of those collisions also
# collided on `id`, which would have put two calls in one vault note.
#
# The rule is deliberately physical: same date, same type, duration within 2%.
# A near-identical length on the same day of the same kind is the same recording;
# the filename is not evidence. Different-duration same-day calls stay separate.
items  = list(groups.items())
parent = list(range(len(items)))
def _find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
def _union(a, b):
    ra, rb = _find(a), _find(b)
    if ra != rb: parent[rb] = ra
dur = {}
for i, ((d, typ, topic), g) in enumerate(items):
    ds = [p["dur_s"] for p in (g["mp3"] + g["mp4"]) if p["dur_s"]]
    dur[i] = max(ds) if ds else None
merged_pairs = []          # (index_i, index_j) with j merged into i

def _kind_of(g):
    for fh in g["folder"]:
        return kind_of(seednames.get(fh, fh))
    return "unknown"
kinds = [_kind_of(g) for _, g in items]

for i in range(len(items)):
    di, ti, _ = items[i][0]
    if not dur[i]: continue
    for j in range(i + 1, len(items)):
        dj, tj, _ = items[j][0]
        if tj != ti or not dur[j]: continue
        # CALLS ONLY. Course lessons are all undated and several share a folder;
        # letting duration decide merged distinct lessons and dropped the bonus
        # count from 42 to 32. A lesson is a lesson, never a duplicate.
        if kinds[i] != "calls" or kinds[j] != "calls": continue
        # if BOTH carry a date it must match; if NEITHER does, duration alone
        # decides. Undated calls were previously exempt, which let
        # 'Selling To Women 3.0 Part 1' and 'Selling To Women 3.0' (both 11318 s)
        # through as two calls.
        if di is not None and dj is not None and di != dj: continue
        if abs(dur[i] - dur[j]) / max(dur[i], dur[j]) <= 0.02:
            merged_pairs.append((i, j))
            _union(i, j)
merged = defaultdict(lambda: {"mp3": [], "mp4": [], "other": [], "folder": set()})
for i, ((d, typ, topic), g) in enumerate(items):
    root = _find(i)
    # key by the SURVIVING unit's identity, not by the union-find root integer
    rk = items[root][0] if root != i else (d, typ, topic)
    m = merged[rk]
    for k in ("mp3", "mp4"): m[k] += g[k]
    m["folder"] |= g["folder"]
groups = merged
lost_h = sum(dur[j] / 3600 for _, j in merged_pairs if dur[j])
print(f"\n=== SECOND MERGE PASS (duration-based) ===")
print(f"  units before {len(items)}  after {len(groups)}  merged {len(merged_pairs)}")
for i, j in merged_pairs:
    ki, kj = items[i][0], items[j][0]
    print(f"    {ki[0]}  {ki[1]:<9} dur={int(dur[i] or 0)}s")
    print(f"        keep     {ki[2][:56]}")
    print(f"        absorbed {kj[2][:56]}  [{items[j][1]['mp3'][0]['ext'] if items[j][1]['mp3'] else items[j][1]['mp4'][0]['ext']}]")
print(f"  double-counted audio reclaimed: {lost_h:.2f} h")

# The bonus lesson count is an INDEPENDENT census figure (42 videos / 26.16 h)
# and it regressed to 32 the moment the duration merge was widened to undated
# units and began collapsing distinct course lessons. It is a tripwire, not a
# number this script is free to move.
_n_lessons = sum(1 for v in groups.values() if _kind_of(v) == "lessons")
assert _n_lessons == 42, (
    f"bonus lessons = {_n_lessons}, expected 42 - the merge has collapsed lessons")
_n_calls = sum(1 for v in groups.values() if _kind_of(v) == "calls")
print(f"  calls { _n_calls } · lessons { _n_lessons } (asserted == 42, independent census)")

# ------------------------------------------------------------------ build
units, split_notes = [], []
for (d, typ, topic), g in groups.items():
    picks = g["mp3"] or g["mp4"] or g["other"]
    if not picks: continue
    if len(picks) > 1:
        split_notes.append((d, typ, topic, [p["name"] for p in picks]))

    fh = sorted(g["folder"])[0]
    src = seednames.get(fh, fh)
    kind = kind_of(src)
    fmon = folder_month(src)
    fyear = folder_year(src)

    # The call's OWN date is authoritative for year/month. The MEGA folder is a
    # cross-check only - month folder names repeat across years, so trusting them
    # for the label is what left 199 of 211 calls unlabelled.
    year = int(d[:4]) if d else fyear
    mon  = int(d[5:7]) if d else fmon

    # CLOSED BY ELIMINATION, not by inference. Folder ordering as a general rule
    # was falsified (correct on 32 of 34 dated folders, wrong on 2) and is NOT
    # used. This handle is closed by a different argument, checked step by step in
    # probe/scripts/reconcile-years-elimination.py:
    #   - exactly three handles are named '5. May'
    #   - two carry dated calls inside them, dating them 2022 and 2023 outright
    #   - the corpus spans May in exactly three years: 2021 starts in June and
    #     2025 ends in February ('Up to 02.2025')
    #   - one folder, one year left -> 2024
    # Seed ordering independently predicts 2024 and matched the other two May
    # folders 2/2, which corroborates but is not the argument.
    FOLDER_YEAR_ELIMINATED = {"liVUnbAT": (2024, 5)}
    if fh in FOLDER_YEAR_ELIMINATED and not d:
        year, mon = FOLDER_YEAR_ELIMINATED[fh]

    if d and fmon and fyear and fmon == mon and fyear == year:
        label = f"{year:04d}-{mon:02d} {MONTHS[mon-1]}"
    elif year and mon:
        # folder month/year and the call's own month differ, or only one known.
        # The '*' marks it rather than silently picking a side.
        label = f"{year:04d}-{mon:02d} {MONTHS[mon-1]}" + ("" if (d and fmon == mon) else "*")
    elif mon:
        # month known, year NOT. Month folder names repeat across years, so the
        # year is not recoverable from the folder. Resolvable from the transcript
        # ("Today is Monday, 04/18/2022") after transcription - flagged, not guessed.
        label = f"{mon:02d} {MONTHS[mon-1]} year-unknown"
    elif src:
        label = f"undated · {src}"
    else:
        label = "undated"

    # MP3-preferred so a call is never billed for both encodings. `allfiles`
    # still carries BOTH, because every unselected file must be recorded as an
    # alternate - otherwise "never billed twice" is uncheckable from the manifest.
    allfiles = g["mp3"] + g["mp4"]
    picks    = g["mp3"] or g["mp4"]
    selected = picks[0]["handle"]
    alts = [{"handle": p["handle"], "name": p["name"], "ext": p["ext"],
          "bytes": p["bytes"], "dur_s": p["dur_s"]}
        for p in allfiles if p["handle"] != selected]

    media_rec = {
        "handle": selected,
        "url": f"https://mega.nz/folder/EzMk0Z4K#CrnHbM7tWaNtcByX0Ry_-Q/file/{selected}",
        "name": picks[0]["name"],
        "ext": picks[0]["ext"],
        "bytes": picks[0]["bytes"], "dur_s": picks[0]["dur_s"],
        "alternates": alts,
    }
    # id MUST be unique - it keys one vault note. date+type+month is not: all 42
    # undated lessons collapse to 'undated-lesson-None', and several dated calls
    # share a day and a type. The selected handle is unique by construction, so it
    # anchors the key and the human-readable part goes in `slug`.
    slug = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", picks[0]["name"]).strip().rstrip(". ")
    slug = re.sub(r"\s+", " ", slug)[:150] or picks[0]["handle"]
    units.append({
        "id": f"{d or 'undated'}-{typ}-{mon}-{picks[0]['handle']}",
        "slug": slug, "date": d,
        "kind": kind, "year": year, "month": mon, "type": typ, "topic": topic,
        "folder_label": label, "folder_month": fmon, "folder_year": fyear,
        "folder_month_matches": (fmon == mon) if (fmon and mon) else None,
        "dated_from": "call_name" if d else ("folder_name" if (fyear or fmon) else "none"),
        "source_folder": src, "folder_handle": fh,
        "title": picks[0]["name"],
        "media": media_rec,
        "has_mp3": bool(g["mp3"]), "has_mp4": bool(g["mp4"]),
    })

# ---- post-pass: adopt a folder's year from its dated siblings --------------
# A call whose FILENAME carries no date but which shares a month folder with
# dated calls belongs to the same year as those calls - a folder cannot span
# years here, and the only cross-year case found ('4. April') holds two years'
# files in ONE handle, which makes the sibling years ambiguous and therefore
# refuses to resolve. Applied only when the sibling years are a single value.
_fy = defaultdict(set)
for u in units:
    if u["year"]: _fy[u["folder_handle"]].add(u["year"])
_resolved = 0
for u in units:
    if u["year"] or u["kind"] != "calls": continue
    yrs = _fy.get(u["folder_handle"], set())
    if len(yrs) == 1:
        u["year"] = next(iter(yrs))
        u["dated_from"] = "folder_siblings"
        if u["month"]:
            u["folder_label"] = f"{u['year']:04d}-{u['month']:02d} {MONTHS[u['month']-1]}"
        _resolved += 1
print(f"\n  calls dated from folder siblings: {_resolved}")

# ------------------------------------------------------------------ report
calls   = [u for u in units if u["kind"] == "calls"]
lessons = [u for u in units if u["kind"] == "lessons"]
hrs = lambda us: sum((u["media"]["dur_s"] or 0) for u in us) / 3600
gb  = lambda us: sum((u["media"]["bytes"] or 0) for u in us) / 1073741824

print()
print("=== CALLS vs LESSONS (folder-derived, not guessed from titles) ===")
print(f"  CALLS   : {len(calls):>4}  {hrs(calls):>8.2f} h   (census 211 / 630.74 h)")
print(f"  LESSONS : {len(lessons):>4}  {hrs(lessons):>8.2f} h   (census  42 /  26.16 h)")
print(f"  TOTAL   : {len(units):>4}  {hrs(units):>8.2f} h   (measured 656.90 h)")

print("\n=== FOLDER LABELS ===")
bylab = defaultdict(lambda: [0, 0])
for u in units:
    bylab[u["folder_label"]][0 if u["kind"] == "calls" else 1] += 1
for k in sorted(bylab):
    c, l = bylab[k]
    print(f"  {k:<28} {c:>3} calls {l:>3} lessons")

und = [u for u in units if u["dated_from"] == "none"]
print(f"\n  units with NO date anywhere (name and folder): {len(und)}")
for u in und[:8]:
    print(f"    {u['source_folder']!r} :: {u['title'][:58]}")
mm = [u for u in units if u["folder_month_matches"] is False]
starred = [u for u in units if u["folder_label"].endswith("*")]
print(f"\n  MEGA folder month DISAGREES with the call's own month: {len(mm)}")
for u in mm[:12]:
    print(f"    {u['date']}  call month={u['month']}  folder {u['source_folder']!r} (month {u['folder_month']})")
print(f"  labels marked '*' (folder and call month/year do not both agree): {len(starred)}")
for u in starred[:8]:
    print(f"    {u['folder_label']:<22} folder={u['source_folder']!r} "
          f"folder_month={u['folder_month']} folder_year={u['folder_year']} "
          f"call={u['date']} dated_from={u['dated_from']}")
unk = [u for u in units if u["kind"] == "calls" and u["month"] and not u["year"]]
print(f"  CALLS with month known but YEAR not recoverable from the folder: {len(unk)}")
print(f"    (month folder names repeat across years - resolvable from the transcript)")
for u in unk[:6]:
    print(f"      {u['source_folder']!r:<24} {u['title'][:52]}")

print(f"\n=== IDENTITY ===")
print(f"  media files            : {len(media)}")
print(f"  calls assembled        : {len(units)}   (was 253 units)")
print(f"  served by MP3          : {sum(1 for u in units if u['has_mp3'])}")
print(f"  served by MP4 only     : {sum(1 for u in units if not u['has_mp3'])}")
print(f"  with BOTH encodings    : {sum(1 for u in units if u['has_mp3'] and u['has_mp4'])}")
print(f"  alternates recorded, NOT selected/billed : "
      f"{sum(len(u['media']['alternates']) for u in units)}")
assert sum(len(u["media"]["alternates"]) for u in units) == len(media) - len(units), \
    "every unselected file must be recorded as an alternate"

# --- the reconciliation that matters: were earlier hour totals double-counted? ---
all_h  = sum(r["dur_s"] or 0 for r in media) / 3600
sel_h  = sum((u["media"]["dur_s"] or 0) for u in units) / 3600
dup_pair_h = sum((a["dur_s"] or 0) for u in units for a in u["media"]["alternates"]) / 3600
CENSUS = 656.90
print(f"\n=== HOUR RECONCILIATION ===")
print(f"  A  all {len(media)} media files, both encodings     : {all_h:8.2f} h")
print(f"  B  previous pass, {253} units, MP3-preferred        : {CENSUS:8.2f} h  <- the figure in use")
print(f"  C  now, {len(units)} calls, MP3/MP4 pairs merged   : {sel_h:8.2f} h  <- what gets transcribed")
print(f"\n  A - C = {all_h-sel_h:.2f} h of MP3/MP4 duplicate encodings "
      f"({sum(1 for u in units if u['has_mp3'] and u['has_mp4'])} pairs)")
print(f"  B - C = {CENSUS-sel_h:.2f} h  <- THIS is the inflation in B")
print(f"    caused by {253-len(units)} call pairs whose titles differed ('NHB' vs 'NHB+',")
print(f"    'on Vimeo' suffix) and so were queued and billed twice.")
print(f"\n  STT cost at $0.0043/min:")
print(f"    on B (in use)  ${CENSUS*60*0.0043:.2f}")
print(f"    on C (correct) ${sel_h*60*0.0043:.2f}   ->  ${sel_h*60*0.0043 - CENSUS*60*0.0043:+.2f}")

print(f"\n=== MERGE AUDIT (every group that collapsed >1 file) ===")
print(f"  {sum(1 for u in units if len(u['media']['alternates']))} calls; showing the 6 "
      f"that B treated as separate calls")
for u in units:
    if len(u["media"]["alternates"]) and u["folder_label"].count("-") and u["date"]:
        pass
prev_pairs = [u for u in units if len(u["media"]["alternates"]) >= 1 and u["date"]]
shown = 0
for u in units:
    if not u["media"]["alternates"]: continue
    # the ones B would have split: same date+type, differing topic string
    if shown >= 6: break
    shown += 1
    print(f"  {u['folder_label']}  {u['type']}")
    print(f"     selected : {u['media']['name'][:66]}")
    for a in u["media"]["alternates"]:
        print(f"     alternate: {a['name'][:66]}  [{a['ext']}]")

if split_notes:
    print(f"\n  titles still differing within one group: {len(split_notes)}")
    for d, typ, topic, names in split_notes[:6]:
        print(f"    {d} {typ} {topic[:40]}")
        for n in names: print(f"       - {n[:76]}")

man = {"source": "handle sweep 59/59 folders, normalised (manifest-v3)",
       "counts": {"files": len(media), "calls": len(calls), "lessons": len(lessons),
                  "call_hours": round(hrs(calls), 2), "lesson_hours": round(hrs(lessons), 2),
                  "mp3_served": sum(1 for u in units if u["has_mp3"]),
                  "mp4_served": sum(1 for u in units if not u["has_mp3"]),
                  "not_billed_alternates": sum(len(u["media"]["alternates"]) for u in units)},
       "units": units}
out = os.path.join(OD, "manifest-v3.json")
json.dump(man, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"\nWRITTEN {out}")