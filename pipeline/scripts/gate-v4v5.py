#!/usr/bin/env python3
"""V4 duration reconcile + V5 span coverage (beads pcp, 724).

V4(d_manifest, d_header, d_decoded): authoritative = decoded (the only
MEASUREMENT). spread = max-min over NON-SENTINEL values; sentinel/zero
d_manifest EXCLUDED (including it manufactures disagreement).
ratio = spread / d_authoritative. FAIL if decoded missing or ratio > 0.10;
WARN if > 0.02. pjFQiLQQ: spread 473.1 / 5431.8 = 0.0871 WARN (NOT the
header-relative 0.0954: a test asserting the verdict instead of the number
passes the wrong formula).

V5(first_start, last_end, d_manifest, n_words): head = first.start,
tail = d_manifest - last.end. FAIL on empty (fetch/decode failure, named
EMPTY), edges > SPAN_EDGE_SEC=10 (assembly failure, named EDGE).
NEGATIVE gaps are NOT failures (10/47 units negative tail). span_ratio
clause: MIN_SPAN_RATIO is UNSET (no sourced value) -> recorded UNSET,
never defaulted to 0. NON_VACUOUS iff words > 0 and duration > 0.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

DURATION_TOLERANCE = 0.10
WARN_BAND = 0.02
SPAN_EDGE_SEC = 10
MIN_SPAN_RATIO = None  # UNSET: no sourced value. Recorded, never defaulted.


class V4Fail(Exception):
    pass


class V5Fail(Exception):
    pass


def is_sentinel_manifest(d):
    """A manifest duration that is a display value, not a measurement: zero,
    missing, or GiB-scale (a byte-count leaked into a seconds field, e.g. a
    2 GiB d_manifest = 68 years of audio). Small KiB-exact second counts are
    ordinary durations, not sentinels: the test is scale, not exactness."""
    return d is None or d == 0 or (isinstance(d, (int, float)) and d >= 2 ** 30)


def v4(d_manifest, d_header, d_decoded):
    """Sentinel/zero d_manifest EXCLUDED; spread from header+decoded only.

    BEAD-TEXT DEFECT RECORDED 2026-10-16: the acceptance bullet says a 2 GiB
    d_manifest '-> FAIL' and 'a V4 that returns PASS here has a broken
    exclusion'. That polarity contradicts the Technical Approach ('EXCLUDED
    from the spread entirely') AND the Success Criteria ('spread computed
    from header and decoded only'), two against one. A FAIL on a sentinel
    manifest PROVES the sentinel was included (it manufactures the
    disagreement); the correct verdict excludes and passes, with the
    exclusion recorded here. Spec/formula wins over the bullet.
    """
    if d_decoded is None:
        raise V4Fail("no decoded duration: no authority")
    excluded = is_sentinel_manifest(d_manifest)
    vals = [float(v) for v in (d_header, d_decoded) if v is not None]
    if not excluded:
        vals.append(float(d_manifest))
    spread = max(vals) - min(vals)
    ratio = spread / float(d_decoded)
    if ratio > DURATION_TOLERANCE:
        raise V4Fail(f"spread ratio {ratio:.4f} > 0.10")
    warn = ratio > WARN_BAND
    return {"ratio": round(ratio, 4), "warn": warn,
            "authoritative": float(d_decoded),
            "manifest_excluded": bool(excluded)}


def v5(first_start, last_end, d_manifest, n_words):
    if n_words == 0:
        raise V5Fail("EMPTY: no words (fetch/decode failure, retry costs money)")
    if d_manifest is None or d_manifest <= 0:
        raise V5Fail("EMPTY: no duration")
    head, tail = float(first_start), float(d_manifest) - float(last_end)
    if head > SPAN_EDGE_SEC:
        raise V5Fail(f"EDGE: head_gap {head:.2f} > {SPAN_EDGE_SEC}")
    if tail > SPAN_EDGE_SEC:
        raise V5Fail(f"EDGE: tail_gap {tail:.2f} > {SPAN_EDGE_SEC}")
    return {"head_gap": round(head, 2), "tail_gap": round(tail, 2),
            "span_ratio": "UNSET (MIN_SPAN_RATIO unsourced)"}


if __name__ == "__main__":
    print(json.dumps({"v4_tol": DURATION_TOLERANCE, "span_edge": SPAN_EDGE_SEC,
                      "min_span_ratio": MIN_SPAN_RATIO}))
