# Spec (delta): site-catalog

## ADDED: Public-domain-only publication
Only works passing the copyright gate at/above the minimum status are included in the build.

## ADDED: Catalog with browse & filter
Client-side facet filtering (discipline, topic, language, translations, type, status, year) +
search over the build-time JSON index, with URL-synced state.

## ADDED: Work page
Metadata, source link + citation, status badge, tabbed original/translation, LaTeX→HTML render
with KaTeX math, ai-draft notice + report-an-error link.

## ADDED: Downloads
Consolidated per-work list: `.tex` (original + translations), shared `readmasters.sty`, and PDF
links when built. `.tex`/preamble emitted to `site/public/tex/`.

## ADDED: PDF compilation (deploy-time)
Tectonic compiles each PD work's `.tex` to PDF in CI into `site/public/pdf/…`; never committed;
optional pre-made override supported.

## ADDED: Citations (BibTeX)
Original / our edition / translations / external translations, with copy + `.bib` download.

## ADDED: Existing translations elsewhere
Referenced `external_translations` linked out, never hosted.

## ADDED: Legal pages
About, Copyright & takedown, Contribute, Contact.
