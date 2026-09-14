# Notation decisions — Picard 1884 (Surfaces algébriques)

Cross-page rendering decisions for Émile Picard's second 1884 *Comptes rendus* note,
*Sur les intégrales de différentielles totales et sur une classe de surfaces algébriques*
(t. XCIX, pp. 1147–1149), established under HOUSESTYLE R27.

## Figures and letters

- **Digits are standard ASCII numerals:** Digits in text and formulas are standard ASCII digits:
  `f(x, y, z) = 0`, `m - 4`, `m + 2`. **Do not** write letter `o` for zero, **do not** write `ı` or
  `\iota` for one.
- **Uppercase Latin polynomials are plain math letters:** `$A$`, `$B$`, and subscripted `$A_{1}$`,
  `$B_{1}$`. In the print, $A$ and $B$ are set in upright roman type while lowercase variables are in
  italic type, but typeface variation of this kind is presentation, not notation (HOUSESTYLE R1).
  **Do not** write `\mathrm{A}`, `\mathbf{A}`, `\text{A}`, or `\operatorname{A}`.
- **Parameters and variables:** Lowercase variables are `$x$, $y$, $z$, $u$, $v$`. The parameter
  `$v$` is the Latin letter $v$, not Greek $\upsilon$ or $\nu$.
- **Degree parameter:** The order/degree is `$m$`.

## Subscripts, exponents, primes

- **Subscripted indices are always braced:** `A_{1}`, `B_{1}`. **Do not** write bare `A_1` or `B_1`.
- **Primes precede subscripts:** `f'_{z}`. The ASCII apostrophe prime comes before the braced
  subscript `_{z}`. **Do not** write `f_{z}'`, **do not** write `\prime`, **do not** use Unicode `′`.
- **Exponents and index arithmetic:** `m(m - 4)`, `m + 2` use spaced minus and plus signs in math mode.

## Differentials, fractions, and derivatives

- **Differentials carry a thin space:** `\,dx`, `\,dy`, `\,dz`, `\,du`, `\,dv` — including inside
  numerators (`B\,dx - A\,dy`, `B_{1}\,dx - A_{1}\,dy`). **Do not** write bare `dx` or `dy`,
  **do not** use `\;` or `\ `.
- **Partial derivative in denominator:** `f'_{z}` represents $\frac{\partial f}{\partial z}$, matching
  Picard's notation in the 1 December 1884 note.
- **Fractions:**
  - Inline fractions: `\frac{m(m - 4)}{2}` on p. 1148 and `\frac{m + 2}{2}` on p. 1149.
  - Display fractions: `\frac{B\,dx - A\,dy}{f'_{z}}` and `\frac{B_{1}\,dx - A_{1}\,dy}{f'_{z}}`.

## Displays and alignment

- **Display math punctuation:** Trailing commas are kept inside `\[ ... \]`, matching the printed
  punctuation:
  - `\[ f(x, y, z) = 0, \]`
  - `\[ \int \frac{B\,dx - A\,dy}{f'_{z}} \quad\text{et}\quad \int \frac{B_{1}\,dx - A_{1}\,dy}{f'_{z}}, \]`
  - In the two-equation system, the first line ends with a comma (`= du,`) and the second has no
    trailing punctuation (`= dv`), matching the print before continuing into prose.
- **Equation numbers:** None of the displays in this note carry printed equation numbers. **Do not**
  invent tags or use LaTeX automatic numbering.
- **Multi-line system on p. 1148:** Aligned on `&=` with `\begin{aligned}` inside `\[ ... \]`:
  ```latex
  \[
  \begin{aligned}
  \frac{B\,dx - A\,dy}{f'_{z}} &= du, \\
  \frac{B_{1}\,dx - A_{1}\,dy}{f'_{z}} &= dv
  \end{aligned}
  \]
  ```
  **Do not** use `cases`, `array`, `gather` or `eqnarray`.
- **Joined displays on p. 1148:**
  `\int \frac{B\,dx - A\,dy}{f'_{z}} \quad\text{et}\quad \int \frac{B_{1}\,dx - A_{1}\,dy}{f'_{z}},`
  Joined with `\quad\text{et}\quad`.

## Structure and typography

- **Comptes Rendus quotation marks:** Following Academy convention for quoted communications
  (HOUSESTYLE R22), a single « opens the first paragraph on p. 1147, » heads each following paragraph
  on pp. 1148 and 1149, and » closes the communication at the end of p. 1149. Written as literal
  Unicode characters tight against the text.
- **Heading:**
  `\section*{Analyse mathématique. --- Sur les intégrales de différentielles totales et sur une classe de surfaces algébriques. Note de M.~E.~Picard, présentée par M.~Hermite.}`
  No text-mode braces inside the section title (HOUSESTYLE R25).
- **Theorem emphasis:** The enunciated theorem on p. 1148 is set in italics in the print:
  `\emph{La surface proposée a une courbe double d'ordre $\frac{m(m - 4)}{2}$ et elle possède deux intégrales de différentielles totales de première espèce}`
  followed by the displayed integrals, and concluding with:
  `\emph{pour lesquelles le déterminant $AB_{1} - A_{1}B$ n'est pas identiquement nul.}`
- **Page boundary joins:**
  - p. 1147 ends mid-sentence ("... présenter quelque"); p. 1148 opens immediately with no blank line
    after `\origpage{1148}` ("intérêt; parmi ces applications...").
  - p. 1148 ends mid-sentence ("... est de degré $m$ et de"); p. 1149 opens immediately with no blank
    line after `\origpage{1149}` ("genre $\displaystyle\frac{m + 2}{2}$, ...").
- **Page furniture omitted:** Running heads, volume/issue notices (`C. R., 1884, 2e Semestre...`),
  feuilleton numbers (`153`), and isolated page numbers are not transcribed.
- **Unrelated Academy items omitted:** Poincaré's note concluding on p. 1147 and M. Amigues' note
  beginning on p. 1149 are omitted.
