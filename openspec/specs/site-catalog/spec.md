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

## Requirement: Citations (BibTeX)

Each work page provides ready-made BibTeX (`site/src/lib/bibtex.js`) for the original work, our
transcription, each of our translations, and any referenced external translations — each with a
Copy button, plus a "Download all as .bib". Citekeys are ASCII (diacritics transliterated).

## Requirement: Existing translations elsewhere

Referenced `external_translations` are shown as an "Existing translations elsewhere" section
linking out (translator, year, venue, license) — never hosted.

## Requirement: Legal pages

The site serves About, Copyright & takedown, Contribute, and Contact pages.
