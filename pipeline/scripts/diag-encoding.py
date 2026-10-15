#!/usr/bin/env python3
"""
DIAGNOSTIC 2: the encoding, and the folder labels.

Two problems to characterise exactly before fixing either.

A) '01. 07-04-2024 NHB+ Theory Call O?C?o Reading Offers #2.mp3' - an em-dash
   that went through a code page. I must not guess the reverse transform; a
   wrong guess corrupts silently. Dump the RAW BYTES and try the candidates.

B) Folder labels: month folder names repeat across years AND month folders do
   not carry their own year, so 199 of 211 calls had year=None. The fix is to
   take the year from the CALL's own date, which is authoritative, and demote
   the MEGA folder to a cross-check.
"""
import glob, json, os, re, sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")

rows = []
for fp in sorted(glob.glob(os.path.join(OD, "handles-*.json"))):
    fh = os.path.basename(fp)[8:-5]
    try: data = json.load(open(fp, encoding="utf-8-sig"))
    except Exception: continue
    if isinstance(data, dict): data = [data]
    for r in data:
        if isinstance(r, dict) and "value" in r: r = r["value"]
        try: hid, text, title, isfolder = r[0], r[1], r[2], int(r[3])
        except Exception: continue
        rows.append((fh, hid, text or "", title or "", int(isfolder)))

# ---------- A: the encoding ----------
na  = lambda s: any(ord(c) > 127 for c in (s or ""))
print("=== A: NON-ASCII, text vs title SEPARATELY ===")
in_text  = [r for r in rows if na(r[2])]
in_title = [r for r in rows if na(r[3])]
print(f"  non-ASCII in `text`  (the field used as the name): {len(in_text)} of {len(rows)}")
print(f"  non-ASCII in `title` (unused by the manifest)     : {len(in_title)} of {len(rows)}")
print(f"  clean ASCII in both                               : "
      f"{len(rows) - len({id(r) for r in in_text} | {id(r) for r in in_title})}")

def codepoints(s, limit=8):
    return ["U+%04X(%s)" % (ord(c), c if c.isprintable() and c != " " else "?")
            for c in s if ord(c) > 127][:limit]

if in_text:
    print("\n  --- rows whose NAME is non-ASCII ---")
    for fh, hid, text, title, _ in in_text[:4]:
        print(f"    text    : {text[:72]}")
        print(f"    cps     : {codepoints(text)}")
    s = in_text[0][2]
    print(f"\n  raw bytes of the name: {s.encode('utf-8')[:90]!r}")
    print("\n  --- candidate reverse transforms (must land on a real dash) ---")
    for name, fn in [
        ("cp1252 -> utf-8", lambda s: s.encode("cp1252").decode("utf-8")),
        ("latin1 -> utf-8", lambda s: s.encode("latin-1").decode("utf-8")),
        ("cp437 -> utf-8",   lambda s: s.encode("cp437").decode("utf-8")),
        ("cp850 -> utf-8",   lambda s: s.encode("cp850").decode("utf-8")),
        ("mac-roman-> utf-8",lambda s: s.encode("mac-roman").decode("utf-8")),
    ]:
        try:
            out = fn(s)
            hit = [c for c in out if c in "\u2014\u2013\u2018\u2019\u201c\u201d\u2026"]
            print(f"    {name:20} -> {'DASH/QUOTE FOUND ' + repr(''.join(hit)) if hit else 'no dash'}  {out[:60]}")
        except Exception as e:
            print(f"    {name:20} -> {type(e).__name__}: {str(e)[:44]}")
    print("\n  does the matching `title` show the TRUE character?")
    for fh, hid, text, title, _ in in_text[:3]:
        print(f"    title cps: {codepoints(title, 10)}")
        print(f"    title    : {title[:100]}")

# ---------- B: folder labels ----------
print("=== B: FOLDER LABEL SOURCES ===")
MONTHNUM = {m.lower(): i for i, m in enumerate(
    ["january","february","march","april","may","june","july","august",
     "september","october","november","december"], 1)}
MONTHABBR = {m: i for i, m in enumerate(
    ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"], 1)}

seednames = {}
for m in re.finditer(r'"([A-Za-z0-9_-]+)=([^"]*)"',
                     open(os.path.join(OD, "seednames.txt"), encoding="utf-8").read()):
    seednames[m.group(1)] = m.group(2)

def folder_month(name):
    n = re.sub(r"^\s*\d{1,2}\s*\.\s*", "", (name or "").lower()).strip()
    for w in re.split(r"[^a-z]+", n):
        if w in MONTHNUM: return MONTHNUM[w]
        if w in MONTHABBR: return MONTHABBR[w]
    if re.search(r"(19|20)\d{2}", n):
        y = int(re.search(r"(19|20)\d{2}", n).group(0))
        return None, y
    return None

DATE = re.compile(r"^\s*(\d{1,2})\s*-\s*(\d{1,2})\s*-\s*((?:19|20)\d{2})")
media = [r for r in rows if not r[4] and re.search(r"\.(mp3|mp4|m4a|wav|mov)$", r[2], re.I)]
print(f"  media rows: {len(media)}")
have_date = [r for r in media if DATE.match(r[2])]
print(f"  rows whose NAME carries a call date: {len(have_date)} of {len(media)}")
years = defaultdict(int)
for r in have_date:
    years[int(DATE.match(r[2]).group(3))] += 1
print(f"  years recoverable from the call name: {dict(sorted(years.items()))}")

agree = disagree = nomatch = 0
bad = []
for r in have_date:
    m = DATE.match(r[2])
    cmon = int(m.group(1)); cyear = int(m.group(3))
    fm = folder_month(seednames.get(r[0], ""))
    if isinstance(fm, tuple): continue
    if fm is None: nomatch += 1
    elif fm == cmon: agree += 1
    else:
        disagree += 1
        bad.append((seednames.get(r[0], r[0]), m.group(0).strip(), cmon, fm))
print(f"\n  MEGA folder month vs call-name month:")
print(f"    agree     {agree}")
print(f"    disagree  {disagree}   <- worth surfacing, not silently reconciled")
print(f"    no month in folder name {nomatch}")
for f, d, c, fm in bad[:12]:
    print(f"      folder {f:26} call {d}  call month={c} folder month={fm}")