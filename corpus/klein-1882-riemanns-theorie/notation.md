# Notation decisions — Klein 1882, *Ueber Riemann's Theorie der algebraischen Functionen und ihrer Integrale*

Cross-page rendering decisions for this work. Batches cannot see each other; this file is how they
agree. Each entry states the decision, one clause of rationale, and **what not to do** — including
spacing, bracing and placement where those are part of the rule.

Author back-references in the text (`Gleichung (3)`, `§. 14`, `Fig. 21`) are printed on the page and
are copied verbatim; they are not entries here.

## Scope and page markers

- **The Vorrede (pp. iii–vi), the Inhalt (pp. vii–viii) and the text (pp. 1–82) are transcribed.**
  Front-matter pages carry their printed lower-case roman numbers: `\origpage{iii}` … `\origpage{viii}`
  (corpus-format, Roman page markers). Do **not** convert them to arabic. The title page is not
  transcribed.
- **The Vorrede heading is `\section*{Vorrede.}`, the Inhalt heading `\section*{Inhalt.}`**, as
  printed. Klein's signature and date line under the Vorrede, if printed, is a paragraph of its own.
- **Inhalt entries are plain paragraphs, one per printed entry, NOT `\section*`** — they are a list
  of the book's headings, and making them headings would duplicate every section in the reader's
  navigation. A part line is `Abschnitt I. Einleitende Betrachtungen.`; a § entry is its number and
  title as printed, then ` --- ` and the printed page number:
  `§.~1. Stationäre Strömungen in der Ebene als Deutung der Functionen von $x + iy$ --- 1`. The
  ` --- ` stands in for the print's dot leaders and page column, which the site cannot set
  (`\hfill`, `\dotfill` and `\quad` render as literal text). **No period before ` --- `**: the dot
  after a title is the first leader dot, not punctuation. The column header `Seite` is kept where
  printed (under Abschnitt I and III), as its own paragraph. Abschnitt lines carry no `\emph`. The
  Inhalt's titles are copied as the Inhalt prints them, even where they differ from the § heading
  in the text. Do **not** use `\hfill`, `\dotfill`, `\quad`, a table or a list environment.
