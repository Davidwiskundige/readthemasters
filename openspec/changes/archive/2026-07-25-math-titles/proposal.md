# Change: math-titles

## Why

Some works have mathematics in their title — e.g. Euler's E251, "De integratione aequationis
differentialis m dx/√(1−x⁴) = n dy/√(1−y⁴)". Until now the title was a single plain-text field, so
that formula rendered as flat ASCII/Unicode everywhere it appeared (work-page heading, catalog card,
author page), just as it does on the Euler Archive — not as set mathematics, even though the
original prints it as a proper display fraction. The transcription body already renders LaTeX via
KaTeX; the title should be able to as well.

The constraint is that a title also feeds places that *cannot* contain math: the browser `<title>`,
OpenGraph/Twitter previews, JSON-LD structured data, the Pagefind result-card title, and the
catalog's free-text filter. So the plain title has to stay the canonical, machine-readable form.

## What changes

- **New optional corpus fields.** `work.yaml` gains optional `title_tex` and `title_en_tex` — LaTeX
  renderings of the title and English title, carrying inline `$…$` math. The plain `title` /
  `title_en` remain required and canonical. A work without the `_tex` fields is unchanged.
- **Rendered wherever a title is shown to a reader.** The work-page `<h1>` and English subtitle, the
  catalog cards, and the author-page work lists use the `_tex` variant when present and run KaTeX
  auto-render over the `$…$` delimiter. Rendering is client-side, consistent with the rest of the
  site's math (build-time pre-rendering stays PLAN.md §9 backlog #18).
- **Plain title stays canonical for non-visual surfaces.** The browser `<title>`, OG/Twitter tags,
  JSON-LD, the Pagefind `title` meta, and the catalog filter/sort all continue to use the plain
  `title` (the catalog filter runs off the existing `data-title` attributes).
- **Heading sizing.** A display fraction (`\dfrac`) at full `<h1>` size overwhelms the heading, so a
  small CSS rule scales the work-page title's math down; catalog and author cards render at their
  smaller heading size already and need no scaling.

## Impact

- Extends **site-catalog** (new "LaTeX titles rendered as math" requirement) and **corpus-format**
  (the two optional fields). No change to the copyright gate.
- `pipeline/build_site_data.py` passes the fields through to `works.json`, including the per-author
  work lists. Touches `site/src/pages/works/[id].astro`, `index.astro`,
  `site/src/pages/authors/[slug].astro`, and a CSS rule in `site/src/styles/global.css`.
- Purely additive: works without `title_tex` render exactly as before.
