# Change: seo-metadata

## Why

PLAN.md §9 backlog #5. That item bundled four things under "Accessibility & SEO for math"; two
already ship and this change delivers the remaining two:

- **Already done — screen-reader MathML.** KaTeX's default `htmlAndMathml` output already emits a
  real `<math>` element beside every formula, with the visual layer marked `aria-hidden="true"`.
  Verified in the rendered page: all formulas carry MathML. No work needed.
- **Already done — sitemap.** `@astrojs/sitemap` is wired in `astro.config.mjs` and `robots.txt`
  already points crawlers at `/sitemap-index.xml`.
- **Missing — page metadata.** The shared `<head>` (`site/src/layouts/Base.astro`) emits only
  `title`, `description`, and a favicon. There is no `schema.org` structured data, no OpenGraph or
  Twitter Card tags, and no canonical link — even though `site:` is configured. So link previews are
  bare, search engines get no structured signal about author/work/date, and pages advertise no
  canonical URL.

This change fills that page-metadata gap. It is pure discoverability plumbing: no reader-facing UI
changes, no corpus-format change, and it draws entirely on metadata the build data already carries
(authors with Wikidata/MacTutor ids and dates, publication year and venue, language, discipline,
type). It closes backlog #5.

## What changes

- **Canonical links, site-wide.** `Base.astro` emits `<link rel="canonical">` for every page,
  derived from `Astro.site` + the current path. Single source of truth; no per-page wiring.
- **OpenGraph + Twitter Card tags, site-wide.** `Base.astro` emits `og:site_name`, `og:type`,
  `og:title`, `og:description`, `og:url`, and `twitter:card` (`summary`) from the `title` /
  `description` each page already passes. `og:type` defaults to `website` and is overridable per
  page: `article` for a work, `profile` for an author.
- **schema.org JSON-LD, per page type.** `Base.astro` gains an optional `jsonLd` prop that it
  serializes into a `<script type="application/ld+json">`. Each page type supplies the right object:
  - **Work page** → a `CreativeWork` subtype chosen from the work's `type` (`paper` →
    `ScholarlyArticle`, `book` → `Book`, else `CreativeWork`): `name` (original title, with
    `alternativeName` for the English title), `author` as `Person` objects carrying `sameAs`
    (Wikidata + MacTutor URLs), `datePublished` (year), `inLanguage`, `url`, `isBasedOn` (the source
    scan URL when present), and `license` `https://creativecommons.org/publicdomain/zero/1.0/` for
    our edition.
  - **Author page** → a `Person`: `name`, `sameAs` (Wikidata + MacTutor), `birthDate` / `deathDate`
    (years, when known), and `url`.
  - **Home / catalog** → a `WebSite` object with `name` and `url`.
- **No new assets and no OG images (yet).** Only an SVG logo exists, and per-work OG images are a
  separate, heavier lift (build-time image generation). Cards render fine as `summary` without an
  image; a default/​per-work `og:image` is called out as an optional follow-up, not built here.

## Impact

- Extends **site-catalog**: a new "SEO & structured metadata" requirement covering the shared head.
  No change to the copyright gate and **no change to `corpus-format`** — every value is derived from
  data already in `works.json`.
- Touches `site/src/layouts/Base.astro` (canonical + OG/Twitter + `jsonLd` serialization),
  `site/src/pages/works/[id].astro`, `site/src/pages/authors/[slug].astro`, and
  `site/src/pages/index.astro` (each builds its `jsonLd` object and passes `ogType`), and adds a
  small builder helper (e.g. `site/src/lib/jsonld.js`) with unit tests.
- Purely additive to the page `<head>`; no visible layout, no behavior change for readers.
