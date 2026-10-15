# STAGE 1 — MASTER SPECIFICATION

**NHB+ corpus transcription. An agent executes this with no other document open.**

Status: Stage 1 complete (four competing plans → synthesis → integration).
G0 anchor: `stage-0/stage-0-intent.md`, passed 2026-10-15.
Next gate: **G1** — ≥4 refinement rounds, last round's changes execution-structural
not fundamental, plan self-contained.

---

## 0. Hard constraints

These outrank every mechanism in this document. Nothing below may trade one away.

| # | Constraint | Enforcement |
|---|---|---|
| 1 | **Nothing media-shaped touches the operator's PC.** Audio in, audio out, images decoded, video — none of it lands there. | The finished vault (markdown) is the deliverable and *does* land there. Gate V6. |
| 2 | **Pay nothing.** No paid tier, no metered API, no vendor free-credit tier. | Sole waiver: Deepgram STT. Sole paid software: none. `python3-pypdf` came from the Ubuntu archive, not a vendor. |
| 3 | **Remove nothing.** No capability is descoped. Where a route is blocked, the route changes. | The 2 sparse PDFs are extracted, not dropped. The 105 MP4 siblings are recorded as alternates, never fetched — that is a route change, not a removal. |
| 4 | **Evidence, not assertion.** A claim is believed when a dated artifact proves it. | W0 probes below. Three claims were withdrawn during planning; the withdrawals are recorded rather than erased. |
| 5 | **Operator picks the files.** Selection is theirs. | `pipeline/out/scope-final.json`, 339 targets, locked. |

**Constraint 2 note.** The Deepgram waiver is settled and closed. The $3.80 already
spent on probes is spent, not a standing item. Re-opening either is out of scope.

---

## 1. Scope — locked

```
339 targets · 146.87 GB · $150.56 forecast · 603.84 h raw → 583.55 h after merge
```

| Population | Count | Bytes | Handling |
|---|---|---|---|
| Audio calls | 188 | — | STT. The corpus body. |
| Bonus lesson videos | 42 | — | STT. All 11 courses + all 36 orphans. |
| Documents | 109 | 0.159 GB PDF + office | Extract, no STT. |
| MP4 siblings | 105 | — | **Recorded as alternates, never fetched.** Saves 132 GB. |

Documents partition **37 written_hand + 36 course_doc + 36 orphan = 109**.
*This corrects a briefing error: an earlier count said "37 + 36".* Of the 109,
**50 are PDFs** (now measured, §7) and 59 are docx/pptx/xlsx.

**42 videos vs 36 course docs is not an arithmetic error.** Operator decision
2026-10-15: videos and documents are independent populations; some courses have
more videos than companion documents. V9 checks the pairing is *self-consistent*,
never forces a 1:1 ratio that does not exist in the source.

---

## 2. Constants — every value carries provenance

```
MEGA_URL_TMPL  = "https://mega.nz/folder/<PH>#<KEY>/file/<HANDLE>"
     PROVEN. HANDLE is the grid row id. Per-file fetch only.
     Peak disk 2.00 GB, never the 320 GB a whole-folder import would need.

FETCH_CONCURRENCY    = 1        # §6.1
REMUX_CONCURRENCY    = 2
TRANSCRIBE_CONCURRENCY = 16     # EU+diarize ceiling is 25; the diarize table
                                # governs the model's 50. Run 16.

FETCH_IMG_BYTES      = 4 GiB    # loopback ext4, kernel-enforced. W0-Cap proves ENOSPC.
CAP_BYTES            = 2_000_000_000   # Deepgram hard cap; one unit displays 2.00 GB
SEGMENT_SEC          = 1500     # PROVISIONAL - 25 min ffmpeg segment
SYNC_CUTOFF_SEC      = 9000     # FALLBACK ONLY. 15x realtime, pessimistic.
                                # 40x was measured on TWO ~3.2 h samples and is
                                # unsafe: the longest call is 276 min and needs
                                # 40x just to survive a 10-min ceiling. Zero margin.
SYNC_HEADROOM_SEC    = 420      # 10-min 504 is server-side; client adds TLS+upload.
ASYNC_POLL_SEC       = 30
ASYNC_TIMEOUT_SEC    = 86400    # retrieval is free, waiting is cheap
FETCH_STALL_SEC      = 120      # no growth -> FETCH_STALL
FETCH_OVERRUN_FACTOR = 1.10     # partial > 1.10x declared -> SIGKILL + rm
POST_KILL_QUIESCE_SEC = 60      # after mega-cancel --all, assert zero growth
WPM_MIN, WPM_MAX     = 60, 260  # PROVISIONAL sanity band. Re-measure §9.
SPAN_EDGE_SEC        = 60       # first.start < 60s, last.end > duration-60s
FORECAST_USD         = 150.56
SPEND_HARD_STOP_USD  = 150.56
RATE_USD_PER_MIN     = FORECAST_USD / 35013    # 0.00430. 35013 = ceil minutes of 583.55 h.
DEEPGRAM_HOST       = "https://api.eu.deepgram.com"
DEEPGRAM_MODEL      = "nova-3"
```

