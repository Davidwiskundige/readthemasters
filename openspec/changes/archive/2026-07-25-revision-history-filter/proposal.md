# Change: revision-history-filter

## Why

The `revision-history` capability (just shipped) lists every commit that touched `corpus/<id>/`,
which is a coarse proxy for "revisions of this text." In practice the list is dominated by
housekeeping: for the Fagnano work, 4 of 7 entries were corpus-wide sweeps that only touched
`work.yaml` ("Add author pages", "Repoint examples in docs/tests", "Set Wikidata QID") or a
mechanical rename. A reader scanning the history to judge how settled a text is has to wade past
changes that never altered the text.

## What changes

- **Filter to content revisions.** A commit is shown as a revision only when it changed the work's
  actual content — `original.tex`, a `translations/<lang>.tex`, `provenance.yaml` (status
  promotions, model re-runs), or `figures/` — not when it only touched `work.yaml` (metadata).
- **Drop corpus-wide sweeps.** A commit that touches many published works at once (≥ a threshold)
  is treated as a migration and excluded from every work's history, even if it edited text — so a
  future "apply house style to all works" pass doesn't flood every page.
- **Keep everything auditable.** Filtered-out commits are not discarded: the section still shows
  the content revisions by default, with a nested "show all changes" expander revealing the
  housekeeping commits. Nothing is hidden, just demoted.
- The classification is computed at build time in `build_site_data.py` (each history entry gains a
  `content` boolean); the work page splits the list on it. Still zero bookkeeping — no new fields
  in `work.yaml` or `provenance.yaml`.

## Impact

- Modifies the **site-catalog** "Revision history" requirement (filtering + the show-all expander).
- Touches `pipeline/build_site_data.py` (sweep tally + `content` flag), `site/src/pages/works/[id].astro`
  (split rendering), `site/src/styles/global.css` (nested expander), and extends
  `pipeline/tests/test_history.py`.
- Known limitation (documented, not fixed here): a one-off rename that changes a status *token*
  without a real re-review can still read as a content revision if it isn't also a corpus-wide
  sweep; distinguishing that would require diffing `provenance.yaml` field-by-field.
