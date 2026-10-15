# REFINEMENT ROUND 2 — REVIEW (verbatim findings, triaged)

Round 2, sequential, reviewing rev 1c (post-six-probe). Model: `opencode/space-bunny-free`
(per-request billing — a provider mistake on my part; superseded rounds use
`opencode-go/step-5-preview-free`).

**Verdict: NOT executable as written.** DISAGREE, with named sections.

The async collapse itself is clean and well-evidenced. The defect is that the
revision was applied to §7 and to the evidence, and **not** applied to §2, §5.4,
§6.3, or the cross-references.

---

## THE FIVE THAT MATTER MOST

### 1. §5.4 has no HTTP-status dimension — a 504 would be booked as a success

The resume table's row 4 reads `sent` + response → "completed | settle,
re-assemble. **Free.**" There is no status check. **A 504 body, a 429 body, a
402 body and a 400 body are all "a response".** §7.3 names the 504 as a live
outcome: *"A 504 or a truncated stream is paid-and-unrecoverable."*

As written, a 504 is **settled as a completed transcription and assembled as a
transcript.** Combined with a possible 429 from the concurrency question, each
failure silently destroys a unit while the ledger books it as success.

**Fix:** add `status` to the receipt, recorded in the same atomic write as
`sent`. Branch row 4 on **HTTP 200 only**; every other status → `PAID_UNKNOWN`.

### 2. No `response_complete` state — a partial file is indistinguishable from a live request

§7.2 mandates streaming the body to disk, which means **a partial file is the
normal mid-run state.** So after any crash, `sent` + partial file is
indistinguishable from `sent` + request still in flight — exactly the ambiguity
§5 was written to eliminate, one level down.

**Fix:** a third atomic write, `status=response_complete`, after the body's last
byte is fsynced.

### 3. §7.1 `-c:a copy` and §7.1a `-ac 1` are mutually exclusive — my own rules contradict each other

§7.1 mandates `-c:a copy` and claims bit-exactness. §7.1a mandates `-ac 1` on the
DUAL-MONO branch. **Changing channel count cannot be done with `-c:a copy`** — it
requires a re-encode. So the moment §7.1a fires, §7.1's fidelity claim is void
and the output becomes a lossy re-encode at an encoder and bitrate the plan never
names.

**Fix:** split DUAL-MONO into `BIT_IDENTICAL → -map_channel -c:a copy, lossless`
and `EFFECTIVELY_DUAL_MONO → re-encode`, withdrawing bit-exactness for the latter
and naming encoder + bitrate.

### 4. §7.1a has no MONO branch, and 82.1% of minutes are mono

The rule is *"compute the difference signal for each part"* using
`pan=mono|c0=c1`. **There is no `c1` on a mono input — ffmpeg errors.** The
decision table has three branches, none of them `MONO`.

**Fix:** `channels == 1 → MONO, no test, commit once`.

### 5. §6.3's `2 × declared` admission is unsatisfiable for a unit the plan itself names

Usable loopback measured at **3,936 MiB.** Max admissible `declared` =
(3936 − 64)/2 = **1,936 MiB.** The eu-limits artifact names a unit at **3.00 GB**
(`10-03-2024 NHB+ Call - October Reading Offers Call - 1476x10`) — the unit that
forced the entire remux architecture. It needs 5.65 GiB. **No sequence of fetches
can raise `free` to 5.65 GiB.** And `bytes % (1<<30) ≠ 0` for it, so §6.4's
sentinel detector does not rescue it. **That unit is permanently unfetchable.**

**Fix:** `free >= Σ(in_flight declared) + declared_next + slack`. The `2 ×` is
an off-by-one for a loopback whose whole purpose is to hold one copy at a time.

---

## DANGLING REFERENCES (§2 and §2.1 never got the revision)

