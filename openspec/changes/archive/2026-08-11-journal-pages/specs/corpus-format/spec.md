# Delta: corpus-format — venue metadata

## ADDED Requirements

### Requirement: Venue metadata

The `venues:` vocabulary in `corpus/vocab.yaml` SHALL accept each entry as either a bare string (the
full venue title, as today) or an object. When an entry is an object, `name` (the full title) MUST
be present and these fields are OPTIONAL: `aka` (short or common name), `kind` (`periodical` | `book` | `manuscript`, default
`periodical`), `founded`/`ceased` (years), `publisher`/`place`, `note` (a one-paragraph
description), and `archives` — an ordered list of `{label, url}` links to the repositories that host
the digitized full run. Every `archives[].url` MUST be an absolute `http(s)` URL, and the `book` and
`manuscript` sentinel venues MUST set `kind` accordingly so the site can exclude them from the
Journals section. The venue **label** consumed elsewhere (catalog, citations, `venue_full`) SHALL
resolve to `name` for objects and to the string itself for bare strings, so existing consumers are
unaffected. Venue metadata describes a public-domain periodical and its digitizations and MUST NOT
affect the copyright gate's verdicts.

#### Scenario: Bare-string venue stays valid
- **WHEN** a `work.yaml` sets `publication.venue` to a key whose `venues` entry is a bare string
- **THEN** the gate accepts it and the venue label resolves to that string, exactly as before

#### Scenario: Object venue with metadata is accepted
- **WHEN** a `venues` entry is an object with `name` present, `kind` in {periodical, book, manuscript}, and every `archives[].url` an absolute http(s) URL
- **THEN** validation passes and the venue label resolves to `name`

#### Scenario: Malformed venue object is rejected
- **WHEN** a `venues` object omits `name`, sets `kind` outside the allowed set, or gives an `archives` entry whose `url` is not an absolute http(s) URL
- **THEN** `pipeline/validate.py` reports an error and the build fails
