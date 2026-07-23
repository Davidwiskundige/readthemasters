// Minimal LaTeX-body -> HTML transform for the reader (MVP).
// Strips the preamble/document wrapper, turns apparatus macros and a few common
// commands into HTML, and leaves inline math ($...$, \[...\]) untouched so KaTeX
// auto-render can handle it in the browser. This is intentionally small; a fuller
// LaTeX renderer is a later phase (see PLAN.md §9 backlog / site-catalog spec).

function escapeHtml(s) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// Classic footnote-symbol cycle (*, †, ‡, §, ¶, ‖; doubled beyond that) for \ednote markers.
const ED_SYMBOLS = ["*", "†", "‡", "§", "¶", "‖"];
function nextEdSymbol(ctx) {
  const i = ctx.ednoteCount++;
  return ED_SYMBOLS[i % ED_SYMBOLS.length].repeat(Math.floor(i / ED_SYMBOLS.length) + 1);
}

// Inline text niceties shared by paragraphs and figure captions. `ctx` threads a per-document
// ednote counter across calls (see texToHtml) so markers number in order of appearance.
function inlineText(html, ctx = { ednoteCount: 0 }) {
  return html
    .replace(/\\uncertain\{([^}]*)\}/g, '<span class="uncertain">$1</span>')
    .replace(/\\illegible\b/g, '<span class="uncertain">[illegible]</span>')
    // \ednote{...} — editorial remark, never part of the author's text (readmasters.sty renders
    // it as a LaTeX \footnote for the PDF). Here it's a popover: hidden until hover/click, marked
    // as ours by a muted footnote-style symbol rather than the author's own words (PLAN house style).
    .replace(/\\ednote\{([^}]*)\}/g, (_, note) => {
      const sym = nextEdSymbol(ctx);
      // data-pagefind-ignore: the marker symbol and the note are ours, not the author's text —
      // indexing them drops stray markers into search excerpts.
      return `<span class="pop ednote" data-pagefind-ignore><button type="button" class="pop-marker" aria-label="Editorial note">${sym}</button>` +
             `<span class="pop-content" role="note">Editorial note: ${note}</span></span>`;
    })
    .replace(/\\(?:emph|textit)\{([^}]*)\}/g, "<em>$1</em>")
    .replace(/\\textbf\{([^}]*)\}/g, "<strong>$1</strong>")
    .replace(/---/g, "—")
    .replace(/``/g, "“").replace(/''/g, "”")
    .replace(/~/g, " ");
}

const RMFIGURE = /^\\rmfigure\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}\s*$/;

// Math stays as LaTeX source in the HTML (KaTeX renders it in the browser), which means the
// search index would otherwise be full of `frac`, `cdot`, `sqrt` and excerpts would show TeX.
// Wrapping each span in data-pagefind-ignore keeps the markup out of the index; KaTeX still
// finds the delimiters inside the wrapper. Display math gets a block-level wrapper so the
// .katex-display measurement in the reader still sees the full column width.
function wrapMath(html) {
  return html
    .replace(/\\\[([\s\S]*?)\\\]/g,
      (_, m) => `<span class="mathblock" data-pagefind-ignore>\\[${m}\\]</span>`)
    .replace(/(?<!\\)\$((?:[^$\\]|\\.)*?)(?<!\\)\$/g,
      (_, m) => `<span class="math" data-pagefind-ignore>$${m}$</span>`);
}

export function texToHtml(tex, opts = {}) {
  if (!tex) return "";
  const figureBase = opts.figureBase || "";
  // Page anchors must be unique across the panels of one work page (original + translations),
  // so each panel prefixes them: `p-236` for the original, `en-p-236` for the English.
  const idPrefix = opts.idPrefix || "";
  const ctx = { ednoteCount: 0 }; // shared across the whole document, not per-paragraph
  let secCount = 0; // headings get ids so search sub-results and section links can address them
  let body = tex;

  // Keep only what is between \begin{document} and \end{document} if present.
  const m = body.match(/\\begin\{document\}([\s\S]*?)\\end\{document\}/);
  if (m) body = m[1];

  // Drop comment lines.
  body = body.replace(/^\s*%.*$/gm, "");

  // Promote block-level markers to their own paragraphs so they render even when they share a
  // source line/paragraph with surrounding text (e.g. \origpage{n} immediately before \section).
  body = body
    .replace(/\\subsection\*?\{[^}]*\}/g, (m) => `\n\n${m}\n\n`)
    .replace(/\\section\*?\{[^}]*\}/g, (m) => `\n\n${m}\n\n`)
    .replace(/\\rmfigure\{[^}]*\}\{[^}]*\}\{[^}]*\}/g, (m) => `\n\n${m}\n\n`)
    .replace(/\\origpage\{\d+\}/g, (m) => `\n\n${m}\n\n`);

  const paras = body.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean);
  const out = [];

  for (let para of paras) {
    // Figure: \rmfigure{path}{caption}{alt} — the crop from the scan (PLAN §4.5).
    const fig = para.match(RMFIGURE);
    if (fig) {
      const file = fig[1].split("/").pop();
      const src = `${figureBase}${file}`;
      const caption = wrapMath(inlineText(escapeHtml(fig[2]), ctx));
      const alt = escapeHtml(fig[3]).replace(/~/g, " ").replace(/"/g, "&quot;");
      out.push(
        `<figure class="rmfig"><img src="${src}" alt="${alt}" loading="lazy" />` +
        `<figcaption>${caption}</figcaption></figure>`
      );
      continue;
    }

    // Section / subsection headings.
    const sec = para.match(/^\\section\*?\{([^}]*)\}\s*([\s\S]*)$/);
    const sub = para.match(/^\\subsection\*?\{([^}]*)\}\s*([\s\S]*)$/);
    let heading = "";
    if (sec) {
      heading = `<h2 id="${idPrefix}sec-${++secCount}">${escapeHtml(sec[1])}</h2>`;
      para = sec[2].trim();
      if (!para) { out.push(heading); continue; }
    } else if (sub) {
      heading = `<h3 id="${idPrefix}sec-${++secCount}">${escapeHtml(sub[1])}</h3>`;
      para = sub[2].trim();
      if (!para) { out.push(heading); continue; }
    }

    const html = wrapMath(inlineText(escapeHtml(para), ctx))
      .replace(/\\origpage\{(\d+)\}/g,
        (_, n) => `<span class="origpage" id="${idPrefix}p-${n}">page ${n}</span>`);

    out.push(`${heading}<p>${html}</p>`);
  }
  return out.join("\n");
}
