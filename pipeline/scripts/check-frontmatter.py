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
# [R4-T5.8] "utterances" and "paragraphs" were banned as bare SUBSTRINGS anywhere
# in the document. A real transcript note discusses utterances and paragraphs in
# its body, so V8 would fail every note it is meant to pass. These are
# FRONTMATTER KEYS. They are now matched as `key:` in a yaml block, never as a
# word in prose.
BANNED_KEYS = [
    "source_handle", "source_ext", "source_url", "source_bytes",
    "mp4_alternate", "duration_s", "duration_human", "manifest_duration_s",
    "words", "utterances", "paragraphs", "stt_request_id", "stt_sha256",
    "vault_path", "extracted_chars", "duration_crosscheck", "size_floor_check",
    "transcribed",
]
BANNED_ANYWHERE = ["## Provenance"]   # body-section bans only

# [R4-T1.9d] This gate has never seen a real note: vault/ is empty and it reads
# the single hand-written YAML block in a DESIGN DOCUMENT. That is "a test that
# passes while proving something else" in its purest form - section 15 claims
# it gates the deliverable. Point it at a real path when one exists, and say so
# until then rather than letting a PASS imply coverage.
import os
VAULT_CANDIDATES = ["vault", "vault-probe"]
def _has_notes(p):
    return os.path.isdir(p) and any(
        f.endswith(".md") for _r, _d, _fs in os.walk(p) for f in _fs)

# prefer a tree that actually holds notes; an empty dir is not a target
DOCS = []   # defined for every path below; the block loop reads it unconditionally
TARGET = next((p for p in VAULT_CANDIDATES if _has_notes(p)), None) \
       or next((p for p in VAULT_CANDIDATES if os.path.isdir(p)), None)

if TARGET and any(
        os.path.join(r, f) for r, _d, fs in os.walk(TARGET) for f in fs
        if f.endswith(".md")):
    _notes = []
    for _r, _d, _fs in os.walk(TARGET):
        _notes += [os.path.join(_r, f) for f in _fs if f.endswith(".md")]
    # [R4-T1.9f] NOTES MUST BE PARSED ONE AT A TIME. Concatenating them and
    # then using \A found only the FIRST note's frontmatter and reported the
    # rest as having none - so a gate over 344 notes silently checked 1.
    DOCS = [(f, io.open(f, encoding="utf-8-sig").read()) for f in _notes]
    s = "\n".join(t for _f, t in DOCS)
    print(f"TARGET: {TARGET} ({len(DOCS)} .md notes)")
elif TARGET:
    # [R4-T3] An EMPTY tree must not read as a PASS. Every gate in section 11
    # needs a FLOOR tied to what should have happened, not a ceiling. `vault/`
    # exists and holds zero notes, so there is nothing to validate and this gate
    # must say so rather than return green.
    s = ""
    print(f"TARGET: {TARGET}  *** EXISTS BUT IS EMPTY - 0 NOTES ***")
    print("       A gate with nothing to check proves nothing. RESULT is FAIL.")
    print("       Expected 344 targets once the run exists. See section 11 floors.")
else:
    s = io.open("stage-1/VAULT-STRUCTURE.md", encoding="utf-8-sig").read()
    print("TARGET: stage-1/VAULT-STRUCTURE.md  [R4-T1.9d] THIS IS AN EXAMPLE,")
    print("       NOT THE DELIVERABLE. vault/ does not exist yet, so a PASS here")
    print("       says nothing about the 344 notes the run will produce.")

print("=== yaml blocks and their fields ===")
ok = True
nblocks = 0

# [F8] VALUE DOMAINS, not just field names. The previous version of this gate
# checked names only, so it returned PASS on a note carrying
# `duration: 3h 14m` - the exact format section 10.1 forbids, and the format V4
# and V10 do arithmetic on. A gate that cannot fail is not a pass.
TYPES = {"call", "theory", "guest", "coaching", "training", "mastermind",
         "other", "lesson", "document"}  # [R4-T1.9] guest=23 and other=59 in the
                                     # manifest. Their absence made 82 of 230
                                     # real notes fail this gate.
