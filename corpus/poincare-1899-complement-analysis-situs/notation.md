# Notation decisions — Poincaré 1899, Complément à l'Analysis situs

Cross-page rendering decisions for this work (HOUSESTYLE R27). Batches cannot see each other; this
file is how they agree. Each entry states the decision, one line of why, and **what not to write
instead**. Where spacing, bracing or placement is part of a rule, it is stated in words.

The Complément continues `poincare-1895-analysis-situs` in the same notation, so the entries below
**seed** this file with that work's decisions wherever the same construction recurs. The
Rendiconti is a different journal set in a different (Elzevir) type; a decision about glyph shapes
in the 1895 glossary is not assumed to hold here unless restated below.

## Seeded from poincare-1895-analysis-situs

### Figures and letters

- **Old-style zero is written `0`.** The zero prints like a small `o`: write `\backsim 0`, `= 0`,
  "égaux à 0" (prose: plain `0`). **Do not** write the letter `o` or `\mathrm{o}`.
- **An unsigned integer standing alone in prose is plain text** ("page 51", "égaux à 0"); a
  *signed* number is math (`égal à $+1$`, `$-1$`). **Do not** write `$1$` for an unsigned integer
  in prose.
- **Upright capitals naming varieties, polyhedra and functions are plain math letters:** `$V$`,
  `$P$`, `$P'$`, `$F$`. **Do not** use `\mathrm`, `\mathbf` or `\operatorname`.
- **Lower-case variety letters are plain italic math letters:** `v`, `a`, `w`. The italic v looks
  like upsilon. **Do not** write `\upsilon`, `\nu` or `\omega` for them.
