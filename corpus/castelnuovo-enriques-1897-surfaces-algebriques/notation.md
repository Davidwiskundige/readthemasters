# Notation decisions — Castelnuovo & Enriques 1897

Cross-page rendering decisions for this work (HOUSESTYLE R27). Batches cannot see each other; this
file is how they agree. Each entry states the decision, one line of why, and **what not to write
instead**.

## Author names as printed

- **Max Noether's name is printed `Nöther` throughout** (title page: "un Mémoire fondamental de
  M. Nöther"). Transcribe `Nöther`, with the umlaut, every time. **Do not** write `Noether`,
  `Nother`, or `Noether` "corrected" — R12 keeps the edition's own orthography, and this spelling
  is the edition's, not a scan artifact.
- Author names set in small capitals in the running text (`Castelnuovo`, `Enriques`, `Picard`)
  are ordinary name mentions; set them as plain text. Small caps is the print's face for a name,
  not emphasis. **Do not** write `\textsc{}`. Where a name is *letterspaced* (Sperrung) rather
  than small-capped, R20 applies and it is `\emph`'d.

## Language and typography

- The memoir is in **French**; the surrounding journal is German. Keep French orthography exactly
  as printed, including `é è à ê ô` and the apostrophe in `l'origine`, `d'une`.
- French quotation marks are guillemets `«…»` as literal Unicode (R22). **Do not** write
  `\og`/`\fg` or ASCII `"`.

- **Author names in the running text are letterspaced (Sperrung), so they are `\emph`'d** (R20):
  `\emph{Nöther}`, `\emph{Picard}`, `\emph{Riemann}`, `\emph{Cremona}`, `\emph{Segre}`,
  `\emph{Castelnuovo}`, `\emph{Enriques}`, `\emph{Bertini}`, `\emph{Poincaré}`, `\emph{Humbert}`,
  `\emph{Clebsch}`. The honorific and any connecting words stay **outside** the `\emph`
  (`M.\ \emph{Nöther}`, `MM.\ \emph{Brill} et \emph{Nöther}`), and each name in a list gets its
  own `\emph` with the commas outside. **Do not** set a letterspaced name plain, and **do not**
  run one `\emph` across `M.` or across a whole comma-list. Small caps occur only in the byline
  and the running heads, so `\textsc{}` is never used in the body.
- **An italicized work title next to a letterspaced author name stays a separate `\emph` run** —
  `\emph{Enriques}, \emph{Ricerche di geometria…}` — because the print uses two distinct devices
  there. **Do not** merge them into one `\emph`.

## Footnotes

- The print marks footnotes with a per-page series `*)`, `**)`, `***)`, and then a dagger `†)`
  (p241 uses all four). Per R15, keep the in-text reference as a math superscript —
  `${}^{*)}$`, `${}^{**)}$`, `${}^{\dagger)}$` (the closing paren sits inside the superscript, no
  space before it) — and place each note as a complete unit at the end of that page's main text,
  led by `\textbf{*)}` / `\textbf{†)}`, the dagger there being **literal Unicode** since that lead
  is text mode. **Do not** use `\footnote{}`, **do not** renumber the asterisks, and **do not**
  write a Unicode `†` inside math or `\dagger` outside it.
- **The fifth mark in the series is a DOUBLE dagger, set as two separate dagger sorts `††`**
  (p308 runs `*) **) ***) †) ††)`): in text `${}^{\dagger\dagger)}$`, two `\dagger` commands with
  no space between them; at the foot `\textbf{††)}` with two literal Unicode daggers. **Do not**
  write `\ddagger` or a Unicode `‡` — the print sets two daggers side by side, not a
  double-dagger sort.
- **Two consecutive footnote markers on one word are two adjacent math groups, no space between**:
  `courbes${}^{*)}$${}^{**)}$.` **Do not** insert a space or a comma between them, and do not
  combine them into a single superscript.
- **A footnote marker attaching to a letterspaced name goes outside the `\emph`**:
  `\emph{Clebsch}${}^{*)}$`. **Do not** put the marker inside the `\emph` braces.
- **A footnote reference attaching to a math symbol goes OUTSIDE that symbol's math span**, as its
  own adjacent math group: `$|C|$${}^{*)}$`, `$g_{n}^{r}$${}^{**)}$`. Close the math (and any
  `\emph`) first. **Do not** fold the marker into the symbol's own math as `$g_{n}^{r**)}$`.
