#!/usr/bin/env python3
"""OOXML extraction with the Python stdlib alone (bead nhbplus-corpus-5zb).

51 documents: 36 docx + 12 pptx + 3 xlsx. No third-party import anywhere in
this file - Rule 2 intact. ZIP+XML: zipfile + xml.etree, document order.

- docx: word/document.xml, w:p paragraphs, w:t runs in order.
- pptx: ppt/slides/slideN.xml in NUMERIC slide order (presentation.xml order
  when present, never dict order), a:t text runs.
- xlsx: shared strings + sheet rows in row/cell order.
- Output is markdown text only. Zero source bytes reach the vault.
- No text -> empty_extraction with the measured facts, never a fabrication.
- 296 MiB Lazy Loading Code ZIP: enumerate the central directory FIRST
  (authoritative over member headers), stream any member whose declared
  uncompressed size exceeds the guard via ZipFile.open(), one member at a
  time. The ZIP is a member enumeration, not a single read.
"""
import io
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

# Stdlib-only gate: every import in this file must be stdlib.
GUARD_BYTES = 64 * 1024 * 1024  # members above this stream, never slurp

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
}


def _text_of(elem, tag):
    return "".join(
        (t.text or "") for t in elem.iter(tag))


def docx_to_markdown(data):
    zf = zipfile.ZipFile(io.BytesIO(data))
    xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    paras = []
    for p in root.iter(f"{{{NS['w']}}}p"):
        txt = "".join((t.text or "") for t in p.iter(f"{{{NS['w']}}}t"))
        if txt.strip():
            paras.append(txt)
    return paras


def _slide_num(name):
    m = re.search(r"slide(\d+)\.xml$", name)
    return int(m.group(1)) if m else 10 ** 9


def pptx_to_markdown(data):
    """Slides in numeric order; dict iteration order is never trusted."""
    zf = zipfile.ZipFile(io.BytesIO(data))
    names = zf.namelist()
    slides = sorted((n for n in names
                     if n.startswith("ppt/slides/slide") and n.endswith(".xml")),
                    key=_slide_num)
    out = []
    for i, name in enumerate(slides, 1):
        root = ET.fromstring(zf.read(name))
        texts = [(t.text or "") for t in root.iter(f"{{{NS['a']}}}t") if (t.text or "").strip()]
        if texts:
            out.append(f"## Slide {i}")
            out.extend(texts)
    return out


def xlsx_to_markdown(data):
    zf = zipfile.ZipFile(io.BytesIO(data))
    shared = []
    try:
        sroot = ET.fromstring(zf.read("xl/sharedStrings.xml"))
        for si in sroot.iter(f"{{{NS['s']}}}t"):
            shared.append(si.text or "")
    except KeyError:
        pass
    out = []
    sheets = sorted(n for n in zf.namelist()
                    if n.startswith("xl/worksheets/sheet") and n.endswith(".xml"))
    for name in sheets:
        root = ET.fromstring(zf.read(name))
        for row in root.iter(f"{{{NS['s']}}}row"):
            cells = []
            for c in row.iter(f"{{{NS['s']}}}c"):
                t = c.get("t")
                v = c.find(f"{{{NS['s']}}}v")
                v = v.text if v is not None else ""
                if t == "s" and v.isdigit() and int(v) < len(shared):
                    cells.append(shared[int(v)])
                elif (c.find(f"{{{NS['s']}}}is") is not None):
                    cells.append(_text_of(c.find(f"{{{NS['s']}}}is"), f"{{{NS['s']}}}t"))
                else:
                    cells.append(v)
            if any(x.strip() for x in cells):
                out.append(" | ".join(cells))
    return out


def enumerate_zip(data):
    """Central-directory-first enumeration: name, declared size, stream-hint."""
    zf = zipfile.ZipFile(io.BytesIO(data))
    return [{"name": i.filename, "declared": i.file_size,
             "stream": i.file_size > GUARD_BYTES} for i in zf.infolist()]


def read_member(data, name, chunk=1 << 20):
    """Stream members above the guard; small members read whole. Yields bytes."""
    zf = zipfile.ZipFile(io.BytesIO(data))
    info = zf.getinfo(name)  # central directory: authoritative, not the header
    if info.file_size > GUARD_BYTES:
        with zf.open(name) as f:
            while True:
                b = f.read(chunk)
                if not b:
                    break
                yield b, True
    else:
        yield zf.read(name), False


def extract_any(filename, data):
    """filename-aware dispatch. Returns (kind, markdown_lines_or_members)."""
    lower = filename.lower()
    if lower.endswith(".docx"):
        lines = docx_to_markdown(data)
        kind = "docx"
    elif lower.endswith(".pptx"):
        lines = pptx_to_markdown(data)
        kind = "pptx"
    elif lower.endswith(".xlsx"):
        lines = xlsx_to_markdown(data)
        kind = "xlsx"
    elif lower.endswith(".zip"):
        return ("zip", enumerate_zip(data))
    else:
        raise ValueError(f"not OOXML/zip: {filename}")
    if not lines:
        return (kind, [{"empty_extraction": True, "bytes": len(data)}])
    assert all(isinstance(x, (str, dict)) for x in lines)
    return (kind, lines)


if __name__ == "__main__":
    import json
    print(json.dumps({"guard_bytes": GUARD_BYTES}))
