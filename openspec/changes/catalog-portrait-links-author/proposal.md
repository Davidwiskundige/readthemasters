## Why

On the catalog, each card's portrait strip currently links to the **work** — the same destination as
the card's title. `catalog-card-portraits` (archived 2026-09-14) chose that deliberately: a second
destination at the card's left edge would compete with the card's main target, so the strip was made
a redundant, wider path to the title.

That argument is about targets; it is not about meaning. A portrait of a person means *that person*,
and every other surface on the site honours that: `/authors/` puts the same 69px derivative beside a
name that links to the author, and `/authors/<slug>/` shows the full portrait. The catalog is the
one place where clicking a face opens a paper. The convention a reader arrives with — an avatar goes
to whose avatar it is — points at the author page, and following it is worth more than the extra few
square centimetres of title target.

The accessibility argument that justified hiding the strip survives the move intact, because the
first author's name is *already* a link to `/authors/<slug>/` in the same card's meta row. The strip
stops being a redundant path to the title and becomes a redundant path to the author link — still
redundant, still correctly hidden, still no new tab stop.

## What Changes

- The catalog card's portrait strip links to the **first author's page** (`/authors/<slug>/`)
  instead of to the work. This is the card's first author — the one whose face is shown — matching
  the first name in the meta row.
- The strip stays hidden from assistive technology (`aria-hidden`, out of the tab order) with an
  empty `alt`, on the re-pointed rationale above: it now duplicates the meta row's author link
  rather than the title link, and both are already announced and focusable.
- A card with no first author to link to renders the portrait box as a plain element rather than a
  dead or mis-aimed link. Every work in the corpus has an author today, so this is a guard, not a
  visible case.
- No change to layout, geometry, breakpoints, the monogram placeholder, or which portrait a card
  shows. Both card layouts (wide strip and the narrow restack) are untouched; only the `href` and
  the element type in the no-author case differ.
- No change to `/authors/`, `/authors/<slug>/`, journal pages, the timeline, search, `work.yaml`,
  `works.json`, the Python pipeline or CI.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `site-catalog`: the `Catalog card portraits` requirement currently states that the portrait "is
  wrapped in a link to the work — the same destination as the card's title." That paragraph is
  replaced: the destination becomes the first author's page, the redundancy that justifies hiding
  the link from assistive technology is restated against the meta row's author link, and the
  no-author case is specified.

## Impact

- `site/src/pages/index.astro` — the portrait element's `href`, its explanatory comment, and a
  branch for the no-author case. Nothing else in the card changes.
- `site/src/styles/global.css` — **no change**. Every portrait rule is keyed on `.pbox` / `.catalog
  .card .pbox`, never on the element being an anchor, so the box renders identically whether it is
  an `<a>` or a `<div>` (which is what `/authors/` already uses).
- `openspec/specs/site-catalog/spec.md` — one paragraph of the `Catalog card portraits` requirement.
  Note that this requirement's authoritative text currently lives in the *unarchived*
  `catalog-card-portraits-phone` change: that change shipped (PR #62, merged) but its delta has not
  been folded into the main spec, which still describes the pre-phone single layout. The delta here
  is written against the shipped text, and folding the phone change first keeps the two consistent.
- No Python, no pipeline, no CI, no new assets, no new requests, no measurable performance
  difference: the same `portrait-thumb.jpg` is served into the same box; only where it points
  changes.
