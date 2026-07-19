# Change: housestyle-math-typography

## Why

Transcribing Fagnano surfaced ad-hoc typographic decisions (inline `\dfrac` vs `\displaystyle`,
whether to wrap multi-letter labels in `\pt`) that were made and reversed case-by-case. That
inconsistency is avoidable: PLAN §4.4 already separates faithful **notation** from house-style
**presentation**; we just hadn't concretised the presentation layer for math, nor recorded the
rulings. This change closes that gap so future transcriptions don't re-litigate the same choices.

## What changes

- Add `corpus/HOUSESTYLE.md`: the notation-vs-presentation principle, a short set of math
  typography conventions, and a **rulings log** (living register of boundary decisions).
- Record the first rulings, including the two already decided while transcribing Fagnano:
  - multi-letter geometric labels stay **plain math letters** (no `\pt`/`\mathit` wrapper) — tried
    and rejected 2026-07-19;
  - inline large operators (∫, ∑) with a fraction integrand use `\displaystyle` (not `\int \dfrac`);
  - author notation and printer's errors are kept faithfully (`zz` for z², archaic spelling, the
    eq.-(2) misprint), documented for review.
- Reflect the conventions in `openspec/specs/corpus-format` (house style), the `readmasters.sty`
  header comment, and `prompts/transcribe-chat.md`, and link `HOUSESTYLE.md` from CONTRIBUTING.

## Impact

- New: `corpus/HOUSESTYLE.md`.
- Extends the `corpus-format` house-style requirement (no code/schema change).
- No effect on the copyright gate or the build.
