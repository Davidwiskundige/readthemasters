"""Tests for the magnification helper (pure logic — no Pillow, no filesystem)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import magnify  # noqa: E402


# A row of the shape prepare_pages.py writes: page 227 cropped at (96, 140) and scaled to 0.8.
MAPPING = {"source": "227.jpg", "offset_x": 96, "offset_y": 140, "scale": 0.8}


# --- region specs ----------------------------------------------------------- #
def test_parse_regions_single():
    assert magnify.parse_regions("120,340,520,382") == [(120, 340, 520, 382)]


def test_parse_regions_multiple_preserves_order():
    spec = "10,20,30,40; 200,300,400,500; 1,2,3,4"
    assert magnify.parse_regions(spec) == [(10, 20, 30, 40), (200, 300, 400, 500), (1, 2, 3, 4)]


def test_parse_regions_tolerates_whitespace_and_trailing_semicolon():
    assert magnify.parse_regions(" 10 , 20 , 30 , 40 ; ") == [(10, 20, 30, 40)]


def test_parse_regions_rejects_wrong_arity():
    with pytest.raises(ValueError, match="4 comma-separated"):
        magnify.parse_regions("10,20,30")


def test_parse_regions_rejects_non_numeric():
    with pytest.raises(ValueError, match="non-numeric"):
        magnify.parse_regions("10,20,x,40")


def test_parse_regions_rejects_inverted_box():
    with pytest.raises(ValueError, match="empty or inverted"):
        magnify.parse_regions("300,20,100,40")


def test_parse_regions_rejects_empty_spec():
    with pytest.raises(ValueError, match="no regions"):
        magnify.parse_regions("  ;  ")


# --- coordinate conversion -------------------------------------------------- #
def test_to_source_box_applies_offset_and_scale():
    # source = offset + prepared / scale, so 120/0.8 = 150, plus the 96px left offset.
    assert magnify.to_source_box((120, 340, 520, 382), MAPPING) == (246, 565, 746, 617)


def test_to_source_box_at_origin_is_the_offset():
    assert magnify.to_source_box((0, 0, 80, 80), MAPPING)[:2] == (96, 140)


def test_to_source_box_round_trips_the_documented_formula():
    region = (200, 400, 600, 460)
    left, top, right, bottom = magnify.to_source_box(region, MAPPING)
    assert left == int(MAPPING["offset_x"] + region[0] / MAPPING["scale"])
    assert bottom == int(MAPPING["offset_y"] + region[3] / MAPPING["scale"])


def test_unscaled_mapping_is_identity_plus_offset():
    mapping = {"offset_x": 0, "offset_y": 0, "scale": 1.0, "source": "p.jpg"}
    assert magnify.to_source_box((5, 6, 7, 8), mapping) == (5, 6, 7, 8)


# --- zoom-map lookup -------------------------------------------------------- #
def test_load_page_mapping_finds_the_row():
    zoom = {"pages": {"227": MAPPING}}
    assert magnify.load_page_mapping(zoom, 227) == MAPPING


def test_load_page_mapping_names_known_pages_when_missing():
    zoom = {"pages": {"227": MAPPING, "228": MAPPING}}
    with pytest.raises(ValueError, match="227, 228"):
        magnify.load_page_mapping(zoom, 999)


def test_load_page_mapping_rejects_incomplete_row():
    zoom = {"pages": {"227": {"offset_x": 0, "offset_y": 0, "source": "a.jpg"}}}
    with pytest.raises(ValueError, match="scale"):
        magnify.load_page_mapping(zoom, 227)


def test_load_page_mapping_rejects_zero_scale():
    zoom = {"pages": {"227": dict(MAPPING, scale=0)}}
    with pytest.raises(ValueError, match="scale 0"):
        magnify.load_page_mapping(zoom, 227)


# --- out-of-bounds and degenerate boxes ------------------------------------- #
def test_check_source_box_passes_a_box_inside_the_page():
    box = (246, 565, 746, 617)
    assert magnify.check_source_box(box, (1400, 1900), (0, 0, 1, 1)) == box


def test_check_source_box_clamps_a_small_overhang():
    # A box running 20px past the right edge is clamped, not refused: it is still mostly type.
    assert magnify.check_source_box((1300, 100, 1420, 200), (1400, 1900), (0, 0, 1, 1)) \
        == (1300, 100, 1400, 200)


def test_check_source_box_refuses_a_box_off_the_page():
    with pytest.raises(ValueError, match="off the page"):
        magnify.check_source_box((3000, 3000, 3200, 3100), (1400, 1900), (10, 20, 30, 40))


def test_check_source_box_refuses_a_degenerate_box():
    with pytest.raises(ValueError, match=f"smaller than {magnify.MIN_REGION_PX}px"):
        magnify.check_source_box((100, 100, 104, 180), (1400, 1900), (10, 20, 30, 40))


def test_check_source_box_error_names_the_prepared_space():
    # The likeliest cause of an off-page box is coordinates named in source space by hand, which is
    # the failure this helper exists to remove — so the message has to say which space to use.
    with pytest.raises(ValueError, match="PREPARED-image coordinates"):
        magnify.check_source_box((5000, 5000, 5100, 5100), (1400, 1900), (1, 2, 3, 4))


# --- the per-page cap ------------------------------------------------------- #
def test_enforce_cap_allows_up_to_the_cap():
    magnify.enforce_cap([1, 2, 3], magnify.DEFAULT_CAP, 227)


def test_enforce_cap_refuses_more_than_the_cap():
    with pytest.raises(ValueError, match="cap is 3"):
        magnify.enforce_cap([1, 2, 3, 4], 3, 227)


def test_enforce_cap_error_points_at_uncertain():
    with pytest.raises(ValueError, match=r"uncertain"):
        magnify.enforce_cap([1, 2, 3, 4], 3, 227)


# --- scaling ---------------------------------------------------------------- #
def test_scale_to_edge_enlarges_a_small_crop():
    assert magnify.scale_to_edge(200, 50, 1400) == (1400, 350)


def test_scale_to_edge_shrinks_a_large_crop():
    assert magnify.scale_to_edge(2800, 700, 1400) == (1400, 350)


def test_scale_to_edge_never_exceeds_the_vision_cap():
    width, height = magnify.scale_to_edge(200, 100, 4000)
    assert max(width, height) == magnify.MAX_EDGE


def test_scale_to_edge_handles_a_zero_dimension():
    assert magnify.scale_to_edge(0, 0, 1400) == (0, 0)


# --- CLI wiring ------------------------------------------------------------- #
def test_multiple_regions_convert_in_one_call(tmp_path):
    """The point of the helper: one invocation covers a page's whole escalation budget."""
    regions = magnify.parse_regions("120,340,520,382; 80,700,300,744; 10,10,90,50")
    magnify.enforce_cap(regions, magnify.DEFAULT_CAP, 227)
    boxes = [magnify.check_source_box(magnify.to_source_box(r, MAPPING), (1400, 1900), r)
             for r in regions]
    assert len(boxes) == 3
    assert all(right > left and bottom > top for left, top, right, bottom in boxes)


