#!/usr/bin/env python3
"""Acceptance tests for the OOXML extractor (bead nhbplus-corpus-5zb).

- Minimal docx built in-test round-trips to readable markdown.
- pptx slide order survives (numeric, never dict order).
- ZIP member above the guard streams with bounded peak (tracemalloc).
- Third-party import -> reject (stdlib-only gate over module source).
- No-text document -> empty_extraction, never fabrication, never OCR.
- 51 restated as 59 -> reject (live scope count).
- Central-directory enumeration before any member read.
One JSONL line per test. Exit non-zero on failure.
"""
import hashlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import tracemalloc
import traceback
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location(
    "extract_ooxml", os.path.join(HERE, "extract-ooxml.py"))
xo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(xo)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "extract-ooxml-tests.jsonl")
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
            log(name, "extract-ooxml.py", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "extract-ooxml.py", {"case": name}, "FAIL",
                traceback.format_exc(limit=5).replace("\n", " | "))
            return False
    return deco


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"


def build_docx(paras):
    buf = io.BytesIO()
    doc = ('<w:document xmlns:w="%s"><w:body>' % W_NS
           + "".join('<w:p><w:r><w:t>%s</w:t></w:r></w:p>' % p for p in paras)
           + "</w:body></w:document>")
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "<t/>")
        z.writestr("word/document.xml", doc)
    return buf.getvalue()


def build_pptx(slides):
    """slides: list of text lists. Written to the zip in REVERSE name order
    so any dict-order reader returns them backwards."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "<t/>")
        for i in range(len(slides), 0, -1):
            texts = "".join('<a:t>slide%d-%s</a:t>' % (i, t) for t in slides[i - 1])
            z.writestr("ppt/slides/slide%d.xml" % i,
                       '<p:sld xmlns:p="%s" xmlns:a="%s"><p:cSld><p:spTree>'
                       '<p:nvSp><p:cNvPr/></p:nvSp><p:sp><p:txBody>%s</p:txBody>'
                       "</p:sp></p:spTree></p:cSld></p:sld>" % (P_NS, A_NS, texts))
    return buf.getvalue()


def build_xlsx(rows):
    buf = io.BytesIO()
    shared = sorted({c for r in rows for c in r})
    sst = ('<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
           + "".join("<si><t>%s</t></si>" % s for s in shared) + "</sst>")
    body = ""
    for r in rows:
        body += "<row>" + "".join(
            '<c t="s"><v>%d</v></c>' % shared.index(c) for c in r) + "</row>"
    sheet = ('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
             "<sheetData>%s</sheetData></worksheet>" % body)
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "<t/>")
        z.writestr("xl/sharedStrings.xml", sst)
        z.writestr("xl/worksheets/sheet1.xml", sheet)
    return buf.getvalue()


@T("docx-round-trips-to-markdown")
def _():
    data = build_docx(["Converting Audiences", "Second paragraph here"])
    kind, lines = xo.extract_any("NHB+ Converting Audiences.docx", data)
    assert kind == "docx", kind
    assert lines == ["Converting Audiences", "Second paragraph here"], lines
    assert all(isinstance(x, str) for x in lines), "binary reached the output"


@T("pptx-slide-order-survives")
def _():
    data = build_pptx([["aa"], ["bb"], ["cc"]])
    kind, lines = xo.extract_any("deck.pptx", data)
    assert kind == "pptx", kind
    heads = [l for l in lines if l.startswith("## Slide")]
    assert heads == ["## Slide 1", "## Slide 2", "## Slide 3"], lines
    assert lines[1] == "slide1-aa" and lines[3] == "slide2-bb", lines


@T("xlsx-rows-in-order")
def _():
    data = build_xlsx([["a", "b"], ["c", "d"]])
    kind, lines = xo.extract_any("sheet.xlsx", data)
    assert lines == ["a | b", "c | d"], lines


@T("oversized-member-streams-peak-bounded")
def _():
    big = b"\x00" * (20 * 1024 * 1024)  # 20 MiB declared, guard lowered to 1 MiB
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as z:
        z.writestr("small.txt", b"tiny")
        z.writestr("big.bin", big)
    data = buf.getvalue()
    # enumerate first, from the central directory, before any member read
    info = xo.enumerate_zip(data)
    names = [m["name"] for m in info]
    assert names == ["small.txt", "big.bin"], names
    old = xo.GUARD_BYTES
    xo.GUARD_BYTES = 1 * 1024 * 1024
    try:
        tracemalloc.start()
        total, streamed = 0, False
        for chunk, was_stream in xo.read_member(data, "big.bin"):
            total += len(chunk)
            streamed = streamed or was_stream
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        assert streamed, "oversized member was slurped, not streamed"
        assert total == 20 * 1024 * 1024, total
        assert peak < 8 * 1024 * 1024, f"peak {peak} unbounded"
    finally:
        xo.GUARD_BYTES = old


@T("stdlib-only-no-third-party-import")
def _():
    import ast
    src = open(os.path.join(HERE, "extract-ooxml.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    allowed = {"io", "re", "sys", "zipfile", "xml.etree.ElementTree", "json",
               "xml", "hashlib", "os"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                assert a.name.split(".")[0] in {x.split(".")[0] for x in allowed}, a.name
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".")[0] in {x.split(".")[0] for x in allowed}, node.module


@T("no-text-ships-empty-extraction-never-fabrication")
def _():
    data = build_docx([])
    kind, lines = xo.extract_any("empty.docx", data)
    assert lines == [{"empty_extraction": True, "bytes": len(data)}], lines
    src = open(os.path.join(HERE, "extract-ooxml.py"), encoding="utf-8").read().lower()
    assert "tesseract" not in src and "ocrmypdf" not in src and "easyocr" not in src


@T("population-51-not-59-live-scope-count")
def _():
    sf = json.load(open(os.path.join(ROOT, "pipeline", "out", "scope-final.json"), encoding="utf-8"))
    docs = [r for r in sf["targets"] if r["kind"] != "audio"]
    ooxml = [r for r in docs if r.get("ext") in ("docx", "pptx", "xlsx")]
    assert len(ooxml) == 51, f"OOXML population is {len(ooxml)}, not 51"
    assert len(ooxml) != 59
    import collections
    assert collections.Counter(r["ext"] for r in ooxml) == {"docx": 36, "pptx": 12, "xlsx": 3}


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} extract-ooxml tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:300]}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
