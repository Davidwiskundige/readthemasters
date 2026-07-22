# Tasks: transcription-skill

- [x] `.claude/skills/transcribe/SKILL.md` — phased workflow, gate-first, DCO PR
- [x] `.claude/skills/transcribe/templates/work.yaml` — annotated new-work template
- [x] Skill reuses existing rules (transcribe-chat prompt, HOUSESTYLE, preamble, validate.py) rather than duplicating
- [x] Honesty constraints baked in (ai-draft default, human-review checkpoint, no gate fudging)
- [x] Un-mark the skill as "planned" in CONTRIBUTING.md
- [x] New `transcription-pipeline` capability spec folded into `openspec/specs/`
- [x] `openspec/project.md` moves `transcription-pipeline` from upcoming to shipped
- [ ] End-to-end dry run on a real work (deferred: needs a chosen unclaimed text + scans)
