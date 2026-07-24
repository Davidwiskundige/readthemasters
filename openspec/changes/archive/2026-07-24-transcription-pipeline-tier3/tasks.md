# Tasks: transcription-pipeline-tier3

- [x] `pipeline/transcribe.py` — Tier-3 Batch API CLI (`<work-id> --pages --images`)
- [x] Gate is a hard precondition — refuse a work that is not `public_domain` (reuse `validate.py`)
- [x] One Batch request per page: pinned `transcribe-chat.md` prompt (cached) + image (+ optional prev-page tail)
- [x] Stitch fragments into `original.tex` with the standard scaffold (page-ordered, fence/scaffold-cleaned)
- [x] Verification pass (cheap model) flags discrepancies; `--no-verify` to skip
- [x] Honest provenance: `ai-draft`, `submitted_via: pipeline`, model/effort/prompt_version/batch_ids
- [x] Human-review checkpoint — write files, do not commit or push; contributor validates + opens PR
- [x] `anthropic` added to `requirements.txt` as a contributor-only, lazily-imported dependency
- [x] `pipeline/tests/test_transcribe.py` — 24 unit tests for the pure logic, no network
- [x] `pytest pipeline/tests` passes (44 total); `validate.py` still imports only PyYAML (asserted)
- [x] Un-mark Tier-3 as generic in CONTRIBUTING.md (now points at the real command)
- [x] Tier-3 requirements folded into `openspec/specs/transcription-pipeline/spec.md`
- [x] `openspec/project.md` notes Tier-3 shipped
- [ ] End-to-end run on a real work (deferred: needs a contributor's API key + scans)
