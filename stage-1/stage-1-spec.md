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
| 7 | **The response is the only retrieval** `[R1]` | `evidence/probes/deepgram-eu-limits-and-chain-proof-2026-10-15.json`, under `limits_that_would_have_broken_the_run`: *"Deepgram does not store transcripts. The API response is the only opportunity to retrieve it."* **Every submission is single-shot.** The response body must stream to disk as it arrives. §7c. |

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
full budget table and `SPEND_HARD_STOP_USD = $207.31`.

| Item | Was | Now |
|---|---|---|
| 2 units with no duration | ~$1.31 estimated | **$1.23 measured** |
| loss allowance for 504s | unset | **$10.00** |
| `SPEND_HARD_STOP_USD` | unresolved | **$207.31** |

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

**D4 — keyterm prompting: ADOPTED 2026-10-15** (operator). $0.0013/min,
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
  treated MP4 as excluded alternates. **`ffmpeg -vn -c:a copy` (§7a) is the
  majority path, not an edge case.**
- **Total is 583.55 h**, not 603.84 h — that figure belongs to a superseded
  **236-call** reconciliation `[R1]`.
- **146.87 is GiB, not GB.** Every `GB` field in the JSONs is binary `[R1]`.

---

## 2. Constants — every value carries provenance

```
MEGA_URL_TMPL  = "https://mega.nz/folder/<PH>#<KEY>/file/<HANDLE>"
     PROVEN. Peak disk 2.00 GB, never 320 GB.

FETCH_CONCURRENCY      = 1        REMUX_CONCURRENCY = 2
TRANSCRIBE_CONCURRENCY = 16       EU+diarize ceiling 25; run 16.

FETCH_IMG_BYTES = 4 GiB   loopback ext4, kernel-enforced. W0-Cap proves ENOSPC.
CAP_BYTES       = 2_000_000_000
SEGMENT_SEC     = 1500    PROVISIONAL, and ONLY for the remuxed >= CAP_BYTES path.
                         The sync fallback has its own constant - see SYNC_SEG_SEC.
ASYNC_POLL_SEC  = 30      ASYNC_TIMEOUT_SEC = 86400
FETCH_STALL_SEC = 120     POST_KILL_QUIESCE_SEC = 60
WPM_MIN, WPM_MAX = 60, 260          PROVISIONAL
SPAN_EDGE_SEC   = 60
FORECAST_USD    = 150.56
```

### 2.1 Sync constants — three contradictions removed `[R1]`

```
SYNC_CUTOFF_SEC   = 8580     was 9000. SYNC_HEADROOM_SEC (420) is now SUBTRACTED,
                           not left unapplied. 9000 at 15x = 600.0 s processing =
                           EXACTLY the 504. The old pair contradicted itself.
SYNC_SEG_SEC      = 600      NEW. The fallback's segment length, previously the
                           phrase "segment smaller" with no number attached.
SYNC_HEADROOM_SEC = 420      Server-side 10-min 504; client adds TLS+upload/queue.
REALTIME_SAFETY  = 15       Pessimistic. 40x rests on two ~3.2 h samples and is
                           unsafe: the 275.9-min longest call needs 40x just to
                           survive a 10-min ceiling. Zero margin.
```

**82.4% of the corpus rides this path.** 155 of 188 calls exceed 9,000 s,
carrying **29,667 of 35,013 call-minutes**. If W0-AsyncContract fails, this
fallback is not a contingency — it is the main plan, and it must be as precise
as the primary.

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

COMMIT_COST           = billed_seconds(part) * (RATE + KEYTERM_RATE)
SETTLE_FROM           = raw metadata.duration seconds, IDENTICALLY in the 7b gate
                        and in V10

