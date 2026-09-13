## MODIFIED Requirements

### Requirement: Author pages

The site SHALL publish a page per author at `/authors/<slug>/` and an index at `/authors/` (linked
from the nav as "Authors"). Established by the `author-pages` change (archived 2026-07-24).

Authors are aggregated across works by a stable identity key: `wikidata_id` when present, otherwise
a slug of the name — so the same author across works merges into one page, while namesakes with
distinct QIDs stay separate (PLAN.md §9a). `pipeline/build_site_data.py` emits the aggregation into
`works.json` as a top-level `authors` list and attaches each author's `slug` to every author object
inside each work, so catalog cards and the work-page header link author names to their page.

Each author page shows the name, an optional one-line `bio` and optional public-domain `portrait`
(a small image we host ourselves, copied from `corpus/authors/<slug>/` into
`site/public/authors/<slug>/` at build time — like figure crops; only full scans are never
rehosted), and the birth/death years. The portrait links to its `source` URL (its Wikimedia Commons
file page) when clicked, and shows the optional `credit` artist attribution as a caption.
Public-domain status is *not* restated on the page — everything on the site has already passed the
gate, so it is a given. A MacTutor (St Andrews) biography link is shown when the author's `mactutor`
field is set (the only external link surfaced — `wikidata_id` is retained in the data for
aggregation and the CI death-date check, but is not shown to visitors), followed by the author's
works on the site (title → work page, year, venue, status badge), ordered by year. Only
public-domain works that pass the gate feed the aggregation, so no author page surfaces an
unpublished work.

The index lists every author alphabetically, each card carrying a portrait thumbnail, the name,
dates and work count, above a search box that filters the list client-side by name/bio as you type
(mirroring the catalog's search) with a live count and an empty-state message.

The thumbnail is a 69 × 86 image set flush to the card's left edge, clipped by the card's own
rounded corners. It MUST NOT contribute to the card's height: the image is absolutely positioned
inside a fixed-width box and sized with `object-fit: cover`, so a card's height is determined by its
text exactly as it was before the thumbnail existed. Cards measure the same height with portraits
as without at desktop widths. An author with no portrait renders a placeholder of the same
footprint carrying the initial of their last name, so the text column stays aligned down the list.
Because the author's name sits in the adjacent heading inside the same link, the thumbnail is
decorative — the image carries an empty `alt` and the placeholder is hidden from assistive
technology, rather than repeating the name. The index card shows no `credit` attribution; it links
through to the author page, which carries the attribution and the Commons `source` link. All
index-card styling is scoped to `.authorlist .card` so the `.card` class shared with the catalog,
journal and work-list pages is unaffected.

Thumbnails are served from a committed derivative rather than the full portrait, which is an order
of magnitude too heavy for a 69px box. `resolve_portrait()` locates it by convention as a sibling of
the portrait file — `portrait.jpg` → `portrait-thumb.jpg` — requiring no new `work.yaml` field (the
`portrait` block is duplicated across every work.yaml by the same author, so a declared key would
have to be kept in sync in N places). Both files are copied into `site/public/authors/<slug>/` and
the portrait record carries both `url` and `thumb_url`. When the derivative is absent, `thumb_url`
falls back to the full portrait's `url` and the build warns, naming the slug: the page stays correct
and merely heavier. `pipeline/validate.py` does not rule on thumbnails — the gate decides copyright,
and a missing cosmetic derivative is not a copyright question.

#### Scenario: Same author across works merges into one page

- **WHEN** the same author (same `wikidata_id`, else name slug) appears in multiple works
- **THEN** they are aggregated into one `/authors/<slug>/` page listing those works, while namesakes with distinct QIDs stay separate

#### Scenario: No author page surfaces an unpublished work

- **WHEN** an author has a work that fails the gate
- **THEN** that work does not appear on the author page

#### Scenario: Index cards show portraits without growing

- **WHEN** a reader loads `/authors/` at a desktop width
- **THEN** every card shows its author's portrait thumbnail at the card's left edge, and every card is the same height it was before thumbnails were added

#### Scenario: A portrait-less author keeps the column aligned

- **WHEN** an author has no `portrait` in their work records
- **THEN** their index card shows a monogram placeholder of the same footprint, hidden from assistive technology, so the text column stays aligned with every other card

#### Scenario: The index serves the derivative, not the full portrait

- **WHEN** `corpus/authors/<slug>/portrait-thumb.jpg` exists beside the portrait
- **THEN** the build copies both into the site, the author's portrait record carries `thumb_url` pointing at the derivative, and the index card requests that URL while the author page still requests the full `url`

#### Scenario: A missing derivative degrades rather than fails

- **WHEN** an author has a portrait but no `portrait-thumb.jpg` beside it
- **THEN** the build warns naming that slug, `thumb_url` falls back to the full portrait's `url`, and the index card renders correctly from the full image
