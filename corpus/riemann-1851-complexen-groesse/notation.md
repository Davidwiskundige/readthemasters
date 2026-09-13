# Notation decisions — Riemann 1851, *Grundlagen für eine allgemeine Theorie der Functionen einer veränderlichen complexen Grösse*

Work-spanning rendering decisions for this transcription, ensuring that all pages (pp. 1–32)
maintain strict notational and typographic consistency. Each entry states the rule, the rationale,
and the forbidden alternatives.

## Symbols and Mathematics

- **Zero in formulas is lowercase letter `o`, not digit `0`.**
  Write `$f = o$`, `$\frac{du}{dx} - \frac{dv}{dy} = o$`, `$N = o$`.
  The print sets a lowercase roman *o* at x-height in mathematical displays and inline equations.
  *Forbidden:* Do not normalize to digit `0`. (Digit 0 appears only in numbers like `10` or subscripts).

- **Partial derivatives use ordinary `d`, never `\partial`.**
  Write `$\frac{du}{dx}$`, `$\frac{dv}{dx}$`, `$\frac{du}{dy}$`, `$\frac{dv}{dy}$`, `$\frac{dX}{dx}$`, `$\frac{dY}{dy}$`, `$\frac{dw}{dz}$`.
  Second derivatives: `$\frac{d^2u}{dx^2}$`, `$\frac{d^2u}{dy^2}$`, `$\frac{d^2\log r}{dx^2}$`.
  Riemann uses standard differential letter $d$ for partial derivatives throughout this work.
  *Forbidden:* Do not modernize to `\partial`: never write `\frac{\partial u}{\partial x}` or `\partial`.

- **Complex variable ordering: `$z = x + yi$` and `$w = u + vi$`.**
  The imaginary unit $i$ follows the real imaginary component: `$x + yi$`, `$u + vi$`, `$dx + dy\,i$`,
  `$\frac{dv}{dx}i$`.
  *Forbidden:* Do not write `$x + iy$` or `$u + iv$`.

- **Integrals use a single `\int` sign for surface integrals.**
  Write `$\int \left(\frac{dX}{dx} + \frac{dY}{dy}\right) dT$` and `$\int \left(X\frac{dx}{ds} + Y\frac{dy}{ds}\right) ds$`.
  The print sets a single integral sign even when integrating over a 2D surface $T$ or region.
  *Forbidden:* Never modernize to `\iint`.
  Every inline integral must carry `\displaystyle\int` per HOUSESTYLE R2/R16. Differentials carry a thin space `\,dx`, `\,dy`, `\,dz`, `\,ds`, `\,dp`, `\,dT`.

- **Greek letters:**
  Looped phi is `\varphi`, plain psi is `\psi`, eta is `\eta`, xi is `\xi`.
  Constants: $\pi$, $e$.

- **No Fraktur mathematical variables:**
  The text and math are typeset in Antiqua/Roman throughout. No `\mathfrak` variables occur.

## Typography and Orthography

- **No `ß` anywhere.**
  This Antiqua print sets round *s* throughout: `Grösse`, `dass`, `muss`, `lässt`, `ausser`, `schliessen`, `Fluss`.
  HOUSESTYLE R19's `ſs → ß` mapping has nothing to convert here.
  *Forbidden:* Never modernize to `Größe`, `daß`, `muß`.

- **Edition orthography is faithful to the 1867 imprint:**
  Preserve `Function`, `Functionen`, `Coordinaten`, `Theil`, `Theile`, `Werthe`, `Hülfsmittel`, `reell`, `complex`.
  *Forbidden:* Never modernize spelling (`Funktion`, `Koordinaten`, `Teil`, `Werte`).
  *(Note: On p. 18 [`mittelst der Funktion \zeta`] and p. 23 [`und wenn in der Funktion u`], the 1867 imprint exceptionally sets `Funktion` with `k`; these are preserved verbatim as printed).*

- **German quotation marks are literal Unicode `„ … “`:**
  Never `\glqq` or ASCII `"`.

- **Emphasis:**
  Letterspaced text (Sperrung) is rendered as `\emph{...}`.
  Proposition headings such as `Lehrsatz.` at the start of Art.~16 are set in `\emph{Lehrsatz.}`.

- **Abbreviation spacing:**
  Abbreviation dots take a LaTeX control space (R17): `Art.\ `, `No.\ `, `Bd.\ `, `S.\ `, `w.\ z.\ b.\ w.`

## Document Structure

- **Section headings are bare article numerals with a period:**
  `\section*{1.}`, `\section*{2.}`, ... `\section*{22.}`.
  Do not add "Art." or "Abschnitt" to the heading. In-text references are transcribed as printed (`Art.~1.`, `Art.~2.`).

- **Footnotes:**
  Footnotes marked with `*)` are set as superscript `${}^{*)}$` in text, and led by `\textbf{*)}` at the foot of that page's text (HOUSESTYLE R15).

- **Page boundaries:**
  Each original page begins with `\origpage{N}`. No blank line follows `\origpage{N}` when a sentence continues across the page break.
  Hyphenated words across a page break are completed on the page where they begin; the next page resumes with the subsequent word.
  Running heads and page numbers are not transcribed.
