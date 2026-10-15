#!/usr/bin/env python3
"""R3 T5: re-derive every load-bearing number in the spec from the JSONs."""
import json, os, re, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def jload(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)

man = jload(os.path.join(OD, "manifest-v3.json"))
sc  = jload(os.path.join(OD, "scope-final.json"))
cn  = jload(os.path.join(OD, "clean-names.json"))
units = man["units"]
targets = sc["targets"]

GiB = 1 << 30
MiB = 1 << 20

print("=" * 78)
print("A. UNIT COUNTS BY EXTENSION")
print("=" * 78)
c = Counter(u["media"]["ext"] for u in units)
print("  media.ext :", dict(c), " total", sum(c.values()))
kind = Counter((u["kind"], u["media"]["ext"]) for u in units)
print("  kind x ext:", dict(kind))
print("  has_mp3:", sum(1 for u in units if u["has_mp3"]),
      " has_mp4:", sum(1 for u in units if u["has_mp4"]),
      " both:", sum(1 for u in units if u["has_mp3"] and u["has_mp4"]))
alts = Counter(a["ext"] for u in units for a in u["media"]["alternates"])
print("  alternates by ext:", dict(alts),
      " total", sum(alts.values()))
print("  scope-final mp4_alternates_never_fetched:",
      sc["mp4_alternates_never_fetched"])

print()
print("=" * 78)
print("B. AUDIO MINUTES / HOURS")
print("=" * 78)
tot_s = sum(u["media"]["dur_s"] or 0 for u in units)
calls = [u for u in units if u["kind"] == "calls"]
less  = [u for u in units if u["kind"] == "lessons"]
cs = sum(u["media"]["dur_s"] or 0 for u in calls)
ls = sum(u["media"]["dur_s"] or 0 for u in less)
print(f"  calls   {len(calls):>4}  {cs/3600:9.4f} h  {cs/60:11.2f} min")
print(f"  lessons {len(less):>4}  {ls/3600:9.4f} h  {ls/60:11.2f} min")
print(f"  TOTAL   {len(units):>4}  {tot_s/3600:9.4f} h  {tot_s/60:11.2f} min")
print(f"  spec claims: 188 calls / 557.39 h ; 42 lessons / 26.16 h ; total 583.55 h")
print(f"  DELTA calls hours  {cs/3600 - 557.39:+.4f}")
print(f"  DELTA lesson hours {ls/3600 - 26.16:+.4f}")
print(f"  DELTA total hours  {tot_s/3600 - 583.55:+.4f}")
nodur = [u for u in units if not u["media"]["dur_s"]]
print(f"  units with dur_s None/0: {len(nodur)}")
for u in nodur:
    print(f"     {u['media']['handle']} {u['media']['name'][:60]!r} bytes={u['media']['bytes']}")

# per-target (scope-final) durations, which is what the runner reads
asum = sum(t["dur_s"] or 0 for t in targets if t["kind"] == "audio")
print(f"  scope-final audio dur sum: {asum/3600:.4f} h  ({asum/60:.2f} min)")
print(f"  scope-final audio units  : {sum(1 for t in targets if t['kind']=='audio')}")

print()
print("=" * 78)
print("C. THE $150.56 FORECAST")
print("=" * 78)
RATE, KR = 0.0043, 0.0013
for label, minutes in [("manifest-v3 total", tot_s/60),
                       ("scope-final total", asum/60),
                       ("spec 35,013.1", 35013.1)]:
    print(f"  {label:<22} {minutes:12.2f} min  x0.0043 = ${minutes*RATE:9.4f}"
          f"   +keyterm = ${minutes*(RATE+KR):9.4f}")
print(f"  spec forecast 150.56 -> implied minutes = {150.56/0.0043:.2f}")
print(f"  spec keyterm  45.52  -> implied minutes = {45.52/0.0013:.2f}")

