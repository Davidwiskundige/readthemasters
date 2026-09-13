## 1. Skill Directory & Template Setup

- [x] 1.1 Create `.agents/skills/transcribe/` directory structure.
- [x] 1.2 Add `work.yaml` starter template under `.agents/skills/transcribe/templates/work.yaml`.

## 2. Skill Definition (`SKILL.md`)

- [x] 2.1 Author `.agents/skills/transcribe/SKILL.md` YAML frontmatter and Antigravity activation guidance.
- [x] 2.2 Author Phase 1: Copyright gate enforcement via `pipeline/validate.py` and print-title orthography check.
- [x] 2.3 Author Phase 2: High-resolution page preparation without lossy 1568px downscaling.
- [x] 2.4 Author Phase 3: Phase 0 Global Notation Scan over all document scans into `corpus/<work-id>/notation.md`.
- [x] 2.5 Author Phase 4: Long-context chunked transcription with `effort: high` and per-fragment `pipeline/houselint.py` validation.
- [x] 2.6 Author Phase 4a: File stitching into `original.tex` with contiguous `\origpage` marker validation.
- [x] 2.7 Author Phase 5: Text-only whole-work proofreading classifying findings as DEFECT, INCONSISTENCY, or NEEDS SCAN.
- [x] 2.8 Author Phase 5a: Scan verification pass settling line-by-line fidelity and resolving all NEEDS SCAN queries.
- [x] 2.9 Author Phase 6: Provenance authoring recording `verification.model: gemini-3-8-flash` and explicit `uncertainty_flags`.
- [x] 2.10 Author Phase 7 & 8: Pre-push validation (`pipeline/validate.py`, pytest), contributor review checkpoint, and PR opening.

## 3. Automated Testing & Verification

- [x] 3.1 Implement automated test `pipeline/tests/test_skills.py` validating skill frontmatter, referenced path integrity, and template validity.
- [x] 3.2 Confirm non-interference with `.claude/skills/transcribe/SKILL.md`.
- [x] 3.3 Run `pipeline/validate.py` and `pytest pipeline/tests -q` to verify CI passes with the new skill and tests.
