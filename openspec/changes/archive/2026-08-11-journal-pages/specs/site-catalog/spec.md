# Delta: site-catalog — journal pages

## ADDED Requirements

### Requirement: Journal pages

The site SHALL publish a page per journal at `/journals/<slug>/` and an index at `/journals/`.
Journals are aggregated across works by their venue key (the `venues:` key in `corpus/vocab.yaml`,
which is already a slug). `pipeline/build_site_data.py` SHALL emit a top-level `journals` list into
`works.json`, each entry carrying the venue's resolved metadata (`name`, `aka`, `kind`, `founded`,
`ceased`, `publisher`, `place`, `note`, `archives`) and the venue's works. Only public-domain works
that pass the gate feed the aggregation, so no journal page can surface an unpublished work; the
copyright status is not restated.

A journal page SHALL show the full `name`, the `aka`/era/`publisher`/`place` when set, the `note`, a
"Find the originals" block linking every `archives` entry, and the journal's works ordered by year
(title → work page, year, the existing `venue_full` citation, and a direct link to each work's
`source.scan_url`). The index SHALL list every `periodical` venue alphabetically with its era and
work count, excluding the `book`/`manuscript` sentinels, and a "Journals" nav link SHALL point to
it. Venue labels in the catalog cards and the work-page header/citation SHALL link to the
corresponding journal page.

#### Scenario: Browsing the journal index
- **WHEN** a visitor opens `/journals/`
- **THEN** every `periodical` venue is listed alphabetically with its era and work count, and the `book`/`manuscript` sentinels are absent

#### Scenario: Finding a journal's originals
- **WHEN** a visitor opens a journal page whose venue has `archives` entries
- **THEN** a "Find the originals" block lists each entry as a labelled link to a repository holding the digitized full run

#### Scenario: A journal page lists its works
- **WHEN** a journal has works in the corpus
- **THEN** each work appears with its title linking to the work page, its year and `venue_full` citation, and a direct link to that work's `source.scan_url`

#### Scenario: Curated journal with no works yet
- **WHEN** a `periodical` venue carries metadata but has zero works
- **THEN** it still appears in the index and gets a page with an empty works list
