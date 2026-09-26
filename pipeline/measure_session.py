#!/usr/bin/env python3
"""Measure what a Claude Code session actually cost, and where the context went.

A transcription run's cost is dominated not by what it reads once but by what it keeps re-sending:
every page image read stays in context and is re-sent on every later turn. This script reports that
directly, so a change to the pipeline can be measured rather than guessed at.

Usage:
    python pipeline/measure_session.py --list
    python pipeline/measure_session.py <session-id-or-path> [--pages N]

`--list` ranks the sessions for this project by input context. Given a session it reports turns,
context per turn, a residency breakdown (each content block's size multiplied by the number of later
turns it stays resident), and the cost at API list prices — for the session itself and for each
subagent under `<session>/subagents/`.

Two things the transcript gets wrong, corrected here:
- Logged `output_tokens` is a stream-start snapshot; output is reconstructed from context growth
  (`reconstruct_output`). The visible/thinking split of it is an estimate.
- Each content block is its own row repeating the message's `usage`; turns are distinct message
  ids, not rows.

Raw volume (every token counted once, unweighted) is still printed, because the archived figures
(4.2M/page, 509k/page) are raw volume — but read in isolation it overweights cache reads, the
cheapest tokens, and the plan meter weights by price.

Transcripts live in ~/.claude/projects/<slugified-cwd>/<session-id>.jsonl. Standard library only —
`pipeline/validate.py` and CI never import this (see tests/test_measure_session.py).
"""
from __future__ import annotations

import argparse
import base64
import collections
import json
import os
import pathlib
import struct
import sys

# Anthropic bills an image at roughly (w*h)/750 tokens, after downscaling so the long edge fits.
# The API cap is 2576px on Opus 4.7 and later (1568 before); Claude Code's Read tool already caps
# at 2000px, so an image stored in a transcript is normally billed at the size it was stored.
IMAGE_TOKEN_DIVISOR = 750
IMAGE_MAX_EDGE = 2576
FALLBACK_IMAGE_TOKENS = 1500
# Characters per token for text blocks. Calibrated 2026-09-26: a verbatim copy of 12k chars of
# corpus LaTeX cost ~6.7k output tokens (1.9), and at 1.9 the output reconstruction matches the 285
# turns whose logged count is final within 4% (at 4 it overestimated by 35-56%). English prose runs
# nearer 4, so this overcounts plain-English tool results somewhat.
CHARS_PER_TOKEN = 1.9

# $/MTok: fresh input, 5-minute cache write, 1-hour cache write, cache read, output.
# List prices; the plan meter was measured to weight usage roughly the same way (2026-09-25).
PRICES = {
    "claude-opus-5-5":   (4.00, 5.00, 8.00, 0.20, 20.00),
    "claude-opus-5":     (5.00, 6.25, 10.00, 0.50, 25.00),
    "claude-opus-4-8":   (5.00, 6.25, 10.00, 0.50, 25.00),
    "claude-opus-4-7":   (5.00, 6.25, 10.00, 0.50, 25.00),
    "claude-opus-4-6":   (5.00, 6.25, 10.00, 0.50, 25.00),
    "claude-sonnet-5":   (2.00, 2.50, 4.00, 0.20, 10.00),
    "claude-sonnet-4-6": (3.00, 3.75, 6.00, 0.30, 15.00),
    "claude-haiku-4-5":  (1.00, 1.25, 2.00, 0.10, 5.00),
    "claude-fable-5-1":  (10.00, 12.50, 20.00, 0.25, 50.00),
}
COST_KEYS = ("input", "write_5m", "write_1h", "read", "output")


# --------------------------------------------------------------------------- #
# Pure helpers (unit-tested — no filesystem, no network)
# --------------------------------------------------------------------------- #
def image_dimensions(data: bytes) -> tuple[int, int] | None:
    """Read (width, height) from PNG or JPEG header bytes, or None if unrecognized."""
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        width, height = struct.unpack(">II", data[16:24])
        return width, height
    if data[:2] == b"\xff\xd8":
        i = 2
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                          0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                height, width = struct.unpack(">HH", data[i + 5:i + 9])
                return width, height
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    return None


