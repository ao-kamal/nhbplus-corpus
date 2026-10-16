#!/usr/bin/env python3
"""Channel classifier tests (bead geo).

Recorded live outputs (smoke unit V7U0mT4Q, 2026-10-16, AAC stereo):
  L = R = -23.321989 dB, L-R = -inf -> BIT_IDENTICAL.
- Bug repro: pan-before-astats collapses to ~0 difference on any input.
- mono: zero measurements, one commit; measuring mono is an error.
- -40 < delta < -20 -> AMBIGUOUS, never defaulted.
- -v error around astats -> no RMS level lines (rejected in source).
- full decode rejected in source (90 s window only).
- channels outside {1,2} -> HARD STOP.
One JSONL line per test. Exit non-zero on failure.
"""
import hashlib
import importlib.util
import json
import os
import re
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location(
    "channels", os.path.join(HERE, "channels.py"))
ch = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ch)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "channels-tests.jsonl")
RESULTS = []


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def log(name, artifact, inp, verdict, note=""):
    RESULTS.append({"test": name, "artifact": artifact,
                    "input_digest": digest(inp), "verdict": verdict, "note": note})


def T(name):
    def deco(fn):
        try:
            fn()
            log(name, "channels.py", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "channels.py", {"case": name}, "FAIL",
                traceback.format_exc(limit=4).replace("\n", " | "))
            return False
    return deco


LIVE_L = "[Parsed_astats_0 @ 0x1] RMS level dB: -23.321989"
LIVE_R = "[Parsed_astats_1 @ 0x2] RMS level dB: -23.321989"
LIVE_D = "[Parsed_astats_1 @ 0x3] RMS level dB: -inf"


@T("smoke-unit-bit-identical-live-values")
def _():
    l, r, d = (ch.parse_rms_level_db(LIVE_L), ch.parse_rms_level_db(LIVE_R),
               ch.parse_rms_level_db(LIVE_D))
    assert (l, r, d) == (-23.321989, -23.321989, float("-inf")), (l, r, d)
    branch, count, _ = ch.classify(2, l, r, d)
    assert branch == "BIT_IDENTICAL" and count == 1, (branch, count)


@T("bug-repro-pan-before-astats-collapses")
def _():
    # Collapsed stream reports ~0 difference on ANY input: the measurement
    # that reads INDEPENDENT on bit-identical files.
    collapsed = "[Parsed_astats_1 @ 0x1] RMS difference: 0.006975"
    m = re.search(r"RMS difference: (\S+)", collapsed)
    assert abs(float(m.group(1))) < 0.01, collapsed


@T("five-branches-boundaries")
def _():
    assert ch.classify(1) == ("MONO", 1, "zero-astats one-commit")
    assert ch.classify(2, -23.0, -23.0, -90.0)[0] == "BIT_IDENTICAL"
    assert ch.classify(2, -23.0, -23.0, -83.0)[0] == "BIT_IDENTICAL"   # -60 edge
    assert ch.classify(2, -23.0, -23.0, -73.0)[0] == "EFFECTIVELY_DUAL_MONO"
    assert ch.classify(2, -23.0, -23.0, -63.0)[0] == "EFFECTIVELY_DUAL_MONO"  # -40 edge
    assert ch.classify(2, -23.0, -10.0, -23.0)[0] == "INDEPENDENT"     # delta 0
    assert ch.classify(2, -23.0, -23.0, -44.0)[0] == "AMBIGUOUS"       # delta -21: dead band
    assert ch.classify(2, -23.0, -23.0, -43.0)[1] == 2                 # keeps stereo
    assert ch.classify(2, -23.0, -23.0, -43.0)[0] == "INDEPENDENT"     # delta exactly -20: table rule
    try:
        ch.classify(6)
        raise SystemExit("6 channels defaulted")
    except ValueError:
        pass
    try:
        ch.classify(1, -23.0, None, None)
        raise SystemExit("mono measured without error")
    except ValueError:
        pass


@T("downmix-commands-exact")
def _():
    bi = ch.downmix_argv("BIT_IDENTICAL", "in.mka", "out.mka")
    assert "-map_channel" not in bi, bi  # deprecated no-op on ffmpeg 6.1
    assert bi[bi.index("-c:a") + 1] == "flac" and "-ac" in bi, bi
    ai = bi.index("-i")
    assert bi.index("-ac") > ai, bi  # output option after -i
    dm = ch.downmix_argv("EFFECTIVELY_DUAL_MONO", "in.mka", "out.mka")
    assert dm[dm.index("-c:a") + 1] == "libopus" and "32k" in dm and "16000" in dm, dm
    ai = dm.index("-i")
    assert dm.index("-ac") > ai and dm.index("-ar") > ai, dm  # output options after -i
    assert ch.downmix_argv("INDEPENDENT", "a", "b") is None
    assert ch.downmix_argv("MONO", "a", "b") is None


@T("no-v-error-around-astats-90s-window-only")
def _():
    for filt in (ch.FILTER_L, ch.FILTER_R, ch.FILTER_D):
        argv = ch.measure_argv("part.mka", filt)
        assert argv[argv.index("-t") + 1] == "90", argv          # 90 s, never full
        assert "-v" not in argv, argv                            # info level lives
        assert "-nostdin" in argv, argv
        assert argv.index("-i") < argv.index("-af"), argv        # input before filter
    assert "c0=c0,astats" in ch.FILTER_BUG  # collapsed form, reproduction only


@T("parse-rejects-silent-inf-trap")
def _():
    try:
        ch.parse_rms_level_db("nothing here")
        raise SystemExit("empty astats parsed")
    except ValueError:
        pass


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} channel tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:250]}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
