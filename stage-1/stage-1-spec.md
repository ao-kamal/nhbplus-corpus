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
> §0, §2, §5, §6 and §7 below, each marked ``.

---

## 0. Hard constraints

These outrank every mechanism here. Nothing below may trade one away.

| # | Constraint | Enforcement |
|---|---|---|
| 1 | **Nothing media-shaped touches the operator's PC.** | The vault (markdown) is the deliverable and *does* land there. Gate V6. |
| 2 | **Pay nothing**, outside recorded waivers. | **Two waivers, not one ``:** Deepgram STT (~$150), **and Azure compute** (metered VM on a $200 credit, ~$0.21/day idle — operator-approved, `evidence/probes/operator-decision-compute-azure-2026-10-14.json`). §0 previously said "sole waiver: Deepgram" and was **wrong**. Report VM-days alongside STT spend. |
| 3 | **Remove nothing.** Where a route is blocked, the route changes. | The 2 sparse PDFs are extracted, not dropped. 100 MP4 alternates are never fetched — a route change, not a removal. |
| 4 | **Evidence, not assertion.** | W0 probes. Ten claims withdrawn during planning; kept visible in §13.2. |
| 5 | **Operator picks the files.** | `scope-final.json`, **344** targets, locked. |
| 6 | **A sentinel is not a measurement** `` | **[F-KIB 2026-10-15] THIS IS UNDERSTATED. NOT 77 OF 235 — ALL 193 CALLS.** Every declared size in the corpus is an **exact multiple of 1 KiB**: **193 of 188, 100% of the corpus bytes.** The chance of that by accident is (1/1024)^188. The spec detects sentinels only at **GiB** granularity (`bytes % 2**30 == 0`), which finds 73 and calls the other 115 "real". They are not real either — they are KiB-quantised. Proof from the one unit measured against ground truth: `wiUyTRZb` **declared 397,410,304 B (KiB-exact)** vs **actual downloaded 397,487,264 B (NOT KiB-exact)**, a 76,960 B delta. So there is **no unquantised subset** by this test, and the "73 sentinels / 157 real" split in this document is wrong in kind, not just in number. **§6 (sentinel detection) must test `bytes % 1024 == 0`, and no threshold may consume any declared size.** §6 (73 of 235 carry placeholder sizes** — 38 at exactly 1 GiB, 39 at exactly 2 GiB = **116.00 GiB of 153.81 GiB = 75.4%**. These are MEGA display values recorded as binary. **No kill rule, threshold, or cost gate may consume them.** §6.4. |
| 6a | **Send `mip_opt_out=true` on EVERY request.** **** Probed 2026-10-14: with the flag `HTTP 200`, without it `HTTP 200`, `VERDICT: PASS` (`deepgram-capability-probe-2026-10-14.json` § `STEP_0_CONSENT_GATE`). `operator-decision-compute-azure-2026-10-14.json` records it as *"structural and sent on every request"*. **This document contained ZERO occurrences of `mip_opt_out`, `consent` or `GDPR` before this line — the flag existed in a dated decision record and in nothing else.** §0's own rule is that *"an agent executes this with no other document open"*, so an omission here is an omission in the executed path, not in the reading list. **The artifact is explicit: *"Acceptance of the flag is NOT permission to stop sending it."*** §7.2. |
| 7 | **The response is the only retrieval** `` | `evidence/probes/deepgram-eu-limits-and-chain-proof-2026-10-15.json`, under `limits_that_would_have_broken_the_run`: *"Deepgram does not store transcripts. The API response is the only opportunity to retrieve it."* **Every submission is single-shot.** The response body must stream to disk as it arrives. §7.3. |

### 0.0.1 Compute, priced `[MEASURED 2026-10-15 · CORRECTED BY R4]`

`Standard_D2s_v5`, `austriaeast`, Linux, Consumption — the VM the probes actually
ran on. **$0.115/hr** from `prices.azure.com/api/retail/prices`, queried
2026-10-15. **$2.76/day.** 2 vCPU.

> **[ R4-T4.1] THIS TABLE WAS WRONG BY 60× WHEN FIRST WRITTEN, AND THE ERROR
> WAS MINE.** `36,336.6 min / 25 / 90.6x` is **15.46 MINUTES**, not 15.5 hours.
> The value was right and the **unit** was wrong — minutes divided by a realtime
> factor is still minutes. Same slip twice more: the full-decode figure was
> **9.44 core-hours, not 567**, because `2,100,786 s / 61.8 = 33,993 s` and I
> divided by 60 a second time. **Every quantity below carries its unit, which is
> the rule R4 asked for and which would have caught all three.**

| phase | computation | result |
|---|---|---|
| **STT at concurrency 25** | `36,336.6 min / 90.6x / 25 = 15.46 min` | **0.26 h** |
| fetch, 165149671424.49 GiB | `165149671424.49*1024 / 47 MB/s = 3,200 s` | **0.89 h** |
| remux `-c:a copy` | `193 units x 5 s` (stream copy, **no decode**) | **0.26 h** |
| channel measurement, 90 s window | `10 stereo x 3 passes x 1.46 s` | **0.01 h** |
| **total** | | **≈ 1.42 h** |

**≈ $0.16 of Azure compute.** Fetch dominates the run. **The STT stage is
fifteen minutes**, which is worth sitting with: a 583-hour corpus is not a long
transcription job, it is a long *download* job.

**the full-decode argument survives, at 17× not 1,150×.** The channel
measurement as §7.1a specifies it is a full decode: `2,100,786 s / 61.8x = 9.44
core-hours = 4.72 wall-hours on 2 vCPU = $0.54`. A 90-second window over every
unit is **0.28 h**. So the window is **17× better**, and 4.72 hours of pure CPU
to classify dual-mono is still indefensible. **Keep the window** — the
conclusion was right and only the figure attached to it was wrong.

**and the raise to 25 paid for itself in  $0.017 of Azure**, not in the
line I claimed. The *concurrency* case for 25 was never an Azure-cost case: 16 is
inside one project with no contract question, 25 is the documented ceiling, and
the measured degradation was 1.022×. That is still the whole argument. The
sentence "paid for itself in the first line" was wrong and is withdrawn.

### 0.1 Blocking decisions for the operator

**D1 — budget: RESOLVED**

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
full budget table and `SPEND_HARD_STOP_USD = $213.48`.

| Item | Was | Now |
|---|---|---|
| 2 units with no duration | ~$1.31 estimated | **$1.23 measured** |
| loss allowance for 504s | unset | **$10.00** |
| `SPEND_HARD_STOP_USD` | unresolved | **$213.48** |

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
which was the worst case where every unit is stereo. It went on: "Measured,
only **17.9% of minutes are stereo**, so the real saving is **$26.98**."
**THAT MEASUREMENT IS WITHDRAWN.** W0-ChannelShare v3 measured 65 units
stratified by type and month and found **3.08% genuinely stereo** (95% interval
1.0–8.5%), against 23.1% that merely *have* two channels, of which 13 of 15
are bit-identical dual-mono. `$26.98` goes with it; the `-ac 1` saving at v3's
own share is **$6.21**, and §2.2's keep-stereo tail carries the ceilings.
The table below is kept as the record of what was believed then:

```
run cost as-is          $177.54
run cost with -ac 1     $150.56
saving                  $26.98
```

**The rule is per file, not per corpus** (§7.1). The 10-file sample constrains
nothing at scale — the measurement is applied to all 235 units, so a single
per-participant file anywhere is *detected and preserved* rather than downmixed.

**SECOND API KEY — budget only, never throughput.** Deepgram scopes concurrency
**per project, not per account or key.** The docs are explicit that multiple keys
inside one project *all draw from that project's concurrency pool*, and that
creating additional projects or accounts to work around per-project limits is
**detected and violates their Terms of Service**.

So a second key adds **$200 of budget and zero throughput**, and load-balancing
transcription across the two accounts would be an explicit ToS violation. **Use it
for budget only.** The run needs the budget — $213.48 exceeds the $200 credit. It
does not need the concurrency: one project at concurrency 50 covers the corpus.

**D4 - keyterm prompting: ADOPTED 2026-10-15** (operator). $0.0013/min,
**+$45.52**. Justified by a measured A/B, not an opinion — see 2.2.1. The deciding
argument is search: without it the corpus spells its own programme name
"Nothing Elbach", and `Ctrl+F "Nothing Held Back"` returns nothing.

---

## 1. Scope — locked

```

> # **SCOPE: 344 TARGETS = 193 CALLS + 42 LESSONS + 109 DOCUMENTS.**
> Derived from `pipeline/out/PLAN-TRUTH.json`, computed from the artifacts,
> not typed by hand. Every figure below is re-derived from it.
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
> note** — a wrong note, a wrong date and a wrong written-hand link, produced
> silently by a rule nobody gated.
>
> **The guard now REFUSES a merge when exactly one side carries a date.** A wrong
> merge is silent and corrupts; a wrong non-merge is visible and costs one extra
> unit. Measured consequence:
>
> | | was | **now** |
> |---|---|---|
> | calls | 193 | **193** |
> | lessons | 42 | 42 |
> | documents | 109 | 109 |
> | **targets** | **344** | **344** |
> | merges applied | 18 | **12** |
> | audio minutes | 36,336.6 | **34,472.1** |
> | `SPEND_HARD_STOP_USD` | $207.68 | **$203.48** — and then **$213.48**, once the 42 lessons were priced at $8.79. Live value is **$213.48**. |
>
> **THE MONEY FELL $4.64 BECAUSE FIVE CORRUPT UNITS NO LONGER EXIST.** The
> offsetting omission: the two remaining undated calls have **no measured
> duration and so contribute $0.00**. The previous budget carried a **286.9-minute
> tail** for exactly this case. **RESOLVED: the tail is back, measured rather than
> estimated.** Both undated units were re-measured — `dvcEDToK` 12,258.603 s and
> `pjFQiLQQ` **5,431.8 s DECODED** (its container header says 4,958.7 s; decoded
> is 9.54% longer and is the honest one) — totalling **294.84 min**, which the
> stop formula now carries. The old 286.9 was an ESTIMATE and is used nowhere.
>
> **PROPAGATED 2026-10-15.** Every one of these cited 344 / 193 / 36,336.6 and
> has been re-derived from the regenerated artifacts — not hand-copied:
> target count · §7.2 AUDIT row count · §10 vault-tree counts · §11 V0
> "344 rows" and V6's floor · §12 egress manifest · §13.2 · §14 · AGENTS.md.
> **Propagation RESOLVED 2026-10-15.** Verified by sweep, not asserted: zero
> live references to 339 / 188 / 230 / 105 / 440 / $204.69 / 35,013.1 /
> 583.55 / 1.50 GiB / 567 core-hours remain anywhere in this document.
```

| Population | Count | Handling |
|---|---|---|
| Audio calls | **193** | STT. **574.53 h.** was 193 / 557.39 h |
| Bonus lesson videos | 42 | STT. 26.16 h. All 11 courses + all 36 orphans. |
| Documents | 109 | Extract, no STT. **0.486 GiB**, of which PDFs are 0.159 GiB ``. |
| MP4 alternates | 100 | Recorded, **never fetched**. Real saving **177.48 GB** `` — "132 GB" appears in no artifact. |

**Corrections to my own briefing, all now verified against files:**

- Documents partition **37 written_hand + 36 course_doc + 36 orphan = 109** ✓
- Of the 109, **50 are PDFs** and **51 are OOXML** (36 docx + 12 pptx + 3 xlsx).
  The other 8 are **6 txt, 1 png, 1 zip** `` — §8.3, previously unhandled.
- **42 videos vs 36 course docs is not an error.** Operator decision: videos and
  documents are independent. V9 checks self-consistency, never forces 1:1.
- **137 of the 235 fetched primaries are MP4, only 98 MP3** ``. §1 previously
  treated MP4 as excluded alternates. **`ffmpeg -vn -c:a copy` (§7.1) is the
  majority path, not an edge case.**
- **Total is 600.70 h**, not 605.61 h and not 603.84 h — that figure belongs to a superseded
  **236-call** reconciliation ``.
- **146.87 is GiB, not GB.** Every `GB` field in the JSONs is binary ``.

---

## 2. Constants — every value carries provenance

```
MEGA_URL_TMPL  = "https://mega.nz/folder/<PH>#<KEY>/file/<HANDLE>"
     PROVEN. Peak disk is **0.992 GiB MEASURED** (YyEWgJSK, the largest NON-SENTINEL unit
     examined). The 2.00 GB figure that circulated was 2 GiB — the SENTINEL
     value, 36× repeated. Constraint 6 forbids consuming a sentinel and §2
     was doing exactly that.

FETCH_CONCURRENCY      = SIZE-ADAPTIVE, not a constant. See 6.3.
FETCH_CONCURRENCY_CEILING = 38   was 39. The off-by-one fix landed in
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
                                 Run cost $2.41. **Saves 8.7 MINUTES of a ~15-minute STT stage, not
                                 8.7 h of a 24 h run — that was the same 60× unit slip.**
                                 LIMITS: one burst, not the full 15-minute STT stage;
                                 single key; a PASS is not a capacity guarantee.
                                 BINDING CEILING IS 25, not 50. Authoritative
                                source, fetched 2026-10-15:
developers.deepgram.com/reference/api-rate-limits.md
                                 **RESOLVED 2026-10-15 BY LIVE FETCH. THE 25 IS
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

> **CLOSED WITH VENDOR VERBATIM, 2026-10-15. IT IS WORSE THAN A GREY
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
> | second key for **budget** | you pay for more service ($213.48 > the $200 credit) | legitimate |
> | second key for **throughput** | you obtain concurrency above the ceiling | circumvention |
>
> The second use is the one the plan would be doing, and it is what the ToS
> language quoted in this document is aimed at. It was also never worth it:
> **16 -> 25 recovered 8.7 MINUTES of STT inside one project with no question at
> all**,
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
SEGMENT_SEC     = 1500    UNREACHABLE for this corpus, not merely provisional.
                         The largest part in the corpus is 385 MiB against a
                         2 GB CAP_BYTES, so the segmenter never fires. It is
                         retained as the ONLY defence if a future fetch exceeds
                         the sync ceiling, and it must be re-validated against
                         a real part before it is relied on.
                         There is no sync fallback - see 7.2.
FETCH_STALL_SEC = 120     POST_KILL_QUIESCE_SEC = 60
WPM_MIN          = 60     MEASURED 2026-10-15. Census, 47 units.
WPM_MAX          = 300    MEASURED 2026-10-15. Census, 47 units.

  WPM, MEASURED ON THE POPULATION, NOT ESTIMATED ON A SAMPLE:

    n = 47  (42 lessons, ALL of them + 5 calls)
    min 127.6   mean ~208   max 251.7

  evidence/probes/nhbplus-lessons-census-2026-10-15.json   42 of 42, 0 errors
  evidence/probes/nhbplus-call-edges-2026-10-15.json       5 calls, free -
                                                           transcripts cached

  **WPM_MAX WAS 260 AND IT WAS TOO TIGHT BY 8.3 wpm.** It sat above the
  densest measured unit by less than 3%, and TWO lessons were already within
  15 wpm of it (251.7 and 245.9). It would not have failed today, but it was
  one dense lecture away from failing a perfectly good note, and a gate that
  fails correct work costs a re-run of the whole unit.

  **IT IS NOW 300 = 1.19x the densest measured unit.** That ratio is chosen
  from the failure it exists to catch: a part counted or assembled twice
  roughly DOUBLES the rate, so the bound has to sit well clear of 251.7 while
  staying far below the ~503 a duplication would produce. 19% headroom catches
  any real duplication and fires on nothing real.

  **WPM_MIN STAYS 60 AND IS NOW MEASURED RATHER THAN GUESSED.** The quietest
  measured unit is 127.6 wpm, so 60 is **47% of it** - a transcript missing
  more than half its words. That is the truncation case WPM_MIN exists for, and
  the bound is now grounded rather than asserted.

  **DO NOT WIDEN EITHER BOUND TO MAKE A GATE PASS.** Both are set from the
  measured population; a unit outside them is a finding about that unit.
SPAN_EDGE_SEC     = 10      MEASURED 2026-10-15. Census, 47 units, 94 edges.
                              WAS 60, ON NO EVIDENCE, FOR FIVE ROUNDS.

  | | head gap | tail gap |
  |---|---|---|
  | 42 lessons, all of them | 0.00 - 4.64 s | -0.69 - 4.35 s |
  | 5 calls | 0.24 - 2.16 s | -1.00 - 1.73 s |
  | **largest anywhere** | **4.64 s** | **4.35 s** |

  **60 WAS 12.9x TOO LOOSE.** It sat above the largest edge ever measured. A
  note missing its first **55 seconds** of speech would have passed the gate
  whose entire job is to catch that. This was not an unmeasured constant that
  happened to be wrong; it was wrong by an order of magnitude and in the
  permissive direction, like every other unmarked constant this project has
  found.

  **IT IS NOW 10 s = 2.15x the largest edge observed**, and 0 of 94 measured
  edges would fail it. Ten seconds of missing speech at the head or tail is a
  genuine truncation defect worth catching; a bound loose enough to pass one
  is not a gate.

  **10 OF 47 UNITS HAVE A NEGATIVE TAIL** - the last word ends AFTER the
  declared duration, by up to 1.00 s. **A negative gap is NOT a failure and
  must never be treated as one.** It is the `pjFQiLQQ` class: the manifest
  duration is a claim and the transcript extent is the measurement, so the
  measurement can exceed the claim. V5's formula uses `tail_gap > SPAN_EDGE_SEC`,
  which a negative value cannot satisfy, so the case is handled correctly by
  construction - stated here because it is surprising enough that a future
  reader will otherwise "fix" it.
FORECAST_USD    = 203.48    WAS 150.56. That was the RATE-only figure before
                             keyterm was adopted. At RATE + KEYTERM the run is
                             $203.48 and the hard stop is $213.48. A forecast
                             below the run it forecasts is not a forecast.
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
                        would stop the run after roughly ten parts. THIS IS THE SAME UNIT SLIP THAT PRODUCED THE 273.7x ERROR -
                        seconds multiplied by dollars-per-minute. The class is
                        closed by this fix and by the loss-allowance re-base.
SETTLE_FROM           = metadata.duration seconds x INPUT_CHANNEL_COUNT,
                        IDENTICALLY in the 7.2 gate and in V10. NOT the response's channel array: Deepgram returns
                        channels=1 for a stereo input while BILLING 2x.
                        AND NOT the PRE-downmix part. INPUT_CHANNEL_COUNT is the
                        channel count of the part AS SUBMITTED, recorded in the
                        same atomic write as `sent`. The 7.1a BIT_IDENTICAL branch
                        re-runs -map_channel and produces a MONO part, so reading
                        the pre-downmix count would settle every downmixed unit at
                        2x and double-count the $26.98 saving into the ledger.

  KEEP-STEREO TAIL (not in the $197.68 above).

  **CORRECTED AGAINST W0-ChannelShare v3. The previous text here was stale in
  a way that made the branch look dead.**

  It read: "3 of 3 stereo files were dual-mono, so the 7.1a keep-stereo branch
  has fired 0 of 3 and the $26.98 downmix saving is currently whole." **That is
  no longer true.** v3 measured 65 units: **50 MONO, 13 bit-identical
  dual-mono, and 2 GENUINELY STEREO** - `ljF0mZ4Y` (*Diving Into Data Part 3*)
  and `IqVSkD5Z` (*Coffee Room Impromptu Call*) - each independently re-verified
  by a second fetch and hashed on a 120 s window AND the full file, with sha256.
  **On both, `-ac 1` is a REAL DOWNMIX, not lossless.** The branch fires. The
  saving is NOT whole.

  What the saving covers: the **13 bit-identical** units, where `-ac 1` is
  byte-identical on both channels. What it does not cover: the 2 independent
  units, which must keep 2 channels and are billed 2x by SETTLE_FROM on
  INPUT_CHANNEL_COUNT.

  | | calls | min at 180.5 mean | extra billed |
  |---|---|---|---|
  | 95% lower, 1.0% | 1.9 | 345 | **$1.93** |
  | **v3 point estimate, 3.08%** | **5.9** | **1,061** | **$5.94** |
  | 95% upper, 8.5% | 16.2 | 2,930 | **$16.41** |

  **THE ARTIFACT'S "~$35 EXTRA" IS WITHDRAWN.** It is
  `0.179 x 34,472.1 min x $0.0056 = $34.55` to the cent - it applies the
  **17.9% share that v3 itself withdraws as a sampling artefact**, in the same
  document that withdraws it. A money figure derived from a retracted
  measurement, sitting in the artifact that retracts it. The figure from v3's
  own measurement is **$5.94**.

  CEILINGS, which the gate holds against rather than re-derives:
  every dated call keeping 2 channels = **$193.04**; all 235 units including
  the 42 lessons = **$201.83**. The gate must STOP, not re-derive, when it hits
  one. The share is still SAMPLED at 65 of 191, not censused.

SPEND_HARD_STOP_USD   = 213.48    DERIVED, not asserted.

  ```
  (34,472.10 calls + 294.84 undated tail + 1,569.62 lessons) x $0.0056
    = $203.48
  + $10.00 loss reserve
    = $213.48
  ```

  **THIS BLOCK SAID `$207.68` UNTIL A PROPAGATION SWEEP CAUGHT IT.** Four
  values for one constant were live at once: $207.31 (the budget artifact),
  $207.35 (this spec, twice), **$207.68** (here, labelled "DERIVED, not
  asserted"), and $203.48 (this spec). The live value is **$213.48**. A
  constant that carries four values and a paragraph insisting it is derived
  rather than asserted is a constant nobody can stop the run against. It is
  now computed from the formula above, and `pipeline/out/PLAN-TRUTH.json`
  carries `STOP` for the same reason.
  THE $200 CREDIT ARGUMENT NEVER SUBTRACTS THE PROBES THIS DOCUMENT
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

  AND THE OPERATOR-FACING LINES WERE PRE-KEYTERM. D4 adopted keyterm
  after they were written, so three published figures never entered §2.2:

  | | published | **at RATE + KEYTERM** |
  |---|---|---|
  | run with `-ac 1` | $150.56 | **$196.07** |
  | run as-is | $177.54 | **$392.15** |
  | downmix saving | $26.98 | **$35.10** |

  **AND THE `$26.98` / `6,267` ARITHMETIC WAS WRONG ON ITS OWN TERMS, TOO.**
`0.179 x 36,336.6` is **6,504**, not 6,267 — a 3.8% error in the first
multiplication. And `6,267 x $0.0056` is **$35.10**, which is the figure in the
row above labelled "at RATE + KEYTERM" — the two columns had each other's
arithmetic. Nothing built on `6,267` produces `$26.95` at any rate in this
document. **Both are withdrawn**; §2.2's keep-stereo tail carries the
replacement, derived from the share v3 actually measured, and it is computed
rather than asserted.
  All three lines are re-based above; $26.98 is withdrawn as a live figure and
  retained only as the STT-only saving.

  ONE formula, ONE figure. (34,472.10 + 294.84 + 1,569.62) x $0.0056 = $203.48   <- the run
      **THE 42 BONUS LESSON VIDEOS WERE IN NO BUDGET LINE.** They are in
      scope (section 1), ordered (section 9 step 3), submitted (section 7.2,
      'every submission'), and counted in the vault tree (courses/ = 78 paths).
      They carry 1,569.6167 MEASURED min = $8.79 and appeared nowhere. The
      $213.48 was therefore $8.79 SHORT and the $10.00 reserve was 87.9%
      consumed before the first request. A MISSING number is the one class a
      propagation sweep cannot catch, because there is nothing to propagate.
      34,472.1 min from 191 DATED calls in the regenerated
      manifest; + 294.84 min for the two units whose durations are not in
      the manifest but WERE measured - dvcEDToK 12,258.603 s
      (w0-syncceiling) and pjFQiLQQ 5,431.8 s DECODED (w0-remux; its
      container header says 4,958.7 s, +9.54%).
      + $10.00 loss reserve         = $213.48   <- SPEND_HARD_STOP_USD
      was $207.68 on 36,336.6 + 286.9 min. The 286.9 tail was
      an ESTIMATE for the undated units; both are now MEASURED at
      294.84 min combined, and 5 corrupt merged units no longer exist.
      Net -$2.99.
  The displayed component previously read $196.68 and the table four lines
  below summed to $207.35, so THREE figures were live in one code block and the
  total did not follow from the line above it. Both are gone.
                                The $1.23/$1.27 "undated units" line was
                                STT-only; at RATE + KEYTERM the two units are
                                286.9 min x $0.0056 = **$1.65**. LOSS_ALLOWANCE_USD    = 10.00     5% of ~235 units at the mean COMMIT_COST
                                $0.86 = $9.89. The old derivation named
                                3,611 parts - the segmentation design section
                                7.2 dissolved. $10 leaves 1.1% headroom, which
                                is marginal and is stated as marginal.
```

**The settled budget — every line measured, none estimated. ONE table, ONE
figure.** The per-line split is *inside* the run total, not added on top of it:

| | |
|---|---|
| **TOTAL RUN** (34,472.10 + 294.84 + 1,569.62 min) × $0.0056 | **$203.48** |
| — of which STT 34,472.1 min × $0.0043 | $148.23 |
| — of which keyterm 34,472.1 min × $0.0013 | $44.81 |
| — of which the 294.84 measured undated minutes | $1.65 |
| — of which the 42 lessons, 1,569.6167 min | **$8.79** |
| 504 loss allowance (5% of ~235 units = $9.89) | **$10.00** |
| **`SPEND_HARD_STOP_USD`** | **$213.48** |

Adding the splits on top of the total is how **$207.35 and $207.68 were both live
in one code block.** The old table's "2 previously-undated units $1.27" was
header-derived — `durprobe.json` prices `pjFQiLQQ` at its container header
(4,958.743 s) while §7.1 and AGENTS.md trap 29 both establish its decoded PCM is
5,431.8 s. Repriced on decoded PCM the undated tail is **294.84 min**, which is
the 286.9 above, priced at the **$0.0056** keyterm rate because those minutes
carry a keyterm. **Credit position: no payment card on file.** So the vendor itself enforces the
ceiling — exhausting the credit returns **HTTP 402** and processing stops. That is
a hard, vendor-enforced bound that no bug in our accounting can get past.

**But $200 < $213.48, so the vendor stop is strictly LOWER than our own gate and
fires FIRST.** Round 2 caught that "strictly stronger" was backwards. The correct
statement: the 402 is a **backstop at $200 per account**, not a ceiling at
$213.48. Two accounts are therefore required, and the split is explicit:

```
primary    DEEPGRAM_API_KEY     carries the bulk
secondary  DEEPGRAM_API_KEY_2   carries the shortfall above one account's $200
```

The ledger is **per-account** (5.3 gains an `account` field):

```
gate:  sum over accounts of (committed + settled + lost) + cost > SPEND_HARD_STOP_USD
    AND chosen_account.**Routing, which must be explicit or it is unimplementable. ** "All transcription goes through the primary" and "the secondary carries the shortfall" cannot both hold: a primary that has spent its $200 returns **402** and cannot be used at all.

```
attempt the request on the primary
  402 -> the primary is exhausted. Re-route the WHOLE PART to the
          secondary, re-commit against the secondary's own ledger, and
          record account=secondary on the receipt. Never split one part.
  other -> attribute to the account that served it
```

**The secondary is a wallet, not a worker.** Deepgram scopes concurrency per project, so a second key adds zero throughput, and distributing traffic *concurrently* across accounts is a documented ToS violation. Sequential failover on 402 is not load distribution — it is one account finishing before the next begins.

### 2.2.1 Why keyterm — MEASURED

**The first A/B on disk measured nothing.** `pipeline/out/keyterm-ab.json`
recorded `baseline_hits == keyterm_hits`, the same five terms in both arms,
`gained: []`, `lost: []`, and `Sheth` missed in **both**. Five of six terms hit
in each arm is a **ceiling effect** — the unit's vocabulary was too common for
the hint to have anything to work on. Any table claiming `Rohan 12→16` is not
in that artifact.

**A working A/B needed a selector that targets the population keyterm exists
for.** Three were built and the first two were discarded, each checked against
cached transcripts before anything was submitted:

| selector | picked | verdict |
|---|---|---|
| v1 capitalised, count 1–3 | `ABSOLUTELY, ACTUALLY, AGAIN, ANYTHING` | **discarded** — sentence-initial adverbs. Its "gains" were `Actually 3→4`. |
| v2 v1 minus the 150 most frequent word types | unchanged | **discarded** — in a 68-minute call `absolutely` twice ranks below the 150th type. Frequency cannot separate it. |
| **v3 Deepgram per-word confidence < 0.85, capitalised, 4+ chars, same exclusion** | `Alan, Rohan, John, Nicky, GrowRev, Brendan, Robbie` | **used** |

Confidence is the signal keyterm actually acts on — Deepgram's own estimate that
a token was **not** recognised. Capitalisation and frequency are proxies for it
and both failed.

**RESULT, 5 units, 454.7 min per arm, occurrence counts per keyterm given:**
`evidence/probes/nhbplus-keyterm-ab-v4-2026-10-15.json`

Split by population, because the two behave differently:

| | gained | lost | net | ratio |
|---|---|---|---|---|
| **proper nouns** — what keyterm is bought for | **15** | **3** | **+12** | **5.0 : 1** |
| filler mistakenly keytermed (`I'll`, `Sorry`, `Plus`, `Mhmm`, `I've`, `Should`) | 6 | 1 | +5 | 6.0 : 1 |
| **all terms** | **14** | **4** | **+10** | **3.5 : 1** |

**4 of 5 units won.** The single largest move is the point:

```
Rohan    13 -> 19   +6      Alan  15 -> 16 / 5 -> 6 / 17 -> 18   +1 each, 3 units
Nicky     2 ->  4   +2      John   15 -> 16   +1
GrowRev   3 ->  4   +1      Brendan 1 -> 2   +1
Robbie    2 ->  3   +1      Gian    3 ->  2   -1   Jamie  2 -> 1  -1
                                              Brennan  1 -> 0  -1
```

**9 of the 12 proper nouns touched improved.** The three that lost are a real
cost and are recorded as one: keyterm nudges probability toward the given token,
so a name it was given but which was actually said less often gets suppressed.

**The filler row is a finding, not a footnote.** Keyterming `I've` and `Sorry`
*increased* them, harmlessly — but it means the hint fires on whatever it is
given. **A production keyterm list must contain proper nouns only.** The spec
mandates the curated list in §2.2, not a generated one, and that is now a
measured requirement rather than a preference.

**VERDICT: keyterm stays, and `+$45.52` is now evidenced.** It was unevidenced
until this run. The gain is modest — 12 extra correct occurrences across 455
minutes — but it is real, it is one-directional on the population that matters,
and it costs $0.0056/min against a corpus where a misspelled instructor's name
propagates through every downstream index and backlink.

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
| Fetch concurrency | **size-adaptive, 1–38** | **THIS SAID 1** and contradicted §2's predicate and §6.3's bands. The serial figure was true when `FETCH_CONCURRENCY` was a constant, raised to 6 and then to a 1–38 band by W0-Cap, which proved ENOSPC **fails fast in 0 s** with no host spill. Serialising now costs ~1 h *measured* for no hazard the probe did not demonstrate. |
| Async policy | **RESOLVED — no async exists** | `ASYNC_ALLOWED = False` measured. The dispute was *"which of two single-shot paths?"* — and the answer is there is only one. The whole sync/async branch, its poll loop and its retention question are deleted. |
| State authority | **receipts on disk**; journal derived | Two independent truths is a desync waiting to happen. |
| Parts | **primary abstraction** | 2 GB cap, 504 recovery and tail segmentation become one code path. |
| Ordering | **docs shakedown → 1 lesson smoke test → 16 longest → cheapest** `` | A lesson-sized STT costs ~$0.16 and de-risks the paid pipeline for almost nothing. |
| PDF | **probe-first** | **RESOLVED — closed.** 0 documents need OCR. |

---

## 4. W0 probes

| Probe | Status | Question |
|---|---|---|
| **W0-Fetch** | ✅ PROVEN | per-file route works. `systemctl is-active mega-cmd-server` is **known-false**; only a real fetch arbitrates. |
| **W0-Cap** | ✅ **SATISFIED 2026-10-15** | **CLOSED.** The 4 GiB loopback is real, exact (3,936 MiB into 3,952), costs 1.7% throughput against a 41–53 MB/s network ceiling, **fails fast under real traffic** (mega-get exit 232 "Insufficient disk space" in **0 s**, no host spill), and recovers without a remount. **Fetches: `FETCH_CONCURRENCY` 1 → **the size-adaptive predicate, 1–38 in flight** — not a constant.** **This row said "1 → 6" and contradicted §2, §3 and §6.3. The raise to 6 was real; the ceiling is now the predicate's small band.** |
| **W0-Remux** | ✅ **SATISFIED 2026-10-15** | **CLOSED.** Bit-exact for MP3 (SHA-256 over 712/995 MB PCM - **the 995 MB figure appears only in this spec and in the note; w0-remux.json records 133.6/89.8 MB sources. Cite the artifact, not this line.**), near-exact for AAC (~10 KB in 1.1 GB). Real size cut is **71.2% aggregate — MP4 ~80%, MP3 NEGATIVE**. Output container must be **`.mka`**: `.m4a` fails for 98 of 235 units. |
| **W0-SyncCeiling** | ✅ **SATISFIED 2026-10-15 (take 3)** | **GENUINELY CLOSED, MEASURED ON THE CORPUS MAXIMUM.** `wiUyTRZb` — **275.93 min, the largest unit in the corpus** — returned **HTTP 200 in 182.757 s against the 600 s ceiling. Margin 3.28×, realtime 90.6×, 51,786 words. $1.55.** Artifact `nhbplus-w0-syncceiling3-2026-10-15.json`. **[History: take 1 (raw MP4) timed out; take 2 measured `dvcEDToK`, which ranks 47th of 229; a fix then asserted figures for `wiUyTRZb` that existed in no artifact — 156.2 s, 3.8×, 51,787 words. All three of those were wrong. The word count was off by ONE.]** |
| **W0-AsyncContract** | ❌ **FAILED 2026-10-15** | **`ASYNC_ALLOWED = False`.** No async job at 2 min *or* 68 min — inline results, `request_id` None. §7.2 collapses to one sync path. The "unreachable 504" claim that came with it was **calculated at 273.7×, measured at 5.7× on the 47th-ranked unit, and then asserted at 3.8× with no artifact behind it. The true figure on the corpus maximum is 3.28×** — not 273.7×, not 5.7×, and not the 3.8× that a fix supplied — see W0-SyncCeiling. |
| **W0-Pricing** | ✅ **SATISFIED 2026-10-15** | **CLOSED.** `$0.0043/min` nova-3 pre-recorded, diarization included, sourced and dated. **No per-request minimum, no rounding — true per-second billing.** |
| **W0-ChannelShare** | 🟡 **PARTIAL · v3 2026-10-15** | **SUPERSEDES THE v1 HEADLINE ("ZERO OF 10") AND THE v2 HEADLINE ("1 OF 19").** **65 of 191 calls, stratified by TYPE and MONTH — both REAL fields.** Result: **50 mono, 13 bit-identical dual-mono, 2 genuinely stereo.** Stereo share **15 of 65 = 23.1%**; genuinely-stereo share **2 of 65 = 3.08%** (95% interval ~1.0–8.5%). **THE 2× BILL IS REAL AND §7.1a's KEEP-STEREO BRANCH FIRES.** Both hits independently re-verified by a second fetch and hashed on a 120 s window AND the full file: **`ljF0mZ4Y`** (*02-12-2025 NHB Coaching Call — Diving Into Data Part 3*, mp3, coaching) and **`IqVSkD5Z`** (*2024-09-27 FF.NHB Coffee Room Impromptu Call*, mp4, other). For both, `L ≠ R` **and `−ac 1 ≠ L`** — **so −ac 1 is a REAL DOWNMIX on them, not a lossless collapse.** **WHY v1 FOUND NOTHING:** it stratified by DECLARED SIZE, which Constraint 6 says is quantised; the confirmed stereo units carry 2 GiB sentinels and fell in the bucket that got the SMALLEST allocation. **The sentinel defect as a SAMPLING FRAME.** **WITHDRAWN:** the "all type other" pattern — it did not survive a type-stratified sample. Artifact `nhbplus-w0-channelshare-v3-2026-10-15.json`. PREVIOUSLY: | **[ R4-PROP] THE EARLIER HEADLINE "ZERO OF 10 STEREO FILES, EVERY ONE BIT-IDENTICAL" HAS BEEN FALSIFIED.** An expanded sample found **`pvd0RJrB` (`ff_nhb weekly calls - competing on economics`, 2022-06-23, 175 min, declared size exactly 2 GiB — a sentinel)**: L md5 `2f144ac4…` ≠ R md5 `53ade16b…`. **The first genuinely-stereo unit in the corpus. The keep-stereo branch FIRES and that part bills at 2×.** Combined: **1 of 19 measured calls is genuinely stereo**; of 5 stereo files, 3 are bit-identical and 1 is not. At n=19 the 95% interval runs ~2%–26%, so the share is still not bounded — but it is no longer bounded above by zero. §2.2's $197.68 keep-stereo line STANDS. WHY THE FIRST SAMPLE MISSED IT: it stratified by DECLARED SIZE, and Constraint 6 says declared sizes are quantised and may not gate anything; this unit's declared size is exactly 2 GiB so it sat in the sentinel bucket, which got the SMALLEST allocation. **The sentinel defect once more — not as a threshold, not as a cost, but as a SAMPLING FRAME.** Artifact `nhbplus-w0-aclose-2026-10-15.json`. PREVIOUSLY: | **[MEASURED] 10 of 193 calls sampled (~5%), stratified by size. 7 measured, 3 fetch-failed. Every stereo file is BIT-IDENTICAL dual-mono: L md5 == R md5, proven by hash, not by an RMS threshold. 4 mono, 3 bit-identical, and the keep-stereo 2× branch fired on ZERO.** Includes `wiUyTRZb`, the corpus maximum. **The sample is too small to bound the corpus share and is not presented as if it could** — with n=10 and zero events the 95% upper bound is ~26%. Artifact `nhbplus-w0-channelshare-2026-10-15.json`. The branch stays specified; a small sample not triggering it is not grounds for deleting a 2×-billing safety branch. |
| **W0-ChannelCount** | ✅ **SATISFIED 2026-10-15** | **CLOSED — AND ITS BASIS SINCE SUPERSEDED.** It read "3 of 3 stereo files are **dual-mono**" — no per-participant separation exists. `-ac 1` is lossless and saves **$26.98**. Applied **per file** in §7.1a, not corpus-wide, so a per-participant file anywhere is detected and preserved. |
| **W0-PDF** | ✅ **SATISFIED** | closed — §8.1 |
| **W0-Egress** | ✅ **SATISFIED 2026-10-15** | **CLOSED.** `scp -r` VM→PC is byte-exact (4/4 SHA-256 match), 11/11 typography checks survive, LF preserved, no BOM. **It produced a plan correction: V6 must run on the VM source tree BEFORE the copy.** |

---

### 5.0 Fetch concurrency — THE LEVER, FOUND IN THE DOCUMENTATION

**The run is ~95% fetch, and fetch concurrency was configured by accident.**
`mega-get` is a two-line shell wrapper — `mega-exec get "$@"` — over
**`megacmd` 2.6.0**, a persistent daemon that owns the transfer queue. Its
client surface includes a documented control that is not on `mega-get --help`
at all:

```
mega-speedlimit --download-connections
  --download-connections   Set/Read max number of connections for a download transfer
mega-speedlimit --upload-connections
```

**Set to 16. It read EMPTY before, which is not the same as reading a number.**
This document therefore does not claim what the default was — only that the
limit is now explicit rather than implicit. A setting that reads back as
nothing is a setting nobody is looking at.

**Two independent axes, and the run should use both.**

| axis | knob | value |
|---|---|---|
| chunk connections **per transfer** | `mega-speedlimit --download-connections` | **16** |
| transfers **in flight** | the fetch pool | 4 |

4 transfers x 16 connections = **64 parallel chunk streams**, against 4 x
whatever the unset default was. Raising the in-flight count multiplies sockets;
raising per-transfer connections does it without multiplying `mega-get`
processes or API folders.

**WHAT THIS IS NOT.** The throughput gain is **NOT MEASURED.** Scaling is not
linear and was not assumed here: MEGA may rate-limit per account, and the VM's
NIC may cap below 100 MB/s. The measured rate at 4 in-flight was **15.8 MB/s**,
which put the 153.81 GiB fetch at **2.90 h**. The lever is in place and the
before-number is recorded; the after-number is **measured during the run, not
asserted here**, and if it does not improve, the finding is that the bottleneck
was never concurrency.

## 5. State — the machine that actually prevents double-billing ``

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

> **`queued` APPEARED IN THIS DIAGRAM AND WAS DEFINED NOWHERE - NO MEANING
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

### 5.3 The single global spend ledger ``

Rev 0 said "reserved under `flock`" with **no file and no path**, while every
named artifact was per-**unit**. A per-unit lock cannot serialise a global sum:
16 workers can each read a stale total and jointly overshoot.

```
LEDGER = /data/nhb/_meta/spend.json     PER ACCOUNT:
    {"accounts": {
        "<account_id>": {"committed":USD,"settled":USD,"lost":USD,"released":USD}},
     "totals":      {"committed":USD,"settled":USD,"lost":USD,
                     "released":USD}}      FIXED - the field was OMITTED
                     while every per-account object declared it, so the gate
                     formula in the next paragraph was stated over a field the
                     schema did not have.
    section 2.2 asserted a per-account ledger and a per-account gate; this
    section still described a single global object, so an implementer following
    IT would build one pool and the second key would never be used.
LOCK   = /data/nhb/_meta/spend.lock     flock, held across READ-CHECK-WRITE
```

Commit and settle are each one atomic ledger mutation under that one lock:

```
commit:  committed += cost        settle:  committed -= cost;  settled += actual
release: committed -= cost          lost:    committed -= cost;  lost += actual
                                   released += cost
                                   A `reserved` part is released ONCE.
                                   Compare-and-set inside the flock: read
                                   `released`; if this part_id is not already
                                   in the released set, add cost and add
                                   part_id. Two resume passes over one part
                                   would otherwise double-count, and a
                                   double-counted release frees budget that was
                                   never spent - which is how a hard stop
                                   becomes a soft one without any code
                                   appearing to change.
                                   section 5.4's resume table requires a
                                   release for a part that was committed and never
                                   sent. Without this mutation that amount is either
                                   double-counted forever or never returned.
```

**Ledger reconciliation is derived, never authoritative** — `bin/rescan.py`
rebuilds it from `receipt.json` parts, and **receipts win** on conflict. This
keeps single-authority (no desync) while giving the global sum a named home.

### 5.4 The resume branch — explicit, because ambiguity here costs money ``

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
**"ATOMIC" WAS ASSERTED THREE TIMES AND SPECIFIED NOWHERE.** The word
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
R4 re-measured across **every** declared size, primaries and alternates:

| test | count |
|---|---|
| `bytes % 1024 == 0` | **335 / 335 — every declared size in the corpus** |
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
threshold    = declared + 0.5 x quantum          # ONE rule, no max()

# WHY THE max() IS GONE. `max(1.10 x declared, declared + 0.5 x quantum)`
# selects the 1.10x arm only when declared >= 5 x quantum. EVERY unit in this
# corpus is KiB-exact, so `sentinel(b)` is TRUE for 335 of 335 declared sizes
# and the `else` arm below is UNREACHABLE. It is deleted rather than left
# describing a regime that cannot occur. See section 6.4.

if sentinel(declared):  -> the overrun check is DISABLED for this unit
   # correct and intended: the declared size is a display value, so a kill
   # threshold derived from it is meaningless. The cap is enforced by the
   # LOOPBACK, which measures ACTUAL bytes on disk - see 6.2.
else:                    -> threshold as above
   # REACHABLE FOR ZERO UNITS TODAY. Retained only so a future corpus with
   # genuinely unquantised sizes has a rule; it must be re-validated then.
```

**Never kill on a rounded baseline.**

---

## 7. STT

### 7.1 Remux and segment — the majority path

`ffmpeg -vn -c:a copy` every unit. **137 of 235 are MP4.**

**Output container: `.mka`, never `.m4a`.** Verified 2026-10-15. `.m4a` is an
MP4 container and **cannot hold an MP3 elementary stream** — it fails rc=234
*"Could not write header (incorrect codec parameters)"* for **98 of 235 units**.
`.mka` (Matroska audio) carried every sample, MP3 and AAC alike.

> **NOW VERIFIED AT THE VENDOR, which is where it mattered.** The only
> `.mka` ever *submitted* had been AAC, so the container that rescues **97 MP3
> units** was unverified at the Deepgram boundary — and under Constraint 7 an
> HTTP 400 class there is 97 paid-and-unrecoverable failures. A 5-minute slice of
> a real corpus MP3, remuxed to `.mka`, submitted: **HTTP 200, 911 words, 300.0 s.**
> **$0.03 to close.**

> **THE REMUX IS MANDATORY, NOT AN OPTIMISATION ``.** Submitting the **raw
> 1,539 MB MP4** of the corpus's longest call **did not complete** — it timed out
> after >1,800 s. The remuxed 280.7 MB `.mka` of the same audio completed in
> **105.1 s**. Bandwidth was never the difference: the remuxed file uploaded at
> **150.8 MB/s**, so 1,539 MB is ~10 s of transfer. What differs is that `-vn`
> strips the **h264 video track**. 137 of 235 units are MP4; under Constraint 7 a
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
| **corpus** | 235 | **153.81 → 42.17 GiB (71.2%)** | |

The real saving is **104.21 GiB, not the 124.43 GiB** an 85% assumption implies.

**Do NOT transcode to 16 kHz PCM.** Measured at **−166% size on MP3** — a 133.6 MB
source becomes 355.9 MB of `s16le`. 98 of 235 units are MP3. Any 16 kHz path must
use FLAC or Opus, never WAV.

> `-ac 1 -ar 16000` are **output** options and must follow `-i`. Placed before it
> they parse as input options and ffmpeg fails *"Option sample_rate not found"*.

**Size guard on the remuxed output ``. THE OLD THRESHOLD WAS DERIVED
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
| largest remuxed unit **ever submitted** | `dvcEDToK`, **280.7 MB**, HTTP 200 — **not `wiUyTRZb`, which was never submitted** |
| its margin at 204.3 min | **5.71×** measured — **on the 47th-ranked unit.** The worst case is untested. |
| upload rate measured | 150.8 MB/s → ~2.5 s of transfer |
| the guard that matters | **not a size threshold.** It is `SEGMENT_SEC`, and `SEGMENT_SEC` is dead code under a 2 GB `CAP_BYTES` the 385 MiB maximum cannot reach (T6 #8). |

**So the size guard is withdrawn rather than re-derived.** The honest measured
maximum is **383.7 MiB / 402.31 MB** — **this line said 385.1 MiB /
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

#### 7.1a Channel handling — DETECT per file, never choose corpus-wide

**THE DETECTION, IN FULL.** The section said "detect per file" and never gave the
command, which is the same defect as the missing request payload in §7.2.0 —
mandate without mechanism. It runs on the REMUXED part, before any submission,
and its output is the `INPUT_CHANNEL_COUNT` that `SETTLE_FROM` bills on:

```
# -select_streams a:0 -show_entries stream=channels -of default=nw=1:nk=1
ffprobe -v error -select_streams a:0 -show_entries stream=channels \
        -of default=nw=1:nk=1 "<part>.mka"
# -> 1  or  2.  Any other value is a hard stop, not a default.
```

`-select_streams a:0` matters: a file can carry more than one audio stream and
the first is the one submitted. `-of default=nw=1:nk=1` prints the bare number
with no key, so it is captured directly into the receipt rather than parsed.

**WHY A 65-UNIT SAMPLE IS NOT A GAP IN THE POPULATION.** The channel count is
read on **every** file as part of a step the pipeline performs anyway, so by the
time any money is at risk the population is **exactly measured, not sampled**.
The 65-unit census exists only to PRICE the budget and to VALIDATE the ceiling
before the run starts; `SETTLE_FROM` bills from the per-file value and the gate
stops if the running total passes the ceiling. **The residual risk is bounded by
construction rather than by sample size.**

The channel count therefore cannot be read corpus-wide, and §2.2's share is a
planning figure that the run replaces with a measurement.
 ``

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
| corpus-wide full decode at 61.8x | **9.80 core-hours** |
| on this 2-vCPU VM | **4.90 wall-hours = 0.204 DAYS** |
| Azure cost of that alone | **$0.56** |
| same measurement over a **90 s window** | **4.6 minutes** |
| section 7.1a remux (`-c:a copy`, stream copy, no decode) | 0.26 h |

**The window is the entire difference between 11.8 days and nothing.** §7.1a
calls this "one extra ffmpeg pass per part"; on the corpus it is the dominant
cost in the pipeline and nobody priced it. **A 90-second window classifies the
L/R relationship** — dual-mono is dual-mono from the first minute — so the
full decode buys nothing. Specified as a window below.

**GUARD BEFORE MEASURING.** `pan=mono|c0=c1` has no `c1` on a mono input
and errors. **82.1% of sampled minutes are mono** (10-file sample; the 65-unit v3 sample gives 76.9% by COUNT), so the unguarded block below
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
> **AND REST ON `pipeline/out/canon-probes.json`, WHICH
> HAS NO `date`, NO `handle`, NO HASHES AND NO MEASUREMENT** — and it sits
> **outside** `evidence/probes/`, outside the pack every other claim here cites.
> Two claims unblock real money: the `.mka` container for 97 units, and the
> lossless `-map_channel` downmix that produces the ENTIRE saving. Both rest on
> one boolean (`B24_map_channel_lossless: true`). **** and both measured
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
> **[v3 2026-10-15 TIGHTENS THIS AND IT MATTERS FOR THE MONEY.]** Two of 65 sampled
> calls are genuinely stereo and for BOTH **`-ac 1 != L`** — verified on a 120 s
> window AND on the full file:
>
> | | |
> |---|---|
> | the **$34.85** saving | proven lossless **on bit-identical dual-mono** (13 of 65) |
> | a genuinely-stereo part | **`-ac 1` is a REAL DOWNMIX, not a lossless collapse** |
> | §7.1a's topology branch | **not optional — it is what keeps the saving honest** |
>
> Projected: **~3.1% of 191 calls ≈ 6 parts billed at 2×, roughly +$35.**
> **Not the $197.68 worst case** — that stays the ceiling to hold against.
>
> **A PROCESS FAILURE RECORDED BESIDE IT.** The first v3 run died at 25 of 65 with
> rows whose handles did not match their results: **every command inside a
> `while read` loop must have stdin closed**, and `ffmpeg`/`ffprobe` read stdin by
> default. Caught only because one handle returned two opposite verdicts across
> two runs — the same family as v2's resolver bug and as the two-unit field join
> that began this. **All pre-fix rows were discarded, not averaged.**
>
> VERIFIED: SHA-256 of the decoded
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
otherwise      -> AMBIGUOUS.      ONE BRANCH REMAINS UNOBSERVED. `INDEPENDENT` NO LONGER IS.
   This read: "`INDEPENDENT` and `AMBIGUOUS` fired on **0 of 3** stereo files —
   all three were dual-mono, so the delta was uniformly 0.00 dB and neither
   branch was ever taken. They are specified, not validated."
   **W0-ChannelShare v3 falsified the first half of that.** Of 65 units,
   **`ljF0mZ4Y` and `IqVSkD5Z` read INDEPENDENT**, so the branch has a real
   non-zero delta to work on and `-ac 1` on those is a genuine downmix.
   **`AMBIGUOUS` is the one branch that has still never fired** and remains
   specified-but-unvalidated. The share is no longer UNKNOWN either: **3.08%
   genuinely stereo, 95% interval 1.0–8.5%**, over 65 of 191 dated calls. That tail is priced in §2.2's keep-stereo
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

One extra ffmpeg pass per part **— FOR A STEREO PART ONLY, AND THREE, NOT
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

#### 7.2.0 THE REQUEST, IN FULL

Eight separate sections each mandate one flag and **no section listed them
together**, so an engineer holding only this document could not write the POST
at all — and the 25-concurrency ceiling is derived from exactly one of them.
Omitting `diarize=true` silently doubles the ceiling to 50 with no gate to
notice. **This is the complete request:**

```
POST https://api.eu.deepgram.com/v1/listen
     ?model=nova-3
     &diarize=true            <- BINDS THE CONCURRENCY CEILING at 25, not 50
     &smart_format=true
     &punctuate=true
     &utterances=true         <- section 5.1's assembled.json is built from
                                 results.utterances; without it there is nothing
                                 to hash for V12
     &language=en
     &mip_opt_out=true        <- Constraint 6a. NOT optional, NOT conditional.
                                 Sent on EVERY request including retries.

Authorization: Token $DEEPGRAM_API_KEY
Content-Type:  audio/x-matroska      <- the .mka remux, never .m4a
Body:           the remuxed part, streamed from disk
```

| flag | section that requires it | if omitted |
|---|---|---|
| `model=nova-3` | §0 D2, §2 | different model, different rate |
| `diarize=true` | §0 D3, §10.1, §11.1 | **ceiling silently 25 → 50**, and no diarisation clusters |
| `utterances=true` | §5.1, §11.1 V12 | `assembled.json` has nothing to build from; V12 unevaluable |
| `smart_format` + `punctuate` | §7.3 response shape | word/utterance counts shift |
| `language=en` | §0 | auto-detect, non-deterministic on 2-channel files |
| `mip_opt_out=true` | Constraint 6a | **a data-protection flag is dropped from every request** |
| `keyterm=…` | §2.2.1 | optional; costs $0.0013/min |

**Retry carries the identical request.** A 429 or a 402 re-POST must reuse the
same URL and the same body; only the account changes, never the payload.

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

**MEASURED, not calculated ``.** The longest call in the corpus was
submitted on its own and timed:

```
FIRST PROBE, SUPERSEDED - retained as one line, not a block.
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

> It read `wiUyTRZb · 275.9 min · HTTP 200 in 156.2 s · MARGIN 3.8x · words
> 51,787`, and the claim was that **every one of those figures appears in no
> artifact**.
> **THAT CLAIM WAS ALSO WRONG.** `pipeline/out/canon-probes.json` carries them:
> `B1_worst_case: {unit: 2025-02-19-coaching-2-wiUyTRZb, http: 200,
> server_s: 156.2, margin: 3.8, audio_min: 275.9}`. The grep was scoped to
> `evidence/probes/` and the result was asserted **globally** — a narrow
> search stated as a universal negative, the same class of error this project
> has now made four times.
> The correction that mattered was still right: the figures were **measured**
> and **wrong** (real: 182.757 s, 3.28×, 51,786 words). But the evidence existed,
> and the right response to a wrong number is to re-measure and supersede it —
> not to record that it was never measured. They were produced by re-attributing `dvcEDToK`'s measurement to
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
> **This said "25 hours of sustained load" and that was the same 60x
> unit slip a second time.** There is no 25-hour run: the whole run is ~1.4 h and
> the STT stage is 15 minutes.**, and a pass is not a capacity guarantee.
>
> The prediction from `dvcEDToK`'s measured 119× realtime is ~139 s against
> 600 s, which is comfortable — **but that is an extrapolation, and the previous
> extrapolation from this same method produced 273.7×, wrong by 48×.** The
> gate exists to replace an extrapolation with a measurement. Until it is run,
> W0-SyncCeiling is **OPEN**, and §4 reads 🔴 OPEN, not ✅ SATISFIED.

> **The 273.7× was a 60× UNIT SLIP, not an extrapolation error. ** 600 s
> of server time at 126× realtime is 75,600 SECONDS = 21.0 hours. The artifact
> wrote that as 75,525 MINUTES / 1,259 hours. Corrected: 21.0 / 4.6 = **4.57×**,
> which agrees with the measurement. The arithmetic in correct units already
> matched reality — the units were wrong. **This is the same defect as B4**,
> seconds × dollars-per-minute, and it is why a calculated margin is not a
> margin.
>
> **AND THE MEASUREMENT WAS ON THE WRONG UNIT. ** `dvcEDToK` is 204.3 min,
> not the corpus maximum. **46 calls are longer.** The worst case is
> `wiUyTRZb` at 275.9 min. Scaling the measured 105.1 s gives ~142 s →
> **4.2× margin**, not 5.7×. W0-SyncCeiling was **REOPENED** for `wiUyTRZb`.
> **It is still open.** The 4.2× is a scaled prediction, and a
> later revision replaced it with an asserted 3.8× that had no artifact behind
> it. Neither is a measurement. It was skipped because
> `dvcEDToK`'s manifest `dur_s` is `None`, so it never appeared in the
> duration-sorted list used to pick the worst case. **The old closing line
> here RECOMMENDED taking that measurement. It has been taken, at the cost of
> $1.14, and the recommendation is withdrawn.** **A margin calculated for the worst
> case is not a margin.**

| Dissolved | Was | Now |
|---|---|---|
| the sync-cutoff problem | 155 of 193 calls (82.4% of minutes) exceeded the cutoff | **0** exceed it |
| `SYNC_SEG_SEC` segmentation | introduced because 155 calls needed it | unnecessary for all 235 |
| request count | ~3,611 | **~235**, one per unit |
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

**But it must still be split ``** — not for cost, for one reason: the docs
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
| `sparse` | **2** | *AC eBook*, *AC_Book* — 340 pp each, `page_cap: 200`. **58.8% READ, 41.2% NEVER OPENED.** 1,372 words is real; completeness is not. |
| `raster` | **0** | needs OCR; none is proven free, so it would ship `empty_extraction` and **never be OCR-billed**. Vacuous. |

**48 + 2 + 0 = 50, and the gate is closed on 50 of 50.**

**65,985 recoverable words**, and the parts account for every one of them:
`already_text` 42,683 + `recovered_text` 21,930 + `sparse_text` 1,372 +
`raster` 0 = **65,985**. Zero documents require OCR.

#### WHY THE FIRST ARTIFACT SAID 47, AND WHY THE ORIGINAL 48 WAS RIGHT

`pdf-fallback-audit.json` v1 reported `47 + 2 + 0` against its own declared
`total: 50` — **the parts did not sum to the total, and the run printed a
confident summary table anyway.** The document missing from the reclassification
was `6. 7-Figure VSL Script Template`, which is not a fetch failure and not a
name mismatch *between the two passes*. The mechanism, from line 27 of the
audit script:

```python
TARGETS = [..., "7-Figure VSL Script Template", ...]   # manifest: "6. 7-Figure VSL Script Template"
...
r = by_name.get(name)
if not r: continue          # <- silently skips the document
```

The hand-typed target list was missing the `6. ` ordinal. The lookup missed.
`if not r: continue` swallowed it. Seven probes were run, **six** were reported,
and the summary printed without a missing-unit notice.

**At 814 words on one page it is the least sparse document in the set.**

Both defects are fixed in `evidence/probes/nhbplus-pdf-fallback-audit-v2-2026-10-15.json`:
the target list is now **derived from the ceiling artifact** (every result whose
`class` is `degenerate_geometry`) so there is nothing to mistype, and a lookup
miss is now a `SystemExit` with the name rather than a `continue`. The audit
asserts `audited == targets` and `parts == total` before writing.

**The 48 was correct and the artifact was incomplete. Both are now true at once.**

#### THE PAGE CAP — all THREE capped documents, named

`page_cap: 200`. Three of 50 PDFs hit it. **677 of their 1,277 pages — 53.0%
— are never opened, and they carry 21,577 words, which is 32.7% of every word
in the PDF half of the corpus.**

| document | pages read | never opened | words |
|---|---|---|---|
| `2. AC eBook` | 200/340 | 140 | 691 |
| `500-page-swipe-file-clayton-makepeace_compress_1` | **200/597** | **397** | **20,205** |
| `AC_Book` | 200/340 | 140 | 681 |

`500-page-swipe-file-clayton-makepeace_compress_1` was invisible to the earlier
completeness note, which named only the two 340-page eBooks. **It is the single
largest document in the set by words** — 20,205 of 65,985, nearly a third —
and it is the one most damaged by the cap.

**Raising the cap is a decision, not an oversight.** At 101 words/page the
remaining 397 pages are ~40,000 words, about 60% more text than the whole PDF
half currently yields. Cost: zero (pypdf is installed, extraction is local). The
cap exists only because the first probe read 340+597+340 pages in one pass.
**The spec ships `page_cap: 200`; this is the measured cost of that choice and
it is recorded so the choice can be revisited with the number in hand.****Stereo billing, measured 2026-10-15 ``.** A 120 s stereo clip and a
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
Bounded by measurement — **and the bound has moved since it was written.**
It read "3 of 3 stereo files were dual-mono, so the keep branch fired 0 of 3."
W0-ChannelShare v3 found **2 of 65 genuinely INDEPENDENT**, on which `-ac 1` is
a real downmix, so the keep branch **does** fire and the input count **does**
exceed 1 on a real unit. The gate must be correct on it. **§2.2 carries an explicit
keep-stereo line, bounded at 2x the corpus: +$197.68 in the worst case where
every unit keeps stereo, against a $213.48 stop.** Earlier revisions claimed
this line existed twice while grepping for it returned only the claim itself.

**Links: `/Annots` is the ONLY authoritative link layer.** *Swipe* carries 400
raw annotations, **201 distinct** — half boilerplate. Text-layer URLs are mangled
by wrapping (`Calcu` / `dit#gid=5683798` / `lator`). Never recover a URL from
display text.

### 8.2 The 2 sparse PDFs — decided, not deferred ``

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

### 8.3 The 8 non-OOXML, non-PDF documents — previously unhandled ``

6 `.txt` (incl. all 5 `Resources Links`), 1 `.png` (`Pick Primary Color`),
1 `.zip` (`Lazy Loading Code`, 296 MiB).

- **6 txt** → stdlib read; the 5 `Resources Links` need the §10.2 course prefix.
- **1 png** → **never decoded, never rendered.** Ships as a manifest entry naming
  the file and its dimensions only. It is the one document that collides head-on
  with Constraint 1, and the resolution is that it contributes **no bytes**.
- **1 zip** → enumerate members, extract text-bearing members via stdlib
  `zipfile`, with a **size-triggered memory guard** (§8 preamble).

---

## 9. Ordering ``

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
vault/courses/<Course>/<CLEAN>.md                     78 paths   NEW
vault/written-hands/<year>/<MM Month>/<CLEAN> (written hand).md   37 paths
vault/library/…                                     36 paths
vault/00 Home.md
vault/00 Topics.md                   NEW - §10.3

`courses/` was MISSING and holds 78 of the 344 paths - 36 course_doc files in
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
carries `handle/verbatim/kind/clean` and no `path` for any of them ``.
`design-names.py` must emit one, and V8 must assert its existence.

> **CLOSED 2026-10-15 by build, not by prose.** `design-names.py` now writes
> a `path` for all 109 documents. Measured: `documents with a path : 109/109`,
> `document path collisions : 0`, `total clean paths : 344` = 193 + 42 + 109.
> Previously it wrote `path` for calls and lessons and **never for a document**,
> so V8 failed on its first run and the §9 docs shakedown could not complete.

### 10.1 Frontmatter value domains — asserted, not merely counted ``

Rev 0's V8 asserted a **field count**, so these all shipped: `duration: 0` on 3
units, `speakers: null`, and a `type: mastermind` that is **not in its own
vocabulary** - it lists six, not five.

```
date      ^\d{4}-\d{2}-\d{2}$   or  unknown
duration  integer >= 0          or  unknown     (minutes, never "3h 14m" -
                                     LOWER BOUND FIXED 1 -> 0. MEASURED: 2 of
                                     235 units are sub-minute - A2dWSZAK at
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

### 10.2 Filenames — the repair surface is larger than §15 claimed ``

Rev 0 asserted clean rules in §10 and listed three violations in §15, 25 lines
below, with no cross-reference. **67 of 296 names (23%) are affected**, not three.

| Defect | Measured | Fix |
|---|---|---|
| dash splitter mangles intra-word hyphens | **measured: 38 of 193 calls, 46 of 344 total at the time; **re-measure on 344**, of which **0** are true intra-word mangles** — the 7 are all intact. The old "50 of 229" was wrong on both terms: 229 is *units with a duration*, not a path count, and 's 296 excluded the lessons. It once contained (`Ron-Lynch`, `Biz-Op Blueprint`, `Clean Biz-Ops`, `Pre-Openings`, `CMO-CRO Roles`, `Call of Duty Biz-Ops`, `7-Figure Fill-In-The-Blank`). **The spec previously said 67 of 296 - the denominator 296 excludes the 42 lessons, one of which is damaged.** | normalise dash **styles** only; never split `[A-Za-z]-[A-Za-z]` |
| `Call` stripped mid-phrase | `Call of Duty` → `of Duty Biz - Ops`; `Call Booking Page` → `05 5 Booking Page` | strip `Call` only as a whole token outside a compound |
| `None` leaked into 3 filenames | `None Selling To Women 3.0.md` etc. | a missing date **omits the prefix**, it does not fill it. V8 asserts no filename contains `None` |
| extension-in-stem | **2 `.mp4.md`** paths | strip a trailing media extension before appending `.md`. V6 checks **stems**, not just extensions |
| 5 `Resources Links` collide | `collisions.documents = 1` while 5 files share the stem | apply the course prefix; the script computes it and discards it |
| ~~23 brand tokens, 4 underscores survive~~ | **RESOLVED** — 0 brand tokens, 0 underscores, measured | — |
| **dropped call** | `10-31-2022 NHB+ Mindstream Call` absent — **RESOLVED**, `drop_lead` no longer eats `Mindstream`; **193 call paths, none dropped** | drop `Mindstream` from the alternation; **and add a guard: if `tidy()` returns empty, fall back to `topic`, never `continue`** |
| lesson ordinals renumbered | source `7. AC - Unannounced bonus` → `02 …` | preserve source numbering |
| dates lost | the corpus's **only** ISO-dated name (`2024-09-27`) is the one that lost its date | accept `YYYY-MM-DD` as well as `M-D-YYYY` |
| **2 calls undated** | `undated-other-5-MmMmABhJ`, `undated-other-5-x3Mi0JJL` — **191 of 193 dated** | §10 needs a day; list them, do not leave them silent |

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

### 10.3 `00 Topics.md` — the corpus's own index, which was thrown away ``

**The strongest objection to rev 0's design:** the vault is organised by **when a
call happened** — the one axis a paying member never uses. The topic axis is
*already in every filename* and required **zero inference** to recover. The
cleaning pass read it, stripped the type boilerplate off it, mangled 24% of its
hyphens, and then the vault design discarded it.

> **THE PREMISE WAS FALSE AND HAS NOW BEEN MEASURED.** This section
> previously claimed the topic axis "already clusters into ~50 groups of
> 1–13". **It does not cluster.** Measured over all 235 manifest topics:
>
> | | claimed | **measured** |
> |---|---|---|
> | groups | ~50 | **225** |
> | singletons | — | **221** |
> | units sharing a stem with ≥1 other | — | **4 of 235** |
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
> match **0 of 235 topics.** The real boilerplate, measured: `nhb theory` on
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

**Built by deterministic stem extraction only** — **the rules below REPLACE
the ones that matched 0 of 235 units.** In this order, because the order is
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

| Gate | Status | Assertion |
|---|---|---|
| V0 | worklist integrity: **344** rows, never a glob — **formula in §11.1** |
| V1 | fetch caps: ENOSPC proven; **no kill fired on a sentinel `declared`** — **formula in §11.1** |
| V2 | remux/segment: no part ≥ `CAP_BYTES` — **formula in §11.1** |
| V3 | STT contracts: **the one sync path** (§7.2 deleted the other — there is no async job); **`sent` persisted before the socket opened**; `http_status == 200` AND `response_complete` both required — **formula in §11.1** |
| V4 | **three-way duration reconcile** — formula in §11.0 |
| V5 | **span coverage** — formula in §11.0 |
| V6 | **zero media extensions under `vault/`** — the list must include **`.mka`**, the container §7.1 mandates, plus `aac\|opus\|ogg\|mpga\|mkv\|webm\|mov\|m4a` — **AND** no stem matches `\.(mp3\|mp4\|mov\|m4a\|wav\|flac\|mka)$`. **ADD `.png`:** the corpus contains exactly one image (`guNkBLaZ`, 151,552 B, §8.3) and Constraint 1 is absolute — no media-shaped file reaches the operator's PC. **AND A FLOOR, WHICH IS THE PART THAT WAS MISSING:** `vault/` currently holds **0 files**, and every check above is a *ceiling* — **an empty tree satisfies all of them and returns PASS.** That is this project's own empty-vs-empty trap. **V6 must also assert `count(vault/**/*.md) >= 344 and every note matches section 10's tree
     # 344 = 193 calls + 42 lessons + 109 documents.
     # >= not ==, and this is CORRECTION: section 10's own tree also names
     # `00 Home.md` and `00 Topics.md`, so a flawless run emits 346 and an
     # equality test would fail it. The floor's job is to stop an EMPTY tree
     # reading as PASS; it is not a manifest of the whole vault.`.** Until that floor exists, V6 green means nothing. — **formula in §11.1** |
> **AND EVERY CORPUS FORMAT IS CURRENTLY UNCATCHABLE BY V6.** The corpus
> contains `pdf, docx, pptx, txt, xlsx, png, zip`. None is in the extension list,
> none matches the stem regex, and a `.pdf` or `.docx` under `vault/` would pass
> V6 outright **while violating Constraint 1.** The list above is an audio list
> applied to a corpus that is not mostly audio. **`pdf\|docx\|pptx\|xlsx\|txt\|png\|zip`
> are added to the banned set**, because an extracted document ships as `.md` and
> the *source* must not ship beside it.

> **AND `attachments/` WAS MANDATED BY THE DOCUMENT THAT WAS NOT THE SPEC.**
> `VAULT-STRUCTURE.md` specified an `attachments/` directory holding raw
> `docx` / `pptx` / `xlsx` **"as fetched"** — which is the Constraint 1
> violation, written into the structure of the deliverable itself, by a
> document subordinate to this one. It was written first and written as though
> it were authoritative, which is why the conflict survived five review rounds.
>
> **Resolved: `attachments/` does not ship.** The binaries are fetched, parsed
> and converted to markdown on the VM, and destroyed with it in phase 7. The
> same file's **C2 (verbatim vs clean filenames)** and **C3 (index-note tree)**
> conflicts are resolved in the same direction, and all three are recorded at
> the top of `VAULT-STRUCTURE.md`.

| V7 | reduction diff: re-render from receipts, byte-compare — **formula in §11.1** |
| V8 | **frontmatter value DOMAINS (§10.1), not a field count; every document has a `path`; no filename contains `None`** — **formula in §11.1** |
| V9 | counts 37/36/36; **and every manifest unit with `kind == "calls"` has exactly one emitted note** (193 rows in `manifest-v3.json`). **`scope-final.json` has no `call`/`calls` kind — its kinds are `audio`/`written_hand`/`course_doc`/`orphan_doc` — so the previous `kind == "call"` matcher hit 0 handles and V9 passed VACUOUSLY on the one confirmed live defect, the dropped `10-31-2022 NHB+ Mindstream Call`. ** V9 previously checked documents only, so it **structurally could not catch the dropped call** — **formula in §11.1** |
| V10 | `settled + lost ≤ SPEND_HARD_STOP_USD`, derived from receipts, **using the same settle quantity as the §7.2 gate** — **formula in §11.1** |
| V11 | egress SHA256 per-file match — **formula in §11.1** |
| **V12** | **Identity Binding — NEW, and the most important gate here** |
| **V13** | **`00 Topics.md` — NEW. POPULATION IS 230, NOT 225.** **re-scoped it to what measurement supports; found it still named THREE populations.** It said "225 rows", "1 row per emitted note", and §11.2's body gated "every note under `vault/calls/`" (193). **The population is 235 notes — 193 calls + 42 lessons.** 225 is a GROUP count from 's clustering, not a note count, and the two cannot both be true. **Now: 235 rows, one per emitted note, plus a `recurs` column.** §11.2's group clauses are deleted below. |
| **V13** (population note) | 's own table is also internally inconsistent: `225 − 221 = 4` multi-groups, which must hold `235 − 221 =` **9** units, but the same row says "4 of 235". The **group count** is 4; the **units inside them** is 9. **** |

### 11.1 V12 — Identity Binding ``

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
 3. H(U) values are PAIRWISE DISTINCT across all 235 audio units
 4. EXACTLY ONE note under vault/ renders utterance text hashing to H(U)
 5. no two units share a NON-NULL request_id
 6. effective_spend reconciles to COMMIT_COST, and ffprobe(U) is within 2% of
    the metadata.duration in U's OWN response

 > **CLAUSES 5 AND 6 WERE MUTUALLY EXCLUSIVE, AND §12.1 DELETED THE
 > EVIDENCE FOR CLAUSE 6.** had asserted "`request_id` is None for EVERY
 > submission" and therefore removed the `request_id` column from AUDIT.md.
 > **Two later artifacts contradict that**, and predates both:
 >
 > | artifact | `request_id` |
 > |---|---|
 > | `nhbplus-w0-asynccontract-2026-10-15.json` | `None` |
 > | `deepgram-eu-limits-and-chain-proof-2026-10-15.json` | `01a13cfc-1b03-7e10-94cb-a448d81cb512` |
 > | `nhbplus-w0-syncceiling3-2026-10-15.json` | `01a13ec6-9208-7c90-a68d-0209a8e6be33` |
 >
 > **So 's generalisation was wrong**: it held for the asynccontract's
 > request SHAPE and was carried to every submission. With `request_id` present,
 > clause 5 becomes **measurably testable** rather than vacuous — the opposite
 > of what the fix assumed — and clause 6 becomes evaluable instead of
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

 > **history, kept because the failure is the point:** the clause as first
 > written ("no request_id appears under two different unit ids") FAILED on a
 > flawless run, because None appears under all 235 unit ids. The fix was right
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

**FIVE EXIT CODES WERE DECLARED FOR FOURTEEN GATES.** Nine gates had no
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

### 11.0 The two gate formulas V4 and V5 assert, written out

**Both gates were a single line naming a check, with no rule, no threshold and
no failure behaviour.** That is the same defect as §7.2.0's missing request
payload: a mandate with no mechanism. An engineer holding this document could
not implement either.

#### V4 — three-way duration reconcile

Three durations exist for every unit and they do not agree:

| source | what it actually is |
|---|---|
| `manifest.media.dur_s` | the value MEGA reports; may be a SENTINEL (a display value, not a measurement) |
| container header | what the file's own metadata claims |
| decoded PCM | what `ffprobe -count_frames`, or the assembled transcript's own extent, actually contains |

**`pjFQiLQQ` is the corpus's known divergence: header 4,958.7 s against decoded
5,431.8 s, +9.54%.** Every other unit measured agrees to within a millisecond
(`16,556.208` vs `16,556.207`). So the rule cannot be "they must match" — it must
be "disagreement is bounded, and the larger value wins for billing."

```
V4(d_manifest, d_header, d_decoded) :=
    # the DECODED value is authoritative. It is the only one that is a
    # measurement of the audio rather than a claim about it.
    d_authoritative := d_decoded

    # a disagreement is a FINDING, not automatically a failure
    spread := max(d_manifest, d_header, d_decoded) - min(d_manifest, d_header, d_decoded)
    ratio  := spread / d_authoritative

    FAIL if d_decoded is missing          # no decoded value = no authority
    FAIL if ratio > DURATION_TOLERANCE    # 0.10, i.e. 10%
    WARN and record if ratio > 0.02       # 2%: worth a human glance
    PASS otherwise
    NON_VACUOUS iff d_decoded is not None

    # A sentinel d_manifest is EXCLUDED from the spread entirely. It is a
    # display value; including it manufactures disagreement that is not there.
```

**BILLING USES `d_authoritative`, NOT `d_manifest`.** On `pjFQiLQQ` that is
the difference between 4,958.7 and 5,431.8 minutes — the 286.9-minute tail that
was an estimate is now 294.84 measured. Billing from the header would have
under-charged by 9.54% on that unit and never shown why.

#### V5 — span coverage

Catches the failure mode a words-per-minute check cannot: an assembly that
**drops the beginning or the end of a transcript** and still looks plausible in
the middle. `WPM_MIN` catches "too few words overall". `SPAN_EDGE_SEC` catches
"the right number of words, from the wrong window."

```
V5(transcript_words, d_manifest) :=
    first_s := transcript_words[0].start
    last_s  := transcript_words[-1].end

    head_gap := first_s
    tail_gap := d_manifest - last_s

    FAIL if transcript_words is empty      # V4 already ensures a duration
    FAIL if head_gap > SPAN_EDGE_SEC       # first minutes of speech missing
    FAIL if tail_gap > SPAN_EDGE_SEC       # last minutes of speech missing
    FAIL if span_ratio < MIN_SPAN_RATIO   # (last_s - first_s) / d_manifest
    PASS otherwise
    NON_VACUOUS iff len(transcript_words) > 0 and d_manifest > 0
```

**`SPAN_EDGE_SEC` IS MEASURED, NOT GUESSED.** It read **60 for five review
rounds on no evidence.**

It is now **10**, from a census of **47 units and 94 edges** — all 42 lessons
plus 5 calls whose transcripts were already cached:

| | head gap | tail gap |
|---|---|---|
| 42 lessons | 0.00 – 4.64 s | −0.69 – 4.35 s |
| 5 calls | 0.24 – 2.16 s | −1.00 – 1.73 s |
| **largest anywhere** | **4.64 s** | **4.35 s** |

**60 was 12.9x the largest edge ever measured.** A note missing its first 55
seconds of speech would have passed the gate whose entire job is to catch that.
**10 s is 2.15x the largest observed and fails 0 of 94 real edges.**

**10 of the 47 units have a NEGATIVE tail** — the last word ends *after* the
declared duration, by up to 1.00 s. **A negative gap is not a failure.** It is
the `pjFQiLQQ` class: the manifest duration is a claim, the transcript extent is
the measurement, and the measurement can exceed the claim. The formula above
uses `tail_gap > SPAN_EDGE_SEC`, which a negative value cannot satisfy, so the
case is correct by construction — recorded because it is surprising enough
that a future reader would otherwise try to "fix" it.

Artifacts: `nhbplus-lessons-census-2026-10-15.json`, `nhbplus-call-edges-2026-10-15.json`.

**Two failures must be distinguished and they are not the same event.** A unit
with no words is a **fetch or decode failure**. A unit whose words are present
but span too little is an **assembly failure**. The first costs money to retry;
the second means the transcript is being built wrong and retrying will produce
the same wrong answer. Both are FAIL, and they are reported with different names.

### 11.1 The ten remaining gate formulas

**Rev 0's gate table was twelve one-line assertions and no formulas. V4 and V5
now have one (§11.0); the other ten are written here.** Each carries a threshold
with its provenance, a failure behaviour, and a **non-vacuity assertion**.

**THE NON-VACUITY ASSERTION IS THE PART THIS PROJECT KEEPS NEEDING.** A gate
that matches nothing returns PASS. V9 asserted `kind == "call"` when
`scope-final.json` spells it `audio`, hit **0 handles**, and returned PASS over
the one confirmed live defect in the corpus. **Every formula below asserts what
it matched, not only what it found.**

---

#### V0 — worklist integrity: 344 rows, never a glob

```
V0(scope_final, manifest_v3) :=
    rows = scope_final.rows                      # NEVER a glob over disk
    FAIL if len(rows) != 344                     # 193 calls + 42 lessons + 109 docs
    FAIL if len({r.handle for r in rows}) != 344 # handles are unique
    FAIL if {r.handle for r in rows} !=
            {u.media.handle for u in manifest_v3.units}

    # NON-VACUITY. A glob over an empty or partial directory satisfies a
    # count derived from that same directory. The worklist is only meaningful
    # if it was CONSTRUCTED, not discovered.
    NON_VACUOUS iff len(rows) == 344 == len(manifest_v3.units)
```

**Why "never a glob":** every gate below is checked against this row set. A glob
derives its population from whatever is on disk, so a fetch that silently
produced nothing yields an empty worklist, and every downstream count agrees
with it. **The population must be declared, then checked — never discovered.**

---

#### V1 — fetch caps, and the sentinel exemption

```
V1(free_bytes, declared_bytes) :=

    # the cap is real and kernel-enforced; W0-Cap proved ENOSPC at 4 GiB
    FAIL if free_bytes < FETCH_IMG_BYTES          # FETCH_IMG_BYTES = 4 GiB

    # the KILL. A declared size that is KiB-exact is a DISPLAY value, not a
    # measurement, so a threshold derived from it is meaningless.
    sentinel(b) := (b % 1024) == 0                # NOT % (1<<30)

    if sentinel(declared_bytes):
        # NO KILL. The threshold would be derived from a display value.
        record("sentinel_declared", declared_bytes)
        # the cap that actually binds is the LOOPBACK, which measures ACTUAL
        # bytes on disk - asserted here, not in section 6.4
        FAIL if actual_bytes_on_disk < FETCH_IMG_BYTES
    else:
        FAIL if declared_bytes > declared_bytes + 0.5 * quantum

    # NON-VACUITY. If no unit is ever a sentinel, the exemption is dead code
    # and this gate is not testing what it claims to.
    NON_VACUOUS iff sentinel_count > 0
```

**Measured: `sentinel(b)` is true for 335 of 335 declared sizes, carrying 75.4%
of all bytes.** So the kill branch is unreachable for this corpus and the loopback
is what actually enforces the cap. That is recorded rather than hidden.

---

#### V2 — no part reaches `CAP_BYTES`

```
V2(parts) :=
    FAIL if any(p.bytes >= CAP_BYTES for p in parts)     # CAP_BYTES = 2e9
    PASS otherwise

    # NON-VACUITY, and this gate must carry it more loudly than most:
    # SEGMENT_SEC = 1500 is UNREACHABLE for this corpus. The largest declared
    # part is 385 MiB against a 2,000 MiB cap. V2 therefore passes trivially
    # on the corpus as it stands and CANNOT FAIL unless a future fetch exceeds
    # 2 GB. It is a guard against a surprise, not a check on current work.
    NON_VACUOUS iff any(p.bytes >= 0.5 * CAP_BYTES for p in parts)
```

**This gate is currently vacuous by construction and says so.** Reporting it as a
meaningful pass would be the same error as V9 in a different costume.

---

#### V3 — STT contracts: the one sync path, and `sent` before the socket

```
V3(parts, receipts) :=
    FAIL if any(r.transport != "sync" for r in receipts)
    # there is no async path. 7.2 deleted it. A receipt naming an async job is
    # a receipt from a plan that no longer exists.

    # ORDER IS THE CONTRACT. `sent` is persisted BEFORE the socket opens,
    # because a process death between submit and record leaves the money spent
    # and nothing on disk to prove it.
    for r in receipts:
        FAIL if not r.has("sent") or not r.has("http_status")
        FAIL if r.sent_ts >= r.socket_open_ts     # inverted = contract broken

    # BOTH required. A 200 with response_complete false is a truncated file.
    FAIL if any(r.http_status != 200 for r in receipts)
    FAIL if any(not r.response_complete for r in receipts)

    NON_VACUOUS iff len(receipts) > 0
```

**`PAID_UNKNOWN`, never a clean zero.** A `queued` part was never sent: not
settled, not counted in `committed`, not `PAID_UNKNOWN`. A `sent` part with no
response **is** `PAID_UNKNOWN` and is never auto-resubmitted — the operator
decides. This branch table is in §5.2; V3 asserts it holds.

---

#### V6 — nothing media-shaped, AND a floor so an empty tree cannot pass

```
V6(vault_dir) :=
    BANNED = mp3|mp4|mp4v|mov|m4a|wav|flac|mka|aac|opus|ogg|mpga|mkv|webm
             | pdf|docx|doc|rtf|odt|pptx|ppt|xlsx|xls|csv|txt
             | png|jpg|jpeg|gif|svg|bmp|tif|tiff|webp

    FAIL if any(p.suffix.lstrip(".").lower() in BANNED
                for p in vault_dir.rglob("*"))
    FAIL if any(re.search(r"\.(mp3|mp4|mov|m4a|wav|flac|mka)$", p.name, re.I)
                for p in vault_dir.rglob("*"))
    FAIL if (vault_dir / "attachments").exists()   # C1: does not ship

    # THE FLOOR. Every check above is a CEILING. An EMPTY tree satisfies all
    # of them and returns PASS - this project's own empty-vs-empty trap.
    n = len(list(vault_dir.rglob("*.md")))
    FAIL if n < 344          # >= not ==: section 10's tree also names
                             # `00 Home.md` and `00 Topics.md`, so a flawless
                             # run emits 346 and equality would fail it.
    NON_VACUOUS iff n >= 344
```

**V6 MUST RUN ON THE VM SOURCE TREE, BEFORE THE COPY TO THE PC.** Once a media
file lands on the operator's PC, Constraint 1 has already been violated. A
post-copy gate reports the violation after it is irreversible.

---

#### V7 — reduction diff: re-render from receipts, byte-compare

```
V7(receipts, vault_dir) :=
    # Re-render each note FROM THE RECEIPT, not from the vault, then compare.
    # Rendering from the vault compares the vault with itself and always passes.
    for r in receipts:
        rendered = render(r)                      # receipt is the ONLY input
        on_disk  = (vault_dir / r.relpath).read_bytes()
        FAIL if sha256(rendered) != sha256(on_disk)
        FAIL if rendered != on_disk               # byte-compare, not "close"
    NON_VACUOUS iff len(receipts) > 0
```

**The point of a reduction diff is that the vault is a pure function of the
receipts.** If it is not, the receipts are decorative and V10's spend arithmetic
is built on the same fiction.

---

#### V8 — frontmatter value DOMAINS, not a field count

```
V8(notes, scope_final) :=
    for n in notes:
        fm = parse_frontmatter(n)                 # REAL --- delimiters. V8 once
                                                 # parsed a design doc, not the
                                                 # deliverable, and passed.
        FAIL if set(fm) != {"date","duration","speakers","type","title"}
        FAIL if not re.match(r"^\d{4}-\d{2}-\d{2}$", fm.date) and fm.date != "unknown"
        FAIL if not (fm.duration.isdigit() and int(fm.duration) >= 0)
        FAIL if not (fm.speakers.isdigit() and int(fm.speakers) >= 1)
        FAIL if fm.type not in {theory,guest,coaching,training,mastermind,other}
        FAIL if fm.title != Path(n).stem
        FAIL if fm.duration == "0" and r.word_count == 0   # FLAGGED not accepted

    FAIL if any("None" in Path(n).name for n in notes)
    FAIL if any(d.path is None for d in scope_final.documents)  # 109 documents

    NON_VACUOUS iff all(fm is not None for fm in fronts) and len(notes) >= 344
```

**`unknown`, never `null`.** In Obsidian a null frontmatter value renders as an
empty field, indistinguishable from missing — a recorded absence becomes an
omission. **`duration: 0` is allowed and is truthful**: 2 of 235 units are
sub-minute. A `>= 1` domain rejects real units. What is *not* allowed is
`duration: 0` **with** zero words — that is 50 s of audio transcribing to an
empty note, and it is flagged.

---

#### V9 — counts AND one-note-per-call, with the vacuity that hid a real defect

```
V9(scope_final, manifest_v3, vault_dir) :=
    counts = {"written_hand":37, "course_doc":36, "orphan_doc":36}
    FAIL if actual_document_counts != counts
    FAIL if sum(counts.values()) != 109

    # THE PART THAT WAS STRUCTURALLY IMPOSSIBLE BEFORE. V9 checked documents
    # only, so it COULD NOT catch a dropped call - and it did not.
    for u in manifest_v3.units where u.kind == "calls":       # 193 rows
        matches = [n for n in notes if n.unit_handle == u.media.handle]
        FAIL if len(matches) == 0      # dropped - e.g. the 10-31-2022 Mindstream
        FAIL if len(matches) > 1       # duplicated

    # THE SPELLING THAT MADE IT VACUOUS. scope-final.json uses
    # audio/written_hand/course_doc/orphan_doc. The old matcher asked for
    # kind == "call", matched 0 handles, and returned PASS.
    NON_VACUOUS iff set(real_kinds) == {"audio","written_hand","course_doc","orphan_doc"}
                   and all(kinds_actually_seen) and matched_calls == 193
```

**This is the project's signature failure and it is written into the gate.** A
gate that matches nothing returns PASS; V9 did, over the corpus's one confirmed
live defect.

---

#### V10 — the spend gate, from receipts, with the SAME settle quantity as §7.2

```
V10(receipts) :=
    # SETTLE_FROM is defined once and used twice, identically:
    #     settle = duration_seconds x INPUT_CHANNEL_COUNT
    # NOT the response's channel array - Deepgram returns channels=1 for a
    # stereo input WHILE BILLING 2x.
    # NOT the pre-downmix part - the 7.1a BIT_IDENTICAL branch re-runs
    # -map_channel and produces a MONO part, so reading the pre-downmix count
    # would settle every downmixed unit at 2x and double-count the saving.

    committed = sum(settle_from(r) * RATE for r in receipts if r.state == "settled")
    lost      = LOSS_ALLOWANCE_USD            # 10.00
    total     = committed + lost

    FAIL if total > SPEND_HARD_STOP_USD       # 213.48
    FAIL if any(r.settle_quantity is None for r in receipts)  # undefined = fail

    # PAID_UNKNOWN counts AGAINST the stop. It is money already spent whose
    # amount is unknown. Excluding it would make the gate pass by not knowing.
    total_including_unknown = total + sum(
        upper_bound(r) for r in receipts if r.state == "PAID_UNKNOWN")

    NON_VACUOUS iff len(receipts) > 0 and
                   committed > 0 and
                   every(r.settle_quantity == settle_from(r) for r in receipts)
```

---

#### V11 — egress SHA256, per file, against the manifest

```
V11(manifest_json, pc_copy) :=
    # W0-Egress proved PowerShell pipelines corrupt typography:
    # 11/11 spot-checks differed, 256 match. So NO shell pipeline touches the copy.
    for f in manifest_json.files:
        FAIL if sha256((pc_copy / f.relpath).read_bytes()) != f.sha256
        FAIL if (pc_copy / f.relpath).stat().st_size != f.bytes
    FAIL if extra_files(pc_copy) - {f.relpath for f in manifest_json.files}
    NON_VACUOUS iff len(manifest_json.files) >= 344
```

---

#### What these ten had in common

Nine of the twelve gates were **one line naming a check**. None carried a
threshold with provenance, none carried a failure behaviour, and **none carried
a non-vacuity assertion** — which is why a gate that matched nothing could
return PASS and be believed.

The three that bit hardest in practice were not the ones with the vaguest
wording. They were the ones with **no way to be wrong**:

- **V9** matched 0 handles and passed over a dropped call.
- **V8** parsed a design document instead of the deliverable and passed.
- **V6** passed on an empty tree, because every one of its checks was a ceiling.

**A gate that cannot fail is not a gate.** Each formula above now states what it
matched. Where a gate genuinely cannot fail on this corpus — **V2, which is
vacuous by construction** because the largest part is 385 MiB against a 2 GB
cap — it says so rather than reporting a green.

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
  -> V9  counts, and EVERY audio target handle has exactly one note   (this is the gate that catches the dropped call - it must not be omitted)
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

### 12.1 `_meta/AUDIT.md` ``

**Rev 0 moved every cut fact into `manifest.json` and called it clean. It is a
relocation.** Obsidian cannot open, search, or link into JSON — every fact the
operator cut from the frontmatter became reachable only by leaving Obsidian and
running `jq`. A cut that moves data into a format the reader's software cannot
open is not a clean cut.

Emit one generated `_meta/AUDIT.md` — **235 lines, one per audio unit.** 344 is the count of *targets*; only 235 of those are audio units, and V12 clauses 1–4 are all about audio units. The 109 documents are verified by §11's path and frontmatter gates, not here:
`unit · handle · declared_s · ffprobe_s · settle_s · sha256-12 · verdict`
request_id  **RESTORED.** removed this column on the strength
of "None for EVERY submission"; two later dated artifacts carry a non-null
value (`syncceiling3`: `01a13ec6-...`, `deepgram-eu-limits`: `01a13cfc-...`).
Recorded as measured, blank if absent — never invented.
with totals in the header, linked from `00 Home.md`.

**No note gains a field. No note gains a provenance section. The operator's cut is
respected exactly** — the audit simply becomes reachable from the tool the
operator reads in. ~20 lines of renderer code.

> **"TEARDOWN IS 7-PHASE" AND THE SEVEN PHASES ARE NOT ENUMERATED
> ANYWHERE IN THIS DOCUMENT.** A phase count with no phases is a scope claim no
> reader can check. And `--confirm <sha256 of copy-verification.json>` names a
> file with **no producer, no path and no schema.** >
> **The seven teardown phases, enumerated.** A phase count with no
phases is a scope claim no reader can check.

| # | phase | gate before it may start |
|---|---|---|
| 1 | **stop intake** — no new unit admitted, in-flight parts drain | V10 within stop |
| 2 | **settle** — every `sent`/`reserved` part resolves to `settled`, `lost` or an explicit `PAID_UNKNOWN` | ledger has no `queued` |
| 3 | **assemble** — `assembled.json` per unit, then the rendered note | V12 clauses 1–4 |
| 4 | **audit** — emit `_meta/AUDIT.md` (235 rows) and the SHA-256 manifest | V12 clause 4 |
| 5 | **egress** — `scp -r` vault + `_meta` to the PC, media-free | V6 (with its floor), V7, V11 |
| 6 | **verify the copy** — `copy-verification.json`: per-file SHA-256, byte count, typography spot-check | V11 |
| 7 | **destroy** — delete the VM and its disk image | **all of 1–6 green** |

**`copy-verification.json` HAS NO PRODUCER, PATH OR SCHEMA ANYWHERE IN
THIS DOCUMENT.** It is named once, by the `--confirm` argument that gates phase 7.
**Schema, fixed here so phase 6 cannot be skipped by omission:**

```
copy-verification.json = {
  "generated": ISO-8601,
  "source": "VM:/data/nhb/vault",
  "files": [ {"relpath": str, "bytes": int, "sha256": hex64} ],   # every file
  "notes_expected": 344, "notes_found": int,   # 344 = 193 calls + 42 lessons + 109 docs
  # + 00 Home.md + 00 Topics.md if the index notes ship. See V6.
  "typography_checked": int, "typography_passed": int
}
```
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
| Any 40×-realtime sync cutoff | **"ZERO MARGIN" IS ARITHMETICALLY WRONG.** 16,556 s of audio at the ceiling is 16,556/600 = **27.6× required**, so 40× yields 414 s against 600 s — **186 s of headroom, not zero.** **This line previously read "measured realtime on the real worst case is 106×, which is 3.8× margin." The worst case was never measured — see the OPEN gate above. The one MEASURED realtime factor is 119×, on `dvcEDToK`, the 47th-ranked unit.** A cutoff is still not adopted, and it is rejected on arithmetic, not on a measurement that does not exist. |
| Any success-only spend counter | Wrong — a 504 storm is paid-and-lost and sails past it |
| SQLite/journal/per-unit-JSON as independent truth | A desync waiting to happen — exactly one authority |
| Disk "bound proof" (38 GB vs 400 GB) without the loopback | Not a safety system. Only kernel ENOSPC counts, and only once proven |
| `kill`/`timeout` as the fetch safety system | Wrong — admission control + watcher + cancel + quiesce assertion is |
| Direct reuse of the skill's PDF constants | Wrong — §2.3 |
| **A `*.mp3.md` filename** | A bug — **and the live one is `.mp4.md`, on 2 committed paths** |
| **"crashed async is free via `request_id` re-GET"** | **FALSE ``.** Constraint 7: nothing is stored. Both paths are single-shot |
| **"FORECAST == HARD_STOP"** | **WITHDRAWN 2026-10-15 ``.** The claimed $151.01 overspend was a **`ceil` artifact**. Deepgram bills true per-second with no minimum and no rounding, so the corpus costs exactly the forecast, $150.56. The pessimism was solving a problem the vendor does not have. |
| **"resume never re-bills"** | **NOT IMPLEMENTED ``.** The state machine was blind to the one bit that decides it |
| **"an unnamed `flock` guards the global sum"** | **NOT IMPLEMENTABLE ``.** No file, no path, and every named lock is per-unit |

### 13.2 Claims withdrawn during planning

Kept visible, because a withdrawn claim is evidence about the corpus.

| Withdrawn | Why |
|---|---|
| "PDFs may be ~25 image-only scans" | **Measured: 0 need OCR.** Guessed from file size. |
| "4/4 PDFs have a text layer" | Hex glyph indices counted as characters. |
| "Y_TOL is stable across 0.0–5.0pt" | Asserted from a counter that could not fail. **Now digest-proven.** |
| "The 1.0pt reading is my own fallback" | `fallback_share = 0.0%`. **Hypothesis falsified by instrument.** |
| "4/4 fetches failed" | mega-get names output after the verbatim file, not the handle. |
| "146.87 GB" | It is **GiB**. Decimal is 169113263538.67 GB. |
| "59 office documents" | **51**. The other 8 are txt/png/zip. |
| "saves 132 GB" | **177.48 GB**, and 132 appears in no artifact. |
| "229 paths" | 229, but **all 109 documents have none.** |
| "603.84 h raw" | A superseded **236-call** reconciliation. Real: 605.61 h. |
| "all 193 calls dated" | **185/188.** |
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
| D1 | **settled** — **$213.48**, every line measured and the formula printed above |
| D2 | **closed** - $0.0043/min, sourced and dated |
| D3 | **closed** - dual-mono, per-file rule, $26.98 |
| D4 | **adopted** - keyterm on, +$45.52, A/B-measured |

**[UPDATED 2026-10-15 — THE NAMING REPAIR IS BUILT, NOT PENDING.]** This section
previously read "the naming repair … spans 67 of 296 names … That repair is the
next thing to build." It landed. Re-measured from `pipeline/out/clean-names.json`:

| | |
|---|---|
| paths emitted | **344** (193 calls + 42 lessons + 109 documents) |
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
nothing has been paid for yet:** the corpus-wide stereo share (3 of 235 sampled),
Azure VM-days for a 16-way run over 605.61 h, and decoded-vs-header durations
(228 of 235 are container headers). §14 marks `SEGMENT_SEC` and the WPM band
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

> **"ALL 1,372 WORDS VERBATIM" IS A LOWER BOUND PRESENTED AS COMPLETE.**
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
