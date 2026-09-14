# Notation decisions — Picard 1885

Cross-page rendering decisions for this work (HOUSESTYLE R27). Batches cannot see each other; this
file is how they agree. Each entry states the decision, one line of why, and **what not to write
instead**. Where spacing, bracing or placement is part of a rule, it is stated in words — not left
to be inferred from an example.

## Figures and letters

- **Old-style figures are transcribed as ordinary digits.** The journal sets text figures: zero
  prints as a small `o`, one as a dotless `ı` (the running head reads `28ı`). Write `f(x, y) = 0`,
  `\tag{1}`, `m - 1`. **Do not** write the letter `o` for zero, **do not** write `\iota` or `ı` for
  one, **do not** write `\mathrm{o}`.
- **Uppercase Latin operators and polynomials are plain math letters:** `P`, `Q`, `M`, `A`, `B`,
  `F`, and subscripted `A_{1}`, `B_{1}`, `P_{1}`, `M_{1}`. The print sets them upright roman against
  italic lowercase, but upright-vs-italic is presentation, not notation. **Do not** write
  `\mathrm{P}`, `\mathbf{P}`, `\text{P}` or `\operatorname{}`.

## Subscripts, exponents, primes

- **Subscripted coefficients are braced even for a single digit:** `a_{1}`, `d_{2}`, `A_{1}`.
  **Not** `a_1`. Exponents likewise: `^{2}`, `^{n'-n}` — **not** `^2`.
- **Primes are the ASCII apostrophe in math:** `x'`, `z'`, `n'`. Where a prime and a subscript meet,
  **the prime comes first**: `f'_{z}`. **Do not** write `\prime`, **do not** write `f_{z}'`,
  **do not** use a Unicode `′`.

## Fractions and differentials

- **Nested fractions inside a display use `\dfrac`; the top level uses `\frac`.** The print sets
  `\partial f/\partial z'` at full size inside the denominator, so write
  `(ax' + by' + cz' + d)^{2}\dfrac{\partial f}{\partial z'}`. **Do not** flatten an inner fraction to
  a slash, and **do not** put `\displaystyle` inside `\[ \]`.
- **Differentials carry a thin space: `\,dx`, `\,dy`, `\,dz`** — including inside numerators
  (`A\,dx' + B\,dy'`). The thin space is part of the rule, not decoration. **Do not** write a bare
  `dx` after a symbol, **do not** use `\;` or `\ `.
- **Partial-derivative displays keep `\partial`; total-derivative displays keep `d`**, exactly as
  printed — `\dfrac{\partial u}{\partial x}` on p. 283 against `\dfrac{du}{dz}` in the
  Briot–Bouquet form. **Do not** unify the two.

## Punctuation and spacing

- **A French thin space before a colon is written `~:`** (`espèce~:`, `algébriques~:`). This journal
  sets a space **only** before the colon: semicolons, question marks and exclamation marks are set
  tight. So write `espèces;` and `indépendantes?` with **no** `~`. **Do not** add `~` before `;`,
  `?` or `!`; **do not** use `\,` or a literal U+00A0.

## Displays

- **Multi-line systems go in one display with `\begin{aligned}`**, aligned on `&=`, keeping the
  print's own line-end punctuation (`,` `,` `;`). Established corpus practice (`betti-1871`).
  **Do not** emit separate `\[ \]` displays, and **do not** use `cases`, `array`, `gather` or
  `eqnarray`.
- **Two displays printed side by side on one line stay one display, joined by `\quad`** — the
  `dx`/`dy` pair, the `P/M`/`Q/M` pair. **Do not** split them into two displays; **do not** use
  `\qquad` or `\hspace`.
- **Equation numbers use `\tag{n}` with the author's bare numeral and no period.** The print writes
  `(1)`, `(2)` without a trailing dot, so `\tag{1}` — **not** `\tag{1.}`, **not** `\tag{(1)}`.
  In-text back-references are copied as printed: `telle que (1)`.

## Structure

- **Numbered articles are `\textbf{1.}` at the head of their paragraph**, matching the print's bold
  article number (R15 already uses `\textbf` for footnote letters). **Do not** write
  `\section*{1.}`, **do not** use Roman `I.`, **do not** italicize.
- **Part headings keep the print's capitals:** `\section*{PREMIÈRE PARTIE.}` — accents included,
  trailing period included. **Do not** lowercase to "Première partie", **do not** add `\emph` or
  `\textsc`, and **never** put a text-mode brace group inside a heading (R25).
- **Footnotes (R15):** the in-text mark is `${}^{(1)}$` — parenthesized, superscript, math-mode —
  and the note itself is the last paragraph of that page's fragment, led by `\textbf{(1)}`.
  **Not** `\footnote{}`, **not** `${}^{1}$` without parentheses.
- **The author's byline is a plain paragraph: `Par M. Émile Picard.`** The print's caps/small-caps
  device (`Pᴀʀ M. Éᴍɪʟᴇ PICARD.`) is typeface, not content. **Do not** set `PICARD` in caps,
  **do not** use `\textsc`, `\emph` or `\textbf`.

## Page breaks and orthography

- **A word hyphenated across a page break is completed on the page where it begins**, before the
  next `\origpage`. So p. 282 ends `…fonctions uniformes` and p. 283 opens `quadruplement…`;
  p. 283 ends `…la différentielle` and p. 284 opens `totale`. **Never** leave a trailing `uni-`,
  **never** repeat the head fragment on the later page, and **do not** move the whole word to the
  later page.
- **French orthography is kept exactly as printed, including missing circumflexes:** `reconnaitre`
  (verified under magnification, twice, pp. 282 and 283). **Never** "correct" it to `reconnaître`.
  Accented letters are literal Unicode (`é è à ê ô ç û`), **never** `\'e` or a backtick form (R18).

## Added after batch 2 (pp. 285–288)