| Line | Text | Verdict | Fix |
|---|---|---|---|
| 166 | `ASYNC_POLL_SEC = 30  ASYNC_TIMEOUT_SEC = 86400` | LIVE | delete both — zero consumers |
| 165 | "The sync fallback has its own constant - see SYNC_SEG_SEC" | LIVE | delete |
| 176–185 | **entire §2.1**, incl. `SYNC_CUTOFF_SEC=8580`, `SYNC_SEG_SEC=600`, `SYNC_HEADROOM_SEC=420`, `REALTIME_SAFETY=15` | LIVE | delete §2.1 |
| 187–190 | *"82.4% of the corpus rides this path. 155 of 188 calls exceed 9,000 s… this fallback is not a contingency — it is the main plan"* | **LIVE, directly contradicts §7.2 (`0` exceed it)** | delete |
| 305 | `W0-SyncCeiling \| OPEN \| calibrate sync at SYNC_SEG_SEC` | LIVE | re-scope to the 275.9-min submission |
| 31 | "must stream to disk as it arrives. **§7c**" | LIVE — §7c does not exist | `§7.3` |
| 133 | "`-c:a copy` (**§7a**) is the majority path" | LIVE — §7a does not exist | `§7.1` |
| 306, 865 | "**§7b** collapses…" / "the same settle quantity as the **§7b** gate" | LIVE — §7b does not exist | `§7.2` both. **V10's money assertion points at a renamed section** |
| 363 | `reserved, no request_id, no response` | LIVE, vestigial | drop `request_id` — §7.2 proved it is always `None` |
| 478 | `max(1.10 × declared, declared + 0.5 × display_unit)` | LIVE, `display_unit` **undefined** | define it — it is in the only formula that issues a SIGKILL |
| 206 vs 530 | `billed_seconds` | defined **twice, differently** | pick one |
| 634 | "the money is gone before the quarantine exists" | LIVE | §5 names no `quarantined` state |
| 211 | "covers 5% across **3,611 parts**" | LIVE, derivation dead | `~230 requests`; magnitude survives |

Historical rows in §13 (`fallback_share`, "no free recovery on any path",
withdrawn claims) are **correct — leave alone.**

---

## OTHER CONTRADICTIONS

- **C2 — "$402 is strictly stronger than `SPEND_HARD_STOP_USD`" is FALSE.** $200 <
  $207.35, so the vendor stop fires **first**. The load-bearing half survives (the
  402 does bound the real bill); "strictly stronger" does not. **And nothing
  specifies the two-account split** — no key-switch rule, no per-account
  attribution in §5.3's single global ledger.
- **C5 — §6.3 bullet 1 vs `FETCH_CONCURRENCY = 6`.** "Delete the raw before the
  next fetch is admitted" serialises the lane to effective concurrency 1, in the
  same bullet block that sets it. The "5–58 raws co-resident" sentence describes
  a system the deletion rule forbids.
- **C6 — sentinel branch defeats its own headroom.** The 512 MiB reserve applies
  to exactly the 73 units that are 1–2 GiB; `dvcEDToK` at ~1.50 GiB real needs
  4.5 GiB against 3.84 usable. **ENOSPC refusals are guaranteed by construction
  at fetch=6.** `LOOPBACK_ENOSPC` has no recovery — no re-queue, ordering, backoff.
- **C7 — `TRANSCRIBE_CONCURRENCY = 50` cites the wrong table.** The eu-limits
  artifact records `speaker_diarization_pre_recorded_eu: up to 25` as the binding
  ceiling, reason: *"diarization is not optional."* §10.1 requires `speakers` =
  diarisation clusters, so `diarize=true` is non-optional. **The concurrency probe
  corrected the MODEL row and silently substituted it for the DIARIZATION row.**
  That is the same stale-prior error a second time.
- **C9 — §9 item 5 still says `ceil(ffprobe_s/60) × RATE`** after §2.2 deleted
  `ceil`; it also omits `KEYTERM_RATE` and uses `ffprobe_s`, the container header
  §7.1 forbids. The very next paragraph already says order on `COMMIT_COST`.
- **C10 — §2.2's budget has no stereo line.** $150.56 is the with-`-ac 1` figure;
  §7.1a preserves stereo on INDEPENDENT/AMBIGUOUS, and the 17.9% share is a
  10-file extrapolation over 230 units.
