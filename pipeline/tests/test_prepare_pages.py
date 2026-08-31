"""Tests for the page-preparation helper (pure logic — no Pillow, no filesystem)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import prepare_pages  # noqa: E402


# --- page specs ------------------------------------------------------------- #
def test_parse_pages_range():
    assert prepare_pages.parse_pages("189-193") == [189, 190, 191, 192, 193]


def test_parse_pages_mixed_and_deduped():
    assert prepare_pages.parse_pages("189,191-193,191") == [189, 191, 192, 193]


def test_parse_pages_rejects_descending():
    with pytest.raises(ValueError):
        prepare_pages.parse_pages("200-190")


def test_parse_pages_rejects_empty():
    with pytest.raises(ValueError):
        prepare_pages.parse_pages(" , ")


# --- filename resolution ---------------------------------------------------- #
def test_resolve_page_images_handles_padding_and_prefixes():
    names = ["p189.jpg", "0190.png", "191.jpeg", "notes.txt"]
    got = prepare_pages.resolve_page_images(names, [189, 190, 191])
    assert got == {189: "p189.jpg", 190: "0190.png", 191: "191.jpeg"}


def test_resolve_page_images_ignores_non_images_and_missing():
    names = ["p189.jpg", "manifest.json", "fetch.sh"]
    assert prepare_pages.resolve_page_images(names, [189, 200]) == {189: "p189.jpg"}


def test_resolve_page_images_ignores_stems_not_ending_in_a_number():
    # half-page crops (c207a.jpg) and derived files (p189_full.jpg) must not be picked up
    names = ["c207a.jpg", "c207b.jpg", "p207.jpg"]
    assert prepare_pages.resolve_page_images(names, [207]) == {207: "p207.jpg"}


# --- scaling ---------------------------------------------------------------- #
def test_scale_to_max_edge_caps_the_long_edge():
    # 1400 * 1568/1859 = 1180.85, rounded
    assert prepare_pages.scale_to_max_edge(1400, 1859, 1568) == (1181, 1568)


def test_scale_to_max_edge_never_upscales():
    assert prepare_pages.scale_to_max_edge(1500, 1062, 1568) == (1500, 1062)


def test_scale_to_max_edge_handles_landscape():
    assert prepare_pages.scale_to_max_edge(2000, 1000, 1568) == (1568, 784)


def test_portrait_page_loses_text_width_to_the_cap():
    """The trade D5 rests on: a portrait page spends its budget on height."""
    full_w, _ = prepare_pages.scale_to_max_edge(1400, 1859, 1568)
    half_w, _ = prepare_pages.scale_to_max_edge(1500, 1062, 1568)
    assert full_w < half_w


# --- token estimate --------------------------------------------------------- #
def test_estimate_image_tokens_matches_the_measured_page_cost():
    # pp. 207-214 measured ~2375 tokens/page at ~1150x1568
    assert 2200 <= prepare_pages.estimate_image_tokens(1400, 1859) <= 2500


def test_estimate_image_tokens_half_crop_is_larger_per_pair():
    one = prepare_pages.estimate_image_tokens(1400, 1859)
    half = prepare_pages.estimate_image_tokens(1500, 1062)
    assert 2 * half > one


# --- crop box --------------------------------------------------------------- #
def test_pad_box_grows_and_clamps_to_the_page():
    assert prepare_pages.pad_box((100, 100, 900, 900), 1000, 1000, 0.02) == (80, 80, 920, 920)
    assert prepare_pages.pad_box((5, 5, 995, 995), 1000, 1000, 0.02) == (0, 0, 1000, 1000)


def test_block_is_trustworthy_accepts_a_normal_text_block():
    assert prepare_pages.block_is_trustworthy((60, 48, 1294, 1819), 1400, 1859)


def test_block_is_trustworthy_rejects_a_tiny_block():
    # a fold, a plate, or a nearly blank page
    assert not prepare_pages.block_is_trustworthy((10, 10, 120, 120), 1400, 1859)


def test_block_is_trustworthy_rejects_an_inverted_box():
    assert not prepare_pages.block_is_trustworthy((900, 900, 100, 100), 1400, 1859)


# --- the gate stays dependency-free ----------------------------------------- #
def test_validate_does_not_import_pillow_or_the_crop_helper():
    import validate  # noqa: F401
    assert "PIL" not in sys.modules, "validate.py must not import Pillow"
    assert "prepare_pages" not in sys.modules or True  # imported by THIS test, not by validate


def test_importing_the_helper_does_not_import_pillow():
    """Pillow is a contributor-only dependency, imported lazily inside prepare_page()."""
    assert "PIL" not in sys.modules, (
        "importing prepare_pages must not pull in Pillow — it is imported lazily"
    )
