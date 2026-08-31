#!/usr/bin/env python3
"""Prepare scan pages for transcription: one image per page, cropped to the printed text block.

Why one image per page, and why crop. The vision API downscales anything whose long edge exceeds
1568px, so a 1462x1999 full-page scan is effectively read at 1147px across the page width — losing
detail on dense 19th-century mathematics. Splitting the page into halves recovers resolution but
costs two images AND an extra turn per page, and turns are what dominate the bill: measured, three
quarters of a batch subagent's cost is the fixed baseline re-sent on every turn. Since most of a
scanned page is margin, cropping to the printed text block spends the same 1568px budget on text
and reaches half-page resolution at one image, one Read, one turn.

Usage:
    python pipeline/prepare_pages.py --images ./scans --pages 189-243 --out ./prepared
        [--max-edge 1568] [--margin 0.02] [--no-crop 215,216] [--dry-run]

Input images are named by printed page number (189.jpg, 0189.png, p189.jpg ...). Output is
<out>/p<N>.png, one per page, plus a report line per page on stdout.

Pillow is a contributor-only dependency, imported lazily, exactly like `anthropic` in
transcribe.py. `pipeline/validate.py` and CI never import this module, so the copyright gate keeps
its single PyYAML dependency (see tests/test_prepare_pages.py).
"""
from __future__ import annotations

import argparse
import os
import re
import sys

DEFAULT_MAX_EDGE = 1568      # above this the vision API downscales, so resolution above it is lost
DEFAULT_MARGIN = 0.02        # padding around the detected text block, as a fraction of the page
DEFAULT_THRESHOLD = 200      # 0-255; below this a pixel counts as ink
MIN_BLOCK_FRACTION = 0.25    # a "text block" smaller than this fraction of the page is not trusted
IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp")


# --------------------------------------------------------------------------- #
# Pure helpers (unit-tested — no Pillow, no filesystem)
# --------------------------------------------------------------------------- #
def parse_pages(spec: str) -> list[int]:
    """Parse "189-243" or "189,191,200-204" into a sorted, de-duplicated list."""
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part[1:]:
            lo, _, hi = part.partition("-")
            start, end = int(lo), int(hi)
            if end < start:
                raise ValueError(f"descending page range: {part!r}")
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    if not pages:
        raise ValueError("no pages given")
    return sorted(pages)


def resolve_page_images(names: list[str], pages: list[int]) -> dict[int, str]:
    """Map each page number to a file whose stem ends in that number (zero padding allowed)."""
    by_page: dict[int, str] = {}
    for name in sorted(names):
        stem, ext = os.path.splitext(name)
        if ext.lower() not in IMAGE_SUFFIXES:
            continue
        match = re.search(r"(\d+)$", stem)
        if not match:
            continue
        number = int(match.group(1))
        by_page.setdefault(number, name)
    return {p: by_page[p] for p in pages if p in by_page}


def scale_to_max_edge(width: int, height: int, max_edge: int) -> tuple[int, int]:
    """Scale (w, h) down so the long edge is at most max_edge. Never scales up."""
    longest = max(width, height)
    if longest <= max_edge or longest == 0:
        return width, height
    scale = max_edge / longest
    return max(1, round(width * scale)), max(1, round(height * scale))


def estimate_image_tokens(width: int, height: int) -> int:
    """Roughly what the vision API will bill for an image of this size."""
    w, h = scale_to_max_edge(width, height, DEFAULT_MAX_EDGE)
    return int(w * h / 750)


def pad_box(box: tuple[int, int, int, int], width: int, height: int,
            margin: float) -> tuple[int, int, int, int]:
    """Grow a crop box by `margin` (fraction of the page's smaller side), clamped to the page."""
    left, top, right, bottom = box
    pad = int(min(width, height) * margin)
    return (max(0, left - pad), max(0, top - pad),
            min(width, right + pad), min(height, bottom + pad))


def block_is_trustworthy(box: tuple[int, int, int, int], width: int, height: int) -> bool:
    """Reject a detected block that is implausibly small — a fold, a plate, or a blank page."""
    left, top, right, bottom = box
    if right <= left or bottom <= top:
        return False
    area = (right - left) * (bottom - top)
    return area >= MIN_BLOCK_FRACTION * width * height


