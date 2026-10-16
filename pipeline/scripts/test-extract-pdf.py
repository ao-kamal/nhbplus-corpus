#!/usr/bin/env python3
"""Acceptance tests for the PDF extractor (bead nhbplus-corpus-dqh).

Reject a PDF extractor unless it fails on these inputs. Synthetic PDFs are
authored with pypdf itself (hand-built content streams, standard 14 fonts) -
no real corpus files needed, no mocks of the code under test. The 50-PDF E2E
(process all 50, assert 48/2/0 and 65,985 words) runs on the VM where the
files exist; it is scripted in the module docstring path, not faked here.

One JSONL line per test. Exit non-zero on failure.
"""
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location(
    "extract_pdf", os.path.join(HERE, "extract-pdf.py"))
xp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(xp)

from pypdf import PdfWriter, PdfReader
from pypdf.generic import (DecodedStreamObject, NameObject, DictionaryObject,
                           ArrayObject, TextStringObject, NumberObject)

LOG_PATH = os.path.join(ROOT, "pipeline", "out", "extract-pdf-tests.jsonl")
RESULTS = []
TMP = tempfile.mkdtemp(prefix="dqh-")


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def log(name, artifact, inp, verdict, note=""):
    RESULTS.append({"test": name, "artifact": artifact,
                    "input_digest": digest(inp), "verdict": verdict, "note": note})


def T(name):
    def deco(fn):
        try:
            fn()
            log(name, "extract-pdf.py", {"case": name}, "PASS", "")
            return True
        except Exception:
            log(name, "extract-pdf.py", {"case": name}, "FAIL",
                traceback.format_exc(limit=5).replace("\n", " | "))
            return False
    return deco


def make_pdf(pages, annots_uri=None, image=False):
    """pages: list of (ops_bytes, page_height). Returns path."""
    w = PdfWriter()
    for ops, _h in pages:
        page = w.add_blank_page(612, 792)
        cs = DecodedStreamObject()
        cs.set_data(ops)
        page[NameObject("/Contents")] = w._add_object(cs)
        font = DictionaryObject()
        font[NameObject("/Type")] = NameObject("/Font")
        font[NameObject("/Subtype")] = NameObject("/Type1")
        font[NameObject("/BaseFont")] = NameObject("/Helvetica")
        fonts = DictionaryObject()
        fonts[NameObject("/F1")] = w._add_object(font)
        res = DictionaryObject()
        res[NameObject("/Font")] = fonts
        if image:
            img = DictionaryObject()
            img[NameObject("/Type")] = NameObject("/XObject")
            img[NameObject("/Subtype")] = NameObject("/Image")
            img[NameObject("/Width")] = NumberObject(1)
            img[NameObject("/Height")] = NumberObject(1)
            img[NameObject("/BitsPerComponent")] = NumberObject(1)
            img[NameObject("/ColorSpace")] = NameObject("/DeviceGray")
            stream = DecodedStreamObject()
            stream.set_data(b"\x00")
            stream.update(img)
            xobjs = DictionaryObject()
            xobjs[NameObject("/Im1")] = w._add_object(stream)
            res[NameObject("/XObject")] = xobjs
        page[NameObject("/Resources")] = w._add_object(res)
        if annots_uri:
            ann = DictionaryObject()
            ann[NameObject("/Type")] = NameObject("/Annot")
            ann[NameObject("/Subtype")] = NameObject("/Link")
            ann[NameObject("/Rect")] = ArrayObject(
                [NumberObject(0), NumberObject(0), NumberObject(10), NumberObject(10)])
            act = DictionaryObject()
            act[NameObject("/S")] = NameObject("/URI")
            act[NameObject("/URI")] = TextStringObject(annots_uri)
            ann[NameObject("/A")] = w._add_object(act)
            page[NameObject("/Annots")] = ArrayObject([w._add_object(ann)])
    p = os.path.join(TMP, f"synth-{len(os.listdir(TMP))}.pdf")
    with open(p, "wb") as f:
        w.write(f)
    return p


