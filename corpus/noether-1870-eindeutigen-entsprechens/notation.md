# Notation and Conventions: Noether (1870)

*Zur Theorie des eindeutigen Entsprechens algebraischer Gebilde von beliebig vielen Dimensionen*
Max Noether, *Mathematische Annalen* 2 (1870), pp. 293–316.

This document records the typographic, mathematical, and structural conventions of the print and their representation in the LaTeX transcription.

---

## 1. Typography & Text Conventions

- **Typeface & Script:** Set in Antiqua (Latin script), both for body text and mathematics.
- **Orthography:** 19th-century German orthography is preserved exactly:
  - `dass`, `muss`, `lässt`, `schliessen` (Antiqua round *s* / *ss*; `ß` is not used).
  - Silent `h` in words like `Theorie`, `Theil`, `theilbar`, `nothwendig`, `Hülfe`, `Werth`, `Werthe`, `Werthsystem`, `Coeffizienten` / `Coefficienten`.
  - Initial `C` in `Curve`, `Curven`, `Coefficienten`, `Classen`, `Constanten`.
  - `sämmtlich`, `Mannigfaltigkeit`, `resp.`
- **Zero vs. Letter O:** Unlike Noether's 1869 note (which used letter `o` for zero), the 1870 *Annalen* paper prints digit `0` throughout for mathematical zero ($f = 0$, $F = 0$, $p = 0$, $0^{\text{ter}}$ Ordnung).
- **Ordinal Suffixes:** Suffixes are superscripted on mathematical symbols:
  - `$n^{\text{ter}}$ Ordnung`, `$s^{\text{ten}}$ Grades`, `$(n-5)^{\text{ten}}$`, `$(m-1)^{\text{te}}$ Potenz`.
- **Quotations:** German-style quotes: `„…“` (literal Unicode).
- **Dashes & Punctuation:**
  - Em-dash: `---` (or `--` depending on context).
  - Range en-dash: `--` (e.g. `293--316`, `1. bis 7.`).
  - Spacing before punctuation in formulas follows LaTeX standards, with `\,` before trailing punctuation in display environments where appropriate.
- **Printer Errors in Original:**
  - p. 299: `0 = F(y_1,\, y_2,\, y_3,\, y_1,\, y_5)` has `y_1` printed instead of `y_4` (flagged with `\ednote`).
  - p. 299: `\varphi'_i(y_4) \cdot \eta_1` has `\eta_1` printed instead of `\eta_4` (flagged with `\ednote`).
  - p. 310: `dio Jacobi'sche Fläche` has `dio` printed instead of `die` (flagged with `\ednote`).
  - p. 313: The running header has a printer error reading `213` instead of `313`. The canonical `\origpage{313}` is used in the transcription.

---

## 2. Mathematical Symbols & Expressions

- **Variables & Functions:**
  - Coordinate variables: $x_1, x_2, \dots, x_{r+2}$, $y_1, y_2, \dots, y_{r+2}$, $z_1, z_2, \dots$.
  - Algebraic equations: $f = 0$, $F = 0$.
  - Transforming polynomials / rational expressions: $\varphi_1, \varphi_2, \dots$, $\psi_1, \psi_2, \dots$.
  - Adjoint forms: $\varPhi$, $\varTheta$, $\varOmega$.
  - Determinants & Jacobians: $D$, $\varDelta$, $M$.
- **Greek Letters:**
  - `\varphi` (variant phi) throughout, matching the curly glyph in print.
  - `\varrho` (variant rho) used on p. 297.
  - `\varkappa` used in § 1 eq. (8) and on p. 297.
  - Capital Greek: `\varDelta`, `\varTheta`, `\varOmega`, `\varPhi` (slanted house style for variables/polynomials).
- **Derivatives & Primes:**
  - Partial derivatives: `\frac{\partial f}{\partial x_i}`, `\frac{\partial^\mu \varphi_i}{\partial y_1^\mu}`.
  - Prime notation for partial derivatives:
    - $\varphi'_i(y_j) \equiv \frac{\partial \varphi_i}{\partial y_j}$.
    - $F'(y_j) \equiv \frac{\partial F}{\partial y_j}$.
    - $f'(x_i) \equiv \frac{\partial f}{\partial x_i}$.
- **Summation & Product Signs:**
  - Capital upright `\Sigma` is used for alternating determinant permutations and coordinate sums:
    - `\Sigma \pm c_1 x_2 \dots x_{r+2}`
    - `\Sigma \pm \varphi'_1(y_1) \dots \varphi'_r(y_r) F'(y_{r+1})`
    - `\sum_{i}` and `\sum_{h}` when index bounds are explicitly specified.
- **Relations & Operators:**
  - Identity / equivalence: `\equiv` (e.g. `\Theta D \equiv A \cdot M + B \cdot F`).
  - Less-than-or-equal: `\leqq` (double-bar sort used in 19th-century Teubner prints).
  - Multiplication dot: `\cdot` in products with functions and coefficients (`\Phi_2 \cdot s^{m-2}`).
  - Dimension / multiplicity notation: `\infty^{2 \cdot r}`, `\infty^{2 \cdot h}`, `\infty^{2(r-1)}`, `\infty^{r-2}` (dot in exponent preserved where printed).
- **Determinants:**
  - Set with `\begin{vmatrix} \dots \end{vmatrix}`.

---

## 3. Structure & Layout

- **Title & Author:**
  - Title: verbatim from print: `Zur Theorie des eindeutigen Entsprechens algebraischer Gebilde von beliebig vielen Dimensionen.`
  - Author: `Von Max Noether in Göttingen.` (printed beneath title).
- **Sections:**
  - Headings are set as `\section*{§ 1.}` with `\subsection*{...}` for the subtitle.
  - § 1: `Eindeutiges Entsprechen von Flächen.` (p. 294)
  - § 2: `Eindeutiges Entsprechen von höheren Mannigfaltigkeiten.` (p. 298)
  - § 3: `Die algebraischen Differentialausdrücke und deren Integrale.` (p. 301)
  - § 4: `Die eindeutigen Transformationen.` (p. 305)
  - § 5: `Untersuchung der Determinante der Substitution.` (p. 307)
  - § 6: `Untersuchung der transformirten Ausdrücke $\Omega$.` (p. 310)
  - § 7: `Das Geschlecht der algebraischen Gebilde.` (p. 315)
- **Numbered Items:**
  - § 5 contains numbered cases `1.` through `6.`
  - § 6 contains numbered cases `1.` through `8.`
- **Equation Numbering:**
  - § 1 equations are tagged `\tag{1}` through `\tag{9}`.
  - § 3 restarts numbering with `\tag{1}`.
  - § 5 uses Greek parenthesized tags: `\tag{$\alpha$}`, `\tag{$\beta$}`, `\tag{$\gamma$}`, `\tag{$\delta$}`, `\tag{$\gamma'$}`, `\tag{$\varepsilon$}`.
  - § 6 restarts numbering with `\tag{1}` through `\tag{4}`.
- **Footnotes:**
  - Footnote marks in print use asterisks: `*)`.
  - Multi-page footnote on p. 304 continuing onto p. 305 is placed in full on p. 304 per Ruling R15.
- **Date & Place:**
  - At the end of the text (p. 316): `Göttingen, den 16. August 1869.`
