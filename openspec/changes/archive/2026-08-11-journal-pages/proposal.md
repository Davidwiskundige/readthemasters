# Change: journal-pages

## Why

The site already treats the publication venue as first-class data — every `work.yaml` carries a
`publication.venue`, the value is validated against a controlled `venues` list in
`corpus/vocab.yaml`, and "Journal / venue" is a catalog facet (PLAN.md §9a, §592). But a venue is
currently only a label: a visitor can filter by "Acta Eruditorum" yet cannot learn what that
journal was, when it ran, or — most importantly for this project's mission — **where to find the
original run for themselves**. That "go read the source" pointer exists per work (`source.scan_url`)
but never at the level of the journal, and there is no overview of which journals the corpus draws
from.

This change promotes the venue from a bare label into a browsable **Journals** section, parallel to
the shipped author pages: an overview of the periodicals, and per-journal pages that curate where
each one's digitized full run lives.

## What changes

- **Richer venue entries.** Each entry in `corpus/vocab.yaml` `venues:` MAY become an object instead
  of a bare string. A bare string keeps working (backward compatible). The object adds optional
  metadata used by the journal pages: `name` (the full title, as today), `aka` (short/common name),
  `kind` (`periodical` | `book` | `manuscript`, default `periodical`), `founded`/`ceased` years,
  `publisher`/`place`, a one-paragraph `note`, and an `archives:` list of
  `{label, url}` links to the repositories that hold the digitized full run (GDZ, Biodiversity
  Heritage Library, Gallica, Internet Archive, ETH e-periodica, the Euler Archive, …).
- **Journal identity + slug.** A venue's vocab key is already a slug; it becomes the permanent page
  path `/journals/<key>/`. `build_site_data.py` aggregates works per venue and emits a top-level
  `journals` list (metadata + the venue's works) into `works.json`.
- **Per-journal page** at `/journals/<slug>/`: full name and `aka`, era (`founded`–`ceased`),
  publisher/place, the `note`, a **"Find the originals"** block linking every `archives` entry, and
  the list of the journal's works on the site (title → work page, year, volume/pages from the
  existing `venue_full`, status badge) — each work also linking directly to its own `source.scan_url`
  so a reader lands on the exact page of the exact scan.
- **Journal index** at `/journals/` listing every `periodical` venue alphabetically with era and
  work count, and a **"Journals"** nav link. The `book`/`manuscript` sentinel venues are excluded
  from the section (they are not journals).
- **Venue labels link** to their journal page from the catalog cards and the work-page header/citation.
- **Overview beyond the corpus (optional).** Because the vocab is curated, a `periodical` venue may
  carry metadata and appear in the overview even with zero works yet — so the section can also point
  readers at journals we intend to draw from, serving the "which journals are there" goal directly.

## Impact

- Extends `corpus-format` (venue entries may be objects with optional metadata + an `archives` list;
  `book`/`manuscript` marked via `kind`) and `site-catalog` (new journal pages/index, venue links,
  new `works.json` `journals` field). Backward compatible: a bare-string venue and a work with no
  extra venue metadata render exactly as before.
- No change to the copyright gate's verdicts — publication already implies public domain, so the
  journal page does not restate copyright status; only public-domain works that pass the gate feed
  the aggregation.
- Touches `pipeline/build_site_data.py` (venue metadata parse + journal aggregation, reusing the
  existing `venues` label resolution), `pipeline/build_catalog.py` and `pipeline/validate.py`
  (accept object-or-string venue entries; validate `archives` urls and `kind`),
  `corpus/vocab.yaml` (upgrade the seed venues), `site/src/pages/journals/`,
  `site/src/pages/index.astro`, `site/src/pages/works/[id].astro`, `site/src/layouts/Base.astro`,
  `site/src/styles/global.css`, and adds `pipeline/tests/test_journals.py`.
