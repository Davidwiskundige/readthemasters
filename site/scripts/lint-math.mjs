#!/usr/bin/env node
/**
 * Zero-token mathematical syntax & KaTeX linter for ReadTheMasters LaTeX files.
 *
 * Checks:
 *  1. Syntax validity: All inline ($...$) and display (\[...\], $$...$$) math
 *     parses without errors in KaTeX (throwOnError: true).
 *  2. HOUSESTYLE R16: Standalone display formulas must be wrapped in \[ ... \].
 *     Bare \begin{align*}, \begin{gather*}, etc. outside \[ ... \] are forbidden.
 *  3. Apparatus boundary: Macros \uncertain, \origpage, \ednote, \rmfigure, \illegible
 *     must not be placed inside math mode.
 *
 * Usage:
 *   node site/scripts/lint-math.mjs <file1.tex> [file2.tex ...] [--json]
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Resolve KaTeX relative to this script so it works from any working directory.
let katex;
try {
  katex = (await import('../node_modules/katex/dist/katex.mjs')).default;
} catch {
  // Fallback to standard package import if running in environment where node_modules is in path
  katex = (await import('katex')).default;
}

const APPARATUS_IN_MATH_RE = /\\(uncertain|origpage|ednote|rmfigure|illegible)\b/;
const BARE_ENV_RE = /\\begin\{(align|gather|multline|flalign|alignat)\*?\}/;

/**
 * Replace comments with spaces/newlines to preserve line and column numbers.
 */
function stripComments(tex) {
  return tex.replace(/(?<!\\)%.*$/gm, '');
}

/**
 * Return line number (1-based) from a character index in original string.
 */
function getLineNumber(text, index) {
  return text.slice(0, index).split('\n').length;
}

/**
 * Lint LaTeX math in a string.
 * Returns an array of violations: [{ line, type, math, error }]
 */
export function lintMath(tex, options = {}) {
  const violations = [];
  const stripped = stripComments(tex);

  // 1. Check for bare display math environments outside \[ ... \] (HOUSESTYLE R16)
  // Mask out legitimate display math first
  const nonDisplay = stripped.replace(/\\\[([\s\S]*?)\\\]/g, (m) =>
    '\n'.repeat(m.split('\n').length - 1)
  );

  let bareMatch;
  const bareSearch = new RegExp(BARE_ENV_RE.source, 'g');
  while ((bareMatch = bareSearch.exec(nonDisplay)) !== null) {
    const line = getLineNumber(stripped, bareMatch.index);
    violations.push({
      line,
      type: 'display-wrap',
      math: bareMatch[0],
      error: `Bare ${bareMatch[0]} outside \\[ ... \\]. Standalone display formulas must be wrapped in \\[ ... \\] (HOUSESTYLE R16).`,
    });
  }

  // 2. Check display math blocks: \[ ... \]
  const displayRegex = /\\\[([\s\S]*?)\\\]/g;
  let m;
  while ((m = displayRegex.exec(stripped)) !== null) {
    const line = getLineNumber(stripped, m.index);
    const math = m[1].trim();

    // Check apparatus macros
    const appMatch = math.match(APPARATUS_IN_MATH_RE);
    if (appMatch) {
      violations.push({
        line,
        type: 'apparatus-in-math',
        math,
        error: `Apparatus macro \\${appMatch[1]} found inside display math. Apparatus macros belong in text mode.`,
      });
      continue;
    }

    // Check KaTeX parse
    try {
      katex.renderToString(math, { throwOnError: true, displayMode: true });
    } catch (err) {
      violations.push({
        line,
        type: 'display-math',
        math,
        error: err.message,
      });
    }
  }

  // 3. Check inline math blocks: $...$
  // First mask all display blocks so $ inside display environments isn't treated as inline delimiter
  const maskedDisplay = stripped.replace(/\\\[([\s\S]*?)\\\]/g, (m) =>
    '\n'.repeat(m.split('\n').length - 1)
  );

  const inlineRegex = /(?<!\\)\$((?:[^$\\]|\\.)*?)(?<!\\)\$/g;
  let inlineMatch;
  while ((inlineMatch = inlineRegex.exec(maskedDisplay)) !== null) {
    const line = getLineNumber(stripped, inlineMatch.index);
    const math = inlineMatch[1].trim();

    // Check apparatus macros
    const appMatch = math.match(APPARATUS_IN_MATH_RE);
    if (appMatch) {
      violations.push({
        line,
        type: 'apparatus-in-math',
        math,
        error: `Apparatus macro \\${appMatch[1]} found inside inline math. Apparatus macros belong in text mode.`,
      });
      continue;
    }

    // Check KaTeX parse
    try {
      katex.renderToString(math, { throwOnError: true, displayMode: false });
    } catch (err) {
      violations.push({
        line,
        type: 'inline-math',
        math,
        error: err.message,
      });
    }
  }

  // 4. Check unescaped $ count parity (odd unescaped $ indicates unclosed math)
  // Mask out matched inline math
  const noMath = maskedDisplay.replace(inlineRegex, '');
  const strayDollarMatch = /(?<!\\)\$/g.exec(noMath);
  if (strayDollarMatch) {
    const line = getLineNumber(noMath, strayDollarMatch.index);
    violations.push({
      line,
      type: 'delimiter-unbalanced',
      math: '$',
      error: 'Unbalanced or unclosed math delimiter ($). A math span was opened but never closed.',
    });
  }

  return violations;
}

/**
 * Lint a file from disk. Returns { file, violations }
 */
export function lintFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const violations = lintMath(content);
  return { file: filePath, violations };
}

// Run as CLI script
const isMain = process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1]);
if (isMain) {
  const args = process.argv.slice(2);
  const jsonOutput = args.includes('--json');
  const fileArgs = args.filter((a) => !a.startsWith('--'));

  if (fileArgs.length === 0) {
    console.error('Usage: node site/scripts/lint-math.mjs <file1.tex> [file2.tex ...] [--json]');
    process.exit(2);
  }

  let totalViolations = 0;
  const results = [];

  for (const file of fileArgs) {
    try {
      const res = lintFile(file);
      results.push(res);
      totalViolations += res.violations.length;
    } catch (err) {
      console.error(`Error reading ${file}: ${err.message}`);
      process.exit(2);
    }
  }

  if (jsonOutput) {
    console.log(JSON.stringify(results, null, 2));
  } else {
    for (const res of results) {
      if (res.violations.length > 0) {
        console.error(`\n❌ ${res.file} (${res.violations.length} math violations):`);
        for (const v of res.violations) {
          console.error(`  Line ${v.line} [${v.type}]: ${v.error}`);
          if (v.math) {
            const preview = v.math.length > 60 ? v.math.slice(0, 57) + '...' : v.math;
            console.error(`    Formula: ${preview}`);
          }
        }
      }
    }
    if (totalViolations === 0) {
      console.log(`✓ Math lint clean: ${fileArgs.length} file(s) checked with 0 errors.`);
    }
  }

  process.exit(totalViolations > 0 ? 1 : 0);
}
