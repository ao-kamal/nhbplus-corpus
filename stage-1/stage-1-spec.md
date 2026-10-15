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
| 5 | **Operator picks the files.** | `scope-final.json`, 339 targets, locked. |
| 6 | **A sentinel is not a measurement** `[R1]` | **73 of 230 units carry placeholder sizes** — 37 at exactly 1 GiB, 36 at exactly 2 GiB = **109.00 GiB of 146.39 GiB = 74.5%**. These are MEGA display values recorded as binary. **No kill rule, threshold, or cost gate may consume them.** §6.4. |
| 7 | **The response is the only retrieval** `[R1]` | `evidence/probes/deepgram-eu-limits-and-chain-proof-2026-10-15.json`, under `limits_that_would_have_broken_the_run`: *"Deepgram does not store transcripts. The API response is the only opportunity to retrieve it."* **Every submission is single-shot.** The response body must stream to disk as it arrives. §7.3. |

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
billing the corpus costs `35,013.1 min × $0.0043 = $150.56` — the forecast.

**Residual, all three need an operator value:**

**SETTLED 2026-10-15.** Both items are now measured, not estimated. See 2.2 for the
full budget table and `SPEND_HARD_STOP_USD = $207.68`.

| Item | Was | Now |
|---|---|---|
| 2 units with no duration | ~$1.31 estimated | **$1.23 measured** |
| loss allowance for 504s | unset | **$10.00** |
| `SPEND_HARD_STOP_USD` | unresolved | **$207.68** |

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
for budget only.** The run needs the budget — $207.68 exceeds the $200 credit. It
does not need the concurrency: one project at concurrency 50 covers the corpus.

**D4 - keyterm prompting: ADOPTED 2026-10-15** (operator). $0.0013/min,
**+$45.52**. Justified by a measured A/B, not an opinion — see 2.2.1. The deciding
argument is search: without it the corpus spells its own programme name
"Nothing Elbach", and `Ctrl+F "Nothing Held Back"` returns nothing.

---

## 1. Scope — locked

```
339 targets · 146.8731 GiB (= 157.70 decimal GB) · 603.84 h is SUPERSEDED [R1]
```

| Population | Count | Handling |
|---|---|---|
| Audio calls | **188** | STT. 557.39 h. |
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
- **Total is 583.55 h**, not 603.84 h — that figure belongs to a superseded
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
FETCH_CONCURRENCY_CEILING = 39   RAISED from 1, 2026-10-15. W0-Cap PASSED: the
                                4 GiB loopback is a real, exact, timely stop.
                                Expected saving 40-65 min. The cap costs 1.7%
                                throughput (169 vs 172 MB/s) against a network
                                fetch ceiling of 41-53 MB/s, so it is free.
