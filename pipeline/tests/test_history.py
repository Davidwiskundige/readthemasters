"""Tests for revision-history derivation in build_site_data.py (PLAN.md §9 backlog #4)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_site_data as bsd  # noqa: E402


def test_classify_path_maps_work_files_to_labels():
    assert bsd.classify_path("original.tex") == "original"
    assert bsd.classify_path("work.yaml") == "metadata"
    assert bsd.classify_path("provenance.yaml") == "provenance"
    assert bsd.classify_path("translations/en.tex") == "en translation"
    assert bsd.classify_path("translations/de.tex") == "de translation"
    assert bsd.classify_path("figures/fig1.png") == "figures"
    # Anything else under the work dir is not a reader-facing artifact.
    assert bsd.classify_path("README.md") is None
    assert bsd.classify_path("notes.txt") is None


def test_work_relative_strips_to_work_tail():
    assert bsd.work_relative("corpus/fag-1/original.tex", "fag-1") == "original.tex"
    assert bsd.work_relative("corpus/fag-1/translations/en.tex", "fag-1") == "translations/en.tex"


def _git_log(*commits: tuple[str, str, str, list[str]]) -> str:
    """Build synthetic `git log --name-only` output (RS \\x1e, field sep \\x1f)."""
    out = ""
    for h, date, subject, files in commits:
        out += f"\x1eCOMMIT\x1f{h}\x1f{date}\x1f{subject}\n"
        out += "".join(f"{f}\n" for f in files)
        out += "\n"
    return out


def test_parse_history_orders_and_maps_artifacts():
    output = _git_log(
        ("abc1234def", "2026-07-25", "Promote en to skimmed",
         ["corpus/fag-1/provenance.yaml"]),
        ("0009999aaa", "2026-07-20", "Correct eq. 12 and its translation",
         ["corpus/fag-1/original.tex", "corpus/fag-1/translations/en.tex"]),
        ("111beef222", "2026-07-18", "Add work",
         ["corpus/fag-1/work.yaml", "corpus/fag-1/original.tex", "corpus/fag-1/README.md"]),
    )
    hist = bsd.parse_history(output, "fag-1")
    # Preserves git's order (newest first) and one entry per commit.
    assert [h["hash"] for h in hist] == ["abc1234def", "0009999aaa", "111beef222"]
    assert hist[0] == {"date": "2026-07-25", "hash": "abc1234def",
                       "subject": "Promote en to skimmed", "artifacts": ["provenance"]}
    assert hist[1]["artifacts"] == ["original", "en translation"]
    # README maps to nothing and drops out; the rest stay in first-seen order.
    assert hist[2]["artifacts"] == ["metadata", "original"]


def test_parse_history_handles_subject_with_field_chars():
    # A subject is taken whole (split caps at 4 fields), so punctuation in it survives.
    output = _git_log(("deadbeef", "2026-07-25", "Fix a, b — and c", ["corpus/w/original.tex"]))
    hist = bsd.parse_history(output, "w")
    assert hist[0]["subject"] == "Fix a, b — and c"


def test_parse_history_empty_output():
    assert bsd.parse_history("", "fag-1") == []


def test_work_history_empty_outside_git_repo(tmp_path):
    # A corpus dir that is not inside a git repo yields no history, and does not raise.
    assert bsd.work_history(tmp_path, "whatever") == []
