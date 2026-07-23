# Change: math-search

## Why

Full-text search (`search` capability) deliberately excludes mathematics — the reader carries
formulas as LaTeX and KaTeX renders them, so indexing them as text is noise. But "where does
Fagnano write $\sqrt{a^4 - z^4}$?" is exactly the query a corpus of historic mathematics should
answer. This change adds formula search.

The hard part, as discussed, splits in two:

- **Layer 1 — same rendered output, different source:** `x^2` vs `x^{2}`, `\frac` vs `\dfrac`,
  `\left(` vs `(`, spacing (`\,`, `~`), redundant braces. A *normalization* problem, solvable.
- **Layer 2 — same mathematics, different expression:** `zz` vs `z^2`, `(x+1)^2` vs `x^2+2x+1`,
  commutativity. Equivalence, undecidable in general, and — critically — at odds with this
  corpus's faithful-transcription mission (§4.4): normalizing `zz` to `z^2` is exactly the
  modernization we promised not to do.

So this change does **Layer 1 only, and explicitly no CAS / no semantic equivalence.** The user's
tool for Layer-2-style variance is a **wildcard** (`?`), matching any one sub-expression — the same
lever MathWebSearch uses. Variable renaming, "sqrt of something", an unknown exponent: all
expressible as `?` without the engine ever reasoning about mathematical meaning.

## What changes

- **A canonical normalizer** (`site/src/lib/mathnorm.js`, pure JS, shared by the build and the
  browser): tokenize TeX, drop spacing/layout commands (`\,`, `\displaystyle`, `\left`/`\right`),
  rename render-identical synonyms (`\dfrac`→`\frac`, `\geq`→`\ge`), strip `\tag`/`\label`, and
  collapse single-token braces (`x^{2}`→`x^2`) to a fixed point. No reordering, no simplification —
  it only removes cosmetic variance, so faithful notation survives (`zz` stays `zz`).
- **A build-time formula index** (`/math-index.json`): every `$…$` and `\[…\]` in every published
  transcription and translation, tagged with the work, artifact, and the `\origpage` it sits under,
  stored as `{ raw tex for display, normalized tokens for matching, deep-link }`.
- **Wildcard matching:** a query is normalized the same way; `?` becomes a wildcard that consumes
  one unit — a single token or a whole `{…}` group. A formula matches when the query occurs as a
  contiguous run (so sub-expression queries work), ranked full-match-first then by tightness.
- **A "Formulas" mode on `/search`,** beside the existing text search: a TeX input with a live
  KaTeX preview of what you typed, results rendered with KaTeX and deep-linked to the page the
  formula appears on. `?mode=math` + `?mq=` make a formula search shareable.

## Impact

- New capability `math-search`. No corpus, schema, or gate change.
- New: `site/src/lib/mathnorm.js`, `site/src/lib/mathindex.js`,
  `site/src/pages/math-index.json.js`. Touches `site/src/pages/search.astro` and
  `site/src/styles/global.css`.
- Explicitly out of scope (may become a later change): semantic/CAS equivalence, structural
  fuzzy ranking (Tangent-style symbol pairs), searching for a formula by its rendered image.
