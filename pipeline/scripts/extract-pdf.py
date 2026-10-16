#!/usr/bin/env python3
"""PDF extraction with pypdf - 48 text, 2 sparse, 0 raster (bead dqh).

Route (measured, not assumed):
  page.extract_text(visitor_text=...) -> per-span size, baseline, x.
REJECTED: content-stream Tj/TJ regex -> hex glyph indices, not characters.
Images enumerated via /Resources /XObject, NEVER decoded: 0 bytes written.
Links: /Annots is the ONLY authoritative layer; display-text URLs are mangled
by wrapping and are never recovered.

Calibration (re-measured on this corpus, never inherited):
  Y_TOL=0.6  DEGENERATE_PT=2.0  TIER_MIN=5  page_cap=200
  tier rule: gate first, title = largest tier, body = most frequent tier,
             every other tier = heading tier.

Classes: text 48 / sparse 2 (AC eBook snViEZ6C, AC_Book 52c22T5D) / raster 0.
Sparse rule (from fallback-audit v2 verdicts): degenerate_geometry AND
words/page < 10 AND images/page >= 0.1. A 7-words-per-page document with an
11.04pt dominant font is text, not sparse; 7-Figure VSL at 814 wpp is the
least sparse document in the set. Raster (0 words) ships empty_extraction
and is never OCR-billed.

The 50-target population is DERIVED from pdf-scope-all.json, never hand-typed:
a lookup miss is SystemExit, not continue. The v1 hand list dropped
`6. 7-Figure VSL Script Template` on a missing `6. ` ordinal.
"""
import hashlib
import json
import os
import sys

try:
    from pypdf import PdfReader
    from pypdf.generic import ContentStream
except ImportError:
    PdfReader = None

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

Y_TOL = 0.6
DEGENERATE_PT = 2.0
TIER_MIN = 5
PAGE_CAP = 200
SPARSE_WPP_MAX = 10.0
SPARSE_IMG_PP_MIN = 0.1


class LookupMiss(SystemExit):
    pass


def target_handles():
    """The 50 PDF targets, derived from the ceiling artifact's population."""
    with open(os.path.join(ROOT, "pipeline", "out", "pdf-scope-all.json"), encoding="utf-8") as f:
        scope = json.load(f)
    with open(os.path.join(ROOT, "pipeline", "out", "pdf-ceiling.json"), encoding="utf-8") as f:
        ceiling = json.load(f)
    targets = [t["handle"] for t in scope["targets"]]
    by_handle = {r["handle"]: r for r in ceiling["results"]}
    for h in targets:
        if h not in by_handle:
            raise LookupMiss(f"target {h} missing from ceiling results")
    missing = [h for h in by_handle if h not in set(targets)]
    if missing:
        raise LookupMiss(f"ceiling results outside target population: {missing}")
    if "46cEGZpD" not in targets:
        raise LookupMiss("6. 7-Figure VSL Script Template (46cEGZpD) not in targets")
    return targets


def collect_spans(page):
    """Per-span (text, size, baseline y, x). No regex over content streams."""
    spans = []

    def visitor(text, cm, tm, font_dict, font_size):
        if text and text.strip():
            # tm = text matrix; ty (tm[5]) is the baseline in page space.
            spans.append({"text": text, "size": float(font_size),
                          "y": float(tm[5]), "x": float(tm[4])})

    page.extract_text(visitor_text=visitor)
    return spans


def group_lines(spans, y_tol=Y_TOL):
    """Order spans top-to-bottom, left-to-right; group baselines within tol."""
    ordered = sorted(spans, key=lambda s: (-round(s["y"] / 0.01), s["x"]))
    lines = []
    for s in ordered:
        if lines and abs(lines[-1][0]["y"] - s["y"]) <= y_tol:
            lines[-1].append(s)
        else:
            lines.append([s])
    out = []
    for line in lines:
        line.sort(key=lambda s: s["x"])
        out.append({"y": line[0]["y"], "text": "".join(s["text"] for s in line),
                    "sizes": [s["size"] for s in line]})
    return [ln for ln in out if ln["text"].strip()]


def line_digest(lines):
    return hashlib.sha256("\n".join(ln["text"] for ln in lines).encode()).hexdigest()


def tiers(lines, tier_min=TIER_MIN):
    """size -> line count for sizes carried by >= tier_min lines."""
    from collections import Counter
    c = Counter()
    for ln in lines:
        for s in set(round(x, 2) for x in ln["sizes"]):
            c[s] += 1
    return {s: n for s, n in c.items() if n >= tier_min}


def title_body_headings(tier_map, lines):
    if not tier_map:
        return None, None, []
    title = max(tier_map)
    body = max(tier_map, key=lambda s: (tier_map[s], -s))
    headings = sorted((s for s in tier_map if s not in (title, body)), reverse=True)
    return title, body, headings


