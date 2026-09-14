# Notation decisions — Picard 1884

Cross-page rendering decisions for Émile Picard's 1884 *Comptes rendus* note,
*Sur les intégrales de différentielles totales algébriques* (t. XCIX, pp. 961–963),
established under HOUSESTYLE R27.

## Figures and letters

- **Old-style figures are transcribed as ordinary digits.** Digits in text and math are standard
  ASCII digits: `f(x, y, z) = 0`, `\tag{1}`, `m - 2`. **Do not** write letter `o` for zero,
  **do not** write `ı` or `\iota` for one.
- **Uppercase Latin polynomials and operators are plain math letters:** `P`, `Q`, `A`, `B`, `C`,
  and subscripted `P_{1}`, `Q_{1}`. The print sets them upright roman against italic lowercase,
  but upright-vs-italic is presentation, not notation. **Do not** write `\mathrm{P}`, `\mathbf{P}`,
  `\text{P}` or `\operatorname{P}`.
- **Parameters and variables:** Lowercase variables are `$x$, $y$, $z$, $t$, $u$, $v$`. The parameter
  `$v$` is the Latin letter $v$, not Greek $\upsilon$ or $\nu$.
- **Greek letters:** The four homogeneous auxiliary polynomials are `\theta_{1}`, `\theta_{2}`,
  `\theta_{3}`, `\theta_{4}`. **Do not** write `\vartheta`.

## Subscripts, exponents, primes

- **Subscripted indices and coordinates are always braced:** `x_{0}`, `y_{0}`, `z_{0}`,
  `P_{1}`, `Q_{1}`, `\theta_{1}`, `\theta_{2}`, `\theta_{3}`, `\theta_{4}`. **Do not** write bare
  `x_0`, `P_1`, or `\theta_1`.
- **Primes precede subscripts:** `f'_{z}(x, y, z)`. The ASCII apostrophe prime comes before the
  braced subscript `_{z}`. **Do not** write `f_{z}'`, **do not** write `\prime`, **do not** use
  Unicode `′`.
- **Exponents and index arithmetic:** `m - 2`, `m - 3`.

## Differentials, fractions, and derivatives

- **Differentials carry a thin space:** `\,dx`, `\,dy`, `\,dz`, `\,dt`, `\,du`, `\,dv` —
  including inside numerators (`B\,dx - A\,dy`). **Do not** write bare `dx` or `dy`, **do not**
  use `\;` or `\ `.
- **Partial derivatives use `\partial`:** `\frac{\partial f}{\partial x}`,
  `\frac{\partial \theta_{1}}{\partial x}`.
- **Integral limits:**
  - On p. 961 (first display): `\int_{x_{0},\,y_{0}}^{x,\,y} P\,dx + Q\,dy,`
  - On p. 961 (equation 2): `\int_{(x_{0},\,y_{0},\,z_{0})}^{(x,\,y,\,z)} \frac{B\,dx - A\,dy}{f'_{z}(x, y, z)},`
  - On p. 963: `\int P\,dx + Q\,dy \quad\text{et}\quad \int P_{1}\,dx + Q_{1}\,dy;`

## Displays and alignment

- **Display math punctuation:** Trailing commas and periods are kept inside `\[ ... \]`, matching
  the printed punctuation.
- **Equation numbers:** `\tag{1}`, `\tag{2}`, `\tag{3}` on the right, using the author's bare
  numerals without periods or parenthesized tags.
- **Multi-line system on p. 963:** Aligned on `&=` with `\begin{aligned}`:
  ```latex
  \[
  \begin{aligned}
  P\,dx + Q\,dy &= du, \\
  P_{1}\,dx + Q_{1}\,dy &= dv,
  \end{aligned}
  \]
  ```
  **Do not** use `cases`, `array`, `gather` or `eqnarray`.
- **Joined displays on p. 962 and p. 963:**
  - `A = 0, \quad B = 0, \quad C = 0`
  - `\int P\,dx + Q\,dy \quad\text{et}\quad \int P_{1}\,dx + Q_{1}\,dy;`
  Joined with `\quad`.

## Structure and typography

- **Comptes Rendus quotation marks:** Following Academy convention for quoted communications
  (R22), a single « opens the first paragraph on p. 961, » heads each following paragraph on
  pp. 961, 962, 963, and » closes the communication at the end of p. 963. Written as literal
  Unicode characters tight against the text.
- **Heading:** `\section*{Analyse mathématique. --- Sur les intégrales de différentielles totales algébriques. Note de M.~E.~Picard, présentée par M.~Hermite.}`
  No text-mode braces inside the section title (R25).
- **Hyphenation across page breaks:** Dropped and completed on the page where the word begins:
  `fonctions` completed at the foot of p. 962 before `\origpage{963}`.
- **Page furniture omitted:** Running heads, volume/issue notices (`C. R., 1884, 2e Semestre...`),
  and isolated page numbers are not transcribed.
- **Unrelated Academy items omitted:** The preceding note on terrestrial magnetism and its footnote
  `(1)` on p. 961, and the subsequent note by M. G. Fouret on p. 963, are omitted.
- **Faithfulness to apparent printer's error (R4):** On p. 962, the text states
  `trouver trois polynômes \theta_{1}, \theta_{2}, \theta_{3}, \theta_{4}`. Although four
  polynomials are listed, the word `trois` is reproduced exactly as printed and documented.