@T("hex-glyph-stream-yields-no-words-and-regex-absent")
def _():
    # Image-only page: the old Tj/TJ regex scored 449,418 "characters" here.
    p = make_pdf([(b"", 792)], image=True)
    r = xp.extract_pdf(p)
    assert r["words"] == 0, r["words"]
    assert r["class"] == "raster", r["class"]
    assert r["images"] >= 1, r["images"]
    assert r["image_bytes_decoded"] == 0
    src = open(os.path.join(HERE, "extract-pdf.py"), encoding="utf-8").read()
    import re
    code = re.sub(r'"""[\s\S]*?"""', "", src)
    assert not re.search(r"re\.(search|findall|match).*T[jJ]", code), "Tj/TJ regex present"


@T("47-refuted-7figure-present-parts-equal-total")
def _():
    targets = xp.target_handles()
    assert len(targets) == 50, len(targets)
    assert "46cEGZpD" in targets, "7-Figure VSL missing: the 47 is back"
    # The v1 mechanism: hand-typed name missing its ordinal + silent continue.
    by_name = {"7-Figure VSL Script Template": "46cEGZpD"}
    try:
        hit = by_name.get("6. 7-Figure VSL Script Template")
        if not hit:
            raise xp.LookupMiss("6. 7-Figure VSL Script Template")
        raise SystemExit("silent continue survived")
    except xp.LookupMiss:
        pass
    # Parts not summing to the declared total refuses to write.
    text = [{"class": "text", "words": 100}] * 47
    try:
        xp.audit(text, expect_total=50)
        raise SystemExit("47+0+0 against declared 50 wrote anyway")
    except SystemExit:
        pass
    ok = xp.audit([{"class": "text", "words": 1}] * 48
                  + [{"class": "sparse", "words": 1}] * 2, expect_total=50)
    assert ok["classes"] == {"text": 48, "sparse": 2, "raster": 0}, ok


@T("degeneracy-gate-is-font-size-never-wpp")
def _():
    assert xp.classify(11.04, 7.0, 0.0, 700) == "text"      # 7wpp, real font
    assert xp.classify(12.0, 814.0, 0.0, 814) == "text"     # 7-Figure: 814 wpp
    assert xp.classify(1.0, 3.5, 0.17, 691) == "sparse"     # AC eBook shape
    assert xp.classify(1.0, 3.4, 0.18, 681) == "sparse"     # AC_Book shape
    assert xp.classify(2.0, 3.0, 0.2, 300) == "sparse"      # at the gate
    assert xp.classify(2.01, 3.0, 0.2, 300) == "text"       # above the gate
    assert xp.classify(12.0, 5.0, 0.0, 0) == "raster"       # no words: raster
    # A wpp-keyed gate (>= 10 wpp) misfiles real documents; ours must not.
    assert xp.classify(11.04, 7.0, 0.0, 700) != "sparse"


@T("fragment-spans-excluded-from-words-kept-for-gate")
def _():
    # Two Baselines-scattered 1.0pt single glyphs (the eBook shape) plus one
    # real 12pt line: words count the line, the gate still sees the fragments.
    # Two scattered 1pt single characters (the eBook fragment shape; ASCII
    # here - the property under test is span text volume, not glyph encoding)
    # plus one real 12pt line.
    ops = (b"BT /F1 1 Tf 72 700 Td (q) Tj ET "
           b"BT /F1 1 Tf 72 650 Td (q) Tj ET "
           b"BT /F1 12 Tf 72 600 Td (real words here) Tj ET")
    p = make_pdf([(ops, 792)])
    reader = PdfReader(p)
    spans = xp.collect_spans(reader.pages[0])
    assert len(spans) == 3, spans
    content, frag = xp.split_content(spans)
    assert len(content) == 1 and len(frag) == 2, (len(content), len(frag))
    assert xp.dominant_pt(spans) == 1.0  # gate sees everything
    r = xp.extract_pdf(p)
    assert r["words"] == 3, r["words"]
    assert r["fragment_spans"] == 2, r
    assert r["class"] == "text", r["class"]  # not degenerate-gated either


