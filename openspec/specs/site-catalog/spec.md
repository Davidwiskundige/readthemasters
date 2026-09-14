# site-catalog

## Purpose

Current source of truth for the public static site. Astro site under `site/`, fed by
`pipeline/build_site_data.py` (emits `site/src/data/works.json`). Established by the `site-catalog`
change (archived 2026-07-18).

## Requirements

### Requirement: Only public-domain works are published

The site build SHALL include a work only if it passes the copyright gate and meets the minimum
status. Non-public-domain works never appear in the catalog or as pages.

#### Scenario: Failing work never appears

- **WHEN** a work fails the copyright gate or falls below the minimum status
- **THEN** it appears neither in the catalog nor as a page

### Requirement: Catalog with browse & filter

The catalog SHALL list works and filter them client-side over the build-time JSON index (no server).
Facets: discipline, topic (tags), language, available translations, type, quality status, and a
year range, plus free-text search over title/author. Filter state is reflected in the URL query
string so a filtered view is shareable.

#### Scenario: Filtered view is shareable

- **WHEN** a visitor applies facets and a text query
- **THEN** the filter state is encoded in the URL query string and reopening it restores the same view

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

### Requirement: Work page

Each work SHALL have a page showing metadata, the source scan link + citation, a status badge, and
the transcription and each translation in tabs. Text is rendered from LaTeX to HTML by a lightweight
transform (`site/src/lib/tex.js`: headings, `\origpage` page markers, emphasis, em-dashes); inline
math is rendered by KaTeX. Every page carries a prefilled "report an error" link below the text.

A work's review level is carried by its status badge alone, which reveals what that level means
(see "Status badge explains its review level"). No status SHALL get a separate banner above the
text: `ai-draft` is 14 of 18 works, so its banner was near-permanent furniture repeating what the
badge beside the title already said, and it pushed the text further down on exactly the works a
reader is most likely to want to check against the scan.

Each text panel carries a heading with the id that tabs and search results link to (`#original`,
`#en`); the heading is visually hidden because the visible label is the tab itself. The tabs read
and write `location.hash`, so `/works/<id>/#en` opens the English translation directly and a link
into a panel survives being shared. Anchors inside a panel are unique to it: section headings are
`sec-<n>` / `<lang>-sec-<n>` and page markers `p-<n>` / `<lang>-p-<n>`.

Math SHALL be typeset as the reader reaches it, never for a whole panel at once. On load the page
typesets only the always-visible regions — the heading and the significance note — and thereafter
each formula is typeset as it approaches the viewport, so the work done at load is proportional to a
screenful rather than to the length of the text. A hidden panel is then simply a region none of whose
formulas is ever near the viewport: it costs nothing until its tab is opened, and opening it typesets
that panel's visible screenful rather than all of it. Each formula is typeset at most once, so
scrolling back over text, or leaving a panel and returning to it, costs nothing.

This is what makes a long work usable. On the corpus's longest work only **13 of a panel's 1,581
formulas** lie within three viewports of the top; typesetting the panel eagerly is ~734 ms of blocked
main thread at load on a desktop and several times that on a mid-range phone — long enough for the
browser to offer to stop the page — while typesetting what the reader can see is ~39 ms, matching a
short paper. Cost SHALL NOT scale with the length of the work.

Because typesetting a formula changes the height of the text around it, a deep link into a region
typeset this way SHALL be scrolled to its anchor again once the formulas around that anchor have been
typeset, so the reader still lands on the linked page marker.

Deferring on visibility has one case it cannot decide for itself: math inside a region that is
hidden until the reader asks for it, such as an editorial note's popover card. Such a card is
`display: none`, so its formulas have no box, never approach the viewport, and would never be
typeset at all — the reader would open the note and be shown raw LaTeX. Math in a hidden card SHALL
therefore be typeset with the marker that opens it, which is itself laid out in the text. This is
not an exception to deferral but the same rule applied to the element that is actually visible; the
cards are a handful per work and cost nothing beside a panel's formulas.

Two consequences are accepted rather than fixed, and are recorded so they are not re-derived. Jumping
directly to a distant part of a long work settles briefly as the formulas there typeset and grow,
because there is no runway in which to typeset ahead; reserving space for display equations does not
solve it, since most of a panel's formulas are inline and each gains a little height as it renders.
And the browser's find-in-page matches raw LaTeX in regions not yet typeset.

