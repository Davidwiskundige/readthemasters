# Spec (delta): housestyle-math-typography

## MODIFIED: LaTeX house style

Adds a math-typography convention to the house-style requirement.

The house style distinguishes faithful **notation** (which symbols and formulas, the author's
notation — kept exactly) from house-style **presentation** (how the same math is set — made
consistent). Math presentation conventions live in `corpus/HOUSESTYLE.md`, which also holds a
**rulings log** of boundary decisions so they are settled once and reused. Current rulings:

- Multi-letter geometric labels (points, arcs, curves) are written as **plain math letters**
  (`$CQ$`, `$ADFNA$`) — no `\pt`/`\mathit`/`\textit` wrapper.
- Inline large operators (∫, ∑, ∏) with a fraction integrand use `\displaystyle` (e.g.
  `\displaystyle\int \frac{...}{...}`), not `\int \dfrac{...}{...}`.
- The author's notation and any printer's errors are transcribed faithfully (e.g. `zz` for
  $z^2$, archaic spelling, the `arc.` abbreviation) and documented for review, never silently
  corrected.