def test_main_reports_missing_zoom_map(tmp_path, capsys):
    code = magnify.main(["--prepared", str(tmp_path), "--scans", str(tmp_path),
                         "--page", "227", "--regions", "1,2,300,300",
                         "--out", str(tmp_path / "out")])
    assert code == 1
    assert "no zoom map" in capsys.readouterr().err


def test_main_dry_run_prints_source_boxes(tmp_path, capsys):
    import json
    prepared = tmp_path / "prepared"
    prepared.mkdir()
    (prepared / "zoom-map.json").write_text(json.dumps({"pages": {"227": MAPPING}}),
                                            encoding="utf-8")
    scans = tmp_path / "scans"
    scans.mkdir()
    (scans / "227.jpg").write_bytes(b"not really a jpeg")
    code = magnify.main(["--prepared", str(prepared), "--scans", str(scans),
                         "--page", "227", "--regions", "120,340,520,382",
                         "--out", str(tmp_path / "out"), "--dry-run"])
    assert code == 0
    assert "246,565" in capsys.readouterr().out.replace(" ", "").replace("(", "").replace(")", "")


def test_main_refuses_over_cap(tmp_path, capsys):
    import json
    prepared = tmp_path / "prepared"
    prepared.mkdir()
    (prepared / "zoom-map.json").write_text(json.dumps({"pages": {"227": MAPPING}}),
                                            encoding="utf-8")
    code = magnify.main(["--prepared", str(prepared), "--scans", str(tmp_path),
                         "--page", "227",
                         "--regions", "1,1,99,99; 2,2,99,99; 3,3,99,99; 4,4,99,99",
                         "--out", str(tmp_path / "out")])
    assert code == 1
    assert "cap is 3" in capsys.readouterr().err


# --- the gate stays dependency-free ----------------------------------------- #
def test_validate_does_not_import_the_magnify_helper():
    import validate  # noqa: F401
    assert "PIL" not in sys.modules, "validate.py must not import Pillow"


def test_importing_the_helper_does_not_import_pillow():
    """Pillow is a contributor-only dependency, imported lazily inside magnify_page()."""
    assert "PIL" not in sys.modules, (
        "importing magnify must not pull in Pillow — it is imported lazily"
    )


# --- the cap is PER PAGE, across invocations (found by the Picard measurement run) --- #
def test_enforce_cap_counts_crops_already_written():
    with pytest.raises(ValueError, match="already used"):
        magnify.enforce_cap([1], 3, 227, already=3)


def test_enforce_cap_allows_a_top_up_within_the_cap():
    magnify.enforce_cap([1], 3, 227, already=2)


def test_enforce_cap_error_says_a_second_call_does_not_help():
    with pytest.raises(ValueError, match="does not buy more regions"):
        magnify.enforce_cap([1, 2], 3, 227, already=2)


