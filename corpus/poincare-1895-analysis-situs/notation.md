# Notation decisions — Poincaré 1895, Analysis situs

Cross-page rendering decisions for this work (HOUSESTYLE R27). Batches cannot see each other; this
file is how they agree. Each entry states the decision, one line of why, and **what not to write
instead**. Where spacing, bracing or placement is part of a rule, it is stated in words — not left
to be inferred from an example.

## Figures and letters

- **Old-style zero is written `0`.** The journal sets text figures and its zero prints like a small
  `o`. Write `> 0`, `= 0`. **Do not** write the letter `o`, **do not** write `\mathrm{o}`.
- **Upright capital function letters are plain math letters:** `$F$`, `$F_{1}$`, `$F_{p}$`. The
  print's upright-vs-italic is presentation. **Do not** write `\mathrm{F}`, `\mathbf{F}` or
  `\operatorname{F}`.
- **The curly phi is `\varphi`.** **Do not** write `\phi`, and **do not** use a literal `ϕ` or `φ`.

## Subscripts, exponents, primes

- **Every subscript and superscript is braced, even a single character:** `x_{1}`, `F_{p}`,
  `\varphi_{q}`, `x^{2}`. **Do not** write `x_1`, `F_p` or `x^2`.

## Derivatives and ellipses

- **Derivatives use a straight `d` and no thin space inside the fraction, as printed:**
  `\frac{dF_{1}}{dx_{1}}`. **Do not** write `\partial` where the print has `d`, **do not** write
  `\mathrm{d}`, and **do not** insert `\,` between `d` and the letter inside such a fraction.
- **A printed `. . .` in a list is `\ldots`, with commas on both sides as printed:**
  `x_{1}, x_{2}, \ldots, x_{n}`. **Do not** write `\dots`, `\cdots` or `...`.
- **A dotted filler row inside a displayed system is six `\ldots` in a row followed by the printed
  punctuation:** `&\ldots\ldots\ldots\ldots\ldots\ldots,\\`. **Do not** write `\cdots` or `\vdots`.

## Punctuation and spacing

- **A French space before a colon is written `~:`** (`nos sens~: elle`, `inégalités~:`). The print
  sets a clear space before the colon; `~` keeps the colon from starting a line. This matches
  `picard-1885`. **Do not** write a plain space before `:`, **do not** write the colon tight
  (`sens:`), **do not** use `\,` or a literal U+00A0.
- **Semicolons, question marks and exclamation marks are set tight** to the preceding word:
  `réel; personne`, `suffisantes? Ce`. The print sets at most a hair space. **Do not** write
  `réel ; personne`, `\,;` or `~?`.
- **`M.` before a name takes a tie:** `M.~Klein`, `M.~Walther Dyck`. **Do not** write `M. Klein` or
  `M.\ Klein`.

## Emphasis

- **Italic is `\emph{}`; the term is `\emph{Analysis Situs}` with capital S** as printed in running
  text. Punctuation following the italic run goes **outside** the braces: `\emph{Analysis Situs},`.
  **Do not** write `\textit`, and **do not** put a trailing comma, period or `?` inside `\emph{}`.
  Italic detection is a by-eye, best-effort pass.

## Displays

- **A braced system is one display:** `\[ \left\{ \begin{aligned} &row,\\ &row. \end{aligned}
  \right. \tag{1} \]`, each row led by `&`, keeping the print's line-end punctuation. **Do not**
  use `cases`, `array`, `gather` or separate displays.
- **Equation numbers are `\tag{n}` with the bare numeral**, as printed `(1)` with no period:
  `\tag{1}`. **Not** `\tag{1.}`, **not** `\tag{(1)}`. Position (left/right) is presentation (R5).
- **A Tableau (array of entries with no delimiters) is `\begin{matrix}` inside `\[ \]`**, keeping
  the printed commas inside the cells, rows separated by `\\[1ex]`. **Do not** use `pmatrix`,
  `bmatrix`, or `array` with a column spec — the print has no delimiters.

## Structure

