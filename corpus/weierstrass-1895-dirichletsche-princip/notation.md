# Notation decisions — Weierstrass 1895, *Über das sogenannte Dirichlet’sche Princip*

Cross-page rendering decisions for this work. Batches cannot see each other; this file is how they
agree. Each entry states the decision, one clause of rationale, and **what not to do** — including
spacing, bracing and placement where those are part of the rule.

Author back-references in the text (`Gleichung (1)`, section numbers) are printed on the page and
are copied verbatim; they are not entries here.

## Orthography of this edition

- **This edition sets `ss`, never `ß`.** The volume is Antiqua with round s throughout — `dass`,
  `Schlussweise`, `Grössen`, `müsste`, `schliesslich`, `Fläche`. The finished file therefore
  contains **no `ß` at all**, and that is correct, not an omission. Do **not** "restore" `ß` in
  `dass`/`muss`/`Grösse`, and do **not** treat this as an exception to R19 — it is the print.
  Umlauts are still literal `ä ö ü` (R19). Confirm on the scan the first time you meet one of these
  words, and say so in your report.
- **The adjectival/genitive apostrophe is the raised comma `’` (U+2019), written as literal
  Unicode.** The print sets `Dirichlet’sche`, `Newton’schen`, `Dirichlet’s`, `Dirichlet’sches`.
  Do **not** use the ASCII `'` (U+0027), do **not** use `\textquoteright`, and do **not** drop it
  (`Dirichletsche`). R18 requires literal Unicode for such glyphs.

## Quotation marks

- **The edition's quotation glyphs are `»` opening and `«` closing** — German angle quotes, whose
  direction is the **reverse** of French guillemets. Write them as literal Unicode `»` and `«`
  (R18). Do **not** use `\guillemotleft`/`\guillemotright`, `` `` ''``, `„…“`, or the French
  `«…»` ordering. The long quotation from Dirichlet's 1856 lecture runs from p. 49 to p. 52 and is
  set this way, and so are the two inline quotations on p. 49, `»Dirichlet’sches Princip«` and
  `»Princips«`.
- **The repetition here is a paragraph convention, not a line-break artifact, so R22 does not
  collapse it: keep the `»`.** Settled on the scan (batch 1): the `»` stands at the first word of
  each quoted *paragraph* — `»Ist irgend eine endliche Fläche…`, `»Zum Beweise schicken wir…`,
  `»Ist irgend ein endlicher zusammenhängender Raum t…`, `»Wir beweisen den Satz…`, `»Es giebt
  also jedenfalls…` — and never at the start of an interior printed line. Write `»` at the head of
  every quoted paragraph, and a closing `«` **only where the print sets one** — p. 49 at
  `…Werth hat.«`, p. 50 at `…stattfinden würde.«`, p. 51 at `…für $M$ zu erhalten.«`, and p. 52 at
  both `…identisch sein.«` and `…unmöglich sind.«`, each verified against the scan. The one quoted
  paragraph the print leaves unclosed is `»Zum Beweise schicken wir den folgenden Satz voraus:` on
  p. 49, and it stays unclosed here. Do **not** collapse the openings to a single pair, and do
  **not** supply a closing `«` at a paragraph that lacks one.

## Function names and symbols

- **The function is `\varphi`, not `\phi`.** The print sets the curly φ. Do **not** write `\phi`
  anywhere in this work, and do **not** switch glyph inside a subscript or an exponent.
- **The author's inverse tangent is `arctg`, set as `\operatorname{arctg}`.** That is his printed
  name for the function, and R-faithfulness keeps it. Do **not** write `\arctan`, `\mathrm{arctg}`,
  or `\text{arctg}`. Settled on the scan (batch 2): the print sets `arctg x/ε` and `arctg 1/ε`
  with the fraction abutting the operator name, so write
  `\operatorname{arctg} \frac{x}{\varepsilon}`. Do **not** add parentheses around the argument,
  do **not** use `\dfrac` for the inner fraction, and do **not** insert `\,` before it.
- **The small Greek of the counterexample is `\varepsilon`, never `\epsilon`.** Confirmed under
  magnification on every display of p. 53: the print sets the curly ε, which at prepared-image
  resolution is easy to mistake for `e` or `s`. Do **not** write `\epsilon`, and do **not** vary
  the glyph between running text and subscripts.
- **The interval's ellipsis is `\cdots`, not `\ldots`.** Confirmed under magnification at both
  occurrences (pp. 52 and 54): the three dots sit at the vertical centre of the digits, level with
  the bar of the `+`. Write `$(-1 \cdots +1)$`. Do **not** write `\ldots`, `\dots`, or three
  literal periods.
