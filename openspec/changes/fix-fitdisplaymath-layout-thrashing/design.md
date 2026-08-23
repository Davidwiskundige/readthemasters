## Context

`fitDisplayMath` decides two CSS classes per display equation, from `site/src/pages/works/[id].astro`:

- `wide` — the formula is wider than its column, so `.katex-display.wide > .katex` left-aligns it and
  horizontal scrolling starts at the beginning of the formula instead of mid-way through it.
- `tag-below` — the `\tag{n}` cannot sit beside the formula, so it drops to its own right-aligned
  line beneath (`global.css:177-180`).

Today it does that in a single loop whose body reads layout, writes a class, reads layout again,
writes again:

```js
const room = eq.clientWidth;                     // READ
eq.classList.remove('wide', 'tag-below');        // WRITE  → invalidates layout
const math = [...].reduce(… getBoundingClientRect().width …); // READ → forces reflow
if (math > room) eq.classList.add('wide');       // WRITE  → invalidates again
const tagW = tag ? tag.getBoundingClientRect().width + 8 : 0; // READ → forces reflow
if (tag && math + 2 * tagW > room) eq.classList.add('tag-below'); // WRITE
```

Each read that follows a write forces a synchronous full-document layout. With ~1,330 display
equations on `abel-1841-fonctions-transcendantes` that is ~2,660 forced reflows over a document
holding 3,162 KaTeX subtrees — measured at ~3.1 s, more than KaTeX's own ~1.9 s of typesetting.

Constraints:

- The function runs from four call sites (initial pass, `document.fonts.ready`, debounced `resize`,
  tab click) and must stay a drop-in replacement for all of them.
- It runs in the browser as an inline module in a `.astro` file, so anything left there is not
  reachable by `node --test`.
- Real layout measurement (`getBoundingClientRect`) cannot be exercised in the existing test harness
  — jsdom has no layout engine and returns zeros — so correctness of the *measuring* half has to be
  established in a browser, not in unit tests.

## Goals / Non-Goals

**Goals:**

- Remove the per-equation forced reflow: the pass should cost a small constant number of layout
  recalculations regardless of how many equations a work has.
- Produce byte-identical `wide` / `tag-below` outcomes to the current implementation.
- Make the decision rule unit-testable, so the arithmetic is pinned by tests even though the
  measurement is not.
- Keep the change contained to one page script plus one small helper.

**Non-Goals:**

- Reducing KaTeX's own ~1.9 s typesetting cost — that is backlog #19 items 2–3 (skip the hidden
  panel; build-time pre-rendering).
- Deferring work off the critical path (viewport-lazy measurement, `requestIdleCallback`) — backlog
  #19 item 4.
- Changing which equations get which class, the CSS, or the four call sites.
- Removing the second pass on `document.fonts.ready`; it is genuinely required, because KaTeX's
  fonts change formula metrics when they land. It becomes cheap once batched.

## Decisions

### Four phases, not two

The obvious "read everything, then write everything" split is not sufficient here, because the
measurement is only valid once the previous run's classes are cleared — `wide` and `tag-below`
change how the formula and its tag are laid out. The clear is itself a write that sits *between*
two reads. So the pass becomes four phases over the whole collection instead of four steps per
element:

```
Phase A  read   clientWidth for every equation            → keep the ones with room > 0
Phase B  write  clear 'wide','tag-below' on those          → one layout invalidation, batched
Phase C  read   formula width + tag width for each         → one forced reflow, then all reads free
Phase D  write  add 'wide' / 'tag-below' from phase C      → invalidates once; browser repaints later
```

Two forced reflows for the whole pass, versus two per equation today.

**Alternative considered — clear all classes up front, then a single read phase (three phases, one
reflow).** Rejected: it would clear classes on hidden-panel equations too, which today keep theirs.
The extra saving is one reflow out of two, i.e. nothing next to the ~2,660 removed, and it would
make the change a behavior change rather than a pure refactor.

### Phase A reads `clientWidth` *before* the clear, preserving today's exact semantics

Today `room` is sampled while the previous run's classes are still applied. `.katex-display` carries
`overflow-x: auto` unconditionally, so in principle a scrollbar's presence — and therefore
`clientWidth` — can differ between the classed and cleared states. Rather than reason about whether
that can actually bite, phase A samples at exactly the same moment the current code does. The
refactor then cannot change a decision even in the corner cases.

