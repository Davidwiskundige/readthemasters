# corpus-format

## Purpose

Current source of truth for how a work is stored. Established by the `corpus-format` change
(archived 2026-07-18) and extended by `site-catalog`.

## Requirements

### Requirement: Work directory layout

Each work SHALL live in `corpus/<id>/`, where `<id>` is the canonical work id.

- `work.yaml` (required) — metadata + copyright assessment.
- `provenance.yaml` (required) — per-artifact status/model/effort/reviewers.
- `original.tex` (required once transcribed) — faithful transcription, original language.
- `translations/<lang>.tex` — one file per hosted translation language.
- `figures/` (optional) — figure crops taken from the public-domain scan.
- `pdf/<name>.pdf` (optional) — pre-made PDF override (see site-catalog PDF build).

#### Scenario: Work stored under its canonical id

- **WHEN** a work with canonical id `<id>` is added
- **THEN** it lives in `corpus/<id>/` with `work.yaml` and `provenance.yaml` present (and `original.tex` once transcribed)

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
`{citation, url?}` backing its claims; the significance text may carry inline `[n]` markers
referencing them, rendered as clickable citation superscripts), `external_translations` (list of
referenced translations elsewhere: `language`, `title`, `translator`, `year`, `license`, `venue`,
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

### Requirement: provenance.yaml schema

`provenance.yaml` MUST use the keys `transcription` and `translations.<lang>`, each an artifact
record: `status` (`ai-draft|skimmed|verified`), `model` (required), `effort` (optional,
provider-agnostic or null), `prompt_version` (required), optional `submitted_via`, `produced`,
`reviewers` (list of `{name, level, date}`), and for translations a `source`
(`transcription` | `external-open` + `license`).

An optional top-level `changelog` records how the work has changed over time — a human-authored
list of `{date, summary}` entries (ISO `date`, short non-empty `summary`), the source of the work
page's revision history. When present, `validate.py` checks it is a list and that every entry has an
ISO date and a non-empty summary.

#### Scenario: Artifact record requires model and prompt_version

- **WHEN** an artifact record omits `model` or `prompt_version`
- **THEN** the gate fails

#### Scenario: Changelog entries are validated when present

- **WHEN** a `changelog` is present
- **THEN** it must be a list whose every entry has an ISO `date` and a non-empty `summary`, or the gate fails

### Requirement: Controlled vocabulary

`corpus/vocab.yaml` SHALL define the allowed values for `disciplines`, `tags`, `venues`, `types`,
`languages`, and `relation_kinds` (`cites`, `builds-on`). Any metadata value outside it MUST be
rejected (prevents facet drift).

#### Scenario: Out-of-vocab value is rejected

- **WHEN** a work uses a `discipline`, `tag`, `venue`, `type`, `language`, or `relation kind` not defined in `corpus/vocab.yaml`
- **THEN** the gate rejects it

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

Presentation conventions that are unambiguous from the source text are **mechanically enforced** by
`pipeline/houselint.py`, which `pipeline/validate.py` runs as part of the gate — so a regression
fails CI and cannot merge. It enforces rulings R2/R16 (an inline large operator `\int`/`\sum`/`\prod`
must carry `\displaystyle`, and use `\frac` not `\dfrac` under it) over the transcription, every
translation, **and the `significance` note in `work.yaml`** (which renders inline math through KaTeX
like the `.tex` panels). The linter is a rule registry so further machine-checkable rulings extend
it. Judgement-based rulings (faithful vs. normalized notation, translation wording) are never linted.
Separately, the reader's LaTeX→HTML transform (`site/src/lib/tex.js`) resolves text niceties —
em-dashes, `~`, `\&`, and LaTeX control spaces `\ ` (ruling R17) — and is covered by
`site/src/lib/tex.test.mjs` (`npm test`, run in CI).

#### Scenario: Machine-checkable ruling regression fails CI

- **WHEN** a `.tex` (or the `significance` note) violates a mechanically-enforced ruling such as R2/R16
- **THEN** `pipeline/houselint.py` (run by the gate) fails the build

#### Scenario: Judgement-based rulings are not linted

- **WHEN** a decision is judgement-based (faithful vs. normalized notation, translation wording)
- **THEN** the linter does not flag it