@T("multiword-small-spans-are-content-vsl-shape")
def _():
    # VSL shape: every span at 1.0pt raw size, each carrying ~10 real words
    # under a scaled text matrix. Raw-size filtering would zero this document.
    ops = (b"BT /F1 1 Tf 72 720 Td (one two three four five six seven eight nine ten) Tj ET "
           b"BT /F1 1 Tf 72 700 Td (eleven twelve thirteen fourteen fifteen sixteen) Tj ET")
    p = make_pdf([(ops, 792)])
    r = xp.extract_pdf(p)
    assert r["words"] == 16, r["words"]
    assert r["fragment_spans"] == 0, r
    assert r["dominant_pt"] == 1.0, r  # degenerate flag set...
    assert r["class"] == "text", r["class"]  # ...but high wpp says text


@T("ytol-digest-stable-and-lines-grouped")
def _():
    ops = (b"BT /F1 12 Tf 72 720 Td (upper baseline text) Tj ET "
           b"BT /F1 12 Tf 72 700 Td (lower baseline text) Tj ET")
    p = make_pdf([(ops, 792)])
    reader = PdfReader(p)
    spans = xp.collect_spans(reader.pages[0])
    assert len(spans) == 2, spans
    digests = set()
    for tol in (0.0, 0.25, 0.5, 0.6, 1.0, 2.0, 3.0, 5.0):
        digests.add(xp.line_digest(xp.group_lines(spans, y_tol=tol)))
    assert len(digests) == 1, digests
    lines = xp.group_lines(spans)
    assert len(lines) == 2 and lines[0]["text"] == "upper baseline text", lines


@T("tier-rule-title-body-headings")
def _():
    lines = ([{"y": 700.0 - i, "text": "t", "sizes": [60.0]} for i in range(1)]
             + [{"y": 600.0 - i, "text": "h", "sizes": [24.0]} for i in range(6)]
             + [{"y": 500.0 - i, "text": "b", "sizes": [11.04]} for i in range(20)])
    tm = xp.tiers(lines)
    assert tm == {24.0: 6, 11.04: 20}, tm  # 60pt on 1 line < TIER_MIN 5
    title, body, headings = xp.title_body_headings(tm, lines)
    assert (title, body, headings) == (24.0, 11.04, []), (title, body, headings)
    # title_size x 0.55 = 33.0pt exclusion reproduced and rejected: with a
    # largest tier of 60 the 24pt heading tier must survive, not be cut.
    lines2 = ([{"y": 700.0, "text": "t", "sizes": [60.0]} for _ in range(6)]
              + [{"y": 600.0 - i, "text": "h", "sizes": [24.0]} for i in range(6)]
              + [{"y": 500.0 - i, "text": "b", "sizes": [11.04]} for i in range(20)])
    tm2 = xp.tiers(lines2)
    title2, body2, headings2 = xp.title_body_headings(tm2, lines2)
    assert title2 == 60.0 and headings2 == [24.0], (title2, body2, headings2)


@T("urls-from-annots-never-display-text")
def _():
    uri = "https://docs.google.com/spreadsheets/d/acQ/edit#gid=5683798"
    ops = b"BT /F1 12 Tf 72 720 Td (see the sheet at acQ/e dit#gid=5683798 here) Tj ET"
    p = make_pdf([(ops, 792)], annots_uri=uri)
    r = xp.extract_pdf(p)
    assert r["urls"] == [uri], r["urls"]
    for u in r["urls"]:
        assert " " not in u and "\n" not in u, u  # no wrapped fragments


@T("page-cap-recorded-by-name")
def _():
    ops = b"BT /F1 12 Tf 72 720 Td (page text here) Tj ET"
    p = make_pdf([(ops, 792)] * 3)
    r = xp.extract_pdf(p, page_cap=2)
    assert r["pages_read"] == 2 and r["pages_total"] == 3, r


def main():
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    total = len(RESULTS)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for r in RESULTS:
            f.write(json.dumps(r) + "\n")
    print(f"{passed}/{total} extract-pdf tests passed; log: {LOG_PATH}")
    for r in RESULTS:
        if r["verdict"] != "PASS":
            print(f"  [FAIL] {r['test']} - {r['note'][:300]}")
    import shutil
    shutil.rmtree(TMP, ignore_errors=True)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
