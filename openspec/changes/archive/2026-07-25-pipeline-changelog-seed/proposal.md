# Change: pipeline-changelog-seed

## Why

`provenance-changelog` made the revision history a curated `changelog` block, but nothing writes a
first entry — every new work starts with no history until a maintainer hand-writes one. That is
avoidable friction: the moment a transcription or translation is produced *is* the first revision.
Having the contributor paths seed a starter entry restores most of the "zero bookkeeping" the git
approach had, while keeping the changelog human-editable.

## What changes

- **All four contributor paths seed a starter `changelog` entry** when they write provenance:
  the Tier-2 skills (`/transcribe`, `/translate`) and the Tier-3 pipelines
  (`pipeline/transcribe.py`, `pipeline/translate.py`).
  - Transcription run → `{date: today, summary: "Transcription added (AI draft)."}`
  - Translation run → `{date: today, summary: "Translation (<lang>) added (AI draft)."}`
- **Idempotent**: the entry is appended only when an entry with the same summary is not already
  present, so re-running a step (or re-transcribing) does not duplicate it, and a translation run
  preserves the transcription's entry (and vice versa).
- A shared helper `validate.add_changelog_entry(provenance, summary, date=None)` implements the
  append-if-absent so the two pipelines share one behavior; the skills' `SKILL.md` instructions gain
  the matching starter block.
- The entry is a **starter**, not the last word: it is ordinary editable YAML, and a maintainer is
  expected to refine or extend it (corrections, status promotions) over the work's life.

## Impact

- Modifies **transcription-pipeline** and **translation-pipeline** ("Honest provenance and status"
  in each — the run now also seeds the changelog).
- Touches `pipeline/validate.py` (the helper), `pipeline/transcribe.py`, `pipeline/translate.py`,
  `.claude/skills/transcribe/SKILL.md`, `.claude/skills/translate/SKILL.md`, and extends
  `pipeline/tests/test_changelog.py`.
- No schema change — `corpus-format` already defines the optional `changelog` block.
