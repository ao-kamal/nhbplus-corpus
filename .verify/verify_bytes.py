import json, sys, os, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"
def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)
sf = load(r"pipeline\out\scope-final.json")
T = sf["targets"]
none_b = [t for t in T if t.get("bytes") is None]
print("targets with bytes == None:", len(none_b))
for t in none_b:
    print("   kind=", t.get("kind"), "| unit=", t.get("unit"), "| label=", t.get("label"),
          "| type=", t.get("type"), "| ext=", t.get("ext"), "| bytes=", t.get("bytes"),
          "| dur_s=", t.get("dur_s"), "| handle=", t.get("handle"))
print()
missing_key = [t for t in T if "bytes" not in t]
print("targets with NO 'bytes' key at all:", len(missing_key))
print()
sumb = sum((t.get("bytes") or 0) for t in T)
print(f"sum(bytes) treating None as 0 = {sumb:,} = {sumb/1e9:.4f} GB (dec) = {sumb/2**30:.4f} GiB")
print("totals.total_GB =", sf["totals"]["total_GB"])
print("totals.audio_GB =", sf["totals"]["audio_GB"], " document_GB =", sf["totals"]["document_GB"])
aud = sum((t.get('bytes') or 0) for t in T if t['kind']=='audio')
print(f"audio bytes sum = {aud:,} = {aud/1e9:.4f} GB")
docs = [t for t in T if t['kind'] in ('written_hand','course_doc','orphan_doc')]
db = sum((t.get('bytes') or 0) for t in docs)
print(f"doc bytes sum   = {db:,} = {db/1e9:.4f} GB")
print(f"audio+doc = {(aud+db)/1e9:.4f} GB")
print()
print("by_kind recomputed vs stated:")
bk = collections.defaultdict(lambda: [0,0])
for t in T:
    bk[t["kind"]][0]+=1
    bk[t["kind"]][1]+= (t.get("bytes") or 0)
for k in sorted(bk):
    print(f"  {k:14s} n={bk[k][0]:4d} bytes={bk[k][1]:>15,} = {bk[k][1]/1e9:.4f} GB   stated={sf['by_kind'].get(k)}")