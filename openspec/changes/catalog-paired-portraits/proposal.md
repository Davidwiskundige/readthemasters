## Why

One work in the corpus has two authors — `castelnuovo-enriques-1897-surfaces-algebriques`, the 1897
memoir that sets out the Italian school's theory of algebraic surfaces — and its catalog card shows
only Castelnuovo. Enriques is named in the meta row and absent from the strip.

`catalog-card-portraits` (archived 2026-09-14) excluded a second portrait deliberately, and gave the
reason: "splitting the strip into two half-height images would break the uniform 69px column for a
single card." That reason describes a **side-by-side** split, which would halve the column to two
34px slivers. It does not describe a **stacked** one, which leaves the 69px column exactly where it
is and divides it the other way. The exclusion was rejecting a shape that is not the only shape
available.

The meaning argument that moved the strip's link in `catalog-portrait-links-author` applies here
too, one level up. That change established that a face on this site means *that person*. A card
whose strip shows one of two authors makes the same class of claim the old `href` did: it presents
a single face for a work that two people wrote, and the reader has no way to see from the card that
the face is a first-of-two rather than the author.

Both portraits already exist. `corpus/authors/guido-castelnuovo/portrait-thumb.jpg` and
`corpus/authors/federigo-enriques/portrait-thumb.jpg` are committed, and `works.json` already
carries a `thumb_url` for each. Nothing has to be generated, fetched, or cleared.

## What Changes

- A catalog card for a work with **exactly two authors, both of whom have a portrait**, shows both
  portraits in the existing 69px box, divided by a straight diagonal cut. Every other card is
  untouched.
- The cut drops **8px across the strip's 69px width — 6.6°** — measured from its lowest point on the
  left to its highest on the right, crossing the box's vertical midpoint. The drop is specified in
  px, not in a percentage of the box: catalog cards run 108–219px tall, and a percentage cut would
  render at roughly 9° on a short card and 18° on a tall one, so the slant would visibly differ down
  the list.
- The two wedges are separated by a **2px seam** showing the box's own background, which is the
  card's `--border` token and therefore re-colours itself in dark mode.
- **Each wedge is its own link to its own author.** The upper-left wedge points at the first author,
  the lower-right at the second. `clip-path` clips pointer events as well as paint, so the hit
  regions follow the diagonal exactly; this was verified by probing with `elementFromPoint` rather
  than assumed.
- Both wedges stay hidden from assistive technology (`aria-hidden`, out of the tab order, empty
  `alt`), on the same rationale `catalog-portrait-links-author` established and for the same reason:
  **both** authors are already links in the card's meta row, so each wedge remains a redundant path
  to a destination that is already announced and already focusable. The spec's requirement that the
  portrait stay redundant with a visible link on the card continues to hold, now for two links
  instead of one.
- A work with three or more authors, or a two-author work where either author lacks a portrait,
  keeps today's behaviour exactly: the first author's portrait alone, or the monogram placeholder.
  Neither case exists in the corpus; the corpus maxes out at two authors and both have portraits.
  **Three or more authors is explicitly out of scope** — a 69px strip cannot carry three legible
  faces, and the question is better answered against a real work than invented now.
- No change to the card's height, its two layouts, the breakpoint between them, the monogram
  placeholder, the 69px column, or any single-author card. The portrait still must not contribute to
  the card's height.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `site-catalog`: the `Catalog card portraits` requirement currently states that "A multi-author work
  shows its first author's portrait only; the meta row already names every author." That sentence is
  replaced by the paired-portrait rule, its geometry, and its fallbacks. Two further paragraphs are
  amended rather than replaced: the portrait's destination, which becomes per-wedge for a paired
  card, and the crop invariant — "A face may lose its sides; it MUST NOT lose its crown or chin" —
  which needs an explicit carve-out, because a wedge is the first box on this surface that can be
  wider than the thumbnail and therefore crop it vertically.

## Impact

- `site/src/pages/index.astro` — the portrait branch grows a third case. Today it chooses between an
  `<a class="pbox">` and a `<div class="pbox mono">`; it gains a paired branch emitting two wedge
  anchors inside one box. The existing two cases are unchanged.
- `site/src/styles/global.css` — a new block for the paired box's wedges and their clip paths, added
  beside the shared `.pbox` rules. The existing `.pbox`, `.pbox img`, `.pbox.mono`, `.catalog .card
  .pbox` and the ≤500px media query are untouched, so every single-author card on the catalog and
  every card on `/authors/` renders byte-identically.
- `openspec/specs/site-catalog/spec.md` — three paragraphs of the `Catalog card portraits`
  requirement, plus a scenario. The main spec is current as of `dc047e9`, which folded both earlier
  portrait changes in, so this delta is written against shipped text with no ordering caveat.
- **No change** to `work.yaml`, `works.json`, `pipeline/build_site_data.py`,
  `pipeline/make_portrait_thumb.py`, `pipeline/validate.py`, CI, the copyright gate, or the
  committed image assets. Both thumbnails are already built, already hosted and already referenced
  by `/authors/`; the paired card serves the same two files the author index serves.
- Performance: one additional 3.5KB thumbnail request on the catalog, for one card, lazy-loaded.
  `clip-path` on a static polygon is composited and does not animate.
