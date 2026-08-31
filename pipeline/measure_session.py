#!/usr/bin/env python3
"""Measure what a Claude Code session actually cost, and where the context went.

A transcription run's cost is dominated not by what it reads once but by what it keeps re-sending:
every page image read stays in context and is re-sent on every later turn. This script reports that
directly, so a change to the pipeline can be measured rather than guessed at.

Usage:
    python pipeline/measure_session.py --list
    python pipeline/measure_session.py <session-id-or-path> [--pages N]

`--list` ranks the sessions for this project by total tokens. Given a session it reports turns,
context per turn, the token total, and a residency breakdown: each content block's size multiplied
by the number of later turns it stays resident, which is what actually drives the bill.

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
IMAGE_TOKEN_DIVISOR = 750
IMAGE_MAX_EDGE = 1568
FALLBACK_IMAGE_TOKENS = 1500
CHARS_PER_TOKEN = 4  # rough, for text blocks; LaTeX runs denser (~3)


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


def analyse(path: str) -> dict:
    tool_names: dict[str, str] = {}
    blocks: list[tuple[int, str, int]] = []
    contexts: list[int] = []
    totals = collections.Counter()
    compaction_at = 0
    turn = 0
    images = 0
    image_token_total = 0
    full_rewrites = 0

    for entry in _entries(path):
        if entry.get("isCompactSummary"):
            compaction_at = turn
        message = entry.get("message") or {}
        content = message.get("content")
        role = message.get("role")

        if isinstance(content, str) and content:
            blocks.append((turn, "user message", len(content) // CHARS_PER_TOKEN))
        elif isinstance(content, list):
            for block in content:
                kind = block.get("type")
                if kind == "thinking":
                    blocks.append((turn, "assistant thinking",
                                   len(block.get("thinking", "")) // CHARS_PER_TOKEN))
                elif kind == "text":
                    label = "assistant text" if role == "assistant" else "user message"
                    blocks.append((turn, label, len(block.get("text", "")) // CHARS_PER_TOKEN))
                elif kind == "tool_use":
                    tool_names[block["id"]] = block["name"]
                    blocks.append((turn, f"tool_use: {block['name']}",
                                   len(json.dumps(block.get("input", {}))) // CHARS_PER_TOKEN))
                elif kind == "tool_result":
                    name = tool_names.get(block.get("tool_use_id"), "?")
                    body = block.get("content")
                    if isinstance(body, str):
                        blocks.append((turn, f"result: {name}", len(body) // CHARS_PER_TOKEN))
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
                            elif sub.get("type") == "text":
                                blocks.append((turn, f"result: {name}",
                                               len(sub.get("text", "")) // CHARS_PER_TOKEN))

        usage = message.get("usage")
        if usage:
            for key, field in (("in", "input_tokens"), ("out", "output_tokens"),
                               ("cw", "cache_creation_input_tokens"),
                               ("cr", "cache_read_input_tokens")):
                totals[key] += usage.get(field, 0)
            contexts.append(turn_context(usage))
            if usage.get("cache_creation_input_tokens", 0) > 60000:
                full_rewrites += 1
            turn += 1

    return {
        "turns": turn,
        "contexts": contexts,
        "totals": totals,
        "blocks": blocks,
        "images": images,
        "image_tokens": image_token_total,
        "compaction_at": compaction_at,
        "full_rewrites": full_rewrites,
    }


def report(path: str, pages: int | None) -> None:
    data = analyse(path)
    turns, contexts, totals = data["turns"], data["contexts"], data["totals"]
    if not turns:
        print(f"{path}: no usage data")
        return
    grand = sum(totals.values())
    print(f"session   {os.path.basename(path)}")
    print(f"  turns                  {turns}")
    print(f"  mean context/turn      {sum(contexts)//turns/1000:.0f}k")
    print(f"  peak context           {max(contexts)/1000:.0f}k")
    print(f"  total tokens           {grand/1e6:.1f}M")
    print(f"    cache read {totals['cr']/1e6:.1f}M   cache write {totals['cw']/1e6:.2f}M   "
          f"output {totals['out']/1000:.0f}k")
    print(f"  images read            {data['images']} ({data['image_tokens']/1000:.0f}k tokens)")
    print(f"  full-context rewrites  {data['full_rewrites']} "
          f"({100*data['full_rewrites']/turns:.1f}% of turns)")
    if data["compaction_at"]:
        print(f"  compacted at turn      {data['compaction_at']}")
    if pages:
        print(f"  PER PAGE ({pages} pages)  {grand/pages/1000:.0f}k tokens/page")

    res = residency(data["blocks"], turns, data["compaction_at"])
    total_res = sum(res.values()) or 1
    print("\n  where the context went (tokens x turns resident):")
    for category, value in res.most_common(10):
        print(f"    {category[:34]:34s} {value/1e6:8.0f}M  {100*value/total_res:5.1f}%")


def list_sessions(directory: str, limit: int) -> None:
    rows = []
    for name in os.listdir(directory):
        if not name.endswith(".jsonl"):
            continue
        path = os.path.join(directory, name)
        total = 0
        turns = 0
        for entry in _entries(path):
            usage = (entry.get("message") or {}).get("usage")
            if usage:
                turns += 1
                total += turn_context(usage) + usage.get("output_tokens", 0)
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
    report(path, args.pages)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