The reader regions are marked `data-pagefind-body` for the search index — see the `search`
capability for what that covers and what it excludes. Indexing is unaffected by when math is
typeset or measured: both the text and formula indexes are built from the HTML at build time.

Display math never collides with its equation number. Each display equation is its own horizontal
scroll area, a formula wider than the text column is left-aligned so scrolling starts at the
beginning of the formula, and a `\tag{n}` that cannot fit beside its formula moves to a line of
its own, right-aligned beneath it. Which layout applies is decided by measuring the rendered
formula, not by a viewport breakpoint, so a long formula stacks its number at any screen width.

That measuring pass MUST batch its DOM reads and writes into whole-collection phases — sample every
equation's available width, then clear the layout classes, then measure every formula and tag, then
apply the resulting classes — so that the number of forced synchronous layouts it triggers is a
small constant rather than growing with the number of equations. Reading layout immediately after
writing to it forces the browser to recompute the whole document's layout, so a per-equation
read/write interleave costs two full reflows per equation; on the corpus's longest works that is
thousands of reflows and seconds of blocked main thread. The decision arithmetic — which widths
imply which classes — SHALL live in a pure function that is unit-tested independently of the DOM.

Measuring SHALL be driven by proximity to the viewport rather than performed for every equation up
front. A panel shown for the first time has never been laid out, so measuring all of its equations
at once forces that whole first layout synchronously — seconds of blocked main thread on the
corpus's longest works, independent of typesetting, which is why fitting the panel eagerly is not
acceptable however cheap each individual measurement is. An equation whose width cannot yet be read
SHALL be treated as pending and measured once it can be, never silently left unfitted: dropping it
is indistinguishable in code from the hidden-panel case and loses the equation. Every equation that
the reader reaches SHALL end up with the same classes an eager pass would have given it, including
equations typeset late, which SHALL be fitted once they exist.

Skipping off-screen layout with `content-visibility` is **not** part of this: measured on the
corpus's longest work it made the first reveal *slower* (4,042 ms with it, 2,919 ms without), while
leaving the cost of switching between already-laid-out panels unchanged. It also required detecting
a second, easily-confused "not measurable yet" state, since a layout-skipped element reports a sane
box width while its children measure zero.

Neither the typesetting nor the measuring of a revealed panel may depend on the order in which the
page's scripts are registered: both are bundled into one file and the bundler may emit them in
either order, so both SHALL be driven by the panel's observed change in visibility.

#### Scenario: Deep link opens the right panel

- **WHEN** a visitor opens `/works/<id>/#en`
- **THEN** the English translation panel is shown directly, its hash preserved for sharing

#### Scenario: Only what the reader can see is typeset at load

- **WHEN** a work with many hundreds of formulas finishes loading
- **THEN** only the always-visible regions and the formulas near the viewport are typeset, and the rest of the page still holds its raw LaTeX

#### Scenario: Scrolling typesets formulas as they arrive

- **WHEN** the reader scrolls into a part of the text whose formulas have not been typeset
- **THEN** those formulas are typeset as they approach the viewport, and are then fitted like any other equation

#### Scenario: An editorial note's formulas are ready before it is opened

- **WHEN** the reader opens an editorial note whose text contains formulas
- **THEN** those formulas are already typeset rather than shown as raw LaTeX, having been typeset with the marker that opens the note

#### Scenario: A hidden panel costs nothing until opened

- **WHEN** a bilingual work's page finishes loading with only the original panel showing
- **THEN** none of the translation panel's math is typeset, and opening its tab typesets that panel's visible screenful rather than the whole panel

#### Scenario: Returning to text already read does not typeset it again

- **WHEN** the reader scrolls back over text, or leaves a panel and returns to it
- **THEN** no formula is typeset a second time

#### Scenario: Deep link into a not-yet-typeset region lands on its anchor

- **WHEN** a search result opens `/works/<id>/#en-p-236`, pointing into a region whose math has not been typeset yet
- **THEN** the formulas around that anchor are typeset and the page is scrolled to `en-p-236` afterwards, so the marker is in view rather than displaced by the formulas that grew around it

#### Scenario: Jumping to a distant part settles rather than blocking

