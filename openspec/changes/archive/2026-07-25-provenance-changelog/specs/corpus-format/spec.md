# Delta: corpus-format — provenance changelog block

## MODIFIED Requirements

### Requirement: provenance.yaml schema

`provenance.yaml` SHALL carry keys `transcription` and `translations.<lang>`, each an artifact
record: `status` (`ai-draft|skimmed|verified`), `model` (required), `effort` (optional,
provider-agnostic or null), `prompt_version` (required), optional `submitted_via`, `produced`,
`reviewers` (list of `{name, level, date}`), and for translations a `source` (`transcription` |
`external-open` + `license`).

`provenance.yaml` MAY also carry an optional top-level `changelog`: a list of `{date, summary}`
entries recording how the work has changed over time (the source of the work page's revision
history). `date` is an ISO calendar date (`YYYY-MM-DD`); `summary` is a short non-empty free-text
line. The block is optional and human-authored; when present, `pipeline/validate.py` checks that it
is a list and that every entry has an ISO `date` and a non-empty `summary`.

#### Scenario: A valid changelog passes the gate

- **WHEN** a `provenance.yaml` has a `changelog` list whose every entry has an ISO `date` and a
  non-empty `summary`
- **THEN** validation accepts it

#### Scenario: A malformed changelog entry fails the gate

- **WHEN** a `changelog` entry is missing its `summary`, or its `date` is not an ISO calendar date
- **THEN** validation reports an error for that work
