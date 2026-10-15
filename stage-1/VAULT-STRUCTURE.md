# Vault structure — NHB+ corpus

**Status:** proposed, pending operator sign-off. **Decided 2026-10-15:**
year → month for calls · written hand inside the call note · one folder per course.

Nothing is fetched against this document until it is signed.

---

## 1. Why this shape

Three properties the vault has to have, and what each one bought:

| Property | How the shape delivers it |
|---|---|
| You can find what was said on a given day | Calls partition `year → month`. The source already partitions this way, so no information is invented |
| Every note traces to a source file | The **filename is the MEGA filename**, untransformed. One note, one source, visible equality |
| The written half is never silently dropped | Frontmatter carries `written_hand: null` when absent. Absence is a *recorded fact*, not an omission |

Rejected, with reasons:

- **Mirror the MEGA tree** — preserves the duplicate-name confusion that caused
  53.06 h of double-counting in the first place.
- **Type-first** (`calls/Theory/`…) — groups like with like, but scatters any single
  month across five folders. Type is queryable from frontmatter; it does not need
  to be the navigation.
- **Flat 236 files in one folder** — unwieldy in Obsidian's file pane.

---

## 2. The tree

```
nhbplus-vault/
├─ 00 Home.md                        index, totals, entry points
├─ calls/
│  ├─ 2021/
│  │  └─ 06 June/
│  │     └─ 2021-06-07 NHB+ Call - ....md
│  ├─ 2022/
│  │  ├─ 10 October/
│  │  │  ├─ 2022-10-06 FF_NHB+ Training Call - Bible Offer + Recurring Membership.md
│  │  │  └─ 2022-10-13 FF_NHB+ Training Call - Web Hosting Offers.md
│  │  ├─ 11 November/
│  │  └─ 12 December/
│  ├─ 2023/
│  ├─ 2024/
│  │  └─ 08 August/
│  │     └─ 2024-08-05 Guest Call - Lonnie Jones on SEO How To Build Authority.md
│  └─ 2025/
│     └─ 02 February/                20 calls — the largest month
├─ courses/
│  ├─ 00 Courses.md                  all 11, grouped and costed
│  └─ 7-Day Fast Start/
│     ├─ 00 7-Day Fast Start.md      course index (MOC)
│     ├─ 01 7-Figure Math & AC Formula.md
│     ├─ 02 Your Market, Superpower & Disruptive Idea.md
│     └─ 07 Getting Your First 10 High Ticket Clients.md
├─ library/
│  ├─ 00 Library.md                  index
│  ├─ swipes/                        4 PDFs — swipe / lead-magnet creative
│  ├─ templates/                     31 PDFs + 1 ZIP — funnel build files
│  └─ resources/                     per-course resource-link files
├─ attachments/                      raw docx / pptx / xlsx as fetched
└─ _meta/
   ├─ manifest.json                  every target, receipt, sha256, cost
   ├─ scope-final.json               the locked scope this vault was built from
   └─ provenance.md                  how every number in the vault was obtained
```

**Paths use the label, not the raw folder name.** `6. June - 2024` becomes
`2024-06 June`. Raw MEGA folder names carry ordinal prefixes and inconsistent
spacing that would leak into every path.

---

## 3. Filename rules

| Kind | Rule | Example |
|---|---|---|
| Call | the MEGA filename, verbatim | `2024-03-07 NHB+ Theory Call - Converting Audiences.md` |
| Course lesson | `NN Title.md`, zero-padded | `03 The Psychology Of Business Models.md` |
| Course index | `00 <Course>.md` | `00 7-Day Fast Start.md` |

Characters stripped from any filename: `< > : " / \ | ? *` and control characters.
The MEGA names in this corpus are already clean; the strip is a guard, not a
routine transform.

---

## 4. Frontmatter — every field, and where it comes from

Nothing here is typed by hand. Every value traces to a receipt or the manifest.

