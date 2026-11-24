#!/usr/bin/env python3
"""Batch-2 final pass, v2. Concurrent STT, disk-aware serial prep.

Fixes over bulk-final.py:
  * reaping threshold now equals worker count (was 25 while pool was 1/12,
    which pre-built parts far ahead of workers and filled the loopback)
  * commit/release use a per-account part_id so the ledger's CAS release
    is not consumed by an earlier failover hop
  * every non-settle outcome releases its commit (no stranded committed $)
  * 400 is bounded, not retried 6x against the same bad request
  * 1800 s submit timeout (600 s caused PAID_UNKNOWN on GB-scale uploads)
"""
import importlib.util, os, csv, glob, json, time, shutil, traceback
from concurrent.futures import ThreadPoolExecutor

SCR = "/home/azureuser/nhbplus-work/scripts"
spec = importlib.util.spec_from_file_location("bf", os.path.join(SCR, "bulk-final.py"))
bf = importlib.util.module_from_spec(spec); spec.loader.exec_module(bf)
sl, ps, sub, log, UNITS, WL = bf.sl, bf.ps, bf.sub, bf.log, bf.UNITS, bf.WL

WORKERS = sub.TRANSCRIBE_CONCURRENCY  # single source of truth with submit.py
DISK_FLOOR = 4_000_000_000
MAX_PASSES = 2


def submit2(prep, keys, ledger):
    h, unit = prep["handle"], prep["unit"]
    udir = os.path.join(UNITS, unit)
    if not os.path.exists(os.path.join(udir, "state.json")):
        ps.admit(udir, "p00")
    dur = prep["dur"]
    if not dur or dur == "unknown":
        dur = bf.sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=nw=1:nk=1", prep["part"]],
                    capture_output=True, text=True).stdout.strip()
    dur = float(dur)
    cost = round(sl.commit_cost(dur, prep["in_ch"]), 4)
    kt = bf.kterms(prep["name"])
    sha = ps.sha256_file(prep["part"])
    ps.reserve(udir, "p00", cost, sha,
               {"model": "nova-3", "diarize": True, "keyterms": kt}, prep["in_ch"])
    ps.mark_sent(udir, extras={"sent_ts": time.time(), "transport": "sync"})
    url = sub.build_url(True, keyterms=kt)
    chain = ["primary", "secondary", "tertiary"]
    acct = chain[0]
    ledger.commit(acct, h + "-p00-" + acct, cost)
    status = None
    retry_400 = 0
    for i, acct in enumerate(chain):
        if i:
            ledger.commit(acct, h + "-p00-" + acct, cost)
        key = keys[acct]
        try:
            status, complete, _ = sub.post_file(
                url, key, prep["part"], os.path.join(udir, "response-part-00.json"),
                timeout=1800)
        except sub.PaidUnknown:
            ledger.release(acct, h + "-p00-" + acct, cost)
            ps.settle(udir, None, False)
            return {"handle": h, "outcome": "PAID_UNKNOWN"}
        if status == 402:
            ledger.release(acct, h + "-p00-" + acct, cost)
            continue
        if status == 429:
            time.sleep(30)
            continue
        if status == 400:
            retry_400 += 1
            if retry_400 > 1:
                ledger.release(acct, h + "-p00-" + acct, cost)
                return {"handle": h, "outcome": "HTTP_400"}
            continue
        break
    if status != 200:
        ledger.release(acct, h + "-p00-" + acct, cost)
        return {"handle": h, "outcome": "HTTP_%s" % status}
    obj = json.load(open(os.path.join(udir, "response-part-00.json"), encoding="utf-8"))
    sub.check_arrival(obj)
    md = obj["metadata"]["duration"]
    actual = round((md / 60.0) * (sl.RATE + (sl.KEYTERM_RATE if kt else 0.0)) * prep["in_ch"], 4)
    ps.settle(udir, status, complete, extras={
        "transport": "sync", "account": acct, "metadata_duration": md,
        "settle_quantity": round(md * prep["in_ch"], 3)})
    ledger.settle(acct, cost, actual, part_id=h + "-p00-" + acct)
    utts = obj["results"]["utterances"]
    gi = {"handle": h, "d_response": md, "d_decoded": dur,
          "n_utterances": len(utts), "first_start": utts[0]["start"],
          "last_end": utts[-1]["end"],
          "words": sum(len(u.get("transcript", "").split()) for u in utts)}
    json.dump(gi, open(os.path.join(udir, "gate-inputs.json"), "w"))
    mirror = os.path.join(bf.BASE, "out", "units-mirror", unit)
    os.makedirs(mirror, exist_ok=True)
    for f in ("receipt.json", "gate-inputs.json", "state.json", "response-part-00.json"):
        p = os.path.join(udir, f)
        if os.path.exists(p):
            with open(p, "rb") as fh: data = fh.read()
            with open(os.path.join(mirror, f), "wb") as fh: fh.write(data)
    for f in os.listdir(udir):
        if f.startswith("part-00") and f.endswith(".mka"):
            os.remove(os.path.join(udir, f))
    return {"handle": h, "outcome": "settled", "account": acct,
            "actual": actual, "words": gi["words"]}


