# Stage 0 — Intent (G0) · NHB+ mentorship-archive transcription

> **Status:** G0 **PASSED** — operator sign-off 2026-10-15. Stage 1 may begin.
>
> **Repository:** `Content OS/nhbplus-corpus/`, a sibling of `content-os/` in the same
> git repo. A separate build on a separate corpus, consuming `cut30-vault/` not at all.
> `content-os/stage-0-intent.md` governs a different build and confers no authority here.

Every figure below is a current measurement with a dated evidence artifact under
`evidence/probes/`. A number that could not be measured is written
**ABSENT**, never estimated.

---

## 1. What we are building

**A call-shaped Obsidian vault** transcribed from the "Alen Sultanic — NHB+ —
Nothing held back Plus (Up to 02.2025)" MEGA public share.

| | units | hours | GB |
|---|---|---|---|
| Calls | 188 | 557.39 | — |
| Bonus lesson videos | 42 | 26.16 | — |
| **Audio total** | **230** | **583.55** | **146.39** |
| Written-hand documents | 37 | — | 0.017 |
| Course companion documents | 36 | — | 0.072 |
| Orphan documents (Swipes, Templates) | 36 | — | 0.397 |
| **Document total** | **109** | — | **0.486** |
| **Everything fetched** | **339** | **583.55** | **146.87** |

**STT forecast $150.56** at Deepgram's $0.0043/min. **Peak disk 2.00 GB** — the
largest single file — because one file is fetched at a time and deleted after
transcription.

The share itself is 319.95 GB. **146.87 GB is fetched**, because MP3 is preferred
wherever an MP3 exists and **105 MP4 siblings are recorded as alternates and never
fetched**. STT cost is identical either way — Deepgram bills audio minutes, not
bytes.

**This is not a link index and not a download.** The deliverable is machine-readable
transcripts with per-call provenance back to the source file.

### The unit that comes out the other end

One note per call, partitioned `calls/<year>/<MM Month>/`, filename identical to the
MEGA filename. The transcript is the spine. A companion document is linked where one
exists, and **its absence is recorded explicitly rather than implied** — 151 of the
188 calls have no written half.

> **This is not the CUT30 seven-entry lesson contract.** That shape assumes a written
> half exists on every lesson. Here most calls have none, and forcing them into a
> lesson vault would misrepresent the corpus's own contents. Operator decision:
> *call-shaped vault*.

The written register is wider than the calls. **36 documents have no counterpart at
all** — 4 swipe/lead-magnet PDFs and 32 funnel-template files — and they belong in
the vault without pretending to attach to anything.

**`Bonuses` is eleven structured video courses**, 42 lesson videos across 11 folders.
Five of the eleven are *mostly documents*: the video is an introduction and the
material is the files beside it.

---

## 2. Why — the constraint

**The corpus cannot be assembled on the operator's machine.** "I refuse to download
to PC" is the requirement that selects every route, not a preference to work around.

No media, no video, and no intermediate lands on the operator's PC. **The finished
vault does** — it is the deliverable. Nothing heavy runs locally; the machine is not
the build.

**`megacmd` is the only thing that can decrypt this corpus.** MEGA's own API returns
HTTP 402 (proof-of-work) to every third-party client — mega.py, rclone,
MegaApiClient. Anonymous sessions receive handles and never keys. megacmd is MEGA's
own binary, so it answers the 402.

**Compute is a throwaway remote Linux VM.** Azure, Austria East, `Standard_D2s_v5`
(2 vCPU / 8 GB), 500 GB disk. ~$0.21/day idle against a $200 credit. **Rule 2 is
what forces this**: free tiers that could hold the corpus were disqualified on
capacity before they were ever disqualified on price.

**Per-file retrieval is what makes it viable.** Fetching one file at a time drops
peak disk from 320 GB to 2.00 GB. Without it the VM needs a 500 GB disk and the
free tiers return.

---

## 3. Who it serves

**Primary: the operator.** One person, consuming a searchable record of calls they
attended or own, plus the written material surrounding them.

**Secondary: the operator's own knowledge system.** Obsidian-flavoured Markdown with
YAML frontmatter, so it opens as a vault and is greppable without tooling.

Agnostic by construction: nothing hard-codes the operator's identity, locale, or
brand. A Nigerian locale is a configuration surface, not an assumption in the
mechanism.

---

## 4. Core workflows

### 4.1 The single workflow

```
for each of 339 targets in scope-final.json:            # the manifest, never a glob
    resolve source file                                # MP3 preferred; MP4 recorded, not fetched
    fetch + decrypt                                    # megacmd, anonymous, per-file URL on the VM
    [mp4] remux audio only                             # ffmpeg -vn -c:a copy — lossless, no re-encode
    POST to Deepgram EU                                # streamed from a file handle
    validate BOTH response paths                       # utterances non-empty AND paragraphs present
    cross-check duration against the manifest          # ±2%; catches a truncated fetch
    write transcript + receipt                         # receipt before anything is deleted
    delete the media                                   # immediately, on the remote box
    assert cumulative spend < ceiling; STOP if exceeded
```

**Both response paths are asserted.** `results.utterances` must be non-empty and
`results.channels[0].alternatives[0].paragraphs` must be present. A response that
parses but returns neither is a failure, not a transcript.

### 4.2 The workflows that are *not* in the corpus

Each is excluded, and the exclusion is recorded because its absence is a design
fact, not an oversight:

