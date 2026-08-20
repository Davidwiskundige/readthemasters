# math-search

## Purpose

Search the corpus for a formula, written as LaTeX. Normalization-based (Layer 1), never semantic.
Surfaced as the "Formulas" mode of `/search`, beside the Pagefind text search (`search`
capability). Established by the `math-search` change (archived 2026-07-23).

## Requirements

### Requirement: Canonical normalization (Layer 1 only)

A shared normalizer (`site/src/lib/mathnorm.js`) SHALL reduce a LaTeX formula to a canonical token
sequence by removing only variance that does not change the rendered output: whitespace and spacing
commands (`\,`, `~`, `\quad`, `\displaystyle`, …), delimiter-size wrappers (`\left`/`\right`,
`\big…`), render-identical command synonyms (`\dfrac`/`\tfrac`→`\frac`, `\geq`→`\ge`, `\lvert`→`|`,
…), equation apparatus (`\tag`, `\label`), and redundant single-token braces (`x^{2}`→`x^2`,
`\frac{a}{b}`→`\frac a b`).

It MUST NOT reorder terms, apply mathematical identities, or otherwise change meaning. Faithful
historic notation is preserved: `zz` does not become `z^2`, so the transcription's fidelity is not
second-guessed by the index. Semantic equivalence and any CAS are out of scope.

#### Scenario: Render-identical variance is collapsed

- **WHEN** two formulas differ only in spacing, delimiter sizes, synonym commands, or redundant braces
- **THEN** they normalize to the same canonical token sequence

#### Scenario: Faithful notation is not rewritten

- **WHEN** a formula contains historic notation such as `zz`
- **THEN** normalization leaves it as `zz` and does not turn it into `z^2`

### Requirement: Formula index

A build-time index (`/math-index.json`, from `site/src/pages/math-index.json.js`) SHALL enumerate
every inline (`$…$`) and display (`\[…\]`) formula in every published transcription and translation.
Each entry carries the raw LaTeX (for rendering), its normalized token sequence (for matching), the
work, the artifact it belongs to (original or a named translation), and the `\origpage` page it
appears under, so a result can deep-link to that page in the correct panel. The index is produced at
deploy time and never committed.

#### Scenario: Every published formula is indexed

- **WHEN** the site is built
- **THEN** each inline and display formula in every published artifact has an index entry carrying its raw LaTeX, normalized tokens, work, artifact, and page

### Requirement: Wildcard query matching

A query SHALL be a LaTeX fragment, normalized identically, in which `?` is a wildcard matching any
one unit — a single token or a whole `{…}` group. A formula matches when the normalized query occurs
as a contiguous run of its normalized tokens, so a sub-expression query (`a^4 - z^4`) finds the
larger formulas that contain it and `\sqrt{?}` finds every square root. Results are ranked full-match
first, then by how tightly the match covers the formula. The wildcard is the only accommodation for
"same maths, written differently"; the engine never reasons about equivalence.

#### Scenario: Sub-expression query matches containing formulas

- **WHEN** the query `a^4 - z^4` is run
- **THEN** formulas whose normalized tokens contain that contiguous run match, ranked full-match first

#### Scenario: Wildcard matches one unit

- **WHEN** the query is `\sqrt{?}`
- **THEN** every square root matches, the `?` standing for a single token or a whole `{…}` group

### Requirement: Formula search UI

`/search` SHALL offer a "Formulas" mode beside text search: a LaTeX input with a live KaTeX preview
of the query, KaTeX-rendered results each labelled with their work, artifact and page and linking to
that page in the reader. The mode and query live in the URL (`?mode=math&mq=…`) so a formula search
is shareable. When the index cannot be loaded (e.g. the dev server), the mode says so rather than
failing.

#### Scenario: Formula search is shareable via the URL

- **WHEN** a visitor runs a formula query
- **THEN** the mode and query are reflected as `?mode=math&mq=…` and reopening that URL re-runs the search

#### Scenario: Missing index degrades gracefully

- **WHEN** the formula index cannot be loaded
- **THEN** the Formulas mode reports this instead of failing