- **Article numbers are Arabic, set bold.** The print runs `1.` (p. 283), `2.` (p. 285), `3.`
  (p. 287), `4.` (p. 288). The p. 287 numeral is an old-style **3** — flat top stroke running
  straight into the bowl, no left stem — which reads as a `5` at prepared resolution but is
  unambiguous magnified, and the 2–3–4 sequence confirms it. Write `\textbf{3.}`. **Do not** write
  `\textbf{5.}`, **do not** use Roman `III.`
- **Greek function letters are `\varphi`, `\psi`, `\chi`.** The print's phi is the loop form, with no
  tall straight stem above x-height. **Do not** write `\phi`, **do not** write `\mathrm{\varphi}`,
  **do not** use a literal Unicode `φ` in math.
- **Second partial derivatives of `f` are `f''_{zy}`, `f''_{zz}`, `f''_{zx}`** — double prime first,
  then the braced two-letter subscript, matching the `f'_{z}` rule above. **Do not** write
  `f_{zy}''`, **do not** expand to `\partial^{2}f/\partial z\,\partial y`, **do not** use a single
  prime.
- **A single long equation broken across two printed lines goes in one `\[ \]` with
  `\begin{aligned}`**, a leading `&` on each line and `\qquad` indenting the continuation (p. 286
  top display). This extends the `aligned` ruling above from systems to run-on equations.
  **Do not** use `split`, `multline`, `gather`, or two separate displays.

## Added after batch 3 (pp. 289–292)

- **`\neq` is written where the print shows only the diagonal slash.** p. 292 sets `MNP ≠ 0` but the
  two horizontal bars of the `=` have dropped out, leaving a bare slash; magnified, the slash sits at
  `=`-height with bar remnants. Write `MNP \neq 0`. **Do not** write `\gtrless`, `\slash` or `/`.
- **Second partials at a double point take the point's own letters as subscripts:** `f''_{aa}`,
  `f''_{ab}`, `f''_{ac}`, `f''_{bb}`, `f''_{bc}`, `f''_{cc}` (p. 290), extending the `f''_{zy}` rule
  above to the `(a, b, c)` system. The symmetric 3×3 pattern is what disambiguates the individually
  mushy subscripts. **Do not** silently re-letter to `f''_{xx}`, and **do not** reorder to `f''_{ba}`.

## Added after batch 4 (pp. 293–296)

- **Inline running-text fractions use `\dfrac`:** `$\dfrac{y}{x}$`, `$\dfrac{x}{z}$`, `$\dfrac{x}{t}$`.
  The print sets them full-size, opening the line leading to fit them. **Not** `\frac`, **not** `y/x`.
- **A connecting word inside a display is `\text{...}`:** p. 295 sets `B/f'_z et A/f'_z` on one
  display line, written `\frac{B}{f'_{z}} \quad \text{et} \quad \frac{A}{f'_{z}}`, extending the
  `\quad` side-by-side rule above. **Not** `\mbox`, **not** two displays, **not** a bare `et` in math.
- **A numerator broken across two printed lines under a tall brace is set as one line and the brace
  dropped** (p. 296). The brace exists only to group the line break, which is presentation.
  **Not** `aligned` nested inside `\frac`, **not** `\left\{ \right.`.
- **Article cross-references use `nº`** — the masculine ordinal indicator as literal Unicode, e.g.
  `(nº 5)` on p. 296. **Not** `n°` (degree sign), **not** `n\textsuperscript{o}`, **not** `no.`
- **`f'_z` is single-primed everywhere** — it is `∂f/∂z`, so `f'_{z}`, `f'_{Z}`,
  `tf'_{z}(x, y, z, t)`. The glyph reads as a possible double prime on pp. 294–296 where the prime
  merges with the `f` descender, but the clean `f'_{Z}(1, Y, Z, T)` on p. 296 settles it. An
  application of the entries above, recorded because the ink invites the wrong call.

## Added after batch 5 (pp. 297–300)

- **The four auxiliary polynomials are `\theta_{1}`…`\theta_{4}`** — plain `\theta`, braced Arabic
  subscript. The print's glyph carries a top-left curl that could be read as `ϑ`, but the work sets
  only one theta form, so there is no contrast to preserve and the curl is a shape of the face.
  **Do not** write `\vartheta`, a literal Unicode `θ`, or `\theta_1`.
- **The p. 300 integral takes only an upper limit, parenthesized: `\int^{(x, y, z)}`.** Unlike the
  p. 296 integral (`\int_{x_{0}, y_{0}, z_{0}}^{x, y, z}`), this one prints `(x, y, z)` above the
  sign with **no** lower limit and **with** parentheses. **Do not** supply a lower limit from p. 296;
  **do not** strip the parentheses.
- **Euler's fourth term is `f'_{t}` with no `t` factor** (p. 297 bottom display): the print writes
  `x f'_{x} + y f'_{y} + z f'_{z} + f'_{t}`, the dehomogenized form at `t = 1`. **Do not** "fix" it
  to `t f'_{t}` — the p. 298 definition of `\theta_{4}` confirms the printed form is consistent.
- **`0 = [\dots] + [\dots] + [\dots]` broken over three printed lines uses square brackets, one
  `aligned`, a leading `&` on each line and `\qquad` on the continuations** (p. 300 final display) —
  an application of the run-on-equation rule above. The print's delimiters really are `[ ]`.
  **Do not** substitute `\left( \right)`.
- **Reach for `\dfrac` only where the nesting condition above actually holds.** On pp. 297–300 no
  fraction sits inside another fraction or inside a script, so every one is top-level `\frac` —
  including those inside `\left( \right)` and `\left[ \right]`, which are display-style anyway.
  **Do not** use `\dfrac` merely because the print sets a fraction full size.

## Corrections from the verification pass

