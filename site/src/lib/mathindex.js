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
const SCANNER = /\\origpage\{(\d+)\}|\\\[([\s\S]*?)\\\]|(?<!\\)\$((?:\\.|[^$])*?)\$/g;

export function extractFormulas(tex) {
  if (!tex) return [];
  const body = documentBody(tex);
  const out = [];
  let page = null;
  let m;
  SCANNER.lastIndex = 0;
  while ((m = SCANNER.exec(body))) {
    if (m[1] !== undefined) { page = Number(m[1]); continue; }
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
