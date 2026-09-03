# Notation decisions — Clebsch 1868, *Sur les surfaces algébriques* (Comptes rendus 67)

Work-spanning rendering decisions for this transcription. The note is two printed pages and was
transcribed in one pass, so these entries exist for the reviewer and for anyone who later
re-transcribes, translates, or extends the work — not to reconcile separate batches.

**This work does not inherit `clebsch-1864-anwendung-abelschen-functionen/notation.md`.** Same
author, different edition and different compositor, and the two prints disagree on at least one
recurring convention (the multiplication dot). Where an entry below contradicts the 1864 file, the
1868 print governs this file only.

## Symbols

- **The zero is the digit `0`, not the letter `o` — and the scan cannot settle that by shape.**
  The Comptes rendus sets oldstyle figures, in which the zero and the lowercase roman `o` are the
  same sort: magnified to any degree, the character in `f = o` is identical in shape and width to
  the `o` of "l'ordre" in the same line. The reading rests on the mathematics — these are the
  equations of two surfaces, and `p = 0` is a genus — not on the glyph. Write `$f = 0$`,
  `$\varphi = 0$`, `$p = 0$` — never `f = o`. Do not revert it to a letter on the strength of the
  glyph, and do not record that magnification decided it: an earlier draft of this entry claimed
  it did, and a verification pass was right to reject that.
- **Phi is `\varphi`, never `\phi`.** The print's glyph is the closed single-storey phi: a small
  oval bowl with a short descender and no ascender above it. Verified magnified on p. 1239.
- **The multiplication dot is a period set SPACED, written `\,.\,`** — a thin space on each side:
  `\dfrac{(n-1)(n-2)(n-3)}{1 \,.\, 2 \,.\, 3}` (p. 1239). Never a tight `1.2.3`, never `\cdot`,
  never `\times`, never juxtaposition. Magnified, each period carries a clear gap of roughly a thin
  space on both sides. **This is the opposite of the 1864 Crelle memoir**, whose 63 dots are all
  tight and whose glossary forbids `\,.\,` outright; do not carry that rule across. It occurs once
  in this note, in the denominator above, and the matching numerator sets its factors by bare
  juxtaposition with no dots at all — reproduce that asymmetry.
- **Inline fractions the print sets at full display size are `\dfrac`, never `\frac`.** All three
  fractions in the note — $\dfrac{(n-1)(n-2)}{2}$, $\dfrac{p(p-3)}{2}$ and
  $\dfrac{(n-1)(n-2)(n-3)}{1 \,.\, 2 \,.\, 3}$ — run inline inside a sentence, at the same size as
  a displayed fraction, with the line spacing visibly opening to take them. None of them is
  promoted to its own display: the print sets no display formula anywhere in the note, so
  `original.tex` contains no `\[ ... \]` and no `\tag`.
- **The minus sign is `-` in math mode.** The print's minus is a long dash of the same length as
  its em-dash, which is a sort choice, not notation: `$n - 4$`, `$k - 4$`, `$p + 1$`.

## Typography

- **Guillemets are literal Unicode `«` and `»`, set tight against the quoted text** — `«Soient`,
  `donnée.»` — never `` `` … '' ``, never `\og`/`\fg`, and never with a space or `~` inside the
  marks. This follows `abel-1841-fonctions-transcendantes`, the corpus's other French work
  (HOUSESTYLE R18, R22). **The print does set the French space inside every mark** ("« Les",
  "donnée. »"); that spacing is presentation and is normalized away, in all eight marks alike. It
  is not an omission to be repaired.
- **Two different repetitions of the quotation mark, handled two different ways.** The print marks
  quotation at two scales and only one of them is a line-break artifact:
  - *Per printed LINE*, inside each of the two quoted theorem statements, a `»` heads every
    typeset line. That is the artifact R22 governs, and it collapses to a single `«…»` pair around
    the whole statement.
  - *Per PARAGRAPH*, across the note as a whole, a single `«` opens the first paragraph and a `»`
    heads each following paragraph. That is the Comptes rendus convention for a communication
    quoted continuously across paragraphs, not a line-break artifact, and it is **kept exactly as
    printed** — one mark at the head of each of the four outer paragraphs. Do not collapse these,
    and do not add a closing `»` to the note: the print never closes the outer quotation, and the
    final `»` on p. 1239 belongs to the second theorem statement.
