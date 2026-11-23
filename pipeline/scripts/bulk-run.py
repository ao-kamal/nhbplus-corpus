#!/usr/bin/env python3
"""Batch-2 bulk runner: fetch -> remux -> channels -> submit -> settle.
Adapted from corpus-1 bulk-run.py. Reads worklist/batch2-targets.csv.
Resources ship as NATIVE attachments (no md conversion). AI Summary excluded.
No hard stop; both Deepgram keys used with sequential 402 failover.
"""
import csv, importlib.util, json, os, re, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

BASE = "/home/azureuser/nhbplus-work"
SCR = os.path.join(BASE, "scripts")
OUT = os.path.join(BASE, "out")
UNITS = os.path.join(BASE, "units")
FETCH = os.path.join(BASE, "fetch")
WL = os.path.join(BASE, "worklist", "batch2-targets.csv")
os.environ["SPEND_LEDGER"] = os.path.join(BASE, "_meta", "spend.json")
FETCH_SEM = threading.Semaphore(2)   # disk guard: 2 x 2.7G on 10G loopback
REMUX_SEM = threading.Semaphore(2)

def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SCR, name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

fp = load("fetch-pool"); ch = load("channels"); sl = load("spend-ledger")
ps = load("part-state"); sub = load("submit")

def sh(cmd, **kw):
    kw.setdefault("stdin", subprocess.DEVNULL)
    return subprocess.run(cmd, **kw)

def probe_channels(part):
    n = fp.ffprobe_channels(part) if hasattr(fp, "ffprobe_channels") else None
    if n is None:
        r = sh(["ffprobe","-v","error","-select_streams","a:0","-show_entries","stream=channels",
                "-of","default=nw=1:nk=1",part], capture_output=True, text=True, check=True)
        n = int(r.stdout.strip())
    if n == 1: return ch.classify(1)
    def lvl(f):
        r = sh(ch.measure_argv(part, f), capture_output=True, text=True, check=True)
        return ch.parse_rms_level_db(r.stdout + r.stderr)
    return ch.classify(2, lvl(ch.FILTER_L), lvl(ch.FILTER_R), lvl(ch.FILTER_D))

def keyterms(name):
    toks = re.findall(r"[A-Z][a-z]{2,}", name)
    seen, out = set(), []
    for t in toks:
        if t not in seen and t.lower() not in ("nhb","the","with","call","part"):
            seen.add(t); out.append(t)
    return out[:30]

def process_call(row, keys, ledger, remux_sem):
    h = row["handle"]; unit = "b2-" + h
    udir = os.path.join(UNITS, unit); os.makedirs(udir, exist_ok=True)
    verdict, _ = ps.recover(udir)
    if verdict in (ps.SETTLED, ps.LOST): return {"handle": h, "outcome": "skip-" + verdict}
    # disk admission: one call can peak ~1.1 GB (part + downmix)
    import shutil as _sh
    if _sh.disk_usage(UNITS).free < 2_900_000_000:
        return {"handle": h, "outcome": "DISK_WAIT"}
    # fetch
    fdir = fp.prepare_target_dir(FETCH, h)
    landed = None
    try: landed = fp.landed_file(fdir)
    except fp.FetchFail: pass
    if not landed:
        url = f"https://mega.nz/folder/7WZkxQjK#yc0fQSTRiV2_NXUF7XFV4Q/file/{h}"
        t0 = time.time()
        with FETCH_SEM:
            p = sh(["mega-get", url, fdir], capture_output=True, text=True)
        if p.returncode != 0: return {"handle": h, "outcome": "FETCH_FAIL", "note": p.stderr[-150:]}
        landed = fp.landed_file(fdir)
        fp.record_rate(os.path.join(OUT,"fetch-rates.jsonl"), h, os.path.getsize(landed), time.time()-t0)
    # remux
    part = os.path.join(udir, "part-00.mka")
    if not os.path.exists(part):
        with remux_sem:
            r = sh(["ffmpeg","-nostdin","-v","error","-y","-i",landed,"-vn","-c:a","copy",part],
                   capture_output=True, text=True)
            if r.returncode != 0: return {"handle": h, "outcome": "REMUX_FAIL"}
    if os.path.exists(landed): os.remove(landed)
    assert os.path.getsize(part) < 2_000_000_000, f"{h}: CAP hit"
    branch, in_ch, note = probe_channels(part)
    submit_part = part
    if branch == ch.BIT_IDENTICAL:
        mono = os.path.join(udir,"part-00-mono.mka")
        if not os.path.exists(mono):
            with remux_sem:
                sh(ch.downmix_argv(branch, part, mono), capture_output=True, check=True)
        submit_part = mono
        if os.path.exists(part): os.remove(part)  # keep only the submitted part
    elif branch == ch.DUAL_MONO:
        opus = os.path.join(udir,"part-00-opus.mka")
        if not os.path.exists(opus):
            with remux_sem:
                sh(ch.downmix_argv(branch, part, opus), capture_output=True, check=True)
        submit_part = opus
        if os.path.exists(part): os.remove(part)  # keep only the submitted part
    return {"handle": h, "unit": unit, "name": row["name"], "branch": branch,
            "in_ch": in_ch, "part": submit_part, "dur": row["dur_s"]}

