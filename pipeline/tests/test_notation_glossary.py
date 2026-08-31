"""The per-work notation glossary is optional, and the gate must ignore it either way.

`corpus/<work-id>/notation.md` records a work's cross-page rendering decisions (HOUSESTYLE R27,
corpus-format). It is a permanent committed artifact, but it is editorial prose: the copyright gate
neither requires it nor parses it, and a work that needed no such decision simply has none.
"""
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
NOW = 2026

WORK = {
    "id": "glossary-test-work",
    "title": "Test",
    "authors": [{"name": "A. Author", "death_year": 1900}],
    "publication": {"year": 1905, "venue": "crelle"},
    "edition": {"year": 1905, "is_transcribed_edition": True,
                "rights_cleared": True, "rights_note": "original edition"},
    "discipline": "mathematics",
    "tags": ["analysis"],
    "language": "de",
    "type": "paper",
    "source": {"scan_url": "http://x", "scan_id": "x:1"},
    "sources": {"death_date": "wikidata:Q1",
                "publication_date": "catalog:1", "edition": "catalog:1"},
}

PROVENANCE = {
    "transcription": {
        "status": "ai-draft",
        "model": "claude-opus-5",
        "prompt_version": "transcribe-v1",
        "submitted_via": "skill",
        "produced": "2026-08-31",
    }
}

ORIGINAL = (
    "\\documentclass{article}\n\\usepackage{readmasters}\n\\begin{document}\n"
    "\\origpage{1}\nEin Satz.\n\\end{document}\n"
)


def _build_work(tmp_path, with_glossary: bool) -> Path:
    work_dir = tmp_path / WORK["id"]
    work_dir.mkdir()
    (work_dir / "work.yaml").write_text(yaml.safe_dump(WORK), encoding="utf-8")
    (work_dir / "provenance.yaml").write_text(yaml.safe_dump(PROVENANCE), encoding="utf-8")
    (work_dir / "original.tex").write_text(ORIGINAL, encoding="utf-8")
    if with_glossary:
        (work_dir / "notation.md").write_text(
            "# Notation decisions\n\n"
            "- Summation sign is the letter `\\Sigma`, never `\\sum`.\n",
            encoding="utf-8",
        )
    return work_dir


def _run(work_dir: Path) -> validate.Issues:
    """Run the gate the way the skill does: --write to compute the assessment, then check."""
    vocab = validate.load_yaml(REPO / "corpus" / "vocab.yaml") or {}
    validate.validate_work(work_dir, vocab, NOW, False, validate.Issues(), write=True)
    issues = validate.Issues()
    validate.validate_work(work_dir, vocab, NOW, False, issues)
    return issues


def test_work_with_a_glossary_passes(tmp_path):
    issues = _run(_build_work(tmp_path, with_glossary=True))
    assert issues.ok, issues.errors


def test_work_without_a_glossary_also_passes(tmp_path):
    """The glossary is optional — a work needing no cross-page decision has none."""
    issues = _run(_build_work(tmp_path, with_glossary=False))
    assert issues.ok, issues.errors


def test_glossary_content_is_not_parsed_by_the_gate(tmp_path):
    """It is editorial prose; malformed markdown must not fail the copyright gate."""
    work_dir = _build_work(tmp_path, with_glossary=True)
    (work_dir / "notation.md").write_text("]]not { valid $ markdown \\sum(", encoding="utf-8")
    assert _run(work_dir).ok


def test_the_shipped_clebsch_glossary_names_its_forbidden_alternatives():
    """R27: an entry must say what NOT to write, or it licenses a fresh divergence.

    Skipped where the work is not present (it lands on its own branch).
    """
    path = (REPO / "corpus" / "clebsch-1864-anwendung-abelschen-functionen" / "notation.md")
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    assert "never" in text.lower(), "entries should name the forbidden alternative"
    assert "\\Sigma" in text and "\\sum" in text, "the summation decision should be recorded"
