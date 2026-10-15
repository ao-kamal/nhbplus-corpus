# G2 — BEADS gate: PASSED

**Date:** 2026-10-15
**Artifacts:** `.beads/issues.jsonl` — 34 beads, 57 dependency edges, 0 cycles
**Driver:** `/repeatedly-apply-skill`, strictly serial, one subagent per pass

## The four exit criteria

| criterion | verdict | evidence |
|---|---|---|
| **≥4 polish rounds** via `/repeatedly-apply-skill` | **MET — six** | passes 1–6, each a fresh subagent, one mission each |
| **convergence signals present** — shrinking deltas, decelerating velocity, rising similarity | **MET** | see the table below |
| **no red flag currently active** | **MET** | no oscillation, no expansion, not a low-quality plateau |
| **dependency graph has no cycles** (`bv --robot-*`) | **MET** | `br dep cycles` ✓ **and** `bv --robot-insights` `Cycles: []`, `valid: 34`, `errors: 0` |

Six passes is above the guide's floor of 4–6 and well above the named beginner
mistake of fewer than 3.

## Convergence, measured not felt

| pass | scope | beads changed | edges | spec sections |
|---|---|---|---|---|
| 1 | lost content, both directions | 25 desc + 9 titles | 53 → 55 | 0 |
| 2 | description completeness | 34 (**one mechanical fix**) | 55 | 0 |
| 3 | gate fidelity to the formulas | **5** | 55 | **7** |
| 4 | dependency graph | 2 desc + 2 priorities | 55 → 57 | 1 |
| 5 | atomicity + priority | **0** desc, 1 priority | 57 | 0 |
| 6 | residuals + spec | 4 desc | 57 | 5 |

**The signals, in the order the reference names them:**

1. **Change velocity decelerating** — bead-graph deltas 34, 34, 5, 2, 0, 4. The
   pass-6 uptick is the final pass carrying an explicit residual list, not a
   rediscovery: every item was queued by pass 5 with its location named.
2. **Content similarity rising** — pass 6's four fixes were all the *same* shape
   (make a criterion falsifiable, or split a doubled claim), while passes 1–2
   found four distinct defect classes.
3. **Output size shrinking** — recorded as **advisory only**, for a reason decided
   before pass 1 and not quietly applied afterwards: this signal is calibrated on
   code diffs, and these are prose beads. A bead that grows because a Test Plan
   gained a mutation test is an improvement. Applying signal 3 mechanically would
   have cut the polish short at pass 3.

**No red flag active.** No oscillation — no pair of passes reverted each other.
No expansion — the bead count never grew after pass 1 added the one genuinely
missing bead. Not a plateau at low quality: pass 6 still found a bead/spec
contradiction on a headline compute figure.

## What the six passes actually caught

**Nine defects in the beads, and nine in the spec.** All verified against
artifacts before being fixed.

The highest-value of each:

- **`mp4`/V12** had replaced the spec's six clauses — including the `H(U)`
  transcript hash and the `request_id` clause — with a generic
  manifest/receipt/ledger traceability check already covered by V7, V9 and V10.
  **It cannot detect two units' transcripts being exchanged.** The spec calls V12
  "the most important gate here".
- **§11.4 V10's `committed` line** was a 60× unit slip the spec warns about
  elsewhere: `settle_from(r) * RATE` multiplies seconds by a per-minute rate. A
  3,600 s part would have committed **$20.16 instead of $0.336** and the corpus
  **$11,764.40 instead of $196.07** — the run stops after roughly ten parts. It
  also omitted `KEYTERM_RATE`, under-booking $44.81 and letting V10 pass a
  genuinely over-stop run.

And the ones that were **mine, this session**:

- `r0k`/V11 asserted *"11 of 11 spot-checks differed while 256 matched on
  length"* and *"256 of 267 files"*. **Neither figure exists.** The artifact
  records `PASS - 11 of 11` and `PASS - scp -r is byte-exact` over 5 files. I
  fabricated numbers into a bead and attributed them to an artifact, and the claim
  was the **opposite** of what it records.
- The STT-stage figure was wrong **four times** before it was right: `15.5 hours`
  (the 60× slip), `6.8 minutes` (dropped the /25), `15.46 minutes` (right shape,
  wrong quotient — and the spec's own formula yields 16.043, not 15.46), and
  `8.7 minutes`. **Now 16.40 MINUTES**, derived, with the 1.022× measured 25-way
  degradation included, and all four wrong values recorded so the fifth reader
  does not invent a fifth.

## The infrastructure defect that cost six recoveries

`frankensqlite`'s WAL-index recovery is unsupported on Windows; every mutation
eventually wedged the DB. **None of the seven skill troubleshooting surfaces
document this failure** — not one mentions frankensqlite, WAL-index quarantine or
`SYNC_CONFLICT`.

Fixed, not worked around: **`br --no-db`**, verified for reads and writes, with
the authority direction inverted and the `br sync` hazard recorded in `AGENTS.md`.
Pass 5 correctly **stopped** on the sixth failure and left the destructive
recovery to the operator rather than running `br init` blind a seventh time.

## What G2 does not claim

- **`uff`, `7w7` and every gate are UNEVALUABLE** until code exists. A
  specification is not an implementation. Stage 3's first executable act is to
  make them evaluable.
- **13 pre-existing malformed table blocks** in the spec (escaped pipes) are
  unchanged at HEAD and now; the polish added none. A renderer pass is Stage 3's.
- **Four operator decisions remain open** and are enumerated in §15 as O1–O4:
  the `00 Topics.md` content decision, the corpus-wide stereo census, Azure
  VM-days for a 16-way run, and decoded-vs-header durations.

## Final verified state

```
34 beads · 57 edges · 0 cycles   (br dep cycles AND bv --robot-insights)
br lint: 0 warnings · all 34 carry all six sections
P0=19  P1=12  P2=3
spec 2,766 lines, fences balanced, 0 U+FFFD
```
