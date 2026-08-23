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

#### Scenario: Significance shown as editorial callout

- **WHEN** a work has a `significance` field
- **THEN** the work page shows it as a distinct "Significance" callout with KaTeX-rendered math

### Requirement: Related reading (dependency graph)

From each work's `relations` (corpus-format), `build_site_data.py` SHALL emit per work:
`relations_out` (its authored backward edges, each enriched with the target's `{id, title,
title_tex, by, year, url}` — `by` is the first author's surname — plus `kind`, `recommended`, `note`,
`sources`), `relations_in` (the computed inverse), `recommended_prev` (the single flagged edge or
null), and `recommended_next` (works that flagged this one, ordered `primary` first then by year).
Edges to a work not in the published set are dropped. The top-level JSON also gains a compact
`graph` — `nodes` (`{id, title, title_tex, by, year, discipline, url}`) and `edges` (`{from, to,
kind, recommended}`).

When a work has a recommended previous or next read, the work page shows a single-line
**"Related reading"** nav near Significance: the recommended previous read on the left
(labelled `Read first:` — surname + first few words of the title) and the recommended next on the
right (labelled `Next:` — surname + first few words), each linking to that work. It is deliberately
terse — the full graph (cites, built-on-by, …) is explored on the timeline. A work with neither
shows nothing. Every work page also carries a "See this work in the timeline →" link to
`/timeline/?focus=<id>`, opening the graph pre-focused on that work.

#### Scenario: Edges to unpublished works are dropped

- **WHEN** a `relations` edge points to a work not in the published set
- **THEN** the emitted `relations_out`/`graph` omits that edge

#### Scenario: Related-reading nav appears only when there is a recommendation

- **WHEN** a work has a recommended previous or next read
- **THEN** the work page shows the single-line "Related reading" nav; a work with neither shows nothing

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

Each work page SHALL offer, in one consolidated list: the source `.tex` for the original and each
translation (always), the compiled PDF for each (when built), and the shared `readmasters.sty`
preamble. `.tex` copies and the preamble are emitted to `site/public/tex/` at build time.

#### Scenario: Consolidated downloads list

- **WHEN** a work page renders
- **THEN** it offers the original and each translation `.tex` (always), each compiled PDF (when built), and the shared preamble in one list

### Requirement: PDF compilation (deploy-time)

`pipeline/build_pdfs.py` SHALL compile each public-domain work's `.tex` to PDF with Tectonic during
the CI deploy, into `site/public/pdf/<id>/<name>.pdf` (served at `/pdf/<id>/…`). PDFs are never
committed and are regenerated per deploy. A work may ship a pre-made PDF override
(`corpus/<id>/pdf/<name>.pdf`), which is copied instead of compiled. When no PDF exists, the page
labels it "compiled on deploy" rather than showing a dead link.

`\rmfigure` paths are written relative to the work root for both `original.tex` and
`translations/<lang>.tex`, so the work directory itself is on Tectonic's search path alongside the
`.tex` file's own directory and `corpus/preamble`.

#### Scenario: PDF override is copied, not recompiled

- **WHEN** a work ships `corpus/<id>/pdf/<name>.pdf`
- **THEN** that file is copied to the served path instead of being compiled

#### Scenario: Absent PDF is labelled, not a dead link

- **WHEN** no PDF exists for an artifact at deploy
- **THEN** the page labels it "compiled on deploy" rather than linking to a missing file

### Requirement: Citations (BibTeX)

Each work page SHALL provide ready-made BibTeX (`site/src/lib/bibtex.js`) for the original work, our
transcription, each of our translations, and any referenced external translations — each with a
Copy button, plus a "Download all as .bib". Citekeys are ASCII (diacritics transliterated).

#### Scenario: BibTeX offered for every citable artifact

- **WHEN** a work page renders
- **THEN** it provides ASCII-citekey BibTeX for the original, transcription, each translation, and referenced external translations, each copyable, with a "Download all as .bib"

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
works on the site (title → work page, year, venue, status badge), ordered by year. The index lists
every author alphabetically with dates and work count, above a search box that filters the list
client-side by name/bio as you type (mirroring the catalog's search) with a live count and an
empty-state message. Only public-domain works that pass the gate feed the aggregation, so no author
page surfaces an unpublished work.

#### Scenario: Same author across works merges into one page

- **WHEN** the same author (same `wikidata_id`, else name slug) appears in multiple works
- **THEN** they are aggregated into one `/authors/<slug>/` page listing those works, while namesakes with distinct QIDs stay separate

#### Scenario: No author page surfaces an unpublished work

- **WHEN** an author has a work that fails the gate
- **THEN** that work does not appear on the author page

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
citation markers, in-text editorial notes (`\ednote`), and the About-page epigraph. The `search`
capability excludes `.pop` apparatus from the index. Established by `about-epigraph` (archived
2026-08-01).

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

