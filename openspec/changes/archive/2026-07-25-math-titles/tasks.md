# Tasks: math-titles

## Corpus fields

- [x] `work.yaml` gains optional `title_tex` / `title_en_tex` (LaTeX with inline `$…$` math); plain
      `title` / `title_en` stay required and canonical.
- [x] `pipeline/build_site_data.py` passes both fields into `works.json`, including the per-author
      work lists in `build_authors`.

## Rendering

- [x] Work page (`works/[id].astro`): `<h1>` and English subtitle use the `_tex` variant when
      present; a hidden `data-pagefind-meta="title"` span keeps the plain title for search; the
      KaTeX auto-render pass covers `.workhead`.
- [x] Catalog (`index.astro`): card title/subtitle use the `_tex` variant; a KaTeX pass renders
      `$…$` over `#works`; filter/sort still read the plain `data-title` attributes.
- [x] Author page (`authors/[slug].astro`): work-list title/subtitle use the `_tex` variant; a KaTeX
      pass renders `$…$` over `.works`.
- [x] `global.css`: scale the work-page `<h1>` math down so a display fraction does not dominate.

## Canonical plain title preserved

- [x] Browser `<title>`, OpenGraph/Twitter, and JSON-LD all still use the plain `title` (via
      `Base.astro`, unchanged).
- [x] Pagefind result-card `title` metadata is the plain title (moved to a hidden span on the work
      page).

## Verification

Client-side rendering, so verified in the preview (no JS unit harness — house convention).

- [x] Work page — H1 + subtitle render the fraction via KaTeX, 0 errors; tab title and Pagefind
      title stay plain; a work without `title_tex` (Leibniz) renders its plain title unchanged.
- [x] Catalog + author page — card titles render the display fraction; other works' plain titles
      unaffected; catalog free-text filter still matches on the plain title.

## Ship

- [x] Fold the delta into `openspec/specs/site-catalog` and `openspec/specs/corpus-format`; archive
      the change.
