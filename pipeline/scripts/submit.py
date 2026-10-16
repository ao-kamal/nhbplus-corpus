#!/usr/bin/env python3
"""The ONE sync submission path (bead z72). No async branch exists.

POST https://api.eu.deepgram.com/v1/listen, eight parameters asserted ON THE
WIRE (outbound URL), never in the code path:
  model=nova-3 diarize=true smart_format=true punctuate=true utterances=true
  language=en mip_opt_out=true keyterm=... (proper nouns only, optional)

diarize=true is a REQUIRED builder argument with no default: omitting it
silently moves the ceiling 25->50 and kills diarisation clusters.
mip_opt_out rides EVERY request including retries. A retry re-POSTs the
IDENTICAL URL; only Authorization changes (failover), never the payload.

Body: the .mka part STREAMED from disk (never read-all; never curl
--data-binary, which OOMs at 1.4 GB and drops the only retrieval there will
ever be). Response streams straight to disk as it arrives; a partial file is
the normal mid-run state and response_complete tells it from complete.

Arrival assertion: results.utterances non-empty AND
results.channels[0].alternatives[0].paragraphs present (paragraphs lives
under alternatives[0], not channels[0]). Either missing -> FAIL, no
assembled.json. Any timeout -> PAID_UNKNOWN, never a clean zero (the raw
1,539 MB MP4 timed out after >1,800 s with unknowable billing).

402 -> WHOLE part to the secondary, re-commit on its ledger,
account=secondary on the receipt, never split. 429 -> identical re-POST.
Concurrency: at most 25 in flight, single key; the second key is a WALLET
(sequential failover, never concurrent distribution).
"""
import json
import os
import urllib.parse
import urllib.request

BASE = "https://api.eu.deepgram.com/v1/listen"
TRANSCRIBE_CONCURRENCY = 25


class SubmitFail(Exception):
    pass


class PaidUnknown(Exception):
    pass


def build_url(diarize, keyterms=()):
    """diarize is REQUIRED: no default, no omission path."""
    if diarize is not True:
        raise SubmitFail("diarize must be exactly True: ceiling 25 depends on it")
    params = [("model", "nova-3"), ("diarize", "true"),
              ("smart_format", "true"), ("punctuate", "true"),
              ("utterances", "true"), ("language", "en"),
              ("mip_opt_out", "true")]
    for k in keyterms:
        if not (isinstance(k, str) and k.strip()):
            raise SubmitFail(f"empty keyterm rejected: {k!r}")
        params.append(("keyterm", k.strip()))
    return BASE + "?" + urllib.parse.urlencode(params)


def headers(api_key, part_path):
    if not part_path.endswith(".mka"):
        raise SubmitFail(f"container must be .mka, not {part_path}")
    if not api_key:
        raise SubmitFail("no API key: refusing unauthenticated submit")
    return {"Authorization": f"Token {api_key}",
            "Content-Type": "audio/x-matroska"}


def check_arrival(obj):
    """Both shapes present or the transcript does not exist."""
    try:
        utterances = obj["results"]["utterances"]
        paras = obj["results"]["channels"][0]["alternatives"][0]["paragraphs"]
    except (KeyError, IndexError, TypeError) as e:
        raise SubmitFail(f"arrival shape missing: {e}")
    if not utterances:
        raise SubmitFail("results.utterances empty: nothing to build from")
    if not paras or not paras.get("paragraphs"):
        raise SubmitFail("paragraphs absent: V12 unevaluable")
    return True


def post_file(url, api_key, part_path, response_path, timeout=600, opener=None):
    """Stream body up, stream response down. Returns (http_status, complete)."""
    size = os.path.getsize(part_path)
    if size == 0:
        raise SubmitFail("refusing to submit an empty part")
    req = urllib.request.Request(url, headers=headers(api_key, part_path), method="POST")
    towrite = open(response_path, "wb")
    complete = False
    try:
        with open(part_path, "rb") as body:
            req.data = body  # streamed; Content-Length set below
            req.add_header("Content-Length", str(size))
            if opener is None:
                opener = urllib.request.build_opener()
            try:
                resp = opener.open(req, timeout=timeout)
            except TimeoutError as e:
                raise PaidUnknown(f"submit timeout: {e}")
            except OSError as e:
                raise PaidUnknown(f"submit transport failure: {e}")
            status = resp.getcode()
            while True:
                chunk = resp.read(1 << 20)
                if not chunk:
                    break
                towrite.write(chunk)
            complete = True
            return status, complete
    finally:
        towrite.close()
        if not complete:
            try:
                with open(response_path + ".partial", "w") as f:
                    f.write("partial")
            except OSError:
                pass
    return None, False
