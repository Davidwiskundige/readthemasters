## Why

`catalog-card-portraits` (archived 2026-09-14) took one trade-off deliberately: portraits apply at
every viewport width, with no narrow-screen breakpoint, costing roughly a fifth more scrolling on a
phone. Its own Risks section said the breakpoint that would undo it "is a three-line addition if it
reads worse in practice than in the prototype."

It reads worse in practice, and for a reason the design predicted but under-measured. Because
`object-fit: cover` fills whatever height a card has, and phone cards run 219–428px against a 69px
strip, the portrait becomes a vertical sliver — **20–39% of the thumbnail's width** on a phone,
against 39–80% on a laptop. The first card on a 375px screen renders its portrait at 69 × 349.
Faces stop being faces.

The cause is that a phone gives the card ~335px and the portrait takes 83px of it off the *title*,
which is the one block that cannot absorb the loss: titles run to 138 characters and wrap to 5–7
lines. Measured across the 18 cards at 375px, the metadata block is the **largest** block on the
card (2176px of 5887px total) and the one that wraps happily, while the title pays for the portrait.

## What Changes

- Below a new breakpoint, the catalog card changes shape: the original title (and nothing else)
  spans the card's full width, and the portrait moves to the card's bottom-left, beside the English
  title and the metadata row taken together.
- The portrait stretches to the exact height of that text block, cropping horizontally about its
  centre — the same mechanism the wide layout uses, applied to a smaller box.
- Pairing the portrait with the English title *and* the metadata (rather than the metadata alone) is
  what makes the layout work: that block is always taller than the portrait is wide, so the portrait
  can never overhang the text beside it and can never be cropped top-to-bottom.
- The breakpoint is new and belongs to the card, not to the existing `max-width: 800px` sidebar
  breakpoint, which it must not reuse.
- No change above the breakpoint. The laptop and desktop catalog, `/authors/`, `/authors/<slug>/`,
  journal pages, the timeline and search are all untouched, as are `work.yaml`, `works.json`, the
  Python pipeline and CI.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `site-catalog`: the `Catalog card portraits` requirement currently describes one layout — a
  69px strip "flush to the card's left edge" filling the card's height. That becomes the wide-screen
  layout only, and the requirement gains the narrow-screen layout, the rule that the portrait is
  paired with the English title and metadata together, and the constraint that the breakpoint is the
  card's own rather than the sidebar's.

## Impact

- `site/src/pages/index.astro` — the card's inner markup gains a wrapper around the English title
  and metadata so the portrait has a single sibling to match; the portrait moves out of its current
  position as the card's first child.
- `site/src/styles/global.css` — a media query under `.catalog .card`. The shared `.pbox` block and
  every rule above the breakpoint stay as they are; no bare `.card` rule and nothing keyed on
  `.works` may change, for the reason recorded in the archived design's decision 6.
- No Python, no pipeline, no CI, no new assets, no new requests: the same `portrait-thumb.jpg` is
  already being served, and this only changes the box it is drawn into.
- Measured against production, the narrow layout is also **shorter** than what ships today —
  5885 → 5401px at 375px, 4900 → 4598px at 430px — so the archived change's accepted mobile cost is
  substantially repaid rather than merely mitigated.
