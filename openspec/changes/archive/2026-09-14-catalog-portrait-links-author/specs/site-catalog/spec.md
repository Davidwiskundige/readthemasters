## MODIFIED Requirements

### Requirement: Catalog card portraits

Each catalog card SHALL carry the portrait thumbnail of its work's first author — the same
committed derivative the author index uses, so the two surfaces read as one system. A face is
recognized faster than a name is read, and the catalog is where a reader scans for an author's
works. The card takes one of two layouts, chosen by a breakpoint that belongs to the card itself.

**Wide layout.** Above the breakpoint the portrait is a 69px-wide strip flush to the card's left
edge, clipped by the card's own rounded corners, spanning the card's full height.

The portrait MUST NOT contribute to the card's height at any card height. Catalog cards vary with
their content (108–219px against an 86px portrait box), so the image is absolutely positioned
inside a fixed-width box and sized with `object-fit: cover`: a card's height is determined by its
text exactly as it was before portraits existed, and the image fills whatever height it is given.
The visible slice of the thumbnail therefore narrows as a card grows taller; this is accepted, and
the derivative is centre-cropped on the face before it is scaled, so the face survives the tallest
card.

**Narrow layout.** Below the breakpoint the card restacks: the original title SHALL span the card's
full width, and the portrait SHALL sit at the card's bottom-left beside the English title and the
metadata row taken together as one block, filling that block's height exactly.

The portrait is paired with both lower blocks, never with the metadata alone. The metadata's own
height varies more than twice over (55–176px across viewports) and collapses to two lines on a
sparse record, which is shorter than a legible portrait is wide — so a portrait matched to it either
overhangs the text or is cropped top-to-bottom into a letterbox. The English title and metadata
together are always taller than the portrait is wide, which makes two properties hold at once: the
portrait is never taller than the text beside it, and its crop is always horizontal, never
vertical. A face may lose its sides; it MUST NOT lose its crown or chin. Where a work has no English
title, the portrait falls back to its natural height rather than shrinking below it.

The narrow layout is narrower *and* shorter than the wide layout applied to the same screen, so the
scrolling cost the wide layout imposes on a phone is repaid rather than merely mitigated.

**The breakpoint.** The two layouts SHALL be separated by a breakpoint chosen from the card's own
width, and it MUST be low enough that the invariant above still holds at it: as the card widens the
text block beside the portrait shrinks, and once that block falls below the portrait's natural
height the floor makes the portrait taller than its own text. The breakpoint is therefore set by
that limit, not by where the two layouts reach equal height — the height curves cross later, and
using that crossover would place the breakpoint inside the range where the invariant is already
broken. It MUST NOT reuse the breakpoint that collapses the filter sidebar: that answers a different
question, and well above the card breakpoint the narrow layout is measurably taller than the wide
one.

**The portrait's destination.** The portrait SHALL be wrapped in a link to the page of the author
whose face it shows — the card's first author, `/authors/<slug>/`. A portrait means the person in
it, and the rest of the site already honours that: `/authors/` pairs the same derivative with a name
that opens the author, `/authors/<slug>/` shows the portrait full size. The catalog MUST NOT be the
one surface where clicking a face opens a paper. This destination is deliberately *not* the card's
title's: widening the title's target by repeating it at the card's left edge is worth less than
matching what a reader already expects a portrait to do.

That link is hidden from assistive technology (`aria-hidden`, removed from the tab order) and the
image carries an empty `alt`: the first author's name is already a link to the same author page in
the card's own meta row, so the portrait remains a redundant path to a link already announced and
already focusable, and a second nameless stop would be noise. The portrait MUST stay redundant with
a visible link on the card — it is hidden from assistive technology only because nothing is lost by
hiding it.

Where a card has no first author to point at, the portrait box SHALL render as a plain element
rather than a link, never as a link with no destination or one aimed elsewhere.

A work whose first author has no portrait renders the same monogram placeholder the author
index uses, so the text column stays aligned down the list. A multi-author work shows its first
author's portrait only; the meta row already names every author. All of this holds in both layouts.

