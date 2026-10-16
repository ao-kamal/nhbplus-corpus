#!/usr/bin/env python3
"""Rebuild the ledger from receipts; receipts win every conflict (bead md5).

Walks unit receipt.json files (WORK loopback tree + BASE smoke tree),
recomputes per-account committed/settled/lost/released, and compares against
the live ledger. Memorials (write_downs, commitments) explain the rest:
kill-cost commits and wiped ghost settles have no receipts by construction.
Exit 0 iff every unexplained diff <= $0.01. Never overwrites the live ledger;
--apply writes the rebuilt file alongside for inspection.
"""
import glob
import json
import os
import sys

HOME = os.path.expanduser("~")
BASE = os.path.join(HOME, "nhbplus")
WORK = os.environ.get("NHBPLUS_WORK", BASE)
LEDGER = os.path.join(BASE, "_meta", "spend.json")
RATE = 0.0043
KEYTERM_RATE = 0.0013


def settle_usd(receipt, md, channels, keyterms):
    rate = RATE + (KEYTERM_RATE if keyterms else 0.0)
    return round((md / 60.0) * rate * channels, 4)


def main():
    apply = "--apply" in sys.argv
    trees = [os.path.join(WORK, "units"), os.path.join(BASE, "units")]
    rec = {}
    n = 0
    for tree in trees:
        for rp in glob.glob(os.path.join(tree, "*", "receipt.json")):
            r = json.load(open(rp, encoding="utf-8"))
            aid = r.get("account", "primary")
            a = rec.setdefault(aid, {"committed": 0.0, "settled": 0.0,
                                     "lost": 0.0, "released": 0.0})
            n += 1
            st = r.get("status")
            c = r.get("committed_usd", 0.0)
            if st in ("reserved", "sent"):
                a["committed"] += c
            elif st == "settled":
                md = r.get("metadata_duration")
                if md is not None:
                    a["settled"] += settle_usd(r, md, r.get("input_channel_count", 1),
                                               r.get("keyterms_sent"))
                else:
                    a["settled"] += c  # pre-V10-field receipt: commit as proxy
            elif st == "lost":
                a["lost"] += c
    live = json.load(open(LEDGER, encoding="utf-8"))
    diffs = {}
    ok = True
    for aid, a in rec.items():
        la = live["accounts"].get(aid, {})
        for k in ("settled", "lost", "released"):
            d = round(a[k] - la.get(k, 0.0), 4)
            if abs(d) > 0.01:
                ok = False
            diffs[f"{aid}.{k}"] = d
    # committed: live also holds receipt-less kill-cost; memorials explain it.
    memorial = sum(c["amount"] for c in live.get("commitments", []))
    rescan_comm = round(sum(a["committed"] for a in rec.values()), 4)
    live_comm = live["totals"]["committed"]
    unexplained = round(live_comm - rescan_comm - memorial, 4)
    diffs["committed_unexplained"] = unexplained
    if abs(unexplained) > 0.01:
        ok = False
    # dead/write_downs are memorial-only: reported, never recomputed.
    diffs["dead_memorial"] = live["totals"].get("dead", 0.0)
    out = {"receipts": n, "diffs": diffs, "verdict": "PASS" if ok else "FAIL"}
    print(json.dumps(out, indent=1))
    if apply:
        open(os.path.join(BASE, "out", "rescan-rebuilt.json"), "w").write(
            json.dumps({"accounts": rec, "memorials": {
                "commitments": live.get("commitments", []),
                "write_downs": live.get("write_downs", [])}}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
