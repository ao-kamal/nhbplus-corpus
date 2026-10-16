#!/usr/bin/env python3
"""Bulk audio runner: fetch -> remux -> channels -> submit -> settle (VM).

Reads worklist/targets.csv order (lpt16 then remainder; --block selects).
Docs blocks are done; smoke unit skipped (settled).

Per unit:
  fetch   mega-get per-handle dir (mkdir first), presence floor
          pulled >= 0.5 * declared, rate logged, source kept until remux ok
  remux   ffmpeg -nostdin -v error -y -i SRC -vn -c:a copy part-00.mka
          (REMUX_CONCURRENCY=2 semaphore). Source deleted after hash-ok.
  chan    ffprobe channels on the PART; stereo -> 90 s astats classifier;
          BIT_IDENTICAL -> flac collapse; DUAL_MONO -> opus; else as-is.
          INPUT_CHANNEL_COUNT = submitted count, in the sent atomic write.
  submit  ledger.commit under flock (stop $213.48 enforced) -> admit/
          reserve/sent with sent_ts -> 25-way POST (streamed, response to
          disk, socket_open_ts) -> arrival assert -> settle with
          metadata.duration x INPUT_CHANNEL_COUNT -> receipt (transport,
          timestamps, account) + gate-inputs.json for V3/V4/V5/V10.
  402     WHOLE part to secondary (sequential failover, never concurrent);
          needs /tmp/dg2.key or the run stops WALLET_NEEDED (operator).
  429/400 per the state table. Timeout/transport -> PAID_UNKNOWN, operator.

Resume: settled/lost skipped; reserved re-reserved; sent-no-outcome stops
PAID_UNKNOWN (0wv owns the branch table; this loop only implements it).
V2: every part asserted < CAP_BYTES before submit (never fires: max 383 MiB).
Keyterms: capitalized tokens from the unit title+topic (proper-noun
heuristic, documented), capped at 30; smoke proved the no-keyterm path.
"""
import csv
import json
import os
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

HOME = os.path.expanduser("~")
BASE = os.path.join(HOME, "nhbplus")
# Bulk audio I/O lives on the loopback (cap-enforced); manifests stay put.
WORK = os.environ.get("NHBPLUS_WORK", BASE)
SCR = os.path.join(BASE, "scripts")
sys.path.insert(0, SCR)
import importlib.util


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SCR, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


fp = load("fetch-pool")
ch = load("channels")
sl = load("spend-ledger")
ps = load("part-state")
sub = load("submit")

FETCH = os.path.join(WORK, "fetch")
UNITS = os.path.join(WORK, "units")
# ONE ledger (md5 founding rule): the smoke $0.103 already sits in the BASE
# ledger. Media bytes live under the cap; the ledger file itself does not
# need to (tiny, append-only, rescan-rebuildable from both trees).
os.environ["SPEND_LEDGER"] = os.path.join(BASE, "_meta", "spend.json")
STOPWORDS = {"The", "And", "For", "With", "From", "Into", "Nhb", "Nbh"}


def keyterms_for(title, topic, cap=30):
    toks = re.findall(r"[A-Z][a-z]{2,}", f"{title} {topic}")
    seen, out = set(), []
    for t in toks:
        if t not in seen and t not in STOPWORDS:
            seen.add(t)
            out.append(t)
    return out[:cap]


def sh(cmd, **kw):
    kw.setdefault("stdin", subprocess.DEVNULL)
    return subprocess.run(cmd, **kw)


def work_free_bytes():
    import shutil
    return shutil.disk_usage(UNITS).free


def wait_for_room(need, timeout=1800):
    """Disk admission: never over-admit the loopback. Completions free
    space, so waiting always terminates unless the box is wedged."""
    t0 = time.time()
    while work_free_bytes() < need:
        if time.time() - t0 > timeout:
            raise RuntimeError(f"DISK_STALL: free {work_free_bytes()} < need {need}")
        time.sleep(15)


def ffprobe_channels(path):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "a:0",
            "-show_entries", "stream=channels",
            "-of", "default=nw=1:nk=1", path],
           capture_output=True, text=True, check=True)
    n = int(r.stdout.strip())
    if n not in (1, 2):
        raise RuntimeError(f"HARD STOP channels={n} on {path}")
    return n


def ffprobe_duration(path):
    r = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=nw=1:nk=1", path],
           capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def astats_level(part, filt):
    r = sh(ch.measure_argv(part, filt), capture_output=True, text=True, check=True)
    return ch.parse_rms_level_db(r.stdout + r.stderr)


