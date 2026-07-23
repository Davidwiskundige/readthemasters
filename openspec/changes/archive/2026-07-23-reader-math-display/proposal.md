# Change: reader-math-display

## Why

Two gaps in how the reader shows mathematics:

- On a narrow screen, a display equation wider than the text column ran straight underneath its
  own equation number. KaTeX centres the formula in a block as wide as the column and pins
  `\tag{n}` absolutely at that block's right edge, so nothing in the layout keeps them apart —
  on the Fagnano *Schediasma I* page at a 335px column, four equations collided, the worst by
  222px of overlap.
- The `significance` callout was plain text only: notation written in the editorial note (e.g.
  the divisions of the lemniscate's arc) read as literal `2·2^m` rather than as mathematics.

## What changes

- Each display equation gets its own horizontal scroll area. A formula wider than the column is
  left-aligned so scrolling starts at the beginning of the formula instead of with its left half
  already cut off and unreachable.
- An equation number that cannot sit beside its formula moves to a line of its own, right-aligned
  under the equation. Decided by measurement, not by a viewport breakpoint: a centred formula
  needs the number's width clear on *both* sides, so the test is `math + 2 × number > column`.
- The measuring pass re-runs when the KaTeX web fonts arrive (the first pass measures short
  without them), on resize, and on tab switch — a hidden translation panel cannot be measured
  until it is shown.
- KaTeX also renders inside the significance callout, and the Fagnano *Schediasma II* note marks
  its notation as math.

## Impact

- Extends `site-catalog` (work page rendering, significance note). No schema or gate change.
- Touches `site/src/styles/global.css` and `site/src/pages/works/[id].astro` only.
