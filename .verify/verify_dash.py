import json, sys, os, collections, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"
def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)
cn = load(r"pipeline\out\clean-names.json")
P=[]
for sec in ("calls","lessons"):
    for e in cn[sec]:
        b=str(e["path"]).rsplit("/",1)[-1][:-3]
        P.append((sec,b,e.get("verbatim")))
D=[(e["kind"], e.get("clean"), e.get("verbatim")) for e in cn["documents"]]

print("### dash-splitter signature: ' - ' (space hyphen space) in the CLEAN name")
a=[x for x in P if " - " in x[1]]
print(f"   calls+lessons paths with ' - ': {len(a)} / {len(P)}")
for s,b,v in a: print(f"      [{s}] {b!r}   <- verbatim={v!r}")
print()
b=[x for x in D if x[1] and " - " in x[1]]
print(f"   documents clean with ' - ': {len(b)} / {len(D)}")
for k,c,v in b: print(f"      [{k}] {c!r}   <- verbatim={v!r}")
print()
print("### DOUBLE-hyphen artifacts ' - - ' (splitter ran twice)")
for s,bn,v in P:
    if " - - " in bn: print(f"      [{s}] {bn!r} <- {v!r}")
for k,c,v in D:
    if c and " - - " in c: print(f"      [{k}] {c!r} <- {v!r}")
print()
print("### intra-word hyphens: spec says PRESERVE. verbatim->clean diff check")
def dashpairs(v,c):
    vh = set(re.findall(r"[A-Za-z0-9]+-[A-Za-z0-9]+", v or ""))
    ch = set(re.findall(r"[A-Za-z0-9]+ - [A-Za-z0-9]+", c or ""))
    return vh, ch
broken=0
for s,bn,v in P:
    vh, ch = dashpairs(v,bn)
    if ch:
        broken+=1
        print(f"      BROKEN [calls/lessons] {bn!r}  <- {v!r}   {sorted(ch)}")
print(f"   calls+lessons names whose intra-word hyphen got spaced: {broken}")
broken2=0
for k,c,v in D:
    vh, ch = dashpairs(v,c)
    if ch:
        broken2+=1
print(f"   documents whose intra-word hyphen got spaced: {broken2}")
print()
print("### brand tokens NOT stripped (spec: strip NHB / NHB+ / FF)")
for s,bn,v in P:
    if re.search(r"\b(NHB\+|FF|NHB)\b", bn): print(f"      [call/lesson] {bn!r}")
n=0
for k,c,v in D:
    if c and re.search(r"\b(NHB\+|FF|NHB)\b", c): n+=1; print(f"      [doc] {c!r}  <- {v!r}")
print(f"   documents retaining a brand token: {n}")
print()
print("### underscores retained (spec: strip underscores)")
n=[ (k,c,v) for k,c,v in D if c and "_" in c ]
for k,c,v in n: print(f"      [doc] {c!r} <- {v!r}")
print("   docs with underscore:", len(n))
n2=[(s,b) for s,b,v in P if "_" in b]
print("   calls/lessons with underscore:", len(n2), n2[:5])
print()
print("### embedded DATE not normalised to ISO (spec: normalise to ISO)")
for s,bn,v in P:
    if re.search(r"\b\d{4}\s*-\s*\d{1,2}\s*-\s*\d{1,2}\b", bn): print(f"      ISO-ok [c] {bn!r}")
    elif re.search(r"\b\d{1,2}\s*-\s*\d{1,2}\s*-\s*\d{4}\b", bn): print(f"      NOT-ISO [c] {bn!r} <- {v!r}")
for k,c,v in D:
    if c and re.search(r"\b\d{1,2}\s*-\s*\d{1,2}\s*-\s*\d{4}\b", c): print(f"      NOT-ISO [doc:{k}] {c!r} <- {v!r}")