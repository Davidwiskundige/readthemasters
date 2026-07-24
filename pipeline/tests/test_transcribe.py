"""Tests for the Tier-3 Batch API transcription pipeline (pure logic — no network, no anthropic)."""
import base64
import sys
from pathlib import Path

import pytest

# Make pipeline/transcribe.py importable regardless of pytest's rootdir.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import transcribe  # noqa: E402

REPO = Path(__file__).resolve().parents[2]


# --- parse_pages ------------------------------------------------------------ #
def test_parse_pages_range():
    assert transcribe.parse_pages("293-297") == [293, 294, 295, 296, 297]


def test_parse_pages_mixed_deduped_sorted():
    assert transcribe.parse_pages("300, 293-295, 294") == [293, 294, 295, 300]


def test_parse_pages_single():
    assert transcribe.parse_pages("42") == [42]


def test_parse_pages_rejects_reversed_range():
    with pytest.raises(ValueError):
        transcribe.parse_pages("297-293")


def test_parse_pages_rejects_empty():
    with pytest.raises(ValueError):
        transcribe.parse_pages("   ")


# --- load_prompt ------------------------------------------------------------ #
def test_load_prompt_from_repo():
    body, version = transcribe.load_prompt(REPO / "prompts" / "transcribe-chat.md")
    assert version == "transcribe-v1"          # keep in sync with the real prompt file
    assert "\\origpage" in body                # the instruction body, not the copy-paste preamble
    assert "prompt_version" not in body        # the H1 / intro (before ---) is excluded


def test_load_prompt_requires_version(tmp_path):
    p = tmp_path / "prompt.md"
    p.write_text("# no version here\n---\nbody\n", encoding="utf-8")
    with pytest.raises(ValueError):
        transcribe.load_prompt(p)


# --- image_source ----------------------------------------------------------- #
def test_image_source_encodes_base64(tmp_path):
    img = tmp_path / "293.png"
    img.write_bytes(b"\x89PNG fake bytes")
    src = transcribe.image_source(img)
    assert src["type"] == "base64"
    assert src["media_type"] == "image/png"
    assert "\n" not in src["data"]
    assert base64.b64decode(src["data"]) == b"\x89PNG fake bytes"


def test_image_source_maps_jpeg(tmp_path):
    img = tmp_path / "1.jpg"
    img.write_bytes(b"jpg")
    assert transcribe.image_source(img)["media_type"] == "image/jpeg"


def test_image_source_rejects_unsupported(tmp_path):
    bad = tmp_path / "1.tiff"
    bad.write_bytes(b"x")
    with pytest.raises(ValueError):
        transcribe.image_source(bad)


# --- resolve_page_images ---------------------------------------------------- #
def test_resolve_page_images_plain_and_padded(tmp_path):
    (tmp_path / "293.png").write_bytes(b"a")
    (tmp_path / "0294.jpg").write_bytes(b"b")   # zero-padded stem still matches page 294
    got = transcribe.resolve_page_images(tmp_path, [293, 294])
    assert got[293].name == "293.png"
    assert got[294].name == "0294.jpg"


def test_resolve_page_images_reports_missing(tmp_path):
    (tmp_path / "293.png").write_bytes(b"a")
    with pytest.raises(FileNotFoundError) as e:
        transcribe.resolve_page_images(tmp_path, [293, 294])
    assert "294" in str(e.value)


# --- build_page_request ----------------------------------------------------- #
def test_build_page_request_shape_and_caching():
    src = {"type": "base64", "media_type": "image/png", "data": "AAAA"}
    req = transcribe.build_page_request(293, "INSTRUCTIONS", src, prev_tail="",
                                        model="claude-opus-4-8", effort="high")
    assert req["custom_id"] == "page-293"
    params = req["params"]
    assert params["model"] == "claude-opus-4-8"
    assert params["output_config"]["effort"] == "high"
    # Pinned instruction is a cached system prefix (byte-identical across pages).
    assert params["system"][0]["text"] == "INSTRUCTIONS"
    assert params["system"][0]["cache_control"] == {"type": "ephemeral"}
    content = params["messages"][0]["content"]
    assert content[0]["type"] == "image" and content[0]["source"] is src
    assert "\\origpage{293}" in content[1]["text"]


def test_build_page_request_includes_tail_when_given():
    src = {"type": "base64", "media_type": "image/png", "data": "AAAA"}
    req = transcribe.build_page_request(2, "I", src, prev_tail="…prior text.",
                                        model="m", effort="low")
    assert "…prior text." in req["params"]["messages"][0]["content"][1]["text"]


# --- clean_fragment / stitch ------------------------------------------------ #
def test_clean_fragment_strips_fences_and_scaffold():
    raw = ("```latex\n"
           "\\documentclass{article}\n"
           "\\usepackage{readmasters}\n"
           "\\begin{document}\n"
           "\\origpage{5}\nHello.\n"
           "\\end{document}\n"
           "```")
    out = transcribe.clean_fragment(5, raw)
    assert out == "\\origpage{5}\nHello."


def test_clean_fragment_prepends_missing_origpage():
    out = transcribe.clean_fragment(7, "Some text without the marker.")
    assert out.startswith("\\origpage{7}\n")


def test_stitch_orders_by_page_and_wraps():
    doc = transcribe.stitch({297: "\\origpage{297}\nB.", 293: "\\origpage{293}\nA."})
    assert doc.startswith("%")                       # header comment
    assert "\\documentclass{article}" in doc
    assert "\\usepackage{readmasters}" in doc
    # page 293 must appear before 297 regardless of dict order
    assert doc.index("\\origpage{293}") < doc.index("\\origpage{297}")
    assert doc.rstrip().endswith("\\end{document}")


# --- tail_of ---------------------------------------------------------------- #
def test_tail_of_truncates():
    assert transcribe.tail_of("x" * 1000, max_chars=10) == "x" * 10


def test_tail_of_keeps_short():
    assert transcribe.tail_of("  short  ") == "short"


# --- is_flagged ------------------------------------------------------------- #
def test_is_flagged_match_is_clean():
    assert transcribe.is_flagged("MATCH") is False
    assert transcribe.is_flagged("  match \n") is False


def test_is_flagged_anything_else():
    assert transcribe.is_flagged("FLAG: eq 12 wrong") is True
    assert transcribe.is_flagged("") is True


# --- build_provenance ------------------------------------------------------- #
def test_build_provenance_ai_draft_with_verification():
    prov = transcribe.build_provenance("claude-opus-4-8", "high", "transcribe-v1",
                                       ["msgbatch_1", "msgbatch_2"], [12, 31],
                                       verify_model="claude-haiku-4-5", produced="2026-07-24")
    assert prov["status"] == "ai-draft"
    assert prov["submitted_via"] == "pipeline"
    assert prov["batch_ids"] == ["msgbatch_1", "msgbatch_2"]
    assert prov["verification"]["flagged_pages"] == [12, 31]
    assert prov["verification"]["model"] == "claude-haiku-4-5"


def test_build_provenance_no_verification_omits_block():
    prov = transcribe.build_provenance("m", "high", "transcribe-v1", ["b"], [],
                                       verify_model=None)
    assert "verification" not in prov


# --- validate.py stays AI-free ---------------------------------------------- #
def test_validate_does_not_import_anthropic():
    import validate  # noqa: F401
    assert "anthropic" not in sys.modules, "validate.py must not import the anthropic SDK"
