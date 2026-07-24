# Tasks: translation-pipeline

- [x] `pipeline/texcompare.py` — math/marker/ref preservation check (stdlib-only)
- [x] Wire the preservation check into `pipeline/validate.py` (CI gate); existing corpus passes
- [x] `pipeline/translate.py` — Tier-3 Batch API CLI (`<work-id> --lang`), chunked by `\origpage`
- [x] Gate is a hard precondition — refuse non-PD works and works with no `original.tex`
- [x] Translate only from our transcription — provenance records `source: transcription` (§2.2)
- [x] Optional per-work glossary fed into the prompt (`corpus/<id>/glossary.yaml` / `--glossary`)
- [x] Post-run preservation check + human-review checkpoint; no commit/push
- [x] `.claude/skills/translate/SKILL.md` — Tier-2 phased workflow, gate-first, DCO PR
- [x] Reuse `transcribe.py` helpers (`load_prompt`, `run_batch`, `_client`); `anthropic` stays lazy
- [x] `pipeline/tests/test_texcompare.py` + `test_translate.py` — pure-logic tests, corpus passes
- [x] `pytest pipeline/tests` passes (67 total); `validate.py` still imports only PyYAML + stdlib
- [x] `translation-pipeline` spec added under `openspec/specs/`
- [x] `openspec/project.md` moves `translation-pipeline` from upcoming to shipped
- [x] CONTRIBUTING.md documents the Tier-2/Tier-3 translation commands
- [ ] End-to-end run on a real work (deferred: needs a chosen work + a run on subscription/API key)