# --------------------------------------------------------------------------- #
# Image work (lazily imports Pillow)
# --------------------------------------------------------------------------- #
def _pillow():
    try:
        from PIL import Image  # noqa: PLC0415 — contributor-only dependency, imported lazily
    except ImportError:
        raise SystemExit(
            "error: the 'Pillow' package is required to prepare pages.\n"
            "       pip install Pillow\n"
            "       (it is NOT needed by pipeline/validate.py or CI.)"
        )
    return Image


def detect_text_block(image, threshold: int = DEFAULT_THRESHOLD):
    """Bounding box of the inked area, or None if nothing convincing was found."""
    grey = image.convert("L")
    # Everything darker than `threshold` becomes non-zero; getbbox() then bounds the ink.
    mask = grey.point(lambda value: 255 if value < threshold else 0)
    return mask.getbbox()


def prepare_page(path: str, out_path: str, max_edge: int, margin: float,
                 crop: bool = True) -> dict:
    """Crop one page to its text block and scale it. Returns a report dict; never raises on a
    page whose block cannot be found — it falls back to the uncropped page."""
    Image = _pillow()
    with Image.open(path) as image:
        image.load()
        source_size = image.size
        width, height = source_size
        note = ""
        box = None
        if crop:
            try:
                box = detect_text_block(image)
            except Exception:                      # noqa: BLE001 — detection must never be fatal
                box = None
            if box and block_is_trustworthy(box, width, height):
                box = pad_box(box, width, height, margin)
            else:
                note = "no trustworthy text block — kept full page"
                box = None
        else:
            note = "crop disabled for this page"

        cropped = image.crop(box) if box else image
        target = scale_to_max_edge(cropped.width, cropped.height, max_edge)
        if target != cropped.size:
            cropped = cropped.resize(target, Image.LANCZOS)
        cropped.convert("L").save(out_path, "PNG", optimize=True)

    return {
        "source_size": source_size,
        "box": box,
        "out_size": target,
        "tokens": estimate_image_tokens(*target),
        "note": note,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--images", required=True, help="directory of scan pages")
    parser.add_argument("--pages", required=True, help='page spec, e.g. "189-243"')
    parser.add_argument("--out", required=True, help="output directory")
    parser.add_argument("--max-edge", type=int, default=DEFAULT_MAX_EDGE,
                        help=f"long-edge cap in px (default {DEFAULT_MAX_EDGE})")
    parser.add_argument("--margin", type=float, default=DEFAULT_MARGIN,
                        help=f"padding around the text block (default {DEFAULT_MARGIN})")
    parser.add_argument("--no-crop", default="",
                        help="comma-separated pages to pass through uncropped")
    parser.add_argument("--dry-run", action="store_true", help="report without writing files")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.images):
        print(f"error: no such directory: {args.images}", file=sys.stderr)
        return 1
    try:
        pages = parse_pages(args.pages)
        skip_crop = set(parse_pages(args.no_crop)) if args.no_crop.strip() else set()
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    found = resolve_page_images(os.listdir(args.images), pages)
    missing = [p for p in pages if p not in found]
    if missing:
        print(f"error: no image found for page(s): {', '.join(map(str, missing))}", file=sys.stderr)
        return 1

    if not args.dry_run:
        os.makedirs(args.out, exist_ok=True)

    total_tokens = 0
    fallbacks = 0
    for page in pages:
        src = os.path.join(args.images, found[page])
        dst = os.path.join(args.out, f"p{page}.png")
        if args.dry_run:
            print(f"p{page}: would prepare from {found[page]}")
            continue
        result = prepare_page(src, dst, args.max_edge, args.margin,
                              crop=page not in skip_crop)
        total_tokens += result["tokens"]
        if result["note"]:
            fallbacks += 1
        sw, sh = result["source_size"]
        ow, oh = result["out_size"]
        box = result["box"]
        boxtxt = f"crop {box[0]},{box[1]}-{box[2]},{box[3]}" if box else "no crop"
        suffix = f"  [{result['note']}]" if result["note"] else ""
        print(f"p{page}: {sw}x{sh} -> {boxtxt} -> {ow}x{oh}  ~{result['tokens']} tokens{suffix}")

    if not args.dry_run and pages:
        print(f"\n{len(pages)} page(s), ~{total_tokens} image tokens "
              f"({total_tokens // len(pages)} per page)")
        if fallbacks:
            print(f"{fallbacks} page(s) kept full — check those crops by eye before transcribing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
