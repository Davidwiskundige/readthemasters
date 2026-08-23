## Context

Four changes have now touched this pass. It is worth being precise about what each removed, because
this one removes the last thing that scales with the length of a work:

| change | removed | left behind |
|---|---|---|
| `fix-fitdisplaymath-layout-thrashing` | ~2,660 forced reflows → 2 | still *measured* every equation |
| `lazy-render-hidden-panel-math` | typesetting the unseen panel at load | still typeset a whole panel on reveal |
| `viewport-lazy-equation-fitting` | measuring the whole panel | still *typeset* the whole panel |
| this change | typesetting the whole panel | — |

What exists to build on (`[id].astro`):

- `renderMath(el)` + a `typeset` WeakSet — typesets a region at most once, returns whether it did.
- `panelWatch` — a `MutationObserver` on each panel's `hidden` attribute, so panel reveal is
  *observed* rather than hung off a tab click. Both scripts on the page are bundled into one file and
  the bundler may order them either way; a click listener was inverted once and left a whole panel
  unfitted.
- `eqWatch` / `observeEquations` / `fitEquations` — viewport-driven fitting, already handling
  equations that appear late and equations that cannot yet be measured.
- `scrollToHash(deepOnly)` — the guarded deep-link scroll, which already distinguishes "a tab click
  rewrote the hash to `#en`" from "a search result points at `#en-p-236`".

Measurements behind the decision (production build, Abel, phone-width viewport):

- 13 of 1,581 formulas within three viewports of the top
- prototype: 39 ms script work at load, 4,584 DOM elements, unchanged 47 KB brotli
- pre-rendering instead: 13.4 MB HTML, 220 KB brotli, 381,991 DOM elements
- typesetting is ~20× dearer than the browser building the same elements natively (≈5,000 ms of
  JavaScript vs ≈250 ms of parse), which is why pre-rendering *works* but costs the wrong resource

## Goals / Non-Goals

**Goals:**

- Make load and tab-switch cost proportional to a screenful, not to the length of the work, so
  adding a longer text never reintroduces this.
- Stop the unresponsive-script dialog on a mid-range phone.
- Keep every formula the reader reaches correctly typeset and correctly fitted.
- Keep deep links landing on their anchor.

**Non-Goals:**

- Build-time pre-rendering (#18) — measured and rejected for this purpose.
- Eliminating the ~2 s panel-switch layout cost; that is the browser laying out a revealed panel.
- Removing the settle-on-jump-to-bottom; it is accepted and documented.
- Any change to the fitting rule or `lib/fitmath.js`.

## Decisions

### Observe math spans, not blocks or panels

The unit of laziness is the individual `span.math` / `span.mathblock` that `tex.js` already emits.
Observing paragraphs or panels would either re-typeset regions or force awkward nesting rules
(a paragraph containing three formulas is one observation target but three units of work). Spans are
the smallest thing KaTeX can be pointed at, they already exist in the markup, and `renderMath`'s
WeakSet keys on the element, so idempotence comes for free.

The cost is many observation targets — ~3,162 on Abel. `IntersectionObserver` is built for exactly
this (infinite-scroll lists are larger), and targets in a `display:none` panel never fire, so the
hidden panel costs nothing until revealed.

**Alternative considered — observe block elements** (paragraphs, list items). Fewer targets, but it
reintroduces the nesting question and typesets formulas the reader has not reached whenever a block
is long. Not obviously cheaper, definitely more rules.

### This supersedes the panel-level rule rather than joining it

`lazy-render-hidden-panel-math` established "typeset only panels the reader can see". Under a
viewport-driven rule that is no longer a separate statement: a hidden panel has no layout, so nothing
inside it is ever near the viewport. Keeping both would leave the spec with two overlapping
statements about when math is typeset, which is precisely how requirements drift apart.

So the spec gets **one** rule, and the panel-reveal hook survives with a different body: on reveal,
start observing that panel's spans. It is still needed — spans in a hidden panel never fire — and it
must stay driven by the observed `hidden` change, not by the tab click, for the bundling reason
above.

### Deep links need more than the prototype's one-shot re-scroll

`applyHash()` scrolls to the target synchronously while the surrounding formulas are still raw
LaTeX. They then typeset and grow, and the target moves. The prototype re-scrolls once after the
first typesetting batch, which happens to work at load and is not good enough as a rule: several
batches can land after the scroll, and the reader can arrive at a deep link at any time via
`hashchange`.

The shape that fits the existing machinery: after a typesetting batch, if the current hash target
lies inside the region just typeset, re-apply `scrollToHash(true)`. That ties the correction to the
thing that moved the target rather than to a moment in the page's life, and reuses the existing
guard that stops a tab click's `#en` from being treated as a jump request.

### The load-time pass keeps its eager cases

`.significance` and `.workhead` stay eager: both are always visible, both are small (2 and 6 formulas
on `euler-1761`), and making them lazy would risk the page title rendering late.

## Risks / Trade-offs

- **A deep link lands in the wrong place** → tie the re-scroll to batches that touched the target's
  region, and verify on a real device at several anchors, cold and warm. This machinery has broken
  once per change in this series; assume it will try again.
- **Formulas visibly typeset as the reader scrolls** → observe with a margin of at least one viewport
  so they are ready before arrival. The prototype used 150 % and the maintainer reported it felt
  fine; a jump straight to a distant part of the document has no runway and will always settle
  briefly.
- **Layout settle on jump-to-bottom is accepted, not fixed** → reserving space for display equations
  was prototyped and does not fix it, because the drift comes mostly from ~900 inline formulas per
  panel each gaining a little height. State it in the spec so nobody re-derives this.
- **Find-in-page matches raw LaTeX** in untypeset regions. Nothing to do about it without typesetting
  eagerly, which is the thing being removed. Worth stating rather than discovering.
- **~3,162 observer targets** on the longest work → measure that registration cost; if it is
  material, fall back to observing block elements.
- **Verification cannot be done by the agent.** The headless pane suspends `IntersectionObserver`,
  `requestIdleCallback`, `requestAnimationFrame` and scroll events; only `setTimeout` fires. Every
  behavioural check in this change needs the maintainer's phone or a real desktop browser, and the
  task list should say so rather than pretending otherwise.
