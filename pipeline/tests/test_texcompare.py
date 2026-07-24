"""Tests for the math/structure preservation check (pure text processing, no dependencies)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import texcompare  # noqa: E402

REPO = Path(__file__).resolve().parents[2]


# --- extraction ------------------------------------------------------------- #
def test_extract_math_inline_and_display():
    latex = r"Text $CQ$ more \[ \int \frac{dz}{z} \tag{1} \] and $x^{2}$."
    got = texcompare.extract_math(latex)
    assert "CQ" in got
    assert "x^{2}" in got
    assert any("\\int" in s and "\\tag{1}" in s for s in got)


def test_extract_math_ignores_comments():
    latex = "Real $A$.\n% commented $B$ should not count"
    assert texcompare.extract_math(latex) == ["A"]


def test_extract_math_whitespace_normalized():
    assert texcompare.extract_math("$ A  B $") == texcompare.extract_math("$A B$")


def test_extract_origpages():
    assert texcompare.extract_origpages(r"\origpage{234} x \origpage{235}") == ["234", "235"]


def test_extract_refs_includes_rmfigure_path():
    latex = r"\ref{eq:1} \label{eq:2} \rmfigure{figures/fig-24.png}{Fig.~24.}{a curve}"
    refs = texcompare.extract_refs(latex)
    assert "eq:1" in refs and "eq:2" in refs and "figures/fig-24.png" in refs


# --- preservation_report ---------------------------------------------------- #
def test_report_ok_when_only_prose_differs():
    orig = r"\origpage{1} Sei $x^{2}$ gleich $y$."
    trans = r"\origpage{1} Let $x^{2}$ equal $y$."
    rep = texcompare.preservation_report(orig, trans)
    assert rep["ok"] is True


def test_report_flags_changed_math():
    orig = r"$NQR$"
    trans = r"$XYZ$"
    rep = texcompare.preservation_report(orig, trans)
    assert rep["ok"] is False
    assert rep["math"]["dropped"] == ["NQR"]
    assert rep["math"]["added"] == ["XYZ"]


def test_report_flags_dropped_origpage():
    rep = texcompare.preservation_report(r"\origpage{1} a \origpage{2} b", r"\origpage{1} a b")
    assert rep["ok"] is False
    assert rep["origpages"]["dropped"] == ["2"]


def test_format_report_nonempty_on_mismatch():
    rep = texcompare.preservation_report(r"$A$", r"$B$")
    out = texcompare.format_report(rep)
    assert "not preserved" in out and "A" in out and "B" in out


# --- the real corpus must pass ---------------------------------------------- #
def test_corpus_translations_preserve_math():
    corpus = REPO / "corpus"
    checked = 0
    for original in sorted(corpus.glob("*/original.tex")):
        for trans in sorted((original.parent / "translations").glob("*.tex")):
            rep = texcompare.preservation_report(
                original.read_text(encoding="utf-8"), trans.read_text(encoding="utf-8"))
            assert rep["ok"], f"{trans} altered math:\n{texcompare.format_report(rep)}"
            checked += 1
    assert checked > 0, "expected at least one translation in the corpus to check"
