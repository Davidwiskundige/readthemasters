## ADDED Requirements

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

## MODIFIED Requirements

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
