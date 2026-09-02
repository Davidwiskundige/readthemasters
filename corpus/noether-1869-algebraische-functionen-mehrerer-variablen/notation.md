# Notation decisions — Noether 1869, *Zur Theorie der algebraischen Functionen mehrerer complexer Variablen*

Work-spanning rendering decisions for this transcription, so that pages transcribed in separate
batches stay consistent with each other. Each entry is the decision plus why it was made, and names
the alternatives that are **not** to be used. The whole paper, pp. 298–306, follows this list.

## Symbols

- **Zero is the letter `o`, not the digit `0`.** Write `$f = o$`, `$h = o$`, `$\theta = o$`,
  `$\varphi = o$`. The print sets a lowercase roman *o* in every equation on pp. 298–301, and the
  author's equations-of-a-variety notation depends on it. Never normalize to `0`.
- **`\infty` with a superscript, never `\propto`.** The dimension of a manifold is written
  `$\infty^{2h}$`, `$\infty^{2r}$`, `$\infty^{2(r-1)}$`, `$\infty^{2.3}$`. The scan's lemniscate is
  open on the left and is easily misread as `∝`; it is an infinity sign. The exponent is always a
  superscript, never a subscript.
- **The multiplication sign is a period on the baseline**, set as a plain `.` — never `\cdot`,
  never `\times`. **Its spacing is part of the rule, and depends on where it sits:**
  - **In ordinary math, spaced with `\;`**: `$\frac{n-1.\; n-2}{1.\; 2.}$`, `$2.\;3$ Dimensionen`,
    `$\varphi_i(\mu,\nu).\; \lambda^{r}$`. The print leaves a clear space there.
  - **Inside a superscript, tight**: `$\infty^{2.3}$`, `$\infty^{2.2}$`, `$\infty^{2.1}$`, where a
    `\;` would be far too wide for the reduced size.

  *A literal space is not spacing.* Writing `\varphi_i(\mu,\nu). \lambda^{r}` renders tight, because
  TeX ignores ordinary spaces in math — it must be `\;`. This entry originally gave only examples
  and never stated the rule, and the very next batch duly set a tight dot in ordinary math, caught
  by the verification pass. That is the failure mode HOUSESTYLE R27 warns about: a vague entry does
  not merely fail to help, it licenses a fresh divergence while looking like guidance.
- **Ellipses in an argument list are `\ldots`** — `$x_2, \ldots x_r$`, `$i = 1, 2, \ldots 5$`.
  Never literal spaced dots, never `\dots`, never `\cdots`. The print's dot count varies between
  three and four and carries no meaning.
- **Greek is `\varphi` (not `\phi`) and `\varrho` (not `\rho`).** This print uses the looped italic
  phi throughout.
- **No Fraktur mathematical variables occur in this work.** Nothing is `\mathfrak{}`. The prose is
  Antiqua, so no blackletter normalization arises either. Recorded so a later batch does not
  introduce one.
- **`p'` is a distinct variable from `p`** — the *Curvengeschlecht* beside the *Flächengeschlecht*.
  Write `$p'$`; never `$p_1$`, never `$\bar p$`, and never conflate the two. Confirmed by
  magnification on p. 303.
- **Capital Phi is `\Phi`**, distinct from the `\varphi` used throughout: never `\varPhi`, never
  `\phi`. The second coordinate system on p. 305 is `\xi` — never `\zeta`.
- **`\psi(\mu,\nu) = 0` on p. 302 sets a DIGIT zero**, against the letter `o` this work uses for
  zero everywhere else. Magnification shows a tall full-height 0 beside the small round `o` of
  `$p = o$` on the same page. Both are transcribed as printed: do not regularize the `0` to `o`,
  and do not regularize the surrounding `o`s to `0`.
- **A prime on `F`.** The display on p. 301 sets `F'` where the object is plain `F` everywhere else
  in the paper — three times in the sentence directly below it, and at every occurrence on
  pp. 302–303. Two batches examined it independently; the glyph is cleanly inked at cap height, not
  a speck. It is reproduced as printed under R4 (a printer's error is kept and flagged, never
  silently fixed) and recorded in `provenance.yaml`. **Do not write `F'` anywhere else.**

## Typography

