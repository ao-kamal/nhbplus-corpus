# AGENTS.md — NHB+ corpus extraction

One file, every agent type reads it. Read it fully before touching anything.

---

## 0. This is its own repository

```
Kamal/
├─ Content OS/          the CUT30 extraction — a DIFFERENT build, different corpus
└─ nhbplus-corpus/      this build
```

**Separate git repository, operator decision 2026-10-15.** Nothing here is tracked
in the Content OS repo and nothing there is tracked here. The two builds share no
code, no artifacts and no architecture. Do not reach across. If a future stage ever
feeds these transcripts into Content OS, that is an edge to draw explicitly.

The parent project's rules are inherited wholesale (`Content OS/AGENTS.md`) but its
corpus, its beads and its build output have **no bearing on this work**. The
`.beads/` graph there tracks the finished CUT30 extraction. **There are no beads
for this build, and none until Stage 2.**

```
nhbplus-corpus/
├─ AGENTS.md              this file
├─ CLAUDE.md              imports this file
├─ stage-0/
│  └─ stage-0-intent.md   INTENT (G0) — PASSED 2026-10-15
├─ stage-1/
│  └─ VAULT-STRUCTURE.md  the vault shape — reviewed, unsigned
├─ evidence/probes/       28 dated evidence artifacts
├─ pipeline/
│  ├─ scripts/            sweep -> normalise -> scope -> reconcile
│  └─ out/                manifest-v3.json, scope-final.json, logs
└─ vault/                 build output; attachments are committed
```

---

## 1. What this project is

Transcribe the **"Alen Sultanic — NHB+ — Nothing held back Plus (Up to 02.2025)"**
archive — a MEGA public share — into a **call-shaped vault**, without downloading
anything media-shaped to the operator's PC. **The finished vault does land on the
operator's PC — it is the deliverable.**

**What is already known, do not re-derive:** **188 calls** (557.39 h) and **42 bonus
lesson videos** (26.16 h) — **583.55 h** across 230 audio units. **339 fetch
targets, 146.87 GB, $150.56 STT forecast.** 37 calls carry a written-hand document;
151 carry none. 36 documents have no call counterpart. **`Bonuses` is eleven
structured video courses**, 42 lesson videos. Every figure has a dated artifact in
`evidence/probes/`.

> **This share is two different things.** A mentorship call archive *plus* an
> eleven-course curriculum. Different shapes, different registers, different costs.
> **The single-call mental model does not describe it.**

---

## 2. The arc

`INTENT → PLAN → BEADS → EXECUTE → HARDEN`, in that order. **G0 passed 2026-10-15**,
so Stage 1 (PLAN) is open. The skill's G1 gate requires **≥4 refinement rounds in
fresh conversations** before beads exist — a plan that has not cleared that gate is
not a plan.

**No beads exist in this repository, and none until Stage 2.**

---

## 3. The three rules that outrank everything here

**Rule 1 — remove nothing.** No capability is descoped. Where a route to one is
blocked, the route changes; the capability does not.

**Rule 2 — pay nothing.** No paid tier, no metered API, **and no vendor's free
credit tier either.** *Sole recorded exception:* Deepgram, the metered STT call.
The operator has confirmed credits and instructed that the point not be raised
again. **Confirming credits did not remove the spend ceiling** — the run still
stops at the forecast, and forecast and actual stay separate in every report.

**The rule carrying both: no claim about what a platform permits is believed until a
live probe proves it, with a dated evidence artifact.** Five platform priors were
wrong on five of five platforms against the operator's own live probes. A prior is
not evidence. *Probe before you build.*

---

## 4. Constraints specific to this build

**Nothing lands on the operator's PC.** Not audio, not video, not an intermediate.
This is the constraint that selects every route. It is not a preference to work
around. Also: no local ffmpeg, nothing heavy running locally.

**Deepgram accepts MP4 containers** — proven, not assumed (WAV and MP4 returned
identical 7 utterances / 1 paragraph / 62 words).

**A remux IS required for the MP4 units, and it is not a transcode.** Deepgram's
documented file-size ceiling is **2 GB** and the largest unit is 2.00 GB displayed —
1.5–2.5 GB actual, sitting on the limit. `ffmpeg -vn -c:a copy` drops the video track
and copies the AAC stream bit for bit. No re-encode, no quality change, and STT cost
is unchanged because Deepgram bills audio minutes, not bytes. It also cuts upload
volume by roughly 85%. A proposal that *transcodes* is still wrong; a proposal that
remuxes is required.