def classify_part(part):
    n = ffprobe_channels(part)
    if n == 1:
        return ch.classify(1)
    L = astats_level(part, ch.FILTER_L)
    R = astats_level(part, ch.FILTER_R)
    D = astats_level(part, ch.FILTER_D)
    return ch.classify(2, L, R, D)


def process_unit(row, keys, ledger, remux_sem, log):
    h, unit, dur_declared = row["handle"], row["unit"], row["dur_s"]
    udir = os.path.join(UNITS, unit)
    os.makedirs(udir, exist_ok=True)
    verdict, action = ps.recover(udir)
    if verdict in (ps.SETTLED, ps.LOST):
        return {"handle": h, "outcome": "skip-" + verdict}
    if verdict == ps.PAID_UNKNOWN:
        raise RuntimeError(f"{h}: PAID_UNKNOWN on resume: operator decides")

    # fetch
    fdir = fp.prepare_target_dir(FETCH, h)
    landed = None
    try:
        landed = fp.landed_file(fdir)
    except fp.FetchFail:
        pass
    if landed is None:
        url = row["url"]
        t0 = time.time()
        p = sh(["mega-get", url, fdir], capture_output=True, text=True)
        dt = time.time() - t0
        if p.returncode != 0:
            raise RuntimeError(f"{h}: mega-get rc={p.returncode}")
        landed = fp.landed_file(fdir)
        fp.record_rate(os.path.join(BASE, "out", "fetch-rates.jsonl"), h,
                       os.path.getsize(landed), dt)
    declared = int(row["bytes"]) if row["bytes"] else 0
    if declared:
        fp.presence_ok(os.path.getsize(landed), declared)

    # remux
    part = os.path.join(udir, "part-00.mka")
    if not os.path.exists(part):
        with remux_sem:
            r = sh(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", landed,
                    "-vn", "-c:a", "copy", part],
                   capture_output=True, text=True)
            if r.returncode != 0:
                raise RuntimeError(f"{h}: remux rc={r.returncode}")
    assert os.path.getsize(part) < 2_000_000_000, f"{h}: V2 CAP hit"
    # Source deleted IMMEDIATELY after remux (7k7): the loopback holds one
    # unit at a time, never the block. Deleting before submit is safe: the
    # part is hashed and receipted; the source is reproducible from MEGA.
    if os.path.exists(landed):
        os.remove(landed)

    # channels
    branch, in_ch, note = classify_part(part)
    submit_part = part
    if branch == ch.BIT_IDENTICAL:
        mono = os.path.join(udir, "part-00-mono.mka")
        if not os.path.exists(mono):
            with remux_sem:
                sh(ch.downmix_argv(branch, part, mono),
                   capture_output=True, check=True)
        submit_part = mono
    elif branch == ch.DUAL_MONO:
        opus = os.path.join(udir, "part-00-opus.mka")
        if not os.path.exists(opus):
            with remux_sem:
                sh(ch.downmix_argv(branch, part, opus),
                   capture_output=True, check=True)
        submit_part = opus

    # commit + submit + settle (single unit shown; pool parallelizes submit)
    return {"handle": h, "unit": unit, "branch": branch, "in_ch": in_ch,
            "part": submit_part, "dur_declared": dur_declared}


