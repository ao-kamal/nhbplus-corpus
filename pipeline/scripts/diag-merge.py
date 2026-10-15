#!/usr/bin/env python3
"""
DIAGNOSTIC. Before normalising anything, find out what is actually wrong.

The smoke test billed one call twice (NHB vs NHB+, 'on Vimeo' suffix). The
manifest counted 211 calls and 630.74 h and that matched two earlier censuses -
but those censuses shared the same grouping logic, so agreement did not make
this axis independent. Measure it.

Three questions:
  Q1 are names truncated in the capture?  (the '(Cou' in the smoke test)
  Q2 does the row `title` attribute carry the FULL name?
  Q3 how many units collapse into one call under a better key?
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
        rows.append({"folder_handle": fh, "handle": hid,
                     "text": text, "title": title, "folder": isfolder})

print(f"rows captured: {len(rows)}")
media = [r for r in rows if not r["folder"]]
print(f"media rows   : {len(media)}")

# --- Q1: is `text` truncated?  a truncated name has no extension at the end ---
DUR = re.compile(r"\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*$")
EXT = re.compile(r"\.([A-Za-z0-9]{2,5})\s*$")
trunc = [r for r in media if not EXT.search(DUR.sub("", r["text"]).strip())]
print(f"\n=== Q1: `text` field with no trailing extension ===")
print(f"  {len(trunc)} of {len(media)}  ({100*len(trunc)/len(media):.1f}%)")
for r in trunc[:6]:
    print(f"    text   : {r['text'][:78]}")

# --- Q2: does `title` carry the full name? ---
print(f"\n=== Q2: can `title` recover the full name? ===")
rec = 0
for r in trunc:
    t = r["title"] or ""
    m = EXT.search(t)
    if m and len(m.group(0)) >= 3 and t.strip().lower().endswith(m.group(0).lower()):
        rec += 1
print(f"  recoverable from title: {rec} of {len(trunc)}")
for r in trunc[:4]:
    print(f"    text   : {r['text'][:64]}")
    print(f"    title  : {(r['title'] or '')[:110]}")

# --- Q3: collapse under a better key ---
def full_name(r):
    """Prefer the title attribute when text is truncated: it holds the full name."""
    t = DUR.sub("", r["text"]).strip()
    if EXT.search(t): return t
    ttl = r["title"] or ""
    parts = ttl.split()
    for i in range(len(parts)):
        cand = " ".join(parts[i:])
        if EXT.search(cand) and not cand[0].isdigit():
            return cand
    return t

PLATFORM = re.compile(r"\s+on\s+(vimeo(\.com)?|youtube(\.com)?|wistia|loom|teachable)\s*$", re.I)
LEADN   = re.compile(r"^\s*\d{1,2}\s*\.\s*")
def key_of(r):
    n = LEADN.sub("", full_name(r))
    n = PLATFORM.sub("", n)
    n = re.sub(r"\.(mp3|mp4|wav|m4a|mov)$", "", n, flags=re.I)
    n = re.sub(r"\s+", " ", n).replace("NHB+", "NHB")
    n = re.sub(r"[^\w\s\-+:&.,'()]", " ", n)
    n = re.sub(r"\s+", " ", n).strip().casefold()
    return n

g = defaultdict(list)
for r in media:
    if re.search(r"\.(mp3|mp4|m4a|wav|mov)$", full_name(r), re.I):
        g[(r["folder_handle"], key_of(r))].append(r)

multi = {k: v for k, v in g.items() if len(v) > 1}
print(f"\n=== Q3: groups that collapse to ONE call ===")
print(f"  media units           : {sum(len(v) for v in g.values())}")
print(f"  groups after re-key   : {len(g)}")
print(f"  groups with >1 member : {len(multi)}   <- these were previously split")
for k, v in list(multi.items())[:12]:
    print(f"    [{len(v)}] {k[1][:66]}")
    for r in v:
        print(f"          {r['handle']}  {full_name(r)[:64]}")