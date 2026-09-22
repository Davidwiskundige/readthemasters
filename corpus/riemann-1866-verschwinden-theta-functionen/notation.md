# Notation decisions — Riemann 1866, *Ueber das Verschwinden der $\vartheta$-Functionen*

Work-spanning rendering decisions for this transcription, ensuring that all pages (pp. 161–172)
maintain strict notational and typographic consistency. Each entry states the rule, the rationale,
and the forbidden alternatives.

## Symbols and Mathematics

- **Theta function symbol is `\vartheta`, never `\theta` or `\Theta`.**
  Write `$\vartheta(v_1, \ldots, v_p)$`, `$\vartheta$-Functionen`.
  The print uses the cursive Greek theta $\vartheta$ throughout.
  *Forbidden:* Do not write `\theta` or `\Theta`.

- **Vector argument abbreviation: `\overset{p}{\underset{1}{v}}(v_\nu)`.**
  Riemann introduces on p. 161 the shorthand notation of a letter ($v$ or $\varrho$) with upper limit $p$
  and lower limit $1$ to represent the system of $p$ arguments:
  `\overset{p}{\underset{1}{v}}(v_\nu)`, `\overset{p}{\underset{1}{v}}(r_\nu)`,
  `\overset{p}{\underset{1}{v}}(t_\nu)`, and on p. 171 `\overset{p}{\underset{1}{\varrho}}(t_\varrho)`.
  *Forbidden:* Do not modernize or replace with vector bold $\mathbf{v}$.

- **Derivatives of $\vartheta$:**
  First derivative: `{\vartheta'}_\mu` or `\vartheta'_\mu`.
  Higher derivatives: `\vartheta^{(n)}` or `\vartheta^{\mu,\nu}` as printed.

- **Summation and product limits:**
  Summations appear as `\sum_1^p`, `\sum_{\mu=1}^{\mu=p}`, `\sum_\mu`, or bare `\sum`.
  Products appear as `\prod_{\mu=1}^{\mu=m}`.
  Limits with explicit index assignments like `\mu=1` and `\mu=p` are transcribed as
  `\sum_{\mu=1}^{\mu=p}` and `\prod_{\mu=1}^{\mu=m}`.
  *Forbidden:* Do not modernize to `\sum_{\mu=1}^p`.

- **Greek letters:**
  Looped epsilon is `\varepsilon`, looped phi is `\varphi`, cursive rho is `\varrho`.
  Eta is `\eta`, zeta is `\zeta`, tau is `\tau`, psi is `\psi`, alpha is `\alpha`, beta is `\beta`.
  Crosscut values: $u_\nu^+$ and $u_\nu^-$ with superscripts $+$ and $-$.

- **Equation tags:**
  Equation numbers in the print are set with parentheses and a period: `(1.)`, `(2.)`, `(3.)`, etc.
  Transcribe as `\tag{(1.)}`, `\tag{(2.)}` inside `\[ ... \]`.

- **Display math wrapping (HOUSESTYLE R16):**
  All standalone formulas must be wrapped in `\[ ... \]`.
  Punctuation (commas, periods) ending formulas must be placed inside `\[ ... \]` before `\tag`.

## Typography and Orthography

- **Antiqua typesetting with `ss` throughout (no `ß`):**
  The original print is typeset in Latin Antiqua, using `ss` exclusively:
  `dass`, `muss`, `lässt`, `ausser`, `Grössen`, `schliessen`, `voraussetze`.
  *Forbidden:* Do not introduce `ß` (`daß`, `muß`, `Größe`).

- **Historical German orthography:**
  Preserve 19th-century spelling:
  `Function`, `Functionen`, `Theorie`, `Theil`, `Theile`, `Werthe`, `Abtheilung`, `Constanten`,
  `Grössen`, `Hülfe`, `reell`, `complex`, `unendlich klein`, `Veränderlichen`.
  *Forbidden:* Do not modernize (`Funktion`, `Teil`, `Werte`, `Konstanten`, `Größen`).

- **Emphasis:**
  Italicized names and words are marked with `\emph{...}`:
  e.g. `\emph{Abel}schen` (on p. 161, where "Abel" is italic and "schen" is upright),
  `\emph{B.~Riemann}` in the byline.

- **Superscripts in abbreviations:**
  `54^{\text{sten}}` or `54\textsuperscript{sten}`.

## Document Structure

- **Section headings:**
  Articles are numbered `1.`, `2.`, `3.`, `4.`, `5.`, `6.` without "Art." or "§".
  Set with `\section*{1.}`, `\section*{2.}`, etc.
  In-text references refer to them as `§.~4`, etc.

- **Page boundaries:**
  Every page fragment begins with `\origpage{N}`.
  A page opening mid-sentence has no blank line after `\origpage{N}`.
  Hyphenated words across page turns are completed on the page where they begin.
