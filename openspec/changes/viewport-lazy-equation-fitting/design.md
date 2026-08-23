## Context

Three changes have now touched this pass, and it is worth being precise about what each did, because
the remaining cost is none of them:

| change | what it removed | what it left |
|---|---|---|
| `fix-fitdisplaymath-layout-thrashing` | ~2,660 forced reflows → 2 | still measures every equation |
| `lazy-render-hidden-panel-math` | typesetting the unseen panel on load | layout was always deferred to reveal anyway |
| this change | the forced first layout | — |

The current pass (`[id].astro`) is four whole-collection phases: read every equation's `clientWidth`,
clear classes, measure every formula and tag, apply verdicts. Phase A's first `clientWidth` read is
what forces layout — and on a panel revealed from `display:none`, that is the first layout its 665
display equations have ever had.

Measurements behind this (production build, Abel 1841):

- first reveal of the translation: **10,416 ms** (unchanged by lazy typesetting: 10,821 ms after)
- typesetting the panel in place while hidden: 4,626 ms
- flip + fit with the panel already typeset: **12,857 ms**

Constraints inherited from the two previous changes, both learned the hard way:

- Correctness must not depend on the order the page's two bundled scripts are emitted in. Panel
  reveal is therefore observed (`MutationObserver` on `hidden`), never hung off the tab click.
- Reads and writes stay batched. Whatever this change does, it must not reintroduce a per-equation
  read-after-write interleave.

## Goals / Non-Goals

**Goals:**

- Make the first reveal of a panel cost time proportional to a screenful of equations, not to the
  whole panel.
- Cut the same forced layout out of initial page load for the visible panel.
- Keep every equation's eventual `wide` / `tag-below` verdict identical to today's.
- Keep deep links landing on their anchor, and keep find-in-page working at least as well as now.

**Non-Goals:**

- Changing the fitting rule or `lib/fitmath.js`.
- Build-time pre-rendering (#18) — orthogonal, and it does not address layout.
- Making the *total* layout cost smaller. Reading the whole panel still costs what it costs; this
  spreads it across scrolling instead of paying it in one block.

## Decisions

### `content-visibility: auto` and viewport-driven fitting are one change, not two

A probe on the built site applied `content-visibility: auto` alone and the fitting pass produced
**0 `wide` and 0 `tag-below`** — layout-skipped elements report no usable geometry, and the
measure-everything loop silently dropped every equation. So the CSS is only safe once fitting is
driven by what is actually laid out. They ship together or not at all.

Conversely, `IntersectionObserver` alone would stop *forcing* layout from script but would not stop
the browser laying the panel out; `content-visibility` is what actually lets the layout be skipped.
Each half is close to pointless without the other.

### `clientWidth === 0` must stop meaning "skip"

Today `if (!room) continue` means "this equation is inside a hidden panel; it will be measured again
when its tab is shown". Under `content-visibility` the same zero also means "not laid out yet",
which is a completely different instruction: come back when it is. Conflating them is exactly how
the probe lost all 665 equations.

The pass therefore needs to treat an unmeasurable equation as *pending* — left for the observer to
bring back — rather than as handled. An equation is only finished once it has been measured with a
real width.

### Guard against the feedback loop

`tag-below` moves the equation number onto its own line, which makes the equation taller. Taller
equations shift what intersects the viewport, which can fire the observer again, which can re-fit,
which can change heights. Left alone that oscillates.

Two mitigations, in order of preference: mark an equation as fitted so it is not re-measured until
something invalidates it (resize), and unobserve it once fitted. Re-entry is then bounded by resize
events rather than by layout feedback. This must be verified deliberately — a "settles within N
frames" check, not a glance.

### Resize invalidates lazily

Today resize re-fits the whole document on a 150 ms debounce. That would reintroduce the very
full-document measurement being removed. Instead resize clears the fitted marks and re-observes, so
only what is on screen is re-measured; the rest is refitted as the reader scrolls back to it.

### Deep links get less reliable before they get better

`scrollIntoView` on a target inside skipped content works — the browser realises it on demand — but
the scroll position depends on `contain-intrinsic-size` estimates for everything above it, which are
by definition approximate. The existing re-scroll machinery (`fonts.ready`, and the post-typeset
re-scroll added by `lazy-render-hidden-panel-math`) becomes load-bearing rather than a nicety, and
may need a further re-scroll once the target's neighbourhood is really laid out.

**Alternative considered — chunk the existing pass into idle slices** (`requestIdleCallback`),
keeping measure-everything but spreading it. Much lower risk: no CSS change, no observer, no
feedback loop, deep links untouched. It does not reduce total layout, so the panel still takes ~10 s
to become fully correct, but the main thread stays responsive throughout and the visible screenful
is right immediately. Worth keeping as the fallback if the full approach proves unstable, and worth
doing first if this change stalls.

**Alternative considered — express the rule in pure CSS** and delete the measuring pass entirely.
`wide` is plausible (a formula wider than its column is exactly an overflow condition), but
`tag-below` compares the formula's width against the column *minus twice the tag's width*, which CSS
has no way to ask. Not viable without changing the rule, which is out of scope.

## Risks / Trade-offs

- **Oscillation between fitting and layout** → fit once and unobserve; invalidate only on resize;
  verify the page settles rather than assuming it.
- **`contain-intrinsic-size` guesses wrong** and the scrollbar jumps while reading, or a deep link
  lands short → pick the estimate from real measured equation heights on the longest work, and treat
  deep-link accuracy as an explicit acceptance test at several anchors, not one.
- **Total layout cost is unchanged**; a reader who scrolls the whole panel still pays all of it, just
  spread out. The win is responsiveness, not throughput — worth stating plainly so the measurement
  is judged on the right axis.
- **Printing may emit blank regions** where skipped content was never realised. Must be checked, and
  is a plausible reason to scope `content-visibility` to a print-safe declaration.
- **The `room === 0` semantic change is subtle** and silently loses equations when got wrong — that
  is precisely how the probe failed. The verification must count fitted equations against the known
  totals (357/146 and 356/146 at 388px on Abel 1841), never eyeball a screenshot.
- **This is the riskiest change of the series** for the least certain payoff: it targets a cost most
  readers meet once. If verification gets messy, the idle-chunking fallback delivers most of the
  perceived benefit for a fraction of the risk.
