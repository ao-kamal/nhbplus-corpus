#!/usr/bin/env python3
"""
PDF PROBE. Measure before adopting anything.

Operator decision 2026-10-15: probe first, then commit. 50 of the 109 documents
are PDFs with no proven extraction path. 25 of them are the Swipes/Templates
orphans and may be IMAGE-ONLY SCANS, where a text-layer pass returns nothing.

Three questions, answered by measurement on THIS corpus:
  Q1 does pypdf extract a text layer at all here?
  Q2 are these images-over-text (rasterised overlay) or genuine text?
  Q3 what is the extraction ceiling - how many PDFs yield usable text?

The course-corpus-extraction skill's calibration constants were measured on
FireShot-captured web pages, NOT this corpus. Its own rule: "re-measure on your
own source before you rely on it."

Writes the probe handles to stdout as JSON so the runner can fetch exactly these.
"""
import json, os, sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")

sc = json.load(open(os.path.join(OUT, "scope-final.json"), encoding="utf-8"))
pdfs = [t for t in sc["targets"]
        if t["kind"] != "audio" and t["ext"] == "pdf"]

print("=" * 74)
print("PDF POPULATION")
print("=" * 74)
by_folder = defaultdict(list)
for t in pdfs:
    by_folder[t.get("folder", "?")].append(t)
print(f"  {len(pdfs)} PDFs in scope")
for f, ts in sorted(by_folder.items()):
    b = sum(t["bytes"] or 0 for t in ts)
    print(f"    {f[:44]:<44} {len(ts):>3}  {b/1048576:>8.1f} MB")

sizes = sorted(t["bytes"] or 0 for t in pdfs)
print(f"\n  smallest {sizes[0]/1024:.0f} KB   median {sizes[len(sizes)//2]/1048576:.1f} MB"
      f"   largest {sizes[-1]/1048576:.1f} MB")
print(f"  total {sum(sizes)/1073741824:.3f} GB")

# Pick a probe set: smallest, a median, a large one, and one per folder family.
probe = []
seen_folders = set()
for t in sorted(pdfs, key=lambda x: x["bytes"] or 0):
    f = t.get("folder", "?")
    if f not in seen_folders:
        probe.append(t); seen_folders.add(f)
        if len(probe) >= 4: break
# plus the single largest
big = max(pdfs, key=lambda x: x["bytes"] or 0)
if big["handle"] not in {p["handle"] for p in probe}:
    probe.append(big)

print("\n" + "=" * 74)
print("PROBE SET")
print("=" * 74)
sel = []
for t in probe:
    print(f"  {t['handle']}  {(t['bytes'] or 0)/1048576:>8.2f} MB  "
          f"{t.get('folder','?')[:26]:<26} {t['name'][:44]}")
    sel.append({"handle": t["handle"], "name": t["name"], "ext": t["ext"],
                "bytes": t["bytes"], "folder": t.get("folder"),
                "url": f"https://mega.nz/folder/EzMk0Z4K#CrnHbM7tWaNtcByX0Ry_-Q/file/{t['handle']}"})

json.dump({"pdf_count": len(pdfs), "total_bytes": sum(sizes),
           "by_folder": {f: len(ts) for f, ts in by_folder.items()},
           "probe_set": sel},
          open(os.path.join(OUT, "pdf-probe-set.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print(f"\nWRITTEN {os.path.join(OUT, 'pdf-probe-set.json')}")
print("\nNext: fetch these on the VM, install pypdf, and measure. The probe answers")
print("Q1 (does a text layer exist), Q2 (images-over-text or real text),")
print("Q3 (what fraction of the 50 yield usable text).")