### §2.1 PDF calibration — RE-MEASURED, do not inherit

The `course-corpus-extraction` skill's constants were measured on FireShot-captured
web pages. Its own rule is to re-measure on your own source. Done, 2026-10-15,
`evidence/probes/nhbplus-pdf-text-layer-2026-10-15.json`.

```
Y_TOL         = 0.6    STABLE on 48/50 documents: SHA-256 of ordered line TEXTS is
                      byte-identical at 0.0 / 0.25 / 0.5 / 0.6 / 1.0 / 2.0 / 3.0 / 5.0 pt.
                      Geometry moves (baselines 444 -> 128 on one 22-page doc);
                      the text does not move.
                      LOAD-BEARING on 2 documents - "500-page-swipe-file-clayton-
                      makepeace_compress_1.pdf" and "fourdaycashmachine.pdf" - whose
                      baselines sit within a few points. Recorded, not smoothed over.

TIER_MIN      = 5      A tier is a font size carried by >= 5 lines. Populations on the
                      22-page document are 395 / 133 / 11, so T in 2..10 all recover
                      the same tiers; 5 tolerates a stray span that 2 would promote.

TIER RULE     = gate first (§7 taxonomy). Then title = largest tier,
               body = most frequent tier, every OTHER tier = a heading tier.
               Measured: title 60.0pt, headings [24.0pt] over 133 lines (25% of 539),
               body 11.04pt.
```

**Two inherited constants are wrong here. One fails silently.**

| Constant | Verdict |
|---|---|
| skill's flat `18.0pt` | Wrong. This corpus tiers 60 / 24 / 11.04. 18.0 sits between body and heading and would pass by luck. |
| `title_size × 0.55` → **33.0pt** | **Silently excludes the 24.0pt tier.** This is what made an early extractor report `headings=0` on a document that plainly has 133. |
| char count as a text-layer test | Wrong. Hex glyph indices are bytes; a raster page scored 449,418 "characters" and 597/597 "pages with text". |

---

## 3. The six disputes — decided

| Dispute | Decision | Why |
|---|---|---|
| Fetch concurrency | **1** | Serialising the only unkillable operation costs ~1 h *measured*, not a day. Parallelism multiplies the hazard for ~1 h of saving. |
| Async policy | **all-async, gated on W0-AsyncContract** | A crashed async is free (`request_id` → re-GET). A crashed sync is **paid and lost**. |
| State authority | **receipts on disk**; journal is derived | Two independent truths is a desync waiting to happen. |
| Parts | **primary abstraction**, not a contingency | The 2 GB cap, 504 recovery and tail segmentation become one code path. Single-part is the degenerate 1-element list. |
| Ordering | **docs → 16 longest → cheapest** | Free full-pipeline shakedown, then makespan, then budget robustness if the hard stop bites. |
| PDF | **probe-first, before any STT dollar** | **NOW RESOLVED — see §7. The probe ran; 0 documents need OCR.** |

