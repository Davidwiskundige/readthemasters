# Delta: site-catalog — LaTeX titles rendered as math

## ADDED Requirements

### Requirement: LaTeX titles rendered as math

When a work's `work.yaml` carries an optional `title_tex` (and/or `title_en_tex`), the site SHALL
display that LaTeX rendering — inline `$…$` math set by KaTeX — wherever the title is shown to a
reader: the work-page `<h1>` and English subtitle, the catalog cards, and the author-page work
lists. The plain `title` / `title_en` SHALL remain canonical for every surface that cannot show
math: the browser `<title>`, OpenGraph/Twitter tags, JSON-LD, the Pagefind result-card `title`
metadata, and the catalog's free-text filter/sort. A work without `title_tex` SHALL render its plain
title unchanged.

Rendering is client-side, consistent with the rest of the site's math. `pipeline/build_site_data.py`
SHALL pass `title_tex` / `title_en_tex` through to `works.json`, including the per-author work lists.

#### Scenario: Work title with math renders as set mathematics

- **WHEN** a work whose `work.yaml` has `title_tex` renders its page
- **THEN** the `<h1>` and English subtitle show the LaTeX title with its `$…$` math set by KaTeX
- **AND** the browser `<title>`, OpenGraph title, JSON-LD name, and Pagefind `title` metadata all
  use the plain `title`

#### Scenario: Catalog and author cards render the title math

- **WHEN** the catalog or an author page lists a work that has `title_tex`
- **THEN** that card's title (and English subtitle) render the `$…$` math via KaTeX
- **AND** the catalog's free-text filter and sort still match on the plain-text title

#### Scenario: A work without title_tex is unaffected

- **WHEN** a work has no `title_tex`
- **THEN** its title is shown as plain text everywhere, exactly as before
