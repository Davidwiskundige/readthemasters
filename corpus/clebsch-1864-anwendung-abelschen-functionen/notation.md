# Notation decisions — Clebsch 1864, *Anwendung der Abelschen Functionen in der Geometrie*

Work-spanning rendering decisions for this transcription, so that pages transcribed in separate
batches stay consistent with each other. Each entry is the decision plus why it was made.
The whole paper, pp. 189–243, follows this list.

## Symbols

- **Summation sign → `\Sigma`, the letter — never `\sum`.** The print sets one slanted capital-sigma
  letter throughout, not a modern large operator. Pages 189–206 use `\Sigma` 21 times; the
  independently-transcribed pp. 211–222 agree (32 times). An early draft of pp. 207–210 used
  `\sum` and was conformed before assembly.
- **Σ carrying limits → `\mathop{\Sigma}\limits_{...}^{...}`.** First arises on p. 207, where the
  print stacks the limits above and below the letter (`n=−∞`…`n=+∞`, `h,k=1`…`h,k=p`, `k=1`…`k=p`).
  This keeps the letter and the printed limit placement. Verified to render in the site's KaTeX
  0.16 build, including nested inside an exponent.
- **Multiplication dot → a literal `.`, set TIGHT with no spacing** — never `\cdot`, `\times`,
  juxtaposition, or `\,.\,`. Clebsch writes products with a period, in numerals and in symbol
  products alike. Write `F''(ss).F''(zz)`, `n.(n-1)`, `\Theta.\frac{...}{...}`, `28.64`,
  `\frac{p.p-1\ldots p-k+1}{1.2\ldots k}` — no space, no thin space, on either side, whatever the
  operands are. It is the author's notation (R3).
  *Do not relax this because the operands are large.* Pages 189–206 set 63 such dots and every one
  is tight, including before a `\frac` and before `\Sigma`. `\cdot` appears in this work **only** as
  a matrix or array continuation row — never as a product, and never replaced by `\vdots`, `\ddots`
  or an `\ldots` row. Write `\cdot`s separated by `\quad`, **counting the dots the print actually
  sets** — it is not a fixed number (7 and 11 on p. 231, 9 on pp. 227–230, 13 on p. 234). Inside an
  `aligned`, give the row an empty second cell so the dots stop at the equation body and do not run
  under the `= 0` / `\equiv` column. Counts verified against the scan: 10 on p. 224 (a 4-column
  matrix row, distributed 3/3/2/2), 12 and 15 and 15 on p. 225, 12 on p. 227, 9 on pp. 228–230,
  7 and 11 on p. 231, 13 on p. 234, 11 and 10 on p. 240, 6 on p. 242. **Count them; do not assume
  the neighbouring page's number.**
- **A `\Sigma` standing immediately before a fraction takes a thin space: `\Sigma\,\frac{...}`** —
  never a tight `\Sigma\frac`, and never a multiplication dot `\Sigma.\frac`. Measured on the scan
  (p. 195): the print leaves a 9px gap there and sets no dot, where a real multiplication period on
  p. 193 is a 5px blob with about 8px of air on each side and registers plainly. The thin space is
  what keeps this case visibly distinct from the dot construction `\Theta.\frac{...}` in the very
  next display. This holds for the limits form too —
  `\mathop{\Sigma}\limits_{h=1}^{h=\mu}\,\frac{...}`, never tight (p. 226, three occurrences).
  *But only when the `\Sigma` stands immediately before the fraction.* Where a coefficient
  intervenes, set it tight — `\Sigma\pm c\dfrac{...}`, never `\Sigma\pm c\,\dfrac{...}` — because
  the thin space exists to keep the sigma from reading as a multiplication dot, and with `c` in
  between there is nothing to disambiguate (p. 228, two occurrences).
