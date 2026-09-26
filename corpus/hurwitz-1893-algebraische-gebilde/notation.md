# Notation and Conventions: Hurwitz (1893)

*Ueber algebraische Gebilde mit eindeutigen Transformationen in sich*
Adolf Hurwitz, *Mathematische Annalen* 41 (1893), pp. 403–442.

This document records the typographic, mathematical, and structural conventions of the original printing in *Mathematische Annalen* and their exact representation in the ReadTheMasters LaTeX transcription.

---

## 1. Typography & Text Conventions

- **Typeface & Script:** Set in Antiqua (Latin script) throughout for both body text and mathematics.
- **Orthography:** 19th-century German orthography is preserved faithfully:
  - Antiqua round *s* / *ss* is used throughout: `dass`, `muss`, `lässt`, `schliessen`, `Schluss` (the letter `ß` is not used in the original print).
  - Silent `h` in words such as: `Theorie`, `Theil`, `theilbar`, `Theilung`, `Theilwerthe`, `Hülfe`, `nothwendig`, `Werth`, `Werthe`, `Werthsysteme`.
  - Initial `C` in `Curve`, `Curven`, `Coefficient`, `Coefficienten`, `Constante`, `Constanten`, `Complexion`.
  - Umlaut spelling: `Ueber` in title and headings; `Oeffnungen`, `ausserdem`.
  - Characteristic 19th-century forms: `Function`, `Functionen`, `Punkt` / `Punkte`, `Mannigfaltigkeit`, `resp.`, `u. s. w.`
- **Emphasis:**
  - Letterspaced emphasis (*Sperrung*) is rendered with `\emph{...}`.
  - Names in Sperrung (e.g. `\emph{Schwarz}`, `\emph{Weierstrass}`, `\emph{Klein}`, `\emph{Poincaré}`, `\emph{Picard}`) are set with `\emph{...}`.
- **Quotations & Punctuation:**
  - German low quotes: `„…“` (literal Unicode).
  - Em-dash: `---` for thought breaks.
  - En-dash: `--` for page and number ranges.
  - Abbreviation spacing: `i.~Pr.`, `z.~B.`, `u.~s.~w.`, `d.~h.`

---

## 2. Mathematical Symbols & Expressions

- **Variables & Genera:**
  - $p$: Genus (*Geschlecht*) of the original algebraic Riemann surface $F$.
  - $\pi$: Genus (*Geschlecht*) of the quotient Riemann surface $F_0$.
  - $N$: Order of the group of transformations / sheet number of the branched covering.
  - $w$: Number of branch points ($a_1, a_2, \dots, a_w$).
  - $r_1, r_2, \dots, r_w$: Branch orders / periods of the branch points.
  - $W$: Total branch number (*Verzweigungszahl*): $W = \sum (N - \frac{N}{r_i})$.
  - Riemann–Hurwitz formula: $2p - 2 = W + N(2\pi - 2)$.
- **Greek Letters:**
  - `\varphi` (variant phi) for functions and substitutions.
  - `\psi`, `\vartheta`, `\eta`, `\chi` as printed.
  - Capital Greek: slanted/standard `\varPhi`, `\varPsi`, `\varOmega` where appropriate.
- **Relations & Inequality Operators:**
  - Less-than-or-equal: `\leqq` (double-bar, standard Teubner printing). **Forbidden alternative:** `\le` or `\leq`.
  - Greater-than-or-equal: `\geqq` (double-bar, standard Teubner printing). **Forbidden alternative:** `\ge` or `\geq`.
  - Equivalence / congruence: `\equiv`.
- **Large Operators:**
  - Inline `\sum` and `\prod` must always carry `\displaystyle`: `$\displaystyle\sum_{i=1}^w \dots$`. **Forbidden alternative:** bare inline `\sum` without `\displaystyle` (machine-enforced by `houselint.py`).
  - Displayed summations use standard `\sum` inside `\[ ... \]`.
- **Display Math & KaTeX Compatibility:**
  - All display equations must be enclosed in `\[ ... \]`. **Forbidden alternative:** bare `\begin{equation}`, `\begin{align*}`, or `$$ ... $$`.
  - Multiline displayed formulas must use `\[ \begin{aligned} ... \end{aligned} \]` or `\[ \begin{gathered} ... \end{gathered} \]`.
  - Equation tags go on the right via `\tag{...}` inside `\[ ... \]`.
- **Differentials & Integrals:**
  - Differentials receive thin space: `\,dz`, `\,dx`, `\,du_i`.
  - Integrals of the first kind: $u_1, u_2, \dots, u_p$ or $v_1, v_2, \dots, v_p$.

---

## 3. Figures & Apparatus

- **Figures:**
  - Two figures exist in the paper, both in Section II (pp. 414–415):
    - `\rmfigure{figures/fig-1.png}{Fig.~1.}{Canonical dissection of Riemann surface of genus $p = 2$ with cross-cuts $a_1, b_1, a_2, b_2$}`
    - `\rmfigure{figures/fig-2.png}{Fig.~2.}{Dissection of Riemann surface showing branching cuts radiating to branch points}`
  - Captions contain only the printed figure label (`Fig.~1.`, `Fig.~2.`); descriptive information is in the alt-text argument.
- **Footnotes:**
  - Placed at the end of the printed page where they occur, led by `\textbf{*) }` or `\textbf{**) }`, with superscript `${}^{*)}$` in text.
- **Editorial Notes:**
  - Flag compositor errors with `\ednote{...}`.
  - No text-mode curly braces in the note prose (inline math `$x$` is allowed per R18).

---

## 4. Structure & Sectioning

- Title: `\section*{Ueber algebraische Gebilde mit eindeutigen Transformationen in sich.}`
- Author: `Von \emph{A. Hurwitz} in Königsberg i.~Pr.`
- Introduction: pp. 403–405.
- Three main sections:
  - `\section*{I. Abschnitt.}` (pp. 405–414, containing numbered items `1.`, `2.`, `3.`)
  - `\section*{II. Abschnitt.}` (pp. 414–427, containing numbered items `4.`, `5.`, `6.`, `7.`, `8.`)
  - `\section*{III. Abschnitt.}` (pp. 427–442, containing numbered items `9.`, `10.`, `11.`, `12.`, `13.`, `14.`, `15.`)
- Concluding place and date (p. 442): `Königsberg i.~Pr., 10.~Februar 1892.`
