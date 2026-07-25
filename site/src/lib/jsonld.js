// Build schema.org JSON-LD objects from the site's build-time data (works.json).
// Pure functions: given a record and the site origin, return a plain object ready to
// JSON.stringify into a <script type="application/ld+json">. Absent source fields are
// omitted rather than emitted empty, so validators never see null/"" values.

const CC0 = "https://creativecommons.org/publicdomain/zero/1.0/";
const WIKIDATA = "https://www.wikidata.org/wiki/";
const MACTUTOR = "https://mathshistory.st-andrews.ac.uk/Biographies/";

// Absolute URL from a site origin + a path already rooted at "/". Origin may be "".
const abs = (origin, path) => (origin ? new URL(path, origin).href : path);

// Drop keys whose value is null/undefined/"" or an empty array, so the emitted object
// carries only fields we actually have. Applied shallowly — nested objects are built clean.
const compact = (obj) =>
  Object.fromEntries(
    Object.entries(obj).filter(
      ([, v]) => v != null && v !== "" && !(Array.isArray(v) && v.length === 0),
    ),
  );

// schema.org type for a work, from the corpus `type` vocabulary.
const workType = (type) =>
  type === "paper" ? "ScholarlyArticle" : type === "book" ? "Book" : "CreativeWork";

// sameAs links for an author, from whichever identifiers are present. Author records on a
// work carry a raw MacTutor id (`mactutor`); author-index records carry a full `mactutor_url`.
function authorSameAs(a) {
  const links = [];
  if (a.wikidata_id) links.push(WIKIDATA + a.wikidata_id);
  if (a.mactutor_url) links.push(a.mactutor_url);
  else if (a.mactutor) links.push(`${MACTUTOR}${a.mactutor}/`);
  return links;
}

// A `Person` object for an author (embedded on a work, or standalone on an author page).
export function personJsonLd(a, origin = "") {
  return compact({
    "@type": "Person",
    name: a.name,
    url: a.url ? abs(origin, a.url) : undefined,
    sameAs: authorSameAs(a),
    birthDate: a.birth_year ? String(a.birth_year) : undefined,
    deathDate: a.death_year ? String(a.death_year) : undefined,
  });
}

// Top-level `Person` for an author page: same as personJsonLd but stamped with @context.
export function authorJsonLd(author, origin = "") {
  return { "@context": "https://schema.org", ...personJsonLd(author, origin) };
}

// A `CreativeWork`/`ScholarlyArticle`/`Book` for a work page.
export function workJsonLd(work, origin = "") {
  return compact({
    "@context": "https://schema.org",
    "@type": workType(work.type),
    name: work.title,
    alternativeName: work.title_en && work.title_en !== work.title ? work.title_en : undefined,
    author: (work.authors ?? []).map((a) => personJsonLd(a, origin)),
    datePublished: work.year ? String(work.year) : undefined,
    inLanguage: work.language || undefined,
    url: work.url ? abs(origin, work.url) : undefined,
    isBasedOn: work.source?.scan_url || undefined,
    license: CC0,
  });
}

// A `WebSite` for the catalog home.
export function websiteJsonLd(origin = "") {
  return compact({
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "ReadTheMasters",
    url: origin || undefined,
  });
}
