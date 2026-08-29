## Why

A `significance` note is one editorial paragraph: what the author did, and why it mattered. For a
work whose result is universally quoted today in notation the author never used, that paragraph
attracts a second one translating the old statement into the new — and the second paragraph is
longer than the first. `roch-1865-anzahl-constanten` is the case in hand: more than half of its
significance had become a divisor-by-divisor dictionary between Roch's count of arbitrary constants
and $\ell(D) - \ell(K-D) = \deg D - p + 1$, with Roch's own argument buried in the middle. The
material is worth keeping and worth reading — but only for some readers, and never on the way in.

The site already has the apparatus for exactly this: the shared `.pop` popover, used by the `[n]`
citation markers in the same paragraph and by `\ednote` in the texts. What is missing is a way for
the corpus to author an aside longer than a citation and give it a name.

## What Changes

- **New optional `work.yaml` field `significance_notes`** — a list of `{label, text}` asides,
  addressed from the significance prose by a `[note n]` marker (positional, like `[n]` to
  `significance_sources`). `label` is the visible inline trigger; `text` is plain prose + inline
  KaTeX, exactly like the significance itself.
- **Work page renders a `[note n]` marker as a labelled chip** whose popover carries the note —
  the same hover/focus/tap/Escape behavior as every other `.pop`, and the same KaTeX pass, which
  already covers the whole `.significance` region including hidden popover content.
- **`renderSignificance()` moves out of `works/[id].astro` into `site/src/lib/significance.js`**
  and gains unit tests (`npm test`, run in CI). It was the only piece of marker-parsing in the
  repo with no test behind it; adding a second marker form made that worth fixing.
- **The gate learns the marker contract**: `pipeline/validate.py` fails on a marker with no entry
  behind it (today it renders as a literal `[3]` on the page), warns on an entry no marker points
  at (it renders nowhere at all), requires a non-empty `label`/`text`, warns on a label too long to
  sit in running prose, and house-lints each aside's math like the significance itself.
- **`corpus/HOUSESTYLE.md` ruling R26** records the editorial half: what belongs in the paragraph
  versus in an aside. R18's pointer to the renderer and R11's marker-numbering bullet are updated.
- **`roch-1865-anzahl-constanten` is rewritten** to the new shape — its modern-notation excursus
  becomes one "In modern notation" aside, and the significance paragraph returns to 1.2k
  characters, in line with the rest of the corpus.

## Capabilities

### New Capabilities

None. Both affected capabilities exist; this extends them.

### Modified Capabilities

- `corpus-format`: the **work.yaml schema** requirement gains the optional `significance_notes`
  list and the `[note n]` marker contract, alongside the `significance_sources`/`[n]` contract it
  already describes; the **LaTeX house style** requirement's mechanical linting extends to each
  aside's text, which carries the same inline math.
- `site-catalog`: the **Significance note** requirement gains the aside rendering — a labelled chip
  in the running prose whose popover holds the note, built on the existing shared `.pop` apparatus.

## Impact

- `corpus/roch-1865-anzahl-constanten/work.yaml` — significance rewritten, one aside added.
- `corpus/HOUSESTYLE.md` — new ruling R26; R11 and R18 updated.
- `prompts/transcribe-chat.md` — the work.yaml sketch mentions the optional field.
- `pipeline/validate.py` — new `check_significance()`; house-lint extended to aside text.
- `pipeline/build_site_data.py` — passes `significance_notes` through to `works.json`.
- `pipeline/tests/test_validate.py`, `site/src/lib/significance.test.mjs` — coverage for both.
- `site/src/lib/significance.js` (new), `site/src/pages/works/[id].astro`, `site/src/styles/global.css`.
- No change to `site/src/scripts/pop.js`: the aside is an ordinary `.pop`, which is the point.
