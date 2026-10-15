# Round 3 — Repo-grounded review

Run against a stale snapshot and **re-verified against the working tree before
reporting**. R3 opened the spec at 65,380 bytes / `82ced3c` and found it at
73,097 bytes / `b1a84e4` with three commits landing mid-read — a concurrent
build. Every finding below was re-checked against the tree as it stood, and
several were closed by that build rather than re-reported.

41 findings: **15 blocking, 21 non-blocking, 5 cosmetic.** Verdict: **NO — not
executable as written**, on the grounds that the money gate stated a derivation
producing `$196.68` and a table summing to `$207.35` while asserting `$207.68`.

## Triage outcome

Every finding was triaged per-finding against the current spec before anything
was applied. Nine were already fixed by the concurrent build and are recorded
here rather than re-applied.

| | |
|---|---|
| applied — blocking | F1–F15, plus B16 and B19 from round 2 |
| applied — non-blocking | F16–F28, F30–F36, F39, F40 |
| applied — cosmetic | F37, F38, F41 |
| already fixed by build | F23, F24 landed alongside F1 |
| superseded on re-measurement | F15's counts — two normalisers, same shape, **both agree max group is 3** |

## What round 2 could not find

Round 2's framing was "what round 1 missed", and its 12 blocking findings were
all **prose-internal** — a section contradicting another section. What lives
outside the spec's prose, in the code and artifacts it cites, was structurally
out of its reach. Five of those, in brief:

1. The worst-case probe ran on the wrong unit, and **three artifacts joined two
   different files** — the 275.9 min belongs to `wiUyTRZb`, the 1,614,043,424
   bytes to `dvcEDToK`, which ranks **47th of 229**.
2. `V9` matched `kind == "call"`, and `scope-final.json`'s kinds are
   `audio`/`written_hand`/`course_doc`/`orphan_doc` — **0 handles matched**, so
   the gate meant to catch the dropped call passed vacuously on it.
3. `check-frontmatter.py` returned **PASS on a note carrying `duration: 3h
   14m`**, the exact format §10.1 forbids. It checked names, not domains.
4. §10.2's repair instruction pointed at the wrong file — `design-names.py`
   already accepted ISO dates; `normalize.py`'s regex is what feeds `u["date"]`.
5. §10.3's central premise was false: the topic axis does **not** cluster.

## The three findings that mattered most

**F2 — the money arithmetic did not produce its own hard stop.**
`(35,013.1 + 286.9) × $0.0056` is **$197.68**, not the `$196.68` displayed, and
the table four lines below summed to **$207.35**. Three figures, one code block,
and the total did not follow from the line above it. This was introduced by the
build, not inherited.

**F5 — `SETTLE_FROM`'s channel source was undefined and the two readings differ
by $26.98.** Read from the pre-downmix part, every downmixed unit settles at 2×
and double-counts the saving into the ledger; read from the submitted part, only
the keep-stereo branch does. The spec chose neither.

**F15 — §10.3 gated a structure that does not exist.** The claim was "~50 groups
of 1–13"; measured, it is 225 groups, 221 singletons, **max 3**. The two
strip rules it specified matched **0 of 230 topics**.

## Residual risks carried forward, ranked by damage-if-wrong

1. The corpus-wide **stereo share is unknown** — 3 of 230 measured, and the
   keep-stereo branch that prices it fired 0 of 3 times. Priced in §2.2's
   keep-stereo line, absorbed nowhere else.
2. `INPUT_CHANNEL_COUNT`'s source part is now specified, but the value is
   *recorded at remux time and consumed at settle time*, with the downmix
   decision falling between them.
3. **Manifest durations are container headers for 228 of 230 units**,
   decoded-verified on 10. `pjFQiLQQ` is +9.54% off.
4. `WPM_MIN/WPM_MAX` and `SEGMENT_SEC` are **PROVISIONAL with no measurement**,
   and `SEGMENT_SEC` is dead code under a 2 GB `CAP_BYTES` the 385 MiB maximum
   cannot reach.
5. `metadata.duration` semantics for stereo were measured on 120-second
   synthetic clips only. `pjFQiLQQ` has never been submitted.
6. **Azure VM-days are unpriced.** §0's second waiver rests on an idle-rate
   figure; no artifact prices a 16-way concurrent run over 583.55 h.
7. `LOSS_ALLOWANCE_USD`'s 5% failure rate is a guess; recomputed it is $9.89
   against a $10.00 allowance.

## Corrections to this review

Two of its own claims did not survive checking, and both were corrected rather
than applied:

- **`A2dWSZAK` is the 50-second unit.** R3 asserted `A2dWSZAK` was 50 s; a
  direct lookup initially appeared to contradict it (`dur_s` read as `None`).
  The field is `media.dur_s`, not `dur_s`. R3 was right; the lookup was wrong.
- **F15's group counts differ between normalisers** — 212 stems / 199
  singletons here, 225 groups / 221 singletons in the spec. Different strip
  rules, same shape. Both agree the premise is false and the max is 3. **The
  spec records both counts rather than silently picking one.**