def image_tokens(dims: tuple[int, int] | None) -> int:
    """Token cost of an image, accounting for the long-edge downscale."""
    if not dims:
        return FALLBACK_IMAGE_TOKENS
    width, height = dims
    if width <= 0 or height <= 0:
        return FALLBACK_IMAGE_TOKENS
    scale = min(1.0, IMAGE_MAX_EDGE / max(width, height))
    return int((width * scale) * (height * scale) / IMAGE_TOKEN_DIVISOR)


def turn_context(usage: dict) -> int:
    """Total context sent on one turn: fresh input + cache reads + cache writes."""
    return (usage.get("input_tokens", 0)
            + usage.get("cache_read_input_tokens", 0)
            + usage.get("cache_creation_input_tokens", 0))


def residency(blocks: list[tuple[int, str, int]], total_turns: int,
              reset_at: int = 0) -> collections.Counter:
    """Sum tokens x turns-resident per category.

    `blocks` is (turn_index, category, tokens). A block appearing before `reset_at` (a compaction)
    stops being resident there; everything else survives to the end of the session.
    """
    out: collections.Counter = collections.Counter()
    for turn, category, tokens in blocks:
        end = reset_at if (reset_at and turn < reset_at) else total_turns
        out[category] += tokens * max(0, end - turn)
    return out


def reconstruct_output(contexts: list[int], fed_in: list[float], visible: list[float],
                       logged: list[int] | None = None) -> list[float]:
    """True output per turn, which the transcript does not reliably record.

    Current Claude Code logs `output_tokens` as a stream-start snapshot (a 42.7k-token reply logs
    as 4); older versions logged the final count on some turns. What a turn produced reappears as
    context on the next turn, so output_i = ctx_{i+1} - ctx_i - fed_in_{i+1}, where fed_in is what
    arrived between the two turns (tool results, user text). A logged count at least half the
    estimate is taken as final and used as-is. Visible content is a floor, and the only estimate
    for a turn with no successor.
    """
    logged = logged or [0] * len(contexts)
    out = []
    for i, ctx in enumerate(contexts):
        estimate = visible[i]
        if i + 1 < len(contexts):
            estimate = max(contexts[i + 1] - ctx - fed_in[i + 1], visible[i])
        chosen = logged[i] if logged[i] >= 0.5 * estimate else estimate
        out.append(max(chosen, visible[i]))
    return out


def turn_cost(usage: dict, output: float, prices: tuple) -> dict:
    """Dollar cost of one turn by component, with cache writes priced by their TTL."""
    written = usage.get("cache_creation_input_tokens", 0)
    one_hour = (usage.get("cache_creation") or {}).get("ephemeral_1h_input_tokens", 0)
    tokens = (usage.get("input_tokens", 0), written - one_hour, one_hour,
              usage.get("cache_read_input_tokens", 0), output)
    return {key: n * price / 1e6 for key, n, price in zip(COST_KEYS, tokens, prices)}


def project_dir(cwd: str) -> str:
    """The transcript directory for a working directory, using Claude Code's slug rule."""
    slug = cwd.replace(":", "-").replace("\\", "-").replace("/", "-")
    return os.path.join(pathlib.Path.home(), ".claude", "projects", slug)


# --------------------------------------------------------------------------- #
# Transcript reading
# --------------------------------------------------------------------------- #
def _entries(path):
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except ValueError:
                continue


