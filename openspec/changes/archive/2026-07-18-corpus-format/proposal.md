# Change: corpus-format

## Why

Every downstream feature — the copyright gate, the site catalog, browse/filter, the translation
pipeline — depends on a stable, machine-readable format for each work. We need the schema before
anything else.

## What changes

- Define the directory layout for a work under `corpus/<id>/`.
- Define the `work.yaml` schema: canonical id, authors (with Wikidata ids and death dates),
  publication (year + venue), edition block, discipline + tags, language, copyright-fact sources,
  and the copyright assessment block.
- Define `provenance.yaml`: per-artifact status, model, effort, prompt version, reviewers.
- Define the controlled vocabulary file `corpus/vocab.yaml` (disciplines, venues, types, languages).
- Define the LaTeX house style: shared preamble `corpus/preamble/readmasters.sty` and the
  apparatus macros (`\origpage`, `\uncertain`, `\illegible`, `\ednote`, `\rmfigure`).
- Ship one fully-worked example work as a fixture (Riemann 1868).

## Impact

- New: `corpus/` layout, `corpus/vocab.yaml`, `corpus/preamble/`, the example work.
- Enables: `copyright-gate` (validates this schema), `site-catalog` (renders it).
