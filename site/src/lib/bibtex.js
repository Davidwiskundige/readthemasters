// Build BibTeX entries for a work from its metadata: the original publication, our
// transcription/edition, our translations, and any referenced external translations.
// Pure function of the work object (from works.json) so it runs at build time.

const TYPE_MAP = {
  paper: "article",
  book: "book",
  chapter: "incollection",
  letter: "misc",
  lecture: "article",
  manuscript: "unpublished",
};

// "Bernhard Riemann" -> "Riemann, Bernhard"; handles simple particles (van, de, von).
function surnameFirst(name) {
  const parts = (name || "").trim().split(/\s+/);
  if (parts.length < 2) return name || "";
  const particles = new Set(["van", "von", "de", "der", "den", "di", "del", "la", "le"]);
  let i = parts.length - 1;
  while (i > 1 && particles.has(parts[i - 1].toLowerCase())) i--;
  return `${parts.slice(i).join(" ")}, ${parts.slice(0, i).join(" ")}`;
}

function authorsBib(authors) {
  return (authors || []).map((a) => surnameFirst(a.name)).join(" and ") || "Anonymous";
}

// Strip diacritics so keys stay ASCII (Über -> Uber, Poincaré -> Poincare).
function deaccent(s) {
  return (s || "").normalize("NFD").replace(/[̀-ͯ]/g, "");
}

function baseKey(work) {
  const first = deaccent((work.authors?.[0]?.name || "anon").split(/\s+/).pop());
  const word = deaccent(work.title || "").replace(/[^A-Za-z0-9 ]/g, "").split(/\s+/)[0] || "";
  return `${first}${work.year || ""}${word}`.replace(/\s+/g, "");
}

function entry(type, key, fields) {
  const lines = Object.entries(fields)
    .filter(([, v]) => v != null && v !== "")
    .map(([k, v]) => `  ${k} = {${v}}`);
  return `@${type}{${key},\n${lines.join(",\n")}\n}`;
}

export function bibtexEntries(work, { base = "" } = {}) {
  const key = baseKey(work);
  const authors = authorsBib(work.authors);
  const workUrl = `${base}${work.url}`;
  const producedYear = (p) => (p?.produced || "").slice(0, 4) || work.year;
  const out = [];

  // 1. The original work — what most people cite.
  const type = TYPE_MAP[work.type] || "misc";
  const isArticle = type === "article";
  out.push({
    label: "Original work",
    kind: "original",
    key,
    text: entry(type, key, {
      author: authors,
      title: work.title,
      journal: isArticle ? work.venue_label : undefined,
      booktitle: type === "incollection" ? work.venue_label : undefined,
      volume: work.volume,
      pages: work.pages,
      year: work.year,
      url: work.source?.scan_url,
    }),
  });

  // 2. Our transcription / edition (for reproducibility).
  out.push({
    label: "This transcription (ReadTheMasters)",
    kind: "transcription",
    key: `${key}-rtm`,
    text: entry("misc", `${key}-rtm`, {
      author: authors,
      title: `${work.title} --- LaTeX transcription`,
      howpublished: `ReadTheMasters, \\url{${workUrl}}`,
      note: `AI transcription (${work.transcription_provenance?.model || "AI"}); ` +
            `status: ${work.status}. Original: ${work.venue_label || ""} ${work.year || ""}`.trim(),
      year: producedYear(work.transcription_provenance),
    }),
  });

  // 3. Our translations.
  for (const [lang, t] of Object.entries(work.translations || {})) {
    out.push({
      label: `${t.label} translation (ReadTheMasters)`,
      kind: "translation",
      lang,
      key: `${key}-${lang}`,
      text: entry("misc", `${key}-${lang}`, {
        author: authors,
        title: `${work.title_en || work.title} --- ${t.label} translation`,
        howpublished: `ReadTheMasters, \\url{${workUrl}}`,
        note: `${t.label} translation (AI, ${t.provenance?.model || "AI"}); status: ${t.provenance?.status}`,
        language: t.label,
        year: producedYear(t.provenance),
      }),
    });
  }

  // 4. Referenced external (open) translations.
  for (const x of work.external_translations || []) {
    const xkey = `${key}-${(x.translator || "trans").split(/\s+/).pop()}${x.year || ""}`;
    out.push({
      label: `${x.language?.toUpperCase() || ""} translation — ${x.translator || "external"} (${x.year || ""})`,
      kind: "external",
      key: xkey,
      text: entry("article", xkey, {
        author: authors,
        title: x.title || work.title,
        note: x.translator ? `Translated by ${x.translator}` : undefined,
        journal: x.venue,
        year: x.year,
        url: x.url,
      }),
    });
  }

  return out;
}
