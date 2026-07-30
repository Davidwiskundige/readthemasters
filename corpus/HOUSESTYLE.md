# Corpus house style — math typography & rulings log

This is the living reference for how we *set* the mathematics and text in a transcription. It
exists so the same typographic choice is decided **once** and reused, instead of being
re-litigated per work. When a new boundary case comes up during transcription or review, add a
ruling here rather than deciding silently.

See also: PLAN.md §4.4 (the three-layer house-style policy) and
`corpus/preamble/readmasters.sty` (the shared macros).

## The principle: notation vs presentation

Every typographic question falls into one of two buckets. Decide which, then apply the rule.

| Layer | Rule | Examples |
|---|---|---|
| **Notation & content** — *what* the mathematics says | **Faithful.** Never silently changed. | which symbols/formula; author notation like `zz` for $z^2$; archaic spelling (*abscisse*, *elisse*); the `arc.` abbreviation; printer's errors |
| **Presentation & typography** — *how* the same math is set | **House style.** Made consistent across the corpus. | display vs inline; `\displaystyle`/`\frac`; size of the ∫ sign; label styling; spacing; headings; em-dashes |

The test: *does the change alter the mathematical meaning or the author's chosen symbols?* If yes →
notation, keep it faithful. If it only changes how it looks → presentation, follow the house style.

## Math typography conventions (presentation layer)

- **Multi-letter geometric labels** (points, segments, arcs, curves — e.g. `CQ`, `ADFNA`, `DIF`)
  are written as **plain math-mode letters**: `$CQ$`, `$ADFNA$`. Do **not** wrap them in
  `\pt`/`\mathit`/`\textit`. (See ruling R1.)
- **Inline large operators** (∫, ∑, ∏) use `\displaystyle` so the operator matches the height of
  its operand instead of shrinking to a small inline glyph:
  `$\displaystyle\int \frac{a^{2}\,dz}{\sqrt{a^{4}-z^{4}}}$`. This holds **however the operand is
  written** — including the author's own `:`/`/` division sign, which stays faithful and is *not*
  rewritten to `\frac`. Under the operator use `\frac`, not `\dfrac` (redundant there). A standalone
  inline `\dfrac` with no operator is fine. (See rulings R2, R16.)
- **Standalone formulas** go in display math `\[ ... \]` (already display style — no `\displaystyle`
  needed there).
- **Equation numbers** go on the **right**, via `\tag{n}` inside the display: `\[ ... \tag{1} \]`.
  Use the author's own numbers with `\tag` (not LaTeX auto-numbering), so the numbering matches the
  source and its in-text references. (See ruling R5.)
- **Exponents** use braces: `x^{2}`. **Differentials** get a thin space: `\,dz`.
- Text: `---` for an em-dash, `~` for a non-breaking space, and a LaTeX control space `\ ` after an
  abbreviation dot (`v.\ g.`, `Apr.\ pag.`) — all resolve to normal spaces on the web; `\section*{}`
  / `\subsection*{}` for headings actually present in the source. (See ruling R17.)
- **Translator/editorial interpolations** in a translation use **square brackets** `[...]`,
  never parentheses — parentheses are reserved for the author's own asides, so bracketing keeps
  our voice visibly distinct from theirs: `potentia [later called vis viva]`. (See ruling R9.)

## Rulings log

Newest first. Each ruling names the layer it belongs to and the reasoning, so it isn't reopened.

