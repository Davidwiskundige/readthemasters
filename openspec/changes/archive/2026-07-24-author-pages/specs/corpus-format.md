# Delta: corpus-format — optional author fields

## MODIFIED Requirement: work.yaml schema

Each entry in `authors` keeps its existing shape (`name` + `wikidata_id` + `death_year` or
`anonymous`, plus optional `birth_year`) and gains two **optional** display fields, used by the
author pages (see site-catalog):

- `bio` — a short one-line biographical descriptor (e.g. "Italian mathematician, count of Fagnano").
- `portrait` — an object `{file, credit, alt, source}`. `file` is a small public-domain portrait
  image **committed under `corpus/authors/<slug>/`** and **hosted by the site** (copied into
  `site/public/authors/<slug>/` at build time), exactly like the figure crops of §4.5. Only full
  scans are never rehosted (PLAN.md §3, §4.5). `alt` is the accessibility text; optional `credit` is
  a short artist attribution caption; optional `source` is the image's provenance URL (its Wikimedia
  Commons file page) that the portrait links to.

Both are optional and backward compatible: an author without them renders as before. When the same
author (same `wikidata_id`) appears in multiple works, `birth_year`/`death_year` must agree across
those works; `pipeline/validate.py` warns on a mismatch.
