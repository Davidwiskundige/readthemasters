# Tasks: pipeline-changelog-seed

## Shared helper

- [x] `pipeline/validate.py`: add `add_changelog_entry(provenance, summary, date=None)` — append
      `{date, summary}` (date defaults to today) only if no existing entry has that summary; keep
      `changelog` as the first key for readability; return the provenance dict.

## Pipelines (Tier-3)

- [x] `pipeline/transcribe.py`: after writing the `transcription` block, seed
      `"Transcription added (AI draft)."`.
- [x] `pipeline/translate.py`: after writing `translations.<lang>`, seed
      `"Translation (<lang>) added (AI draft)."`.

## Skills (Tier-2)

- [x] `.claude/skills/transcribe/SKILL.md`: add the starter `changelog` block to the Phase-6
      provenance example and instruct appending it (append-if-absent).
- [x] `.claude/skills/translate/SKILL.md`: same, with the translation summary; preserve any existing
      changelog entries.

## Tests

- [x] Extend `pipeline/tests/test_changelog.py`: `add_changelog_entry` appends, is idempotent by
      summary, defaults the date, and orders `changelog` first.

## Ship

- [x] Fold the deltas into `openspec/specs/transcription-pipeline` + `translation-pipeline`; update
      `project.md`; archive the change.
