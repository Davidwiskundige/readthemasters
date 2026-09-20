## Why

The ReadTheMasters static reader renders mathematical formulas in the browser using KaTeX. Currently, neither `pipeline/houselint.py` nor `pipeline/validate.py` verifies whether transcribed LaTeX math can actually be parsed by KaTeX without crashing. When an LLM transcription produces malformed braces, unclosed delimiters, unrecognized control sequences (such as `\oe`), apparatus macros inverted into math mode (`$\uncertain{...}$`), or stray ampersands (`$a & b$`), the work passes CI and `validate.py` completely, but renders as raw red error text or broken layouts for readers on the website.

This change introduces automated, zero-token KaTeX math validation into the repository to eliminate hard syntax crashes before pull requests are opened.

## What Changes

- **New standalone Node math linter (`site/scripts/lint-math.mjs`)**:
  - Extracts all inline `$...$` and display `\[ ... \]` / `$$ ... $$` math blocks from a LaTeX file or scratch fragment.
  - Verifies each math block using `katex.renderToString(expr, { throwOnError: true, displayMode })` using the project's existing KaTeX installation in `site/`.
  - Enforces display math wrapping rules (HOUSESTYLE R16): flags bare `\begin{align*}` or `\begin{gather*}` outside `\[ ... \]`.
  - Flags apparatus macros (`\uncertain`, `\origpage`, `\ednote`, `\rmfigure`, `\illegible`) mistakenly placed inside math mode.
  - Reports exact file paths, line numbers, and actionable KaTeX syntax error diagnostics. Exits non-zero on failure.
- **Python bridge / integration in `pipeline/`**:
  - Integrates math linting into `pipeline/houselint.py` (or a dedicated python runner `pipeline/check_math.py`) so Python workflows can run KaTeX checks seamlessly when Node is available.
  - Adds a fallback check for delimiter and brace parity when Node is not present.
- **Transcription skill updates (`.agents/skills/transcribe/SKILL.md` and `.claude/skills/transcribe/SKILL.md`)**:
  - Updates Phase 4 early linting: runs the math syntax check immediately after each 4-page scratch chunk is generated, catching errors while context is fresh.
  - Updates Phase 7 validation: verifies the assembled `original.tex` passes KaTeX validation.
- **CI / Test gate integration**:
  - Adds math validation tests to `site/` (`npm test`) or `pipeline/tests/` to guarantee that regressions cannot be merged in PRs.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `transcription-pipeline`: Phase 4 early linting and Phase 7 validation require all transcribed math blocks to pass KaTeX syntax validation with zero parse errors.
- `corpus-format`: All LaTeX body files (`original.tex` and translations) must parse cleanly under KaTeX without undefined control sequences or broken delimiters.

## Impact

- **New**: `site/scripts/lint-math.mjs` (stdlib Node.js + existing `katex` package).
- **Modified**: `pipeline/houselint.py` (adds math lint execution bridge), `pipeline/tests/test_houselint.py`.
- **Modified**: `.agents/skills/transcribe/SKILL.md` and `.claude/skills/transcribe/SKILL.md` (invokes math linting in Phase 4 and Phase 7).
- **Modified**: `site/package.json` (adds `lint:math` npm script) and `site/src/lib/` tests.
- **Unaffected**: The copyright gate algorithm in `pipeline/validate.py` remains dependency-free.
