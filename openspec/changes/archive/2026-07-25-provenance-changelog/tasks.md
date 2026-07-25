# Tasks: provenance-changelog

## Data & validation

- [x] `pipeline/build_site_data.py`: remove the git-log extraction (`classify_path`,
      `work_relative`, `parse_history`, `work_history`, `is_content_revision`, `SWEEP_MIN_WORKS`,
      the sweep tally, the `subprocess` import). Add `changelog_entries(provenance)` returning
      normalized `{date, summary}` newest first; emit it as each work's `changelog`.
- [x] `pipeline/validate.py`: in `check_provenance`, validate an optional `changelog` — must be a
      list; each entry needs an ISO `date` and a non-empty `summary`.

## Site

- [x] `site/src/pages/works/[id].astro`: render the collapsed "Revision history" from
      `work.changelog` (date + summary, newest first); omit when empty. Drop the content/housekeeping
      split, artifact tags, hashes, and the nested expander.
- [x] `site/src/styles/global.css`: simplify `.revhistory` styles; remove `.arts`,
      `.revhistory code`, `.revhistory-all`.

## CI

- [x] `.github/workflows/ci.yml`: remove `fetch-depth: 0` from the build checkout (no longer needed).

## Seed & tests

- [x] Add a `changelog` block to each of the three `corpus/*/provenance.yaml`, drawn from real
      history.
- [x] Replace `pipeline/tests/test_history.py` with `pipeline/tests/test_changelog.py`:
      `changelog_entries` ordering/normalization, and `validate` flagging a bad entry.

## Ship

- [x] Fold the deltas into `openspec/specs/corpus-format` + `site-catalog`; update `project.md`;
      archive the change.
