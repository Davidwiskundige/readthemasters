## 1. Baseline measurement

- [x] 1.1 On `/works/abel-1841-fonctions-transcendantes/`, record the current load cost at 1280px and
      at ~388px: the `domInteractive` → `domContentLoadedEventEnd` gap, the total `.katex` count, and
      the per-panel `.katex` split (original vs `en`). Reuse the harness pattern from the archived
      `2026-08-23-fix-fitdisplaymath-layout-thrashing/measure.js`.
      → 3,162 `.katex` total, split exactly 1,581 / 1,581 (665 display equations each); the hidden
      `en` panel is fully typeset today. DCL gap: 3,837 ms at 388px, 2,997 ms at desktop.
      `.significance` / `.workhead` carry no math on this work.
- [x] 1.2 Time `renderMathInElement` over one panel alone versus over both, so the expected saving is
      known before the change and the after-measurement has something to be compared against.
      → fresh markup, same page load: one panel **2,970 ms** (1,581 katex) vs both **6,387 ms**
      (3,162 katex) — a 3,417 ms / **53%** saving available.
- [x] 1.3 Capture the reference deep-link behaviour *before* the change: open `#en-p-<n>` for a page
      marker well into the translation, and record the anchor's `getBoundingClientRect().top` once
      the page has settled. This is what the lazy path must still achieve.
      → `#en-p-220` at 388px: `en` panel open, `original` hidden, anchor top **26 px**, scrollY
      52,374, in view. (89 `en-p-*` markers available.)

## 2. Render only what is visible

- [x] 2.1 In `site/src/pages/works/[id].astro`, extract the KaTeX options object and the render call
      into a single `renderMath(el)` helper so the load pass and the reveal pass cannot drift in
      delimiters or `throwOnError`.
- [x] 2.2 Change the load-time pass to typeset `.significance` and `.workhead` unconditionally, and
      `.text` panels only where the panel is currently visible — decided by observed visibility, not
      by assuming the original-language panel is the open one, so the result does not depend on which
      of the page's two scripts the bundler emitted first.
- [x] 2.3 Track which panels have been typeset (a module-level `WeakSet` keyed on the panel element,
      or an equivalent marker on the element) so a panel is never typeset twice.

## 3. Typeset on reveal

- [x] 3.1 Extend the existing `panelWatch` MutationObserver callback: for each panel that is now
      visible and not yet typeset, typeset it, then run `fitDisplayMath(document)` as it already
      does. Rendering must precede fitting — fitting measures rendered KaTeX.
- [x] 3.2 Confirm the callback does no work when a panel is *hidden* (the mutation fires in both
      directions) and no work on a reveal of a panel already typeset.
- [x] 3.3 After typesetting a panel, re-apply the deep-link scroll — the same guarded
      `scrollIntoView` the `document.fonts.ready` handler performs — so an anchor inside the panel
      is not left displaced by the formulas that just grew above it.

## 4. Verify behaviour is unchanged

- [x] 4.1 On the Abel page at 388px: confirm on load that only the visible panel's math is typeset
      and the hidden panel still holds raw LaTeX, then open the translation tab and confirm its math
      typesets and its equations get the same `wide` / `tag-below` counts as the pre-change reference
      (356 / 146 at that width).
- [x] 4.2 Switch tabs back and forth several times; confirm no panel is typeset twice (KaTeX element
      counts stay stable) and the fit classes stay correct on both panels.
- [x] 4.3 Deep-link straight into the translation with `#en-p-<n>` — the shape a formula-search
      result produces — and confirm the panel opens, its math typesets, and the anchor ends up in
      view, matching the 1.3 reference. Check with fonts warm (reload) as well as cold, since
      `document.fonts.ready` can resolve before or after the lazy render.
- [x] 4.4 Repeat 4.1 and 4.3 on `abel-1826-unmoeglichkeit` (a shorter bilingual work) and confirm a
      single-language work still renders correctly with no translation panel present.
- [x] 4.5 Confirm in a production build (`npm run build` + preview), not only the dev server — the
      previous change's regression only appeared once the scripts were bundled.

## 5. Measure and write up

- [x] 5.1 Re-run the 1.1 and 1.2 measurements in the same environment; record the new `.katex` count
      on load, the new DCL gap, and the cost of opening the second tab, next to the baseline.
      → production build. Load improves as designed; **the reveal does not**:
      | metric | before | after |
      |---|---|---|
      | `.katex` typeset on load | 3,162 | **1,581** |
      | DCL gap @388px | 3,837 ms | **2,165 ms** |
      | DCL gap @1280px | 2,997 ms | **2,086 ms** |
      | first reveal of translation @388px | ~0 (already typeset) | **10,774 ms** |
      | first reveal of translation @1280px | ~0 | **10,821 ms** |
      Equivalence held everywhere checked: original 357/146, en 356/146 on Abel 1841; en 28/4 on
      abel-1826 matching a rebuilt baseline exactly; deep links land on their anchor (cold and warm).
- [x] 5.2 Judge the reveal cost from 5.1: if opening the translation reads as broken rather than
      merely slow, note it and consider idle pre-warming as a follow-up (design.md records why it is
      deliberately not in this change).
      → **verdict: acceptable — the reveal cost is pre-existing, not caused by this change.**
      A first measurement compared this change's *first* reveal against the baseline's *subsequent*
      tab switches, which is not a like-for-like comparison and wrongly suggested a ~10 s regression.
      Measured properly, across the observer, on the same build and viewport:

      | first reveal of the translation | baseline | lazy |
      |---|---|---|
      | @1280px | 10,416 ms | 10,821 ms |

      i.e. unchanged. Decomposed, the reveal is not typesetting at all:
      - typesetting the panel in place while still hidden: 4,626 ms (no layout involved)
      - flip + fit with the panel **already** typeset: 12,857 ms

      The cost is the browser's **first layout** of a panel that was `display:none` — 665 display
      equations laid out for the first time — which `fitDisplayMath` then forces synchronously by
      reading `clientWidth` on every one of them. Eager typesetting does not avoid it; it only
      typesets earlier and still defers all layout to the reveal. Recorded as backlog #19 item 4
      (viewport-lazy fitting), which is now known to be the actual fix for tab-reveal cost — and
      note that build-time pre-rendering (#18) would remove the typesetting but **not** this layout.

      Probe: `content-visibility: auto` + `contain-intrinsic-size` on paragraphs and equations is the
      natural CSS answer, but it breaks the current pass outright (fit produced 0 `wide` / 0
      `tag-below`, since layout-skipped elements report no usable geometry). It is only viable
      together with viewport-lazy fitting, not on its own.

- [x] 5.3 Update PLAN.md §9 backlog #19: mark fix 2 as shipped with the measured before/after, and
      leave items 3–4 open with whatever cost remains.
      → item 4 rewritten as the fix for the ~10 s first tab reveal, with the root cause and the
      evidence; noted that #18 does not address it.
- [x] 5.4 Open the PR with the before/after numbers and the deep-link verification in the
      description, DCO `Signed-off-by` per §11.1.
      → https://github.com/Davidwiskundige/readthemasters/pull/27 (merged)

## 6. Close out the change

- [x] 6.1 Run `openspec validate lazy-render-hidden-panel-math --strict`.
- [x] 6.2 After merge, fold the `site-catalog` delta into `openspec/specs/site-catalog/spec.md` and
      archive the change (`/opsx:archive`).
