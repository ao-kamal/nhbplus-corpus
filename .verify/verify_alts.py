import json, sys, os, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"
def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)
mv = load(r"pipeline\out\manifest-v3.json"); U = mv["units"]
sf = load(r"pipeline\out\scope-final.json"); T = sf["targets"]

print("### units with NO media.dur_s in manifest-v3")
nod = [u for u in U if not isinstance(u.get("media"),dict) or u["media"].get("dur_s") is None]
for u in nod:
    print("   ", u["id"], "|", json.dumps(u.get("media"), ensure_ascii=False)[:300])
print()
print("### scope-final audio targets with NO dur_s")
nods = [t for t in T if t["kind"]=="audio" and t.get("dur_s") is None]
for t in nods:
    print("   ", t.get("unit"), "| handle=", t.get("handle"), "| bytes=", t.get("bytes"))
print()
print("   scope-final: 2 missing.  manifest-v3:", len(nod), "missing.")
ids_s = {t.get("unit") for t in nods}
ids_m = {u["id"] for u in nod}
print("   scope-only missing:", ids_s - ids_m)
print("   manifest-only missing:", ids_m - ids_s)

print()
print("### CALL/LESSON hours check: counts.call_hours vs recomputed")
ch = sum(u["media"]["dur_s"] for u in U if u.get("kind")=="calls" and isinstance(u.get("media"),dict) and u["media"].get("dur_s") is not None)
lh = sum(u["media"]["dur_s"] for u in U if u.get("kind")=="lessons" and isinstance(u.get("media"),dict) and u["media"].get("dur_s") is not None)
print(f"   calls   {ch} s = {ch/3600:.2f} h   stated call_hours  = {mv['counts']['call_hours']}")
print(f"   lessons {lh} s = {lh/3600:.2f} h   stated lesson_hours= {mv['counts']['lesson_hours']}")
print(f"   TOTAL   {(ch+lh)/3600:.2f} h  stated = {(ch+lh)/3600:.2f}  (spec asserts 583.55)")

print()
print("### ALTERNATE (MP4) BYTES -- sentinel check")
alts = []
for u in U:
    m = u.get("media")
    if isinstance(m, dict):
        for a in (m.get("alternates") or []):
            alts.append(a)
print("   total alternates:", len(alts), " stated not_billed_alternates =", mv["counts"]["not_billed_alternates"])
bc = collections.Counter(a.get("bytes") for a in alts)
print("   distinct bytes values:", dict(list(bc.items())[:10]), "... distinct count =", len(bc))
print("   2147483648 == 2 GiB sentinel appears:", bc.get(2147483648,0), "times")
tb = sum((a.get("bytes") or 0) for a in alts)
print(f"   sum alternate bytes = {tb:,} = {tb/1e9:.2f} GB = {tb/2**30:.2f} GiB   (spec says 'Saves 132 GB')")
print("   alternate ext counts:", dict(collections.Counter(a.get("ext") for a in alts)))
print("   alternates with dur_s:", sum(1 for a in alts if a.get('dur_s') is not None))

print()
print("### '603.84 h raw -> 583.55 h after merge' -- does 603.84 exist anywhere?")
tot_raw = sum((u['media'].get('dur_s') or 0) for u in U if isinstance(u.get('media'),dict))
print(f"   primary-media sum = {tot_raw/3600:.2f} h")
raw_all = tot_raw + sum((a.get('dur_s') or 0) for a in alts)
print(f"   primary+alternates sum = {raw_all/3600:.2f} h")
print("   (603.84 would be raw union of all files incl. mp4 siblings; search repo next)")