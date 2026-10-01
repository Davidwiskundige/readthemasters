# Notation decisions — Poincaré 1902, Quatrième complément à l'Analysis situs

Cross-page rendering decisions for this work (HOUSESTYLE R27). Batches cannot see each other; this
file is how they agree. Each entry states the decision, one line of why, and **what not to write
instead**. Where spacing, bracing or placement is part of a rule, it is stated in words.

The Quatrième complément continues the first three Compléments, so this file is **seeded** with
their decisions wherever the same construction recurs. The Journal de Mathématiques Pures et
Appliquées is a different journal set in a different type from the Rendiconti and the Bulletin de
la S.M.F.: where a seeded entry concerns a glyph shape, a spelling or a print-specific convention
(e.g. "sitûs", "ième" vs "ème", `p.\ 60`) and this print differs, **follow this print** and record
the decision under "Added after batch N".

## This work's print

- **Page furniture is dropped:** running heads, page numbers, signature marks at the foot of a
  page. The paper occupies pp. 169–214 of the JMPA, 5e série, tome 8; any text of a neighbouring
  paper on p. 169 (above the title) or p. 214 (below the end) is not transcribed.
- **Italic in running text is `\emph{}`; the title of the 1895 memoir is `\emph{Analysis situs}`
  with the spelling and accents the print gives at that place (R23).**

## Seeded from the first and second Compléments

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

- **§ headings are `\subsection*{\S~1. --- Title in sentence case.}`** — tie after `\S`, spaced
  `---` where the print has a dash, the print's trailing period kept, capitals/small caps
  normalized to sentence case with accents restored. Roman part numerals are `\section*{I.}`.
  **Do not** write `\textsc`, all capitals, or put a text-mode brace group inside a heading (R25).
- **Italic centred sub-headings are `\subsection*{…}`,** period kept, no `\emph`.
- **A word hyphenated across a page break is completed on the page where it begins;** the next
  fragment starts after the continuation, with **no** blank line after its `\origpage`.
- **Footnotes follow R15.** The print marks them `(*)`, `(**)`: keep the in-text call as
  `${}^{(*)}$` and give the note as a complete unit at the end of that page's main text, led by
  `\textbf{(*)}`. A note running onto the next page is given whole on the page where it begins.
  **Do not** use `\footnote{}`, and **do not** renumber the asterisks.

## From the first Complément, batch 1 (pp. 285–296)

- **"bis" numbers are `\tag{5 \textit{bis}}`;** a running-text reference is `(5~\emph{bis})`. The
  Rendiconti sets "bis" as a superscript; that is presentation. **Do not** write `5^{bis}`,
  `\textsuperscript{bis}` or `(5 bis)`.
- **A large Σ (operator size) is `\sum` even without limits beneath it;** inline, write
  `\displaystyle\sum` only if the print sets it large in running text. A letter-height Σ is
  `\Sigma`. Decide by printed size.
- **Guillemets around a quotation are `«~…~»`,** tie inside each guillemet; italic quoted words
  inside are `\emph{}`.
- **Letterspaced names (Betti, Heegaard, Picard) are `\emph{}`** (R20).

## From the first Complément, batch 2 (pp. 297–308)

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
- **§ headings normalize capitals to sentence case** except proper names:
  `\subsection*{\S~IV. Subdivision des polyèdres.}` (print "Polyèdres"),
  `\subsection*{\S~V. Influence de la subdivision sur les nombres de Betti réduits.}` — no `\emph`
  inside a heading even where the name is letterspaced.
- **Missing circumflexes are kept as printed** ("entraine", "connaitre"), R12/R23. **Do not** add
  them.

## From the first Complément, batch 3 (pp. 309–320)

- **Ditto lists set as rows of prose (pp. 315–316) are one paragraph per printed row,** ditto marks
  as literal `»` separated by single spaces, the print's final punctuation kept (`» ».`), math cells
  inline `$…$`. These are sentences laid out in rows, not an array of entries. **Do not** write
  `matrix`, `tabular`, `\qquad`/`&` alignment, or replace `»` with words. (A true delimiter-free
  array of math entries is still `matrix`, above.)
