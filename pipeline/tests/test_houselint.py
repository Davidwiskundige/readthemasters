"""Tests for the mechanical house-style linter (pure text processing, no dependencies)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import houselint  # noqa: E402

REPO = Path(__file__).resolve().parents[2]


# --- R2: inline integral over a fraction ------------------------------------ #
def test_flags_inline_int_without_displaystyle():
    vios = houselint.lint(r"the arc $\int \dfrac{dx}{\sqrt{1-x^{4}}}$ is transcendent")
    assert len(vios) == 1
    assert vios[0]["rule"] == "R2"
    assert "displaystyle" in vios[0]["problem"]
    assert "dfrac" in vios[0]["problem"]  # both fixes reported for one span


def test_flags_displaystyle_but_dfrac():
    vios = houselint.lint(r"$\displaystyle\int \dfrac{dx}{x}$")
    assert len(vios) == 1
    assert "dfrac" in vios[0]["problem"]
    assert "wrap" not in vios[0]["problem"]  # displaystyle already present, so no "wrap" fix


def test_clean_inline_int_displaystyle_frac():
    assert houselint.lint(r"$\displaystyle\int \frac{dx}{\sqrt{1-x^{4}}}$") == []


def test_chained_integrals_one_displaystyle_is_enough():
    # \displaystyle at the front of the span covers a later \int in the same group.
    span = r"$\displaystyle\int \frac{dz}{\sqrt{1-z^{4}}} = n\int \frac{du}{\sqrt{1-u^{4}}}$"
    assert houselint.lint(span) == []


def test_display_math_is_never_flagged():
    assert houselint.lint(r"\[ m\int \frac{dx}{\sqrt{1-x^{4}}} = n\int \dfrac{dy}{y} \]") == []


def test_flags_inline_int_without_fraction():
    # R16: an inline integral is flagged even when its operand is not a \frac — a small ∫ next to a
    # radicand reads just as badly. \displaystyle fixes it.
    vios = houselint.lint(r"$\int dx\,\sqrt{1+x^{4}}$")
    assert len(vios) == 1 and "displaystyle" in vios[0]["problem"]
    assert houselint.lint(r"$\displaystyle\int dx\,\sqrt{1+x^{4}}$") == []


def test_flags_inline_int_with_colon_or_slash_division():
    # Bernoulli sets integrals with his own ":" / "/" division sign, no \frac at all.
    assert houselint.lint(r"$2\sqrt{t} = \int(a\,dz : \sqrt{aaz - z^{3}})$")[0]["rule"] == "R2"
    assert houselint.lint(r"$\int a^{2}\,du/\sqrt{a^{4}-u^{4}}$")[0]["rule"] == "R2"
    # …and \displaystyle clears both, leaving the faithful division sign untouched.
    assert houselint.lint(r"$\displaystyle 2\sqrt{t} = \int(a\,dz : \sqrt{aaz - z^{3}})$") == []


def test_inline_dfrac_without_operator_is_allowed():
    # Standalone inline \dfrac (no large operator) is an accepted form and stays unflagged.
    assert houselint.lint(r"$y = \dfrac{1-yy}{1+yy}$") == []
    assert houselint.lint(r"$\frac{4}{9}$") == []


def test_flags_inline_sum_without_displaystyle():
    assert houselint.lint(r"$s = \sum a_n$")[0]["rule"] == "R2"
    assert houselint.lint(r"$s = \displaystyle\sum a_n$") == []


def test_comments_are_ignored():
    assert houselint.lint("real text\n% $\\int \\dfrac{dx}{x}$ commented out") == []


def test_line_number_reported():
    latex = "line one\nline two\nhere $\\int \\dfrac{dx}{x}$ bad\n"
    vios = houselint.lint(latex)
    assert vios and vios[0]["line"] == 3


def test_format_violations_nonempty_on_hit():
    vios = houselint.lint(r"$\int \dfrac{dx}{x}$")
    out = houselint.format_violations(vios, path="foo.tex")
    assert "foo.tex" in out and "R2" in out


# --- the real corpus must stay clean ---------------------------------------- #
def test_corpus_is_house_style_clean():
    corpus = REPO / "corpus"
    checked = 0
    for tex in sorted(corpus.glob("*/original.tex")) + sorted(corpus.glob("*/translations/*.tex")):
        vios = houselint.lint(tex.read_text(encoding="utf-8"))
        assert not vios, f"{tex} has house-style violations:\n{houselint.format_violations(vios)}"
        checked += 1
    assert checked > 0, "expected at least one corpus .tex to lint"


def test_corpus_significance_is_house_style_clean():
    # The significance note carries inline math rendered by KaTeX like the .tex panels, so it is
    # linted too (see validate.check_house_style). Guards the fix in the Bernoulli work.
    import yaml  # available in the pipeline env (validate.py uses it)

    corpus = REPO / "corpus"
    checked = 0
    for wy in sorted(corpus.glob("*/work.yaml")):
        sig = (yaml.safe_load(wy.read_text(encoding="utf-8")) or {}).get("significance")
        if not isinstance(sig, str):
            continue
        vios = houselint.lint(sig)
        assert not vios, f"{wy} significance has violations:\n{houselint.format_violations(vios)}"
        checked += 1
    assert checked > 0, "expected at least one work.yaml with a significance note"
