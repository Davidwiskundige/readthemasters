# Tasks: work-relations

- [x] Add `relation_kinds` (`cites`, `builds-on`) to `corpus/vocab.yaml`
- [x] `validate.py`: `check_relations` — dangling targets, `to ≠ self`, `year(to) ≤ year(self)`,
      `kind` ∈ vocab, `recommended` ∈ {true, primary} (≤1 per work), acyclic (DAG) check
- [x] Wire `check_relations` into `validate_corpus`
- [x] Tests in `pipeline/tests/test_validate.py` (valid graph, dangling, self, forward-in-time,
      bad kind, double-recommended, cycle)
- [x] `build_site_data.py`: emit `relations_out`, `relations_in`, `recommended_prev`,
      `recommended_next`, and top-level `graph`
- [x] Work page: single-line "Related reading" nav (Read first: / Next:) + "See in timeline" link
- [x] Panel styles in `global.css`
- [x] Seed `relations:` for the six existing works
- [x] Verify: pytest green, gate passes seeded corpus, `npm run build` succeeds, preview check
- [x] Fold deltas into `openspec/specs/` and archive this change; update `openspec/project.md`
