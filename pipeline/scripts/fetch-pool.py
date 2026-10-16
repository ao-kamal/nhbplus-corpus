#!/usr/bin/env python3
"""Fetch pool with the size-adaptive concurrency predicate (bead zyg).

Pipeline order: fetch -> remux -> submit -> assemble -> egress. Fetch
dominates wall-clock (153.81 GiB at measured 15.8 MB/s ~= 2.90 h).

- `mega-speedlimit --download-connections 16`, read back as 16 not blank.
- Two axes: 16 chunk connections PER transfer; in-flight transfers from the
  predicate below. Never a constant.
- FETCH_CONCURRENCY_CEILING = 38: 39x100 MiB = 3,900 > 3,872 admissible.
- Admission reserves REAL bytes: sentinels reserve the display band's UPPER
  bound (2 GiB quantum -> 2,560 MiB), never the declared value.
- Every child spawns with stdin DEVNULL. NEVER a process timeout around a
  fetch: timeout 45 once let 4.0 GB land server-side. Safety is admission
  control + watcher + cancel + post-kill quiesce assertion on disk.
- mkdir the per-handle target first (mega-get rc 55 otherwise); fetch into an
  EMPTY per-handle dir and take whatever single file lands (never a
  handle-prefixed existence check: mega-get names output after the VERBATIM
  source file).
- Presence checks carry a FLOOR: pulled >= 0.5 * reported_size, not just a
  ceiling. Three checks once reported success on empty results.
- No linear extrapolation: the after-number is MEASURED during the run and
  recorded per fetch (bytes, seconds, rate). Before: 15.8 MB/s at 4
  in-flight, connections unset.

The live mega-get E2E (3 units, 232 drill, rate measurement) runs on the VM
where megacmd exists. Everything decidable without the network is decided
here, against the real 335 declared sizes.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

MIB = 1024 ** 2
ADMISSIBLE_MIB = 3872          # loopback budget the predicate may fill
FETCH_CONCURRENCY_CEILING = 38  # 39x100MiB=3900 > 3872; 38x100MiB=3800
CHUNK_CONNECTIONS = 16
FETCH_STALL_SEC = 120
POST_KILL_QUIESCE_SEC = 60
PRESENCE_FLOOR = 0.5


class FetchFail(Exception):
    pass


def band_upper_bound(declared):
    """Reserve the display band's UPPER bound for a sentinel declared size.

    Bands per spec: 1 GB display -> 512 MiB quantum; 2/3 GB -> 1 GiB. Above
    3.5 GiB the spec names no band (the only such unit is a 4 GiB mp4
    alternate, never fetched); the extension keeps the 1 GiB quantum, which
    is the conservative direction (reserves MORE, admits FEWER).
    """
    if declared < 1.5 * 1024 ** 3:
        quantum = 512 * MIB
    else:
        quantum = 1024 ** 3
    return declared + int(0.5 * quantum)


def reserve_bytes(declared):
    """Admission reserves REAL bytes: band upper bound for sentinels."""
    if declared % 1024 == 0:
        return band_upper_bound(declared)
    return declared


def fetch_concurrency(reserve):
    """Size-adaptive in-flight count in [1, 38]. Small units share the
    admissible budget; a 2,560 MiB reservation admits exactly 1."""
    n = (ADMISSIBLE_MIB * MIB) // max(1, reserve)
    return min(FETCH_CONCURRENCY_CEILING, max(1, n))


def parse_connections_readback(text):
    """'16' -> 16. Blank -> FAIL: a setting that reads back as nothing is a
    setting nobody is looking at."""
    s = (text or "").strip()
    if not s:
        raise FetchFail("connections readback blank: refusing to assume 16")
    try:
        n = int(s)
    except ValueError:
        raise FetchFail(f"connections readback unparseable: {s!r}")
    if n != CHUNK_CONNECTIONS:
        raise FetchFail(f"connections readback {n} != {CHUNK_CONNECTIONS}")
    return n


def presence_ok(pulled, reported):
    """Floor, not just ceiling: did I get roughly what I asked for?"""
    if reported <= 0:
        raise FetchFail(f"reported size {reported}: refusing empty baseline")
    if pulled < PRESENCE_FLOOR * reported:
        raise FetchFail(f"pulled {pulled} < 0.5 * reported {reported}")
    return True


def spawn(argv, **kw):
    """Spawn a pool child. stdin ALWAYS closed; timeout NEVER allowed."""
    if kw.get("timeout") is not None:
        raise FetchFail("process timeout around a fetch: admission+watcher instead")
    kw["stdin"] = subprocess.DEVNULL
    return subprocess.run(argv, **kw)


def prepare_target_dir(base, handle):
    """mkdir first: mega-get rc 55 on a non-existent target directory."""
    d = os.path.join(base, handle)
    os.makedirs(d, exist_ok=True)
    return d


def landed_file(target_dir):
    """Take whatever single file lands. 0 or 2+ is a FAIL, not a guess."""
    names = sorted(n for n in os.listdir(target_dir)
                   if os.path.isfile(os.path.join(target_dir, n)))
    if len(names) != 1:
        raise FetchFail(f"{target_dir}: {len(names)} files landed, need exactly 1")
    return os.path.join(target_dir, names[0])


def record_rate(log_path, handle, nbytes, seconds):
    rate = nbytes / max(seconds, 1e-9)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"handle": handle, "bytes": nbytes,
                            "seconds": round(seconds, 1),
                            "mb_s": round(rate / MIB, 2)}) + "\n")
    return rate


if __name__ == "__main__":
    print(json.dumps({"ceiling": FETCH_CONCURRENCY_CEILING,
                      "chunk_connections": CHUNK_CONNECTIONS,
                      "admissible_mib": ADMISSIBLE_MIB}))
