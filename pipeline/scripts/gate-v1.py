#!/usr/bin/env python3
"""V1 fetch caps and the sentinel exemption (bead nhbplus-corpus-0or).

V1(free_bytes, declared_bytes, actual_bytes):
  FAIL if free_bytes < FETCH_IMG_BYTES               # 4 GiB loopback present
  if sentinel(declared):                             # (b % 1024) == 0
      NO KILL. record sentinel_declared.             # display value, not measure
      FAIL if loopback free < FETCH_IMG_BYTES        # the binding cap exists
  else:
      FAIL if actual_bytes > declared + 0.5*quantum  # ONE rule, no max()

CORRECTIONS vs the bead text (spec wins, recorded in bead comments):
  C1. `sentinel(2**30 + 512)` -> False, not True: (2**30+512)%1024 == 512.
      Same defect as 06k; the True case needs a KiB-exact offset.
  C2. The bead's else arm reads `declared > declared + 0.5*quantum`, which is
      self-comparison and can never fire. Implemented as actual_bytes >
      declared + 0.5*quantum per spec section 6 (threshold consumed by a
      MEASUREMENT, never by the declared baseline).

Non-vacuity: sentinel_count == 335, not > 0. A run where the exemption never
applied must be distinguishable from one where it protected everything.
The else arm is unreachable for this corpus: every declared size including
wiUyTRZb's 397,410,304 is KiB-exact, so all 335 take the sentinel arm. The
wiUyTRZb download (397,487,264, NOT exact, +76,960 B) is the measured proof
that a declared baseline is a display value - it is why no kill may fire,
not an else-arm case. The else-arm LOGIC is unit-tested on synthetic
non-sentinel declared values for a future corpus.

The mega-get-232 loopback drill runs on the VM (provision-loopback.sh); the
live free-space probe here takes injected values so the predicate itself is
tested on this PC without a mount.
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location(
    "disk_cap", os.path.join(HERE, "disk-cap.py"))
dc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dc)

FETCH_IMG_BYTES = 4 * 1024 ** 3


class V1Fail(Exception):
    pass


def check_mount(free_bytes):
    """The binding cap exists with room. Pure predicate, values injected."""
    if free_bytes < FETCH_IMG_BYTES:
        raise V1Fail(f"loopback free {free_bytes} < {FETCH_IMG_BYTES}")
    return True


def check_unit(declared, actual_bytes=None, free_bytes=None):
    """One unit through V1. Returns (killed: bool, note)."""
    if free_bytes is not None:
        check_mount(free_bytes)
    if dc.sentinel(declared):
        return (False, "sentinel_declared")
    quantum = dc.quantum_for(declared)
    threshold = declared + 0.5 * quantum
    if actual_bytes is None:
        return (False, "else-arm-no-measurement-recorded-never-taken")
    if actual_bytes > threshold:
        raise V1Fail(f"actual {actual_bytes} > declared {declared} + band")
    return (False, "else-arm-measured-no-kill")


def check_corpus(free_bytes=None):
    """All 335 declared sizes: zero kills, sentinel_count == 335 exactly."""
    mf = dc.load_manifest()
    sizes = ([u["media"]["bytes"] for u in mf["units"]]
             + [a["bytes"] for u in mf["units"] for a in u["media"].get("alternates", [])])
    kills, sentinels, notes = [], 0, []
    for b in sizes:
        killed, note = check_unit(b, free_bytes=free_bytes)
        if killed:
            kills.append(b)
        if note == "sentinel_declared":
            sentinels += 1
        notes.append(note)
    if kills:
        raise V1Fail(f"kills fired on declared sizes: {kills[:5]}")
    if sentinels != 335:
        raise V1Fail(f"sentinel_count {sentinels} != 335: exemption coverage unproven")
    return {"kills": 0, "sentinel_count": sentinels}


if __name__ == "__main__":
    try:
        print(json.dumps(check_corpus()))
    except V1Fail as e:
        print(json.dumps({"verdict": "FAIL", "reason": str(e)}))
        raise SystemExit(1)
