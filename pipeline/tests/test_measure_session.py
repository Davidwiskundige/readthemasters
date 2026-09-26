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
    # 2000x4000 -> 1288x2576 -> ~4424 tokens
    assert 4300 <= measure_session.image_tokens((2000, 4000)) <= 4500


def test_image_tokens_bills_a_read_capped_image_at_its_stored_size():
    # Claude Code's Read stores a 2000px-long-edge image; the API does not shrink it further
    assert measure_session.image_tokens((1398, 2000)) == int(1398 * 2000 / 750)


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


# --- output reconstruction and pricing -------------------------------------- #
def test_reconstruct_output_reads_output_from_the_next_turns_growth():
    # turn 0 at 1000 context; 100 tokens of tool result fed in; turn 1 at 43800
    got = measure_session.reconstruct_output([1000, 43800], [0, 100], [10, 5])
    assert got == [42700, 5]


def test_reconstruct_output_never_goes_below_visible_content():
    # a context that shrinks (compaction, dropped thinking) must not produce negative output
    got = measure_session.reconstruct_output([5000, 1000], [0, 0], [300, 20])
    assert got == [300, 20]


def test_reconstruct_output_trusts_a_logged_count_that_looks_final():
    # older transcripts logged the final count on some turns: 40k logged vs a 42.7k estimate
    got = measure_session.reconstruct_output([1000, 43800], [0, 100], [10, 5], [40_000, 3])
    assert got == [40_000, 5]


def test_reconstruct_output_ignores_a_stream_start_snapshot():
    got = measure_session.reconstruct_output([1000, 43800], [0, 100], [10, 5], [4, 3])
    assert got == [42_700, 5]


def test_turn_cost_prices_cache_writes_by_ttl():
    usage = {"input_tokens": 0, "cache_read_input_tokens": 1_000_000,
             "cache_creation_input_tokens": 1_000_000,
             "cache_creation": {"ephemeral_1h_input_tokens": 400_000}}
    cost = measure_session.turn_cost(usage, 1_000_000,
                                     measure_session.PRICES["claude-opus-5-5"])
    assert cost["write_5m"] == 600_000 * 5.00 / 1e6
    assert cost["write_1h"] == 400_000 * 8.00 / 1e6
    assert cost["read"] == 0.20
    assert cost["output"] == 20.00


def _row(message_id, usage, content, role="assistant", model="claude-opus-5-5"):
    return {"type": role, "message": {"id": message_id, "role": role, "model": model,
                                      "usage": usage, "content": content}}


def _write_transcript(path, rows):
    import json
    path.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")


def test_analyse_recovers_a_known_output_that_the_log_records_as_four(tmp_path):
    """The probe-B shape: one long reply logged at stream start, then a short final turn."""
    start = {"input_tokens": 2, "cache_read_input_tokens": 0,
             "cache_creation_input_tokens": 44_000, "output_tokens": 4}
    end = {"input_tokens": 2, "cache_read_input_tokens": 44_002,
           "cache_creation_input_tokens": 42_800, "output_tokens": 4}
    rows = [
        # Claude Code writes one row per content block, each repeating the same usage
        _row("m1", start, [{"type": "thinking", "thinking": ""}]),
        _row("m1", start, [{"type": "tool_use", "id": "t1", "name": "Report",
                            "input": {"text": "x" * 400}}]),
        {"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "t1", "content": "y" * 400}]}},
        _row("m2", end, [{"type": "text", "text": "done"}]),
    ]
    transcript = tmp_path / "s.jsonl"
    _write_transcript(transcript, rows)
    data = measure_session.analyse(str(transcript))

    assert data["turns"] == 2                      # message ids, not rows
    assert data["totals"]["logged_out"] == 8       # what the log claims
    known = 42_800 - 400 / measure_session.CHARS_PER_TOKEN   # growth minus the tool result
    assert abs(data["totals"]["out"] - known - 1) <= 0.05 * known   # + "done" as floor
    assert data["totals"]["cw"] == 86_800          # counted once per message, not per row


def test_analyse_skips_synthetic_placeholder_turns(tmp_path):
    usage = {"input_tokens": 0, "cache_creation_input_tokens": 1000,
             "cache_read_input_tokens": 0, "output_tokens": 1}
    zero = {"input_tokens": 0, "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0, "output_tokens": 0}
    transcript = tmp_path / "s.jsonl"
    _write_transcript(transcript, [_row("m1", usage, []),
                                   _row("m2", zero, [], model="<synthetic>")])
    data = measure_session.analyse(str(transcript))
    assert data["turns"] == 1
    assert data["unpriced"] == []


def test_analyse_leaves_unknown_models_unpriced(tmp_path):
    usage = {"input_tokens": 10, "cache_creation_input_tokens": 0,
             "cache_read_input_tokens": 0, "output_tokens": 1}
    transcript = tmp_path / "s.jsonl"
    _write_transcript(transcript, [_row("m1", usage, [], model="claude-future-9")])
    data = measure_session.analyse(str(transcript))
    assert data["unpriced"] == ["claude-future-9"]
    assert sum(data["cost"].values()) == 0


def test_subagent_transcripts_reads_descriptions(tmp_path):
    import json
    session = tmp_path / "abc.jsonl"
    session.write_text("", encoding="utf-8")
    sub = tmp_path / "abc" / "subagents"
    sub.mkdir(parents=True)
    (sub / "agent-1.jsonl").write_text("", encoding="utf-8")
    (sub / "agent-1.meta.json").write_text(json.dumps({"description": "Transcribe pp. 1-4"}),
                                           encoding="utf-8")
    assert measure_session.subagent_transcripts(str(session)) == [
        ("Transcribe pp. 1-4", str(sub / "agent-1.jsonl"))]


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
