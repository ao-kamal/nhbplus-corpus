#!/usr/bin/env python3
"""Vault assembly: 344 notes at exactly the clean-names paths (bead a7z).

Paths come from clean-names.json (344 measured, unique case-insensitively):
never a glob, never title-derived at assembly time. attachments/ never
exists. Zero media bytes under vault/ (V6 owns that verdict).

Audio notes: utterances concatenated in order (part offsets applied by the
caller), overlaps deduped, per-30-minute `### 0:00`-style jump headings
(zero inference: timestamps already in the data), speaker-cluster caveat in
the BODY, WPM recorded. Doc notes: extractor lines joined. Sparse books: stub
with measured facts + every content word verbatim in page order under
#### p. N headings + explicit no-layout statement (never a summary, never a
bare handle). PNG: the png_note. Empty extractions: measured-facts stub.

Frontmatter is rendered by frontmatter.py AFTER the body exists (uff owns
the domains; assembly owns the bytes).
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location(
    "frontmatter_mod", os.path.join(HERE, "frontmatter.py"))
fm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fm)

SPEAKER_CAVEAT = ("Speaker labels below are algorithmically derived clusters, "
                  "not identified people: one label on a long call usually "
                  "means diarisation failed, not that one person spoke.")


def half_minute_headings(utterances):
    """Per-30-minute ### headings from utterance starts. Zero inference."""
    marks = []
    for u in utterances:
        slot = int(u["start"] // 1800)
        if not marks or marks[-1][0] != slot:
            marks.append((slot, u["start"]))
    out = []
    for slot, _ in marks:
        out.append(f"### {slot // 2}:{slot % 2 * 30:02d}")
    return out


def dedupe_overlap(texts):
    """Drop a segment fully contained in the previous one (seam repeats)."""
    out = []
    for t in texts:
        if not out or t not in out[-1]:
            out.append(t)
    return out


def audio_body(utterances, speakers):
    lines, last_slot = [], None
    texts = []
    for u in utterances:
        slot = int(u["start"] // 1800)
        if slot != last_slot:
            lines.append(f"### {slot // 2}:{slot % 2 * 30:02d}")
            last_slot = slot
        sp = f"Speaker {u.get('speaker', '?')}: " if u.get("speaker") is not None else ""
        lines.append(f"{sp}{u.get('transcript', '')}")
        texts.append(u.get("transcript", ""))
    words = sum(len(t.split()) for t in dedupe_overlap(texts))
    body = "\n\n".join(lines)
    body += f"\n\n*{SPEAKER_CAVEAT} Speakers observed: {speakers}.*\n"
    return body, words


def sparse_stub(name, pages_detail, measured):
    lines = [f"# {name} (sparse extraction)",
             "",
             f"Measured: {measured}. No layout is recoverable from these pages; "
             "what follows is every recovered word verbatim in page order, "
             "not a summary.",
             ""]
    for p in pages_detail:
        lines.append(f"#### p. {p['page']}")
        lines.append("")
        lines.extend(p["lines"] if p["lines"] else ["*(no recoverable text)*"])
        lines.append("")
    return "\n".join(lines)


def doc_body(lines):
    return "\n\n".join(lines) + "\n"


def assemble_note(path, body, front):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body if body.endswith("\n") else body + "\n")
    return fm.render_frontmatter(path, words=front.pop("words"), **front)