```yaml
---
# ---- identity -------------------------------------------------------------
id: 2024-03-07-theory-3-EqN2UTLK      # unique; keys exactly one note
kind: call                            # call | lesson
title: 2024-03-07 NHB+ Theory Call - Converting Audiences
date: 2024-03-07
type: theory                          # theory | guest | coaching | training | other
topic: converting audiences
vault_path: calls/2024/03 March/...

# ---- source ---------------------------------------------------------------
source_handle: EqN2UTLK               # MEGA node handle — stable, resolvable
source_ext: mp3
source_bytes: 140086019
mp4_alternate_not_fetched: 1          # recorded, never billed

# ---- transcription --------------------------------------------------------
duration_s: 11662.308
duration_human: 3h 14m
words: 37027
utterances: 2058
paragraphs: 1149
speakers: 22
model: general-nova-3
stt_request_id: 01a13cfc-1b03-7e10-94cb-a448d81cb512
stt_sha256: 6953fcd956696173279efcd7e194f2cacc4f9852fcce7981e7ff8371dc075a00

# ---- the written register -------------------------------------------------
written_hand:                        # null is a RECORDED FACT, not a gap
  name: NHB+ Selling To Women 2
  ext: docx
  handle: ...
  extracted_chars: 18422
  attachment: attachments/...

# ---- integrity ------------------------------------------------------------
duration_crosscheck: pass             # pass | fail — Deepgram vs manifest
size_floor_check: pass
transcribed: 2026-10-15T00:00:00Z
---
```

`duration_crosscheck` and `size_floor_check` are **not decorative**. They are the
two guards that caught today's defects, and they stay in the note so a future
reader can see the transcript was verified rather than assumed.

---

## 5. The call note

```markdown
---
(frontmatter above)
---

# 2024-03-07 NHB+ Theory Call - Converting Audiences

**3h 14m** · 22 speakers · 37,027 words · [[general-nova-3]]
Recorded 2024-03-07 · source `EqN2UTLK`

## Transcript

<!-- elided in this spec. The two lines below are REAL output, but they are from
     the 2022-04-18 Mike Gandia call, NOT from the 2024-03-07 note whose
     frontmatter is shown above. They are quoted to show the rendering format.
     Never pair a frontmatter block with a transcript you did not verify came
     from that same source. -->

[00:02] **Speaker 0** — Alright, gang. Today is Monday, 04/18/2022...

[12:41] **Speaker 3** — ...

## Written hand

> **No written half for this call.**
> Recorded absence — this is a property of the corpus, not a processing gap.

<!-- when one EXISTS: -->
## Written hand — *NHB+ Selling To Women 2*

[[NHB+ Selling To Women 2]] · `.docx` · 18,422 characters extracted

<extracted text here>

## Provenance

- MEGA handle `EqN2UTLK` · SHA-256 `6953fcd9…`
- Deepgram request `01a13cfc-1b03-7e10-94cb-a448d81cb512`
- `manifest.json` → `EqN2UTLK`
- An MP4 of this call exists and was **not** fetched: `alternates_not_fetched: 1`
```

Timestamps render as `[h:mm:ss]`. Speaker labels are Deepgram's diarisation
indices — they are stable within a call and meaningless across calls. Do not
pretend otherwise; they are labelled `Speaker N` and nothing more.

---

## 6. Index pages

Four levels, each generated, none hand-maintained:

| File | Content |
|---|---|
| `00 Home.md` | totals, year links, links to Courses and Library |
| `calls/YYYY/00 YYYY.md` | that year's calls by month, with counts and hours |
| `calls/YYYY/MM Month/00 MM Month.md` | that month's calls, in date order |
| `courses/00 Courses.md` | all 11 courses, videos, hours, cost |

Month folders hold a small number of calls — **2025-02 holds 20** — so a month
index is worth it. Year folders hold at most 12 months, so a year index earns
its place; anything coarser does not.

---

## 7. Linking rules

- A call links to its course material **only where the corpus says so** — where a
  lesson's name or the call's topic genuinely matches. No speculative links.
- A course index links to its lessons in order.
- `library/` documents link **up** to nothing. They have no call counterpart,
  and inventing a relationship would be a fabrication.
- Every call links to its month index. That is the only guaranteed backlink.

---

## 8. What this shape deliberately does not do

- **No speaker identity.** Deepgram diarises; it does not identify. `Speaker 3`
  stays `Speaker 3`.
- **No cross-call speaker graph.** It would require name matching across 194
  calls, and a false merge there corrupts everything downstream.
- **No AI summaries.** 165 exist in the source and decision C excluded them.
  Adding them later is additive and needs no migration.
- **No transcript → article generation.** That belongs to Content OS, a separate
  build.
- **No timestamps invented.** A duration the source did not carry is recorded as
  absent. 6 calls currently have no recoverable year.

---

## 9. Reconciliation — all three closed

### 9.1 G0's "84 calls / 250.5 h have no written half" — WITHDRAWN

G0 §1 cites `nhbplus-call-join-slotrule-v2-2026-10-14.json`. That artifact closes
arithmetically:

