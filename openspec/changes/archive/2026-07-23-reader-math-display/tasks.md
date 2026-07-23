# Tasks: reader-math-display

- [x] Display equations scroll horizontally instead of overflowing the text column
- [x] Formulas wider than the column are left-aligned so no part is cut off unreachably
- [x] Equation numbers that cannot fit beside their formula drop to their own line
- [x] Measuring pass re-runs on `document.fonts.ready`, on resize, and on tab switch
- [x] KaTeX renders inside the significance callout
- [x] Fagnano *Schediasma II* significance note marked up as math
- [x] Verified: 0 collisions at 335px and 320px columns (was 4 and 5), no left-cut formulas, no
      page-level horizontal scroll, no vertical clipping, desktop unchanged (nothing flagged,
      all numbers still flush right)
- [x] site-catalog spec updated