- **Title block (p. 1):** `\section*{Analysis situs;}` (the print's own semicolon), then the plain
  paragraph `Par M.~H.~Poincaré.`, then `\section*{Introduction.}`. The journal masthead and the
  signature line (`J. E. P., 2e s. (C. no 1)`) are page furniture and are not transcribed.
- **Roman chapter numerals are `\section*{I.}`**; **§ headings are
  `\subsection*{\S~1. --- Title in sentence case.}`** — tie after `\S`, a spaced em-dash `---`,
  the print's trailing period kept, small caps/capitals normalized to sentence case (as in
  `poincare-1910`). **Do not** write `\S 1` without the tie, `--` for `---`, all capitals, or
  `\textsc`; never put a text-mode brace group inside a heading (R25).
- **A word hyphenated across a page break is completed on the page where it begins**, before the
  next `\origpage`; the next fragment starts after the continuation, with **no** blank line after
  its `\origpage`. (p. 4 ends `quelconques`.) **Never** leave a trailing `quel-`, and **never**
  repeat the fragment on the later page.
- **Page furniture is dropped:** running heads, page numbers, library stamps, end-of-section
  ornaments.

## Added after batch 2 (pp. 5–8)

- **Epsilon is `\varepsilon`** (the print's round ε). **Do not** write `\epsilon`.
- **A prime comes before a subscript:** `x'_{k}`, `\varphi'_{\beta}`, `F'_{\alpha}`, `\psi'_{k}`.
  **Do not** write `x_{k}'`, `x^{\prime}_{k}`, or a Unicode `′`.
- **Upright capitals naming varieties and domains are plain math letters,** extending the `F` rule:
  `$V$`, `$V'$`, `$D$`, `$D'$`, `$W$`, `$K^{2}$`. **Do not** use `\mathrm`.
- **The stacked sign `>` over `<` (read as "different from") is `\gtrless`,** as printed:
  `(\gamma \gtrless \beta)`. It is the author's glyph, so it stays. **Do not** write `\neq`,
  `\lessgtr`, `\substack{>\<}` or `\overset{>}{<}`.
- **A side condition in a braced system sits in its own aligned column after `&&`:**
  `&F_{\alpha} = 0 &&(\alpha = 1, 2, \ldots, p),\`. A multi-column system uses `&&` between every
  printed column. **Do not** use `\qquad` for these gaps inside a braced system, and **do not** use
  `array`.
- **In a multi-column system a dotted filler row is two `\ldots` per cell,** each followed by that
  cell's printed punctuation: `&\ldots\ldots, &&\ldots\ldots,\`. The six-`\ldots` rule above holds
  for single-column systems only.
- **A "bis" equation number is `\tag{1 \textit{bis}}`** — numeral, a space, italic `bis`. **Do not**
  write `\tag{1bis}`, `\tag{1'}` or `\tag{(1 bis)}`.
- **A repeated equation number is kept as printed:** p. 7 reuses `(1)`, so `\tag{1}` again. **Do
  not** renumber.
- **Ordinals use the literal superscript letter:** `4ᵉ`. **Do not** write `\textsuperscript{e}` or
  `4^{e}`.

## Added after batch 3 (pp. 9–12)

- **A superscript printed stacked over a subscript is written superscript first:** `x^{0}_{i}`.
  **Do not** write `x_{i}^{0}`, `x^0_i`, `x_{i}^{(0)}` or `\overset`.
- **Greek equation labels are `\tag{$\alpha$}`, `\tag{$\beta$}` — with the dollar signs;** a
  running-text reference is `($\alpha$)`. `\tag{}` is set in text mode, so a bare `\tag{\alpha}`
  fails in KaTeX (corrected at assembly; corpus convention). **Do not** write `\tag{\alpha}`,
  `\tag{(\alpha)}`, `\tag{a}`, or a literal `α`.
- **The index `i` is `_{i}` even where its dot failed to print** (it reads as ι). **Do not** write
  `\iota` or `\imath`.
- **A displayed list of items is separated by `\qquad`, including around `\ldots`,** keeping the
  printed trailing comma: `\[ y_{1}, \qquad y_{2}, \qquad \ldots, \qquad y_{n}, \]`. **Do not** use
  `\quad`, `&`, or an array.
- **A lone displayed relation with no printed number gets no `\tag`.** **Do not** invent numbers.
- **Where one bar of an `=` failed to print** (a single mid-height stroke where `=` must stand, as
  on p. 8 (6) and p. 10 (8 bis)), write `=` and attach an `\ednote` saying one stroke of the `=`
  did not print (R29). **Do not** write `-` or `—`.

## Added after batch 4 (pp. 13–16)

- **A multi-line system with no printed brace is `\[ \begin{aligned} &row,\ &row. \end{aligned} \]`**,
  each row led by `&`, no `\left\{`, the print's line-end punctuation kept (the torus
  parametrization on p. 15, the $\Phi$ system on p. 16). **Do not** add a brace the print lacks,
  and **do not** use `gathered`, `&=` alignment, or separate displays.
- **A double index separated by a printed period keeps the period:** `A_{1.1}`, `A_{i.k}`,
  `A_{p.p}`. It is the author's notation. **Do not** write `A_{1,1}`, `A_{1\cdot 1}` or `A_{11}`.
- **A printed `. . .` between operators is `\ldots` with the operator on both sides:**
  `y_{1} = y_{2} = \ldots = y_{p} = 0`, `+ \ldots +`. **Do not** write `\cdots` or `\dots`.
- **Trigonometric functions are `\cos`, `\sin`, followed by a space and the bare argument as
  printed:** `r\cos y_{1}`. **Do not** write `\mathrm{cos}`, italic `cos`, or add parentheses.

## Added after batch 5 (pp. 17–20)

- **The homology sign is `\backsim`:** `v_{1} + v_{2} + \ldots + v_{\lambda} \backsim 0`. The print
  sets a large reversed tilde (∽, left end high); it is Poincaré's own glyph and recurs through the
  rest of the work. **Do not** write `\sim`, `\thicksim`, `\simeq`, `\approx`, `\mathrel{\sim}`, or a
  literal `∽`.
- **Lower-case variety letters are plain italic math letters with braced subscripts:** `$v$`,
  `v_{1}`, `w_{q}`, `k_{1}v_{1}`. The italic v and w look like upsilon and omega. **Do not** write
  `\upsilon`, `\nu`, `\omega` or `\mathit{v}`.
- **The print's `≦` is `\leqq`** (and `≧` is `\geqq`). **Do not** write `\leq`/`\le` for the
  double-barred form.

## Added after batch 6 (pp. 21–24)

- **A Jacobian printed with a round d is `\partial`; one printed with a straight d stays `d`:**
  `\frac{\partial(x_{\alpha_{1}}, \ldots, x_{\alpha_{m}})}{\partial(y_{1}, \ldots, y_{m})}` (p. 22)
  against `\frac{d(\alpha_{1}, \ldots)}{d[\alpha_{m+1}]}` in (12). The glyph is the author's.
  **Do not** write `\mathrm{d}`, and **do not** swap one form for the other.
- **The large summation operator in displays is `\sum`; differentials after a factor take `\,`:**
  `\int \sum X_{\alpha_{1}\alpha_{2}\ldots\alpha_{m}}\,dx_{\alpha_{1}}\,dx_{\alpha_{2}} \ldots dx_{\alpha_{m}}`.
  Differentials printed with commas between them keep the commas: `F\,dy_{1}, dy_{2}, \ldots, dy_{m}`.
  **Do not** write `\Sigma` for the large operator, **do not** drop printed commas, **do not** use
  `\cdots`.
- **Multiple indices keep the print's form (R23):** tight `X_{\alpha_{1}\alpha_{2}\ldots\alpha_{m}}`
  where the print has no commas, `X_{\alpha_{1}, \alpha_{2}, \ldots, \alpha_{m}}` where it has them.
  **Do not** normalize one into the other.
- **A bracketed index uses plain square brackets:** `[\alpha_{p}]`, `d[\alpha_{m+1}]`. **Do not**
  write `\lbrack` or `\left[`.
- **A continuation row's printed indent is not reproduced** in a braced two-line equation: write
  `&\pm \ldots`, **not** `&\qquad\pm \ldots`.
- **A parenthesized tuple is one object and takes ordinary comma spacing:**
  `(\alpha_{1}, \alpha_{2}, \ldots, \alpha_{m})`. The `\qquad` rule is for displayed *lists* only.

## Added after batch 7 (pp. 25–28)

- **Absolute value is plain bars:** `|y_{k}|`. **Do not** write `\lvert`, `\left|` or `\vert`.
- **The author's division colon between two displayed fractions stays a `:`** (p. 26: two Jacobians
  separated by `:`). **Do not** merge them into one `\frac`, **do not** write `\div` (R16).