def analyse(path: str, price_as: str | None = None) -> dict:
    """Read one transcript into per-turn records.

    Claude Code writes one row per content block, each repeating the message's `usage`, so a turn
    is a distinct message id, not a row with usage — counting rows inflates turns and totals 2-3x.
    """
    tool_names: dict[str, str] = {}
    blocks: list[tuple[int, str, int]] = []
    turns: list[dict] = []
    seen: dict[str, dict] = {}
    compaction_at = 0
    images = 0
    image_token_total = 0
    fed_in = 0.0          # tokens arriving since the last turn (tool results, user text)

    for entry in _entries(path):
        if entry.get("isCompactSummary"):
            compaction_at = len(turns)
        message = entry.get("message") or {}
        content = message.get("content")
        role = message.get("role")
        usage = message.get("usage")
        turn = len(turns)
        record = None
        # "<synthetic>" rows are placeholders Claude Code writes itself (e.g. after an interrupt),
        # not API calls; their zero usage would break the context series.
        if usage and role == "assistant" and message.get("model") != "<synthetic>":
            key = message.get("id") or f"row-{turn}"
            record = seen.get(key)
            if record is None:
                record = {"usage": usage, "model": message.get("model"),
                          "fed_in": fed_in, "visible": 0.0}
                seen[key] = record
                turns.append(record)
                fed_in = 0.0
            record["usage"] = usage
            turn = len(turns) - 1

        if isinstance(content, str) and content:
            blocks.append((turn, "user message", len(content) // CHARS_PER_TOKEN))
            fed_in += len(content) / CHARS_PER_TOKEN
        elif isinstance(content, list):
            for block in content:
                kind = block.get("type")
                if kind == "thinking":
                    blocks.append((turn, "assistant thinking",
                                   len(block.get("thinking", "")) // CHARS_PER_TOKEN))
                elif kind == "text":
                    size = len(block.get("text", "")) / CHARS_PER_TOKEN
                    if role == "assistant":
                        blocks.append((turn, "assistant text", int(size)))
                        if record is not None:
                            record["visible"] += size
                    else:
                        blocks.append((turn, "user message", int(size)))
                        fed_in += size
                elif kind == "tool_use":
                    tool_names[block["id"]] = block["name"]
                    size = len(json.dumps(block.get("input", {}),
                                          ensure_ascii=False)) / CHARS_PER_TOKEN
                    blocks.append((turn, f"tool_use: {block['name']}", int(size)))
                    if record is not None:
                        record["visible"] += size
                elif kind == "tool_result":
                    name = tool_names.get(block.get("tool_use_id"), "?")
                    body = block.get("content")
                    if isinstance(body, str):
                        blocks.append((turn, f"result: {name}", len(body) // CHARS_PER_TOKEN))
                        fed_in += len(body) / CHARS_PER_TOKEN
                    elif isinstance(body, list):
                        for sub in body:
                            if sub.get("type") == "image":
                                raw = b""
                                try:
                                    raw = base64.b64decode(
                                        sub.get("source", {}).get("data", "")[:120000])
                                except Exception:      # noqa: BLE001 — malformed data is not fatal
                                    pass
                                cost = image_tokens(image_dimensions(raw))
                                images += 1
                                image_token_total += cost
                                blocks.append((turn, f"IMAGE via {name}", cost))
                                fed_in += cost
                            elif sub.get("type") == "text":
                                size = len(sub.get("text", "")) / CHARS_PER_TOKEN
                                blocks.append((turn, f"result: {name}", int(size)))
                                fed_in += size

    contexts = [turn_context(t["usage"]) for t in turns]
    outputs = reconstruct_output(contexts, [t["fed_in"] for t in turns],
                                 [t["visible"] for t in turns],
                                 [t["usage"].get("output_tokens", 0) for t in turns])
    totals = collections.Counter()
    cost = collections.Counter()
    unpriced = set()
    for record, output in zip(turns, outputs):
        usage = record["usage"]
        totals["in"] += usage.get("input_tokens", 0)
        totals["cw"] += usage.get("cache_creation_input_tokens", 0)
        totals["cr"] += usage.get("cache_read_input_tokens", 0)
        totals["out"] += output
        totals["visible"] += record["visible"]
        totals["logged_out"] += usage.get("output_tokens", 0)
        prices = PRICES.get(price_as or record["model"])
        if prices:
            cost.update(turn_cost(usage, output, prices))
        else:
            unpriced.add(record["model"])

    return {
        "turns": len(turns),
        "contexts": contexts,
        "per_turn": [(t["usage"].get("output_tokens", 0), out, t["visible"])
                     for t, out in zip(turns, outputs)],
        "totals": totals,
        "cost": cost,
        "models": sorted({t["model"] for t in turns if t["model"]}),
        "price_as": price_as,
        "unpriced": sorted(m for m in unpriced if m),
        "blocks": blocks,
        "images": images,
        "image_tokens": image_token_total,
        "compaction_at": compaction_at,
        "full_rewrites": sum(1 for t in turns
                             if t["usage"].get("cache_creation_input_tokens", 0) > 60000),
    }


def raw_volume(totals: collections.Counter) -> float:
    """Fresh input + cache writes + cache reads + (reconstructed) output, unweighted."""
    return totals["in"] + totals["cw"] + totals["cr"] + totals["out"]


def print_cost(label: str, data: dict, pages: int | None = None) -> None:
    """The price-weighted breakdown: what the run is billed for, component by component."""
    cost, totals = data["cost"], data["totals"]
    dollars = sum(cost.values())
    priced = f"; priced as {data['price_as']}" if data.get("price_as") else ""
    print(f"\n  cost at API list prices ({label}; models: {', '.join(data['models']) or '?'}"
          f"{priced})")
    if data["unpriced"]:
        print(f"    not priced (no entry in PRICES): {', '.join(data['unpriced'])}")
    rows = (("cache reads", totals["cr"], cost["read"]),
            ("cache writes", totals["cw"], cost["write_5m"] + cost["write_1h"]),
            ("fresh input", totals["in"], cost["input"]),
            ("output (reconstructed)", totals["out"], cost["output"]))
    for name, tokens, usd in rows:
        share = 100 * usd / dollars if dollars else 0
        print(f"    {name:24s} {tokens/1e3:9.0f}k  ${usd:8.2f}  {share:5.1f}%")
    thinking = max(0.0, totals["out"] - totals["visible"])
    print(f"      of output: visible ~{totals['visible']/1e3:.0f}k, "
          f"thinking ~{thinking/1e3:.0f}k (estimate; logged output was "
          f"{totals['logged_out']/1e3:.1f}k)")
    print(f"    {'total':24s} {raw_volume(totals)/1e6:8.2f}M  ${dollars:8.2f}   (raw volume, "
          f"unweighted, on the left)")
    if pages:
        print(f"    per page ({pages})           {raw_volume(totals)/pages/1e3:8.0f}k  "
              f"${dollars/pages:8.2f}")


def subagent_transcripts(path: str) -> list[tuple[str, str]]:
    """(description, path) for each subagent of a session, from <session>/subagents/."""
    directory = os.path.join(path[:-len(".jsonl")], "subagents")
    if not os.path.isdir(directory):
        return []
    out = []
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".jsonl"):
            continue
        description = name[:-len(".jsonl")]
        meta = os.path.join(directory, name[:-len(".jsonl")] + ".meta.json")
        try:
            with open(meta, encoding="utf-8") as handle:
                description = json.load(handle).get("description") or description
        except (OSError, ValueError):
            pass
        out.append((description, os.path.join(directory, name)))
    return out


def report_subagents(path: str, pages: int | None, price_as: str | None = None,
                     only: str | None = None) -> None:
    subagents = [(d, p) for d, p in subagent_transcripts(path)
                 if not only or only.lower() in d.lower()]
    if not subagents:
        print("\n  no subagent transcripts for this session")
        return
    combined = {"totals": collections.Counter(), "cost": collections.Counter(),
                "models": set(), "unpriced": set()}
    print(f"\n  subagents ({len(subagents)}):")
    print(f"    {'description':40s} {'turns':>5s} {'reads':>8s} {'writes':>7s} "
          f"{'output':>7s} {'cost':>8s}")
    for description, sub_path in subagents:
        data = analyse(sub_path, price_as)
        totals = data["totals"]
        print(f"    {description[:40]:40s} {data['turns']:5d} {totals['cr']/1e3:7.0f}k "
              f"{totals['cw']/1e3:6.0f}k {totals['out']/1e3:6.1f}k "
              f"${sum(data['cost'].values()):7.2f}")
        combined["totals"].update(totals)
        combined["cost"].update(data["cost"])
        combined["models"].update(data["models"])
        combined["unpriced"].update(data["unpriced"])
    combined["models"] = sorted(combined["models"])
    combined["price_as"] = price_as
    combined["unpriced"] = sorted(combined["unpriced"])
    print_cost("all subagents", combined, pages)


def report(path: str, pages: int | None, price_as: str | None = None,
           only: str | None = None) -> None:
    data = analyse(path, price_as)
    turns, contexts, totals = data["turns"], data["contexts"], data["totals"]
    if not turns:
        print(f"{path}: no usage data")
        return
    print(f"session   {os.path.basename(path)}")
    print(f"  turns                  {turns}")
    print(f"  mean context/turn      {sum(contexts)//turns/1000:.0f}k")
    print(f"  peak context           {max(contexts)/1000:.0f}k")
    print(f"  raw volume             {raw_volume(totals)/1e6:.1f}M")
    print(f"    cache read {totals['cr']/1e6:.1f}M   cache write {totals['cw']/1e6:.2f}M   "
          f"output ~{totals['out']/1000:.0f}k")
    print(f"  images read            {data['images']} ({data['image_tokens']/1000:.0f}k tokens)")
    print(f"  full-context rewrites  {data['full_rewrites']} "
          f"({100*data['full_rewrites']/turns:.1f}% of turns)")
    if data["compaction_at"]:
        print(f"  compacted at turn      {data['compaction_at']}")
    print_cost("this session, excluding subagents", data, pages)

    res = residency(data["blocks"], turns, data["compaction_at"])
    total_res = sum(res.values()) or 1
    print("\n  where the context went (tokens x turns resident):")
    for category, value in res.most_common(10):
        print(f"    {category[:34]:34s} {value/1e6:8.0f}M  {100*value/total_res:5.1f}%")

    report_subagents(path, pages, price_as, only)


def list_sessions(directory: str, limit: int) -> None:
    rows = []
    for name in os.listdir(directory):
        if not name.endswith(".jsonl"):
            continue
        path = os.path.join(directory, name)
        total = 0
        turns = 0
        seen = set()
        for entry in _entries(path):
            message = entry.get("message") or {}
            usage = message.get("usage")
            if usage and message.get("id") not in seen:
                seen.add(message.get("id"))
                turns += 1
                total += turn_context(usage)
        rows.append((total, turns, name[:-6]))
    rows.sort(reverse=True)
    print(f"{'session':40s} {'turns':>7s} {'total':>9s}")
    for total, turns, sid in rows[:limit]:
        print(f"{sid:40s} {turns:7d} {total/1e6:8.1f}M")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("session", nargs="?", help="session id, or a path to a .jsonl transcript")
    parser.add_argument("--list", action="store_true", help="rank this project's sessions by cost")
    parser.add_argument("--limit", type=int, default=15, help="rows for --list (default 15)")
    parser.add_argument("--pages", type=int, help="pages transcribed, to report tokens per page")
    parser.add_argument("--price-as", choices=sorted(PRICES),
                        help="price every turn as this model (re-pricing an old run's tokens)")
    parser.add_argument("--only", metavar="TEXT",
                        help="report only subagents whose description contains TEXT")
    parser.add_argument("--project", default=os.getcwd(),
                        help="working directory whose transcripts to read (default: cwd)")
    args = parser.parse_args(argv)

    directory = project_dir(args.project)
    if args.list:
        if not os.path.isdir(directory):
            print(f"error: no transcripts at {directory}", file=sys.stderr)
            return 1
        list_sessions(directory, args.limit)
        return 0
    if not args.session:
        parser.error("give a session id or --list")

    path = args.session
    if not os.path.isfile(path):
        path = os.path.join(directory, f"{args.session}.jsonl")
    if not os.path.isfile(path):
        print(f"error: no transcript at {path}", file=sys.stderr)
        return 1
    report(path, args.pages, args.price_as, args.only)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
