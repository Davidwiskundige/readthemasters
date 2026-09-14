## Why

`/authors/` gives every author a portrait at the card's left edge, and the page became markedly
easier to scan: a face is recognized faster than a name is read. The catalog — the site's front
door — still identifies authors by name only, so finding "the Abel papers" or "the Bernoulli ones"
means reading fourteen names instead of seeing three faces.

This reopens a decision. `author-index-portraits` (archived 2026-09-13) listed "portraits on
catalog cards" under **Non-Goals**, on the reasonable assumption that a card holding two titles and
a meta row could not afford the width. Measurement against production says the cost is much smaller
than that assumption: catalog cards are already 108–219px tall, so a 69 × 86 portrait adds **no**
height of its own, and the whole list grows 4.3% from titles wrapping. That is what changed.

## What Changes

- Catalog cards (`/`) carry the author's portrait thumbnail as a full-bleed 69px strip at the
  card's left edge, clipped by the card's rounded corners — the same treatment `/authors/` uses,
  reusing the same committed `portrait-thumb.jpg` derivatives and the same `thumb_url` field.
- The strip is a link to the work, matching the card's title link rather than competing with it,
  and hidden from assistive technology so the card announces one target, not two.
- A work whose first author has no portrait gets the monogram placeholder already defined for
  `/authors/`, so the text column stays aligned down the list.
- A multi-author work shows its first author's portrait only.
- The portrait is applied at every viewport width, with no narrow-screen breakpoint. On a phone
  this costs roughly 22% more scroll; that trade is taken deliberately and recorded in design.md.
- No change to `/authors/`, `/authors/<slug>/`, journal pages, the timeline, search results, or the
  work page. No change to `work.yaml`, `works.json`'s shape, the pipeline, or CI.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `site-catalog`: the requirement describing catalog cards gains the portrait strip — its
  footprint, its inability to affect card height, its link and accessibility behaviour, the
  monogram fallback, and the multi-author rule. The author-index portrait requirements are
  unchanged; this adds a second consumer of the same derivative.

## Impact

- `site/src/pages/index.astro` — a build-time `slug → thumb_url` map over the `authors` array
  already present in the imported `works.json`, and the portrait box in the card markup.
- `site/src/styles/global.css` — new rules scoped to `.works .card`, alongside the existing
  `.authorlist .card` block. `.card` is shared with `/authors/<slug>/`'s work list, which must not
  shift, so no bare `.card` rule may change.
- No Python, no pipeline, no `work.yaml`, no CI, no new dependency, and no new bytes: the
  thumbnails are already generated, already committed, already copied into the site by
  `resolve_portrait()`, and already carried in `works.json` as `authors[].portrait.thumb_url`.
- Page weight: zero additional requests for a visitor who has seen `/authors/`; at most the same
  66 KB set otherwise, lazy-loaded.
