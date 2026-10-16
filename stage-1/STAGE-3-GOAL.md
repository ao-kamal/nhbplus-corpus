# STAGE 3 — EXECUTE: completion condition (the goal)

**Set:** 2026-10-16, entering Stage 3 with G2 passed.
**Lane:** SOLO — one session, claiming beads in `bv --robot-*` priority order.

## Why solo, recorded so it is not re-litigated

The flywheel skill calls the swarm lane primary for multi-day builds. This is
neither multi-day nor coordination-bound. It is **~3 h of wall-clock, 95% of it
network**, and the binding constraints are physical:

- one VM with a **4 GiB loopback** (W0-Cap proved ENOSPC in 0 s)
- one network link measured at **15.8 MB/s**
- one Deepgram account with a **25-concurrency ceiling**, and a second key that is
  a **wallet, not a worker** (self-serve secondary projects are single-stream by
  design, and these setups are detected)

More agents contending for the same disk, the same link and the same 25 streams
buys contention, not parallelism. The swarm lane's advantage — parallel work
selection — does not exist when the bottleneck is a single fetch pipe.

## THE COMPLETION CONDITION

Stage 3 is done when **all seven** of these hold. Any one missing means Stage 3 is
open, regardless of how much code exists.

1. **`vault/` holds ≥344 markdown notes** at exactly the paths in
   `clean-names.json`, and no non-markdown byte anywhere under it.
2. **`nhbplus-source-documents.zip` exists beside `vault/`** with 109 members whose
   sha256s match `manifest.json`, and every document-derived note carries a source
   line naming its member. (§0.0.1)
3. **All 14 gates V0–V13 pass on real artifacts**, each with a non-vacuity
   assertion that FIRES. A gate that passes vacuously is not a pass. **V2 is
   expected to report `NON_VACUOUS false`** — the largest part is 385 MiB against
   a 2,000 MiB cap — and that honest red is the required output, not a failure.
4. **`_meta/AUDIT.md` has 235 lines**, one per audio unit, and
   `copy-verification.json` matches per-file SHA-256, byte count and the 11
   typography samples. A run that cannot produce these does not reach teardown.
5. **Spend is ≤ `$213.48`**, derived from receipts with the same `COMMIT_COST` the
   submission path uses, and the two cost lines (STT spend **and** Azure VM-days)
   are both present in the report.
6. **V6 ran on the VM source tree BEFORE the copy to the PC.** A post-copy V6
   reports a Constraint 1 violation that has already happened.
7. **The VM is destroyed and both Deepgram keys are shredded**, only after
   verification — and the `~335 GB` import in the operator's personal MEGA account
   is left alone; only the operator can delete it.

## The order, and why it is not negotiable

§9 and §12 both say the ordering is load-bearing. Encoded in the graph:

```
documents first (free end-to-end shakedown, no STT dollar spent)
  -> one lesson-sized smoke test
  -> then the 16 longest audio units
  -> then the remaining 191
```

The documents-first rule exists because a free end-to-end shakedown catches
assembly and egress bugs before any dollar is spent. **Skipping it to "save time"
spends money to learn the same thing.**

## Stop conditions — no others are valid

| condition | evidence | action |
|---|---|---|
| A gate cannot be made to fail | a mutation test that still passes | **stop, report** — the gate is decoration |
| Spend crosses `$213.48` | ledger total from receipts | **stop**, do not re-derive |
| `PAID_UNKNOWN` appears | a `sent` part with no response | **stop, never auto-resubmit**, operator decides |
| A bead's gate has no formula | the spec's §11.3/§11.4 | **stop** — that was the defect that cost G1 |
| `br` wedges the DB | `SYNC_CONFLICT` | `br --no-db`, never `br sync`, never recover the DB |
| All seven conditions hold | the checks above | G3 |

## What Stage 3 does NOT decide

O2–O4 (stereo share, Azure VM-days, decoded-vs-header durations) **convert by
running**, under the ordering above. They are not open decisions and do not block
entry — they are measurements the run produces.
