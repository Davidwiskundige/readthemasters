# Change: revision-history

## Why

PLAN.md §9 backlog #4. A work page shows only the *current* state of each artifact — one
attribution line per panel (model + reviewer). A visitor cannot see how a text got there:
corrections ("eq. 12 corrected"), status promotions (`ai-draft` → `skimmed` → `verified`), or
model re-runs. Git already records every one of these as an ordinary commit, so the history exists
with zero extra bookkeeping — nothing on the site surfaces it. Showing it builds trust: a reader
can judge how settled a text is, and see that changes are tracked in the open.

## What changes

- **History derived from git at build time.** `pipeline/build_site_data.py` runs `git log` scoped
  to each work's directory (`corpus/<id>/`) and emits a per-work `history` list into `works.json`,
  newest first. Each entry carries the commit date, short hash, subject line, and which artifacts
  the commit touched — mapped from the changed paths to readable labels (`original`, `<lang>
  translation`, `metadata`, `provenance`). History is **derived, not stored**: no new `work.yaml`
  field, so the corpus format is unchanged.
- **Collapsed "Revision history" section on the work page.** A single `<details>` near the bottom
  (grouped with the "Report an error" link), whole-work scope, one line per commit: *date ·
  artifacts touched · subject*, with the short hash linking to the commit on GitHub (reusing the
  `repo` URL the page already builds for the report-error link). Collapsed by default so it never
  competes with the text.
- **Graceful degradation.** If git history is unavailable at build time — not a git repo, a
  build from a tarball, or a clone with no reachable commits — `history` is empty and the section
  is omitted entirely. The build never fails on account of history.
- **Full history at build.** The "Build site" job's checkout gets `fetch-depth: 0` so the log is
  complete; the default shallow clone (depth 1) would render a history of a single commit.

## Impact

- Extends **site-catalog**: a new work-page section and a `history` field in the build-time data.
  No change to the copyright gate and **no change to `corpus-format`** — history is computed from
  git, not declared in `work.yaml`.
- Touches `pipeline/build_site_data.py` (git-log extraction + path→artifact mapping),
  `site/src/pages/works/[id].astro` (render the collapsed section), `site/src/styles/global.css`
  (section styling), `.github/workflows/ci.yml` (`fetch-depth: 0` on the build checkout), and adds
  `pipeline/tests/test_history.py`.
- Commit-message quality becomes lightly visitor-facing (the subject line is shown). This is a
  nudge toward clear messages, not a new requirement; nothing enforces it and the section works
  regardless.