- **Letterspaced place names are `\emph`** like names (`\emph{Borkum}`, the Vorrede's date line).

## Orthography of this edition

- **This edition sets `ss`, never `ß`** (`dass`, `heissen`, `zweckmässig`, `schliesst`, `weiss`,
  `Diess`). The file contains no `ß` at all, and that is correct. Do **not** restore `ß`.
  Umlauts are literal `ä ö ü`.
- **The apostrophe (`in's`, `Riemann'sche`) is written as plain ASCII `'`**, the corpus's majority
  practice. Do **not** use `’` or `\textquoteright`, and do not drop it.
- **`Punct` and `Punkt` are both printed** (p. 4 has `Kreuzungspunkt` beside `Kreuzungspuncte`).
  Each occurrence is transcribed as printed (R23); do **not** regularize either way. The same holds
  for any other spelling doublet.
- **German quotation marks are literal `„…“`** (p. 27). Do **not** use ASCII `"` or
  ``` `` '' ```.
- **Dashes in prose are `---`**: the parenthetical dash (`— und dies ist … —,`) and the range dash
  between references (`(1)---(3)`, `§.~2---4`). Do **not** use `--` or a Unicode dash.

## Formulas

- **Minus is an ordinary `-` in math**, though the print sets it as a long dash (`z — z₀` →
  `$z - z_{0}$`). Never `---` or `—` inside math.
- **`Const.` is `\text{Const.}`**, capital C, with the abbreviation dot inside the `\text{}`, as
  printed upright: `$u = \text{Const.}$`. Following sentence punctuation goes outside the math:
  `$v = \text{Const.}$, die`. Do **not** write `const`, `\mathrm{Const}`, or put the dot outside.
- **`log` is `\log`.**
- **Inline fractions are printed full-size and are written `\dfrac`**, each standalone in its own
  `$…$` (`$\dfrac{\partial u}{\partial x}$`, `$\dfrac{dw}{dz}$`); parenthesized ones as
  `\left(\dfrac{…}{…}\right)^{2}`. This is allowed because no large operator precedes them (R2/R16);
  an inline integral with a fraction integrand is still `\displaystyle\int \frac{…}{…}`.
- **The differential `d` is a plain italic `d`** (`\dfrac{d^{2}w}{dz^{2}}`), never `\mathrm{d}`.
  Write `\partial^{2} u`, `\partial x^{2}`. Every sub- and superscript is braced: `z_{0}`, `x^{2}`.
- **A sans-serif upright `A` is `\mathsf{A}`.** From p. 7 Klein writes a pure-imaginary coefficient
  as $i\mathsf{A}$, and the print sets that A sans-serif; it is a different quantity from the italic
  $A$ in the same passage. Do **not** write plain `A`, `\mathrm{A}` or `\mathbf{A}`.
- **Greek `\nu` vs Latin `v` is decided by meaning**, since the italic glyphs look alike: the
  multiplicity/order is `\nu` (`$\nu$-fachen`, `$\nu$-mal`, `$A_{\nu}$`); the imaginary part of $w$
  is Latin `v` (`$v = \text{Const.}$`). Do **not** cross them.
- **Rho is `\varrho`, phi is `\varphi`, kappa is `\varkappa`** (the print's open/curled forms). Do
  **not** write `\rho`, `\phi` or `\kappa`.
- **`\cos`, `\sin`** like `\log`. Do **not** write plain `cos` or `\mathrm{cos}`.
- **A product of factors under a radical is kept in Klein's form, without added parentheses**
  (p. 52, `\sqrt{1 - z^{2} \cdot 1 - \varkappa^{2} z^{2}}`). Where the print sets a bar (vinculum)
  over each factor, write `\overline{…}` for it. Do **not** rewrite as `(1 - z^{2})(1 - …)`.
- **A series ellipsis printed as four dots is `\cdot\cdot\cdot\cdot`** (p. 5:
  `+ \cdot\cdot\cdot\cdot \dfrac{A_{\nu}}{…}`, no `+` after the dots, as printed). Do **not** write
  `\cdots` or `\ldots`, and do not add the missing `+`. **Match the printed dot count**: a
  three-dot run is `\cdot\cdot\cdot` (p. 28: `A_{1}, A_{2}, \cdot\cdot\cdot A_{p}`, no comma after
  the dots, as printed).
- **`Const.` in running prose, outside any formula, stays plain text**, with a control space before
  a following word: `von Const.\ genommen`. Only inside a formula is it `\text{Const.}`.
- **Abbreviations take control spaces** (R17): `u.\ s.\ f.`, `d.\ h.`, `z.\ B.`.
- **Ordinal suffixes after a math symbol are upright text in the superscript**: `$n^{\text{te}}$`,
  `$(2n - 2)^{\text{ten}}$`. Do **not** write `n^{te}` (italic), `n$^{te}$` or `n-te`.
- **Upper-case `\Phi`, `\Psi` are upright as printed**, distinct from lower-case `\varphi`, `\psi`.
  Do **not** write `\varPhi`/`\varPsi`.
- **Small printed fractions are `\frac`, full-size ones `\dfrac`.** Where the print sets a fraction
  small (the ½ and ¼ in the p. 16 footnote, `(\zeta - \frac{1}{2})^{2} = \frac{1}{4}`), write
  `\frac`; the `\dfrac` rule is only for full-size inline fractions. Never `1/2`.
- **Italic `A` stays plain `A`**; only the sans-serif letters are `\mathsf{A}`, `\mathsf{B}`
  (`$\mathsf{A} + i\mathsf{B}$`, p. 13). Decide per occurrence from the typeface.
- **A derivative printed as `∂` over a fraction keeps that form**: the numerator fraction is
  `\dfrac` inside an outer `\frac`, e.g. `\frac{\partial \dfrac{F\dfrac{\partial u}{\partial q} -
  G\dfrac{\partial u}{\partial p}}{\sqrt{EG - F^{2}}}}{\partial p}` (p. 18, (2) and (5)). Do **not**
  rewrite it as `\frac{\partial}{\partial p}\left(…\right)`.
- **A brace-grouped pair of equations with one number** is
  `\[ \left\{ \begin{aligned} … &= … \\ … \end{aligned} \right. \tag{3} \]` — one tag for the pair,
  as printed. Do **not** use `cases`, and do not tag each line.
- **Radicals are `\sqrt{…}`** (the print's `VEG − F²` is `\sqrt{EG - F^{2}}`).
- **`ff.` after a page number is `p.~329~ff.`** Do **not** write `329ff.` or `sqq.`
- **`etc.` printed upright inside a display line is `\ \text{etc.}`** (p. 22). Do **not** write
  `\mathrm{etc}` or move it out of the display.
- **Compound words with a math prefix keep only the letters in math**: `$XY$-Ebene`,
  `$\alpha$-fachen`. Do **not** write `XY-Ebene` in plain text or put the hyphen in math.
- **The summation sign is the Greek letter `\Sigma`, not `\sum`**: the print sets `Σ a_i u_i` as a
  small upright letter at text size → `$\Sigma a_{i}u_{i}$` (p. 40). Do **not** write `\sum`, and do
  not add `\displaystyle` or limits.
- **`≧` (double-barred) is `\geqq`**, `≦` is `\leqq`, matching the glyph (p. 45 `m \geqq p + 1`).
  Do **not** write `\geq` or `>=`.
- **Zero is sometimes printed as an italic letter `o`, sometimes as the digit `0`**, and the choice
  recurs throughout (pp. 20, 22, 65, 68: `w = o`, `F = o`, `f(w, z) = o`, `p = o` beside `p = 0`).
  It is the print's own habit, not a misprint: transcribe each as printed (`$p = o$` or `$p = 0$`)
  and add **no** `\ednote`. Do not regularize either way (R23). This includes integral limits
  (p. 51: `\int_{o}^{\alpha}`, `\displaystyle\int_{o}^{\pi}`).
- **Klein's list numbering is kept as printed** (p. 66: `1.` then `2)`, `3)`), as plain text at the
  start of the paragraph. Do **not** use a list environment or make it consistent.
- **Spacing between `\infty^{…}` and `mal`/`fach` follows the print**: `$\infty^{3}$ mal`
  (spaced), `$\infty^{\varrho}$mal` (tight).
- **Equation numbers are printed on the LEFT as `(1)`, with no period.** Write `\tag{1}` at the end
  of the display; a period printed after the formula stays inside the display before the tag:
  `= 0. \tag{3}`. Do **not** write `\tag{1.}` and do not rely on auto-numbering.

## Figures

- **The caption follows the printed label word exactly**: Fig. 1 is printed `Figur 1.` → caption
  `Figur~1.`; the others seen so far are printed `Fig. 2.` → `Fig.~2.`. Do **not** normalize one
  form to the other. Side-by-side figures that are separable get one crop and one `\rmfigure` each.
  A missing dot in a label (p. 39 prints `Fig 31.`) is lost type; the caption is still `Fig.~31.`
- **Figures follow HOUSESTYLE R30.** A figure printed between lines of the text goes exactly there,
  even mid-paragraph or mid-sentence (pp. 37, 38, 52 and others set figures inside a running
  paragraph, often right after a colon that introduces them); one printed beside the text goes
  before the paragraph it stands beside. Figures printed side by side — most of Klein's pairs, e.g.
  Figs. 2|3, 25|26, 27|28 — are adjacent `\rmfigure` lines with **no blank line** between them;
  figures printed one above the other are separated by a blank line. (This replaces an earlier
  rule here that moved mid-paragraph figures to the paragraph's end.)

## Footnotes

- **The print marks footnotes `*)`, `**)` …, restarting on each page.** In the text write the mark
  as a superscript with the closing paren inside it: `${}^{*)}$`, `${}^{**)}$`. The note itself goes
  as a complete unit at the end of that page's main text, as its own paragraph led by `\textbf{*)}`
  (R15). A note that runs onto the next page is given whole on the page where it begins. Do **not**
  use `\footnote`, and do **not** put a space between the word and the mark. If the page's main
  text ends mid-sentence, the note paragraph still sits after it, and the next page continues the
  sentence directly after `\origpage{N+1}` with no blank line. Letterspaced names inside notes are
  `\emph` as in the text.
- **The mark stays where it is printed relative to punctuation** (`können.${}^{*)}$` on p. 71), and
  it always sits **outside** an `\emph`: `\emph{… $J = \dfrac{g_{2}^{3}}{\Delta}$}${}^{*)}$.`

## Headings

- **Section headings are `\section*{...}`, one per printed heading**, with the § number and its
  title as printed: `\section*{§.~2. Berücksichtigung der Unendlichkeitspuncte von $w = f(z)$.}`.
  Part headings ("Abschnitt I. Einleitende Betrachtungen.") are also `\section*{...}`, set before the
  § heading that follows them. Do **not** `\emph` inside a heading (R20).
- **A footnote mark in a heading is a separate math span**: `…nach der Zahl $p$${}^{*)}$.}`
  (p. 25). Math is safe inside a heading; a text-mode brace group (`\emph{…}`, `\textbf{…}`) is not.
- **The dot after `§` is kept or omitted as printed**, in headings and in running text alike:
  §§. 1–4 print `§. N.`, but p. 16 prints `§ 5.` → `\section*{§~5. …}`; in prose `(§~10)` beside
  `§.~9`. Do **not** regularize either way.

- **An italic run crossing a page break is closed at the page end and reopened after
  `\origpage`**: p. 61 ends `\emph{… eindeutig}`, p. 62 opens `\emph{in die gegebene …}`. An `\emph`
  can contain neither the footnote paragraph nor `\origpage`. Do **not** leave one open.
- **References are tied with `~`**: `p.~173`, `Bd.~15`, `p.~329~ff.` Do **not** use a plain space.

## Names

- **A name is `\emph` only where the print sets it italic or letterspaced** (`\emph{Roch}`,
  `\emph{Brill} und \emph{Nöther}`, `\emph{Abel}'schen`). A name printed in roman (`Riemann`,
  `Borchardt's`) stays plain. Do **not** `\emph` every author name. The same name may be set
  differently in different places (`Borchardt` is letterspaced in the p. 57 note, roman elsewhere);
  decide per occurrence.
- **An initial is separated by a control space and sits outside the `\emph`** unless the print
  letterspaces the initial too. Throughout this print only the surname is letterspaced:
  `C.\ \emph{Neumann}`, `G.\ \emph{Cantor}`, `C.\ \emph{Jordan}`; a roman name is `C.\ Neumann`.
  Do **not** write `\emph{C.\ Neumann}` or `C.~`.
