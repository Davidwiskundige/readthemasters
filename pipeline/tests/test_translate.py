"""Tests for the Tier-3 translation pipeline (pure logic — no network, no anthropic)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import texcompare  # noqa: E402
import translate  # noqa: E402

REPO = Path(__file__).resolve().parents[2]


# --- language_name ---------------------------------------------------------- #
def test_language_name_known_and_fallback():
    assert translate.language_name("en") == "English"
    assert translate.language_name("EN") == "English"
    assert translate.language_name("xx") == "xx"


# --- strip_scaffold / split_chunks ------------------------------------------ #
def test_strip_scaffold_drops_header_and_scaffold():
    latex = ("% a comment header\n"
             "\\documentclass{article}\n\\usepackage{readmasters}\n\\begin{document}\n\n"
             "\\origpage{1}\nBody text $x$.\n\n\\end{document}\n")
    body = translate.strip_scaffold(latex)
    assert body == "\\origpage{1}\nBody text $x$."


def test_split_chunks_by_origpage():
    body = "\\origpage{1}\nA $x$.\n\n\\origpage{2}\nB $y$."
    chunks = translate.split_chunks(body)
    assert len(chunks) == 2
    assert chunks[0].startswith("\\origpage{1}")
    assert chunks[1].startswith("\\origpage{2}")


# --- glossary / prompt ------------------------------------------------------ #
def test_format_glossary_terms():
    out = translate.format_glossary({"terms": {"Mannigfaltigkeit": "manifold"}})
    assert "Mannigfaltigkeit" in out and "manifold" in out


def test_format_glossary_empty():
    assert translate.format_glossary(None) == ""
    assert translate.format_glossary({}) == ""


def test_render_prompt_substitutes_language_and_appends_glossary():
    instruction = f"Translate into {translate._PLACEHOLDER} carefully."
    out = translate.render_prompt(instruction, "German", "\n\nGlossary: ...")
    assert "Translate into German carefully." in out
    assert translate._PLACEHOLDER not in out
    assert "Glossary:" in out


def test_render_prompt_on_real_prompt():
    instruction, version = translate.load_prompt(REPO / "prompts" / "translate-chat.md")
    assert version == "translate-v1"
    out = translate.render_prompt(instruction, "English")
    assert "English" in out
    assert translate._PLACEHOLDER not in out


# --- build_chunk_request ---------------------------------------------------- #
def test_build_chunk_request_shape():
    req = translate.build_chunk_request(3, "\\origpage{1} A.", "PROMPT",
                                        model="claude-opus-4-8", effort="high")
    assert req["custom_id"] == "chunk-3"
    p = req["params"]
    assert p["model"] == "claude-opus-4-8"
    assert p["output_config"]["effort"] == "high"
    assert p["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert p["messages"][0]["content"][0]["text"] == "\\origpage{1} A."


# --- clean_chunk / assemble ------------------------------------------------- #
def test_clean_chunk_strips_fences_and_scaffold():
    raw = "```latex\n\\begin{document}\n\\origpage{1} Hi.\n\\end{document}\n```"
    assert translate.clean_chunk(raw) == "\\origpage{1} Hi."


def test_assemble_translation_orders_and_wraps():
    doc = translate.assemble_translation({1: "\\origpage{2} B.", 0: "\\origpage{1} A."},
                                         translate.translation_header("English"))
    assert "\\documentclass{article}" in doc
    assert doc.index("\\origpage{1}") < doc.index("\\origpage{2}")
    assert doc.rstrip().endswith("\\end{document}")


# --- provenance ------------------------------------------------------------- #
def test_provenance_source_is_transcription():
    prov = translate.build_translation_provenance("claude-opus-4-8", "high", "translate-v1",
                                                  ["msgbatch_1"], produced="2026-07-24")
    assert prov["status"] == "ai-draft"
    assert prov["source"] == "transcription"        # translation_source rule (PLAN §2.2)
    assert prov["submitted_via"] == "pipeline"
    assert prov["batch_ids"] == ["msgbatch_1"]


# --- round-trip: chunking never drops math ---------------------------------- #
def test_split_then_assemble_preserves_math():
    original = REPO / "corpus" / "leibniz-1689-isochrona" / "original.tex"
    text = original.read_text(encoding="utf-8")
    chunks = translate.split_chunks(translate.strip_scaffold(text))
    # A no-op "translation" (identical chunks) must round-trip with math intact.
    rebuilt = translate.assemble_translation(dict(enumerate(chunks)),
                                             translate.translation_header("English"))
    rep = texcompare.preservation_report(text, rebuilt)
    assert rep["ok"], texcompare.format_report(rep)


# --- gate refuses non-transcribed work -------------------------------------- #
def test_check_gate_requires_original(tmp_path):
    wd = tmp_path / "w"
    (wd).mkdir()
    (wd / "work.yaml").write_text("id: w\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        translate.check_gate(wd, 2026)
