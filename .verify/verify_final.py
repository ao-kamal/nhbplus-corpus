import os, sys, json, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"
def load(p): return json.load(open(os.path.join(ROOT,p),encoding="utf-8"))

print("### alternate bytes: are they real sizes or MiB-rounded / sentinel?")
mv=load(r"pipeline\out\manifest-v3.json")
alts=[a for u in mv["units"] for a in (u["media"].get("alternates") or [])]
mib=2**20
nonint=[a for a in alts if (a.get("bytes") or 0)%mib]
print(f"   alternates={len(alts)}  bytes NOT a whole MiB multiple: {len(nonint)}")
c=collections.Counter(a["bytes"]//mib for a in alts)
print(f"   most common sizes (MiB): {c.most_common(6)}")
print(f"   exactly 2048 MiB (2 GiB): {c.get(2048,0)} times   1024 MiB: {c.get(1024,0)}   3072 MiB: {c.get(3072,0)}")
print(f"   sum = {sum(a['bytes'] for a in alts):,} = {sum(a['bytes'] for a in alts)/1e9:.2f} GB = {sum(a['bytes'] for a in alts)/2**30:.2f} GiB")
print(f"   spec says 'Saves 132 GB'.  132 GB = {132*1e9:,} bytes ; 132 GiB = {132*2**30:,} bytes")
print(f"   neither the sum nor 105*avg matches 132.")
# what avg would give 132?
print(f"   132 GB / 105 files = {132*1e9/105/1e9:.3f} GB/file")

print()
print("### PDF probe: taxonomy + word count (spec 48/2/0, 65,985 words, 0.159 GB, 50 fetched)")
pb=load(r"evidence\probes\nhbplus-pdf-text-layer-2026-10-15.json")
print("   top keys:", list(pb.keys()))
def find(o,key,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k==key: print(f"      {path}/{k} = {json.dumps(v,ensure_ascii=False)[:300]}")
            find(v,key,f"{path}/{k}")
    elif isinstance(o,list) and o and isinstance(o[0],dict):
        find(o[0],key,f"{path}[0]")
for key in ("class_counts","taxonomy","words_total","total_words","recoverable_words","pdf_count","documents","sparse","counts"):
    find(pb,key)

print()
print("### spec 0.159 GB for 50 PDFs")
sf=load(r"pipeline\out\scope-final.json")
pdfs=[t for t in sf["targets"] if str(t.get("ext","")).lower()=="pdf"]
pb2=sum((t.get("bytes") or 0) for t in pdfs)
print(f"   scope-final PDF bytes = {pb2:,} = {pb2/1e9:.4f} GB = {pb2/2**30:.4f} GiB   -> spec's '0.159 GB' is GiB again")

print()
print("### doc extension breakdown (spec: 50 pdf + '59 docx/pptx/xlsx')")
docs=[t for t in sf["targets"] if t["kind"] in ("written_hand","course_doc","orphan_doc")]
ex=collections.Counter(str(t.get("ext")).lower() for t in docs)
print("   ", dict(ex), " total", sum(ex.values()))
ooxml=ex["docx"]+ex["pptx"]+ex["xlsx"]
print(f"   docx+pptx+xlsx = {ooxml}   (spec asserts 59)")
print(f"   remainder = {sum(ex.values())-50-ooxml}:  txt={ex['txt']} png={ex['png']} zip={ex['zip']}")
print("   the spec's '59' == 109-50, so it assumes ALL non-PDF are OOXML. The 6 txt / 1 png / 1 zip disprove that.")
for t in docs:
    if str(t.get("ext")).lower() in ("png","zip"):
        print(f"      {t['kind']}: {t.get('name')!r} ext={t.get('ext')} bytes={t.get('bytes')}")