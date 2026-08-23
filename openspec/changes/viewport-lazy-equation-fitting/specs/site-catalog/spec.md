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

Math SHALL be typeset only in panels the reader can actually see. On load the page typesets the
always-visible regions and whichever panels are currently showing; a hidden panel keeps its raw
LaTeX until it is revealed, and is typeset on first reveal — by a tab click or by the programmatic
reveal a deep link performs — before that panel's equations are measured. Each panel is typeset at
most once, so switching tabs repeatedly costs nothing after the first reveal. Because typesetting a
panel changes the height of everything below each formula, a deep link into a panel typeset this way
SHALL be scrolled to its anchor again once that panel has been typeset.

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
front, and equations far from the viewport MAY have their layout skipped by the browser entirely. A
panel shown for the first time has never been laid out, so measuring all of its equations at once
forces that whole first layout synchronously — seconds of blocked main thread on the corpus's
longest works, independent of typesetting, which is why fitting the panel eagerly is not acceptable
however cheap each individual measurement is. An equation whose width cannot yet be read SHALL be
treated as pending and measured once it can be, never silently left unfitted: skipping it is
indistinguishable in code from the hidden-panel case and loses the equation. Every equation that the
reader reaches SHALL end up with the same classes an eager pass would have given it.

Neither the typesetting nor the measuring of a revealed panel may depend on the order in which the
page's scripts are registered: both are bundled into one file and the bundler may emit them in
either order, so both SHALL be driven by the panel's observed change in visibility.

#### Scenario: Deep link opens the right panel

- **WHEN** a visitor opens `/works/<id>/#en`
- **THEN** the English translation panel is shown directly, its hash preserved for sharing

#### Scenario: Hidden panel is not typeset until opened

- **WHEN** a bilingual work's page finishes loading with only the original panel showing
- **THEN** only the original panel's math is typeset, and the translation panel's math is typeset when its tab is first opened

#### Scenario: Reopening a panel does not typeset it again

- **WHEN** the reader switches away from a panel and back to it
- **THEN** that panel is not typeset a second time

#### Scenario: Deep link into a lazily typeset panel lands on its anchor

- **WHEN** a search result opens `/works/<id>/#en-p-236`, revealing a panel whose math has not been typeset yet
- **THEN** the panel is typeset and the page is scrolled to `en-p-236` afterwards, so the linked page marker is in view

#### Scenario: Revealing a panel does not block on its whole length

- **WHEN** a reader opens the translation tab of a work with many hundreds of display equations
- **THEN** the equations on screen are fitted without the page first laying out and measuring every equation in the panel

#### Scenario: Scrolling fits equations as they arrive

- **WHEN** the reader scrolls to a part of a panel whose equations have not been measured yet
- **THEN** those equations are fitted as they approach the viewport, receiving the same classes an eager pass would have given them

#### Scenario: An equation that cannot yet be measured is not lost

- **WHEN** an equation's available width reads as zero because its layout has been skipped
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
