## Why

The "Related reading" nav (`Read first:` / `Next:`) sits only at the top of the work page, above the
text. A reader who just finished the transcription is scrolled to the bottom of the page and has to
scroll back up to find out what to read next — the one moment they're most likely to want that link
is the one moment it's out of view.

## What Changes

- Add a second, bottom-of-page "Related reading" nav after the text panels (original +
  translations), using the same terse style and link targets as the top one.
- The bottom nav shows **only** the `Next:` link, not `Read first:` — by the time a reader reaches
  the bottom they've already read the current text, so pointing them at what they should have read
  *before* it is no longer actionable. The top nav is unchanged and still shows both.
- Reuse the existing markup/logic for the nav rather than duplicating divergent copy — both instances
  render from the same `recPrev`/`recNext` data.
- No changes to `build_site_data.py` or the underlying `relations`/`recommended_prev`/
  `recommended_next` data — this is a presentational addition to the work page template only.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `site-catalog`: the "Related reading (dependency graph)" requirement gains a second nav placement
  at the bottom of the work page (after the text, `Next:`-only), in addition to the existing top
  placement (`Read first:` + `Next:`).

## Impact

- Affected code: [site/src/pages/works/[id].astro](site/src/pages/works/[id].astro) (the `.relnav`
  block and its render call) and possibly [site/src/styles/global.css](site/src/styles/global.css)
  if a bottom-specific style tweak is needed (e.g. spacing above the downloads/report-error area).
- No data pipeline, corpus, or spec-data changes; no CI/copyright-gate impact.
