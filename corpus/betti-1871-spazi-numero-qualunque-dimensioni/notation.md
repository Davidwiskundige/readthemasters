# Notation decisions — Betti 1871, *Sopra gli spazi di un numero qualunque di dimensioni*

Cross-page rendering decisions for this work. Batches cannot see each other; this file is how they
agree. Each entry states the decision, one clause of rationale, and **what not to do** — including
spacing, bracing and placement where those are part of the rule.

Author back-references in the text (`equazione (9)`, section numbers) are printed on the page and
are copied verbatim; they are not entries here.

## Summation

- **The summation glyph is `\sum`, never `\Sigma`.** Betti's sign is a large operator carrying
  limits in (5)/(6), and the same glyph appears bare elsewhere. Do **not** write `\Sigma`, and do
  **not** switch glyph because a particular Σ happens to carry no limits.
- **Betti's summation with limits and a running index is `\sum_{1}^{n}{}_{m}`.** The limits `1` and
  `n` go in the ordinary sub/superscript slots and the index letter follows as a separate
  empty-atom subscript `{}_{m}`, written immediately after the closing brace **with no space
  between them** — that reproduces the print, which sets `1` under the Σ, `n` over it, and `m`
  tucked at the Σ's lower right. Do **not** modernize to `\sum_{m=1}^{n}`, do **not** drop the `m`,
  and do **not** fold it into the lower limit as `\sum_{1,m}^{n}`.
- **A Σ printed bare stays bare: plain `\sum`, no sub/superscript, no index.** Confirmed under
  magnification on p143 (including eq. (10), which otherwise repeats eq. (6)). This is a genuine
  printed inconsistency and is reproduced under R23. Do **not** supply the `1`/`n`/`m` from (5)–(6)
  "for consistency".

## Derivatives, fractions and products

- **Derivatives use `d`, never `\partial`** — Betti writes total-derivative `d` throughout, even
  where the derivative is partial (`\frac{dF}{dz_{m}}`, `\frac{dz_{m}}{du_{r}}`). Do **not** write
  `\partial` anywhere in this work.
- **Fraction macro depends on position: `\frac` in display math, `\dfrac` inside `\begin{vmatrix}`,
  `\dfrac` for a standalone inline fraction.** Do **not** put `\dfrac` in an ordinary display, and
  do **not** use `\frac` inside a determinant.
- **Products are juxtaposition with nothing between the factors — no `\cdot`, no `\times`, and no
  spacing macro at all.** Betti sets adjacent fractions with no sign between them:
  `\frac{dF}{dz_{m}}\frac{dl_{m}}{dt_{0}}`. Do **not** insert `\cdot`, `\,` or `\;` between two
  multiplied fractions.
- **In a product of differentials each differential after the first takes a preceding `\,`:**
  `du_{r}\,du_{s}`, `dz_{1}\,dz_{2}\ldots dz_{n}`, `M\,du_{1}\,du_{2}`. This is the house thin
  space (R2/R16). Do **not** run them together as `du_{r}du_{s}`, and do **not** use `\;` or a
  literal space instead.

## Ellipses and determinants

- **`\cdots` (raised) between binary operators and inside matrices; `\ldots` (baseline) in a
  comma-separated list of symbols.** The print itself sets the dots at two heights. Do **not** use
  `\dots`, and do **not** use `\ldots` in a `+ \cdots +` chain.
- **A row of omitted rows in a determinant is one full row of `\cdots` cells — one `\cdots` per
  column — and where the print shows two dot lines, write two such rows.** Do **not** use
  `\hdotsfor`: it was tested and KaTeX 0.16 fails with "Undefined control sequence". Do **not**
  substitute `\vdots`.
- **Determinants are `\begin{vmatrix}` … `\end{vmatrix}`.** Do **not** hand-build the bars with
  `\vert`.
- **A system braced on the right is `\left.\begin{aligned}…\end{aligned}\right\}`, with `\tag{n}`
  placed after the `\right\}` and still inside the `\[ … \]`.** Do **not** use `\begin{cases}` for
  the braced systems.

## Subscripts, superscripts and Betti's objects

- **Every sub/superscript is braced, always — single characters included:** `S_{n}`, `S_{n-1}`,
  `S_{n-m}`, `T_{n-1}`, `z_{1}^{0}`, `ds_{n}^{2}`. Do **not** write `S_n` or `z_1^0` unbraced, and
  do **not** put spaces around the minus in a dimension index (`S_{n - 1}`).
- **A coordinate carrying the superscript zero is written subscript first, then superscript:**
  `z_{1}^{0}`. Do **not** reorder to `z^{0}_{1}`.
- **Betti's spaces are `S` with the dimension as a subscript. The *linear element* is lowercase
  `ds_{n}`; the *space element* is capital `dS_{n}`.** These are two different objects and must
  stay distinct. Do **not** normalize the case of either.