- **p. 287's article numeral is settled by the 2–3–4 sequence, not by the glyph.** The entry above
  called it "unambiguous magnified"; the verifier found it near-indistinguishable from this face's
  `5` even at source resolution (compare the `5` in the running head of p. 285). What decides it is
  that `2.` (p. 285) and `4.` (p. 288) are both clean, so the article between them is 3. Treat any
  isolated old-style 3/5 in this print as undecidable on shape alone and look for a sequence.
- **p. 296 `(nº 3)` was first transcribed `(nº 5)`** — the same glyph, misread because no sequence
  was available there. Both the shape (flat top stroke into the bowl, no left stem) and the
  mathematics (articles 3 established `A = x\varphi + A_{1}`, `B = y\varphi + B_{1}`; article 5 is
  about isolated double points) give 3.
- **p. 292 sets an upright roman capital `B` in `… + a'x\,dx - By\,dy + …`**, a different sort from
  the italic lowercase `b` of the same term's second occurrence four lines below. The algebra wants
  lowercase (`a = b' = c'' = 0` in `A = ax + by + cz + …`), so this is a compositor's error — and R4
  says reproduce it, not correct it. **Write `By\,dy` in the display on p. 292 and `by\,dy` in the
  fraction below it**, exactly as printed. **Do not** normalize the two to each other.

## Added after batch 6 (pp. 301–304)

- **Chapter II's article numbers restart at 1.** Part I ran `1.`–`8.` (pp. 283–297); the
  `\section*{CHAPITRE II.}` on p. 299 restarts the count, so `\textbf{1.}` (p. 299), `\textbf{2.}`
  (p. 302), `\textbf{3.}` (p. 303). Verified against the assembled sequence, not against the glyph.
  **Do not** continue the Part I numbering with `\textbf{9.}`, and **do not** read p. 303's numeral
  as `5.` from its shape — it is the undecidable old-style 3/5 sort recorded above.
- **The same undecidable sort is a `5` in these pages' cross-references and a `3` in p. 303's
  article head.** p. 302 ("le cas du point double") and p. 303 ("point double non planaire") cite
  Part I's article on double points, which is `nº 5` (p. 290). Write `(nº 5)` there. **Do not**
  normalize it to the p. 296 `(nº 3)` on grounds of shape — the two are settled by subject matter,
  not by ink.
- **A superscripted French ordinal is literal Unicode: `Iʳᵉ Partie`** (p. 303), parallel to the `nº`
  ruling above. **Do not** write `I\textsuperscript{re}`, `I$^{re}$`, `Ire` or `1re`.
- **`\varphi'_{z}` is the derivative of the tangent-cone form and stays distinct from `f'_{z}`.**
  The p. 302 abelian-integral denominator is `\varphi'_{z}(1, y/x, z/x)`, attached to
  `\varphi(x, y, z) = 0`. **Do not** unify it to `f'_{z}`.
- **`\dfrac` requires nesting *and* full-size setting in the print — nesting alone is not enough.**
  The p. 302 abelian integral prints `y/x` and `z/x` at reduced size inside the big fraction, where
  LaTeX's own script reduction already matches the print, so those take plain `\frac`. This narrows
  the `\dfrac` entry at the top of this file; it does not repeal it.
- **A system printed under a tall left brace is one `aligned` with the brace dropped, and the
  `\tag` goes on its own line after `\end{aligned}`** (p. 304, display (2)). **Do not** use `cases`,
  `array`, or `\left\{ \right.`.
- **An integral with `x, y, z` above a bare sign is `\int^{x, y, z}` — unparenthesized — on p. 302**,
  unlike the parenthesized p. 300 form. **Do not** import the p. 300 parentheses, and do not supply
  a lower limit.
- **Ink loss that destroys part of a glyph or a delimiter is repaired, not reproduced (R29).**
  p. 302 prints `p − 2` twice with the opening parenthesis dropped; p. 304 prints `tormes` where the
  `f` lost its ascender and crossbar, four lines below a correctly set `formes`. These are failed
  ink, not the compositor's choices, and are transcribed whole. **Do not** confuse them with the
  R4 printer's errors recorded in `provenance.yaml`, which are reproduced.
- **p. 304 sets the three ratio differences inconsistently — `AB_{1} - A_{1}B` but
  `BC_{1} - CB_{1}` and `CA_{1} - AC_{1}` — in all four displays where they occur.** Confirmed under
  magnification. Reproduce as printed (R23); **do not** regularize the subscript order.

## Added after batch 7 (pp. 305–308)

- **Chapter II's article sequence continues `\textbf{4.}` (p. 306), `\textbf{5.}` (p. 308).** As
  above, settled by the sequence and by the text ("quatrième degré", then "cinquième degré"), not
  by the 3/5 sort. In-text back-references on pp. 307–308 (`nº 3 de ce Chapitre`, `nº 3`) point at
  article 3 (pp. 303–306), where `AB_{1} - A_{1}B = Qf'_{z} + Rf` was derived — so those are 3.
  **Do not** settle any of these numerals on glyph shape.
- **`AB_{1} - A_{1}B` is the work's form, but p. 308 display (2) prints `AB_{1} - BA_{1}`.**
  Verified magnified. Reproduce both as printed (R23); **do not** normalize either to the other.
- **Two consecutive centred display lines that are not a system take one `\[ \]` with `aligned`, a
  leading `&` on each line and no `\qquad`.** The `\qquad` in the run-on-equation rule above marks
  a *continuation* of one equation; these are two separate lines set one under the other (p. 308).
  **Do not** emit two `\[ \]`, **do not** use `gather`.
