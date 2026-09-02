# House style — transcription extract

**What this is.** The rulings from `corpus/HOUSESTYLE.md` that bear on *transcribing a page*, in
operative form. `HOUSESTYLE.md` is ~37KB (~10k tokens) and most of it argues site-rendering
questions a page transcriber never faces; every batch subagent would re-read all of it. This
extract is what the `/transcribe` skill sends instead (~4k tokens).

**Authority.** `corpus/HOUSESTYLE.md` remains authoritative. This file restates, never amends. If
the two ever disagree, HOUSESTYLE wins and this file is the bug. Rulings omitted here are
site-rendering or editorial-workflow rulings with no bearing on a transcribed page: R9, R11, R21,
R26, and the site-internals half of R25.

---

## The principle: notation vs presentation

Every typographic question is one of two things. Decide which, then apply the rule.

| Layer | Rule | Examples |
|---|---|---|
| **Notation & content** — *what* the mathematics says | **Faithful.** Never silently changed. | which symbols and formulas; author notation like `zz` for $z^2$; archaic spelling (*abscisse*, *elisse*); the `arc.` abbreviation; printer's errors |
| **Presentation & typography** — *how* the same math is set | **House style.** Consistent across the corpus. | display vs inline; `\displaystyle` / `\frac`; size of the ∫ sign; label styling; spacing; headings; em-dashes |

The test: *does the change alter the mathematical meaning or the author's chosen symbols?* If yes →
notation, keep it faithful. If it only changes how it looks → presentation, follow house style.

---

## Math typography

- **Multi-letter geometric labels** (points, segments, arcs, curves — `CQ`, `ADFNA`, `DIF`) are
  plain math-mode letters: `$CQ$`, `$ADFNA$`. Never `\pt`, `\mathit`, or `\textit` around them.
  **Do not reintroduce `\pt`** — it was tried and rejected. (R1)
- **Every inline large operator** (`\int`, `\sum`, `\prod`) carries `\displaystyle`, whatever its
  operand looks like: `$\displaystyle\int \frac{a^{2}\,dz}{\sqrt{a^{4}-z^{4}}}$`. This is
  machine-enforced by `pipeline/houselint.py`. Under the operator use `\frac`, **not** `\dfrac`
  (redundant there). A standalone inline `\dfrac` with no operator is fine. (R2, R16)
- **The author's own division sign stays faithful.** If the print writes `∫(a dz : √…)`, transcribe
  `$\displaystyle\int(a\,dz : \sqrt{...})$` — add the `\displaystyle`, do **not** rewrite the `:` or
  `/` into a `\frac`. (R16)
- **Standalone formulas** go in display math `\[ ... \]`. Display math is already display style, so
  no `\displaystyle` there.
- **Equation numbers go on the right, via `\tag{n}` inside the display**, even where the print sets
  them on the left — number *position* is presentation. The number *itself* is faithful: force the
  author's own number with `\tag{}`, never LaTeX auto-numbering, so in-text references match. If
  the print writes the number with a trailing period, keep it: `\tag{12.}`. (R5)
- **Exponents use braces**: `x^{2}`. **Differentials get a thin space**: `\,dz`.
- Text: `---` for an em-dash, `~` for a non-breaking space, and a LaTeX control space `\ ` after an
  abbreviation dot (`v.\ g.`, `Apr.\ pag.`, `scil.\ spatiolum`). All three render as normal spaces
  on the web. (R17)

---

## Faithfulness rules

- **Author notation is faithful** (R3). Keep `zz` for $z^2$, archaic spelling (*ànno*, *Bernulli*,
  *abscisse*, *elisse*), abbreviations (`arc.`). Content, not presentation.
- **Printer's errors are kept and flagged, never silently fixed** (R4). Reproduce the misprint
  exactly, and report it so it reaches the file header / provenance. Do not correct the author.
- **Before deciding a mark was ADDED, check whether ink is MISSING nearby** (R29). Letterpress
  fails by dropping ink, not only by setting the wrong sort, and a letter that breaks up leaves
  fragments that read as separate marks. "The mark is cleanly inked and at the right height,
  therefore it is type" is *not* a sufficient test — it cannot tell ink that was put there from ink
  left behind when a neighbouring glyph broke.
  *Measured failure:* Noether 1869 p. 301 appears to set `F'` where the paper writes plain `F`
  everywhere else. Three independent passes — two transcribing batches and a verification pass —
  each applied that test, each concluded it was real type, and each was wrong: ink is missing from
  the top of the `F` and the surviving fragment of its upper arm reads as a prime. Because all
  three shared the same flawed test, their agreement made the wrong answer look *better* supported.
  **When a mark appears exactly once on a symbol that is plain throughout a work, suspect damage to
  the adjacent glyph before you suspect a deliberate mark** — and say so in your report rather than
  reproducing it silently under R4.
- **Edition orthography is kept exactly as printed** (R12). Capital `V` for `U` (`EVLERO`,
  `AEQVATIONIS`), no `u`/`v` distinction (`inuentionum`, `vt`, `vti`), period `i`/`j` usage,
  edition spelling (`Ueber` not `Über`, `Coefficienten`, `Function`, `nemliche`). What *is*
  normalized is only the **shape** of a letter that no longer exists — long-ſ, ligatures,
  blackletter *type* — never the choice of which letter was set. Transcribe faithful to the
  orthography of the specific edition in front of you; two corpus works legitimately differ here.
- **Inconsistency in the print is reproduced, not regularized** (R23). Where an author writes
  `θ(y)` in one line and `θy` in the next for the same function, follow each occurrence as printed.
  Confirm it is real (compare several occurrences on the page) rather than a scan artifact — then
  keep it. Silently imposing one form is what a later re-setting did, and it is a loss.
