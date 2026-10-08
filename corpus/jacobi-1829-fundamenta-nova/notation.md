# Notation decisions — Jacobi 1829, *Fundamenta nova theoriae functionum ellipticarum*

Work-spanning rendering decisions, so that isolated transcription batches agree. Each entry states
the rule, the rationale, and the forbidden alternatives. Author back-references (`§.`, `(12)`) are
copied verbatim and are not listed here.

## Pagination

- **Scan layout.** The Kyoto scan has two printed pages per image; the pipeline splits each spread
  into single pages, indexed in scan order. Printed page 1 is scan index 14; from there the printed
  page number is index − 13. Front matter: title page = index 8 (unnumbered, `\origpage{i}`),
  Proœmium = iii–iv, Index rerum = v–vi.
- **Roman front matter** uses `\origpage{iii}` etc. (as weyl-1913). Roman numerals that are
  inferred rather than printed are noted in provenance.
- Library ownership stamps (Kyoto, Zittau, kanji margin stamp) and bleed-through are never
  transcribed.

## Typography

- **Amplitude function.** The print sets `sin am`, `cos am`, `Δ am`, `sin^n am(…)` in roman: write
  `\sin\operatorname{am}`, `\sin^{n}\operatorname{am}(\dots)`. *Forbidden:* rewriting as `sn`, `cn`,
  `dn` (Jacobi's later notation, not in this print), or `\mathrm{am}` without `\operatorname`.
- **Ranges in contents/index** use the printed long dash `---` (R17): `§§.\ 1---34`. *Forbidden:*
  `--` or `–`. Dotted leaders in contents are dropped; the page number follows as ` --- N` or
  `pag.\ N` where "pag." is printed. *Forbidden:* `\dotfill`, `\hfill`.
- **Ligatures** Æ, Œ (PROŒMIUM, BORNTRÆGER) are written as literal Unicode. *Forbidden:* `\AE`,
  `\OE`.
- **Contents entries** are one paragraph each, no list environment.
- **Headings.** The work/part title (e.g. DE TRANSFORMATIONE FUNCTIONUM ELLIPTICARUM) is
  `\section*`. Sub-part headings (EXPOSITIO…, PRINCIPIA…, PROPONITUR…, TABULA I.) **and** the
  printed article numbers (`1.`, `2.`, … ) are `\subsection*{…}`; the article number is written as
  `\subsection*{5.}`. *Forbidden:* `\subsubsection*` (the site's `tex.js` does not render it).
  A heading may contain `\dfrac` math (R25).
- **Greek phi** is `\phi` (the print's straight-stroked ϕ), never `\varphi`.
- **Capital Sin/Cos** printed with a squared argument: `\operatorname{Sin}\phi^{2}`,
  `\operatorname{Cos}\phi^{2}`. *Forbidden:* `\sin`/`\cos` (they are capitalised in the print).
- **Exponents of exponents:** the print's `a^(2^m) x^(2^m)` is `a^{(2^{m})}x^{2^{m}}` (same for
  `3^m`). *Forbidden:* `a^{(2m)}`.
- **Doubled letters stay doubled**, like zz: `nn`, `mm`, `xx`, `m''m''` as printed, never squares.
- **Roots:** printed √k is `\sqrt{k}`, √(k.x) is `\sqrt{k.x}` (dotted product kept), fourth roots
  `\sqrt[4]{\dots}`.
- **Superscript ordinals:** `Cl$^{\mathrm{i}}$` (Clⁱ), `Cl$^{\mathrm{o}}$`, `$p^{\mathrm{ti}}$`.
  *Forbidden:* `\textsuperscript`, Unicode superscript letters.
- **Numbered equation lists** printed `1)`, `2)` … (not the author's formula numbers) are
  `\text{1)}` inside a `gathered` display, *not* `\tag`. Formula numbers printed `(1)` use `\tag{1}`.
- **Emphasis (Sperrung)** of author names (Crelle, Abel, Legendre) and italic runs is `\emph{…}`;
  an italic run interrupted by displays is re-wrapped in `\emph{…}` around each segment.
- **Printer's errors** (e.g. printed `√((1−x)(1−k²x²))` where `(1−x²)` is expected, p. 6) are kept
  as printed and flagged with `\ednote{…}` (R4); faint hand corrections in ink are not transcribed.
- **Capital Φ** (pp. 14–16, Tabulae III/IV, §9, set at capital height) is `\Phi`; lowercase φ stays
  `\phi`. *Forbidden:* `\varphi`, or `\phi` for the capital.
- **Roman function names:** `\operatorname{tg}`, `\operatorname{tang}` as printed. *Forbidden:*
  `\tan`.
- **Script ℋ** labelling the equation system ("Aequationes ℋ §. 12") is `\mathcal{H}`. *Forbidden:*
  `H`, `\mathfrak{H}`.
- **Trig of a squared argument:** the print puts the exponent on the argument: `\sin\psi^{2n}`,
  `\sin\Phi^{2}`, `\cos\Phi^{2}`. *Forbidden:* `\sin^{2}\Phi`.
- **Dot ellipses:** three dots → `\ldots`; the print's two-dot form → `.\,.`. *Forbidden:*
  collapsing the two-dot form to `\ldots`.
- **Radical extent:** keep the printed extent of the bar: `\sqrt{1-xx}(v^{2}-u^{6}x^{2})`.
  *Forbidden:* extending the root over the following factor.
- **A lone `1)` or `2)` display** is `\[\text{1)}\quad\dots\]` (see the equation-list rule above).
- **Words split across a page break** are joined by the assembler without a space (e.g. p. 17→18
  `eius-|modi`); the fragment opening the next page starts with no blank line after `\origpage`.
- **Φ vs φ (revised, §§17–19, pp. 27+):** where the amplitude glyph descends below the baseline it
  is lowercase straight-stroked ϕ → `\phi`; only the capital-height glyph (pp. 14–16) is `\Phi`.
  `\vartheta` for ϑ (am(u−v)), `\sigma` for σ. *Forbidden:* `\theta`, `\varsigma`, `\varphi`.
- **Other roman function names:** `\operatorname{coam}`, `\operatorname{cotg}`, `\operatorname{Arg}`;
  `\sec`. A capital `Sin`/`Cos` outside the squared-argument case is `\operatorname{Sin}` /
  `\operatorname{Cos}` as printed, plus an `\ednote` where a lowercase is plainly expected.
  *Forbidden:* bare `coam`; `\tan`, `\cot`.
- **sin² am u vs sin a²:** `\sin^{2}\operatorname{am}u` (exponent on the sign before `am`) but
  `\sin a^{2}`, `\sin T^{2}`, `\operatorname{Cos}T'^{2}` (exponent on the argument, as printed).
  *Forbidden:* mixing the two forms on one line.
- **Dotted products** keep the printed period with no spaces: `\cos a.\cos b`,
  `\operatorname{am}.u`, `.xx`; after a fraction `.\,b'`. *Forbidden:* dropping it or `\cdot`.
- **Equation lists** `1)`–`33)`: `\text{n)}\quad…` rows inside one `gathered` per page/group, rows
  separated by `\[1ex]` (`\[1.5ex]` for tall rows). *Forbidden:* `\tag`.
- **Item markers a. / b.** are `\emph{a.}`, `\emph{b.}`, each opening its own paragraph.
- **Four-dot ellipses** in product rows: `.\,.\,.\,.`; three dots `\ldots`; two dots `.\,.`.
- **Heading levels:** DE NOTATIONE NOVA …, DE TRANSFORMATIONE … are `\section*`; QUOMODO …,
  FORMULAE …, DE IMAGINARIIS …, THEORIA ANALYTICA …, THEOREMA and article numbers are `\subsection*`.
- **ednote after a display:** an `\ednote` cannot sit inside math; put it right after `\]` on the
  same line and continue the text on the next line without a blank.
- **Prefix Pi/Sigma operators** (from p. 44) are the letters `\Pi`, `\Sigma`, `\Pi^{(q)}`, as the
  print sets them. *Forbidden:* `\prod`, `\sum`.
- **Footnote marker `*)`** in a display is `{}^{*)}`; the footnote itself is `\textbf{*)}` at the end
  of the page text (R15). *Forbidden:* `\footnote`.
- **Product dot before an ellipsis** is not doubled: `8\omega.\,.\,.\,.` is four dots in total.
- **Sub-comma quantities** (the print sets a comma as a lower index): `\lambda_{,}`,
  `\lambda_{,}'`, `\Lambda_{,}`, `M_{,}`, `M_{,}'`. Only where the comma is visibly lowered; a plain
  list comma between items stays a plain comma. *Forbidden:* `\lambda_{1}`, `\bar\lambda`.
- **`2\Sigma`, `\frac{2}{k}\Sigma`:** a coefficient before the prefix Sigma is kept as printed.
- **`{Mod k'}`** is `\left\{\operatorname{Mod}k'\right\}`. *Forbidden:* `\mathrm{Mod}`, `\text{Mod}`.
- **Quoted italic theorem statements** whose lines each open with „ : one pair
  `„\emph{…}"` for the whole quotation, variables as `$k$` inside. *Forbidden:* repeating the
  opening mark per line.
- **Section sign printed raised** (`§^i 19`): `§$^{\mathrm{i}}$ 19`. A heading printed `S.` for `§.`
  is written `§.`. *Forbidden:* `\S`.
- **Dotted product** between a root and a fraction: `.`; between two fractions: `.\,`.
  *Forbidden:* `\cdot`.
- **Bare asterisk with no footnote** (p. 62): `{}^{*}` and no invented footnote text; `{}^{*)}` only
  where a `*)` footnote exists.
- **`§^o praecedente`** (raised o): `§$^{\mathrm{o}}$`.
- **`arg. am`:** `\text{arg.\ am}` in displays, `arg.\ am$(\dots)$` in running text. *Forbidden:*
  `\operatorname{Arg}` (a different glyph, see above).
- **Prose words inside a display line** ("unde:", "fit:") are `\text{…}`.
- **Printed-dot products in k-series** keep plain periods: `5.5.9.9.q^{6}`. *Forbidden:* `\cdot`.
- **Tall products/quotients:** one `\frac` with `\left(…\right)` factors; `\ldots` between factors
  unless the print visibly differs.
- **Part 2 opens on p. 84:** THEORIA EVOLUTIONIS FUNCTIONUM ELLIPTICARUM. is `\section*`; DE EVOLUTIONE
  … IN PRODUCTA INFINITA. is `\subsection*`; `35.` is `\subsection*{35.}`.
- **Item markers `a)` / `b)`** (italic, pp. 81–82): `\emph{a)}`, `\emph{b)}`, each opening its own
  paragraph. *Forbidden:* `\textbf`.
- **Sub-comma on ω, Λ, λ, M** in the "transformatio secunda" passages: `\omega_{,}`, `\Lambda_{,}`,
  `\Lambda_{,}'`, `M_{,}M_{,}`. *Forbidden:* `\omega_1`, `\bar\omega`.
- **`sin^2 .` before a fraction** keeps the printed dot: `\sin^{2}.\dfrac{i\pi K'}{K}` (same for
  `\cos^{2}.`). *Forbidden:* `\sin^{2}\left(…\right)`, dropping the dot.
- **"Q. D. E."** is `Q.\ D.\ E.` as its own paragraph.
- **`*)` footnote marker in running text:** `${}^{*)}$`. *Forbidden:* `\footnote`.
- **`d²k²`** printed for (d²k)² is kept as `d^{2}k^{2}`; `d^{2}\lambda^{2}` likewise.
- **Radical over a dotted product:** `\sqrt{k.K}` when the bar covers both letters. *Forbidden:*
  `\sqrt{k}.K`.
- **Prime after a bracketed index:** `k^{(m)\prime}`, `k^{(2)\prime}`. *Forbidden:* `k'^{(m)}`,
  `k^{(m)'}`.
- **Four-dot rows in a radicand or product end** use `.\,.\,.\,.`; a printed two-dot row `.\,.`;
  three dots `\ldots`.
- **Unnumbered "X in Y" substitution rules** (Theoremata I–III, pp. 91–92): `\text{ in }` rows inside
  one `gathered`, columns joined with `\qquad\qquad`. *Forbidden:* `array`, `&`.
- **Quoted theorem statements printed in roman** (not italic) are `„…"` without `\emph`.
- **`e^{-\frac{\pi K'}{K}}`:** keep the printed order inside the exponent (`\frac{K'\pi}{K}` where
  printed so).
- **Exponent letter l** in `2^{l}`, `2^{l+1}`, `q^{2^{l}m}` (pp. 105–107; the text says "l, m numeri
  omnes"). *Forbidden:* `2^{1}`.
- **Prefix Σ φ(p)** uses `\phi(p)`; the result Φ of the THEOREMA integral (pp. 97–98) is `\Phi`, the
  integration variable `\phi`. *Forbidden:* `\Phi(p)`, `\varphi`.
- **Arc functions:** `\operatorname{Arc}\operatorname{tg}`, `\operatorname{Arc}\sin k`;
  `Arc. sin` in running text `\operatorname{Arc.}\sin k`. *Forbidden:* `\arctan`, `\arcsin`.
- **Stacked ± alternatives** (p. 102): two-row `gathered`, `\qquad` spacing in the lower row.
  *Forbidden:* `array`, `\substack`.
- **Printed spellings kept:** "Formulas", "Coëfficientem"; a plain misprint like "co casu" for "eo
  casu" is read as the plainly printed letter (`eo`) and not flagged.
- **Legendre's `E^I`:** `E^{\mathrm{I}}` (like `F^{\mathrm{I}}`). *Forbidden:* `E^{I}`, `E_1`.
- **Centred series labels** (I., II., I. a., II. a.): `\emph{I.}`, `\emph{I.\ a.}`, each its own
  paragraph. *Forbidden:* `\subsection*`, `\textbf`.
- **Vertical rows of dots** between table formulas: `\vdots` as its own `gathered` row.
- **A display crossing a page break** is closed at the end of the first page and a new `\[` opened
  on the next page, with no blank line after `\origpage`.
- **Π followed by a number/factor:** `\Pi 2`, `\Pi 2n`, `\Pi(2n-1)`; the product 1.2.3 . . n is
  `1.2.3.\,.\,n`.
- **A heading containing displayed expressions** (p. 115) is one `\subsection*` with `\dfrac` math;
  article numbers 41–44 are `\subsection*{n.}`.
- **Subscript digit 1 printed as small ɪ** (`R_I`, `S_I`): `R_{1}`, `S_{1}`. *Forbidden:* `R_{,}`,
  `R_{\mathrm{I}}`. A small 6 printed like σ (`13R_6`): `R_{6}`. *Forbidden:* `R_{\sigma}`.
- **Dots inside numeral products** are counted as printed: `1.3.\,.\,11`, `2.4.\,.\,.\,12`.
  *Forbidden:* `\ldots`, `\cdots`.
- **Page-top series label** (`III.`, `IV.`): `\emph{III.}` as its own paragraph right after
  `\origpage`.
- **Tangent:** `\operatorname{tang}\operatorname{am}`, `\operatorname{cotang}\operatorname{am}`.
  *Forbidden:* `\tan`, `\operatorname{cotg}` for this.
- **Stacked fractions** (2K/π over sin am …): `\frac{\dfrac{…}{…}}{…}`; do not flatten.
- **"Cll."** (Clarissimis) before italic names: `Cll.\ \emph{Maclaurin} et \emph{Lagrange}`;
  "Iournal" spelling kept.
- **Product dot after d²/Π numerators** kept per occurrence, as printed (`d^{2}.` vs none).
- **Partial-derivative-shaped glyph ∂** (§50 and Theorema II, pp. 140–141), a variable distinct from
  ϑ: `\partial` (`F(\partial)`, `\sin\partial\cos\partial\Delta\partial`). Plain ϑ stays `\vartheta`.
  *Forbidden:* merging them, `\theta`.
- **`Const.`** in formulas is `\text{Const.}`; Θ inside a heading is `$\Theta$`.
- **Headings (pp. 133–144):** each part title (INTEGRALIUM ELLIPTICORUM SECUNDA SPECIES…,
  INTEGRALIA ELLIPTICA TERTIAE SPECIEI…) is one `\subsection*`; article numbers 47.–51. and
  `THEOREMA I.`/`II.` are `\subsection*`. Italic theorem statements are `\emph{…}` per segment
  around displays. *Forbidden:* `\section*` for these.
- **A multi-row equation with one number:** `\text{n)}` in the first row of a `gathered`.
- **Page footnote containing a display** (`*)` on p. 144): `${}^{*)}$` marker, `\textbf{*)}` note at
  the end of the page text, display inside it.
- **Equation labels in Roman numerals** (`I)`, `II)`, `III)`, p. 154): `\text{I)}\quad` inside a
  `gathered`. *Forbidden:* `\tag`.
- **Small printed fractional exponents** (¹⁄₂, ¹⁄₁₆, ³⁄₂): `^{\frac{1}{2}}`, `^{\frac{3}{2}}`.
  *Forbidden:* `^{1/2}`.
- **Exponent on a Δ with a bracketed index:** `\Delta^{\frac{1}{2}}{\Delta^{(2)}}^{\frac{1}{4}}`.
  *Forbidden:* `\Delta^{(2)\frac14}`. Braced products with exponent:
  `\left\{k^{(2)\prime}\right\}^{\frac{3}{2}}`.
- **Printed ∝** (in E(φ)+E(∝)−E(σ), p. 152) is `\alpha`.
- **Letterspaced centred THEOREMA. / COROLLARIUM.** are `\subsection*`; article numbers 52.–54. are
  `\subsection*{n.}`; DE ADDITIONE ARGUMENTORUM … is a `\subsection*` (print's wording, not the
  contents list's).
- **Printer's misprints kept as printed:** e.g. `\operatorname{siu}^{2}` for sin² (p. 156).
- **A value left blank in print** (`Z(2iK')=` on p. 164): leave `=\ ;`/blank as printed with an
  `\ednote`; do not transcribe the hand-written ink or fill it in.
- **Imaginary unit** is plain `i` (`iu`, `e^{ix}`). *Forbidden:* `\mathrm{i}`.
- **`cotg am`:** `\operatorname{cotg}\operatorname{am}`; `Arc. tg .`: `\operatorname{Arc.}\operatorname{tg}.`
  *Forbidden:* `\cot`.
- **`√∝`** is `\sqrt{\alpha}`.
- **Heading** REDUCTIONES EXPRESSIONUM … (p. 161) is one `\subsection*` with inline math; articles
  55.–59. are `\subsection*{n.}`.
- **Integral printed without its differential** (pp. 161–162) is kept as printed with an `\ednote`.
- **Heading levels (pp. 172, 176):** FUNCTIONES ELLIPTICAE SUNT FUNCTIONES FRACTAE… and DE EVOLUTIONE
  FUNCTIONUM H, Θ IN SERIES… are each one `\subsection*` (math as `$H$`, `$\Theta$`); articles
  61.–64. are `\subsection*{n.}`. *Forbidden:* `\section*`.
- **Printed `e`** (once ε-shaped in the scan) is `e`. *Forbidden:* `\epsilon`.
- **Dot exponents** (`q^{2·3}`, `q^{1·2}`): `q^{2.3}`, `q^{1.2}`. *Forbidden:* `\cdot`.
- **Primed series coefficients:** `A'`, `A''`, `A'''`, `A''''` as that many `'`. *Forbidden:*
  `\prime` stacks, `^{(n)}`.
- **Ditto marks `- -`** in the n-ranges table (p. 157) are `\text{-}` inside a `gathered`.
- **A sentence continuing after a display** (lowercase, flush left) follows `\]` with no blank line;
  a blank line is used only before an indented new paragraph.

## Reconciliation after the scan-verification pass (supersedes any earlier entry it contradicts)

- **tg vs tang, cotg vs cotang:** the print itself uses both (tang on pp. 21, 22 … , tg am/tg coam on
  pp. 31–66 …, cotg on p. 35, cotang on p. 119); follow the print per occurrence:
  `\operatorname{tg}`, `\operatorname{tang}`, `\operatorname{cotg}`, `\operatorname{cotang}`.
- **Paragraph breaks (the most frequent batch error):** text after a display that is flush left in
  the print continues the sentence and takes NO blank line (also at a page top, after
  `\origpage`); a blank line only before an indented line. Q.D.E. printed inline stays inline.
- **Product dots:** `.\,` between two fractions, `.` between a root and a fraction, none where
  the print shows only a gap. Checked per occurrence against the print.
- **Ellipsis dot counts** vary in the print (two, three, four, five, six); each was settled from the
  scan and a flat `\ldots` default is wrong in places. Where the count could not be checked at
  higher resolution it rests on the full-page image.
- **Centred series labels** `I.`/`II.` that head a block of formulas are `\emph{…}` paragraphs; on
  pp. 52 and 64 they stand above A./B. headings and are `\subsection*{II.}`.
- **Hand-inked corrections** are never transcribed; the print's reading is kept and an `\ednote`
  cites the author's Corrigenda where they list it. Inline (non-display) misprints get the
  `\ednote` right after the word.
- **Printed ∝** for α in the index and p. 152 is `\alpha`.