print()
print("=" * 78)
print("D. THE $207.35 HARD STOP")
print("=" * 78)
base = 35013.1 * 0.0043
kt   = 35013.1 * 0.0013
print(f"  150.56 + 1.27 + 10.00 + 45.52 = {150.56+1.27+10.00+45.52:.2f}")
print(f"  0.1.23 variant               = {150.56+1.23+10.00+45.52:.2f}")
# what do the 2 undated units actually cost?
und = [u for u in units if not u["media"]["dur_s"]]
print(f"  undated units ({len(und)}): cannot be priced - no duration. spec says $1.23 / $1.27")
print(f"  $1.27 implies {1.27/0.0043/60:.2f} min ; $1.23 implies {1.23/0.0043/60:.2f} min")

print()
print("=" * 78)
print("E. SENTINELS AND BYTE SHARE")
print("=" * 78)
sent = [u for u in units if (u["media"]["bytes"] or 0) % GiB == 0 and u["media"]["bytes"]]
by_sz = Counter(u["media"]["bytes"] // GiB for u in sent)
print(f"  sentinel units (media.bytes %% 1<<30 == 0): {len(sent)} of {len(units)}")
print(f"  by GiB value: {dict(sorted(by_sz.items()))}")
sent_b = sum(u["media"]["bytes"] for u in sent)
all_b  = sum(u["media"]["bytes"] or 0 for u in units)
print(f"  sentinel bytes {sent_b/GiB:.4f} GiB ; all bytes {all_b/GiB:.5f} GiB")
print(f"  sentinel share of bytes: {100*sent_b/all_b:.2f}%")
# spec: 37 at exactly 1 GiB, 36 at exactly 2 GiB = 109.00 GiB of 146.39 GiB = 74.5%
print(f"  spec: 37 @1GiB + 36 @2GiB = 109.00 GiB of 146.39 GiB = 74.5%")
print(f"  computed: {dict(sorted(by_sz.items()))} -> "
      f"{sum(k*v for k,v in by_sz.items())/GiB:.2f} GiB")
print(f"  is any alternate also a sentinel? ",
      sum(1 for u in units for a in u['media']['alternates']
          if (a['bytes'] or 0) % GiB == 0 and a['bytes']))
# the 3 GiB claim in round 2 review / eu-limits artifact
big = sorted(units, key=lambda u: -(u["media"]["bytes"] or 0))[:6]
for u in big:
    b = u["media"]["bytes"]
    print(f"    largest: {b/GiB:7.3f} GiB  {u['media']['ext']}  sentinel={b%GiB==0}"
          f"  {u['media']['name'][:58]}")

print()
print("=" * 78)
print("F. PER-UNIT OVERSUM (sentinel display-value inflation)")
print("=" * 78)
# normalize.size_of parses "N GB" from the MEGA title -> these ARE the display values
infl = 0.0
n_gt = 0
for u in units:
    m = u["media"]
    if m["bytes"] and m["dur_s"]:
        pass
# compare against manifest implied: use alternates to see if a sibling differs
pairs = 0
for u in units:
    for a in u["media"]["alternates"]:
        if a["bytes"] and u["media"]["bytes"]:
            pairs += 1
print(f"  (informational) unit/alternate byte pairs available: {pairs}")

print()
print("=" * 78)
print("G. TARGETS AND THE 339")
print("=" * 78)
bk = Counter(t["kind"] for t in targets)
print("  scope-final by kind:", dict(bk))
print("  sum:", sum(bk.values()))
print("  scope-final totals:", json.dumps(sc["totals"], indent=2))
print("  by_kind:", json.dumps(sc["by_kind"], indent=2))
print("  spec table: 188 calls + 42 videos + 109 docs = 339 ; 105 MP4 alternates")
print(f"  computed calls={bk.get('audio',0) and Counter(u['kind'] for u in units)['calls']}"
      f" lessons={Counter(u['kind'] for u in units)['lessons']}")
print(f"  alternates computed = {sum(len(u['media']['alternates']) for u in units)}"
      f"  (spec says 105)")