DURATION = re.compile(r"[0-9]+")               # [R4-T1.9] >= 0, NOT >= 1. [F40]
                                           # corrected this in PROSE and the code
                                           # kept 1 - so A2dWSZAK (media.dur_s
                                           # = 50, floors to 0) fails the gate that
                                           # was written to catch its opposite.
DATE     = re.compile(r"([0-9]{4}-[0-9]{2}-[0-9]{2})|unknown")  # [R4-T1.9] section 10.1
                                     # says "or unknown" and "unknown, never null".
                                     # "undated" was MY invention and would fail
                                     # 44 of 230 real notes at this gate.
DOMAIN_ERRORS = []

# [R4-T1.9e] THIS GATE ONLY EVER PARSED FENCED ```yaml BLOCKS INSIDE A DESIGN
# DOCUMENT. Real vault notes use `---` frontmatter delimiters at the top of the
# file, which this never matched - so pointed at a real note it would have found
# zero blocks and reported success. Both forms are now recognised; the fenced
# form is kept because VAULT-STRUCTURE.md still uses it.
_blocks = []
for _f, _t in (DOCS if TARGET and DOCS else [("(design doc)", s)]):
    for _m in re.findall(r"\A---\s*\n(.*?)\n---", _t, re.S):
        _blocks.append((_f, _m))
    for _m in re.findall(r"```yaml(.*?)```", _t, re.S):
        _blocks.append((_f, _m))
# Count REAL blocks before any padding. [R4-T3] padding the list to avoid a
# crash also made `nblocks` permanently >= 1, so the "nothing to validate"
# guard could never fire and an empty tree PASSED. That is the empty-vs-empty
# trap this project has hit twice, in its own gate.
n_real = len(_blocks)
_blocks = _blocks or [("(none)", "")]
for i, (_src, b) in enumerate(_blocks, 1):
    nblocks += 1
    fields = re.findall(r"^([a-z_]+):", b, re.M)
    vals = dict(re.findall(r"^([a-z_]+):\s*(.*?)\s*$", b, re.M))
    limit = ALLOWED          # [B16] one shape, one allow-list
    extra = [f for f in fields if f not in limit]
    print(f"  block {i} [{_src}]: {fields}")
    print(f"           allowed: {sorted(limit)}")
    print(f"           EXTRA  : {extra if extra else 'none'}")
    if extra:
        ok = False
    for k, v in vals.items():
        v = v.strip().strip("'\"")
        if k == "duration":
            if not DURATION.fullmatch(v):
                e = (f"block {i} [{_src}]: duration={v!r} must be an integer of MINUTES >= 0"
                                     f" - never '3h 14m'")
                DOMAIN_ERRORS.append(e)
        elif k == "date":
            if not DATE.fullmatch(v):
                DOMAIN_ERRORS.append(f"block {i} [{_src}]: date={v!r} must be YYYY-MM-DD or 'unknown'")
        elif k == "type":
            if v not in TYPES:
                DOMAIN_ERRORS.append(f"block {i} [{_src}]: type={v!r} not in {sorted(TYPES)}")
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
if n_real == 0:
    print(f"    XX NO REAL FRONTMATTER FOUND ({nblocks} padded placeholder) -"
          " the gate proved nothing")
    ok = False

print("\n=== banned fields anywhere in the document ===")
hits = [b for b in BANNED_ANYWHERE if b in s]
_banned_keys = sorted({k for _b in re.findall(r"```yaml(.*?)```", s, re.S)
                       for k in re.findall(r"^([a-z_]+):", _b, re.M)
                       if k in BANNED_KEYS})
print(f"  banned body sections : {hits if hits else 'NONE'}")
print(f"  banned FRONTMATTER keys: {_banned_keys if _banned_keys else 'NONE'}")
if hits or _banned_keys:
    ok = False

print("\n=== other ===")
print(f"  '## Provenance' section present : {'## Provenance' in s}")
print(f"  written-hands/ tree present     : {'written-hands/' in s}")
print(f"  U+FFFD                          : {s.count(chr(0xFFFD))}")
print(f"  lines                           : {s.count(chr(10)) + 1}")
print(f"\n  RESULT: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)