## Why

`/authors/` is the one page on the site that lists people rather than texts, and it shows none of
them. Every author page already carries a public-domain portrait — 13 of the 14 authors have one
committed under `corpus/authors/<slug>/`, hosted at build time, and rendered at 120px on
`/authors/<slug>/`. The index reads the very same `authors` array out of `works.json`, portrait URL
included, and throws it away. A reader scanning the list gets a column of names where a column of
faces would let them find Euler at a glance.

The reason to do it now is that it costs almost nothing. The index card is 969 × 86 px and uses
roughly 70 of its 935 usable pixels of width; every portrait in the corpus is portrait-orientation
at aspect ratio 0.68–0.87, clustered on 0.80. A full-bleed 69 × 86 thumbnail drops into the card's
left edge, contributes zero to its height, and leaves the text column with more room than it uses.
The constraint driving this proposal is the reader's: the list must stay as fast to scan as it is
today, so **no card may get taller on desktop** and the page may not get appreciably heavier.

## What Changes

- **The authors index shows a portrait per card** — a full-bleed 69 × 86 thumbnail flush to the
  card's left edge, ahead of the name, dates and work count. It is decorative (`alt=""`): the
  author's name sits in the adjacent heading, so announcing it twice only slows a screen reader
  down. The whole card keeps its existing single link target.
- **Card height is unchanged on desktop.** The image lives in a fixed-width flex item and is
  absolutely positioned inside it, so its intrinsic aspect ratio cannot push the card. All cards
  measure 86px before and after. On a 375px phone the narrower text column wraps two long names
  (Leibniz, Jacobi) onto a second line — accepted deliberately, in preference to shrinking the
  faces on the screen where they are already smallest.
- **Thumbnail derivatives are committed to the corpus** as `corpus/authors/<slug>/portrait-thumb.jpg`
  — 138 × 172 (2× the display box), face-biased crop, progressive JPEG. The full-size portraits
  total 1,040 KB, which is not a defensible payload for images drawn at 69px; the derivatives total
  66 KB. **No new build-time dependency**: the bytes are committed like the portraits themselves,
  so CI keeps installing nothing but PyYAML.
- **`resolve_portrait()` finds the thumbnail by convention, not by schema** — given
  `portrait.file: portrait.jpg` it looks for `portrait-thumb.jpg` beside it, copies both into
  `site/public/authors/<slug>/`, and adds `thumb_url` to the portrait dict. A missing derivative
  falls back to `url` and warns at build time. This deliberately avoids a new `work.yaml` field:
  the `portrait` block is duplicated in every work.yaml of a given author, so any new key would
  have to be edited in N places and kept in sync.
- **A new `pipeline/make_portrait_thumb.py`** generates the derivative from the committed portrait.
  Pillow is imported lazily and listed as optional, exactly like `prepare_pages.py` — a contributor
  adding an author runs it once and commits the result. Because the output is an ordinary committed
  file, a portrait whose automatic crop lands badly can simply be cropped by hand and committed
  instead; the tooling has no opinion about where the bytes came from.
- **Authors with no portrait get a monogram placeholder** occupying the same 69 × 86 footprint —
  the initial of the author's last name, set in `var(--muted)` on `var(--border)`. Without it the
  one portrait-less author's text would sit flush against the card edge and break the alignment of
  the whole column. `Émile Picard` is the case in hand.
- **The new CSS is scoped to `.authorlist .card`**, never bare `.card`. The card class is shared
  with the catalog and journal pages, and `site/src/styles/global.css` already carries a comment
  warning about precisely this.

Not in scope: portraits on catalog cards or work-page headers, and any change to the 120px portrait
on the author detail page, which keeps serving the full-size image with its `credit` caption and
Commons `source` link. The index card has no room for attribution and does not need it — it links
through to the page that carries it.

## Capabilities

### New Capabilities

None. The change extends one existing requirement.

### Modified Capabilities

- `site-catalog`: the **Author pages** requirement currently specifies the index as listing "every
  author alphabetically with dates and work count". It gains the portrait thumbnail, the fixed card
  height that the thumbnail must respect, the monogram fallback, and the convention by which
  `build_site_data.py` locates and hosts the derivative alongside the full portrait.

## Impact

- `corpus/authors/<slug>/portrait-thumb.jpg` — 13 new committed derivatives, ~66 KB in total.
- `pipeline/make_portrait_thumb.py` (new) — contributor-run generator, optional Pillow.
- `pipeline/build_site_data.py` — `resolve_portrait()` copies and returns the derivative.
- `pipeline/tests/test_authors.py` — coverage for the fallback, the convention, and the copy.
- `pipeline/requirements.txt` — a comment noting Pillow's second optional use. No new hard dep.
- `site/src/pages/authors/index.astro` — card markup.
- `site/src/styles/global.css` — `.authorlist .card` rules and the monogram.
- `pipeline/validate.py` — untouched. The gate rules on copyright, not on cosmetics; a missing
  thumbnail degrades to the full image rather than failing a build.
