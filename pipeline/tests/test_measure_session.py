"""Tests for the session cost meter (pure logic — no transcripts, no network)."""
import collections
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import measure_session  # noqa: E402


# --- image headers ---------------------------------------------------------- #
def _png(width, height):
    return b"\x89PNG\r\n\x1a\n" + b"\x00" * 8 + struct.pack(">II", width, height)


def _jpeg(width, height):
    return (b"\xff\xd8" + b"\xff\xc0" + struct.pack(">H", 17) + b"\x08"
            + struct.pack(">HH", height, width) + b"\x00" * 6)


def test_image_dimensions_png():
    assert measure_session.image_dimensions(_png(1400, 1859)) == (1400, 1859)


def test_image_dimensions_jpeg():
    assert measure_session.image_dimensions(_jpeg(1500, 1062)) == (1500, 1062)


def test_image_dimensions_unrecognized():
    assert measure_session.image_dimensions(b"not an image") is None


# --- token estimates -------------------------------------------------------- #
def test_image_tokens_applies_the_long_edge_cap():
    # 1400x1859 -> 1180x1568 -> ~2468 tokens
    assert 2300 <= measure_session.image_tokens((1400, 1859)) <= 2600


def test_image_tokens_does_not_upscale_a_small_image():
    small = measure_session.image_tokens((100, 100))
    assert small == int(100 * 100 / measure_session.IMAGE_TOKEN_DIVISOR)


def test_image_tokens_falls_back_when_dimensions_unknown():
    assert measure_session.image_tokens(None) == measure_session.FALLBACK_IMAGE_TOKENS
    assert measure_session.image_tokens((0, 500)) == measure_session.FALLBACK_IMAGE_TOKENS


# --- context accounting ----------------------------------------------------- #
def test_turn_context_sums_fresh_input_and_both_cache_paths():
    usage = {"input_tokens": 5, "cache_read_input_tokens": 300,
             "cache_creation_input_tokens": 40, "output_tokens": 999}
    assert measure_session.turn_context(usage) == 345


def test_residency_multiplies_size_by_turns_resident():
    # a 100-token block appearing at turn 0 of a 10-turn session sits there for 10 turns
    got = measure_session.residency([(0, "IMAGE", 100)], total_turns=10)
    assert got["IMAGE"] == 1000


def test_residency_is_the_point_of_the_tool():
    """A block read early costs far more than the same block read late."""
    early = measure_session.residency([(1, "IMAGE", 100)], total_turns=100)["IMAGE"]
    late = measure_session.residency([(99, "IMAGE", 100)], total_turns=100)["IMAGE"]
    assert early > 90 * late


def test_residency_stops_at_a_compaction():
    blocks = [(0, "IMAGE", 100), (60, "IMAGE", 100)]
    got = measure_session.residency(blocks, total_turns=100, reset_at=50)
    assert got["IMAGE"] == 100 * 50 + 100 * 40


def test_residency_returns_a_counter():
    assert isinstance(measure_session.residency([], 0), collections.Counter)


# --- transcript location ---------------------------------------------------- #
def test_project_dir_slugifies_a_windows_path():
    got = measure_session.project_dir(r"C:\Users\david\Documents\Wetenschap\ReadTheMastersAI")
    assert got.endswith("C--Users-david-Documents-Wetenschap-ReadTheMastersAI")


def test_project_dir_slugifies_a_posix_path():
    got = measure_session.project_dir("/home/d/ReadTheMastersAI")
    assert got.endswith("-home-d-ReadTheMastersAI")


# --- the gate stays dependency-free ----------------------------------------- #
def test_validate_does_not_import_the_meter():
    import validate  # noqa: F401
    assert "anthropic" not in sys.modules
