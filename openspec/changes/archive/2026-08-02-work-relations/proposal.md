# Change: work-relations

## Why

Works on the site stand alone. The historical threads that connect them — Fagnano's lemniscate
sketches feeding Euler's addition theorem, Euler feeding Legendre/Abel/Jacobi, Leibniz's and
Bernoulli's isochrone exchange — live only inside `significance` prose, never as data. Capturing
those links as a real graph lets us (1) show a reader *what to read before and after* a given
work, nudging them toward the important antecedents, and (2) later draw a dependency timeline
(a separate change). The goal is to encourage people to read more of the foundational works.

## What changes

- Add an optional `relations:` list to `work.yaml`. Each edge is authored on the **newer** work
  and points **backward** to an earlier corpus work it depends on:
  `{to, kind, recommended?, note?, sources?}`. `kind` ∈ a new `relation_kinds` vocab
  (`cites` = the transcribed text references it; `builds-on` = a curated conceptual dependency).
  At most one edge per work may be `recommended` (`true`, or `primary` to also claim the head of
  the target's "continue with" list) — that edge is the reader's **recommended previous read**.
- Validate relations in the copyright gate: targets must exist, `to ≠ self`,
  `year(to) ≤ year(self)`, `kind` ∈ vocab, `recommended` ∈ {true, primary} with at most one per
  work, and the whole graph must be acyclic (a DAG).
- Aggregate in `build_site_data.py`: emit per-work `relations_out` (enriched antecedents),
  `relations_in` (the computed inverse), `recommended_prev` (the single flagged edge) and
  `recommended_next` (the inverse, an ordered list — `primary` first, then by year), plus a
  compact top-level `graph` (nodes + edges) for the future timeline.
- Render a single-line **"Related reading"** nav on the work page: the recommended previous read
  on the left (*Read first* — surname + first few words) and the recommended next on the right
  (*Next*). The fuller graph (cites, built-on-by, …) is explored on the timeline.
- Seed `relations:` across the six existing works (the lemniscate lineage and the isochrone pair).

## Impact

- Extends `corpus-format` (new optional field + vocab + gate rules) and `site-catalog`
  (work-page display, new `works.json` fields).
- No copyright-gate semantics change; relation errors are ordinary validation errors.
- Backward compatible: a work with no `relations:` renders exactly as before.
