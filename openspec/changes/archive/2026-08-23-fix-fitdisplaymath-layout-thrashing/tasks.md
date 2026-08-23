## 1. Baseline measurement

- [x] 1.1 Open `/works/abel-1841-fonctions-transcendantes/` in a browser and record the baseline: the
      `domInteractive` → `domContentLoadedEventEnd` gap from `performance.getEntriesByType('navigation')`,
      and the count of `.katex` and `.katex-display` elements.
      → 3,162 `.katex`, 1,330 `.katex-display` (665 visible + 665 in the hidden `en` panel);
      DCL gap 4,468 ms on the measured load.
- [x] 1.2 Record the baseline split by replaying the page's own script over an off-screen copy of its
      markup: time `renderMathInElement` and the current `fitDisplayMath` separately. Save the harness
      snippet in the change folder (or the PR description) so the after-measurement is run identically.
      → harness saved as `measure.js`. Method improved on the plan: instead of comparing across page
      loads, it runs both implementations over the *same* DOM in the same load, removing machine and
      load variance. Old `fitDisplayMath`: **312 ms** at 1280px, **153,708 ms** at 388px.
- [x] 1.3 Capture the current class assignment for every display equation — an ordered list of
      `{index, wide, tagBelow}` — at a wide viewport and at a narrow one (e.g. 1280px and 375px). This
      is the reference the refactor must reproduce exactly.
      → 1280px: 1 `wide`, 0 `tag-below` (weak signal). 388px: **357 `wide`, 146 `tag-below`** — the
      viewport that actually exercises the rule.

## 2. Pure decision helper

- [x] 2.1 Add `site/src/lib/fitmath.js` exporting a pure function that takes the available width, the
      formula width, and the tag width (or null when there is no tag) and returns which of `wide` /
      `tag-below` apply — the arithmetic currently inline in `fitDisplayMath`, including the `+ 8`
      gutter and the `2 ×` tag allowance for a centred formula needing clearance on both sides.
- [x] 2.2 Add `site/src/lib/fitmath.test.mjs` (`node --test`, alongside the existing `tex.test.mjs`)
      covering: formula narrower than the column with no tag; formula wider than the column; formula
      that fits but whose tag cannot sit beside it; formula that is both wide and tag-below; the
      no-tag case never producing `tag-below`; and the boundary cases at exactly `math === room` and
      exactly `math + 2*tagW === room`, pinning the current strict-greater-than comparisons.
- [x] 2.3 Run `npm test --prefix site` and confirm the new tests pass alongside the existing ones.
      → 17 pass, 0 fail (10 new + 7 existing).

## 3. Batch the DOM pass

- [x] 3.1 In `site/src/pages/works/[id].astro`, import the helper into the math `<script type="module">`
      and rewrite `fitDisplayMath` into the four phases from design.md: (A) read `clientWidth` for every
      `.katex-display`, keeping only those with room > 0 and resolving each one's `.katex-html` and
      `:scope > .tag`; (B) clear `wide` / `tag-below` on exactly those; (C) read each formula's summed
      child-rect width and its tag's rect width into the collected records; (D) apply the classes the
      helper returns. No layout read may follow a layout write within a phase.
- [x] 3.2 Confirm phase A still samples `clientWidth` before the classes are cleared, matching today's
      ordering, and that equations with `clientWidth === 0` (hidden panel) are skipped and keep their
      existing classes rather than being cleared.
- [x] 3.3 Leave all four call sites unchanged — the initial pass, the `document.fonts.ready`
      re-measure, the debounced `resize` handler, and the tab-click handler.

## 4. Verify equivalence

- [x] 4.1 On the fully-rendered Abel page, run the old and new implementations over the same DOM and
      assert they assign identical `wide` / `tag-below` classes to every display equation — compare
      against the 1.3 reference at both viewports. Any mismatch blocks the change.
      → identical, 0 mismatches across all 1,330 equations, at 1280px and 388px, on both the live
      page and the local build. Timing at 388px: old 153,708 ms vs new 35 ms (~4,400x).
- [x] 4.2 Repeat the equivalence check on a work with a translation panel, switching tabs, to confirm
      the hidden-panel skip and the tab-click re-measure still behave as before.
      → **caught a real regression.** Bundling the script (needed for the `fitmath` import) merged it
      with the tabs script and inverted their order, so the click-time re-measure ran *before* the
      panel flip and left every equation in the incoming panel unfitted (en: 0 `wide` instead of 356).
      Instrumenting the class writes proved it: all 1,022 writes happened while `en.hidden === true`.
      Fixed by reacting to the panels' `hidden` attribute with a MutationObserver instead of racing
      the flip on click. Verified in dev and in a production build, both tab directions.
- [x] 4.3 Visually confirm on a narrow viewport that wide formulas still left-align and scroll, and
      that tags that cannot fit still drop to their own right-aligned line beneath.
      → verified by computed style rather than a screenshot (the headless pane does not composite
      frames): on the 109 equations that are both `wide` and `tag-below` at 388px, `.katex` resolves
      to `text-align: left`, the tag to `position: static; display: block`, and the equation box to
      `overflow-x: auto` with `scrollWidth > clientWidth`.

## 5. After-measurement and write-up

- [x] 5.1 Re-run the 1.1 and 1.2 measurements in the same environment; record the new `fitDisplayMath`
      cost and the new `DOMContentLoaded` gap next to the baseline.
      → same-DOM comparison, `fitDisplayMath` only:
      | viewport | old | new | factor |
      |---|---|---|---|
      | 1280px (live page) | 312 ms | 35 ms | ~9x |
      | 388px (live page) | 153,708 ms | 35 ms | ~4,400x |
      | 388px, both panels measured (production build) | 463,647 ms | — | — |
      Production build page load at 388px: `DOMContentLoaded` gap 5,019 ms, all of it now KaTeX
      typesetting rather than fitting. The old code could not finish this page at phone width at all.
- [x] 5.2 Update PLAN.md §9 backlog #19: mark fix 1 as shipped, replace the projected numbers with the
      measured before/after, and leave items 2–4 open with the remaining KaTeX typesetting cost noted.
- [x] 5.3 Open the PR with the before/after numbers and the equivalence-check result in the
      description, DCO `Signed-off-by` per §11.1.
      → https://github.com/Davidwiskundige/readthemasters/pull/25

## 6. Close out the change

- [x] 6.1 Run `openspec validate fix-fitdisplaymath-layout-thrashing --strict`.
- [x] 6.2 After merge, fold the `site-catalog` delta into `openspec/specs/site-catalog/spec.md` and
      archive the change (`/opsx:archive`).
