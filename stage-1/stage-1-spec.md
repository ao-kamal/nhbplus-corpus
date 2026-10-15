# STAGE 1 — MASTER SPECIFICATION (rev 1)

**NHB+ corpus transcription. An agent executes this with no other document open.**

Rev 1 applies **round 1** of the refinement loop: four adversarial rounds —
red team, repo-grounded verification, money/state audit, output quality — run
as one broadened round across four orthogonal attack surfaces.

Next gate: **G1** — rounds 2–4 must run **strictly sequential**, each reviewing
the plan *after* the prior round's changes are applied, so that "incremental vs
fundamental" becomes measurable. Convergence is measured between revisions.

> **Round 1 found 6 blocking defects that would have destroyed data or money, and
> one arithmetic contradiction that fails the plan on a flawless run.** They are in
> §0, §2, §5, §6 and §7 below, each marked `[R1]`.

---

## 0. Hard constraints

These outrank every mechanism here. Nothing below may trade one away.

| # | Constraint | Enforcement |
|---|---|---|
| 1 | **Nothing media-shaped touches the operator's PC.** | The vault (markdown) is the deliverable and *does* land there. Gate V6. |
| 2 | **Pay nothing**, outside recorded waivers. | **Two waivers, not one `[R1]`:** Deepgram STT (~$150), **and Azure compute** (metered VM on a $200 credit, ~$0.21/day idle — operator-approved, `evidence/probes/operator-decision-compute-azure-2026-10-14.json`). §0 previously said "sole waiver: Deepgram" and was **wrong**. Report VM-days alongside STT spend. |
| 3 | **Remove nothing.** Where a route is blocked, the route changes. | The 2 sparse PDFs are extracted, not dropped. 105 MP4 alternates are never fetched — a route change, not a removal. |
| 4 | **Evidence, not assertion.** | W0 probes. Ten claims withdrawn during planning; kept visible in §13.2. |
| 5 | **Operator picks the files.** | `scope-final.json`, **344** targets, locked. |
| 6 | **A sentinel is not a measurement** `[R1]` | **[F-KIB 2026-10-15] THIS IS UNDERSTATED. NOT 73 OF 230 — ALL 188 CALLS.** Every declared size in the corpus is an **exact multiple of 1 KiB**: **188 of 188, 100% of the corpus bytes.** The chance of that by accident is (1/1024)^188. The spec detects sentinels only at **GiB** granularity (`bytes % 2**30 == 0`), which finds 73 and calls the other 115 "real". They are not real either — they are KiB-quantised. Proof from the one unit measured against ground truth: `wiUyTRZb` **declared 397,410,304 B (KiB-exact)** vs **actual downloaded 397,487,264 B (NOT KiB-exact)**, a 76,960 B delta. So there is **no unquantised subset** by this test, and the "73 sentinels / 157 real" split in this document is wrong in kind, not just in number. **§6 (sentinel detection) must test `bytes % 1024 == 0`, and no threshold may consume any declared size.** §6 (73 of 230 carry placeholder sizes** — 37 at exactly 1 GiB, 36 at exactly 2 GiB = **109.00 GiB of 146.39 GiB = 74.5%**. These are MEGA display values recorded as binary. **No kill rule, threshold, or cost gate may consume them.** §6.4. |
| 6a | **Send `mip_opt_out=true` on EVERY request.** **[R4-8.47]** Probed 2026-10-14: with the flag `HTTP 200`, without it `HTTP 200`, `VERDICT: PASS` (`deepgram-capability-probe-2026-10-14.json` § `STEP_0_CONSENT_GATE`). `operator-decision-compute-azure-2026-10-14.json` records it as *"structural and sent on every request"*. **This document contained ZERO occurrences of `mip_opt_out`, `consent` or `GDPR` before this line — the flag existed in a dated decision record and in nothing else.** §0's own rule is that *"an agent executes this with no other document open"*, so an omission here is an omission in the executed path, not in the reading list. **The artifact is explicit: *"Acceptance of the flag is NOT permission to stop sending it."*** §7.2. |
| 7 | **The response is the only retrieval** `[R1]` | `evidence/probes/deepgram-eu-limits-and-chain-proof-2026-10-15.json`, under `limits_that_would_have_broken_the_run`: *"Deepgram does not store transcripts. The API response is the only opportunity to retrieve it."* **Every submission is single-shot.** The response body must stream to disk as it arrives. §7.3. |

### 0.0 How to read the tags in this document `[F41]`

This spec carries **review-finding tags** inline: `[R1]`, `[B1]`…`[B26]`,
`[F1]`…`[F41]`, `[T5 #n]`, `[R1 corrected]`. **[F41] They were left in the body
with no legend, so a reader cannot tell specification from review commentary.**

**The rule, which is the only one that matters: the PROSE is authoritative and
the tag is provenance.** Where a tagged block and the surrounding text disagree,
the prose wins and the tag is stale — report it, do not reconcile it silently.

| tag | source |
|---|---|
| `[R1]` `[R1 corrected]` | round 1 review, and its correction pass |
| `[B1]…[B26]` | round 2 canon review — `stage-1/ROUND-2-CANON-REVIEW.md` |
| `[F1]…[F41]` | round 3 repo-grounded review — `stage-1/ROUND-3-REVIEW.md` |
| `[T5 #n]` | the six-untested-claims resolution pass |

Tags are **not deleted when a finding is applied.** A fix that removes its own
provenance is indistinguishable from a fix that was never checked, and the
question "was this ever wrong?" has no answer. What expires is the finding, not
the record that it existed. Every tag names a defect **that was real**.

### 0.0.1 Compute, priced `[MEASURED 2026-10-15 · CORRECTED BY R4]`

`Standard_D2s_v5`, `austriaeast`, Linux, Consumption — the VM the probes actually
ran on. **$0.115/hr** from `prices.azure.com/api/retail/prices`, queried
2026-10-15. **$2.76/day.** 2 vCPU.

> **[ R4-T4.1] THIS TABLE WAS WRONG BY 60× WHEN FIRST WRITTEN, AND THE ERROR
> WAS MINE.** `35,013.1 min / 25 / 90.6x` is **15.46 MINUTES**, not 15.5 hours.
> The value was right and the **unit** was wrong — minutes divided by a realtime
> factor is still minutes. Same slip twice more: the full-decode figure was
> **9.44 core-hours, not 567**, because `2,100,786 s / 61.8 = 33,993 s` and I
> divided by 60 a second time. **Every quantity below carries its unit, which is
> the rule R4 asked for and which would have caught all three.**

| phase | computation | result |
|---|---|---|
| **STT at concurrency 25** | `35,013.1 min / 90.6x / 25 = 15.46 min` | **0.26 h** |
| fetch, 146.8731 GiB | `146.8731*1024 / 47 MB/s = 3,200 s` | **0.89 h** |
| remux `-c:a copy` | `193 units x 5 s` (stream copy, **no decode**) | **0.26 h** |
| channel measurement, 90 s window | `10 stereo x 3 passes x 1.46 s` | **0.01 h** |
| **total** | | **≈ 1.42 h** |

**≈ $0.16 of Azure compute.** Fetch dominates the run. **The STT stage is
fifteen minutes**, which is worth sitting with: a 583-hour corpus is not a long
transcription job, it is a long *download* job.

**[R4-T4.2] the full-decode argument survives, at 17× not 1,150×.** The channel
measurement as §7.1a specifies it is a full decode: `2,100,786 s / 61.8x = 9.44
core-hours = 4.72 wall-hours on 2 vCPU = $0.54`. A 90-second window over every
unit is **0.28 h**. So the window is **17× better**, and 4.72 hours of pure CPU
to classify dual-mono is still indefensible. **Keep the window** — the
conclusion was right and only the figure attached to it was wrong.

**[R4-8.46] and the raise to 25 paid for itself in  $0.017 of Azure**, not in the
line I claimed. The *concurrency* case for 25 was never an Azure-cost case: 16 is
inside one project with no contract question, 25 is the documented ceiling, and
the measured degradation was 1.022×. That is still the whole argument. The
sentence "paid for itself in the first line" was wrong and is withdrawn.

### 0.1 Blocking decisions for the operator

**D1 — budget: RESOLVED WITH RESIDUAL `[R1 corrected 2026-10-15]`**

Rev 1 recorded a contradiction: `FORECAST == SPEND_HARD_STOP == $150.56`, while
the plan's own `ceil` commit spends $151.01, so V10 failed on a flawless run.

**That contradiction was an artifact of a rounding rule Deepgram does not charge.**
From the dated price page (`evidence/probes/nhbplus-deepgram-pricing-2026-10-15.json`):

> *"Deepgram uses **true per-second billing**. If your audio file is 14 seconds
> long, you pay for exactly 14 seconds. Many competitors round up to the nearest
> 15 seconds or full minute, which can inflate their actual invoice by 15-20%."*

There is **no per-request minimum and no rounding**. Against true per-second
billing the corpus costs `34,472.1 min × $0.0043 = $148.23` — the forecast.

**Residual, all three need an operator value:**

**SETTLED 2026-10-15.** Both items are now measured, not estimated. See 2.2 for the
full budget table and `SPEND_HARD_STOP_USD = $204.69`.

| Item | Was | Now |
|---|---|---|
| 2 units with no duration | ~$1.31 estimated | **$1.23 measured** |
| loss allowance for 504s | unset | **$10.00** |
| `SPEND_HARD_STOP_USD` | unresolved | **$204.69** |

**D2 — price: RESOLVED 2026-10-15.** `RATE_USD_PER_MIN = 0.0043`, now sourced and
dated from the price page instead of derived from the forecast. The figure was
correct all along; only its provenance was wrong. The circularity is gone.

**D3 — multichannel billing: RESOLVED 2026-10-15. Detect, do not choose.**

> *"We bill based on the total duration of processed audio. If you process a
> 10-minute file with 2 channels (stereo), you are billed for 20 minutes."*

`W0-ChannelCount` measured it (`evidence/probes/nhbplus-w0-channelcount-2026-10-15.json`).
**Every stereo file in the sample is dual-mono** — both channels carry the same
signal, two of the three bit-identical. **There is no per-participant channel
separation anywhere in the corpus.**

**What `-ac 1` loses: nothing measurable.** Two identical in-phase signals average
to the same signal at −6 dB. No cancellation — cancellation requires opposite
phase, and identical signals are in phase. No content change, no diarization
change, because there was never separate channel content to lose.

**The money — and a correction to rev 1.** Rev 1 quoted a **$150.56** exposure,
which was the worst case where every unit is stereo. Measured, only **17.9% of
minutes are stereo**, so the real saving is **$26.98**:

```
run cost as-is          $177.54
run cost with -ac 1     $150.56
saving                  $26.98
```

**The rule is per file, not per corpus** (§7.1). The 10-file sample constrains
nothing at scale — the measurement is applied to all 230 units, so a single
per-participant file anywhere is *detected and preserved* rather than downmixed.

**SECOND API KEY — budget only, never throughput.** Deepgram scopes concurrency
**per project, not per account or key.** The docs are explicit that multiple keys
inside one project *all draw from that project's concurrency pool*, and that
creating additional projects or accounts to work around per-project limits is
**detected and violates their Terms of Service**.

So a second key adds **$200 of budget and zero throughput**, and load-balancing
transcription across the two accounts would be an explicit ToS violation. **Use it
for budget only.** The run needs the budget — $204.69 exceeds the $200 credit. It
does not need the concurrency: one project at concurrency 50 covers the corpus.

**D4 - keyterm prompting: ADOPTED 2026-10-15** (operator). $0.0013/min,
**+$45.52**. Justified by a measured A/B, not an opinion — see 2.2.1. The deciding
argument is search: without it the corpus spells its own programme name
"Nothing Elbach", and `Ctrl+F "Nothing Held Back"` returns nothing.

---

## 1. Scope — locked

```

> # **[R4-T5.5] THE UNIT COUNT IS NOW 344, NOT 339, AND EVERY CELL THAT CITED
> 339 IS WRONG UNTIL IT IS RE-DERIVED. THIS PROPAGATION IS NOW DONE — see the table below.**
>
> R4 found `normalize.py`'s date check applied only when **both** sides carried
> a date, so an **undated** unit could absorb a **dated** one on a duration tie
> alone. It did, six times, and every one was wrong:
>
> | undated | absorbed | |
> |---|---|---|
> | `market efficiency ratios` | `2025-01-16 … mechanism of comprehension` | different calls |
> | `selling to women 3.0` | `2022-07-07 … the philosophy of offers` | different calls |
> | `the mechanism of will power` | `2024-12-12 … value matrix` | different calls |
> | `the next 5 years` | `2025-01-20 … introduction to google ads` | different calls |
>
> **A 2025 call folded into an undated unit, and three different years into one
> note** \u2014 a wrong note, a wrong date and a wrong written-hand link, produced
> silently by a rule nobody gated.
>
> **The guard now REFUSES a merge when exactly one side carries a date.** A wrong
> merge is silent and corrupts; a wrong non-merge is visible and costs one extra
> unit. Measured consequence:
>
> | | was | **now** |
> |---|---|---|
> | calls | 188 | **193** |
> | lessons | 42 | 42 |
> | documents | 109 | 109 |
> | **targets** | **339** | **344** |
> | merges applied | 18 | **12** |
> | audio minutes | 35,013.1 | **34,472.1** |
> | `SPEND_HARD_STOP_USD` | $207.68 | **$203.04** (34,472.1 \xd7 $0.0056 + $10) |
>
> **THE MONEY FELL $4.64 BECAUSE FIVE CORRUPT UNITS NO LONGER EXIST.** The
> offsetting omission: the two remaining undated calls have **no measured
> duration and so contribute $0.00**. The previous budget carried a **286.9-minute
> tail** for exactly this case and **it is not in $203.04.** It must be re-added
> from a measurement of those two units, not from the old figure.
>
> **PROPAGATED 2026-10-15.** Every one of these cited 339 / 188 / 35,013.1 and
> has been re-derived from the regenerated artifacts — not hand-copied:
> target count \u00b7 \u00a77.2 AUDIT row count \u00b7 \u00a710 vault-tree counts \u00b7 \u00a711 V0
> "339 rows" and V6's floor \u00b7 \u00a712 egress manifest \u00b7 \u00a713.2 \u00b7 \u00a714 \u00b7 AGENTS.md.
> **Recorded as an open propagation rather than hand-edited into a false green.**
```

| Population | Count | Handling |
|---|---|---|
| Audio calls | **193** | STT. **574.53 h.** [R4-PROP] was 188 / 557.39 h |
| Bonus lesson videos | 42 | STT. 26.16 h. All 11 courses + all 36 orphans. |
| Documents | 109 | Extract, no STT. **0.486 GiB**, of which PDFs are 0.159 GiB `[R1]`. |
| MP4 alternates | 105 | Recorded, **never fetched**. Real saving **185.45 GB** `[R1]` — "132 GB" appears in no artifact. |

**Corrections to my own briefing, all now verified against files:**

- Documents partition **37 written_hand + 36 course_doc + 36 orphan = 109** ✓
- Of the 109, **50 are PDFs** and **51 are OOXML** (36 docx + 12 pptx + 3 xlsx).
  The other 8 are **6 txt, 1 png, 1 zip** `[R1]` — §8.3, previously unhandled.
- **42 videos vs 36 course docs is not an error.** Operator decision: videos and
  documents are independent. V9 checks self-consistency, never forces 1:1.
- **133 of the 230 fetched primaries are MP4, only 97 MP3** `[R1]`. §1 previously
  treated MP4 as excluded alternates. **`ffmpeg -vn -c:a copy` (§7.1) is the
  majority path, not an edge case.**
- **Total is 600.70 h**, not 583.55 h and not 603.84 h — that figure belongs to a superseded
  **236-call** reconciliation `[R1]`.
- **146.87 is GiB, not GB.** Every `GB` field in the JSONs is binary `[R1]`.

---

## 2. Constants — every value carries provenance

```
MEGA_URL_TMPL  = "https://mega.nz/folder/<PH>#<KEY>/file/<HANDLE>"
     PROVEN. [B26] Peak disk is **1.50 GiB MEASURED** (dvcEDToK, the largest unit
     examined). The 2.00 GB figure that circulated was 2 GiB — the SENTINEL
     value, 36× repeated. Constraint 6 forbids consuming a sentinel and §2
     was doing exactly that.

FETCH_CONCURRENCY      = SIZE-ADAPTIVE, not a constant. See 6.3.
FETCH_CONCURRENCY_CEILING = 38   [R4-T4.5] was 39. The [F17] off-by-one fix landed in
                                 section 6.3 and section 4 and NOT in the constants
                                 block - the one an engineer reads first.
                                 39 x 100 MiB = 3,900 MiB > 3,872 admissible;
                                 38 x 100 MiB = 3,800 MiB.   RAISED from 1, 2026-10-15. W0-Cap PASSED: the
                                4 GiB loopback is a real, exact, timely stop.
                                Expected saving 40-65 min. The cap costs 1.7%
                                throughput (169 vs 172 MB/s) against a network
                                fetch ceiling of 41-53 MB/s, so it is free.
REMUX_CONCURRENCY      = 2
TRANSCRIBE_CONCURRENCY = 25       RAISED FROM 16, 2026-10-15, ON MEASUREMENT.
                                 **[W0-CONCURRENCY25] 25 CONCURRENT REQUESTS
                                 FIRED SIMULTANEOUSLY: 25/25 HTTP 200, ZERO
                                 429s, and the corpus's LARGEST call completed
                                 in 186.738 s against the 600 s ceiling.**
                                 Its SOLO time was 182.757 s, so
                                 DEGRADATION = 1.022x - 2.2%. The 3.28x
                                 margin survives at 25-way as 3.21x.
                                 25 IS NOT A HOPE NOW; IT IS A MEASUREMENT.
                                 Artifact: nhbplus-w0-concurrency25-2026-10-15.json
                                 Run cost $2.41. **[R4-PROP] Saves 8.7 MINUTES of a ~15-minute STT stage, not
                                 8.7 h of a 24 h run — that was the same 60× unit slip.**
                                 LIMITS: one burst, not the full 15-minute STT stage;
                                 single key; a PASS is not a capacity guarantee.
                                 BINDING CEILING IS 25, not 50. Authoritative
                                source, fetched 2026-10-15:
developers.deepgram.com/reference/api-rate-limits.md
                                 **[R4-8.57] RESOLVED 2026-10-15 BY LIVE FETCH. THE 25 IS
                                 CONFIRMED.** Artifact:
                                 `nhbplus-deepgram-rate-limits-2026-10-15.json`.
                                 Nova-3 EU Pre-Recorded = 50; Speaker Diarization EU
                                 Pre-Recorded = **25**; the lower applies. The
                                 following note records what the probe cost, and it
                                 was worth it:
                                 THIS TABLE WAS NEVER PROBED IN THIS
                                 PROJECT AND WAS THE WEAKEST LOAD-BEARING CLAIM OUTSIDE
                                 THE STEREO SHARE.** "fetched 2026-10-15" cites a URL,
                                 not an artifact: no dated evidence file records the fetch
                                 or what it said. WORSE, `stt-concurrency-2026-10-15.json`
                                 already records this table **moved once** - "the 25
                                 figure predates Deepgram's February 2026 3x concurrency
                                 increase". A ceiling the project has already caught moving,
                                 pinned exactly, at ZERO headroom, on a 5% sample.
                                 ACTION BEFORE THE RUN: fetch it, write the page to
                                 evidence/probes/ with a date and a hash, re-confirm 25.
                                 Until then 25 is DOCUMENTED, not MEASURED.
                                  Nova-3            | EU | Pre-Recorded  up to 50
                                  Speaker Diarization | EU | Pre-Recorded  up to 25
                                  "If multiple services are used in one API call...
                                   the lower of the rate limits is applied."
                                diarize=true is NON-OPTIONAL (10.1 needs diarisation
                                clusters; Rule 3 forbids removing it), so the LOWER
                                limit binds: min(50, 25) = 25. **We now run AT 25, not below it.**

> **[R4 CLOSED THIS WITH VENDOR VERBATIM, 2026-10-15. IT IS WORSE THAN A GREY
> AREA AND THE DECISIVE CLAUSE WAS NOT KNOWN BEFORE.]** The rate-limit page,
> fetched, says:
>
> * *"Rate limits apply per project, not per account or API key."*
> * *"**Secondary projects created on a self-serve account are limited to a single
>   concurrent stream by design.**"*
> * *"Do not create additional projects, additional accounts, or otherwise
>   distribute traffic across projects to work around per-project limits.
>   **These setups are detected.**"*
>
> **So the split-the-corpus hypothesis would not merely have failed to help — it
> would have been 25× WORSE**, because a secondary self-serve project is capped at
> **one** concurrent stream, and the carrier request would have had to run alone.
> The operator's instinct that concurrency is per-project was exactly right; the
> consequence of acting on it was not.
>
> And the reason a second key buys *budget* but not *throughput*, in the vendor's
> own words: *"Multiple API keys inside a single project all draw from that
> project's concurrency pool."*
>
> **ON THE SECOND DEEPGRAM ACCOUNT - A QUESTION THAT WAS ASKED AND ANSWERED.**
> Splitting the corpus across two accounts WOULD roughly double throughput:
> concurrency is scoped per project, so two projects are two pools, and 32-way
> would take the run from 15.5 h to 12.1 h. **It is refused anyway**, and the
> distinction is worth stating because it is the whole contract question:
>
> | use | what it does | verdict |
> |---|---|---|
> | second key for **budget** | you pay for more service ($204.69 > the $200 credit) | legitimate |
> | second key for **throughput** | you obtain concurrency above the ceiling | circumvention |
>
> The second use is the one the plan would be doing, and it is what the ToS
> language quoted in this document is aimed at. It was also never worth it:
> **16 -> 25 recovered 8.7 MINUTES of STT inside one project with no question at
> all** [R4-PROP: this said 8.7 h, the same 60x slip], and
> the remaining 25 -> 32 would have bought **3.4 h** in exchange for a standing
> doubt about the whole run. §2.2's rule stands: **a wallet, not a worker**,
> sequential failover on 402, never concurrent.
                                THE 16 -> 50 'CORRECTION' WAS WRONG: it read the
                                MODEL row and substituted it for the DIARIZATION row.
                                The original 25 was right and was doubted because a
                                newer-looking number existed.
                                Round 2 caught that the 16 -> 50 correction fixed
                                the MODEL row (nova-3 pre-recorded EU) and
                                silently substituted it for the BINDING row,
                                which is diarize=true pre-recorded EU = 25. The
                                model row was never the constraint on THIS build:
                                10.1 requires `speakers` = diarisation clusters,
                                so diarize=true is non-optional (Rule 3).
                                The concurrency probe also measured ZERO 429s at
                                levels up to 16 only - never at 25, never with a
                                request shape above that level. Setting 50 would
                                assert evidence that was never gathered.
                                Re-read the diarization row and re-measure before
                                this moves. evidence/probes/nhbplus-stt-concurrency-2026-10-15.json

FETCH_IMG_BYTES = 4 GiB   loopback ext4, kernel-enforced. W0-Cap proves ENOSPC.
CAP_BYTES       = 2_000_000_000
SEGMENT_SEC     = 1500    PROVISIONAL. The remuxed >= CAP_BYTES guard ONLY.
                         There is no sync fallback - see 7.2.
FETCH_STALL_SEC = 120     POST_KILL_QUIESCE_SEC = 60
WPM_MIN, WPM_MAX = 60, 260          PROVISIONAL
SPAN_EDGE_SEC   = 60
FORECAST_USD    = 150.56
```

### 2.2 Spend constants — sourced, settled, and measured `[settled 2026-10-15]`

```
RATE_USD_PER_MIN      = 0.0043    nova-3 monolingual, PRE-RECORDED, Pay As You Go.
                                   Sourced + dated. Diarization INCLUDED on
                                   pre-recorded, so diarize=true costs $0.00.

KEYTERM_RATE_USD/MIN  = 0.0013    ADOPTED - operator decision 2026-10-15,
                                   justified by a measured A/B, see 2.2.1
KEYTERM               = ON, per unit, list built from that unit's OWN vocabulary

PER_REQUEST_MINIMUM   = NONE      Proven: true per-second billing, no minimum,
                                   no rounding. The pessimistic ceil was deleted.

COMMIT_COST           = (billed_seconds(part) / 60) * (RATE + KEYTERM_RATE)
                        RATE and KEYTERM_RATE are USD PER MINUTE; billed_seconds
                        is SECONDS. Without the /60 this is a 60x OVERCOMMIT: a
                        3,600 s part commits $20.16 instead of $0.336, and the
                        corpus commits $11,764.40 instead of $196.07. The preflight
                        would stop the run after roughly ten parts. [B4]
                        THIS IS THE SAME UNIT SLIP THAT PRODUCED THE 273.7x ERROR -
                        seconds multiplied by dollars-per-minute. The class is
                        closed by this fix and by the loss-allowance re-base.
SETTLE_FROM           = metadata.duration seconds x INPUT_CHANNEL_COUNT,
                        IDENTICALLY in the 7.2 gate and in V10. [T5 #3][F5]
                        NOT the response's channel array: Deepgram returns
                        channels=1 for a stereo input while BILLING 2x.
                        AND NOT the PRE-downmix part. INPUT_CHANNEL_COUNT is the
                        channel count of the part AS SUBMITTED, recorded in the
                        same atomic write as `sent`. The 7.1a BIT_IDENTICAL branch
                        re-runs -map_channel and produces a MONO part, so reading
                        the pre-downmix count would settle every downmixed unit at
                        2x and double-count the $26.98 saving into the ledger.

  KEEP-STEREO TAIL (not in the $197.68 above). [F6]
    3 of 3 stereo files were dual-mono, so the 7.1a keep-stereo branch has
    fired 0 of 3 and the $26.98 downmix saving is currently whole. If a future
    part reads INDEPENDENT and keeps 2 channels, SETTLE_FROM bills 2x for it.
    Worst case over the corpus: +$197.68, i.e. a $405.36 run against a
    $207.68 stop. The gate must stop, not re-derive, when this happens -
    the unmeasured tail is a spend risk the flat budget does not cover.
    Corpus-wide stereo share is UNKNOWN (see section 6 residual risks).

SPEND_HARD_STOP_USD   = 207.68    DERIVED, not asserted. [B6] Three values
                                were in circulation and all three were wrong:
                                $207.31 (the budget artifact), $207.35 (this
                                spec, twice), and this one — which is derived.
  [R4-T1.7] THE $200 CREDIT ARGUMENT NEVER SUBTRACTS THE PROBES THIS DOCUMENT
  ITSELF RECORDS. It compared the RUN ($197.68) to the credit and concluded two
  accounts are required. But ~$6.54-$10.23 is ALREADY SPENT:

  | | |
  |---|---|
  | run | $197.68 |
  | W0-Concurrency25 | $2.41 |
  | W0-SyncCeiling take 3 (carrier) | $1.55 |
  | W0-SyncCeiling take 2 (`dvcEDToK`) | $1.14 |
  | keyterm A/B | $0.76 |
  | W0-AsyncContract | $0.40 |
  | W0-Concurrency (concprobe) | $0.11 |
  | T5 stereo / B23 .mka | $0.06 |
  | **run + probes (de-duplicated, lo / hi)** | **$204.22 / $207.91** |
  | **credit** | **$200.00** |
  | **shortfall** | **$4.22 to $7.91** |

  Several of those rows OVERLAP (deepgram-eu-limits records
  `spent_on_probes_to_date_usd: 3.80` covering several), so $6.54-$10.23 is a
  de-duplicated band, not a sum. **The real reason two accounts are needed is
  that the ACCOUNT is not at $200 — not that the run exceeds it.** Plus the
  take-1 raw-MP4 submission, which TIMED OUT and whose billing status is
  unknowable from here (§7.3).

  [R4-T1.8] AND THE OPERATOR-FACING LINES WERE PRE-KEYTERM. D4 adopted keyterm
  after they were written, so three published figures never entered §2.2:

  | | published | **at RATE + KEYTERM** |
  |---|---|---|
  | run with `-ac 1` | $150.56 | **$196.07** |
  | run as-is | $177.54 | **$392.15** |
  | downmix saving | $26.98 | **$35.10** |

  **`$26.98` is `RATE`-only.** The stereo share is `0.179 x 35,013.1 = 6,267`
  minutes, and at `RATE` alone that is $26.95 — so the number is internally
  consistent but **computed at the wrong rate and never entered this budget.**
  All three lines are re-based above; $26.98 is withdrawn as a live figure and
  retained only as the STT-only saving.

  ONE formula, ONE figure. [F2]
      (34,472.1 + 294.84) x $0.0056 = $194.69   <- the run
      [R4-PROP] 34,472.1 min from 191 DATED calls in the regenerated
      manifest; + 294.84 min for the two units whose durations are not in
      the manifest but WERE measured - dvcEDToK 12,258.603 s
      (w0-syncceiling) and pjFQiLQQ 5,431.8 s DECODED (w0-remux; its
      container header says 4,958.7 s, +9.54%).
      + $10.00 loss reserve         = $204.69   <- SPEND_HARD_STOP_USD
      [R4-PROP] was $207.68 on 35,013.1 + 286.9 min. The 286.9 tail was
      an ESTIMATE for the undated units; both are now MEASURED at
      294.84 min combined, and 5 corrupt merged units no longer exist.
      Net -$2.99.
  The displayed component previously read $196.68 and the table four lines
  below summed to $207.35, so THREE figures were live in one code block and the
  total did not follow from the line above it. Both are gone.
                                The $1.23/$1.27 "undated units" line was
                                STT-only; at RATE + KEYTERM the two units are
                                286.9 min x $0.0056 = **$1.65**. [B1]
LOSS_ALLOWANCE_USD    = 10.00     5% of ~230 units at the mean COMMIT_COST
                                $0.86 = $9.89. [F3] The old derivation named
                                3,611 parts - the segmentation design section
                                7.2 dissolved. $10 leaves 1.1% headroom, which
                                is marginal and is stated as marginal.
```

**The settled budget — every line measured, none estimated. [F2] ONE table, ONE
figure.** The per-line split is *inside* the run total, not added on top of it:

| | |
|---|---|
| **TOTAL RUN** (34,472.1 + 294.84 min) × $0.0056 | **$194.69** |
| — of which STT 34,472.1 min × $0.0043 | $148.23 |
| — of which keyterm 34,472.1 min × $0.0013 | $44.81 |
| — of which the 294.84 measured undated minutes | $1.65 |
| 504 loss allowance (5% of ~230 units = $9.89) | **$10.00** |
| **`SPEND_HARD_STOP_USD`** | **$204.69** |

Adding the splits on top of the total is how **$207.35 and $207.68 were both live
in one code block.** The old table's "2 previously-undated units $1.27" was
header-derived — `durprobe.json` prices `pjFQiLQQ` at its container header
(4,958.743 s) while §7.1 and AGENTS.md trap 29 both establish its decoded PCM is
5,431.8 s. Repriced on decoded PCM the undated tail is **294.84 min**, which is
the 286.9 above, priced at the **$0.0056** keyterm rate because those minutes
carry a keyterm. [F4]

**Credit position: no payment card on file.** So the vendor itself enforces the
ceiling — exhausting the credit returns **HTTP 402** and processing stops. That is
a hard, vendor-enforced bound that no bug in our accounting can get past.

**But $200 < $204.69, so the vendor stop is strictly LOWER than our own gate and
fires FIRST.** Round 2 caught that "strictly stronger" was backwards. The correct
statement: the 402 is a **backstop at $200 per account**, not a ceiling at
$204.69. Two accounts are therefore required, and the split is explicit:

```
primary    DEEPGRAM_API_KEY     carries the bulk
secondary  DEEPGRAM_API_KEY_2   carries the shortfall above one account's $200
```

The ledger is **per-account** (5.3 gains an `account` field):

```
gate:  sum over accounts of (committed + settled + lost) + cost > SPEND_HARD_STOP_USD
    AND chosen_account.**Routing, which must be explicit or it is unimplementable. [B12]** "All transcription goes through the primary" and "the secondary carries the shortfall" cannot both hold: a primary that has spent its $200 returns **402** and cannot be used at all.

```
attempt the request on the primary
  402 -> the primary is exhausted. Re-route the WHOLE PART to the
          secondary, re-commit against the secondary's own ledger, and
          record account=secondary on the receipt. Never split one part.
  other -> attribute to the account that served it
```

**The secondary is a wallet, not a worker.** Deepgram scopes concurrency per project, so a second key adds zero throughput, and distributing traffic *concurrently* across accounts is a documented ToS violation. Sequential failover on 402 is not load distribution — it is one account finishing before the next begins.

### 2.2.1 Why keyterm — the measurement, not the opinion

`$0.761` A/B, one 68-min unit, identical audio and parameters, keyterm as the only
variable:

| | baseline | with keyterm |
|---|---|---|
| "Rohan" correct | 12 | **16** |
| "Ron" mangled | 4 | **3** |
| "Nothing Held Back" correct | 0 | **1** |
| programme-name mangled variants | 2 | **1** |
| word count | 15,349 | 15,347 |

It fixed the speaker's surname and **"Nothing Elbach" → "nothing held back"** —
the programme's own name, rendered phonetically for want of a hint.

**The decisive argument is search, not accuracy.** This vault exists to be
searched. A corpus that spells its own programme name "Nothing Elbach" returns
nothing for `Ctrl+F "Nothing Held Back"`. No term was lost and no words dropped.

**Implementation, per unit — not one global list.** The keyterm list is derived
from *that unit's* `media.name` and `topic`: capitalised content words, stop-words
and brand tokens removed, no invented terms. `topic` strings are normalised to
lowercase in `manifest-v3.json`, so **capitalisation must come from
`media.name`** — reading `topic` yields an empty list, which is a silent no-op.
A `keyterm` request parameter costs nothing extra to send when empty.

### 2.3 PDF calibration — RE-MEASURED, do not inherit

`evidence/probes/nhbplus-pdf-text-layer-2026-10-15.json`.

```
Y_TOL    = 0.6   Digest-stable on 48/50: SHA-256 of ordered line TEXTS is
                 byte-identical at 0.0/0.25/0.5/0.6/1.0/2.0/3.0/5.0 pt.
                 Geometry moves (baselines 444 -> 128); text does not.
                 LOAD-BEARING on 2 documents, whose baselines sit within a few
                 points: "500-page-swipe-file-clayton-makepeace_compress_1.pdf"
                 and "fourdaycashmachine.pdf". Recorded, not smoothed over.
TIER_MIN = 5     A tier is a size carried by >= 5 lines. Populations 395/133/11,
                 so T in 2..10 agree; 5 tolerates a stray span 2 would promote.
TIER RULE= gate first (§8.1 taxonomy). Then title = largest tier, body = most
                 frequent tier, every OTHER tier = a heading tier.
                 Measured: title 60.0pt, headings [24.0pt] over 133 lines (25%),
                 body 11.04pt.
```

| Inherited constant | Verdict |
|---|---|
| skill's flat `18.0pt` | Wrong. This corpus tiers 60 / 24 / 11.04. |
| `title_size × 0.55` → **33.0pt** | **Silently excludes the 24.0pt tier.** This made an early extractor report `headings=0` on a document with 133. |
| char count as a text-layer test | Wrong. Hex glyph indices are bytes; a raster page scored 449,418 "characters". |

---

## 3. The six disputes — decided

| Dispute | Decision | Why |
|---|---|---|
| Fetch concurrency | **size-adaptive, 1–39** | **[F16] THIS SAID 1** and contradicted §2's predicate and §6.3's bands. The serial figure was true when `FETCH_CONCURRENCY` was a constant, raised to 6 and then to a 1–39 band by W0-Cap, which proved ENOSPC **fails fast in 0 s** with no host spill. Serialising now costs ~1 h *measured* for no hazard the probe did not demonstrate. |
| Async policy | **RESOLVED — no async exists** | `ASYNC_ALLOWED = False` measured. The dispute was *"which of two single-shot paths?"* — and the answer is there is only one. The whole sync/async branch, its poll loop and its retention question are deleted. |
| State authority | **receipts on disk**; journal derived | Two independent truths is a desync waiting to happen. |
| Parts | **primary abstraction** | 2 GB cap, 504 recovery and tail segmentation become one code path. |
| Ordering | **docs shakedown → 1 lesson smoke test → 16 longest → cheapest** `[R1]` | A lesson-sized STT costs ~$0.16 and de-risks the paid pipeline for almost nothing. |
| PDF | **probe-first** | **RESOLVED — closed.** 0 documents need OCR. |

---

## 4. W0 probes

| Probe | Status | Question |
|---|---|---|
| **W0-Fetch** | ✅ PROVEN | per-file route works. `systemctl is-active mega-cmd-server` is **known-false**; only a real fetch arbitrates. |
| **W0-Cap** | ✅ **SATISFIED 2026-10-15** | **CLOSED.** The 4 GiB loopback is real, exact (3,936 MiB into 3,952), costs 1.7% throughput against a 41–53 MB/s network ceiling, **fails fast under real traffic** (mega-get exit 232 "Insufficient disk space" in **0 s**, no host spill), and recovers without a remount. **Fetches: `FETCH_CONCURRENCY` 1 → **the size-adaptive predicate, 1–38 in flight** — not a constant.** **[F18] This row said "1 → 6" and contradicted §2, §3 and §6.3. The raise to 6 was real; the ceiling is now the predicate's small band.** |
| **W0-Remux** | ✅ **SATISFIED 2026-10-15** | **CLOSED.** Bit-exact for MP3 (SHA-256 over 712/995 MB PCM - **[F23] the 995 MB figure appears only in this spec and in the [B24] note; w0-remux.json records 133.6/89.8 MB sources. Cite the artifact, not this line.**), near-exact for AAC (~10 KB in 1.1 GB). Real size cut is **71.2% aggregate — MP4 ~80%, MP3 NEGATIVE**. Output container must be **`.mka`**: `.m4a` fails for 97 of 230 units. |
| **W0-SyncCeiling** | ✅ **SATISFIED 2026-10-15 (take 3)** | **GENUINELY CLOSED, MEASURED ON THE CORPUS MAXIMUM.** `wiUyTRZb` — **275.93 min, the largest unit in the corpus** — returned **HTTP 200 in 182.757 s against the 600 s ceiling. Margin 3.28×, realtime 90.6×, 51,786 words. $1.55.** Artifact `nhbplus-w0-syncceiling3-2026-10-15.json`. **[History: take 1 (raw MP4) timed out; take 2 measured `dvcEDToK`, which ranks 47th of 229; a fix then asserted figures for `wiUyTRZb` that existed in no artifact — 156.2 s, 3.8×, 51,787 words. All three of those were wrong. The word count was off by ONE.]** |
| **W0-AsyncContract** | ❌ **FAILED 2026-10-15** | **`ASYNC_ALLOWED = False`.** No async job at 2 min *or* 68 min — inline results, `request_id` None. §7.2 collapses to one sync path. The "unreachable 504" claim that came with it was **calculated at 273.7×, measured at 5.7× on the 47th-ranked unit, and then asserted at 3.8× with no artifact behind it. The true figure on the corpus maximum is 3.28×** — not 273.7×, not 5.7×, and not the 3.8× that a fix supplied — see W0-SyncCeiling. |
| **W0-Pricing** | ✅ **SATISFIED 2026-10-15** | **CLOSED.** `$0.0043/min` nova-3 pre-recorded, diarization included, sourced and dated. **No per-request minimum, no rounding — true per-second billing.** |
| **W0-ChannelShare** | 🟡 **PARTIAL · OVERTURNED 2026-10-15** | **[ R4-PROP] THE EARLIER HEADLINE "ZERO OF 10 STEREO FILES, EVERY ONE BIT-IDENTICAL" HAS BEEN FALSIFIED.** An expanded sample found **`pvd0RJrB` (`ff_nhb weekly calls - competing on economics`, 2022-06-23, 175 min, declared size exactly 2 GiB — a sentinel)**: L md5 `2f144ac4…` ≠ R md5 `53ade16b…`. **The first genuinely-stereo unit in the corpus. The keep-stereo branch FIRES and that part bills at 2×.** Combined: **1 of 19 measured calls is genuinely stereo**; of 5 stereo files, 3 are bit-identical and 1 is not. At n=19 the 95% interval runs ~2%–26%, so the share is still not bounded — but it is no longer bounded above by zero. §2.2's $197.68 keep-stereo line STANDS. WHY THE FIRST SAMPLE MISSED IT: it stratified by DECLARED SIZE, and Constraint 6 says declared sizes are quantised and may not gate anything; this unit's declared size is exactly 2 GiB so it sat in the sentinel bucket, which got the SMALLEST allocation. **The sentinel defect once more — not as a threshold, not as a cost, but as a SAMPLING FRAME.** Artifact `nhbplus-w0-aclose-2026-10-15.json`. PREVIOUSLY: | **[MEASURED] 10 of 188 calls sampled (~5%), stratified by size. 7 measured, 3 fetch-failed. Every stereo file is BIT-IDENTICAL dual-mono: L md5 == R md5, proven by hash, not by an RMS threshold. 4 mono, 3 bit-identical, and the keep-stereo 2× branch fired on ZERO.** Includes `wiUyTRZb`, the corpus maximum. **The sample is too small to bound the corpus share and is not presented as if it could** — with n=10 and zero events the 95% upper bound is ~26%. Artifact `nhbplus-w0-channelshare-2026-10-15.json`. The branch stays specified; a small sample not triggering it is not grounds for deleting a 2×-billing safety branch. |
| **W0-ChannelCount** | ✅ **SATISFIED 2026-10-15** | **CLOSED.** 3 of 3 stereo files are **dual-mono** — no per-participant separation exists. `-ac 1` is lossless and saves **$26.98**. Applied **per file** in §7.1a, not corpus-wide, so a per-participant file anywhere is detected and preserved. |
| **W0-PDF** | ✅ **SATISFIED** | closed — §8.1 |
| **W0-Egress** | ✅ **SATISFIED 2026-10-15** | **CLOSED.** `scp -r` VM→PC is byte-exact (4/4 SHA-256 match), 11/11 typography checks survive, LF preserved, no BOM. **It produced a plan correction: V6 must run on the VM source tree BEFORE the copy.** |

---

## 5. State — the machine that actually prevents double-billing `[R1]`

> **This section replaces rev 0 entirely.** Round 1 proved the previous resume
> rule **could not distinguish a kill before the socket opened from a kill mid-request**,
> and therefore re-billed. The claim "resume never re-bills" was asserted while the
> state machine was blind to the one bit that decides it.

### 5.1 Per-unit

`units/<UNIT_ID>/` — `state.json`, `receipt.json`, `part-NN.bin`,
`response-part-NN.json`, `assembled.json`. Atomic write+rename throughout.

### 5.2 Per-PART states — the part is the unit of atomicity

```
queued -> reserved -> sent -> settled | lost

> **[F33] `queued` APPEARED IN THIS DIAGRAM AND WAS DEFINED NOWHERE - NO MEANING
> AND NO RESUME BRANCH.** It is now defined, because a state with no meaning in
> a ledger that is resumed after a crash is how a part gets processed twice.
>
> | | |
> |---|---|
> | **meaning** | Admitted to the run and **not yet committed**. No spend, no socket, no file. It is the only state that exists purely because the run is ordered. |
> | **written when** | At admission, in the same atomic write that records the reservation attempt. |
> | **resume** | **`queued` is safe to replay.** It carries no commit and nothing billed, so re-admitting every `queued` part on restart is correct and idempotent. This is exactly why it is distinct from `reserved`, which is NOT safe to replay. |
> | **never** | A `queued` part is never settled, never counted in `committed`, and never reported as `PAID_UNKNOWN`. It has not been sent. |
>
> **Unit completion.** Also missing until now, and it is the rule the whole
> resume path hangs off: **a unit is complete when every part it owns is in
> `settled` or `lost`, and the unit's assembled note exists on disk.** A unit
> with any part still `queued`/`reserved`/`sent` is **not complete** and its note
> is not emitted. Partial transcripts are never published as notes — the same
> principle that makes a 504 body not a transcript (below) applied one level up.
```

**`reserved`** means: spend committed, **and** nothing has been sent.
**`sent`** means: the socket opened. These are different facts and the plan must
record which one happened *before* the crash can erase it.

### 5.3 The single global spend ledger `[R1]`

Rev 0 said "reserved under `flock`" with **no file and no path**, while every
named artifact was per-**unit**. A per-unit lock cannot serialise a global sum:
16 workers can each read a stale total and jointly overshoot.

```
LEDGER = /data/nhb/_meta/spend.json     PER ACCOUNT:
    {"accounts": {
        "<account_id>": {"committed":USD,"settled":USD,"lost":USD,"released":USD}},
     "totals":      {"committed":USD,"settled":USD,"lost":USD,
                     "released":USD}}      [F34] FIXED - the field was OMITTED
                     while every per-account object declared it, so the gate
                     formula in the next paragraph was stated over a field the
                     schema did not have.
    [B11] section 2.2 asserted a per-account ledger and a per-account gate; this
    section still described a single global object, so an implementer following
    IT would build one pool and the second key would never be used.
LOCK   = /data/nhb/_meta/spend.lock     flock, held across READ-CHECK-WRITE
```

Commit and settle are each one atomic ledger mutation under that one lock:

```
commit:  committed += cost        settle:  committed -= cost;  settled += actual
release: committed -= cost          lost:    committed -= cost;  lost += actual
                                   released += cost
                                   [F34] A `reserved` part is released ONCE.
                                   Compare-and-set inside the flock: read
                                   `released`; if this part_id is not already
                                   in the released set, add cost and add
                                   part_id. Two resume passes over one part
                                   would otherwise double-count, and a
                                   double-counted release frees budget that was
                                   never spent - which is how a hard stop
                                   becomes a soft one without any code
                                   appearing to change.
                                   [B11] section 5.4's resume table requires a
                                   release for a part that was committed and never
                                   sent. Without this mutation that amount is either
                                   double-counted forever or never returned.
```

**Ledger reconciliation is derived, never authoritative** — `bin/rescan.py`
rebuilds it from `receipt.json` parts, and **receipts win** on conflict. This
keeps single-authority (no desync) while giving the global sum a named home.

### 5.4 The resume branch — explicit, because ambiguity here costs money `[R1]`

**Three durable bits per part, each written atomically before the fact it
describes** — round 2's central finding was that two of them did not exist:

```
status = reserved              committed, socket NOT open
status = sent                  socket OPEN - written BEFORE the request bytes leave
status = response_complete     body's last byte fsynced to disk
http_status = <int>            recorded in the same atomic write as sent
```

`status` and `http_status` are both required. A **504 body, a 429 body, a 402
body and a 400 body are all "a response"** — without `http_status` the table
settled a 504 as a completed transcription and assembled it as a transcript.
**[F35] "ATOMIC" WAS ASSERTED THREE TIMES AND SPECIFIED NOWHERE.** The word
appears in "Atomic write+rename throughout", in "a *single* receipt write", and in
the three-durable-bits table. None of the three named a syscall. That matters
because the §5.4 recovery table's central claim — *a kill after `sent` leaves
`sent`* — rests on a durability step nobody wrote. The four steps, named:

1. write the temp file at `<path>.tmp` in the **same directory** as the target
   (a cross-directory `rename` is not atomic on NTFS and is a copy on some mounts)
2. `f.flush()`, then `os.fsync(fd)` — flush pushes to the OS, **fsync pushes to
   the device**. Without fsync, a power loss loses the bytes and `sent` is a lie.
3. `os.replace(tmp, path)` — atomic on POSIX **and** on NTFS via `MoveFileEx` with
   `REPLACE_EXISTING`. It is NOT atomic on SMB or a 9p share, which is a further
   reason the receipt ledger lives on the VM's ext4 and not on the shared mount.
4. `fsync` the **containing directory**, so the rename itself is durable. This is
   the step everyone skips, and without it the new name can be lost after a crash
   even though the bytes survive.

**The receipt is the unit of durability, and it is one file.** `status`,
`http_status`, the per-account committed amount, the part hash and the request
placeholder land in **one** `os.replace` — never two, never a batch. A receipt
half-written is worse than one not written, because it is indistinguishable from
one that was written before the socket opened.

`response_complete` exists because §7.2 streams the body to disk, so **a partial
file is the normal mid-run state**: without it, `sent` + partial is
indistinguishable from `sent` + still in flight, which is the exact ambiguity
this table was written to eliminate.

| On disk | Meaning | Action |
|---|---|---|
| no part file | nothing happened | redo. No spend incurred. |
| `reserved` | committed, **never sent** | release the commit, re-reserve, submit. No spend incurred. |
| `sent`, no file, `http_status` unset | in flight when the process died | `PAID_UNKNOWN`. **Never auto-resubmit.** Operator decides. |
| `sent`, **partial** file | response truncated | `PAID_UNKNOWN`. The prefix is not a transcript. Operator decides. |
| `sent`, `http_status` **402** | **credit exhausted. NOT BILLED.** | **Re-route the WHOLE PART to the secondary** per §2.2. Do **not** touch `lost`. `committed` is released, re-committed against the secondary's ledger, resubmitted. **[ R4-T1.2]** |
| `sent`, `http_status` **429** | **rate limited. NOT BILLED, and retryable.** | **Retry with exponential backoff, base 2 s, cap 60 s.** Not terminal. Not `lost`. **[ R4-T1.2]** There was previously **no 429 path anywhere in this document** — and a 429 is the single most likely transient on a 25-way run. |
| `sent`, `http_status` **400** | **malformed request. NOT BILLED.** | Re-prepare from the receipt and resubmit. Not terminal, not `lost`. | `[ R4-T1.2]` |
| `sent`, `http_status` **504 / timeout / truncated** | vendor gave up **after** accepting the bytes | `PAID_UNKNOWN`, then settled as `lost`. **This is the only genuinely-paid non-200.** |

> **[ R4-T1.2] THIS WAS A WRONG *RULE*, NOT A WRONG NUMBER, AND IT IS THE MOST
> SERIOUS DEFECT FOUND IN FOUR ROUNDS.** `lost iff (http_status != 200)` made
> **402, 429 and 400 terminal, BILLED, unrecoverable** corpus losses — all three
> are **unbilled**, and two are recoverable. It also contradicted §2.2's own
> instruction to re-route a 402 to the second account, so an implementer
> following §5.4 never executed §2.2's routing at all.
>
> The damage compounded: `lost += actual` charges the ledger for money never
> spent, which **corrupts V10 in the direction that hides the breach**, and
> §2 runs at the documented ceiling with **zero headroom**, so one 429 storm
> would permanently delete content under Constraint 7 and consume the headroom
> that would have finished the run.
>
> **The distinction is billing, not status code.** Billed: 200, and 504/timeout
> after acceptance. Unbilled: 402, 429, 400. That is the whole rule.
| `sent`, `http_status` 200, `response_complete` | completed | settle, re-assemble. No new spend. |
| any of the above, `status = lost` | declared lost by the operator | terminal. See 5.4a. |

**The one atomic write happens before the socket opens:** `status=sent`,
committed spend, and the request placeholder land in a *single* receipt write.
A kill after that leaves `sent`, which is unambiguously billable. A kill before it
leaves `reserved`, which is unambiguously free.

**Per-part, not per-unit `[R1]`.** Rev 0 said "a unit reaches `submitted` at most
once" while the state machine is per-part — a 3-part unit submits 3 times, so the
invariant as written forbids parts 2..N. Correct form:

> Each **`(unit_id, part_index)`** reaches `sent` at most once.

A resumed unit must **never** re-submit parts already `settled` or `lost`.

### 5.4a When a part becomes `lost` — the rule that did not exist `[R2]`

`lost` was a declared terminal state, a ledger mutation, a §5.5 preflight input
and a V10 input — with **no section stating when it happens**. Round 2 caught it.

```
lost  iff  (http_status is set AND http_status != 200)
      OR  (a truncated response body after the socket closed)
      OR  (operator decision, recorded as operator_lost_at with a timestamp)
```

**`lost += actual` needs a duration for a part whose response never arrived, and
`metadata.duration` does not exist for it.** The estimation rule is therefore
explicit and conservative — reserve, never understate:

```
actual_for_lost = the part's DECODED PCM seconds, recorded at remux time
                  (decoded length, per §7.1 - never a container header)
```

That figure is already on disk in the part's own receipt, so the money gate never
depends on an out-of-band operator estimate. **The operator's decision is to
accept the loss, not to price it.**

### 5.5 The preflight gate — one formula, everywhere `[R1]`

```
(totals.committed + totals.settled + totals.lost) + cost > SPEND_HARD_STOP_USD
    ->  stop, do not submit
AND chosen_account.committed + cost <= that account's own $200
    ->  else route the shortfall to the secondary account (see 2.2)
```

Rev 0 omitted `lost`, so headroom already consumed by 504s was invisible to the
gate while V10 counted it. **Asymmetric accounting between gate and assertion is
the bug.** `lost` lives in the §5.3 ledger.

---

## 6. Fetch — serialised, watched, kernel-capped `[R1]`

### 6.1 Route

Per-file only, into `fetch_mnt/` (the loopback). **Never `timeout(1)`** — `timeout`
does not stop megacmd; a probe silently pulled 4.0 GB that way.

`mega-get` names its output after the **verbatim source file** with the extension
appended (`Vimeo gif thumbnail custom code.pdf`), **not the handle**. Fetch into
an **empty per-handle directory** and take whatever single file lands. **Never
infer fetch failure from the absence of an expected filename** — that inference
reported 4/4 failures while the route worked.

### 6.2 Watcher

`partial > threshold` → SIGKILL + `rm` + `FETCH_OVERRUN`.
No growth 120 s → `mega-cancel --all` + `FETCH_STALL`.
After any kill/cancel: `mega-cancel --all`, watch 60 s, **assert zero growth**
(server-side transfer survives client death). **[R4-8.33] ONE WAIT: 60 s.**

### 6.3 Loopback lifecycle — the missing deletion point `[R1]`

**Build the loopback at PIPELINE START and assert writability before admitting
any work.** A loopback mount does not survive a reboot, and the pipeline runs as
`azureuser` while `mkfs.ext4` produces a **root-owned** mount:

```
truncate -s 4G /home/azureuser/fetch.img
sudo mkfs.ext4 -q -F -m 0 /home/azureuser/fetch.img
sudo mount -o loop /home/azureuser/fetch.img /home/azureuser/fetch_mnt
sudo chown "$(id -u):$(id -g)" /home/azureuser/fetch_mnt      # REQUIRED
sudo chmod 775 /home/azureuser/fetch_mnt                     # REQUIRED
test -w /home/azureuser/fetch_mnt || { echo "LOOPBACK NOT WRITABLE"; exit 1; }
```

> `mkfs.ext4 -m 0` clears reserved **blocks**, not **directory ownership**. Without
> the `chown`, every fetch fails `EACCES` while *looking* like a cap failure. This
> cost two false readings during the W0-Cap run itself — test 3 returned
> "Permission denied" and test 5 returned `Write not allowed`, both of which the
> first verdict function accepted as cap behaviour.

**Measured cap behaviour** (`evidence/probes/nhbplus-w0-cap-2026-10-15.json`): a full
loopback makes `mega-get` exit **232 "Insufficient disk space" in 0 seconds**, with
no host spill. It appears to **pre-check** and refuse rather than fail mid-transfer,
so a full loopback never produces partial audio.

> This **contradicts round 1's premise** that megacmd is "the only unkillable
> operation". `timeout(1)` genuinely cannot stop it, but the kernel can, and does.
> The overrun watcher is still required — the cap stops the *write*, it does not
> reap the *process*.

**Concurrency.** **[F18] NOT A CONSTANT.** `FETCH_CONCURRENCY` is the predicate in §2 — no literal appears in its definition, and none appears here. (An earlier revision of this same bullet block opened with the literal `FETCH_CONCURRENCY = 6`, which defined the thing as a constant and then described it as a predicate two lines later.)

- **Delete the raw at the remux receipt.** Not *before* the next fetch is admitted:
  that phrase serialises the lane to effective concurrency 1 and contradicts
  `FETCH_CONCURRENCY` in the same bullet block. Deletion happens at remux
  receipt; concurrency is bounded by the admission arithmetic below, not by
  serialising the lane.
- **Gate fetch admission** on
  `free(fetch_mnt) >= Σ(in_flight REAL bytes) + REAL bytes(next) + 64 MiB`.

  **And this IS the concurrency control `[R2]`.** Round 2 showed a fixed
  `2 ×` was unsatisfiable; measuring the real population showed a fixed constant
  is too, and worse:

  ```
  usable loopback 3,936 MiB (W0-Cap, measured)
  a 2 GiB sentinel's true size is unknown to a ±0.5 quantum band, up to 2,560 MiB

    small  (<100 MiB)            max 38 in flight   [F17] off-by-one, FIXED
      39 x 100 MiB = 3,900 MiB against 3,872 MiB admissible. 38 x 100 = 3,800.
    mid    (100-512 MiB)         max  7
    large  (512-1536 MiB)        max  2
    2 GiB sentinel (1536-2560)   max  1
  ```

  `FETCH_CONCURRENCY = 6` would need 6 × 2,560 = 15,360 MiB for six large units.
  **W0-Cap proved the cap EXISTS. It never proved that any fixed concurrency is
  ADMISSIBLE across a corpus spanning 20 MiB to 2 GiB.** One predicate yields 1
  for large units and up to 39 for small ones.

  **Admission must use REAL bytes.** For the 73 sentinels the real size is unknown
  until fetched — `dvcEDToK` declared 2 GiB and is actually 1.50 GiB — so reserve
  the display band's **upper bound**, never the declared value.

  > **[B25] AND THE REAL BYTES DO NOT EXIST YET.** For a sentinel the control
  > cannot be evaluated before the irreversible act it exists to bound — which is
  > the same shape as the sentinel bug itself: a predicate that reads as
  > load-bearing and is not. Two stages:
  >
  > ```
  > ADMIT   on the display-band UPPER BOUND  (known before the fetch)
  > VERIFY  on arrival, from the real file on disk
  >         real > upper_bound * 1.10  ->  FETCH_OVERRUN, kill, rm, re-plan
  > ```
  >
  > Admission is therefore conservative by construction, and the post-fetch check
  > is what actually enforces the cap. The predicate alone would not.

  **The `2 ×` was an off-by-one for a loopback whose purpose is to hold one
  copy at a time**, and is replaced by the size-adaptive predicate above.

  > **[B2] The 3.00 GB unit that motivated it DOES NOT EXIST IN SCOPE.** The file
  > is `EyFE2DpD` at 3,221,225,472 B = **3 × 2³⁰ exactly, so it IS a sentinel**,
  > and it is a **never-fetched MP4 alternate**. That call's fetched primary is
  > `03UW2LCY` at **151 MiB**. Largest non-sentinel audio in scope is 1.0654 GB.
  > The `2 ×` was removed on the authority of a phantom.
  When `declared` is a sentinel, reserve the **2,560 MiB** display-band upper
  bound above. **[B3] A 512 MiB reserve also appeared here, contradicting the
  2,560 MiB figure 20 lines above - a 5x disagreement inside one block on the
  safety-critical number. Measured `dvcEDToK`: declared 2 GiB, real 1.50 GiB, so
  512 MiB was 3x under.**
- **Reap partial files** after any failed fetch — a refused transfer still leaves
  one 0-byte partial behind.
- **Name `LOOPBACK_ENOSPC`** as a state distinct from overrun/stall.
  **[F19] NAMING IT IS NOT HANDLING IT.** For three rounds this line named the
  state and stopped. The recovery, which is now specified:

  | | |
  |---|---|
  | **detect** | `mega-get` exit **232**, or `OSError.errno == ENOSPC` on write. Neither is a retryable network error and neither is an overrun. |
  | **classify** | Not `lost`. **Not `reserved`.** The part is re-fetchable in full and nothing was billed. `LOOPBACK_ENOSPC` is a *fetch-side* state and never reaches the STT ledger. |
  | **release** | Free the reservation immediately. Holding a reservation for a unit that cannot be fetched makes the budget tighter for units that can. |
  | **drain** | **Drain the whole in-flight fetch set before retrying.** A single ENOSPC means the cap was consumed by *concurrent* admissions; re-admitting one fetch while 16 are still writing is the same failure again. |
  | **re-queue** | Re-admit **once** at the head of the queue, after the loopback's used bytes are re-measured (`df`, not the admission estimate). |
  | **backoff** | Exponential, base 2 s, cap 60 s. Not a constant. |
  | **give up** | **3 consecutive failures on the same part → the run STOPS.** Not a skip. ENOSPC is a cap defect; skipping it converts a system-level fault into a silent hole in the corpus. |
  | **evidence** | Write a `LOOPBACK_ENOSPC` receipt row with `used_bytes`, `in_flight`, `declared`, `actual`, and the `mega-get` exit code. W0-Cap measured this failure in **0 s**, so it is cheap to detect and must be cheap to diagnose after. |

### 6.4 The overrun threshold must not consume a sentinel `[R1]`

**73 of 230 units carry placeholder sizes** (Constraint 6). Fed those:

```
declared 1 GiB -> killed above 1.100 GiB   (37 units)
declared 2 GiB -> killed above 2.200 GiB   (36 units)
```

**73 units — nearly a third of the corpus — would be SIGKILLed and deleted as
false overruns**, on traffic that is perfectly legal, by a safety system that
would log it as working correctly. The per-target sizes also over-sum the
folder-exact total by **10.79 GB (7.4%)**, confirming they are display values.

**[ R4-T1.3] DETECTION WAS WRONG IN KIND, AND CONSTRAINT 6 MANDATED THE FIX
THAT WAS NEVER APPLIED HERE.** This said `bytes % (1 << 30) == 0` is the test
and that the other **157 "genuine" values** are real. **They are not.**

R4 re-measured across **every** declared size, primaries and alternates:

| test | count |
|---|---|
| `bytes % 1024 == 0` | **440 / 440 — every declared size in the corpus** |
| `bytes % (1 << 30) == 0` | 156 / 335 |

Ground truth from the files actually downloaded: `wiUyTRZb` declared
397,410,304 B (**KiB-exact**) vs actual 397,487,264 B (**not** KiB-exact).

**So there is no un-quantised subset by this test.** GiB-exactness found 73
primaries and called the rest genuine; the rest are quantised at the KiB
boundary — 30 bits coarser than the test assumed.

**THE FIX, NOW APPLIED:**

```
sentinel(b) := (b % 1024) == 0        # NOT (b % (1<<30)) == 0
```

**The `max()` in this section's threshold is dead code and is deleted.**
`threshold = max(1.10 * declared, declared + 0.5 * quantum)` takes the `1.10x`
arm only when `declared >= 5 * quantum`. For all 157 non-sentinel units
`declared < 5 * quantum`, so **the band arm always wins**. For `pjFQiLQQ`
(90 MiB declared, 512 MiB quantum) the effective threshold is **353 MiB — 3.9×
its declared size**, while the table below says `×1.10` and describes a branch
that never executes. **One threshold, stated once: the band arm.**

```
if declared is sentinel:
    disable the overrun check for this unit entirely
    rely on the 4 GiB kernel ENOSPC cap  (the real safety system)
    log  DECLARED_UNKNOWN
else:
    display_unit = the quantum MEGA rounded its displayed size to, per format.
                MEGA shows "1 GB"/"2 GB"/"3 GB" for a range of true sizes; the
                rounding band is +/- 0.5 of the displayed quantum. 1 GB files use
                512 MiB, 2 GB and 3 GB files use 1 GiB.
threshold    = max(1.10 x declared, declared + 0.5 x display_unit)
```

**Never kill on a rounded baseline.**

---

## 7. STT

### 7.1 Remux and segment — the majority path

`ffmpeg -vn -c:a copy` every unit. **133 of 230 are MP4.**

**Output container: `.mka`, never `.m4a`.** Verified 2026-10-15. `.m4a` is an
MP4 container and **cannot hold an MP3 elementary stream** — it fails rc=234
*"Could not write header (incorrect codec parameters)"* for **97 of 230 units**.
`.mka` (Matroska audio) carried every sample, MP3 and AAC alike.

> **[B23] NOW VERIFIED AT THE VENDOR, which is where it mattered.** The only
> `.mka` ever *submitted* had been AAC, so the container that rescues **97 MP3
> units** was unverified at the Deepgram boundary — and under Constraint 7 an
> HTTP 400 class there is 97 paid-and-unrecoverable failures. A 5-minute slice of
> a real corpus MP3, remuxed to `.mka`, submitted: **HTTP 200, 911 words, 300.0 s.**
> **$0.03 to close.**

> **THE REMUX IS MANDATORY, NOT AN OPTIMISATION `[R2]`.** Submitting the **raw
> 1,539 MB MP4** of the corpus's longest call **did not complete** — it timed out
> after >1,800 s. The remuxed 280.7 MB `.mka` of the same audio completed in
> **105.1 s**. Bandwidth was never the difference: the remuxed file uploaded at
> **150.8 MB/s**, so 1,539 MB is ~10 s of transfer. What differs is that `-vn`
> strips the **h264 video track**. 133 of 230 units are MP4; under Constraint 7 a
> failed submission is **paid and unrecoverable**, so this is a correctness
> requirement, not a size one.

> The plan did not specify a container at all. `.m4a` is the conventional
> audio-only extension, so an implementer would reach for it and fail 42% of the
> corpus with an error that reads like a codec fault rather than a container fault.

**Bit-exactness** — verified by SHA-256 over decoded PCM:

| codec | result |
|---|---|
| MP3 | **EXACT**, identical hash over 711 MB and 994 MB of PCM |
| AAC | near-exact — ~10 KB differs in 1.1 GB (encoder delay on repack) |

Claim bit-exactness for MP3; claim **near-exact** for AAC.

**Size cut — the plan's "~85%" was wrong two ways:**

| format | units | measured cut | why |
|---|---|---|---|
| MP4 | 133 | **+78.5% to +81.8%** | the video track is most of the file |
| MP3 | 97 | **−1.6% — the output is LARGER** | no video to strip; only repackaging |
| **corpus** | 230 | **146.39 → 42.17 GiB (71.2%)** | |

The real saving is **104.21 GiB, not the 124.43 GiB** an 85% assumption implies.

**Do NOT transcode to 16 kHz PCM.** Measured at **−166% size on MP3** — a 133.6 MB
source becomes 355.9 MB of `s16le`. 97 of 230 units are MP3. Any 16 kHz path must
use FLAC or Opus, never WAV.

> `-ac 1 -ar 16000` are **output** options and must follow `-i`. Placed before it
> they parse as input options and ffmpeg fails *"Option sample_rate not found"*.

**Size guard on the remuxed output `[T5 #5]`. [F20] THE OLD THRESHOLD WAS DERIVED
FROM A SENTINEL AND THE "NOT SUBMITTED" CLAIM IS NOW FALSE. BOTH REPLACED.**

The old text estimated the largest remuxed unit at "~400 MB (a 2 GiB sentinel
source less the measured ~80% MP4 cut)". That is a **sentinel display value
consumed as a threshold**, which Constraint 6 forbids — the sentinel defect is the
recurring one in this project and it has now masqueraded as a measurement four
times. It is also arithmetically inapplicable: MP3 has a **negative** cut
(−1.6%), so the measured ~80% MP4 cut cannot describe an MP3 at all.

What is actually true, from the repo:

| | |
|---|---|
| largest remuxed unit **ever submitted** | `dvcEDToK`, **280.7 MB**, HTTP 200 — **[F1-CORRECTION] not `wiUyTRZb`, which was never submitted** |
| its margin at 204.3 min | **5.71×** measured — **on the 47th-ranked unit.** The worst case is untested. |
| upload rate measured | 150.8 MB/s → ~2.5 s of transfer |
| the guard that matters | **not a size threshold.** It is `SEGMENT_SEC`, and `SEGMENT_SEC` is dead code under a 2 GB `CAP_BYTES` the 385 MiB maximum cannot reach (T6 #8). |

**So the size guard is withdrawn rather than re-derived.** The honest measured
maximum is **383.7 MiB / 402.31 MB** — **[R4-8.10] this line said 385.1 MiB /
403.8 MB while §7.2 said 383.7 in the same document.** `wiUyTRZb`'s remuxed
`.mka` is 402,307,896 B = 383.67 MiB. It is an **MP3, not a sentinel MP4**; and
since the largest remuxed unit sits at 19% of `CAP_BYTES`, a size guard has
nothing to catch. `CAP_BYTES` stays, `SEGMENT_SEC` stays, and the branch is
recorded as never taken rather than dressed up as a live control.

**Segment** when remuxed ≥ `CAP_BYTES` → `ffmpeg -f segment -segment_time
SEGMENT_SEC`. Single-part otherwise. **Every part gets its own receipt entry.**

**The cost gate MUST read decoded PCM length, never a container header.**
Deepgram bills the decoded duration. Measured: `pjFQiLQQ`'s header claims 4,958 s
while its decoded PCM is **5,431.8 s (+9.54%)** — a header-derived reservation is
under-reserved by exactly the header's error, per part, silently.

> A 10-MP3 stratified sample then confirmed the **manifest** durations are sound
> (all within 0.02% of decoded truth), so the $150.56 forecast stands.
> `pjFQiLQQ` slipped through only because its recorded `dur_s` was 0 — the exact
> class of unit the check exists for.

#### 7.1a Channel handling — DETECT per file, never choose corpus-wide `[R1]`

Deepgram bills stereo at **×2**. But **every stereo file measured is dual-mono**
(§0 D3), so downmixing is lossless and worth **$26.98**. Both pure options are
worse than measuring: unconditional `-ac 1` would destroy channel separation on
any per-participant file; unconditional stereo pays 2× on files that gain nothing.

**[F-MEASURE 2026-10-15] THE CHANNEL MEASUREMENT IS A FULL DECODE AND AT CORPUS
SCALE IT IS THE WHOLE RUN.** Measured in take 3: `astats` over the complete
275.93-min unit took **4m28s of 111% CPU on one core = 61.8x realtime.** The
corpus is 35,300 min of audio:

| | |
|---|---|
| corpus-wide full decode at 61.8x | **567 core-hours** |
| on this 2-vCPU VM | **284 wall-hours = 11.8 DAYS** |
| Azure cost of that alone | **$32.61** |
| same measurement over a **90 s window** | **4.6 minutes** |
| section 7.1a remux (`-c:a copy`, stream copy, no decode) | 0.26 h |

**The window is the entire difference between 11.8 days and nothing.** §7.1a
calls this "one extra ffmpeg pass per part"; on the corpus it is the dominant
cost in the pipeline and nobody priced it. **A 90-second window classifies the
L/R relationship** — dual-mono is dual-mono from the first minute — so the
full decode buys nothing. Specified as a window below.

**[F7] GUARD BEFORE MEASURING.** `pan=mono|c0=c1` has no `c1` on a mono input
and errors. **82.1% of sampled minutes are mono**, so the unguarded block below
fails on the majority of parts.

```
channels == 1  ->  MONO.  No measurement, no second pass, commit once.

rms_L  = ffmpeg -i part  -af "pan=mono|c0=c0,astats"        -f null -
# [F-MEASURE] ^ THE pan FILTERS BELOW ARE THE BUG, AND I REPRODUCED IT.
# Running `pan=mono|c0=c0` BEFORE astats collapses the stream to mono, so
# "RMS difference dB" has no second channel left to differ from and reports
# 0.0 - which then reads as INDEPENDENT on a file whose L and R are
# bit-identical. It happened to me: pjFQiLQQ showed L = R = -28.585805 dB and
# the parse returned INDEPENDENT_KEEP_STEREO_2x. The correct classifier is:
#   -t 90 -i part -af astats                      (read RMS difference dB)
#   -t 90 -i part -af "pan=mono|c0=c0-c1,astats"  (read RMS level of L-R)
# and branch on whether L-R carries ANY signal at all, which does not depend
# on dB rounding the way a difference-in-dB comparison does.
rms_R  = ffmpeg -i part  -af "pan=mono|c0=c1,astats"        -f null -
rms_D  = ffmpeg -i part  -af "pan=mono|c0=c0-c1,astats"     -f null -
delta  = rms_D - rms_L        (dB)
```

```
channels == 1  -> MONO.  No test, no second pass, commit once.
                 82.1% of sampled minutes are mono, and `c1` does not exist on a
                 mono input - pan=mono|c0=c1 would ERROR on the majority of parts.

delta <= -60   -> BIT_IDENTICAL.   -map_channel 0.0 -c:a copy.  LOSSLESS, keeps
                                         §7.1's bit-exactness claim. Saves money.
> **[R4-8.60] [B23] AND [B24] REST ON `pipeline/out/canon-probes.json`, WHICH
> HAS NO `date`, NO `handle`, NO HASHES AND NO MEASUREMENT** — and it sits
> **outside** `evidence/probes/`, outside the pack every other claim here cites.
> Two claims unblock real money: the `.mka` container for 97 units, and the
> lossless `-map_channel` downmix that produces the ENTIRE saving. Both rest on
> one boolean (`B24_map_channel_lossless: true`). **[R4-8.18]** and both measured
> MP3s ran `channels_out: 2` — the copy path WITHOUT the downmix — so **the
> downmixed path is the one thing never probed.**
> **[RESOLVED 2026-10-15 — NOW PROVEN BY HASH, $0.00.]**
> `nhbplus-w0-aclose-2026-10-15.json`. On `wiUyTRZb.mka` (the corpus maximum,
> 2 channels), 600 s window:
>
> ```
> L                sha256 = 58c695abde872bfc2da405eefb95edf300d684e9e616f6affae04dc57bc6b3d4
> R                sha256 = 58c695abde872bfc2da405eefb95edf300d684e9e616f6affae04dc57bc6b3d4
> -ac 1 downmix    sha256 = 58c695abde872bfc2da405eefb95edf300d684e9e616f6affae04dc57bc6b3d4
> ```
>
> **All three are the same string.** No tolerance, no RMS threshold, no dB
> comparison, no rounding in the path — either the bytes match or they do not.
> **The $34.85 saving is now PROVEN, not asserted.**
>
> **Scope stated precisely:** proven for a **bit-identical dual-mono** source,
> where −(L+R)/2 = L is arithmetic. **It is NOT proven for genuinely-stereo
> audio, and the same probe found some** — see the W0-ChannelShare row. For
> those, `-ac 1` IS a downmix and is NOT lossless, which is exactly why §7.1a's
> INDEPENDENT/AMBIGUOUS branches exist and why they must not be deleted.
>
> [B24] VERIFIED: SHA-256 of the decoded
                                         PCM is IDENTICAL before and after -
                                         994.6 MB both sides. The standing worry
                                         was that a copy codec cannot extract a
                                         channel from JOINT-STEREO MP3; on the
                                         corpus's own joint-stereo file it does
                                         exactly that, losslessly. The worry was
                                         wrong and is withdrawn.
delta <= -40   -> EFFECTIVELY_DUAL_MONO.  -ac 1 RE-ENCODES (a copy codec cannot
                                         change channel count).  §7.1's
                                         bit-exactness claim is WITHDRAWN for
                                         these parts. Encoder and bitrate MUST be
                                         named: -c:a libopus -b:a 32k, mono 16k.
delta >= -20   -> INDEPENDENT.     KEEP STEREO.  Per-participant audio; downmixing
                                   would force acoustic diarization instead of
                                   channel-derived attribution. Pay the 2x.
otherwise      -> AMBIGUOUS.      [F22] TWO OF FIVE BRANCHES ARE UNOBSERVED.
   `INDEPENDENT` and `AMBIGUOUS` fired on **0 of 3** stereo files — all three
   were dual-mono, so the delta was uniformly 0.00 dB and neither branch was
   ever taken. They are specified, not validated. The corpus-wide stereo share
   is also UNKNOWN (3 of 230 measured), so the branch that bills 2x has no
   measured population behind it. That tail is priced in §2.2's keep-stereo
   line, not here.       keep stereo, flag AMBIGUOUS_CHANNELS for the
                                   operator. NEVER silently decide.
```

**Round 2 caught that §7.1 and §7.1a contradicted each other.** §7.1 mandates
`-c:a copy` and claims bit-exactness; §7.1a mandated `-ac 1`, which cannot be
done with a copy codec. Every time the downmix rule fired, the fidelity claim was
void and the output became a lossy re-encode at an unnamed encoder. The split
above makes the two cases explicit: two of three measured stereo files were
BIT_IDENTICAL and are downmixed **losslessly with the copy codec intact**; only
the -46 dB case re-encodes, and it says so.

One extra ffmpeg pass per part **[F21] — FOR A STEREO PART ONLY, AND THREE, NOT
ONE**: the pass is `-map_channel`, but `channels == 1` takes the MONO branch and
runs none of it, and the stereo branch runs the `astats` measurement **three**
times (rms_L, rms_R, and the difference signal) before deciding. A mono part is
one commit and no measurement; a stereo part is up to four passes. `channels` goes in the receipt, and the
downmix decision is recorded beside it — so the money path and the fidelity path
are auditable together.

> **Do not invoke ffmpeg with `-v error` around `astats`.** It writes at `info`
> level, so every reading silently returns `-inf` — indistinguishable from a silent
> input. This cost one probe run and is recorded in the evidence artifact.

### 7.2 Submit — ONE path, sync. The async branch is withdrawn.

**W0-AsyncContract FAILED 2026-10-15: `ASYNC_ALLOWED = False`.**
`evidence/probes/nhbplus-w0-asynccontract-2026-10-15.json`

```
POST /v1/listen, 2-min clip  -> keys ['metadata','results'], request_id None,  1.6s
POST /v1/listen, 68-min clip -> keys ['metadata','results'], request_id None, 32.4s
```

Both sizes return **inline results with no `request_id`**. Short-file inline
behaviour was tested and excluded — a 68-minute file behaves identically. **There
is no async job, therefore no re-GET, therefore no free recovery on any path.**

**The larger finding: the 10-minute 504 ceiling is unreachable by this corpus.**

**MEASURED, not calculated `[R2]`.** The longest call in the corpus was
submitted on its own and timed:

```
FIRST PROBE, SUPERSEDED - [F1] retained as one line, not a block.
  dvcEDToK, 204.3 min, 280.7 MB remuxed .mka, HTTP 200 in 103.2 s, total
  105.1 s -> a 5.7x "margin". dvcEDToK RANKS 47th OF 229 BY DURATION. It is not
  the worst case and its margin means nothing. 46 calls are longer. Its real cost
  on metadata.duration is $1.14, not $1.54 - 204.31 min x $0.0056.
  Three artifacts had joined two different files: the 275.9 min figure belongs to
  wiUyTRZb, the 1,614,043,424 bytes belong to dvcEDToK. THE REAL ONE IS BELOW.
```

**THE REAL WORST CASE, measured 2026-10-15 — W0-SyncCeiling genuinely CLOSED.**

`dvcEDToK` had been picked because its manifest `dur_s` is `None`, so it never
appeared in the duration-sorted list used to choose the worst case.

> **⛔ [F1-CORRECTION 2026-10-15] THE BLOCK THAT STOOD HERE WAS NEVER MEASURED.**
> It read `wiUyTRZb · 275.9 min · HTTP 200 in 156.2 s · MARGIN 3.8x · words
> 51,787`, and **every one of those figures appears in no artifact in
> `evidence/probes/`** — verified by grep across all 41 files. The declared byte
> count, the 383.7 MiB remux, the 156.2 s, the 106× and the word count are all
> unevidenced. They were produced by re-attributing `dvcEDToK`'s measurement to
> the unit that *should* have been measured. **A fix that invents the number it
> is fixing is worse than the defect, because it removes the reason to go and
> measure.**
>
> **WHAT IS MEASURED, and it is the only thing:**
>
> ```
> unit       dvcEDToK, 204.3 min / 12,258.603 s — RANK 47 OF 229
> submitted  remuxed .mka, 294,302,207 B (the path §7.1/§7.2 actually take)
> upload     1.9 s at 150.8 MB/s
> response   HTTP 200 in 103.2 s
> total      105.1 s   against a 600 s ceiling
> MARGIN     5.71x at THIS UNIT   realtime 119x   words 37,372
> ```
>
> **5.71× is measured and it does not bound the corpus.** 46 calls are longer
> than the unit it was measured on.
>
> **TAKE 3 — MEASURED 2026-10-15 ON THE ACTUAL CORPUS MAXIMUM.**
>
> ```
> unit       wiUyTRZb, 275.93 min / 16,556.207 s  — THE ACTUAL CORPUS MAXIMUM
> source     mp3, 397,487,264 B, 48 kHz, 2 CHANNELS, with an mjpeg video stream
> submitted  remuxed .mka, 402,307,896 B  (-vn -c:a copy, no transcode)
> response   HTTP 200 in 182.757 s against the 600 s ceiling
> MARGIN     3.28x        realtime 90.6x        words 51,786
> request_id 01a13ec6-9208-7c90-a68d-0209a8e6be33
> cost       $1.55        (16,556.207/60 x $0.0056)
> ```
>
> **3.28× is the true margin on the true worst case.** Every figure this gate
> previously carried for `wiUyTRZb` was invented, and measurement corrected all
> of them:
>
> | invented | **measured** | error |
> |---|---|---|
> | 156.2 s | **182.757 s** | −15%, and in the **optimistic** direction |
> | 3.8× margin | **3.28×** | −14% |
> | 51,787 words | **51,786** | **off by ONE** |
> | 106× realtime | **90.6×** | −15% |
> | 383.7 MiB remuxed | **383.7 MiB** | the one figure that survived |
>
> Being wrong by one word in fifty thousand is indistinguishable from being
> right. **That is exactly why an unevidenced number is worse than no number.**
>
> **Header and decoded agree on this unit** (16,556.208 vs 16,556.207, 1 ms) —
> the opposite of `pjFQiLQQ` at +9.54%. **The header/decoded gap is per-file, not
> a corpus-wide constant**, which is why §7.1 requires decoded and a correction
> measured on one unit does not transfer to another.
>
> **The remux made this file BIGGER:** +1.21% (397.5 MB → 402.3 MB). Container
> overhead dominates for MP3, corroborating the measured **negative** MP3 cut of
> −1.6% and the opposite sign to the ~80% MP4 cut.
>
> > **[ R4-T1.11] A TAKE-2 PARAGRAPH SURVIVED INSIDE THE TAKE-3 BLOCK AND
> ASSERTED THE WRONG GATE STATE.** It read *"Until it is run, W0-SyncCeiling is
> **OPEN**, and §4 reads 🔴 OPEN, not ✅ SATISFIED."* It HAS now been run,
> §4 reads ✅ SATISFIED (take 3), and the artifact says *"GENUINELY CLOSED."*
> **The OPEN sentence is struck.**

**3.28× is measured SOLO. It is not a concurrency margin.** **But the gap it
left has since been filled by measurement, not by hope:**
**[W0-CONCURRENCY25] 25 requests fired simultaneously, the same carrier included,
and it completed in 186.738 s — degradation 1.022×, margin 3.21× under load.**
The solo figure is no longer the operative number. The artifact's other warning
stands and is not withdrawn: **one 3-minute burst is not the full 15-minute STT stage
> **[R4-PROP] This said "25 hours of sustained load" and that was the same 60x
> unit slip a second time.** There is no 25-hour run: the whole run is ~1.4 h and
> the STT stage is 15 minutes.**, and a pass is not a capacity guarantee.
>
> The prediction from `dvcEDToK`'s measured 119× realtime is ~139 s against
> 600 s, which is comfortable — **but that is an extrapolation, and the previous
> extrapolation from this same method produced 273.7×, wrong by 48×.** The
> gate exists to replace an extrapolation with a measurement. Until it is run,
> W0-SyncCeiling is **OPEN**, and §4 reads 🔴 OPEN, not ✅ SATISFIED.

> **The 273.7× was a 60× UNIT SLIP, not an extrapolation error. [B1][B4]** 600 s
> of server time at 126× realtime is 75,600 SECONDS = 21.0 hours. The artifact
> wrote that as 75,525 MINUTES / 1,259 hours. Corrected: 21.0 / 4.6 = **4.57×**,
> which agrees with the measurement. The arithmetic in correct units already
> matched reality — the units were wrong. **This is the same defect as B4**,
> seconds × dollars-per-minute, and it is why a calculated margin is not a
> margin.
>
> **AND THE MEASUREMENT WAS ON THE WRONG UNIT. [B1]** `dvcEDToK` is 204.3 min,
> not the corpus maximum. **46 calls are longer.** The worst case is
> `wiUyTRZb` at 275.9 min. Scaling the measured 105.1 s gives ~142 s →
> **4.2× margin**, not 5.7×. W0-SyncCeiling was **REOPENED** for `wiUyTRZb`.
> **[F1-CORRECTION] It is still open.** The 4.2× is a scaled prediction, and a
> later revision replaced it with an asserted 3.8× that had no artifact behind
> it. Neither is a measurement. It was skipped because
> `dvcEDToK`'s manifest `dur_s` is `None`, so it never appeared in the
> duration-sorted list used to pick the worst case. **[F24] The old closing line
> here RECOMMENDED taking that measurement. It has been taken, at the cost of
> $1.14, and the recommendation is withdrawn.** **A margin calculated for the worst
> case is not a margin.**

| Dissolved | Was | Now |
|---|---|---|
| the sync-cutoff problem | 155 of 188 calls (82.4% of minutes) exceeded the cutoff | **0** exceed it |
| `SYNC_SEG_SEC` segmentation | introduced because 155 calls needed it | unnecessary for all 230 |
| request count | ~3,611 | **~230**, one per unit |
| per-request overhead | open risk in two rounds | moot — no minimum exists |
| R1's $163.30 fallback ceiling | would have stopped the run ~49 h short | **withdrawn** |

**So: one path.** Preflight under the §5.3 lock → commit `COMMIT_COST` → persist
`sent` + placeholder in **one atomic write before the socket opens** → a
Python-streamed POST to `/v1/listen` (**never `curl --data-binary`**, which OOMs at
1.4 GB) → **stream the response body straight to disk**.

Assert **both** paths on arrival: `results.utterances` non-empty **and**
`results.channels[0].alternatives[0].paragraphs` present. Proven shapes:
`metadata.duration` is a plain float; **`paragraphs` lives under `alternatives[0]`,
not `channels[0]`.**

**There is no segmentation fallback.** §2.1 and its four constants
(`SYNC_CUTOFF_SEC`, `SYNC_SEG_SEC`, `SYNC_HEADROOM_SEC`, `REALTIME_SAFETY`) were
deleted on 2026-10-15 — round 2 found §2.1 still live, still asserting that
*"82.4% of the corpus rides this path"* while §7.2 measured **zero** units on it.
`SEGMENT_SEC` survives solely as the §7.1 `CAP_BYTES` guard, which is a
different mechanism.

The only segmentation trigger left is `CAP_BYTES` (2 GB) in §7.1. On the measured
largest unit — **1.54 GB source, 280 MB remuxed** — it should never fire either.
If it does, that is a finding, not a routine path: log it and report it.

> **One measurement would convert the analytical margin into a measured one:**
> submit the longest call in the corpus (275.9 min) alone and record its server
> time. Expected ~138 s against the 600 s ceiling. **$1.54.**

### 7.3 Response durability — the single-shot rule, now proven

> **Constraint 7, CONFIRMED BY PROBE:** Deepgram stores nothing. No async job, no
> `request_id`, no re-GET. **Every submission in this pipeline is single-shot.**

Therefore:

- **The response body must stream to disk as it arrives** — never buffered fully
  in memory, never left only in a pipe. It is the only copy that will ever exist.
- **A 504 or a truncated stream is paid-and-unrecoverable.** Not pending.
  `PAID_UNKNOWN` is **loss acceptance**, not recovery.
- **A TIMEOUT IS NOT A CLEAN ZERO `[R2]`.** The worst-case probe timed out at
  1,800 s and whether it was billed **cannot be determined from here** —
  `GET /v1/balances` returns 404 on this key. A timeout must be classified
  `PAID_UNKNOWN`, never as "nothing spent". The operator may need to check the
  account balance directly.
- Quarantine-then-operator is a correct **anti-double-bill** control. It is **not**
  a spend control — the money is gone before the quarantine exists.

Assembly: concatenate utterances with part offsets, dedupe overlaps, three-way
duration reconcile, span coverage, WPM band.

---

## 8. Documents — docs before dollars

**109 documents. 37 written_hand + 36 course_doc + 36 orphan.** Processed before
the paid pipeline: a free end-to-end shakedown of fetch, extract, render, egress.

R1 measured this as **cheap**: ~10–25 min fetch (109 handshakes, not the 0.486 GiB),
~30–90 min extraction, first STT dollar at **T0 + 45–120 min**. The 2×340-page
books are minutes each — **the real extraction risk is the 296 MiB
`Lazy Loading Code` ZIP**, where `ElementTree` memory on 8 GB is the exposure.

**But it must still be split `[R1]`** — not for cost, for one reason: the docs
phase is the debugging front for §15's naming defects (one of which already
dropped a call). Debugging tail on free work must not serialise in front of the
paid pipeline while the VM burns.

> Run a **shakedown subset first**: ~10 documents covering all three §8.1 classes,
> both sparse books, and the ZIP — **through egress**. Then start the audio lanes
> with the remaining documents running alongside.

### 8.1 PDF — measured, gate closed

`evidence/probes/nhbplus-pdf-text-layer-2026-10-15.json`. 50/50 fetched, 0
failures, 0.159 GiB, **$0.00**.

```
pypdf 4.0.2   Ubuntu 24.04 archive (python3-pypdf 4.0.2-1). Not pip, not a vendor.
ROUTE     page.extract_text(visitor_text=...) -> per-span size, baseline, x.
REJECTED  content-stream Tj/TJ regex -> hex glyph indices, not characters.
IMAGES    enumerated via /Resources /XObject. NEVER decoded. 0 bytes written.
```

**Three classes. A binary text/raster gate is wrong** — it was tried and
discarded for filing 7 readable documents as degraded and discarding real text.

| Class | Count | Handling |
|---|---|---|
| `text` | **48** | tiering and reflow valid |
| `sparse` | **2** | *AC eBook*, *AC_Book* — 340 pp each, `page_cap: 200`. **[R4-T1.6] 59% READ, 41% NEVER OPENED — see the note below. 1,372 words is real; completeness is not.** |
| `raster` | **0** | needs OCR; none is proven free, so it would ship `empty_extraction` and **never be OCR-billed**. Vacuous. |

**65,985 recoverable words. Zero documents require OCR.**

**Stereo billing, measured 2026-10-15 `[T5 #3]`.** A 120 s stereo clip and a
120 s mono clip of the same audio were submitted identically:

| | true | reported | ratio | channels in response |
|---|---|---|---|---|
| stereo | 120.00 s | 120.00 s | **1.00×** | **1** |
| mono | 120.00 s | 120.00 s | 1.00× | 1 |

**Good news:** stereo reports 1× true duration, so `COMMIT_COST` and
`SETTLE_FROM` agree and V12's 2% reconcile holds. Round 2 predicted 2× reporting
and that prediction is **not confirmed**.

**The residual round 2 missed:** Deepgram's own pricing says stereo bills 2×, so
**the response reports 1× while the card is charged 2×.** The receipt therefore
**under-records the bill** on any kept-stereo unit. `SETTLE_FROM` multiplies by
the **input** channel count read from the local part, never from the response.
Bounded by measurement — 3 of 3 stereo files were dual-mono, so the keep branch
fired 0 of 3 — but the gate must be correct on it. **§2.2 carries an explicit
keep-stereo line, bounded at 2x the corpus: +$197.68 in the worst case where
every unit keeps stereo, against a $204.69 stop.** [F6] Earlier revisions claimed
this line existed twice while grepping for it returned only the claim itself.

**Links: `/Annots` is the ONLY authoritative link layer.** *Swipe* carries 400
raw annotations, **201 distinct** — half boilerplate. Text-layer URLs are mangled
by wrapping (`Calcu` / `dit#gid=5683798` / `lator`). Never recover a URL from
display text.

### 8.2 The 2 sparse PDFs — decided, not deferred `[R1]`

Rev 0 deferred this to "a presentation decision". Deferred decisions are abdications.
**Decision: a stub note carrying the measured facts and all 1,372 words verbatim
in page order, under per-page `#### p. N` headings, with an explicit statement
that no layout is recoverable.**

- **Not a per-page summary.** At 3.4 words/page the only honest per-page artefact
  is a report of absence, and any actual summary would have to come from images —
  which needs OCR (not proven free, Rule 2) or fabricates. A summary of an unread
  page is a fabrication.
- **Not a reference-only stub.** 1,372 measured characters exist. Discarding them
  is a descope, and Rule 1 forbids it. A bare MEGA handle is the link index that
  stage-0 §1 says this build is not.
- Compatible with Constraint 1: markdown, 0 bytes of media. The route Constraint 1
  *blocks* — page screenshots so a human can read the book in Obsidian — is exactly
  the shortcut that exists to stop someone doing this.

### 8.3 The 8 non-OOXML, non-PDF documents — previously unhandled `[R1]`

6 `.txt` (incl. all 5 `Resources Links`), 1 `.png` (`Pick Primary Color`),
1 `.zip` (`Lazy Loading Code`, 296 MiB).

- **6 txt** → stdlib read; the 5 `Resources Links` need the §10.2 course prefix.
- **1 png** → **never decoded, never rendered.** Ships as a manifest entry naming
  the file and its dimensions only. It is the one document that collides head-on
  with Constraint 1, and the resolution is that it contributes **no bytes**.
- **1 zip** → enumerate members, extract text-bearing members via stdlib
  `zipfile`, with a **size-triggered memory guard** (§8 preamble).

---

## 9. Ordering `[R1]`

`worklist/targets.csv` — **NEVER globbed. The only work list.**

1. **Shakedown subset** — ~10 documents, all three §8.1 classes + both sparse books
   + the ZIP, **through egress**.
2. **Remaining 99 documents**, alongside the audio lanes.
3. **One lesson-sized STT smoke test (~$0.16)** before the paid bulk. The 16-longest
   LPT block runs next; it is the riskiest spend in the run at $1.1–2.0 each.
4. **16 longest audio** head-of-line (LPT fill, minimises makespan).
5. **Remainder cheapest-first** by `COMMIT_COST` — maximises completed
   units if the hard stop bites.

> Alphabetical ordering dropped: unjustified, worst for both makespan and budget
> robustness. Ordering cost ≠ billed cost for segmented units — order on
> `COMMIT_COST` (§2.2), not raw minutes.

---

## 10. Vault assembly — on the VM, then copy

```
vault/calls/<year>/<MM Month>/<CLEAN>.md              193 paths
vault/courses/<Course>/<CLEAN>.md                     78 paths   [F9] NEW
vault/written-hands/<year>/<MM Month>/<CLEAN> (written hand).md   37 paths
vault/library/…                                     36 paths
vault/00 Home.md
vault/00 Topics.md                   NEW - §10.3

[F9] `courses/` was MISSING and holds 78 of the 344 paths - 36 course_doc files in
36 per-course folders plus the 5 `Resources Links` that the course prefix pulls
out of the library. design-names.py emits it; §10 did not name it, so §10 and
VAULT-STRUCTURE.md disagreed on the tree. The counts above are measured from
pipeline/out/clean-names.json, not asserted.
_meta/manifest.json
_meta/AUDIT.md                       NEW - §12.1
```

Exactly **5 frontmatter fields**: `title, date, type, duration, speakers`.

**Every documented output location needs a `path`.** Rev 0 assigned locations for
the 109 documents that **no artifact actually populated** — `clean-names.json`
carries `handle/verbatim/kind/clean` and no `path` for any of them `[R1]`.
`design-names.py` must emit one, and V8 must assert its existence.

> **[B19] CLOSED 2026-10-15 by build, not by prose.** `design-names.py` now writes
> a `path` for all 109 documents. Measured: `documents with a path : 109/109`,
> `document path collisions : 0`, `total clean paths : 344` = 193 + 42 + 109.
> Previously it wrote `path` for calls and lessons and **never for a document**,
> so V8 failed on its first run and the §9 docs shakedown could not complete.

### 10.1 Frontmatter value domains — asserted, not merely counted `[R1]`

Rev 0's V8 asserted a **field count**, so these all shipped: `duration: 0` on 3
units, `speakers: null`, and a `type: mastermind` that is **not in its own
vocabulary** - it lists six, not five.

```
date      ^\d{4}-\d{2}-\d{2}$   or  unknown
duration  integer >= 0          or  unknown     (minutes, never "3h 14m" -
                                     [F40] LOWER BOUND FIXED 1 -> 0. MEASURED: 2 of
                                     230 units are sub-minute - A2dWSZAK at
                                     media.dur_s = 50 (0.833 min, floors to 0), and
                                     one at 0.0 s whose container reports no duration
                                     at all. An `integer >= 1` domain REJECTS REAL
                                     UNITS IN THIS CORPUS. 0 is a truthful minute
                                     count for a sub-minute unit; the alternative is
                                     rounding up, which invents a second the
                                     recording does not have. Keep >= 0, and ADD: a
                                     response whose duration is 0 or whose word count
                                     is 0 is FLAGGED, not silently accepted - 50 s of
                                     audio must not transcribe to an empty note.
                                                V4 and V10 do arithmetic on it)
speakers  integer >= 1          or  unknown     (diarisation CLUSTERS, not people)
type      theory|guest|coaching|training|mastermind|other
title     == the filename stem
no key outside the five
```

**`unknown`, never `null`.** In Obsidian a null frontmatter value renders as an
empty field, indistinguishable from missing — the absence stops being a recorded
fact and becomes an omission. That is exactly what the §11 constraint exists to
prevent.

A speaker count carries its caveat in the note **body**, not a sixth field:
> Speaker labels are algorithmically derived clusters, not identified people. A
> single label on a multi-hour call usually means diarisation failed to separate
> participants, not that one person spoke.

### 10.2 Filenames — the repair surface is larger than §15 claimed `[R1][R3]`

Rev 0 asserted clean rules in §10 and listed three violations in §15, 25 lines
below, with no cross-reference. **67 of 296 names (23%) are affected**, not three.

| Defect | Measured | Fix |
|---|---|---|
| dash splitter mangles intra-word hyphens | **[R4-8.55] measured: 38 of 188 calls, 46 of 344 total at the time; **re-measure on 344**, of which **0** are true intra-word mangles** — the 7 are all intact. The old "50 of 229" was wrong on both terms: 229 is *units with a duration*, not a path count, and [B20]'s 296 excluded the lessons. It once contained (`Ron-Lynch`, `Biz-Op Blueprint`, `Clean Biz-Ops`, `Pre-Openings`, `CMO-CRO Roles`, `Call of Duty Biz-Ops`, `7-Figure Fill-In-The-Blank`). **[B20] The spec previously said 67 of 296 - the denominator 296 excludes the 42 lessons, one of which is damaged.** | normalise dash **styles** only; never split `[A-Za-z]-[A-Za-z]` |
| `Call` stripped mid-phrase | `Call of Duty` → `of Duty Biz - Ops`; `Call Booking Page` → `05 5 Booking Page` | strip `Call` only as a whole token outside a compound |
| `None` leaked into 3 filenames | `None Selling To Women 3.0.md` etc. | a missing date **omits the prefix**, it does not fill it. V8 asserts no filename contains `None` |
| extension-in-stem | **2 `.mp4.md`** paths | strip a trailing media extension before appending `.md`. V6 checks **stems**, not just extensions |
| 5 `Resources Links` collide | `collisions.documents = 1` while 5 files share the stem | apply the course prefix; the script computes it and discards it |
| 23 brand tokens, 4 underscores survive | against §10's own rules | fix the strippers |
| **dropped call** | `10-31-2022 NHB+ Mindstream Call` absent; **187 paths, not 188** | drop `Mindstream` from the alternation; **and add a guard: if `tidy()` returns empty, fall back to `topic`, never `continue`** |
| lesson ordinals renumbered | source `7. AC - Unannounced bonus` → `02 …` | preserve source numbering |
| dates lost | the corpus's **only** ISO-dated name (`2024-09-27`) is the one that lost its date | accept `YYYY-MM-DD` as well as `M-D-YYYY` |
| **[R4-8.54] 2 calls are undated, not 3.** The manifest carries
`undated-other-5-MmMmABhJ` and `undated-other-5-x3Mi0JJL` — there is no
`undated-other-9` prefix, and **186 of 188 calls are dated, not 185.** |
| ~~3 calls undated~~ | `undated-other-9/-5/-5` | §10 needs a day; list them, do not leave them to run time |

**Written hands derive their filename from their CALL's clean name**, suffixed
`(written hand)`. This is one line and it simultaneously kills: 10 of 37 hands
whose own names match no call topic, the `Selling To Women 2 / 3.0 / Part 2`
collision cluster, and the exact call-vs-hand stem collision. **Rev 0's
bidirectional link was a name-resolved link across two different vocabularies —
10 of 37 depended on Obsidian's shortest-path heuristic.**

**The stale wart.** Rev 0 claimed lexical order was wrong until month folders
fixed it. Since the cleaner normalises dates to ISO, **filenames alone sort
correctly** — that wart belonged to the verbatim-name design the operator
overrode. The **real** wart is that written-hands did *not* get ISO normalisation,
so the two trees sort by incompatible conventions across the vault. Deriving
hand names from call names fixes that too.

### 10.3 `00 Topics.md` — the corpus's own index, which was thrown away `[R1]`

**The strongest objection to rev 0's design:** the vault is organised by **when a
call happened** — the one axis a paying member never uses. The topic axis is
*already in every filename* and required **zero inference** to recover. The
cleaning pass read it, stripped the type boilerplate off it, mangled 24% of its
hyphens, and then the vault design discarded it.

> **[F15] THE PREMISE WAS FALSE AND HAS NOW BEEN MEASURED.** This section
> previously claimed the topic axis "already clusters into ~50 groups of
> 1–13". **It does not cluster.** Measured over all 230 manifest topics:
>
> | | claimed | **measured** |
> |---|---|---|
> | groups | ~50 | **225** |
> | singletons | — | **221** |
> | units sharing a stem with ≥1 other | — | **4 of 230** |
> | largest group | 13 | **3** |
>
> A round-3 review measured the same shape independently (212 stems / 199
> singletons / max 3 / 13 multi-member groups). The counts differ because the two
> normalisers differ; **both agree the claim is false and the maximum is 3.**
> Measured here with: split on the dash separator FIRST, drop qualifier segments
> (`with|and|part|pt|feat`), then strip the call boilerplate from the head. Order
> matters — stripping `call` before the dash-split collapses 126 units to
> `untitled`, which is how a first attempt produced a plausible-looking but
> meaningless clustering.
>
> The two leading-strip rules this section specified (`nhb - `, `theory - `)
> match **0 of 230 topics.** The real boilerplate, measured: `nhb theory` on
> **108**, `nhb coaching` on **21**, `ff guest` on **11**, `ff ` on **14**, `nhb`
> on **136** of 230.
>
> **So: `00 Topics.md` is not a clustered index, because there are no clusters.
> It is a chronological index with a topic column — 225 rows, 221 of them a
> single note.** That is still the right artifact (it answers "where did we
> discuss X" for the 4 that recur, and lists the rest once), and it is still $0.00,
> but V13 is re-scoped below to gate what actually exists.

`type: theory` returns ~120 notes across 36 month folders in 5 years. That is not
a view. And the fallback — Ctrl+F across 4–5M words of machine diarisation where
`Speaker 7` means nothing — is the absence of a retrieval strategy.

**Artifact:** one generated note at vault root, linked from `00 Home.md`. One
section per topic stem, sorted by member count descending, each row carrying ISO
date, type, duration and a wikilink. ~250–400 lines.

**Built by deterministic stem extraction only** — **[F15] the rules below REPLACE
the ones that matched 0 of 230 units.** In this order, because the order is
load-bearing:

1. lowercase, `_` → space
2. **split on the dash separator FIRST** (`-`, `|`, en/em dash)
3. **drop qualifier segments** — `with|and|part|pt.|feat|featuring …`. If every
   segment is a qualifier, keep them all.
4. take the last surviving segment as the topic; if it is empty, the head
5. strip the head boilerplate: ordinal, `ff `, `nhb `, then the call-type words
   `guest|speaker|theory|coaching|training|mastermind|mindstream`, then `call`
6. keep only `[a-z0-9 &+]`, collapse spaces, fall back to `untitled`

The subject is frequently the **middle** segment — `nhb coaching call - offer
fundamentals - with kevin sheerin` is a `kevin sheerin`-segment if step 3 is
skipped, and the corpus is full of that shape. **Do not merge stems differing
only by a verb** — `digging into data` and `diving into data` stay separate and
appear adjacent so a human sees the inconsistency once and decides, with the
decision recorded in the script.

**Cost $0.00, ~2 hours**, computed from `clean-names.json` and `scope-final.json`,
both already on disk. No network, no STT, no vendor, no new dependency.

**Rider, ~30 min, same zero:** emit transcripts under per-30-minute `### 0:00` /
`### 0:30` headings. Timestamps are already in the utterance data — zero
inference, mechanically verifiable, and it turns every call note into a jumpable
outline. `00 Topics.md` answers *"where did we discuss X"*; this answers
*"where in the call is the bit about X"*.

---

## 11. Verification — gates

| Gate | Assertion |
|---|---|
| V0 | worklist integrity: **344** rows, never a glob |
| V1 | fetch caps: ENOSPC proven; **no kill fired on a sentinel `declared`** |
| V2 | remux/segment: no part ≥ `CAP_BYTES` |
| V3 | STT contracts: **the one sync path** (§7.2 deleted the other — there is no async job); **`sent` persisted before the socket opened**; `http_status == 200` AND `response_complete` both required |
| V4 | three-way duration reconcile |
| V5 | span coverage |
| V6 | **zero media extensions under `vault/`** — the list must include **`.mka`**, the container §7.1 mandates, plus `aac\|opus\|ogg\|mpga\|mkv\|webm\|mov\|m4a` — **AND** no stem matches `\.(mp3\|mp4\|mov\|m4a\|wav\|flac\|mka)$`. **[R4-8.39] ADD `.png`:** the corpus contains exactly one image (`guNkBLaZ`, 151,552 B, §8.3) and Constraint 1 is absolute — no media-shaped file reaches the operator's PC. **AND A FLOOR, WHICH IS THE PART THAT WAS MISSING:** `vault/` currently holds **0 files**, and every check above is a *ceiling* — **an empty tree satisfies all of them and returns PASS.** That is this project's own empty-vs-empty trap. **V6 must also assert `count(vault/**/*.md) == 235 + 109 == 344`.** Until that floor exists, V6 green means nothing. |
> **[R4-8.40] AND EVERY CORPUS FORMAT IS CURRENTLY UNCATCHABLE BY V6.** The corpus
> contains `pdf, docx, pptx, txt, xlsx, png, zip`. None is in the extension list,
> none matches the stem regex, and a `.pdf` or `.docx` under `vault/` would pass
> V6 outright **while violating Constraint 1.** The list above is an audio list
> applied to a corpus that is not mostly audio. **`pdf\|docx\|pptx\|xlsx\|txt\|png\|zip`
> are added to the banned set**, because an extracted document ships as `.md` and
> the *source* must not ship beside it.

| V7 | reduction diff: re-render from receipts, byte-compare |
| V8 | **frontmatter value DOMAINS (§10.1), not a field count; every document has a `path`; no filename contains `None`** |
| V9 | counts 37/36/36; **and every manifest unit with `kind == "calls"` has exactly one emitted note** (193 rows in `manifest-v3.json`). **`scope-final.json` has no `call`/`calls` kind — its kinds are `audio`/`written_hand`/`course_doc`/`orphan_doc` — so the previous `kind == "call"` matcher hit 0 handles and V9 passed VACUOUSLY on the one confirmed live defect, the dropped `10-31-2022 NHB+ Mindstream Call`. [B7]** V9 previously checked documents only, so it **structurally could not catch the dropped call** |
| V10 | `settled + lost ≤ SPEND_HARD_STOP_USD`, derived from receipts, **using the same settle quantity as the §7.2 gate** |
| V11 | egress SHA256 per-file match |
| **V12** | **Identity Binding — NEW, and the most important gate here** |
| **V13** | **`00 Topics.md` — NEW. [R4-T1.5] POPULATION IS 230, NOT 225.** **[F15] re-scoped it to what measurement supports; [R4-T1.5] found it still named THREE populations.** It said "225 rows", "1 row per emitted note", and §11.2's body gated "every note under `vault/calls/`" (188). **The population is 230 notes — 188 calls + 42 lessons.** 225 is a GROUP count from [F15]'s clustering, not a note count, and the two cannot both be true. **Now: 230 rows, one per emitted note, plus a `recurs` column.** §11.2's group clauses are deleted below. |
| **V13** (population note) | [F15]'s own table is also internally inconsistent: `225 − 221 = 4` multi-groups, which must hold `230 − 221 =` **9** units, but the same row says "4 of 230". The **group count** is 4; the **units inside them** is 9. **[R4-T1.5]** |

### 11.1 V12 — Identity Binding `[R1]`

> **V7 proves determinism, not correctness.** It re-runs the same renderer on the
> same inputs. If assembly cross-wires two units' responses — a file-handle
> reuse, an off-by-one in `part-NN` offset concatenation — **V7 reproduces the
> mistake byte-perfectly and reports success.** No existing gate binds the identity
> of the *content* to the identity of the *unit it landed in*.

```
For each audio unit U:
 1. H(U) = SHA-256 of the ordered concatenation of every
          utterances[*].transcript in U/assembled.json
 2. H(U) equals the value recorded in U/receipt.json at assembly time
 3. H(U) values are PAIRWISE DISTINCT across all 230 audio units
 4. EXACTLY ONE note under vault/ renders utterance text hashing to H(U)
 5. no two units share a NON-NULL request_id
 6. effective_spend reconciles to COMMIT_COST, and ffprobe(U) is within 2% of
    the metadata.duration in U's OWN response

 > **[R4-T1.10] CLAUSES 5 AND 6 WERE MUTUALLY EXCLUSIVE, AND §12.1 DELETED THE
 > EVIDENCE FOR CLAUSE 6.** [F14] had asserted "`request_id` is None for EVERY
 > submission" and therefore removed the `request_id` column from AUDIT.md.
 > **Two later artifacts contradict that**, and [F14] predates both:
 >
 > | artifact | `request_id` |
 > |---|---|
 > | `nhbplus-w0-asynccontract-2026-10-15.json` | `None` |
 > | `deepgram-eu-limits-and-chain-proof-2026-10-15.json` | `01a13cfc-1b03-7e10-94cb-a448d81cb512` |
 > | `nhbplus-w0-syncceiling3-2026-10-15.json` | `01a13ec6-9208-7c90-a68d-0209a8e6be33` |
 >
 > **So [F14]'s generalisation was wrong**: it held for the asynccontract's
 > request SHAPE and was carried to every submission. With `request_id` present,
 > clause 5 becomes **measurably testable** rather than vacuous — the opposite
 > of what the [F14] fix assumed — and clause 6 becomes evaluable instead of
 > unimplementable.
 >
 > **RESOLUTION.** Clause 5 stays, worded for the null case so it is falsifiable
 > either way. **Clause 6 is re-worded to bind `ffprobe(U)` to U's OWN stored
 > response**, not to a request_id lookup, so it no longer depends on the field
 > existing at all. **The `request_id` column is RESTORED to AUDIT.md** — it was
 > deleted on the strength of a claim two later artifacts disprove, and the
 > artifact that disproves it says so in writing and asks for this.
 >
 > **STILL OPEN, and not settled by the re-wording:** whether `request_id` is
 > present on the sync path *generally* or only on some request shapes is not
 > established. Two present, one absent, three probes. Clause 5 is written to
 > pass in both cases; **do not read that as evidence the question is settled.**

 > **[F14] history, kept because the failure is the point:** the clause as first
 > written ("no request_id appears under two different unit ids") FAILED on a
 > flawless run, because None appears under all 230 unit ids. The fix was right
 > about that and wrong about why.
```

**Why it cannot fail trivially:** `H` is computed from the **raw response**, not
from the rendered note, so re-running the renderer cannot satisfy it. Clause 4 is
load-bearing: if two units' transcripts were exchanged, both `H` values still
exist on disk and **V7 still passes** — but each note now renders the other's
hash, so clause 4 fails for **both** units. A single swap is caught twice.
Clauses 5 and 6 catch the same defect at the vendor and money boundaries.

**Cost $0.00**, a hash over strings already on disk, well under a second.

### 11.2 V13 — Topics

> Every note under `vault/calls/` appears in **exactly one** topic group; every
> group has ≥1 member; and **every token in a group heading appears in at least one
> member's topic string.**

The last clause is what makes it unforgeable — it cannot be satisfied by a
hand-written heading like "Pricing Psychology" that no filename supports.

**[F36] FIVE EXIT CODES WERE DECLARED FOR FOURTEEN GATES.** Nine gates had no
code, and two shared one. A code an implementer must map by hand is a code they
will get wrong. **The rule is now mechanical: `exit((gate_index + 1) * 10)`.**
 `[ R4-T1.4] **NOT `exit(gate_index * 10)`** — that form returns **0 for V0,
and 0 is success**, so **V0 can never report failure.** V0 is *worklist
integrity: 344 rows, never a glob* — the gate that stops a re-billed corpus. The
`+1` is not cosmetic; it is the difference between a gate that works and one
that cannot fail.

| | |
|---|---|
| 0 | all gates passed |
| 10×N | gate N failed (N = 0, 1, 2, …) |
| **1** | **crash** — an exception escaped a gate, not a verdict |
| **2** | usage error, before any gate ran |

That last row is the distinction the old scheme could not express: **exit 1 is
not "a gate failed", it is "no gate reached a verdict"**, and a wrapper script
that treats it as a gate failure will misreport a bug as a measurement. Any gate failure **writes its receipt and
increments its count**.

---

## 12. Egress and teardown

Binary-only copy VM→PC of `vault/` + `_meta/`. **The finished markdown IS the
deliverable; nothing media-shaped ever touches the PC.** Per-file SHA256 manifest
compared. PowerShell pipelines **forbidden by name** — W0-Egress proved 11/11
typography checks survive `scp -r` and that the two forbidden PowerShell rewrites
destroy exactly that typography.

**The transfer is a dumb binary pipe with no filter, and that is correct.**
W0-Egress planted a `.mp3` in the source tree and `scp` copied it to the PC,
because `scp -r` copies whatever it is given. The control does not belong there:

> **V6 MUST RUN ON THE VM SOURCE TREE, BEFORE THE COPY.** Once a media file lands
> on the operator's PC, Constraint 1 has already been violated. A post-copy gate
> reports a violation that has already happened. The gate must sit upstream of the
> only irreversible step in the pipeline.

**Mandatory sequence — the ordering is load-bearing:**

```
assemble vault/
  -> V6  on the VM, zero media extensions and stems   <-- BEFORE any transfer
  -> V7  reduction diff, re-render byte-compare
  -> V8  frontmatter value domains + every document has a path
  -> V9  counts, and EVERY audio target handle has exactly one note   [F12]
        (this is the gate that catches the dropped call - it must not be omitted)
        scope-final.json's kinds are audio/written_hand/course_doc/orphan_doc.
        There is NO kind == "call": the old matcher hit 0 handles and PASSED
        VACUOUSLY on the very call the gate exists to catch.
  -> V10 settled + lost <= hard stop, from receipts
  -> V12 identity binding
  -> V13 topics index        [CONDITIONAL on the 00 Topics.md decision, §15]
  -> EMIT the SHA256 manifest of vault/ + _meta/  (no step produced this before)
  -> ONLY NOW  scp -r VM -> PC
  -> V11 SHA256 compare on the PC
```

Egress is always **PC-initiated**: the SSH key lives on the PC, so running `scp`
from the VM fails on host resolution. That failure is `rc=255 "Could not resolve
hostname c"` and it reads like a network fault but is not one.

### 12.1 `_meta/AUDIT.md` `[R1]`

**Rev 0 moved every cut fact into `manifest.json` and called it clean. It is a
relocation.** Obsidian cannot open, search, or link into JSON — every fact the
operator cut from the frontmatter became reachable only by leaving Obsidian and
running `jq`. A cut that moves data into a format the reader's software cannot
open is not a clean cut.

Emit one generated `_meta/AUDIT.md` — **[R4-8.44] 230 lines, one per AUDIO UNIT, not 339.** 339 is the count of *targets*; only 230 of those are audio units, and V12 clauses 1–4 are all about audio units. The 109 documents are verified by §11's path and frontmatter gates, not here:
`unit · handle · declared_s · ffprobe_s · settle_s · sha256-12 · verdict`
request_id  **[R4-T1.10] RESTORED.** [F14] removed this column on the strength
of "None for EVERY submission"; two later dated artifacts carry a non-null
value (`syncceiling3`: `01a13ec6-...`, `deepgram-eu-limits`: `01a13cfc-...`).
Recorded as measured, blank if absent — never invented.
with totals in the header, linked from `00 Home.md`.

**No note gains a field. No note gains a provenance section. The operator's cut is
respected exactly** — the audit simply becomes reachable from the tool the
operator reads in. ~20 lines of renderer code.

> **[R4-8.56] "TEARDOWN IS 7-PHASE" AND THE SEVEN PHASES ARE NOT ENUMERATED
> ANYWHERE IN THIS DOCUMENT.** A phase count with no phases is a scope claim no
> reader can check. And `--confirm <sha256 of copy-verification.json>` names a
> file with **no producer, no path and no schema.** [R4-2.17]
>
> **The seven teardown phases, enumerated.** [R4-8.56] A phase count with no
phases is a scope claim no reader can check.

| # | phase | gate before it may start |
|---|---|---|
| 1 | **stop intake** — no new unit admitted, in-flight parts drain | V10 within stop |
| 2 | **settle** — every `sent`/`reserved` part resolves to `settled`, `lost` or an explicit `PAID_UNKNOWN` | ledger has no `queued` |
| 3 | **assemble** — `assembled.json` per unit, then the rendered note | V12 clauses 1–4 |
| 4 | **audit** — emit `_meta/AUDIT.md` (230 rows) and the SHA-256 manifest | V12 clause 4 |
| 5 | **egress** — `scp -r` vault + `_meta` to the PC, media-free | V6 (with its floor), V7, V11 |
| 6 | **verify the copy** — `copy-verification.json`: per-file SHA-256, byte count, typography spot-check | V11 |
| 7 | **destroy** — delete the VM and its disk image | **all of 1–6 green** |

**[R4-2.17] `copy-verification.json` HAS NO PRODUCER, PATH OR SCHEMA ANYWHERE IN
THIS DOCUMENT.** It is named once, by the `--confirm` argument that gates phase 7.
**Schema, fixed here so phase 6 cannot be skipped by omission:**

```
copy-verification.json = {
  "generated": ISO-8601,
  "source": "VM:/data/nhb/vault",
  "files": [ {"relpath": str, "bytes": int, "sha256": hex64} ],   # every file
  "notes_expected": 339, "notes_found": int,
  "typography_checked": int, "typography_passed": int
}
```

**A run that cannot produce this file does not reach phase 7.** The destroy step
is the only irreversible one in the plan and it is gated on the artifact that was
previously unnameable.

Teardown is 7-phase. Final destroy requires `--confirm <sha256 of
copy-verification.json>` — deliberately awkward, so the operator has looked.

---

## 13. Where the plans are wrong

### 13.1 The four plans, and round 1

| Item | Verdict |
|---|---|
| "146.87 GB ≈ 30–50 h serial fetch" | **~30× wrong.** Measured 41–53 MB/s → **0.99–1.28 h** |
| Alphabetical-smallest-first | Dropped — unjustified and pessimal |
| Any 40×-realtime sync cutoff | **[F25] "ZERO MARGIN" IS ARITHMETICALLY WRONG.** 16,556 s of audio at the ceiling is 16,556/600 = **27.6× required**, so 40× yields 414 s against 600 s — **186 s of headroom, not zero.** **[F1-CORRECTION] This line previously read "measured realtime on the real worst case is 106×, which is 3.8× margin." The worst case was never measured — see the OPEN gate above. The one MEASURED realtime factor is 119×, on `dvcEDToK`, the 47th-ranked unit.** A cutoff is still not adopted, and it is rejected on arithmetic, not on a measurement that does not exist. |
| Any success-only spend counter | Wrong — a 504 storm is paid-and-lost and sails past it |
| SQLite/journal/per-unit-JSON as independent truth | A desync waiting to happen — exactly one authority |
| Disk "bound proof" (38 GB vs 400 GB) without the loopback | Not a safety system. Only kernel ENOSPC counts, and only once proven |
| `kill`/`timeout` as the fetch safety system | Wrong — admission control + watcher + cancel + quiesce assertion is |
| Direct reuse of the skill's PDF constants | Wrong — §2.3 |
| **A `*.mp3.md` filename** | A bug — **and the live one is `.mp4.md`, on 2 committed paths** |
| **"crashed async is free via `request_id` re-GET"** | **FALSE `[R1]`.** Constraint 7: nothing is stored. Both paths are single-shot |
| **"FORECAST == HARD_STOP"** | **WITHDRAWN 2026-10-15 `[R1]`.** The claimed $151.01 overspend was a **`ceil` artifact**. Deepgram bills true per-second with no minimum and no rounding, so the corpus costs exactly the forecast, $150.56. The pessimism was solving a problem the vendor does not have. |
| **"resume never re-bills"** | **NOT IMPLEMENTED `[R1]`.** The state machine was blind to the one bit that decides it |
| **"an unnamed `flock` guards the global sum"** | **NOT IMPLEMENTABLE `[R1]`.** No file, no path, and every named lock is per-unit |

### 13.2 Claims withdrawn during planning

Kept visible, because a withdrawn claim is evidence about the corpus.

| Withdrawn | Why |
|---|---|
| "PDFs may be ~25 image-only scans" | **Measured: 0 need OCR.** Guessed from file size. |
| "4/4 PDFs have a text layer" | Hex glyph indices counted as characters. |
| "Y_TOL is stable across 0.0–5.0pt" | Asserted from a counter that could not fail. **Now digest-proven.** |
| "The 1.0pt reading is my own fallback" | `fallback_share = 0.0%`. **Hypothesis falsified by instrument.** |
| "4/4 fetches failed" | mega-get names output after the verbatim file, not the handle. |
| "146.87 GB" | It is **GiB**. Decimal is 157.70 GB. |
| "59 office documents" | **51**. The other 8 are txt/png/zip. |
| "saves 132 GB" | **185.45 GB**, and 132 appears in no artifact. |
| "229 paths" | 229, but **all 109 documents have none.** |
| "603.84 h raw" | A superseded **236-call** reconciliation. Real: 583.55 h. |
| "all 188 calls dated" | **185/188.** |
| "≈1 h for documents first" | Roughly right — but the **296 MiB ZIP**, not the 340-page books, is the extraction risk. |
| "Deepgram does not store transcripts → async re-GET is free" | The limit was **right and unused.** The conclusion drawn from it was false. |

---

## 14. Provisional — re-measure if these move

`SEGMENT_SEC`, the WPM band, the remux saving, `Y_TOL` on the 2 named documents.
`RATE` is **blocking** (D2) — not provisional, unobtained.

---

## 15. Open

**None. All four operator decisions are settled:**

| | Outcome |
|---|---|
| D1 | **settled** - $207.68, every line measured |
| D2 | **closed** - $0.0043/min, sourced and dated |
| D3 | **closed** - dual-mono, per-file rule, $26.98 |
| D4 | **adopted** - keyterm on, +$45.52, A/B-measured |

**[UPDATED 2026-10-15 — THE NAMING REPAIR IS BUILT, NOT PENDING.]** This section
previously read "the naming repair … spans 67 of 296 names … That repair is the
next thing to build." It landed. Re-measured from `pipeline/out/clean-names.json`:

| | |
|---|---|
| paths emitted | **339** (188 calls + 42 lessons + 109 documents) |
| casefold-unique | **True** |
| documents carrying a `path` | **109 / 109** (was **0** — V8 could never pass) |
| document path collisions | **0** |
| brand tokens surviving | **0** (was 22) |
| `None` in a path | **0** |
| media extensions in a stem | **0** |
| intra-word hyphen mangles | **7 / 7 intact** |
| source lesson ordinals carried | **42 / 42** |
| written hands linked to their call | **37 / 37** |

`check-frontmatter.py` returns **PASS on 0 domain violations**, and can now fail.

**What remains is not naming. It is measurement, and it is unmeasured because
nothing has been paid for yet:** the corpus-wide stereo share (3 of 230 sampled),
Azure VM-days for a 16-way run over 583.55 h, and decoded-vs-header durations
(228 of 230 are container headers). §14 marks `SEGMENT_SEC` and the WPM band
provisional for the same reason. §9's ordering — documents, one lesson-sized
smoke test, then the 16 longest — is what converts them.

**Content decisions still open:** whether `00 Topics.md` and the 30-minute
transcript headings are wanted (§10.3) — both $0.00, ~2.5 h combined, and R4's
objection is that without them the vault answers only *"what did I already know
the date of"*.

**Un-audited:** `7-Figure VSL Script Template` was classified degraded and missed
the fallback audit on a name mismatch; it measured 814 words/page (80× the sparse
threshold), so it is readable by the same metric but was never separately audited.

**Out of scope, flagged once:** the 335 GB import still sitting in the operator's
personal MEGA account. Only the operator can delete it.

> **[R4-T1.6] "ALL 1,372 WORDS VERBATIM" IS A LOWER BOUND PRESENTED AS COMPLETE.**
> `pdf-fallback-audit.json` shows `page_cap: 200` and both sparse books at
> `pages_read: 200 / pages_total: 340` — **59% of each was read and 41% was
> never opened.** The 1,372 words is real; what is wrong is the completeness.
>
> | book | read | total | words | words/page **as measured** | over the whole book |
> |---|---|---|---|---|---|
> | `2. AC eBook` | 200 | 340 | 691 | 3.5 (first 200 pp) | **2.02** |
> | `AC_Book` | 200 | 340 | 681 | 3.4 (first 200 pp) | **2.00** |
> | unread tail | — | **140 pp each** | — | — | **≈ 565 words unaccounted** |
>
> The 3.4–3.5 w/pg figure that both the artifact and this section quote is a
> property of the **first 200 pages only**, and it is the density the cap was
> calibrated on. **A section titled "decided, not deferred" carried a silent
> completeness hole**, which under Rule 1 is the one kind of hole that is not
> allowed to stand.
>
> **Either re-run both books without the cap, or label the note
> `partial_extraction` with pages 201–340 named as unread.** The note's status is
> not yet chosen; what is not permitted is calling a 59%-read book complete.

**1,372 words** |
