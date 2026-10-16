#!/usr/bin/env python3
"""Channel topology classifier - five branches, never corpus-wide (geo).

Measurement (90 s window, never full decode; NO -v error around astats):
  rms_L = astats RMS level dB on the stereo stream
  rms_R = astats RMS level dB on pan=mono|c0=c1
  rms_D = astats RMS level dB on pan=mono|c0=c0-c1   (the L-R signal)
  delta = rms_D - rms_L  (dB; -inf when L-R is digital silence)

Branches:
  MONO                  channels == 1: zero astats, one commit. Guard BEFORE
                        measuring: c1 does not exist on mono input.
  BIT_IDENTICAL         delta <= -60: -map_channel 0.0 -c:a copy (lossless).
  EFFECTIVELY_DUAL_MONO -60 < delta <= -40: -c:a libopus -b:a 32k, mono 16k
                        (re-encode; bit-exactness WITHDRAWN for these parts).
  INDEPENDENT           delta >= -20: keep stereo, pay 2x. -ac 1 would be a
                        REAL DOWNMIX here (proven on ljF0mZ4Y, IqVSkD5Z).
  AMBIGUOUS             otherwise: keep stereo, flag AMBIGUOUS_CHANNELS.
                        Never silently decided; never fired on a measured
                        input, kept anyway.

INPUT_CHANNEL_COUNT goes in the receipt: SETTLE_FROM bills on the AS
SUBMITTED count, never the response's channels array (Deepgram returns
channels=1 while billing 2x). Any channel count outside {1, 2} is a HARD
STOP, not a default.
"""
import json
import math
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

MONO, BIT_IDENTICAL, DUAL_MONO, INDEPENDENT, AMBIGUOUS = (
    "MONO", "BIT_IDENTICAL", "EFFECTIVELY_DUAL_MONO", "INDEPENDENT", "AMBIGUOUS")

DB_INF = float("-inf")


def parse_rms_level_db(astats_text):
    """First 'RMS level dB:' value; '-inf' -> float -inf. No reading -> error."""
    m = re.search(r"RMS level dB:\s*(\S+)", astats_text)
    if not m:
        raise ValueError("no RMS level dB in astats output (was -v error used?)")
    return float(m.group(1))


def classify(nchannels, rms_l=None, rms_r=None, rms_d=None):
    """Returns (branch, input_channel_count, note)."""
    if nchannels == 1:
        if any(v is not None for v in (rms_l, rms_r, rms_d)):
            raise ValueError("mono input measured: guard before measuring")
        return (MONO, 1, "zero-astats one-commit")
    if nchannels != 2:
        raise ValueError(f"HARD STOP: channels={nchannels}")
    if rms_l is None or rms_d is None:
        raise ValueError("stereo input without L and L-R measurements")
    delta = rms_d - rms_l
    if delta <= -60:
        return (BIT_IDENTICAL, 1, f"delta={delta:.1f}dB map_channel-lossless")
    if delta <= -40:
        return (DUAL_MONO, 1, f"delta={delta:.1f}dB opus-re-encode")
    if delta >= -20:
        return (INDEPENDENT, 2, f"delta={delta:.1f}dB keep-stereo-pay-2x")
    return (AMBIGUOUS, 2, f"delta={delta:.1f}dB AMBIGUOUS_CHANNELS")


WINDOW_SEC = 90  # measurement window, NEVER a full decode


def measure_argv(part, filt, window=WINDOW_SEC):
    """Exact astats passes. No -v error: astats writes at info level, and
    -v error turns every reading into -inf, indistinguishable from silence."""
    return ["ffmpeg", "-nostdin", "-t", str(window), "-i", part,
            "-af", filt, "-f", "null", "-"]


FILTER_L = "astats"
FILTER_R = "pan=mono|c0=c1,astats"
FILTER_D = "pan=mono|c0=c0-c1,astats"
FILTER_BUG = "pan=mono|c0=c0,astats"  # the collapsed form, for reproduction only


def downmix_argv(branch, src, dst):
    # CORRECTED 2026-10-16 (live defect): the bead's `-map_channel 0.0 -c:a
    # copy` is a silent no-op on ffmpeg 6.1.1 (`-map_channel` deprecated,
    # stream mapping shows full stereo copy, same byte size). It would have
    # submitted stereo while the receipt claimed a mono collapse: billed 2x
    # with a 1x receipt. BIT_IDENTICAL now re-encodes LOSSLESSLY:
    # `-ac 1 -c:a flac`, proven bit-exact on the smoke unit (L-minus-FLAC =
    # digital silence, -inf RMS/peak, full 23:56 file). Upload is bigger
    # (126 vs 46 MB); billing is by duration, so the money claim holds.
    if branch == BIT_IDENTICAL:
        return ["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src,
                "-ac", "1", "-c:a", "flac", dst]
    if branch == DUAL_MONO:
        return ["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src,
                "-ac", "1", "-c:a", "libopus", "-b:a", "32k", "-ar", "16000", dst]
    if branch in (INDEPENDENT, AMBIGUOUS, MONO):
        return None
    raise ValueError(f"unknown branch {branch}")


def run(cmd, stdin_closed=True):
    kw = {"capture_output": True, "text": True}
    if stdin_closed:
        import subprocess as sp
        kw["stdin"] = sp.DEVNULL
    return subprocess.run(cmd, **kw)


if __name__ == "__main__":
    print(json.dumps({"branches": [MONO, BIT_IDENTICAL, DUAL_MONO, INDEPENDENT, AMBIGUOUS]}))