- **A long dash printed as a sign name in prose ("le signe + ou le signe —") is `$+$` / `$-$`.**
  **Do not** write `---` or `—` there.
- **Superscript-indexed variables follow the superscript-first rule:** `y^{i}_{1}`,
  `y^{i+1}_{m}`.

## Added after batch 8 (pp. 29–32)

- **"C. Q. F. D." is `C.~Q.~F.~D.`** after a space at the end of the proof's last sentence, in the
  same paragraph. The print's small caps are presentation. **Do not** write `\textsc`, `\hfill`,
  `CQFD`, or put it in its own paragraph.
- **A numbered list "1°, 2°, 3°" uses a literal `°`, each item its own paragraph** (`1° Tout
  domaine…;`), keeping the printed end punctuation. **Do not** write `\textsuperscript{o}`,
  `^{\circ}`, `ᵒ`, or `enumerate`/`itemize`.
- **A "bis" reference in running text is `(13~\emph{bis})`**, matching `\tag{13 \textit{bis}}`.
  **Do not** write `(13bis)`, `(13 bis)` without the tie, or `\textit` in running text.
- **A short last row of a braced system goes in the first column** (`&y^{1}_{i} = x'_{\alpha_{i}}`);
  its printed centring is not reproduced. **Do not** pad it with empty `&&` cells or `\qquad`.