- **`≧` → `\geqq`, for both of the sorts this print uses — never `\geq`, and never `\leqq`.** The
  compositor has two double-barred sorts and mixes them: the bars sit *below* the wedge in p. 229's
  first display and *above* it in the other five occurrences on pp. 229–230, and p. 195 uses the
  bars-above cut. Magnified, every wedge opens leftward in both sorts, and the mathematics agrees —
  `k ≦ m` beside `k ≧ m+n−3` in one display would force max(m,n) ≤ 3. Sort variation is glyph
  shape, so it is normalized; the direction of the sign is notation, so it is not.
- **Ellipsis height follows the print, per context: `\cdots` between `+` signs, `\ldots` on the
  baseline.** The print raises the dots to the operators' centre in a `+`-chain
  (`m^{(1)}+m^{(2)}+\cdots+m^{(s)}`) and sets them on the baseline in comma lists and products
  (`x_{1}$, $x_{2}$, \ldots`, `X_{1}X_{2}\ldots X_{s}`). Do not unify on one macro in either
  direction.
- **An ordinal fused to a parenthesised index is one exponent: `m^{(1)\text{ten}}`** — never
  `m^{(1)}{}^{\text{ten}}`, which sets a second exponent group, and never a bare `m^{(1)ten}`
  (p. 227).
- **Capital Greek letters are the plain macros — `\Delta`, `\Omega`, `\Sigma`, `\Theta`, `\Psi` —
  never the `\var...` variants.** The print sets Δ and Ω slanted exactly as it sets the Σ, Θ and Ψ
  this work already renders with the plain macro; using `\varDelta` for one of them would make a
  single capital behave differently from its neighbours in the same display (pp. 225–226).
- **`≡` vs `=` followed per occurrence.** The three-bar sign is set `\equiv`, the two-bar `=`. The
  distinction is mathematical — congruence mod periods or mod 2 against plain equality — and must
  never be normalized to one sign.
- **Rank → upright `\mathrm{w}`.** The print sets the rank as an upright w while every neighbouring
  variable is italic, and an italic `w` is already in use in this work for other quantities (the
  quadratic form on pp. 213–217, the surface `w=0` on p. 222). Used on pp. 191–192 and 220–221.
- **Ordinals → `^{\text{ter}}` / `^{\text{ten}}` / `^{\text{te}}` / `^{\text{tes}}`** (R21), e.g.
  `m^{\text{ter}}`, `p^{\text{ten}}`, `h^{\text{te}}`, `r^{\text{tes}}` — never a bare `h^{te}`. This includes numeric stems:
  `9^{\text{ten}}`, `49^{\text{ten}}`, never `9ten` and never `9\textsuperscript{ten}`.
  Where the ordinal follows a fraction, write `\frac{...}{...}{}^{\text{ter}}` so the fraction is
  not swallowed into the exponent.
- **`§.`** is a literal section sign followed by a non-breaking space **when a number follows**:
  `§.~9.` (R19). The tie exists to keep the sign with its number, so where a word follows instead —
  "im folgenden §. geschehen" (p. 223) — write a plain space, not `~`.
- **Equation tags keep the author's trailing period**: `\tag{1.}`, `\tag{12.}` (R5). Every number is
  printed on the page it belongs to, so batches need no shared state for it — **and must not infer
  one.** The run is *not* continuous through the paper: it climbs to `(28.)` on p. 236 and then
  **restarts at `(1.)` in §. 19** (pp. 240–241 print `(1.)`–`(6.)`). Tag whatever the page prints.
  Never continue the earlier series as `(29.)` ff., and never disambiguate a repeat by inventing a
  compound label such as `19.1` — the author's own back-references on pp. 241–242 ("Gleichung (2.)",
  "die Gleichungen (3.)") point at the restarted series and would stop matching.

## Formula layout

