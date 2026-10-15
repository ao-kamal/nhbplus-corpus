#!/usr/bin/env python3
"""R3: mojibake / BOM / non-ASCII integrity sweep over the artifacts the spec cites."""
import io, os, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

roots = ["pipeline/out", "stage-1", "evidence"]
pat = re.compile(r'[\u00c2\u00c3\u00e2][\u0080-\u00bf]|\ufffd')
rows = []
for base in roots:
    for root, dirs, files in os.walk(base):
        if "_r3scratch" in root:
            continue
        for f in files:
            p = os.path.join(root, f)
            try:
                raw = open(p, "rb").read()
            except Exception:
                continue
            bom = raw.startswith(b"\xef\xbb\xbf")
            try:
                s = raw.decode("utf-8-sig")
            except Exception as e:
                rows.append((p, "NOT-UTF8", str(e)[:50], bom))
                continue
            hits = pat.findall(s)
            if hits:
                rows.append((p, len(hits), sorted(set(hits))[:5], bom))

print("=" * 78)
print("FILES CARRYING MOJIBAKE OR U+FFFD (artifacts the spec cites as evidence)")
print("=" * 78)
for p, n, h, bom in sorted(rows):
    print(f"  {p:<70} n={n:<5} bom={bom}  {h}")
print(f"  total: {len(rows)}")

print()
print("=" * 78)
print("WHICH OF THESE THE SPEC CITES AS LOAD-BEARING")
print("=" * 78)
cited = ["scope-final.json", "manifest-v3.json", "clean-names.json",
         "final-scope.log", "norm.log", "reconcile.log", "union.json",
         "selection-inventory.json", "scope-decision.json", "audio-worklist.json"]
for c in cited:
    p = os.path.join("pipeline/out", c)
    if os.path.exists(p):
        raw = open(p, "rb").read()
        s = raw.decode("utf-8-sig", errors="replace")
        n = len(pat.findall(s))
        bom = raw.startswith(b"\xef\xbb\xbf")
        # where exactly
        ex = []
        for m in list(pat.finditer(s))[:3]:
            ex.append(s[max(0, m.start()-40):m.start()+20].replace("\n", " "))
        print(f"  {c:<28} mojibake={n:<4} BOM={bom}")
        for e in ex:
            print(f"      ...{e}...")
    else:
        print(f"  {c:<28} MISSING")
