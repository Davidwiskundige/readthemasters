# Spec (delta): math-search

## ADDED: Capability `math-search`

Search the corpus for a formula, written as LaTeX. Normalization-based (Layer 1), never semantic.

### Requirement: Canonical normalization (Layer 1 only)

A shared normalizer reduces a LaTeX formula to a canonical token sequence by removing only
variance that does not change the rendered output: whitespace and spacing commands (`\,`, `~`,
`\quad`, `\displaystyle`, …), delimiter-size wrappers (`\left`/`\right`, `\big…`), render-identical
command synonyms (`\dfrac`/`\tfrac`→`\frac`, `\geq`→`\ge`, `\lvert`→`|`, …), equation apparatus
(`\tag`, `\label`), and redundant single-token braces (`x^{2}`→`x^2`, `\frac{a}{b}`→`\frac a b`).

It MUST NOT reorder terms, apply mathematical identities, or otherwise change meaning. Faithful
historic notation is preserved: `zz` does not become `z^2`, so the transcription's fidelity is not
second-guessed by the index. Semantic equivalence and any CAS are out of scope.

### Requirement: Formula index

A build-time index enumerates every inline (`$…$`) and display (`\[…\]`) formula in every published
transcription and translation. Each entry carries the raw LaTeX (for rendering), its normalized
token sequence (for matching), the work, the artifact it belongs to (original or a named
translation), and the `\origpage` page it appears under, so a result can deep-link to that page in
the correct panel. The index is produced at deploy time and never committed.

### Requirement: Wildcard query matching

A query is a LaTeX fragment, normalized identically, in which `?` is a wildcard matching any one
unit — a single token or a whole `{…}` group. A formula matches when the normalized query occurs as
a contiguous run of its normalized tokens, so a sub-expression query (`a^4 - z^4`) finds the larger
formulas that contain it and `\sqrt{?}` finds every square root. Results are ranked full-match
first, then by how tightly the match covers the formula. The wildcard is the only accommodation for
"same maths, written differently"; the engine never reasons about equivalence.

### Requirement: Formula search UI

`/search` offers a "Formulas" mode beside text search: a LaTeX input with a live KaTeX preview of
the query, KaTeX-rendered results each labelled with their work, artifact and page and linking to
that page in the reader. The mode and query live in the URL (`?mode=math&mq=…`) so a formula search
is shareable. When the index cannot be loaded (e.g. the dev server), the mode says so rather than
failing.
