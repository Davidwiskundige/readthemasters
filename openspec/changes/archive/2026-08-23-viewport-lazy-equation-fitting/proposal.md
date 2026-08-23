## Why

Opening a translation tab on a long work blocks the main thread for about ten seconds. Measured on
`abel-1841-fonctions-transcendantes` (665 display equations per panel), production build:

| | |
|---|---|
| first reveal of the translation panel | **10,416 ms** |
| typesetting that panel in place while still hidden | 4,626 ms |
| flip + fit with the panel **already** typeset | **12,857 ms** |

The third row is the finding: the cost persists with no typesetting left to do, so this is not a
KaTeX problem. A `display:none` panel is never laid out, so the browser defers layout for all 665 of
its display equations until the panel is shown — and `fitDisplayMath` then forces that entire first
layout synchronously, in one blocking chunk, by reading `clientWidth` on every equation before it
can decide anything.

The same mechanism taxes the initial page load: the visible panel's equations are all measured up
front, so its first layout is forced synchronously too, inside the ~2.2 s DCL gap that remains after
`lazy-render-hidden-panel-math`.

Neither of the shipped fixes touches this, and neither would the next one on the list:
`fix-fitdisplaymath-layout-thrashing` made the pass cheap *per equation* but it still measures all of
them; `lazy-render-hidden-panel-math` moved typesetting off the load path but layout was always
deferred to the reveal anyway; and build-time pre-rendering (backlog #18) removes typesetting while
leaving this layout cost exactly as it is. This is PLAN.md §9 backlog #19 item 4.

## What Changes

- Fit a display equation when it approaches the viewport rather than fitting every equation up
  front, using an `IntersectionObserver` with a margin so equations are classed slightly before they
  are scrolled into view.
- Let the browser skip layout for off-screen equations entirely via `content-visibility: auto`, with
  `contain-intrinsic-size` so skipped content still occupies a plausible height and the scrollbar
  does not lurch.
- **These two must land together.** `content-visibility` alone breaks the current pass outright — a
  probe on the built site produced 0 `wide` and 0 `tag-below`, because layout-skipped elements report
  no usable geometry to a measure-everything loop.
- Re-interpret a zero `clientWidth`. Today it means "inside a hidden panel, skip it"; with
  `content-visibility` it also means "not laid out yet, come back later". The fitting pass must
  distinguish "will never be measured here" from "not measurable *yet*" instead of silently
  dropping the equation.
- Re-fit on resize as now, but invalidate lazily: drop what has been fitted and let the observer
  re-fit what is on screen, rather than re-measuring the whole document.
- Keep deep links landing on their anchor, which gets harder when the target may sit inside
  layout-skipped content whose height is only an estimate until it is realised.

## Capabilities

### New Capabilities

None. This changes when and how existing behavior is computed.

### Modified Capabilities

- `site-catalog`: the "Work page" requirement already fixes the batching rule and the lazy-typesetting
  rule for the display-math pass. It gains the rule that fitting is driven by proximity to the
  viewport rather than performed for every equation up front, that off-screen equations may have
  their layout skipped, and that an equation not yet measurable is deferred rather than dropped.

## Impact

- **Code**: `site/src/pages/works/[id].astro` (the fitting pass, its call sites, and the panel
  observer) and `site/src/styles/global.css` (`content-visibility` / `contain-intrinsic-size` on
  equations and/or paragraphs). `site/src/lib/fitmath.js` and its tests are unaffected — the
  arithmetic does not change, only which equations it is asked about and when.
- **Find-in-page**: an improvement rather than a risk. `content-visibility: auto` content stays
  searchable by the browser's find, which reveals it on a hit — unlike the `display:none` panel,
  whose text is unreachable today.
- **Search**: none. Pagefind and the formula index are built from the HTML at build time.
- **Printing**: needs checking — a printed page must realise skipped content rather than emit blank
  space where equations should be.
- **Risk**: the highest of the three changes in this series. `wide` and especially `tag-below` change
  an equation's height, which can change what intersects the viewport, so a naive implementation can
  oscillate or thrash the observer. Deep links and scroll position rest on `contain-intrinsic-size`
  estimates until real layout happens.
- **Not in scope**: build-time pre-rendering (#18), and any change to the wide/tag-below rule itself.
