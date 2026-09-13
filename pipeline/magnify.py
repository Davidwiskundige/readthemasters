#!/usr/bin/env python3
"""Magnify doubtful regions of a prepared page — all of a page's regions in one invocation.

Why this exists, and why it takes many regions at once. A batch subagent reads one prepared image
per page, which costs about 21% of the page's text width to the 1568px long-edge cap. It buys that
back by cropping a doubtful region out of the *source* scan, where the detail still is. Measured on
Clebsch pp. 223-243, that escalation ran at 1.7 regions per page and each region cost two turns —
one to compute and save the crop, one to read it. Turns are three quarters of a subagent's bill, so
per-region cropping roughly doubled the cost of a page.

This helper collapses that: one invocation writes every region for a page, and the subagent reads
them in a single turn by issuing parallel Read calls in one message. Six turns become two at the
three-region cap.

It also owns the coordinate conversion. The subagent names regions in the coordinate space of the
image it can actually see — the prepared page — and this helper applies `zoom-map.json` to reach
the source scan. A batch that did that arithmetic by hand landed 2 of its 3 crops on the wrong
lines and spent its whole per-page budget settling nothing; that is now tested code rather than a
warning in a prompt.

Usage:
    python pipeline/magnify.py --prepared ./prepared --scans ./scans --page 227 \
        --regions "120,340,520,382; 80,700,300,744" --out ./crops
        [--target-edge 1400] [--cap 3] [--dry-run]

Regions are `left,top,right,bottom` in PREPARED-image pixels, separated by `;`. Output is
<out>/p<page>-r<i>.png, one per region, plus a report line per crop on stdout.

Pillow is a contributor-only dependency, imported lazily, exactly like in prepare_pages.py.
`pipeline/validate.py` and CI never import this module, so the copyright gate keeps its single
PyYAML dependency (see tests/test_magnify.py).
"""
from __future__ import annotations

import argparse
import json
import os
import sys

DEFAULT_TARGET_EDGE = 1400   # what a magnified crop is scaled to; under the 1568px vision cap
MAX_EDGE = 1568              # above this the vision API downscales, so resolution above it is lost
DEFAULT_CAP = 3              # magnified regions per page (transcription-pipeline spec)
# A region smaller than this in SOURCE pixels cannot be a glyph — it is a mis-typed coordinate or a
# box named in the wrong space. Cropping it would produce a plausible-looking image of nothing,
# which is the failure mode prepare_pages.py's whole-page check exists to prevent: a silent no-op
# costs the subagent its escalation budget without telling anyone.
MIN_REGION_PX = 8


# --------------------------------------------------------------------------- #
# Pure helpers (unit-tested — no Pillow, no filesystem)
# --------------------------------------------------------------------------- #
def parse_regions(spec: str) -> list[tuple[int, int, int, int]]:
    """Parse "l,t,r,b; l,t,r,b" into a list of boxes, in the order given.

    Order is preserved and duplicates are kept: the subagent numbers its own crops, and silently
    dropping or reordering one would misalign its reading of the results.
    """
    regions: list[tuple[int, int, int, int]] = []
    for part in spec.split(";"):
        part = part.strip()
        if not part:
            continue
        fields = [f.strip() for f in part.split(",")]
        if len(fields) != 4:
            raise ValueError(f"region needs 4 comma-separated numbers, got {part!r}")
        try:
            left, top, right, bottom = (int(round(float(f))) for f in fields)
        except ValueError:
            raise ValueError(f"region has a non-numeric coordinate: {part!r}") from None
        if right <= left or bottom <= top:
            raise ValueError(f"region is empty or inverted (need left<right, top<bottom): {part!r}")
        regions.append((left, top, right, bottom))
    if not regions:
        raise ValueError("no regions given")
    return regions