- **C11** — §10.1 "5-value vocabulary" lists six. **C12** — §7.1a says "one extra
  ffmpeg pass"; the code block issues three. **C13** — undefined money symbols:
  `actual` (unobtainable for a `lost` part), `effective_spend`, `display_unit`.
  **C14** — the settled budget table ignores ~$1.27 already spent, against its own
  standing condition "forecast and actual spend recorded separately."

---

## GATE CHAIN

Ordering is coherent; V6 before `scp` is correct. But:

1. **V13 is mandatory pre-copy on an artefact §15 leaves an open decision**
   (`00 Topics.md`). A mandatory gate on an undecided deliverable.
2. **V8 asserts a field nothing assigns** — `design-names.py:180-182` emits
   `{handle, verbatim, kind, clean}`, **no `path`.** The gate is correctly
   fail-closed, but §9 runs the docs shakedown "through egress" while §15 only
   requires the repair "before the first STT dollar" — a later point. **On the
   plan's own ordering the shakedown is guaranteed to fail V8 with no exemption.**
3. **V9 and V10 are absent from the "mandatory" sequence.** V9 is the gate that
   catches the dropped call; V10 must run before the teardown `--confirm`.
4. **V6's extension list omits `.mka`** — the container §7.1 mandates — plus
   `aac|opus|ogg|mkv|webm|mpga`. A hole in the one extension this plan creates.
5. **§12's sequence has drifted from the evidence that produced it.** The egress
   artifact records `V6 → V7 → V12 → scp → V11`; the spec now reads differently.
6. Nothing emits the PC-side SHA256 manifest before `scp`, yet §12 asserts it and
   the teardown gate depends on a `copy-verification.json` no step produces.
7. **The 42 bonus videos have no handle-level coverage** — V9 is scoped to
   `kind-call`; V12 is the only gate reaching them.

---

## STATE MACHINE (§5) — 4 holes

`segmented` is correctly absent. The real problem: **§5.1 creates `state.json` at
unit level, §5.2 defines only per-part states.** No unit-level aggregation, no
"when is a unit complete".

- **D3 — `lost` has no transition rule anywhere.** It is a declared terminal
  state, a ledger mutation, a §5.5 preflight input and a V10 input — and **no
  section states when a part becomes `lost`.** Worse, `lost += actual` needs an
  `actual` for a part whose response never arrived; `metadata.duration` does not
  exist for it. The money gate's correctness rests on an out-of-band operator
  action with no source of truth.
- **D4** — `queued` is in the diagram with no definition and no resume branch.
- **D5** — row 4's "**Free.**" means "no new spend" but sits where rows 1–2 use
  the same word for "nothing was spent". Row 3 is the one that costs.

---

## UNTESTED CLAIMS, RANKED

1. **`TRANSCRIBE_CONCURRENCY = 50` against a `diarize=true` ceiling of 25, with
   no status handling downstream.** Evidence at a level never tested, for a
   request shape never tested. Damage: every 429 assembled as a transcript and
   booked as success.
2. **The 275.9-min worst-case submission is tracked NOWHERE.** The async artifact
   names it, says "RECOMMENDED, not yet run"; §7.2 quotes it. It appears in no
   probe table, no provisional list, no open list, no gate. **The 273.7× margin
   is the load-bearing number in the entire sync argument and it is measured at
   concurrency 1 while the plan runs at 50.**
3. **Stereo `metadata.duration` semantics.** Every stereo measurement in the
   evidence is a mono file. If Deepgram reports doubled duration for stereo, then
   `COMMIT_COST` (1×) ≠ `SETTLE_FROM` (2×); **V12 clause 6's 2% check fails on
   every part §7.1a preserves**; and §5.3 absorbs a 2× gap with no reconciliation.
4. **§6.3's admission arithmetic against the largest real unit** (C4). W0-Cap
   proved the cap *exists*, not that the admission rule is satisfiable.
5. **Full-duplex streaming upload.** §7.2 requires request bytes streamed from
   disk *and* response bytes to disk simultaneously, single-shot, no recovery.
   Untested above 140 MB. A socket deadlock is paid-and-lost.

*Runner-up: the $26.98 stereo saving is a 10-file extrapolation applied to 230
units by a rule that admits it may be wrong per file, with no budget line for the
keep-stereo branch.*