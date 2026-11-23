# Batch 2 — Delta Plan (NHB+ continuations)

**Date:** 2026-11-23
**Status:** PLAN — pending execution
**Authority:** This is a *delta* on `stage-1/stage-1-spec.md` (rev 1), not a new plan.
The spec, its gates V0–V13, its constants-with-provenance, and the 35-bead graph
(recoverable at `git show 4e2895f^:.beads/issues.jsonl`) are the authoritative
architecture. Nothing here overrides them; where this document is silent, the spec wins.

---

## 1. What this batch is

The operator supplied a MEGA folder of **continuations** — later calls in the same
NHB+ archive, March 2025 → April 2026. They are **not** stitched to existing notes:
each is a new, standalone call note in the **same vault** as corpus #1. No new note
architecture, no new gate logic, no new pipeline stage.

Source folder: `https://mega.nz/folder/7WZkxQjK#yc0fQSTRiV2_NXUF7XFV4Q`

## 2. Recon result (evidence: pipeline/out/batch2-*.json)

The folder mixes old and new. The re-shared 2021–25 tree (NHB Calls Playlists,
Swipes, Templates, Bonuses) is corpus #1 and is **excluded**. The new material is
in the two UPDATE trees plus the 2025 guest playlists.

| Class | Count | Decision |
|---|---|---|
| Audio rows (mp3/mp4) | 400 | Dedup by call → **362 unique calls** |
| — mp3/mp4 duplicate pairs | 36 | Transcribe **once** per call |
| — mp4 only | 1 | include |
| Known durations | 360 calls, **878.7 h** | 2 calls need on-fetch measurement |
| Resource docs | 50 (22 pdf, 27 docx, 1 other) | Ship as **native attachments**, no md conversion |
| "AI Summary" files | 83 (10 mp4, 68 pdf, 5 other) | **Excluded entirely** — no STT, no import, no attachment |
| Handle/name overlap with corpus #1 | 0 | Clean new set |

**Spend estimate (derived, not asserted):** 878.7 h × 60 × $0.0056 = **$295.25** at
the mono/keyterm-on rate; ~$590 if every unit keeps stereo. **No hard stop** — the
operator wants everything transcribed. The vendor's ~$200/account 402 backstop still
applies, so the secondary key is a required sequential wallet, not optional.

## 3. Decisions carried forward (operator, 2026-11-23)

1. Same vault — append to the existing `vault/`, do not create a second one.
2. No stitching — each continuation is its own note.
3. Resources ship as native binaries in `vault/attachments/`. **Skip the
   convert-to-markdown stage entirely** (`extract-pdf.py`, `extract-ooxml.py`,
   `extract-misc.py` are NOT used in batch 2). This reverses the spec's §8 rule
   and matches the corpus #1 delivered state; operator explicitly changed their mind.
4. AI Summary files excluded — no STT, no import, no attachment.
5. No spend stop; transcribe all 362 calls.

## 4. Reuse ledger

**Reuse as-is (no edits):**
`part-state.py`, `channels.py`, `submit.py`, `spend-ledger.py`, `fetch-pool.py`,
`disk-cap.py`, `frontmatter.py`, `assemble.py`, `run-gates.py`, all `gate-v*.py`,
all `test-*.py`, `rescan.py`, `verify-names.py`, `verify_egress.py`.

**Parameterize (population/constants only — logic unchanged):**
- `build-worklist.py` — `N_ROWS`, `N_AUDIO`, rates, input paths → read from a
  batch-2 config file instead of hardcoded 344/235/0.0043.
- `bulk-run.py` — `BASE`, `WORK`, the $213.48 stop reference, key paths → same config.
- `design-names.py` — the 193/42/109 counts are assertions; re-derive from the new
  scope or relax to equality against the emitted set.
- Gate constants (V8's 344 floor, V9's 235) → batch-2 values (412 notes, 362 audio).

**New (small, bounded):**
- `batch2/scope.json` — the 362-call worklist with handles, URLs, durations,
  container choice (mp3 preferred where both exist), and the 50 resource handles.
- `batch2/config.json` — paths, rates, key locations, no-stop flag.
- Bead graph regenerated from the 35 recovered templates (new IDs, batch-2 prefix).

**Explicitly not used:** `extract-pdf.py`, `extract-ooxml.py`, `extract-misc.py`.

## 5. Execution sequence (mirrors corpus #1)

1. **Fresh probes** — Deepgram rate/concurrency/credit + MEGA per-file fetch.
   All prior probes are dated 2026-10-14/15; the spec's own rule forbids relying
   on a prior. Dated artifacts into `evidence/probes/`.
2. **Beads** — regenerate 35-bead graph from recovered templates; `br dep cycles` empty.
3. **Provision** — new VM, 4 GiB loopback (`provision-loopback.sh`), keys restored
   from `.env.private` (primary) and `.env.private.bak-2026-11-09` (secondary,
   `DEEPGRAM_API_KEY_2`) **at use time**, never written into the repo.
4. **Fetch → remux → channels → submit → settle** — the existing `bulk-run.py`,
   with container dedup applied before fetch (mp3 preferred; the 36 mp4 duplicates
   are never fetched). 25-way sync, 402 failover to the wallet, PAID_UNKNOWN never
   auto-resubmitted. No stop; run to completion.
5. **Resources** — fetch the 50 docs to `vault/attachments/` as native binaries.
   Do not convert. Record hashes.
6. **Assemble** — append 362 audio notes + 2 updated indexes to the existing vault.
   `00 Topics.md` 235 → 597 rows. Frontmatter value domains unchanged.
7. **Verify** — gates V0–V13 on the merged tree; AUDIT.md 235 → 597 rows;
   copy-verification on all files; typography check on all notes.
8. **Egress + teardown** — binary copy to PC, V6 before copy, shred keys, destroy VM.

## 6. Risks / open items

- **Spend** ~$295 needs the secondary wallet (402 at ~$200/account). Both keys are
  known where to find them, but their *validity* is unproven — probe before spending.
- **2 undated durations** — measure on fetch, as corpus #1 did for `dvcEDToK`.
- **Container dedup correctness** — 36 calls exist as both mp3 and mp4; picking
  the wrong one could double-fetch or lose a call. Assert 362 unique calls before
  any submission.
- **AI Summary exclusion** — 83 files must be filtered at the worklist stage so
  they cannot leak into either STT or attachments. Gate on the literal token.
- **Spec contradiction** — batch 2 deliberately follows the operator's native-
  attachment decision over spec §8. This is recorded here, not silently applied.
