## MODIFIED Requirements

### Requirement: Journal pages

The site SHALL publish a page per journal at `/journals/<slug>/` and an index at `/journals/`.
Journals are aggregated across works by their venue key (the `venues:` key in `corpus/vocab.yaml`,
which is already a slug). `pipeline/build_site_data.py` SHALL emit a top-level `journals` list into
`works.json`, each entry carrying the venue's resolved metadata (`name`, `aka`, `kind`, `founded`,
`ceased`, `publisher`, `place`, `note`, `archives`) and the venue's works. Only public-domain works
that pass the gate feed the aggregation, so no journal page can surface an unpublished work; the
copyright status is not restated.

The index SHALL present every `periodical` venue as a compact, title-led list — each row being the
journal's `name` linking to its page — ordered alphabetically, excluding the `book`/`manuscript`
sentinels, with a "Journals" nav link pointing to it. The index SHALL NOT show a venue's era or
place. A work count SHALL be shown for a venue only when that venue has one or more works, as a
positive marker; a venue with zero works SHALL show no count (never `0 works`) and SHALL appear as an
equal in the same alphabetical order, neither demoted nor hidden.

A journal page SHALL show the full `name`, the `aka`/era/`publisher`/`place` when set, the `note`,
and a "Find the originals" block linking every `archives` entry. Its works SHALL be grouped into
collapsible sections, one section per volume when a work records a `volume`, otherwise one section
per dated issue keyed by `month`+`year` (a journal issued monthly rather than by volume, such as the
Acta Eruditorum, is grouped by issue). Sections SHALL be ordered chronologically and open by
default (the reader may collapse any section). Each section's collapsed control SHALL show a label — `Volume {volume} ({year})` when a
volume is recorded, otherwise `{month} ({year})` (falling back to `{year}` when no month is recorded)
— together with the section's work count. Expanding a section SHALL reveal its works, each showing
the title linking to the work page, the work's English translated title (`title_en`) when one exists,
the author, the existing `venue_full` citation, the status, and a direct link to the work's
`source.scan_url`. `pipeline/build_site_data.py` SHALL emit `title_en`, `volume`, and `month` on each
journal work so the grouping and translated titles can render.

When a `periodical` venue carries metadata but has zero works, its page SHALL still be published with
its metadata and its "Find the originals" block promoted, and SHALL replace an empty works list with a
single quiet line inviting the reader to help revive the journal, linking to the Contribute page. The
Contribute page SHALL, in its transcribing step, refer readers to the journals as a place to discover
originals worth reviving.

Venue labels in the catalog cards and the work-page header/citation SHALL link to the corresponding
journal page.

#### Scenario: Browsing the journal index
- **WHEN** a visitor opens `/journals/`
- **THEN** every `periodical` venue is listed as a title-led link ordered alphabetically, the `book`/`manuscript` sentinels are absent, and no era or place is shown on the index

#### Scenario: Work count shown only when non-zero
- **WHEN** the index lists a venue that has one or more works
- **THEN** a work count is shown as a positive marker on that row, while a venue with zero works shows no count at all

#### Scenario: Finding a journal's originals
- **WHEN** a visitor opens a journal page whose venue has `archives` entries
- **THEN** a "Find the originals" block lists each entry as a labelled link to a repository holding the digitized full run

#### Scenario: A journal's works are grouped into collapsible sections
- **WHEN** a visitor opens a journal page that has works
- **THEN** the works are grouped into collapsible sections, open by default and collapsible by the reader, each labelled `Volume {volume} ({year})` when a volume is recorded or `{month} ({year})` otherwise, with the section's work count

#### Scenario: Expanding a section reveals works with their translation
- **WHEN** a visitor expands a section
- **THEN** each work shows its title linking to the work page, its English translated title when one exists, its author, `venue_full` citation, status, and a direct link to that work's `source.scan_url`

#### Scenario: Curated journal with no works yet
- **WHEN** a `periodical` venue carries metadata but has zero works
- **THEN** its page is published with the metadata and a promoted "Find the originals" block, and shows a single quiet line inviting the reader to help revive the journal, linking to the Contribute page

#### Scenario: Contribute page points to the journals
- **WHEN** a visitor reads the Contribute page's transcribing step
- **THEN** it refers them to the journals as a place to discover originals worth reviving