**Per-file retrieval works, and it is what makes the build viable.** The URL form is
`https://mega.nz/folder/<PH>#<KEY>/file/<HANDLE>`, where the handle is the grid row's
`id` attribute. Fetching one file at a time drops **peak disk from 320 GB to 2.00 GB**.
The `::` subpath syntax is not the mechanism. Eight routes were tested and are dead —
`::` subpaths, `mega-cd`, `mega-cat`, WebDAV, account import, `mega-fuse`, and the
MEGA API via mega.py/rclone. Full list with evidence in
`nhbplus-perfile-fetch-solved-2026-10-15.json`. Do not re-propose them.

**GitHub Actions remains dead**, but for one reason rather than four: a 14 GB runner
disk against a 2.00 GB peak is no longer disqualifying. It stays dead on
`libfuse2t64` availability and native-binary execution, not on capacity.

**The compute box is a throwaway remote Linux VM.** Everything runs there. Nothing
long-lived. Current: Azure `Standard_D2s_v5`, Austria East, 500 GB disk.

---

## 5. The traps — these are real incidents, not hypotheticals

1. **`timeout` does not stop a megacmd fetch.** A probe bounded by `timeout 45` kept
   running server-side and silently pulled **4.0 GB**. The 320 GB disaster was
   avoided by noticing, not by design. **The runner must assert on disk after every
   file and hard-stop on a threshold.** Process timeouts are not a control here.

2. **Never glob the output directory to build the work list.** A glob that matches
   its own output re-bills the corpus — the vendor bills per request. Targets come
   from the manifest.

3. **Receipts key on stable call identity, never on a MEGA URL or expiring token.**
   A retried job must skip completed calls, or the retry re-bills.

4. **A zero that evaluates nothing is a failure, not a result.** Seven probe bugs
   produced plausible-looking wrong numbers; two produced clean zeros that would have
   shipped a confident wrong answer.

5. **MEGA is an SPA.** `goto` to a URL already loaded does not repaint — `reload()`
   is required. And `.file-name` also matches MEGA's own chrome placeholders, so a
   naive `waitFor('.file-name')` succeeds *before* the real list paints. Folder
   handles live in the left nav tree: `<li id="treeli_<HANDLE>">`.

6. **The grid renders some files as two DOM nodes.** Raw row counts overstated the
   PDF population by exactly 2×. Deduplicate before reporting any count.

7. **Two enumeration defects pointed in opposite directions** — a folder-level
   MP4-only classification *undercounted* by 64 h, a weak filename normaliser
   *overcounted* by 21%. Their near-cancellation is why the intermediate figure
   looked plausible. Both were caught by reconciling a total against an independent
   bound, not by reading code. **Reconcile against something that cannot move.**

8. **MEGA rounds every displayed file size to a whole unit.** 100% of 156 GB-valued
   files are whole numbers, and 100% of 229 MB-valued files are too. Folder and year
   figures are EXACT and additive; per-file figures are NOT. Never reconcile a sum of
   per-file sizes against a folder figure - you will conclude MEGA is wrong, and be
   wrong yourself.

9. **A row id is the node handle.** Grid rows are `<TR id="HANDLE">` /
   `<A id="HANDLE">`; the nav tree is `<li id="treeli_<HANDLE>">`. A route declared
   "blocked" for want of handles was blocked for want of *the right selector*. Before
   calling anything unobtainable, re-read the DOM you are already printing.

10. **Tiles view and list view carry different fields.** Tiles set `title` =
   resolution + codecs + **exact size** + name, and render duration. List renders
   duration and leaves `title` **empty**. **Neither carries both.** A size probe
   reading the rendered column gets null; the same probe reading the attribute gets
   null in a folder MEGA rendered as a list. Force the view to get both.

11. **`Select-Object -First N` kills an upstream PowerShell pipeline.** It truncated
    a probe driver mid-script, before it wrote its output — the run *looked* like it
    had produced results. Capture to a variable, truncate after. See also trap 20.

---

## 6. Definition of done

A unit of work is done when its own stated gate passes **and the evidence is in the
output** — a test result, a check verdict, a count. Not an assertion that it is done.

If a gate cannot be satisfied, say so explicitly and leave the work open with the
reason recorded. **An honest blocker is a success. Work closed on a hopeful
assertion is a failure that costs a day.**