- **A pair of columns of definitions is one `aligned` with `& … &\quad`**, extending the
  side-by-side `\quad` ruling to a multi-row pair (p. 308's `A`/`A_{1}`, `B`/`B_{1}`, `C`/`C_{1}`).
  **Do not** split into two displays, **do not** use `array`.
- **The p. 306 double integral is `\int^{x} \int^{y}`: two bare upper limits, no parentheses, no
  lower limits.** A third distinct integral form in this work, alongside p. 296's fully-limited and
  p. 300's parenthesized ones. **Do not** parenthesize and **do not** supply lower limits.
- **`\theta` subscripts on p. 307 are settled by structure, never by shape.** This face's `1` is a
  dotless `ı` and its `4` degrades to a near-identical thin vertical, so `\theta_{1}` and
  `\theta_{4}` are indistinguishable in the final display. Read them off the four-term
  `\partial/\partial x, y, z, t` correspondence and the chain
  `\theta_{1} = \theta_{2} = \theta_{3} = \theta_{4} = 0`. Likewise `2m - 5` on p. 305 is settled by
  the degrees (`\deg f'_{z} = m-1`, `\deg Q = m-4`), not by the numeral.
- **A prime-height stroke beside a symbol is not automatically a prime.** p. 307's second
  `\theta_{4}` carries one; the work defines no `\theta'`, the same symbol three words earlier is
  plain, and this scan carries comparable stray specks on pp. 305 and 306. Write `\theta_{4}`.
  **Do not** write `\theta'_{4}`.
- **R29 ink-loss repairs continue to be made silently and reported, not reproduced:** p. 305's
  `F = Q\varphi + R\psi,` (the `=` survives as two broken dot pairs at `=` height) and p. 306's
  `d'ordre (m - 4)` (dropped opening parenthesis, as on p. 302). **Do not** transcribe a
  half-inked `=` as a dash or drop the delimiter.

## Added after batch 8 (pp. 309–312)

- **Chapter II's article sequence continues `\textbf{6.}` (p. 311).** As above.
- **From p. 309 the surface under discussion is of the fifth degree, and every old-style 3/5 in
  this stretch is a 5**: `-5\,\partial Q/\partial x`, `-5f(x, y, z)`, `-5C`, `f/z^{5}`, `Cz^{5}`,
  p. 311's `-\frac{1}{5}[\dots]`. They follow from Euler's relation on a degree-5 form and from
  `\partial(f/z^{5})/\partial z = (zf'_{z} - 5f)/z^{6}`. **Do not** read any of them as 3, and do
  not decide them on the glyph.
- **Numeric fractions are `\frac`, never `\tfrac`** — p. 312's `\frac{1}{4}` and the `\frac{1}{2}`
  throughout display (7), each confirmed by carrying (5) through the `z`-free term of
  `(BC_{1} - CB_{1})/z`. **Do not** write `\tfrac`, and **do not** read them as `\frac{1}{5}`.
- **p. 310 prints `\dfrac{\partial L_{1}}{dx}` — an italic `d` where its neighbours have
  `\partial` — and it is reproduced (R4), not repaired.** The R29 test comes out negative here:
  the glyph is a cleanly inked `d` with a straight ascender, sitting beside fully inked
  `\partial y`, `\partial z` and under a clean `\partial L_{1}`. A wrong sort, not lost ink.
  **Do not** normalize it to `\partial x`.
- **Tall vertical strokes with lost serifs are square brackets** (p. 311's `-\frac{1}{5}[\dots]`,
  p. 312's two inner groups). The cleanly set `[ ]` of display (6) settles the sort. **Do not**
  write `\vert`, `\left| \right|`, or parentheses.
- **`AB_{1} - BA_{1}` on p. 309 display (4) against `AB_{1} - A_{1}B` on p. 310** — a third site of
  the ordering inconsistency already recorded for pp. 304 and 308. Reproduce each as printed (R23);
  **do not** unify them.
- **The `TROISIÈME PARTIE.` heading on p. 312 resets the equation numbering to `\tag{1}`** and
  introduces the parametric symbol set `F`, `F_{1}`, `F_{2}` as uniform functions of `u`, `v`.
  Later `\tag{n}` in this part are the print's own restarted numerals. **Do not** continue the
  Chapter II sequence, and **do not** disambiguate a reused number by renumbering (see the
  pp. 285/286 precedent in `provenance.yaml`).

## Added after batch 9 (pp. 313–316)

- **An in-text article cross-reference is plain, even where the print sets its numeral in a heavier
  sort.** p. 316 sets `(nº 1, Chap. II)` with a slab `1`, plainly a different sort from this face's
  thin dotless `ı`. Weight in running text is typeface, not notation (HOUSESTYLE's
  notation-vs-presentation principle) — and pp. 296, 302 and 303 already set theirs plain. Write
  `(nº 1, Chap. II)`. **Do not** write `(nº \textbf{1}, …)`. This does **not** touch the
  `\textbf{n.}` at an article's *head*, which is structure and stays bold.
- **Part III's article sequence is `\textbf{2.}` (p. 314), `\textbf{3.}` (p. 316)** — p. 314's is a
  clean `2`, p. 316's is the undecidable sort settled by that sequence. **Do not** read p. 316's as
  `5.`, and **do not** continue Chapter II's count with `7.`
- **Part III's equation numbers run `\tag{1}`, `\tag{2}`, then the lettered `\tag{K}` for the
  conic** — all three set in the print's left margin, all three moved right. p. 315 back-references
  "l'équation (2)" and "l'équation (1)", confirming the restart. **Do not** write `\tag{(K)}`, and
  **do not** renumber to avoid the clash with p. 312's `(1)`.
- **p. 313's parametric display has only two lines, `dx` and `dy`.** `F_{2}` is introduced on
  p. 312 but never gets a `dz = \partial F_{2}/\partial u\,du + \dots` line here. **Do not** supply
  a third line to complete the pattern.
- **p. 313's `\varphi`/`\psi` expressions take plain `\frac`, including the `\partial x/\partial u`
  inside a numerator** — the print sets those inner derivatives at reduced size, so LaTeX's own
  script reduction already matches. An application of the batch-6 narrowing, not an exception.
- **`BA_{1} - AB_{1}` is p. 316's order** — a fourth site of the ordering inconsistency recorded for
  pp. 304, 308 and 309/310. Reproduce as printed (R23).
- **This face does print graves; a flat-looking accent is blur, not an acute.** p. 316's
  `c'est-à-dire` was magnified and the grave is genuinely there, so p. 313's blurred `espéce` and
  `troisiéme` are written `espèce` and `troisième`, with the rest of the work. **Do not** transcribe
  a blurred accent as an acute, and **do not** treat this as licence to normalize the genuine
  missing-accent cases already recorded (p. 288 `homogenes`, p. 306 `possedent`).

## Added after batch 10 (pp. 317–320)

- **An italic run broken by a page break is closed on the page where it begins and reopened on the
  next.** p. 319 ends `M. Bouquet (\emph{Bulletin des}` and p. 320 opens
  `\emph{Sciences mathématiques,} t. III)`. Each fragment stays brace-balanced and the rendered
  italics read continuously. **Do not** leave `\emph{` unclosed at a fragment's end, **do not** put
  `\origpage` inside `\emph{}`, and **do not** move the tail of a title back onto the earlier page —
  the hyphenated-word rule at the top of this file covers words, not spans.
- **`Chap. Iᵉʳ` is literal Unicode superscript** (p. 320), parallel to the `Iʳᵉ Partie` ruling —
  `er` because *premier*, not `re`. **Do not** write `I\textsuperscript{er}`, `I$^{er}$`, `Ier` or
  `1er`.
- **p. 317 cites `(nº 1, Part. II)` where p. 316 cites the same article as `(nº 1, Chap. II)`.**
  Verified magnified; the word on p. 317 is unmistakably `Part.` Reproduce each as printed (R23).
  **Do not** normalize either, and do not read this as evidence against the other.
- **Two adjacent `=` signs in a display whose fraction rule has itself broken into dashes are one
  `=` (R29).** p. 317's first display and p. 318's display (1) both show the doubling; magnified,
  the fraction bar in the same display has dropped to a dotted line, so the second "sign" is the
  bar. Write a single `=`. **Do not** transcribe `==` or `\equiv`.
- **`\dfrac` *is* right for the `\partial x/\partial u` factors inside the big `Q(\dots)/f'_{z}`
  fraction (p. 317 bottom, p. 318 middle) and for the inline `\partial x/\partial u` and
  `(y-b)/(x-a)`** — the print sets these full size, so the batch-6 condition (nesting **and**
  full-size setting) is genuinely met here, unlike p. 302's reduced-size `y/x`.
- **Part III's article sequence continues `\textbf{4.}` (p. 318), `\textbf{5.}` (p. 319);** the
  three ratio numerators on p. 318 display (2) are `BA_{1} - AB_{1}`, `BC_{1} - CB_{1}`,
  `CA_{1} - AC_{1}`, a fifth site of the ordering inconsistency. Reproduce as printed (R23).
- **A capital `Γ` in this face is distinguishable from `I'` only under magnification** — stem plus
  a right-running top arm. The curves complementary to the intersection are `\Gamma` from p. 320
  on. **Do not** write `I'`.

## Added after batch 11 (pp. 321–324)

- **Part III's numbered displays switch from Arabic to Roman: `\tag{I}` (p. 323), `\tag{II}`
  (p. 324)**, after `(1)`, `(2)` and the lettered `(K)`. p. 324 back-references "les équations (I)"
  and "les équations (II)", confirming it. **Do not** write `\tag{1}`/`\tag{2}`, **do not** write
  `\tag{(I)}`, and **do not** renumber to avoid the clash with p. 312's `(1)`.
- **Part III's Greek coefficients are `\alpha`, `\beta`, `\alpha_{1}`, `\beta_{1}`, and its two
  holomorphic functions are `\lambda`, `\lambda_{1}`** (pp. 323–324). This face's alpha degrades to
  something resembling an italic `z` at prepared resolution; magnified it is unmistakably alpha, and
  p. 324's own list fixes the set. **Do not** transcribe any of them as `z`, `z_{1}` or `\varkappa`.
- **The p. 323 series brackets are square outside, round inside:**
  `[\beta + P(x - x_{0}, y - y_{0})]\,dx`, as on p. 300. **Do not** substitute `\left( \right)` for
  the outer pair.
- **Part III's article sequence continues `\textbf{6.}` and `\textbf{7.}`, both on p. 321.** Two
  articles on one page; both numerals are clean sorts.
- **`BA_{1} - AB_{1}` (p. 323 mid) against `AB_{1} - A_{1}B` (p. 321 and p. 323 bottom)** — sixth and
  seventh sites of the ordering inconsistency. Reproduce each as printed (R23).

## Added after batch 12 (pp. 325–328)

- **Part III's article sequence continues `\textbf{8.}` (p. 326) and `\textbf{9.}` (p. 328)** — both
  clean sorts, both confirmed by the run 1–7.
- **A partial derivative evaluated at the point is `\left( \frac{\partial B_{1}}{\partial x}
  \right)_{0}`** — big parentheses, braced `0` subscript on the closing paren. **Do not** write
  `\partial B_{1}/\partial x |_{0}`, `\left[ \right]_{0}`, or drop the subscript.
- **An `f'` derivative evaluated at the point carries a nested subscript: `f'_{z_{0}}`,
  `f'_{x_{0}}`, `f'_{y_{0}}`** — prime first, then the braced `z_{0}`, extending the `f'_{z}` rule.
  **Do not** write `f'_{z0}`, `f_{z_{0}}'` or `(f'_{z})_{0}`.
- **This signature drops `0` subscripts, and those omissions are reproduced (R4), not repaired.**
  p. 326's third denominator prints `f'_{z}` where its partners print `f'_{x_{0}}` and `f'_{y_{0}}`;
  p. 327's `Écrivons donc` display prints `p(y - y)^{2}` and `3\beta(x - x_{0})^{2}(y - y)`. In each
  case the sort is absent rather than broken, and neighbouring `y_{0}` on the same lines are cleanly
  set. **Do not** supply the missing `0` from the parallel — that is the R4/R29 line.
- **p. 328's integrals take two-variable limits, `\int_{x_{0}, y_{0}}^{x, y}`**, against p. 327's
  three-variable `\int_{x_{0}, y_{0}, z_{0}}^{x, y, z}` for the same two integrals. Verified
  magnified; a fourth distinct integral form in this work. **Do not** import the `z`, and **do not**
  parenthesize.
- **Two integral equations set one under the other are one `\[ \]` with `aligned` on `&=`**
  (p. 327 top, p. 328 middle) — a system, so the `&=` ruling applies rather than the leading-`&`
  one used for a run-on equation. **Do not** emit two displays.
- **`\dfrac` only where the two-part condition holds, again:** the inner
  `\partial B_{1}/\partial x` inside p. 326's three-way fraction chain takes `\dfrac`; the visually
  identical expression at top level on p. 325 and in p. 326's bracket displays takes `\frac`.
- **p. 328 prints `A une valeur de $t$` — an unaccented capital A for `À`.** Kept as printed
  (R12/R23). **Do not** write `À`.

## Added after batch 13 (pp. 329–332)

- **Every display is written over three lines** — `\[` alone, the body, `\]` alone. The whole work is
  set that way. **Do not** compress a short display onto one line.
- **Part III's article sequence continues `\textbf{10.}` (p. 331) and `\textbf{11.}` (p. 332).**
- **Part III restarts its equation numbering a second time on p. 330: `\tag{1}`, `\tag{2}` (p. 330),
  `\tag{3}`, `\tag{4}` (p. 331)** — after the same Part's earlier `(1)`, `(2)`, `(K)`, `(I)`,
  `(II)`. p. 331 back-references "les équations (1) et (2)" and "l'équation (3)"/"l'équation (4)"
  inside the restarted run. **Do not** renumber to avoid the clash, and **do not** read (3)/(4) as
  continuing (II).
- **Two *numbered* consecutive display lines are two separate `\[ \]`, each with its own `\tag`**
  (p. 331's (3) and (4)). The batch-8 "two centred lines → one `aligned`" ruling covers unnumbered
  lines only, since `aligned` cannot carry a per-line `\tag`. **Do not** merge them, **do not** use
  `gather`.
- **The p. 329 integrals are `\int_{0, 0, 0}^{x, y, z}`** — three literal zeros, no parentheses. A
  fifth distinct integral form in this work. **Do not** substitute `x_{0}, y_{0}, z_{0}` and **do
  not** parenthesize.
- **The tangent-plane fraction's denominator is `2P` throughout** (`\frac{c'x - cy - \lambda Pz}{2P}`,
  pp. 329–330). p. 329's numeral is a degraded sort readable as `3`; p. 330 sets the identical
  expression twice with a clean `2`. **Do not** write `3P`.
- **A leading serif blob on this face's italic `x` and `y` is the glyph, not a comma.** pp. 329–330
  print what looks like `c' .x — c ,y`; magnified it is `c'x - cy`. **Do not** transcribe those
  blobs as punctuation.
- **`f'_{z}(1, Y, Z, T)` on p. 331 against bare `f'_{z}` on p. 332 for the same two quotients** —
  reproduce each as printed (R23). **Do not** supply the argument list on p. 332 or strip it on
  p. 331. Likewise p. 331 writes `Chapitre Iᵉʳ` in full where p. 320 abbreviates `Chap. Iᵉʳ`.
- **The three inline running-text fractions on p. 329 take `\dfrac`, including the one inside
  `\left( \right)^{2}`** — `$\dfrac{y}{x}$`, `$M + N\left( \dfrac{y}{x} \right)^{2}$`. This is the
  batch-4 inline rule (the print sets them full size and opens the leading), not the display-nesting
  condition. **Do not** write `\frac` or `y/x`.

## Added after batch 14 (pp. 333–336)

- **Part III's article sequence continues `\textbf{12.}` (p. 335) and `\textbf{13.}` (p. 336);** its
  second restarted equation run continues `\tag{1}` on p. 333 (settled by that page's own
  back-reference "à cause de la relation (1)" — the margin numeral has lost both parentheses and
  survives as a bare bar plus a speck), and p. 336 carries the lettered `\tag{C}`, as p. 314 carries
  `\tag{K}`. In-text `la relation (C)` and `la courbe (C)` are copied as printed. **Do not** write
  `\tag{(C)}`.
- **A plural article cross-reference is literal Unicode `nᵒˢ`** (p. 336, `Chap. II, nᵒˢ 4, 5, 6`),
  parallel to the singular `nº` ruling and to `Iʳᵉ`/`Iᵉʳ`. **Do not** write `n^{os}`, `nos`,
  `n\textsuperscript{os}`, or the singular `nº` for a plural.
- **A sixth distinct integral form: p. 336's two integrals are bare `\int` with no limits at all**,
  against the fully-limited `\int_{x_{0}, y_{0}, z_{0}}^{x, y, z}` of pp. 333–335. **Do not** supply
  limits from the neighbouring pages.
- **p. 334 prints a full stop mid-sentence — `va correspondre. au moyen des équations précédentes` —
  and it is reproduced (R4).** The R29 test is negative: the mark is a clean square period at
  baseline, and the comma four words earlier carries a fully inked tail under magnification. A wrong
  sort, not lost ink. **Do not** write a comma. By contrast p. 334's `constan'e` *is* R29 ink loss
  (the `t` lost its crossbar and stem top), repaired to `constante` as p. 304's `tormes` was.
- **Do not nest `\uncertain{}` inside `\emph{}`** — the brace interaction is exactly what R25/R18
  warn about. Where a doubtful reading falls inside an italic run, settle it from the mathematics
  and record the doubt in the batch report instead.
- **A doubled or broken-looking `=` with no fraction rule nearby is a single over-inked `=`**
  (pp. 334–335, `f(x, y, z) == 0`, the `= du` line). The batch-10 doubling rule attributes the second
  sign to a collapsed fraction bar; where there is no bar, the cause is just the sort. Write one `=`.

## Added after batch 15 (pp. 337–340)

- **The memoir's divisions are `PREMIÈRE PARTIE.` (p. 283), `CHAPITRE II.` (p. 299),
  `TROISIÈME PARTIE.` (p. 312), `QUATRIÈME PARTIE.` (p. 338).** The print names the same kind of
  division two ways and never sets `CHAPITRE I.` or `DEUXIÈME PARTIE`; the running text refers to
  both as "Chapitre". Set each heading exactly as printed with `\section*{}` and the trailing
  period. **Do not** supply the missing headings, **do not** regularize `CHAPITRE II.` to
  `DEUXIÈME PARTIE.`, and **do not** renumber.
- **Each new part restarts the article count and the equation count, and Part III restarts its
  equation count three times over.** Part IV: `\textbf{1.}` and `\tag{1}` (p. 338), `\tag{2}`
  (p. 339), `\tag{3}` (p. 340). Part III's third restart is `\tag{1}`, `\tag{2}` on p. 337. Every
  one is confirmed by the page's own back-references. **Do not** renumber to avoid a clash — the
  pp. 285/286 precedent in `provenance.yaml` governs.
- **`zt^{\frac{1}{2}}` on p. 337 carries a genuine fractional exponent.** The stacked numerals above
  the `t` are a half, confirmed by homogenizing `z = \sqrt{ax^{3} + \dots}`. `\frac`, not `\dfrac`,
  since it already sits in a script. **Do not** write `zt^{2}`, `zt^{1}` or `z t \frac{1}{2}`.
- **A row of omission dots inside a display system is `\ldots` on both sides of the `&`** (p. 340).
  The work uses `\ldots` throughout. **Do not** use `\dots`, `\cdots`, `\dotfill`, `\hdotsfor`, or a
  separate display.
- **A comma-separated list of point pairs in a display is joined by `\quad`** —
  `(x_{1}, y_{1}), \quad (x_{2}, y_{2}), \quad \ldots, \quad (x_{m}, y_{m})` (pp. 339–340),
  extending the side-by-side rule to a list. **Do not** use `\;`, `\qquad`, or bare spaces.
- **Small caps inside an italic run collapse into the surrounding `\emph{}` as plain words (R24).**
  Part IV's theorem statement sets `ARBITRAIRE` and `UN SEUL` in small caps inside its italic.
  **Do not** write `\textsc{}`, `\textbf{}` or capitals, and **do not** nest a macro inside the
  `\emph{}`.
- **`A un point arbitraire` keeps its unaccented capital A** on p. 337 and in p. 339's italic
  statement, as on p. 328. **Never** write `À`.

## Added after batch 16 (pp. 341–344)

- **Part IV restarts its equation numbering again at each new article: `\tag{1}` on p. 343
  (article 2) and `\tag{1}` again on p. 344 (article 3)**, after the p. 338–340 run (1)–(3).
  p. 344's own back-reference "les équations aux différentielles totales (1)" points at the p. 343
  system. **Do not** continue as `(4)`/`(5)`, and **do not** renumber p. 344 to `(2)`.
- **Part IV's article sequence is `\textbf{1.}` (p. 338), `\textbf{2.}` (p. 343), `\textbf{3.}`
  (p. 344);** p. 344's numeral is the undecidable sort, settled by the sequence. The same page's
  cross-reference `(nº 3, Chap. III)` is the same sort at the same weight and is likewise 3 — Part
  III's article 3 (pp. 316–317) is where the adjoint `Q(\dots)/f'_{z}` appears. `Chap. III` is
  certain under magnification. **Do not** write `nº 5` or normalize to `Chap. II`.
- **The derivative with respect to `w` is `f'_{w}`** (pp. 343–344) — the `f'_{z}` rule carried into
  the `(u, v, w)` system. **Do not** write it unbraced or as `f''_{w}`.
- **A seventh integral form: p. 341's `\int^{u, v, w}` (bare upper limit, unparenthesized, no lower
  limit) sits beside p. 343's completely bare `\int`.** Reproduce each as printed; **do not** import
  limits from a neighbouring page.
- **p. 341 prints `entiere` without its grave** ("une fonction entiere et du premier degré"),
  verified magnified — with `homogenes` (p. 288) and `possedent` (p. 306). **Never** write
  `entière`.

## Added after batch 17 (pp. 345–346)

- **Part IV article 3's equation run continues `\tag{2}`, `\tag{3}`, `\tag{4}` (p. 345) and
  `\tag{5}` (p. 346)**, after the `\tag{1}` opening the article on p. 344; the pages' own
  back-references ("Les équations (2) et (3)", "les deux expressions (4) et (5)") confirm each one.
- **The derivatives of `f` in this article are `f'_{u}`, `f'_{v}`, `f'_{w}`** — single prime, braced
  subscript. p. 345's `f'_{u}` merges its prime into the `f` descender, as on pp. 294–296; magnified
  it is a single prime. **Do not** write `f''_{u}` or a bare `f_{u}`. In this face small `u`, `v`
  and `w` subscripts are near-identical; settle them by the derivation, not the ink.
- **p. 345 prints `a f'_{w} f'_{v}` in the `dx` numerator but `a f'_{v} f'_{w}` in display (4), for
  the same quantity.** Both verified magnified. An eighth site of this print's factor-ordering
  inconsistency, after the `AB_{1}`/`BA_{1}` family. Reproduce each as printed (R23); **do not**
  unify them.
- **`\partial x\,\partial y` carries a thin space in a mixed second-derivative denominator**,
  matching the differentials rule at the top of this file. **Do not** write `\partial x \partial y`
  or `\partial x\partial y`.
- **The memoir ends on p. 346 with "…comme au numéro précédent."** There is no concluding heading,
  no `TABLE DES MATIÈRES`, no place-and-date line and no signature; below the last paragraph sits
  only a centred printer's ornament (a short swelled rule), which is furniture and is not
  transcribed. **Do not** supply an end-of-memoir apparatus for this work.

## Corrections and confirmations from the second verification pass (pp. 301–346)

- **The print sets the "première partie" ordinal two ways, and both are reproduced.** pp. 303 and
  307 set a genuine **capital `I`** — a full cap-height stem with a wide slab serif extending
  symmetrically to *both* sides at top and foot, matching the adjacent `P` in height. pp. 329 and
  331 set the **old-style figure one** — a short stroke with an angled top-left flag and a single
  wide base serif — and p. 331 proves the contrast on its own page, setting `1ʳᵉ Partie` against a
  true capital in `Chapitre Iᵉʳ`. So: `Iʳᵉ Partie` on pp. 303, 307; `1ʳᵉ Partie` on pp. 329, 331.
  **Do not** normalize them to each other — this is another site of the sort inconsistency that
  runs through the `AB_{1}`/`BA_{1}` family (R23).
- **A display-terminal colon is a bare `:` inside the math, with no `~`.** p. 307's `\theta_{4}`
  display ends in one. The `~:` rule at the top of this file is **text-mode only**: in math mode
  TeX already sets `:` as a relation and supplies the space before it, so a `~` would double it.
  In running text the rule is unchanged — p. 338's `…de $x$ et $y$~: je me propose` takes the `~`.
  **Do not** write `\right)~:`, and **do not** drop the `~` from a colon in prose.
- **Telling this face's `;` from `:` is a measurement, not an impression.** Compare the *lower*
  element's height to the upper dot's: a semicolon's comma runs about twice the upper dot's height
  and tapers down-left (p. 307's `Af'_{x} + Bf'_{y} + Cf'_{z} = 0;`, p. 305's
  `f'_{z}(x, y, z) = 0;`); a colon's two elements match within a few percent and neither tapers
  (p. 307's `\theta_{4}` display, p. 338's prose mark). A comma that lost its tail keeps its
  *head*, which is markedly wider than a colon's dot — so a small round pair is a colon, not damage.
