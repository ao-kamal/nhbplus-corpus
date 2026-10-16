#!/usr/bin/env python3
"""The 8 non-OOXML, non-PDF documents (bead nhbplus-corpus-8pt).

Identified BY CLASS from scope-final.json (ext in txt/png/zip), never by
filename. 6 txt + 1 png + 1 zip.

- txt: stdlib read (utf-8-sig). The 5 `Resources Links` share a stem across
  5 courses; the §10.2 course prefix (courses/<Course>/...) is what keeps
  their paths distinct. Distinctness is asserted, not assumed.
- png (guNkBLaZ Pick Primary Color): NEVER decoded, never rendered. Ships as
  a manifest entry (description + IHDR dimensions + sha256), contributing
  no bytes. The exporter turns a png path into a NOTE, never a file.
- zip (Lazy Loading Code, 296 MiB): central-directory enumeration BEFORE any
  parse, guarded streaming via the shared OOXML helpers. Parsed members are
  never read as one blob.
- No text -> empty_extraction with measured facts. No OCR anywhere.
- attachments/ does not exist and is never created.
"""
import hashlib
import importlib.util
import json
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location(
    "extract_ooxml", os.path.join(HERE, "extract-ooxml.py"))
xo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(xo)

MISC_EXTS = ("txt", "png", "zip")


def misc_handles(scope_targets=None):
    """The 8, derived by class from scope-final. Never a name list."""
    if scope_targets is None:
        with open(os.path.join(ROOT, "pipeline", "out", "scope-final.json"), encoding="utf-8") as f:
            scope_targets = json.load(f)["targets"]
    return [r["handle"] for r in scope_targets if r.get("ext") in MISC_EXTS]


def read_txt(data):
    text = data.decode("utf-8-sig")
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return [{"empty_extraction": True, "bytes": len(data)}]
    return lines


def png_entry(filename, data):
    """Manifest entry from header bytes only. No decode, no render."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    (length, kind) = struct.unpack(">I4s", data[8:16])
    if kind != b"IHDR":
        raise ValueError("first chunk is not IHDR")
    width, height = struct.unpack(">II", data[16:24])
    return {"file": filename, "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "dimensions": f"{width}x{height}"}


def png_note(entry):
    """A png path produces a NOTE (markdown lines), never a file."""
    return [
        f"# {entry['file']} (image reference, no bytes shipped)",
        "",
        f"Dimensions: {entry['dimensions']}. Size on source: {entry['bytes']} bytes.",
        f"SHA-256: `{entry['sha256']}`",
        "",
        "Recorded by description and hash per §8.3. Constraint 1: this note",
        "carries zero image bytes.",
    ]


def txt_paths_distinct(paths):
    return len(set(paths)) == len(paths)


if __name__ == "__main__":
    print(json.dumps({"misc_handles": misc_handles()}))
