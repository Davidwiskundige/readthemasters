## Why

A long work is unusable on a mid-range phone. On a Samsung A16 in Samsung Internet, the maintainer
gets **"pagina reageert niet meer"** — the browser's unresponsive-script dialog — when opening the
translation of `abel-1841-fonctions-transcendantes`, and the initial load is very slow before any tab
is touched. Both come from the same cause: `renderMathInElement` typesets a whole panel's 1,581
formulas in one synchronous task. On desktop that is ~734 ms at load and ~4–5.5 s on a tab switch; a
budget phone is several times slower, which is long enough to trip the watchdog.

Everything shipped so far reduced the *fitting* cost and moved typesetting off the load path for
hidden panels, but none of it changed how much typesetting happens: the cost stays proportional to
the length of the work.

The measurement that reframes it: **only 13 of the 1,581 formulas in Abel's panel sit within three
viewports of the top.** The page opens with metadata, significance and prose. Typesetting the other
1,568 is work for content the reader has not reached and may never reach.

A prototype was built and tested on the maintainer's phone. Against the short-work target
(`leibniz-1689-isochrona`, 82 formulas, 41 ms of script work):

| | current | prototype | short work |
|---|---|---|---|
| script work at load | 734 ms | **39 ms** | 41 ms |
| total to interactive | 758 ms | **312 ms** | 259 ms |
| DOM elements | 194,630 | **4,584** | 1,563 |
| download (brotli) | 47 KB | **47 KB** | — |

Abel loads like a short work. The maintainer's verdict on the phone was that it "feels nice".

Build-time pre-rendering (backlog #18) was also prototyped and measured, and is **not** proposed:
it fixes the same bug but ships 13.4 MB of HTML (220 KB brotli, up from 47 KB) and doubles the DOM to
381,991 elements — the wrong trade on the device that is struggling. It also leaves cost proportional
to document length, where this does not.

## What Changes

- Typeset each math span when it approaches the viewport, instead of typesetting a whole panel at
  once. Work at load becomes proportional to a screenful rather than to the length of the work, so
  a work ten times longer than Abel loads no slower.
- **Supersede** the panel-level rule from `lazy-render-hidden-panel-math` rather than sit beside it.
  A hidden panel is simply a region that is never near the viewport, so the general rule subsumes the
  special case. The spec must state one rule about when math is typeset, not two overlapping ones.
- Keep the panel-reveal hook, changing its body from "typeset this panel" to "start watching this
  panel's math", so a revealed translation typesets its visible screenful rather than all of itself.
- Re-fit newly typeset equations through the existing viewport-driven fitting pass, which already
  handles equations arriving late.
- Handle deep links deliberately: a link into a page marker must land on it even though the formulas
  around it typeset after the scroll. The prototype's one-shot re-scroll is not good enough to ship.
- Accept and document two consequences (see Impact).

## Capabilities

### New Capabilities

None. This changes when existing work happens.

### Modified Capabilities

- `site-catalog`: the "Work page" requirement currently says math is typeset in whole panels, lazily
  per panel. That rule is replaced by a viewport-driven one covering both panels and regions within
  them, and gains the accepted limitations below. This is the **fourth** change to modify this
  requirement, and its text was written by two earlier changes — the sync must be done by diffing
  against the current spec, never by wholesale replacement.

## Impact

- **Code**: `site/src/pages/works/[id].astro` — the load-time typesetting pass and the panel-reveal
  observer. The prototype was ~25 lines, because it reuses what three merged changes already built:
  `renderMath` and the `typeset` WeakSet, `panelWatch`, `scrollToHash`, and
  `observeEquations`/`eqWatch`/`fitEquations`. No CSS, no build, no corpus changes.
- **None of the three merged performance changes is superseded in code.** Batched read/write phases
  and viewport-driven fitting are both directly reused; only the panel-level typesetting *rule* is
  generalised.
- **Accepted limitation — layout settle on a jump to the bottom.** Scrolling straight to the end of a
  long work causes a brief settle as the formulas there typeset and grow, so the reader is no longer
  exactly at the bottom. Reserving space for display equations was prototyped and did **not** fix it:
  roughly 900 of the ~1,580 formulas per panel are inline, and typeset inline math is slightly taller
  than the raw text it replaces, so the drift accumulates per line. Reserving for that would mean
  constraining prose line-height, which is a worse trade than the symptom. Judged acceptable against
  a load that drops from 734 ms to 39 ms.
- **Accepted limitation — find-in-page.** Regions not yet typeset still contain raw `$x$` source, so
  the browser's find matches LaTeX there until the region renders. Pagefind and the formula index are
  unaffected: both are built from the HTML at build time.
- **Risk**: deep links are the sharp edge, for the fourth time in this series. Verification must be on
  a real device — the agent's headless browser suspends `IntersectionObserver`,
  `requestIdleCallback`, `requestAnimationFrame` and scroll events entirely.
- **Not in scope**: build-time pre-rendering (#18), and the ~2 s panel-switch layout cost, which is
  the browser laying out a revealed panel and is expected to shrink here only as a side effect of
  there being fewer typeset equations to lay out.
