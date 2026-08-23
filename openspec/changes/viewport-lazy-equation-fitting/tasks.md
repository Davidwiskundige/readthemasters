## 1. Baseline and instrumentation

- [ ] 1.1 Re-confirm the starting numbers on the current production build of
      `abel-1841-fonctions-transcendantes` at 388px and 1280px: DCL gap, first-reveal cost of the
      translation panel measured **across the observer**, and the fitted counts per panel
      (357/146 original, 356/146 `en` at 388px). These counts are the correctness reference.
- [ ] 1.2 Note the two measurement traps before starting, both of which produced wrong numbers in the
      previous change: observer-driven state must be read in a **separate** tool call from the click
      (the callback is a microtask), and the viewport must be confirmed non-zero before trusting any
      layout figure.
- [ ] 1.3 Record a scroll-position reference: for two or three `#<lang>-p-<n>` anchors spread through
      a panel, the anchor's `getBoundingClientRect().top` after the page settles.

## 2. Make fitting tolerate deferred layout

- [ ] 2.1 Split the current `room === 0` case in `fitDisplayMath` into its two distinct meanings:
      "inside a hidden panel — not ours to fit" and "not laid out yet — fit it later". Only the first
      may be dropped; the second must remain pending.
- [ ] 2.2 Introduce a per-equation fitted marker so an equation is measured once and not remeasured
      until something invalidates it, and so pending equations can be identified.
- [ ] 2.3 Keep the four batched phases intact for whatever set of equations is being fitted — no
      layout read may follow a class write within a phase. Confirm `lib/fitmath.js` and its tests
      need no change.

## 3. Drive fitting from the viewport

- [ ] 3.1 Observe display equations with an `IntersectionObserver` carrying a `rootMargin` generous
      enough that equations are fitted before they are scrolled into view; on intersection, fit the
      pending ones in a batch.
- [ ] 3.2 Unobserve an equation once fitted, so `tag-below` making an equation taller cannot feed
      back into the observer and re-trigger fitting.
- [ ] 3.3 Wire the panel-reveal observer to start observing the revealed panel's equations rather
      than fitting the whole document, keeping typesetting before fitting as now.
- [ ] 3.4 Change the resize handler to clear the fitted markers and re-observe rather than
      re-measuring the entire document.

## 4. Let the browser skip off-screen layout

- [ ] 4.1 Add `content-visibility: auto` with a `contain-intrinsic-size` to display equations (and
      paragraphs if it measures better) in `global.css`. Land this only together with §3 — on its own
      it silently zeroes the fit, which is how the probe failed.
- [ ] 4.2 Choose `contain-intrinsic-size` from real measured equation heights on the longest work,
      not a guess, and check the scrollbar does not visibly lurch while scrolling a full panel.
- [ ] 4.3 Verify printing renders equations rather than blank space; if not, scope the declaration so
      print is unaffected.

## 5. Verify

- [ ] 5.1 Fitted counts converge to the 1.1 reference on Abel 1841 at 388px: scroll a panel end to
      end and confirm 357/146 and 356/146, with no equation left unfitted.
- [ ] 5.2 Confirm the page settles — after a reveal and after a resize, fitting stops within a
      bounded number of frames rather than oscillating. Assert this, do not eyeball it.
- [ ] 5.3 Deep links still land: check the 1.3 anchors, fonts cold and warm, including one deep in a
      panel whose intervening equations were never laid out.
- [ ] 5.4 Find-in-page reaches text in a skipped region and reveals it.
- [ ] 5.5 Repeat the core checks on `abel-1826-unmoeglichkeit` and `euler-1761` (title and
      significance math), and confirm no console errors or failed resources.
- [ ] 5.6 Verify in a production build, not only the dev server.

## 6. Measure and write up

- [ ] 6.1 Re-measure 1.1 and record first-reveal cost and DCL gap next to the baseline. Judge on
      responsiveness, not throughput — total layout for a fully-scrolled panel is expected to be
      unchanged.
- [ ] 6.2 If the approach proves unstable, stop and fall back to the idle-chunking alternative in
      design.md, which keeps measure-everything but spreads it — most of the perceived benefit for a
      fraction of the risk.
- [ ] 6.3 Update PLAN.md §9 backlog #19 item 4 with the measured before/after.
- [ ] 6.4 Open the PR with the numbers, the settling check, and the deep-link results, DCO
      `Signed-off-by` per §11.1.

## 7. Close out the change

- [ ] 7.1 Run `openspec validate viewport-lazy-equation-fitting --strict`.
- [ ] 7.2 After merge, fold the `site-catalog` delta into `openspec/specs/site-catalog/spec.md` and
      archive the change (`/opsx:archive`). Note this delta also carries the lazy-typesetting rules
      from `lazy-render-hidden-panel-math`; if that change is archived first, re-check the two
      restatements agree before syncing.