- **An upper index and a prime are different things:** `y^{1}_{1}` (upper index, superscript first)
  against `y'_{1}` (a true prime). **Do not** conflate them.
- **A heavy or double-width `==` where one equals sign is meant is written `=` with no `\ednote`**
  (pp. 13, 30): two sorts setting one sign is presentation, not a misprint of content. **Do not**
  write `==`.

## Added after batch 9 (pp. 33–36)

- **A determinant printed between bars is `\[ \begin{vmatrix} … \end{vmatrix} \]`,** rows separated
  by `\[1ex]`, a printed `…` column as its own `\ldots` cell, a dotted filler row as one `\ldots`
  per cell (however many dots the print sets), and any trailing punctuation after
  `\end{vmatrix}`. **Do not** write `\left|…\right|`, `array`, `pmatrix`, `\cdots` or `\vdots`.
  (A delimiter-free *Tableau* stays `matrix`, above.)
- **"n°" is the `\no` macro followed by a plain space:** `le \no 8`. The macro already has
  `\ignorespaces`. **Do not** write `n°`, `n\textsuperscript{o}`, or `\no~8`.
- **A minus in an index or subscript that is not visible in the scan (`v'_{p} {}_{1}` with a gap
  where `p-1` must stand) is written `-` with NO `\ednote`:** `v'_{p-1}`, `n-p`, `\theta_{q-2}`.
  *Revised after batch 26.* The small index minus is a hairline that drops out of this 1749px
  scan systematically — 15 occurrences on pp. 101–104 alone — so it records the scan's
  resolution, not a printing failure, and one note per occurrence overclaims and clutters the
  page. The pattern is documented once in provenance instead. Write the minus only where a gap is
  present **and** the index sequence requires it; otherwise transcribe what is printed. **Do
  not** write `n\ p`, `np` or `v'_{p}{}_{1}`, and **do not** ednote it. (A full-size `=`, `≡`,
  `-` or `±` that lost strokes keeps its `\ednote`, per the rules above.)
- **A prime over a stacked superscript/subscript is `x'^{0}_{1}`.** **Do not** write
  `x^{\prime 0}_{1}` or `x^{0}_{1}{}'`.
