## Context

The ReadTheMasters project relies on KaTeX to typeset 17th–19th century mathematical manuscripts in the web browser. While `pipeline/houselint.py` and `pipeline/validate.py` perform static analysis on copyright, schema, monotonic tags, and specific regex house style rules (R2/R16 and R18), neither validates whether mathematical expressions parse cleanly in KaTeX.

When an AI transcription introduces unclosed braces (`\frac{1}{2`), unmatched delimiters (`\left(`), undefined control sequences (`\oe`), stray ampersands (`$a & b$`), or apparatus macros in math mode (`$\uncertain{...}$`), the text passes all existing Python gates. In the browser reader, KaTeX runs with `throwOnError: false`, rendering an inline red error box that degrades reader experience and damages corpus credibility.

This design introduces a two-tier math linting system:
1. A deterministic, zero-token Node.js CLI (`site/scripts/lint-math.mjs`) executing against `site/node_modules/katex`.
2. A Python bridge integrated into `pipeline/houselint.py` so existing transcription skills run math validation automatically during early chunk transcription (Phase 4) and final validation (Phase 7).

## Goals / Non-Goals

**Goals:**
- **Zero token cost**: Complete validation runs locally using CPU in milliseconds.
- **100% parser fidelity**: Uses the exact same KaTeX engine and version (`katex: ^0.16.11`) deployed on the production website.
- **Early detection**: Runs after every 4-page fragment in Phase 4 of transcription so mistakes are corrected immediately.
- **Actionable errors**: Pinpoints exact file, line number, offending formula snippet, and KaTeX error diagnostics.
- **Enforces HOUSESTYLE R16**: Detects bare display math environments (`align*`, `gather*`) not wrapped in `\[ ... \]`.
- **Enforces apparatus boundaries**: Flags apparatus macros (`\uncertain`, `\ednote`, `\origpage`, `\rmfigure`, `\illegible`) placed inside math mode.

**Non-Goals:**
- Re-implementing a LaTeX/KaTeX parser in pure Python.
- Checking semantic correctness of mathematical theorems (handled in Phase 5 text proofreading and Phase 5a scan verification).
- Replacing Tectonic for PDF compilation.

## Decisions

### Decision 1: Use a dedicated Node script (`site/scripts/lint-math.mjs`) importing `katex`

*Rationale*:
KaTeX's syntax rules (macro arguments, delimiter scoping, strict mode warnings, supported symbol sets) are complex and evolve across releases. Any regex approximation in Python would either produce false negatives (letting broken math slip through) or false positives (rejecting valid historical LaTeX). Because Node and KaTeX are already installed in `site/`, writing a standalone ESM script (`site/scripts/lint-math.mjs`) gives us exact parser parity for free.

*Alternatives considered*:
- *Pure Python regex checker*: Brittle, fails to parse nested macros or complex group balancing.
- *Headless browser with Puppeteer*: Heavyweight, takes several seconds to spin up Chromium, whereas `katex.renderToString` in Node takes < 2 ms per formula.

### Decision 2: Python bridge in `pipeline/houselint.py`

*Rationale*:
Phase 4 of the transcription skill already instructs agents to run `python pipeline/houselint.py <scratch>/p<N>.tex`. By embedding a call from `houselint.py` to `lint-math.mjs` (via `subprocess.run`), we activate math linting across all existing contributor workflows without requiring prompt or behavioral rewrites.

*Behavior when Node is unavailable*:
If `node` or `site/node_modules/katex` is not found, `houselint.py` prints a warning and falls back to text-based delimiter balancing (`$` parity and brace matching), while CI's `build-site` job enforces the full KaTeX check.

### Decision 3: Math extraction and wrapping rules

The linter parses LaTeX files by:
1. Stripping LaTeX comment lines (`%...`).
2. Isolating display math: `\[ ... \]` and `$$ ... $$`.
3. Isolating inline math: `(?<!\\)\$((?:[^$\\]|\\.)*?)(?<!\\)\$`.
4. Checking for illegal bare environments: `\begin{align*}` or `\begin{gather*}` outside `\[ ... \]` (HOUSESTYLE R16).
5. Checking for apparatus macros (`\uncertain`, `\origpage`, `\ednote`, `\rmfigure`, `\illegible`) inside extracted math spans.
6. Invoking `katex.renderToString(math, { throwOnError: true, displayMode })`.

### Decision 4: Integration in CI and Test Suite

1. Add `npm run lint:math` in `site/package.json`.
2. Add a test in `site/src/lib/tex.test.mjs` or `pipeline/tests/test_houselint.py` verifying that:
   - Valid corpus files pass cleanly.
   - Syntax errors (unbalanced braces, bad delimiters, unsupported macros) are caught and reported with non-zero exit codes.

## Risks / Trade-offs

- **[Risk] Missing Node or node_modules on contributor machine**
  → *Mitigation*: If `node` is absent, `houselint.py` warns and runs a basic Python fallback check. CI runs in Ubuntu with Node 20 and strictly blocks PRs on failure.
- **[Risk] Slower linting during transcription**
  → *Mitigation*: Tested on Riemann (1,771 formulas) and Clebsch (1,410 formulas); full paper validation takes under 2 seconds. A single 4-page fragment (< 100 formulas) takes less than 150 ms.
- **[Risk] Custom macros in `readmasters.sty`**
  → *Mitigation*: The linter provides a macros configuration dictionary matching `readmasters.sty` if any legitimate custom macros are introduced to KaTeX in the future.
