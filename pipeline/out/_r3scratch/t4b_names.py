#!/usr/bin/env python3
"""R3: second pass on names - the defect classes round 2 and the spec missed."""
import json, os, re, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
def jload(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)

cn = jload(os.path.join(OD, "clean-names.json"))
man = jload(os.path.join(OD, "manifest-v3.json"))
units = man["units"]
calls, lessons, docs = cn["calls"], cn["lessons"], cn["documents"]

print("=" * 78)
print("A. Mangled intra-word hyphen, EXACTLY (verbatim had no space, emitted has ' - ')")
print("=" * 78)
mang = []
for label, rows, key in [("call", calls, "path"), ("lesson", lessons, "path"),
                         ("doc", docs, "clean")]:
    for r in rows:
        v = r["verbatim"]
        out = r[key]
        # any letter-hyphen-letter in the verbatim whose site is now ' - ' in the output
        for m in re.finditer(r"[A-Za-z]-[A-Za-z]", v):
            a, b = m.group(0)[0], m.group(0)[-1]
            # find the corresponding mangled site: look for 'a - b' in the output
            if re.search(re.escape(a) + r"\s*-\s*" + re.escape(b), out):
                mang.append((label, v, out))
                break
print(f"  total mangled intra-word hyphens: {len(mang)}")
for label, v, out in mang:
    print(f"     [{label}] {v[:66]!r}")
    print(f"            -> {out[:66]!r}")
print()
print("  ALL names (any kind) containing a letter-hyphen-letter in the verbatim:")
n = 0
for label, rows in [("call", calls), ("lesson", lessons), ("doc", docs)]:
    c = sum(1 for r in rows if re.search(r"[A-Za-z]-[A-Za-z]", r["verbatim"]))
    print(f"     {label:<7} {c}")
    n += c
print(f"     TOTAL {n}")

print()
print("=" * 78)
print("B. PLATFORM SUFFIX LEAKED INTO THE CLEAN NAME ('on Vimeo' etc.)")
print("=" * 78)
PLAT = re.compile(r"\s+on\s+(vimeo(\.com)?|youtube(\.com)?|wistia|loom|teachable)\s*$", re.I)
leak = [c for c in calls if PLAT.search(c["verbatim"])]
print(f"  verbatim carrying a platform suffix: {len(leak)}")
still = [c for c in leak if PLAT.search(c["path"].rsplit("/", 1)[-1])]
print(f"  ... still present in the EMITTED filename: {len(still)}")
for c in still:
    print(f"     {c['path'].rsplit('/',1)[-1]}")
print("  lesson/doc names with platform suffix:",
      sum(1 for l in lessons if PLAT.search(l['verbatim'])),
      sum(1 for d in docs if PLAT.search(d['verbatim'])))

print()
print("=" * 78)
print("C. TYPE DOMAIN vs §10.1  (theory|guest|coaching|training|mastermind|other)")
print("=" * 78)
print("  manifest type counts:", dict(Counter(u["type"] for u in units)))
print("  clean-names call type counts:", dict(Counter(c["type"] for c in calls)))
DOM = {"theory", "guest", "coaching", "training", "mastermind", "other"}
bad = [(u["media"]["handle"], u["type"], u["media"]["name"][:60])
       for u in units if u["type"] not in DOM]
print(f"  units whose type is OUTSIDE the §10.1 domain: {len(bad)}")
for h, t, nm in bad[:20]:
    print(f"     {h}  type={t!r}  {nm}")
print("  V8 would fail on:", len(bad), "notes" if bad else "")

print()
print("=" * 78)
print("D. topic IS casefolded in manifest-v3 (the §2.2.1 keyterm warning)")
print("=" * 78)
caps = [u for u in units if u["topic"] != u["topic"].casefold()]
print(f"  units whose topic is NOT lowercase: {len(caps)}")
noalpha = [u for u in units if not re.search(r"[A-Z]", u["topic"])]
print(f"  units whose topic contains NO capital letter at all: {len(noalpha)} "
      f"of {len(units)}")
print("  -> keyterm built from `topic` alone yields an empty list for "
      f"{len(noalpha)}/{len(units)} units")
mcaps = [u for u in units if re.search(r"[A-Z]", u["media"]["name"])]
print(f"  units whose media.name carries capitals: {len(mcaps)}/{len(units)}")

print()
print("=" * 78)
print("E. DURATION / SPEAKERS AVAILABILITY FOR §10.1")
print("=" * 78)
nd = [u for u in units if not u["media"]["dur_s"]]
print(f"  units with no dur_s -> duration must be 'unknown': {len(nd)}")
for u in nd:
    print(f"     {u['media']['handle']} {u['media']['name'][:56]}")
# is any dur_s < 60s (would round to 0 minutes)?
tiny = [u for u in units if u["media"]["dur_s"] and u["media"]["dur_s"] < 60]
print(f"  units with dur_s < 60 s (round to 0 minutes -> V8 'integer >= 1' fails): "
      f"{len(tiny)}")
for u in tiny:
    print(f"     {u['media']['handle']} dur={u['media']['dur_s']} {u['media']['name'][:50]}")

print()
print("=" * 78)
print("F. BRAND TOKENS / UNDERSCORES / AMPERSANDS - all three kinds")
print("=" * 78)
for label, rows, key in [("call", calls, "path"), ("lesson", lessons, "path"),
                         ("doc", docs, "clean")]:
    fn = [r[key].rsplit("/", 1)[-1] for r in rows]
    print(f"  {label}:")
    print(f"     carrying NHB/NHB+/FF/FF. : "
          f"{sum(1 for f in fn if re.search(r'(NHB|FF)', f))}")
    print(f"     carrying '_'             : {sum(1 for f in fn if '_' in f)}")
    for f in [f for f in fn if "_" in f][:6]:
        print(f"        {f}")
    print(f"     carrying '&'             : {sum(1 for f in fn if '&' in f)}")
    for f in [f for f in fn if "&" in f][:8]:
        print(f"        {f}")

print()
print("=" * 78)
print("G. 'Call' STRIPPED MID-PHRASE (spec: Call of Duty -> of Duty Biz - Ops)")
print("=" * 78)
mid = [c for c in calls if re.match(r"^(of|Booking|Booking Page)\b",
                                    c["path"].rsplit("/", 1)[-1][11:])]
print(f"  emitted names starting with a lowercase 'of'/'Booking': {len(mid)}")
for c in mid:
    print(f"     {c['verbatim'][:62]!r}")
    print(f"        -> {c['path'].rsplit('/',1)[-1][:62]!r}")

print()
print("=" * 78)
print("H. NAME POPULATION DENOMINATOR (spec says 296)")
print("=" * 78)
print(f"  calls {len(calls)} + lessons {len(lessons)} + documents {len(docs)} = "
      f"{len(calls)+len(lessons)+len(docs)}")
print(f"  calls {len(calls)} + documents {len(docs)} = {len(calls)+len(docs)}  <- the 296")
print(f"  all 230 audio + 109 docs = {230+109}")
