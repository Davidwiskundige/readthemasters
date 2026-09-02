r"""The gate's `\rmfigure` reference check.

A dangling figure reference renders as a broken image on the work page, and nothing caught it
before: houselint has no opinion on figures, and texcompare only checks that the path is the same
in an original and its translation — not that it points at anything.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate  # noqa: E402

CORPUS = Path(__file__).resolve().parents[2] / "corpus"


def _work(tmp_path, body: str, figures=()) -> Path:
    work = tmp_path / "some-work"
    (work / "figures").mkdir(parents=True)
    (work / "original.tex").write_text(
        "\\documentclass{article}\n\\begin{document}\n" + body + "\n\\end{document}\n",
        encoding="utf-8")
    for name in figures:
        (work / "figures" / name).write_bytes(b"\x89PNG\r\n\x1a\n")
    return work


def _check(tmp_path, body, figures=()):
    issues = validate.Issues()
    validate.check_figure_references(_work(tmp_path, body, figures), issues)
    return issues


def test_a_resolving_reference_passes(tmp_path):
    issues = _check(tmp_path, r"\rmfigure{figures/fig-215.png}{Fig.}{alt}", ["fig-215.png"])
    assert issues.errors == [] and issues.warnings == []


def test_a_dangling_reference_is_an_error(tmp_path):
    """The exact Clebsch defect: text says fig-215.png, the file is fig-1.png."""
    issues = _check(tmp_path, r"\rmfigure{figures/fig-215.png}{Fig.}{alt}", ["fig-1.png"])
    assert any("missing file: figures/fig-215.png" in e for e in issues.errors)


def test_an_unreferenced_figure_warns_but_does_not_block(tmp_path):
    # a crop may be staged before the text that will use it
    issues = _check(tmp_path, r"\rmfigure{figures/fig-1.png}{Fig.}{alt}",
                    ["fig-1.png", "fig-2.png"])
    assert issues.errors == []
    assert any("not referenced" in w and "fig-2.png" in w for w in issues.warnings)


def test_a_reference_inside_a_comment_is_ignored(tmp_path):
    body = ("% the plate is emitted as \\rmfigure{figures/fig-99.png} once cropped\n"
            r"\rmfigure{figures/fig-1.png}{Fig.}{alt}")
    issues = _check(tmp_path, body, ["fig-1.png"])
    assert issues.errors == []


def test_a_work_with_no_figures_passes(tmp_path):
    work = tmp_path / "plain-work"
    work.mkdir()
    (work / "original.tex").write_text("\\begin{document}\nno figures\n\\end{document}\n",
                                       encoding="utf-8")
    issues = validate.Issues()
    validate.check_figure_references(work, issues)
    assert issues.errors == [] and issues.warnings == []


def test_every_shipped_figure_reference_resolves():
    """The real corpus must pass — this is the check that would have caught Clebsch."""
    issues = validate.Issues()
    for work_dir in sorted(p for p in CORPUS.iterdir() if (p / "original.tex").exists()):
        validate.check_figure_references(work_dir, issues)
    assert issues.errors == [], "\n".join(issues.errors)
