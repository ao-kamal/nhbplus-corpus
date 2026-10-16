#!/usr/bin/env python3
"""Acceptance tests for the 8 misc documents (bead nhbplus-corpus-8pt).

- png through the exporter produces a NOTE, never a file.
- png omitted from _meta-style entries -> reject (entry carries hash+dims).
- ZIP parsed before enumeration -> reject (enumerate-first asserted).
- Two Resources Links in the same path -> reject (distinctness asserted).
- No-text doc -> empty_extraction, never fabrication, never OCR.
- attachments/ present-or-created -> reject.
- 8 identified by class from scope-final, never by filename.
One JSONL line per test. Exit non-zero on failure.
"""
import hashlib
import importlib.util
import json
import os
import struct
import sys
import traceback
import zipfile
import io

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location(
    "extract_misc", os.path.join(HERE, "extract-misc.py"))
xm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(xm)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "extract-misc-tests.jsonl")
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
            log(name, "extract-misc.py", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "extract-misc.py", {"case": name}, "FAIL",
                traceback.format_exc(limit=5).replace("\n", " | "))
            return False
    return deco


def craft_png(w=3, h=2):
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    def chunk(kind, payload):
        import zlib
        c = struct.pack(">I", len(payload)) + kind + payload
        return c + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IEND", b""))


@T("population-8-by-class-never-by-name")
def _():
    handles = xm.misc_handles()
    assert len(handles) == 8, handles
    assert set(handles) == {"YvNyGbqS", "VvVSGbhJ", "knMmWRSD", "ErdCVRgJ",
                            "FzdgmLQD", "c7Ew1TaQ", "guNkBLaZ", "xyUQhDAa"}, handles
    # Derivation, not a list: an added txt row is picked up automatically.
    sf = json.load(open(os.path.join(ROOT, "pipeline", "out", "scope-final.json"), encoding="utf-8"))
    grown = sf["targets"] + [{"handle": "ZZZZZZZZ", "ext": "txt", "kind": "course_doc"}]
    assert "ZZZZZZZZ" in xm.misc_handles(grown)
    # Background prose may name the files; CODE must derive by class.
    import re
    src = open(os.path.join(HERE, "extract-misc.py"), encoding="utf-8").read()
    code = re.sub(r'"""[\s\S]*?"""', "", src)
    code = "\n".join(l.split("#")[0] for l in code.splitlines())
    assert "guNkBLaZ" not in code and "xyUQhDAa" not in code, "filename hardcoded"


@T("txt-reads-and-empty-is-empty-extraction")
def _():
    lines = xm.read_txt("a\n\nb\n".encode("utf-8-sig"))
    assert lines == ["a", "b"], lines
    assert xm.read_txt(b"   \n  ") == [{"empty_extraction": True, "bytes": 6}]
    src = open(os.path.join(HERE, "extract-misc.py"), encoding="utf-8").read().lower()
    assert "tesseract" not in src and "ocrmypdf" not in src


@T("resources-links-paths-distinct")
def _():
    import csv
    rows = list(csv.DictReader(open(os.path.join(ROOT, "worklist", "targets.csv"), encoding="utf-8")))
    txts = [r["path"] for r in rows if r["handle"] in
            ("YvNyGbqS", "VvVSGbhJ", "knMmWRSD", "ErdCVRgJ", "FzdgmLQD", "c7Ew1TaQ")]
    assert len(txts) == 6 and xm.txt_paths_distinct(txts), txts
    assert not xm.txt_paths_distinct(txts[:2] + [txts[0]]), "collision not caught"


@T("png-note-never-file-hash-and-dims-recorded")
def _():
    data = craft_png(3, 2)
    entry = xm.png_entry("Pick Primary Color", data)
    assert entry["dimensions"] == "3x2", entry
    assert entry["bytes"] == len(data) and len(entry["sha256"]) == 64, entry
    note = xm.png_note(entry)
    assert isinstance(note, list) and all(isinstance(l, str) for l in note)
    assert any("3x2" in l for l in note) and any(entry["sha256"] in l for l in note)
    joined = "\n".join(note).encode()
    # No image bytes in the note: the raw file must not appear as a run.
    # (Length comparison is meaningless on tiny test files; the invariant
    # is absence of the bytes, which holds at any scale.)
    assert data not in joined, "image bytes leaked into note"


@T("zip-enumerate-before-parse-guard-live")
def _():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as z:
        z.writestr("code/intro.txt", b"hello lazy")
        z.writestr("code/big.bin", b"\x00" * (2 * 1024 * 1024))
    data = buf.getvalue()
    members = xm.xo.enumerate_zip(data)  # central directory first
    assert [m["name"] for m in members] == ["code/intro.txt", "code/big.bin"]
    old = xm.xo.GUARD_BYTES
    xm.xo.GUARD_BYTES = 1 * 1024 * 1024
    try:
        seen_stream = False
        for chunk, was_stream in xm.xo.read_member(data, "code/big.bin"):
            seen_stream = seen_stream or was_stream
        assert seen_stream, "oversized member parsed without streaming"
    finally:
        xm.xo.GUARD_BYTES = old


@T("no-attachments-anywhere")
def _():
    import re
    for f in ("extract-misc.py", "extract-ooxml.py", "extract-pdf.py"):
        src = open(os.path.join(HERE, f), encoding="utf-8").read()
        code = re.sub(r'"""[\s\S]*?"""', "", src)
        assert "attachments" not in code, f"{f} references attachments/"


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} extract-misc tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:300]}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
