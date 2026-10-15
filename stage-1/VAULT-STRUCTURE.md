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

Every filename below is a **real MEGA filename**, taken from `manifest-v3.json`, not
an invention. The date is whatever the archiver wrote — `03-07-2024` in some years,
`2024-03-07` in others.

```
nhbplus-vault/
├─ 00 Home.md                        index, totals, entry points
├─ calls/
│  ├─ 2021/
│  │  └─ 06 June/
│  │     └─ 6-7-2021 - How To Sell & Close High Ticket.md
│  ├─ 2022/
│  │  ├─ 10 October/
│  │  │  ├─ 10-6-2022 FF_NHB+ Training Call - Bible Offer + Recurring Membership Models.md
│  │  │  ├─ 10-13-2022 FF_NHB+ Training Call - Web Hosting Offers + 5 Step Sales Process.md
│  │  │  └─ 10-27-2022 FF NHB+ Training Call - The What and the Who.md
│  │  └─ 12 December/
│  │     └─ 12-1-2022 NHB+ Theory Call - Authority Handover_watermarked.md
│  ├─ 2023/
│  ├─ 2024/
│  │  ├─ 03 March/
│  │  │  ├─ 03-07-2024 NHB+ Theory Call - Converting Audiences.md
│  │  │  ├─ 03-14-2024 NHB+ Theory Call - Market Assumptions 2.0 (Counter Arguments).md
│  │  │  └─ 03-28-2024 NHB+ Theory Call - Lowering Argumentative Resistance.md
│  │  └─ 08 August/
│  │     ├─ 08-01-2024 NHB+ Theory Call - Reading Offers 3.md
│  │     ├─ 08-05-2024 Guest Call - Lonnie Jones on SEO.md
│  │     └─ 08-12-2024 Guest Call - Luke Jaten on Direct Mail Secrets.md
│  └─ 2025/
│     └─ 02 February/                20 calls — the largest month
│        └─ 02-04-2025 NHB+ Coaching Call - Offer Fundamentals - With Kevin Sheerin.md
├─ written-hands/
│  ├─ 2023/
│  │  └─ 10 October/
│  │     └─ 01. NHB+ Selling To Women 2.md
│  └─ 2024/
│     └─ 03 March/
│        └─ NHB+ Converting Audiences.md
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

### 2.1 Ordering inside a folder — a known and accepted wart

**The MEGA filename sorts by day-within-month, not chronologically.** Every file in
`calls/2024/03 March/` starts `03-`, so lexical order is correct there — but a bare
lexical sort across the whole corpus puts `03-07-2024` before `11-02-2023`.

This is **deliberate**. It buys filename ↔ source-file equality, which is worth more
than a sort that the folder partition already provides. Month folders make
chronological order correct *by construction*; the index pages in §6 are the
chronological view.

The alternative — rewriting every name to `YYYY-MM-DD …` — was rejected. It would
have been one line of code and it would have broken the property that a reader can
hold the vault filename and the MEGA filename side by side and see they are the same
artefact.

---

## 3. Filename rules

| Kind | Rule | Real example |
|---|---|---|
| Call | the MEGA filename, verbatim | `03-07-2024 NHB+ Theory Call - Converting Audiences.md` |
| Course lesson | `NN Title.md`, zero-padded | `03 The Psychology Of Business Models.md` |
| Course index | `00 <Course>.md` | `00 7-Day Fast Start.md` |

Characters stripped from any filename: `< > : " / \ | ? *` and control characters.
**At least one real name needs it** — `02-03-2025 - NHB Coaching Call - Google Case
Studies - With Charles Kirkland` is fine, but the corpus does contain `Reading Offers
#3` and `Relationship_Trust Cycles`, so the strip is a guard against a name that has
not been seen yet, not a routine transform.

**The date prefix is NOT normalised.** Some years are `03-07-2024`, some are
`6-7-2021`, some are `2024-03-07`. Rewriting them to one form would make the vault
tidier and would break filename equality with the source. §2.1 explains why that
trade is not worth making.

---

## 4. Frontmatter — five fields

The frontmatter is for **finding and sorting notes**, not for recording how the note
was made. Every field below answers a question you would ask in Obsidian's search
box. Nothing else earns a field.

```yaml
---
title: 03-07-2024 NHB+ Theory Call - Converting Audiences
date: 2024-03-07
type: theory
duration: 3h 14m
speakers: 22
---
```

| Field | Why it is here |
|---|---|
| `title` | The verbatim MEGA filename. Also the H1 and the note filename |
| `date` | Parsed to ISO so date queries work. The title keeps the archiver's own format |
| `type` | `theory` · `guest` · `coaching` · `training` · `other` — the filter you would actually use |
| `duration` | The one number you want before committing to a three-hour read |
| `speakers` | Ditto. A call with 22 speakers is not a call with 3 |

**No source block.** No MEGA handle, no URL, no byte counts. **No transcription
block.** No word counts, no utterance counts, no model name, no request ID. **No
integrity block.** No cross-check verdicts, no timestamps. **No provenance
section.**

That information is not discarded — it moves to `_meta/manifest.json` (§6), which is
a machine-readable record, not something anyone reads by opening a note. The
distinction is deliberate: **a note is for a person; the manifest is for the audit.**

Nothing here is typed by hand. All five fields come from `manifest-v3.json` and the
transcription receipt.

---

## 4a. Written-hand notes

The extracted document is **its own file**, not a section inside the call note. A
three-hour transcript with eighteen thousand characters of written material appended
to it is two documents pretending to be one.

