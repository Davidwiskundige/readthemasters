## Why

Every client-side filter on the site counts correctly and hides nothing. A visitor who filters the
catalog sees "1 of 26 works" above all 26 cards. The same failure hits `/authors/` and `/journals/`.

The cause is one line of CSS. The filter scripts hide a row with the `hidden` attribute
(`c.hidden = !ok`), which only hides anything because the *user-agent* stylesheet carries
`[hidden] { display: none }`. Any author rule that sets `display` on the same element wins over the
UA rule regardless of specificity — and `.catalog .card`, `.authorlist .card` and
`.journallist .jrow` each set `display: flex` to seat a portrait or a title-led row beside their
text. The attribute lands on the element and changes nothing.

It arrived with `c942199` ("Put the author's portrait on every catalog card", 2026-09-13), which
turned the card into a flexbox. Before that, `.card` set no `display`, so `hidden` worked. Nothing
caught it: the site's three test suites cover pure functions in `src/lib/`, none of them touch DOM
or CSS, and the portrait change's own spec scenario asserted that portraits survive filtering
without asserting that filtering still filters.

## What Changes

- A single `[hidden] { display: none !important; }` rule enters `site/src/styles/global.css`,
  restoring the attribute's meaning against every author `display` rule, present and future.
- The `site-catalog` spec gains an explicit guarantee that a filtered-out row is **not rendered** —
  today the spec only promises the filter state and the live count, both of which kept working
  while the visible result was wrong.
- No JavaScript changes. The filter logic, the counts, the URL sync and the empty-state messages
  are all already correct; only the visual hide was defeated.

## Capabilities

### New Capabilities

None. This restores behavior the `site-catalog` capability already claims.

### Modified Capabilities

- `site-catalog`: the catalog's browse & filter requirement, and the author index's client-side
  filter, gain a requirement that a row excluded by a filter is removed from the rendered list —
  not merely marked — and that the rendered row count matches the displayed count. The journal
  index's search box, which the spec describes only as part of the index's presentation, is
  covered by the same requirement.

## Impact

- `site/src/styles/global.css` — one rule added.
- Behavior restored on three pages, all of which set the attribute correctly today:
  `site/src/pages/index.astro` (catalog facets, free text, year range),
  `site/src/pages/authors/index.astro` (name/bio search),
  `site/src/pages/journals/index.astro` (journal search).
- Unaffected: the work page's text-panel tabs, the search page's mode panels and its formula
  preview all use `hidden` on elements with no author `display` rule, so they work today and
  continue to.
- No change to the corpus, the pipeline, the copyright gate, or CI.
