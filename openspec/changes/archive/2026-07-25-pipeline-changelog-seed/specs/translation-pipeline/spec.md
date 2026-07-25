# Delta: translation-pipeline — seed a starter changelog entry

## MODIFIED Requirements

### Requirement: Honest provenance and status

The run MUST record, under `translations.<lang>`, `status: ai-draft` with `model`, `effort`,
`prompt_version` (matching `prompts/translate-chat.md`), `submitted_via` (`skill` or `pipeline`),
`source: transcription`, the `produced` date, and (Tier-3) the `batch_ids`. It preserves the
`transcription:` block and other languages. A higher status on the ladder is set only by a human
reviewer, with a `reviewers:` entry.

The run SHALL also seed a starter `changelog` entry in `provenance.yaml` —
`{date: today, summary: "Translation (<lang>) added (AI draft)."}` — appended only when no entry
with that summary already exists, so it does not duplicate on re-runs and preserves the
transcription's entry and other languages' entries. Both the Tier-2 skill and the Tier-3 pipeline
seed it; the entry is a starting point the maintainer may edit.

#### Scenario: Adding a translation seeds a changelog entry

- **WHEN** a translation run writes `translations.<lang>` into a work whose changelog already has
  the transcription entry
- **THEN** the provenance gains a further `changelog` entry dated today summarizing that the
  `<lang>` translation was added, and the transcription entry is preserved

#### Scenario: Re-running a translation does not duplicate the entry

- **WHEN** a translation run writes provenance that already contains that language's starter entry
- **THEN** no duplicate entry is added
