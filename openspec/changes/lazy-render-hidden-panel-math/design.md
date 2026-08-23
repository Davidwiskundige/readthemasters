## Context

Three things on the work page currently run over the whole document regardless of what is visible:

| step | scope today | after `fix-fitdisplaymath-layout-thrashing` |
|---|---|---|
| `renderMathInElement` | every `.text` panel + significance + heading | unchanged — still typesets hidden panels |
| `fitDisplayMath` | skips `clientWidth === 0`, re-runs on reveal | already lazy |
| deep-link scroll | once on load, once on `document.fonts.ready` | unchanged |

So the fitting pass is already visibility-aware and the render pass is not. This change closes that
gap, using the same trigger the fitting pass uses.

The relevant machinery already in place (`[id].astro`):

- Panels are `<section class="text" data-panel="…" hidden>`; the tabs script flips `hidden`
  (`[id].astro:270-271`), and `applyHash()` flips it programmatically for a deep link and then
  scrolls (`[id].astro:281-291`).
- `panelWatch`, a `MutationObserver` on each panel's `hidden` attribute, re-fits on reveal
  (`[id].astro:422-424`). It exists precisely because the two scripts are bundled together and the
  bundler may emit them in either order, so nothing may depend on a click listener's registration
  order.
- `document.fonts.ready` re-fits and re-applies the deep-link scroll (`[id].astro:403-408`),
  because typesetting reflow moves the anchor.

Constraints:

- Rendering must precede fitting for a given panel — fitting measures rendered KaTeX.
- Correctness must not depend on which of the page's two scripts the bundler emits first. That
  assumption already broke once, in the previous change.
- Anchors (`p-<n>`, `<lang>-p-<n>`) exist in the served HTML before any rendering, so
  `getElementById` resolves them at any time; only their *position* depends on typesetting.

## Goals / Non-Goals

**Goals:**

- Halve KaTeX's load-time cost on a bilingual work by not typesetting the panel that is not shown.
- Keep the reader's eventual experience identical, including deep links landing on the right line.
- Typeset each panel at most once, however often tabs are switched.
- Stay robust to script ordering, as the fitting pass now is.

**Non-Goals:**

- Reducing the cost of the *visible* panel — that is build-time pre-rendering (backlog #18) or
  viewport-lazy rendering (backlog #19 item 4).
- Changing delimiters, `throwOnError`, or anything about how a formula is typeset.
- Deferring the significance note or page heading; both are always visible and small.
- Pre-warming the hidden panel during idle time. It would give back much of the saving on the very
  devices that need it most, and the on-reveal cost is a deliberate, user-initiated wait. Worth
  revisiting only if opening a tab measures badly.

## Decisions

### Reuse the existing `panelWatch` observer rather than the tab click

The observer already fires exactly when a panel becomes visible, from a click *or* from
`applyHash()`. Hanging the lazy render off it means one trigger for both "render it" and "fit it",
in the right order, with no new coupling to the tabs script. The alternative — a click listener —
is what the previous change had to remove, because bundling reordered it ahead of the panel flip.

Concretely the observer callback becomes: for each panel that is now visible and not yet typeset,
render it; then fit the document as it already does.

### Drive the initial pass from current visibility, not from "the first panel"

The initial render pass selects panels that are visible *at that moment*, rather than assuming the
original-language panel is the open one. If the bundler emits the tabs script first, `applyHash()`
may already have opened a translation panel for a deep link before this script runs; keying off
actual visibility is correct either way, and needs no knowledge of which script ran first.

`.significance` and `.workhead` are always visible and are rendered unconditionally, as now.

**Alternative considered — render `[data-panel]:not([hidden])` by selector only.** Equivalent for
the panels, but the significance note and heading are not panels, so the pass still needs to handle
them separately; keeping one explicit list is clearer than two selectors that must stay in sync.

### Mark "already rendered" on the element itself

A flag stored per panel element (a `WeakSet` in the module, or a data attribute) makes the render
idempotent. Tab switching then costs nothing after the first reveal, and the observer callback stays
safe to fire on any attribute mutation, including a panel being hidden again.

Using the element rather than the language code avoids assuming panels are unique per language or
that a work has exactly two.

### Re-apply the deep-link scroll after a lazy render

This is the sharp edge. `applyHash()` flips the panel and calls `scrollIntoView()` synchronously;
the observer's callback runs afterwards as a microtask, so the scroll happens against an untypeset
panel and every formula that then renders above the target pushes it away. The `fonts.ready` handler
re-scrolls for exactly this reason, but it cannot be relied on here: with fonts already cached it
can resolve before the lazy render, and it fires once rather than per reveal.

So after rendering a panel that contains the current hash target, re-apply the same scroll the
`fonts.ready` path does. The existing guard — only scroll when the target is not inside a hidden
panel — carries over unchanged.

**Alternative considered — render the panel synchronously inside `applyHash()` before it scrolls.**
That would require the tabs script to know about the math script, reintroducing exactly the
cross-script coupling this design is avoiding.

## Risks / Trade-offs

- **A deep link lands on the wrong line** → the change re-scrolls after a lazy render, and the test
  plan opens a `#<lang>-p-<n>` link directly (the shape search results produce) and checks the
  anchor is in view, rather than only checking that the panel opened.
- **Opening the second tab now costs a visible pause** where it used to be instant — the work moved
  rather than vanished. On the Abel page that is roughly half of the current load cost, paid only by
  readers who actually open the translation. Measure it; if it reads as broken rather than slow,
  idle pre-warming is the fallback, at the cost of some of the saving.
- **The observer callback now does more work** and fires on every `hidden` mutation, including
  hiding. The render step is guarded by both "is visible" and "not yet rendered", so hiding a panel
  does no work, and the fit call is unchanged from today.
- **Screen readers reach a panel's MathML only after it is opened** — acceptable because a
  `display:none` panel is already outside the accessibility tree; nothing reachable regresses.
- **The saving is zero for single-language works** and for readers who open both tabs; it is
  proportional to how much of the corpus is bilingual. Abel is the worst case and the motivating
  one, so the measurement should be taken there.
