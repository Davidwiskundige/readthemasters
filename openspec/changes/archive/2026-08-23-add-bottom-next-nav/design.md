## Context

The work page ([site/src/pages/works/[id].astro](site/src/pages/works/[id].astro)) already computes
`recPrev` and `recNext` from the work's `recommended_prev`/`recommended_next` data and renders one
`.relnav` block near the top, right after the Significance callout. The text itself (original +
translation tabs) can run to many screens for a long transcription, so the top nav is out of view by
the time a reader reaches the end.

## Goals / Non-Goals

**Goals:**
- Show the same "Related reading" information again immediately after the text panels, so a reader
  who just finished sees where to go next without scrolling back up.
- Keep both navs in sync automatically — one data source, one render path, no risk of the top and
  bottom copy drifting apart.

**Non-Goals:**
- No change to how `recommended_prev`/`recommended_next` are computed or emitted by
  `build_site_data.py`.
- No "auto-advance" or keyboard-navigation behavior — this is a link, not a paginator.
- No change to the top nav's position or condition.

## Decisions

- **Extract the nav markup into a small local Astro helper/snippet reused for both placements**,
  rather than copy-pasting the JSX-like block twice. Astro doesn't have a lightweight inline
  component the way JSX does, so the simplest reuse within a single `.astro` file is a tiny
  render function (mirroring the existing `attribution()`/`renderSignificance()` helpers already in
  this file) that returns the nav's inner HTML/string, called from both spots. Alternative
  considered: duplicate the JSX block verbatim at the bottom — rejected because any future copy or
  markup change would need to be kept in sync manually in two places.
- **Same visual style, `Next:`-only condition**: the bottom nav uses the existing `.relnav` CSS
  class (no new class needed for the base look) but renders only when `recNext` exists, and only
  ever fills the `Next:` side — the `Read first:` side is never populated at the bottom. Rationale:
  once a reader has finished the text, telling them what they should have read *before* it isn't
  actionable; only "what to read next" still is. The top nav is unchanged — it still shows both
  sides under `{(recPrev || recNext) && (...)}`.
- **Placement**: directly after the closing of the text panels (after the last translation
  `<section>`, before the "Existing translations elsewhere" section), so it reads as "you just
  finished the text — here's what's next," ahead of the more peripheral downloads/report-error/
  revision-history content instead of below it.
- **Minor spacing tweak**: add a top margin variant (e.g. a `relnav-bottom` modifier class) only if
  the default `.relnav` margin looks cramped directly under the text — implementation detail decided
  during the tasks/implementation pass, not a spec-level concern.

## Risks / Trade-offs

- [Two navs on one page could feel redundant on a short work where both are visible in one viewport]
  → Acceptable: the guard condition already limits the nav to works that have a recommendation, and
  the terse one-line style keeps the repeat low-cost; no need to suppress the bottom nav based on
  page length.
- [Helper-function reuse adds a small refactor inside an already-large `.astro` file] → Scoped
  tightly to the existing render-function pattern already used in the file (`attribution`,
  `renderSignificance`), so it stays consistent with current style rather than introducing a new
  pattern.

## Migration Plan

Presentational-only change to a single page template; ships as a normal PR, no data migration, no
rollback concerns beyond reverting the commit.

## Open Questions

None — scope is small enough that implementation choices (e.g. exact helper name, whether a
spacing modifier class is needed) are left to the tasks/implementation step.
