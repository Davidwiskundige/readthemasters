## Why

The site sits on one flat paper tone from the top of the page to the bottom, so nothing marks where
a page begins: the header is separated from the content only by a hairline. A soft, warm band of
colour behind the header — fading into the paper within the first screen — gives every page a head,
like the toned top edge of an old printed sheet, without touching the long flat stretch where the
reading happens. It was tried against the live site (a throwaway stylesheet on the built `dist/`) on
the catalog, timeline and a work page in both colour schemes, and tuned until light and dark read
as equally quiet.

## What Changes

- A warm gradient band is painted behind the top of every page: a linear fade from a band-top tone
  into `--bg`, with a faint radial glow in the accent colour centred just above the header. It is
  purely a page background — no element, markup or script is added.
- The band has a **fixed height** (16rem), not a height relative to the document, so it looks the
  same on a one-screen legal page and a forty-screen memoir, and scrolls away with the page.
- Two new colour tokens per scheme, `--band-top` and `--band-glow`:
  light `#f5f0e8` / accent at 5%, dark `#231e18` / accent at 8%.
- The header's bottom hairline becomes transparent where the band is present — the band's own tonal
  change now separates header from content. (The footer's top rule is unchanged.)
- In print the page background is dropped, so the band never prints as a grey wash.

## Capabilities

### New Capabilities

_None._

### Modified Capabilities

- `site-catalog`: adds a site-wide requirement for the header band — fixed height, the colour
  tokens per scheme, the contrast floor for text drawn on it, the transparent header rule, and no
  band in print.

## Impact

- `site/src/styles/global.css` only: the two tokens in `:root` and the dark `:root` block, the
  `body` background, the `header.site` border, and a print rule.
- No change to markup, layouts, data, pipeline, or client scripts. No new dependencies.
- Every page is affected (they all share `Base.astro` and `global.css`), so the check covers the
  catalog, timeline, search, an author page, a journal page and a work page, in both schemes and at
  phone width.
