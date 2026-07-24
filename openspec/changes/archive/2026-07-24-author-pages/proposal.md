# Change: author-pages

## Why

PLAN.md §9 backlog #4. The catalog and each work page name their authors as plain text, so a
visitor cannot see everything one author contributed, nor find a biography and the author's other
works in one place. Two works already share an author (Fagnano, Q1528006), and the corpus stores
exactly what an author page needs — `name`, `wikidata_id`, `birth_year`, `death_year` — but nothing
surfaces it.

## What changes

- **Author identity across works.** Authors are grouped by a stable key — `wikidata_id` when present,
  else a slug of the name (PLAN.md §9a: "id disambiguates namesakes"). Each distinct author gets a
  readable slug (`giulio-carlo-de-toschi-di-fagnano`) and a permanent page at `/authors/<slug>/`.
- **Per-author page.** Name, an optional one-line `bio` and optional public-domain `portrait`,
  the birth/death years, a MacTutor (St Andrews) biography link and a Wikidata link, and the list of
  the author's works on the site (title, year, venue, status badge). Public-domain status is not
  restated — everything on the site has already passed the gate, so it is a given.
- **Author index** at `/authors/` listing every author alphabetically with dates and work count,
  and an **"Authors"** nav link.
- **Author names link** to their author page from the catalog cards and the work-page header.
- **New optional author fields** `bio`, `mactutor` (a MacTutor/St Andrews biography id or URL —
  the site always links this biography when present), and `portrait` (`{file, credit, alt}`) — backward compatible;
  omitted authors render exactly as before. A `portrait` is a small public-domain image **hosted by
  the site**, committed under `corpus/authors/<slug>/` and copied into `site/public/authors/<slug>/`
  at build time — exactly like the figure crops of §4.5. Only full scans are never rehosted
  (PLAN.md §3, §4.5); small portraits, like figures, we host.
- **Cross-work consistency check.** `validate.py` warns when the same `wikidata_id` carries
  conflicting `birth_year`/`death_year` across works, so an author page never aggregates bad data.

## Impact

- Extends `site-catalog` (new author pages/index, author links, portrait hosting) and
  `corpus-format` (optional author display fields; portraits committed under `corpus/authors/<slug>/`).
  No change to the copyright gate's verdicts — publication already implies public domain, so the
  page does not restate it.
- Touches `pipeline/build_site_data.py` (author aggregation, slug), `pipeline/validate.py`
  (warn-only check), `site/src/pages/authors/`, `site/src/pages/index.astro`,
  `site/src/pages/works/[id].astro`, `site/src/layouts/Base.astro`, `site/src/styles/global.css`,
  and adds `pipeline/tests/test_authors.py`.
