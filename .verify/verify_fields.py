import json, sys, os, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"
def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)
sf = load(r"pipeline\out\scope-final.json")
T = sf["targets"]

keys = collections.Counter()
for t in T: keys.update(t.keys())
print("### field presence across 339 targets")
for k,v in keys.most_common(): print(f"   {k:28s} present in {v}")

print()
print("### audio targets: any field marking call vs lesson?")
audio = [t for t in T if t["kind"]=="audio"]
print("  sample audio target keys:", sorted(audio[0].keys()))
# look for label/type/date patterns
print("  distinct labels:", sorted({str(t.get('label')) for t in audio})[:20])
print()
print("  distinct 'label' for non-audio:", sorted({str(t.get('label')) for t in T if t['kind']!='audio'})[:20])

print()
print("### CLAIM 8: are all 188 calls dated? (audience: audio population)")
noday = [t for t in audio if not t.get("date") or str(t.get("date")).lower() in ("none","null","unknown","tbd","","undated")]
print("  audio targets with missing/placeholder date:", len(noday))
for t in noday:
    print("    unit=", t.get("unit"), "| date=", repr(t.get("date")), "| label=", repr(t.get("label")),
          "| topic=", repr(t.get("topic")), "| handle=", t.get("handle"), "| dur_s=", t.get("dur_s"))
print()
# year recoverable from unit string
noyear = [t for t in audio if t.get("date") is None]
print("  audio targets with date == None:", len(noyear))
for t in audio:
    u = str(t.get("unit") or "")
    if u.startswith("undated"):
        print("    UNDATED-UNIT:", u, "| date=", repr(t.get("date")), "| label=", repr(t.get("label")), "| topic=", repr(t.get("topic")))
print()
print("### dur_s sanity")
nd = [t for t in audio if not t.get("dur_s")]
print("  audio targets with no dur_s:", len(nd), [t.get('unit') for t in nd])
tot = sum((t.get("dur_s") or 0) for t in audio)
print(f"  sum(dur_s) audio = {tot} s = {tot/3600:.2f} h   totals.audio_hours = {sf['totals']['audio_hours']}")
print("  MATCH 583.55?", abs(tot/3600 - 583.55) < 0.01)