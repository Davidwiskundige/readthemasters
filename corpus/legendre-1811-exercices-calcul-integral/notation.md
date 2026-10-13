# Notation decisions — Legendre 1811, *Exercices de calcul intégral* (tome premier)

Work-spanning rendering decisions, so that isolated transcription batches agree. Each entry states
the rule, the rationale, and the forbidden alternatives. Author back-references (`art. 12`,
`équation (3)`, `n°`) are copied verbatim and are not listed here.

## Pagination

- **Scan layout.** The University of California scan (archive.org `exercicescalculi01legerich`) has
  one printed page per leaf image, named `..._NNNN.jpg`. Leaf 5 = title page (unnumbered,
  `\origpage{i}`); leaf 7 = printed page 1. Through the body the printed page number is leaf − 6;
  batches report any drift (blank leaves, plates).
- The work is one book in three continuously paginated parts (Première partie, Seconde partie,
  Troisième partie), then the Table des matières, the Errata and the folded plates. The 1816
  *Supplément* that follows in the scan is a separate work and is not transcribed here.
- **Roman / unnumbered front matter** uses `\origpage{i}` etc. Library ownership stamps, the
  bookplate, the shelf-mark and the pencil marginalia and underlining added by readers are never
  transcribed.

## Typography

- **Title page.** One `\section*` holds the whole title (EXERCICES DE CALCUL INTÉGRAL SUR DIVERS
  ORDRES DE TRANSCENDANTES ET SUR LES QUADRATURES;); author block, PARIS, publisher and year follow
  as plain paragraphs, with `M\textsuperscript{me} V\textsuperscript{e}`. The handwritten "Tome
  Premier" is reader marginalia: not transcribed.
- **Headings.** Part and chapter titles (EXERCICES DE CALCUL INTÉGRAL., PREMIÈRE PARTIE., DES
  FONCTIONS ELLIPTIQUES.) and the printed italic subheadings are `\section*`, with inline math kept
  (e.g. `$\displaystyle\int\frac{P\,dx}{R}$`). *Forbidden:* `\subsubsection*`.
- **Article numbers** keep the printed form `(N).`: write `\subsection*{(1).}` and begin the text as
  a new paragraph. *Forbidden:* `\subsection*{1.}`.
- **Greek letters.** The print's curly ϐ is `\beta`; epsilon is `\varepsilon`; the curly phi is
  `\varphi`; the coefficient letters beside ζ and θ are eta, `\eta` (not `n`). The lowercase
  amplitude letter on p. 10 is `\psi`. *Forbidden:* `\epsilon`, `\phi`, `\Psi`, `\mathfrak`, a
  literal `6` or `n` for any of these.
- **Capitals** (P, R, Π, Γ, A, B…) are plain math letters. *Forbidden:* `\mathrm`.
- **Radicals.** The print's √( ) with no overbar is `\sqrt{(...)}`; with brackets `\sqrt{[...]}`.
- **Trigonometry and dots.** `tang` is `\operatorname{tang}`. A dot printed after the function name
  is kept where printed (`\sin.^{2}\varphi` as in the p. 15 heading, `\sin^{2}.\varphi` on p. 16).
  Products like "a−c.a−d.b−c.b−d" keep their printed dots.
- **Ellipses and fractions.** Printed "...." is `\ldots`, never four literal dots. Small fractions
  inside displays are `\tfrac`. A product dot in a display is `\cdot`.
- **Spacing before punctuation** is dropped: the print's space before `,` `;` `:` is compositor
  spacing. *Forbidden:* " ," or " ;" in the output.
- **Footnotes.** The call is `${}^{(n)}$` in the text and the note is `\textbf{(n)} …` at the end of
  the page's fragment.
- **Catchwords and signatures** (the repeated first word at the foot of a page, a signature "2")
  are not transcribed.
- **Spelling** is kept as printed: essaia, constans, coefficiens, développemens, différens, ensorte,
  jusques-là. *Forbidden:* modernizing to -ents.
- **Hyperbola-arc letter Υ** is `\Upsilon` (a capital Greek upsilon in the print). *Forbidden:* `Y`,
  `\Psi`, `\mathrm{Y}`.