### The written-hand note

```markdown
---
title: NHB+ Converting Audiences
kind: written-hand
date: 2024-03-07
source_call: 03-07-2024 NHB+ Theory Call - Converting Audiences
---

# NHB+ Converting Audiences

<!-- the extracted document text, headings preserved from the source -->
```

Extraction is `zipfile` + `ElementTree` on the OOXML container — Python standard
library only, no converter and no office install. A `.docx` that turns out not to be
OOXML is reported as such, never as empty text.

`kind` distinguishes the four note shapes in the vault: `call`, `lesson`,
`written-hand`, `document`. Every note says what it is from its first line.

### The link, both ways

```markdown
<!-- in the call note -->
## Written hand

[[NHB+ Converting Audiences]]
```

```markdown
<!-- at the top of the written-hand note -->
Part of [[03-07-2024 NHB+ Theory Call - Converting Audiences]]
```

**151 calls have no written hand.** They get the recorded absence in place of a link,
because silence would read as an oversight:

```markdown
## Written hand

> No written half for this call.
```

Written hands are partitioned `written-hands/<year>/<MM Month>/`, mirroring `calls/`,
so a document is where you would look for it given the date of its call.

---

## 5. The call note

```markdown
---
(frontmatter above)
---

# 03-07-2024 NHB+ Theory Call - Converting Audiences

**3h 14m · 22 speakers**

## Transcript

[00:02] **Speaker 0** — <first utterance>

[12:41] **Speaker 3** — <next utterance>

<one block per utterance, in timestamp order, speaker-labelled>

## Written hand

[[NHB+ Converting Audiences]]
```

That is the entire note. Five frontmatter fields, a heading, the transcript, and one
link.

**Every utterance appears.** A transcript is not a summary and not a highlight reel.
The speaker labels are Deepgram diarisation indices — stable within this call,
meaningless across calls, and `Speaker 3` stays `Speaker 3`. The operator is not
identified in these transcripts and this build does not attempt to identify anyone.

---

## 6. Index pages and _meta

### Index pages — generated, none hand-maintained

| File | Content |
|---|---|
| `00 Home.md` | totals, year links, links to Courses and Library |
| `calls/YYYY/00 YYYY.md` | that year's calls by month, with counts and hours |
| `calls/YYYY/MM Month/00 MM Month.md` | that month's calls, in date order |
| `courses/00 Courses.md` | all 11 courses, videos, hours |

Month folders hold a small number of calls — **2025-02 holds 20** — so a month index
earns its place. Year folders hold at most 12 months, so a year index does too.
Anything coarser does not.

### _meta — the machine-readable record

Everything cut from the frontmatter lives here, because it has to survive being cut
and it has to be checkable by something other than a person reading a note.

| File | Content |
|---|---|
| `_meta/manifest.json` | one record per target: MEGA handle, URL, bytes expected and actual, STT request ID, SHA-256, cross-check verdicts, spend to date |
| `_meta/receipts/` | the per-unit receipt as written at run time |
| `_meta/scope-final.json` | the locked 339-target scope this vault was built from |
| `_meta/provenance.md` | how every number in the vault was obtained, and what was superseded |

**This is the split.** A note answers *"what was said on 3 July 2024"*. The manifest
answers *"can I prove where this came from and that nothing was truncated"*. Different
questions, different formats, different audiences — and the second one is not worth
taxing the first for.

---

## 7. Linking rules

- **A call links to its written hand, and the written hand links back to its call.**
  This is the only bidirectional link in the vault, and it is bidirectional because
  both notes genuinely need each other.
- A call links to its course material **only where the corpus says so** — where a
  lesson's name or the call's topic genuinely matches. No speculative links.
- A course index links to its lessons in order.
- `library/` documents link **up** to nothing. They have no call counterpart, and
  inventing a relationship would be a fabrication.
- Every call links to its month index. That is the only other backlink.

---

## 8. What this shape deliberately does not do

- **No speaker identity.** Deepgram diarises; it does not identify. `Speaker 3`
  stays `Speaker 3`.
- **No cross-call speaker graph.** It would require name matching across 188 calls,
  and a false merge there corrupts everything downstream.
- **No AI summaries.** 150 calls have one; operator decision excluded them. Adding
  them later is additive and needs no migration.
- **No transcript → article generation.** That belongs to Content OS, a separate
  build.
- **No timestamps invented.** A duration the source did not carry is recorded as
  absent. All 188 calls now carry a year.
- **No frontmatter that describes how the note was made.** Source handles, STT
  request IDs, byte counts and cross-check verdicts live in `_meta/`, not in a note
  someone is trying to read. §4.

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
2. **A note is for reading; the manifest is for auditing.** Frontmatter carries only
   what helps you find and sort. Everything about how a note was produced lives in
   `_meta/`. Cutting it from the note does not discard it.
3. **Every count is reproducible.** Each figure here names the script and log that
   produced it — *the* script, not *a* script. Where a figure was superseded, the
   current number appears and the withdrawal lives in §9 and in the evidence
   artifacts.
4. **Divergences from G0 are recorded, not resolved by preference.** Where G0 and a
   current measurement disagree and no test settles it, both figures appear.
5. **Guards are part of the deliverable.** Colliding ids, duplicate handles,
   mis-paired documents, collapsed lessons, and unvalidated inferences each have an
   assertion that fails the build. **Eight** of them fired on real defects during
   scoping, including one that caught the merge collapsing 42 bonus lessons to 32.