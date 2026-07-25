# Delta: site-catalog — revision history from the changelog

## MODIFIED Requirements

### Requirement: Revision history

Each work page SHALL show a revision history of the work, sourced from the optional `changelog`
block in the work's `provenance.yaml` — a curated, human-authored list rather than anything derived
from git.

`pipeline/build_site_data.py` emits each work's `changelog` into `works.json` as a list of
`{date, summary}` entries ordered newest first. The work page renders it as a single collapsed
`<details>` "Revision history" section near the "Report an error" link, whole-work in scope, one row
per entry (date + summary). A work with no `changelog` shows no revision-history section — the build
never fails for its absence.

#### Scenario: Changelog rendered newest first

- **WHEN** a work's `provenance.yaml` has a `changelog` with several dated entries
- **THEN** the work page shows a collapsed "Revision history" section listing them newest first,
  each as a date and its summary

#### Scenario: No changelog, no section

- **WHEN** a work has no `changelog` block
- **THEN** the work page omits the revision-history section entirely
