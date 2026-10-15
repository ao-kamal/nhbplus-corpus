import os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"
DIRS = ["stage-0", "stage-1", os.path.join("evidence","probes")]
print("### CLAIM 16: U+FFFD scan over stage-0/, stage-1/, evidence/probes/")
tot_files=0; tot_bad=0; tot_fffd=0
for d in DIRS:
    base=os.path.join(ROOT,d)
    files=[]
    for dp,_,fn in os.walk(base):
        for f in fn:
            if f.lower().endswith((".md",".json")):
                files.append(os.path.join(dp,f))
    print(f"\n  --- {d}  ({len(files)} .md/.json files) ---")
    for f in sorted(files):
        tot_files+=1
        raw=open(f,"rb").read()
        try:
            s=raw.decode("utf-8")
        except UnicodeDecodeError as e:
            print(f"    DECODE-ERROR (not valid utf-8): {os.path.relpath(f,ROOT)}  {e}")
            tot_bad+=1
            continue
        n=s.count("\ufffd")
        if n:
            tot_fffd+=n
            print(f"    U+FFFD x{n}  {os.path.relpath(f,ROOT)}")
            for i,line in enumerate(s.splitlines(),1):
                c=line.count("\ufffd")
                if c: print(f"        line {i}: {c}  {line[:160]!r}")
print(f"\n  TOTAL files scanned: {tot_files}   files with U+FFFD: {tot_bad}   total U+FFFD: {tot_fffd}")
print()
print("### extra: also scan pipeline/out and pipeline/scripts json/md for U+FFFD (not required, informational)")
extra=0; ebad=0
for d in ("pipeline","AGENTS.md"):
    base=os.path.join(ROOT,d)
    if os.path.isfile(base):
        cand=[base]
    else:
        cand=[os.path.join(dp,f) for dp,_,fn in os.walk(base) for f in fn if f.lower().endswith((".md",".json",".txt",".log"))]
    for f in cand:
        extra+=1
        try: s=open(f,"rb").read().decode("utf-8")
        except UnicodeDecodeError: ebad+=1; print(f"   DECODE-ERROR {os.path.relpath(f,ROOT)}"); continue
        n=s.count("\ufffd")
        if n:
            ebad+=1
            print(f"   U+FFFD x{n}  {os.path.relpath(f,ROOT)}")
print(f"   informational: {extra} files, {ebad} with issues")