## Why

An `\emph{...}` (or any text-mode macro with an argument) written inside an `\ednote{}` or
`\uncertain{}` argument silently corrupts the published page: the reader's transform
(`site/src/lib/tex.js`) matches both macros with `[^}]*`, so the note ends at the *first* closing
brace and its tail — including the literal `}` — leaks into the author's running text. The `.tex` is
valid LaTeX and compiles fine, so `validate.py`, `texcompare.py` and `houselint.py` all pass; the
only signal is reading the rendered page. This happened in `jacobi-1832-considerationes` (a
translator's note containing `\emph{Clarissimus}`) and was caught by eye during review, after CI was
green. The rule is already written down as the third bullet of HOUSESTYLE R18 — this change makes it
machine-enforced, like R2/R16 before it.

## What Changes

- Add a rule to the `pipeline/houselint.py` registry that flags a **text-mode brace group** inside
  the argument of `\ednote{}` or `\uncertain{}`, reporting file, line, and the offending macro.
- Math stays allowed: `$...$` spans are masked before the check, because the site stashes math
  before its own `[^}]*` match, so `$\sqrt{X}$` inside a note renders correctly — and
  `abel-1828-remarques` relies on this in nineteen ednotes. Masking must handle escaped `\$`.
- The check runs wherever the linter already runs: every `.tex` (transcription and translations) and
  the `significance` note in `work.yaml`, via `pipeline/validate.py` — so a violation fails CI.
- Extend `pipeline/tests` to cover both directions (math inside a note passes; `\emph` inside a note
  fails), so the rule cannot regress.
- No corpus content changes: a sweep of all 20 corpus `.tex` files at the time of writing found zero
  remaining violations, so the new rule is green on the existing corpus.

## Capabilities

### New Capabilities

None. This extends an existing capability's mechanical enforcement.

### Modified Capabilities

- `corpus-format`: the **LaTeX house style** requirement gains one more mechanically-enforced
  presentation ruling — apparatus macros (`\ednote{}`, `\uncertain{}`) take no nested text-mode
  brace group, with math explicitly exempt. The requirement already states that the linter is a rule
  registry that further machine-checkable rulings extend; this names the second such ruling and the
  reason it belongs there (the failure is invisible to every other gate).

## Impact

- `pipeline/houselint.py` — one new rule function in the registry.
- `pipeline/tests/` — new cases for the rule (pass and fail).
- `pipeline/validate.py` — unchanged; it already runs the linter over `.tex` files and `significance`.
- `corpus/HOUSESTYLE.md` — unchanged; R18's third bullet already states the rule in prose. It may
  gain a note that the rule is now machine-enforced, matching how R2/R16 are annotated.
- No change to `site/src/lib/tex.js`. Widening the site's own parser to accept nested braces was
  considered and is out of scope here (see design.md).