---

## 4. W0 probes — nothing load-bearing runs before these exist

Each writes `/data/nhb/evidence/YYYY-MM-DD-<name>.json`.

| Probe | Status | Question it answers |
|---|---|---|
| **W0-Fetch** | ✅ PROVEN | per-file route works; `systemctl is-active mega-cmd-server` is **known-false** on Ubuntu 24.04 — only a real fetch is the arbiter |
| **W0-Cap** | OPEN | does a 5 GiB write into the 4 GiB loopback actually raise ENOSPC? An untested cap is not a cap |
| **W0-Remux** | OPEN | `ffmpeg -vn -c:a copy` is audio-identical; log the real size cut (85% expected — measure, do not assume) |
| **W0-SyncCeiling** | OPEN, fallback only | calibrate the sync path. **Must not** be used to raise `SYNC_CUTOFF_SEC` |
| **W0-AsyncContract** | OPEN, **GO/NO-GO for §7** | is async reachable outbound-only, and is retention establishable from a dated source? |
| **W0-PDF** | ✅ **SATISFIED 2026-10-15** | closed — see §7 |
| **W0-Egress** | OPEN | binary VM→PC copy with a per-file SHA256 manifest compared |

### 4.1 W0-AsyncContract — the architecture gate

Streamed POST body (a Python file handle, **never** `curl --data-binary`, which OOMs
at 1.4 GB). `model=nova-3&diarize=true`. No callback URL, no public audio host.
**Persist `request_id` BEFORE polling.** Record: submit path, poll path, GET path,
retention window with a dated source quote, and that re-GET is $0 because Deepgram
bills at processing, not retrieval.

> **If async needs inbound infrastructure, or retention cannot be established from a
> dated source: `ASYNC_ALLOWED = False`.** Fall back to §7b. The multi-part model
> makes vendor async optional rather than load-bearing.

---

## 5. State — filesystem wins, the journal derives

Per unit `/data/nhb/units/<UNIT_ID>/`:

```
state.json             state machine, written BEFORE the fetch, atomic (write+rename)
receipt.json           {parts:[{index,bytes,duration_s,request_id,response_path,status}],
                        effective_spend}
part-00.bin ...        local audio parts
response-part-00.json  RAW Deepgram response, verbatim. THE ONLY IRREPLACEABLE ARTIFACT.
assembled.json         utterances re-offset and deduped
```

Transitions, monotonic, `flock`-guarded:

```
queued -> fetching -> fetched -> remuxed -> segmented -> submitted
       -> received -> assembled -> noted
plus: failed_free_retryable | failed_billable_unknown | PAID_UNKNOWN
      | FETCH_OVERRUN | FETCH_STALL | empty_extraction
```

**Resume rule.** Nothing on disk → redo, free. Parts or responses present →
**re-assemble, never re-transcribe.** `PAID_UNKNOWN` (stale lease, 504, killed
submitter) or `failed_billable_unknown` → quarantine, **operator decides, never
auto-retry**. A unit reaches `submitted` **at most once**.

`/data/nhb/_meta/journal.jsonl` is single-writer, append-only, **derived**.
`bin/rescan.py` rebuilds it from `units/*/receipt.json`. **On conflict, receipts win.**

**Money is derived, never counted.**

```
effective_spend = Σ settle(part.duration_s) + Σ loss(declared)
```

Spend is **committed pre-request** (reserved under `flock`), then **settled** from
`metadata.duration` or **declared lost** on a 504 with no receipt. There is no
`spent.txt`.

> **This is the single most important correctness property in the plan.** A success-only
> counter is wrong: a 504 storm is *paid but lost*, and would sail straight past it.

---

## 6. Fetch — serialised, watched, kernel-capped

All fetches land in `fetch_mnt/` (the loopback). Never to the PC. **Never
`timeout(1)`** — `timeout` does not stop megacmd; a probe silently pulled 4.0 GB
that way.

