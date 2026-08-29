// The editorial `significance` note from work.yaml, rendered to HTML.
//
// The field is plain prose plus inline math: everything is HTML-escaped, and only two bracket
// markers are structural.
//
//   [n]      — a citation marker, resolved against `significance_sources[n-1]`. Renders as a small
//              superscript number; the full citation (linked, when the source carries a url) is
//              revealed in a popover.
//   [note n] — an aside marker, resolved against `significance_notes[n-1]`. Renders as an inline
//              chip carrying the note's own label; the note's prose is revealed in a popover. It
//              exists so a technical excursus — the modern restatement of a theorem, say — sits one
//              hover away from the paragraph instead of swallowing it.
//
// Both build on the shared `.pop` apparatus (scripts/pop.js, styles in global.css) and are marked
// data-pagefind-ignore, like every other popover: hidden apparatus text would otherwise surface in
// search excerpts with nothing around it. Math inside either marker is left alone here — the work
// page's KaTeX pass typesets the whole `.significance` region, popovers included. A marker that
// resolves to nothing is left as the literal text the author wrote, never dropped.

const esc = (s) => String(s ?? "")
  .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

export function renderSignificance(text, sources = [], notes = []) {
  if (!text) return "";
  return esc(text)
    .replace(/\[note (\d+)\]/g, (m, n) => {
      const note = notes?.[Number(n) - 1];
      if (!note) return m;
      const label = esc(note.label);
      return `<span class="pop signote" data-pagefind-ignore>` +
             `<button type="button" class="pop-marker" aria-label="Note: ${label}">${label}</button>` +
             `<span class="pop-content" role="note">${esc(note.text)}</span></span>`;
    })
    .replace(/\[(\d+)\]/g, (m, n) => {
      const src = sources?.[Number(n) - 1];
      if (!src) return m;
      const cite = esc(src.citation);
      const inner = src.url ? `<a href="${esc(src.url)}" rel="noopener">${cite}</a>` : cite;
      return `<span class="pop cite" data-pagefind-ignore>` +
             `<button type="button" class="pop-marker" aria-label="Citation ${n}">${n}</button>` +
             `<span class="pop-content" role="note">${inner}</span></span>`;
    });
}