- **Old-style 3 in this font has a flat top and reads like a 5** at prepared resolution (compare
  `picard-1885`). Settle it by magnification and by sequence or cross-reference (the "second
  definition" of varieties is \S~3), and flag with `\uncertain` only if both fail.

## Added after batch 10 (pp. 37–40)

- **A small inline fraction in running text is `\frac`:** `$\frac{1}{\psi(M, M')}$` (p. 37). The
  print sets it small. **Do not** write `\dfrac` or `1/\psi(M, M')`.

## Added after batch 11 (pp. 41–44)

- **The letter-sized Σ in homologies and sums is `\Sigma`:** `\Sigma k_{i}V_{i} \backsim 0`,
  `\Sigma k'_{i}N(V, V_{i})`. It is set at letter height, not as a large operator. **Do not** write
  `\sum` for it. `\sum` is only for the large operator set in the integrals of p. 22ff.; decide
  each occurrence by the printed size.
- **A chain of homologies stays one relation as printed:**
  `\Sigma k_{i}V_{i} \backsim \Sigma k'_{i}V_{i} \backsim 0. \tag{$\alpha$}`. **Do not** split it or
  brace it.
- **An ordinal suffix on a math variable is `$p^{\text{ième}}$`.** **Do not** write `$p$ⁱᵉᵐᵉ`,
  `$p$\textsuperscript{ième}` or `p^{ieme}`. (A numeral ordinal in prose stays `4ᵉ`, above.)
- **The Greek index ν is `\nu`** (`\Phi_{\nu}`, pointed bottom, alongside α, β, γ indices); it is
  distinct from the italic variety letter `v`. **Do not** write `\Phi_{v}` or `\upsilon`.
- **A "1° … 2° …" list run inside a sentence stays inline in one paragraph.** The
  paragraph-per-item rule applies only where the print breaks the items onto separate lines.
- **An unparenthesized Greek label in prose stays bare as printed** ("des équations $\beta$"); a
  parenthesized one is `($\gamma$)`. **Do not** add or remove parentheses.
- **Subscript 1 and dotless i look alike in this font** (old-style 1 reads like ı). Decide from
  context — a particular variety is `V_{1}`, the generic index is `V_{i}` — and magnify where the
  context does not settle it.

## Added after batch 12 (pp. 45–48)

- **A subscript printed as a stacked fraction is `P_{\frac{h}{2}}`.** **Do not** write `P_{h/2}`,
  `P_{\tfrac{h}{2}}` or `P_{\dfrac{h}{2}}`.
- **After a display, a blank line (new paragraph) only where the print indents the next line**
  ("Donc" on p. 45). An unindented continuation ("mais, en changeant…", "est impair.") follows the
  `\]` with no blank line. **Do not** treat the two alike.
- **The author's phrasing "multiple de 4 + 2" is kept as printed:** `multiple de $4 + 2$`.
  **Do not** rewrite it as `4k + 2`, and **do not** ednote it.

## Added after batch 13 (pp. 49–52)

- **The face/cycle identification sign ≡ is `\equiv`:** `ABDC \equiv A'B'D'C'`; in prose,
  `le signe $\equiv$`. It is not the homology sign. **Do not** write `\backsim`, `==`, `\cong` or
  `\sim`.
- **A `≡` with only two strokes or broken fragments printed is `\equiv` with an `\ednote`** that
  strokes did not print (R29), as for `=`. **Do not** write `=`.
- **Italic centred sub-headings ("Premier exemple.") are `\subsection*{Premier exemple.}`**, period
  kept, no `\emph`. **Do not** use `\subsubsection*` (unsupported), `\emph` in the heading, or an
  italic paragraph.
- **Face and edge labels with primes are tight plain math letters:** `ABB'A'`, `DD'C'C`. **Do not**
  write `\prime` or add spaces.
- **Side-by-side coordinate tableaux form one `matrix`,** the halves separated by an empty
  `\qquad` cell, rows with `\[1ex]`. **Do not** use `array`, `pmatrix`, or two displays.
- **An unbraced list of cycles is `aligned` with rows led by `&`,** and `&&` between columns of a
  two-column list. **Do not** use `\qquad` or `gathered`.

## Added after batch 14 (pp. 53–56)

- **Dot leaders in a Tableau's label column are `\text{Premier}\ldots\ldots`** — the label in
  `\text{}`, then exactly two `\ldots`, however many dots are printed. **Do not** write `\dotfill`,
  `\text{Premier.......}` or `\cdots`, and **do not** drop the leaders.
- **A Tableau's column headers keep their printed period;** math headers are math:
  `\text{Exemple.} & q_{\alpha}. & \varphi_{\alpha}. & l_{\alpha}.`. **Do not** wrap math headers in
  `\text{}`, and **do not** drop the periods.
- **In a delimiter-free array of functions a dotted cell is `\ldots\ldots` plus that cell's printed
  punctuation** (none where the print has none). Function arguments take ordinary comma spacing,
  `(x, y, z)`. **Do not** use `\cdots`, `\vdots`, `array`, or tight `(x,y,z)`.
- **The `\qquad` list rule applies to every displayed list, whatever the printed spacing** —
  spacing is presentation.

## Added after batch 15 (pp. 57–60)

- **A substitution is written as Poincaré's tuple, a tight semicolon between old and new
  coordinates:** `(x, y, z; x + 1, y, z)`. **Do not** write `\mapsto` or `\to`, and **do not**
  set it tight `(x,y,z;x+1,y,z)`.
- **The script-looking f in the defining relations `f_{\alpha} = 0` is plain `f`.** **Do not**
  write `\int`, `\mathcal`, `\mathscr` or a long s.
- **The δ that looks like a round ∂ is `\delta`** where it is a Greek letter among α, β, γ
  (`\alpha\delta - \beta\gamma = 1`). **Do not** write `\partial` there — but keep `\partial` for
  printed round-d Jacobians (above).
- **Coordinate shorthand is displayed exactly as printed:** `\[ x; y; z = 0; 1. \]`. **Do not**
  expand it.
- **Equation numbering restarts within sections** (§ 12 opens again at (1)); tags follow the print.

## Added after batch 16 (pp. 61–64)

- **An unbraced equation printed across two lines is `\[ \begin{aligned} &first line\ &= second
  line. \end{aligned} \]`;** the continuation indent is not reproduced. **Do not** use `multline`,
  `split`, or two displays.
- **An `\ednote` about a display goes directly after the closing `\]`, never inside the math.**
- **Path labels are tight plain math letters with braced subscripts:** `M_{0}AM_{1}CM_{0}`,
  `M_{0}BM_{0}`. **Do not** add spaces or `\,` between labels, even where the print spaces them.
- **Initial and final values are `F^{0}_{a}` and `F^{1}_{a}`** (superscript first; the subscript is
  italic Latin `a`, not α). **Do not** write `F'_{a}` or `F_{a}^{0}`.
- **A product of powered substitutions is tight, superscript first:**
  `S^{k_{1}}_{1}S^{k_{2}}_{2}S^{k'_{1}}_{1}`. **Do not** write `S_{1}^{k_{1}}` or use `\cdot`.
- **A wholly italic sentence is one `\emph{…}` run including its inline math,** final period
  outside.
- **Contour equivalences of § 12–13 use `\equiv`** (`M_{0}BM_{0} \equiv 0`); a two-stroke print of
  it is still `\equiv` with an `\ednote` (above).

## Added after batch 17 (pp. 65–68)

- **Contour labels printed at the left of a conjugation list, "(C₁)", are the first aligned
  column:** `\[ \begin{aligned} &(C_{1}) &&ABDC \equiv A'B'D'C',\ … \end{aligned} \]`; a single
  labelled line is a one-row `aligned` of the same form. They name contours; they are not equation
  numbers. **Do not** use `\tag{C_{1}}`, `\qquad`, `\text{}`, or separate displays.
- **The small italic headings "Équivalences fondamentales." / "Homologies fondamentales." are
  `\subsection*{…}`,** like "Premier exemple." Their initial accent is kept exactly as printed —
  the print has both "Équivalences" and "Equivalences" (R23). **Do not** regularize.
- **A connecting word printed in the margin between two displays ("d'où", "et") is an unindented
  text line between two separate `\[ \]` displays.** **Do not** put it in `\text{}` inside the
  math, and **do not** merge the displays.
- **A displayed pair joined by "et" is `\[ 0 \qquad \text{et} \qquad C_{1}. \]`.**
- **A display broken across a page break is closed at the foot of the earlier page and reopened
  after the next `\origpage`** (no blank line), continuing the same `aligned` structure.

## Added after batches 18–19 (pp. 69–76)

- **An unbraced, unnumbered system of homologies is an unbraced `aligned` display,** rows led by
  `&`. **Do not** add `\left\{`, **do not** use `gathered`.
- **The Greek eta, which prints like "τι" or "ɳ", is `\eta`** (`\eta_{0}`); μ is `\mu`, ρ is
  `\rho`. **Do not** write `\tau`, `\iota`, `n`, `u` or `p`.
- **A determinant standing for a linear substitution uses the `vmatrix` rule:**
  `\begin{vmatrix} \alpha & \beta \[1ex] \gamma & \delta \end{vmatrix}`; a printed `= 0` or
  `\tag{2}` stays in the same display.
- **Every "ième" superscript on a math letter is `h^{\text{ième}}`,** even where the small accent
  failed to print (read as lost ink, R29). **Do not** write `h^{\text{ieme}}`.
- **A Greek label printed at the left, "(λ)", is `\tag{$\lambda$}`;** the text reference is
  `($\lambda$)`.
- **A clean two-stroke `=` printed where neighbouring lines use `≡` is kept as `=`,** without an
  ednote, unless a missing stroke is actually visible (p. 66 `4C_{1} = 0`, p. 73).

## Added after batch 20 (pp. 77–80)

- **A congruence modulus is `\qquad (\text{mod.}\ \nu)` in the same display,** keeping the printed
  "mod." with its period. **Do not** write `\pmod{\nu}`, `\bmod`, or `(\mathrm{mod}\ \nu)`.
- **An integer standing alone in prose is plain text:** "égal à 1", "déterminant 1". **Do not**
  write `$1$` there.
- **A connecting word printed at the paragraph indent before a display ("Soit") opens a new
  paragraph** with the display after it. **Do not** put it in `\text{}` in the math.
- **Two words set without a space between them are separated, with no `\ednote`**
  ("recherchessur", "nesont", "dedéterminant" → "recherches sur", "ne sont", "de déterminant").
  Word spacing is presentation. **Do not** reproduce the run-together form, and **do not** ednote
  it.

## Added after batch 21 (pp. 81–84)

- **A broken letter in prose that makes a misprint-looking word is written as the intended letter,
  with no `\ednote`** ("devia" → devra, "scrte" → sorte), as lost ink (R29). **Do not** reproduce
  the broken form, **do not** ednote it. This is for broken *letters in words*; a sign that lost
  strokes (`=`, `≡`, `-`, `±`) still gets its `\ednote`, per the rules above.
- **A minus printed as two short broken strokes is `-` with an `\ednote` after the display.** **Do
  not** write `--`, `=` or `---`.

## Added after batch 22 (pp. 85–88)

- **A system with a printed brace on both sides followed by "= 0" is
  `\[ \left\{ \begin{aligned} &row\ … \end{aligned} \right\} = 0, \tag{1} \]`,** rows without
  punctuation, as printed (p. 85). **Do not** write `\right.` with a separate `=`, use `cases` or
  `array`, or put `= 0` on every row.
- **A three-column grid of substitutions with no brace is `aligned` with `&` and `&&`:**
  `&x_{1} = y^{2}_{1}, &&x_{2} = \ldots, &&x_{3} = \ldots,\`. **Do not** use `\qquad` or `matrix`.
- **A trigonometric product is `\cos \varphi \sin \theta`.** **Do not** write `\cos(\varphi)`.

## Added after batch 23 (pp. 89–92)

- **A short last row of an unbraced grid fills its cells in order with `&`/`&&`,** whatever column
  the print sets it under. **Do not** pad with empty `&&` cells, `\qquad` or `matrix`.
- **A display ending in a comma and followed by an indented line keeps its comma and still takes a
  blank line after `\]`** (the indent rule above). **Do not** drop the comma.

## Added after batch 24 (pp. 93–96)

- **Centred result lines in running text are one plain paragraph each;** `C.~Q.~F.~D.` goes at the
  end of the last. **Do not** use `\text{}` in a display, `center`, or `\` breaks.
- **The round-d symbol standing for a product of differentials is `\partial`** (p. 94
  `\int \sum X \partial`, p. 95 "et $\partial$ le produit"), matching the Jacobian's ∂. It is not a
  Greek letter among α, β, γ, so the `\delta` rule does not apply. **Do not** write `\delta`,
  `\mathrm{d}` or `d\omega`.
- **Curly ϑ is `\vartheta`, plain θ is `\theta`, each as printed (R23):**
  `d\vartheta_{1}\,d\vartheta_{2} \ldots d\theta_{q-1}`. **Do not** regularize either way.

## Added after batch 25 (pp. 97–100)

- **A prose ellipsis between math items is text-mode `\ldots` between commas:**
  "des $v_{p-1}$, \ldots, des $v_{1}$". **Do not** write `$\ldots$`, `...` or `\dots`.
- **A title before a name takes the same tie:** `M.~l'amiral de Jonquières`.
- **An unaccented capital A for "À" is kept as printed** ("A toute variété"), R12/R23. **Do not**
  add the accent.

