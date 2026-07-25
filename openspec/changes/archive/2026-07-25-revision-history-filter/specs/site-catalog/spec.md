# Delta: site-catalog — revision history filtering

## MODIFIED Requirements

### Requirement: Revision history

Each work page SHALL show a revision history of the work, derived at build time from git — no
revision data is stored in `work.yaml`. The history SHALL distinguish **content revisions** of the
text from incidental housekeeping, and lead with the former.

`pipeline/build_site_data.py` emits a per-work `history` list into `works.json`, derived from
`git log` scoped to the work's directory (`corpus/<id>/`) and ordered newest first. Each entry
records the commit date, short hash, subject line, the artifacts the commit touched (mapped from the
changed paths to readable labels: `original.tex` → `original`, `translations/<lang>.tex` →
`<lang> translation`, `work.yaml` → `metadata`, `provenance.yaml` → `provenance`, `figures/` →
`figures`), and a `content` flag.

A commit is a **content revision** when it changed the work's actual content — the text
(`original.tex` or a translation), its `provenance` (status promotions, model re-runs), or its
`figures` — and is **not** a corpus-wide sweep. A commit that only touched `work.yaml` (metadata),
or that touches many published works at once (a migration, at or above a fixed threshold of works),
is not a content revision. The sweep threshold is judged across the published corpus so a single
repo-wide change is demoted on every work's page even when it edited text.

The work page renders the history as a single collapsed `<details>` "Revision history" section near
the "Report an error" link, whole-work in scope (not split per panel). Content revisions are listed
by default; the summary count is the number of content revisions. Housekeeping commits are not
discarded but demoted behind a nested "show all changes" expander, so the history stays fully
auditable. When a work has no content revisions, all commits are shown in the main list. Each row
shows the date, the artifacts touched, and the subject, with the short hash linking to the commit on
the source host (reusing the repository URL the page already builds for the report-error link).

History is derived, so it degrades gracefully: when git history is unavailable at build time (not a
git repository, a tarball build, or a clone with no reachable commits), `history` is empty and the
section is omitted — the build never fails for lack of history. Rendering the full history requires
the complete commit history at build, so the site build job checks out with `fetch-depth: 0` rather
than the default shallow clone, which would otherwise truncate every work's history to one commit.

#### Scenario: Content revisions lead, housekeeping is demoted

- **WHEN** a work's history contains both content revisions and commits that only touched metadata
  or that swept many works at once
- **THEN** the work page lists the content revisions by default and moves the rest behind a nested
  "show all changes" expander
- **AND** the "Revision history" summary count is the number of content revisions

#### Scenario: A metadata-only sweep is not a content revision

- **WHEN** a commit changed only `work.yaml` (e.g. a corpus-wide field addition)
- **THEN** its history entry has `content: false` and does not appear in the default list

#### Scenario: Graceful degradation without git history

- **WHEN** the build runs outside a git repository, from a tarball, or from a clone with no
  reachable commits
- **THEN** `history` is empty, the "Revision history" section is omitted, and the build succeeds

#### Scenario: Full history available at build

- **WHEN** the site build job checks out the repository
- **THEN** it uses unbounded depth (`fetch-depth: 0`) rather than the default shallow clone, so a
  work's rendered history is not limited to a single commit
