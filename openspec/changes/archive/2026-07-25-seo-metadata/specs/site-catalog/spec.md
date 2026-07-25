# Delta: site-catalog — SEO & structured metadata

## ADDED Requirements

### Requirement: SEO & structured metadata

Every page SHALL advertise a canonical URL, social-preview metadata, and machine-readable
structured data, derived at build time from data already in `works.json` — no new corpus field.

The shared layout (`site/src/layouts/Base.astro`) SHALL emit, for every page: a
`<link rel="canonical">` built from the configured `site` and the page path; OpenGraph tags
(`og:site_name`, `og:type`, `og:title`, `og:description`, `og:url`); and a Twitter `summary` card.
`og:type` SHALL default to `website` and be overridable per page. The layout SHALL accept optional
JSON-LD and, when supplied, render it in a single `<script type="application/ld+json">`.

Work pages, author pages, and the catalog home SHALL each supply schema.org structured data
appropriate to their type. This is metadata only: it changes nothing a reader sees, and it does not
alter the copyright gate or the corpus format.

#### Scenario: Canonical and social tags on every page

- **WHEN** any page renders
- **THEN** its `<head>` contains a `<link rel="canonical">` absolute URL built from `site` + the
  page path, OpenGraph tags (`og:site_name`, `og:type`, `og:title`, `og:description`, `og:url`), and
  a `twitter:card` of `summary`
- **AND** `og:type` is `website` unless the page overrides it (`article` for a work, `profile` for
  an author)

#### Scenario: Structured data for a work

- **WHEN** a work page renders
- **THEN** its `<head>` carries one `application/ld+json` block describing a `CreativeWork` whose
  subtype follows the work's `type` (`paper` → `ScholarlyArticle`, `book` → `Book`, otherwise
  `CreativeWork`)
- **AND** it records the title (with the English title as `alternativeName`), each author as a
  `Person` with `sameAs` linking Wikidata and, when present, MacTutor, the publication year as
  `datePublished`, the original `inLanguage`, the page `url`, the source scan as `isBasedOn` when
  present, and a CC0 `license` for our edition

#### Scenario: Structured data for an author

- **WHEN** an author page renders
- **THEN** its `<head>` carries one `application/ld+json` block describing a `Person` with the
  author's name, `sameAs` links (Wikidata and MacTutor when present), and `birthDate` / `deathDate`
  when those years are known
- **AND** fields whose source data is absent are omitted rather than emitted empty

#### Scenario: JSON-LD is well-formed and reflects the page

- **WHEN** any page that supplies structured data is built
- **THEN** the emitted `application/ld+json` is valid JSON in a single script element
- **AND** its values match the visible page (author names, publication year, language)
