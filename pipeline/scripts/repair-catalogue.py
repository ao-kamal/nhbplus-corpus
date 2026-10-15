#!/usr/bin/env python3
"""
Repair selection-catalogue.py.

Two problems:
  1. A PowerShell `Set-Content -Encoding utf8` round-trip mangled the file's own
     em-dashes and middots - the identical encoding defect that corrupted the
     MEGA capture (cp850 in place of UTF-8). Repaired by transcoding explicitly.
  2. 'calls with neither companion' was computed as len(calls) - nw, which is not
     "neither". It needs its own count.
"""
import io, re, sys

P = "selection-catalogue.py"
s = io.open(P, encoding="utf-8", errors="replace").read()

# ---- 1. repair the mojibake that PowerShell introduced --------------------
MOJI = [("\u00e2\u20ac\u201c", "\u2014"),   # â€œ  -> em dash
        ("\u00c2\u00b7", "\u00b7"),          # Â·    -> middot
        ("\u00e2\u20ac\u201d", "\u2014"),
        ("\u00e2\u2013\u2013", "\u2014"),    # â€“ -> em dash
        ("\u00e2\u203a", ">"),
        ("\u00c2\u00a0", " ")]
for bad, good in MOJI:
    s = s.replace(bad, good)
# anything left in the C1/C2 range is mojibake; fall back to ASCII
s = "".join(c if (ord(c) < 128 or c in "\u2014\u2013\u00b7\u2026\u00e9\u2019")
            else "-" for c in s)

# ---- 2. the wrong 'neither' count -----------------------------------------
old = ('A(f"**{nw} calls carry a written hand \u00b7 {ns} carry an AI summary \u00b7 "\n'
       '  f"{len(calls)-nw} have neither.**")')
new = ('A(f"**{nw} calls carry a written hand - {ns} carry an AI summary - "\n'
       '  f"{NEITHER} of {len(calls)} calls carry neither.**")')
if old in s:
    s = s.replace(old, new)
else:
    # tolerate whatever dash survived
    s = re.sub(r'A\(f"\*\*\{nw\} calls carry a written hand.{0,4}\{ns\} carry an AI summary.{0,4}"\s*\n\s*f"\{len\(calls\)-nw\} have neither\.\*\*"\)',
               new, s)

# define NEITHER right after the guards
anchor = 'assert nw >= 0.75 * W_IN_CALLS, (\n    f"only {nw} of {W_IN_CALLS} written-hand documents paired - scoring is broken")'
if anchor in s and "NEITHER =" not in s:
    s = s.replace(anchor, anchor +
                  '\ncalls   = [u for u in units if u["kind"] == "calls"]\n'
                  'lessons = [u for u in units if u["kind"] == "lessons"]\n'
                  'NEITHER = sum(1 for u in calls if not companions(u)[0] and not companions(u)[1])')

# drop any now-duplicated later definitions of calls/lessons
s = re.sub(r'\n+calls   = \[u for u in units if u\["kind"\] == "calls"\]\n'
           r'lessons = \[u for u in units if u\["kind"\] == "lessons"\]\n', '\n', s, count=0)

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
bad = [c for c in s if ord(c) > 127]
print(f"repaired {P}")
print(f"  remaining non-ascii: {len(bad)} -> {sorted(set(bad))}")
print(f"  NEITHER defined: {'NEITHER =' in s}")
print(f"  stale len(calls)-nw: {'len(calls)-nw' in s}")