## MODIFIED Requirements

### Requirement: Work page

Each work SHALL have a page showing metadata, the source scan link + citation, a status badge, and
the transcription and each translation in tabs. Text is rendered from LaTeX to HTML by a lightweight
transform (`site/src/lib/tex.js`: headings, `\origpage` page markers, emphasis, em-dashes); inline
math is rendered by KaTeX. An `ai-draft` work shows a "not yet human-checked" notice and a
prefilled "report an error" link.

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

#### Scenario: ai-draft work is marked

- **WHEN** a work's status is `ai-draft`
- **THEN** the page shows a "not yet human-checked" notice and a prefilled "report an error" link
