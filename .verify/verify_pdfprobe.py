import os, sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"
pb=json.load(open(os.path.join(ROOT,"evidence","probes","nhbplus-pdf-text-layer-2026-10-15.json"),encoding="utf-8"))
for k in ("probe","date","status","verdict","cost","classification_taxonomy","open","reproduce"):
    print(f"--- {k} ---")
    print(json.dumps(pb.get(k), indent=1, ensure_ascii=False)[:2600])
    print()