def dominant_pt(spans):
    from collections import Counter
    c = Counter(round(s["size"], 2) for s in spans)
    return c.most_common(1)[0][0] if c else 0.0


def is_fragment(span):
    """Single-character spans at degenerate raw size are glyph-index leakage,
    not characters (live: 'b'/'ǧ' at 1.0pt, one per baseline, 170k of them on
    the sparse books). Multi-word spans at small raw size are real text under
    a scaled text matrix (live: 81 of 82 spans on the 1-page VSL, ~10
    words/span; 2,746 of 4,103 on Swipe). Raw size alone cannot tell them
    apart; span text volume can."""
    return len(span["text"].strip()) <= 1 and span["size"] <= DEGENERATE_PT


def split_content(spans):
    """Content spans carry characters; fragments ARE the degenerate geometry.
    Counting fragments as words double-counts the disease as health (live:
    4,877 phantom words on AC eBook vs the probe's 691). Words, lines,
    digests and tiers derive from content spans only; the gate still sees
    every span, so dominant_pt is unchanged."""
    content = [s for s in spans if not is_fragment(s)]
    frag = [s for s in spans if is_fragment(s)]
    return content, frag


def enumerate_images(page):
    """Count image XObjects. Decode nothing; 0 bytes written, always."""
    try:
        resources = page.get("/Resources")
        if resources is None:
            return 0
        xobj = resources.get("/XObject")
        if xobj is None:
            return 0
        xobj = xobj.get_object()
        n = 0
        for ref in xobj.values():
            try:
                if ref.get_object().get("/Subtype") == "/Image":
                    n += 1
            except Exception:
                pass
        return n
    except Exception:
        return 0


def annot_urls(page):
    """The ONLY authoritative link layer."""
    urls = set()
    try:
        annots = page.get("/Annots")
        if not annots:
            return urls
        for ref in annots:
            try:
                a = ref.get_object()
                act = a.get("/A")
                if act:
                    uri = act.get_object().get("/URI")
                    if uri:
                        urls.add(str(uri))
            except Exception:
                pass
    except Exception:
        pass
    return urls


def classify(dominant, words_per_page, images_per_page, words):
    """text / sparse / raster. Font-size gate, never words-per-page."""
    if words == 0:
        return "raster"
    degenerate = dominant <= DEGENERATE_PT
    if degenerate and words_per_page < SPARSE_WPP_MAX and images_per_page >= SPARSE_IMG_PP_MIN:
        return "sparse"
    return "text"


def extract_pdf(path, page_cap=PAGE_CAP):
    """Full per-document extraction. Returns dict; decodes 0 image bytes."""
    if PdfReader is None:
        raise RuntimeError("pypdf not installed")
    reader = PdfReader(path)
    total = len(reader.pages)
    pages = reader.pages[:page_cap]
    all_spans, content_lines, images, urls = [], [], 0, set()
    frag_total, content_words = 0, 0
    for page in pages:
        spans = collect_spans(page)
        all_spans.extend(spans)
        content, frag = split_content(spans)
        frag_total += len(frag)
        page_lines = group_lines(content)
        content_lines.extend(page_lines)
        content_words += sum(len(ln["text"].split()) for ln in page_lines)
        images += enumerate_images(page)
        urls |= annot_urls(page)
    words = content_words
    dom = dominant_pt(all_spans)
    wpp = words / max(1, len(pages))
    ipp = images / max(1, len(pages))
    cls = classify(dom, wpp, ipp, words)
    tier_map = tiers(content_lines)
    title, body, headings = title_body_headings(tier_map, content_lines)
    return {
        "pages_read": len(pages), "pages_total": total,
        "words": words, "dominant_pt": dom,
        "fragment_spans": frag_total,
        "words_per_page": round(wpp, 2), "images": images,
        "images_per_page": round(ipp, 3),
        "class": cls, "title_pt": title, "body_pt": body,
        "heading_pts": headings, "urls": sorted(urls),
        "digest": line_digest(content_lines),
        "image_bytes_decoded": 0,
    }


def audit(results, expect_total=None):
    """Aggregate results; parts MUST equal the total before writing.

    expect_total is the DECLARED population (50). v1 reported 47+2+0
    against its own declared total 50 and printed the summary anyway -
    that shape raises here instead of writing.
    """
    classes = {"text": 0, "sparse": 0, "raster": 0}
    words = 0
    for r in results:
        classes[r["class"]] += 1
        words += r["words"]
    total = len(results)
    parts = classes["text"] + classes["sparse"] + classes["raster"]
    if parts != total:
        raise SystemExit(f"parts {parts} != total {total}: refusing to write")
    if expect_total is not None and total != expect_total:
        raise SystemExit(f"results {total} != declared {expect_total}: refusing to write")
    return {"n": total, "classes": classes, "words": words}


if __name__ == "__main__":
    print(json.dumps({"targets": len(target_handles())}))
