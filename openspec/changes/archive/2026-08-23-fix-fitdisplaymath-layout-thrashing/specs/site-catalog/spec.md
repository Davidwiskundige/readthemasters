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

The reader regions are marked `data-pagefind-body` for the search index — see the `search`
capability for what that covers and what it excludes.

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

#### Scenario: Deep link opens the right panel

- **WHEN** a visitor opens `/works/<id>/#en`
- **THEN** the English translation panel is shown directly, its hash preserved for sharing

#### Scenario: Wide equation keeps its number legible

- **WHEN** a display equation is wider than the text column and its `\tag{n}` cannot fit beside it
- **THEN** the equation scrolls in its own area and the tag moves to its own right-aligned line beneath, decided by measuring the rendered formula

#### Scenario: Fitting cost does not scale with equation count

- **WHEN** the fitting pass runs over a work with many hundreds of display equations
- **THEN** it triggers a constant number of forced layout recalculations for the whole pass rather than one or more per equation, and assigns every equation the same classes an unbatched pass would

#### Scenario: ai-draft work is marked

- **WHEN** a work's status is `ai-draft`
- **THEN** the page shows a "not yet human-checked" notice and a prefilled "report an error" link
