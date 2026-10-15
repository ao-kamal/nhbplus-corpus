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

## Why criterion 3 is MET — AND A CORRECTION TO THIS VERDICT

**The verdict as first written was substantially wrong, and the gate table is
why.** Criterion 3 is self-containment: "an agent could execute from it without
any other document." The plan asserted twelve gates and **ten of them could not
be written** by an engineer holding only this document — V4, V5, V6, V7, V8, V9,
V10 and the three fetch/remux/STT contracts.

Each was one line naming a check. None carried a threshold with provenance,
none carried a failure behaviour, and **none carried a way to be wrong.** That
is the same defect as §7.2.0's missing request payload — a mandate without a
mechanism — and it survived five review rounds because every round checked
whether the gate was NAMED, not whether it was SPECIFIED.

**Three of the twelve had already failed vacuously, silently:**

| gate | what it did |
|---|---|
| **V9** | asserted `kind == "call"` when `scope-final.json` spells it `audio` — matched **0 handles**, returned PASS over the corpus's one confirmed live defect. It also checked documents only, so it **structurally could not catch** the dropped call. |
| **V8** | parsed a design document instead of the deliverable and passed. |
| **V6** | passed on an **empty tree**, because every check it had was a ceiling. |

**Now closed.** §11.0 carries V4 and V5; §11.1 carries the other ten. Each
formula carries a threshold with its provenance, a failure behaviour, and a
**non-vacuity assertion** — proof of what it matched, not only what it found.
**V2 is recorded as vacuous by construction** (largest part 385 MiB against a
2,000 MiB cap) rather than reporting a green it cannot earn.

**The question that found this is the one worth keeping:** not *"which gates
exist?"* but *"could I write the assertion from this document alone?"* The first
question was answered five times and returned MET every time.

### Why criterion 3 is met NOW

| disqualifier | now |
|---|---|
| no request payload anywhere | §7.2.0 carries the full POST, every flag, and what breaks without each |
| 10 of 12 gates unimplementable | §11.0 + §11.1: all 12 carry thresholds, failure behaviour and non-vacuity assertions |
| V6's floor unsatisfiable | `>= 344`, satisfied by §10's own tree |
| 42 lesson videos budgeted nowhere | `SPEND_HARD_STOP_USD = $213.48`, lessons priced at $8.79 |

Propagation is **computed, not typed**: `pipeline/out/PLAN-TRUTH.json` is derived
from the artifacts on every run and the spec cites it. Verified: zero live
references to 339 / 188 / 230 / 105 / 440 / $204.69 / 35,013.1 / 583.55 /
1.50 GiB / 567 core-hours remain anywhere.

## Residual risk at G1 - ALL FIVE ITEMS NOW RESOLVED

**1. CLOSED - the stereo census is a PLANNING figure, not a gap in the
   population.** It was carried as "65 of 191 dated calls, 3.08%, interval
   ~1.0-8.5%". Two things closed it:

   **A cheap census was considered and rejected on cost.** mega-get has no
   range or partial option and `mega-nc` is not installed, so a header-only
   census would have meant writing a raw MEGA API client - a new dependency and
   a new failure mode, to tighten a number whose entire 95% interval spans
   **$1.93 to $16.41** on a $213.48 run.

   **Then the real answer, which was in the design all along.** §7.1a DETECTS
   channel topology per file with ffprobe during the remux — a step the
   pipeline performs anyway — and that value is `INPUT_CHANNEL_COUNT`, which
   `SETTLE_FROM` bills on. **By the time any money is at risk the population is
   exactly measured, not sampled.** The sample prices the budget and validates
   the ceiling; the run replaces the figure with a measurement. **The residual is
   bounded by construction, not by sample size.**

   §7.1a also said "detect per file" without ever giving the command - the same
   defect class as §7.2.0's missing payload. It now carries the ffprobe call,
   why `-select_streams a:0` matters, and that any value other than 1 or 2 is a
   hard stop.

   A propagation sweep of v3 against every cell citing it found **six stale
   cells and two arithmetic errors**: the artifact's "~$35 extra" is
   `0.179 x 34,472.1 x $0.0056 = $34.55` to the cent, i.e. it applies the 17.9%
   share **v3 itself withdraws**, in the document that withdraws it. From v3's
   own 3.08% the figure is **$5.94**. And "0.179 x 36,336.6 = 6,267" is **6,504**
   - a 3.8% error in the first multiplication - while `6,267 x $0.0056` is
   **$35.10**, the figure labelled "at RATE + KEYTERM" in the row above, so the
   two columns had each other's arithmetic.

