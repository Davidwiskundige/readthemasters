# Spec (delta): dependency-timeline

## ADDED: Timeline page

A new page at `/timeline/` visualises the whole-corpus dependency `graph` (from
`build_site_data.py`) as a time-ordered dependency diagram, and is linked from the site nav.

- **Layout is computed at build time** in the page frontmatter: x = one column per work in reading
  order (topological sort — Kahn's algorithm, year then id tie-break), so same-year works split into
  their true order and a lineage becomes a straight line; y = the Sugiyama barycenter-median step
  (median of each node's neighbours' lanes → a convergent node sits between its parents, a chain
  stays on one lane). The axis is a thin dashed rule at each century boundary — in the gap before
  that century's first work, labelled with the century (e.g. `1600`); tag + axis give the exact year.
- **Nodes** are compact citation-style tags — first two letters of the surname + last two digits of
  the year (e.g. `Eu61`, disambiguated `a`/`b`/… in reading order on collision). Hover or click a
  tag to open a `.pop` popover with the full work — a linked title (work page) and linked author(s)
  (author pages), plus year and venue, mirroring the catalog card's click targets.
  **Edges** are plain SVG lines (no arrowheads — order is clear from left → right), `builds-on` solid
  and `cites` dashed; a column-skipping edge curves to clear the node between.
- **Focus + depth:** a work selector and "steps back / forward" controls. Focusing a work fades the
  rest in equal steps scaled to the chosen depth — a node `d` hops away on a side with `N` steps
  sits `d/N` of the way to faint, and anything outside the range fades away; only the tag fades (the
  popover stays fully legible), and the default ("All") shows the entire corpus at full strength.
  This realises "pick a work and choose how far back and forward to look."
- **Accessibility:** each node is a focus/hover-revealed popover (CSS `:focus-within`/`:hover`)
  carrying the work's linked title and author(s), so every work (and its author) is reachable by
  keyboard and screen reader without JavaScript; focus-dimming is a JS enhancement only. Wide diagrams scroll
  within their own horizontal-scroll container; the page body never scrolls sideways.

## ADDED: graph node field

Each `graph.nodes[]` entry gains `by` — the first author's surname — for compact node labelling.
