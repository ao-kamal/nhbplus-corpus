# ROUND 2 (CANON) — repo-grounded review, 60 findings

Ran on `opencode-go/step-5-preview-free`, sequential, after round 1 and the
six-probe revision. **26 BLOCKING + 24 NON-BLOCKING + 10 COSMETIC.**

**Verdict: NOT executable as written.** DISAGREE, naming §2.2, §6.3, §7.1–§7.2,
§11 V9/V12, and §3 + §0 D3.

Full findings as returned are held in the session record. The ten that matter
most, all applied:

| | Finding | Effect if shipped |
|---|---|---|
| **B4** | `COMMIT_COST = billed_seconds × (RATE + KEYTERM)` — seconds × **dollars-per-minute** | **60× overcommit.** $20.16 instead of $0.336 per hour-long part; corpus commits $11,764.40 against a true $196.07. The preflight stops the run after ~10 parts. |
| **B1** | `dvcEDToK` is **not** the longest call. **46 calls are longer.** True worst case `wiUyTRZb`, 275.9 min | W0-SyncCeiling closed on the wrong unit. True margin ~4.2×, not 5.7×. Gate REOPENED. |
| **B1b** | The 273.7× was a **60× unit slip**, not an extrapolation error | 600 s at 126× is 75,600 **seconds** = 21 h, not 75,525 minutes. Corrected margin 4.57×, which matches the measurement. Same defect class as B4. |
| **B7** | V9's `kind == "call"` matches **0 handles** | The gate written to catch the dropped call **cannot fire**, and passed vacuously on the one confirmed live defect. |
| **B19** | No script writes `path` to any document record (grepped all of `pipeline/scripts/`) | V8 **can never pass**; §9's docs shakedown cannot complete. A build task, not a note. |
| **B2** | The 3.00 GB unit is `3 × 2³⁰` — **a sentinel** — and a never-fetched MP4 alternate. Its fetched primary is **151 MiB** | A safety factor was removed on the authority of a phantom. Largest non-sentinel audio is 1.0654 GB. |
| **B3** | Sentinel reserve stated as both **512 MiB and 2,560 MiB**, 20 lines apart | 5× disagreement inside one block on the safety-critical number. 512 MiB was 3× under. |
| **B26** | "Peak disk 2.00 GB, PROVEN" was the **sentinel value**, 36× repeated | Constraint 6 forbids consuming a sentinel, and §2 was doing exactly that. Measured peak is 1.50 GiB. |
| **B20** | "67 of 296 names" is actually **50 of 229** paths, 7 true mangles | The denominator 296 excludes the 42 lessons, one of which is damaged. §15 called this the largest remaining work on a figure 10× the truth. |
| **B23** | **MP3-in-`.mka` has never been submitted** to Deepgram | The container fix for the 97-MP3 `.m4a` failure is itself unverified at the vendor boundary. $0.16 to close. |

## Not yet applied — carried forward

- **B5/B11/B12** — per-account ledger asserted in §2.2 but §5.3 has no `account`
  field and §5.5 still carries the old formula; "all transcription on the primary"
  and "the secondary carries the shortfall" cannot both hold.
- **B13** — the spec quotes Deepgram's ToS prohibiting account multiplication and
  then *requires* a second account. Rule 2 bars free-credit tiers and never waived it.
  Operator decision, not an engineering call.
- **B16/B17/B18** — three conflicting vault trees across §10, §12 and
  `VAULT-STRUCTURE.md`; `courses/` missing from §10 while `design-names.py` already
  emits it; 42 lesson notes have **no gate asserting they exist**.
- **B23/B24** — `.mka` for MP3 untested; `-map_channel` asserted lossless for
  joint-stereo MP3, which is not a valid stream copy.
- **B25** — the admission predicate needs REAL bytes that **do not exist until
  after the fetch**, so the control cannot be evaluated before the act it bounds.
  Same shape as the sentinel bug: a safe-looking control that is not one.
- **B8** — `request_id` existence is contradicted by two same-dated artifacts, so
  V12 clauses 5–6 and AUDIT.md's column are unfalsifiable.
- **B6** — three hard-stop values ($207.31 / $207.35 / correctly derived $207.68).
- **C10 (PROCESS)** — the spec changed three times *during* this review, because
  I launched round 3 on top of round 2. That is my error and it invalidates the
  convergence signal for both rounds. Rounds must be sequential.