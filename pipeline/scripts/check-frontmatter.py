#!/usr/bin/env python3
"""
Verify VAULT-STRUCTURE.md carries only the five agreed frontmatter fields.
Run:  python check-frontmatter.py
The operator cut the source, transcription, integrity and provenance blocks on
2026-10-15. This asserts they are actually gone rather than trusting the edit.
"""
import io, re, sys

ALLOWED = {"title", "date", "type", "duration", "speakers"}
# [B16] DELETED, not repaired. This allow-list existed for the written-hand
# shape {title, kind, date, source_call}, which section 4a of VAULT-STRUCTURE.md
# no longer declares - that section now carries the SAME five fields as every
# other note, with the shape in `type`. It was unreachable anyway: the loop
# applied it only to blocks after the first, and exactly one yaml block exists in
# the document, so it never ran. A dead branch that asserts a shape the spec
# rejected is worse than no branch - it looks like coverage.
# There is now ONE allow-list for ONE shape.
assert ALLOWED == {"title", "date", "type", "duration", "speakers"}, \
    "every note shape carries the same five fields (B16)"
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
nblocks = 0

# [F8] VALUE DOMAINS, not just field names. The previous version of this gate
# checked names only, so it returned PASS on a note carrying
# `duration: 3h 14m` - the exact format section 10.1 forbids, and the format V4
# and V10 do arithmetic on. A gate that cannot fail is not a pass.
TYPES = {"call", "theory", "coaching", "training", "mastermind", "lesson", "document"}
DURATION = re.compile(r"[1-9][0-9]*")          # integer >= 1 minutes. NO 'h'/'m'.
DATE     = re.compile(r"([0-9]{4}-[0-9]{2}-[0-9]{2})|undated")
DOMAIN_ERRORS = []

for i, b in enumerate(re.findall(r"```yaml(.*?)```", s, re.S), 1):
    nblocks += 1
    fields = re.findall(r"^([a-z_]+):", b, re.M)
    vals = dict(re.findall(r"^([a-z_]+):\s*(.*?)\s*$", b, re.M))
    limit = ALLOWED          # [B16] one shape, one allow-list
    extra = [f for f in fields if f not in limit]
    print(f"  block {i}: {fields}")
    print(f"           allowed: {sorted(limit)}")
    print(f"           EXTRA  : {extra if extra else 'none'}")
    if extra:
        ok = False
    for k, v in vals.items():
        v = v.strip().strip("'\"")
        if k == "duration":
            if not DURATION.fullmatch(v):
                e = f"block {i}: duration={v!r} must be an integer of MINUTES >= 1"
                DOMAIN_ERRORS.append(e)
        elif k == "date":
            if not DATE.fullmatch(v):
                DOMAIN_ERRORS.append(f"block {i}: date={v!r} must be YYYY-MM-DD or 'undated'")
        elif k == "type":
            if v not in TYPES:
                DOMAIN_ERRORS.append(f"block {i}: type={v!r} not in {sorted(TYPES)}")
        elif k == "title":
            if not v:
                DOMAIN_ERRORS.append(f"block {i}: title is empty")

print(f"\n=== [F8] value domains ===")
print(f"  blocks found : {nblocks}")
print(f"  VIOLATIONS   : {len(DOMAIN_ERRORS)}")
for e in DOMAIN_ERRORS:
    print(f"    XX {e}")
if DOMAIN_ERRORS:
    ok = False
if nblocks == 0:
    print("    XX no yaml block found - the gate proved nothing")
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