```
198 calls − 108 with an original PDF = 90 without
  99 + 9  = 108 paired
  39 + 9 + 42 = 90 unpaired
  108 + 90 = 198 ✓
```

**The artifact says 90. G0's prose says 84.** The artifact's identity is exact, so
the prose is the error. `84/198 = 42.4%`, which is where the 42% in G0 came from —
a different pass wrote the prose than wrote the artifact.

`250.5 h` reproduces under no definition tested. It predates the duration merge,
which reclaimed 56.56 h of duplicate audio; adding that back moves it further away,
not closer.

**Neither figure is adopted, and neither is replaced by a substitute.** The reason
they cannot be reconciled numerically is structural: they were measured on a
**198-call** set, and the corpus is now **188 calls** after 18 documented merge
corrections. Two sets, two join methodologies. The reconciliation is that they are
**not comparable**, and the current measurements supersede both.

**Withdrawn from my own work as well:** the *"150 calls with an AI summary"* figure
from my scoping. It paired a call to any PDF in its folder on date or topic
overlap, sweeping in written material that is not a summary — a 3× overcount. The
artifact's own summary counts (51 files / 44 calls) also do not reproduce on the
current file set (70 named-summary PDFs), so those are recorded as a divergence
rather than adopted in either direction.

**What the vault uses**, under decision C (written hand only):
**37 of 188** calls carry a `docx`/`pptx`/`xlsx` written hand.
**151 carry none**, and each records *"No written half for this call."* This is a
third category the artifact never measured and is never presented as if it were
either the 90 or the 44.

### 9.2 "Five bonus courses" — RECONCILED

G0 named five folders; **eleven** carry video. Videos and hours agree **exactly**
with G0 and with an independent census.

| | videos | hours |
|---|---|---|
| the five G0 named | 28 | 23.46 |
| the six G0 omitted | 14 | 2.70 |
| **all measured** | **42** | **26.16** |

The six omitted: *Million Dollar Branding, Get Ready To Launch, 7-Figure Sales
Funnel, Converting Upsells, Revenue Generating Emails, Plug & Play High
Converting Sales Letter*. **Closed.**

### 9.3 Year-less calls — ALL CLOSED, by two different arguments

The folder-ordering inference was tested and **falsified** (correct on 32 of 34
dated folders, wrong on 2). It was rejected, not used.

The five `5. May` calls were then closed by **elimination**, each step checked:

1. Exactly **three** folder handles are named `5. May`.
2. Two carry dated calls inside them, dating them outright: `B2FEmJjC` → **2022**,
   `RyV0FDpI` → **2023**.
3. The corpus spans May in exactly **three** years — 2021 begins in June, 2025 ends
   in February (`Up to 02.2025`).
4. One folder, one year left → **`liVUnbAT` = May 2024**.

Seed ordering independently predicts 2024 and matched the other two May folders
**2/2** — corroboration, not the argument.

The sixth call, `FF.NHB Coffee Room Impromptu Call`, had four dated siblings in its
own folder, all 2024, and was resolved by a general rule: **a call whose filename
carries no date adopts its folder's year when the sibling years are a single
value.** The one cross-year folder found holds two years in one handle, which
makes siblings ambiguous and therefore refuses to resolve.

**Every one of the 188 calls now carries a year.** The 42 undated units remaining
are the bonus lesson videos, which correctly have no date.

---

## 10. Final scope, locked

```
AUDIO      230 units   583.55 h   146.39 GB
  calls 188 · bonus lessons 42
DOCUMENTS  109                     0.486 GB
  written_hand 37 · course_doc 36 · orphan_doc 36
TOTAL      339 targets            146.87 GB

STT $150.56 · peak disk 2.00 GB · 105 MP4 alternates never fetched
```

36 month folders across 2021–2025. Largest: `2025-02 February` (20),
`2025-01 January` (10), `2022-07 July` (9), `2024-08 August` (8).

---

## 11. Standing constraints on this vault

1. **Nothing is inferred into a field.** An absent date stays absent; an absent
   written half is recorded as absent. No placeholder, no estimate.
2. **Every count is reproducible.** Each figure here names the script and log
   that produced it.
3. **Divergences from G0 are recorded, not resolved by preference.** Where G0 and
   a current measurement disagree and no test settles it, both figures appear.
4. **Guards are part of the deliverable.** Colliding ids, duplicate handles,
   mis-paired documents, collapsed lessons, and unvalidated inferences each have an
   assertion that fails the build. **Eight** of them fired on real defects during
   scoping, including one that caught this script collapsing 42 lessons to 32.