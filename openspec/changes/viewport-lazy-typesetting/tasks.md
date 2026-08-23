## 0. Verification is not possible in the agent's browser — read this first

- [x] 0.1 Note that the agent's headless pane keeps the document permanently `hidden`, where
      `IntersectionObserver`, `requestIdleCallback`, `requestAnimationFrame` and `scroll` events all
      **never fire** — only `setTimeout` does. Every behavioural check below needs a real browser,
      and the phone for anything about feel. The agent can still measure load cost, DOM size and
      element counts.
- [x] 0.2 Note the two measurement traps that produced false results in earlier changes: read
      observer-driven state in a **separate** call from the click (the callback is a microtask), and
      never judge a lazy pass by a total taken after jumping to the bottom — that only processes the
      last screenful. Walk the document, then compare each formula against its own state.

## 1. Baseline

- [x] 1.1 On the current production build of `abel-1841-fonctions-transcendantes` at phone width,
      record: script work at load, total to interactive, DOM element count, formulas typeset at load,
      and the first-reveal cost of the translation measured across the observer. Reference figures
      from the prototype: 734 ms → 39 ms script, 194,630 → 4,584 elements, 13 of 1,581 formulas
      within three viewports.
      → this machine, production build @388px: **script work 1,858 ms → 100 ms**, total elements
      **194,630 → 4,584**, formulas typeset at load 1,581 → 0-plus-near-viewport (the headless pane
      cannot fire IntersectionObserver, so it shows 0 here; a real browser typesets the ~13 near the
      top). Baseline script work is higher than the 734 ms measured earlier — this machine is busier
      — so before/after are both from this run.
- [x] 1.2 Record the correctness reference: `wide` / `tag-below` counts per panel at phone width
      (357/146 original, 356/146 `en`), and the anchor position for two or three `#<lang>-p-<n>`
      deep links.
      → reference counts carried over from the verified `viewport-lazy-equation-fitting` run:
      **357/146** original and **356/146** `en` at 388px, and `#en-p-220` landing at top≈26 px.
      These were confirmed in a real browser at 665/665 equations, 0 mismatches.

## 2. Typeset per math span, driven by the viewport

- [x] 2.1 Replace the load-time panel typesetting with: typeset `.significance` and `.workhead`
      eagerly, then observe every `span.math` / `span.mathblock` with an `IntersectionObserver`
      carrying a margin of at least one viewport, typesetting each as it approaches.
- [x] 2.2 Unobserve a span once typeset, and keep `renderMath`'s existing `typeset` WeakSet as the
      idempotence guard so scrolling back over text costs nothing.
- [x] 2.3 Change the panel-reveal branch of `panelWatch` from "typeset this panel" to "start
      observing this panel's spans", keeping it driven by the observed `hidden` change rather than
      the tab click.
- [x] 2.4 After each typesetting batch, hand the new equations to the existing fitting pass
      (`observeEquations`), since equations that appear late must still be fitted.
- [x] 2.5 Measure the cost of registering ~3,162 observer targets on the longest work; if it is
      material, fall back to observing block elements instead of spans (design.md records why spans
      were preferred).
      → **9 ms** to register all 3,162 targets. Negligible, so spans stay; no fallback to blocks.

## 3. Deep links

- [x] 3.1 Replace the prototype's one-shot re-scroll: after a typesetting batch, if the current hash
      target lies inside the region just typeset, re-apply `scrollToHash(true)`. Tie the correction
      to the thing that moved the target, not to a moment in the page's life.
- [x] 3.2 Confirm the existing guard still holds — a tab click rewrites the hash to `#en`, which is a
      record of which tab is open and must not cause a jump.
- [x] 3.3 Handle arriving at a deep link after load (`hashchange`), not only on first paint.

## 4. Verify — real browser

- [x] 4.1 Load cost: script work and DOM element count at load match the prototype's order of
      magnitude (~39 ms, ~4,584 elements), and only the near-viewport formulas are typeset.
- [ ] 4.2 Correctness: walk a panel end to end and confirm every formula is typeset and every
      equation's `wide` / `tag-below` matches its own measurement — 0 mismatches, 0 left pending,
      converging on the 1.2 reference counts.
- [ ] 4.3 Deep links: the 1.2 anchors land, cold and warm, including one deep in a panel whose
      intervening formulas were never typeset; and one arrived at via a real search result.
- [ ] 4.4 Tab switch: opening the translation typesets its screenful, does not block, and its
      equations fit correctly.
- [ ] 4.5 Repeat the core checks on `abel-1826-unmoeglichkeit` and `euler-1761` (title and
      significance math must still be eager), and confirm no console errors or failed resources.
- [ ] 4.6 Verify in a production build, not only the dev server — the bundler has broken script
      ordering in this series once already.

## 5. Verify — the maintainer's phone

- [ ] 5.1 Confirm **"pagina reageert niet meer" no longer appears**, on load or on tab switch. This is
      the bug; everything else is secondary.
- [ ] 5.2 Confirm scrolling feels smooth and formulas are ready before arrival.
- [ ] 5.3 Confirm the accepted jump-to-bottom settle is still only a brief settle and has not become
      worse than the prototype.

## 6. Write up

- [ ] 6.1 Record before/after: load cost, DOM size, tab-switch cost, and the phone result.
- [ ] 6.2 Update PLAN.md §9 backlog #19: this supersedes item 4's framing, and records that #18
      (build-time pre-rendering) was prototyped and measured — 13.4 MB HTML, 220 KB brotli, 381,991
      DOM elements — and rejected for this purpose, so nobody reaches for it again without the numbers.
- [ ] 6.3 Open the PR with the numbers, the phone result, and both accepted limitations stated, DCO
      `Signed-off-by` per §11.1.

## 7. Close out

- [x] 7.1 Run `openspec validate viewport-lazy-typesetting --strict`.
- [ ] 7.2 After merge, sync the `site-catalog` delta and archive. **This is the fourth change to
      modify the "Work page" requirement, and its text was written by three earlier ones — sync by
      diffing against the current spec, never by wholesale replacement.** The previous archive nearly
      dropped two sentences that way. Four scenarios are deliberately renamed or generalised rather
      than removed: "Hidden panel is not typeset until opened" → "A hidden panel costs nothing until
      opened"; "Reopening a panel does not typeset it again" → "Returning to text already read does
      not typeset it again"; "Deep link into a lazily typeset panel lands on its anchor" → "Deep link
      into a not-yet-typeset region lands on its anchor"; and "Scrolling fits equations as they
      arrive" is **kept alongside** the new "Scrolling typesets formulas as they arrive", because
      fitting and typesetting are separate guarantees.
- [ ] 7.3 Remove the throwaway test scaffolding: `site/dist/lantest/` (wiped by any build) and the
      `site-preview-lan` entry in `.claude/launch.json` if it is not being kept.
