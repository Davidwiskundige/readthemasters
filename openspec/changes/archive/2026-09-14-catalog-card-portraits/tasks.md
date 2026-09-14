## 1. Baseline measurements

- [x] 1.1 Record catalog card heights and total list height at 1280px and 375px before any edit, from a local build — the numbers the change is judged against (design.md records 2493px / 4621px from production)
- [x] 1.2 Record `/authors/` card heights at 1280px before any edit (expected: 86px, every card) — the regression baseline for the shared `.pbox` extraction

Baseline, local build, 18 works (production had 17 when design.md was written):

| surface | before | after |
|---|---|---|
| catalog @1280px (cards 760px) | 2601px total; heights 108 / 141 median / 219 | 2736px (+5.2%); range still 108–219 |
| catalog @375px (cards 335px) | 4890px total | 5872px (+20.1%); cards 219–428px |
| `/authors/` @1280px | 1204px total; all 14 cards exactly 86px | 1204px; all 14 still exactly 86px |

The image adds no height: the range is unchanged (108–219), and every added pixel comes from a
title wrapping. Two cards gained a line at 1280px, one of them the monogram card (Picard, 108→136).

## 2. Data join

- [x] 2.1 In `site/src/pages/index.astro` frontmatter, build a `slug → thumb_url` map from the imported `works.json`'s `authors` array
- [x] 2.2 Add the same last-initial helper the author index uses for the monogram fallback, keeping the surrogate-pair-safe spread
- [x] 2.3 Confirm no change to `pipeline/build_site_data.py`, `work.yaml`, or `works.json`'s shape

## 3. Card markup

- [x] 3.1 Wrap each catalog card's existing content in a `.body` div and prepend the portrait box, mirroring the author index's structure
- [x] 3.2 Render `.pbox` with the first author's `thumb_url` when present, `.pbox.mono` with their last initial when not
- [x] 3.3 Wrap the box in a link to the work, with `aria-hidden="true"` and `tabindex="-1"`; image gets `alt=""`, `width="69"`, `height="86"`, `loading="lazy"`
- [x] 3.4 Leave the card's `data-*` filter/sort attributes on the `li` itself, so filtering and sorting are untouched

## 4. CSS

- [x] 4.1 Lift the portrait box's visual rules out of `.authorlist .card` into a shared `.pbox` block (absolutely positioned `object-fit: cover` image; monogram placeholder), leaving per-list layout where it is
- [x] 4.2 Add `.catalog .card` layout rules (NOT `.works .card` — `ul.works` is also /authors/<slug>/'s work list; the catalog's list carries an extra `catalog` class): `display:flex`, `align-items:stretch`, `padding:0`, `overflow:hidden`, `gap:.9rem`; `.pbox` at `flex:0 0 69px`; `.body` with `padding:.9rem 1.1rem .9rem 0` and `min-width:0`
- [x] 4.3 Verify no bare `.card` rule was changed, and that the rules added are scoped to `.catalog .card` or the shared `.pbox`

## 5. Verification

- [x] 5.1 Build and measure: no catalog card is taller than its text requires (compare against 1.1); record the new totals at 1280px and 375px
- [x] 5.2 Measure `/authors/` again — every card still 86px at desktop width (compare against 1.2)
- [x] 5.3 Load `/authors/<slug>/` and a journal page: work lists unchanged, no portraits, no layout shift
- [x] 5.4 Check every one of the 14 portraits at the tallest card height; hand-crop and commit over any whose face is lost to the crop
- [x] 5.5 Confirm the portrait-less author's card (Picard) shows the monogram and stays aligned
- [x] 5.6 Confirm the multi-author work (`castelnuovo-enriques-1897-surfaces-algebriques`) shows one portrait and still links both authors
- [x] 5.7 Filter by a facet and change the sort order; portraits survive the DOM reordering
- [x] 5.8 Keyboard-tab through a card: one stop for the title, one per author link, none for the portrait; check the same with a screen reader or the accessibility tree
- [x] 5.9 Check a title carrying KaTeX math: the card re-crops rather than reflowing the list when the math renders
- [x] 5.10 Check both colour schemes — the monogram's `--border` background and `--muted` initial in dark mode
- [x] 5.11 Confirm the page requests `portrait-thumb.jpg`, not the full portraits, and that network weight is unchanged for a visitor arriving from `/authors/`

## 6. Ship

- [x] 6.1 Run `python pipeline/validate.py` and the site build; both clean
- [x] 6.2 Open the PR with before/after screenshots at 1280px and 375px, and the measured list-height deltas
- [x] 6.3 After merge, fold the delta spec into `openspec/specs/site-catalog/spec.md` and archive the change
