# Change: site-catalog

## Why

With the corpus format and copyright gate in place, the corpus needs a public face: a browsable
catalog and per-work pages that render the transcriptions/translations, expose the source and
downloads, and let people cite the texts. (This change is being recorded retroactively — the work
was built and verified in the browser before the spec was written; it is reconciled here so
`openspec/specs/` reflects reality.)

## What changes

- Astro static site under `site/`, built from a single `works.json` produced by
  `pipeline/build_site_data.py` (only public-domain works at/above the minimum status).
- Catalog with client-side facet filtering (discipline, topic, language, translations, type,
  status, year) + search, URL-synced.
- Work page: metadata, source, status badge, tabbed original/translation, LaTeX→HTML render
  (`site/src/lib/tex.js`) with KaTeX math, ai-draft notice + report-an-error link.
- Downloads: `.tex` (original + translations) and the shared preamble, plus PDF links when built.
- PDF compilation at deploy time with Tectonic (`pipeline/build_pdfs.py`), never committed.
- BibTeX citations (`site/src/lib/bibtex.js`) for the original, our edition, translations, and
  referenced external translations, with copy + download.
- "Existing translations elsewhere" section from `external_translations`.
- Legal pages (About, Copyright, Contribute, Contact).

## Impact

- New: `site/`, `pipeline/build_site_data.py`, `pipeline/build_pdfs.py`.
- Extends `corpus-format` (adds `external_translations`, `publication.volume/pages`) and depends on
  `copyright-gate` (only PD works are published).
- Adds a CI `build-site` job (Tectonic + Astro build).