- **No `ß` anywhere.** This is an Antiqua print setting round *s* throughout: `dass`, `muss`,
  `lässt`, `ausser`, `Grössen`, `Schliesslich`. HOUSESTYLE R19's `ſs → ß` mapping has nothing to
  convert here, and that is faithful, not an oversight. Never "correct" these forms.
- **Ordinal suffixes are superscripted on the math**: `$n^{\text{ter}}$ Ordnung`,
  `$n^{\text{ten}}$ Grades`, `$(n-4)^{\text{ter}}$ Ordnung`. Never `n-ter`, never a baseline
  `$n$ter`. The print sets the suffix raised after a bare letter and on the baseline after a closing
  parenthesis; that inconsistency is presentation and is normalized to the raised form.
- **A Greek letter glued to a German word is a math span followed by plain text**: `$\mu$fach`,
  `$\mu$fache`, `$\mu$fachen`. Never `\mu\text{fach}`, never a hyphen. The same holds for a
  coefficient: `$2r$ fach`, `$2h$ fach`, never `$2r\text{fach}$`.
- **German quotation marks are literal Unicode `„ … “`** — never `"`, never `\glqq`. Where the print
  repeats `„` at the head of every line of a block quotation, that is a line-break artifact and is
  dropped to a single opening/closing pair (R22). A `„` standing in the **middle** of a line is a
  ditto mark and is kept.
- **Letterspaced runs become `\emph{...}`** (R20): `\emph{einer}`, `\emph{Geschlecht}`,
  `\emph{Theorem 1:}`. A theorem label is **one** `\emph` run including its number and punctuation —
  never split into `\emph{Theorem} 2.:`.
- **Author names are NOT letterspaced in this print and take no `\emph`**: `Riemann`,
  `Herr Clebsch`, `Clebsch und Gordan`. Verified by magnification on p. 298. This differs from
  other corpus works, where names often are letterspaced — do not add emphasis here by analogy.
- **Abbreviation dots take a LaTeX control space** (R17): `Bd.\ 54.`, `21.\ Dec.\ 1868`, `p.\ 1238`.
  An ordinal numeral with a period takes one too: `5.\ Ordnung`, `30.\ Juni 1869`, `§.\ 18.`.
- **An apostrophe in a name is the plain ASCII `'`**: `Abel'sche`, `Crelle's` — never `’`, never
  `\textquoteright`.
- **The closing dateline is `\emph{Göttingen}, den 30.\ Juni 1869.`** — the print letterspaces only
  the place name, so only that is `\emph`'d, not the whole line.

## Structure

- **Section headings are a bare roman numeral with a period**: `\section*{I.}`, `\section*{II.}`.
  Do not add a word ("Abschnitt", "§"), and do not demote them to `\subsection*`.
- **Footnotes are numbered with a single closing parenthesis**: the in-text mark is `${}^{1)}$` and
  the note is led by `\textbf{1)}`, placed inline as a complete unit at the end of that page's main
  text (R15). Never `\footnote`, never `${}^{(1)}$`.
  *A footnote block always ends its page fragment with a blank line before it*, so that assembling
  the fragments does not glue the note onto the sentence continuing from the previous page. This is
  the one case where a page opening mid-sentence still needs a paragraph break above the note.
- **Function application is set tight**: `$f(s, x_1, \ldots x_r)$`, even though the print leaves a
  space before the parenthesis. Spacing there is presentation.
- **A braced system of equations is `\begin{aligned} … \end{aligned}` carrying a single `\tag{n}`.**
  The print's right-hand curly brace grouping the lines is presentation and is dropped — the tag
  carries the grouping. Never `\left. … \right\}`, never one `\tag` per line, never `cases`.
- **A compound exponent the print sets on the baseline is still an exponent**: p. 302 prints
  `λ r−1` level with the λ where the preceding term raises `λ^r`. Write `\lambda^{r-1}`, never a
  baseline `\lambda r-1`.
- **Words hyphenated across a page break** are written whole on the page where the word *begins*;
  the next fragment starts at the following word. Never leave a trailing hyphen. A *formula* split
  across a page break is split at the boundary as printed, with each fragment separately balanced
  (`$(\mu - r$` on p. 300, `$+ 1)$` on p. 301), so both fragments are valid on their own.
- **Running heads, printed page numbers and signature marks** are page furniture and are not
  transcribed.
