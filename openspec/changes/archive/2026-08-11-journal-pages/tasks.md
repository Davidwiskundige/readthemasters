# Tasks: journal-pages

## Vocab & validation

- [x] Upgrade `corpus/vocab.yaml` `venues:` to allow object entries; add metadata (`name`, `aka`,
      `kind`, `founded`/`ceased`, `publisher`/`place`, `note`, `archives`) to the seed periodicals,
      and mark `book`/`manuscript` with `kind`. Research the digitized full-run links per journal.
- [x] `pipeline/validate.py` — accept object-or-string venue entries; check object `name` present,
      `kind` in {periodical, book, manuscript}, and every `archives[].url` is absolute http(s).
- [x] Resolve the venue **label** from `name` (object) or the string (bare) everywhere it is read —
      `build_catalog.py` and `build_site_data.py` — so existing citations are unaffected.

## Data

- [x] Aggregate works per venue in `pipeline/build_site_data.py`; emit a top-level `journals` list
      (metadata + works, ordered by year). Exclude `book`/`manuscript` sentinels from the section.

## Site

- [x] `site/src/pages/journals/[slug].astro` — per-journal page (name/aka, era, publisher, note,
      "Find the originals" archive links, works list with per-work scan links).
- [x] `site/src/pages/journals/index.astro` — alphabetical journal index (era + work count).
- [x] Link venue labels from `index.astro` catalog cards and `works/[id].astro` header/citation.
- [x] Add "Journals" nav link in `Base.astro`; journal styles in `global.css`.

## Tests & verification

- [x] `pipeline/tests/test_journals.py` — object/string venue parsing, label resolution,
      aggregation, `kind` exclusion, archive-url validation.
- [x] Build site data + Astro build; verify a journal page, the index, and venue links in the
      preview browser.

## Ship

- [ ] Fold deltas into `openspec/specs/site-catalog` + `corpus-format`; update
      `openspec/config.yaml` context if needed; archive the change.