- **A fraction nested inside another fraction is written `\dfrac`, never `\frac`.** This print sets
  the inner fraction at the SAME size as the outer one — it does not shrink it the way TeX's
  default `\frac` does. Measured against the scan on pp. 193 and 195, across four separate compound
  fractions: at both nesting levels the `x` glyph is 13–14px tall and 14–16px wide and the `∂` is
  21–22px, agreeing within ±1px, where a script-size shrink would put the inner `x` at 9–10px.
  Inner rules are shorter (47px against 172–347px) only because `∂f/∂x_1` is a shorter expression.
  So write `\frac{x_{2}\,dx_{3} - x_{3}\,dx_{2}}{\dfrac{\partial f}{\partial x_{1}}}` — outer
  `\frac`, inner `\dfrac`.
  *Do not reason from "display math is already display style, so `\dfrac` is redundant".* That is
  true of a fraction at the top level of a display and false of a nested one, and it is the exact
  mistake two independent batches made: given only the house-style rule that `\dfrac` is redundant
  under a large operator, both wrote `\frac` at every level and flattened about 28 nested fractions
  across pp. 193–195. HOUSESTYLE's `\frac`-not-`\dfrac` ruling governs the operand of a large
  operator; it says nothing about nesting.

- **A bracketed system of equations is `\left\{ \begin{aligned} ... \end{aligned} \right.`** with the
  `=` signs aligned and any `\tag` outside the brace — never `cases`, which left-aligns the rows and
  drops the alignment the print shows, and never a bare `matrix`. Used for eq. (3.) on p. 191 and
  eq. (20.) on p. 225, both of which the print sets with a full-height brace.

- **An inline fraction the print sets at full display size is `\dfrac`** — never `\frac`, never
  promoted to its own display, and never rewritten to a `/` or `:`. Clebsch sets `mnk/r`,
  `mn(m+n-4)/2`, `(n/2)^{2p}` and their like inline at the same size as a displayed fraction, with
  the line spacing visibly opening to take them. HOUSESTYLE permits a standalone inline `\dfrac`;
  its `\frac`-not-`\dfrac` rule governs only the operand of a large operator. A fraction at the top
  level of a display stays `\frac`, which is already display style.

- **Subscripts are braced: `x_{1}`, `c_{2}`, `\beta_{3}`** — never bare `x_1`, even for a single
  digit. Both forms render identically, so nothing about the page decides it; it is a consistency
  rule, and its whole value is that it is not re-decided per batch. Two batches of this same work
  disagreed on it (one wrote `x_1` throughout pp. 191–192, the next `x_{1}` throughout pp. 193–196),
  and the assembled file had drifted the same way — pp. 189–206 braced 218 subscripts while
  pp. 207–222 left 166 bare. Normalized to braced throughout on 2026-08-31. Braced also stays
  correct when a subscript grows past one character (`u_{23}`, `x_{12}`), which this work has.

- **Footnotes follow HOUSESTYLE R15 exactly, using the print's own asterisks.** The in-text
  reference is a superscript `${}^{*)}$` / `${}^{**)}$`; where it attaches to a display formula it
  is carried inside the display as `\,{}^{*)}$`. The note itself is placed inline as a complete
  unit at the end of that page's main text, led by `\textbf{*)}`. Never re-letter the marks to
  `(a)`/`(b)` — R15 fixes the note's *placement*, not the mark the compositor used — and never
  write the in-text mark as a bare `~*)` or the note as a bare `*)` line.

- **A LaTeX control space follows an abbreviation dot: `p.\ 129`, `pag.\ 285`, `Monatsber.\ der`,
  `A.\ Clebsch`** — not `~`, and not a bare space. This is HOUSESTYLE R17. Normalized throughout on
  2026-08-31; pp. 189–206 had previously mixed the two (8 tildes against 13 control spaces) while
  pp. 207–222 used the control space exclusively (40).

## Typography

- **No long-ſ and no eszett.** This print is Antiqua with round s only: `dass`, `muss`, `lässt`,
  `grosse` stay as `ss`. HOUSESTYLE **R19's `ſs → ß` mapping does not apply to this work** — the
  file contains no `ß`, and that is faithful, not an oversight.
- **German quotation marks** are written as literal Unicode `„ … "` rather than `` `` … '' ``
  (R18, R22).
