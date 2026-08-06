# Capability: site-catalog

Current source of truth for the public static site. Astro site under `site/`, fed by
`pipeline/build_site_data.py` (emits `site/src/data/works.json`). Established by the `site-catalog`
change (archived 2026-07-18).

## Requirement: Only public-domain works are published

The site build includes a work only if it passes the copyright gate and meets the minimum status.
Non-public-domain works never appear in the catalog or as pages.

## Requirement: Catalog with browse & filter

The catalog lists works and filters them client-side over the build-time JSON index (no server).
Facets: discipline, topic (tags), language, available translations, type, quality status, and a
year range, plus free-text search over title/author. Filter state is reflected in the URL query
string so a filtered view is shareable.

## Requirement: Work page

Each work has a page showing metadata, the source scan link + citation, a status badge, and the
transcription and each translation in tabs. Text is rendered from LaTeX to HTML by a lightweight
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

## Requirement: LaTeX titles rendered as math

When a work's `work.yaml` carries an optional `title_tex` (and/or `title_en_tex`), the site displays
that LaTeX rendering — with inline `$…$` math set by KaTeX — wherever the title is shown to a reader:
the work-page `<h1>` and English subtitle, the catalog cards, and the author-page work lists.
Established by `math-titles` (archived 2026-07-25).

The plain `title` / `title_en` remain canonical for everything that cannot show math: the browser
`<title>`, OpenGraph/Twitter tags, JSON-LD, the Pagefind result-card `title` metadata, and the
catalog's free-text filter/sort (which run off the plain `data-title` attributes). A work without
`title_tex` is unaffected — its plain title is shown as before.

