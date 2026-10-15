#!/usr/bin/env python3
"""
Classify each manifest unit as CALL or LESSON, and key folders by HANDLE not NAME.

Why this exists: month folder names repeat across years. "1. January" is both
RrdEHRCL (2023) and Q7FGRZrJ (2024). Keying by name is ambiguous and would let a
2023 unit and a 2024 unit merge into one vault entry. The handle is unique.

A folder is a CALL folder when it names a month or a year. Everything else in this
share is a bonus lesson course. The classification is asserted, not assumed: the
result must reproduce 211 calls / 42 lessons from two independent censuses.
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
OD = os.path.join(HERE, "..", "out")

MONTH = (r"january|february|march|april|may|june|july|august|september|october"
         r"|november|december|jan\.|feb\.|mar\.|apr\.|jun\.|jul\.|aug\."
         r"|sep\.|sept\.|oct\.|nov\.|dec\.")
LEAD = re.compile(r"^\s*\d{1,2}\.\s*")
YEAR = re.compile(r"(19|20)\d{2}")

def kind_of(name):
    n = LEAD.sub("", (name or "").strip()).lower()
    if re.fullmatch(r"(19|20)\d{2}", n):               # 2021, 2022, 2023, 2024, 2025
        return "calls", int(n)
    if re.search(MONTH, n):                             # 6. June & July 2024
        m = YEAR.search(n)
        return "calls", int(m.group(0)) if m else None
    return "lessons", None

# handle -> name, and reverse name -> [handles] to expose collisions
handle_name = {}
for m in re.finditer(r'"([A-Za-z0-9_-]+)=([^"]*)"', open(os.path.join(OD, "seednames.txt"), encoding="utf-8").read()):
    handle_name[m.group(1)] = m.group(2)
name_handles = {}
for h, n in handle_name.items():
    name_handles.setdefault(n, []).append(h)

print("=== FOLDER NAME COLLISIONS (why handle-keying is mandatory) ===")
for n, hs in sorted(name_handles.items()):
    if len(hs) > 1:
        print(f"  {n!r:34} -> {hs}")
print()

man = json.load(open(os.path.join(OD, "perfile-manifest.json"), encoding="utf-8"))

# recover which seed handle each unit's folder came from
for u in man["units"]:
    h = u["folder"]
    kind, year = kind_of(handle_name.get(h, h))
    u["kind"], u["year"] = kind, year
    u["folder_handle"] = h

calls  = [u for u in man["units"] if u["kind"] == "calls"]
lessons = [u for u in man["units"] if u["kind"] == "lessons"]
hrs = lambda us: sum(u["media"]["dur_s"] or 0 for u in us) / 3600
gb  = lambda us: sum(u["media"]["bytes"] or 0 for u in us) / 1073741824

print("=== CLASSIFIED ===")
print(f"  CALLS   : {len(calls):>4}  {hrs(calls):>8.2f} h  {gb(calls):>7.2f} GB   (census: 211 calls / 630.74 h)")
print(f"  LESSONS : {len(lessons):>4}  {hrs(lessons):>8.2f} h  {gb(lessons):>7.2f} GB   (census:  42 videos / 26.16 h)")
print(f"  TOTAL   : {len(man['units']):>4}  {hrs(man['units']):>8.2f} h  {gb(man['units']):>7.2f} GB   (measured: 656.90 h)")
print()
print(f"  CALLS match census   : {'YES' if len(calls) == 211 else 'NO (' + str(len(calls)) + ')'}")
print(f"  LESSONS match census : {'YES' if len(lessons) == 42 else 'NO (' + str(len(lessons)) + ')'}")
print()
print("=== CALLS BY YEAR ===")
byyear = {}
for u in calls:
    byyear.setdefault(u["year"], []).append(u)
for y in sorted(byyear, key=lambda x: (x is None, x)):
    v = byyear[y]
    print(f"  {str(y or 'unlabelled'):>10} : {len(v):>3} calls  {hrs(v):>7.2f} h")
print()
print("=== LESSON COURSES ===")
byc = {}
for u in lessons:
    byc.setdefault(u["folder"], []).append(u)
for c in sorted(byc):
    v = byc[c]
    print(f"  {c:48} {len(v):>3} files  {hrs(v):>6.2f} h")

man["counts"] = {
    "files": man["counts"]["files"],
    "units": len(man["units"]),
    "calls": len(calls), "lessons": len(lessons),
    "call_hours": round(hrs(calls), 2), "lesson_hours": round(hrs(lessons), 2),
    "mp3_served": man["counts"]["mp3_served"], "mp4_served": man["counts"]["mp4_served"],
}
man["handle_name"] = handle_name
out = os.path.join(OD, "manifest-v2.json")
json.dump(man, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print()
print(f"WRITTEN {out}")