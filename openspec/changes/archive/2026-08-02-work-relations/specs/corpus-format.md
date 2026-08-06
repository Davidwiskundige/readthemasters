# Spec (delta): work-relations

## MODIFIED: work.yaml schema

Adds one optional field:

- `relations` (list, optional) — directed dependency edges from **this** work to **earlier**
  corpus works. Each edge is a mapping:
  - `to` (string, required) — the id of another corpus work. Must exist and must be same-year or
    earlier than this work.
  - `kind` (string, required) — a `relation_kinds` vocab key: `cites` (the transcribed text
    references that work) or `builds-on` (a curated conceptual dependency — editorial, like
    `significance`).
  - `recommended` (optional) — `true` or `primary`. At most one edge per work may carry it; that
    edge is the reader's **recommended previous read**. `primary` additionally makes the target
    treat this work as the head of its own "recommended next" list (ties fall back to
    chronological order).
  - `note` (string, optional) — a short editorial gloss on this specific edge. Plain text + inline
    KaTeX only (the same house-style constraints as `significance`).
  - `sources` (list, optional) — `{citation, url?}` references backing the edge, shown via the
    shared `.pop` popover apparatus.

Edges are authored backward in time so that adding a new work never requires editing an older
one; the build computes the inverse ("cited by" / "recommended next").

## ADDED: Controlled vocabulary — relation_kinds

`corpus/vocab.yaml` gains a `relation_kinds` map (key → display label), mirroring `tags`/`types`.
The validator rejects any `relations[].kind` not listed. Initial keys: `cites`, `builds-on`.

## MODIFIED: Copyright gate (validation)

The gate additionally checks, across the whole corpus:

- every `relations[].to` resolves to an existing work id (no dangling edges);
- `to ≠ self`;
- `year(to) ≤ year(self)` (edges point backward in time);
- `kind` ∈ `relation_kinds`;
- `recommended` ∈ {true, primary}, with at most one recommended edge per work;
- the dependency graph is acyclic (a DAG).

These are ordinary validation errors; they do not change the copyright semantics.