def submit_one(prep, keys, ledger, title, topic):
    h = prep["handle"]
    udir = os.path.join(UNITS, prep["unit"])
    # Room for the RESPONSE + journal headroom. The part is already on disk:
    # requiring 2x its size double-counts and deadlocks the pool (live
    # 2026-10-16: two 1.4 GB parts, 847 MB free, submits waiting on room
    # that only submits can free). In-flight bytes are bounded upstream by
    # the main loop's 85% backpressure + post-settle deletes.
    wait_for_room(256 * 1024 * 1024)  # response + headroom
    dur = ffprobe_duration(prep["part"])
    cost = round(sl.commit_cost(dur, prep["in_ch"]), 4)
    kt = keyterms_for(title, topic)
    sha = ps.sha256_file(prep["part"])
    # release of the same part (compare-and-set is per id). Receipt keeps p00.
    st_path = os.path.join(udir, "state.json")
    if not os.path.exists(st_path):
        ps.admit(udir, "p00")  # never clobber existing state on resume
        trial, n = f"{h}-p00-a1", 1
        st = ps.read_json(st_path)
        st["submit_attempts"] = 1
        ps.atomic_write_json(st_path, st)
    else:
        v, _ = ps.recover(udir)
        st = ps.read_json(st_path)
        n = int(st.get("submit_attempts", 0)) + 1
        trial = f"{h}-p00-a{n}"
        if v == ps.RESERVED:
            old = ps.read_json(os.path.join(udir, "receipt.json"))
            ledger.release("primary", f"{h}-p00-a{n-1}",
                           old.get("committed_usd", 0.0))
            # falls through to reserve() below: re-reserve + resubmit, no spend
            st["status"] = ps.QUEUED
        st["submit_attempts"] = n
        ps.atomic_write_json(st_path, st)
    ledger.commit("primary", trial, cost)
    ps.reserve(udir, "p00", cost, sha,
               {"model": "nova-3", "diarize": True, "keyterms": kt}, prep["in_ch"])
    sent_ts = time.time()
    ps.mark_sent(udir, extras={"sent_ts": sent_ts, "transport": "sync"})
    url = sub.build_url(True, keyterms=kt)
    acct, key = "primary", keys["primary"]
    try:
        status, complete, opened = sub.post_file(
            url, key, prep["part"], os.path.join(udir, "response-part-00.json"))
    except sub.PaidUnknown as e:
        ps.settle(udir, None, False)
        return {"handle": h, "outcome": "PAID_UNKNOWN", "note": str(e)}
    if status == 402:
        if "secondary" not in keys:
            ps.settle(udir, 402, False)
            return {"handle": h, "outcome": "WALLET_NEEDED"}
        ledger.release("primary", trial, cost)
        cost2 = cost
        ledger.commit("secondary", trial + "-sec", cost2)
        acct, key = "secondary", keys["secondary"]
        status, complete, opened = sub.post_file(
            url, key, prep["part"], os.path.join(udir, "response-part-00.json"))
    if status == 429:
        time.sleep(2)
        status, complete, opened = sub.post_file(
            url, key, prep["part"], os.path.join(udir, "response-part-00.json"))
    obj = json.load(open(os.path.join(udir, "response-part-00.json"), encoding="utf-8"))
    sub.check_arrival(obj)
    md = obj["metadata"]["duration"]
    actual = round((md / 60.0) * sl.RATE * prep["in_ch"]
                   + (md / 60.0) * sl.KEYTERM_RATE * prep["in_ch"] * (1 if kt else 0), 4)
    st, action = ps.settle(udir, status, complete,
                           extras={"transport": "sync", "socket_open_ts": opened,
                                   "account": acct, "keyterms_sent": kt,
                                   "metadata_duration": md,
                                   "settle_quantity": round(md * prep["in_ch"], 3)})
    ledger.settle(acct, cost, actual)
    utts = obj["results"]["utterances"]
    gi = {"handle": h, "d_response": md, "d_decoded": dur,
          "d_manifest": prep["dur_declared"], "n_utterances": len(utts),
          "first_start": utts[0]["start"], "last_end": utts[-1]["end"],
          "words": sum(len(u.get("transcript", "").split()) for u in utts)}
    json.dump(gi, open(os.path.join(udir, "gate-inputs.json"), "w"))
    # Mirror small files to the root disk after settle: loopback wipes must
    # never again take receipts (live 2026-10-16: 2 settles wiped, $2.69
    # re-billed). Responses stay on the loopback (assembly runs there).
    mirror = os.path.join(BASE, "out", "units-mirror", prep["unit"])
    os.makedirs(mirror, exist_ok=True)
    for f in ("receipt.json", "gate-inputs.json", "state.json"):
        src = os.path.join(udir, f)
        if os.path.exists(src):
            with open(src, "rb") as fh:
                data = fh.read()
            with open(os.path.join(mirror, f), "wb") as fh:
                fh.write(data)
    # Responses live on the MIRROR (root disk): assembly reads them there.
    # The loopback keeps only in-flight bytes; settled responses are moved
    # off (size-verified) the moment they land. Live 2026-10-16: 135
    # responses (~1 GB) pruned mid-run to unstick a 100% loopback.
    rpath = os.path.join(udir, "response-part-00.json")
    rdest = os.path.join(mirror, "response-part-00.json")
    if os.path.exists(rpath):
        with open(rpath, "rb") as fh:
            rdata = fh.read()
        with open(rdest, "wb") as fh:
            fh.write(rdata)
        if os.path.getsize(rdest) == len(rdata):
            os.remove(rpath)
    # Post-settle disk assertion: deleting parts must grow free room.
    before = work_free_bytes()
    for f in os.listdir(udir):
        if f.startswith("part-00") and f.endswith(".mka"):
            os.remove(os.path.join(udir, f))
    if work_free_bytes() < before:
        raise RuntimeError(f"{h}: post-settle disk did not grow (overrun)")
    return {"handle": h, "outcome": st, "account": acct, "actual": actual,
            "server_words": gi["words"]}


