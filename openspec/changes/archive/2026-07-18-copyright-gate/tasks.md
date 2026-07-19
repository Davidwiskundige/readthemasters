# Tasks: copyright-gate

- [x] `pipeline/requirements.txt` (PyYAML)
- [x] Schema + vocabulary validation in `validate.py`
- [x] `pma_70` rule (life + 70, Jan-1 rollover, unknown-death handling)
- [x] `us_publication` rule (95-year rule, Jan-1 rollover)
- [x] `edition_rights` rule
- [x] `translation_source` rule
- [x] Optional `pma_100` strict mode (config flag)
- [x] Require sourced publication date + edition (§2.5)
- [x] Status/provenance consistency (validated needs 2 reviewers, etc.)
- [x] Cross-work unique-id check
- [x] Test suite: passing work + one failure per rule
- [x] `external-open` translation source allowed with a named license (added with site-catalog)
- [x] Wikidata death-date cross-check as a warn-only CI step (`pipeline/wikidata_check.py`)
