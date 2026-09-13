## 1. Thumbnail generator

- [x] 1.1 Add `pipeline/make_portrait_thumb.py`: for one slug or `--all`, read `corpus/authors/<slug>/portrait.jpg`, cover-fit to 138 × 172 (centre-x, 18%-from-top crop), save as `portrait-thumb.jpg` at quality 82, optimized and progressive. Import Pillow lazily with an install hint on ImportError, matching `pipeline/prepare_pages.py`.
- [x] 1.2 Make it idempotent and explicit: skip an existing derivative unless `--force`, so a hand-cropped thumbnail committed by a contributor is never silently overwritten.
- [x] 1.3 Note Pillow's second optional use in `pipeline/requirements.txt`, alongside the existing `prepare_pages.py` note. Do not add a hard dependency.
- [x] 1.4 Run it over all 13 authors with a committed portrait and eyeball each result; hand-crop and commit over any whose face lands badly. Confirm the set totals roughly 66 KB.

## 2. Build pipeline

- [x] 2.1 In `pipeline/build_site_data.py`, extend `resolve_portrait()` to derive the sibling name from `portrait["file"]` (stem + `-thumb` + suffix), copy it into `site/public/authors/<slug>/` when present, and set `thumb_url` on the returned dict.
- [x] 2.2 Fall back to the full portrait's `url` for `thumb_url` when the derivative is missing, and emit a build warning naming the slug.
- [x] 2.3 Leave `pipeline/validate.py` untouched — a missing derivative is not a gate condition.
- [x] 2.4 Add cases to `pipeline/tests/test_authors.py`: derivative present (copied, `thumb_url` points at it), derivative absent (`thumb_url` equals `url`, warning emitted), portrait itself absent (unchanged existing behavior), and a non-`.jpg` portrait filename resolving its sibling correctly.
- [x] 2.5 Run `python -m pytest pipeline/tests -q` and confirm green.

## 3. Index card markup

- [x] 3.1 In `site/src/pages/authors/index.astro`, restructure the card into a portrait box plus a `.body` wrapper holding the existing `<h3>` and `.meta`, keeping `data-search` on the `li` so the client-side filter is unaffected.
- [x] 3.2 Render the thumbnail as `<img>` with `src={a.portrait.thumb_url}`, `alt=""`, `width="69"`, `height="86"` and `loading="lazy"`.
- [x] 3.3 Render the monogram placeholder when `a.portrait?.thumb_url` is absent: the initial of the last whitespace-separated token of `a.name`, with `aria-hidden="true"`.
- [x] 3.4 Verify the card's single link target and hover behavior are unchanged.

## 4. Styling

- [x] 4.1 Add `.authorlist .card` rules to `site/src/styles/global.css`: `display:flex`, `padding:0`, `overflow:hidden`, `align-items:stretch`, `gap:.9rem`.
- [x] 4.2 Add `.authorlist .card .pbox` (`flex:0 0 69px`, `position:relative`, `background:var(--border)`) and its `img` (`position:absolute`, `inset:0`, `width/height:100%`, `object-fit:cover`, `display:block`).
- [x] 4.3 Add `.authorlist .card .body` with `padding:.9rem 1.1rem .9rem 0` and `min-width:0` so long names can shrink the flex item.
- [x] 4.4 Style `.authorlist .card .pbox.mono`: centred initial in `var(--muted)` on `var(--border)`, sized to read as a placeholder rather than a heading.
- [x] 4.5 Confirm every new selector is prefixed `.authorlist .card`, and that the catalog, journal and author-detail work lists render unchanged.
- [x] 4.6 Check both light and dark themes — `var(--border)` is the placeholder ground in both and must keep the initial legible.

## 5. Verification

- [x] 5.1 Run `npm run dev` in `site/`, load `/authors/`, and measure every card's height in the browser; assert a single distinct value at 1024px width, matching the pre-change height of 86px.
- [x] 5.2 Measure at 375px. Measured: thirteen cards at 87px and two (Fagnano, Leibniz) at 115px. Fagnano already wrapped before the change, so Leibniz is the only regression — one card, not the two predicted; Jacobi fits at 226px in a 226px column. Correction recorded in design.md decision 7.
- [x] 5.3 Confirm total image transfer for `/authors/` is in the tens of KB, not ~1 MB, via the network panel.
- [x] 5.4 Confirm Émile Picard's card renders the monogram and that his text column aligns with every other card.
- [x] 5.5 Type in the search box and confirm filtering, the live count and the empty state still work.
- [x] 5.6 Check a screen reader or the accessibility tree: each row announces the author's name once, not twice.
- [x] 5.7 Run `npm run build` and confirm the derivatives land in `dist/authors/<slug>/`.

## 6. Wrap-up

- [x] 6.1 Update `openspec/specs/site-catalog/spec.md` with the modified **Author pages** requirement and archive the change (`/opsx:archive`).
- [x] 6.2 Open a pull request with a DCO `Signed-off-by` line: Davidwiskundige/readthemasters#53, stacked on the six-portraits commit in one PR.
