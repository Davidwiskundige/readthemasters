// Differential harness for the fitDisplayMath batching change (backlog #19, fix 1).
//
// Paste into the browser console on a long work page — e.g.
//   https://readthemasters.org/works/abel-1841-fonctions-transcendantes/
// It defines both implementations, runs each over the SAME DOM in the same page
// load, and reports (a) the time each takes and (b) whether they assign identical
// `wide` / `tag-below` classes to every display equation.
//
// Running both against one DOM is the point: it removes machine, network, build,
// and page-load variance from the comparison, so the only difference is the code.
//
// NOTE: at narrow viewports the OLD implementation can block the main thread for
// minutes on the Abel page, which starves the console itself. Kick it off via
// setTimeout and poll `window.__oldDone` rather than awaiting it inline.

(() => {
  // ---- OLD: verbatim from site/src/pages/works/[id].astro before this change ----
  function fitOld(root) {
    root.querySelectorAll('.katex-display').forEach((eq) => {
      const room = eq.clientWidth;
      if (!room) return;
      const html = eq.querySelector('.katex-html');
      if (!html) return;
      const tag = html.querySelector(':scope > .tag');
      eq.classList.remove('wide', 'tag-below');
      const math = [...html.children]
        .filter((c) => c !== tag)
        .reduce((w, c) => w + c.getBoundingClientRect().width, 0);
      if (math > room) eq.classList.add('wide');
      const tagW = tag ? tag.getBoundingClientRect().width + 8 : 0;
      if (tag && math + 2 * tagW > room) eq.classList.add('tag-below');
    });
  }

  // ---- pure decision helper — mirrors site/src/lib/fitmath.js ----
  function decideFit(room, math, tagWidth) {
    const tagW = tagWidth === null ? 0 : tagWidth + 8;
    return { wide: math > room, tagBelow: tagWidth !== null && math + 2 * tagW > room };
  }

  // ---- NEW: four batched phases (read / write / read / write) ----
  function fitNew(root) {
    const recs = [];
    for (const eq of root.querySelectorAll('.katex-display')) {        // A: reads
      const room = eq.clientWidth;
      if (!room) continue;
      const html = eq.querySelector('.katex-html');
      if (!html) continue;
      recs.push({ eq, html, tag: html.querySelector(':scope > .tag'), room });
    }
    for (const r of recs) r.eq.classList.remove('wide', 'tag-below');  // B: writes
    for (const r of recs) {                                            // C: reads
      let math = 0;
      for (const c of r.html.children) if (c !== r.tag) math += c.getBoundingClientRect().width;
      r.math = math;
      r.tagWidth = r.tag ? r.tag.getBoundingClientRect().width : null;
    }
    for (const r of recs) {                                            // D: writes
      const d = decideFit(r.room, r.math, r.tagWidth);
      if (d.wide) r.eq.classList.add('wide');
      if (d.tagBelow) r.eq.classList.add('tag-below');
    }
  }

  const all = () => [...document.querySelectorAll('.katex-display')];
  const snapshot = () => all().map((e) =>
    (e.classList.contains('wide') ? 'w' : '') + (e.classList.contains('tag-below') ? 't' : '')).join('|');
  const reset = () => {
    all().forEach((e) => e.classList.remove('wide', 'tag-below'));
    void document.body.offsetHeight; // settle layout so both runs start from the same state
  };
  const time = (fn) => { reset(); const t = performance.now(); fn(document); return performance.now() - t; };

  const compare = (a, b) => {
    const p = a.split('|'), q = b.split('|');
    const diffs = p.map((v, i) => (v === q[i] ? null : i)).filter((i) => i !== null);
    return {
      identical: a === b,
      mismatchCount: diffs.length,
      mismatchIndices: diffs.slice(0, 10),
      wide: p.filter((x) => x.includes('w')).length,
      tagBelow: p.filter((x) => x.includes('t')).length,
    };
  };

  window.__fitExp = { fitOld, fitNew, decideFit, snapshot, reset, time, compare, all };
  return 'harness ready — window.__fitExp';
})();

// ---- usage ----------------------------------------------------------------
// Fast side first:
//   const E = window.__fitExp;
//   const ms = E.time(E.fitNew); window.__snapNew = E.snapshot(); ms
//
// Slow side, async so it cannot starve the console call that reads it:
//   window.__oldDone = null;
//   setTimeout(() => { const t = E.time(E.fitOld); window.__snapOld = E.snapshot(); window.__oldDone = Math.round(t); }, 0);
//   // ...poll until non-null:
//   window.__oldDone
//
// Verdict:
//   E.compare(window.__snapOld, window.__snapNew)
//
// Page-load cost, for the DOMContentLoaded figure:
//   const n = performance.getEntriesByType('navigation')[0];
//   Math.round(n.domContentLoadedEventEnd - n.domInteractive)
