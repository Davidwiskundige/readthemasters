# Tasks: housestyle-lint

## Linter

- [x] `pipeline/houselint.py` — stdlib-only, isolates inline `$…$` spans (blanks display math /
      comments first), rule registry, `lint()` + `format_violations()` + CLI.
- [x] Rule R2: inline `\int` over a fraction must use `\displaystyle` and `\frac` (not `\dfrac`);
      lone inline `\int` without a fraction integrand is out of scope.

## Gate integration

- [x] `pipeline/validate.py` — `check_house_style(work_dir, issues)` runs the linter over
      `original.tex` and every `translations/*.tex`; wired into `validate_work`. No CI YAML change
      (CI already runs `validate.py`).

## Tests

- [x] `pipeline/tests/test_houselint.py` — flag/clean cases, displaystyle-but-dfrac, chained
      integrals, display-math exemption, lone-integral exemption, inline `\dfrac` without integral,
      comments ignored, line numbers, `format_violations`, and a corpus-stays-clean regression guard.

## Reminders & docs

- [x] `prompts/translate-chat.md` — add the R2 note (it had none); math copied verbatim from the
      already-house-styled original.
- [x] `prompts/transcribe-chat.md` — note the R2 rule is now machine-checked and blocks the PR.
- [x] `.claude/skills/translate/SKILL.md` — add the `houselint` command to the preservation-check
      phase; `.claude/skills/transcribe/SKILL.md` — note the linter is part of the gate.
- [x] `corpus/HOUSESTYLE.md` — R2 records that it is machine-enforced by `houselint`.

## Motivating corpus fix

- [x] `corpus/euler-1761-integratione-aequationis/original.tex` and `translations/en.tex` — inline
      integrals converted to `\displaystyle\int \frac{}{}`; `texcompare` still passes (identical
      edits both sides).

## Verification

- [x] `python pipeline/houselint.py corpus/*/original.tex corpus/*/translations/*.tex` → clean.
- [x] Regression demo: feeding `$\int \dfrac{dx}{…}$` to the linter reports R2 and exits non-zero.
- [x] `python pipeline/validate.py` → 4 works pass; `python -m pytest pipeline/tests -q` → all pass.

## Ship

- [x] Fold the delta into `openspec/specs/corpus-format`; archive the change.
