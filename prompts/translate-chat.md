# Translation prompt (chat) — prompt_version: translate-v1

Copy the box below into your AI chat app, then paste the project's **transcription** (the
`original.tex` content) for the section you are translating. Translate only from our transcription,
never from an existing published translation. Submit via the **"Chat translation" issue form**.

Unlike a transcription, a translation needs **no `work.yaml`** — the work already exists in the
catalog and cleared the copyright gate. Your one deliverable is the translated LaTeX body, which is
committed as `corpus/<work-id>/translations/<lang>.tex`. Preserve every formula, `\tag`, and
`\origpage` marker exactly, so it aligns line-for-line with the original.

---

You are translating a historic mathematics/physics text into {TARGET LANGUAGE, e.g. English} for a
public-domain digitization project. You are given the LaTeX transcription of the original. Follow
these rules exactly:

1. **Translate the prose; preserve the mathematics.** Every math expression, symbol, equation,
   label, and `\ref`/`\eqref` must be reproduced **unchanged**. Do not "modernize" notation. The
   math is also linted for presentation house-style (e.g. inline integrals set as
   `\displaystyle\int \frac{...}{...}`, HOUSESTYLE R2, checked by `pipeline/houselint.py`); since
   you copy it verbatim from the already-house-styled original, keep it exactly — do not reformat.
   **One exception — prose set inside a formula via `\text{...}` is translated like any other
   prose** (HOUSESTYLE R21): a connective such as `\text{ und }`→`\text{ and }`, `\text{ oder}`→
   `\text{ or}`, Latin `\text{seu}`→`\text{or}`, or an ordinal suffix `\mu^{\text{ten}}`→
   `\mu^{\text{th}}`. `pipeline/texcompare.py` ignores the *content* of `\text{...}` (and
   `\textrm`/`\mbox`/… — but **not** `\operatorname`, which names an operator), while still checking
   that each insert is present and that the surrounding math is unchanged. So: translate the words
   inside `\text{...}`, but never drop, add, or reposition the insert or the math around it.
2. **Preserve structure and apparatus verbatim.** Keep every `\origpage{N}` marker in the same
   place (they align the translation to the original). Keep `\section*{}`, environments, and
   `\rmfigure{}{}{}` calls; translate only the human-readable caption/alt text inside them.
3. **Faithful, readable scholarly English** (or the target language). Prefer period-appropriate
   mathematical terminology; when a term is ambiguous, add a brief `\ednote{translator's note: …}`
   rather than guessing silently. For the author's own period technical term (e.g. an archaic name
   for a modern concept), prefer a **literal, untranslated rendering** (e.g. keep "potentia" as
   "potentia") rather than an inline gloss — let the reader meet the author's own word directly;
   historical context belongs in the work's editorial significance note, not inside the
   translation. If an inline gloss is ever genuinely necessary, use **square brackets**, never
   parentheses — parentheses are the author's own device for asides, so a bracketed gloss keeps
   your addition visibly distinct from their words.
4. **House style.** Assume `\usepackage{readmasters}`. Use `\uncertain{...}` if unsure of a
   rendering. Keep the author's meaning; do not add or remove content.
5. **Output only the translated LaTeX body** — no commentary, no preamble.

If a glossary is provided, apply it consistently.
