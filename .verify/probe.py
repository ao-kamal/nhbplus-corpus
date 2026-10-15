import json, sys, os, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"

def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)

sf = load(r"pipeline\out\scope-final.json")
print("=== scope-final.json TOP-LEVEL TYPE:", type(sf).__name__)
if isinstance(sf, dict):
    for k, v in sf.items():
        t = type(v).__name__
        n = len(v) if isinstance(v, (list, dict, str)) else v
        print(f"  key={k!r:40s} type={t:6s} len/value={n}")
print()

# dig down
def walk(o, path="", depth=0):
    if depth > 3:
        return
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)):
                print("  "*depth + f"{path}/{k}  {type(v).__name__} len={len(v)}")
                walk(v, f"{path}/{k}", depth+1)
            else:
                print("  "*depth + f"{path}/{k} = {v!r}"[:160])
    elif isinstance(o, list):
        print("  "*depth + f"{path}[] len={len(o)}  first={repr(o[0])[:400] if o else None}")

print("--- full structure walk ---")
walk(sf)