def load_page_mapping(zoom_map: dict, page: int) -> dict:
    """Pull one page's row out of a parsed zoom-map.json, with a message that names the fix."""
    pages = zoom_map.get("pages", {})
    row = pages.get(str(page))
    if row is None:
        known = ", ".join(sorted(pages, key=lambda p: int(p))[:8]) or "none"
        raise ValueError(f"page {page} is not in the zoom map (it has: {known}). "
                         f"Prepare that page first with prepare_pages.py.")
    for key in ("offset_x", "offset_y", "scale", "source"):
        if key not in row:
            raise ValueError(f"zoom map row for page {page} is missing {key!r}")
    if not row["scale"]:
        raise ValueError(f"zoom map row for page {page} has scale 0")
    return row


def to_source_box(region: tuple[int, int, int, int],
                  mapping: dict) -> tuple[int, int, int, int]:
    """Map a prepared-image box onto the source scan: source = offset + prepared / scale."""
    left, top, right, bottom = region
    ox, oy, scale = mapping["offset_x"], mapping["offset_y"], mapping["scale"]
    return (int(ox + left / scale), int(oy + top / scale),
            int(ox + right / scale), int(oy + bottom / scale))


def clamp_box(box: tuple[int, int, int, int],
              size: tuple[int, int]) -> tuple[tuple[int, int, int, int], bool]:
    """Clamp a box to the page. Returns (clamped, was_clamped)."""
    width, height = size
    left, top, right, bottom = box
    clamped = (max(0, min(left, width)), max(0, min(top, height)),
               max(0, min(right, width)), max(0, min(bottom, height)))
    return clamped, clamped != box


