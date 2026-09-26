# Notation glossary — dedekind-weber-1882-algebraische-functionen

Cross-page rendering decisions for this work. Every batch follows these exactly.

## Title, authors, headings (from batch 1, pp. 181–192)

- Title line as printed: "Theorie der algebraischen Functionen einer Veränderlichen." — set as
  `\section*{...}` on p. 181 (Clebsch 1864 Crelle precedent).
- Author line as printed, as a plain paragraph with the names in `\emph`:
  "(Von den Herren \emph{R.\ Dedekind} in Braunschweig und \emph{H.\ Weber} in Königsberg.)"
- Part and introduction headings are `\section*`: `\section*{Einleitung.}`, `\section*{I. Abtheilung.}`.
- A § heading is ONE `\subsection*` that joins the number to its small-type subtitle, using a
  literal § and a tie: `\subsection*{§~1. Körper algebraischer Functionen.}`. Do NOT use `\S`, do
  NOT put the subtitle on a separate line, and do NOT use `\emph` inside a heading.
- In running text, "§ 1" is written `§~1` (a literal § followed by a tie).
- Numbered propositions ("1.", "2.", …) are plain text at the start of the paragraph. NOT
  `enumerate`, NOT bold.

## Letters and symbols

- Fraktur is notation: always `\mathfrak{...}`. From p. 191 on, the system of integral functions is
  `$\mathfrak{o}$`. Never write it as a roman or italic o, and never as the digit 0.
- The variable is plain `$z$`. The print's ʒ-shaped z is only the typeface.
- θ is `\theta` (NOT `\vartheta`). φ is `\varphi` (NOT `\phi`). The field is `\Omega`, the
  discriminant is `\Delta`.
- Σ is always the Sigma LETTER `\Sigma`, never `\sum`.
  - A determinant is written `\Sigma \pm x_{0}^{(1)} \ldots`.
  - Index labels go above and below: `\overset{\iota,\iota'}{\underset{1,n}{\Sigma}}`.
- Products are juxtaposed. Where the print sets a baseline period as the product sign, keep it as a
  literal `.` in math, tight with no spacing: `F(\theta, z).H(\theta, z)`, `e.f = n`. NEVER use
  `\cdot` or `\times`.
- Ellipses in lists follow the print, with no comma before the last term:
  `a_{0}, a_{1}, \ldots a_{n}`. Do NOT regularize to `\ldots, a_{n}`.

- EXCEPTION to "never `\cdot`" (from batch 2): where magnification shows a vertically CENTRED dot,
  set `\cdot` — p. 218 `S(\eta\alpha_{r}\cdot\frac{\alpha'_{s}}{\eta})`, p. 271, and p. 199 `\frac{\mathfrak{b}}{\mathfrak{a}}\cdot\mathfrak{a}`. A dot on the baseline
  is still the literal `.` (`r.s`, p. 198). Decide by the dot's height, not by the mathematics.
- ϱ is `\varrho` (NOT `\rho`). ϰ is `\varkappa` (NOT `\kappa`, NOT the letter x). ∂ is `\partial`.
- Iota as an index is `\iota`: `x_{\iota,\iota'}`, `\lambda_{\iota}`.
- Modules are Fraktur: `\mathfrak{a}, \mathfrak{b}, \mathfrak{c}, \mathfrak{d}` (the gcd),
  `\mathfrak{m}` (the lcm). 𝔡 has a leftward-curling ascender; 𝔟 does not. An indexed module is
  `\mathfrak{a}_{r-1}`. A product of modules is juxtaposed: `\mathfrak{a}\mathfrak{b}`.
- Congruence: `\alpha \equiv \beta \ (\text{mod.}\,\mathfrak{a})` — a control space `\ ` before the
  parenthesis (use `\quad` where the print sets a wide gap in a display), and inside it
  `\text{mod.}`, a thin space `\,`, then the module. NEVER `\pmod`, `\bmod`, `\mod` or
  `\mathrm{mod}`, and never drop the period. A braced congruence system is
  `\left. \begin{aligned}...\end{aligned} \right\} (\text{mod.}\,\mathfrak{a})`.
- ε is `\varepsilon` (NOT `\epsilon`). Π is the letter `\Pi`, juxtaposed with its operand:
  `\Pi(t-a)`, `\Pi\mathfrak{p}^{e-1}` (NOT `\prod`), like Σ.
- The stacked "=" over "<" / ">" is `\leqq` / `\geqq` (NOT `\le`, `\leq`, `\overset`). A ">" with a
  single SLANTED bar beneath it (p. 213) is a different glyph, set `\geqslant`. Decide by shape.
- A congruence to a non-ideal modulus has no extra parentheses: `(\text{mod.}\,z-c)`.
- A half in an exponent is `\frac{1}{2}`: `(-1)^{\frac{1}{2}n(n-1)}`.
- A § reference inside display math is `(\text{§~2})`.
- An `\ednote` for a misprint inside a display goes straight AFTER the closing `\]`, never inside
  the math.