### R18 — Author markup must match what the site actually renders: the `significance` field is
### plain text + KaTeX only, and the `.tex` transform has no `\oe` (use a literal `œ`) (presentation)
*2026-07-30.* Two site-rendering limits surfaced while previewing
`jacob-bernoulli-1694-constructio-lemniscata` (the first work to name the lemniscate, whose text
carries the author's embedded French phrase "nœud"). Both are presentation-layer — they change only
how the same text is set — and neither is caught by `validate.py`, `texcompare.py`, or
`houselint.py`, so **preview a new work in the site before opening the PR** to catch leaked markup.

- The `work.yaml` **`significance`** note is rendered by `renderSignificance()` in
  `site/src/pages/works/[id].astro`, which only HTML-escapes the prose and expands `[n]` citation
  markers; a later client-side KaTeX pass renders `$...$`. It does **not** run the `.tex` text
  transform, so `\emph{}`, `~`, and `---` leak as literal characters. **Rule: write `significance`
  as plain prose — a real em-dash `—`, a plain "No. LX", no `\emph`; only `$...$` math is processed.**
- The transcription/translation `.tex` panels go through `inlineText()` in `site/src/lib/tex.js`,
  which supports `\emph`/`\textit`, `\textbf`, `\uncertain`, `\illegible`, `\ednote`, `\&`, `\ `,
  `~`, `---`, and `` `` ''`` — but **not** accent/ligature macros such as `\oe`. **Rule: render such
  a letter as the literal Unicode character (`œ`, not `\oe{}`).** This is consistent with existing
  corpus `.tex` bodies that already use literal UTF-8 (e.g. Fagnano's "ànno"): Tectonic/XeTeX
  compiles the character for the PDF, and the site's `escapeHtml` passes it through unchanged.

Applied in `jacob-bernoulli-1694-constructio-lemniscata`.

### R17 — LaTeX control spaces (`\ `) after abbreviations render as a normal space on the web
### (presentation)
*2026-07-30.* Faithful transcriptions keep the source's abbreviation spacing by writing a LaTeX
control space after the dot — `v.\ g.`, `Apr.\ pag.`, `scil.\ spatiolum`, `Num.\ sequentem`,
`Tr.\ ` — so a real TeX engine sets an inter-word (not inter-sentence) space and the `.tex` stays
correct for the PDF. The reader's LaTeX→HTML transform (`site/src/lib/tex.js`) previously left the
`\ ` untouched, so a literal backslash leaked into the running text. It now maps a **text** `\ ` to
a single space (math spans are masked first, so a `\ ` inside `$...$` still reaches KaTeX). Covered
by `site/src/lib/tex.test.mjs` (`npm test`, run in CI) so the transform can't regress. Surfaced and
fixed in `jacob-bernoulli-1694-isochrona-elastica`.

### R16 — *Every* inline large operator uses `\displaystyle`, and the check now covers the
### `significance` note too (presentation, extends R2)
*2026-07-30.* R2 balanced an inline `\int` only against a `\frac` integrand, but Jacob Bernoulli
sets his integrals with the author's own `:`/`/` division sign (`$\int(a\,dz : \sqrt{...})$`), and
one such integral sat in the work's `significance` note — both rendered as a tiny inline ∫ that R2's
fraction-gated rule never caught. The rule is therefore widened: **any inline large operator
(`\int`, `\sum`, `\prod`) must carry `\displaystyle`**, whatever its operand looks like, and the
author's division sign is left faithful (not rewritten to `\frac`). **Machine-enforced:**
`pipeline/houselint.py` now flags any inline large operator lacking `\displaystyle`, and
`validate.py` runs the linter over the `significance` field of `work.yaml` as well as every `.tex`.
A standalone inline `\dfrac` with no operator is still fine — Leibniz's `$\frac{4}{9}$` and Euler's
`$\dfrac{m\,dx}{\sqrt{1-x^4}}$` are unaffected. Applied in
`jacob-bernoulli-1694-isochrona-elastica`.

### R15 — The Opera edition's lettered footnotes are placed inline as complete units at the end
### of each page (presentation)
*2026-07-29.* Jacob Bernoulli's *Solutio Problematis Leibnitiani*
(`jacob-bernoulli-1694-isochrona-elastica`) carries long two-column analytic footnotes (a)–(m) at
the foot of each printed page. On the web there is no foot-of-page, so each note is placed inline as
a **complete unit at the end of its page's main text**, led by a bold letter (`\textbf{(b)}`), while
the in-text reference stays a superscript `${}^{(b)}$`. A note that physically runs onto the next
printed page in the source is given whole at the page where it begins. This mirrors R8 (relocating
apparatus for web reading while `\origpage` preserves provenance). Whether the notes are the
author's own or the 1744 editor's (Gabriel Cramer) is a separate content question, flagged per work.

### R14 — The et-ligature "&" is kept, not expanded, and rendered by the site (notation, with
### presentation support)
*2026-07-29.* Early-modern printing sets "and" as the ampersand "&" (an *et*-ligature), and "&c."
for "et cetera". These are kept exactly as printed (faithful — R3), written in the `.tex` as the
LaTeX-escaped `\&` so the file still compiles under a real engine. The reader's LaTeX→HTML transform
(`site/src/lib/tex.js`) was extended to render a **text** `\&` as `&`, and to run
`\section*`/`\subsection*` headings through the same text pipeline (so `~` and `\&` also resolve in
headings); a `\&` **inside math** is left untouched, since KaTeX already renders it (the transform
masks math spans before applying text substitutions). First applied in
`jacob-bernoulli-1694-isochrona-elastica`, the first corpus work with a text ampersand.

### R13 — Fraktur letters used as *mathematical variables* are preserved with `\mathfrak`, not
### normalized to roman (notation/content, not typography)
*2026-07-25.* Euler's E251 §32 introduces a second set of coefficients in **Fraktur**
($\mathfrak{A},\mathfrak{B},\mathfrak{C},\mathfrak{D},\mathfrak{E}$) that are *distinct variables*
from the roman $A,B,C,D,E$ used in the same passage. The general "normalize Fraktur/blackletter to
normal letters" rule (transcribe-chat, for long-ſ and German prose set in Fraktur *type*) does
**not** apply here: normalizing would conflate two different variables and destroy the
mathematics. The test (does the change alter meaning?) says these are notation. **Rule: Fraktur
that is a mere typeface for text is normalized to roman; Fraktur that names a distinct mathematical
symbol is preserved with `\mathfrak{...}`** (KaTeX- and Tectonic-supported). Applied in
`euler-1761-integratione-aequationis`.

### R12 — Original-edition u/v/i/j orthography is kept faithfully; only glyph *shapes* are
### normalized (notation/content, not presentation)
*2026-07-25.* Transcribing Euler's E251 from the **original 1761 printing** (Novi Commentarii VI)
raised whether the era's letter conventions — capital `V` for `U` (`EVLERO`, `AEQVATIONIS`), no
`u`/`v` distinction (`inuentionum`, `vt`, `vti`, `inuoluere`), and `i`/`j` usage — should be
modernized. **Decision: keep them exactly as printed.** These are the source edition's spelling,
which R3 protects as content, not a glyph *shape* to be normalized. What we still normalize is only
the shape of a letter that no longer exists (long-ſ → s), ligatures, and Fraktur/blackletter — not
the choice of which letter (`u` vs `v`, `i` vs `j`) was set. The rule is therefore: **transcribe
faithful to the orthography of the specific edition being transcribed.** This legitimately makes
different works differ: `leibniz-1689-isochrona` reads in modern `u/v/j` because its *source* (the
Gerhardt 1858 reprint) was already modernized — not because we modernized it — whereas Euler from
the 1761 original keeps `vt`/`EVLERO`. Applied in `euler-1761-integratione-aequationis`.

### R11 — Significance notes get the same care as the transcription, plus a contributor pass
### before they're settled (editorial content, not the notation/presentation split)
*2026-07-22.* Drafting the `significance` paragraphs for `fagnano-1718-lemniscata` and
`fagnano-1718-lemniscata-ii` took many rounds of correction: a claim about which sketch contains
which result turned out to be backwards; a quote ("the birthday of the theory of elliptic
functions") was first attributed to the wrong person (Weil recounts it — Jacobi said it);
`[[wiki-link]]` syntax — the memory-file cross-reference convention — leaked into corpus prose and
rendered as literal text on the site; and citation numbers went stale once after a cited source
was cut from the text. Rules going forward:
- Verify *what result is in which work* against the transcribed `original.tex`/scan itself, not
  from general knowledge or by echoing the sibling work's blurb.
- When attributing a claim or turn of phrase, check who actually said it versus who is merely
  reporting/recounting it — don't collapse the two into one citation.
- Never use `[[...]]` in corpus text — that syntax is for the assistant's own memory files only;
  the site renders it as literal brackets. Cross-reference other works by name/id in plain prose.
- `[n]` markers in `significance` are positional to `significance_sources`, in list order; adding
  or removing a source means renumbering every marker in the prose to match.
- For a multi-part work (a "Schediasma I/II" pair, etc.), draft or revise all parts' significance
  together, re-reading each one after editing the other, so they stay complementary instead of
  quietly drifting apart or repeating each other.
- Treat the first draft as a draft: `significance` is editorial commentary the project is adding,
  not transcribed text, so — unlike the source material — it doesn't get "faithful, don't touch"
  protection. Expect a contributor (ideally one with domain knowledge) to read it over before
  treating it as settled.

### R10 — An in-text figure reference with no locatable plate gets an inline `\ednote`, not a
### silently dangling citation (notation, with a presentation fallback)
*2026-07-20.* Leibniz's paper cites "(fig.~116)", but no plate for it survives in the scanned
Gerhardt edition (checked to the end of the 450-leaf volume: no plates section). Rather than leave
the reference dangling with nothing for the reader to find, both the transcription and the
translation add `\ednote{...}` immediately after the citation, stating plainly that the plate
could not be located in the available scans and is not reproduced. This is our own honest
gap-flag, not a reconstruction of the figure — we do not attempt to redraw or infer it. This was
also the first real use of `\ednote{}`, which until now had no rendering on the website; it now
shows as a small muted marker (a footnote-style symbol) that reveals the note only on hover or
click — the same popover mechanism used for significance citations, generalised as `.pop` /
`.pop-marker` / `.pop-content` (see `site/src/lib/tex.js` and the work page's shared JS/CSS), so
the note stays out of the way of the author's own text until the reader asks for it.
Applied in `leibniz-1689-isochrona`.

### R9 — Prefer a literal translation of a period technical term over an inline gloss; if a gloss
### is used at all, bracket it (notation, with a presentation fallback)
*2026-07-20, revised 2026-07-20.* Leibniz's "potentia" was first rendered with an inline gloss,
"potentia (later called vis viva)". On reflection this was reversed: the translation renders
period technical terms **literally** ("potentia", untranslated and unglossed) so the reader meets
the author's own term directly; historical context (that it was later called vis viva, and why it
matters) belongs in the editorial **significance** note, not inside the translation. This keeps
the translation itself faithful to the author's wording rather than layering explanation into it.
If a genuinely necessary inline gloss ever comes up, use **square brackets**, not parentheses —
the author himself uses parentheses for his own asides throughout this text, so a parenthetical
gloss would read as if it were his. Applied in `leibniz-1689-isochrona`.

### R8 — Figures are placed inline at first reference, not collected at the end (presentation)
*2026-07-19.* The original prints figures on plates at the back of the volume — a letterpress/
engraving printing constraint, not authorial intent. On the web there is no such constraint, so we
place each figure inline at its first reference for reading flow. Provenance is preserved: the alt
text names the source plate (Tav. II / III) and the `\origpage` markers keep the pagination
traceable. A separate "plates" appendix view is a possible future addition, not needed now.

### R7 — Figure captions show only the original's label; description goes in alt text (notation)
*2026-07-19.* The original plates carry no caption, only a figure number ("Fig. 24"). So the
**visible** `\rmfigure` caption is just that number (faithful); any editorial description of what
the figure shows goes in the **alt text** (accessibility), not on the page. A richer visible
caption is an editorial addition — allowed only as a clearly demarcated layer from `skimmed`
onward, never in an `ai-draft`. Applied in `fagnano-1718-lemniscata`.

### R6 — Figures are scan crops embedded via `\rmfigure`, placed at first reference (presentation)
*2026-07-19.* Figures are cropped from the original plate (never redrawn) and embedded with
`\rmfigure{figures/fig-N.png}{caption}{alt}`. Plates that live at the back of the volume are placed
in the transcription **at the point of first reference**. The Italian caption is a brief editorial
label naming the curves; the alt text (English) notes the source plate. Applied in
`fagnano-1718-lemniscata` (fig. 24 = Tav. II, djvu p. 497; fig. 25 = Tav. III, djvu p. 499).

### R5 — Equation numbers on the right via `\tag{n}` (presentation)
*2026-07-19.* The source prints equation numbers on the left, before the formula; modern LaTeX
sets them on the right. Number *position* is presentation, so we follow the modern convention:
`\[ ... \tag{n} \]`. The number *itself* is faithful (the text refers to it), so we force the
author's number with `\tag` rather than auto-numbering. Applied in `fagnano-1718-lemniscata`.

### R2 — Inline integrals with a fraction integrand use `\displaystyle` (presentation)
*2026-07-19.* A large `\dfrac` next to a small inline `\int` looks unbalanced and unlike the
print, where the ∫ spans the fraction. Write `\displaystyle\int \frac{...}{...}` (and `\frac`, not
`\dfrac`, since it is redundant under `\displaystyle`). Applied in `fagnano-1718-lemniscata` and
`euler-1761-integratione-aequationis` (both the transcription and the English translation).
**Machine-enforced:** `pipeline/houselint.py` flags an inline integral over a fraction that lacks
`\displaystyle` (or that uses `\dfrac`), and `validate.py` runs it in the gate — so a regression
cannot merge.

### R1 — Multi-letter labels stay plain math letters (presentation)
*2026-07-19.* `\pt{}` (→ `\mathit`) was tried to tighten the spacing of labels like `CQACFC`, then
**rejected**: it reads too differently from how mathematics is normally set, and the plain
math-mode rendering is the familiar convention. Labels are plain `$CQ$` etc.; no wrapper macro.
Do not reintroduce `\pt`.

### R3 — Author notation is faithful (notation)
*2026-07-19.* Keep the author's notation exactly where the print uses it: `zz` for $z^2$, archaic
spelling (*ànno*, *Bernulli*, *abscisse*, *elisse*), abbreviations (`arc.`). These are content, not
presentation.

### R4 — Printer's errors are kept and flagged, not silently fixed (notation)
*2026-07-19.* Reproduce apparent misprints faithfully (e.g. Fagnano eq. (2) denominator
`\sqrt{a^{2}-az}`, which differs from `\sqrt{a^{2}-z^{2}}` elsewhere) and note them in the file
header / provenance for a reviewer, rather than correcting them in the transcription.
