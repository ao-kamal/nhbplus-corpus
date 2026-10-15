import json, sys, os, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"
def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)
mv = load(r"pipeline\out\manifest-v3.json")
print("### manifest-v3 counts block")
print(json.dumps(mv["counts"], indent=2, ensure_ascii=False))
print("source:", mv["source"])
print()
U = mv["units"]
print("### 'media' field structure")
for u in U[:2]:
    print("  ", json.dumps({k:u[k] for k in ("id","slug","kind","media","has_mp3","has_mp4","title")}, ensure_ascii=False)[:700])
print()
med_types = collections.Counter()
tot = 0
durs = []
sizes = []
for u in U:
    m = u.get("media")
    med_types[type(m).__name__] += 1
    if isinstance(m, list):
        for e in m:
            if isinstance(e, dict):
                for k,v in e.items():
                    if "dur" in k.lower() and isinstance(v,(int,float)): durs.append(v)
                    if k in ("bytes","size") and isinstance(v,(int,float)): sizes.append(v)
    elif isinstance(m, dict):
        for k,v in m.items():
            if "dur" in k.lower() and isinstance(v,(int,float)): durs.append(v)
            if k in ("bytes","size") and isinstance(v,(int,float)): sizes.append(v)
print("   media container types:", dict(med_types))
print("   numeric duration-ish values found:", len(durs), " sum=", sum(durs) if durs else None)
print("   numeric size values found:", len(sizes), " sum=", sum(sizes) if sizes else None)
print()
print("### raw dump of one unit, all fields")
print(json.dumps(U[0], indent=2, ensure_ascii=False))
print()
print("### where do durations live? sample media of a unit that has one")
cand = [u for u in U if isinstance(u.get("media"), list) and u["media"]][:1] or [u for u in U if isinstance(u.get("media"), dict)][:1]
for c in cand:
    print(json.dumps(c.get("media"), indent=2, ensure_ascii=False)[:1200])