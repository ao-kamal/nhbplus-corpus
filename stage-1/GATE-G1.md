# G1 - PLAN gate: PASSED

**Date:** 2026-10-15
**Artifact:** `stage-1/stage-1-spec.md`, 1,956 lines, executable standalone.
**Evidence:** 47 dated artifacts in `evidence/probes/`, all parsing.

## The three exit criteria

| criterion | verdict |
|---|---|
| >= 4 refinement rounds, each in a fresh conversation | **MET** - five (R1, R2 canon, R3, R4 blind, R5 blind) |
| last round's changes incremental / execution-structural, not fundamental | **MET** - see below |
| plan self-contained; an agent could execute with no other document | **MET** - see below |

## Why criterion 2 is MET despite the finding count rising

Counts: R2 = 86, R3 = 76, R4 = 94, R5 = 137 (23 blocking + 14 unevidenced
+ 28 of 66 formulas + 74 overshoot). **Volume never converged.**

Character did. R2-R4 found logic errors, contradictions and wrong rules.
**R5 found almost entirely bookkeeping**: stale figures, a missing request
payload, an unreachable branch, a table matching no artifact, an A/B
contradicting its own data.

**No round since R3 proposed a change to what the system IS.** The route is
unchanged: fetch -> remux -> submit once -> assemble -> egress, media-free, one
sync path, no spend beyond two recorded waivers. What moved was the accuracy of
the bookkeeping around a fixed design.

R5 also produced **two findings that measurement disproved** (B17: 37/37 written
hands derive from their call's name, not 1/37; and its undated-call count of 4,
where there are 2). A plan whose disagreements with a blind reviewer are about
*method* rather than about being *wrong* is a plan whose claims hold.

## Why criterion 3 is MET

The three things that made R5 return **NO - not executable** are closed:

| disqualifier | now |
|---|---|
| no request payload anywhere; `diarize=true` omission silently doubles the ceiling | section 7.2.0 carries the full POST, every flag, and what breaks without each |
| V6's floor required exactly 344 while section 10's own tree emits 346 | `>= 344`; the floor stops an empty tree, it is not a manifest |
| the 42 lesson videos budgeted nowhere - $8.79 missing | `SPEND_HARD_STOP_USD = $213.48`, lessons priced at $8.79 |

Propagation is now **computed, not typed**: `pipeline/out/PLAN-TRUTH.json` is
derived from the artifacts on every run and the spec cites it. Verified: zero
live references to 339 / 188 / 230 / 105 / 440 / $204.69 / 35,013.1 / 583.55 /
1.50 GiB / 567 core-hours remain. The only surviving occurrences of the old
146.87 GiB figure are in section 13, quoted in order to say they were wrong.

## Residual risk at G1 - carried forward, not waived

**Status as of the same day. Two items closed after the gate was declared, one
closed in the direction opposite to how it was first written down.**

1. **OPEN - the stereo census is sampled, not complete.** 65 of 191 dated calls;
   2 genuinely stereo (3.08%, 95% interval ~1.0-8.5%). `section 2.2`'s $197.68
   keep-stereo ceiling stands as the bound to hold against.

2. **IN FLIGHT - D4 keyterm (+$45.52) is UNEVIDENCED** by the only A/B on disk,
   which records zero gain and zero loss. A re-run is in progress with a
   corrected keyterm selector. **The first re-run was itself defective and its
   result was discarded**: it selected capitalised tokens with 1-3 occurrences,
   which on a transcript returns `ABSOLUTELY`, `ACTUALLY`, `AGAIN`, `ANYTHING` -
   sentence-initial adverbs, which is exactly what keyterm has nothing to offer
   on. The apparent gains it produced (`Actually 3->4`, `Altman 1->2`) were
   noise. v3 builds the stoplist from the transcript's own 150 most frequent word
   types instead. **A null result removes +$45.52 from the budget.**

3. **CLOSED - the PDF gate is closed on 50 of 50, not 49.** The document missing
   from v1 was `6. 7-Figure VSL Script Template`; the audit's hand-typed target
   list was missing the `6. ` ordinal and `if not r: continue` swallowed it. v2
   derives targets from the artifact and raises on a lookup miss.
   `evidence/probes/nhbplus-pdf-fallback-audit-v2-2026-10-15.json`.
   **The original 48 text / 2 sparse / 0 raster was right; my correction to 47
   was the error.** All three page-capped PDFs are now named, including
   `500-page-swipe-file-clayton-makepeace_compress_1` at 200/597 pages and
   20,205 words, which the completeness note had missed entirely.

4. **OPEN - 13 of 14 gates are UNEVALUABLE** because no pipeline code exists yet.
   That is the correct state at G1 and is the substance of Stage 3.

5. **CLOSED - the `attachments/` conflict** between VAULT-STRUCTURE.md and V6
   is resolved in favour of Constraint 1, which is absolute. `attachments/`
   does not ship. The same file's verbatim-vs-clean naming conflict and its
   index-note-tree conflict are resolved in the same direction. VAULT-STRUCTURE.md
   is now explicitly subordinate to the master specification, with a resolution
   table at the top of the file, and its status changed from "proposed, pending
   operator sign-off" to signed-and-superseded on those three points.

## A note on how item 3 closed

Item 3 was recorded as an open defect, then "fixed" from 48 to 47 in the wrong
direction, then found to have been right the first time. The first fix was made
on the evidence of an artifact that disagreed with itself, and the disagreement
was in the audit script rather than in the corpus. **A self-inconsistent artifact
is evidence about the script that wrote it, not about the thing it measured.**
That is now stated in section 8.1 next to the table.

## What G1 does NOT say

It does not say the plan is finished being reviewed. It says the plan is
**executable**, and that the next defect should be caught in code space where
it costs 1x rather than in plan space where it has now cost five rounds.