- **WHEN** the reader jumps straight to the end of a long work, where nothing could be typeset ahead
- **THEN** the formulas there typeset and the page settles briefly, rather than blocking the browser

#### Scenario: Revealing a panel does not block on its whole length

- **WHEN** a reader opens the translation tab of a work with many hundreds of display equations
- **THEN** the equations on screen are fitted without the page first laying out and measuring every equation in the panel

#### Scenario: Scrolling fits equations as they arrive

- **WHEN** the reader scrolls to a part of a panel whose equations have not been measured yet, whether they were typeset just now or earlier and left unfitted by a resize
- **THEN** those equations are fitted as they approach the viewport, receiving the same classes an eager pass would have given them

#### Scenario: An equation that cannot yet be measured is not lost

- **WHEN** an equation's available width cannot be read, because it sits in a panel that is not showing or is otherwise not laid out
- **THEN** it is left pending and fitted once it is laid out, rather than treated as already handled

#### Scenario: Wide equation keeps its number legible

- **WHEN** a display equation is wider than the text column and its `\tag{n}` cannot fit beside it
- **THEN** the equation scrolls in its own area and the tag moves to its own right-aligned line beneath, decided by measuring the rendered formula

#### Scenario: Fitting cost does not scale with equation count

- **WHEN** the fitting pass runs over a work with many hundreds of display equations
- **THEN** it triggers a constant number of forced layout recalculations for the whole pass rather than one or more per equation, and assigns every equation the same classes an unbatched pass would

#### Scenario: ai-draft work is marked by its badge, not a banner

- **WHEN** a work's status is `ai-draft`
- **THEN** the page marks it with the status badge, whose popover says the text is machine output
  not yet human-checked, and shows no separate notice above the text

#### Scenario: Every work offers a way to report an error

- **WHEN** any work page renders, whatever its status
- **THEN** it carries a prefilled "report an error" link below the text

### Requirement: Work page source line

The work page's source line SHALL be a single line: the scan link, and the original work's BibTeX
Copy button. It SHALL NOT render `source.scan_id`, which is an internal provenance identifier whose
free-text form ranges from a bare key to several sentences, nor `publication_full`, which on 15 of
18 works restates the heading block's author, year, venue, volume and pages.

Where the transcribed edition is not the original printing — `edition.year` differing from the
work's `year` — the line SHALL say so in a short parenthetical after the scan link, since the
heading block cannot carry it. Where the two years agree the parenthetical is omitted. The
parenthetical names the edition by its year alone (`from the 1858 edition`): `edition` carries no
short title, and its `rights_note` is free prose of no guaranteed shape, so nothing else is
derivable without new corpus data.

`scan_id`, `publication_full` and `edition` remain in the corpus YAML for validation and audit; this
requirement governs display only.

#### Scenario: Source line shows the link and citation only

- **WHEN** a work page renders whose `edition.year` equals its `year`
- **THEN** the source line shows the scan link and the original's BibTeX Copy button, and shows
  neither `scan_id` nor `publication_full`

#### Scenario: A later edition is flagged after the scan link

- **WHEN** a work's `edition.year` differs from its `year` (e.g. `leibniz-1689-isochrona`, printed
  1689 and transcribed from Gerhardt's c.1858 reprint)