SPEND_HARD_STOP_USD   = 207.31    OPERATOR-SET, measured, not estimated
LOSS_ALLOWANCE_USD    = 10.00     covers a 5% failure rate across 3,611 parts
```

**The settled budget — every line measured, none estimated:**

| | |
|---|---|
| corpus 35,013.1 min × $0.0043 | **$150.56** |
| 2 previously-undated units, **measured today** | **$1.23** |
| 504 loss allowance | **$10.00** |
| keyterm 35,013.1 min × $0.0013 | **$45.52** |
| **`SPEND_HARD_STOP_USD`** | **$207.31** |

**Credit position: no payment card on file.** So the vendor itself enforces the
ceiling — exhausting the credit returns **HTTP 402** and processing stops. That is
a *hard*, external stop, which is strictly stronger than `SPEND_HARD_STOP_USD`,
which is our own code and can be wrong. The 402 is the safety system; the ledger
is the refinement. This removes the only path by which a bug in our spend
accounting becomes a real bill.

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
| Async policy | **all-async, gated on W0-AsyncContract** | **Premise corrected `[R1]`:** it is *not* that "async is free to re-GET" — Constraint 7 says **nothing is stored**. Both paths are single-shot; what differs is crash exposure, not recovery. |
| State authority | **receipts on disk**; journal derived | Two independent truths is a desync waiting to happen. |
| Parts | **primary abstraction** | 2 GB cap, 504 recovery and tail segmentation become one code path. |
| Ordering | **docs shakedown → 1 lesson smoke test → 16 longest → cheapest** `[R1]` | A lesson-sized STT costs ~$0.16 and de-risks the paid pipeline for almost nothing. |
| PDF | **probe-first** | **RESOLVED — closed.** 0 documents need OCR. |

---

## 4. W0 probes

| Probe | Status | Question |
|---|---|---|
| **W0-Fetch** | ✅ PROVEN | per-file route works. `systemctl is-active mega-cmd-server` is **known-false**; only a real fetch arbitrates. |
| **W0-Cap** | OPEN | does a 5 GiB write into the 4 GiB loopback raise ENOSPC? An untested cap is not a cap. |
| **W0-Remux** | OPEN | `ffmpeg -vn -c:a copy` audio-identical; log the **real** size cut (85% expected — measure). **The majority path**: 133/230 are MP4. |
| **W0-SyncCeiling** | OPEN | calibrate sync at `SYNC_SEG_SEC`. **Must not** raise the cutoff. |
| **W0-AsyncContract** | OPEN, **GO/NO-GO** | outbound-only async, and **does a GET after N minutes actually return a transcript?** Constraint 7 says retention is none. This is now the highest-value probe in the plan. |
| **W0-Pricing** | ✅ **SATISFIED 2026-10-15** | **CLOSED.** `$0.0043/min` nova-3 pre-recorded, diarization included, sourced and dated. **No per-request minimum, no rounding — true per-second billing.** |
| **W0-ChannelCount** | ✅ **SATISFIED 2026-10-15** | **CLOSED.** 3 of 3 stereo files are **dual-mono** — no per-participant separation exists. `-ac 1` is lossless and saves **$26.98**. Applied **per file** in §7.1a, not corpus-wide, so a per-participant file anywhere is detected and preserved. |
| **W0-PDF** | ✅ **SATISFIED** | closed — §8.1 |
| **W0-Egress** | OPEN | binary VM→PC copy, per-file SHA256 manifest compared. |

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
LEDGER = /data/nhb/_meta/spend.json     {"committed":USD,"settled":USD,"lost":USD}
LOCK   = /data/nhb/_meta/spend.lock     flock, held across READ-CHECK-WRITE
```

Commit and settle are each one atomic ledger mutation under that one lock:

```
commit:  committed += cost        settle:  committed -= cost;  settled += actual
declare:                            lost:    committed -= cost;  lost     += actual
```

**Ledger reconciliation is derived, never authoritative** — `bin/rescan.py`
rebuilds it from `receipt.json` parts, and **receipts win** on conflict. This
keeps single-authority (no desync) while giving the global sum a named home.

### 5.4 The resume branch — explicit, because ambiguity here costs money `[R1]`

| On disk | Meaning | Action |
|---|---|---|
| no part file | nothing happened | redo, **free** |
| `reserved`, no `request_id`, no response | committed, **never sent** | release the commit, re-reserve, submit. **Free.** |
| `sent`, no response | **in flight or 504'd** | `PAID_UNKNOWN`. **Never auto-resubmit.** Operator decides. |
| `sent` + response | completed | settle, re-assemble. **Free.** |

**The one atomic write happens before the socket opens:** `status=sent`,
committed spend, and the request placeholder land in a *single* receipt write.
A kill after that leaves `sent`, which is unambiguously billable. A kill before it
leaves `reserved`, which is unambiguously free.

**Per-part, not per-unit `[R1]`.** Rev 0 said "a unit reaches `submitted` at most
once" while the state machine is per-part — a 3-part unit submits 3 times, so the
invariant as written forbids parts 2..N. Correct form:

> Each **`(unit_id, part_index)`** reaches `sent` at most once.

A resumed unit must **never** re-submit parts already `settled` or `lost`.

### 5.5 The preflight gate — one formula, everywhere `[R1]`

```
committed + settled + lost + cost > SPEND_HARD_STOP_USD  ->  stop, do not submit
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

Rev 0 never said when a fetched raw is deleted. With fetch=1, remux=2 and
transcribe=16, **2–17 raws are naturally co-resident — 5–32 GB against a 4 GiB
cap.** Legal traffic hits ENOSPC, `mega-get` dies, the watcher sees no growth,
and units fail one after another as `FETCH_STALL` with no cause named.

- **Delete the raw at the remux receipt**, before the next fetch is admitted.
- **Gate fetch admission** on `free(fetch_mnt) >= 2 × declared + slack`.
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
    threshold = max(1.10 x declared, declared + 0.5 x display_unit)
```

