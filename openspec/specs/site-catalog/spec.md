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

## Requirement: Significance note

When a work's `work.yaml` carries an optional `significance` field, the work page shows it as a
clearly-labelled "Significance" callout, visually distinct from the transcription so it reads as
editorial context (ours), not the author's text. Math in the note is rendered by KaTeX, as in the
transcription.

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
alphabetically with dates and work count. Only public-domain works that pass the gate feed the
aggregation, so no author page surfaces an unpublished work.

## Requirement: Legal pages

The site serves About, Copyright & takedown, Contribute, and Contact pages.
