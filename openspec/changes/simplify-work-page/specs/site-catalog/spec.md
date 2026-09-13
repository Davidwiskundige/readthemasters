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
