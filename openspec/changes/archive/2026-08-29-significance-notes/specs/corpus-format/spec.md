## MODIFIED Requirements

### Requirement: work.yaml schema

`work.yaml` MUST provide the required fields: `id` (equals directory name, unique across corpus),
`title`, `authors` (≥1, each `name` + `wikidata_id` + `death_year` or `anonymous`, plus optional
`birth_year` and the optional author display fields below), `publication` (`year`, `venue` ∈ vocab;
optional `volume`, `month`, `pages`, `title_full`), `edition` (`year`, `is_transcribed_edition`,
`rights_cleared`, `rights_note`), `discipline` (a vocab key or a list of them, for works that
straddle fields such as `[mathematics, physics]`), `language` ∈ vocab, `type` ∈ vocab,
`source` (`scan_url`, `scan_id`), `sources` (citations for `death_date`, `publication_date`,
`edition`).

Optional: `title_en`, `title_tex` / `title_en_tex` (LaTeX renderings of the title / English title
for on-page display, carrying inline `$…$` math — the plain `title` / `title_en` stay canonical for
the browser tab, search index, and structured data), `tags` (each ∈ vocab), `significance` (a short
editorial paragraph on the work's historical importance — our commentary, distinct from the
transcription; does not affect the gate) with optional `significance_sources` (a list of
`{citation, url?}` backing its claims) and optional `significance_notes` (a list of
`{label, text}` asides — see below), `external_translations` (list of referenced
translations elsewhere: `language`, `title`, `translator`, `year`, `license`, `venue`,
`url`, `note`), `relations` (dependency edges to earlier works — see below), `copyright_assessment`
(written/verified by the gate).

Optional author display fields (used by the author pages — see site-catalog; backward compatible):
`bio` (a short one-line biographical descriptor), `mactutor` (a MacTutor/St Andrews biography path
id, e.g. `Leibniz`, or a full URL — the site always links this biography when present), and
`portrait` (`{file, credit, alt, source}`). The portrait `file` is a small public-domain image
**committed under `corpus/authors/<slug>/`** and **hosted by the site** — like the figure crops of
§4.5, and unlike full scans, which are never rehosted (PLAN.md §3, §4.5). `alt` is the accessibility
text; optional `credit` is a short artist attribution shown as a caption (e.g. "Portrait by Bernhard
Christoph Francke (c. 1700)"); optional `source` is the image's provenance URL (e.g. its Wikimedia
Commons file page) that the portrait links to when clicked. When the same author (same
`wikidata_id`) appears in multiple works, `birth_year`/`death_year` must agree across them;
`pipeline/validate.py` warns on a mismatch.

**Significance markup.** The `significance` text is plain prose plus inline `$…$` math, carrying two
kinds of positional marker, each addressing an optional list by position (1-based, in list order):

- `[n]` → `significance_sources[n-1]`, a `{citation, url?}` reference backing a claim.
- `[note n]` → `significance_notes[n-1]`, a `{label, text}` **aside**: an excursus — a restatement
  of the author's result in modern notation, say — that would otherwise swamp the paragraph
  (HOUSESTYLE R26). `label` is short, because the site renders it as the visible marker inside the
  running prose; `text` is one paragraph under the same plain-text-plus-KaTeX rules as the
  significance itself. Both render as popovers — see site-catalog.

The gate checks the correspondence in both directions: a marker addressing an entry that does not
exist fails the build (it would print as literal `[3]` on the page), and an entry no marker
addresses warns (it would render nowhere). Adding or removing an entry means renumbering the
markers that follow it.

**Dependency relations.** The optional `relations` list records directed dependency edges from
**this** work to **earlier** corpus works, so the corpus forms a dependency graph (surfaced as
per-work "Related reading" and the timeline — see site-catalog). Each edge is a mapping:

- `to` (required) — the id of another corpus work; must exist and be same-year-or-earlier.
- `kind` (required) — a `relation_kinds` vocab key: `cites` (the transcribed text references that
  work) or `builds-on` (a curated conceptual dependency, editorial like `significance`).
- `recommended` (optional) — `true` or `primary`; at most one edge per work carries it, marking the
  reader's **recommended previous read**. `primary` additionally makes the target list this work
  first among its "recommended next" reads (ties fall back to chronological order).
- `note` (optional) — a short editorial gloss on the edge (plain text + inline KaTeX).
- `sources` (optional) — `{citation, url?}` references, shown via the shared `.pop` popover.

Edges are authored backward in time so adding a new work never requires editing an older one; the
build computes the inverse ("cited by" / "recommended next"). The gate validates, across the whole
corpus, that every `to` resolves, `to ≠ self`, `year(to) ≤ year(self)`, `kind` ∈ vocab,
`recommended` ∈ {true, primary} with at most one per work, and that the graph is acyclic (a DAG).

**Canonical work identity.** `id` prefers a stable external identifier: Wikidata QID → DOI →
deterministic `author-year-shorttitle` slug. It is the directory name and the permanent URL.

**Publication citation.** `volume`, `month` and `pages` are the structured issue locators; all are
optional. The site composes them with the venue's display name into a single human-readable citation
string (`venue_full`, built in `build_site_data.py` and shown on the work page and catalog card):
`<venue>, vol. <volume>, p./pp. <pages>`. A journal issued monthly rather than by volume — e.g.
the *Acta Eruditorum*, cited by month — records `month` instead of `volume`; month fills the
same slot when no `volume` is given (`Acta Eruditorum, April`). `p.` is used for a single page,
`pp.` for a range or list. The year is shown separately, so it is not repeated in `venue_full`.

