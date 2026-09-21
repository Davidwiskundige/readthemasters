## 1. Standalone KaTeX Math Linter (Node CLI)

- [x] 1.1 Implement `site/scripts/lint-math.mjs` to extract inline math (`$...$`) and display math (`\[ ... \]`, `$$ ... $$`) with precise line numbers.
- [x] 1.2 Implement KaTeX rendering check using `katex.renderToString(expr, { throwOnError: true, displayMode })`.
- [x] 1.3 Add enforcement for HOUSESTYLE R16 (detect bare `\begin{align*}` or `\begin{gather*}` outside `\[ ... \]`).
- [x] 1.4 Add checks for apparatus macros (`\uncertain`, `\origpage`, `\ednote`, `\rmfigure`, `\illegible`) mistakenly placed inside math spans.
- [x] 1.5 Add CLI argument handling to support inspecting single files, scratch fragments, or multiple target files with actionable error outputs and proper exit codes.
- [x] 1.6 Add `lint:math` script to `site/package.json`.

## 2. Python Bridge in pipeline/houselint.py

- [x] 2.1 Update `pipeline/houselint.py` to detect `node` and call `site/scripts/lint-math.mjs` via subprocess.
- [x] 2.2 Add fallback checks in `pipeline/houselint.py` for basic delimiter and brace balance when Node is absent.
- [x] 2.3 Format math syntax errors consistently with existing houselint violation reporting.

## 3. Skill Documentation Updates

- [x] 3.1 Update `.agents/skills/transcribe/SKILL.md` Phase 4 (Early Linting) and Phase 7 (Validate) to require KaTeX math validation.
- [x] 3.2 Update `.claude/skills/transcribe/SKILL.md` Phase 3 and Phase 7 to require KaTeX math validation.

## 4. Tests and Corpus Baseline Verification

- [x] 4.1 Add unit tests in `site/` verifying that `lint-math.mjs` catches syntax errors, unclosed delimiters, bare align, and apparatus macro violations.
- [x] 4.2 Add unit tests in `pipeline/tests/test_houselint.py` verifying the Python bridge and violation reporting.
- [x] 4.3 Run the math linter across all existing works in `corpus/` to verify baseline cleanliness.