def check_source_box(box: tuple[int, int, int, int], size: tuple[int, int],
                     region: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Clamp to the page and refuse anything that survives as less than a glyph.

    Loud, not lenient. A region that lands off the page or collapses to a few pixels means the
    coordinates were named in the wrong space or mistyped, and returning a crop of blank paper
    would spend the subagent's escalation budget while looking like it worked.
    """
    clamped, was_clamped = clamp_box(box, size)
    left, top, right, bottom = clamped
    if right - left < MIN_REGION_PX or bottom - top < MIN_REGION_PX:
        raise ValueError(
            f"region {region} maps to {box} on a {size[0]}x{size[1]} scan, which is off the page "
            f"or smaller than {MIN_REGION_PX}px. Name regions in PREPARED-image coordinates — the "
            f"helper converts them.")
    return clamped


def existing_crops(out_dir: str, page: int) -> list[str]:
    """Crops already written for this page, so the cap counts across invocations."""
    if not os.path.isdir(out_dir):
        return []
    prefix = f"p{page}-r"
    return sorted(n for n in os.listdir(out_dir)
                  if n.startswith(prefix) and n.endswith(".png"))


def enforce_cap(regions: list, cap: int, page: int, already: int = 0) -> None:
    """Refuse more regions than the per-page cap allows, counting earlier calls for this page.

    The cap lives here rather than only in the skill's prose because this helper makes magnification
    cheap, and the measured behaviour when it is cheap and ungoverned is 32 crops for 4 pages.

    `already` exists because the cap is specified PER PAGE, not per invocation. A first version
    counted only the current call, and a measured batch duly took "3 + 1 follow-up" regions on one
    page — within the cap twice over, past it in total — and silently overwrote its own first crop,
    because the output names restart at r1 on every call. Counting what is already on disk closes
    both holes at once.
    """
    total = len(regions) + already
    if total > cap:
        seen = f" ({already} already written for this page)" if already else ""
        raise ValueError(
            f"page {page}: {len(regions)} regions requested{seen}, cap is {cap} per page. Magnify "
            f"the {cap} that most need it and flag the rest with \\uncertain{{}} — that is the "
            f"honest signal. A second call does not buy more regions.")


def scale_to_edge(width: int, height: int, target_edge: int) -> tuple[int, int]:
    """Scale (w, h) so the long edge is `target_edge`, never above the vision cap."""
    target = min(target_edge, MAX_EDGE)
    longest = max(width, height)
    if longest == 0:
        return width, height
    factor = target / longest
    return max(1, round(width * factor)), max(1, round(height * factor))


def estimate_image_tokens(width: int, height: int) -> int:
    """Roughly what the vision API will bill for an image of this size."""
    w, h = scale_to_edge(width, height, MAX_EDGE)
    return int(w * h / 750)


# --------------------------------------------------------------------------- #
# Pillow-backed
# --------------------------------------------------------------------------- #
def _pillow():
    try:
        from PIL import Image
    except ImportError:                                            # pragma: no cover
        print("error: this helper needs Pillow (pip install -r pipeline/requirements.txt)",
              file=sys.stderr)
        raise SystemExit(1) from None
    return Image


def magnify_page(scan_path: str, regions: list[tuple[int, int, int, int]], mapping: dict,
                 out_dir: str, page: int, target_edge: int) -> list[dict]:
    """Crop every region out of one source scan and write them. Returns a report per crop."""
    Image = _pillow()
    reports: list[dict] = []
    with Image.open(scan_path) as image:
        image.load()
        size = image.size
        for index, region in enumerate(regions, start=1):
            raw = to_source_box(region, mapping)
            box = check_source_box(raw, size, region)
            crop = image.crop(box)
            target = scale_to_edge(crop.width, crop.height, target_edge)
            if target != crop.size:
                crop = crop.resize(target, Image.LANCZOS)
            out_path = os.path.join(out_dir, f"p{page}-r{index}.png")
            crop.convert("L").save(out_path, "PNG", optimize=True)
            reports.append({
                "region": region,
                "source_box": box,
                "clamped": box != raw,
                "out_size": target,
                "tokens": estimate_image_tokens(*target),
                "path": out_path,
            })
    return reports


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--prepared", required=True,
                        help="directory prepare_pages.py wrote (holds zoom-map.json)")
    parser.add_argument("--scans", required=True, help="directory of source scan pages")
    parser.add_argument("--page", required=True, type=int, help="printed page number")
    parser.add_argument("--regions", required=True,
                        help='"l,t,r,b; l,t,r,b" in PREPARED-image pixels')
    parser.add_argument("--out", required=True, help="output directory for the crops")
    parser.add_argument("--target-edge", type=int, default=DEFAULT_TARGET_EDGE,
                        help=f"long edge of each crop in px (default {DEFAULT_TARGET_EDGE}, "
                             f"capped at {MAX_EDGE})")
    parser.add_argument("--cap", type=int, default=DEFAULT_CAP,
                        help=f"maximum regions per page (default {DEFAULT_CAP})")
    parser.add_argument("--dry-run", action="store_true",
                        help="report the source boxes without writing files")
    args = parser.parse_args(argv)

    map_path = os.path.join(args.prepared, "zoom-map.json")
    if not os.path.isfile(map_path):
        print(f"error: no zoom map at {map_path} — run prepare_pages.py first", file=sys.stderr)
        return 1
    try:
        with open(map_path, encoding="utf-8") as fh:
            zoom_map = json.load(fh)
        regions = parse_regions(args.regions)
        already = existing_crops(args.out, args.page)
        enforce_cap(regions, args.cap, args.page, len(already))
        mapping = load_page_mapping(zoom_map, args.page)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    scan_path = os.path.join(args.scans, mapping["source"])
    if not os.path.isfile(scan_path):
        print(f"error: source scan not found: {scan_path}", file=sys.stderr)
        return 1

    if args.dry_run:
        for index, region in enumerate(regions, start=1):
            print(f"p{args.page}-r{index}: {region} -> source {to_source_box(region, mapping)}")
        return 0

    os.makedirs(args.out, exist_ok=True)
    try:
        reports = magnify_page(scan_path, regions, mapping, args.out, args.page, args.target_edge)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    total = 0
    for report in reports:
        left, top, right, bottom = report["source_box"]
        ow, oh = report["out_size"]
        note = "  [clamped to the page edge]" if report["clamped"] else ""
        total += report["tokens"]
        print(f"{report['path']}: {report['region']} -> crop {left},{top}-{right},{bottom} "
              f"-> {ow}x{oh}  ~{report['tokens']} tokens{note}")
    print(f"\n{len(reports)} crop(s) for page {args.page}, ~{total} image tokens. "
          f"Read them in ONE message so they cost one turn, not one turn each.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