- **Numeral ordinals copy the printed suffix exactly:** `1\textsuperscript{ère}`,
  `2\textsuperscript{de}`, `2\textsuperscript{ème}`, `3\textsuperscript{e}`. **Do not** normalize
  them to one suffix.
- **A prime on a superscripted letter comes before the superscript:** `a'^{2}_{k}`, `P(a'^{2}_{k})`.
  **Do not** write `a^{\prime 2}_{k}` or `a^{2}_{k}{}'`.
- **A coefficient and a letter in prose are one math span:** "2 q" → `$2q$`. **Do not** write
  "2 $q$".
- **A § reference printed with an Arabic numeral is kept:** "au § 3" → `au \S~3`, even though the
  headings are Roman. **Do not** convert to Roman.

## From the first Complément, batch 4 (pp. 321–332)

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

## From the first Complément, batch 5 (pp. 333–343)

- **"ter" numbers follow the "bis" rule:** `\tag{2 \textit{ter}}`, reference `(2~\emph{ter})`.
- **∞ is math, with its printed sign:** `jusqu'à $+\infty$`, `de 0 à $\infty$`. **Do not** write a
  Unicode ∞.
- **A system with printed ranges at the right is `aligned`, the range after `\qquad`:**
  `&row \qquad (i = 1, 2, \ldots, n),\`; the tag goes outside. **Do not** use `cases`.
- **A prose list of indexed varieties is one math span** (`$a^{p}_{i}, a^{p-1}_{i}, \ldots,
  a^{0}_{i}$`) unless the print breaks it with prose words or punctuation.

## From the first Complément, proofread

- **A footnote on a page that ends mid-sentence goes at that page's last paragraph break,** before
  the paragraph that runs over, so it stays on its own page without splitting a sentence (p. 329).
  This extends R15, which places notes at the end of the page's main text. **Do not** put the note
  between the two halves of a sentence.
- **`\ednote` is for the printer's errors and lost strokes (R29), not for scan legibility.** A reading
  the scan does not settle is `\uncertain{…}`. **Do not** write an ednote that says only that the
  scan is faded or blotted.
- **The prose-list rule (one math span) is applied work-wide:** "Soient $a^{q}_{1}, a^{q}_{2},
  \ldots, a^{q}_{i}$", unless the print interrupts the list with prose words.

## From the first Complément, verification

- **A comma inside a double index that did not print (a gap where `i,1` must stand) is written
  with no `\ednote`,** like the lost index minus. **Do not** ednote it.
- **Where two readings of an index conflict and the print does not show which is wrong** (p. 292),
  the `\ednote` states the conflict neutrally. **Do not** assert one correction.


## From the Troisième complément (Bull. SMF 1902), batch 1

- **Title block (p. 49):** `\section*{Sur certaines surfaces algébriques. --- Troisième complément
  à l'«~Analysis sitûs~»;}` — sentence case, the print's capital "A" given its accent "à", the
  guillemets tied, the trailing semicolon kept — then the paragraph `Par M.~H.~\textsc{Poincaré}.`
  The rubric "MÉMOIRES." above the title is the journal's section head and is not transcribed.
  **Do not** put the byline in the heading.
- **This print spells the memoir "sitûs", with a circumflex, throughout:** `\emph{Analysis sitûs}`.
  **Do not** write "situs" where "sitûs" is printed (R12/R23).
- **An ordinal suffix on a math letter copies the print; this print sets "ième":**
  `$i^{\text{ième}}$`. The seeded "ème" entry came from the Rendiconti. **Do not** write
  `^{\text{ème}}` where "ième" is printed.
- **A numeral ordinal with this print's "e" is `6\textsuperscript{e}`.** **Do not** write "ème"
  or `$6^{e}$`.
- **Page references are `p.\ 60` (control space);** "cf." keeps the print's italic or roman:
  `(\emph{cf}.\ p.\ 61)`, `(cf.\ \emph{Analysis sitûs}, p.\ 60)`. **Do not** write `p.~60`.
- **The print's η looks like "ŋ" or "n"; it is `\eta`** (paired with ξ throughout). **Do not**
  write `n` or `\nu`.
- **A substitution named by a letter-size Σ is `\Sigma`** (`\Sigma`, `\Sigma_{1}, \ldots,
  \Sigma_{q}`). **Do not** write `\sum`.
- **Stacked indices: superscript first, prime first:** `R^{0}_{1}`, `s'^{2}_{a}`.
- **Accented capital "À" is kept where the print accents it; "A" stays bare where it does not**
  (R23: p. 60 "À la substitution", elsewhere "A chaque"). **Do not** normalize either way — except
  in the title heading, whose small-capital "A" is restored to "à" with the sentence case.

## From the Troisième complément, batch 2

- **The cut-origin O with italic letters is one plain math span:** `$Oa$`, `$Oma$`, `$Om'd$`,
  `$OA_{i}$` (R1). **Do not** write `O$a$`, `\mathrm{O}a`, or a lower-case o or a zero.
- **The ditto tables of cuts (pp. 64, 66) are one paragraph per printed row, ditto as literal
  `»`;** a comma list of cuts is one math span until "et" interrupts it:
  `$Ob$ » $Ond, Oma, Ob, Oma$ et $Ond$ » $dabad$,`. **Do not** use `matrix`, `tabular` or `&`.
- **Letter-words printed in spaced groups keep the grouping with thin spaces:**
  `da\,da\,ba\,dad` (p. 66). **Do not** close them up to `dadabadad` or use plain spaces.
- **"mod 2" printed without a period inside a parenthesized condition is `\text{ mod}\ 2`:**
  `(\varepsilon_{1} + \ldots \equiv 0, \text{ mod}\ 2)`. **Do not** add "mod." or use `\pmod`.

## From the Troisième complément, verification

- **The cut origin is an upright roman capital O in the text** (full cap height, visibly larger
  than the old-style zero: p. 62 "$x = 0$ … autour du point $O$"). Only the figures label it with an
  italic lower-case o; the figure is an image and is not transcribed. **Do not** change the text's
  `$O$` to `o` or `0`.
- **Readings that are odd but clearly printed are kept without a note** (p. 52 "βξ + αη"; p. 53
  "changent ξ et η en φ, ψ, ζ"; p. 62 "$x_{0}, \ldots, x_{6}$"; p. 63 "autour de $OA_{i}$"; p. 64
  "$Om'a$" beside "On'a"; p. 61 $z^{2} = y^{2} - x^{2}$ beside p. 67 $z^{2} = x^{2} - y^{2}$).
  Where a relation contradicts the rest of the paper directly, a neutral `\ednote` states the
  conflict (p. 61 $S'' \equiv S'''$).


## Added after batch 1 (pp. 169–180)

- **This print spells the memoir "Analysis Sitûs", capital S and circumflex:**
  `\emph{Analysis Sitûs}`. **Do not** write "situs", "sitûs" or "Situs" where "Sitûs" is printed.
- **Title block (p. 169):** `\section*{Sur les cycles des surfaces algébriques;}`, then the
  paragraph `Par M.~H.~\textsc{Poincaré}.`, then the plain paragraph
  `Quatrième complément à l'\emph{Analysis Sitûs}.`, then `\subsection*{\S~1. --- Introduction.}`.
  The subtitle is a paragraph, not a heading, so its italic survives (R25). **Do not** put the
  byline or subtitle inside the `\section*`.
- **§ headings have Arabic numerals in this print:** `\subsection*{\S~2. --- Cycles à trois
  dimensions.}`. **Do not** convert to Roman.
- **Upright capitals naming varieties and cells are plain math letters, compounds juxtaposed:**
  `F'_{k}`, `MF'_{k}`, `(MB_{q})`, `S(M)`, `S_{0}`. **Do not** use `\mathrm`.
- **Cells built from vertices of Q are juxtaposed letters with no space:**
  `\alpha_{i}\beta_{i+1}F_{k}`, `\beta F''`, `\alpha\beta C'`. **Do not** insert `\,` or `\cdot`.
- **θ is `\theta`, even where worn type makes it look like a zero** (`\Sigma \theta'_{k}`).
  **Do not** write `0` or `O` for it.
- **Σ is letter-size throughout this paper so far:** `\Sigma`, double sum `\Sigma \Sigma`, one
  space between. **Do not** write `\sum` unless the print sets an operator-size Σ with limits.
- **A display with a range line printed beneath it is `gathered`:**
  `\[ \begin{gathered} row \ (i, j = 1, 2, \ldots, q). \end{gathered} \tag{2} \]`. A range printed
  at the right stays after `\qquad` (seeded rule). **Do not** move the range into prose.
- **Equation numbers restart and repeat as printed** (p. 177 restarts at (1); p. 180 has (6) then
  (5)). **Do not** renumber.
- **The Tableau's ditto marks inside `matrix` are `\text{»}`;** a horizontal brace over column
  heads is dropped. **Do not** use `tabular`.

## Added after batch 2 (pp. 181–192)

- **A superscript-0 cycle is `\Omega^{0}_{i}`** (superscript first, zero as `0`). **Do not** write
  `\Omega_{i}^{0}`, `\Omega^{o}` or `\Omega^{\circ}`.
- **A dotted row in an unbraced system is a row `&\ldots\ldots,` inside `aligned`,** the print's
  comma kept. **Do not** use `\vdots`, `\cdots` or an empty row.
- **"t. I, p. 82" is `(t.\ I, p.\ 82)`** — control spaces after both abbreviations. **Do not**
  write `p.~82` or `p. 82`.
- **Worn subscripts: k often looks like h, a dotless i like l (pp. 191 ff.).** Write the letter the
  index sequence requires, with no note; keep a genuine h where the sequence has one
  (`\varepsilon'_{h}`, `B'_{h}` on p. 186).
- **"catégorie 1" is plain text** (the old-style 1 prints like "ı"). **Do not** write `$1$` or "ı".
- **An italic sentence ends its `\emph` before a roman equation reference:**
  `\emph{… de la forme} (2).`

## Added after batch 3 (pp. 193–204)

- **A worn ≡ is `\equiv` with no note while three broken strokes still show.** Only where the
  residue reads as `=` or a gap, and the text calls the relation a congruence, write `\equiv` with
  an `\ednote` after `\]` (R29). **Do not** ednote every worn ≡.
- **A relation the text calls an "identité" is `=`,** even where the sign is worn. **Do not**
  restore it to `\equiv`.
- **Column-aligned two-row lists of cycles are `matrix` with `\[1ex]`;** a single-row displayed
  list uses `\qquad`. **Do not** use `aligned` with `\qquad` for rows that align in columns.
- **"(A)" naming a system is `($A$)`.** **Do not** write `(A)` in text mode.

## Added after batch 4 (pp. 205–214)

- **"au paragraphe 2" is plain text,** though the print sets the numeral in bold. **Do not** write
  `\textbf{2}` or `\S~2`.
- **A figure printed mid-sentence sits on its own line with no blank line before or after it** (R30),
  so the sentence runs on (p. 209 "de deux / Fig. 1 / manières"). **Do not** add a paragraph break.
- **Face labels in prose are `($\alpha$)`; inside a display `(\alpha)`.** The print's δ (shaped like
  ∂) is `\delta`. **Do not** write `$(\alpha)$` in prose or `\partial`.
- **Edges juxtapose with no space (`B'_{1}D`, `OB'_{2}`); a coefficient is separated by one space**
  (`\zeta_{1} B_{1}D`, `\Sigma \zeta_{2} OB_{2}`). **Do not** write `O\,B_{2}`.
