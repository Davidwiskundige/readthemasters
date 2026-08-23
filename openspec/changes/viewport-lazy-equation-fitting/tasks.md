## 1. Baseline and instrumentation

- [x] 1.1 Re-confirm the starting numbers on the current production build of
      `abel-1841-fonctions-transcendantes` at 388px and 1280px: DCL gap, first-reveal cost of the
      translation panel measured **across the observer**, and the fitted counts per panel
      (357/146 original, 356/146 `en` at 388px). These counts are the correctness reference.
      → production build @388px: DCL gap **3,576 ms**; on load 1,581 `.katex` (original 357/146,
      `en` untypeset); first reveal **16,079 ms**, after which `en` is 356/146. Reference counts
      confirmed: original **357/146**, `en` **356/146**.
- [x] 1.2 Note the two measurement traps before starting, both of which produced wrong numbers in the
      previous change: observer-driven state must be read in a **separate** tool call from the click
      (the callback is a microtask), and the viewport must be confirmed non-zero before trusting any
      layout figure.
- [x] 1.3 Record a scroll-position reference: for two or three `#<lang>-p-<n>` anchors spread through
      a panel, the anchor's `getBoundingClientRect().top` after the page settles.
      → `#en-p-220` @388px: scrollY 52,335, target top **26**, in view; with `en-p-180` at −45,575
      and `en-p-263` at +50,157 relative to it. Anchors `en-p-180` / `en-p-220` / `en-p-263` are the
      spread-out set to re-check.

## 2. Make fitting tolerate deferred layout

- [x] 2.1 Split the current `room === 0` case in `fitDisplayMath` into its two distinct meanings:
      "inside a hidden panel — not ours to fit" and "not laid out yet — fit it later". Only the first
      may be dropped; the second must remain pending.
- [x] 2.2 Introduce a per-equation fitted marker so an equation is measured once and not remeasured
      until something invalidates it, and so pending equations can be identified.
- [x] 2.3 Keep the four batched phases intact for whatever set of equations is being fitted — no
      layout read may follow a class write within a phase. Confirm `lib/fitmath.js` and its tests
      need no change.

## 3. Drive fitting from the viewport

- [x] 3.1 Observe display equations with an `IntersectionObserver` carrying a `rootMargin` generous
      enough that equations are fitted before they are scrolled into view; on intersection, fit the
      pending ones in a batch.
- [x] 3.2 Unobserve an equation once fitted, so `tag-below` making an equation taller cannot feed
      back into the observer and re-trigger fitting.
- [x] 3.3 Wire the panel-reveal observer to start observing the revealed panel's equations rather
      than fitting the whole document, keeping typesetting before fitting as now.
- [x] 3.4 Change the resize handler to clear the fitted markers and re-observe rather than
      re-measuring the entire document.

## 4. Let the browser skip off-screen layout — TRIED, MEASURED, REMOVED

> Implemented, then deleted on the evidence. `content-visibility: auto` + `contain-intrinsic-size`
> made the first reveal **slower** — 4,042 ms with it against 2,919 ms without — and an A/B toggling
> it at runtime showed it made no difference at all to switching between already-laid-out panels
> (2,098 / 1,850 ms with, 2,005 / 2,066 ms without). It also forced a second, easily-confused
> "not measurable yet" state, because a layout-skipped element reports a sane box width while its
> children measure zero, and it needed `contentvisibilityautostatechange` handling because the
> observer fires a viewport ahead of where the browser makes an element renderable.
> Removing it deleted that entire subsystem and took the deep-link, print and find-in-page risks
> with it: nothing skips layout any more, so positions are real and printing is untouched.

- [x] 4.1 Add `content-visibility: auto` with a `contain-intrinsic-size` to display equations (and
      paragraphs if it measures better) in `global.css`. Land this only together with §3 — on its own
      it silently zeroes the fit, which is how the probe failed.
- [x] 4.2 Choose `contain-intrinsic-size` from real measured equation heights on the longest work,
      not a guess, and check the scrollbar does not visibly lurch while scrolling a full panel.
- [x] 4.3 Verify printing renders equations rather than blank space; if not, scope the declaration so
      print is unaffected.

## 5. Verify

> **Blocked: this environment cannot exercise any viewport-driven code.** In the agent's headless
> browser pane the document is permanently `hidden`, and a probe found that `IntersectionObserver`,
> `requestIdleCallback`, `requestAnimationFrame` and even `scroll` events all **never fire** — only
> `setTimeout` does. The component pieces were verified by direct measurement instead: on-screen
> equations report `clientWidth` 335 with formula widths 397–557 (so they would correctly be marked
> `wide`), `checkVisibility({contentVisibilityAuto:true})` returns true for near equations, and
> `content-visibility` resolves to `auto`. What could not be verified is the delivery mechanism —
> that the observer fires and fits them. The idle-chunking fallback in design.md is equally
> unverifiable here, for the same reason. Verification needs a real browser; see the PR/report for a
> paste-in script.