def disk_used_pct():
    import shutil
    u = shutil.disk_usage(UNITS)
    return u.used / (u.used + u.free)


def reap_done(futs, log, ledger=None):
    done = [f for f in futs if f.done()]
    for f in done:
        p = futs.pop(f)
        try:
            out = f.result()
        except Exception as e:
            out = {"handle": p["handle"], "outcome": "ERROR", "note": str(e)[:300]}
            # A commit may have landed with no receipt update (kill/ENOSPC
            # mid-submit): memorialize the receipt's committed_usd so rescan
            # can tell stranded-but-possibly-spent from a real leak.
            if ledger is not None:
                try:
                    rp = os.path.join(UNITS, p["unit"], "receipt.json")
                    stp = os.path.join(UNITS, p["unit"], "state.json")
                    if os.path.exists(rp):
                        r = json.load(open(rp, encoding="utf-8"))
                        n = json.load(open(stp, encoding="utf-8")).get("submit_attempts", 1) \
                            if os.path.exists(stp) else 1
                        ledger.note_commitment(
                            "primary", r.get("committed_usd", 0.0),
                            f"{p['handle']}-p00-a{n}: submit_one exception post-commit")
                except Exception:
                    pass
        log.write(json.dumps(out) + "\n")
        log.flush()
        print(json.dumps(out), flush=True)
    return len(done)


def main():
    block = sys.argv[1] if len(sys.argv) > 1 else "lpt16"
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    rows = [r for r in csv.DictReader(open(os.path.join(BASE, "worklist", "targets.csv")))
            if r["block"] == block and r["kind"] == "audio"]
    sf = json.load(open(os.path.join(BASE, "out", "scope-final.json")))
    surl = {r["handle"]: r["url"] for r in sf["targets"]}
    for r in rows:
        r["url"] = surl[r["handle"]]
    print(f"block={block} audio_units={len(rows)}", flush=True)
    keys = {"primary": open("/tmp/dg.key", encoding="utf-8").read().strip()}
    if os.path.exists("/tmp/dg2.key"):
        keys["secondary"] = open("/tmp/dg2.key", encoding="utf-8").read().strip()
    ledger = sl.Ledger()
    remux_sem = threading.Semaphore(2)
    log_path = os.path.join(BASE, "out", f"bulk-{block}.jsonl")
    titles = {}
    try:
        mf = json.load(open(os.path.join(BASE, "out", "manifest-v3.json")))
        for u in mf["units"]:
            titles[u["media"]["handle"]] = (u.get("title", ""), u.get("topic", ""))
    except Exception:
        pass
    # INTERLEAVED: prep one unit, hand to the pool immediately, backpressure
    # on pool depth AND disk use. Two-phase (all preps then all submits)
    # overflows the loopback: sources+parts accumulate with no drain.
    with open(log_path, "a", encoding="utf-8") as log:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futs = {}
            for row in rows:
                if row["dur_s"] == "unknown":
                    print(f"SKIP unknown-duration {row['handle']}", flush=True)
                    continue
                while len(futs) >= workers or disk_used_pct() > 0.85:
                    reap_done(futs, log, ledger)
                    time.sleep(10)
                try:
                    prep = process_unit(row, keys, ledger, remux_sem, log_path)
                except Exception as e:
                    raw = getattr(e, "stderr", "") or ""
                    err = raw.decode(errors="replace")[-300:] if isinstance(raw, bytes) else str(raw)[-300:]
                    print(json.dumps({"handle": row["handle"], "outcome": "PREP_ERROR",
                                      "note": (str(e)[:200] + " | " + err)}), flush=True)
                    continue
                if "part" not in prep:
                    print(json.dumps(prep), flush=True)
                    continue
                futs[pool.submit(submit_one, prep, keys, ledger,
                                 *titles.get(prep["handle"], ("", "")))] = prep
            while futs:
                reap_done(futs, log, ledger)
                time.sleep(10)
    print("LEDGER " + json.dumps(ledger.totals()), flush=True)


if __name__ == "__main__":
    main()
