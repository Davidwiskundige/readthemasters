# Tasks: seo-metadata

## Shared head (Base.astro)

- [x] Emit `<link rel="canonical" href={new URL(Astro.url.pathname, Astro.site)}>` on every page.
- [x] Emit OpenGraph tags from the existing `title` / `description`: `og:site_name` (`ReadTheMasters`),
      `og:type` (from a new optional `ogType` prop, default `website`), `og:title`, `og:description`,
      `og:url` (canonical). Guard `og:description` on `description` being set.
- [x] Emit `twitter:card` = `summary`.
- [x] Add an optional `jsonLd` prop; when present, render
      `<script type="application/ld+json" set:html={JSON.stringify(jsonLd)} />`. Accept an object or
      an array of objects.

## Structured-data builder

- [x] `site/src/lib/jsonld.js` — pure functions that map build data to schema.org objects:
      `workJsonLd(work, siteOrigin)`, `authorJsonLd(author, siteOrigin)`, `websiteJsonLd(siteOrigin)`.
- [x] Work → `CreativeWork` subtype by `type` (`paper`→`ScholarlyArticle`, `book`→`Book`, else
      `CreativeWork`); `name`, `alternativeName` (English title), `author[]` as `Person` with `sameAs`
      (Wikidata `https://www.wikidata.org/wiki/<qid>` + MacTutor URL when present), `datePublished`
      (year), `inLanguage`, `url`, `isBasedOn` (source URL when present), `license` CC0.
- [x] Author → `Person`: `name`, `sameAs` (Wikidata + MacTutor), `birthDate`/`deathDate` (years when
      known), `url`. Omit fields that are absent rather than emitting empty values.
- [x] Home → `WebSite` with `name` + `url`.

## Wire pages

- [x] `works/[id].astro` — build the work object, pass `jsonLd` and `ogType="article"` to `Base`.
- [x] `authors/[slug].astro` — pass `jsonLd` (Person) and `ogType="profile"`.
- [x] `index.astro` — pass `jsonLd` (WebSite); other pages inherit the `website` default.

## Verification

The site has no JS unit-test harness — pure libs (`bibtex.js`, `tex.js`) are verified through the
build/preview, so `jsonld.js` follows the same house convention rather than adding a lone runner.

- [x] Astro build + preview, checking each page type in the rendered `<head>`:
  - work page — canonical link, OG (`article`) + Twitter tags, and one `application/ld+json` that
    parses to a `ScholarlyArticle` with the right authors (`sameAs` → Wikidata + MacTutor), year,
    language, `isBasedOn` scan URL, and CC0 license. ✓ (Fagnano + Leibniz)
  - author page — canonical, OG (`profile`), and a `Person` with `sameAs` + birth/death years;
    absent fields omitted. ✓
  - home — canonical, OG (`website`), and a `WebSite` object. ✓
  - production `astro build` compiles all 12 pages and emits `sitemap-index.xml`. ✓

## Ship

- [x] Fold the delta into `openspec/specs/site-catalog`; update `project.md`; archive the change.
- [x] Mark PLAN.md §9 backlog #5 as delivered.
