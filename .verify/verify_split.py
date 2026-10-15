import json, sys, os, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\layiw\Documents\Kamal\nhbplus-corpus"
def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)
sf = load(r"pipeline\out\scope-final.json")
audio = [t for t in sf["targets"] if t["kind"]=="audio"]

lessonish = [t for t in audio if str(t.get("label","")).startswith("undated ·")]
print("### calls vs lessons discriminator test")
print("  audio total:", len(audio))
print("  label startswith 'undated \\u00b7':", len(lessonish), "  <- candidate = lessons (spec: 42)")
undated = [t for t in audio if t.get("date") is None]
print("  date is None:", len(undated))
other = [t for t in undated if t not in lessonish]
print("  undated but NOT lesson-shaped:", len(other))
for t in other:
    print("     unit=", t.get("unit"), "| label=", repr(t.get("label")), "| topic=", repr(t.get("topic")), "| dur_s=", t.get("dur_s"))
dated = [t for t in audio if t.get("date") is not None]
print("  audio WITH a date:", len(dated))
print("  => if 42 lessons: calls =", len(audio)-42, "(spec asserts 188)")
print()
print("### target 'unit' prefix year distribution")
yr = collections.Counter()
for t in audio:
    u = str(t.get("unit") or "")
    yr[u[:4] if u[:4].isdigit() else "UNDATED"] += 1
print("  ", dict(sorted(yr.items())))
print()
print("### the 6 course_doc with bytes=None - full records")
for t in sf["targets"]:
    if t.get("bytes") is None:
        print("   ", json.dumps(t, ensure_ascii=False)[:500])
print()
print("### documents: 'name' and 'course'/'folder' fields")
docs = [t for t in sf["targets"] if t["kind"] in ("written_hand","course_doc","orphan_doc")]
for k in ("written_hand","course_doc","orphan_doc"):
    sub=[t for t in docs if t["kind"]==k]
    ex = collections.Counter(str(t.get("ext")) for t in sub)
    print(f"  {k:14s} n={len(sub):3d} exts={dict(ex)}")
print()
print("### doc record shape sample (one of each kind)")
for k in ("written_hand","course_doc","orphan_doc"):
    t = next(t for t in docs if t["kind"]==k)
    print(f"  --- {k}: {json.dumps(t, ensure_ascii=False)[:600]}")