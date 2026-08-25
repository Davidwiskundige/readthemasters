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

### R24 — When a print uses TWO emphasis devices (italic and letterspacing), both collapse to
### `\emph`, and the distinction is recorded in the file header instead (presentation)
*2026-08-25.* R20 mapped German letterspacing (Sperrung) to `\emph` for a print — Abel's 1826 paper
— where Sperrung was the *only* emphasis device in use. Jacobi's 1832 Crelle note
(`jacobi-1832-considerationes`) is the first corpus work whose print uses **both**: italic for the
author's own stress (terms he is defining, whole quoted theorem statements, *theorematis Abeliani*,
*periodo duplici et reali et imaginaria*) and letterspacing for **personal names**
(E u l e r u s, L a n d e n, L e g e n d r e, A b e l, F o u r r i e r, L a g r a n g e). The site's
LaTeX→HTML transform renders exactly one emphasis, `\emph` → `<em>`, so the two devices cannot be
kept apart on the page. **Rule: render both with `\emph`, and state in the transcription's header
comment which passages carried which device**, so the information is preserved in the corpus even
though the rendering flattens it. Rejected alternatives: dropping the name-marking entirely (loses
a device the print actually uses), and pressing `\textbf` into service for one of them (bold is
far heavier than letterspacing and would misrepresent the page). One consequence, also applied
here: where a letterspaced name falls **inside** an italic passage ("demonstratum est a Cl. Abel,
dato numero…", with "Cl. Abel" upright-letterspaced inside the italic run), the passage is set as a
single `\emph` run rather than being split — both halves would render identically anyway.

### R23 — The 1841 original's function-application notation — parenthesized `θ(y)` versus bare
### `θy` for the *same* symbol — is itself inconsistent, and is followed exactly per occurrence,
### not normalized to one form (notation)
*2026-08-22.* Abel's Paris memoir, transcribed from the 1841 original (Mémoires présentés par
divers savants, not the 1881 Oeuvres complètes re-setting — see R22), does not apply a single
convention for writing "apply this function to this argument." Some functions are parenthesized
from their first appearance and stay that way — `θ(y)`, `χ(y)`, `φ(x)`, two-argument `f(x,y)`
always. Others are bare from their first appearance and stay that way — `Fx`, `F_0x`, `F'x`,
`θ_1x`. But several — `θy` itself chief among them — genuinely switch mid-passage: a restated
formula keeps the parens of its first statement, while the very next line of new derivation drops
them, within the same paragraph, by the same compositor. This was checked and confirmed to be a
real feature of the print (not a scan artifact) by comparing multiple occurrences on the same
page. Rather than silently imposing one form throughout (which is what the 1881 Oeuvres complètes
re-setting did, uniformly dropping the parentheses — see R22), this transcription reproduces
whichever form is printed at each specific occurrence, since the notation is what the author's
edition actually shows and "which of two equivalent notations" is content here, not typesetting to
be regularized. Applied throughout `abel-1841-fonctions-transcendantes`.

### R22 — A quoted theorem statement printed with a repeated opening quotation mark at the start
### of every typeset line collapses to a single opening/closing pair; use the edition's own
### quotation glyph, as literal Unicode (presentation)
*2026-08-21, revised 2026-08-22.* Abel's Paris memoir (`abel-1841-fonctions-transcendantes`) prints
two verbatim theorem statements with the 19th-century convention of repeating the opening
quotation mark at the start of *every* printed line of the quotation, closing only once at the
very end. That repetition exists solely to mark, line by line, that the quotation continues — a
page-layout artifact of the print's line breaks, which the transcription already drops when it
reflows text into paragraphs (transcribe-chat rule 2). Collapsing it to a single opening/closing
pair preserves the quoted content exactly, following the same "drop the line-break artifact" logic
already applied to hyphenation.

The glyph itself is notation, not presentation, and is edition-specific (R12): the memoir's true
first printing, Mémoires présentés par divers savants, t. VII (Paris, 1841) — consulted on Gallica,
ark:/12148/bpt6k33126 — sets the quotation in French guillemets «...» (repeated « at each line);
the later Oeuvres complètes re-setting (Sylow & Lie, 1881) re-typeset the same quotation in
German/Scandinavian-style low quotes „...", also repeated per line. Since this work transcribes
the 1841 original, it uses «...», written as literal Unicode characters (not a macro): consistent
with R18's rule for `œ` — `tex.js`'s `escapeHtml` passes `«`/`»` through unchanged, and XeTeX
compiles them directly. (An earlier draft of this ruling, before the source edition was switched
from the 1881 reprint to the 1841 original, used `` ... '' for the low-quote glyph; superseded.)
Applied in `abel-1841-fonctions-transcendantes`.

### R21 — Prose inside a `\text{...}` insert in a formula is translated like any other prose; the
### math-preservation check ignores its content (translation policy; presentation)
*2026-08-21.* A translation must reproduce every formula verbatim, but a formula sometimes carries
**prose** inside a text insert: Abel joins two displayed equations with `\text{ und }`, glosses one
with `\text{ oder}`, and writes ordinals as `\mu^{\text{ten}}` ("μ-ten" = "μ-th"); Euler uses
`\text{et}` / `\text{seu}`. That prose is language, not mathematics, so it is **translated** —
`\text{ und }`→`\text{ and }`, `\text{ oder}`→`\text{ or}`, `\text{seu}`→`\text{or}`,
`\mu^{\text{ten}}`→`\mu^{\text{th}}` — rather than left in the source language. (This reverses an
earlier ad-hoc choice, first taken in the Euler translation, to leave such words untranslated
"because they live inside the preserved formula".)
- **Machine-enforced boundary.** `pipeline/texcompare.py` now neutralizes the *content* of a text
  insert (`\text`, `\textrm`, `\textnormal`, `\textup`, `\textit`, `\textbf`, `\textsf`, `\texttt`,
  `\mbox`, `\hbox`) before comparing, so translating the words is allowed — but it keeps the insert
  itself (as `\text{}`) so the check still requires each insert to be **present, un-added, and not
  repositioned**, and all surrounding math to be identical. `\operatorname{...}` is deliberately
  **excluded** (it names a mathematical operator, e.g. `\operatorname{arc}`, not translatable
  prose). Covered by `pipeline/tests/test_texcompare.py`.