- **Personal names** italicized in the print are wrapped at the stem only: `\emph{Abel}schen`,
  `\emph{Riemann}s`, `\emph{Jacobi}sche` — matching what the print italicizes.
- **Headings carry no `\emph`** (R25), even where the print italicizes a name inside them.
- **Letterspacing *inside* an already-italic passage is not marked at all** — leave the word plain
  within the surrounding `\emph` run, and never nest a second `\emph` inside the first. The print
  gesperrts a word inside an italic *Satz* ("g a n z e" on p. 224, "s ä m m t l i c h e r" on
  p. 226), but R24 collapses both devices to `\emph`, so a nested run would render identically —
  and a text-mode brace group inside `\emph{}` breaks `tex.js`'s `[^}]*` match (R18). The same
  word set gesperrt in *roman* text IS `\emph`'d, as on p. 223. Flagged as a discrepancy once by a
  verification pass; it is not one.
- **`\uncertain{}` is never nested inside `\emph{}`.** `site/src/lib/tex.js` matches these
  arguments with `[^}]*`, so a nested brace group silently leaks the tail into the running text
  (R18). Split the `\emph` run and place `\uncertain{...}` between the two halves.
- **An `\emph` run is broken around every display formula**, never spanned across one: write
  `\emph{...}` `\[ ... \]` `\emph{...}`, not `\emph{... \[ ... \] ...}`. Same `[^}]*` limit — the
  display's braces would truncate the run. This work's italic *Sätze* routinely enclose a display
  (pp. 195, 223, 224, 226), so the case is common, not exotic. An italic run interrupted by a
  **page break** is likewise split, one `\emph` per fragment (pp. 236/237) — never one run spanning
  an `\origpage`.
- **An italic *Satz* is its own paragraph**, with a blank line before and after — never run on into
  the roman text that follows it. The print sets a Satz as a doubly-indented block and resumes the
  following roman text flush left, which is block-quote layout rather than paragraph continuation.
  A roman continuation after a *display* (`oder`, `d.\ h.`, `woraus der Satz folgt:`) takes no blank
  line, as before.
- **A prime on a subscripted variable goes before the subscript: `u'_{k}`, `u''_{k}`, `A'_{k}`** —
  never `u_{k}'`. The print stacks the prime directly above the subscript (p. 238); writing it after
  sets it beside the subscript instead. **A primed variable raised to a power is braced:
  `{r'}^{2p}`** — never `r'^{2p}`, which KaTeX rejects as a double superscript (p. 242).

- **A display whose continuation line hangs its relation sign out to the left** is an `aligned` with
  the sign in the left cell — `& body \\ \equiv{} & body` (p. 240 eq. (3.), p. 241). Never `cases`,
  never `gathered`, and never pull the sign inline into one long row.

- **The `\left\{` brace form is used only where the print sets a full-height brace.** An untagged,
  unbraced run of display equations — even one carrying a dot-continuation row — is a bare
  `\begin{aligned}` inside `\[ \]` (p. 242). Do not add a brace the compositor did not set.

## Structure

- **Section headings are two elements**: `\section*{§.~N.}` for the centred number line, then
  `\subsection*{...}` for the descriptive title beneath it, matching the print's two lines.
- **Words hyphenated across a page break** are written whole on the page where the word *begins*;
  the next fragment starts at the following word. This keeps concatenated fragments from inserting
  a break mid-word. Two pages violated this and were repaired on 2026-08-31: p. 195 ended `An-`
  with p. 196 opening `zahl`, and p. 198 ended `aus-` with p. 199 opening `reichend`, both of which
  rendered as a stray hyphen and space inside the running word.
- **Running heads, page numbers and signature lines** (e.g. `27 *`) are page furniture and are not
  transcribed.
- **An unnumbered figure** (p. 215, referenced only as "siehe die Fig.") is keyed to its page:
  `\rmfigure{figures/fig-215.png}{Fig.}{...}`. Numbered figures elsewhere in the work should use
  `fig-<number>.png` as usual (R7).
