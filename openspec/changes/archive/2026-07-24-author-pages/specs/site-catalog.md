# Delta: site-catalog — author pages

## ADDED Requirement: Author pages

The site publishes a page per author at `/authors/<slug>/` and an index at `/authors/`.

Authors are aggregated across works by a stable identity key: `wikidata_id` when present, otherwise
a slug of the name (so namesakes with distinct QIDs stay separate, and the same author across works
merges into one page). `pipeline/build_site_data.py` emits the aggregation into `works.json` as a
top-level `authors` list, and attaches the author's `slug` to every author object inside each work
so the catalog and work pages can link to it.

Each author page shows:

- the author's name, an optional one-line `bio`, and an optional public-domain `portrait` — a small
  image the site hosts itself (copied from `corpus/authors/<slug>/` into `site/public/authors/`,
  like figure crops; only full scans are never rehosted). The portrait links to its `source` URL
  (Wikimedia Commons file page) when clicked, and shows the optional `credit` attribution caption;
- the birth and death years (public-domain status is not restated — everything on the site has
  already passed the gate, so it is a given);
- a MacTutor (St Andrews) biography link when `mactutor` is set (the only external link shown to
  visitors; `wikidata_id` is kept in the data for aggregation and the CI death-date check, but not
  displayed);
- the list of the author's works on the site (title → work page, year, venue, status badge), ordered
  by year.

The author index lists every author alphabetically with dates and work count, each linking to the
author page. A nav link "Authors" points to the index. Author names in the catalog cards and the
work-page header link to the corresponding author page.

Only public-domain works that pass the gate feed the author aggregation, so no author page can
surface a work that is not itself published.
