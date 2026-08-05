# Tasks: dependency-timeline

- [x] Add author surname (`by`) to each `graph` node in `build_site_data.py`
- [x] `site/src/pages/timeline.astro`: build-time layout (reading-order x, barycenter-median y)
- [x] Compact citation-tag nodes with `.pop` popovers (linked title + author) + plain SVG lines
      (solid builds-on / dashed cites, no arrowheads; column-skippers curve)
- [x] Century axis (thin dashed rule + label per boundary)
- [x] Client JS: focus selector + back/forward controls fade the rest by graph distance (equal
      steps); click-a-node focuses it; `?focus=<id>` deep link; each work page links in
- [x] No-JS access via focus/hover popovers
- [x] Timeline styles in `global.css` (theme-aware, wide content scrolls in its own container)
- [x] Nav link to `/timeline/` in `Base.astro`
- [x] Verify: `npm run build` succeeds, preview renders graph, focus+fade works, screenshot
- [x] Fold delta into `openspec/specs/site-catalog`, archive this change, update `openspec/project.md`
