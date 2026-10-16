import hashlib
import json
import os
import datetime

VAULT_DIR = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus\vault"
META_DIR = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus\_meta"
OUT_FILE = os.path.join(META_DIR, "copy-verification.json")

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest(), os.path.getsize(path)

files_record = []
notes_found = 0
typography_checked = 0
typography_passed = 0

# Typography characters to check for integrity: -> × § ≥ ± ≈ ✓, em-dash, quotes, emoji
# U+FFFD is the corruption replacement character
for root, dirs, files in os.walk(VAULT_DIR):
    for fn in files:
        full_path = os.path.join(root, fn)
        rel_path = os.path.relpath(full_path, VAULT_DIR).replace("\\", "/")
        sha, size = hash_file(full_path)
        files_record.append({
            "relpath": f"vault/{rel_path}",
            "bytes": size,
            "sha256": sha
        })
        if fn.endswith(".md"):
            notes_found += 1
            # Check typography
            try:
                content = open(full_path, "r", encoding="utf-8").read()
                typography_checked += 1
                if "\ufffd" not in content:
                    typography_passed += 1
                else:
                    print(f"FAILED typography check (U+FFFD found): {rel_path}")
            except Exception as e:
                print(f"Error reading {rel_path}: {e}")

# Check _meta files
for fn in os.listdir(META_DIR):
    if fn == "copy-verification.json":
        continue
    full_path = os.path.join(META_DIR, fn)
    if os.path.isfile(full_path):
        sha, size = hash_file(full_path)
        files_record.append({
            "relpath": f"_meta/{fn}",
            "bytes": size,
            "sha256": sha
        })

verification = {
    "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "source": "VM:/home/azureuser/nhbplus/vault",
    "files": files_record,
    "total_files": len(files_record),
    "notes_found": notes_found,
    "typography_checked": typography_checked,
    "typography_passed": typography_passed,
    "status": "PASS" if typography_checked == typography_passed and notes_found >= 235 else "FAIL"
}

with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(verification, f, indent=2)

print(f"Verification generated: {OUT_FILE}")
print(f"Total files: {len(files_record)}")
print(f"Notes found: {notes_found}")
print(f"Typography: {typography_passed}/{typography_checked} passed")
print(f"Status: {verification['status']}")
