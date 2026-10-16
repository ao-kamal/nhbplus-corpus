#!/usr/bin/env python3
"""Frontmatter emitter: value DOMAINS, not a field count (bead uff).

render_frontmatter(note_path, *, date, duration, speakers, type, words)
writes the --- block into a note that ALREADY EXISTS (assembly created it;
this function never creates, renames, or moves files).

Domains (violations RAISE at emit; the writer never produces them):
  date      ^\\d{4}-\\d{2}-\\d{2}$ or "unknown"
  duration  int >= 0 or "unknown" (minutes; "3h 14m" converted by the CALLER,
            never stored). 0 allowed iff words > 0 (sub-minute units floor
            to 0: A2dWSZAK 50 s). 0 with 0 words -> FLAGGED, never written.
  speakers  int >= 1 or "unknown" (diarisation CLUSTERS, never people; the
            caveat goes in the body, never a sixth field)
  type      closed six: theory|guest|coaching|training|mastermind|other
  title     == the note's filename stem, read from the path itself
  keys      exactly the five, never null anywhere (null renders as an empty
            field in Obsidian: absence stops being a recorded fact)
"""
import os
import re

TYPES = ("theory", "guest", "coaching", "training", "mastermind", "other")
KEYS = ("title", "date", "type", "duration", "speakers")


class EmitFail(Exception):
    pass


class Flagged(EmitFail):
    """duration 0 with zero words: 50 s of audio, empty note. Human looks."""


def render_frontmatter(note_path, *, date, duration, speakers, type, words):
    if not os.path.exists(note_path):
        raise EmitFail("emitter writes into existing notes only: no such file")
    title = os.path.splitext(os.path.basename(note_path))[0]
    if date != "unknown" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(date)):
        raise EmitFail(f"date out of domain: {date!r}")
    if isinstance(duration, str):
        if duration != "unknown":
            raise EmitFail(f"duration out of domain: {duration!r}")
    elif not (isinstance(duration, int) and not isinstance(duration, bool) and duration >= 0):
        raise EmitFail(f"duration out of domain: {duration!r}")
    if duration == 0 and words == 0:
        raise Flagged("duration 0 with zero words: flagging, not writing")
    if isinstance(speakers, str):
        if speakers != "unknown":
            raise EmitFail(f"speakers out of domain: {speakers!r}")
    elif not (isinstance(speakers, int) and not isinstance(speakers, bool) and speakers >= 1):
        raise EmitFail(f"speakers out of domain: {speakers!r}")
    if type not in TYPES:
        raise EmitFail(f"type out of domain: {type!r}")
    values = {"title": title, "date": date, "type": type,
              "duration": duration, "speakers": speakers}
    if any(v is None for v in values.values()):
        raise EmitFail("null frontmatter value: use unknown")
    block = "---\n" + "".join(f"{k}: {values[k]}\n" for k in KEYS) + "---\n"
    with open(note_path, encoding="utf-8") as f:
        body = f.read()
    if body.startswith("---\n"):
        end = body.index("---\n", 4) + 4
        body = body[end:]
    with open(note_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(block + body)
    return block


if __name__ == "__main__":
    print("types: " + "|".join(TYPES))
