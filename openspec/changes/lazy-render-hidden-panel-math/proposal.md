## Why

The work page renders every panel's math on load, including the translation panels that are
`hidden` and that most readers never open:

```js
document.querySelectorAll('.text, .significance, .workhead').forEach((el) =>
  renderMathInElement(el, { … }));            // [id].astro:346 — all panels, visible or not
```

On `abel-1841-fonctions-transcendantes` that is 3,162 KaTeX elements where 1,581 would do — the
French original and its English translation carry ~665 display equations each, and exactly one panel
is on screen. Half of KaTeX's typesetting is spent on a panel nobody is looking at.

With `fix-fitdisplaymath-layout-thrashing` (archived 2026-08-23) removing the measuring pass as a
bottleneck, KaTeX's own typesetting is now the entire remaining cost of a long work: ~5 s of blocked
main thread at phone width on the Abel page. This is PLAN.md §9 backlog #19 fix 2 — the cheapest
remaining lever, and the last one that does not require re-architecting how math is produced
(fix 3 is build-time pre-rendering, backlog #18).

The fitting pass already works this way: it skips zero-width elements and re-runs when a panel is
revealed. This change brings the render pass in line with it.

## What Changes

- Render math on load only in the panels that are actually visible, plus the always-visible
  significance note and page heading. A `hidden` panel is left as raw LaTeX until it is revealed.
- Render a panel's math the first time it becomes visible, reusing the `MutationObserver` on
  `[data-panel]`'s `hidden` attribute that the previous change already installed for re-fitting.
  Rendering must happen *before* the fit for that panel, since fitting measures rendered output.
- Render each panel at most once, tracked per element rather than by tab identity, so repeated tab
  switching does not re-typeset.
- Re-apply the deep-link scroll after a lazy render. A search result linking to `#en-p-236` flips
  the panel and scrolls to the anchor before the newly revealed panel has been typeset; typesetting
  then changes every subsequent line's height and the reader lands in the wrong place. The page
  already re-scrolls for the equivalent font-loading reflow (`[id].astro:403-408`); this needs the
  same treatment.
- Decide the initial pass from *current* panel visibility rather than assuming the first panel is
  the open one, so it stays correct whichever order the bundler emits the page's two scripts in —
  a deep link may already have flipped a translation panel open before this script runs.
- No change to what a reader eventually sees: the same math renders with the same delimiters and
  `throwOnError: false`, only later for panels they open.

## Capabilities

### New Capabilities

None. This changes when existing behavior happens, not what the site does.

### Modified Capabilities

- `site-catalog`: the "Work page" requirement describes the panels and their math rendering. It
  gains the rule that a hidden panel's math is rendered on first reveal rather than on load, that
  each panel is typeset at most once, and that a deep link into a lazily-rendered panel still lands
  on its anchor.

## Impact

- **Code**: `site/src/pages/works/[id].astro` — the render call at line 346 and the `panelWatch`
  observer at lines 422-424. No new files; no change to `lib/fitmath.js`.
- **Search**: none. Both the Pagefind index and the formula index are built from the HTML at build
  time (`search`, `math-search`), and math spans are already `data-pagefind-ignore`, so what gets
  indexed does not depend on client-side rendering. Deep links from results are the reason for the
  re-scroll above, not an indexing concern.
- **Accessibility**: KaTeX's MathML output for a hidden panel arrives when the panel is opened. A
  hidden panel is `display:none` and already outside the accessibility tree and browser find, so
  nothing a reader could reach is degraded.
- **Dependencies**: none added. No build, CI, corpus, or copyright-gate surface is touched.
- **Risk**: moderate and concentrated in one place — the deep-link path, where the panel is revealed
  programmatically rather than by a click. That path is the main thing to verify, alongside "does
  the other tab still render correctly when opened".
- **Not in scope** (remain PLAN.md §9 backlog #19 / #18): build-time KaTeX pre-rendering, and
  viewport-lazy rendering within a panel.