- **A LaTeX control space follows an abbreviation dot: `M.\ Riemann`, `M.\ Cayley`, `M.\ Chasles`,
  `M.\ Cremona`, `M.\ A.\ Clebsch`** (HOUSESTYLE R17) — not `~`, and not a bare space, which TeX
  would set as an inter-sentence space. (`abel-1841-fonctions-transcendantes` writes a bare
  `M. Legendre`; it predates the R17 normalization and is not the model here.)
- **No space before `:` and `;`.** The print sets the French thin space before high punctuation
  ("le théorème suivant :"). Spacing is presentation, not notation, and the corpus's other French
  work sets none, so it is normalized away. Never write ` :` and never `~:`.
- **Small capitals and italics both collapse to `\emph`, and a name set in small caps inside an
  italic run does not split it** (R20, R24). The print sets `(Voir` CLEBSCH `und` GORDAN,
  `Theorie der Abelschen Functionen.)` with the two author names in small caps and everything else
  in italic; that is written as one run,
  `(\emph{Voir Clebsch und Gordan, Theorie der Abelschen Functionen}.)`, with the closing period
  and parenthesis outside the run. The parentheses are plainly roman. The period is not decidable
  at any magnification — a period has no italic form to read — and sits outside the run because
  that is where the parenthesis puts it, not because the scan settles it.
- **`coefficients` is set with separate `o` and `e`, not the `œ` ligature.** Verified magnified on
  p. 1239 — the bowl of the `o` closes before the `e` begins. The word is not `cœfficients`, a
  spelling the period does sometimes use.
- **Edition orthography is kept** (R12): `A ce genre appartiennent` with an unaccented capital `A`,
  as printed. Do not modernize to `À`.

## Structure

- **The printed heading is transcribed as one `\section*`**, in the print's own order and without
  emphasis (R25): `\section*{Géométrie. --- Sur les surfaces algébriques. Note de M.\ A.\ Clebsch,
  présentée par M.\ Chasles.}`. The Comptes rendus sets subject rubric, title and byline as a
  single centred heading block broken over two lines, not as a title line with a separate byline
  beneath it, so it is not split the way `abel-1841-fonctions-transcendantes` splits its title from
  its `Par M. N. H. Abel` line. The small-capital rubric `GÉOMÉTRIE` is normalized to
  `Géométrie` — case is a typeface shape.
- **The note begins partway down p. 1238**, under unrelated Academy business. `\origpage{1238}`
  therefore sits at the section heading, and nothing above it on that page is transcribed —
  including the footnote `(1)` at the foot of p. 1238, which belongs to the Zantedeschi item and
  not to Clebsch. The signature mark `163` at the foot of p. 1239 is page furniture and is not
  transcribed either.
- **p. 1239 opens mid-sentence** ("il y a des" / "théorèmes tout à fait analogues"), with no
  hyphenation at the break. Its `\origpage{1239}` therefore takes **no blank line after it** — a
  blank line there is a `\par` inside a sentence.

## Printer's errors reproduced (R4)

Both are reproduced exactly as printed, and neither is corrected in the transcription.

- **p. 1239, `de la surface de l'ordre $n = 4$ étant arbitraires`** — an equals sign where the
  sense requires the minus of "l'ordre $n - 4$", which the very next sentence sets correctly.
  Magnified: two clean parallel rules of equal length, unmistakably `=` and not a broken or
  doubly-inked dash.
- **p. 1239, the first theorem gives $f = 0$ the order $m$ and $\varphi = 0$ the order $n$**, then
  measures the adjoint of $f = 0$ as a surface "de l'ordre $n - 4$", where its own lettering calls
  for $m - 4$. Both readings verified magnified; the statement is transcribed as it stands.
