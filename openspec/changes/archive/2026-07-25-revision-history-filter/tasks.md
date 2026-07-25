# Tasks: revision-history-filter

## Data

- [x] `pipeline/build_site_data.py`: add `is_content_revision(artifacts, hash, sweeps)` — True when
      a commit touched a non-`metadata` artifact and is not a corpus-wide sweep.
- [x] Tally each commit hash across all published works' histories; treat a hash touching
      `SWEEP_MIN_WORKS`+ works as a sweep. Set a `content` flag on every history entry.

## Site

- [x] `site/src/pages/works/[id].astro`: split `history` into content vs housekeeping; render
      content revisions in the main list, housekeeping behind a nested "show all changes" expander.
      Count in the summary is the content-revision count. Fall back to showing all if none are
      content.
- [x] `site/src/styles/global.css`: style the nested expander (small, muted).

## Tests & verification

- [x] Extend `pipeline/tests/test_history.py`: `is_content_revision` truth table (metadata-only →
      False, text/provenance/figures → True, sweep hash → False, empty → False).
- [x] Rebuild data + Astro build; verify Fagnano's history now leads with content revisions and the
      housekeeping commits are behind the expander, in the preview browser.

## Ship

- [x] Fold the delta into `openspec/specs/site-catalog`; archive the change.