def test_existing_crops_counts_only_this_page(tmp_path):
    for name in ("p227-r1.png", "p227-r2.png", "p228-r1.png", "p227-r1.txt"):
        (tmp_path / name).write_bytes(b"")
    assert magnify.existing_crops(str(tmp_path), 227) == ["p227-r1.png", "p227-r2.png"]


def test_existing_crops_on_missing_dir_is_empty(tmp_path):
    assert magnify.existing_crops(str(tmp_path / "nope"), 227) == []


# --- the ledger: the cap cannot be reset by the caller (transcribe-skill-rebaseline) --- #
# A verifier took 7 regions on one page by writing to fresh --out directories, and --cap let any
# caller raise the limit. These run through main() with --dry-run, which enforces the cap exactly
# as a real call does but needs no Pillow and no real scan.
def _prepared(tmp_path, ledger=None):
    import json
    prepared = tmp_path / "prepared"
    prepared.mkdir()
    (prepared / "zoom-map.json").write_text(json.dumps({"pages": {"227": MAPPING}}),
                                            encoding="utf-8")
    scans = tmp_path / "scans"
    scans.mkdir()
    (scans / "227.jpg").write_bytes(b"not really a jpeg")
    if ledger is not None:
        (prepared / magnify.LEDGER_NAME).write_text(json.dumps(ledger), encoding="utf-8")
    return prepared, scans


def _run(prepared, scans, out, regions="1,1,99,99", *extra):
    return magnify.main(["--prepared", str(prepared), "--scans", str(scans), "--page", "227",
                         "--regions", regions, "--out", str(out), "--dry-run", *extra])


SPENT = {"pages": {"227": {"transcribe": [[1, 1, 9, 9], [2, 2, 9, 9], [3, 3, 9, 9]]}}}


def test_a_fresh_out_directory_does_not_reset_the_cap(tmp_path, capsys):
    prepared, scans = _prepared(tmp_path, SPENT)
    assert _run(prepared, scans, tmp_path / "vcrops2") == 1
    err = capsys.readouterr().err
    assert "3 already used" in err and magnify.LEDGER_NAME in err


def test_verification_has_its_own_budget(tmp_path, capsys):
    prepared, scans = _prepared(tmp_path, SPENT)
    assert _run(prepared, scans, tmp_path / "vcrops", "1,1,99,99", "--pass", "verify") == 0
    assert "p227-v1" in capsys.readouterr().out


def test_numbering_continues_after_earlier_crops(tmp_path, capsys):
    one = {"pages": {"227": {"transcribe": [[1, 1, 9, 9]]}}}
    prepared, scans = _prepared(tmp_path, one)
    assert _run(prepared, scans, tmp_path / "crops", "1,1,99,99; 2,2,99,99") == 0
    out = capsys.readouterr().out
    assert "p227-r2" in out and "p227-r3" in out and "p227-r1:" not in out


def test_cap_cannot_be_raised(tmp_path, capsys):
    prepared, scans = _prepared(tmp_path)
    assert _run(prepared, scans, tmp_path / "crops", "1,1,99,99", "--cap", "5") == 1
    assert "lowered, not raised" in capsys.readouterr().err


def test_cap_can_be_lowered(tmp_path, capsys):
    prepared, scans = _prepared(tmp_path)
    assert _run(prepared, scans, tmp_path / "crops", "1,1,99,99; 2,2,99,99", "--cap", "1") == 1
    assert _run(prepared, scans, tmp_path / "crops", "1,1,99,99", "--cap", "1") == 0


def test_ledger_record_and_clear_are_per_page_and_pass():
    ledger = magnify.ledger_record({}, 227, "verify", [(1, 2, 3, 4)])
    ledger = magnify.ledger_record(ledger, 228, "transcribe", [(5, 6, 7, 8)])
    assert magnify.ledger_used(ledger, 227, "verify") == [[1, 2, 3, 4]]
    assert magnify.ledger_used(ledger, 227, "transcribe") == []
    ledger = magnify.ledger_clear(ledger, [227])
    assert magnify.ledger_used(ledger, 227, "verify") == []
    assert magnify.ledger_used(ledger, 228, "transcribe") == [[5, 6, 7, 8]]


def test_preparing_a_page_again_clears_its_ledger_entries(tmp_path):
    import json
    import prepare_pages
    both = {"pages": {"227": {"transcribe": [[1, 1, 9, 9]]}, "228": {"verify": [[1, 1, 9, 9]]}}}
    (tmp_path / magnify.LEDGER_NAME).write_text(json.dumps(both), encoding="utf-8")
    prepare_pages.reset_magnify_ledger(str(tmp_path), [227])
    left = json.loads((tmp_path / magnify.LEDGER_NAME).read_text(encoding="utf-8"))
    assert "227" not in left["pages"] and "228" in left["pages"]
    assert not (tmp_path / (magnify.LEDGER_NAME + ".lock")).exists()
