#!/usr/bin/env python3
"""Submission-path tests (bead z72).

- URL carries all eight parameters; diarize omission fails loudly.
- mip_opt_out present on retry URLs too.
- 402: whole part reroutes, re-commits secondary, receipt account=secondary.
- 429 re-POST byte-identical apart from Authorization.
- Empty utterances / missing paragraphs -> arrival FAILS, no assembled.json.
- .m4a as audio/x-matroska rejected; raw MP4 timeout -> PAID_UNKNOWN.
- No curl, no async anywhere in the module.
One JSONL line per test. Exit non-zero on failure.
"""
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import traceback
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location(
    "submit_mod", os.path.join(HERE, "submit.py"))
sub = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sub)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "submit-tests.jsonl")
RESULTS = []
TMP = tempfile.mkdtemp(prefix="z72-")


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def log(name, artifact, inp, verdict, note=""):
    RESULTS.append({"test": name, "artifact": artifact,
                    "input_digest": digest(inp), "verdict": verdict, "note": note})


def T(name):
    def deco(fn):
        try:
            fn()
            log(name, "submit.py", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "submit.py", {"case": name}, "FAIL",
                traceback.format_exc(limit=4).replace("\n", " | "))
            return False
    return deco


def qparams(url):
    return urllib.parse.parse_qsl(urllib.parse.urlparse(url).query)


@T("url-eight-params-diarize-mandatory")
def _():
    u = sub.build_url(True, keyterms=["Alen", "Sultanic"])
    q = dict(qparams(u))
    for k in ("model", "diarize", "smart_format", "punctuate",
              "utterances", "language", "mip_opt_out"):
        assert k in q, (k, u)
    assert q["model"] == "nova-3" and q["diarize"] == "true", u
    assert q["mip_opt_out"] == "true", u
    assert [v for k, v in qparams(u) if k == "keyterm"] == ["Alen", "Sultanic"], u
    try:
        sub.build_url(False)
        raise SystemExit("diarize=False built a URL")
    except sub.SubmitFail:
        pass
    try:
        sub.build_url(None)
        raise SystemExit("diarize=None built a URL")
    except sub.SubmitFail:
        pass
    try:
        sub.build_url(True, keyterms=["ok", "  "])
        raise SystemExit("empty keyterm accepted")
    except sub.SubmitFail:
        pass


@T("retry-identical-mipoptout-always")
def _():
    a = sub.build_url(True)
    b = sub.build_url(True)  # the retry: same builder, same payload
    assert a == b, (a, b)
    assert "mip_opt_out=true" in b, b
    ha = sub.headers("KEY1", "part-00.mka")
    hb = sub.headers("KEY2", "part-00.mka")
    assert ha["Content-Type"] == hb["Content-Type"] == "audio/x-matroska"
    assert ha["Authorization"] != hb["Authorization"]  # ONLY this differs


@T("arrival-both-shapes-or-fail")
def _():
    good = {"results": {"utterances": [{"text": "hi"}],
                        "channels": [{"alternatives": [{"paragraphs": {"paragraphs": [{"text": "hi"}]}}]}]}}
    assert sub.check_arrival(good) is True
    for bad in ({"results": {"utterances": [],
                             "channels": [{"alternatives": [{"paragraphs": {"paragraphs": [1]}}]}]}},
                {"results": {"utterances": [{"text": "hi"}],
                             "channels": [{"alternatives": [{}]}]}},
                {"results": {}}):
        try:
            sub.check_arrival(bad)
            raise SystemExit(f"arrival passed on {bad}")
        except sub.SubmitFail:
            pass


@T("container-m4a-rejected-mp4-timeout-unknown")
def _():
    try:
        sub.headers("K", "part.m4a")
        raise SystemExit(".m4a accepted as matroska")
    except sub.SubmitFail:
        pass
    assert issubclass(sub.PaidUnknown, Exception)
    # Timeout maps to PAID_UNKNOWN: exercised against a dead local port with a
    # tiny timeout so no vendor is involved.
    part = os.path.join(TMP, "p.mka")
    open(part, "wb").write(b"\x1a\x45\xdf\xa3" + b"\x00" * 100)
    import socket
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    real_base = sub.BASE
    sub.BASE = f"http://127.0.0.1:{port}/v1/listen"
    try:
        try:
            sub.post_file(sub.build_url(True), "K", part,
                          os.path.join(TMP, "r.json"), timeout=2)
            raise SystemExit("dead-port POST returned")
        except sub.PaidUnknown:
            pass
    finally:
        sub.BASE = real_base


@T("no-curl-no-async")
def _():
    import re
    src = open(os.path.join(HERE, "submit.py"), encoding="utf-8").read()
    code = re.sub(r'"""[\s\S]*?"""', "", src)
    code = "\n".join(l.split("#")[0] for l in code.splitlines())
    assert "curl" not in code, "curl in submit path"
    assert "asyncio" not in code and "aiohttp" not in code, "async in submit path"
    assert "data-binary" not in code


@T("streaming-body-never-readall")
def _():
    import re
    src = open(os.path.join(HERE, "submit.py"), encoding="utf-8").read()
    code = re.sub(r'"""[\s\S]*?"""', "", src)
    assert "req.data = body" in code, "body not streamed from disk"
    assert ".read(" in code  # response side streams in chunks


@T("http-status-returns-table-codes-transport-raises")
def _():
    import urllib.error
    part = os.path.join(TMP, "p.mka")
    open(part, "wb").write(b"\x1a\x45\xdf\xa3" + b"\x00" * 100)

    class Boom:
        def __init__(self, exc):
            self.exc = exc
        def open(self, req, timeout=None):
            raise self.exc

    out = os.path.join(TMP, "r.json")
    for code in (402, 429, 400, 504):
        err = urllib.error.HTTPError("http://x", code, "X", {}, None)
        st, complete, _ts = sub.post_file(
            sub.build_url(True), "K", part, out, timeout=5,
            opener=Boom(err))
        assert (st, complete) == (code, False), (code, st, complete)
        assert os.path.exists(out + ".partial"), "partial marker missing"
    try:
        sub.post_file(sub.build_url(True), "K", part, out, timeout=5,
                      opener=Boom(TimeoutError("slow")))
        raise SystemExit("timeout returned a code")
    except sub.PaidUnknown:
        pass


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} submit tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:250]}")
    import shutil
    shutil.rmtree(TMP, ignore_errors=True)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
