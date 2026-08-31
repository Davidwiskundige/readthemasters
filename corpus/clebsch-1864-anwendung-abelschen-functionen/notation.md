# Notation decisions — Clebsch 1864, *Anwendung der Abelschen Functionen in der Geometrie*

Work-spanning rendering decisions for this transcription, so that pages transcribed in separate
batches stay consistent with each other. Each entry is the decision plus why it was made.
Pages 189–222 follow this list; pp. 223–243 are not yet transcribed and must follow it too.

## Symbols

- **Summation sign → `\Sigma`, the letter — never `\sum`.** The print sets one slanted capital-sigma
  letter throughout, not a modern large operator. Pages 189–206 use `\Sigma` 21 times; the
  independently-transcribed pp. 211–222 agree (32 times). An early draft of pp. 207–210 used
  `\sum` and was conformed before assembly.
- **Σ carrying limits → `\mathop{\Sigma}\limits_{...}^{...}`.** First arises on p. 207, where the
  print stacks the limits above and below the letter (`n=−∞`…`n=+∞`, `h,k=1`…`h,k=p`, `k=1`…`k=p`).
  This keeps the letter and the printed limit placement. Verified to render in the site's KaTeX
  0.16 build, including nested inside an exponent.
- **Multiplication dot → a literal `.`, set TIGHT with no spacing** — never `\cdot`, `\times`,
  juxtaposition, or `\,.\,`. Clebsch writes products with a period, in numerals and in symbol
  products alike. Write `F''(ss).F''(zz)`, `n.(n-1)`, `\Theta.\frac{...}{...}`, `28.64`,
  `\frac{p.p-1\ldots p-k+1}{1.2\ldots k}` — no space, no thin space, on either side, whatever the
  operands are. It is the author's notation (R3).
  *Do not relax this because the operands are large.* Pages 189–206 set 63 such dots and every one
  is tight, including before a `\frac` and before `\Sigma`. `\cdot` appears in this work **only** as
  the matrix continuation row `\cdot\quad\cdot\quad\cdot`, never as a product.
- **`≡` vs `=` followed per occurrence.** The three-bar sign is set `\equiv`, the two-bar `=`. The
  distinction is mathematical — congruence mod periods or mod 2 against plain equality — and must
  never be normalized to one sign.
- **Rank → upright `\mathrm{w}`.** The print sets the rank as an upright w while every neighbouring
  variable is italic, and an italic `w` is already in use in this work for other quantities (the
  quadratic form on pp. 213–217, the surface `w=0` on p. 222). Used on pp. 191–192 and 220–221.
- **Ordinals → `^{\text{ter}}` / `^{\text{ten}}`** (R21), e.g. `m^{\text{ter}}`, `p^{\text{ten}}`.
  Where the ordinal follows a fraction, write `\frac{...}{...}{}^{\text{ter}}` so the fraction is
  not swallowed into the exponent.
- **`§.`** is a literal section sign followed by a non-breaking space: `§.~9.` (R19).
- **Equation tags keep the author's trailing period**: `\tag{1.}`, `\tag{12.}` (R5). Numbering runs
  continuously through the paper and is printed on each page, so batches need no shared state
  for it.

## Typography

- **No long-ſ and no eszett.** This print is Antiqua with round s only: `dass`, `muss`, `lässt`,
  `grosse` stay as `ss`. HOUSESTYLE **R19's `ſs → ß` mapping does not apply to this work** — the
  file contains no `ß`, and that is faithful, not an oversight.
- **German quotation marks** are written as literal Unicode `„ … "` rather than `` `` … '' ``
  (R18, R22).
- **Personal names** italicized in the print are wrapped at the stem only: `\emph{Abel}schen`,
  `\emph{Riemann}s`, `\emph{Jacobi}sche` — matching what the print italicizes.
- **Headings carry no `\emph`** (R25), even where the print italicizes a name inside them.
- **`\uncertain{}` is never nested inside `\emph{}`.** `site/src/lib/tex.js` matches these
  arguments with `[^}]*`, so a nested brace group silently leaks the tail into the running text
  (R18). Split the `\emph` run and place `\uncertain{...}` between the two halves.

## Structure

- **Section headings are two elements**: `\section*{§.~N.}` for the centred number line, then
  `\subsection*{...}` for the descriptive title beneath it, matching the print's two lines.
- **Words hyphenated across a page break** are written whole on the page where the word *begins*;
  the next fragment starts at the following word. This keeps concatenated fragments from inserting
  a break mid-word.
- **Running heads, page numbers and signature lines** (e.g. `27 *`) are page furniture and are not
  transcribed.
- **An unnumbered figure** (p. 215, referenced only as "siehe die Fig.") is keyed to its page:
  `\rmfigure{figures/fig-215.png}{Fig.}{...}`. Numbered figures elsewhere in the work should use
  `fig-<number>.png` as usual (R7).
