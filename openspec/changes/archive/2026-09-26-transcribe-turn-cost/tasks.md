## 1. Baseline

- [x] 1.1 Pick the measurement pages: an untranscribed range on a work with a comparable scan to Clebsch pp. 223–243, ~20 pages, five batches. Record which, and why it is comparable.
  - **Chosen 2026-09-12: Picard 1885, *Sur les intégrales de différentielles totales algébriques de première espèce*, Journal de mathématiques pures et appliquées, pp. 281–346. Measurement range pp. 281–300 — 20 pages, five batches.** Not previously transcribed.
  - **Why it qualifies.** Source scans are 3308×4678 bilevel (A4, aspect 1:1.41). `prepare_pages.py` over all 66 pages: text width 977–1277px, **median 1015px**, **9 of 66 under the 1000px threshold (14%)**, and **0 pages where text-block detection failed**. That means one image per page, as Clebsch was — not the half-page split castelnuovo was forced into at 72/76 warned.
  - **Caveat to carry into the measurement.** At a 1015px median Picard is ~14% narrower than Clebsch's 1180px, so it will likely want more magnified regions per page than Clebsch's 1.7. That is a property of the scan, not of the method, and it makes the run a *harder* test of D1 rather than an easier one. **Report the crop count, and compute the turn saving internally** — measured `t` against what `t` would have been at 2 turns per region under per-region cropping — rather than resting the result on the Clebsch comparison alone. The Clebsch figures stay as a secondary, caveated reference.
  - The source is 3308×4678 against Clebsch's 1400×1859 — 2.4× the linear resolution — so magnification buys back far more here than it could there.
  - *Superseded plan:* parked 2026-09-12 pending a new work; the work arrived the same day.
  - `castelnuovo-enriques-1897-surfaces-algebriques` was considered and **rejected**. It is fully transcribed (pp. 241–316, 19 batches, 2026-09-07), so it has no untranscribed range; and more importantly its scan is tall (1:1.7), `prepare_pages.py` warned on 72 of 76 pages, and the run therefore used **landscape half-page crops — two images and one extra turn per page by design**. The baseline this change is measured against (509k/page, `t = 5.7`) is a **one-image-per-page** figure. Measuring `magnify.py` on a half-page run confounds the turn saving with the split's extra turn, which is what the "why it is comparable" clause above exists to prevent.
  - **What the next work needs to qualify:** untranscribed; a scan `prepare_pages.py` does *not* warn on (so one image per page, as Clebsch was); and ~20 pages so the run is five batches. Aspect ratio is the thing to check first — it decides the method, and the method decides whether the comparison means anything.
- [x] 1.2 Restate the figures this change is measured against, from `archive/2026-09-02-transcribe-per-batch-subagents/measurements.md`: 509k tokens/page transcription, ~1.0M/page with verification, `t = 5.7` transcription and ~4.9 verification, 1.7 magnified regions/page, and serial verification round-trips.
- [x] 1.3 Confirm `measure_session.py` still reports the same quantity (fresh input + cache reads + cache writes + output) so the comparison stays like-for-like, and note the standing caveat that subagent transcripts are not persisted and per-page figures are modelled from endpoints.

## 2. The magnification helper

- [x] 2.1 Write `pipeline/magnify.py`: takes a page number, the prepared-pages directory (for `zoom-map.json`), the source scan, and a list of regions in prepared-image coordinates; converts each with `source = offset + prepared/scale`; writes all crops in one invocation to a scratch directory; prints one line per crop (region, source box, output size).
- [x] 2.2 Enforce the cap in the helper, not only in prose: refuse more than 3 regions for a page and say so, so the cap survives magnification becoming cheap.
- [x] 2.3 Fail loudly on a region that maps outside the source page or degenerates to a near-empty box, following the precedent in `prepare_pages.py` where a silent no-op crop cost a whole batch's escalation budget.
- [x] 2.4 Keep the dependency footprint to stdlib + Pillow, matching `prepare_pages.py`. `pipeline/validate.py` and CI must not gain a dependency.
- [x] 2.5 Add `pipeline/tests/` coverage: coordinate conversion against a known `zoom-map.json` row, the cap, the out-of-bounds refusal, and multi-region output in one call.
- [x] 2.6 Run `python -m pytest pipeline/tests -q` and `python pipeline/validate.py`; both must pass.

## 3. Skill changes — turns

- [x] 3.1 Rewrite the escalation guidance in `.claude/skills/transcribe/SKILL.md` Phase 3: a page's regions are produced by one `magnify.py` call and read in one turn via parallel `Read`s in a single message. Delete the ad-hoc per-crop cropping instructions.
- [x] 3.2 Update the batch-subagent prompt contract to pass the prepared-pages directory and source scan paths for `magnify.py` instead of raw `zoom-map.json` rows for hand conversion.
- [x] 3.3 Add the magnified-region count as a required batch report section. Leave `TRAILING LINES` in place — transcription stays sequential and the join still depends on it (design D4).
- [x] 3.4 Leave the Phase 3 batch loop, batch size, and Phase 3a glossary update untouched. If a subsequent task tempts a change here, it is out of scope.