| Not here | Why |
|---|---|
| Video assembly, editing, post-production | Content OS's job — a separate build |
| Transcript → first-article generation | Content OS consumes this corpus |
| Speaker identification | Deepgram diarises; it does not identify. `Speaker 3` stays `Speaker 3` |
| A cross-call speaker graph | Requires name matching across 188 calls; one false merge corrupts everything downstream |
| AI-summary PDFs | Excluded by operator decision — 150 calls have one; 151 have no written half of any kind |
| Any vendor account | Anonymity is sufficient; an account is a new dependency |

---

## 5. Known technical constraints

### 5.1 The two hard rules

**Rule 1 — remove nothing.** No capability descoped. Where a route to one is
blocked, the route changes; the capability does not.

**Rule 2 — pay nothing.** No paid tier, no metered API, no vendor free credit tier.

> **Sole recorded exception:** Deepgram, the metered STT call. Waived twice, credits
> confirmed by the operator. Recorded for audit accuracy, **not** as an open blocker.
> Forecast and actual spend stay separate in every report, and the run still stops at
> the ceiling. Confirming credits is not the same as removing the ceiling.

**The rule carrying both: no claim about what a platform permits is believed until a
live probe proves it, with a dated evidence artifact.** A prior is not evidence — five
platform priors in this project were wrong on five of five platforms against the
operator's own live probes.

### 5.2 Vendor limits, read from the documentation

| Limit | Value | Consequence |
|---|---|---|
| STT concurrency, EU, with diarisation | **25** | The diarisation table governs; the model table's 50 does not apply. **We run 16** |
| STT concurrency, EU, without diarisation | 50 | Not applicable — diarisation is required |
| Maximum file size | **2 GB** | One unit is 2.00 GB displayed, i.e. 1.5–2.5 GB actual. **Remux is required** |
| Synchronous request duration | 10 min → `504` | Longest call is 276 min ≈ 6.9 min at 40× realtime. Inside, with the thinnest margin in the build |
| Transcript retention | **none** | The API response is the only retrieval. Receipts and transcripts are written **before** any delete |
| Response shape | `metadata.duration` is a float; `paragraphs` lives under `channels[0].alternatives[0]` | Both paths asserted; a parse that "succeeds" with zeros is a failure |

### 5.3 Transport facts

- **Per-file URL**: `https://mega.nz/folder/<PH>#<KEY>/file/<HANDLE>`. The `::`
  subpath syntax is not the mechanism and never was.
- **Upload bandwidth is not the bottleneck.** The VM's NIC allows 12,500 Mbps; a
  single upload uses 4.6% of it. 159 s for 1,436 MB was Deepgram *processing* at
  ~40× realtime, which no bandwidth change would alter.
- **`curl --data-binary @file` loads the entire body into memory** and reports a
  misleading `out of memory` at 1.4 GB. Python streams the file handle instead.
- **Peak disk is one file.** Never the tree.

### 5.4 Operational hazards

- **`timeout` does not stop a megacmd fetch.** A bounded client kept running and
  pulled 4.0 GB after it died. Disk is asserted after every file with a floor tied to
  expected size; process timeouts are not a control here.
- **A presence check needs a floor.** Three checks in one session passed on empty
  results. "Did I get roughly what I asked for", not "is this number small".
- **Never glob the output directory to build the work list.** Targets come from the
  manifest; a glob matching its own output re-bills the corpus.
- **A duration the source does not carry is ABSENT.** Every call carries a year.
  Course lesson videos do not, and that is correct.

---

## 6. Evidence base

Stage 1 does not re-derive any of this and may not re-open it without a dated
counter-artifact. All under `evidence/probes/`.

| Fact | Artifact |
|---|---|
| Per-file fetch solved; peak disk 2.00 GB not 320 GB; every dead route enumerated | `nhbplus-perfile-fetch-solved-2026-10-15.json` |
| 188 calls / 42 lessons; 56.56 h of duplicate audio identified and merged; mojibake repaired | `nhbplus-identity-correction-2026-10-15.json` |
| Full chain proven end to end; EU+diarise cap 25; 2 GB and 10 min limits; response shape | `deepgram-eu-limits-and-chain-proof-2026-10-15.json` |
| Share is 319.95 GB; Calls & Playlists is 312.16 GB | `mega-nhbplus-corpus-census-2026-10-14.json` |
| megacmd fetches a public link with **no account** and **decrypts** | `megacmd-public-link-anonymous-2026-10-14.json` |
| Deepgram accepts MP4 containers; consent gate passes | `deepgram-capability-probe-2026-10-14.json` |
| docx/xlsx/pptx extract with the Python standard library alone | `nhbplus-binary-office-extractability-2026-10-14.json` |
| MEGA rounds every displayed file size to a whole unit; folder figures **are** additive | `nhbplus-residuals-root-cause-2026-10-14.json` |

**Superseded figures are recorded in the artifacts, not in this document.** G0 states
what is true now. Where an earlier figure disagrees and no test settles it, both
appear in the artifact and neither is adopted by preference.

---

## 7. Boundary

**In scope:** enumeration, per-file fetch and decryption on remote compute,
transcription, receipting, resumability, spend-ceiling enforcement, call-note
emission with provenance, capture of companion documents, capture of the orphan
Swipes and Templates material, and the eleven bonus courses.

**Out of scope:** anything the Content OS spec owns; any vendor account; any
persistent copy of audio or video; any local processing on the operator's PC.

---

## 8. G0 sign-off

**G0 passes when the operator reads §1–§7 and either confirms that what, why, users
and workflows are correctly stated, or corrects them.** Stage 1 does not begin until
it passes.

**G0 PASSED 2026-10-15** — operator confirmed §1–§7. Stage 1 is unblocked.