- The rule lives in `prompts/translate-chat.md` (rule 1) and the translate skill; it does not change
  the transcription — the original keeps the author's own words (`\text{ und }`, `\text{ten}`).
Applied retroactively to the `en` translations of `abel-1826-unmoeglichkeit` and
`euler-1761-integratione-aequationis`.

### R20 — German letterspaced emphasis (Sperrung) is rendered `\emph`; letterspaced section
### titles stay headings (presentation)
*2026-08-21.* Abel's 1826 paper stresses words by **letterspacing** (Sperrung, "g a n z e") — the
Fraktur-era equivalent of italics — throughout: `algebraisch rational`, `Versetzung`, `ganze
Function`, `kleiner als fünf ist`, `von der ersten Ordnung`, etc. Emphasis is presentation (it does
not change the author's words or their meaning), so it follows house style: **inline Sperrung is
rendered `\emph`** (italic on the web via `tex.js` → `<em>`, R14/R18), matching how the Latin/Italian
corpus works already set emphasis. Two boundary calls:
- **Section/paragraph titles are also letterspaced in the print, but stay headings** (`\subsection*`)
  and are *not* additionally `\emph`'d — the heading markup already carries their prominence, so the
  two uses of the same device are deliberately *not* treated identically.
- **Author names set in Sperrung** (e.g. `Cauchy`) are `\emph`'d too, consistent with the device.
Because identifying every letterspaced word is a per-instance reading of the scan (the same word is
spaced in one place and not another, and short words are subtle), the Sperrung→`\emph` mapping is a
**best-effort pass, flagged in provenance for human verification**. Applied in
`abel-1826-unmoeglichkeit`.

### R19 — German long-ſ is rendered `s` and the eszett ligature `ſs` is rendered `ß`; the site now
### maps `\S` → `§` (presentation; a German-language application of R12)
*2026-08-21.* `abel-1826-unmoeglichkeit` (Abel's 1826 impossibility proof, Crelle Band 1) is the
corpus's first German-language work. **Note on the typeface:** contrary to a first assumption, this
paper is set in **Antiqua (roman type), not Fraktur** — the letterforms are upright roman; only the
long-ſ, the `ſs` eszett ligature, and letterspaced emphasis (Sperrung, see R20) are period features.
So no Fraktur→roman conversion was needed here, and there is **no Fraktur in the math** either
(variables are ordinary italic), so **`\mathfrak` is not used** (contrast R13/Euler, where Fraktur
letters were *distinct* math variables). The two normalizations that *did* apply, per the transcribe
rule and R12 (normalize glyph *shape*, keep orthography faithful):
- `ſ` → `s`; ligatures expanded; umlauts as `ä ö ü`.
- The terminal-s **eszett** is written `ſs` (long-s + round-s): `daſs`, `muſs`, `Gröſse`, `heiſst`,
  `läſst` → rendered **`ß`** (`daß`, `muß`, `Größe`, `heißt`, `läßt`), not `ss`, because `ſs` is the
  glyph *shape* of `ß`. A genuine double-s is set `ſſ` and stays `ss` (`müssen`, `gewisse`).
For a *future* German work actually set in Fraktur, the same rule extends: normalize blackletter to
roman for prose, but keep Fraktur that names a distinct math variable with `\mathfrak` (R13).
What is *not* changed (R12, content): edition spelling — `Ueber` (not `Über`), `nemliche`/`nämliche`,
`grade`/`ungrade`, `Coefficienten`, `Function`, `Primzahl`, `irreductibel`. `ß ä ö ü` are written as
literal UTF-8 (R18: `escapeHtml` passes them through, Tectonic/XeTeX compiles them); no `\ss`/`\"a`.
**Site support for `\S`:** the section sign was needed for the `§`-numbered headings and `(§. II.)`
cross-references. `tex.js` `inlineText` now maps a text-mode **`\S` → `§`** (scoped so it cannot eat
a longer control word; math `\Sigma` is stashed and untouched), covered by `tex.test.mjs`. This work
uses a **literal `§`** in both the `.tex` body and the `significance` field (the `significance`
renderer does not run `inlineText`, so `\S` would leak there — R18) — one convention across the work;
`\S` is now equally valid in a `.tex` body for future contributors. Applied throughout
`abel-1826-unmoeglichkeit`.

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
- *Added 2026-08-25.* `\ednote{...}` and `\uncertain{...}` are matched in `tex.js` with `[^}]*`, so
  the argument **may not contain a text-mode brace group**: an `\emph{...}` inside a note ends it at
  the first `}`, and the tail of the note leaks into the author's running text — silently, since
  `validate.py`, `texcompare.py` and `houselint.py` all pass. Math is safe (`$...$` spans are
  stashed before that regex runs, so `$\sqrt{X}$` inside a note is fine, and is used throughout
  `abel-1828-remarques`). **Rule: inside a note, use `$...$` freely but no text-mode macro with an
  argument — write the emphasis as plain words or `` `` ''`` quotes.** Found in a translator's note
  in `jacobi-1832-considerationes` when the leaked tail showed up on the rendered page.

Applied in `jacob-bernoulli-1694-constructio-lemniscata`, extended in
`jacobi-1832-considerationes`.

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