- **Psi.** Both the Ψ-shaped glyph on p. 11 and the ↓-shaped psi from p. 20 on are the lowercase
  amplitude variable `\psi`. *Forbidden:* `\Psi`.
- **Superscript old-style "o"** (Z°, Π°) is the digit zero: `Z^{0}`, `\Pi^{0}`; `H¹` is `H^{1}`.
  *Forbidden:* `Z^{o}`, `Z^{\circ}`.
- **Equation labels** (a'), (b') stay inline as printed, `\ldots(a')`, and are not turned into
  `\tag`; for a braced system use `\left.\begin{aligned}…\end{aligned}\right\}\ldots(b')`.
- **Product dots** between factors are `\cdot` in inline math as well as in displays.
- **Margin figure references** ("Fig. N.") become `\rmfigure{figures/fig-N.png}{Fig.~N.}{…}`, placed
  before the paragraph they stand beside, at the first occurrence only (repeat margin references
  are not re-emitted). The plates are at the back of the volume (leaf 395); crops are made from there.
- **F¹ and the other "complete" functions** follow `H^{1}`: write `F^{1}`. *Forbidden:* `F'`, `F_{1}`.
- **Fractional indices** are `\varphi_{\frac{1}{2}}`, `\varphi_{\frac{1}{4}}`. *Forbidden:*
  `\varphi_{1/2}`.
- **Baseline-size indices.** The author's Δi and φi, printed at baseline size (not subscripts), stay
  `\Delta i` and `\varphi i`. *Forbidden:* converting them to subscripts.
- **Ordinal abbreviation** "nme degré" is `n^{\text{me}}`. **√−1** is `\sqrt{-1}`; cube roots are
  `\sqrt[3]{...}`.
- **Words split across a page break** (con-/naître, algé-/brique) are written whole at the end of
  the earlier page; the next fragment then begins at the next whole word, with no leftover syllable.
- **Stray rules** inside parentheses (a printing defect, R29) are not transcribed.
- **Angle tables** are an `aligned` display in column pairs, with degrees/minutes/seconds exactly as
  printed: `^{\circ}`, `'`, `''`. A seconds figure with no printed dot ("30''91", "0''00") stays
  without one; one with a dot ("25''.92", "5.64") keeps it. *Forbidden:* normalizing the dots,
  `\text` around the numbers.
- **Corollary numerals** ("I.", "II.", … "V.") are inline paragraph starts. *Forbidden:*
  `\subsection*`. **"EXEMPLE."** (letterspaced capitals) is `\section*{EXEMPLE.}`.
- **Figure alt texts** were written from the prose before the plates were seen; they are to be
  checked against the plate crops when the figures are cut.
- **Problem headings.** Write `\subsection*{(34).}`, then a new paragraph beginning
  "Problème I. \emph{…}" with "Problème" as plain text. *Forbidden:* `\textsc`, putting "Problème"
  inside the subsection heading.
- **Italic subheadings** such as "Développement particulier de la formule Z=∫…" are `\section*` with
  inline `\displaystyle` math.
- **Compositor spacing defects** (e.g. "précis émentegal") are normalized to the word intended
  ("précisément égal"); this is not a content change.
- **Roman-numeral superscripts** (m^iv, A^v) are `m^{\text{iv}}`, `A^{\text{v}}`, following
  `n^{\text{me}}`. *Forbidden:* `\mathrm{iv}`, `m^{iv}`.
