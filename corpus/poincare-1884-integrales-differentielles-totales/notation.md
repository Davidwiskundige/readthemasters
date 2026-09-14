# Notation decisions — Poincaré 1884

Cross-page rendering decisions for Henri Poincaré's 1884 *Comptes rendus* note,
*Sur les intégrales de différentielles totales* (t. XCIX, pp. 1145–1147),
established under HOUSESTYLE R27.

## Figures and letters

- **Old-style figures are transcribed as ordinary digits.** Digits in text and math are standard
  ASCII digits: `0`, `2`, `4`. **Do not** write letter `o` for zero.
- **Points are plain italic math letters:** `$M_{1}, M_{2}, \ldots, M_{q}$` and
  `$M'_{1}, M'_{2}, \ldots, M'_{q}$`. Upright type in the 19th-century French print is presentation,
  not notation (R1). **Do not** write `\mathrm{M}`, `\mathbf{M}`, or `\pt`.
- **Greek letters:**
  - `\varphi` (looped phi) for the surface polynomials $\varphi, \varphi_{1}$. **Do not** write `\phi`.
  - `\psi` for the parameter relation $\psi(a, b) = 0$.
  - `\alpha`, `\beta`, `\gamma` for the polynomial numerators.
  - `\lambda`, `\mu`, `\nu` and primed `\lambda'`, `\mu'`, `\nu'` for constant denominators.
    The denominator $\nu$ is Greek nu, not Latin $v$.
- **Uppercase polynomials:** `$Z_{2}$` and `$Z_{4}$` for the polynomials in $z$.

## Subscripts, exponents, primes

- **Subscripted indices are always braced:** `$M_{1}$`, `$\varphi_{1}$`, `$u_{1}$`, `$Z_{2}$`,
  `$Z_{4}$`. **Do not** write bare `M_1`, `\varphi_1`, or `Z_2`.
- **Primes precede subscripts:** `$M'_{1}$`, `$M'_{2}$`, `$M'_{q}$`, `$u'_{1}$`, `$u'_{2}$`,
  `$u'_{q}$`. The ASCII apostrophe prime comes before the braced subscript `_{1}`.
  **Do not** write `M_{1}'`, **do not** write `\prime`, **do not** use Unicode `′`.
- **Coefficients with primes:** `$a', b', c', a'', b'', c''$`.

## Differentials, fractions, and operators

- **Differentials carry a thin space:** `\,dz`. **Do not** write bare `dz`.
- **Fractions in display:** Standard `\frac{...}{...}` inside displays.
- **Proportions / continued equations:**
  ```latex
  \[
  \frac{\alpha}{\lambda} = \frac{\beta}{\mu} = \frac{\gamma}{\nu},
  \]
  ```

## Displays and alignment

- **Display math punctuation:** Trailing commas and periods are kept inside `\[ ... \]`, matching
  the printed punctuation.
- **Three-equation system on p. 1147:** Formatted with `\begin{gathered}`:
  ```latex
  \[
  \begin{gathered}
  \varphi(x, y, z, a, b) = 0, \\
  \varphi_{1}(x, y, z, a, b) = 0, \\
  \psi(a, b) = 0.
  \end{gathered}
  \]
  ```
  **Do not** use `cases`, `array`, `gather` or `eqnarray`.
- **Terminal quote mark on p. 1147:** The note ends on a displayed formula. To avoid KaTeX
  unrecognized unicode character warnings inside math mode, the closing guillemet is placed
  immediately following the closing display delimiter: `\]»`.

## Structure and typography

- **Comptes Rendus quotation marks:** Following Academy convention for quoted communications
  (R22), a single « opens the first paragraph on p. 1145, » heads each following paragraph on
  pp. 1146 and 1147, and » closes the communication at the end of p. 1147. Written as literal
  Unicode characters tight against the text.
- **Heading:**
  `\section*{Analyse mathématique. --- Sur les intégrales de différentielles totales. Note de M.~H.~Poincaré, présentée par M.~Hermite.}`
  No text-mode braces inside the section title (R25).
- **Emphasis:** `\emph{déterminée}` on p. 1146; `\emph{les plus généraux de leurs degrés}` on p. 1147.
- **Hyphenation and page joins:**
  - p. 1145 ends with a complete paragraph.
  - p. 1146 ends mid-sentence (`deux`); p. 1147 opens with `paramètres` with **no blank line**
    following `\origpage{1147}`.
- **Page furniture omitted:** Running heads, volume/issue notices, and page numbers are not
  transcribed.
- **Unrelated Academy items omitted:** Preceding items on p. 1145 and the subsequent note by
  Émile Picard on p. 1147 are omitted.

## Printer's errors reproduced (R4)

- **p. 1146, display 1:** `x^{2}(az^{2} + 2b - z + c)`. The print sets a dash/hyphen between
  `b` and `z`. Kept as printed and flagged with `\ednote`.
- **p. 1146, line 11:** `deux polygones de degré 2 et 4 en $z$`. The print sets `polygones` for
  `polynômes`. Kept as printed and flagged with `\ednote`.
- **p. 1146, line 14:** `» Il est ailleurs aisé de voir`. The print sets `ailleurs` for `d'ailleurs`.
  Kept as printed.
- **p. 1146, line 18:** `» De inême`. The print sets `inême` for `même`. Kept as printed.
