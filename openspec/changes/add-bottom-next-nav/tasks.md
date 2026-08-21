## 1. Extract shared nav rendering

- [x] 1.1 In [site/src/pages/works/[id].astro](site/src/pages/works/[id].astro), add a small render
      helper (alongside `attribution()`/`renderSignificance()`) that returns the "Related reading"
      nav markup given `recPrev`/`recNext`/`firstWords`, so both placements call the same code.
- [x] 1.2 Replace the existing top `.relnav` block (lines ~130-151) with a call to the new helper,
      confirming the rendered output is unchanged from before the refactor.

## 2. Add the bottom nav

- [x] 2.1 Render the same helper again directly after the last translation `<section>` (after the
      `translations.map(...)` block, before the "Existing translations elsewhere" section). The
      bottom instance shows only the `Next:` side (never `Read first:`) and is guarded by whether
      `recNext` exists, not the top nav's `(recPrev || recNext)` condition.
- [x] 2.2 If the default `.relnav` spacing looks cramped directly under the text, add a modifier
      class (e.g. `.relnav-bottom`) in [site/src/styles/global.css](site/src/styles/global.css) for
      extra top margin only — no other visual changes.

## 3. Verify

- [x] 3.1 Run the Astro dev server and check a work page that has both a recommended prev and next
      (e.g. via `recommended_prev`/`recommended_next` in the built `works.json`): confirm the top nav
      shows both `Read first:`/`Next:` and the bottom nav shows only `Next:`, pointing to the correct
      work.
- [x] 3.2 Check a work page with no recommendation: confirm neither nav placement renders anything.
- [x] 3.3 Check a work page with only a recommended previous (no next): confirm the top nav shows
      `Read first:` only and the bottom nav renders nothing.
- [x] 3.4 Spot-check on a narrow viewport that the bottom nav wraps the same way the top one does.
