# Notation decisions — Noether 1871, *Ueber die algebraischen Functionen einer und zweier Variabeln*

Work-spanning rendering decisions for this transcription, following `prompts/transcribe-chat.md`
and `corpus/HOUSESTYLE.md`. The whole paper, pp. 267–278, follows this list.

## Symbols

- **Zero is the digit `0`, not the letter `o`.** Write `$x_1 = x_2 = 0$`, `$C = \ldots = 0$`,
  `$F = \ldots = 0$`, `$\leqq 0$`. Unlike the 1869 Göttingen note (which set lowercase roman *o*
  for zero throughout), the 1871 print sets standard tall digit zeros in every equation. Never
  regularize to `o`.
- **Inequality and order relations:**
  - **`\leqq` for less-than-or-equal-to:** The print uses the double-bar sort (e.g.
    `$\mu + \nu - 1 \leqq n$`, `$\nu \leqq \mu$`, `$\leqq 0$`). Never `\le`, never `\leq`.
  - **`>` and `<` are standard ASCII:** `$2\mu - 1 > n$`.
- **Multiplication:**
  - **Products in denominators and indices are set with plain periods on the baseline:** `1.2` in
    denominators `\frac{\nu(\nu-1)}{1.2}`, `\frac{(2n-2)(2n-3)}{1.2}`, `\frac{\varrho(\varrho-1)}{1.2}`.
    Never `\cdot`, never `\times`.
  - Spaced products in display math use a period with LaTeX spacing `.\;` if separated.
- **Ellipses:**
  - **Ellipses in argument lists and formulas are `\ldots`:** `$x_1, x_2, \ldots$`,
    `$1, 2, \ldots 7$`, `$+\ldots+ f_n(x) = 0$`. Never literal periods, never `\cdots`.
- **Greek letters:**
  - Looped italic phi: `\varphi` — never `\phi`.
  - Looped rho: `\varrho` — never `\rho`.
  - Lowercase kappa in series expansions (pp. 276–277): `\varkappa` (`\xi_4 = \varkappa \xi_1^{\varrho-1} + \ldots`,
    `\xi_4 = \pm \varkappa \xi_1^{\frac{2\varrho-1}{2}}`).
  - Summation operator on p. 277: `\Sigma_i` (Clebsch/Noether notation, capital Greek sigma with
    subscript `i`) — never `\sum_{i}`.
  - Surface and coordinate systems: `\Phi` (capital Phi), `\Pi` (capital Pi for point `\Pi`),
    `\Omega_{2m}` (capital Omega), `\xi_1, \xi_2, \xi_3, \xi_4`, `\psi_2`.
- **Primes on variables:**
  - Transformed curves, surfaces, and points take standard primes: `$C'$`, `$C''$`, `$F'$`, `$E'$`,
    `$K'$`, `$P'$`.

## Typography

- **No `ß` anywhere.** This Antiqua typesetting uses round *s* throughout: `dass`, `muss`,
  `lässt`, `ausser`, `Grössen`, `Schliesslich`. Never "correct" these forms.
- **German quotation marks are literal German guillemets `» … «`:** set tight against the quoted
  text (`»Nachrichten«`, `»postulation«-Formel`, `»Uebergangscurve«`, `»Curvengeschlecht«`, and around
  the two theorem statements on pp. 276 and 277).
- **Ordinal suffixes are superscripted on math:** `$n^{\text{ter}}$ Ordnung`,
  `$2n^{\text{ter}}$ Ordnung`, `$(\nu-1)^{\text{ten}}$ Ordnung`, `$(m-4)^{\text{ter}}$ Ordnung`,
  `$(m-3)^{\text{ter}}$ Ordnung`, `$4^{\text{ter}}$ Ordnung`, `$6^{\text{ter}}$ Ordnung`,
  `$3^{\text{ter}}$ Ordnung`.
- **A Greek letter glued to a German word:** `$\nu$facher Punkt`, `$\mu$fachen`, `$\nu$fache Kante`,
  `$2i$fache`, `$(2i+1)$fache`.
- **Colons in projective coordinates are spaced:** `$y_1 : y_2 : y_3 = x_2 x_3 : x_3 x_1 : x_1 x_2$`,
  `$x_1 : x_2 : x_3 : x_4 = y_1 y_4 : y_2 y_4 : y_3 y_4 : \varphi_2(y_1, y_2, y_3)$`.
- **Abbreviation dots take a LaTeX control space:** `Bd.\ 3.`, `pag.\ 180.`, `vol.\ VII.`,
  `p.\ 212.`, `d.\ h.`.
- **Apostrophes in names use plain ASCII `'`:** `Cayley'schen`, `Puiseux'schen`, `Jacobi'sche`.

## Structure

- **Section headings are roman numerals with a period:** `\section*{I.}`, `\section*{II.}`,
  `\section*{III.}`.
- **Footnotes are numbered with a single closing parenthesis:** `${}^{1)}$`, `${}^{2)}$`, led at the
  bottom of the page by `\textbf{1)}`, `\textbf{2)}`.
- **Braced systems of equations:** Wrap in `\[ \begin{aligned} ... \end{aligned} \tag{n} \]` per
  HOUSESTYLE R16.
- **Printer's errors:** Transcribe faithfully with an attached `\ednote{...}` per HOUSESTYLE R4.
  No curly braces in the ednote prose (R18).