**Never kill on a rounded baseline.**

---

## 7. STT

### 7.1 Remux and segment — the majority path

`ffmpeg -vn -c:a copy` every unit. **133 of 230 are MP4.**

`ffprobe` duration is the cost-gate input, **not the manifest, and not a placeholder**.
If remuxed ≥ `CAP_BYTES` → `ffmpeg -f segment -segment_time SEGMENT_SEC`.
Single-part otherwise. **Every part gets its own receipt entry.**

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
delta <= -40  -> DUAL-MONO.      -ac 1.  Lossless, saves money.
delta >= -20  -> INDEPENDENT.    KEEP STEREO.  Per-participant audio; downmixing
                                   would force acoustic diarization instead of
                                   channel-derived attribution. Pay the 2x.
otherwise    -> AMBIGUOUS.      keep stereo, flag AMBIGUOUS_CHANNELS for the
                                operator. NEVER silently decide.
```

One extra ffmpeg pass per part. `channels` goes in the receipt, and the
downmix decision is recorded beside it — so the money path and the fidelity path
are auditable together.

> **Do not invoke ffmpeg with `-v error` around `astats`.** It writes at `info`
> level, so every reading silently returns `-inf` — indistinguishable from a silent
> input. This cost one probe run and is recorded in the evidence artifact.

### 7.2 Submit

Preflight under the §5.3 lock. Commit pessimistically (`COMMIT_COST`). Persist
`sent` + the placeholder in **one atomic write before the socket opens**. Then a
Python-streamed POST — **never `curl --data-binary`, which OOMs at 1.4 GB**.

**Primary (W0 passes) — async.** Poll 30 s, GET, **save the raw response body
immediately**. Assert **both** paths: `results.utterances` non-empty **and**
`results.channels[0].alternatives[0].paragraphs` present. Proven shapes:
`metadata.duration` is a plain float; **`paragraphs` lives under `alternatives[0]`,
not `channels[0]`.**

**Fallback (W0 fails) — sync.** Parts ≤ `SYNC_CUTOFF_SEC (8580)` via
`/v1/listen`; anything longer is segmented at **`SYNC_SEG_SEC (600)`** and sent
sync. This covers **155 of 188 calls** — it is a main plan, not a contingency,
and must carry the same precision as the primary.

### 7.3 Response durability — the single-shot rule `[R1]`

> **Constraint 7: Deepgram does not store transcripts. The API response is the
> only opportunity to retrieve it.**

Therefore:

- **The response body must stream to disk as it arrives**, never buffer fully in
  memory, never exist only in a pipe.
- **A 504 or a truncated stream is paid-and-unrecoverable.** Not pending.
  `PAID_UNKNOWN` is **loss acceptance**, not recovery. Rev 0's "crashed async is
  free via `request_id` re-GET" was **false** and rested on this contradiction.
- Quarantine-then-operator is a correct **anti-double-bill** control. It is
  **not** a spend control — the money is gone before the quarantine exists.

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
5. **Remainder cheapest-first** by `ceil(ffprobe_s/60) × RATE` — maximises completed
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

### 10.1 Frontmatter value domains — asserted, not merely counted `[R1]`

Rev 0's V8 asserted a **field count**, so these all shipped: `duration: 0` on 3
units, `speakers: null`, and a `type: mastermind` that is **not in its own
5-value vocabulary**.

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
| dash splitter mangles intra-word hyphens | **67/296** names contain ` - `, incl. the spec's own example `Ron-Lynch` → `Ron - Lynch`, and a double-hyphen `A - - ` artifact | normalise dash **styles** only; never split `[A-Za-z]-[A-Za-z]` |
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
| V6 | **zero media extensions under `vault/`, AND no stem matches `\.(mp3\|mp4\|mov\|m4a\|wav\|flac)$`** |
| V7 | reduction diff: re-render from receipts, byte-compare |
| V8 | **frontmatter value DOMAINS (§10.1), not a field count; every document has a `path`; no filename contains `None`** |
| V9 | counts 37/36/36; **and every kind-`call` handle in `scope-final.json` has exactly one emitted note** — V9 previously checked documents only, so it **structurally could not catch the dropped call** |
| V10 | `settled + lost ≤ SPEND_HARD_STOP_USD`, derived from receipts, **using the same settle quantity as the §7b gate** |
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
compared. PowerShell pipelines **forbidden by name**.

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
| D1 | **settled** - $207.31, every line measured |
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