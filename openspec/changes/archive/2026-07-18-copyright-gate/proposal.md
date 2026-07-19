# Change: copyright-gate

## Why

The project's core promise is that it publishes only public-domain texts. That promise must be
enforced by code, not by memory — an automated gate that runs in CI and fails the build on any
violation.

## What changes

- Implement `pipeline/validate.py`: schema validation + vocabulary check + the copyright gate +
  status/provenance checks + cross-work checks (unique ids).
- Encode the copyright rules of PLAN.md §2:
  - `pma_70` — every author died long enough ago (life + 70, Jan-1 rollover).
  - `us_publication` — first published long enough ago (95-year rule, Jan-1 rollover).
  - `edition_rights` — the transcribed edition carries no fresh copyright.
  - `translation_source` — translations derive only from our own PD transcription.
  - optional strict `pma_100`.
- Require sourced copyright facts (publication date + edition) — PLAN.md §2.5.
- Write/refresh the `copyright_assessment` block and fail on any rule violation.
- A test suite covering passing and each failing scenario.

## Impact

- New: `pipeline/validate.py`, `pipeline/tests/`, `pipeline/requirements.txt`.
- Wired into CI as a required check.
- Depends on: `corpus-format`.
