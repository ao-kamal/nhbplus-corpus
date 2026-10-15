#!/usr/bin/env python3
"""
Analyse all 230 real filenames so a clean naming scheme is designed from the
DATA, not from three examples.

Run:  python analyse-names.py

Answers:
  1. What junk is actually present, and how often?
  2. Which tokens are redundant (repeated on every file)?
  3. What is the date format distribution?
  4. What would a clean name look like, derived by rule rather than typed?
  5. Does the cleaned set collide? (A rename that collides is a data loss event.)
"""
import json, os, re, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")

man = json.load(open(os.path.join(OUT, "manifest-v3.json"), encoding="utf-8"))
units = [u for u in man["units"] if u["kind"] in ("calls", "lessons")]
sc = json.load(open(os.path.join(OUT, "scope-final.json"), encoding="utf-8"))
docs = [t for t in sc["targets"] if t["kind"] in ("written_hand", "course_doc")]

print("=" * 78)
print("1. WHAT IS ACTUALLY IN THE NAMES")
print("=" * 78)
names = [u["media"]["name"] for u in units]
print(f"  audio units: {len(names)}   documents: {len(docs)}")

JUNK = [
    ("_watermarked", r"_water\s?mark(ed)?\b"),
    ("_water", r"_water\b"),
    ("resolution/size suffix", r"\b\d{3,4}x\d{3,4}\b"),
    ("kb/mb size suffix", r"\b\d{2,5}k\b"),
    ("stray bracket", r"[\[\]]"),
    ("underscores", r"_"),
    ("double spaces", r"  "),
    ("trailing space", r"\s+$"),
    ("ampersand", r"&"),
    ("parentheses", r"[()]"),
    ("hash-N part marker", r"#\d"),
    ("'Part N' marker", r"\bpart\s*\d\b"),
    ("'with <Name>' suffix", r"\bwith\s+[A-Z]"),
    ("'on <Topic>' suffix", r"\bon\s+[A-Z]"),
    ("ordinal prefix", r"^\s*\d{1,2}\s*[.)]\s*"),
]
for label, pat in JUNK:
    n = sum(1 for s in names if re.search(pat, s))
    print(f"  {label:<24} {n:>4} of {len(names)}  ({100*n/len(names):>4.1f}%)")

print("\n" + "=" * 78)
print("2. REDUNDANT TOKENS (present on a large share of files)")
print("=" * 78)
for tok in ["NHB+", "NHB", "FF", "Call", "Theory", "Coaching", "Guest", "Training",
            "NHB+ Theory Call", "NHB+ Call", "FF_NHB+"]:
    n = sum(1 for s in names if tok in s)
    if n:
        print(f"  {tok:<20} {n:>4} of {len(names)}  ({100*n/len(names):>4.1f}%)")

print("\n" + "=" * 78)
print("3. DATE FORMAT DISTRIBUTION")
print("=" * 78)
fmt = Counter()
for s in names:
    m = re.match(r"^\s*(?:\d{1,2}\s*[.)]\s*)?(\d{1,2})-(\d{1,2})-(\d{4})", s)
    if m:
        a, b, y = m.groups()
        fmt["MM-DD-YYYY" if len(a) == 2 else "M-D-YYYY"] += 1
    elif re.match(r"^\s*(?:\d{1,2}\s*[.)]\s*)?((?:19|20)\d{2})-(\d{2})-(\d{2})", s):
        fmt["YYYY-MM-DD"] += 1
    else:
        fmt["NO DATE IN NAME"] += 1
for k, v in fmt.most_common():
    print(f"  {k:<20} {v:>4}")

print("\n" + "=" * 78)
print("4. CALL TYPE DISTRIBUTION (for a type token)")
print("=" * 78)
for k, v in Counter(u["type"] for u in units).most_common():
    print(f"  {k:<12} {v:>4}")

# ---------------------------------------------------------------- cleaners
TYPES = ["Theory", "Coaching", "Guest", "Training"]

