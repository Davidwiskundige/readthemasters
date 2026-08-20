## Context

The journal surfaces are two Astro pages over the build-time `journals` list in `works.json`:
`site/src/pages/journals/index.astro` (a directory of all `periodical` venues) and
`site/src/pages/journals/[slug].astro` (one journal's metadata, external-archive links, and works).
Both currently render entries as `.card` boxes. The corpus is sparse: 10 journals, 7 with zero works,
the largest holding 3. Each `work.yaml` carries `title_en` (an English title), `publication.year`,
and `publication.month` (Acta Eruditorum is cited by month, not volume), and may carry
`publication.volume` (no current work does). `title_en`, `volume`, and `month` are all available in
the flat work dict `build_site_data.py` already assembles but were not surfaced onto the journal
works — this change plumbs them through. The corpus format and copyright gate are untouched.

## Goals / Non-Goals

**Goals:**
- Make both journal surfaces compact and title-led — the title is the only thing needed to navigate.
- Treat an empty journal as a contribution on-ramp, not a dead end, tying it to the Contribute page.
- Give a journal's works an eudml-style browse: collapsible volume/issue sections that scale from a
  sparse corpus to a dense one, showing each work's translated title.
- Ship with data that already exists in `work.yaml`; no corpus-format or copyright-gate change.

**Non-Goals:**
- Any change to which works appear (the copyright-gated aggregation is unchanged).
- Adding new fields to `work.yaml`; only surfacing existing ones onto the journal `works.json`.
- Reworking the index search box or the timeline; era/period browsing stays on `timeline.astro`.

## Decisions

**1. Index: title-led rows, non-zero work count only, no era/place.**
The index becomes a plain list of journal-title links. A work count renders *only* when the venue has
≥1 work, as a positive "there's something to read here" marker; venues with zero works show no count
at all (never `0 works`). Empties stay in the same alphabetical order as equals.
- *Why:* answers "you only need the titles"; a positive-only count spotlights where content already
  exists without a negative `0` shaming empty journals.
- *Alternatives considered:* keep the work-count pill always (re-introduces `0 works` noise);
  de-emphasize or segregate empties (signals "lesser" journals — rejected once empties are reframed
  as invitations); hide empties (would hide the best recruitment surface — rejected).

**2. Empty journals are invitations, not dead ends.**
An empty journal page still carries metadata and the "Find the originals" archive links — the links
are the payload. The empty state promotes that block and replaces the flat "no works yet" message with
one quiet line inviting the reader to help revive the journal, linking to `contribute.md`.
- *Why:* the archive links point straight at the scanned runs a contributor would transcribe; this is
  the Tier-2 contributor loop (PLAN.md §4.1/§10). The empties are the seedbed.
- *Alternatives considered:* a louder call-to-action block (heavier than the surface warrants — user
  chose a quiet line); leaving the flat message (wastes the recruitment opportunity).

**3. Detail works: eudml-style collapsible dropdowns (native `<details>`).**
Works are grouped into collapsible sections that mirror eudml's per-volume accordions (whose labels
read `volume {n} ({year})`). Sections are **open by default** to avoid friction on the current sparse
corpus (a reader shouldn't have to click to see a journal's one or two works); the reader can collapse
any section. Each section's `<summary>` shows the label and a work count. Implemented with native
`<details>`/`<summary>` — no JavaScript, keyboard-accessible, degrades gracefully without JS.
- *Why:* the user explicitly wants eudml's browse model, which scales from a handful of works to a
  full multi-hundred-volume run. Native `<details>` gives the accordion for free.
- *Alternatives considered:* plain non-collapsible subheads (the earlier revision of this change —
  reversed at the user's request); a JS accordion (unnecessary; `<details>` is native); a table
  (long Latin titles dominate a title column and read poorly on mobile).

**4. Group by volume when present, else by dated issue.**
A section key is the `volume` when a work records one (label `Volume {n} ({year})`), otherwise the
`month`+`year` issue (label `{month} ({year})`, falling back to `{year}` with no month). Sections
sort chronologically (year → volume → month). No current work has a volume — Acta is cited by month —
so today every section is an issue; volume sections engage automatically for any future work with a
`volume`.
- *Why:* matches how each journal is actually cited (Acta by monthly issue, later journals by
  volume) without inventing a `volume` where none exists.

**5. Show the translated title from `title_en`, plumbed through the pipeline.**
`build_site_data.py` now emits `title_en`/`title_en_tex`, `volume`, and `month` onto each journal
work (they already existed in `work.yaml` and the flat work dict). The detail page shows `title_en`
beneath the original title when present, preferring `title_en_tex` so title math renders.
- *Why:* the translated title aids readers scanning a Latin/German corpus; the data already exists,
  so this is plumbing, not a schema change.
- *Alternatives considered:* deriving a translation on the page (none to derive — `title_en` is the
  source of truth).

**6. Contribute page closes the loop.**
`contribute.md` Step 1 (transcribing) gains a referral to the journals as the discovery surface for
originals worth reviving — the reverse pointer to the empty-journal invitation.
- *Why:* the page tells contributors to "pick a work" but never says where to look; the journals'
  archive links are exactly that hunting ground.

## Risks / Trade-offs

- **Losing era/place from the index reduces at-a-glance context** → mitigated: that context lives on
  each detail page and browsing by period is served by `timeline.astro`.
- **Open-by-default sections could grow long once a journal has many volumes** → accepted for now:
  the corpus is sparse and open-by-default removes click friction; native `<details>` still lets a
  reader collapse sections, and a future refinement could collapse by default past a volume threshold.
- **A reader seeking works may land on an empty journal** → mitigated: the reframe makes that a
  useful landing (archives + revive invitation) rather than a dead end.
- **KaTeX must render both the title and the translation** → mitigated: the `renderMathInElement`
  pass targets the `.jvols` container, covering titles and `title_en_tex` alike.

## Migration Plan

Update `build_site_data.py` (emit `title_en`/`volume`/`month`), the two Astro pages, the journal CSS,
and `contribute.md`; run `npm run data` then rebuild, and verify the three states (title index,
populated detail with working dropdowns, empty-invitation detail) in the preview. No corpus or
copyright data changes, so rollback is a straight revert of the page/CSS/pipeline edits. When the
change ships, fold this delta into `openspec/specs/site-catalog/spec.md` and archive.

## Open Questions

- None blocking. A `volume` field is already read from `work.yaml`; volume-labelled sections will
  render automatically once any work records one.
