## Why

Books number their front matter in lower-case roman numerals, and a preface is often part of the
author's text. Klein's 1882 *Ueber Riemann's Theorie der algebraischen Functionen* has a Vorrede on
pp. iii–vi and an Inhalt on pp. vii–viii. Today `\origpage` works only with digits in practice:
the LaTeX macro takes any argument, but the site's page-anchor transform (`site/src/lib/tex.js`),
the formula index (`site/src/lib/mathindex.js`, which casts the page with `Number()`), the search
page's page lookup (`site/src/pages/search.astro`) and the gate's page-order check
(`pipeline/validate.py`) all match `\d+`. A marker such as `\origpage{iii}` would print as literal
TeX in the reader, index formulas under page `NaN`, and be invisible to the order check. The only
way around it was to leave the front matter untranscribed, which drops the author's own text.

## What Changes

- `\origpage{…}` SHALL accept a lower-case roman numeral (`i`, `ii`, … `viii`, …) as well as an
  arabic number. Printed page numbers are copied as printed; roman stays roman.
- The reader renders a roman marker exactly like an arabic one: `page iii`, anchor `p-iii` (and
  `en-p-iii` in a translation panel).
- The formula index keeps the page as printed — a string for a roman page — and the search page
  resolves `p-iii` anchors like `p-12` ones.
- The gate's page-marker check treats roman and arabic as two runs: roman markers MUST come before
  the first arabic marker, and within each run the existing rules hold (ascending, no duplicates;
  a gap is a warning).
- `klein-1882-riemanns-theorie` adds its Vorrede and Inhalt (pp. iii–viii) as the first user.

## Impact

- `site/src/lib/tex.js`, `site/src/lib/mathindex.js`, `site/src/pages/search.astro`,
  `pipeline/validate.py`, with tests in `site/src/lib/tex.test.mjs`, a new mathindex test, and
  `pipeline/tests/test_page_markers.py`.
- No existing work changes: every current marker is arabic and renders exactly as before.
