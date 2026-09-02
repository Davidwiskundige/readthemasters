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
  * R18 — an apparatus note (`\\ednote{...}`, `\\uncertain{...}`) must contain no brace character in
    its argument. The site's reader transform matches both macros with `[^}]*`, so a nested
    `\\emph{...}` (or even an escaped `\\}`) ends the note at the *first* closing brace and its tail
    leaks into the author's running text — silently, since the file is still valid LaTeX. Inline
    math inside a note is fine and stays legal: the transform stashes `$...$` spans before that
    match runs, so this rule masks math the same way before looking for braces.

Each rule declares a *scope*: ``inline-math`` rules are predicates over one ``$...$`` span (R2),
while ``document`` rules see the whole comment-stripped file (R18) — a text-mode ruling cannot be
expressed as a statement about a math span.

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


def strip_comments(latex: str) -> str:
    """Drop LaTeX comments so commented-out examples never count as content.

    Public because validate.py reuses it: a file header comment may discuss an \origpage marker,
    and the page-marker check must not count that as a real one.
    """
    return "\n".join(_COMMENT_RE.sub("", line) for line in latex.splitlines())


def _blank_preserving_lines(m: re.Match) -> str:
    """Replace a matched region with just its newlines, so later line numbers stay accurate."""
    return "\n" * m.group(0).count("\n")


def inline_spans(latex: str):
    """Yield (line_number, content) for every inline ``$...$`` span, display math removed.

    Display forms are blanked first (preserving line breaks) so a ``$`` inside ``$$...$$`` or a
    display block is never mistaken for an inline delimiter.
    """
    text = strip_comments(latex)
    for pat in _DISPLAY_PATTERNS:
        text = pat.sub(_blank_preserving_lines, text)
    for m in _INLINE_RE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        yield line, m.group(1)


def text_mode_body(latex: str) -> str:
    """Return the document with comments, display math and inline math blanked out.

    What is left is the text-mode LaTeX — the part a text-mode rule reasons about. Math is removed
    because the site's transform stashes `$...$` spans before applying its own text-level regexes,
    so anything inside math cannot break them. Every removal preserves the region's newlines, so
    line numbers computed against the result still match the source file.
    """
    text = strip_comments(latex)
    for pat in _DISPLAY_PATTERNS:
        text = pat.sub(_blank_preserving_lines, text)
    return _INLINE_RE.sub(_blank_preserving_lines, text)


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


# Apparatus notes whose argument the site matches with `[^}]*` (site/src/lib/tex.js).
_NOTE_MACROS = ("ednote", "uncertain")
_NOTE_OPEN_RE = re.compile(r"\\(" + "|".join(_NOTE_MACROS) + r")\{")
_EXCERPT_CHARS = 60


def _excerpt(body: str) -> str:
    """One-line, length-capped view of a note's argument, for the error message."""
    flat = " ".join(body.split())
    return flat if len(flat) <= _EXCERPT_CHARS else flat[:_EXCERPT_CHARS - 1] + "…"


def _note_argument(text: str, start: int) -> tuple[str, bool]:
    r"""Read the LaTeX-balanced argument beginning at ``start`` (just past the opening brace).

    Returns ``(body, closed)``. An escaped brace (``\{``/``\}``) is a literal character, so it does
    not move the nesting depth — that is how a real TeX engine reads it, and it is exactly why such
    a note still compiles while the site truncates it.
    """
    depth, i = 1, start
    while i < len(text) and depth:
        ch = text[i]
        if ch == "\\":          # escape: consume the next character whatever it is
            i += 2
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i], True
        i += 1
    return text[start:], False


def _r18_violations(text: str) -> list[dict]:
    r"""R18: a note's argument must carry no brace, so the site's ``[^}]*`` match sees all of it.

    Runs over :func:`text_mode_body`, so math inside a note (``\ednote{printed $\sqrt{X}$ here}``)
    is already blanked and never counts — matching the transform, which stashes math first.
    """
    problems: list[dict] = []
    for m in _NOTE_OPEN_RE.finditer(text):
        macro, line = m.group(1), text.count("\n", 0, m.start()) + 1
        body, closed = _note_argument(text, m.end())
        if not closed:
            problems.append({
                "line": line,
                "problem": rf"\{macro}{{...}} is never closed",
                "excerpt": _excerpt(body),
            })
        elif "{" in body or "}" in body:
            problems.append({
                "line": line,
                "problem": rf"\{macro}{{...}} takes no braces in its argument — the site reads the "
                           r"note as far as the first '}' and spills the rest into the running "
                           r"text; write plain words or ``...'' quotes (inline math is fine)",
                "excerpt": _excerpt(body),
            })
    return problems


# Registry: (rule id, human name, scope, predicate). `inline-math` predicates take one `$...$` span
# and return a list of problem strings; `document` predicates take the text-mode body (see
# text_mode_body) and return {line, problem, excerpt} records. Add future machine-checkable rulings
# here beside R2 and R18.
_RULES = [
    ("R2", "inline large operator uses \\displaystyle (\\int/\\sum/\\prod)",
     "inline-math", _r2_problems),
    ("R18", "apparatus note takes no braces in its argument (\\ednote/\\uncertain)",
     "document", _r18_violations),
]


def lint(latex: str) -> list[dict]:
    """Return a list of house-style violations, each ``{line, rule, problem, ...}``.

    An `inline-math` rule contributes a `span` (rendered back as `$…$`); a `document` rule
    contributes an `excerpt` of the offending text. Results are ordered by line so a file's
    violations read top to bottom whatever order the rules ran in.
    """
    violations: list[dict] = []
    spans = list(inline_spans(latex))
    body = None
    for rule_id, _name, scope, predicate in _RULES:
        if scope == "inline-math":
            for line, span in spans:
                problems = predicate(span)
                if problems:
                    violations.append({
                        "line": line,
                        "rule": rule_id,
                        "problem": "; ".join(problems),
                        "span": " ".join(span.split()),
                    })
        else:
            if body is None:
                body = text_mode_body(latex)
            for found in predicate(body):
                violations.append({**found, "rule": rule_id})
    violations.sort(key=lambda v: (v["line"], v["rule"]))
    return violations


def format_violations(violations: list[dict], path: str = "") -> str:
    """Render violations as terse human-readable lines (empty string if clean)."""
    lines: list[str] = []
    for v in violations:
        loc = f"{path}:{v['line']}" if path else f"line {v['line']}"
        detail = f"${v['span']}$" if "span" in v else v.get("excerpt", "")
        lines.append(f"  {loc}: HOUSESTYLE {v['rule']}: {v['problem']} — {detail}")
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
