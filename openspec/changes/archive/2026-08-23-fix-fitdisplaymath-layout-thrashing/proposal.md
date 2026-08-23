## Why

The work page's display-math fitting pass (`fitDisplayMath` in `site/src/pages/works/[id].astro`)
interleaves DOM reads with DOM writes inside one loop over every `.katex-display` element. Each
write invalidates layout and each following read forces the browser to recompute it synchronously,
so the pass costs roughly two forced reflows *per equation* — and every one of those reflows is over
the whole document.

Measured on the live `abel-1841-fonctions-transcendantes` page (3,162 KaTeX elements across both
language panels, ~1,330 display equations), by replaying the page's own script over an off-screen
copy of its markup:

| Phase | Cost |
|---|---|
| `renderMathInElement` (KaTeX typesetting) | ~1.9 s |
| `fitDisplayMath` (this measuring pass) | **~3.1 s** |

The homegrown fitting pass costs *more than KaTeX's own typesetting*, and the two together block
`DOMContentLoaded` for ~9–11 s on that page. The network is not the cause — KaTeX's CSS, JS, and
fonts all finish downloading in ~1.2 s; the rest is pure main-thread compute. This is PLAN.md §9
backlog #19, fix priority 1: the cheapest and safest of the four identified levers, and the one
targeting the larger of the two measured costs.

## What Changes

- Restructure `fitDisplayMath` from one interleaved read/write loop into batched phases: read every
  equation's available width, then clear the layout classes on all of them, then measure every
  formula and tag, then apply all class changes from the recorded measurements. Two forced reflows
  total instead of two per equation.
- Preserve the existing read ordering exactly, so the decisions are bit-for-bit what they are today:
  available width is still sampled *before* the classes are cleared, and formula/tag widths still
  *after*, matching the current function's observable semantics.
- Keep the hidden-panel skip (`clientWidth === 0`) and every existing call site unchanged: the
  initial pass, the `document.fonts.ready` re-measure, the debounced `resize` handler, and the
  tab-click handler.
- Extract the wide/tag-below decision arithmetic into a pure, unit-testable helper so the rule
  ("formula wider than the column ⇒ `wide`; formula plus a tag's width on both sides wider than the
  column ⇒ `tag-below`") is pinned by tests rather than only by eye.
- No user-visible behavior change: the same equations receive the same `wide` and `tag-below`
  classes; only the cost of deciding that changes.

## Capabilities

### New Capabilities

None. This changes how an existing behavior is computed, not what the site does.

### Modified Capabilities

- `site-catalog`: the existing "Work page" requirement documents the display-math fitting behavior
  ("Which layout applies is decided by measuring the rendered formula, not by a viewport
  breakpoint"). It gains a constraint that this measuring pass batches its reads and writes so its
  cost stays proportional to the number of equations rather than to equations × forced reflows —
  turning today's ad-hoc implementation detail into a stated property that a future refactor cannot
  silently undo.

## Impact

- **Code**: `site/src/pages/works/[id].astro` (the inline `<script type="module">`, currently lines
  ~357–393) and a small new pure helper plus its test under `site/src/lib/`.
- **Tests**: one new `node --test` file alongside the existing `site/src/lib/tex.test.mjs`; the
  before/after timing is verified in a browser against a long work, since real layout measurement
  cannot be exercised under `node --test`.
- **Dependencies**: none added. No build, CI, corpus, or copyright-gate surface is touched.
- **Risk**: low and contained to one page's client script. The failure mode to watch is a changed
  `wide`/`tag-below` decision on some equation, which is why the change verifies old and new
  implementations agree on a real long page before landing.
- **Not in scope** (remain PLAN.md §9 backlog #19 items 2–4): skipping the hidden translation panel
  during KaTeX render, build-time math pre-rendering (#18), and viewport-lazy rendering.
