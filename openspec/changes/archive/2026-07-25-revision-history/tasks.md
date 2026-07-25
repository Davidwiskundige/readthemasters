# Tasks: revision-history

## Data

- [x] Add git-log extraction to `pipeline/build_site_data.py`: for each work, run
      `git log --name-only --format=...` scoped to `corpus/<id>/`; parse each commit into
      `{date, hash, subject, artifacts}` where `artifacts` is the set of touched files mapped to
      labels (`original.tex`→`original`, `translations/<lang>.tex`→`<lang> translation`,
      `work.yaml`→`metadata`, `provenance.yaml`→`provenance`, figures→`figures`).
- [x] Emit the per-work `history` list (newest first) into `works.json`.
- [x] Degrade gracefully: wrap the `git` subprocess so a non-repo / missing-git / no-commits
      build yields `history: []` instead of raising.

## Site

- [x] `site/src/pages/works/[id].astro` — collapsed `<details>` "Revision history" near the
      report-error link, one line per commit (*date · artifacts · subject*), short hash linking to
      `${repo}/commit/<hash>`. Reuse the existing `repo` value.
- [x] Render nothing when `history` is empty.
- [x] Section styling in `site/src/styles/global.css`.

## CI

- [x] Set `fetch-depth: 0` on the `actions/checkout` step of the "Build site" job in
      `.github/workflows/ci.yml` so the full history is present at build.

## Tests & verification

- [x] `pipeline/tests/test_history.py` — path→artifact mapping, newest-first ordering, and
      empty-history fallback when run outside a git repo.
- [x] Build site data + Astro build; verify the section renders, is collapsed, and a hash links to
      the right commit, in the preview browser.

## Ship

- [x] Fold the delta into `openspec/specs/site-catalog`; update `project.md` if needed; archive the
      change.