- A degree label printed ABOVE an argument is `\overset`: `G(\overset{e}{z_{1}}, \overset{e_{1}}{z})`.
  NOT a superscript, and never dropped.
- A value "at the point" is a plain subscript 0: `\alpha_{0}`, `\left(\frac{1}{z}\right)_{0}`. A primed
  quantity takes its prime before the 0: `\pi'_{0}`.
- A braced array of basis functions is `\left\{ \begin{matrix}...\end{matrix} \right.`, keeping the
  printed commas, with `\cdots` in each cell of a dot row. NOT `aligned`, NOT `array`.
- A differential takes a thin space before it in a product: `\,dx_{1}`. Inside ratios, `da_{m}` takes
  none.
- The indeterminate form keeps its baseline dot: `0.\infty`.
- A table with ditto marks is `\begin{matrix}...\end{matrix}` inside `\[ \]`. Each ditto is
  `\text{''}`, words are in `\text{...}`, and a dot row has `\cdots` in each cell. NEVER write out the
  words a ditto repeats. A plain unbraced list of basis functions is also a bare `matrix`.
- The stacked ">" over "<" is `\gtrless` (NOT `\lessgtr`, `\neq`, `\overset`).
- Keep the print's two forms of the derivative apart. The parenthesised one is
  `\left(\frac{d\alpha}{d\beta}\right)`, with a value at the point written
  `\left(\frac{…}{…}\right)_{0}`. The bare one is `\frac{d\alpha}{d\beta}`.
- A footnote mark after a display's closing parenthesis is `\right){}^{*)}`.
- The symbolic differential is `d\varpi` (`d\varpi_{1}`, `\frac{d\varpi}{dz}`), NOT `\omega` or
  `\bar\omega`. The differential of the first kind is an italic `dw`: upright `\mathrm{w}` stays
  reserved for the Verzweigungszahl.
- A coefficient times a differential takes a thin space: `c_{1}\,d\varpi_{1}`,
  `\omega\,dz = \omega_{1}\,dz_{1}`.
- A word inside a display is `\quad \text{für} \quad`.
- A Σ with an index only above it is `\overset{\iota}{\Sigma}`.
- A footnote mark inside display math is `1{}^{*)}`.

- FAILURE MODE (settled by human review, pp. 216 and 233): in this scan a subscript 1 that has
  lost the ink of its top flag reads as a bare dotless stroke, i.e. as ι. Where the maths wants 1
  and the stroke has no flag, it is a damaged 1 — not ι. Compare against a clean 1 nearby.
- A comma whose tail has lost ink can show as a dot with a speck above it (p. 232) — a damaged
  comma, not a semicolon.

## Subscripts, primes, equation numbers, displays

- Subscripts are always in braces. Double indices are comma-separated: `y_{1,1}`, `x_{\iota,h}`.
- The prime comes before the subscript: `b'_{e}`, `y'_{h,\iota}`. A primed quantity raised to a
  power is written `b_{e}^{\prime f}`.
- The print's left-side "(1.)" becomes `\tag{1.}`, keeping the period. Numbering restarts in each §.
  Each numbered equation gets its own `\[...\]` display.
- Determinants use `vmatrix`, keeping the printed commas after the entries. A row of dots is
  `\cdots` in each cell.
- In aligned systems a row of dots is `&\cdots\cdots\cdots\cdots`. A left-braced system is
  `\left\{ \begin{aligned}...\end{aligned}\right.`
- Small-type index ranges go after `\qquad`, as
  `{\scriptstyle (h = 0,\, 1,\, \ldots\, e-1;\ \ldots)}`, or on a second line of `gathered`.

## Text

- "const." is roman with its period, then a thin space before the factor:
  `\text{const.}\,N(\mu)`. NOT `\mathrm{const}`, NOT italic const, never drop the period.
- Abbreviations take control spaces, like `d.\ h.`: `w.\ z.\ b.\ w.`, `u.\ s.\ f.`. NOT plain
  spaces, NOT ties.
- "Beweis." and "Definition." are italic lead-ins at the start of a paragraph: `\emph{Beweis.}`.
  NOT bold, NOT a heading.
- Numbered items ("I.", "II.", "1.", …) are plain paragraphs separated by blank lines. NOT
  `enumerate`.
- Ideals are Fraktur: `\mathfrak{p}` (a prime ideal), `\mathfrak{q}`, `\mathfrak{r}`,
  `\mathfrak{c}`. Never roman or italic p, q, r, c for these.
- More ideal letters (from batch 4): the Verzweigungsideal is `\mathfrak{z}`; in 𝔬D = 𝔡𝔷² it is
  `\mathfrak{d}`; `\mathfrak{e}`, `\mathfrak{r}`; and in f'(θ)𝔢 = 𝔨 it is `\mathfrak{k}` (NOT
  `\mathfrak{f}`, which descends; to be confirmed at verification — p. 223 carries the one
  \uncertain). Italic z and r keep their own, separate meanings.
- The point 𝔓 (from p. 236) is the Fraktur capital `\mathfrak{P}`, with powers `\mathfrak{P}^{r}` and
  the prime straight after the letter: `\mathfrak{P}'`. Lowercase `\mathfrak{p}` is a DIFFERENT
  object (the prime ideal). NOT roman or italic P, NOT `\mathfrak{B}`.
