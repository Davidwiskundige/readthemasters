# Tasks: author-pages

## Data

- [x] Add `slugify()` and author aggregation to `pipeline/build_site_data.py`: group by
      `wikidata_id`/name-slug, dedupe slugs, collect per-author works.
- [x] Attach `slug` to each author object inside every work; emit top-level `authors` list.
- [x] Warn in `pipeline/validate.py` when one `wikidata_id` has conflicting birth/death years.

## Site

- [x] `site/src/pages/authors/[slug].astro` — per-author page (bio, portrait, dates,
      MacTutor/Wikidata links, works list).
- [x] `site/src/pages/authors/index.astro` — alphabetical author index with work counts.
- [x] Link author names from `index.astro` catalog cards and `works/[id].astro` header.
- [x] Add "Authors" nav link in `Base.astro`; author styles in `global.css`.

## Tests & verification

- [x] `pipeline/tests/test_authors.py` — aggregation, slug uniqueness, pma-70 derivation.
- [x] Build site data + Astro build; verify an author page and links in the preview browser.

## Ship

- [x] Fold deltas into `openspec/specs/site-catalog` + `corpus-format`; update `project.md`;
      archive the change.
