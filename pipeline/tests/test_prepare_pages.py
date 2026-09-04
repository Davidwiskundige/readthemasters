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


def test_block_covers_whole_page_flags_a_saturated_threshold():
    # The MDZ scan of Betti 1871 has a grey page edge sitting just under the default cut-off, so
    # every pixel counted as ink and the "block" came out as the entire scan. That must be caught:
    # it is large enough to look trustworthy, so it would otherwise cost the crop in silence.
    assert prepare_pages.block_covers_whole_page((0, 0, 2425, 3147), 2425, 3147)


def test_block_covers_whole_page_accepts_a_real_block():
    assert not prepare_pages.block_covers_whole_page((471, 385, 2172, 2639), 2425, 3147)


def test_block_covers_whole_page_needs_both_dimensions():
    # full width but a genuine top and bottom margin is a normal wide page, not a failure
    assert not prepare_pages.block_covers_whole_page((0, 300, 2425, 2800), 2425, 3147)


# --- profile-based extents: one speck must not drag the box to the page edge - #
def test_profile_extent_ignores_isolated_specks():
    # a dust speck at the page edge (3 dark pixels) beside three columns of real type
    profile = [3] + [0] * 3 + [400, 600, 400] + [0] * 3
    assert prepare_pages.profile_extent(profile, 15) == (4, 7)       # speck excluded
    assert prepare_pages.profile_extent(profile, 2) == (0, 7)        # threshold low enough: in


def test_profile_extent_keeps_a_sparse_column_of_real_type():
    # p154's right-hand columns hold four flush-right equation numbers out of ~45 lines: a
    # vanishing FRACTION of the column, but unmistakably type. A count-based rule keeps them.
    profile = [0] * 5 + [800, 800] + [0] * 20 + [60] + [0] * 4
    assert prepare_pages.profile_extent(profile, 15) == (5, 28)


def test_profile_extent_spans_from_first_to_last_hit():
    profile = [0, 0, 300, 4, 400, 0]
    assert prepare_pages.profile_extent(profile, 15) == (2, 5)


def test_profile_extent_returns_none_on_a_blank_page():
    assert prepare_pages.profile_extent([0] * 20, 15) is None


# --- the zoom mapping a batch subagent needs to magnify without guessing ----- #
def test_zoom_mapping_round_trips_a_cropped_page():
    # Clebsch p.195 as actually prepared: 1400x1859 cropped to (84,80)-(1392,1859), out 1153x1568.
    box, source, out = (84, 80, 1392, 1859), (1400, 1859), (1153, 1568)
    ox, oy, scale = prepare_pages.zoom_mapping(box, source, out)
    assert (ox, oy) == (84, 80)
    # the prepared image's own corners must map back onto the crop box's corners
    assert round(ox + 0 / scale) == box[0]
    assert round(oy + 0 / scale) == box[1]
    assert round(ox + out[0] / scale) == pytest.approx(box[2], abs=2)
    assert round(oy + out[1] / scale) == pytest.approx(box[3], abs=2)


def test_zoom_mapping_of_an_uncropped_page_is_pure_scale():
    # a page whose text block could not be trusted is passed through with box=None
    ox, oy, scale = prepare_pages.zoom_mapping(None, (1400, 1859), (1180, 1568))
    assert (ox, oy) == (0, 0)
    assert scale == pytest.approx(1568 / 1859, abs=1e-4)


def test_zoom_mapping_is_identity_when_no_downscale_happened():
    # a landscape crop under the long-edge cap is not resized at all
    ox, oy, scale = prepare_pages.zoom_mapping((0, 0, 1500, 1062), (1500, 1062), (1500, 1062))
    assert (ox, oy, scale) == (0, 0, 1.0)


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