Never invent a number, a threshold, a path, or a credential. If the source material
does not carry a fact you need, that is a gap in the source — report it, do not fill
it with a plausible guess.

---

## 7. Secrets

`DEEPGRAM_API_KEY` lives in `C:\Users\layiw\.env.private` — read at use time, never
committed. **Never write a credential, token, or personal detail into a file, a
document, or a commit message in this repository.**

---

## 8. Current state — read this, it changes

- **G0 PASSED** 2026-10-15, operator sign-off on §1–§7.
  `stage-0/stage-0-intent.md` is the anchor.
- **Stage 1 is open.** One artifact exists and has been reviewed:
  `stage-1/VAULT-STRUCTURE.md`. The five scope decisions are locked in
  `pipeline/out/scope-final.json`. **The G1 gate is not met** — the skill
  requires ≥4 refinement rounds in fresh conversations before beads.
- **The corpus is fully enumerated and normalised.** 59 of 59 folder handles walked,
  0 failed, 709 rows, 654 files. Every count is reproducible from
  `pipeline/scripts/` with a matching log under `pipeline/out/`.
- **The chain is proven end to end on real compute**, not designed. Per-file fetch,
  remux, Deepgram EU, receipt, delete.
- **Eight assertions** guard the scope and the manifest. Each fired on a real defect
  during scoping, including one that caught the merge collapsing 42 bonus lessons
  into 32. Treat a tripwire failure as a stop, not a threshold to relax.

12. **Read the reference before running the command, not after it fails.** This has
    cost hours repeatedly, in five separate tools: `mega-cmd` usage syntax, the
    argument order of `mega-fuse-add` (it is `<LOCAL> <REMOTE>`, not the reverse),
    an `az vm list-skus` query with no `--size`, and two of my own regexes. Each one
    I guessed, ran, and diagnosed from the error. `--help` costs one second and
    answers all of them. The tell is writing a command whose syntax I am guessing
    at: stop, read the help, then run it.

13. **A presence check needs a FLOOR tied to what should have happened, not just a
    ceiling.** Three checks in one session reported success on empty results:
    `COUNT -le 3 && TOTAL < 5MB` passed on `0, 0`; `D > 0 && D < 1GB` passed on a
    12,288-byte metadata write for a 4.36 GB file. Ask "did I get roughly what I
    asked for?" (`pulled >= 0.5 * reported_size`), not only "is this number small?"

14. **Before changing someone's account, running their card, or writing to their
    drive: ask.** The Azure hypothesis test required importing 320 GB into a personal
    MEGA account. It cost ~40 minutes of recovery, wedged a client, and broke the
    operator's cloud sync. The test was worth running; taking the action without
    asking was not a judgement call to make. When a hypothesis needs someone's
    resources, that is a one-line question, not a decision.

15. **`curl --data-binary @file` reads the whole body into memory** and reports a
    misleading `option --data-binary: out of memory` on a large file. Stream from a
    Python file handle instead. `--data-binary @-` does **not** fix it.

16. **Windows pipes send CRLF.** A key read with `IFS= read -r` arrives one
    character long, which silently breaks an `Authorization` header in a way that
    points nowhere near the cause. Strip `\r` and print the length.

17. **`systemctl is-active` is not a health check for `mega-cmd-server`.** It is not
    a systemd unit on Ubuntu 24.04, so it reports `inactive` for a process that is
    running. `ps` shows it. A real fetch is the only arbiter — a *false negative*
    reading as "the server is down" sends you debugging a server that is up.

18. **Never pipe a file through PowerShell to rewrite it.** `Get-Content -Raw |
    Set-Content -Encoding utf8` and a `python -c @"…"@` heredoc both corrupt
    non-ASCII — the same defect that mangled the MEGA capture. Write the script to
    a file with the write tool, then run it.

19. **An encoding "fix" needs a positive test, not a character-class filter.** A
    repair pass using an allow-list of expected characters silently overwrote
    legitimate typography (`→ × § ≥ ± ≈ ✓`) with em-dashes across three documents.
    **U+FFFD is the only corruption signal.** Before running any repair, list what it
    would change and read the list.

20. **`Select-Object -First N` truncates an upstream pipeline**, and so does any
    early-exit consumer. Capture to a variable, then slice — the process writing the
    output gets killed mid-run and the file looks complete.