- **To judge an accent, first prove the crop can resolve accents at all.** A magnified crop of
  p. 313 lost *every* diacritic on its line including a certain acute, so a crop showing no accent
  is not evidence of absence. Name a known-accented word on the same line as the control, and only
  then give a verdict. Under that test p. 303 yields two more genuine missing accents —
  `de première espece` and `possede` — joining `homogenes` (p. 288), `possedent` (p. 306) and
  `entiere` (p. 341). **Never** "correct" any of them.
- **p. 311's primed triple ends `a'_{2}, b'_{2}, c_{2}`** — the third prime is absent, with clean
  white paper above the `c` while the two primes beside it are solidly inked. R4, like the dropped
  `0` subscripts on pp. 326–327. **Do not** supply it from the pattern.
- **A period set mid-sentence where the sense wants a comma is this compositor's recurring slip,
  and it is reproduced**: p. 326's `n\alpha - p\beta = 0.`, p. 334's `va correspondre.`, p. 339's
  `bien entendu.`, p. 336's display-terminal stop. In each the mark is a clean tailless baseline
  dot beside a fully tailed comma on the same line, so the R29 test is negative. **Do not**
  regularize them.
- **Part III carries no article `1.`** The margin beside its opening paragraph on p. 312 is blank
  paper and its first printed numeral is `2.` on p. 314 — verified against the scan, not inferred
  from the sequence. **Do not** supply a `\textbf{1.}` to match the other three divisions.
