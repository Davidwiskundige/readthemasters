"""The gate's \\origpage page-marker check.

A batched transcription assembles one fragment per printed page, so a dropped, duplicated or
out-of-order fragment is a real failure mode. Nothing caught it before this check existed: the
gate never looked at page markers and houselint has no opinion on them.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import houselint  # noqa: E402
import validate  # noqa: E402

CORPUS = Path(__file__).resolve().parents[2] / "corpus"


def _work(tmp_path, body: str) -> Path:
    work = tmp_path / "some-work"
    work.mkdir()
    (work / "original.tex").write_text(
        "\\documentclass{article}\n\\begin{document}\n" + body + "\n\\end{document}\n",
        encoding="utf-8")
    return work


def _check(tmp_path, body):
    issues = validate.Issues()
    validate.check_page_markers(_work(tmp_path, body), issues)
    return issues


def test_contiguous_markers_pass(tmp_path):
    issues = _check(tmp_path, "\\origpage{189}\na\n\n\\origpage{190}\nb\n\n\\origpage{191}\nc")
    assert issues.errors == [] and issues.warnings == []


def test_duplicate_marker_is_an_error(tmp_path):
    issues = _check(tmp_path, "\\origpage{189}\na\n\n\\origpage{189}\nb")
    assert any("duplicate" in e for e in issues.errors)


def test_descending_markers_are_an_error(tmp_path):
    issues = _check(tmp_path, "\\origpage{191}\na\n\n\\origpage{190}\nb")
    assert any("ascending order" in e for e in issues.errors)


def test_a_gap_warns_but_does_not_block(tmp_path):
    # a work may legitimately transcribe a selection of pages, so a gap is informational
    issues = _check(tmp_path, "\\origpage{189}\na\n\n\\origpage{195}\nb")
    assert issues.errors == []
    assert any("skip page(s): 190-194" in w for w in issues.warnings)


def test_a_marker_named_in_a_comment_is_not_counted(tmp_path):
    """Jacobi's header comment explains why a display is split around \\origpage{401}.

    Counting that as a real marker reported a duplicate that does not exist — the bug this
    check shipped with, caught by running it over the existing corpus.
    """
    body = ("% the display spanning pp. 400-401 is split around \\origpage{401} here\n"
            "\\origpage{400}\na\n\n\\origpage{401}\nb")
    issues = _check(tmp_path, body)
    assert issues.errors == [] and issues.warnings == []


def test_a_work_with_no_transcription_is_skipped(tmp_path):
    work = tmp_path / "metadata-only"
    work.mkdir()
    issues = validate.Issues()
    validate.check_page_markers(work, issues)
    assert issues.errors == [] and issues.warnings == []


def test_every_shipped_work_has_sane_page_markers():
    """The real corpus must pass — this is what caught the comment bug."""
    issues = validate.Issues()
    for work_dir in sorted(p for p in CORPUS.iterdir() if (p / "original.tex").exists()):
        validate.check_page_markers(work_dir, issues)
    assert issues.errors == [], "\n".join(issues.errors)


def test_clebsch_is_contiguous_over_the_whole_paper():
    tex = (CORPUS / "clebsch-1864-anwendung-abelschen-functionen" / "original.tex")
    body = houselint.strip_comments(tex.read_text(encoding="utf-8"))
    import re
    pages = [int(n) for n in re.findall(r"\\origpage\{(\d+)\}", body)]
    assert pages == list(range(189, 244)), "pp. 189-243, contiguous, no duplicates"


# --- the title / transcription cross-check ---------------------------------- #
def test_title_near_match_warns(tmp_path):
    """Noether 1869: metadata said 'Variablen', the print sets 'Variabeln'."""
    work = _work(tmp_path, "\section*{Zur Theorie der Functionen complexer Variabeln.}")
    issues = validate.Issues()
    validate.check_title_matches_transcription(
        work, {"title": "Zur Theorie der Functionen complexer Variablen."}, issues)
    assert any("nearly matches" in w for w in issues.warnings)
    assert issues.errors == []


def test_title_exact_match_is_silent(tmp_path):
    work = _work(tmp_path, "\section*{Zur Theorie der Functionen complexer Variabeln.}")
    issues = validate.Issues()
    validate.check_title_matches_transcription(
        work, {"title": "Zur Theorie der Functionen complexer Variabeln."}, issues)
    assert issues.warnings == []


def test_a_printed_article_number_prefix_is_not_a_mismatch(tmp_path):
    """Three shipped works keep the print's article number in the heading; that is not a defect."""
    work = _work(tmp_path, "\section*{30. Remarques sur quelques proprietes generales}")
    issues = validate.Issues()
    validate.check_title_matches_transcription(
        work, {"title": "Remarques sur quelques proprietes generales."}, issues)
    assert issues.warnings == []


def test_a_work_that_does_not_transcribe_its_title_is_silent(tmp_path):
    # most corpus works have no title line at all — the check must not invent one
    work = _work(tmp_path, "\section*{I.}\n\nDer Text beginnt hier.")
    issues = validate.Issues()
    validate.check_title_matches_transcription(
        work, {"title": "Ein ganz anderer Titel uber etwas anderes."}, issues)
    assert issues.warnings == []