- **The et-ligature `&` is kept, not expanded** (R14). Write it `\&` so the file still compiles;
  `&c.` stays `&c.` A `\&` inside math is left alone.

---

## Typeface normalization

- **Long-ſ → `s`; ligatures expanded; umlauts as literal `ä ö ü`.** (R19)
- **The German eszett**: a terminal `ſs` ligature is rendered `ß` (`daſs`→`daß`, `muſs`→`muß`,
  `Gröſse`→`Größe`), because `ſs` is the glyph *shape* of `ß`. A genuine double-s is set `ſſ` and
  stays `ss` (`müssen`, `gewisse`). **Check the print first** — an Antiqua German print that sets
  round s throughout has nothing to convert, and then the file correctly contains no `ß` at all.
  Record that as a `notation.md` entry (R27), not as an exception to R19.
- **Fraktur splits in two** (R13). Fraktur as a mere *typeface* for prose is normalized to roman.
  Fraktur that names a **distinct mathematical variable** — Euler's
  $\mathfrak{A},\mathfrak{B},\mathfrak{C}$ standing alongside a roman $A,B,C$ in the same passage —
  is preserved with `\mathfrak{...}`, because normalizing it would conflate two different variables
  and destroy the mathematics.
- **Letterspaced emphasis (Sperrung) is rendered `\emph`** (R20). Author names in Sperrung are
  `\emph`'d too. Identifying letterspacing is a per-instance reading of the scan, so it is a
  best-effort pass — say so in your report.
- **Where a print uses two emphasis devices** — italic for stress *and* letterspacing for names —
  **both collapse to `\emph`**, and which passage carried which device is recorded in the file
  header comment instead. Do not press `\textbf` into service for one of them. A letterspaced name
  falling inside an italic run is set as one `\emph` run, not split. (R24)
- **Accented and special letters are written as literal Unicode**, not macros: `œ` not `\oe{}`,
  `ß ä ö ü` not `\ss`/`\"a`, `«» „ "` as themselves. The site's transform has no `\oe`. (R18, R22)
- **A quotation whose opening mark is repeated at the start of every printed line** collapses to a
  single opening/closing pair — that repetition is a line-break artifact of the print, and
  transcription already reflows lines. Use the **edition's own** quotation glyph as literal
  Unicode: French guillemets `«…»`, German low quotes `„…"`. (R22)

---

## Structure on the page

- **Headings** use `\section*{}` / `\subsection*{}`, and only where the source actually has a
  heading.
- **A heading may contain math (`$\omega$`) but never a text-mode brace group.** The site matches a
  heading's argument with `[^}]*`, so `\section*{Theorie der \emph{Abel}'schen Functionen.}` ends
  the heading at `\emph{Abel}` and silently leaks the tail into the next paragraph. A heading needs
  no `\emph` anyway — R20 rules that the heading's own face carries its prominence. Write
  `\section*{Theorie der Abel'schen Functionen.}` even where the print italicizes the name.
  (R25, R20)
- **The same brace limit applies inside `\ednote{...}` and `\uncertain{...}`**: no text-mode macro
  with an argument. Math is safe (`$\sqrt{X}$` inside a note is fine, because math spans are stashed
  first), but `\emph{...}` inside a note ends the note at the first `}` and leaks the rest into the
  running text. Write the emphasis as plain words or `` `` '' `` quotes instead. `houselint.py`
  flags this, including an escaped `\}`. (R18)
- **Figures are never redrawn.** Emit `\rmfigure{figures/fig-N.png}{<the original's label only>}{<alt
  text>}`; the crop is made separately from the scan. Place the figure **inline at its first
  reference**, even where the print collects plates at the back — that was a letterpress
  constraint, and `\origpage` keeps the pagination traceable. The visible caption carries **only**
  the original's own label ("Fig. 24"); any description of what the figure shows goes in the alt
  text. A richer visible caption is an editorial addition, never allowed in an `ai-draft`.
  (R6, R7, R8)
- **A figure reference whose plate cannot be located** gets an inline `\ednote{...}` immediately
  after the citation, stating plainly that the plate is not in the available scans and is not
  reproduced. Never reconstruct or infer the figure. (R10)
- **Footnotes**: where the print sets lettered or numbered notes at the foot of the page, place each
  note inline as a **complete unit at the end of that page's main text**, led by a bold letter
  (`\textbf{(b)}`), with the in-text reference kept as a superscript `${}^{(b)}$`. A note that runs
  onto the next printed page is given whole at the page where it begins. (R15)
- **Running heads, page numbers and signature marks are page furniture and are not transcribed.**

---

## Cross-page decisions — `notation.md` (R27)

A decision that must hold across the **whole work** — which glyph a recurring sign is, whether a
house-style ruling applies to this print at all, how a symbol is disambiguated from its neighbour —
belongs in `corpus/<work-id>/notation.md`, a permanent committed artifact. It does not belong in a
transcriber's memory, and batches cannot see each other.

This is not hypothetical. Two batches of the same work, same model, same scans, disagreed on that
work's most frequent symbol: one wrote `\sum` 19 times where the rest of the work uses the Sigma
*letter* `\Sigma`. Given the glossary, a later batch got it right 19 times out of 19.

**Write each entry exactly, and name the forbidden alternatives.** A vague entry is worse than none,
because it licenses a *new* divergence while looking like guidance — an entry saying only that
spacing "is normalized" produced 11 spaced dots where the work sets 63 tight ones. Record the
decision, one line of why, and what **not** to write instead.

An author's own back-reference (`Gleichung (3)`, `équation (92)`) is printed on the page you are
transcribing and is copied verbatim. It is not a notation decision.
