"""Tests for inlining readmasters.sty into the served .tex (simplify-work-page).

A downloaded .tex has to compile with nothing beside it, so build_site_data substitutes the
preamble's body for the \\usepackage{readmasters} line when writing site/public/tex/. The corpus
copy is never touched — corpus-format still requires every .tex to use the shared preamble.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_site_data as bsd  # noqa: E402


STY = Path(__file__).resolve().parents[2] / "corpus" / "preamble" / "readmasters.sty"
TEX = "\\documentclass{article}\n\\usepackage{readmasters}\n\\begin{document}\nHi\n\\end{document}\n"


# --- build_site_data.preamble_body ------------------------------------------------------------ #

def test_preamble_body_drops_package_file_syntax():
    """\\endinput would end input of the *document*, silently dropping the text below it."""
    body = bsd.preamble_body(STY.read_text(encoding="utf-8"))
    assert "\\NeedsTeXFormat" not in body
    assert "\\ProvidesPackage" not in body
    assert "\\endinput" not in body


def test_preamble_body_rewrites_require_to_usepackage_keeping_options():
    body = bsd.preamble_body(STY.read_text(encoding="utf-8"))
    assert "\\RequirePackage" not in body
    assert "\\usepackage{amsmath}" in body
    assert "\\usepackage[export]{adjustbox}" in body


def test_preamble_body_keeps_the_apparatus_macros():
    body = bsd.preamble_body(STY.read_text(encoding="utf-8"))
    for macro in ("\\origpage", "\\uncertain", "\\illegible", "\\ednote", "\\rmfigure"):
        assert "\\newcommand{%s}" % macro in body


def test_preamble_body_drops_the_leading_comment_block():
    """The file's own header describes the package, not the work — the macro comments stay."""
    body = bsd.preamble_body(STY.read_text(encoding="utf-8"))
    assert not body.startswith("%")
    assert "readmasters.sty — shared LaTeX house style" not in body
    assert "marks the boundary of page n in the original scan" in body


# --- build_site_data.write_tex_copy ----------------------------------------------------------- #

def test_write_tex_copy_inlines_the_preamble(tmp_path):
    body = bsd.preamble_body(STY.read_text(encoding="utf-8"))
    url = bsd.write_tex_copy(tmp_path, "w-1", "original", TEX, body)
    assert url == "/tex/w-1/original.tex"
    served = (tmp_path / "w-1" / "original.tex").read_text(encoding="utf-8")
    assert "\\usepackage{readmasters}" not in served
    assert "\\newcommand{\\origpage}[1]{\\ignorespaces}" in served
    # The document itself survives the substitution intact.
    assert served.startswith("\\documentclass{article}")
    assert served.rstrip().endswith("\\end{document}")


def test_write_tex_copy_without_a_preamble_is_a_plain_copy(tmp_path):
    """Callers that pass no preamble (or a corpus with no .sty) still get the file verbatim."""
    bsd.write_tex_copy(tmp_path, "w-2", "original", TEX)
    assert (tmp_path / "w-2" / "original.tex").read_text(encoding="utf-8") == TEX


def test_write_tex_copy_leaves_other_usepackage_lines_alone(tmp_path):
    body = bsd.preamble_body(STY.read_text(encoding="utf-8"))
    tex = TEX.replace("\\begin{document}", "\\usepackage{tikz}\n\\begin{document}")
    served = (bsd.write_tex_copy(tmp_path, "w-3", "original", tex, body),
              (tmp_path / "w-3" / "original.tex").read_text(encoding="utf-8"))[1]
    assert "\\usepackage{tikz}" in served