## Added after batch 26 (pp. 101–104)

- **A displayed list whose first item is an equation is still a `\qquad` list:**
  `\[ P_{0} = P', \qquad P_{1}, \qquad \ldots, \qquad P_{m}. \]`.
- **A text-mode `\ldots` followed by a word takes a control space:** `\ldots\ et le polyèdre`.

## Added after batch 27 (pp. 105–108)

- **A Latin equation label printed at the left, "(A)", is `\tag{A}`;** a text reference is plain
  "(B)". **Do not** write `\tag{(A)}`, `\tag{\text{A}}` or `\tag{\mathrm{A}}`.
- **A word inside a display is `\text{ ou }`:** `= 2 \text{ ou } 0,`. **Do not** leave bare italic
  "ou", **do not** split the display.
- **An ellipsis printed with only two dots is still `\ldots`,** with no ednote (dot count is
  presentation).
- **A side condition on its own centred line under an equation makes a two-row unbraced `aligned`**
  (rows led by `&`); on the same line it follows `\qquad`. **Do not** use `gathered` or two
  displays.

## Added after batch 28 (pp. 109–112)

- **The round-looking δ naming a count (`\delta_{q}`, `\delta'_{q}`, `\delta''_{q}`, beside
  `\alpha_{q}`) is `\delta`,** prime before subscript. **Do not** write `\partial` or
  `\delta_{q}''`.
