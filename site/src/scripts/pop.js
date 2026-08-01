// Inline popover markers (".pop"): hover or keyboard focus shows the content (CSS handles that
// via :hover / :focus-within); a click pins one open, which makes them usable on touch. JS keeps
// each popover positioned inside the viewport. Shared by significance citation markers and
// in-text editorial notes on work pages, and the Abel epigraph on the About page — anything with
// a ".pop" wrapper on any page. Loaded globally from Base.astro.
function initPops() {
  const allPops = () => document.querySelectorAll('.pop');
  function positionPop(wrap) {
    const pop = wrap.querySelector('.pop-content');
    if (!pop) return;
    pop.style.position = 'fixed';
    const pw = pop.offsetWidth, ph = pop.offsetHeight, m = 8;
    const r = (wrap.querySelector('.pop-marker') || wrap).getBoundingClientRect();
    let left = Math.min(Math.max(m, r.left), window.innerWidth - pw - m);
    left = Math.max(m, left);
    let top = r.bottom + 4;
    if (top + ph > window.innerHeight - m) top = Math.max(m, r.top - ph - 4);
    pop.style.left = left + "px";
    pop.style.top = top + "px";
  }
  const closeAllPops = () =>
    document.querySelectorAll('.pop.open').forEach((c) => c.classList.remove('open'));
  allPops().forEach((wrap) => {
    // Bind to the whole wrapper so the trigger is the entire hoverable/focusable region — the
    // citation number on work pages, or the full quote + attribution of the About epigraph.
    wrap.addEventListener('mouseenter', () => positionPop(wrap));
    wrap.addEventListener('focusin', () => positionPop(wrap));
    wrap.addEventListener('click', (e) => {
      // A click inside the open card (e.g. a citation link) must act, not toggle the card shut.
      if (e.target.closest('.pop-content')) return;
      e.stopPropagation();
      const wasOpen = wrap.classList.contains('open');
      closeAllPops();
      if (!wasOpen) { wrap.classList.add('open'); positionPop(wrap); }
    });
  });
  document.addEventListener('click', closeAllPops);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeAllPops(); });
  const repositionVisiblePops = () => allPops().forEach((wrap) => {
    const pop = wrap.querySelector('.pop-content');
    if (pop && getComputedStyle(pop).display !== 'none') positionPop(wrap);
  });
  window.addEventListener('scroll', repositionVisiblePops, { passive: true });
  window.addEventListener('resize', repositionVisiblePops);
}

initPops();