def clean_name(u, *, drop_brand=True, drop_ordinal=True, keep_type=True,
               strip_junk=True, iso_date=True):
    s = u["media"]["name"]
    s = s.rsplit(".", 1)[0] if s.lower().endswith((".mp3", ".mp4")) else s
    if strip_junk:
        s = re.sub(r"\s*_water\s?mark(ed)?\b", "", s, flags=re.I)
        s = re.sub(r"\s*_water\b", "", s, flags=re.I)
        s = re.sub(r"\s+\d{3,4}x\d{3,4}\b.*$", "", s)      # resolution+size tail
        s = re.sub(r"\s+\d{2,5}k\b", "", s)
        s = re.sub(r"[\[\]]", "", s)
    if drop_ordinal:
        s = re.sub(r"^\s*\d{1,2}\s*[.)]\s*", "", s)
    if drop_brand:
        s = s.replace("FF_NHB+", "").replace("NHB+", "").replace("FF ", "")
    if iso_date:
        m = re.match(r"^\s*(\d{1,2})-(\d{1,2})-((?:19|20)\d{2})\s*(.*)$", s)
        if m:
            a, b, y, rest = m.groups()
            s = f"{y}-{int(a):02d}-{int(b):02d} {rest}".strip()
    if keep_type:
        for t in TYPES:
            if re.search(rf"\b{t}\b", s, re.I):
                s = re.sub(rf"\b{t}\b\s*(Call)?\b\s*[-–—:]*\s*", "", s, flags=re.I)
                s = f"{s.strip()} ({t})"
                break
    s = re.sub(r"\s*[-–—:]\s*", " - ", s)
    s = re.sub(r"\s*-\s*-\s*", " - ", s)
    s = re.sub(r"\s+", " ", s).strip(" -")
    return re.sub(r"[<>:\"/\\|?*]", "", s).strip() or u["media"]["name"]

print("\n" + "=" * 78)
print("5. THE CLEANED SET — real before/after, and collision check")
print("=" * 78)
variants = {
    "A  drop brand + ordinal + junk, keep type": dict(),
    "B  as A, but also drop the type token":     dict(keep_type=False),
}
for label, kw in variants.items():
    seen, coll = {}, []
    for u in units:
        c = clean_name(u, **kw)
        k = c.casefold()
        if k in seen: coll.append((seen[k], c))
        seen[k] = u["media"]["name"]
    print(f"\n  {label}")
    print(f"    unique: {len(seen)} of {len(units)}   collisions: {len(coll)}")
    for a, b in coll[:5]: print(f"      {a!r}  ==  {b!r}")
    if not coll:
        for u in units[:14]:
            print(f"      {u['media']['name'][:52]:<54} ->  {clean_name(u, **kw)[:52]}")

print("\n" + "=" * 78)
print("6. DOCUMENT NAMES")
print("=" * 78)
dseen, dcoll = {}, []
for t in docs:
    c = re.sub(r"\s*_water\s?mark(ed)?\b", "", t["name"], flags=re.I)
    c = re.sub(r"[\[\]]", "", c)
    c = re.sub(r"[<>:\"/\\|?*]", "", c).strip() or t["name"]
    k = c.casefold()
    if k in dseen: dcoll.append((dseen[k], c))
    dseen[k] = t["name"]
print(f"  unique after cleaning: {len(dseen)} of {len(docs)}   collisions: {len(dcoll)}")
for t in docs[:12]:
    c = re.sub(r"[\[\]]", "", t["name"])
    print(f"    {t['name'][:48]:<50} ->  {c[:48]}")

print("\n" + "=" * 78)
print("7. TOTAL WRITABLE CHECK")
print("=" * 78)
WINDOWS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
RESERVED = {"CON","PRN","AUX","NUL",*[f"COM{i}" for i in range(1,10)],
            *[f"LPT{i}" for i in range(1,10)]}
bad = [n for n in list(dseen) if WINDOWS.search(n) or n.split(".")[0].upper() in RESERVED
       or n.endswith((" ", "."))]
print(f"  audio + doc names still unwritable after cleaning: {len(bad)}")
for n in bad[:10]: print(f"    {n!r}")
print("\n  longest resulting name:")
allc = [clean_name(u) for u in units] + list(dseen)
for n in sorted(allc, key=len, reverse=True)[:3]:
    print(f"    {len(n):>4} chars  {n}")