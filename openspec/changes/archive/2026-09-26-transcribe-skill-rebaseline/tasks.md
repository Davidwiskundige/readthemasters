## 0. Precondition

- [x] 0.1 *`transcribe-turn-cost`'s code is on main; its remaining tasks were closed and it is archived in the same PR.* Confirm `transcribe-turn-cost` has landed on main (this change edits the Phase 3 and Phase 5 text it wrote); rebase onto it before starting.

## 1. Magnification ledger

- [x] 1.1 `pipeline/magnify.py`: `--pass transcribe|verify` (default `transcribe`); read/write `magnify-ledger.json` in `--prepared`, keyed by page and pass; enforce the cap against the ledger, not against files in `--out`.
- [x] 1.2 `--cap` may lower the cap, never raise it above `DEFAULT_CAP`; refuse with a message that says so.
- [x] 1.3 The cap-exceeded message names the ledger path and the regions already recorded for that page and pass.
- [x] 1.4 `pipeline/prepare_pages.py`: clear ledger entries for every page it prepares.
- [x] 1.5 Tests in `pipeline/tests/test_magnify.py` (and `test_prepare_pages.py`): fresh `--out` does not reset; passes have separate budgets; `--cap` above default refused, below accepted; re-preparing clears; the existing per-page cap tests still pass.
- [x] 1.6 `python -m pytest pipeline/tests -q` and `python pipeline/validate.py` pass.

## 2. Skill: batch sizes

- [x] 2.1 Phase 3: default batch 12, snapped to a chapter/part/article boundary within ~3 pages, never above ~15. Replace the "measured optimum 2–4, curve flat" paragraph with the measured rationale (turns per batch constant; fixed ~$0.11 warm, $0.23 for the first batch; N=12 vs N=4 vs N=28 table in one line each) and a pointer to `transcribe-cost-rebaseline/measurements.md`.
- [x] 2.2 Phase 3: the inline threshold becomes "about 8 pages", with the sentence saying why it is absolute.
- [x] 2.3 Phase 3: batch report and magnify instructions pass `--pass transcribe`; the "one message writing all fragments" step allows as few messages as needed when 12 fragments do not fit in one.
- [x] 2.4 Phase 5a: replace "Batch size here is inherited from transcription rather than measured" with the decoupled 4-page concurrent rule and its reason; a 12-page batch gets three verifiers.

## 3. Skill: verifier prompt and effort

- [x] 3.1 Phase 5a verifier instructions: the post-display paragraph check (indented = new paragraph, flush left = continuation; list each change), worded as a rule about the print.
- [x] 3.2 Phase 5a: magnify calls in the verifier prompt pass `--pass verify`.
- [x] 3.3 "Before you start": effort `medium` recommended, the evidence in two sentences, how to confirm (`CLAUDE_EFFORT`, or `effort` on transcript rows); `low` named as measured and rejected.
- [x] 3.4 Phase 6: check the provenance template's `effort` comment says to record the effort actually used.

## 4. Land it

- [x] 4.1 Re-read the delta spec against what was built; correct the spec where the build contradicted it.
- [x] 4.2 `openspec validate transcribe-skill-rebaseline --strict`, the test suite, and `validate.py` pass.
- [x] 4.3 *Deferred by nature — it needs a real run after this lands; recorded in the `transcribe-token-cost` memory so the next transcription session does it.* First real run under the new skill: measure with `measure_session.py` and review its verification discrepancy lists; if quality at N=12 is visibly worse than the N=4 baseline, revert the default to 4 and record why.
- [x] 4.4 Show the contributor the summary; open the PR with a DCO sign-off; sync the delta into `openspec/specs/transcription-pipeline/spec.md` and archive.
