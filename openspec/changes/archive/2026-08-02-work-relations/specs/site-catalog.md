# Spec (delta): work-relations

## MODIFIED: build_site_data output (works.json)

For every published work, `build_site_data.py` emits, from the work's `relations`:

- `relations_out` — the work's authored backward edges, each enriched with the target work's
  `{id, title, title_tex, by, year, url}` (`by` = first author's surname) plus the edge's `kind`,
  `recommended`, `note`, `sources`. Edges whose target is not in the published set (filtered by
  copyright/min-status) are dropped.
- `relations_in` — the computed inverse: works that cite or build on this one, same shape.
- `recommended_prev` — the single edge in `relations_out` flagged `recommended`, or null.
- `recommended_next` — the entries of `relations_in` whose source flagged this work
  `recommended`, ordered `primary` first then by year (a list; may be empty).

The top-level JSON also gains a compact `graph`: `nodes` (`{id, title, title_tex, by, year,
discipline, url}`) and `edges` (`{from, to, kind, recommended}`), for the dependency timeline.

## MODIFIED: Work page

When a work has a recommended previous or next read, the work page shows a single-line
**"Related reading"** nav near the Significance callout: the `recommended_prev` on the left
(labelled `Read first:` — surname + first few words of the title) and the first `recommended_next`
on the right (labelled `Next:` — surname + first few words), each linking to that work. Every work
page also links "See this work in the timeline →" (`/timeline/?focus=<id>`). Deliberately terse; the
fuller graph is on the timeline. A work with neither prev nor next shows only the timeline link.
