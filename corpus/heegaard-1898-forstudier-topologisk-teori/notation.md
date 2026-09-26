# Notation decisions — Heegaard 1898, *Forstudier til en topologisk Teori for de algebraiske Fladers Sammenhæng*

Work-spanning rendering decisions for this transcription, ensuring that all pages (pp. 1–97 plus Errata and Theses pp. 98–100)
maintain strict notational and typographic consistency. Each entry states the rule, the rationale, and forbidden alternatives.

## Mathematical Symbols and Formulas

- **Display math wrapping (HOUSESTYLE R16):**
  All standalone displayed formulas must be wrapped in `\[ ... \]`.
  Multiline formulas must be enclosed in `\[ \begin{aligned} ... \end{aligned} \]` or `\[ \begin{gathered} ... \end{gathered} \]`.
  *Forbidden:* Bare `\begin{align*}` or `\begin{gather*}` outside `\[ ... \]`.

- **Display math punctuation:**
  Display formulas must preserve trailing punctuation (periods, commas, semicolons) exactly as printed in the scan.

- **Coordinate systems and indices:**
  - Real and imaginary coordinate splits are denoted by subscripts: $X_1, X_2$, $y_1, y_2$, $z_1, z_2$, $u_1, u_2$, $v_1, v_2$.
  - Subscripts must always be braced: `$X_{1}$` or `$X_1$`, `$a_{i}$`, `$p_{m-1}$`.
  - Superscripts and powers: `$a_1^2 + a_2^2$`.
  - Coordinates in 4-space: $X_1, X_2, Y_1, Y_2$ or $(x_1, y_1, x_2, y_2)$.

- **Partial derivatives and Jacobians:**
  - Jacobians and functional determinants use partial derivative symbol `\partial`:
    `\frac{\partial(y_1, y_2, \dots)}{\partial(x_1, x_2, \dots)}`.
  - Differentials use thin space: `\,dx`, `\,dy`, `\,dt`.

- **Greek letters:**
  - Standard mathematical Greek letters: `\alpha`, `\beta`, `\gamma`, `\delta`, `\eta`, `\theta`, `\xi`, `\pi`, `\varphi`, `\psi`, `\omega`.
  - Capital Greek for manifolds/surfaces: `\Phi`, `\Psi`, `\Omega`, `\Sigma`.

- **Connectivity numbers and topological notation:**
  - Connectivity / Betti numbers: $p_1, p_2, \dots, p_m$ or $P_1, P_2, \dots$.
  - Equivalence / homology: `\sim` or `\equiv` (transcribe strictly as printed).
  - Torsion coefficients and matrices: transcribed as standard LaTeX arrays.

- **Author's Errata (TRYKFEJL, p. 98 / HOUSESTYLE R4):**
  - All errors listed in Heegaard's own errata table (*Trykfejl*, p. 98) must be transcribed faithfully as printed in the body, with an immediate `\ednote{...}` explaining the author's erratum.
  - Per R18, no curly braces inside `\ednote{...}` prose (inline math like `$a_1 - i a_2$` is permitted).

- **Footnotes (HOUSESTYLE R15):**
  - Footnotes use the print's own asterisk mark: the in-text callout is `${}^{*)}$` and the note is led by `\textbf{*)}` placed inline at the foot of that page's text.
  - *Forbidden:* Bare `\footnote{...}`.

## Typography and Orthography

- **Danish 19th-century orthography (pre-1948 reform):**
  - Retain `aa` everywhere (never normalize to `å`): `altsaa`, `gaa`, `staa`, `faa`, `Bærerplan`, `Aarsag`, `Maaned`.
  - Retain capital letters on all substantive nouns: `Planen`, `Fladen`, `Punkt`, `Punkter`, `Mangfoldighed`, `Kurver`, `Linier`, `Retning`, `Kotetal`, `Hank`, `Traad`.
  - Retain archaic verb and adjective plurals: `ere`, `have`, `bleve`, `kunne`, `ville`, `skulde`.
  - Retain historical spellings: `eentydig`, `flertydig`, `kompleks`, `imaginær`, `projektive`, `Asymptoter`, `Cirkel`.
  - *Forbidden:* Do not modernize Danish spelling or grammar.

- **Quotation marks:**
  - Literal Danish low-high quotation marks `„ … “` are used for quoted terms and chapter titles.
  - In French or foreign quotations (e.g. Picard, Poincaré citations), use the punctuation printed in the scan.

- **Emphasis:**
  - Letterspaced type (Sperrung) in the original Danish print indicates emphasis or defined terminology: render as `\emph{...}`.

- **Abbreviations:**
  - Abbreviation periods carry LaTeX spacing: `p.\ `, `Pag.\ `, `Bd.\ `, `Fig.\ `, `Cap.\ `, `f.\ Eks.\ ` (for eksempel), `o.\ s.\ v.\ ` (og saa videre).

## Figures and Document Structure

- **Figures (Plates):**
  - Figures are referenced as `\rmfigure{figures/fig-XX.png}{<fig-num>}{<alt-text>}`.

- **Document Structure:**
  - Division into `FØRSTE AFSNIT`, `ANDET AFSNIT`, `SLUTNING`, `TRYKFEJL`, `TESER`.
  - Sections headed by `§ 1.`, `§ 2.`, etc.
  - Page markers: strictly contiguous `\origpage{N}` at each page boundary.
  - Seamless page boundary joins: mid-sentence page breaks must have no blank line following `\origpage{N}`.
