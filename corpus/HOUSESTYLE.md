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
- **Inline large operators** (∫, ∑, ∏) whose operand is a fraction use `\displaystyle` so the
  operator and the fraction are balanced: `$\displaystyle\int \frac{a^{2}\,dz}{\sqrt{a^{4}-z^{4}}}$`.
  Use `\frac`, not `\dfrac` (redundant under `\displaystyle`). (See ruling R2.)
- **Standalone formulas** go in display math `\[ ... \]` (already display style — no `\displaystyle`
  needed there).
- **Equation numbers** go on the **right**, via `\tag{n}` inside the display: `\[ ... \tag{1} \]`.
  Use the author's own numbers with `\tag` (not LaTeX auto-numbering), so the numbering matches the
  source and its in-text references. (See ruling R5.)
- **Exponents** use braces: `x^{2}`. **Differentials** get a thin space: `\,dz`.
- Text: `---` for an em-dash, `~` for a non-breaking space; `\section*{}` / `\subsection*{}` for
  headings actually present in the source.
- **Translator/editorial interpolations** in a translation use **square brackets** `[...]`,
  never parentheses — parentheses are reserved for the author's own asides, so bracketing keeps
  our voice visibly distinct from theirs: `potentia [later called vis viva]`. (See ruling R9.)

## Rulings log

Newest first. Each ruling names the layer it belongs to and the reasoning, so it isn't reopened.

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
caption is an editorial addition — allowed only as a clearly demarcated layer from `proofread`
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
print, where the ∫ spans the fraction. Write `\displaystyle\int \frac{...}{...}`. Applied in
`fagnano-1718-lemniscata`.

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