REMUX_CONCURRENCY      = 2
TRANSCRIBE_CONCURRENCY = 16       BINDING CEILING IS 25, not 50. Authoritative
                                source, fetched 2026-10-15:
                                developers.deepgram.com/reference/api-rate-limits.md
                                  Nova-3            | EU | Pre-Recorded  up to 50
                                  Speaker Diarization | EU | Pre-Recorded  up to 25
                                  "If multiple services are used in one API call...
                                   the lower of the rate limits is applied."
                                diarize=true is NON-OPTIONAL (10.1 needs diarisation
                                clusters; Rule 3 forbids removing it), so the LOWER
                                limit binds: min(50, 25) = 25. 16 leaves 60% headroom.
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
                        IDENTICALLY in the 7.2 gate and in V10. [T5 #3]
                        NOT the response's channel array: Deepgram returns
                        channels=1 for a stereo input while BILLING 2x.

SPEND_HARD_STOP_USD   = 207.68    DERIVED, not asserted. [B6] Three values
                                were in circulation and all three were wrong:
                                $207.31 (the budget artifact), $207.35 (this
                                spec, twice), and this one — which is derived.
                                  (35,013.1 + 286.9) x $0.0056 = $196.68 run
                                  + $10.00 loss reserve            = $207.68
                                The $1.23/$1.27 "undated units" line was
                                STT-only; at RATE + KEYTERM the two units are
                                286.9 min x $0.0056 = **$1.65**. [B1]
LOSS_ALLOWANCE_USD    = 10.00     covers a 5% failure rate across 3,611 parts
```

**The settled budget — every line measured, none estimated:**

| | |
|---|---|
| corpus 35,013.1 min × $0.0043 | **$150.56** |
| 2 previously-undated units, **measured today** | **$1.27** |
| 504 loss allowance | **$10.00** |
| keyterm 35,013.1 min × $0.0013 | **$45.52** |
| **`SPEND_HARD_STOP_USD`** | **$207.68** |

**Credit position: no payment card on file.** So the vendor itself enforces the
ceiling — exhausting the credit returns **HTTP 402** and processing stops. That is
a hard, vendor-enforced bound that no bug in our accounting can get past.

**But $200 < $207.68, so the vendor stop is strictly LOWER than our own gate and
fires FIRST.** Round 2 caught that "strictly stronger" was backwards. The correct
statement: the 402 is a **backstop at $200 per account**, not a ceiling at
$207.68. Two accounts are therefore required, and the split is explicit:

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
| Fetch concurrency | **1** | Serialising the only unkillable operation costs ~1 h *measured*. Parallelism multiplies the hazard. |
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
| **W0-Cap** | ✅ **SATISFIED 2026-10-15** | **CLOSED.** The 4 GiB loopback is real, exact (3,936 MiB into 3,952), costs 1.7% throughput against a 41–53 MB/s network ceiling, **fails fast under real traffic** (mega-get exit 232 "Insufficient disk space" in **0 s**, no host spill), and recovers without a remount. **Fetches `FETCH_CONCURRENCY 1 → 6`.** |
| **W0-Remux** | ✅ **SATISFIED 2026-10-15** | **CLOSED.** Bit-exact for MP3 (SHA-256 over 712/995 MB PCM), near-exact for AAC (~10 KB in 1.1 GB). Real size cut is **71.2% aggregate — MP4 ~80%, MP3 NEGATIVE**. Output container must be **`.mka`**: `.m4a` fails for 97 of 230 units. |
| **W0-SyncCeiling** | ✅ **SATISFIED 2026-10-15** | **CLOSED, MEASURED.** The longest call in the corpus — 204.3 min, 280.7 MB remuxed — completed in **105.1 s against the 600 s ceiling. Margin 5.7×, measured, not calculated.** $1.54. Take 1 (the raw 1,539 MB MP4) **timed out**; see §7.1. |
| **W0-AsyncContract** | ❌ **FAILED 2026-10-15** | **`ASYNC_ALLOWED = False`.** No async job at 2 min *or* 68 min — inline results, `request_id` None. §7.2 collapses to one sync path. The "unreachable 504" claim that came with it was **calculated at 273.7× and later measured at 5.7×** on the worst case — see W0-SyncCeiling. |
| **W0-Pricing** | ✅ **SATISFIED 2026-10-15** | **CLOSED.** `$0.0043/min` nova-3 pre-recorded, diarization included, sourced and dated. **No per-request minimum, no rounding — true per-second billing.** |
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
     "totals":      {"committed":USD,"settled":USD,"lost":USD}}
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
| `sent`, `http_status` **≠ 200** | vendor refused or timed out | `PAID_UNKNOWN`. **Settled as `lost`, never as a transcript.** |
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
(server-side transfer survives client death), then 5 s after SIGKILL.

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

**Concurrency.** `FETCH_CONCURRENCY = 6`, gated on §6.3 admission:

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

    small  (<100 MiB)            max 39 in flight
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

Detection is exact and free: **`bytes % (1 << 30) == 0` is a sentinel** — 0 false
positives among the 157 genuine values.

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

**Size guard on the remuxed output `[T5 #5]`.** The proven submission is
**280.7 MB**. The largest remuxed unit in scope is estimated at **~400 MB**
(a 2 GiB sentinel source less the measured ~80% MP4 cut) and has **not** been
submitted. Upload runs at 150.8 MB/s so 400 MB is ~2.7 s of transfer, and the
proven case held 5.7× time headroom — but this is **bounded, not closed**, and is
recorded as such.

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

After remux, compute the difference signal for each part:

```
rms_L  = ffmpeg -i part  -af "pan=mono|c0=c0,astats"        -f null -
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
delta <= -40   -> EFFECTIVELY_DUAL_MONO.  -ac 1 RE-ENCODES (a copy codec cannot
                                         change channel count).  §7.1's
                                         bit-exactness claim is WITHDRAWN for
                                         these parts. Encoder and bitrate MUST be
                                         named: -c:a libopus -b:a 32k, mono 16k.
delta >= -20   -> INDEPENDENT.     KEEP STEREO.  Per-participant audio; downmixing
                                   would force acoustic diarization instead of
                                   channel-derived attribution. Pay the 2x.
otherwise      -> AMBIGUOUS.       keep stereo, flag AMBIGUOUS_CHANNELS for the
                                   operator. NEVER silently decide.
```

**Round 2 caught that §7.1 and §7.1a contradicted each other.** §7.1 mandates
`-c:a copy` and claims bit-exactness; §7.1a mandated `-ac 1`, which cannot be
done with a copy codec. Every time the downmix rule fired, the fidelity claim was
void and the output became a lossy re-encode at an unnamed encoder. The split
above makes the two cases explicit: two of three measured stereo files were
BIT_IDENTICAL and are downmixed **losslessly with the copy codec intact**; only
the -46 dB case re-encodes, and it says so.

One extra ffmpeg pass per part. `channels` goes in the receipt, and the
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
unit        dvcEDToK, 204.3 min, 280.7 MB remuxed .mka
                        *** NOT THE WORST CASE. [B1] 46 calls are LONGER. ***
                        The longest is wiUyTRZb at 275.9 min / 16,556 s.
upload      1.9 s at 150.8 MB/s
response    HTTP 200 in 103.2 s
total       105.1 s   against a 600 s ceiling
MARGIN      5.7x
```

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
> **4.2× margin**, not 5.7×. W0-SyncCeiling is **REOPENED** for `wiUyTRZb`. It
> was skipped because `dvcEDToK`'s manifest `dur_s` is `None`, so it never
> appeared in the duration-sorted list used to pick the worst case.
>
> (superseded note retained: the earlier reading)
> extrapolated a 126× realtime factor measured on a 68-minute, 124.5 MB file to a
> unit 4× longer and 12× larger. **A margin calculated for the worst case is not a
> margin.** $1.54 bought the real number; nothing else could.

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
| `sparse` | **2** | *AC eBook*, *AC_Book* — 340 pp, ~3.4 w/pg, 0.18 img/pg. **1,372 words** |
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
fired 0 of 3 — but the gate must be correct on it. §2.2 carries an explicit
keep-stereo line.

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
vault/calls/<year>/<MM Month>/<CLEAN>.md
vault/written-hands/<year>/<MM Month>/<CLEAN> (written hand).md
vault/library/…                       the 36 orphan documents
vault/00 Home.md
vault/00 Topics.md                   NEW - §10.3
_meta/manifest.json
_meta/AUDIT.md                       NEW - §12.1
```

Exactly **5 frontmatter fields**: `title, date, type, duration, speakers`.

**Every documented output location needs a `path`.** Rev 0 assigned locations for
the 109 documents that **no artifact actually populated** — `clean-names.json`
carries `handle/verbatim/kind/clean` and no `path` for any of them `[R1]`.
`design-names.py` must emit one, and V8 must assert its existence.

> **[B19] V8 CANNOT PASS TODAY.** Verified by grepping every write to a `path`
> key across `pipeline/scripts/`: `design-names.py` writes `path` for calls
> (line 114) and lessons (line 137) and **never for a document**. All 109 document
> records carry exactly `['clean','handle','kind','verbatim']`. This is a build
> task, not a note: until the line is written, V8 fails on its first run and the
> §9 docs shakedown cannot complete.

### 10.1 Frontmatter value domains — asserted, not merely counted `[R1]`

Rev 0's V8 asserted a **field count**, so these all shipped: `duration: 0` on 3
units, `speakers: null`, and a `type: mastermind` that is **not in its own
vocabulary** - it lists six, not five.

```
date      ^\d{4}-\d{2}-\d{2}$   or  unknown
duration  integer >= 1          or  unknown     (minutes, never "3h 14m" -
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
| dash splitter mangles intra-word hyphens | **50 of 229** cleaned paths contain ` - `, of which **7** are true intra-word mangles (`Ron-Lynch`, `Biz-Op Blueprint`, `Clean Biz-Ops`, `Pre-Openings`, `CMO-CRO Roles`, `Call of Duty Biz-Ops`, `7-Figure Fill-In-The-Blank`). **[B20] The spec previously said 67 of 296 - the denominator 296 excludes the 42 lessons, one of which is damaged.** | normalise dash **styles** only; never split `[A-Za-z]-[A-Za-z]` |
| `Call` stripped mid-phrase | `Call of Duty` → `of Duty Biz - Ops`; `Call Booking Page` → `05 5 Booking Page` | strip `Call` only as a whole token outside a compound |
| `None` leaked into 3 filenames | `None Selling To Women 3.0.md` etc. | a missing date **omits the prefix**, it does not fill it. V8 asserts no filename contains `None` |
| extension-in-stem | **2 `.mp4.md`** paths | strip a trailing media extension before appending `.md`. V6 checks **stems**, not just extensions |
| 5 `Resources Links` collide | `collisions.documents = 1` while 5 files share the stem | apply the course prefix; the script computes it and discards it |
| 23 brand tokens, 4 underscores survive | against §10's own rules | fix the strippers |
| **dropped call** | `10-31-2022 NHB+ Mindstream Call` absent; **187 paths, not 188** | drop `Mindstream` from the alternation; **and add a guard: if `tidy()` returns empty, fall back to `topic`, never `continue`** |
| lesson ordinals renumbered | source `7. AC - Unannounced bonus` → `02 …` | preserve source numbering |
| dates lost | the corpus's **only** ISO-dated name (`2024-09-27`) is the one that lost its date | accept `YYYY-MM-DD` as well as `M-D-YYYY` |
| **3 calls undated** | `undated-other-9/-5/-5` | §10 needs a day; list them, do not leave them to run time |

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
*already in every filename*, already clusters into ~50 groups of 1–13, and
required **zero inference** to recover. The cleaning pass read it, stripped the
type boilerplate off it, mangled 24% of its hyphens, and then the vault design
discarded it.

`type: theory` returns ~120 notes across 36 month folders in 5 years. That is not
a view. And the fallback — Ctrl+F across 4–5M words of machine diarisation where
`Speaker 7` means nothing — is the absence of a retrieval strategy.

**Artifact:** one generated note at vault root, linked from `00 Home.md`. One
section per topic stem, sorted by member count descending, each row carrying ISO
date, type, duration and a wikilink. ~250–400 lines.

**Built by deterministic stem extraction only** — take `topic`, lowercase, strip
the ISO prefix, strip a leading `nhb - `/`theory - `, strip a trailing
`- with <name>` and `part N`/`pt. N`/`#N`/`2.0`. **Do not merge stems differing
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
| V0 | worklist integrity: 339 rows, never a glob |
| V1 | fetch caps: ENOSPC proven; **no kill fired on a sentinel `declared`** |
| V2 | remux/segment: no part ≥ `CAP_BYTES` |
| V3 | STT contracts: both response paths; **`sent` persisted before the socket opened** |
| V4 | three-way duration reconcile |
| V5 | span coverage |
| V6 | **zero media extensions under `vault/`** — the list must include **`.mka`**, the container §7.1 mandates, plus `aac\|opus\|ogg\|mpga\|mkv\|webm\|mov\|m4a` — **AND** no stem matches `\.(mp3\|mp4\|mov\|m4a\|wav\|flac\|mka)$` |
| V7 | reduction diff: re-render from receipts, byte-compare |
| V8 | **frontmatter value DOMAINS (§10.1), not a field count; every document has a `path`; no filename contains `None`** |
| V9 | counts 37/36/36; **and every manifest unit with `kind == "calls"` has exactly one emitted note** (188 rows in `manifest-v3.json`). **`scope-final.json` has no `call`/`calls` kind — its kinds are `audio`/`written_hand`/`course_doc`/`orphan_doc` — so the previous `kind == "call"` matcher hit 0 handles and V9 passed VACUOUSLY on the one confirmed live defect, the dropped `10-31-2022 NHB+ Mindstream Call`. [B7]** V9 previously checked documents only, so it **structurally could not catch the dropped call** |
| V10 | `settled + lost ≤ SPEND_HARD_STOP_USD`, derived from receipts, **using the same settle quantity as the §7.2 gate** |
| V11 | egress SHA256 per-file match |
| **V12** | **Identity Binding — NEW, and the most important gate here** |
| **V13** | **`00 Topics.md` — NEW** |

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
 5. no request_id appears under two different unit ids
 6. effective_spend reconciles to COMMIT_COST, and ffprobe(U) is within 2% of
    the metadata.duration in the response named by U's OWN request_id
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

Exit codes 0 / 10 / 20 / 30 / 40. Any gate failure **writes its receipt and
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
  -> V8  frontmatter domains + every document has a path
  -> V9  counts, and EVERY kind-call handle has exactly one note
        (this is the gate that catches the dropped call - it must not be omitted)
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

Emit one generated `_meta/AUDIT.md` — 339 lines, one per unit:
`unit · handle · request_id · declared_s · ffprobe_s · settle_s · sha256-12 · verdict`,
with totals in the header, linked from `00 Home.md`.

**No note gains a field. No note gains a provenance section. The operator's cut is
respected exactly** — the audit simply becomes reachable from the tool the
operator reads in. ~20 lines of renderer code.

Teardown is 7-phase. Final destroy requires `--confirm <sha256 of
copy-verification.json>` — deliberately awkward, so the operator has looked.

---

## 13. Where the plans are wrong

### 13.1 The four plans, and round 1

| Item | Verdict |
|---|---|
| "146.87 GB ≈ 30–50 h serial fetch" | **~30× wrong.** Measured 41–53 MB/s → **0.99–1.28 h** |
| Alphabetical-smallest-first | Dropped — unjustified and pessimal |
| Any 40×-realtime sync cutoff | Unsafe — the 275.9-min longest call needs 40× to survive, zero margin |
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

**The largest remaining risk is not a decision, it is work:** the naming repair in
10.2 spans 67 of 296 names plus a dropped call, three undated calls and five
collisions. It must land before the first STT dollar, because 9 puts documents
first as the shakedown. That repair is the next thing to build.

**Naming repair** — §10.2 lists 10 defect classes across 67 names, plus the
dropped call and 3 undated calls. Not three defects. This is the largest single
piece of work left and it must land **before** the first STT dollar, because §9
puts documents first as the shakedown.

**Content decisions still open:** whether `00 Topics.md` and the 30-minute
transcript headings are wanted (§10.3) — both $0.00, ~2.5 h combined, and R4's
objection is that without them the vault answers only *"what did I already know
the date of"*.

**Un-audited:** `7-Figure VSL Script Template` was classified degraded and missed
the fallback audit on a name mismatch; it measured 814 words/page (80× the sparse
threshold), so it is readable by the same metric but was never separately audited.

**Out of scope, flagged once:** the 335 GB import still sitting in the operator's
personal MEGA account. Only the operator can delete it.