- **Epsilon is `\varepsilon`** (the print's round ε). **Do not** write `\epsilon`.
- **The curly phi is `\varphi`.** **Do not** write `\phi`.

### Indices

- **Every subscript and superscript is braced, even a single character:** `v_{p}`, `a^{q}_{i}`.
  **Do not** write `v_p` or `a^q_i`.
- **A superscript printed stacked over a subscript is written superscript first:** `a^{q}_{i}`,
  `a^{q-1}_{j}`, `\varepsilon^{q+1}_{k,i}`. **Do not** write `a_{i}^{q}`.
- **Multiple indices keep the print's form (R23):** `\varepsilon^{q}_{i,j}` where the print has a
  comma, tight `\alpha_{ik}` where it has none. **Do not** normalize one into the other.
- **A prime comes before a subscript or stacked indices:** `v'_{p}`, `a'^{q}_{i}`. **Do not** write
  `v_{p}'` or a Unicode `′`.
- **A minus in an index that the scan lost (a gap where `q-1` must stand) is written `-` with no
  `\ednote`,** only where a gap is visible **and** the index sequence requires it.
- **An ordinal suffix on a math quantity keeps the print's suffix in `\text{}`:**
  `$(n+1)^{\text{ème}}$`, `$\beta^{\text{ème}}$` — this print sets "ème", not "ième". **Do not**
  write `^{\text{ième}}` where "ème" is printed, or `^{eme}`.
- **A numeral ordinal in prose is `3\textsuperscript{ème}`** (text mode, suffix as printed; ruled
  after batch 1, precedent `picard-1884`). **Do not** write `$3^{\text{ème}}$`, `3ᵉ` (drops the
  "me"), or `3ème` on the baseline.

### Signs

- **The homology sign is `\backsim`** (Poincaré's large reversed tilde ∽, left end high):
  `\Sigma \varepsilon a \backsim 0`; in prose "par $\backsim$". **Do not** write `\sim`,
  `\thicksim`, `\approx`, or a literal `∽`.
- **The congruence sign ≡ is `\equiv`:** `a^{q+1}_{k} \equiv \sum_{i} \ldots`. It is not the
  homology sign. **Do not** write `\backsim`, `\cong` or `==`.
- **`≦` is `\leqq`, `≧` is `\geqq`.** **Do not** write `\leq` for the double-barred form.
- **The letter-sized Σ is `\Sigma`; the large operator (with limits under it) is `\sum`.** Decide
  each occurrence by printed size: `\sum_{i} \varepsilon^{q+1}_{k,i} a^{q}_{i}` where the print
  sets a large Σ with `i` beneath it. **Do not** use one for the other.
- **A sign that lost strokes (`=`, `≡`, `-`, `±`) is written as intended with an `\ednote`** that
  strokes did not print (R29), placed directly after the closing `\]`, never inside the math. A
  broken *letter* in a prose word is written as the intended letter with no ednote.
- **Absolute value is plain bars** `|x|`. **Do not** write `\lvert` or `\left|`.

### Ellipses

- **A printed `. . .` in math is `\ldots`,** commas or operators on both sides as printed:
  `a_{1}, a_{2}, \ldots, a_{n}`, `+ \ldots +`. **Do not** write `\dots`, `\cdots` or `...`.
- **A prose ellipsis is text-mode `\ldots`;** followed by a word it takes a control space
  (`\ldots\ et`).

### Punctuation and spacing

- **A French space before a colon is `~:`** (`il viendra~:`, `la congruence~:`). **Do not** write a
  plain space before `:`, a tight colon, `\,` or U+00A0.
- **Semicolons, question marks and exclamation marks are set tight** (`nulle; mais`). **Do not**
  write `nulle ; mais`.
- **`M.` before a name takes a tie:** `M.~Heegaard`. A title before a name likewise.
- **Two words run together by the compositor are separated, with no `\ednote`.**

### Emphasis and references

- **Italic is `\emph{}`,** trailing punctuation outside the braces. The title of the 1895 memoir,
  set in italic in running text, is `\emph{Analysis situs}` **with the capitalization the print
  gives at that place** (R23) — the Rendiconti prints "Analysis situs" with lower-case s; if some
  place prints "Situs", keep that. **Do not** write `\textit`.
- **Page references to the 1895 memoir are copied verbatim** ("page 51", "\emph{Analysis situs},
  page 43"). They are the author's; **do not** turn them into links or add editorial notes.
- **"n°" is the `\no` macro followed by a plain space:** `le \no 8`. **Do not** write `n°`.
- **"C. Q. F. D." is `C.~Q.~F.~D.`** at the end of the proof's last sentence, same paragraph.
- **A numbered list "1°, 2°" uses a literal `°`,** each item its own paragraph where the print
  breaks them onto separate lines; inline where the print runs them in a sentence.

### Displays

- **Equation numbers are `\tag{…}` with the print's content, no parentheses:** `(4)` → `\tag{4}`,
  `(9, q)` → `\tag{9, q}` (the `q` is italic in print: write `\tag{9, $q$}`). A "bis" number is
  `\tag{1 \textit{bis}}`. Greek labels are `\tag{$\alpha$}`. **Do not** write `\tag{(4)}` or
  `\tag{9, q}` with a bare math letter in text mode. A running-text reference is plain "(4)",
  "(9, $q$)" as printed.
- **A lone displayed relation with no printed number gets no `\tag`.** Do not invent numbers; a
  repeated number is kept as printed.
- **A braced system is one display:** `\[ \left\{ \begin{aligned} &row,\\ &row. \end{aligned}
  \right. \tag{1} \]`, rows led by `&`, the print's line-end punctuation kept. An unbraced
  multi-line system is `aligned` without `\left\{`. **Do not** use `cases`, `array` or `gather`.
- **A displayed list of items is separated by `\qquad`,** including around `\ldots`, keeping the
  printed punctuation. **Do not** use `\quad` or `&`.
- **A delimiter-free Tableau (array of entries) is `\begin{matrix}` inside `\[ \]`,** rows separated
  by `\\[1ex]`, printed commas kept in the cells. A determinant printed between bars is `vmatrix`.
  **Do not** use `pmatrix`, `bmatrix`, `array` or `tabular`; a dotted cell is `\ldots`, never
  `\cdots`/`\vdots`.
- **A word inside a display is `\text{ ou }`.** A congruence modulus is
  `\qquad (\text{mod.}\ 2)` with the printed "mod.". **Do not** write `\pmod`.
- **After a display, a blank line (new paragraph) only where the print indents the next line.** An
  unindented continuation follows `\]` with no blank line. A new sentence after a display is not
  by itself a new paragraph.
- **A display broken across a page break is closed at the foot of the earlier page and reopened
  after the next `\origpage`** (no blank line).

### Structure

- **Title block (p. 285):** `\section*{Complément à l'Analysis situs;}` — capitals normalized, the
  print's semicolon kept — then the plain paragraph with the byline as printed
  (`Par M.~H.~Poincaré, à Paris.`), then the session date as its own paragraph in `\emph{}` as
  printed (`\emph{Adunanza del …}`). The journal's running head and page number are furniture.
- **§ headings are `\subsection*{\S~1. --- Title in sentence case.}`** — tie after `\S`, spaced
  `---` where the print has a dash, the print's trailing period kept, capitals/small caps
  normalized to sentence case with accents restored. Roman part numerals are `\section*{I.}`.
  **Do not** write `\textsc`, all capitals, or put a text-mode brace group inside a heading (R25).
- **Italic centred sub-headings are `\subsection*{…}`,** period kept, no `\emph`.
- **A word hyphenated across a page break is completed on the page where it begins;** the next
  fragment starts after the continuation, with **no** blank line after its `\origpage`.
- **Page furniture is dropped:** running heads ("COMPLÉMENT À L'ANALYSIS SITUS.", "H. POINCARÉ."),
  page numbers, and the signature line at the foot of a gathering ("Rend. Circ. Matem., t. XIII,
  parte 1ª.—Stampato il … 1899." and its sheet number).
- **Footnotes follow R15.** The print marks them `(*)`, `(**)`: keep the in-text call as
  `${}^{(*)}$` and give the note as a complete unit at the end of that page's main text, led by
  `\textbf{(*)}`. A note running onto the next page is given whole on the page where it begins.
  **Do not** use `\footnote{}`, and **do not** renumber the asterisks.

## Added after batch 1 (pp. 285–296)

- **"bis" numbers are `\tag{5 \textit{bis}}`;** a running-text reference is `(5~\emph{bis})`. The
  Rendiconti sets "bis" as a superscript; that is presentation. **Do not** write `5^{bis}`,
  `\textsuperscript{bis}` or `(5 bis)`.
- **§ headings here are numbered in Roman with the title on the next line, no dash:**
  `\subsection*{\S~I. Introduction.}`, `\subsection*{\S~II. Schéma d'un polyèdre.}`. One heading,
  numeral and title together. **Do not** add `---` (the print has none), and **do not** split the
  numeral and the title into two headings.
- **The Elzevir italic α can print like an "x"** (p. 295: rank α₁, α₂; β − α_q). Where the variable
  is α by context and sequence, write `\alpha`. **Do not** write `x` or `\varkappa`. Magnify when
  the context does not settle it.
- **The inequality index in (1)/(2) is `\varphi_{\gamma}`:** this font's γ. **Do not** write
  `\upsilon` or `Y`.
- **A large Σ (operator size) is `\sum` even without limits beneath it;** inline, write
  `\displaystyle\sum` only if the print sets it large in running text. A letter-height Σ is
  `\Sigma`. Decide by printed size.
- **Guillemets around a quotation are `«~…~»`,** tie inside each guillemet; italic quoted words
  inside are `\emph{}`.
- **Letterspaced names (Betti, Heegaard, Picard) are `\emph{}`** (R20).

## Added after batch 2 (pp. 297–308)

- **The italic h prints like "b"** in `B(q, h, j, k)`, `a^{h}_{j}`, `h'`, `h_{1}`, `h'_{0}`; it is
  `h` by context ("l'indice $h$"). **Do not** write `b` there. The subdivision varieties
  `b^{q}_{i}` use a genuinely different letter and stay `b`.
- **The summation over one class is an italic capital `S`,** which the author contrasts with Σ:
  `S \alpha B(q, h, j, k)`, `S_{1} \alpha_{1} B(\ldots)`. **Do not** write `\sum`, `\Sigma` or
  `\mathcal{S}` for it.
- **Every letter in a multi-part tag is in math:** `\tag{2, $q$, $h$, $j$, $k$}`,
  `\tag{3, $q$, $i$}`. Running-text references follow the same pattern: "(2, $q$, $q$, $i$, $k$)",
  "(1, $q - 1$, $j$)". **Do not** write `\tag{2, q, h, j, k}`.
- **A zero subscript is braced, nested ones too:** `j_{0}`, `\alpha_{0}`, `a^{q}_{j_{0}}`,
  `a^{h'_{0}}_{j'_{0}}`. **Do not** write `j_0` or `j_{o}`.
- **A large Σ inline without limits is `\displaystyle\sum`** (houselint requires the
  `\displaystyle` for operator-size Σ in running text). A letter-height Σ inline is `\Sigma`.
- **A condition printed at the right of a numbered display stays in the display after `\qquad`:**
  `\sum \alpha B(q, h, j, k) \equiv 0, \qquad (h \geqq q) \tag{1}`. **Do not** move it into prose.
- **Equation numbers restart in each §** (§ V has its own (1)–(10), (5 bis), (6 bis)). Copy tags as
  printed. **Do not** renumber or disambiguate.
- **§ headings normalize capitals to sentence case** except proper names:
  `\subsection*{\S~IV. Subdivision des polyèdres.}` (print "Polyèdres"),
  `\subsection*{\S~V. Influence de la subdivision sur les nombres de Betti réduits.}` — no `\emph`
  inside a heading even where the name is letterspaced.
- **Missing circumflexes are kept as printed** ("entraine", "connaitre"), R12/R23. **Do not** add
  them.

## Added after batch 3 (pp. 309–320)

- **Ditto lists set as rows of prose (pp. 315–316) are one paragraph per printed row,** ditto marks
  as literal `»` separated by single spaces, the print's final punctuation kept (`» ».`), math cells
  inline `$…$`. These are sentences laid out in rows, not an array of entries. **Do not** write
  `matrix`, `tabular`, `\qquad`/`&` alignment, or replace `»` with words. (A true delimiter-free
  array of math entries is still `matrix`, above.)
- **Numeral ordinals copy the printed suffix exactly:** `1\textsuperscript{ère}`,
  `2\textsuperscript{de}`, `2\textsuperscript{ème}`, `3\textsuperscript{e}`. **Do not** normalize
  them to one suffix.
- **The subdivision-edge letter is `b_{1}`** (numeral subscript: `\sum b_{1}`, `V(b_{1})`); the
  edges of $P'$ from § VII on are `b^{1}_{i}` (superscript). **Do not** write `b_{i}` or `b_{l}` for
  the former, or conflate the two.
- **A prime on a superscripted letter comes before the superscript:** `a'^{2}_{k}`, `P(a'^{2}_{k})`.
  **Do not** write `a^{\prime 2}_{k}` or `a^{2}_{k}{}'`.
- **A coefficient and a letter in prose are one math span:** "2 q" → `$2q$`. **Do not** write
  "2 $q$".
- **A § reference printed with an Arabic numeral is kept:** "au § 3" → `au \S~3`, even though the
  headings are Roman. **Do not** convert to Roman.

## Added after batch 4 (pp. 321–332)

- **A numbered Tableau is `\[ \begin{matrix} … \end{matrix} \tag{1} \]`,** the tag outside the
  matrix; an unnumbered one has no tag; a printed trailing period stays in the last cell (`0.`).
  **Do not** put the number in a cell or column.
- **Primed counts are `N'_{2}`, `N''_{2}`** (prime before subscript). **Do not** write `N_{2}'` or
  `N^{\prime\prime}_{2}`.
- **An italic sentence is `\emph{…}` with its final `?`, `.` or `~:` outside the braces;** where a
  roman equation reference interrupts it, split the runs: `\emph{…tableau} (1) \emph{une …}`.
- **"pag." references are `pag.\ 38`** (control space). **Do not** write `pag.~38` or `pag. 38`.
- **"C. Q. F. D." at the end of a displayed list is `\qquad \text{C.~Q.~F.~D.}` inside the
  display;** at the end of a prose sentence it stays `C.~Q.~F.~D.` in the paragraph.
- **The homology sign stays `\backsim` in the "par division" discussion of § IX** (`dc_{4} \backsim
  0`). **Do not** switch to `\sim`.

## Added after batch 5 (pp. 333–343)

- **The Elzevir italic z prints with a tail (like ʒ) and is `z`:** `\psi_{j}(z_{1}, z_{2}, \ldots,
  z_{p})`. **Do not** write `\zeta` or `\mathfrak{z}`.
- **The "n with a long tail" in the convergence conditions of § XI is `\eta_{k}`.** **Do not**
  write `n_{k}` or `\nu_{k}`.
- **"ter" numbers follow the "bis" rule:** `\tag{2 \textit{ter}}`, reference `(2~\emph{ter})`.
- **∞ is math, with its printed sign:** `jusqu'à $+\infty$`, `de 0 à $\infty$`. **Do not** write a
  Unicode ∞.
- **A system with printed ranges at the right is `aligned`, the range after `\qquad`:**
  `&row \qquad (i = 1, 2, \ldots, n),\`; the tag goes outside. **Do not** use `cases`.
- **A prose list of indexed varieties is one math span** (`$a^{p}_{i}, a^{p-1}_{i}, \ldots,
  a^{0}_{i}$`) unless the print breaks it with prose words or punctuation.
- **Closing lines (p. 343) are two plain paragraphs:** `Paris, mars 1899.` then `H.~Poincaré.`

## Added after the proofread (whole work)

- **A footnote on a page that ends mid-sentence goes at that page's last paragraph break,** before
  the paragraph that runs over, so it stays on its own page without splitting a sentence (p. 329).
  This extends R15, which places notes at the end of the page's main text. **Do not** put the note
  between the two halves of a sentence.
- **`\ednote` is for the printer's errors and lost strokes (R29), not for scan legibility.** A reading
  the scan does not settle is `\uncertain{…}`. **Do not** write an ednote that says only that the
  scan is faded or blotted.
- **The prose-list rule (one math span) is applied work-wide:** "Soient $a^{q}_{1}, a^{q}_{2},
  \ldots, a^{q}_{i}$", unless the print interrupts the list with prose words.

## Added after verification

- **A comma inside a double index that did not print (a gap where `i,1` must stand) is written
  with no `\ednote`,** like the lost index minus. **Do not** ednote it.
- **Ordinal suffixes are kept as printed without a note,** even an unusual one ("1ème", p. 325).
- **Where two readings of an index conflict and the print does not show which is wrong** (p. 292),
  the `\ednote` states the conflict neutrally. **Do not** assert one correction.