- **The two kinds of derivative are both printed, and each stays where it belongs.** Settled on
  the scan: the potential-theory passages on pp. 50–52 print the curly `∂` — confirmed under
  magnification on p. 50's first display and on p. 52's Laplace display — so those are `\partial`
  throughout (`\frac{\partial^{2} w}{\partial x^{2}}`, and likewise in $M$, $N$, $U$, $U'$). The
  one-dimensional counterexample on pp. 52–54 prints the straight `d`, and prints the argument
  with it, so it is **`\frac{d\varphi(x)}{dx}`**, with the `(x)` — not `\frac{d\varphi}{dx}`, and
  not `\varphi'`. Do **not** back-convert the potential-theory displays to `d`, and do **not**
  write `\partial` in the counterexample.
- **The standalone display on p. 54 contains the bare fraction `\frac{d\varphi(x)}{dx}` and no
  leading `x`.** Checked under magnification across the whole left half of the text block, which
  is blank: this looks at first like a dropped factor, since it is $x\,d\varphi/dx$ that the
  vanishing integral forces to be zero, but the print really sets the fraction alone and the
  reasoning is complete as printed — the sentence's appeal to the continuity of $\varphi(x)$ and
  $\frac{d\varphi(x)}{dx}$ is exactly what carries $x\,\varphi' = 0$ to $\varphi' = 0$ at
  $x = 0$ as well. Do **not** insert an `x`, and do **not** attach an `\ednote`: nothing is
  misprinted.
- **Integrals in those displays are set `\left\{ … \right\}` around the integrand, with the
  differential as `\,dt`.** Used uniformly across every integral display in the work. Do **not**
  substitute plain `\{ \}` or `\big\{`, and do **not** drop the thin space before `dt`.

## Headings and the reading-date line

- **The heading printed in full capitals is set in normal case**, as
  `\section*{Über das sogenannte Dirichlet’sche Princip.}`, keeping the printed final period.
  Full capitals are a typographic style, not orthography (R12/R20); the running heads repeat the
  same words and are **not** transcribed.
- **The parenthetical line under the heading is part of the article and is transcribed** as
  ordinary text on its own paragraph: `(Gelesen in der Königl. Akademie der Wissenschaften am 14.
  Juli 1870.)`. Do **not** turn it into an `\ednote`, a `\subsection*`, or a footnote — the print
  sets it as a display line beneath the title. Do **not** expand the abbreviation `Königl.`

## Emphasis (Sperrung)

- **Letterspaced words become `\emph{...}`, including author names** (R20/R24): `Lejeune
  Dirichlet`, `Riemann`, `Dedekind` on p. 49; `kleinsten` on p. 50; `eine einzige` and `absolutes
  Minimum` on p. 51. Do **not** reach for `\textbf` for any of them.
- **Numerals are never letterspaced emphasis.** This volume sets digits with a naturally wide
  spacing — `1856`, `1870` — and magnification shows the same spacing in ordinary running text.
  Do **not** `\emph` a numeral anywhere in this work.
- **The print emphasizes the same words inconsistently, and that inconsistency is reproduced
  (R23).** `eine einzige` is plain on p. 49 (`aber nur eine einzige Function w`) and letterspaced
  on p. 51. Do **not** regularize either occurrence to match the other.
- Identifying letterspacing is a per-instance reading of the scan and the show-through on this
  scan makes it hard by eye; magnify the word rather than judging a loose justified line, and
  report it as a best-effort pass.
- **The full set found, all `\emph`'d:** `Lejeune Dirichlet`, `Riemann`, `Dedekind` (p. 49);
  `kleinsten` (p. 50); `eine einzige`, `absolutes Minimum` (p. 51); `überall` — the second
  occurrence only — and `untere Grenze` (p. 52); `positive` (p. 53).
- **Further R23 inconsistencies of the print, reproduced and not regularized:** the first
  `überall` on p. 52 is plain while the second is letterspaced, and `(absolutes)` on p. 52 is
  plain although `absolutes Minimum` on p. 51 is letterspaced.

## Paragraphing

- **In this volume a line set flush left after a display is a continuation, not a new paragraph;
  only an indented line begins one.** So `Genüge leistet.` (p. 50), `so ist für diese specielle
  Function` and `Daraus erhellt…` (p. 53) carry on the paragraph that preceded the display, and
  take **no** blank line before them. The genuine paragraph openings are the indented ones:
  `Unter der Voraussetzung…`, `Ich will schliesslich…`, `Es bezeichne nämlich…` (p. 52) and
  `Die erwähnte untere Grenze…` (p. 53). Do **not** insert a paragraph break merely because a
  display intervenes.
- **Page furniture is not transcribed**: the signature marks at the feet of pp. 49 and 51
  (`II.`, `7`, `7*`), the running heads, the page numbers, and the centred end-of-article rule
  below the last paragraph of p. 54.

## Displays

- **A pair of equations the print aligns at `=` is set
  `\[ \begin{aligned} … \end{aligned} \]`** (the $M$/$N$ pair on p. 51). Do **not** write a bare
  `align*`, and do **not** split an aligned pair into two separate displays.