def submit_call(prep, keys, ledger):
    h = prep["handle"]; udir = os.path.join(UNITS, prep["unit"])
    if not os.path.exists(os.path.join(udir,"state.json")):
        ps.admit(udir, "p00")
    else:
        v,_ = ps.recover(udir)
        st = ps.read_json(os.path.join(udir,"state.json"))
        if v in (ps.SENT, ps.PAID_UNKNOWN):
            return {"handle": h, "outcome": "PAID_UNKNOWN", "note": "resume: operator decides"}
        st["status"] = ps.QUEUED
        ps.atomic_write_json(os.path.join(udir,"state.json"), st)
    dur = prep["dur"]
    if not dur or dur == "unknown":
        r = sh(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",
                prep["part"]], capture_output=True, text=True)
        dur = r.stdout.strip()
    dur = float(dur)
    cost = round(sl.commit_cost(dur, prep["in_ch"]), 4)
    kt = keyterms(prep["name"])
    ledger.commit("primary", h+"-p00", cost)
    sha = ps.sha256_file(prep["part"])
    ps.reserve(udir, "p00", cost, sha, {"model":"nova-3","diarize":True,"keyterms":kt}, prep["in_ch"])
    ps.mark_sent(udir, extras={"sent_ts": time.time(), "transport":"sync"})
    url = sub.build_url(True, keyterms=kt)
    acct, key = "primary", keys["primary"]
    backoff = 2
    for attempt in range(6):
        try:
            status, complete, opened = sub.post_file(url, key, prep["part"],
                os.path.join(udir,"response-part-00.json"), timeout=600)
        except sub.PaidUnknown as e:
            ps.settle(udir, None, False)
            return {"handle": h, "outcome":"PAID_UNKNOWN", "note": str(e)[:120]}
        if status == 402 and acct == "primary":
            ledger.release("primary", h+"-p00", cost)
            ledger.commit("secondary", h+"-p00-sec", cost)
            acct, key = "secondary", keys["secondary"]
            continue
        if status == 429:
            time.sleep(backoff); backoff = min(60, backoff*2); continue
        if status == 400:
            continue
        break
    if status != 200:
        return {"handle": h, "outcome": f"RETRY_EXHAUSTED_{status}"}
    obj = json.load(open(os.path.join(udir,"response-part-00.json"), encoding="utf-8"))
    sub.check_arrival(obj)
    md = obj["metadata"]["duration"]
    rate = sl.RATE + (sl.KEYTERM_RATE if kt else 0.0)
    actual = round((md/60.0)*rate*prep["in_ch"], 4)
    ps.settle(udir, status, complete, extras={"transport":"sync","socket_open_ts":opened,
        "account":acct,"keyterms_sent":kt,"metadata_duration":md,
        "settle_quantity":round(md*prep["in_ch"],3)})
    ledger.settle(acct, cost, actual)
    utts = obj["results"]["utterances"]
    gi = {"handle":h,"d_response":md,"d_decoded":dur,"n_utterances":len(utts),
          "first_start":utts[0]["start"],"last_end":utts[-1]["end"],
          "words":sum(len(u.get("transcript","").split()) for u in utts)}
    json.dump(gi, open(os.path.join(udir,"gate-inputs.json"),"w"))
    # mirror small files to root disk
    mirror = os.path.join(BASE, "out", "units-mirror", prep["unit"])
    os.makedirs(mirror, exist_ok=True)
    for f in ("receipt.json","gate-inputs.json","state.json","response-part-00.json"):
        src = os.path.join(udir,f)
        if os.path.exists(src):
            with open(src,"rb") as fh: data=fh.read()
            with open(os.path.join(mirror,f),"wb") as fh: fh.write(data)
    for f in os.listdir(udir):
        if f.startswith("part-00") and f.endswith(".mka"): os.remove(os.path.join(udir,f))
    return {"handle":h,"outcome":"settled","account":acct,"actual":actual,"words":gi["words"]}

def main():
    rows = [r for r in csv.DictReader(open(WL, encoding="utf-8")) if r["kind"]=="audio"]
    only = os.environ.get("HANDLES")
    if only:
        want = set(only.split(","))
        rows = [r for r in rows if r["handle"] in want]
    sh(["mega-speedlimit", "--download-connections", "16"], capture_output=True)
    keys = {"primary":open("/home/azureuser/dg1.key").read().strip(),
            "secondary":open("/home/azureuser/dg2.key").read().strip()}
    ledger = sl.Ledger()
    remux_sem = REMUX_SEM
    logp = os.path.join(OUT,"bulk-batch2.jsonl")
    with open(logp,"a",encoding="utf-8") as log:
        with ThreadPoolExecutor(max_workers=25) as pool:
            futs = {}
            for row in rows:
                while len(futs) >= 25:
                    done = [f for f in futs if f.done()]
                    for f in done:
                        try: out = f.result()
                        except Exception as e: out={"handle":futs[f]["handle"],"outcome":"ERROR","note":str(e)[:150]}
                        log.write(json.dumps(out)+"\n"); log.flush(); print(json.dumps(out),flush=True)
                        del futs[f]
                    if futs: time.sleep(10)
                # Retry DISK_WAIT / transient failures in place; never drop a row.
                for attempt in range(30):
                    prep = process_call(row, keys, ledger, remux_sem)
                    if prep.get("outcome") != "DISK_WAIT":
                        break
                    if attempt % 5 == 0:
                        print(json.dumps({"handle":row["handle"],"outcome":"DISK_WAIT","attempt":attempt}),flush=True)
                    time.sleep(20)
                if "part" in prep:
                    futs[pool.submit(submit_call, prep, keys, ledger)] = prep
                else:
                    log.write(json.dumps(prep)+"\n"); log.flush(); print(json.dumps(prep),flush=True)
            while futs:
                done = [f for f in futs if f.done()]
                for f in done:
                    try: out = f.result()
                    except Exception as e: out={"handle":futs[f]["handle"],"outcome":"ERROR","note":str(e)[:150]}
                    log.write(json.dumps(out)+"\n"); log.flush(); print(json.dumps(out),flush=True)
                    del futs[f]
                if futs: time.sleep(10)
    print("LEDGER", json.dumps(ledger.totals()), flush=True)

if __name__ == "__main__": main()