#### Scenario: Missing required field fails the gate

- **WHEN** a `work.yaml` omits a required field such as `publication.venue` or `sources.publication_date`
- **THEN** `pipeline/validate.py` fails the work

#### Scenario: Relation edge must point backward to an existing work

- **WHEN** a `relations` edge has `to` resolving to a work with `year(to) ≤ year(self)`, `to ≠ self`, and a `kind` in vocab, keeping the graph acyclic
- **THEN** the edge validates; otherwise the gate fails

#### Scenario: At most one recommended edge per work

- **WHEN** more than one `relations` edge on a work is marked `recommended`
- **THEN** the gate fails

#### Scenario: A significance marker with no entry behind it fails the gate

- **WHEN** a `significance` text carries a `[note 2]` or `[3]` marker with no matching `significance_notes` / `significance_sources` entry
- **THEN** `pipeline/validate.py` fails the work, naming the marker

#### Scenario: An aside needs a label and a text

- **WHEN** a `significance_notes` entry omits `label` or `text`, or is not a mapping
- **THEN** the gate fails; an over-long label, or an entry no marker references, warns

### Requirement: LaTeX house style

Every `.tex` SHALL use `corpus/preamble/readmasters.sty`. Content and notation stay faithful to the
original; typography is normalized; markup is standardized. Apparatus macros: `\origpage{n}`,
`\uncertain{}`, `\illegible`, `\ednote{}`, `\rmfigure{file}{caption}{alt}` (figures are crops from
the scan, not redrawn).

The house style distinguishes faithful **notation** (which symbols/formula, the author's notation —
kept exactly) from house-style **presentation** (how the same math is set — made consistent).
Math-typography conventions and the **rulings log** of boundary decisions live in
`corpus/HOUSESTYLE.md`. Current conventions include: multi-letter geometric labels stay plain
math letters (no `\pt`/`\mathit`); any inline large operator (∫, ∑, ∏) uses `\displaystyle`
whatever its operand looks like — including the author's own `:`/`/` division sign, which stays
faithful; equation numbers go on the right via `\tag{n}` with the author's own numbers; author
notation and printer's errors are kept faithfully (`zz` for z², archaic spelling, `arc.`) and
flagged for review, never silently corrected.

The argument of an apparatus note — `\ednote{...}` or `\uncertain{...}` — SHALL contain no
text-mode brace group. Inline math (`$...$`) inside such a note IS permitted and MUST keep
rendering. This is not a stylistic preference but a rendering constraint: `site/src/lib/tex.js`
matches both macros with `[^}]*`, so a nested `\emph{...}` ends the note at the first `}` and its
tail — including the literal brace — leaks into the author's running text, while math survives
because the transform stashes `$...$` spans before that match runs (ruling R18).

Presentation conventions that are unambiguous from the source text are **mechanically enforced** by
`pipeline/houselint.py`, which `pipeline/validate.py` runs as part of the gate — so a regression
fails CI and cannot merge. It enforces rulings R2/R16 (an inline large operator `\int`/`\sum`/`\prod`
must carry `\displaystyle`, and use `\frac` not `\dfrac` under it) and the apparatus-note brace rule
above (R18), over the transcription, every translation, **the `significance` note in `work.yaml`
and each of its `significance_notes` asides** (which render inline math through KaTeX like the
`.tex` panels). The linter is a rule registry so further machine-checkable rulings extend it; each rule declares whether it applies to inline math
spans or to the document as a whole, since a text-mode ruling cannot be expressed as a predicate
over a math span. Judgement-based rulings (faithful vs. normalized notation, translation wording)
are never linted. Separately, the reader's LaTeX→HTML transform (`site/src/lib/tex.js`) resolves
text niceties — em-dashes, `~`, `\&`, and LaTeX control spaces `\ ` (ruling R17) — and is covered by
`site/src/lib/tex.test.mjs` (`npm test`, run in CI).

#### Scenario: Machine-checkable ruling regression fails CI

- **WHEN** a `.tex` (or the `significance` note) violates a mechanically-enforced ruling such as R2/R16
- **THEN** `pipeline/houselint.py` (run by the gate) fails the build

#### Scenario: Judgement-based rulings are not linted

- **WHEN** a decision is judgement-based (faithful vs. normalized notation, translation wording)
- **THEN** the linter does not flag it

#### Scenario: Text-mode markup inside an apparatus note fails the gate

- **WHEN** a `.tex` contains `\ednote{...\emph{word}...}` or the same nesting inside `\uncertain{}`
- **THEN** `pipeline/houselint.py` reports a violation naming the file, line, and macro, and the gate fails

#### Scenario: Math inside an apparatus note is accepted

- **WHEN** a note's argument contains inline math with braces, such as `\ednote{printed $\sqrt{X}$ here}`
- **THEN** the linter reports no violation, because the site renders that note correctly

#### Scenario: An unterminated apparatus note is reported

- **WHEN** a `\ednote{` or `\uncertain{` argument has no matching closing brace
- **THEN** the linter reports a violation rather than scanning to end of file

#### Scenario: A significance aside is linted like the significance itself

- **WHEN** a `significance_notes` entry's `text` violates a mechanically-enforced ruling such as R2/R16
- **THEN** `pipeline/houselint.py` (run by the gate) fails the build, naming the aside's index
