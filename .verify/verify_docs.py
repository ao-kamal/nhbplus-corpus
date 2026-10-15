import json, sys, os, collections, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"
def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)
cn = load(r"pipeline\out\clean-names.json")
D=[e for e in cn["documents"]]
ILLEGAL=set('\\/:*?"<>|')
RESERVED={"CON","PRN","AUX","NUL"}|{f"COM{i}" for i in range(1,10)}|{f"LPT{i}" for i in range(1,10)}

print("### documents: `clean` collisions (these WILL be filenames)")
for label, fn in (("clean exact", lambda e: e.get("clean")),
                  ("clean casefold", lambda e: str(e.get("clean")).casefold()),
                  ("clean casefold+space->hyphen", lambda e: str(e.get("clean")).casefold().replace(" ","-"))):
    c=collections.Counter(fn(e) for e in D)
    dups={k:v for k,v in c.items() if v>1}
    print(f"   {label}: distinct={len(c)} colliding_keys={len(dups)}")
    for k,v in dups.items():
        print(f"      x{v}  {k!r}")
        for e in [x for x in D if fn(x)==k]:
            print(f"           handle={e['handle']} kind={e['kind']} verbatim={e.get('verbatim')!r} clean={e.get('clean')!r}")
print()
print("### documents: illegal chars / reserved / trailing in `clean`")
bad=[]
for e in D:
    v=e.get("clean")
    if not isinstance(v,str): bad.append((v,"NOT A STRING")); continue
    issues=[]
    ch=ILLEGAL & set(v)
    if ch: issues.append(f"illegal {sorted(ch)}")
    if v!=v.rstrip(" ."): issues.append("trailing dot/space")
    if v.split(".")[0].strip().upper() in RESERVED: issues.append("reserved")
    if v!=v.strip(): issues.append("edge whitespace")
    if any(ord(c)<32 for c in v): issues.append("control")
    if issues: bad.append((v,issues))
print("   documents with a problem:", len(bad))
for v,i in bad: print(f"      {v!r} -> {i}")
print()
print("### documents clean == verbatim? (prefix stripped?)")
same=[e for e in D if e.get("clean")==e.get("verbatim")]
print(f"   identical: {len(same)} / {len(D)}   changed: {len(D)-len(same)}")
for e in D:
    if e.get("clean")!=e.get("verbatim"):
        print(f"      {e.get('verbatim')!r}  ->  {e.get('clean')!r}   [{e['kind']}]")
print()
print("### documents by kind with path assigned?")
print("   ", dict(collections.Counter((e['kind'], bool(e.get('path'))) for e in D)))