- **Author names inside footnotes are letterspaced and `\emph`'d exactly as in the running text**,
  each name its own run with `et`, commas and semicolons outside:
  `\emph{Brill} et \emph{Nöther}, l.\ c.\ pag.\ 308`. **Do not** set footnote names plain, and
  **do not** wrap a whole citation in one `\emph`.
- **A footnote reference falling inside a parenthetical keeps BOTH closing parens** — `${}^{**)}$)`
  — one belonging to the marker and one to the parenthetical (p248, "Brill et Nöther"). **Do not**
  collapse the doubled `)` as a misprint.
- **A footnote whose body is a bibliography list keeps the print's paragraphing**: the
  `\textbf{*)}` lead paragraph, then each further cited item as its own blank-line-separated
  paragraph (p243's `*)` is the model). **Do not** run the list into a single paragraph, and
  **do not** repeat the `*)` on each item.

## The close of the memoir

- **The dateline on p316 is ordinary running text at the end of that page's main text, before its
  footnotes**: `\emph{Florence}, 13.\ février 1896.` The place name is letterspaced, so R20 makes
  it `\emph`; the day number's period takes a control space so it does not get inter-sentence
  spacing. **Do not** wrap it in a heading, a `flushright`, or an `\ednote`, and do not set
  `Florence` plain. There is no signature and no "Fin"; the rule below the last footnote is page
  furniture and is not transcribed.

## Citations and abbreviations

- **Superscript ordinals in citations are math superscripts with `\text`**, set immediately after
  the digit or letter with no space: `4${}^{\text{e}}$ s${}^{\text{e}}$`, `2${}^{\text{a}}$`.
  **Do not** write `\textsuperscript{e}`, `$^e$`, or flatten to `4e se`.
- **An abbreviation dot inside a name or citation takes a LaTeX control space** (R17): `M.\ `,
  `MM.\ `, `Ac.\ d.\ Sc.`, `Math.\ Annalen`, `Bd.\ VII`, `t.\ X`, `Journ.\ d.\ Math.`,
  `Mem.\ dell'Acc.\ d.\ Scienze`. A dot followed by a comma (`ibid.,`) and a sentence-final dot
  take **no** `\ `. **Do not** leave a bare space after an abbreviation dot.
- **The print's spaced ellipsis is normalized to three tight ASCII periods `...`, placed outside
  any `\emph` it follows**: `\emph{Ueber die algebraischen Functionen}..., Math.\ Annalen`.
  **Do not** write `\dots` or `\ldots`, do not keep the spacing between the dots, and do not pull
  the ellipsis inside the `\emph` braces.
- **Em-dashed number ranges use `---`**: `1863---1865`, `1893---95`. **Do not** write `--` or a
  Unicode dash.

## Headings

> Six batches split on this and produced three different shapes. **The rule below is the settled
> one**; earlier fragments were normalized to it.

- **A numbered article is ONE heading with the number inside it**:
  `\subsection*{2. Eléments exceptionnels d'une transformation.}` — number, period, single space,
  title. The print sets the bare number centred on its own line above the title, but heading
  layout is presentation, and a standalone `\subsection*{2.}` renders on the site as a meaningless
  lone numeral. The number is also load-bearing: the text back-references articles as
  `n${}^{\text{o}}$ 9`. **Do not** emit the number as its own heading, **do not** leave it as a
  bare paragraph of running text, and **do not** drop it.
- **A chapter opening is likewise ONE `\section*`**, merging the print's two lines:
  `\section*{Chapitre III. Courbes adjointes à une courbe plane. --- Surfaces sous-adjointes à une
  surface de l'espace ordinaire.}`, with the print's own em-dash as `---`. **Do not** split it
  into `\section*{Chapitre III.}` plus a second heading, and **do not** demote the chapter to
  `\subsection*`.
- **`\section*` is reserved for the memoir title and the chapter openers; `\subsection*` is for
  the numbered articles.** Keeping the two levels distinct is what makes the site's table of
  contents work. **Do not** use `\section*` for a numbered article. The one other `\subsection*`
  is the **byline** under the title on p241, following the corpus precedent set by
  `noether-1869-algebraische-functionen-mehrerer-variablen` (`\subsection*{Von Max Nöther.}`).
  Its abbreviation dots take R17 control spaces like every other in the work:
  `\subsection*{Par MM.\ G.\ Castelnuovo à Rome et F.\ Enriques à Bologne.}`.
- Only Chapitre III joins its two printed title halves with `---`; Chapitres I, II and VI set a
  plain `. ` between theirs. That is the print's own punctuation and is reproduced per chapter —
  **do not** regularize it either way.
- A name inside a heading is left **plain**, never `\emph`'d, even where the print letterspaces
  it (R25 forbids a text-mode brace group in a heading; R20 gives the prominence to the heading's
  own face).
- A name that falls inside a heading is left **plain**, never `\emph`'d, even where the print
  letterspaces it: R25 forbids a text-mode brace group inside a heading, and R20 rules that the
  heading's own face carries its prominence.

## Mathematical symbols

- **The image variety is `F'`, with a SINGLE prime, throughout the work** — likewise `P'`, `C'`.
  At half-page resolution the italic `F`'s top-right serif reads as a second prime; magnification
  of the raw scan settled that it is a serif, not type (R29). **Do not** write `F''`.
  **This rule is about a spurious prime only.** Where the text genuinely means the adjoint of an
  adjoint, the double prime is real and is kept: `$|C''|$` in "l'adjoint $|C''|$ de $|C'|$"
  (p276). **Do not** flatten a second-order adjoint to `$|C'|$`.
- **The stacked "greater-or-equal over less-or-equal" is `\gtreqqless`** (p273,
  `$(i \gtreqqless 0)$`) — magnification shows `>` over TWO bars over `<`, the double-bar sort
  matching this print's `\geqq`/`\leqq`. One math span, parentheses inside. **Do not** write
  `\gtreqless` (single bar), `\gtrless`, `\lesseqgtr`, or stack `\geqq`/`\leqq` by hand.
- **The proportionality factors are `\varrho` and `\sigma`, and the forms are `f_{i}` and
  `\varphi_{k}`** — the print sets the curly rho and the looped phi. **Do not** write `\rho` or
  `\phi`.
- **The print's "greater/less or equal" is the double-bar sort: `\geqq` and `\leqq`**, verified by
  magnification on pp. 248, 253, 264. Inside a parenthesized qualifier the whole thing is one math
  span with the parentheses inside it, set tight against the preceding variable:
  `$d(\geqq 0)$`, `$(r \geqq 0)$`, `$(r < s \leqq n)$`. **Do not** write `\geq`, `\leq`, `\ge`,
  `\le` or `\geqslant`, and do not put the parentheses in text mode. A plain single-stroke `<` or
  `>` is a genuinely different sort and stays as it is.
- **The "equals with a vertical stroke through it" is `\neq`** (p249, `$p_{g} \neq p_{n}$`),
  confirmed by magnification. **Do not** build it by hand from `=` and a rule, and **do not** read
  it as `\gtrless` or as a damaged `=`.
- **A linear system in bars is plain math with ASCII pipes**: `$|C|$`, `$|C'|$`, `$|C_{1}|$`,
  `$|C+D|$`, `$|(C+D)'|$`. The bars are the authors' own notation for the system, not a norm.
  **Do not** write `\lvert…\rvert`, `\left|…\right|` or `\|`, do not insert `\,` inside the bars,
  and do not split `$|C+D|$` into `$|C|+|D|$`.
- **The surface families printed as capital phi and psi are `$\Phi$` and `$\Psi$`** (upright
  capitals). **Do not** write `\varPhi`, `\varphi` or `\psi` for these, and do not set them as
  text-mode Unicode.
- **Series symbols carry the subscript first, then the superscript, both braced**: `$g_{n}^{r}$`,
  `$g_{2\pi-2}^{\pi-1}$`, `$g_{n-\nu}^{\varrho}$`, `$g_{2}^{1}$`. Where the print staggers the two
  indices rather than stacking them, it is still written stacked — index *placement* is
  presentation. **Do not** write `g^{r}_{n}`, `g_n^r` unbraced, or `g_2{}^1` to mimic a stagger.
- **The genus of the double curve is `\pi`**, the authors' own letter. **Do not** substitute `p`
  or `\varpi`.
- **`∞` with a raised numeral is `$\infty^{3}$`**, exponent braced. A parenthesis around it goes
  **inside** the math span — `le système adjoint $(\infty^{2})$` — by the all-mathematical
  parenthetical rule below. **Do not** write `\infty^3` unbraced, and do not leave the parentheses
  in text mode. *(An earlier entry here said the opposite; the file was normalized to the rule
  below, which the work already followed 5 times to 1 for the very same expression.)*
- **`n°` is `n${}^{\text{o}}$` followed by an ordinary space and the numeral**: `n${}^{\text{o}}$ 9`.
  **Do not** write `n°`, `nº`, `$n^o$`, `\textsuperscript{o}` or `no.` Where the print instead sets
  a plain `n.`, keep `n.\ 15, 16.` as printed — that inconsistency is the print's.
- **The section sign is literal Unicode `§` with a non-breaking space**: `§~14`. **Do not** write
  `\S`, and do not use a plain space.
- **The numerical plurigenera carry the subscript first: `$p_{n}^{(1)}$`, `$p_{n}^{(2)}$`**,
  matching the `g_{n}^{r}` rule; the plain geometric ones stay `$p^{(1)}$`, `$p^{(2)}$` with no
  subscript. **Do not** write `p^{(1)}_{n}`, do not leave indices unbraced, and do not conflate
  `p_{n}^{(1)}` with `p^{(1)}`.
- **A braced two-line system is ONE numbered display**:
  `\[ \left\{ \begin{aligned} … &= … \\ … &= … \end{aligned} \right. \tag{1} \]`, rows aligned on
  `=`, and the `\tag` carries the print's own number even though the print sets it to the left of
  the brace (number position is presentation, R5). **Do not** emit two separate displays, **do
  not** use `\begin{cases}` (these rows are equations, not case alternatives), and **do not** drop
  the `\right.`.
- **A parenthetical whose contents are entirely mathematical is ONE math span, parentheses
  inside** — whether it holds one relation, several, or a bare list of symbols:
  `$(p_{g} = 0)$`, `$(r \geqq 0)$`, `$(p_{g} = 0, p_{n} = -1)$`,
  `$(\pi = 6, n = 5; \pi' = 12, n' = 16)$`, `$(p_{g}, p_{n}, P_{2}, p^{(1)})$`. The commas and
  semicolons between them are the print's and are kept, inside the math. **Do not** break it into
  `($p_{g} = 0$, $p_{n} = -1$)` with the parentheses in text mode, and do not reproduce the
  print's visual gap before the parenthesis with `\,` or `\ `.
  *(Two batches split on this — one wrapped punctuated lists in text-mode parentheses. The single
  rule above is the settled one; it renders identically and is easier to apply consistently.)*
  The exception is a parenthetical that also contains **words**, which stays in text mode with a
  math span per symbol: `(le système adjoint, $\infty^{2}$)`.
- **A stacked pair inside a large parenthesis is a binomial coefficient: `\binom{\nu+2}{2}`,
  `\binom{n-1}{3}`.** The print's staggered two rows are only its way of setting a binomial, and
  the stagger is presentation. **Do not** write `\left(\begin{matrix}…\end{matrix}\right)`,
  `{n-1 \choose 3}`, or a `\frac` inside parentheses.
- **`const.` stays inside the math span**: `$y = const.$`, giving the print's own math italics.
  **Do not** write `\text{const.}` or `\mathrm{const.}`, and do not break it into text mode.
- **Whether an elided article `l'` belongs inside an italic run is decided PER INSTANCE from the
  scan.** The print really does both: p249 sets `\emph{l'expression de $p_{n}$…}` and p250
  `\emph{l'ordre}` with a slanted `l` and an italic apostrophe, while p248's `l'\emph{Analysis
  situs}` has an upright roman `l`. Check the letterform against the roman words on the same line
  rather than assuming either shape. **Do not** regularize all occurrences one way.
- **A hyphenated two-name attribution is ONE `\emph` run**: `\emph{Riemann-Roch}`. The
  "each name its own `\emph`" rule above is about names separated by commas or `et`, and does not
  split a hyphenated compound. **Do not** write `\emph{Riemann}-\emph{Roch}`. Note the print
  letterspaces this compound only sometimes — plain on p294, letterspaced on p295 — and R20 is
  read per instance, so check the spacing on the page in hand rather than regularizing.
- **A standalone inline fraction the print sets at FULL size is `\dfrac`**, e.g.
  `$\dfrac{k(k-1)}{2}$`. R2/R16 ban `\dfrac` only *under* a large operator; with no operator
  present, and the print setting the fraction at display size in the running line, `\dfrac` is
  right. **Do not** write `\frac` for these, and **do not** promote the fraction to a `\[ … \]`
  display.
  **The rule is scoped by the printed size, so look before choosing.** Where the print sets an
  inline fraction at REDUCED size — numerals visibly smaller than the adjacent roman text, as in
  p296's `$\frac{1}{2} m(m+3)$` — it is `\frac`. Magnify if the two sizes are hard to tell apart.
- **The plurigenera characters of article 24 are `$p^{(1)}$` and `$p^{(2)}$`** — a parenthesized
  numeral as a braced superscript on a plain `p`, the parentheses raised as part of the exponent,
  as the print sets them. **Do not** write `p^1`, `p_{1}`, `p^{1)}`, or put the parentheses in
  text mode. They occur inside the heading of article 24 too, where math is permitted.
- **There are two different ellipses in this work, and they are set differently.**
  - The **bibliographic** ellipsis, standing for the tail of a cited title, is three tight ASCII
    periods in **text** mode, outside any `\emph`, with no space before them:
    `\emph{Ueber die algebraischen Functionen}..., Math.\ Annalen`. **Do not** write `\dots` or
    `\ldots` there, and do not pull it inside the `\emph` braces.
  - The **mathematical** ellipsis, standing for omitted terms, is `\ldots` on the baseline
    (`$x_{1}, x_{2}, \ldots, x_{r}$`, `$(\alpha = 2, 3 \ldots)$`) or `\cdots` when it sits between
    operators on the math axis (`$\lambda_{1}R_{1} + \cdots + \lambda_{r}R_{r}$`). **Do not**
    write bare `...` inside `$...$`. This follows settled corpus practice — nine works use
    `\ldots`/`\cdots` in math and none uses tight periods there.

## Things that look like exceptions but are not

- **This is an Antiqua French text**: there is no `ß`, no long-ſ and no Fraktur anywhere in it, so
  R19's normalizations simply have nothing to act on and the file correctly contains no `ß`.
  German titles quoted in the footnotes keep their edition spelling — `Ueber`, **not** `Über`.
- **Apostrophes are ASCII `'`** (`l'origine`, `d'une`, `dell'Acc.`), and an elision broken across
  a printed line is rejoined with no space (`dell'Acc.`, not `dell' Acc.`). **Do not** use the
  Unicode right single quote.
- **Hyphens the print spaces out for justification (`celle - ci`, `elle - même`) are set tight**:
  `celle-ci`, `elle-même`. **Do not** preserve the spacing or promote it to a dash.
- **`Cremona` used adjectivally is NOT letterspaced and is set plain** — "une transformation
  birationnelle (ou de Cremona)", "transformations de Cremona" name the kind of transformation,
  not the man, and the print spaces them normally. R20 is a per-instance reading of the scan, so
  check the spacing rather than the name. The same caution applies to any name that has become a
  term of art.
- **An `\emph` run broken by a page boundary is closed before the break and reopened after the
  next `\origpage{}`**, so every fragment file is brace-balanced on its own. **Do not** leave an
  `\emph{` open at the end of a page for the next one to close.
- **A word hyphenated across a PAGE break is joined, and the whole word is placed BEFORE the next
  `\origpage{}`** — `dif-` at the foot of p297 plus `férentes` at the head of p298 becomes
  `différentes` ending p297, with `\origpage{298}` after it and no blank line following. A page
  break is a line break, and R22 drops line-break hyphenation like every other such artifact; no
  corpus work leaves a word split at a page boundary. **Do not** keep the trailing hyphen, and
  **do not** leave the two halves on either side of the marker.
  *(Three batches left these split; they were joined mechanically at assembly.)*
- **A list numeral `1)` / `2)` stays outside any `\emph{}`**, even where the print italicizes the
  whole enumerated clause; the italics start at the first word after the parenthesis. **Do not**
  write `\emph{1) ou bien ...}`.
- **French thin spaces before `; : ? !` are dropped** — `réciproque?`, `théorème:`, `système;`.
  Spacing is presentation. **Do not** insert `\,`, `~` or a literal space before those marks.
- **The print's accents are genuinely inconsistent and are reproduced as printed** (R4, R23):
  p242 sets `rélation` and `géomètrique`, p244 `géomètrie` alongside a correct `géométrie` on the
  same page. **Do not** regularize any of these.
