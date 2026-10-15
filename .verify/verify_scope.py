import json, sys, os, collections, math
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"
def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)

sf = load(r"pipeline\out\scope-final.json")
T = sf["targets"]
print("### CLAIM 1: exactly 339 targets, sum(bytes) == 146.87 GB")
print("  len(targets) =", len(T))
sumb = sum((t.get("bytes") or 0) for t in T)
print(f"  sum(bytes)   = {sumb:,} bytes")
print(f"  = {sumb/1e9:.4f} GB (decimal)   = {sumb/2**30:.4f} GiB (binary)")
print(f"  totals.total_GB = {sf['totals']['total_GB']}")
print(f"  delta vs totals.total_GB: {sumb/1e9 - sf['totals']['total_GB']:+.4f}")
print(f"  MATCHES 146.87 within 0.01? {abs(sumb/1e9 - 146.87) < 0.01}")

print()
print("### CLAIM 2: audio 188 / bonus 42 / docs 109")
kinds = collections.Counter(t["kind"] for t in T)
print("  kind counts:", dict(kinds))
# distinguish calls vs lessons inside audio
def is_call(t):
    return t.get("type") not in ("bonus", "lesson") and not str(t.get("unit","")).startswith("bonus")
subs = collections.Counter()
for t in T:
    if t["kind"] == "audio":
        subs[(t.get("type"), str(t.get("unit","")).split("-")[0][:6])] += 1
print("  audio subtypes (type, unit-prefix):", dict(subs))
print("  audio total =", kinds.get("audio"), " docs total =", kinds.get("course_doc",0)+kinds.get("orphan_doc",0)+kinds.get("written_hand",0))
print(f"  188+42+109 = {188+42+109}  (vs len targets {len(T)})")

# Does any field mark calls vs lessons?
print("  audio unit names that do NOT start with a 4-digit year:")
for t in T:
    if t["kind"]=="audio":
        u = t["unit"]
        if not (len(u)>=4 and u[:4].isdigit()):
            print("    ", u)
            break
audio_units = [t for t in T if t["kind"]=="audio"]
print("  distinct 'type' among audio:", collections.Counter(t.get('type') for t in audio_units))

print()
print("### CLAIM 3: documents partition 37 written_hand + 36 course_doc + 36 orphan")
docs = [t for t in T if t["kind"] in ("written_hand","course_doc","orphan_doc")]
print("  doc kind counts:", dict(collections.Counter(t["kind"] for t in docs)))
print("  doc total =", len(docs))
print("  37+36+36 =", 37+36+36, " actual =", len(docs), " MATCH:", len(docs)==109)
print("  SPEC V9 says 'counts 37 / 36 (+36 orphan)' -> 37+36+36=109")

print()
print("### CLAIM 4: how many documents are PDFs (spec says 50)")
docs_ext = collections.Counter(str(t.get("ext","")).lower().lstrip(".") for t in docs)
print("  doc extensions:", dict(docs_ext))
pdfs = [t for t in docs if str(t.get("ext","")).lower()=="pdf"]
print("  PDFs =", len(pdfs))
pdfbytes = sum((t.get("bytes") or 0) for t in pdfs)
print(f"  PDF bytes = {pdfbytes:,} = {pdfbytes/1e9:.4f} GB = {pdfbytes/2**30:.4f} GiB   (spec says 0.159 GB)")
allbytes = sum((t.get("bytes") or 0) for t in docs)
print(f"  all doc bytes = {allbytes:,} = {allbytes/1e9:.4f} GB = {allbytes/2**30:.4f} GiB  (totals.document_GB={sf['totals']['document_GB']})")

print()
print("### CLAIM 5: 105 MP4 siblings recorded but not fetched")
n_alt_files = sum(len(t.get("alternates_not_fetched",[]) or []) for t in T)
alt_exts = collections.Counter()
alt_files_raw = []
for t in T:
    for a in (t.get("alternates_not_fetched",[]) or []):
        alt_files_raw.append(a)
        alt_exts[str(a).split(".")[-1].lower()] += 1
print("  total alternate file entries =", n_alt_files)
print("  top-level mp4_alternates_never_fetched =", sf["mp4_alternates_never_fetched"])
print("  distinct alternate handles =", len(set(alt_files_raw)))
print("  (alt handles are opaque ids; extension counted from id is meaningless:", dict(alt_exts),")")

print()
print("### CLAIM 6: derivation of $150.56 in repo?")
print("  totals.stt_forecast_usd =", sf["totals"]["stt_forecast_usd"])
print("  audio_hours =", sf["totals"]["audio_hours"])
rate = 150.56/35013
print(f"  spec RATE = 150.56/35013 = {rate:.8f} USD/min")
print(f"  35013 min = {35013/60:.2f} h  vs totals.audio_hours = {sf['totals']['audio_hours']}")
print(f"  583.55 h * 60 = {583.55*60} min")
print(f"  150.56 / {35013} = {150.56/35013:.8f}")
# reverse-engineer: what per-hour rate gives 150.56?
print(f"  implied USD/hour = {150.56/583.55:.6f}")
print(f"  implied USD/min on 35013min = {150.56/35013:.8f} -> deepgram nova-3 EU+di? unknown")

print()
print("### EXTRA: unreconciled notes")
for u in sf["unreconciled"]:
    print("  -", u[:300])
print("  decisions.B_encoding =", sf["decisions"]["B_encoding"])
print("  (!! that says 88 MP4 siblings, top-level says 105)")