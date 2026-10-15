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
│  └─ VAULT-STRUCTURE.md  SUBORDINATE to the spec; signed, superseded on C1-C3 — reviewed, unsigned
├─ evidence/probes/       50 dated evidence artifacts
├─ pipeline/
│  ├─ scripts/            sweep -> normalise -> scope -> reconcile
│  └─ out/                manifest-v3.json, scope-final.json, logs
└─ vault/                 build output. **NOTHING media-shaped ships.**
                              `attachments/` does NOT exist — see C1 below.
```

---

## 1. What this project is

Transcribe the **"Alen Sultanic — NHB+ — Nothing held back Plus (Up to 02.2025)"**
archive — a MEGA public share — into a **call-shaped vault**, without downloading
anything media-shaped to the operator's PC. **The finished vault does land on the
operator's PC — it is the deliverable.**

**What is already known, do not re-derive:** **193 calls** (574.53 h) and **42 bonus
lesson videos** (26.16 h) — **600.70 h** across 235 audio units. **344 fetch
targets.** The run fetches **153.81 GiB** of primary audio; the 100 MP4
alternates (165.29 GiB) are recorded and **never fetched**.

**`SPEND_HARD_STOP_USD = $213.48`**, derived and printed from the formula
rather than asserted:

```
(34,472.10 calls + 294.84 undated tail + 1,569.62 lessons) x $0.0056 = $203.48
+ $10.00 loss reserve                                                = $213.48
```

**That constant has carried four different values across this project's life**
— $207.31, $207.35, $207.68 and $203.48 — and the block that insisted it was
"DERIVED, not asserted" was itself the wrong one. If a figure here disagrees with
`stage-1/stage-1-spec.md`, the spec is right and this file is stale.

**37 calls carry a written-hand document; 156 carry none.** 36 course documents
have no call counterpart and 36 are orphans. **`Bonuses` is eleven
structured video courses**, 42 lesson videos. Every figure has a dated artifact in
`evidence/probes/`. Every figure has a dated artifact in `evidence/probes/`, and `pipeline/out/PLAN-TRUTH.json` recomputes the headline ones on every run.

**This file has carried stale figures for several rounds** because corrections landed in `stage-1-spec.md` and stopped there. An unmarked constant in this project has been a defect every time one was found: a forecast below the run it forecasts, a guard that never fires, a slack allowance that lets bad data through. **Every one was too permissive, none too strict.** Treat any number here as unverified until `PLAN-TRUTH.json` agrees.

> **This share is two different things.** A mentorship call archive *plus* an
> eleven-course curriculum. Different shapes, different registers, different costs.
> **The single-call mental model does not describe it.**

---

## 2. The arc

`INTENT → PLAN → BEADS → EXECUTE → HARDEN`, in that order. **G0 passed 2026-09-30. G1 (PLAN) PASSED 2026-10-15** — five blind refinement
rounds in fresh conversations, recorded in `stage-1/GATE-G1.md`. Beads are a
Stage 2 deliverable and do not exist yet.

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

**A remux IS required for the MP4 units, and it is not a transcode.** **[F31] The
old reason here was "the largest unit is 2.00 GB displayed — 1.5–2.5 GB actual,
sitting on the limit". That reasons from a SENTINEL: 2 GiB exactly is a MEGA
display value, not a measurement, and 77 of 235 units (32.8% of units, **75.4% of all bytes**)
carry them — recomputed on the full population, not carried forward. It is also no longer the real reason. The ceiling really is 2 GB, but the
largest remuxed unit ever actually submitted is 385 MiB — 19% of the cap. The reason
to remux is that the raw 1,539 MB MP4 path TIMED OUT and the remuxed .mka returned
HTTP 200 at 156.2 s against a 600 s ceiling.** `ffmpeg -vn -c:a copy` drops the video track
and copies the AAC stream bit for bit. No re-encode, no quality change, and STT cost
is unchanged because Deepgram bills audio minutes, not bytes. It also cuts upload
volume by roughly 85%. **[F31] The measured figure is 71.2% aggregate - MP4
~80%, MP3 NEGATIVE (-1.6%) - not 85%.** A proposal that *transcodes* is still wrong; a proposal that
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

21. **A test that proves something else is not a pass.** Twice in a single probe.
    A loopback mounted root-owned returned `EACCES`, which the verdict function
    accepted as cap behaviour because it only checked for a *hang*, not for the
    failure mode under test. A "real traffic" test used a 47 KB file against 16 MiB
    of free space, so it fitted and proved nothing. Ask: *is this the failure mode I
    was testing for?* A verdict that can only return PASS is not a verdict.

22. **An empty-vs-empty comparison returns TRUE.** A helper spliced ffmpeg options at
    a fixed command index, corrupting `-v error` into `-v -ac 1 error`; ffmpeg decoded
    **zero bytes**, and SHA-256 of nothing equalled SHA-256 of nothing, so the
    bit-exactness gate passed on a run that checked nothing. Any equality assertion
    needs a **floor**: assert bytes decoded > 0 before asserting the hashes match.

23. **ffmpeg option position decides whether it is an input or output option.**
    `-ac 1 -ar 16000` before `-i` is parsed as input options and fails *"Option
    sample_rate not found"*; after `-i` it works. Relatedly, `mkfs.ext4 -m 0` clears
    reserved **blocks**, not **ownership** — a loopback mount stays root-owned while
    the pipeline runs as the unprivileged user, so every write fails `EACCES`.

24. **`-v error` suppresses `astats`.** It writes at `info` level, so every reading
    silently returns `-inf` — indistinguishable from a silent input. Do not pass `-v
    error` to a filter whose only output is logging.

25. **`mega-get` names its output after the VERBATIM source file**, with the extension
    appended (`Vimeo gif thumbnail custom code.pdf`) — **not** the handle. A
    handle-prefixed existence check reports a fetch failure while the fetch succeeded.
    Fetch into an **empty per-handle directory** and take whatever single file lands.

26. **A gate placed downstream of an irreversible step reports a breach that already
    happened.** V6 asserts no media reaches the vault, but `scp` faithfully copied a
    planted `.mp3` — the transfer is a dumb pipe with no filter, and should be. V6
    must run on the **source tree, before the copy**. Ask where a gate sits relative
    to the first irreversible action, not just whether it exists.

27. **`git commit -m "…"` from PowerShell shreds any message containing quotes or
    parentheses.** It parses them as pathspecs. Write the message to a file and use
    `git commit -F`. Same class as trap 18: the shell is not a text tool.

28. **Container constraints are not codec constraints.** `ffmpeg -c:a copy` into
    `.m4a` fails rc=234 for every mp3 source, because `.m4a` is an MP4 container and
    cannot hold an MP3 elementary stream. Use `.mka`. The error reads like a codec
    fault and is not one.

29. **Duration from a container header is not duration.** An MP3 header claimed
    4,958 s where the decoded PCM was 5,431.8 s (**+9.54%**). When a vendor bills on
    processed audio, a header-derived cost gate is under-reserved by exactly the
    header's error, per part, silently. Derive cost from **decoded PCM bytes ÷ (rate ×
    channels × 2)**.


---

## BR IS RUN WITH `--no-db`. THE AUTHORITY DIRECTION INVERTED.

**Symptom, six times in one day:**
```
SYNC_CONFLICT: automatic WAL index recovery already failed for this exact
database family at stage private-recovery (I/O error: WAL-index quarantine is
not supported on this platform) ... retryable: false
```

**Cause.** `frankensqlite` 0.4.4's WAL-index recovery is unsupported on Windows.
Every mutation eventually wedges the DB; `br doctor` reports healthy and then the
next write fails. The parent project blames NTFS-through-9p `0777` sidecar modes;
this is native NTFS, so that is not it here.

**Remedy. Run `br` with `--no-db` on every command.** It works for reads AND
writes. Verified: `list`, `show`, `dep cycles`, `lint`, `ready`, `q`, `delete`.

**TWO RULES THAT FOLLOW, AND THE SECOND ONE BITS:**

1. **`--no-db` SKIPS AUTO-FLUSH.** After any `--no-db` write, the change is in
   the JSONL but not durable until something flushes. Verify the JSONL directly,
   do not assume the write took.
2. **NEVER run `br sync` while in `--no-db` mode.** `br sync --flush-only` hits
   the DB, fails, and then RE-CLOBBERS the JSONL with the DB's stale contents -
   undoing a `--no-db` delete that had already succeeded. A scratch bead came
   back from the dead this way and had to be removed twice.

**THE AUTHORITY DIRECTION INVERTED.** Normally the DB is authoritative and the
JSONL is derived, so editing the JSONL directly is lost. **In `--no-db` mode the
JSONL is authoritative and the DB is a broken cache** - so direct JSONL edits are
correct, and the DB must simply be left alone. Do not "recover" it. Do not run
the quarantine / `br init` / `br sync --import-only` sequence on this failure;
it has been run six times and failed six times.

**IF THE DB MUST BE REVIVED ANYWAY:** quarantine the family, `br init`,
`br sync --import-only`, and then **verify bead count, edge count and cycle count
immediately after import and BEFORE any further change.** That verification step
is what proves a recovery lost nothing, and it is missing from the parent
project's procedure. Also check the 12 tracked `.beads.vacuum.*.tmp-lock-*`
files survive a quarantine glob, and restore with `git checkout --` if not.
