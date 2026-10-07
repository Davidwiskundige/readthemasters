# Notation decisions — abel-1827-recherches-fonctions-elliptiques

Cross-page rendering decisions for this work. Batches cannot see each other; follow these exactly.
Each entry states the rule, then what NOT to do.

## Differentials and derivatives
- The author's `∂` is a differential sign (`∂x`, `∂θ`, `∂y`, `∂.Φα`). Write `\partial` everywhere: `\partial x` in fractions, `R\,\partial x` or `R.\partial x` after an integrand. Do NOT use `d` or `\mathrm{d}`.
- A partial derivative printed as a parenthesized fraction stays parenthesized: `\left(\frac{\partial r}{\partial\alpha}\right)`. Do NOT drop the parentheses.

## Letters
- Two distinct glyphs are printed for the function: large `Φ` and small `φ`. Reproduce each as printed: `\Phi` / `\varphi`. Do NOT normalize one to the other (R23). Batch 1 judged them from glyph size and flagged the choice for the verifier, so treat a doubtful case as printed and report it.
- `ω` is `\omega`; the second period is `\varpi` (NOT `\pi`). `ε` is `\varepsilon` (NOT `\epsilon`). The angle is `\theta`.
- The infinite value `1/0` is `\frac{1}{0}`. The small 0 is the zero, not the letter o or b. Do NOT write `\infty`.
- The constant `b` (in b/c, b/e) is the letter b; a mark printed above it on one page is a scan blemish, not a diacritic.
- Roman `m` is `\mathrm{m}` only where the print sets it upright (p103: `\mathrm{m}^{2}-1`, `\mathrm{m}+1`); elsewhere italic `m`.

## Radicals
- Always `\sqrt{...}` keeping the printed inner parentheses or brackets inside the braces: `\sqrt{(1-c^{2}x^{2})}`, `\sqrt{[(1-c^{2}x^{2})(1+e^{2}x^{2})]}`. Do NOT drop the printed `( )` or `[ ]`, and do NOT write a fractional power.

## Multiplication
- The baseline `.` between factors (`fα.Fβ`, `Φα.Φ'α`) is a plain period in math, written TIGHT: `f\alpha.F\beta`. Do NOT use `\cdot` or `\times`, and do NOT add `\;` after it. A literal space is not spacing in math mode.
- Exception: a raised `·` (p102, `(A+By²)/(C+Dy²) · ∂y/√…`) is `\cdot`.
- Where factors are printed with no dot (`e²c²φ²α`, `φα φβ`), add no dot; use `\,` only where the printed gap is visible.

## Function arguments
- Follow the print: `Φα` is `\Phi\alpha` and `Φ(α)` is `\Phi(\alpha)`. Do NOT regularize either form (R23). Large parentheses around fractions or radicands are `\left(...\right)`.

