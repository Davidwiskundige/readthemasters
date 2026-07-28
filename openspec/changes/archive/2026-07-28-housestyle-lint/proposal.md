# Change: housestyle-lint

## Why

The house style separates faithful **notation** from house-style **presentation** (PLAN §4.4,
`corpus/HOUSESTYLE.md`), and some presentation rulings are unambiguous from the source text — most
notably R2: an inline integral over a fraction must be `\displaystyle\int \frac{...}{...}`, not the
cramped `\int \dfrac{...}{...}`. R2 was already documented in `HOUSESTYLE.md` and in
`prompts/transcribe-chat.md`, yet Euler's E251 shipped with the old form in both the transcription
and its English translation, and the miss was only caught by eye. Documentation alone does not
prevent regressions: the project's other non-negotiables (copyright facts, math preservation) are
enforced by machine in the gate, and this presentation ruling should be too.

## What changes

- **New linter `pipeline/houselint.py`** — stdlib-only, same shape as `texcompare.py`. It isolates
  inline `$…$` spans (display math is never flagged) and applies a **rule registry**; the first rule
  is R2 (inline `\int` over a fraction must use `\displaystyle`, and `\frac` not the redundant
  `\dfrac`). Further machine-checkable rulings drop in beside it.
- **Wired into the gate.** `pipeline/validate.py` runs the linter over each work's `original.tex`
  and every `translations/*.tex`; a violation is a gate error, so CI (which already runs
  `validate.py`) blocks the merge. No CI workflow change needed.
- **Tests.** `pipeline/tests/test_houselint.py` covers the flag/clean cases, the display-math
  exemption, comments, line numbers, and a regression guard asserting the whole corpus stays clean.
- **Prompt/skill reminders.** `prompts/translate-chat.md` (which did not mention R2) now notes it;
  `prompts/transcribe-chat.md` (which already spelled out R2) notes it is now machine-checked; both
  skill files reference the linter. `corpus/HOUSESTYLE.md` R2 records that it is machine-enforced.
- **Corpus fix that motivated it.** Euler's E251 inline integrals were corrected to the
  `\displaystyle\int \frac{}{}` form in both `original.tex` and `translations/en.tex` (ships in the
  same PR; the linter now keeps them that way).

## Impact

- New: `pipeline/houselint.py`, `pipeline/tests/test_houselint.py`.
- Extends the **corpus-format** "LaTeX house style" requirement (presentation conventions are now
  mechanically enforced). No change to the copyright/publication rules themselves.
- `pipeline/validate.py` gains a `check_house_style` step. Touches `prompts/transcribe-chat.md`,
  `prompts/translate-chat.md`, `.claude/skills/{transcribe,translate}/SKILL.md`,
  `corpus/HOUSESTYLE.md`.
- The current corpus already passes (Euler fixed in this change); the linter only ever fires on a
  new violation.
