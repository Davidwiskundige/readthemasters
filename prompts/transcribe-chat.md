# Transcription prompt (chat) — prompt_version: transcribe-v1

Copy everything in the box below into your AI chat app, then attach a few scan pages (as images or
PDF). Work in batches of a few pages so quality stays high. Paste the LaTeX output back into the
project's **"Chat transcription" issue form**.

> Keep this prompt in sync with the pipeline. The `prompt_version` you used goes into the
> submission so provenance is accurate.

---

You are transcribing a page from a historic mathematics/physics text into LaTeX for a
public-domain digitization project. Follow these rules exactly:

1. **Be faithful.** Transcribe exactly what is printed. Do **not** modernize notation, correct the
   author, or paraphrase. Preserve the original language (do not translate).
2. **Normalize typography, not content.** Render Fraktur/blackletter and long-s (ſ) as normal
   letters; expand ligatures; drop original line breaks and end-of-line hyphenation. Keep the
   author's spelling and symbols.
3. **Use the house style.** Assume `\usepackage{readmasters}` is loaded. Use these macros:
   - `\origpage{N}` at the start of each original page (N = the printed page number).
   - `\uncertain{...}` for text you are not fully sure of; `\illegible` for unrecoverable text.
   - `\ednote{...}` only for genuinely editorial remarks (rare).
   - For a figure/diagram, output `\rmfigure{figures/fig-XX.png}{<caption>}{<alt text>}` — do
     **not** attempt to redraw it; we crop the figure from the scan separately.
4. **Math in LaTeX.** Use standard LaTeX/`amsmath` math. Keep it within what KaTeX supports.
   Preserve the author's notation even where it differs from modern usage.
5. **Structure.** Use `\section*{...}` for headings actually present. Output a paragraph break
   (blank line) where the original has one.
6. **Output only LaTeX** for the body — no commentary, no preamble, no `\documentclass` or
   `\begin{document}`. Start at the first page you were given.

If several pages are attached, transcribe them in order, each preceded by its `\origpage{N}`.
