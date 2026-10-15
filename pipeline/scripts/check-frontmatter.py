#!/usr/bin/env python3
"""
Verify VAULT-STRUCTURE.md carries only the five agreed frontmatter fields.
Run:  python check-frontmatter.py
The operator cut the source, transcription, integrity and provenance blocks on
2026-10-15. This asserts they are actually gone rather than trusting the edit.
"""
import io, re, sys

ALLOWED = {"title", "date", "type", "duration", "speakers"}
ALLOWED_WRITTEN_HAND = {"title", "kind", "date", "source_call"}
BANNED_ANYWHERE = [
    "source_handle", "source_ext", "source_url", "source_bytes",
    "mp4_alternate", "duration_s:", "duration_human", "manifest_duration_s",
    "words:", "utterances", "paragraphs", "stt_request_id", "stt_sha256",
    "vault_path", "extracted_chars", "duration_crosscheck", "size_floor_check",
    "transcribed:", "## Provenance",
]

s = io.open("stage-1/VAULT-STRUCTURE.md", encoding="utf-8").read()

print("=== yaml blocks and their fields ===")
ok = True
for i, b in enumerate(re.findall(r"```yaml(.*?)```", s, re.S), 1):
    fields = re.findall(r"^([a-z_]+):", b, re.M)
    limit = ALLOWED if i == 1 else ALLOWED_WRITTEN_HAND
    extra = [f for f in fields if f not in limit]
    print(f"  block {i}: {fields}")
    print(f"           allowed: {sorted(limit)}")
    print(f"           EXTRA  : {extra if extra else 'none'}")
    if extra:
        ok = False

print("\n=== banned fields anywhere in the document ===")
hits = [b for b in BANNED_ANYWHERE if b in s]
print(f"  {hits if hits else 'NONE'}")
if hits:
    ok = False

print("\n=== other ===")
print(f"  '## Provenance' section present : {'## Provenance' in s}")
print(f"  written-hands/ tree present     : {'written-hands/' in s}")
print(f"  U+FFFD                          : {s.count(chr(0xFFFD))}")
print(f"  lines                           : {s.count(chr(10)) + 1}")
print(f"\n  RESULT: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)