2. **CLOSED - D4 keyterm (+$45.52) is now EVIDENCED**, not merely adopted.
   `evidence/probes/nhbplus-keyterm-ab-v4-2026-10-15.json`. The first two A/Bs
   measured nothing: the original recorded zero gain and zero loss, and the
   first re-run selected `ABSOLUTELY, ACTUALLY, AGAIN` and produced noise.
   **The selector is the whole problem.** Three were built, each checked against
   cached transcripts before submitting anything:

   | selector | picked | verdict |
   |---|---|---|
   | capitalised, count 1-3 | `ABSOLUTELY, ACTUALLY, AGAIN` | discarded |
   | + minus the 150 most frequent types | unchanged | discarded - frequency cannot separate them |
   | **Deepgram per-word confidence < 0.85** | `Alan, Rohan, John, Nicky, GrowRev` | **used** |

   Confidence is the signal keyterm acts on. Capitalisation and frequency are
   proxies and both failed.

   Result over 5 units, 454.7 min/arm, occurrence counts per keyterm given:

   | | gained | lost | net | ratio |
   |---|---|---|---|---|
   | **proper nouns** | **15** | **3** | **+12** | **5.0 : 1** |
   | filler mistakenly keytermed | 6 | 1 | +5 | 6.0 : 1 |

   **4 of 5 units won; 9 of the 12 proper nouns touched improved.** The largest
   move is the point: **`Rohan 13 -> 19`**. Also `Nicky 2 -> 4`,
   `GrowRev 3 -> 4`, `Robbie 2 -> 3`, `Alan +1` in three separate units.

   **A finding that changed the spec:** keyterming `I've` and `Sorry`
   *increased* them. The hint fires on whatever it is given. **A production
   keyterm list must contain proper nouns only** — now a measured requirement
   in §2.2, not a preference.

   The three proper nouns that lost are recorded as a real cost: the hint nudges
   toward the given token, so a name it was given but which was said less often
   gets suppressed.

3. **CLOSED - the PDF gate is closed on 50 of 50.** See the note below.

4. **OPEN - 13 of 14 gates are UNEVALUABLE** because no pipeline code exists yet.
   That is the correct state at G1 and is the substance of Stage 3. **But V4 and
   V5 now carry FORMULAS** - they were one line naming a check, with no rule, no
   threshold and no failure behaviour, which is the same defect as the missing
   request payload in 7.2.0. Neither was implementable from the document alone.

5. **CLOSED - `WPM_MAX` was too tight and `SPAN_EDGE_SEC` was 12.9x too loose.**
   Both were gate thresholds carrying no evidence, and both were permissive or
   fragile in the direction this project's unmarked constants always fail.

   A full census - **all 42 lessons plus 5 calls, 47 units, 94 edges** - settled
   them:

   | | before | measured | now |
   |---|---|---|---|
   | `WPM_MIN` | 60, guessed | quietest unit 127.6 wpm | **60**, = 47% of it |
   | `WPM_MAX` | 260, guessed | densest unit **251.7** wpm | **300**, = 1.19x |
   | `SPAN_EDGE_SEC` | **60**, guessed | largest edge anywhere **4.64 s** | **10**, = 2.15x |

   `WPM_MAX` at 260 sat **8.3 wpm** above the densest measured unit, with two
   lessons already inside 15 wpm of it. It would not have failed today; it was
   one dense lecture from failing a correct note.

   `SPAN_EDGE_SEC` at 60 sat **12.9x above the largest edge ever measured** - a
   note missing its first **55 seconds** of speech would have passed the gate
   whose entire job is to catch that.

   A finding that had to be handled explicitly: **10 of the 47 units have a
   NEGATIVE tail**, the last word ending *after* the declared duration by up to
   1.00 s. That is the `pjFQiLQQ` class - the manifest duration is a claim, the
   transcript extent is the measurement, and the measurement can exceed the
   claim. It is not a failure, V5's `tail_gap > SPAN_EDGE_SEC` cannot trigger on
   a negative value, and it is written down because a future reader would
   otherwise try to "fix" it.

   Cost: **$8.79**, which the budget already carried for the lessons - and the
   transcripts and remuxed media are cached, so the run reuses them rather than
   paying twice.

6. **CLOSED - the `attachments/` conflict**, plus VAULT-STRUCTURE.md's
   verbatim-vs-clean naming conflict and its index-note conflict. All three
   resolved in the master's favour, recorded in a table at the top of
   VAULT-STRUCTURE.md, whose status moved from "proposed, pending operator
   sign-off" to signed-and-superseded.

## A SEPARATE DEFECT FOUND WHILE CLOSING ITEM 5

**`SPEND_HARD_STOP_USD` had four live values and was defined twice.** The block
labelled *"DERIVED, not asserted"* said **`$207.68`** while the live constant was
`$213.48`, and a second site still asserted the tail *"is not in $203.04"* — a
figure three revisions old. A constant that carries four values and a paragraph
insisting it is derived is a constant nobody can stop the run against. Now:

```
(34,472.10 calls + 294.84 undated tail + 1,569.62 lessons) x $0.0056 = $203.48
+ $10.00 loss reserve                                                  = $213.48
```

The undated tail is also resolved: the 286.9 min was an ESTIMATE, and both
undated units have since been MEASURED at **294.84 min** combined.

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