- **A delimiter-free table mixing words and math is `matrix`,** words in `\text{…}`, each ditto mark
  `\text{»}`, dotted rows `\ldots\ldots` per cell without punctuation as printed. **Do not** use
  `array`, `tabular` or `aligned`, and **do not** replace » with words.
- **A staircase Tableau is one `matrix` with empty leading cells (`& &`)** so every entry stays in
  its printed column; the final period goes inside the last cell. **Do not** left-align the rows.
- **The period of a double index (`\beta_{\lambda.p}`) is written where a gap shows it and the
  scan lost it, with no ednote,** like the index minus. **Do not** write `\beta_{\lambda p}`.
- **An inline side condition set tight stays one math span with a space:** `$v_{q} (q < p)$`.
- **A heading printed in capitals keeps the accents the capitals omitted when normalized to
  sentence case:** "CAS OU p EST IMPAIR" → `\subsection*{Cas où $p$ est impair.}`. Capitals
  dropping accents is typography. In running text an unaccented capital `A` for "À" stays as
  printed (above).

## Added after batch 29 (pp. 113–116)

- **The perimeter symbol that prints like "II" is `\Pi`** (p. 116, "les $\alpha_{2}$ périmètres
  $\Pi$"). **Do not** write `II`, `\mathrm{II}` or `\prod`.
- **A displayed count followed by an unindented "si $p$ est …" line is its own `\[ \]` without
  punctuation, then the text line.** **Do not** merge such pairs into one `aligned`, and **do not**
  put "si" in `\text{}`.
