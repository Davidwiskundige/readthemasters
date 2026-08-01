# Delta: site-catalog — About epigraph and shared source popovers

## ADDED Requirements

### Requirement: Source popovers (shared apparatus)

The site SHALL provide a single popover behavior, shared across all pages, for revealing editorial
source material without cluttering the running text. Any element marked `.pop` containing a
`.pop-content` child SHALL reveal that content on pointer hover, on keyboard focus, and on a
click/tap that pins it open (so it is usable on touch); pressing Escape or clicking outside SHALL
close it, and JavaScript SHALL keep the revealed card within the viewport. The trigger SHALL be the
whole `.pop` wrapper, and a click that lands inside an open `.pop-content` (e.g. a citation link)
SHALL act normally rather than toggling the card shut.

The behavior SHALL be defined once in `site/src/scripts/pop.js` and loaded from `Base.astro`, so
every page — including Markdown pages — has it without per-page script. Its uses are the
significance citation markers, in-text editorial notes (`\ednote`), and the About-page epigraph. The
`search` capability continues to exclude `.pop` apparatus from the index.

#### Scenario: Whole wrapper reveals the card

- **WHEN** a reader hovers, focuses, or clicks anywhere on a `.pop` element
- **THEN** its `.pop-content` card is revealed, positioned within the viewport

#### Scenario: Interacting inside the open card

- **WHEN** a reader clicks a link inside an open `.pop-content`
- **THEN** the link acts normally and the card does not toggle shut

#### Scenario: Available on every page

- **WHEN** any page in the site is served
- **THEN** the shared popover script from `Base.astro` wires up every `.pop` element on it,
  including on Markdown pages such as About

## MODIFIED Requirements

### Requirement: Legal pages

The site serves About, Copyright & takedown, Contribute, and Contact pages. The About page opens
with an epigraph — Abel's "study the masters, not the pupils" attributed to `Niels Henrik Abel` —
whose full source (manuscript, page, archive) and French original are revealed in a source popover
(see "Source popovers (shared apparatus)").

#### Scenario: About page opens with the sourced Abel epigraph

- **WHEN** the About page is served
- **THEN** it opens with the Abel quotation and `— Niels Henrik Abel` inline
- **AND** the manuscript source and the French original are reachable via the epigraph's popover
