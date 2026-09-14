## 1. Markup

- [x] 1.1 In `site/src/pages/index.astro`, point the portrait box at `/authors/<first author slug>/` instead of `w.url`
- [x] 1.2 Render the box as a plain `div` (not an `a`) when a work has no first author, matching the shape `/authors/` already uses for a portrait-less author
- [x] 1.3 Keep `aria-hidden="true"`, `tabindex="-1"` on the link and the empty `alt` on the image, and rewrite the comment above it so it states the new justification — redundant with the meta row's author link, not with the title
- [x] 1.4 Confirm nothing else in the card changed: the title link, the meta row, every `data-*` filter/sort attribute, the monogram branch and the `thumbs` lookup are untouched
- [x] 1.5 Confirm no change to `site/src/styles/global.css`, `pipeline/build_site_data.py`, `work.yaml` or `works.json`

## 2. Verification — the destination

- [x] 2.1 Build the site and confirm every catalog card's portrait `href` equals that card's first author link in the meta row, across all 20 works (the corpus gained picard-1885 after this change was written)
- [x] 2.2 Confirm the multi-author card (`castelnuovo-enriques-1897-surfaces-algebriques`) points at Castelnuovo — the author shown — and that its meta row still links both authors
- [x] 2.3 Click a portrait in both layouts (wide and below the 500px breakpoint) and land on the author page
- [x] 2.4 Confirm no built page contains `/authors/undefined/` or an empty `href` on a `.pbox`
- [x] 2.5 Force the monogram branch on one card (no `thumb_url`) and confirm the placeholder box carries the same author link
- [x] 2.6 Force the no-author branch on one card and confirm the box renders as a `div` with the same footprint and no link

## 3. Verification — nothing else moved

- [x] 3.1 Diff rendered card heights and total list height against the current build at 375px, 500px and 1280px: identical to the pixel, both layouts
- [x] 3.2 Confirm `.pbox` geometry is unchanged when the element is a `div` rather than an `a` — measure the forced no-author card, don't infer it from the stylesheet
- [x] 3.3 Keyboard-tab a card in both layouts: one stop for the title, one per author link, none for the portrait; confirm against the accessibility tree
- [x] 3.4 Screen-reader pass on one card: the portrait announces nothing, and the author page is still reachable via the meta row
- [x] 3.5 `/authors/`, `/authors/<slug>/`, a journal page, the timeline and search: unchanged at 375px and 1280px
- [x] 3.6 Filter by a facet and change the sort order: surviving cards keep portraits pointing at the right authors after DOM reordering
- [x] 3.7 Both colour schemes, phone and desktop width

## 4. Ship

- [x] 4.1 Run `python pipeline/validate.py` and the full site build; both clean
- [x] 4.2 Run `openspec validate --changes catalog-portrait-links-author`
- [ ] 4.3 Open the PR, noting that the change is one `href` plus a no-author guard and that the a11y posture is re-justified rather than relaxed

## 5. Spec sync

- [ ] 5.1 Fold `catalog-card-portraits-phone`'s delta into `openspec/specs/site-catalog/spec.md` and archive that change **first** — it shipped in PR #62 and its delta is still pending, so the main spec's `Catalog card portraits` requirement is stale and folding in the wrong order would revert the narrow layout's text
- [ ] 5.2 Then fold this change's delta and archive it; confirm the resulting requirement carries both the narrow layout and the author destination