**Alternative considered — read `clientWidth` after the clear** (arguably "more correct", since the
other measurements are taken in the cleared state). Rejected for this change: it is a behavior
change wearing a refactor's clothes. If the current ordering is genuinely wrong, that is its own
proposal, with its own before/after evidence.

### Pure decision helper in `site/src/lib/`, DOM orchestration stays in the page

The arithmetic — given available width, formula width, and tag width, which classes apply — moves to
a small pure function exported from `site/src/lib/` and imported by the page script. It has no DOM
dependency, so `node --test` can pin it (including the `+ 8` gutter and the `2 ×` tag allowance for a
centred formula needing clearance on both sides). The reads, writes, and phase ordering stay in
`[id].astro`, where they belong.

**Alternative considered — extract the whole `fitDisplayMath` into a module and test it with jsdom.**
Rejected: jsdom reports zero for every `getBoundingClientRect`, so such a test would assert nothing
about the behavior that matters while implying it had been covered. Worse than no test.

### The page script becomes bundled, which forces the tab re-measure off the click

Importing the helper only works if Astro processes the script, and Astro leaves a `<script
type="module">` inline — its imports then resolve against the page URL, so `../../lib/fitmath.js`
404s from `/works/<id>/`. Dropping `type="module"` (the same form `search.astro` already uses to
import `lib/mathnorm.js`) makes Astro bundle it and the import resolve correctly.

That has a consequence found during verification, not predicted here: bundling merges this script
with the tabs script at the top of the page into a single hoisted file, and the bundler emitted this
one **first**. Previously the tabs script was hoisted into `<head>` while the math script stayed
inline in the body, so the tab-flip listener was always registered before the re-measure listener and
therefore always ran first. Inverted, the click-time re-measure ran while the incoming panel was
still `hidden`, skipped all 665 of its equations on `clientWidth === 0`, and left the panel unfitted.

So the re-measure no longer hangs off the tab click. A `MutationObserver` on each panel's `hidden`
attribute reacts to the flip itself, which by construction cannot run before it. This is
order-independent, survives any future bundling decision, and additionally covers the programmatic
flip that a deep link performs via `applyHash()`. Only the panels' own attributes are observed
(no `subtree`), so the classes the pass writes on descendant equations cannot retrigger it.

**Alternative considered — `requestAnimationFrame` on the click.** Correct for real users but it
cannot be verified in a headless/background document, where rAF callbacks are suspended; observing
the attribute works everywhere and expresses the actual dependency ("measure when the panel becomes
visible") rather than a timing guess.

**Alternative considered — keep the script inline and serve the helper from `public/`.** Preserves
the original ordering exactly, but costs an extra unbundled, unminified request for a ~600-byte file
and leaves the underlying fragility (correctness depending on script order) in place.

### Equivalence is verified in a real browser, against a real long work

Because the risky half cannot be unit-tested, the change is gated on an explicit differential check:
run the old and new implementations over the same fully-rendered page and assert they assign
identical classes to every equation, on `abel-1841-fonctions-transcendantes` (the worst case, and
the page the measurements came from) at both a wide and a narrow viewport. The same harness produces
the before/after timing.

## Risks / Trade-offs

- **A batching mistake silently changes an equation's layout** → the differential check above compares
  every equation's resulting classes between implementations, rather than spot-checking by eye; a
  mismatch on any equation blocks the change.
- **Phase C holds one array of measurements for every equation** → a few thousand small objects on the
  worst page in the corpus; negligible next to the 3,162 KaTeX subtrees already in that DOM.
- **The pure helper drifts from the page's call site** (someone changes the arithmetic in one place) →
  the helper is the only definition of the rule; the page performs no arithmetic of its own, so there
  is nothing to drift from.
- **The win is real but partial** → after this, KaTeX's ~1.9 s typesetting remains and still blocks the
  page. Expectation-setting matters: this removes the larger of the two costs, it does not make the
  Abel page instant. Items 2–4 of backlog #19 remain open, and the same measurement harness will show
  what is left.
- **Measurements are environment-specific** → the ~1.9 s / ~3.1 s split came from one browser on one
  machine. The absolute numbers will differ elsewhere; the before/after comparison is run in the same
  environment so the ratio is what is judged.
