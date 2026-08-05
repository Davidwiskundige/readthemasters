# Change: dependency-timeline

## Why

`work-relations` captures the corpus's dependency graph as data and surfaces it per work
("Related reading"). The same graph, seen whole, tells a second story: how ideas descend through
time. A timeline that draws the works on a shared time axis with their dependency edges lets a
reader trace a lineage — Leibniz's isochrone → Bernoulli's lemniscate → Fagnano → Euler — and,
by focusing one work and choosing how far back and forward to look, explore just its
neighbourhood. This is the discovery surface that encourages reading the important antecedents.

## What changes

- New page `site/src/pages/timeline.astro`, linked from the site nav. It consumes the top-level
  `graph` (nodes + edges) already emitted by `build_site_data.py`.
- **Layout computed at build** (in the page frontmatter): x = one column per work in reading order
  (topological sort), y = the Sugiyama barycenter-median step (a convergent node centres between its
  parents; a chain stays a straight line). The axis marks only the century. Nodes render as compact
  citation-style tags (surname initials + year, e.g. `Eu61`) whose full details appear in a `.pop`
  popover on hover/click; edges render as plain SVG lines (no arrowheads — order is clear from
  left → right), `builds-on` solid and `cites` dashed, column-skippers curved. Focusing a work fades
  the rest by graph distance.
- **Focus + depth (client JS):** a work selector plus "steps back / forward" controls; focusing a
  work fades the rest by graph distance in equal steps scaled to the chosen depth, and clicking a
  node focuses it. A `?focus=<id>` deep link (used by each work page) arrives pre-focused. "All"
  (default) shows the whole corpus undimmed.
- **Accessibility / no-JS:** each node's `.pop` popover (focus/hover-revealed) carries the work's
  linked title and author(s), so every work is reachable without JavaScript.
- Zero runtime dependencies — SVG + a small inline script only.

## Impact

- Extends `site-catalog` (a new page + nav entry). No corpus-format or gate change.
- Depends on the `graph` structure from `work-relations`; adds an author surname (`by`) to each
  graph node for compact labelling.
- Purely additive; nothing else changes.
