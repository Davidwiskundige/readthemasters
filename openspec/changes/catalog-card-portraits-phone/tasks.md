## 1. Baseline measurements

- [x] 1.1 From a local build, record total list height and per-card heights at 375px, 430px, 560px and 768px, measuring the metadata and English-title blocks by **ink** (first line's top to last line's bottom), not by box height — a wrapped flex container stretches its lines and box measurements hide the mismatch
- [x] 1.2 Record the rendered portrait box at 375px (expected: 69px wide by 219–428px tall, aspect 0.16–0.31) — the defect this change exists to remove
- [x] 1.3 Record `/authors/` card heights at 375px (expected 86 and 114px) as the regression baseline for a page this change must not touch

## 2. Markup

- [x] 2.1 In `site/src/pages/index.astro`, wrap the English title and the metadata row in a single container inside `.body`, leaving the original title as its sibling
- [x] 2.2 Make the portrait and that container siblings in one row, so the wide layout is the same DOM laid out differently rather than a second markup path
- [x] 2.3 Leave every `data-*` filter/sort attribute on the `li` itself, untouched
- [x] 2.4 Confirm no change to `pipeline/build_site_data.py`, `work.yaml`, or `works.json`

## 3. CSS

- [x] 3.1 Express the wide layout through the new structure so nothing above the breakpoint changes — verify against the 1280px baseline before writing any narrow-layout rule
- [x] 3.2 Add the narrow-layout media query at the card breakpoint (500px — design.md §3 was corrected from 560px during implementation): title full width, portrait and text block in a row, portrait stretched to the row
- [x] 3.3 Floor the portrait at its natural height so a work with no `title_en` cannot produce a box wider than it is tall
- [x] 3.4 Verify every added rule is scoped to `.catalog .card`, and that no bare `.card` rule and nothing keyed on `.works` was changed

## 4. Verification — the defect

- [x] 4.1 At 375px and 430px: the portrait's height equals the English-title-plus-metadata block's ink height on every card, within a couple of pixels
- [x] 4.2 At 375px and 430px: on no card is the portrait taller than that text block
- [x] 4.3 At every width from 320px to the breakpoint, the portrait box is taller than it is wide on every card — the letterbox crop must be impossible, not merely absent
- [x] 4.4 Record the visible-width fraction of the thumbnail; expect roughly 33–54% at 375px and 39–57% at 430px, against 20–39% today
- [x] 4.5 Check the sparse-metadata cards specifically (Leibniz, Fagnano, Enriques) — these are where every earlier approach failed
- [x] 4.6 Temporarily remove `title_en` from one work and confirm its card still renders a portrait taller than it is wide (task 3.3)

## 5. Verification — no collateral damage

- [x] 5.1 At 1280px: card heights and total list height identical to the 1.1 baseline, to the pixel
- [x] 5.2 At 768px: the wide layout is in use, not the narrow one
- [x] 5.3 Sweep 480–530px across the breakpoint: the switch is clean, with no card left in a broken intermediate state
- [x] 5.4 `/authors/` at 375px and 1280px: identical to the 1.3 baseline
- [x] 5.5 `/authors/<slug>/` and a journal page at both widths: work lists unchanged, no portraits
- [x] 5.6 Filter by a facet and change the sort order below the breakpoint; portraits survive the DOM reordering
- [x] 5.7 Keyboard-tab a card below the breakpoint: one stop for the title, one per author link, none for the portrait; confirm against the accessibility tree
- [x] 5.8 The monogram and multi-author cards both correct in the narrow layout — NOTE: no work in the current corpus renders a monogram (every catalogued first author now has a portrait), so the monogram was verified by forcing `.pbox.mono` onto the shortest-text card in the DOM: aspect 0.57, matches its text exactly, `display:flex` with the letter centred on both axes
- [x] 5.9 A title carrying KaTeX math: the card re-crops rather than reflowing the list when the math renders
- [x] 5.10 Both colour schemes at phone width

## 6. Ship

- [x] 6.1 Run `python pipeline/validate.py` and the full site build; both clean
- [ ] 6.2 Open the PR with before/after screenshots at 375px and 430px and the measured height and crop deltas
- [ ] 6.3 After merge, fold the delta spec into `openspec/specs/site-catalog/spec.md` and archive the change

## Measured results

Same build, measured with the narrow-layout media rule enabled vs. deleted at the same viewport —
apples to apples. Text blocks measured by ink, not box height.

| viewport | before | after | portrait | aspect | portrait taller than text |
|---|---|---|---|---|---|
| 320px | — | 6298px | 147–259px | 0.27–0.47 | 0/18 |
| 375px | 5885px | **5401px (−8.2%)** | 128–227px | **0.30–0.54** *(was 0.16–0.32)* | 0/18 |
| 430px | 4900px | **4598px (−6.2%)** | 120–175px | 0.39–0.57 | 0/18 |
| 500px | 4305px | **4225px (−1.9%)** | 99–169px | 0.41–0.70 | 0/18 |
| 520px | — | wide layout | — | — | n/a |
| 1280px | 2736px | **2736px** | unchanged | unchanged | n/a |

The portrait box is never wider than tall at any width in range, so no face is ever cropped
top-to-bottom. `/authors/` cards all still equal height; `/authors/<slug>/` back to `display:
list-item` with padding intact and no `.pbox` or `.txt`; journal pages untouched.

Two findings that changed the artifacts: the breakpoint moved 560px → 500px (design.md §3), and the
wrapped flex's inherited row gap had to be zeroed (design.md §3a).