Catalog portrait styling SHALL be scoped to a class carried only by the catalog's own list. Neither
bare `.card` nor `.works` is such a scope: `/authors/<slug>/`'s work list uses both, and its works
are all by one author, so it keeps no portraits and no visual change. The catalog's list carries an
additional `catalog` class for this purpose, following the convention `.authorlist` and
`.journallist` already set.

#### Scenario: Catalog cards show portraits without growing

- **WHEN** a reader loads the catalog at a desktop width
- **THEN** every card shows its first author's portrait thumbnail at the card's left edge, and no card is taller than its text alone requires

#### Scenario: A tall card crops rather than reflows

- **WHEN** a work's title wraps enough to make its card considerably taller than the portrait's natural height
- **THEN** the portrait fills the card's full height, cropped horizontally about its centre, and the card's height is still set by its text

#### Scenario: A narrow screen gives the title the full width

- **WHEN** a reader loads the catalog below the card breakpoint
- **THEN** the original title spans the card's full width, and the portrait sits at the card's bottom-left beside the English title and metadata

#### Scenario: The portrait never overhangs the text beside it

- **WHEN** the catalog is rendered below the breakpoint, including on a work whose metadata is only two lines
- **THEN** the portrait's height equals the height of the English title and metadata beside it, and on no card is the portrait taller than that text

#### Scenario: A phone crop never cuts the top of the head

- **WHEN** a portrait is drawn in the narrow layout
- **THEN** its box is taller than it is wide, so the thumbnail is cropped horizontally about its centre and never letterboxed

#### Scenario: The narrow layout is not used on wide screens

- **WHEN** the viewport is above the card breakpoint
- **THEN** the wide layout is used, because at greater widths the narrow layout would both break the no-overhang invariant and produce a taller list

#### Scenario: The breakpoint sits below where the invariant fails

- **WHEN** the catalog is measured at the breakpoint itself
- **THEN** no card's portrait is taller than the text beside it, with margin to spare before the width at which the floor would start to overhang

#### Scenario: Clicking a face opens that person

- **WHEN** a visitor clicks the portrait on a catalog card, in either layout
- **THEN** the first author's page opens — the same destination as that author's name in the card's meta row, and not the work the title opens

#### Scenario: The portrait is a redundant target, not a second one

- **WHEN** a visitor reaches the card by keyboard or screen reader, in either layout
- **THEN** the portrait contributes no extra tab stop and no announcement, the card presenting its title and author links exactly as before, every destination the portrait offers still reachable through the meta row's author link

#### Scenario: A card with no author to point at renders no link

- **WHEN** a work has no first author
- **THEN** its portrait box renders as a plain element with the same footprint and no link, rather than a link with an empty or mis-aimed destination

#### Scenario: A work whose author has no portrait keeps the column aligned

- **WHEN** a work's first author has no `portrait` in their records
- **THEN** its card shows a monogram placeholder of the same footprint, hidden from assistive technology, so the text column stays aligned with every other card

#### Scenario: A multi-author work shows one portrait

- **WHEN** a work has more than one author
- **THEN** its card shows the first author's portrait only, and the meta row still links every author

#### Scenario: The author page's work list keeps no portraits

- **WHEN** a reader opens `/authors/<slug>/`, whose work list shares both the `card` class and the `works` list class with the catalog
- **THEN** its cards render exactly as before — no portrait, no flex layout, their padding intact — at every viewport width

#### Scenario: Portraits survive filtering and sorting

- **WHEN** a visitor filters by facet or changes the sort order
- **THEN** the surviving cards keep their portraits, including after cards are reordered in the DOM

#### Scenario: The catalog reuses the author index's derivative

- **WHEN** the catalog is built
- **THEN** it reads `thumb_url` from the `authors` array of the existing `works.json`, joined to each work by author slug at build time, adding no field to `work.yaml`, no key to the works records, and no step to the Python pipeline
