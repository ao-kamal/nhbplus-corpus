import json, sys, os, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"
def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)
mv = load(r"pipeline\out\manifest-v3.json")
print("### manifest-v3.json structure")
for k,v in mv.items():
    t=type(v).__name__
    n=len(v) if isinstance(v,(list,dict,str)) else v
    print(f"   {k!r:36s} {t:6s} len/val={n}")

units = mv.get("units") or mv.get("targets") or []
print()
print("### CLAIM 7: exactly 230 units (188 calls + 42 lessons), 583.55 h")
print("   units:", len(units))
if units:
    print("   unit keys:", sorted(units[0].keys()))
    kinds = collections.Counter(u.get("kind") or u.get("type") for u in units)
    print("   kind/type:", dict(kinds))
    d = [u.get("dur_s") for u in units if u.get("dur_s") is not None]
    print(f"   sum(dur_s) over {len(d)} units = {sum(d)} s = {sum(d)/3600:.4f} h")
    nod = [u for u in units if u.get("dur_s") is None]
    print("   units with no dur_s:", len(nod))
    for u in nod[:10]: print("      ", json.dumps(u, ensure_ascii=False)[:300])
print()
print("### CLAIM 8: all 188 calls dated?")
DATEKEYS = ("date","day","call_date","recorded")
und = [u for u in units if not any(u.get(k) for k in DATEKEYS)]
print("   units with no date field:", len(und))
for u in und:
    print("      ", json.dumps(u, ensure_ascii=False)[:260])
print()
print("### CLAIM 9: '10-31-2022 NHB+ Mindstream Call' present?")
hit=[]
for u in units:
    s = json.dumps(u, ensure_ascii=False)
    if "Mindstream" in s or "Mindstream" in s:
        hit.append(u)
print("   units mentioning 'Mindstream':", len(hit))
for u in hit: print("      ", json.dumps(u, ensure_ascii=False)[:400])
print("   name-like fields containing 'mindstream' (case-insens) elsewhere in file:")
s = json.dumps(mv, ensure_ascii=False)
import re
for m in set(re.findall(r'"[^"]*[Mm]indstream[^"]*"', s)):
    print("      ", m)