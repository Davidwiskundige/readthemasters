## 1. Prepare the rule registry

- [x] 1.1 Give `_RULES` entries in `pipeline/houselint.py` a `scope` field — `"inline-math"` for the
      existing R2/R16 predicate, `"document"` for the new one — and dispatch on it in `lint()`,
      leaving `_r2_problems` and its output untouched
- [x] 1.2 Add a document-scoped helper that masks inline `$...$` spans (respecting escaped `\$`)
      using the existing newline-preserving substitution, so reported line numbers stay accurate
- [x] 1.3 Tag each violation with its kind so `format_violations()` renders a math span as `$…$` and
      a text excerpt bare; confirm existing R2 output is byte-identical

## 2. Implement the apparatus-note rule

- [x] 2.1 Write the brace-depth walk: from each `\ednote{` / `\uncertain{`, scan to the matching
      close and flag any `{` inside the (math-masked) argument
- [x] 2.2 Report an unterminated argument (depth never returns to zero) as a violation instead of
      scanning to end of file
- [x] 2.3 Emit `{line, rule: "R18", problem, excerpt}` naming the offending macro, with a message
      that says what to do instead (plain words or `` `` '' `` quotes; math is fine)
- [x] 2.4 Register the rule in `_RULES` beside R2

## 3. Test

- [x] 3.1 Add failing cases to `pipeline/tests/test_houselint.py`: `\emph{}` inside `\ednote{}`,
      the same inside `\uncertain{}`, and an unterminated note
- [x] 3.2 Add passing cases: a note containing inline math with braces (`$\sqrt{X}$`), a note of
      plain prose with `` `` '' `` quotes, and a note containing an escaped `\$`
- [x] 3.3 Assert the reported line number is correct for a violation several lines into a document
- [x] 3.4 Confirm the existing R2/R16 tests still pass unchanged

## 4. Verify against the real corpus

- [x] 4.1 Run `python pipeline/houselint.py` over every corpus `.tex` (transcriptions and
      translations) and confirm zero violations
- [x] 4.2 Run `python pipeline/validate.py` and `python -m pytest pipeline/tests -q` — both green
- [x] 4.3 Temporarily reintroduce the `jacobi-1832-considerationes` nesting bug in a scratch copy
      and confirm the gate now fails on it, then discard the scratch copy

## 5. Documentation and close-out

- [x] 5.1 Annotate HOUSESTYLE R18's third bullet as **Machine-enforced**, matching how R2/R16 are
      annotated (see the design's open question)
- [x] 5.2 Fold the delta spec into `openspec/specs/corpus-format/spec.md` and archive the change
- [x] 5.3 Open a PR with a DCO sign-off; include the before/after of the failing case from 4.3
