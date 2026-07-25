# Delta: site-catalog — revision history

## ADDED Requirements

### Requirement: Revision history on work pages

Each work page SHALL show a revision history of the work, derived at build time from git. No
revision data is stored in `work.yaml` — the history is computed, not declared.

`pipeline/build_site_data.py` SHALL emit a per-work `history` list into `works.json`, derived from
`git log` scoped to the work's directory (`corpus/<id>/`) and ordered newest first. The work page
SHALL render it as a single collapsed `<details>` section, whole-work in scope, placed with the
"Report an error" link at the bottom of the page. The section SHALL degrade gracefully when git
history is unavailable, and the build job SHALL check out the full history so entries are not
truncated.

#### Scenario: History derived from git and emitted into the data

- **WHEN** `build_site_data.py` runs inside a git repository
- **THEN** each work in `works.json` carries a `history` list, newest first
- **AND** each entry records the commit date, short hash, subject line, and the artifacts the
  commit touched, mapped from changed paths to labels (`original.tex` → `original`,
  `translations/<lang>.tex` → `<lang> translation`, `work.yaml` → `metadata`, `provenance.yaml` →
  `provenance`, `figures/` → `figures`)

#### Scenario: Rendered as a collapsed whole-work section

- **WHEN** a work page renders with a non-empty `history`
- **THEN** it shows a collapsed `<details>` titled "Revision history" near the "Report an error"
  link, not split per translation panel
- **AND** each row shows the date, the artifacts touched, and the commit subject, with the short
  hash linking to that commit on the source host (reusing the repository URL the page already
  builds for the report-error link)

#### Scenario: Graceful degradation without git history

- **WHEN** the build runs outside a git repository, from a tarball, or from a clone with no
  reachable commits
- **THEN** `history` is empty, the "Revision history" section is omitted, and the build succeeds

#### Scenario: Full history available at build

- **WHEN** the site build job checks out the repository
- **THEN** it uses unbounded depth (`fetch-depth: 0`) rather than the default shallow clone, so a
  work's rendered history is not limited to a single commit
