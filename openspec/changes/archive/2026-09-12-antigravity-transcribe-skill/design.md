## Context

The repository supports multiple contribution tiers (PLAN.md §10). Tier 2 was originally implemented as a Claude Code skill (`.claude/skills/transcribe/SKILL.md`) tailored to Claude Opus 4.8/5. That skill's architecture—strict subagent isolation, downscaling to 1568px, 4-page batch limits, and batching crops through `pipeline/magnify.py`—was designed to counter Opus's high per-token pricing and the "image residency tax" across turns.

Recent empirical work in the Claude pipeline (`transcribe-turn-cost`) revealed critical process improvements:
1. Running a whole-work text-only proofread *before* scan verification eliminates stranded `needs scan` queries and cuts redundant scan opens.
2. Running `pipeline/houselint.py` on fragments as they land isolates house-style drift to the generating step rather than post-assembly.
3. Explicitly recording the verification model and uncertainty flag counts in `provenance.yaml` ensures auditable quality.

Google Antigravity provides an agentic environment running Gemini models (such as Gemini 3.8 Flash) with a 1M+ token context window, ultra-cheap multimodal input, and economical thinking tokens. Antigravity discovers project-specific skills in `.agents/skills/<name>/SKILL.md`.

## Goals / Non-Goals

**Goals:**
- Provide a first-class Antigravity workspace skill at `.agents/skills/transcribe/SKILL.md`.
- Leverage Gemini 3.8 Flash's cost economics: high-resolution scans upfront, whole-work resident context, and `effort: high` reasoning across all pages.
- Implement the Phase 0 Global Notation Scan over all scans to establish `notation.md` before generating LaTeX.
- Implement the state-of-the-art verification flow: `[stitch] -> [text-only proofread] -> [verify against scans carrying needs-scan queries]`.
- Enforce per-fragment `pipeline/houselint.py` checks as fragments land.
- Preserve 100% compatibility with repository invariants: `pipeline/validate.py` copyright gate, `prompts/transcribe-chat.md`, and `HOUSESTYLE.md`.
- Add automated testing via `pipeline/tests/test_skills.py` to prevent skill bitrot, validating frontmatter, referenced file links, and template integrity.

**Non-Goals:**
- Modifying `.claude/skills/transcribe/SKILL.md` (Claude Code users continue using their Opus-optimized skill).
- Modifying `pipeline/transcribe.py` (Tier-3 Batch API script).
- Modernizing archaic notation or changing the public-domain quality ladder (`ai-draft`).

## Decisions

### 1. Skill Location: `.agents/skills/transcribe/SKILL.md`
- **Choice**: Place the skill in `.agents/skills/transcribe/SKILL.md` with frontmatter `name: transcribe`.
- **Rationale**: Antigravity automatically discovers `.agents/skills/` as the highest-precedence workspace skill root. Claude Code continues reading `.claude/skills/transcribe/SKILL.md`. Both tools coexist without conflict or interference.

### 2. Upfront High-Resolution Scans vs. Downscaled Interactive Magnification
- **Choice**: Eliminate the 1568px downscaling cap and interactive `magnify.py` crop escalation. Feed full-resolution scans or landscape half-page tiles upfront.
- **Rationale**: Downscaling was necessary in Opus to avoid massive token bills, but it caused narrow portrait pages to lose critical subscript and punctuation detail (Göttinger Nachrichten measured 817–907px text width). In Gemini Flash, multimodal tokens cost fractions of a cent; high resolution can be provided upfront, avoiding glyph degradation and eliminating the multi-turn crop calculation loop.

### 3. Phase 0 Global Notation Scan
- **Choice**: Before generating any LaTeX fragments, the agent ingests all page images in a single call to inspect typographical and mathematical conventions across the entire text, emitting `corpus/<work-id>/notation.md`.
- **Rationale**: In Opus, batches were isolated and could only see trailing lines, leading to divergent notations across batches (e.g. `\sum` vs `\Sigma`). With Flash's 1M context, whole-document scanning upfront costs ~$0.01 and locks conventions before line 1 is written.

### 4. High Reasoning Effort (`effort: high`) by Default
- **Choice**: Instruct the agent to run with `effort: high` (extended thinking) on both transcription and verification, and record `effort: high` in `provenance.yaml`.
- **Rationale**: Flash thinking tokens are economical. Enabling high thinking effort gives the model the reasoning runway to analyze complex Fraktur ligatures, ambiguous subscripts, and multiline display equations without meaningful financial penalty.

### 5. Chunked Generation with Early House-Style Linting
- **Choice**: Emit LaTeX in chunks of 4 pages (or page-by-page) into scratch files, running `python pipeline/houselint.py <fragment>` immediately as each fragment lands.
- **Rationale**: Respects LLM output completion token limits (~8k tokens) while catching macro and formatting drift at the exact step that introduced it, prior to stitching.

### 6. Reordered Verification: Proofread First, Then Scan Verification
- **Choice**: Reorder Phase 5 to:
  1. **Phase 5 (Proofread, text-only)**: Whole-document read of assembled `original.tex` + `notation.md` without images. Classifies findings as `DEFECT`, `INCONSISTENCY`, or `NEEDS SCAN`.
  2. **Phase 5a (Verify against scans)**: Checks line-by-line fidelity against the scans, carrying the specific `NEEDS SCAN` items so each page image is opened only once.
- **Rationale**: Directly adopts the measured finding from `transcribe-turn-cost` (D3). Running proofreading after verification left `NEEDS SCAN` questions stranded, requiring a second round of scan openings.

### 7. Explicit Provenance and Title Orthography
- **Choice**: Always take the work title from the printed scan rather than catalogue entries (R12), and explicitly record `verification: { model: gemini-3-8-flash, flagged_pages: [...], date: ... }` and `uncertainty_flags: N` in `provenance.yaml`.
- **Rationale**: Catalogues routinely modernize orthography (`Variabeln` vs `Variablen`). Explicit verification models prevent ambiguous provenance.

### 8. Automated Testing Strategy (`pipeline/tests/test_skills.py`)
- **Choice**: Add an automated pytest suite in `pipeline/tests/test_skills.py`.
- **Rationale**: Guarantees that YAML frontmatter, all referenced script paths, house-style extracts, and starter templates remain strictly valid across CI runs.

## Risks / Trade-offs

- **[Risk]** Output token limit exceeded if too many pages are generated in a single completion.
  → *Mitigation*: The skill instructs generating fragments in 4-page batches or one page per write tool call.
- **[Risk]** Hallucination on faint or damaged print without Opus's dense parameter scale.
  → *Mitigation*: Enforce full-resolution scans upfront, `effort: high`, and a dedicated verification pass carrying `NEEDS SCAN` queries.
- **[Risk]** Divergence between Claude and Antigravity skill conventions.
  → *Mitigation*: Both skills enforce identical preconditions (`validate.py`), identical house-style prompt references (`prompts/transcribe-chat.md`), and identical provenance schemas (`provenance.yaml`).
