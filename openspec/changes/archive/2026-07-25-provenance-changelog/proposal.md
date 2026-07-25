# Change: provenance-changelog

## Why

The git-derived revision history (`revision-history` + `revision-history-filter`) never read well.
Even after filtering, it surfaced commit subjects written for the repo, not the reader, and the
subject↔work mapping was always approximate (a status-token rename still read as a revision). A
work's history is editorial content — "what changed about this text and when" — and is better
authored than inferred. We replace the git derivation with a curated `changelog` block in
`provenance.yaml`.

## What changes

- **New optional `changelog` block in `provenance.yaml`** — a top-level list of `{date, summary}`
  entries, human-written, alongside `transcription:` / `translations:`. `date` is ISO
  (`YYYY-MM-DD`), `summary` is a short free-text line. CI schema-checks entries when present.
- **The work page's "Revision history" section is sourced from the changelog**, newest first
  (date + summary), collapsed as before, omitted when a work has no changelog. No commit hashes,
  artifact tags, or "show all changes" expander — those existed only to tame git noise.
- **The git machinery is removed**: `git log` extraction, the metadata/sweep filtering, the
  `content` flag, and `fetch-depth: 0` in CI all go, since the build no longer reads git for
  history.
- **The three existing works are seeded** with changelogs drawn from their real history, so the
  section is populated on day one.

## Impact

- Modifies **corpus-format** (provenance gains the optional `changelog` block; validated in
  `pipeline/validate.py`) and **site-catalog** (the "Revision history" requirement is re-sourced
  from the changelog).
- Touches `pipeline/build_site_data.py` (drop git extraction, emit `changelog`),
  `pipeline/validate.py` (schema-check `changelog`), `site/src/pages/works/[id].astro` and
  `site/src/styles/global.css` (simpler rendering), `.github/workflows/ci.yml` (drop
  `fetch-depth: 0`), the three `corpus/*/provenance.yaml` files (seed entries), and replaces
  `pipeline/tests/test_history.py` with `pipeline/tests/test_changelog.py`.
- Trade-off (accepted): revision history is now **manual bookkeeping** rather than derived — the
  cost of a history that reads well and says exactly what the maintainer means.
- `revision-history` and `revision-history-filter` remain archived as decision history; this change
  supersedes their behavior in the live spec.
