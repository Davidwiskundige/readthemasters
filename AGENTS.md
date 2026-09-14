# Agent Instructions for ReadTheMasters

## Direct Execution for Skills (Do Not Create Implementation Plans)

When invoked with `/transcribe` or `/translate`, or when executing the `transcribe` or `translate` skills:
- **DO NOT enter planning mode.**
- **DO NOT create an implementation plan** (`implementation_plan.md` artifact).
- **DO NOT ask the user to approve a plan** or wait for confirmation before starting.
- The transcription and translation skill workflows are pre-determined, authoritative operational runbooks.
- **Execute immediately**: begin Phase 1 right away upon invocation and proceed through each phase sequentially to completion. The contributor will review the final output at the review checkpoint (Phase 8) before anything is committed or pushed.
