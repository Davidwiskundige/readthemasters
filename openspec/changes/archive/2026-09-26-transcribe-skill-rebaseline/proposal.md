## Why

`transcribe-cost-rebaseline` re-measured the Claude Code transcription skill on the model it now runs
(Opus 5.5), with a meter that prices tokens the way the plan does, and ran four arms on the same
twelve Picard pages adjudicated against the scan. Three of the skill's current rules rest on the old
raw-volume measurements, and two defects surfaced that no pass catches:

- **Batch size 4 was a cost optimum that no longer exists.** Per transcription batch the turns are
  ~6 regardless of page count, and the fixed part is ~$0.11. A 12-page batch cost 10% less than
  three 4-page batches ($0.37 against $0.41 per page, transcription + verification) and was equal or
  better on every adjudicated reading — it alone of three arms caught the p. 332 `(n − 4)` misprint.
  A 28-page batch was cheaper still ($0.32) but adopted a wrong paragraph convention on its first
  page and held it for all 28 (8 wrong breaks on the compared pages against 1–2), and its verifier
  missed a misprint the others caught.
- **Effort is unstated.** `low` failed the kill criterion (five substantive errors `medium` did not
  make, three of them introduced by `low`'s own verifier). `medium` on Opus 5.5 made no misreadings
  where the Opus 5 `high` reference made two.
- **Paragraph breaks after displays are the most frequent error in every run, the reference
  included**, and no pass checks them: the verifiers compare readings, not paragraph structure. In
  this print a continuation after a display starts flush left and a new paragraph is indented; that
  is visible on the page and nowhere else.
- **The magnification cap can be reset by the caller.** `magnify.py` counts crops already in its
  `--out` directory, so a verifier took 7 regions on one page by writing to `vcrops2` and `vcrops3`.

## What Changes

- **Transcription batches of 12 pages**, or up to a chapter or part boundary within a few pages of
  that. The skill's "measured optimum 2–4, curve flat" rationale is replaced by the price-weighted
  numbers. The inline threshold for short works stays at its current absolute size (~8 pages)
  instead of scaling with the batch.
- **Verification batches stay at 4 pages, dispatched concurrently** — now stated as a deliberate
  decoupling from the transcription batch, for wall-clock, not inherited from it.
- **Effort `medium` is the recommended setting** for a run, stated in the skill with the evidence;
  `low` is named as measured and rejected. Provenance already records effort.
- **Verifiers check every paragraph break adjacent to a display against the scan**: flush-left
  continuation versus indented new paragraph, and report each one they change.
- **`magnify.py` enforces the cap per page and pass, independent of the output directory**, via a
  ledger kept beside the prepared pages.

Non-goals: crop targeting (the model's coordinates land 40–150px off; separate follow-up), a shipped
proofread checker (separate follow-up), image resolution (measured at 5–12% of cost; no change), the
Antigravity skill, and the two corpus corrections to Picard 1885 (separate corpus PR).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `transcription-pipeline`: the Tier-2 skill's default batch size and short-work threshold change;
  new requirements for the recommended effort, post-display paragraph verification, and a cap the
  caller cannot reset. The requirements `transcribe-turn-cost` modifies (*Verification pass*,
  *Capped per-page escalation*, *Prepared pages carry a coordinate mapping*) are left untouched here
  and extended by ADDED requirements, so the two changes do not collide.

## Impact

- **Modified**: `.claude/skills/transcribe/SKILL.md` — Phase 3 (batch size, rationale, threshold),
  Phase 5a (verifier prompt: paragraph check; decoupled batch size), a note on effort.
- **Modified**: `pipeline/magnify.py` and `pipeline/tests/test_magnify.py` — the ledger. Stdlib +
  Pillow, as now; `validate.py` and CI untouched.
- **Depends on**: `transcribe-turn-cost` landing first (this change edits text that change wrote).
- **Evidence**: `openspec/changes/transcribe-cost-rebaseline/measurements.md`.