## Equations
- The author's equation numbers carry a period: `\tag{n.}`, e.g. `\tag{1.}`, `\tag{12.}`; a primed one is `\tag{22$'$.}`. Do NOT write a bare `\tag{n}` and do NOT auto-number. In-text references `(1.)`, `(10.)` are copied verbatim with the period.
- Brace systems: `\left\{\begin{aligned}...\end{aligned}\right.` inside `\[ ... \tag{n.} \]`. Several clauses on one line separated by `;` stay on one line. Do NOT use `gathered` for a system.
- `½` in a display is `\tfrac{1}{2}`, as in `(m+\tfrac{1}{2})\omega`; inline in running text it is `\frac{1}{2}`.
- `et` / `ou` between equations are plain text (`\text{et}`), not italic math.
- A lower limit printed with no upper limit is `\int_{0}`; with both, `\int_{0}^{x}`.

## Structure and text
- Title: `\section*{Recherches sur les fonctions elliptiques.}`, then the byline paragraph `(Par M. \emph{N. H. Abel}.)`. The printed article number "12." above the title is not transcribed.
- `§. I.` is `\section*{§. I.}`; numbered articles `1.`, `2.`, … are `\subsection*{n.}` (keep the period). Do NOT put `\emph` inside a heading.
- Letterspaced names and words are `\emph`: `M. \emph{Legendre}` (the `M.` outside), `\emph{Euler}`, `\emph{réelles}`, `\emph{périodiques}`.
- Footnote: `${}^{*)}$` in the text and `\textbf{*)} …` at the end of the page.
- Keep the edition's own spelling and accents: longtems, tems, rationelle, connoît, resolubles, parcequ'on, `l'equation`, `differentiant`, `verifiera`, `ou` for `où`. Do NOT modernize. Long ſ is rendered as `s` (`Aussi`, never `Aufsi`).
- `Par ex.\ on` takes a control space after the abbreviation dot (R17).
- Hyphenation at line ends is removed; hyphens printed inside words (`c'est-à-dire`, `quelques-unes`) are kept, and none is added to `ci dessus`.
- Printer's errors are reproduced and marked `\ednote{...}` (R4), never silently corrected. Place the `\ednote` on the line AFTER the display; never inside a `\[ \]` display (it breaks KaTeX).
- Sub-titles under a section number (`Formules, qui donnent …`, `Résolution des équations`) are a letterspaced paragraph under `\section*{§. II.}`, with `\emph` on the letterspaced words and math left outside the `\emph`. Do NOT make them `\subsection*`. Letterspaced run-in headings such as `Si n est un nombre pair.` are also `\emph`; math may sit inside.
- A `\tag{n.}` goes only on a single-equation display. Several stacked numbered equations (36/37, 38/39, 63/64) are separate `\[ \]` displays, one tag each. Do NOT put `\tag` inside `aligned` or `gathered` rows.
- A comment printed beside a brace for two displays (the 63/64 comment) is a flush-left line after both displays.
- Primes and subscripts: `P'_n`, `P''_n`, `P_{n+1}` (never `\prime`). Large-parenthesis arguments with fractions use `\left( \right)` with `\frac`.
- Φ/φ: small `φ` is `\varphi` only where the print visibly sets the small glyph (batch 2: formula (12) as applied, p113 `2φ(...)`, `φ²(...)`; p115 `2φ(nβ)`, eq. 35 `φβ`, `φ⁴β`, `c²e²φ²β`; p116 first line `c²e²φ²β.P²`). Everything else, including `Φ²β` in eqs. 36–39, is `\Phi`. Judged by glyph size; the verifier re-checks.
- Page furniture is dropped: `Crelle's Journal. II. Bd. 2. Hft.`, sheet signatures (`16`, `16*`), catchwords at the foot of a page (`En`, `en`).
- Summation: the print's `Σ` is the letter Sigma with the limits stacked on it and the index letter as a subscript of the whole stack: `\overset{+n}{\underset{-n}{\Sigma}}_{m}`. Do NOT use `\sum` or `\sum_{m=-n}^{+n}`. A sum with limits and no index letter takes no subscript (`\overset{+n}{\underset{-n}{\Sigma}}\psi(m+k)`); do NOT add an `_{m}` the print does not show.
- An n-th root with the index over the radical is `\sqrt[2n+1]{[...]}`, `\sqrt[4]{(...)}`, printed inner brackets kept. Do NOT use a fractional power. A fractional exponent printed as a small fraction over a bracket is `[...]^{\frac{k}{2n+1}}`, NOT `^{k/(2n+1)}`.
- Ordinal suffixes: `(2n+1)^{\text{ième}}`, `^{\text{ème}}`. Do NOT use `\mathrm` or a bare `ième` in math.
- A printed row of dots between displayed lines is `\cdots\cdots\cdots` on its own `aligned` row. Do NOT use `\vdots` and do NOT drop the row.
- Indices on ψ keep the print's placement: `\psi_{2}`, `\psi_{3}`, `\psi_{1}^{k}`, `\psi^{1}`, `\psi_{1}^{1}`. Do NOT write `\psi^{(k)}` and do NOT normalize `\psi^{1}` to `\psi_{1}`.
- Φ/φ per page (judged by glyph size, verifier re-checks): pp. 125–128 small φ except the explicit large Φ (Φα, Φ, f, F on p125; Φβ=x on p128; Φα, fα, Fα on p127); p129 Φ for the outer Φβ and Φ(2n+1)β, φ inside λ; pp. 130 and 132 small φ, φ₁; pp. 131 and 134–136 large Φ, Φ₁; p133 large Φβ, Φ₁β, small φ inside the sums. Do NOT normalize globally.
- Product: `Π` takes the same stacked-limit form as Σ: `\overset{k'}{\underset{k}{\Pi}}_{m}`. Do NOT use `\prod` or `\prod_{m=k}^{k'}`. A double sum or product repeats the stack per index (`\overset{k'}{\underset{k}{\Sigma}}_{m}\overset{\nu'}{\underset{\nu}{\Sigma}}_{\mu}`); do NOT merge them into one stack.
- A multi-line display with ONE printed number and a left brace (eqs. 97, 100, 102, 103, 123, 125) is `\left\{\begin{aligned}...\end{aligned}\right.` with one `\tag{n.}` after the aligned block. Do NOT use `gathered`; no tag inside a row. A system whose brace is printed on the RIGHT is `\left.\begin{aligned}...\end{aligned}\right\}` followed by `\ \text{pour }...`.
- n-th root of a variable is `\sqrt[n]{v_{k}}`; a fractional exponent printed over `v` is `v^{\frac{1}{n}}`, `v^{\frac{n-1}{n}}`. Do NOT write `v^{1/n}`.
- Rows of baseline dots inside a sum or system are `\ldots\ldots`; a full-width printed dot row on its own line is `\cdots\cdots` on its own aligned row. Do NOT use `\vdots`.
- Quoted passage (p146): one pair of quotation marks in the edition's glyphs; the repeated line-start marks are dropped (R22).
- A letterspaced subtitle of a section (§. VI) is entirely `\emph{...}`, math outside it. `Gaufs` is `\emph{Gauss}` (long ſ rule).
- `\pm` where the print sets ±, including an underlined plus (p138 eq. 91, p143 `a_{n+m}=\pm a_m`).
- Φ/φ on pp. 137–148: large `\Phi` throughout, except p142's line `quantités φ(ω/2m+1); φ(ϖi/2n+1)` and the p148 fractions `\varphi(2n+1)\beta/\varphi\beta`, which are small. Judged by glyph size; the verifier re-checks.
- Missing apostrophes and spaces in the print are supplied (`l'équation`, `au lieu`).
- A printed row of four or more baseline dots INSIDE math on pp. 158–160 is written as raw periods matching the printed count (`....`, `......` in eq. 145), because the dots are the author's punctuation. Do NOT use `\ldots`, `\cdots` or `\vdots` for those. (Dot rows between displayed lines and short `\ldots` runs follow the earlier entries.)
- The upper limit printed as a small stacked "1 over 0" (eq. 145) is `\overset{\frac{1}{0}}{\underset{0}{\Sigma}}`, following the infinite-value rule; the printed ∞ in eq. 146 is `\infty`. Do NOT swap them.
- A lower limit printed as the small numeral "ı" under Σ or Π is the digit 1 (`\underset{1}`), NOT `I` or `l`.
- Superscript index on `v` is `v_{\mu}^{1}`, NOT `v^{(1)}` or `v_{\mu 1}`. The printed `lim.` is `\text{lim.}`, NOT `\lim`.
- A case label `a)` / `b)` opening a paragraph is `$a)$` / `$b)$` in math italic, NOT `\emph` or roman.
- Φ/φ on pp. 149–160 (glyph size; verifier re-checks): large `\Phi` for `Φ(2n+1)β` and `(2n+1)Φβ` in eqs. 126, 129, 130; `Φβ` in running text (pp. 150, 153); `Φ²β` in the p153 first display; `Φα` in text and headings on pp. 154–155 and in eqs. 132, 134; and the `Φ( )` inside the braced sums of eq. 132 and the left sides of the `A_m`, `B_μ` displays on p155. Everything else is small `\varphi` (product factors in 128–130', `φ²β` and `φ(α/(2n+1))` in 132, 133, 138, and all of pp. 157–158).
- A primed equation number is `\tag{130$'$.}`.
- An equation number printed alone at the foot of a page (e.g. `178.` under p172) is a catchword for the next page's display and is dropped. Do NOT transcribe a trailing number with no display after it.
- Σ and Π with a variable upper limit keep the variable in the stack: `\overset{\mu}{\underset{1}{\Pi}}`. Do NOT rewrite it to `n`. An index letter is added only where the print shows one.
- Latin italic `a` (a limit value, pp. 165–166) is `a`, NOT `\alpha`; `\Phi^{2}a` has large Φ.
- Dot rows inside math: four dots `....`, five dots `.....`; three dots after a minus (eq. 155) are `\ldots`. Do NOT use `\cdots` or `\vdots`.
- A bare `etc.` under or after a display is `\text{etc.}` as a last `gathered` row, or a trailing `\ \text{etc.}` on the same line. Do NOT drop it. A stack of equations printed as one centred group is `aligned` or `gathered` with no tag inside a row; a single printed number goes after the block.
- Φ/φ on pp. 161–172 (glyph size, confirmed by magnification): large `\Phi` for Φα in text and displays on pp. 161, 162, 171, 172; the `Φ( )` in `-iec.\Phi(...)` on p163; `\Phi^{2}a` on p165; `\Phi^{2}\alpha` on p167; `e^{2}c^{2}\Phi^{2}(...)` on p171. Small `\varphi` for everything else. Do NOT normalize globally.
- Paragraphing at about 8–10 px indent was treated as a flush-left continuation, not a new paragraph (p163, p166); the verifier checks these against the print.
- French spacing before a colon is normalized to none; a missing space in the print (`on auraégalement`) is supplied (`on aura également`).
