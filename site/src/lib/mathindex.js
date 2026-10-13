// Pull every formula out of a transcription/translation, tagged with the page it sits under, so
// the formula-search index can point a hit at the exact page in the reader. Pairs with mathnorm.js
// (normalization + matching) and the /math-index.json endpoint (which assembles the corpus-wide
// index at build time).

import { normalize } from "./mathnorm.js";

function documentBody(tex) {
  const m = tex.match(/\\begin\{document\}([\s\S]*?)\\end\{document\}/);
  let body = m ? m[1] : tex;
  return body.replace(/^\s*%.*$/gm, ""); // drop comment lines (whole-line % only)
}

// Scan in source order for page markers and math spans; a formula's page is the last \origpage
// seen before it. Display: `\[ … \]`. Inline: `$ … $` (an escaped \$ is not a delimiter).
// A page is arabic (kept as a number) or front matter's lower-case roman (kept as printed, "iii").
const SCANNER = /\\origpage\{(\d+|[ivxlcdm]+)\}|\\\[([\s\S]*?)\\\]|(?<!\\)\$((?:\\.|[^$])*?)\$/g;

export function extractFormulas(tex) {
  if (!tex) return [];
  const body = documentBody(tex);
  const out = [];
  let page = null;
  let m;
  SCANNER.lastIndex = 0;
  while ((m = SCANNER.exec(body))) {
    if (m[1] !== undefined) { page = /^\d+$/.test(m[1]) ? Number(m[1]) : m[1]; continue; }
    const display = m[2] !== undefined;
    const raw = (display ? m[2] : m[3]).trim();
    if (!raw) continue;
    // The equation number is apparatus, not part of the formula: drop it from what we render,
    // and normalization drops it from the tokens too (so an inline render never sees \tag).
    const render = raw.replace(/\\tag\{[^}]*\}/g, "").trim();
    if (!render) continue;
    out.push({ page, display, tex: render, tokens: normalize(raw) });
  }
  return out;
}

// --- the corpus-wide index (/math-index.json) --------------------------------
//
// Compact on purpose. The first layout repeated each hit's URL, work title and "where" label on
// every one of ~120k entries; that metadata was three quarters of the file, which reached 27.6 MiB
// with Legendre's Exercices and broke the deploy (Cloudflare Pages serves files up to 25 MiB).
// Now each work's URL, title and artifact labels are stored once, and an entry is a small array:
//   [workIndex, artifactKey, page, tex, display (1/0), tokens]
// where artifactKey is "original" or a translation's language code. expandEntry() rebuilds the
// full record for the hits that are actually shown.

// Anchor a formula to the reader: `p-293` in the original, `en-p-293` in the English panel; when a
// formula sits before any \origpage marker, fall back to the panel itself (`original` / `en`).
function anchor(art, page) {
  const prefix = art === "original" ? "" : `${art}-`;
  return page != null ? `${prefix}p-${page}` : art;
}

export function buildIndex(works) {
  const index = { v: 2, works: [], entries: [] };
  for (const w of works ?? []) {
    const wi = index.works.length;
    const arts = { original: `Original (${w.language_label})` };
    const sources = [["original", w.original_tex]];
    for (const [lang, t] of Object.entries(w.translations ?? {})) {
      arts[lang] = `${t.label} translation`;
      sources.push([lang, t.tex]);
    }
    index.works.push({ url: w.url, title: w.title, arts });
    for (const [art, tex] of sources) {
      const seen = new Set();
      for (const f of extractFormulas(tex)) {
        if (!f.tokens.length) continue;
        const key = `${f.page} ${f.tokens.join(" ")}`;
        if (seen.has(key)) continue; // same formula, same place — index once
        seen.add(key);
        index.entries.push([wi, art, f.page, f.tex, f.display ? 1 : 0, f.tokens]);
      }
    }
  }
  return index;
}

export function expandEntry(index, e) {
  const [wi, art, page, tex, display, tokens] = e;
  const w = index.works[wi];
  return {
    url: `${w.url}#${anchor(art, page)}`,
    title: w.title,
    where: w.arts[art] + (page != null ? ` · page ${page}` : ""),
    tex,
    display: display === 1,
    tokens,
  };
}