- **A blank line after `\]` starts a new indented paragraph, so there must be none where the
  sentence continues** — that is, where the next line opens with a lowercase letter or with inline
  math. This was repaired at 39 sites work-wide. It is decided by the text, not the scan: a
  sentence cannot continue in a new paragraph.
- **The inline-`\dfrac` rule needs the print to open the line leading, and p. 345's inline pair
  does not.** `$\frac{\partial^{2} u}{\partial x^{2}}$` and
  `$\frac{\partial^{2} u}{\partial x\,\partial y}$` are set at reduced size there, in a measure
  matching the page's ordinary leading, so they take plain `\frac`. The batch-4 entry's warrant was
  always the opened leading; this records the case where it is absent.
- **A blank slot wider than a word space is a failed sort, not an absent one.** p. 318's equation
  (1) prints 49px of clean paper between the `=` and the `1/a` where p. 319's identical
  construction fits a 21px minus rule with ~14px either side; a sort never set would have closed
  the gap to a single word space. The minus is restored (R29) and the algebra agrees. Use the
  *reserved width*, not the presence of ink, to run the absent-vs-damaged test on a vanished
  operator. **Do not** read a wide blank as the author omitting a sign.
- **p. 320 prints `(Chap. Iᵉʳ. nº 2)` with a period where the sense wants a comma** — the mark's
  box bottoms out 3–5px below the baseline where this face's comma descends 15–16px, so the tail
  was never set. R4, reproduce. p. 319 likewise prints a bare `(Chap. I, nº 5)` with no `ᵉʳ`, the
  ~13px that superscript occupies on p. 320 being empty. **Do not** regularize either.
- **Superscripted ordinals stay literal Unicode, and the shared preamble now makes that safe.**
  `corpus/preamble/readmasters.sty` maps `ʳ ᵉ ᵒ ˢ ⁿ ᵐ` to `\textsuperscript`, because XeTeX has no
  glyph for them and was dropping them from the PDF without an error. **Do not** switch these to
  `\textsuperscript{}` in the transcription, and **do not** remove the mappings.
