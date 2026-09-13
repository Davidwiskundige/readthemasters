#!/usr/bin/env python3
"""Generate the index-card thumbnail beside an author's committed portrait.

Why a committed derivative. `/authors/` draws each portrait in a 69x86 box. The full-size
portraits average 80KB and peak at 236KB, which is an absurd payload for an image that size:
the whole set is 1,040KB against 66KB for these derivatives, a 16x reduction. Generating them at
build time instead would put Pillow in pipeline/requirements.txt, which CI installs for the
copyright gate too — and that gate's single PyYAML dependency is deliberate. So the bytes are
committed alongside the portrait they come from, exactly like the portrait itself.

Usage:
    python pipeline/make_portrait_thumb.py --all [--corpus corpus] [--force]
    python pipeline/make_portrait_thumb.py leonhard-euler bernhard-riemann [--force]

Output is <corpus>/authors/<slug>/portrait-thumb.jpg, the sibling name build_site_data.py looks
for. An existing file is left alone unless --force: the crop below is a heuristic, and a portrait
it frames badly is meant to be cropped by hand and committed over, which only works if the tool
cannot silently undo it.

Pillow is a contributor-only dependency, imported lazily, exactly like prepare_pages.py. Neither
`pipeline/validate.py` nor CI imports this module.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# 2x the 69x86 display box, so the thumbnail stays sharp on a high-density screen. The aspect
# ratio (0.802) is the one the corpus already clusters on: of the 13 portraits committed when this
# was written, 11 sit between 0.77 and 0.87, so the cover-crop below discards very little.
THUMB_W, THUMB_H = 138, 172
# Faces in a formal portrait sit above centre — a centred vertical crop cuts foreheads and leaves
# empty coat. Measured against the corpus, taking the window from 18% down the (scaled) image
# frames the head well for engravings and photographs alike.
TOP_BIAS = 0.18
JPEG_QUALITY = 82
THUMB_SUFFIX = "-thumb"


def _pillow():
    try:
        from PIL import Image  # noqa: PLC0415 — contributor-only, imported lazily
    except ImportError:
        raise SystemExit(
            "error: the 'Pillow' package is required to make portrait thumbnails.\n"
            "       pip install Pillow\n"
            "       (it is NOT needed by pipeline/validate.py or CI.)"
        )
    return Image


def thumb_path(portrait: Path) -> Path:
    """The derivative's path beside its portrait: portrait.jpg -> portrait-thumb.jpg.

    The same stem+suffix convention build_site_data.resolve_portrait() uses to find it, so the two
    must agree. The derivative is always .jpg regardless of the source's suffix.
    """
    return portrait.with_name(portrait.stem + THUMB_SUFFIX + ".jpg")


def make_thumb(portrait: Path, dest: Path) -> tuple[int, int]:
    """Write a THUMB_W x THUMB_H cover-crop of `portrait` to `dest`. Returns (source, dest) bytes."""
    Image = _pillow()
    with Image.open(portrait) as im:
        im = im.convert("RGB")
        scale = max(THUMB_W / im.width, THUMB_H / im.height)
        scaled = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        left = (scaled.width - THUMB_W) // 2
        top = int((scaled.height - THUMB_H) * TOP_BIAS)
        scaled.crop((left, top, left + THUMB_W, top + THUMB_H)).save(
            dest, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    return portrait.stat().st_size, dest.stat().st_size


def portraits_in(authors_dir: Path, slugs: list[str]) -> list[Path]:
    """Committed portraits for the named slugs, or for every author when none are named."""
    if slugs:
        found = []
        for slug in slugs:
            hits = sorted(p for p in (authors_dir / slug).glob("portrait.*")
                          if not p.stem.endswith(THUMB_SUFFIX))
            if not hits:
                print(f"warning: no portrait found for {slug}", file=sys.stderr)
            found.extend(hits)
        return found
    return sorted(p for p in authors_dir.glob("*/portrait.*")
                  if not p.stem.endswith(THUMB_SUFFIX))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("slugs", nargs="*", help="author slugs; omit and pass --all for every one")
    parser.add_argument("--corpus", default="corpus", help="corpus directory (default: corpus)")
    parser.add_argument("--all", action="store_true", help="process every author with a portrait")
    parser.add_argument("--force", action="store_true",
                        help="overwrite an existing thumbnail (including a hand-cropped one)")
    args = parser.parse_args(argv)

    if not args.slugs and not args.all:
        parser.error("name at least one slug, or pass --all")

    authors_dir = Path(args.corpus) / "authors"
    if not authors_dir.is_dir():
        print(f"error: no such directory: {authors_dir}", file=sys.stderr)
        return 1

    portraits = portraits_in(authors_dir, args.slugs)
    if not portraits:
        print("error: no portraits to process", file=sys.stderr)
        return 1

    total_src = total_dest = 0
    written = skipped = 0
    for portrait in portraits:
        slug = portrait.parent.name
        dest = thumb_path(portrait)
        if dest.exists() and not args.force:
            total_dest += dest.stat().st_size
            skipped += 1
            print(f"{slug:40s} exists, kept ({dest.stat().st_size / 1024:.1f}K) — --force to redo")
            continue
        src_bytes, dest_bytes = make_thumb(portrait, dest)
        total_src += src_bytes
        total_dest += dest_bytes
        written += 1
        print(f"{slug:40s} {src_bytes / 1024:7.1f}K -> {dest_bytes / 1024:6.1f}K  {dest.name}")

    print(f"\n{written} written, {skipped} kept. "
          f"Thumbnails total {total_dest / 1024:.1f}K.")
    if written:
        print("Review each crop before committing: the framing is a heuristic, and a portrait it\n"
              "frames badly should be cropped by hand and committed over (this tool will keep it).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
