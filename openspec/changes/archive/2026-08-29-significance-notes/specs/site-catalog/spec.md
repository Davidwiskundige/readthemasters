## MODIFIED Requirements

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
citation markers, significance asides (`[note n]`), in-text editorial notes (`\ednote`), the
timeline's node cards, and the About-page epigraph. The `search` capability excludes `.pop`
apparatus from the index. Established by `about-epigraph` (archived
2026-08-01).

#### Scenario: Popover reveals on hover, focus, and tap

- **WHEN** a visitor hovers, focuses, or taps a `.pop` element
- **THEN** its `.pop-content` is revealed (pinned open on tap), kept within the viewport, and closed on Escape or outside click
