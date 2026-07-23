# Spec (delta): search

## ADDED: Capability `search`

Full-text search over the corpus, built by Pagefind as a post-build pass over the rendered site.

### Requirement: Full-text search page

The site serves `/search`: a query box that searches the full text of every published
transcription and translation. Results are ranked, show an excerpt with the match highlighted, and
carry the work's author, year and quality status. The query is reflected in the URL (`?q=…`) so a
search is shareable, and `/search?q=…` runs that search on load.

The catalog's own box keeps filtering titles and authors client-side; the two are cross-linked so a
reader who wants the other one is one click away.

### Requirement: What is indexed

Indexing is scoped to the reader section of work pages: the transcription and every translation,
plus the work's title and significance note. Site chrome (nav, footer), the downloads list, the
BibTeX store, status notices and the standalone legal pages are not indexed.

Mathematics is excluded from the index. The reader carries LaTeX source in the HTML, so indexing it
would fill the index with markup tokens and show TeX in excerpts; math spans are marked
`data-pagefind-ignore` instead. Searching for notation itself is out of scope for this capability
as specified.

### Requirement: Results address the exact text

A result links to the panel it was found in — a hit in a translation opens the translation tab, not
the original — and, where the text carries `\origpage` markers, to the page within it. Sub-results
are titled by the artifact ("English translation", "Original (Latin)") and the printed page number.

### Requirement: Built at deploy, never committed

The index is produced by `pagefind --site dist` after `astro build`, as part of `npm run build`, and
is written into the build output only. No index files are committed. When the index is absent (the
Astro dev server serves no `dist`), the search page reports that the index is built at deploy time
rather than failing.
