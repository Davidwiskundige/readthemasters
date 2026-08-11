# search

## Purpose

Full-text search over the corpus. Built by **Pagefind** as a post-build pass over the rendered
site, so the index is static files fetched on demand and no server is involved — the same posture
as the deploy-time PDFs. Established by the `search-full-text` change (archived 2026-07-23).

## Requirements

### Requirement: Full-text search page

The site SHALL serve `/search`: a query box that searches the full text of every published
transcription and translation. Results are ranked and show the work's title, author, year, original
language and quality status, plus an excerpt with the match highlighted. The query is reflected in
the URL (`?q=…`) so a search is shareable, and `/search?q=…` runs that search on load.

The catalog's own box keeps filtering titles and authors client-side over `works.json`; the two are
deliberately separate — synchronous facet filtering with URL-synced state on one side, ranked
asynchronous results on the other — and are cross-linked so either is one click away.

#### Scenario: Shareable search runs on load

- **WHEN** a visitor opens `/search?q=elastica`
- **THEN** the page runs that query on load and shows ranked results with highlighted excerpts

### Requirement: What is indexed

Indexing SHALL be scoped with `data-pagefind-body` to the reader regions of work pages: the
significance note and every text panel (transcription and translations). Everything else — site
chrome, the work's heading block, downloads, status notices, the BibTeX store, and the standalone
legal pages — sits outside every body region and is not indexed. The heading block still supplies
`data-pagefind-meta` (title, author, year, status, language) for the result cards.

Excluded from the index within those regions:

- **Mathematics.** The reader ships LaTeX source in the HTML and KaTeX renders it in the browser,
  so an unfiltered index would be full of markup tokens and excerpts would show TeX. `texToHtml`
  wraps every math span in `<span class="math|mathblock" data-pagefind-ignore>`; KaTeX still finds
  the delimiters inside the wrapper, and the block-level wrapper keeps the display-equation
  measurement (site-catalog) seeing the full column width. Searching *for* notation is a separate
  problem and is not part of this capability.
- **Our apparatus.** Citation markers and editorial-note popovers (`.pop`) are ours, not the
  author's text; indexing them drops stray markers and note text into excerpts.

#### Scenario: Only reader regions are indexed

- **WHEN** the index is built
- **THEN** the significance note and text panels are indexed while site chrome, the heading block, downloads, BibTeX, and legal pages are not

#### Scenario: Math and apparatus are excluded from excerpts

- **WHEN** a work page contains math spans and `.pop` apparatus
- **THEN** those are marked `data-pagefind-ignore` and never appear as index tokens or in excerpts

### Requirement: Results address the exact text

A result SHALL link to the panel the hit was found in — a hit in a translation opens the translation
tab, not the original — and, where the text carries `\origpage` markers, to the printed page within
it. Page markers are anchors rather than headings, so the page is resolved by pairing each
sub-result's word position with the last preceding page anchor.

Sub-results are labelled with the artifact they come from ("Original", "EN translation" — derived
from the anchor's language prefix), the section heading, and the printed page.

#### Scenario: Hit opens the correct panel and page

- **WHEN** a hit occurs in an EN translation on printed page 42
- **THEN** the result opens the EN translation panel at that page, labelled with artifact, section, and page

### Requirement: Built at deploy, never committed

The index SHALL be built at deploy and never committed: `npm run build` is
`astro build && pagefind --site dist`, writing the index into the build output only. When the index
is absent — the Astro dev server serves no `dist` — the search page reports that the index is built
at deploy time instead of failing. A `site-preview` launch configuration serves a built site locally
for searching.

#### Scenario: Missing index reports instead of failing

- **WHEN** the search page loads with no built index present (e.g. the dev server)
- **THEN** it reports that the index is built at deploy time rather than erroring
