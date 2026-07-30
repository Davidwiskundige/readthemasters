#!/usr/bin/env python3
"""Mechanical house-style linter for corpus LaTeX (corpus/HOUSESTYLE.md).

Some house-style rulings are *presentation* choices that can be checked by machine — the same way
`texcompare.py` checks math preservation and `validate.py` checks the copyright facts. This module
catches those so a regression cannot be merged, whether the file was written by a human or drafted
by an AI transcription/translation pass.

Scope note: this only enforces rules that are unambiguous from the source text. Judgement calls
(faithful vs. modernized notation, translation wording) are never linted here.

Rules currently enforced:
  * R2 (extended by R16) — any *inline* large operator (`\\int`, `\\sum`, `\\prod`) must be set with
    `\\displaystyle`, so the operator matches the height of its operand instead of shrinking to a
    small inline glyph. This holds however the operand is written — a `\\frac`, or the author's own
    `:`/`/` division sign (`$\\displaystyle\\int(a\\,dz : \\sqrt{...})$`). Under such an operator use
    `\\frac`, not the redundant `\\dfrac`. A standalone inline `\\dfrac` with no operator is fine and
    is never flagged. Display math (`\\[ ... \\]`, environments) is already display style and is
    never flagged.

Pure text processing, stdlib only — so it runs in the free CI gate as well as in the pipelines.
"""
from __future__ import annotations

import re

# --- comment stripping + math-span isolation -------------------------------- #
_COMMENT_RE = re.compile(r"(?<!\\)%.*")
_MATH_ENVS = "equation|align|gather|multline|eqnarray|displaymath|math"
_DISPLAY_PATTERNS = [
    re.compile(r"\\begin\{(" + _MATH_ENVS + r")\*?\}(.*?)\\end\{\1\*?\}", re.DOTALL),
    re.compile(r"\\\[(.*?)\\\]", re.DOTALL),
    re.compile(r"\\\((.*?)\\\)", re.DOTALL),
    re.compile(r"\$\$(.*?)\$\$", re.DOTALL),
]
_INLINE_RE = re.compile(r"\$((?:\\.|[^$\\])*?)\$", re.DOTALL)


def _strip_comments(latex: str) -> str:
    """Drop LaTeX comments so commented-out examples never count as content."""
    return "\n".join(_COMMENT_RE.sub("", line) for line in latex.splitlines())


def _blank_preserving_lines(m: re.Match) -> str:
    """Replace a matched region with just its newlines, so later line numbers stay accurate."""
    return "\n" * m.group(0).count("\n")


def inline_spans(latex: str):
    """Yield (line_number, content) for every inline ``$...$`` span, display math removed.

    Display forms are blanked first (preserving line breaks) so a ``$`` inside ``$$...$$`` or a
    display block is never mistaken for an inline delimiter.
    """
    text = _strip_comments(latex)
    for pat in _DISPLAY_PATTERNS:
        text = pat.sub(_blank_preserving_lines, text)
    for m in _INLINE_RE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        yield line, m.group(1)


# --- rules ------------------------------------------------------------------ #
# Inline large operators that render as a tiny glyph in text style and so must be set display style.
_BIG_OPS = (r"\int", r"\sum", r"\prod")


def _r2_problems(span: str) -> list[str]:
    r"""R2 + R16: an inline large operator (``\int``/``\sum``/``\prod``) → ``\displaystyle``.

    Any inline span containing a large operator is in scope, regardless of how its operand is
    written — a ``\frac`` or the author's own ``:``/``/`` division sign both render the operator too
    small when left in text style. (A span with *no* large operator — e.g. a lone ``$y=\dfrac{..}{..}$``
    — is left alone; standalone ``\dfrac`` is an accepted inline form.)
    """
    if not any(op in span for op in _BIG_OPS):
        return []
    problems: list[str] = []
    if r"\displaystyle" not in span:
        problems.append(r"wrap the inline large operator (\int/\sum/\prod) in \displaystyle")
    if r"\dfrac" in span:
        problems.append(r"use \frac, not \dfrac, under \displaystyle")
    return problems


# Registry: (rule id, human name, predicate span -> list[str] of problems). Add future
# machine-checkable rulings here beside R2.
_RULES = [
    ("R2", "inline large operator uses \\displaystyle (\\int/\\sum/\\prod)", _r2_problems),
]


def lint(latex: str) -> list[dict]:
    """Return a list of house-style violations, each ``{line, rule, problem, span}``."""
    violations: list[dict] = []
    for line, span in inline_spans(latex):
        for rule_id, _name, predicate in _RULES:
            problems = predicate(span)
            if problems:
                violations.append({
                    "line": line,
                    "rule": rule_id,
                    "problem": "; ".join(problems),
                    "span": " ".join(span.split()),
                })
    return violations


def format_violations(violations: list[dict], path: str = "") -> str:
    """Render violations as terse human-readable lines (empty string if clean)."""
    lines: list[str] = []
    for v in violations:
        loc = f"{path}:{v['line']}" if path else f"line {v['line']}"
        lines.append(f"  {loc}: HOUSESTYLE {v['rule']}: {v['problem']} — ${v['span']}$")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        raise SystemExit("usage: python pipeline/houselint.py <file.tex> [<file.tex> ...]")
    any_bad = False
    for arg in sys.argv[1:]:
        text = open(arg, encoding="utf-8").read()
        vios = lint(text)
        if vios:
            any_bad = True
            print(f"{arg}:")
            print(format_violations(vios))
    if any_bad:
        print("\nHouse-style violations found (see corpus/HOUSESTYLE.md).")
        raise SystemExit(1)
    print("OK — no house-style violations.")