- **THEN** the source line carries a short parenthetical giving that edition's year — `from the 1858
  edition` — after the scan link

### Requirement: Status badge explains its review level

The work page's status badge SHALL reveal what its review level means, using the shared `.pop`
popover behavior rather than a `title` tooltip. A `title` attribute is not sufficient: it is
unreachable on touch devices, is not keyboard-focusable, and its screen-reader support is
inconsistent.

#### Scenario: Review level is revealed on hover, focus, and tap

- **WHEN** a visitor hovers, focuses, or taps the status badge on a work page
- **THEN** a popover explains that review level, pinned open on tap and closed on Escape or outside
  click, matching the behavior of every other `.pop` element on the site

### Requirement: LaTeX titles rendered as math

When a work's `work.yaml` carries an optional `title_tex` (and/or `title_en_tex`), the site SHALL
display that LaTeX rendering — with inline `$…$` math set by KaTeX — wherever the title is shown to a
reader: the work-page `<h1>` and English subtitle, the catalog cards, and the author-page work
lists. Established by `math-titles` (archived 2026-07-25).

The plain `title` / `title_en` remain canonical for everything that cannot show math: the browser
`<title>`, OpenGraph/Twitter tags, JSON-LD, the Pagefind result-card `title` metadata, and the
catalog's free-text filter/sort (which run off the plain `data-title` attributes). A work without
`title_tex` is unaffected — its plain title is shown as before.

`pipeline/build_site_data.py` passes `title_tex` / `title_en_tex` through to `works.json` (including
the per-author work lists). Rendering is client-side, consistent with the rest of the site's math
(build-time pre-rendering remains PLAN.md §9 backlog #18); each title page/list runs KaTeX
auto-render over the `$…$` delimiter. Titles use `\frac`/`\dfrac` as the author chooses; the
work-page `<h1>` scales its math down with CSS so a display fraction does not overwhelm the heading.

#### Scenario: Math title rendered where shown to readers

- **WHEN** a work has `title_tex`
- **THEN** the KaTeX rendering is shown in the work-page `<h1>`, catalog cards, and author-page lists, while the plain `title` remains canonical for the browser tab, metadata, and search

### Requirement: Significance note

When a work's `work.yaml` carries an optional `significance` field, the work page SHALL show it as a
clearly-labelled "Significance" callout, visually distinct from the transcription so it reads as
editorial context (ours), not the author's text. Math in the note is rendered by KaTeX, as in the
transcription.

The note's prose carries two positional markers (corpus-format), each rendered with the shared
`.pop` apparatus so the apparatus stays out of the reader's way until asked for:

- `[n]` renders as a small superscript number revealing its `significance_sources` citation,
  linked when the source carries a url.
- `[note n]` renders as a labelled inline chip — the `significance_notes` entry's own `label`,
  set on the baseline at reading size rather than as a superscript — revealing that entry's `text`.
  The card is wider than a citation card and scrolls when it must, because an aside is a paragraph.

A marker addressing an entry that does not exist renders as the literal text the author wrote, never
as an empty popover; the gate rejects that case before it ships. Math inside either popover is
typeset by the same KaTeX pass that covers the rest of the note, and both are excluded from the
search index like every other `.pop` apparatus. The renderer is `site/src/lib/significance.js`,
unit-tested by `site/src/lib/significance.test.mjs` (`npm test`, run in CI).

#### Scenario: Significance shown as editorial callout

- **WHEN** a work has a `significance` field
- **THEN** the work page shows it as a distinct "Significance" callout with KaTeX-rendered math

#### Scenario: An aside marker renders as a labelled popover

- **WHEN** a work's `significance` carries a `[note n]` marker and a matching `significance_notes` entry
- **THEN** the work page shows the entry's label as an inline chip in the running prose, revealing the note — with its math typeset — on hover, focus, or tap

### Requirement: Related reading (dependency graph)

From each work's `relations` (corpus-format), `build_site_data.py` SHALL emit per work:
`relations_out` (its authored backward edges, each enriched with the target's `{id, title,
title_tex, by, year, url}` — `by` is the first author's surname — plus `kind`, `recommended`, `note`,
`sources`), `relations_in` (the computed inverse), `recommended_prev` (the single flagged edge or
null), and `recommended_next` (works that flagged this one, ordered `primary` first then by year).
Edges to a work not in the published set are dropped. The top-level JSON also gains a compact
`graph` — `nodes` (`{id, title, title_tex, by, year, discipline, url}`) and `edges` (`{from, to,
kind, recommended}`).

The work page SHALL show a single-line **"Related reading"** nav in **two places** — near
Significance and directly after the text panels — each with three slots:

- **Left**: the recommended previous read, labelled `Read first:` (surname + first few words of the
  title, linking to that work). Rendered in the top nav only. It is intentionally omitted from the
  bottom nav: a reader who has reached the bottom has already read the current text, so telling them
  what to read *before* it is no longer actionable.
- **Middle**: the word `timeline`, linking to `/timeline/?focus=<id>` and opening the graph
  pre-focused on that work. Present in both navs.
- **Right**: the recommended next read, labelled `Next:`. Present in both navs.

Because the middle slot always has content, both navs SHALL render on every work page, including a
work with neither a recommended previous nor a recommended next. A slot with nothing to show renders
empty rather than suppressing the nav. This is what keeps every work reachable from the graph, and
it balances the row on works whose left slot is empty.

Both placements render from the same `recommended_prev`/`recommended_next` data through one shared
render path, so they cannot drift apart, and share the same terse style — the full graph (cites,
built-on-by, …) is explored on the timeline. The work page carries no separate standalone link to
the timeline; the middle slot is the only one.

#### Scenario: Edges to unpublished works are dropped

- **WHEN** a `relations` edge points to a work not in the published set
- **THEN** the emitted `relations_out`/`graph` omits that edge

#### Scenario: Both navs render on every work page

- **WHEN** any work page renders, including one with neither a recommended previous nor a
  recommended next read
- **THEN** both the top and the bottom "Related reading" nav render, each carrying at least the
  centred `timeline` link to `/timeline/?focus=<id>`

#### Scenario: Top nav carries Read first, timeline, and Next

- **WHEN** a work has both a recommended previous and a recommended next read
- **THEN** the top nav shows the `Read first:` link on the left, `timeline` in the middle, and the
  `Next:` link on the right

#### Scenario: Bottom nav omits Read first

- **WHEN** a work with a recommended previous read renders its bottom nav
- **THEN** that nav shows `timeline` and, when one exists, the `Next:` link — and never the
  `Read first:` link

### Requirement: Timeline page

A page at `/timeline/` (linked from the nav) SHALL visualise the whole-corpus `graph` as a
reading-order dependency map. Layout is computed at build time. **x** = one column per work in
**reading order** — a topological sort of the dependency graph (Kahn's algorithm, earliest year
then id to break ties), so same-year works split into their true order (June before September,
sketch I before II) and a pure lineage becomes a straight line. **y** = a lane from the **Sugiyama
barycenter-median** step (each node relaxes to the median of its neighbours' lanes, so a work
depending on two others settles between them; a chain stays on one lane). The **axis** is a thin
dashed rule at each century boundary — placed in the gap before that century's first work and
labelled with the century (e.g. `1600`); the exact year is read off each node's tag (century +
tag = year). Each node is a compact citation tag — first two letters of the surname + last two
digits of the year (e.g. `Eu61`, disambiguated `a`/`b`/… in reading order on collision); hover or
click it for a `.pop` popover with the full work — a linked title (to the work page) and linked
author(s) (to the author pages), plus year and venue, mirroring the catalog card's click targets —
reusing the shared popover apparatus. Edges are plain SVG lines (no arrowheads — order is clear
left → right), `builds-on` solid and `cites` dashed; an edge that skips a column curves to clear the
node between. A work selector plus "steps back / forward" controls **fade** the rest in equal steps
scaled to the chosen depth — a node `d` hops away on a side with `N` steps sits `d/N` of the way to
faint, and anything outside the range fades away; only the tag fades (the popover stays fully
legible), and "All" shows the whole corpus at full strength. Clicking a node focuses that work (as
well as opening its popover), and the page accepts a `?focus=<id>` deep link — arriving focused on
that work and scrolled to it — which each work page uses to link into the graph. The page works
without JavaScript: each node is a focus/hover-revealed popover (CSS `:focus-within`/`:hover`)
carrying the work's linked title and author(s), so every work (and its author) is reachable by
keyboard and screen reader; focus-dimming is a JS enhancement only. The diagram scrolls within its
own horizontal-scroll container. Zero runtime dependencies (SVG + a small inline script).

The hand-rolled barycenter layout is deliberate at the current corpus size. **Future option:** if
the graph ever grows tangled, a dedicated layered-layout engine — `dagre` (as used by mermaid) or
`elkjs` — could replace the build-time layout step; it would add a dependency, so it is worth doing
only when hand-rolling stops being enough.

#### Scenario: Works laid out in reading order with a focus deep link

- **WHEN** a visitor opens `/timeline/?focus=<id>`
- **THEN** the graph is laid out left-to-right in topological reading order, pre-focused on and scrolled to that work

#### Scenario: Timeline works without JavaScript

- **WHEN** JavaScript is disabled
- **THEN** each node's popover is still reachable by focus/hover and every work and author is reachable by keyboard and screen reader; only focus-dimming is lost

### Requirement: Downloads

Each work page SHALL offer the source `.tex` (always) and the compiled PDF (when built) for each
text, placed inside that text's own tab panel rather than in a consolidated list above the text.
Inside a panel the tab already names the text, so the download row SHALL NOT repeat that label; it
shares one row with the panel's transcription/translation provenance line.

The served `.tex` SHALL be self-contained: when emitting to `site/public/tex/`, the build
substitutes the body of the shared `readmasters.sty` for the `\usepackage{readmasters}` line, so a
downloaded `.tex` compiles without a second file. The preamble is therefore no longer offered as a
separate download. The corpus `.tex` is unchanged and still uses `corpus/preamble/readmasters.sty`;
`readmasters.sty` is still emitted and served at `/tex/readmasters.sty`.

#### Scenario: Downloads sit in the panel of the text they belong to

- **WHEN** a work page renders
- **THEN** each tab panel offers that text's `.tex` (always) and its PDF (when built) in one row
  with that panel's provenance line, and no consolidated downloads list appears above the text

#### Scenario: A downloaded .tex compiles on its own

- **WHEN** the build emits a work's `.tex` to `site/public/tex/<id>/<name>.tex`
- **THEN** that file carries the preamble's macro definitions inline in place of
  `\usepackage{readmasters}`, and no separate preamble download is offered on the page

### Requirement: PDF compilation (deploy-time)

`pipeline/build_pdfs.py` SHALL compile each public-domain work's `.tex` to PDF with Tectonic during
the CI deploy, into `site/public/pdf/<id>/<name>.pdf` (served at `/pdf/<id>/…`). PDFs are never
committed and are regenerated per deploy. A work may ship a pre-made PDF override
(`corpus/<id>/pdf/<name>.pdf`), which is copied instead of compiled. When no PDF exists, the page
SHALL render nothing in its place — neither a dead link nor a placeholder label. Build state is not
reader-facing, and `original_pdf` is null for every work outside a deploy, so a placeholder would be
permanently visible in development and would reach readers unchanged if a deploy build failed.

`\rmfigure` paths are written relative to the work root for both `original.tex` and
`translations/<lang>.tex`, so the work directory itself is on Tectonic's search path alongside the
`.tex` file's own directory and `corpus/preamble`.

#### Scenario: PDF override is copied, not recompiled

- **WHEN** a work ships `corpus/<id>/pdf/<name>.pdf`
- **THEN** that file is copied to the served path instead of being compiled

#### Scenario: Absent PDF renders nothing

- **WHEN** no PDF exists for an artifact
- **THEN** the page renders neither a PDF link nor any placeholder text in its place

### Requirement: Citations (BibTeX)

Each work page SHALL provide ready-made BibTeX (`site/src/lib/bibtex.js`) for the original work, our
transcription, each of our translations, and any referenced external translations — each with a Copy
button. Citekeys are ASCII (diacritics transliterated). Each entry sits next to the artifact it
cites: the original's beside the source line, each text's beside that text's downloads in its own
tab panel, and an external translation's beside its entry. A whole-file "Download all as `.bib`" is
not offered — per-artifact Copy buttons already cover citation, and a third citation affordance on
one page is redundant.

#### Scenario: BibTeX offered for every citable artifact

- **WHEN** a work page renders
- **THEN** it provides ASCII-citekey BibTeX for the original, transcription, each translation, and
  referenced external translations, each copyable beside the artifact it cites, and offers no
  whole-file `.bib` download

### Requirement: Existing translations elsewhere

Referenced `external_translations` SHALL be shown as an "Existing translations elsewhere" section
linking out (translator, year, venue, license) — never hosted.

#### Scenario: External translations are linked, not hosted

- **WHEN** a work has `external_translations`
- **THEN** they appear as an "Existing translations elsewhere" section linking out, and are never hosted on the site

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
through to the author page, which carries the attribution and the Commons `source` link. Index-card
layout is scoped to `.authorlist .card`; the portrait box itself — the absolutely positioned
`object-fit: cover` image and the monogram placeholder — is a shared `.pbox` block the catalog's
card portraits use too. No bare `.card` rule is changed, so the class shared with the work-list
pages is unaffected.

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

### Requirement: Revision history

Each work page SHALL show a revision history of the work, sourced from the optional `changelog`
block in the work's `provenance.yaml` — a curated, human-authored list, not anything derived from
git. Established by `revision-history` (archived 2026-07-25), then re-sourced from the changelog by
`provenance-changelog` (archived 2026-07-25, PLAN.md §9 #4); the earlier git-derived approach
(`revision-history` / `revision-history-filter`) is superseded.

`pipeline/build_site_data.py` emits each work's `changelog` into `works.json` as a list of
`{date, summary}` entries ordered newest first. The work page renders it as a single collapsed
`<details>` "Revision history" section near the "Report an error" link, whole-work in scope, one row
per entry (date + summary). A work with no `changelog` shows no revision-history section, and the
build never fails for its absence.

#### Scenario: Changelog renders newest-first, absence is fine

- **WHEN** a work has a `changelog`
- **THEN** the page renders a collapsed "Revision history" of its entries newest first; a work with no changelog shows no section and the build does not fail

### Requirement: SEO & structured metadata

Every page SHALL advertise a canonical URL, social-preview metadata, and machine-readable structured
data, all derived at build time from data already in `works.json` — no new corpus field. Established
by `seo-metadata` (archived 2026-07-25, PLAN.md §9 #5). Screen-reader MathML (KaTeX's default
`htmlAndMathml` output) and the sitemap (`@astrojs/sitemap` + `robots.txt`) were already in place, so
this requirement covers only the page-metadata layer.

The shared layout (`site/src/layouts/Base.astro`) emits, for every page: a `<link rel="canonical">`
built from the configured `site` + the page path; OpenGraph tags (`og:site_name`, `og:type`,
`og:title`, `og:description`, `og:url`) with `og:type` defaulting to `website` and overridable per
page (`article` for a work, `profile` for an author); and a Twitter `summary` card. When a page
supplies JSON-LD, the layout renders it in one `<script type="application/ld+json">`.

`site/src/lib/jsonld.js` builds the structured data: a work page emits a `CreativeWork` subtype from
its `type` (`paper` → `ScholarlyArticle`, `book` → `Book`, else `CreativeWork`) with title (English
title as `alternativeName`), each author as a `Person` with `sameAs` (Wikidata + MacTutor),
`datePublished`, `inLanguage`, `url`, `isBasedOn` (source scan when present), and a CC0 `license`; an
author page emits a `Person` with `sameAs` and birth/death years; the home emits a `WebSite`. Fields
whose source data is absent are omitted rather than emitted empty. This is metadata only — no
reader-facing change.

#### Scenario: Every page carries canonical, social, and structured metadata

- **WHEN** any page is built
- **THEN** it emits a canonical link, OpenGraph/Twitter tags, and (where applicable) JSON-LD, with absent fields omitted rather than emitted empty

### Requirement: Source popovers (shared apparatus)

The site SHALL provide a single popover behavior, shared across all pages, for revealing editorial
source material without cluttering the running text. Any element marked `.pop` containing a
`.pop-content` child reveals that content on pointer hover, on keyboard focus, and on a click/tap
that pins it open (so it is usable on touch); pressing Escape or clicking outside closes it, and
JavaScript keeps the revealed card within the viewport. The trigger is the whole `.pop` wrapper, and
a click that lands inside an open `.pop-content` (e.g. a citation link) acts normally rather than
toggling the card shut.

The behavior is defined once in `site/src/scripts/pop.js` and loaded from `Base.astro`, so every
page — including Markdown pages — has it without per-page script. Its uses are the significance
citation markers, significance asides (`[note n]`), in-text editorial notes (`\ednote`), the work
page's status badge, the timeline's node cards, and the About-page epigraph. The `search` capability
excludes `.pop` apparatus from the index. Established by `about-epigraph` (archived 2026-08-01).

#### Scenario: Popover reveals on hover, focus, and tap

- **WHEN** a visitor hovers, focuses, or taps a `.pop` element
- **THEN** its `.pop-content` is revealed (pinned open on tap), kept within the viewport, and closed on Escape or outside click

### Requirement: Legal pages

The site SHALL serve About, Copyright & takedown, Contribute, and Contact pages. The About page opens
with an epigraph — Abel's "study the masters, not the pupils" attributed to `Niels Henrik Abel` —
whose full source (manuscript, page, archive) and French original are revealed in a source popover
(see "Source popovers (shared apparatus)").

#### Scenario: Legal pages are served

- **WHEN** a visitor navigates the site
- **THEN** About, Copyright & takedown, Contribute, and Contact pages are served, the About page opening with the sourced Abel epigraph

### Requirement: Journal pages

The site SHALL publish a page per journal at `/journals/<slug>/` and an index at `/journals/`.
Journals are aggregated across works by their venue key (the `venues:` key in `corpus/vocab.yaml`,
which is already a slug). `pipeline/build_site_data.py` SHALL emit a top-level `journals` list into
`works.json`, each entry carrying the venue's resolved metadata (`name`, `aka`, `kind`, `founded`,
`ceased`, `publisher`, `place`, `note`, `archives`) and the venue's works. Only public-domain works
that pass the gate feed the aggregation, so no journal page can surface an unpublished work; the
copyright status is not restated.

The index SHALL present every `periodical` venue as a compact, title-led list — each row being the
journal's `name` linking to its page — ordered alphabetically, excluding the `book`/`manuscript`
sentinels, with a "Journals" nav link pointing to it. The index SHALL NOT show a venue's era or
place. A work count SHALL be shown for a venue only when that venue has one or more works, as a
positive marker; a venue with zero works SHALL show no count (never `0 works`) and SHALL appear as an
equal in the same alphabetical order, neither demoted nor hidden.

A journal page SHALL show the full `name`, the `aka`/era/`publisher`/`place` when set, the `note`,
and a "Find the originals" block linking every `archives` entry. Its works SHALL be grouped into
collapsible sections, one section per volume when a work records a `volume`, otherwise one section
per dated issue keyed by `month`+`year` (a journal issued monthly rather than by volume, such as the
Acta Eruditorum, is grouped by issue). Sections SHALL be ordered chronologically and open by
default (the reader may collapse any section). Each section's collapsed control SHALL show a label — `Volume {volume} ({year})` when a
volume is recorded, otherwise `{month} ({year})` (falling back to `{year}` when no month is recorded)
— together with the section's work count. Expanding a section SHALL reveal its works, each showing
the title linking to the work page, the work's English translated title (`title_en`) when one exists,
the author, the existing `venue_full` citation, the status, and a direct link to the work's
`source.scan_url`. `pipeline/build_site_data.py` SHALL emit `title_en`, `volume`, and `month` on each
journal work so the grouping and translated titles can render.

When a `periodical` venue carries metadata but has zero works, its page SHALL still be published with
its metadata and its "Find the originals" block promoted, and SHALL replace an empty works list with a
single quiet line inviting the reader to help revive the journal, linking to the Contribute page. The
Contribute page SHALL, in its transcribing step, refer readers to the journals as a place to discover
originals worth reviving.

Venue labels in the catalog cards and the work-page header/citation SHALL link to the corresponding
journal page.

#### Scenario: Browsing the journal index
- **WHEN** a visitor opens `/journals/`
- **THEN** every `periodical` venue is listed as a title-led link ordered alphabetically, the `book`/`manuscript` sentinels are absent, and no era or place is shown on the index

#### Scenario: Work count shown only when non-zero
- **WHEN** the index lists a venue that has one or more works
- **THEN** a work count is shown as a positive marker on that row, while a venue with zero works shows no count at all

#### Scenario: Finding a journal's originals
- **WHEN** a visitor opens a journal page whose venue has `archives` entries
- **THEN** a "Find the originals" block lists each entry as a labelled link to a repository holding the digitized full run

#### Scenario: A journal's works are grouped into collapsible sections
- **WHEN** a visitor opens a journal page that has works
- **THEN** the works are grouped into collapsible sections, open by default and collapsible by the reader, each labelled `Volume {volume} ({year})` when a volume is recorded or `{month} ({year})` otherwise, with the section's work count

#### Scenario: Expanding a section reveals works with their translation
- **WHEN** a visitor expands a section
- **THEN** each work shows its title linking to the work page, its English translated title when one exists, its author, `venue_full` citation, status, and a direct link to that work's `source.scan_url`

#### Scenario: Curated journal with no works yet
- **WHEN** a `periodical` venue carries metadata but has zero works
- **THEN** its page is published with the metadata and a promoted "Find the originals" block, and shows a single quiet line inviting the reader to help revive the journal, linking to the Contribute page

#### Scenario: Contribute page points to the journals
- **WHEN** a visitor reads the Contribute page's transcribing step
- **THEN** it refers them to the journals as a place to discover originals worth reviving

