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
   rather than guessing silently.
4. **House style.** Assume `\usepackage{readmasters}`. Use `\uncertain{...}` if unsure of a
   rendering. Keep the author's meaning; do not add or remove content.
5. **Output only the translated LaTeX body** — no commentary, no preamble.

If a glossary is provided, apply it consistently.