## 4. Skill changes — verification order and concurrency

- [x] 4.1 Reorder Phase 5: the text-only proofread of the assembled file runs **first**, then the batch verifiers. Renumber the skill's phases so the proofread is no longer "5b" sitting after the scan pass.
- [x] 4.2 Route the proofread's `needs scan` findings to the verifier covering each page, as targeted checks in that verifier's prompt, so they are settled during a reading that happens anyway rather than by a further subagent afterwards.
- [x] 4.3 Dispatch the batch verifiers concurrently.
- [x] 4.4 State in the skill why verifier concurrency is safe where transcription concurrency is not: each verifier re-reads its own images in a fresh context and consumes no other subagent's output, so nothing orders them.
- [x] 4.5 Check the proofread's contract still holds when it reads pre-verification text: it is still given `provenance.yaml` so it does not re-report documented misprints, and its findings must still be verified before they are acted on.

## 5. Provenance

- [x] 5.1 Record the verification model in `provenance.yaml` for Tier-2 runs, matching the `verification: {model: ...}` shape `pipeline/transcribe.py` already writes for Tier-3.
- [x] 5.2 Update the Phase 6 template in the skill and check `pipeline/validate.py` accepts the field on an existing work without complaint.

## 6. Measure the turn reduction

- [x] 6.1 Transcribe the task 1.1 pages under the new skill. Record per batch: reported tokens, tool calls, magnified regions.
- [x] 6.2 Compute `t` and tokens/page the same way `measurements.md` does, and compare against 509k/page and `t = 5.7`. The design predicts `t` near 3.3; report what it actually is, including if the crop tax turns out not to have been the whole gap.
- [x] 6.3 Measure verification separately: `t`, tokens/page, and wall-clock round-trips against the serial baseline.
- [x] 6.4 Confirm concurrent verification did not change what verification *finds* — compare the discrepancy list against what a serial pass produced on comparable pages, not just the time it took.
- [x] 6.5 Count how many `needs scan` findings the proofread produced and how many the verifiers settled without a further subagent. This is what design D3 buys; if it is near zero on this work, say so rather than claiming the reorder paid.
- [x] 6.6 *Closed without the planned measurement (2026-09-26).* Superseded by `transcribe-cost-rebaseline`: with a price-weighted meter, verification cost per page was flat ($0.22–0.24) across the measured arms, and `transcribe-skill-rebaseline` fixes verification at 4 pages, concurrent, as a wall-clock decision. N=1/2 was not run. Original task: Measure the verification batch size rather than inheriting it: run one wave at the default N and one at N=1 or 2 on the same pages, and report reported tokens, tool calls and per-page cost for each. Design D2 gives two readings of the cost model that disagree by 3×; this is the measurement that separates them.
- [x] 6.7 Re-measure the orchestrating session with `measure_session.py` — images must still be 0, and report whether several reports arriving together moved its mean context.
- [x] 6.8 Write all of it to `measurements.md` in this change folder, following the archived change's format.

## 7. A/B the verification model tier

- [x] 7.1 *Closed, adopting nothing (2026-09-26).* A lower **model tier** was not tested. A lower **effort** was (`transcribe-cost-rebaseline`, effort A/B on Opus 5.5): `low` failed this group's kill criterion — five substantive defects `medium` did not make, three introduced by `low`'s own verifiers — so verification stays on the transcription model at `medium`. A model-tier A/B remains possible later; nothing here supports one. Original task: Re-verify a fixed subset of the new run's pages on a lower model tier, in isolation, using the group-5 methodology from the archived change.
- [x] 7.2 Diff the two discrepancy lists. Kill criterion: if the lower tier misses any correction the higher tier found on those pages, the tier stays and the change adopts nothing here.
- [x] 7.3 Record the outcome either way in `measurements.md`, including the misses if there were any — a negative result is the point of running it.
- [x] 7.4 Only if the A/B passes: set the lower tier as the skill's default verification model and say so in the skill.

## 8. Land it

- [x] 8.1 Re-read the delta spec against what was actually built and correct the spec where the measurement contradicted the design, rather than the other way round.
- [x] 8.2 `python pipeline/validate.py` and `python -m pytest pipeline/tests -q` pass; `openspec validate transcribe-turn-cost` passes.
- [x] 8.3 Show the contributor the measurement summary before pushing, per the human review checkpoint.
- [x] 8.4 *Landed together with `transcribe-cost-rebaseline` and `transcribe-skill-rebaseline` in one PR, at the contributor's request.* Open the PR with a DCO sign-off; state the measured `t`, tokens/page, and wall-clock change, and whether the verification A/B was adopted.
- [x] 8.5 Sync the delta into `openspec/specs/transcription-pipeline/spec.md` and archive the change.
