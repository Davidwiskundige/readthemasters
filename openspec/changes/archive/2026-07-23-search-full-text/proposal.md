# Change: search-full-text

## Why

The catalog's search box filters `works.json` — titles and author names only. Nothing on the site
searches the *texts*. For a corpus project that is the search readers actually want: find
*lemniscate*, *isochrona*, *potentia* inside the transcriptions and translations, not just in the
metadata. PLAN.md picks Pagefind for this (§3, §9a) and `project.md` lists `search` as an upcoming
capability; the archived `site-catalog` change already parked "(future) Pagefind full-text search"
as a task.

Pagefind fits the architecture: it is a post-build indexer over the rendered HTML, the index is
static files fetched on demand, and no server appears anywhere. Same posture as the deploy-time
PDFs.

## What changes

- **A `/search` page** doing full-text search over the transcriptions and translations, separate
  from the catalog's metadata filtering. The two stay apart deliberately: the catalog's facets are
  synchronous over `works.json` with URL-synced state, Pagefind's results are asynchronous and
  ranked; merging them means reconciling two result models for no reader benefit. Each page links
  to the other.
- **Only work pages are indexed.** `data-pagefind-body` scopes indexing to the reader section of a
  work page, which also keeps nav, footer, downloads, notices and the BibTeX store out of the
  index. About/Copyright/Contribute are not searched — search is over the corpus.
- **Math is excluded from the index.** The reader ships raw LaTeX in the HTML (`$…$`, `\[…\]`) and
  KaTeX renders it in the browser, so an unfiltered index would be full of `frac`, `cdot` and
  `sqrt`, and excerpts would show TeX source. `texToHtml` now wraps each math span in
  `<span class="math" data-pagefind-ignore>`; KaTeX still renders it. Searching *for* notation is a
  separate, harder problem (it needs the TeX normalized into searchable tokens) and is not in this
  change.
- **Results deep-link to the right panel.** Transcription and translations live in tab panels on
  one page, so a hit in the English translation would otherwise land the reader on the Original
  tab with nothing highlighted. Each panel gets a visually-hidden heading and an id; the tabs
  read and write `location.hash`; Pagefind's sub-results are anchored to those headings and to the
  `\origpage` markers, so a result reads "English translation — page 236" and opens there.
- **Page anchors are unique per panel.** `\origpage{236}` produced `id="p-236"` in *every* panel of
  a work, so a work with a translation had duplicate ids and `#p-236` was ambiguous. `texToHtml`
  takes an id prefix; the translation panels use `en-p-236`.
- **Result cards carry metadata.** `data-pagefind-meta` records author, year, status and language
  so results render like catalog cards rather than as bare titles.
- **The index is built at deploy, never committed.** `npm run build` becomes
  `astro build && pagefind --site dist`; `site/dist/` is already gitignored, so CI needs no change
  beyond the dependency. In `astro dev` there is no index and the search page says so instead of
  erroring.

## Impact

- New capability `search`; extends `site-catalog` (work-page indexing markup, panel anchors).
- Touches `site/package.json` (pagefind devDependency + build script), `site/src/pages/search.astro`
  (new), `site/src/pages/works/[id].astro`, `site/src/layouts/Base.astro` (nav link),
  `site/src/lib/tex.js` (math wrapper + id prefix), `site/src/styles/global.css`.
- No corpus, schema or gate change. Nothing about what publishes changes.
