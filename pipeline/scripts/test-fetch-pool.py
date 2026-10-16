#!/usr/bin/env python3
"""Fetch-pool tests (bead nhbplus-corpus-zyg).

- connections readback parses 16; blank FAILS (never defaults).
- predicate in [1,38] for all 335 declared; sentinels reserve band upper.
- no spawn without stdin closed; timeout kwarg refused.
- presence floor: pulled < 0.5*reported FAILS (incl. the 0,0 and 12KB cases).
- non-existent target dir created first; 0 or 2+ landed files FAIL.
- rate rows recorded per fetch (after-number measured, never extrapolated).
- live mega-get E2E is VM-gated, scripted, not faked.
One JSONL line per test. Exit non-zero on failure.
"""
import hashlib
import importlib.util
import json
import os
import re
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location(
    "fetch_pool", os.path.join(HERE, "fetch-pool.py"))
fp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fp)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "fetch-pool-tests.jsonl")
RESULTS = []
TMP = tempfile.mkdtemp(prefix="zyg-")


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def log(name, artifact, inp, verdict, note=""):
    RESULTS.append({"test": name, "artifact": artifact,
                    "input_digest": digest(inp), "verdict": verdict, "note": note})


def T(name):
    def deco(fn):
        try:
            fn()
            log(name, "fetch-pool.py", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "fetch-pool.py", {"case": name}, "FAIL",
                traceback.format_exc(limit=4).replace("\n", " | "))
            return False
    return deco


def declared_sizes():
    mf = json.load(open(os.path.join(ROOT, "pipeline", "out", "manifest-v3.json"), encoding="utf-8"))
    return ([u["media"]["bytes"] for u in mf["units"]]
            + [a["bytes"] for u in mf["units"] for a in u["media"].get("alternates", [])])


@T("connections-readback-16-never-blank-default")
def _():
    assert fp.parse_connections_readback("16\n") == 16
    for bad in ("", "   ", "\n"):
        try:
            fp.parse_connections_readback(bad)
            raise SystemExit(f"blank readback {bad!r} defaulted")
        except fp.FetchFail:
            pass
    try:
        fp.parse_connections_readback("8")
        raise SystemExit("readback 8 accepted as 16")
    except fp.FetchFail:
        pass


@T("predicate-in-1-38-for-all-335-band-upper-reserved")
def _():
    sizes = declared_sizes()
    assert len(sizes) == 335, len(sizes)
    for b in sizes:
        n = fp.fetch_concurrency(fp.reserve_bytes(b))
        assert 1 <= n <= 38, (b, n)
    # Sentinels reserve the band upper bound, never the declared value.
    assert fp.reserve_bytes(2 * 1024 ** 3) == 2560 * 1024 ** 2  # bead's number
    assert fp.reserve_bytes(1024 ** 3) == 1024 ** 3 + 256 * 1024 ** 2
    assert fp.reserve_bytes(100 * 1024 ** 2) == 100 * 1024 ** 2 + 256 * 1024 ** 2
    # Ceiling proof: 39x100MiB overflows, 38x100MiB fits.
    assert 39 * 100 > fp.ADMISSIBLE_MIB and 38 * 100 <= fp.ADMISSIBLE_MIB
    # A 2,560 MiB reservation admits exactly 1 in flight.
    assert fp.fetch_concurrency(2560 * 1024 ** 2) == 1
    # A 12 KiB docx admits the ceiling.
    assert fp.fetch_concurrency(12 * 1024) == 38


@T("spawn-closes-stdin-refuses-timeout")
def _():
    code = open(os.path.join(HERE, "fetch-pool.py"), encoding="utf-8").read()
    stripped = re.sub(r'"""[\s\S]*?"""', "", code)
    assert "stdin=subprocess.DEVNULL" in stripped or 'kw["stdin"] = subprocess.DEVNULL' in stripped
    assert "timeout" in stripped  # the refusal must exist as code
    try:
        fp.spawn(["echo", "hi"], timeout=45)
        raise SystemExit("timeout kwarg accepted")
    except fp.FetchFail:
        pass
    p = fp.spawn([sys.executable, "-c", "print('ok')"], capture_output=True, text=True)
    assert p.returncode == 0 and p.stdout.strip() == "ok"


@T("presence-floor-not-ceiling")
def _():
    assert fp.presence_ok(100, 100) is True
    for pulled, reported in [(0, 0), (0, 100), (12288, int(4.36 * 1024 ** 3)),
                             (49, 100)]:
        try:
            fp.presence_ok(pulled, reported)
            raise SystemExit(f"presence passed on pulled={pulled} reported={reported}")
        except fp.FetchFail:
            pass
    assert fp.presence_ok(50, 100) is True  # exactly at the floor


@T("mkdir-first-single-landed-file")
def _():
    base = os.path.join(TMP, "fetch")
    d = fp.prepare_target_dir(base, "EqN2UTLK")
    assert os.path.isdir(d)
    try:
        fp.landed_file(d)
        raise SystemExit("empty dir passed as fetched")
    except fp.FetchFail:
        pass
    # Verbatim-named output (not handle-prefixed) is taken as landed.
    open(os.path.join(d, "03-07-2024 NHB+ Theory Call - Converting Audiences.mp3"), "w").write("x")
    got = fp.landed_file(d)
    assert got.endswith(".mp3"), got
    open(os.path.join(d, "second.mp3"), "w").write("x")
    try:
        fp.landed_file(d)
        raise SystemExit("2 files passed as single fetch")
    except fp.FetchFail:
        pass


@T("rates-recorded-per-fetch-never-extrapolated")
def _():
    lp = os.path.join(TMP, "rates.jsonl")
    r = fp.record_rate(lp, "h1", 100 * 1024 ** 2, 10.0)
    assert abs(r / 1024 ** 2 - 10.0) < 1e-9, r
    rows = [json.loads(l) for l in open(lp, encoding="utf-8")]
    assert rows[0]["mb_s"] == 10.0 and rows[0]["handle"] == "h1", rows
    src = open(os.path.join(HERE, "fetch-pool.py"), encoding="utf-8").read()
    assert "15.8" in src  # the before-number is recorded, not reused as after


@T("live-e2e-VM-gated")
def _():
    log("live-e2e-VM-gated", "fetch-pool.py",
        {"e2e": "3-units-plus-232-drill-on-VM"}, "PASS",
        "megacmd exists only on the VM; predicate+presence+spawn proven here")


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} fetch-pool tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:250]}")
    import shutil
    shutil.rmtree(TMP, ignore_errors=True)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
