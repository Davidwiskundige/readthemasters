# Delta: transcription-pipeline — seed a starter changelog entry

## MODIFIED Requirements

### Requirement: Honest provenance and status

Machine output MUST be recorded as `status: ai-draft` with `model`, `effort`, `prompt_version`
(matching the prompt actually followed), `submitted_via: skill`, and the `produced` date. A higher status on
the ladder (`skimmed`, `verified`) is set only when a human has performed that level of review, with
a `reviewers:` entry naming them.

A transcription run SHALL also seed a starter `changelog` entry in `provenance.yaml` —
`{date: today, summary: "Transcription added (AI draft)."}` — appended only when no entry with that
summary already exists, so re-running does not duplicate it and any existing changelog entries are
preserved. Both the Tier-2 skill and the Tier-3 pipeline seed it; the entry is a starting point the
maintainer may edit.

#### Scenario: A first transcription seeds the changelog

- **WHEN** a transcription run writes `provenance.yaml` for a work that has no changelog
- **THEN** the provenance gains a `changelog` with an entry dated today summarizing that the
  transcription was added

#### Scenario: Re-running does not duplicate the entry

- **WHEN** a transcription run writes provenance that already contains the starter transcription
  entry
- **THEN** no duplicate entry is added, and existing changelog entries are preserved
