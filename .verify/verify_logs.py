import os, sys, json, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"
print("### what encoding are the pipeline/out .log/.txt files?")
for f in ("final-scope.log","reconcile.log","design-names.log"):
    p=os.path.join(ROOT,"pipeline","out",f)
    raw=open(p,"rb").read()
    for enc in ("utf-8","cp1252","utf-16"):
        try:
            s=raw.decode(enc); print(f"   {f}: decodes as {enc}  (first line: {s.splitlines()[0][:70]!r})"); break
        except UnicodeDecodeError: continue
    print(f"      U+FFFD under best decode: {s.count(chr(0xFFFD))}   bytes with 0x80-0x9F: {sum(1 for b in raw if 0x80<=b<=0x9F)}")

print()
print("### 'Saves 132 GB' -- is it anywhere in a log or json?")
import subprocess
for f in ("final-scope.log","reconcile.log","slotrule.log","years2.log","norm.log","cat.log"):
    p=os.path.join(ROOT,"pipeline","out",f)
    s=open(p,"rb").read().decode("cp1252",errors="replace")
    for i,l in enumerate(s.splitlines(),1):
        if "132" in l or "MP4" in l.upper() and "GB" in l.upper() or "saved" in l.lower() or "never fetched" in l.lower():
            print(f"   {f}:{i}: {l.strip()[:150]}")