- **Two-index `E` subscripts are set exactly as printed: no comma when both indices are digits
  (`E_{11}`, `E_{12}`, `E_{22}`), a comma when the second index is compound (`E_{1,n-1}`,
  `E_{2,n-1}`, `E_{n-1,n-1}`).** Verified under magnification. Do **not** regularize to `E_{1,1}`,
  and do **not** drop the comma in `E_{1,n-1}`.

## Text, emphasis and structure

- **Letterspaced (Sperrung) definitional terms and small-caps proper names both become `\emph{...}`,
  one `\emph` run per continuous emphasized phrase** (R20/R24). Do **not** use `\textbf`,
  `\textsc` or `\textit`, and do **not** split a two-word term (`elemento lineare`,
  `linearmente connesso`) across two `\emph` runs. An elided article stays outside the run:
  `l'\emph{elemento lineare}`.
- **Ordinal degree is `$2^{\circ}$`.** Do **not** write `2\textordmasculine` or a literal `°`.
- **Section headings are the bare printed numeral with its period: `\section*{1.}`,
  `\section*{2.}`.** Betti's divisions are unlabelled numbers. Do **not** add `§`, and do **not**
  use `\subsection*`.
- **Not transcribed as page furniture:** running heads (which read "Sugli spazi di un numero
  qualunque di dimensioni" — note this differs from the title's "Sopra gli spazi"), page numbers,
  signature marks, the ornamental rule under the byline, and the decoration of p140's drop cap
  (transcribed as a plain letter).

## Ordinals

- **Word- and letter-ordinal superscripts are upright, via `\text{}` inside math:**
  `$m^{\text{esima}}$`, `$(p_{m}+1)^{\text{esimo}}$`, `$(m-1)^{\text{esima}}$`, `$2^{\text{a}}$`,
  `$1^{\text{a}}$`. Corpus precedent (`$\mu^{\text{ten}}$` in abel-1826), and the print sets them
  upright. Do **not** write `\mathrm{}`, `\textordfeminine`, a literal `ª`, or an italic `$2^{a}$`.
  The masculine *degree* ordinal keeps its own form, `$2^{\circ}$` / `$3^{\circ}$`.

## More on emphasis

- **Small-caps proper names become `\emph{}` in ordinary mixed case:** `\emph{Listing}`,
  `\emph{Riemann}`. Do **not** use `\textsc{}`, and do **not** keep the all-caps shape as
  `\emph{RIEMANN}`.
- **A whole letterspaced theorem or lemma statement is ONE `\emph{...}` run**, its closing period
  inside the run and its inline math left in place. Do **not** split it per sentence, and do
  **not** emphasize only the opening clause.

## Page joins

- **A letterspaced run that crosses a printed page boundary is closed at the end of the earlier
  fragment and reopened as a fresh `\emph{` immediately after the next `\origpage{}`, with no
  blank line between the two.** An unclosed `\emph{` would stop the assembled `original.tex`
  compiling; a blank line there would invent a paragraph break the print does not have. Do
  **not** do either.
- **A word hyphenated across a page break is written whole at the START of the later page's
  fragment**, and the earlier fragment stops at the preceding word boundary. Do **not** leave the
  half-word on the earlier page.
- **A page that opens mid-sentence has NO blank line after its `\origpage{}`.** Only start a new
  paragraph where the print does.

## Punctuation as printed

- **A comma after `\ldots` appears only where the print sets one.** p145 prints
  `$A_{1}$, $A_{2},\ldots A_{t}$` (none) and p147 prints `$a_{2}$, $a_{3},\ldots, a_{m-1}$` (one);
  both are verified against the scan. Do **not** regularize the two to a single form.

## Integrals and indexed sums (from §§5–7)

- **Betti's multiple integral carries its multiplicity as a subscript on the integral sign:**
  `\int_{n}`, `\int_{n-1}`. Do **not** write a bare `\int` where the print sets a multiplicity, do
  **not** promote it to `\iint`/`\idotsint`, and do **not** move it to a superscript. Where the
  print genuinely sets a bare ∫ (p153, eq. (3)) it stays bare, under R23.
- **An integral whose subscript is a DOMAIN rather than a multiplicity uses the same slot, braced:**
  `\int_{S^{(t)}_{n-1}}`, `\int_{R}`, `\int_{A_{r}}`, `\int_{C}`. Do **not** write
  `\int\limits_{...}`, do **not** add `\,` before the integrand, and do **not** convert a domain
  subscript into a multiplicity or the reverse — both forms occur on p154 and are distinct.
- **A Σ carrying a running index is `\sum_{t}` / `\sum_{r}`: the index in the ordinary subscript
  slot, braced, and nothing else.** This is not the `\sum_{1}^{n}{}_{m}` form of §5. Do **not**
  write `\sum_{t=1}`, do **not** add the `{}_{m}` empty atom here, and do **not** strip the index
  to a bare `\sum` (a bare Σ also occurs and must stay bare).

## Primes, superscripts and their order

- **Primes and subscripts keep the print's own order, per symbol, and are not regularized across
  symbols:** `S'_{n-1}`, `S''_{n-1}` (prime first) but `X_{r}^{0}`, `X_{r}'`, `X_{r}''`,
  `X_{r}'''` (subscript first); likewise `R'_{1}`, `R'_{2}`, `R''`. Do **not** write `X'_{r}` or
  `X^{0}_{r}`, and do **not** move `S`'s prime after its subscript.
- **A parenthesized index superscript precedes the subscript: `S^{(t)}_{n-1}`, `du^{(t)}_{1}`,
  `du^{(t)}_{n-1}`, both braced.** The p153 determinant sets the two orders inconsistently for one
  and the same symbol (`du_{1}^{(t)}` in the first column, `du^{(t)}_{n-1}` in the last), which is
  compositor variation, so this order is imposed throughout. Do **not** write `du_{1}^{(t)}` or
  `S_{n-1}^{(t)}`. (The "subscript first" rule elsewhere is specific to the coordinate `z_{1}^{0}`.)

## Emphasis around displays

- **A letterspaced theorem statement interrupted by a display becomes TWO `\emph{...}` runs — one
  closing at the colon before the display, one reopening on the line after the `\]` — separated by
  a plain newline, not a blank line, with the display itself outside both runs.** `\emph{}` cannot
  span `\[ … \]`. This refines the "one `\emph` run per statement" rule, which assumed prose-only
  statements. Do **not** wrap the display inside `\emph{}`, and do **not** drop the emphasis from
  the tail sentence after the display.

## Inequalities

- **Relational operators keep spaces around them (`$0 < t < m$`, `$t' > t$`) while dimension
  arithmetic stays tight (`$n-1$`, `$m-t-1$`).** Do **not** write `$0<t<m$`, and do **not** space
  the minus in a dimension index.

## Show-through is not type

- This scan bleeds the reverse leaf through at roughly the type's own grey. A centred row of dots
  and a marginal `(2)` on p152 are p151's equation (2) showing through **mirrored**, and are not
  transcribed. Do **not** "restore" them in a verification pass. When something looks like stray
  type in a margin or across a fraction bar, read it for mirroring before transcribing it.

## The doubled integral sign (§7)

- **A printed pair of full-size ∫ glyphs is `\iint`** (p157, the integral over the 2-dimensional
  `C`). Do **not** write `\int\int`, and do **not** convert it to `\int_{2}`. This does not
  conflict with the rule above: that one governs an integral whose *subscript* carries the
  multiplicity, whereas here the multiplicity is in the doubled sign itself and no subscript is
  printed.

## Two more readings settled

- **`L` with a compound index is `L_{p_{1}}`, with a lowercase italic `p`** — verified under
  magnification on p156, where at page resolution it reads as a capital `P`. Do **not** write
  `L_{P_{1}}` or `L_{p1}`.
- **The `\section*{7.}` heading on p156 is real type, not show-through** — it is bold and correctly
  oriented while everything around it is mirrored. Do **not** delete it in a verification pass, and
  do **not** read the wide gap there as a mere paragraph break.

## Rulings from the whole-work proofread (Phase 5b)

These settle constructions that two batches had rendered two different ways. They are presentation
only — none of them changes what the print says.

- **A differential that follows a NON-differential factor takes `\,` too, not a bare space:**
  `\frac{dV}{dp_{c}}\,dC`, `\left(\ldots\right)\,dz_{1}`, `\frac{dz_{r}}{du}\,du`. A literal space
  renders as *nothing* in math mode, so the two forms looked different on the page. This extends
  the "product of differentials" rule above, whose own example `M\,du_{1}\,du_{2}` already shows a
  non-differential factor taking it. Do **not** leave a bare space at such a junction. The one
  place a bare space is right is **after `\ldots`** (`\ldots dz_{n}`), which supplies its own
  spacing — do **not** write `\ldots\,dz_{n}`.
- **The separator between the members of a displayed list of equations is `\quad`:**
  `F_{1} = 0, \quad F_{2} = 0,\ldots`. Do **not** use `\;`.
- **Inside a function's argument list the separator is a plain space, not `\quad` or `\;`:**
  `F[l_{1}(t_{0}), l_{2}(t_{0}),\ldots, l_{n}(t_{0})]`, matching `F(z_{1}, z_{2},\ldots, z_{n})`.
- **Elided rows in an `aligned` SYSTEM are a wide dot line,
  `&\;\;\cdots\cdots\cdots\cdots\cdots\cdots\`, one such row per dot line the print shows** — the
  print sets a dotted rule spanning nearly the full width of the equations. Do **not** use the
  short `\cdots & \cdots` form here. This is distinct from the DETERMINANT rule above, where the
  elided row is one `\cdots` per column; determinants keep that form.
- **Relational operators keep their spaces even against a bare numeral: `$< 0$`, not `$<0$`.**