def main():
    sh = bf.sh
    sh(["mega-speedlimit", "--download-connections", "16"], capture_output=True)
    keys = {"primary": open("/home/azureuser/dg1.key").read().strip(),
            "secondary": open("/home/azureuser/dg2.key").read().strip(),
            "tertiary": open("/home/azureuser/dg3.key").read().strip()}
    ledger = sl.Ledger(); settled = bf.settled_handles()
    # Any paid-but-unsettled attempt from an earlier pass is booked as lost
    # and reset, so this pass re-fetches it cleanly instead of reusing a sent
    # state (which made ps.reserve refuse with "reserve from sent").
    for d in glob.glob(os.path.join(UNITS, "b2-*")):
        h = os.path.basename(d)[3:]
        rp = os.path.join(d, "receipt.json")
        if not os.path.exists(rp): continue
        try: rr = json.load(open(rp))
        except Exception: continue
        if rr.get("status") == "settled": continue
        c = rr.get("committed_usd", 0) or 0
        if c:
            ledger.mark_lost("tertiary", c, c,
                             part_id=str(rr.get("sent_ts", h)))
            log({"handle": h, "outcome": "committed_marked_lost", "amount": c})
        for fn in ("state.json", "receipt.json", "response-part-00.json",
                   "response-part-00.json.partial", "gate-inputs.json"):
            q = os.path.join(d, fn)
            if os.path.exists(q): os.remove(q)
        settled.discard(h)
    rows = [r for r in csv.DictReader(open(WL, encoding="utf-8"))
            if r["kind"] == "audio" and r["handle"] not in settled]
    log({"event": "start", "remaining": len(rows), "already_settled": len(settled),
         "workers": WORKERS})
    done_n = 0
    pending = list(rows)
    retryable = {"FETCH_FAIL", "PREP_ERROR", "REMUX_FAIL", "ERROR", "HTTP_400"}
    for pass_no in range(1, MAX_PASSES + 1):
        if not pending:
            break
        if pass_no > 1:
            log({"event": "retry_pass", "pass": pass_no, "remaining": len(pending)})
        next_pending = []
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futs = {}
            by_handle = {r["handle"]: r for r in pending}
            def reap(wait):
                if not futs:
                    return
                if wait:
                    from concurrent.futures import FIRST_COMPLETED, wait as cwait
                    cwait(list(futs), return_when=FIRST_COMPLETED, timeout=60)
                ready = [f for f in futs if f.done()]
                for f in ready:
                    try: out = f.result()
                    except Exception as e:
                        out = {"handle": futs[f], "outcome": "ERROR",
                               "note": str(e)[:200]}
                    log(out); del futs[f]; done_n += 1
                    if (out.get("outcome") in retryable and
                            out["handle"] in by_handle):
                        next_pending.append(by_handle[out["handle"]])
            for row in pending:
                if len(futs) >= WORKERS:
                    reap(False)
                while len(futs) >= WORKERS:
                    reap(True)
                while shutil.disk_usage(UNITS).free < DISK_FLOOR:
                    reap(False)  # report completions while waiting for disk
                    time.sleep(20)
                try:
                    prep = bf.process(row, keys, ledger)
                except Exception as e:
                    log({"handle": row["handle"], "outcome": "PREP_ERROR",
                         "note": str(e)[:200]})
                    next_pending.append(row); continue
                if "part" not in prep:
                    log(prep); next_pending.append(row); continue
                futs[pool.submit(submit2, prep, keys, ledger)] = prep["handle"]
            reap(True)
            while futs:
                reap(True)
        pending = next_pending
    if pending:
        log({"event": "unresolved", "handles": [r["handle"] for r in pending]})
    log({"event": "done", "processed": done_n, "ledger": ledger.totals()})


if __name__ == "__main__":
    try: main()
    except Exception:
        log({"event": "FATAL", "trace": traceback.format_exc()[:1200]}); raise
