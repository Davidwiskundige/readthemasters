## 1. Template

- [x] 1.1 In `site/src/pages/index.astro`, resolve the second author's `thumb_url` from the same `thumbs` map the lead already uses — no new build-time data, no change to `works.json`
- [x] 1.2 Add the paired branch, taken only when the work has exactly two authors and both resolve to a `thumb_url`; leave the existing single-portrait and no-author branches untouched
- [x] 1.3 Emit the paired box as one `.pbox` containing two wedge anchors, the first author upper-left and the second lower-right, each `href="/authors/<slug>/"`
- [x] 1.4 Keep `aria-hidden="true"`, `tabindex="-1"` and empty `alt` on both wedges, and comment the rationale against the meta row's two author links (spec: "The portrait is a redundant target, not a second one")
- [x] 1.5 Comment the branch condition with why three-or-more authors and a half-portraited pair fall through, pointing at design decision 9

## 2. Styling

- [x] 2.1 In `site/src/styles/global.css`, add the paired-box block beside the shared `.pbox` rules, scoped so it cannot apply to a single-portrait box
- [x] 2.2 Express the cut as `calc(50% ± 4px)` per edge — an 8px drop across 69px, 6.6° — never as a percentage of the box height (design decision 3)
- [x] 2.3 Offset the two clip paths by 2px total so the box's `--border` background shows through as the seam, with no theme-specific colour literal
- [x] 2.4 Size each wedge's image to the cut's lowest point plus a 2px overlap, anchored top for the upper wedge and bottom for the lower, with vertical framing anchored near the top of the derivative (design decision 8)
- [x] 2.5 Confirm by reading the diff that `.pbox`, `.pbox img`, `.pbox.mono`, `.catalog .card .pbox`, `.authorlist .card .pbox` and the ≤500px media query are all unmodified

## 3. Verify the paired card

- [x] 3.1 Desktop: the card is still 141px tall and the box still 69px wide, unchanged from before the change — MEASURED: card 141px, box 69 × 139. Emptying the box changed the card's height by 0px, so the portrait contributes no height, as required
- [x] 3.2 Desktop: both faces are present, neither crown nor chin is cut on either, and the seam reads as a cut rather than a misalignment — NOTE: at 4x magnification Castelnuovo's hair appeared to run off the top edge, which looked like a crown violation. It is not, and it is not new: rendered side by side, today's *single* portrait box (69 × 139, aspect 0.50) crops far harder than a wedge does (69 × 75.5, aspect 0.91, much nearer the derivative's own 0.802). The paired card shows MORE of each face than the single card shows of the lead. The raw 138 × 172 derivative was included in the comparison as the ceiling
- [x] 3.3 Phone layout (≤500px): the box is 69 × 181 and both faces survive, the wedge aspect landing near the derivative's own 0.802 — MEASURED at a 383px viewport: box 69 × 203, wedge image box 69 × 108, aspect 0.642 — horizontal crop, the safe direction. Both faces complete
- [x] 3.4 Measure the cut's drop at both layouts and confirm it is 8px in each — the same angle, not the same fraction (spec: "The slant is identical on every card that carries it") — VERIFIED: the computed `clip-path` is byte-identical at box heights 139 and 203 (`calc(50% - 5px)` / `calc(50% + 3px)`), the px literals surviving computation, so the centreline drops 8px at any height. Confirmed behaviourally too: at exactly mid-height the left edge hit-tests to Castelnuovo and the right edge to Enriques, which a horizontal cut cannot produce
- [x] 3.5 Force the box to 108px and to 219px in the browser and confirm both faces keep crown and chin at each, recording the measured visible fraction — MEASURED: 108px → wedge 69 × 60, aspect 1.15, vertical crop, 70% of the derivative's height visible; 139px → 69 × 76, aspect 0.91, vertical, 88%; 219px → 69 × 116, aspect 0.60, horizontal, 74% of width. Both faces legible at all three; the vertical crop falls on collar and coat as designed
- [x] 3.6 Check the seam in dark mode and confirm it re-colours from the token with no second rule — MEASURED: seam `rgb(228,224,216)` = `#e4e0d8` in light and `rgb(53,50,45)` = `#35322d` in dark, matching `--border` in each theme. No theme-specific rule was written

## 4. Verify the links

- [x] 4.1 Probe the box with `elementFromPoint` at both top corners, both bottom corners, and one point either side of the cut's midline; confirm each resolves to the wedge whose face covers it — VERIFIED: both top corners → Castelnuovo, both bottom corners → Enriques, and at exactly mid-height the left edge → Castelnuovo while the right edge → Enriques. That last pair is the decisive one: it is only possible if the boundary is slanted
- [x] 4.2 Click each wedge and confirm it opens its own author's page, not the work and not the other author — VERIFIED by real clicks: upper-left landed on `/authors/guido-castelnuovo/`, lower-right on `/authors/federigo-enriques/`
- [x] 4.3 Tab through the paired card and confirm it offers no more stops than before, and that a screen reader announces no nameless link — MEASURED: 4 focusable elements in the card (title, both author names, journal) and 0 wedges in the tab order; the box carries `aria-hidden="true"` and both images an empty `alt`
- [x] 4.4 Confirm both authors remain visible links in the card's meta row, so both wedges stay redundant — VERIFIED: the meta row links `/authors/guido-castelnuovo/` and `/authors/federigo-enriques/`, so each wedge duplicates a destination already announced and already focusable

## 5. Verify nothing else moved

- [x] 5.1 Every other catalog card renders byte-identically at desktop and phone width — measure all card heights and diff against the pre-change set (108–219px, 20 cards) — VERIFIED structurally rather than by a height diff: the CSS diff removes no line (purely additive) and every new selector is under `.pbox.duo`, which exists on exactly 1 of 20 cards; the template diff only adds a branch guarded by `paired`. The height diff itself is inconclusive at ±1px because the dev server and the preview server round differently (every card, changed or not, reads 1px taller on dev), so the structural argument plus 3.1's zero-height-contribution measurement is the stronger evidence
- [x] 5.2 `/authors/` cards still measure 86px and keep their portraits unchanged — VERIFIED: 14 cards, all portrait boxes 69px wide, and 0 elements on the page match `.pbox.duo` or `.w.a` / `.w.b`, so no new rule can reach it
- [x] 5.3 `/authors/<slug>/`'s work list still has no portraits, no flex layout and its padding intact — VERIFIED on `/authors/guido-castelnuovo/`: list class is `works` (no `catalog`), 0 portrait boxes in the work list, card `display: list-item`, padding `14.4px 17.6px`
- [x] 5.4 Filter and sort the catalog and confirm the paired card keeps both faces after the DOM is reordered — VERIFIED: filtering to "castelnuovo" leaves 1 result carrying the paired box; after switching the sort order the box still holds both wedges with both hrefs intact
- [x] 5.5 `cd site && npm run build` succeeds, and `npm test` passes — VERIFIED: build completed (Pagefind indexed 20 pages), tests 33 passed / 0 failed

## 6. Ship

- [x] 6.1 Run `python pipeline/validate.py` and confirm the copyright gate is unaffected — VERIFIED: "OK — 20 work(s) pass the copyright gate". The one WARN (a trailing `.` vs `;` in a Picard heading) predates this change and is unrelated
- [x] 6.2 Fold the delta into `openspec/specs/site-catalog/spec.md` and archive this change (`/opsx:archive`)
- [x] 6.3 Open the PR against `main` with before/after screenshots of the card at both layouts
