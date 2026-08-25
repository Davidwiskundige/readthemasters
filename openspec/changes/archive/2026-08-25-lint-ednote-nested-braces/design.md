## Context

`pipeline/houselint.py` today is built around one shape of rule: `lint()` walks **inline `$...$`
spans** (`inline_spans()`, which strips comments and blanks display math first) and hands each span
string to every predicate in the `_RULES` registry. That fits R2/R16 exactly — those rulings are
statements about the contents of an inline math span.

The rule this change adds is a different shape. It is about **text-mode LaTeX outside math**: the
argument of `\ednote{}` or `\uncertain{}` must not contain a brace group, because
`site/src/lib/tex.js` matches both macros with `[^}]*` and therefore truncates the note at the first
`}`. So it cannot be expressed as a predicate over an inline math span; it needs to see the whole
document.

The failure it prevents is unusually nasty: the `.tex` is valid LaTeX, compiles under Tectonic, and
passes `validate.py`, `texcompare.py` and `houselint.py`. The corruption exists only in the rendered
HTML, where the note's tail — including a literal `}` — appears inside the author's sentence. In
`jacobi-1832-considerationes` it survived a full AI verification pass and CI, and was caught by the
contributor reading the page.

Constraints: stdlib only (the gate must stay dependency-free and AI-free); line numbers in
violations must stay accurate; the rule must be green on the existing corpus (a sweep of all 20
`.tex` files found zero violations after the one fix).

## Goals / Non-Goals

**Goals:**

- Fail CI when an apparatus macro's argument contains a text-mode brace group.
- Keep math inside notes legal — `abel-1828-remarques` carries `$\sqrt{X}$`-style math in nineteen
  ednotes and renders correctly, because the site stashes math spans *before* its own `[^}]*` match.
- Extend the linter's registry so a document-scoped ruling has an obvious home, rather than bolting
  a special case onto `lint()`.
- Keep the existing R2/R16 rule and its tests untouched.

**Non-Goals:**

- Widening `tex.js` to parse balanced braces in `\ednote{}`/`\uncertain{}`. That would remove the
  underlying limitation rather than lint around it, but it means hand-rolling brace matching in the
  reader transform, re-testing every apparatus macro, and re-rendering the corpus to confirm nothing
  shifts — a larger change with its own risk. The corpus convention (notes are plain prose plus
  math) is not burdensome, so linting is the proportionate fix. Recorded here so the option is not
  forgotten.
- Linting other text-mode macros for site-support gaps (e.g. `\oe`, HOUSESTYLE R18's second bullet).
  Worth doing, but it is a different check — a whitelist of supported macros — and should be its own
  ruling and change.
- Any corpus content change.

## Decisions

**1. Give each rule a declared scope instead of adding a parallel registry.**

`_RULES` entries become `(rule_id, name, scope, predicate)` where `scope` is `"inline-math"` (the
predicate takes a span string, as today) or `"document"` (the predicate takes the comment-stripped
document and yields its own `{line, problem, excerpt}` records). `lint()` dispatches on scope.

Alternative considered: a second module-level `_DOC_RULES` list plus a second loop in `lint()`. It
works, but it splits "the registry" into two things a future rule author has to know about, and the
spec already describes the linter as *a* rule registry that further rulings extend. One registry
with a scope tag keeps that description true.

**2. Mask math before checking, mirroring what the site does.**

The check replaces every `$...$` span (respecting escaped `\$`) with a placeholder of equal newline
count before looking for braces, exactly parallel to `tex.js` stashing math before its regex runs.
This is what makes `\ednote{... $\sqrt{X}$ ...}` legal and `\ednote{... \emph{x} ...}` illegal, and
it means the lint rule and the renderer agree by construction rather than by coincidence. Reusing
the existing `_blank_preserving_lines` helper keeps line numbers accurate.

**3. Scan with a brace-depth walk, not a regex.**

Finding the macro's true argument end requires counting braces; a regex cannot. The walk starts at
`\ednote{`/`\uncertain{`, tracks depth to the matching close, and reports if any `{` occurs inside
(after masking). This also correctly handles an unterminated argument (depth never returns to zero)
— report it as a violation rather than silently scanning to EOF.

**4. Report an excerpt, not a math span.**

`format_violations()` currently wraps `v["span"]` in `$...$`, which is right for R2 but would be
misleading for a text-mode note. Violations gain an explicit kind so the formatter renders math
spans as `$…$` and document excerpts bare. Existing R2 output stays byte-identical so no current
test or CI log format changes.

**5. Apply to `\ednote{}` and `\uncertain{}` only.**

These are the two apparatus macros `tex.js` matches with `[^}]*`. `\rmfigure{}{}{}` is matched with
three `[^}]*` groups and has the same limitation for its caption/alt text, but no corpus file
currently puts markup there and the argument structure differs; folding it in would widen the rule's
surface without evidence it is needed. If a figure caption ever wants emphasis, extend this rule
then.

## Risks / Trade-offs

- **The rule could flag a legitimate future construct** (someone wants real markup inside a note) →
  The rule fires exactly where the site would corrupt the page, so a "false positive" is a genuine
  rendering bug. If the constraint ever becomes real friction, the answer is the non-goal above —
  fix `tex.js` to balance braces, then drop this rule — not to weaken the check.
- **Math masking must match the site's, or the rule and the renderer disagree** → Mirror the
  existing `_INLINE_RE` handling of escaped `\$`, and cover a note containing math with a test so
  the two stay aligned.
- **Line numbers drift if masking removes newlines** → Use the existing newline-preserving
  substitution helper; assert on a reported line number in the tests.
- **Registry refactor touches the working R2 path** → Keep `_r2_problems` and its output unchanged;
  the existing `test_houselint.py` cases pass untouched, which is the regression signal.

## Open Questions

- Should `HOUSESTYLE.md` R18's third bullet gain a "**Machine-enforced:**" annotation, the way R2/R16
  carry one? Consistent with existing practice; assumed yes unless the maintainer objects.
