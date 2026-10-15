import json, sys, os, collections, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"
def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)
cn = load(r"pipeline\out\clean-names.json")
ALL=[]
for sec in ("calls","lessons","documents"):
    for e in cn.get(sec,[]):
        e=dict(e); e["_sec"]=sec; ALL.append(e)

print("### PATHS ACTUALLY PRESENT")
for sec in ("calls","lessons","documents"):
    sub=[e for e in ALL if e["_sec"]==sec]
    withp=[e for e in sub if e.get("path")]
    print(f"   {sec:10s} entries={len(sub):4d}  with path={len(withp):4d}  path=None={len(sub)-len(withp):4d}")
print(f"   TOTAL entries={len(ALL)}  TOTAL paths={sum(1 for e in ALL if e.get('path'))}")
print(f"   -> 229 or 230?  ACTUAL = {sum(1 for e in ALL if e.get('path'))}")
print()
print("### documents entry shape")
d0=[e for e in ALL if e['_sec']=='documents'][0]
print("   keys:", sorted(d0.keys()))
print("   sample:", json.dumps(d0, ensure_ascii=False)[:400])
print()

print("### CLAIM 11 (corrected): collisions on REAL PATHS")
def bn(e):
    b=str(e["path"]).rsplit("/",1)[-1]
    return b[:-3] if b.lower().endswith(".md") else b
PATHS=[e for e in ALL if e.get("path")]
for label, fn in (("exact", bn),
                  ("casefold", lambda e: bn(e).casefold()),
                  ("casefold + space->hyphen", lambda e: bn(e).casefold().replace(" ","-"))):
    c=collections.Counter(fn(e) for e in PATHS)
    dups={k:v for k,v in c.items() if v>1}
    print(f"   {label}: distinct={len(c)} colliding_keys={len(dups)}")
    for k,v in dups.items():
        for e in [x for x in PATHS if fn(x)==k]:
            print(f"      x{v} {k!r} <- [{e['_sec']}] {e['path']!r} | verbatim={e.get('verbatim')!r}")
print()
print("### documents: collisions on VERBATIM (documents have no path)")
for label, fn in (("verbatim exact", lambda e: e.get("verbatim")),
                  ("verbatim casefold", lambda e: str(e.get("verbatim")).casefold())):
    D=[e for e in ALL if e['_sec']=='documents']
    c=collections.Counter(fn(e) for e in D)
    dups={k:v for k,v in c.items() if v>1}
    print(f"   {label}: distinct={len(c)} colliding_keys={len(dups)}")
    for k,v in dups.items():
        for e in [x for x in D if fn(x)==k]:
            print(f"      x{v} {k!r} | verbatim={e.get('verbatim')!r} | extra={ {kk:vv for kk,vv in e.items() if kk not in ('verbatim','_sec')} }")
print()
print("### 'Resources Links' population")
rl=[e for e in ALL if 'resources link' in str(e.get('verbatim','')).casefold()]
print("   documents whose verbatim is 'Resources Links':", len(rl))
for e in rl: print("      ", json.dumps({k:v for k,v in e.items() if k!='_sec'}, ensure_ascii=False)[:300])
print("   file's own collision verdict:", cn.get("collisions"))
print()
print("### CLAIM 12 (corrected): illegal chars in BASENAME COMPONENT only")
ILLEGAL=set('\\/:*?"<>|')
RESERVED={"CON","PRN","AUX","NUL"}|{f"COM{i}" for i in range(1,10)}|{f"LPT{i}" for i in range(1,10)}
bad=[]
for e in PATHS:
    segs=str(e["path"]).split("/")
    for s in segs:
        issues=[]
        ch=ILLEGAL & set(s)
        if ch: issues.append(f"illegal {sorted(ch)}")
        if s!=s.rstrip(" ."): issues.append("trailing dot/space")
        stem=s.split(".")[0].strip().upper()
        if stem in RESERVED: issues.append(f"reserved {stem}")
        if len(s)>255: issues.append("len>255")
        if any(ord(c)<32 for c in s): issues.append("control char")
        if issues: bad.append((e["path"], s, issues))
print("   path SEGMENTS with an illegal/reserved property:", len(bad))
for p,s,i in bad: print(f"      {p!r} seg={s!r} -> {i}")
print("   (empty = clean)")
print()
print("### leading/trailing whitespace or double spaces in basenames")
ws=[e for e in PATHS if bn(e)!=bn(e).strip() or "  " in bn(e)]
print("   basenames with edge/inner whitespace issues:", len(ws))
for e in ws[:15]: print("      ", repr(e["path"]))
print()
print("### basename length distribution")
L=[len(bn(e)) for e in PATHS]
print(f"   min={min(L)} max={max(L)} mean={sum(L)/len(L):.1f}  over 200: {sum(1 for x in L if x>200)}")