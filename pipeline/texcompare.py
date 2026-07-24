#!/usr/bin/env python3
"""Math/structure preservation check for translations (PLAN.md §4.2).

A translation must reproduce every mathematical expression and structural anchor from the original
transcription **unchanged** — only the prose is translated. This module extracts the invariant
tokens (math spans, `\\origpage{N}` markers, cross-reference keys) from two LaTeX bodies and reports
any that were altered, dropped, or added. Pure text processing, no dependencies beyond the stdlib —
so it runs in the free CI gate as well as in the translation pipeline's own post-check.
"""
from __future__ import annotations

import re
from collections import Counter

# --- comment stripping ------------------------------------------------------ #
_COMMENT_RE = re.compile(r"(?<!\\)%.*")

# --- math delimiters (display/env forms extracted before inline $...$) ------ #
_MATH_ENVS = "equation|align|gather|multline|eqnarray|displaymath|math"
_DISPLAY_PATTERNS = [
    re.compile(r"\\begin\{(" + _MATH_ENVS + r")\*?\}(.*?)\\end\{\1\*?\}", re.DOTALL),
    re.compile(r"\\\[(.*?)\\\]", re.DOTALL),
    re.compile(r"\\\((.*?)\\\)", re.DOTALL),
    re.compile(r"\$\$(.*?)\$\$", re.DOTALL),
]
_INLINE_RE = re.compile(r"\$((?:\\.|[^$\\])*?)\$", re.DOTALL)

_ORIGPAGE_RE = re.compile(r"\\origpage\{([^}]*)\}")
_REF_RE = re.compile(r"\\(?:label|ref|eqref|pageref)\{([^}]*)\}")
_RMFIGURE_RE = re.compile(r"\\rmfigure\{([^}]*)\}")  # first arg (image path) is invariant


def _strip(latex: str) -> str:
    """Drop LaTeX comments so commentary differences never look like content changes."""
    return "\n".join(_COMMENT_RE.sub("", line) for line in latex.splitlines())


def _norm(span: str) -> str:
    """Collapse internal whitespace so trivial spacing differences don't trip the check."""
    return " ".join(span.split())


def extract_math(latex: str) -> list[str]:
    """Return the normalized content of every math span (display forms then inline $...$)."""
    text = _strip(latex)
    spans: list[str] = []
    for pat in _DISPLAY_PATTERNS:
        def _take(m: re.Match) -> str:
            spans.append(_norm(m.group(m.lastindex)))
            return " "  # blank the consumed region so it isn't re-scanned as inline math
        text = pat.sub(_take, text)
    for m in _INLINE_RE.finditer(text):
        spans.append(_norm(m.group(1)))
    return spans


def extract_origpages(latex: str) -> list[str]:
    return [_norm(a) for a in _ORIGPAGE_RE.findall(_strip(latex))]


def extract_refs(latex: str) -> list[str]:
    text = _strip(latex)
    return [_norm(a) for a in _REF_RE.findall(text)] + [_norm(a) for a in _RMFIGURE_RE.findall(text)]


def _diff(original: list[str], translation: list[str]) -> dict:
    """Multiset diff: what the original has that the translation lost, and vice versa."""
    co, ct = Counter(original), Counter(translation)
    return {
        "dropped": sorted((co - ct).elements()),   # in original, missing/changed in translation
        "added": sorted((ct - co).elements()),     # in translation but not the original
    }


def preservation_report(original: str, translation: str) -> dict:
    """Compare the invariant tokens of an original transcription and its translation.

    Returns {"ok": bool, "math": {...}, "origpages": {...}, "refs": {...}} where each token-class
    diff lists what was `dropped` (lost/altered from the original) and `added` (not in the original).
    """
    report = {
        "math": _diff(extract_math(original), extract_math(translation)),
        "origpages": _diff(extract_origpages(original), extract_origpages(translation)),
        "refs": _diff(extract_refs(original), extract_refs(translation)),
    }
    report["ok"] = all(not (d["dropped"] or d["added"]) for d in report.values()
                       if isinstance(d, dict))
    return report


def format_report(report: dict) -> str:
    """Render a preservation report as terse human-readable lines (empty string if all clean)."""
    lines: list[str] = []
    labels = {"math": "math expression", "origpages": "\\origpage marker", "refs": "label/ref"}
    for key, label in labels.items():
        d = report[key]
        for tok in d["dropped"]:
            lines.append(f"  - {label} in original not preserved: {tok!r}")
        for tok in d["added"]:
            lines.append(f"  + {label} in translation not in original: {tok!r}")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        raise SystemExit("usage: python pipeline/texcompare.py <original.tex> <translation.tex>")
    orig = open(sys.argv[1], encoding="utf-8").read()
    trans = open(sys.argv[2], encoding="utf-8").read()
    rep = preservation_report(orig, trans)
    if rep["ok"]:
        print("OK — math, \\origpage markers, and refs are preserved.")
    else:
        print("MISMATCH — the translation altered invariant tokens:")
        print(format_report(rep))
        raise SystemExit(1)
