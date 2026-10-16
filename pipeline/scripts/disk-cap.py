#!/usr/bin/env python3
"""Sentinel-aware disk cap (bead nhbplus-corpus-06k).

Spec: stage-1/stage-1-spec.md. Every declared size in the corpus is an exact
multiple of 1 KiB (335 of 335). A GiB-granularity sentinel finds 77 and calls
the other 258 "real" - they are quantised 30 bits coarser than that test
assumed. Ground truth (wiUyTRZb): declared 397,410,304 B vs downloaded
397,487,264 B, a 76,960 B delta. No kill rule, threshold, or cost gate may
consume a declared size.

  sentinel(b) := (b % 1024) == 0      # NOT (b % 2**30) == 0

Census (recomputed here on every run, not asserted):
  declared sizes = 235 primary media bytes + 100 mp4-alternate bytes
                   (manifest-v3.json; cross-checked against scope-final.json)
  KIB-exact over all 335            -> 335
  GiB-exact over the 235 primaries  -> 77  (38 x 1 GiB, 39 x 2 GiB)
  sentinel bytes 38*1 + 39*2        -> 116.00 GiB of 153.81 = 75.4%

Kill predicate:
  sentinel -> NO kill, ever. Log DECLARED_UNKNOWN, rely on the 4 GiB
             kernel ENOSPC loopback. Zero kills across all 335.
  else     -> threshold = declared + 0.5 * quantum, ONE rule, no max().
             Quantum: 1 GB display -> 512 MiB; 2/3 GB display -> 1 GiB.
             REACHABLE FOR ZERO UNITS TODAY: every declared size is
             KiB-exact, so the else arm never fires. Recorded as never
             taken, never dressed as a live control. There is deliberately
             NO max(1.10*declared, ...) arm: it selects 1.10x only when
             declared >= 5*quantum, a regime that cannot occur here.

The cap itself is a 4 GiB loopback filesystem, kernel-enforced, mounted
before the first fetch and never unmounted mid-run. W0-Cap proved it at VM
scale; pipeline/scripts/provision-loopback.sh carries the exact VM recipe
and the scaled WSL proof log lives beside the test log.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

MIB = 1024 ** 2
GIB = 1024 ** 3

QUANTUM_1GB = 512 * MIB    # MEGA "1 GB" display band +/- 512 MiB
QUANTUM_23GB = 1 * GIB     # MEGA "2 GB"/"3 GB" display band +/- 1 GiB


def sentinel(nbytes):
    """KiB-exactness. The ONLY sentinel predicate."""
    return (nbytes % 1024) == 0


def quantum_for(declared):
    """Display quantum MEGA rounded to, per format. Unreachable on this corpus."""
    if declared < 1.5 * GIB:
        return QUANTUM_1GB
    if declared < 3.5 * GIB:
        return QUANTUM_23GB
    raise ValueError(f"no quantum defined for {declared}: outside 1/2/3 GB bands")


def kill_threshold(declared):
    """None for sentinels (no kill, ever). declared + 0.5*quantum otherwise."""
    if sentinel(declared):
        return None
    return declared + 0.5 * quantum_for(declared)


def load_manifest():
    with open(os.path.join(ROOT, "pipeline", "out", "manifest-v3.json"), encoding="utf-8") as f:
        return json.load(f)


def load_scope():
    with open(os.path.join(ROOT, "pipeline", "out", "scope-final.json"), encoding="utf-8") as f:
        return json.load(f)


def census():
    """Recompute the 335-size census. Returns dict; asserts nothing itself."""
    mf = load_manifest()
    primaries = [u["media"]["bytes"] for u in mf["units"]]
    alternates = [a["bytes"] for u in mf["units"] for a in u["media"].get("alternates", [])]
    sf = load_scope()
    scope_audio = {r["handle"]: r["bytes"] for r in sf["targets"] if r["kind"] == "audio"}
    # Cross-check: scope audio bytes agree with manifest primaries per handle.
    mismatched = [u["media"]["handle"] for u in mf["units"]
                  if scope_audio.get(u["media"]["handle"]) != u["media"]["bytes"]]
    gib1 = sum(1 for b in primaries if b == GIB)
    gib2 = sum(1 for b in primaries if b == 2 * GIB)
    gib_prim = sum(1 for b in primaries if b % GIB == 0)
    all_sizes = primaries + alternates
    # Byte totals cover the FETCHED population (primaries only): alternates
    # are never fetched, so they never touch the loopback. PLAN-TRUTH
    # TOT_BYTES 153.81 GiB is the primaries sum, and SENT_PCT 75.4% is
    # 116.00/153.81 on that same population.
    tot_gib = sum(primaries) / GIB
    sent_gib = (gib1 * 1.0 + gib2 * 2.0)
    return {
        "n_decl": len(all_sizes),
        "n_primaries": len(primaries),
        "n_alternates": len(alternates),
        "kib_exact": sum(1 for b in all_sizes if sentinel(b)),
        "gib_exact_primaries": gib_prim,
        "gib1": gib1,
        "gib2": gib2,
        "sent_gib": sent_gib,
        "tot_gib": round(tot_gib, 2),
        "sent_pct": round(100 * sent_gib / tot_gib, 1),
        "scope_mismatches": mismatched,
    }


if __name__ == "__main__":
    print(json.dumps(census(), indent=1))