`pipeline/build_site_data.py` passes `title_tex` / `title_en_tex` through to `works.json` (including
the per-author work lists). Rendering is client-side, consistent with the rest of the site's math
(build-time pre-rendering remains PLAN.md §9 backlog #18); each title page/list runs KaTeX
auto-render over the `$…$` delimiter. Titles use `\frac`/`\dfrac` as the author chooses; the
work-page `<h1>` scales its math down with CSS so a display fraction does not overwhelm the heading.

## Requirement: Significance note

When a work's `work.yaml` carries an optional `significance` field, the work page shows it as a
clearly-labelled "Significance" callout, visually distinct from the transcription so it reads as
editorial context (ours), not the author's text. Math in the note is rendered by KaTeX, as in the
transcription.

## Requirement: Related reading (dependency graph)

From each work's `relations` (corpus-format), `build_site_data.py` emits per work: `relations_out`
(its authored backward edges, each enriched with the target's `{id, title, title_tex, by, year,
url}` — `by` is the first author's surname — plus `kind`, `recommended`, `note`, `sources`),
`relations_in` (the computed inverse), `recommended_prev` (the single flagged edge or null), and
`recommended_next` (works that flagged this one, ordered `primary` first then by year). Edges to a
work not in the published set are dropped. The top-level JSON also gains a compact `graph` —
`nodes` (`{id, title, title_tex, by, year, discipline, url}`) and `edges` (`{from, to, kind,
recommended}`).

When a work has a recommended previous or next read, the work page shows a single-line
**"Related reading"** nav near Significance: the recommended previous read on the left
(labelled `Read first:` — surname + first few words of the title) and the recommended next on the
right (labelled `Next:` — surname + first few words), each linking to that work. It is deliberately terse — the
full graph (cites, built-on-by, …) is explored on the timeline. A work with neither shows nothing.
Every work page also carries a "See this work in the timeline →" link to `/timeline/?focus=<id>`,
opening the graph pre-focused on that work.

## Requirement: Timeline page

A page at `/timeline/` (linked from the nav) visualises the whole-corpus `graph` as a
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
that work and scrolled to it — which each work page uses to link into the graph. The page works without JavaScript: each
node is a focus/hover-revealed popover (CSS `:focus-within`/`:hover`) carrying the work's linked
title and author(s), so every work (and its author) is reachable by keyboard and screen reader;
focus-dimming is a JS enhancement only. The diagram scrolls within its own horizontal-scroll container. Zero
runtime dependencies (SVG + a small inline script).

The hand-rolled barycenter layout is deliberate at the current corpus size. **Future option:** if
the graph ever grows tangled, a dedicated layered-layout engine — `dagre` (as used by mermaid) or
`elkjs` — could replace the build-time layout step; it would add a dependency, so it is worth doing
only when hand-rolling stops being enough.

## Requirement: Downloads

Each work page offers, in one consolidated list: the source `.tex` for the original and each
translation (always), the compiled PDF for each (when built), and the shared `readmasters.sty`
preamble. `.tex` copies and the preamble are emitted to `site/public/tex/` at build time.

## Requirement: PDF compilation (deploy-time)

`pipeline/build_pdfs.py` compiles each public-domain work's `.tex` to PDF with Tectonic during the
CI deploy, into `site/public/pdf/<id>/<name>.pdf` (served at `/pdf/<id>/…`). PDFs are never
committed and are regenerated per deploy. A work may ship a pre-made PDF override
(`corpus/<id>/pdf/<name>.pdf`), which is copied instead of compiled. When no PDF exists, the page
labels it "compiled on deploy" rather than showing a dead link.

`\rmfigure` paths are written relative to the work root for both `original.tex` and
`translations/<lang>.tex`, so the work directory itself is on Tectonic's search path alongside the
`.tex` file's own directory and `corpus/preamble`.

## Requirement: Citations (BibTeX)

Each work page provides ready-made BibTeX (`site/src/lib/bibtex.js`) for the original work, our
transcription, each of our translations, and any referenced external translations — each with a
Copy button, plus a "Download all as .bib". Citekeys are ASCII (diacritics transliterated).

## Requirement: Existing translations elsewhere

Referenced `external_translations` are shown as an "Existing translations elsewhere" section
linking out (translator, year, venue, license) — never hosted.

## Requirement: Author pages

The site publishes a page per author at `/authors/<slug>/` and an index at `/authors/` (linked from
the nav as "Authors"). Established by the `author-pages` change (archived 2026-07-24).

Authors are aggregated across works by a stable identity key: `wikidata_id` when present, otherwise
a slug of the name — so the same author across works merges into one page, while namesakes with
distinct QIDs stay separate (PLAN.md §9a). `pipeline/build_site_data.py` emits the aggregation into
`works.json` as a top-level `authors` list and attaches each author's `slug` to every author object
inside each work, so catalog cards and the work-page header link author names to their page.

Each author page shows the name, an optional one-line `bio` and optional public-domain `portrait`
(a small image we host ourselves, copied from `corpus/authors/<slug>/` into
`site/public/authors/<slug>/` at build time — like figure crops; only full scans are never
rehosted), and the birth/death years. The portrait links to its `source` URL (its Wikimedia Commons
file page) when clicked, and shows the optional `credit` artist attribution as a caption. Public-domain status is *not* restated on the page —
everything on the site has already passed the gate, so it is a given. A MacTutor (St Andrews)
biography link is shown when the author's `mactutor` field is set (the only external link surfaced —
`wikidata_id` is retained in the data for aggregation and the CI death-date check, but is not shown
to visitors), followed by the author's works on the site (title → work page, year, venue, status
badge), ordered by year. The index lists every author
alphabetically with dates and work count, above a search box that filters the list client-side by
name/bio as you type (mirroring the catalog's search) with a live count and an empty-state message.
Only public-domain works that pass the gate feed the
aggregation, so no author page surfaces an unpublished work.

## Requirement: Revision history

Each work page shows a revision history of the work, sourced from the optional `changelog` block in
the work's `provenance.yaml` — a curated, human-authored list, not anything derived from git.
Established by `revision-history` (archived 2026-07-25), then re-sourced from the changelog by
`provenance-changelog` (archived 2026-07-25, PLAN.md §9 #4); the earlier git-derived approach
(`revision-history` / `revision-history-filter`) is superseded.

`pipeline/build_site_data.py` emits each work's `changelog` into `works.json` as a list of
`{date, summary}` entries ordered newest first. The work page renders it as a single collapsed
`<details>` "Revision history" section near the "Report an error" link, whole-work in scope, one row
per entry (date + summary). A work with no `changelog` shows no revision-history section, and the
build never fails for its absence.

## Requirement: SEO & structured metadata

Every page advertises a canonical URL, social-preview metadata, and machine-readable structured
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

## Requirement: Source popovers (shared apparatus)

The site provides a single popover behavior, shared across all pages, for revealing editorial source
material without cluttering the running text. Any element marked `.pop` containing a `.pop-content`
child reveals that content on pointer hover, on keyboard focus, and on a click/tap that pins it open
(so it is usable on touch); pressing Escape or clicking outside closes it, and JavaScript keeps the
revealed card within the viewport. The trigger is the whole `.pop` wrapper, and a click that lands
inside an open `.pop-content` (e.g. a citation link) acts normally rather than toggling the card
shut.

The behavior is defined once in `site/src/scripts/pop.js` and loaded from `Base.astro`, so every
page — including Markdown pages — has it without per-page script. Its uses are the significance
citation markers, in-text editorial notes (`\ednote`), and the About-page epigraph. The `search`
capability excludes `.pop` apparatus from the index. Established by `about-epigraph` (archived
2026-08-01).

## Requirement: Legal pages

The site serves About, Copyright & takedown, Contribute, and Contact pages. The About page opens
with an epigraph — Abel's "study the masters, not the pupils" attributed to `Niels Henrik Abel` —
whose full source (manuscript, page, archive) and French original are revealed in a source popover
(see "Source popovers (shared apparatus)").