For each unit in §9 order: write `state.json=fetching` **first**, then
`mega-get <per-file-URL> fetch_mnt/<UNIT_ID>.bin`.

- partial `> 1.10 × declared` → SIGKILL + `rm` + `FETCH_OVERRUN`
- no growth for 120 s → `mega-cancel --all` + `FETCH_STALL`
- on any kill/cancel: `mega-cancel --all`, watch 60 s, **assert zero growth** —
  server-side transfer survives client death — then assert 5 s after SIGKILL

Log throughput. Expected **≈1 h** for 146.87 GB at the measured 41–53 MB/s.

> **One path assumption that is now proven wrong.** `mega-get` names its output after
> the **verbatim source file** and appends the extension
> (`Vimeo gif thumbnail custom code.pdf`), **not** the handle. A handle-prefixed
> existence check reports a fetch failure while the fetch succeeded. Fetch into an
> **empty per-handle directory** and take whatever single file lands. No name matching.

---

## 7. One code path for STT

### 7a. Remux and segment

`ffmpeg -vn -c:a copy` every unit — lossless, cuts upload ~85%, mandatory for the
2.00 GB unit. **`ffprobe` duration is the cost-gate input, not the manifest.**
If remuxed size ≥ `CAP_BYTES`: `ffmpeg -f segment -segment_time 1500` → `part-*.bin`.
Single-part otherwise. **Every part gets its own receipt entry.** This is the unit of
atomicity.

### 7b. Transcribe

Preflight per part under `flock`: `cost = ceil(ffprobe_min) * RATE`. If
`committed + settled + cost > SPEND_HARD_STOP` → **stop, do not submit.** Commit
spend, persist the `request_id` placeholder, then Python-streamed POST.

**Primary (W0-AsyncContract passes) — everything async.** Poll 30 s, GET result, save
raw `response-part-NN.json` immediately (Deepgram stores nothing — the response is
the only retrieval). Assert **both** paths: `results.utterances` non-empty **and**
`results.channels[0].alternatives[0].paragraphs` present. Proven shapes:
`metadata.duration` is a plain float; **`paragraphs` lives under `alternatives[0]`,
not `channels[0]`.** Settle from `Σ metadata.duration`. On 504 or disconnect →
`PAID_UNKNOWN`, quarantine, operator decides.

**Fallback (W0 fails) — sync head, async tail.** Parts with
`ffprobe ≤ SYNC_CUTOFF_SEC (9000)` via sync `/v1/listen`; anything longer via async-tail
if allowed, else segment smaller and sync. Same assertions, same commit/settle.

Concurrency 16. Assembly: concatenate utterances with part offsets, dedupe overlaps
(same start ±0.5 s, or identical text), three-way duration reconcile
(declared vs ffprobe vs Σ metadata), span coverage, WPM 60–260.

---

## 8. Documents — docs before dollars

**109 documents. 37 written_hand + 36 course_doc + 36 orphan.** Fetched and fully
processed before a single STT dollar moves: a free end-to-end shakedown of fetch,
extract, vault-render and egress.

docx/xlsx/pptx via Python stdlib `zipfile + ElementTree` — proven, no dependency.

### 8.1 PDF — MEASURED, the probe gate is closed

`evidence/probes/nhbplus-pdf-text-layer-2026-10-15.json`. All 50 PDFs fetched, 0
failures, 0.159 GB, **$0.00**.

```
pypdf 4.0.2   from the Ubuntu 24.04 archive (python3-pypdf 4.0.2-1).
              Not pip. Not a vendor. No account, no key, no egress.

ROUTE     page.extract_text(visitor_text=...) -> per-span size, baseline, x.
REJECTED  content-stream Tj/TJ regex -> hex glyph indices, not characters.
IMAGES    enumerated via /Resources /XObject. NEVER decoded. 0 bytes written.
```

**Three-class taxonomy. A binary text/raster gate is wrong** — it was tried and
discarded for filing 7 readable documents as degraded and discarding real characters.