- Polygons are Fraktur capitals: `\mathfrak{A}, \mathfrak{B}, \mathfrak{C}, \mathfrak{D}, \mathfrak{M}`.
  Products are juxtaposed (`\mathfrak{M}\mathfrak{A}`), with the prime straight after the letter
  (`\mathfrak{A}'`). NOT roman or italic letters.
- The Nulleck is `\mathfrak{O}`. It is NOT the ideal `\mathfrak{o}`, NOT the digit 0, NOT a roman O.
- The tailed branch point on p. 243 is `\mathfrak{Q}`. Tell it from 𝔒 by the tail.
- The Verzweigungspolygon (a Fraktur 3-shape) is `\mathfrak{Z}_{z}`, with its argument in the
  subscript: `\mathfrak{Z}_{z'}`. NOT the digit 3, and NOT the ideal `\mathfrak{z}`.
- The Windungszahl is an upright roman w: `\mathrm{w}_{z}`. NOT italic w, NOT `\omega`.
- Polygon classes are italic math capitals `A, B, C, D`. The print's heavy italic is the typeface:
  NO `\mathbf` or `\boldsymbol` (to be confirmed at verification).
- A ratio of polygons is `\frac{\mathfrak{A}}{\mathfrak{B}}`, in displays and inline alike.
- The r-Eck is `\mathfrak{R}` (NOT `\mathfrak{N}`), juxtaposed in products: `\mathfrak{P}\mathfrak{R}`.
  The C polygons are `\mathfrak{C}_{1}` and `\mathfrak{C}'_{1}` (NOT `\mathfrak{E}`).
- The Verzweigungszahl is the same upright w: `\mathrm{w}_{z}`, `\mathrm{w}_{\alpha}`, and a bare
  `\mathrm{w}`.
- The Verzweigungspolygone are `\mathfrak{Z}_{\alpha}` and `\mathfrak{Z}_{\beta}`. The ideal stays
  `\mathfrak{z}`.
- The Unterecke is `\mathfrak{U}`: `\mathfrak{U}_{1}^{2}`, `\mathfrak{U}^{k+1}` (NOT `\mathfrak{V}`). A
  Verzweigungspolygon with no subscript is `\mathfrak{Z}`, and `\mathfrak{Z}_{1}` for z₁.
- The Grundpolygon is `\mathfrak{W}` (`\mathfrak{W}_{1}`, `\mathfrak{W}'`). Its class is the italic
  `W`. The Polygon der Doppelpunkte is `\mathfrak{R}`, the same glyph as the r-Eck. On p. 265 only,
  the numerators are `\mathfrak{K}` and `\mathfrak{L}`.
- The class symbol O in `(A, W) = (O, B)` is an italic `O`. It is NOT the Nulleck `\mathfrak{O}`.
- A primed Fraktur letter raised to a power: `\mathfrak{A}'^{2}`.
- The auxiliary polygon of class N (pp. 279, 283) is `\mathfrak{N}`. Its Fraktur N shape has to be
  kept apart from the r-Eck `\mathfrak{R}`, which is to be rechecked at verification. The
  Verzweigungspolygon of σ is `\mathfrak{S}` / `\mathfrak{S}'` (NOT `\mathfrak{G}`).
- Differentials of the 2nd and 3rd kind carry their argument in a parenthesised subscript:
  `dt_{(\mathfrak{P}^{r-1})}`, `d\pi_{(\mathfrak{P}_{1}, \mathfrak{P}_{r})}`.
- A Σ with a PARENTHESISED index above it is `\overset{(\iota)}{\Sigma}`. It is kept distinct from
  `\overset{\iota}{\Sigma}`. Coefficients with both indices put the subscript first:
  `a_{m-2}^{(\iota)}`.
- Case labels at the start of a paragraph: `\emph{a})`.
- Ideal powers put the subscript first, then the braced exponent, with the factors juxtaposed and
  no dot: `\mathfrak{p}_{1}^{e_{1}}\mathfrak{p}_{2}^{e_{2}}\ldots\mathfrak{p}_{r}^{e_{r}}`.

- Italic and letterspacing (Sperrdruck) are both set as `\emph`. The print uses them for stress,
  defined terms, theorem statements, author names, and the letterspaced "Lehrsatz".
  - A suffix on an author's name stays outside the emphasis: `\emph{Riemann}schen`.
- Footnotes:
  - The mark in the text is `${}^{*)}$`.
  - The note goes at the end of the page's main text, led by `\textbf{*)}`.
  - A note with several paragraphs keeps all of them.
- Orthography is kept exactly as printed: Functionen, Theil, giebt, existirt, sämmtlich,
  Coefficienten, Discriminante, Uebertragung, ins Besondere.
  - The print uses `ss`, with no ß anywhere: dass, muss, grösst.
  - German quotation marks are the literal „…“.
  - Ordinals are written `n^{\text{te}}` and `n^{\text{ten}}`.