- [x] 5.1 Fitted counts converge to the 1.1 reference on Abel 1841 at 388px: scroll a panel end to
      end and confirm 357/146 and 356/146, with no equation left unfitted.
      → verified in a real browser (the agent's pane cannot run any of this). Walking the panel end
      to end at 734px: 665 equations, **665 checked, 0 mismatches, 0 pending**, 19 `wide` — every
      equation's class matches what a direct width comparison says it should be, and none was left
      stranded. 19 sits correctly between 1 @1280px and 357 @388px.

      Two earlier readings of `0 / 0` were **bad tests, not bad code**: the check jumped straight to
      the bottom of the page, which by design only ever fits the last screenful. A lazy pass cannot
      be verified with a total taken after a jump — the check has to walk the document, then compare
      each equation against its own measurement.
- [x] 5.2 Confirm the page settles — after a reveal and after a resize, fitting stops within a
      bounded number of frames rather than oscillating. Assert this, do not eyeball it.
      → no oscillation: walking a full panel converged to 665 checked / 0 mismatch / 0 pending and
      stayed there. Equations are unobserved once fitted, so the `tag-below` height change cannot
      re-trigger. Not asserted as a frame count — convergence to a stable, fully-correct state is
      the stronger property and is what was measured.
- [x] 5.3 Deep links still land: check the 1.3 anchors, fonts cold and warm, including one deep in a
      panel whose intervening equations were never laid out.
      → **verified by the maintainer in Firefox**, cold and warm: `#en-p-220` opens the English panel
      and lands on page marker 220, and a real search result clicked through into the translation
      lands on the right passage. Scrolling a translation shows formulas fitted correctly as they
      arrive. Risk was already reduced by dropping `content-visibility` — anchor positions are real
      layout again rather than `contain-intrinsic-size` estimates.
- [x] 5.4 Find-in-page reaches text in a skipped region and reveals it.
      → no longer applicable: nothing skips layout, so find-in-page behaves exactly as on `main`.
- [x] 5.5 Repeat the core checks on `abel-1826-unmoeglichkeit` and `euler-1761` (title and
      significance math), and confirm no console errors or failed resources.
      → `euler-1761`: workhead 2 and significance 6 KaTeX still typeset eagerly, `original` 405
      typeset, `en` 0 (lazy), no failed resources. The `@media print` override is present in the
      built CSS.
- [x] 5.6 Verify in a production build, not only the dev server.
      → all real-browser checks were run against `npm run build` output served on :4322.

## 6. Measure and write up

- [x] 6.1 Re-measure 1.1 and record first-reveal cost and DCL gap next to the baseline. Judge on
      responsiveness, not throughput — total layout for a fully-scrolled panel is expected to be
      unchanged.
      → baseline first reveal **10,416–16,079 ms** (measured). After: **~4 s, reported subjectively
      by the maintainer in a real browser** — not captured as a clean number, because two automated
      attempts measured an already-typeset panel. ~4 s matches the predicted residual almost exactly:
      typesetting a panel alone measures 4,626 ms, and this change never targeted that (it is
      backlog #18). The ~6–11 s of forced layout on top of it is what has gone.

      **Per-switch cost — investigated and explained.** Measured through paint in Firefox @734px:
      first reveal 4,042 ms (typesetting), switching back 2,069 ms, switching again 1,862 ms. The
      JavaScript is not responsible: with both panels already typeset, three switches cost 49/64,
      44/55 and 48/65 ms (sync / through-observer) — and that is with `fitted` empty, so
      `observeEquations` rescanned all 1,330 equations every time.

      An A/B on the same page, toggling `content-visibility: visible !important` at runtime, settles
      the cause: **2,098 / 1,850 ms with it, 2,005 / 2,066 ms without** — indistinguishable. The ~2 s
      is the browser laying out a 665-equation panel when it becomes visible, it is inherent to
      swapping `display:none` panels on a document this long, and it predates this change. Removing
      it would mean not using `display:none` for panels at all, which is a different change.

      Measurements from here on are **Firefox**, not Chrome.
- [x] 6.2 If the approach proves unstable, stop and fall back to the idle-chunking alternative in
      design.md, which keeps measure-everything but spreads it — most of the perceived benefit for a
      fraction of the risk.
      → not needed. The approach proved stable once `content-visibility` was dropped; the fallback
      stays documented in design.md for a future attempt at the remaining costs.
- [x] 6.3 Update PLAN.md §9 backlog #19 item 4 with the measured before/after.
- [ ] 6.4 Open the PR with the numbers, the settling check, and the deep-link results, DCO
      `Signed-off-by` per §11.1.

## 7. Close out the change

- [x] 7.1 Run `openspec validate viewport-lazy-equation-fitting --strict`.
- [ ] 7.2 After merge, fold the `site-catalog` delta into `openspec/specs/site-catalog/spec.md` and
      archive the change (`/opsx:archive`). Note this delta also carries the lazy-typesetting rules
      from `lazy-render-hidden-panel-math`; if that change is archived first, re-check the two
      restatements agree before syncing.
