## MODIFIED Requirements

### Requirement: Related reading (dependency graph)

From each work's `relations` (corpus-format), `build_site_data.py` SHALL emit per work:
`relations_out` (its authored backward edges, each enriched with the target's `{id, title,
title_tex, by, year, url}` — `by` is the first author's surname — plus `kind`, `recommended`, `note`,
`sources`), `relations_in` (the computed inverse), `recommended_prev` (the single flagged edge or
null), and `recommended_next` (works that flagged this one, ordered `primary` first then by year).
Edges to a work not in the published set are dropped. The top-level JSON also gains a compact
`graph` — `nodes` (`{id, title, title_tex, by, year, discipline, url}`) and `edges` (`{from, to,
kind, recommended}`).

When a work has a recommended previous or next read, the work page shows a single-line
**"Related reading"** nav (surname + first few words of the title, linking to that work) in **two
places**:

- Near Significance (top of the page): the recommended previous read on the left, labelled
  `Read first:`, and the recommended next on the right, labelled `Next:`. A work with neither shows
  nothing.
- Directly after the text panels (original + translations): the recommended next only, labelled
  `Next:`. The previous read is intentionally omitted here — a reader who has reached the bottom has
  already read the current text, so telling them what to read *before* it is no longer actionable.
  Shown only when a recommended next exists; a work with no recommended next shows nothing at the
  bottom, even if it has a recommended previous.

Both placements render from the same `recommended_prev`/`recommended_next` data and share the same
terse style — the full graph (cites, built-on-by, …) is explored on the timeline. Every work page
also carries a "See this work in the timeline →" link to `/timeline/?focus=<id>`, opening the graph
pre-focused on that work.

#### Scenario: Edges to unpublished works are dropped

- **WHEN** a `relations` edge points to a work not in the published set
- **THEN** the emitted `relations_out`/`graph` omits that edge

#### Scenario: Top nav appears only when there is a recommendation

- **WHEN** a work has a recommended previous or next read
- **THEN** the work page shows the single-line "Related reading" nav near Significance; a work with
  neither shows nothing there

#### Scenario: Bottom nav shows Next only, and only when a recommended next exists

- **WHEN** a work has a recommended next read
- **THEN** the work page shows a "Related reading" nav after the text panels containing only the
  `Next:` link, matching the top nav's `recommended_next` target

#### Scenario: Bottom nav is absent without a recommended next

- **WHEN** a work has a recommended previous read but no recommended next
- **THEN** the top nav shows the `Read first:` link but the bottom nav renders nothing