- **arc tang** is `\operatorname{arc}\operatorname{tang}`. *Forbidden:* `\arctan`.
- **Equation labels** (d'), (e'), (f') follow the (a')/(b') rule; where the formula has no brace the
  label goes after `\end{aligned}`.
- **Uncertain readings inside math** cannot carry `\uncertain`; they are recorded in an `\ednote`
  after the display instead (and counted as flags in provenance).
- **Curly δ-shaped letter** (p. 82, art. 58, "le plus petit arc") is `\delta`. *Forbidden:*
  `\partial`, `\vartheta`, `\mathfrak`. The "ϑ" variant of θ (p. 72) is `\theta`, not `\vartheta`.
- **Inconsistencies are reproduced** (R23): Δψ printed without parentheses on p. 75 stays `\Delta\psi`
  though neighbouring lines have Δ(ψ).
- **Left-set formula lines** are written as `aligned` displays.
- **Superscript circles** (c°, c°⁵, c°⁷) are written as zeros: `c^{0}`, `c^{05}`, `c^{07}`.
  *Forbidden:* `^{\circ}`, `^{o}`, `c^{0 7}`. Superscript i and n (b^i, c^n) are `b^{i}`, `c^{n}`;
  a printed superscript 1 on G, F, E (the complete function) is `G^{1}`, not `G'`.
- **Two-column formula tables** are one `aligned` display, columns separated by `&\qquad&` (`&&` on
  later rows), with an `&\text{etc.} && \text{etc.}` closing row; a vertical rule between the columns
  is not transcribed. *Forbidden:* two separate displays, an `array` with a rule.
- **Decimal comma** in a printed number (9,9650547) is `9{,}9650547`.
- **Ordinals "1°.", "2°."** in prose are the literal text `1°.` / `2°.`; inside math `1^{\circ}`.
- **Ten-place logarithms printed with a gap** ("9.99992 99167") keep the gap as a control space,
  `9.99992\ 99167`; ones printed without a gap stay unspaced. *Forbidden:* removing the gap, `\,`, `~`.
- **Ruled numerical tables** (Log. F¹ / Log. E¹ table, p. 118) are one `aligned` display: cells
  separated by `&&`, `&\qquad&` only between the two halves in the header row; rules not transcribed.
  *Forbidden:* `array`/`tabular` with rules. Log-computation columns are `&label\ldots\ldots && value`.
- **Circles on transformed quantities** follow the zero rule: `H^{0}`, `\varphi^{00}`, `\theta^{000}`,
  `\Delta^{0}`; a circle followed by a square is `c^{02}`, `c^{002}`.
- **μ as an index** is a superscript: `c^{\mu}`, `H^{\mu}`, `\lambda^{\mu-1}`; "μ^{ième}" is
  `\mu^{\text{ième}}`. *Forbidden:* a subscript μ. Primed indices are `b'^{2}`, `c'^{2}`; *forbidden:*
  `b^{\prime 2}`.
- **cot** is `\cot` (not `\operatorname{cot}`), unlike `\operatorname{tang}`.
- **A duplicated article number** printed in error (art. (85) twice) is kept as printed, with an
  `\ednote` opening the paragraph (a macro cannot go in a heading).
- **Small-capital case headings** ("PREMIER CAS n = cot²θ.") are `\section*{Premier cas $n=\cot^{2}\theta$.}`,
  `\section*{Second cas, $n=-1+b^{2}\sin^{2}\theta$.}`. *Forbidden:* `\textsc`, `\subsection*`, all caps.
- **Braced systems** labelled (i'), (k'), (l'), (m') with no printed dots: the brace goes on the side
  where printed (`\left\{…\right.`, `\left.…\right\}`, or both), the label follows as `\;(k')` or
  `\qquad(i')`. *Forbidden:* `\ldots` before the label where none is printed, `\tag`.
- **True subscripts** (φ₂, φ₃, φ_ν, p. 139) are `\varphi_{2}`, unlike the baseline-size φi rule.
  Vertical dots are `\vdots`. An "=" repeated at a line break is written once.
- **Case headings** "TROISIÈME CAS, n=−c²sin²θ." follow the Premier/Second cas rule:
  `\section*{Troisième cas, $n=-c^{2}\sin^{2}\theta$.}`.
- **Greek variants.** ν is `\nu`, λ `\lambda`, μ `\mu`, ε `\varepsilon`; the ϑ in sin²ϑ and the
  Φ-shaped φ are `\theta` and `\varphi` (variant sorts of the same letters, as for p. 72).
- **Equation labels** (n'), (p'), (q'), (r') follow the (a') rule; a label printed at the end of the
  first display line stays there. Specks and stray marks that are not product dots are left out.
- **"n°s 53 et 57"** is `n\textsuperscript{os} 53 et 57`, following `M\textsuperscript{me}`. *Forbidden:*
  `n^{os}` in math, plain "nos".
- **"sinθ²"** (p. 157) is kept as printed, `\sin\theta^{2}`. *Forbidden:* normalizing it to `\sin^{2}\theta`.
- **Broken glyphs** (R29) are written as the letter intended (`\varphi`, `C^{0}`, `2b\nu`), without a
  note, unless the intended letter is itself in doubt.
- **ν** in "my=1+ν²" is Greek nu: `\nu`. *Forbidden:* `v`.
- **"nieme / nième"** is reproduced as printed in each place (`n^{\text{ieme}}` p. 170,
  `n^{\text{ième}}` p. 171, R23). *Forbidden:* making them agree.
- **Numeric product dots** are `\cdot` (`2\cdot3C`, `\frac{1\cdot3}{2\cdot4}`). *Forbidden:* a bare `.`
  (reads as a decimal point).
- **Double integral** ∫∫ is `\iint`, in displays only. *Forbidden:* `\int\int`, `\int\!\!\int`.
- **Cursive β-like glyph** (pp. 185–188, coordinate β beside α) is `\beta`.
- **Figure placement** when a margin "Fig. N." stands beside a line that continues a paragraph begun
  on the previous page: place the `\rmfigure` after the end of that paragraph.
- **In-text figure citations** ("La figure 14") emit `\rmfigure{figures/fig-14.png}{Fig.~14.}{…}`
  right after the paragraph citing it. *Forbidden:* a descriptive caption.
- **Leader dots** before a formula that runs onto the next line are `\ldots\ `, never literal dots.
- **Small-type explanatory notes** beside a figure are ordinary paragraphs, one per printed line.
  *Forbidden:* a footnote or `\textbf` label.
- **The (p/q) transcendents** are `\left(\frac{1}{1}\right)`, `\left(\frac{p}{q}\right)`, inline and in
  displays (the printed parenthesised fraction symbol). *Forbidden:* `\binom`, `(1/1)`.
- **Case headings** "PREMIER … CINQUIÈME CAS, n = 3 …" are `\section*{Premier cas, $n=3$.}`.
  A roman numeral printed in small capitals inside prose ("cas VII") is plain "VII"; *forbidden:*
  `\textsc`.
- **Part break.** "FIN DE LA PREMIÈRE PARTIE." is a plain paragraph line; the Seconde partie opens
  with `\section*{SECONDE PARTIE.}` and `\section*{DES INTÉGRALES EULÉRIENNES.}` on printed p. 221
  (leaf 227). Article numbering restarts at (1) in each part; the continuous `\origpage` numbering
  does not.
- **Old-style digit 1 as subscript** (M_ı) is `M_{1}` (cf. `F^{1}`). *Forbidden:* `M_{i}`, `M_{\imath}`.
- **Overlined index** "p+\overline{i+1}.n" is `p+\overline{i+1}\cdot n`. *Forbidden:* dropping the
  vinculum, a bare `.`.
- **Primes and circles on M:** `M^{0}`, `M'`, `M''`, `M'''`, `M^{(i)}`. *Forbidden:* `M^{\circ}`.
- **Euler's bracket symbol** is `\left[\frac{p}{q}\right]`; Γ(a) is `\Gamma(a)`; roots
  `\sqrt[n]{(1-x^{n})^{n-q}}`.
- **Equation labels (a), (b)., (c)., (d), (e).** go inside the display as `\qquad(a)`; with printed
  leader dots `\ldots\ldots(e).`; no `\tag`. Show-through from the back of the leaf is never transcribed.
- **Drop-cap openings** ("QUOIQUE") are set in ordinary case ("Quoique").
- **"cotang"** (the word printed in full) is `\operatorname{cotang}`, by analogy with `tang`;
  "cot" printed short stays `\cot`. *Forbidden:* `\cot` for the printed "cotang".
- **Labels with no leader dots** ((u), (v), (x), (y), (z), (a'), (d')…) go inside the display as
  `\qquad(x)`; braced systems `\left.\begin{aligned}…\end{aligned}\right\}\qquad(u)`. *Forbidden:*
  `\tag`, `\ldots` where no dots are printed.
- **Old-style subscript digit 2** (A₂, M₂) that looks like "a" is read from context as `A_{2}`.
- **Latin quotations and journal names** (Nova acta Petropol.) are `\emph` runs.
- **Ψ(x) / ψ(x)** of the Seconde partie (a Ψ-shaped glyph on pp. 243–244, a ↓-shaped psi after) is
  `\psi` throughout, as for the amplitude variable. *Forbidden:* `\Psi`.
- **Curly β** (p=αn, q=βn, β=−½+½√5) is `\beta`; **Λ(x)** is `\Lambda`. *Forbidden:* `6`, `\mathfrak`,
  `\wedge`, `A`.
- **Product chains** "n−q.2n−q" are `n-q\cdot 2n-q`. "l2" (for log 2) is kept as printed.
- **Primed and double-primed labels** ((n')…(z'), (a'')…(k'')) go inside the display as `\qquad(x')`;
  a period or comma after the label is kept only where printed. Right-braced systems are
  `\left.\begin{aligned}…\end{aligned}\right\}\qquad(d'')`; a connecting prose line inside the brace
  ("et si n est pair, on aura") is a `\text{…}` row of the aligned block.
- **(a,n)^m** is `(a,n)^{m}`. A tiny superscript after log that looks like "s" is read as the
  exponent `\log^{2}` by parallel with the neighbouring formulae.
- **Inline integrals in exponents** (ue^{∫u dp}) must avoid R2 hits: write them so that houselint
  passes (display `\int` is not allowed inline in an exponent; use `\textstyle` or restructure).
- **Small-capital roman superscript** (P^VI) is `P^{\text{vi}}`. *Forbidden:* `P^{VI}`, `P^{vi}`.
  P°, P', P'', P''', P^{(m)} follow the zero rule (`P^{0}`).
- **Plain decimals** are kept with a plain point: `S_{3}=1.2020567`, `1.202056903159594281` (no
  printed gap, so no control space). *Forbidden:* `{,}`, `\cdot`.
- **"L(1+z)=L2"** keeps the printed capital L next to "log 2" (R23).
- **A brace followed by punctuation and a label** is `\right\};\qquad(x'')`.
- **Greek equation labels** (α), (β), (γ), … (ν), (λ'), (μ') go inside the display as
  `\qquad(\alpha)`, same rule as (a)/(x). The curly ϰ that looks like "x" in the sequence θ, ι, κ, λ
  is `\kappa`. *Forbidden:* `\tag`, an `x` label, `\varkappa`.
- **Vinculum-grouped factors** in the Φ(α,m) products: `\ldots\overline{\lambda m-1}`,
  `\alpha+\overline{\lambda m-1}\cdot\beta`; no bar is written where none is visible.
- **Variant ω** (curly numerator of ω/sin pω) is `\omega`. Inline and display exponents that differ
  as printed (x^{λnm−1} vs x^{λmn−1}) are both kept (R23).
- **Exponent separators** in 2^{−0.30} and the like are written with a plain point.
- **Prose ordinals** ("15ème", "10ème") are `15\textsuperscript{ème}`, following `M\textsuperscript{me}`;
  in math "le nème terme" is `n^{\text{ème}}`. *Forbidden:* `15^{ème}` in math.
- **Series denominators** "1.2k", "3.4k³", "2n.2n−1.k^{2n−1}" use `\cdot`; but "2.4Γ(1.100)" is the
  decimal 2.4 and keeps a plain point (10/24 = 1/2.4). *Forbidden:* `2\cdot4` there.
- **Greek labels** (ρ), (σ), (υ), (φ), (ψ), (ω) go inside the display as `\qquad(\rho)`; a label with
  printed leader dots is `\text{etc.}\ldots(\tau)`. Upsilon is `\upsilon`.
- **Flush-left lines after displays** continue the same paragraph; only indented lines start one.
- **Log Γ table** (leaves 308–312, a = 1.000 … 2.000). Its title "TABLE DES LOGARITHMES DE LA
  FONCTION Γ(a)." is set once as `\section*{… $\Gamma(a)$.}`; "SUITE DE LA TABLE." is a running head
  and is not transcribed. The 8-column pages follow the p. 118 rule (`&\qquad&` between column pairs
  in the header row only, `&&` elsewhere); header cells are `a`, `a.`, `\text{Log }\Gamma`,
  `\text{Log }\Gamma.` with or without the period exactly as printed in each column (R23); a
  boundary row repeated at the foot of one column and the head of the next is kept. *Forbidden:*
  `array`/`tabular`, transcribing rules, `\log\Gamma` in headers. All 1,020 cells were checked
  numerically against log₁₀Γ(a)+10: three misprints are `\ednote`d; the remaining deviations (≤ 1.9 in
  the 7th decimal) are Legendre's own rounding and are kept as printed.
- **Numeric equation numbers** (the Troisième partie's (1), (2), … printed on an equation) are
  `\tag{N}` (R5); letter and Greek labels stay `\qquad(x)`.
- **Misprinted page numbers.** Leaf 322 prints its page number "163" (digits transposed); `\origpage`
  follows the sequence (316) with a `%` comment. *Forbidden:* `\origpage{163}`.
- **Equation (3)** printed with leader dots is `…, \tag{3}`; all numeric labels (1), (2), (3) are `\tag`.
- **Ψ(m) in the Troisième partie (arts. 12–13)** is `\Psi(m)`: it is printed as a clear upright
  capital, paired with the capital Φ(m), and is a different function from the Seconde partie's
  ψ(x) / the amplitude ψ. The `\psi` rules above apply to those, not here. *Forbidden:* `\psi(m)`.
- **Numerical tables of the quadrature examples** (pp. 332–333) follow the ruled-table rule: one
  `aligned` display, `&&` between columns, header row θ. / s. / Δs. / …, `\text{Sommes}\ldots` in its
  cell, rules not transcribed; totals and running sums were checked numerically.
- **"L(…)" and "log"** each keep the form printed at that place (R23).
- **ψ(p), ψ'(b), ψ(a,x)** (arts. 22, 27–28) are `\psi`; the curly β-like "Є" angle (tang Є = b) is
  `\beta`. Equation numbers restarting inside the Γ(a,x) section and art. 29 are each `\tag{N}` as
  printed (duplicate tags across the book are expected; each display stands alone).
- **"Exemple I."** (letterspaced small capitals) is `\section*{EXEMPLE I.}`. Angles are written
  without spaces: `46^{\circ}55'23''4`, undotted seconds kept. Product chains "a.a+1.a+2" are
  `a\cdot a+1\cdot a+2`.
- **Z¹** (pp. 349–350) is `Z^{1}`; **Γ'(α)** is `\Gamma'`; **"l 1/z"** is `l\frac{1}{z}`; the ↓-shaped
  ψ(m) of art. 35 is `\psi` (the `\Psi(m)` rule covers arts. 12–13 only).
- **Equation (2) printed with leader dots** is `\ldots\ldots \tag{2}`; a trailing printed period after
  the label is dropped.
- **A blot or hole covering words** is `\uncertain{…}` when the sense is clear but the print is not.
- **Both the large ∫ and the small long-s-shaped ∫** are `\int`. *Forbidden:* `\smallint`, a literal ſ.
- **A sentence period, comma or semicolon printed after an equation label** ("(1).", "(2) ;") goes at
  the end of the formula, not into `\tag`. *Forbidden:* `\tag{1.}`.
- **A square bracket across a two-line aligned display** is `\Big[ … \Big]` (`\left`/`\right` cannot
  span aligned rows).
- **"n° 46", "n° 76"** are literal text; "II^e partie" is `II\textsuperscript{e}`.
- **Table des matières** (leaves 383–392, printed pp. 377 ff.): title `\section*{TABLE DES MATIÈRES.}`,
  then `\section*{PREMIÈRE PARTIE.}` / `\section*{DES FONCTIONS ELLIPTIQUES.}` and likewise for the
  other two parts. Each § entry is one paragraph, "§ N. \emph{description with inline math}, <page>"
  with the page reference exactly as printed ("pag.~4", "page 14", or a bare number); each printed
  summary under an entry is its own paragraph. "§. XX." keeps its printed period. *Forbidden:* the §
  number inside `\emph`, a list environment, `\dotfill`, normalizing "page"/"pag.".
- **Unnumbered page** (leaf 383 prints only the signature "48") takes the number the sequence requires
  (377) with a `%` comment saying so.
- **Errata** (leaf 393, printed unnumbered, `\origpage{387}` by sequence): `\section*{ERRATA.}` and
  one `aligned` display (empty leading `&`, `&&` between columns; words in `\text{}`, italic cells
  `\textit{}`, leader dots `\ldots\ldots`, rules not transcribed). The printed "findelapag." is
  "fin de la pag." (compositor spacing).