| Class | Count | Handling |
|---|---|---|
| `text` | **48** | tiering and reflow valid, layout trusted |
| `sparse` | **2** | *AC eBook*, *AC_Book* — both 340 pp at ~3.4 words/page, 0.18 img/page. Real characters extracted, layout flagged untrusted. **1,372 words.** Never dropped. |
| `raster` | **0** | needs OCR; none is proven free, so it would ship `empty_extraction` and **never be OCR-billed**. Vacuous here. |

**65,985 recoverable words. Zero documents require OCR.**

**Links: `/Annots` is the ONLY authoritative link layer.** Measured: *Swipe* carries
400 raw annotations, **201 distinct** — half boilerplate. Its text-layer URLs are
mangled by wrapping; "Calculator" renders as `Calcu` / `dit#gid=5683798` / `lator`.
Never recover a URL from display text.

**Reflow.** Five-clause join plus the sixth veto, each clause named, with
`reflow_min_len` = median non-heading body line length **measured per document**.
Assert the one-space token-multiset invariant and `chars_stripped_equal` on every
document.

---

## 9. Ordering — worklist order is load-bearing

`worklist/targets.csv` — **NEVER globbed. The only work list.**

Columns: `unit_id,handle,kind,raw_name,clean_name,year,month,declared_bytes,ffprobe_s,cost_usd,doc_class,state`

1. **All 109 documents first** — free shakedown, exercises everything except STT.
2. **16 longest audio head-of-line** — fills 16 lanes, minimises makespan.
3. **Remainder cheapest-first** by `ceil(ffprobe_s/60) * RATE` — maximises completed
   units if the hard spend stop bites.

> Alphabetical ordering is **dropped**: unjustified, and worst for both makespan and
> budget robustness.

---

## 10. Vault assembly — on the VM, then copy

```
vault/calls/<year>/<MM Month>/<CLEAN NAME>.md
vault/written-hands/<year>/<MM Month>/<CLEAN NAME>.md
_meta/manifest.json
```

Exactly **5 frontmatter fields**: `title, date, type, duration, speakers`.
**ALL source, transcription, integrity and provenance data → `_meta/manifest.json`,
never into a note.** Written hands are **separate notes**, linked both ways.

**Clean filenames** (operator overrode verbatim MEGA names): strip ordinal prefixes,
brand tokens (`NHB`/`NHB+`/`FF`), the word `Call`, `_watermarked`, underscores, stray
brackets; normalise embedded dates to ISO from the manifest; **preserve intra-word
hyphens** (`Ron-Lynch` intact); course-prefix the 5 colliding `Resources Links`.
Verbatim MEGA name retained **in the manifest only**. Extension-in-stem
(`*.mp3.md`) is a bug — never emit it.

> Accepted wart, documented: MEGA dates are MM-DD-YYYY, so lexical order is by
> day-within-month. Month folders make order correct by construction.

---

## 11. Verification — 12 gates

| Gate | Assertion |
|---|---|
| V0 | worklist integrity: 339 rows, never a glob |
| V1 | fetch caps: ENOSPC proven, overrun/stall counts |
| V2 | remux/segment: no part ≥ `CAP_BYTES` |
| V3 | STT contracts: both response paths on every receipt, `request_id` persisted pre-poll |
| V4 | three-way duration reconcile |
| V5 | span coverage (`first.start<60s`, `last.end>duration-60s`) |
| V6 | **zero media extensions under `vault/`** — mechanical proof of Constraint 1 |
| V7 | reduction diff: re-render every note from `(receipt, response.json)`, byte-compare |
| V8 | frontmatter exactly 5 fields; path and clean-name rules |
| V9 | counts 37 / 36 (+36 orphan); **a mismatch is a scope discrepancy to REPORT, never fudged.** Videos and documents are independent — no 1:1 forced |
| V10 | spend `Σ settle + Σ loss ≤ 150.56`, **derived from receipts** |
| V11 | egress SHA256 per-file match |

