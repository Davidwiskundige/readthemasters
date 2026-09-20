## MODIFIED Requirements

### Requirement: LaTeX house style

Every `.tex` SHALL use `corpus/preamble/readmasters.sty`. Content and notation stay faithful to the
original; typography is normalized; markup is standardized. Apparatus macros: `\origpage{n}`,
`\uncertain{}`, `\illegible`, `\ednote{}`, `\rmfigure{file}{caption}{alt}` (figures are crops from
the scan, not redrawn).

The house style distinguishes faithful **notation** (which symbols/formula, the author's notation —
kept exactly) from house-style **presentation** (how the same math is set — made consistent).
Math-typography conventions and the **rulings log** of boundary decisions live in
`corpus/HOUSESTYLE.md`. Current conventions include: multi-letter geometric labels stay plain
math letters (no `\pt`/`\mathit`); any inline large operator (∫, ∑, ∏) uses `\displaystyle`
whatever its operand looks like — including the author's own `:`/`/` division sign, which stays
faithful; equation numbers go on the right via `\tag{n}` with the author's own numbers; author
notation and printer's errors are kept faithfully (`zz` for z², archaic spelling, `arc.`) and
flagged for review, never silently corrected.

The argument of an apparatus note — `\ednote{...}` or `\uncertain{...}` — SHALL contain no
text-mode brace group. Inline math (`$...$`) inside such a note IS permitted and MUST keep
rendering. This is not a stylistic preference but a rendering constraint: `site/src/lib/tex.js`
matches both macros with `[^}]*`, so a nested `\emph{...}` ends the note at the first `}` and its
tail — including the literal brace — leaks into the author's running text, while math survives
because the transform stashes `$...$` spans before that match runs (ruling R18).

All mathematical formulas in `.tex` files and `work.yaml` fields (`significance`, `significance_notes`)
SHALL parse cleanly without syntax errors under KaTeX. Standalone display formulas MUST be enclosed
in `\[ ... \]` per ruling R16; bare `\begin{align*}` or `\begin{gather*}` outside `\[ ... \]` are
prohibited because the site reader relies on `\[ ... \]` wrappers for layout and fitting. Apparatus
macros (`\uncertain`, `\illegible`, `\origpage`, `\ednote`, `\rmfigure`) are text-mode apparatus and
MUST NOT be placed inside math spans.

Presentation conventions that are unambiguous from the source text are **mechanically enforced** by
`pipeline/houselint.py` (and the underlying KaTeX validator `site/scripts/lint-math.mjs`), which
`pipeline/validate.py` runs as part of the gate — so a regression fails CI and cannot merge. It enforces:
- Rulings R2/R16 (an inline large operator `\int`/`\sum`/`\prod` must carry `\displaystyle`, and use `\frac` not `\dfrac` under it).
- Apparatus-note brace rule (R18).
- KaTeX syntax validity (all inline and display math expressions parse without `ParseError`).
- Display math wrapping (R16 display environments must be enclosed in `\[ ... \]`).
- Apparatus macro containment (no apparatus macros inside math mode).

These rules apply over the transcription, every translation, **the `significance` note in `work.yaml`
and each of its `significance_notes` asides** (which render inline math through KaTeX like the
`.tex` panels). The linter is a rule registry so further machine-checkable rulings extend it.
Judgement-based rulings (faithful vs. normalized notation, translation wording) are never linted.
Separately, the reader's LaTeX→HTML transform (`site/src/lib/tex.js`) resolves text niceties — em-dashes,
`~`, `\&`, and LaTeX control spaces `\ ` (ruling R17) — and is covered by `site/src/lib/tex.test.mjs`
(`npm test`, run in CI).

#### Scenario: Machine-checkable ruling regression fails CI

- **WHEN** a `.tex` (or the `significance` note) violates a mechanically-enforced ruling such as R2/R16
- **THEN** `pipeline/houselint.py` (run by the gate) fails the build

#### Scenario: Judgement-based rulings are not linted

- **WHEN** a decision is judgement-based (faithful vs. normalized notation, translation wording)
- **THEN** the linter does not flag it

#### Scenario: Text-mode markup inside an apparatus note fails the gate

- **WHEN** a `.tex` contains `\ednote{...\emph{word}...}` or the same nesting inside `\uncertain{}`
- **THEN** `pipeline/houselint.py` reports a violation naming the file, line, and macro, and the gate fails

#### Scenario: Math inside an apparatus note is accepted

- **WHEN** a note's argument contains inline math with braces, such as `\ednote{printed $\sqrt{X}$ here}`
- **THEN** the linter reports no violation, because the site renders that note correctly

#### Scenario: An unterminated apparatus note is reported

- **WHEN** a `\ednote{` or `\uncertain{` argument has no matching closing brace
- **THEN** the linter reports a violation rather than scanning to end of file

#### Scenario: A significance aside is linted like the significance itself

- **WHEN** a `significance_notes` entry's `text` violates a mechanically-enforced ruling such as R2/R16
- **THEN** `pipeline/houselint.py` (run by the gate) fails the build, naming the aside's index

#### Scenario: Invalid KaTeX math syntax fails the gate

- **WHEN** a `.tex` file contains unclosed delimiters, unmatched braces, or unsupported macros inside math
- **THEN** the math linter reports the exact line and syntax error, and validation fails

#### Scenario: Bare display math outside brackets fails the gate

- **WHEN** a `.tex` file contains a bare `\begin{align*}` or `\begin{gather*}` outside `\[ ... \]`
- **THEN** the math linter reports a violation of HOUSESTYLE R16 display wrapping

#### Scenario: Apparatus macro inside math mode fails the gate

- **WHEN** a `.tex` file contains `$\uncertain{...}$` or `\[ \origpage{...} \]` inside math mode
- **THEN** the math linter reports an apparatus boundary violation
