# Translation prompt (chat) — prompt_version: translate-v1

Copy the box below into your AI chat app, then paste the project's **transcription** (the
`original.tex` content) for the section you are translating. Translate only from our transcription,
never from an existing published translation. Submit via the **"Chat translation" issue form**.

---

You are translating a historic mathematics/physics text into {TARGET LANGUAGE, e.g. English} for a
public-domain digitization project. You are given the LaTeX transcription of the original. Follow
these rules exactly:

1. **Translate the prose; preserve the mathematics.** Every math expression, symbol, equation,
   label, and `\ref`/`\eqref` must be reproduced **unchanged**. Do not "modernize" notation.
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