Exit codes 0 / 10 / 20 / 30 / 40. Any gate failure **writes its receipt and increments
its count**. **Resume never re-bills.**

---

## 12. Egress and teardown

Binary-only copy VM→PC of `vault/` + `_meta/`. **The finished markdown IS the
deliverable; nothing media-shaped ever touches the PC.** Per-file SHA256 manifest
compared. PowerShell pipelines are **forbidden by name**.

Teardown is 7-phase. Final destroy requires
`--confirm <sha256 of copy-verification.json>` — deliberately awkward, so the
operator has demonstrably looked.

---

## 13. Where the four plans are wrong

Not just divergent — wrong. Eleven items, kept because they constrain execution.

1. **"146.87 GB ≈ 30–50 h serial fetch" is ~30× wrong.** Measured 41–53 MB/s → **0.99–1.28 h**.
2. **A `*.mp3.md` filename is a bug** — extension in the stem.
3. **Alphabetical-smallest-first is unjustified and pessimal** — delays LPT fill and budget robustness.
4. **Any 40×-realtime sync cutoff is unsafe.** The longest call is 276 min against a 10-min ceiling — 40× to survive, zero margin. 15× pessimism is the only defensible cutoff.
5. **Any success-only spend counter is wrong.** A 504 storm is paid-and-lost and sails past it.
6. **Any SQLite/journal/per-unit-JSON as independent truth alongside receipts is a desync waiting to happen.** Exactly one may be authoritative.
7. **Any disk "bound proof" (38 GB vs 400 GB) without the loopback is not a safety system.** Only kernel ENOSPC counts, and only after the overflow probe proves it.
8. **Any plan treating `kill`/`timeout` as the fetch safety system is wrong.** The system is admission control + watcher + `mega-cancel --all` + quiesce assertion.
9. **Unconditional all-async *and* unconditional sync-tail are both wrong until W0 rules.**
10. **Any direct reuse of the PDF calibration constants is wrong** — see §2.1.
11. **Briefing errors all four plans caught and this spec carries:** documents are **37+36+36=109**, not 37+36; 50 PDFs had no proven path (now measured); and 42 videos vs 36 docs is **not** an error.

### 13.1 Claims withdrawn during planning

Kept visible, because a withdrawn claim is evidence about the corpus.

| Withdrawn | Why |
|---|---|
| "PDFs may be ~25 image-only scans" | **Measured: 0 need OCR.** Guessed from file size. |
| "4/4 PDFs have a text layer; zero image-only" | Hex glyph indices counted as characters. **Character count is not a text-layer test.** |
| "Y_TOL is stable across 0.0–5.0pt" | Asserted from a counter that could not fail (539 lines vs 444→128 buckets). **Now digest-proven.** |
| "The 1.0pt reading is my own fallback, contaminating the gate" | `fallback_share = 0.0%`. **The hypothesis was falsified by instrument.** 1.0pt is a real reported font size. |
| "4/4 fetches failed" | mega-get names output after the verbatim file, not the handle. The route was working. |

---

## 14. Provisional — re-measure if these move

`SEGMENT_SEC`, the WPM band, `RATE` if Deepgram pricing shifts (recompute from a
dated price page; still $0 added unless the forecast is re-approved), the remux
saving, the actual async retention window.

`Y_TOL = 0.6` is load-bearing on exactly 2 named documents (§2.1). If either shifts,
those two need re-verification before their layout is trusted.

---

## 15. Open at G1

- 2 sparse PDFs: characters extracted, layout untrusted. Whether the vault needs
  their layout is a **presentation** decision, not an extraction one. Flagged.
- `7-Figure VSL Script Template` was classified degraded and missed the fallback
  audit on a name mismatch; it measured 814 words/page (80× the sparse threshold) so
  it is readable, but was not separately audited.
- 3 defects in `pipeline/scripts/design-names.py`: the UNSAFE dropped call
  (`10-31-2022 NHB+ Mindstream Call` — 188 became 187), the over-eager dash splitter,
  and course-prefixing for the 5 `Resources Links`.