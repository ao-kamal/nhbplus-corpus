#!/usr/bin/env python3
"""
Build the PER-FILE MANIFEST from the completed handle sweep.

This is the artifact that makes the run mechanical. Every file gets a minted
per-file URL:

    https://mega.nz/folder/PH#KEY/file/<HANDLE>

which fetches ONE file (measured: 1,436 MB, peak disk 1 file) instead of the
whole 320 GB share. The `::` syntax that every earlier attempt used is NOT the
mechanism; the handle belongs inside the URL.

MP3-preferred selection is preserved: where a call has both encodings, only the
MP3 is put in the STT queue. The MP4 is recorded but never selected, so no call
can be billed twice.
"""
import json, os, re, sys, glob
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
OD = os.path.join(HERE, "..", "out")
PH = "https://mega.nz/folder/EzMk0Z4K#CrnHbM7tWaNtcByX0Ry_-Q"

names = {}
sn = os.path.join(OD, "seednames.txt")
if os.path.exists(sn):
    for m in re.finditer(r'"([A-Za-z0-9_-]+)=([^"]*)"', open(sn, encoding="utf-8").read()):
        names[m.group(1)] = m.group(2)

DASHES = dict.fromkeys(map(ord, "‐‑‒–—―−"), "-")
LEAD = re.compile(r"^\s*\d{1,2}\s*\.\s*")
def norm(s):
    s = s.translate(DASHES)
    s = "".join(c if ord(c) < 128 else " " for c in s)
    s = re.sub(r"\s+", " ", s).strip().casefold()
    s = LEAD.sub("", s)
    m = re.match(r"^(\d{1,2})-(\d{1,2})-(\d{4})", s)
    if m: s = f"{int(m.group(1)):02d}-{int(m.group(2)):02d}-{m.group(3)}" + s[m.end():]
    s = re.sub(r"\b(?:guest|coaching|theory)\s+calls?\b", " call ", s)
    s = re.sub(r"\bcalls?\b", " call ", s)
    s = re.sub(r"\bnhb\s*\+?\s*", "nhb ", s)
    return re.sub(r"\s+", " ", s).strip()

SZ  = re.compile(r"([\d.]+)\s*[^0-9A-Za-z]*\s*([KMG])B\b")
DUR = re.compile(r"\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*$")
EXT = re.compile(r"\.([A-Za-z0-9]{2,5})\s*$")
gb  = lambda v,u: {"K":v/1048576,"M":v/1024,"G":v}[u.upper()]
def to_sec(d):
    p=[int(x) for x in d.split(":")]
    return p[0]*3600+p[1]*60+p[2] if len(p)==3 else p[0]*60+p[1]

files = []
for fp in sorted(glob.glob(os.path.join(OD, "handles-*.json"))):
    handle = os.path.basename(fp)[8:-5]
    try: rows = json.load(open(fp, encoding="utf-8-sig"))
    except Exception: continue
    if isinstance(rows, dict): rows = [rows]
    for r in rows:
        # PowerShell wraps each nested JSON array as {"value":[...],"Count":N}.
        # Iterating that directly yields dict KEYS. Same trap as final-census.
        if isinstance(r, dict) and "value" in r:
            r = r["value"]
        try: hid, text, title, is_folder = r[0], r[1], r[2], int(r[3])
        except Exception: continue
        if is_folder or not hid: continue
        stem_txt = DUR.sub("", text).strip()
        m = EXT.search(stem_txt)
        if not m: continue
        ext = m.group(1).lower()
        d = DUR.search(text.strip())
        s = SZ.search(title or "")
        files.append({
            "handle": hid,
            "url": f"{PH}/file/{hid}",
            "folder": names.get(handle, handle),
            "name": stem_txt,
            "ext": ext,
            "bytes": int(gb(float(s.group(1)), s.group(2)) * 1073741824) if s else None,
            "dur_s": to_sec(d.group(1)) if d else None,
            "title_key": norm(EXT.sub("", stem_txt).strip()),
        })

print(f"files captured          : {len(files)}")
nofh = [f for f in files if not f["handle"]]
nofz = [f for f in files if f["bytes"] is None]
print(f"  without handle        : {len(nofh)}")
print(f"  without size          : {len(nofz)}")

# --- group into calls, MP3-preferred ---
calls = defaultdict(lambda: {"mp3": None, "mp4": None, "pdf": []})
for f in files:
    k = (f["folder"], f["title_key"])
    if f["ext"] in ("mp3", "mp4"):
        calls[k][f["ext"]] = f
    elif f["ext"] == "pdf":
        calls[k]["pdf"].append(f)

units = []
for (folder, key), v in calls.items():
    pick = v["mp3"] or v["mp4"]
    if not pick: continue
    units.append({
        "folder": folder, "key": key,
        "media": pick, "has_mp3": bool(v["mp3"]), "has_mp4": bool(v["mp4"]),
        "pdfs": v["pdf"], "pdf_count": len(v["pdf"]),
    })

total_h = sum(u["media"]["dur_s"] or 0 for u in units) / 3600
total_b = sum(u["media"]["bytes"] or 0 for u in units)
print()
print(f"distinct calls          : {len(units)}")
print(f"  served by MP3         : {sum(1 for u in units if u['has_mp3'])}")
print(f"  served by MP4 (no mp3): {sum(1 for u in units if not u['has_mp3'])}")
print(f"  carrying PDFs         : {sum(1 for u in units if u['pdf_count'])}")
print(f"  PDF files attached    : {sum(u['pdf_count'] for u in units)}")
print(f"audio hours (measured)  : {total_h:.2f}")
print(f"download bytes (MP3-pref): {total_b/1073741824:.2f} GB")
print(f"peak disk needed        : {max((u['media']['bytes'] or 0) for u in units)/1073741824:.2f} GB (largest single file)")

manifest = {
    "generated_from": "handle sweep (59/59 folders) - per-file URLs",
    "per_file_url_form": "https://mega.nz/folder/PH#KEY/file/HANDLE",
    "counts": {
        "files": len(files), "calls": len(units),
        "mp3_served": sum(1 for u in units if u["has_mp3"]),
        "mp4_served": sum(1 for u in units if not u["has_mp3"]),
    },
    "audio_hours": round(total_h, 2),
    "download_GB": round(total_b / 1073741824, 2),
    "peak_disk_GB": round(max((u["media"]["bytes"] or 0) for u in units) / 1073741824, 2),
    "units": units,
}
out = os.path.join(OD, "perfile-manifest.json")
json.dump(manifest, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print()
print(f"WRITTEN {out}")
print()
print("=== first 3 units, showing the minted URL ===")
for u in units[:3]:
    print(f"  {u['media']['name'][:56]}")
    print(f"    {u['media']['url']}")
    print(f"    {u['media']['bytes'] and round(u['media']['bytes']/1073741824,3)} GB   {u['media']['dur_s']}s")