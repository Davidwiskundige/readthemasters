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

// Inline text niceties shared by paragraphs and figure captions.
function inlineText(html) {
  return html
    .replace(/\\uncertain\{([^}]*)\}/g, '<span class="uncertain">$1</span>')
    .replace(/\\illegible\b/g, '<span class="uncertain">[illegible]</span>')
    .replace(/\\(?:emph|textit)\{([^}]*)\}/g, "<em>$1</em>")
    .replace(/\\textbf\{([^}]*)\}/g, "<strong>$1</strong>")
    .replace(/---/g, "—")
    .replace(/``/g, "“").replace(/''/g, "”")
    .replace(/~/g, " ");
}

const RMFIGURE = /^\\rmfigure\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}\s*$/;

export function texToHtml(tex, opts = {}) {
  if (!tex) return "";
  const figureBase = opts.figureBase || "";
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
      const caption = inlineText(escapeHtml(fig[2]));
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
      heading = `<h2>${escapeHtml(sec[1])}</h2>`;
      para = sec[2].trim();
      if (!para) { out.push(heading); continue; }
    } else if (sub) {
      heading = `<h3>${escapeHtml(sub[1])}</h3>`;
      para = sub[2].trim();
      if (!para) { out.push(heading); continue; }
    }

    const html = inlineText(escapeHtml(para))
      .replace(/\\origpage\{(\d+)\}/g, (_, n) => `<span class="origpage" id="p-${n}">page ${n}</span>`);

    out.push(`${heading}<p>${html}</p>`);
  }
  return out.join("\n");
}
