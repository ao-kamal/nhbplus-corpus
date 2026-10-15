import json, sys, os, collections, re, unicodedata
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"
def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)
cn = load(r"pipeline\out\clean-names.json")
print("### clean-names.json top-level")
for k,v in cn.items():
    t=type(v).__name__; n=len(v) if isinstance(v,(list,dict,str)) else v
    print(f"   {k!r:34s} {t:6s} len/val={n}")
print()
entries = None
for k,v in cn.items():
    if isinstance(v, list) and v and isinstance(v[0], dict):
        entries = v; key=k; break
print("### entry list key =", key, " count =", len(entries))
print("   entry keys:", sorted(entries[0].keys()))
for i,e in enumerate(entries[:3]):
    print("   ", json.dumps(e, ensure_ascii=False)[:400])
print()

print("### CLAIM 10: how many paths? (229 / 230 / ?)")
pathkeys = [k for k in ("path","clean_path","target","out","vault_path","note_path") if k in entries[0]]
print("   path-like keys present:", pathkeys)
for pk in pathkeys:
    print(f"   len({pk}) =", len(entries), " non-null:", sum(1 for e in entries if e.get(pk)))
    print("   samples:", [e.get(pk) for e in entries[:3]])
print()

namekeys = [k for k in ("clean","clean_name","name","stem","basename") if k in entries[0]]
print("   name-like keys present:", namekeys, "-> deriving clean name from `path` basename instead")
ALL = []
for sec in ("calls","lessons","documents"):
    for e in cn.get(sec, []):
        e = dict(e); e["_sec"]=sec; ALL.append(e)
def basename(e):
    p = str(e.get("path") or "")
    b = p.rsplit("/",1)[-1]
    return b[:-3] if b.lower().endswith(".md") else b
def fullpath(e): return str(e.get("path") or "")
print("   TOTAL PATHS =", len(ALL), " = calls", len(cn.get("calls",[])), "+ lessons", len(cn.get("lessons",[])), "+ documents", len(cn.get("documents",[])))
print("   collisions block in file:", json.dumps(cn.get("collisions"), ensure_ascii=False)[:800])
print("   decision:", cn.get("decision"))
print()
print("### CLAIM 11: collisions after case-fold AND space->hyphen")
def probe(label, fn):
    c = collections.Counter(fn(e) for e in ALL)
    dups = {k:v for k,v in c.items() if v>1}
    print(f"   {label}: distinct={len(c)} colliders={len(dups)}")
    for k,v in list(dups.items())[:30]:
        ex=[e for e in ALL if fn(e)==k][:8]
        print(f"      x{v}  {k!r}")
        for e in ex: print(f"           <- [{e['_sec']}] verbatim={e.get('verbatim')!r} path={e.get('path')!r}")
    return dups
d1 = probe("exact basename", basename)
d2 = probe("casefold", lambda e: basename(e).casefold())
d3 = probe("casefold+space->hyphen", lambda e: basename(e).casefold().replace(" ","-"))
print()
print("### CLAIM 12: Windows-illegal chars / trailing dot-space / reserved names")
ILLEGAL = set('\\/:*?"<>|')
RESERVED = {"CON","PRN","AUX","NUL"} | {f"COM{i}" for i in range(1,10)} | {f"LPT{i}" for i in range(1,10)}
bad = []
for e in ALL:
    for pk, v in (("basename", basename(e)), ("path", fullpath(e))):
        s = v.rsplit("/",1)[-1].split(".")[0]
        issues=[]
        ch = ILLEGAL & set(v)
        if ch: issues.append(f"illegal-chars {sorted(ch)}")
        if v != v.rstrip(" ."): issues.append(f"trailing-dot/space {v!r}")
        if s.upper() in RESERVED: issues.append(f"reserved {s}")
        if len(v) > 255: issues.append("too long")
        if any(ord(ch)<32 for ch in v): issues.append("control char")
        if issues: bad.append((pk, v, issues))
print("   names/paths with an illegal/reserved property:", len(bad))
for pk,v,i in bad[:40]: print(f"      [{pk}] {v!r} -> {i}")
print()
print("### CLAIM 13: doubled extension like .mp3.md / .mp4.md")
dbl = [e for e in ALL if re.search(r"\.(mp3|mp4|m4a|wav|aac|flac)\.(md|txt|json)$", fullpath(e), re.I)]
print("   paths with doubled media extension:", len(dbl))
for e in dbl[:20]: print("      ", e["_sec"], repr(e.get("path")), "verbatim=", repr(e.get("verbatim")))
dbl2 = [e for e in ALL if re.search(r"\.(mp3|mp4)\b", str(e.get("verbatim") or ""), re.I) and re.search(r"\.(mp3|mp4)\.(md|txt)$", fullpath(e), re.I)]
print("   (strict .mp3.md / .mp4.md):", len(dbl2))