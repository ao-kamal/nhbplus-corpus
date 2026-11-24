#!/usr/bin/env python3
"""Robust batch-2 runner: skip settled at row level, log all exceptions."""
import csv, importlib.util, json, os, re, subprocess, sys, threading, time, glob, traceback
from concurrent.futures import ThreadPoolExecutor

BASE = "/home/azureuser/nhbplus-work"
SCR = os.path.join(BASE, "scripts"); OUT = os.path.join(BASE, "out")
UNITS = os.path.join(BASE, "units"); FETCH = os.path.join(BASE, "fetch")
WL = os.path.join(BASE, "worklist", "batch2-targets.csv")
os.environ["SPEND_LEDGER"] = os.path.join(BASE, "_meta", "spend.json")
FETCH_SEM = threading.Semaphore(2); REMUX_SEM = threading.Semaphore(2)
LOG = os.path.join(OUT, "bulk-final.log")

def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(SCR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
fp=load("fetch-pool"); ch=load("channels"); sl=load("spend-ledger")
ps=load("part-state"); sub=load("submit")

def log(r):
    with open(LOG,"a",encoding="utf-8") as f: f.write(json.dumps(r)+"\n")
    print(json.dumps(r), flush=True)

def sh(c, **kw):
    kw.setdefault("stdin", subprocess.DEVNULL)
    return subprocess.run(c, **kw)

def settled_handles():
    s=set()
    for f in glob.glob(os.path.join(UNITS,"*","receipt.json")):
        try:
            r=json.load(open(f))
            if r.get("status") in ("settled","lost"): s.add(os.path.basename(os.path.dirname(f))[3:])
        except Exception: pass
    return s

def probe_ch(part):
    n=int(sh(["ffprobe","-v","error","-select_streams","a:0","-show_entries",
              "stream=channels","-of","default=nw=1:nk=1",part],
             capture_output=True,text=True,check=True).stdout.strip())
    if n==1: return ch.classify(1)
    def lvl(f):
        r=sh(ch.measure_argv(part,f),capture_output=True,text=True,check=True)
        return ch.parse_rms_level_db(r.stdout+r.stderr)
    return ch.classify(2,lvl(ch.FILTER_L),lvl(ch.FILTER_R),lvl(ch.FILTER_D))

def kterms(name):
    out=[]; seen=set()
    for t in re.findall(r"[A-Z][a-z]{2,}",name):
        if t not in seen and t.lower() not in ("nhb","the","with","call","part","vsl"):
            seen.add(t); out.append(t)
    return out[:30]

def process(row, keys, ledger):
    h=row["handle"]; unit="b2-"+h; udir=os.path.join(UNITS,unit)
    os.makedirs(udir,exist_ok=True)
    fdir=fp.prepare_target_dir(FETCH,h); landed=None
    try: landed=fp.landed_file(fdir)
    except fp.FetchFail: pass
    if not landed:
        url=f"https://mega.nz/folder/7WZkxQjK#yc0fQSTRiV2_NXUF7XFV4Q/file/{h}"
        with FETCH_SEM:
            p=sh(["mega-get",url,fdir],capture_output=True,text=True,timeout=900)
        if p.returncode!=0: return {"handle":h,"outcome":"FETCH_FAIL"}
        landed=fp.landed_file(fdir)
    part=os.path.join(udir,"part-00.mka")
    if not os.path.exists(part):
        with REMUX_SEM:
            r=sh(["ffmpeg","-nostdin","-v","error","-y","-i",landed,"-vn","-c:a","copy",part],
                 capture_output=True,text=True)
        if r.returncode!=0: return {"handle":h,"outcome":"REMUX_FAIL"}
    if os.path.exists(landed): os.remove(landed)
    branch,in_ch,_=probe_ch(part); submit_part=part
    if branch==ch.BIT_IDENTICAL:
        mono=os.path.join(udir,"part-00-mono.mka")
        if not os.path.exists(mono):
            with REMUX_SEM: sh(ch.downmix_argv(branch,part,mono),capture_output=True,check=True)
        submit_part=mono; os.remove(part)
    elif branch==ch.DUAL_MONO:
        opus=os.path.join(udir,"part-00-opus.mka")
        if not os.path.exists(opus):
            with REMUX_SEM: sh(ch.downmix_argv(branch,part,opus),capture_output=True,check=True)
        submit_part=opus; os.remove(part)
    return {"handle":h,"unit":unit,"name":row["name"],"branch":branch,
            "in_ch":in_ch,"part":submit_part,"dur":row["dur_s"]}

def submit(prep,keys,ledger):
    h=prep["handle"]; unit=prep["unit"]; udir=os.path.join(UNITS,unit)
    if not os.path.exists(os.path.join(udir,"state.json")): ps.admit(udir,"p00")
    dur=prep["dur"]
    if not dur or dur=="unknown":
        dur=sh(["ffprobe","-v","error","-show_entries","format=duration","-of",
                "default=nw=1:nk=1",prep["part"]],capture_output=True,text=True).stdout.strip()
    dur=float(dur); cost=round(sl.commit_cost(dur,prep["in_ch"]),4)
    kt=kterms(prep["name"])
    ledger.commit("primary",h+"-p00",cost)
    sha=ps.sha256_file(prep["part"])
    ps.reserve(udir,"p00",cost,sha,{"model":"nova-3","diarize":True,"keyterms":kt},prep["in_ch"])
    ps.mark_sent(udir,extras={"sent_ts":time.time(),"transport":"sync"})
    url=sub.build_url(True,keyterms=kt); acct,key="primary",keys["primary"]
    for attempt in range(6):
        try: status,complete,opened=sub.post_file(url,key,prep["part"],
              os.path.join(udir,"response-part-00.json"),timeout=600)
        except sub.PaidUnknown as e:
            ps.settle(udir,None,False); return {"handle":h,"outcome":"PAID_UNKNOWN"}
        if status==402 and acct=="primary":
            ledger.release("primary",h+"-p00",cost); ledger.commit("secondary",h+"-p00",cost)
            acct,key="secondary",keys["secondary"]; continue
        if status==429: time.sleep(min(60,2**attempt)); continue
        if status==400: continue
        break
    if status!=200: return {"handle":h,"outcome":f"HTTP_{status}"}
    obj=json.load(open(os.path.join(udir,"response-part-00.json"),encoding="utf-8"))
    sub.check_arrival(obj); md=obj["metadata"]["duration"]
    rate=sl.RATE+(sl.KEYTERM_RATE if kt else 0.0)
    actual=round((md/60.0)*rate*prep["in_ch"],4)
    ps.settle(udir,status,complete,extras={"transport":"sync","account":acct,
        "metadata_duration":md,"settle_quantity":round(md*prep["in_ch"],3)})
    ledger.settle(acct,cost,actual)
    utts=obj["results"]["utterances"]
    gi={"handle":h,"d_response":md,"d_decoded":dur,"n_utterances":len(utts),
        "first_start":utts[0]["start"],"last_end":utts[-1]["end"],
        "words":sum(len(u.get("transcript","").split()) for u in utts)}
    json.dump(gi,open(os.path.join(udir,"gate-inputs.json"),"w"))
    mirror=os.path.join(BASE,"out","units-mirror",unit); os.makedirs(mirror,exist_ok=True)
    for f in ("receipt.json","gate-inputs.json","state.json","response-part-00.json"):
        p=os.path.join(udir,f)
        if os.path.exists(p):
            with open(p,"rb") as fh: data=fh.read()
            with open(os.path.join(mirror,f),"wb") as fh: fh.write(data)
    for f in os.listdir(udir):
        if f.startswith("part-00") and f.endswith(".mka"): os.remove(os.path.join(udir,f))
    return {"handle":h,"outcome":"settled","account":acct,"actual":actual,"words":gi["words"]}

def main():
    sh(["mega-speedlimit","--download-connections","16"],capture_output=True)
    keys={"primary":open("/home/azureuser/dg1.key").read().strip(),
          "secondary":open("/home/azureuser/dg2.key").read().strip()}
    ledger=sl.Ledger(); settled=settled_handles()
    rows=[r for r in csv.DictReader(open(WL,encoding="utf-8"))
          if r["kind"]=="audio" and r["handle"] not in settled
          and r["handle"] not in ("qPwXRLxB","WHACUJ5J")]
    log({"event":"start","remaining":len(rows),"already_settled":len(settled)})
    with ThreadPoolExecutor(max_workers=25) as pool:
        futs={}
        for row in rows:
            while len(futs)>=25:
                done=[f for f in futs if f.done()]
                for f in done:
                    try: out=f.result()
                    except Exception as e: out={"handle":futs[f],"outcome":"ERROR","note":str(e)[:200]}
                    log(out); del futs[f]
                if futs: time.sleep(5)
            try: prep=process(row,keys,ledger)
            except Exception as e: log({"handle":row["handle"],"outcome":"PREP_ERROR","note":str(e)[:200]}); continue
            if "part" in prep: futs[pool.submit(submit,prep,keys,ledger)]=prep["handle"]
        while futs:
            done=[f for f in futs if f.done()]
            for f in done:
                try: out=f.result()
                except Exception as e: out={"handle":futs[f],"outcome":"ERROR","note":str(e)[:200]}
                log(out); del futs[f]
            if futs: time.sleep(5)
    log({"event":"done","ledger":ledger.totals()})

if __name__=="__main__":
    try: main()
    except Exception: log({"event":"FATAL","trace":traceback.format_exc()[:1000]}); sys.exit(1)
