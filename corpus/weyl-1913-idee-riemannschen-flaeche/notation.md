# Notation Rulings — Weyl (1913): Die Idee der Riemannschen Fläche

This document records document-wide typographic, notational, and structural decisions for Hermann Weyl's *Die Idee der Riemannschen Fläche* (B. G. Teubner, Leipzig und Berlin, 1913), following `HOUSESTYLE.md` (R27).

## 1. Typefaces and Mathematical Alphabets

- **Fraktur variables vs Roman**:
  - The text is set in Antiqua, but uses distinct Fraktur capitals for topological and function-theoretic entities:
    - $\mathfrak{P}$: Power series / element of an analytic function (e.g. $\mathfrak{P}(z - a)$). Transcribe as `\mathfrak{P}`, never as roman $P$.
    - $\mathfrak{F}$: Riemann surface or open sub-surface. Transcribe as `\mathfrak{F}`, never roman $F$.
    - $\mathfrak{M}$: Manifold or point set. Transcribe as `\mathfrak{M}`, never roman $M$.
    - $\mathfrak{U}$: Neighborhood (Umgebung). Transcribe as `\mathfrak{U}`, never roman $U$.
    - $\mathfrak{S}$: System or collection. Transcribe as `\mathfrak{S}`, never roman $S$.
  - Latin italic capitals ($P, Q, A, B, C$) are used for polynomials, points, or curve names.

- **Variables and Parameters**:
  - Standard complex variables: $z = x + iy$, $u = \xi + i\eta$, $w$, local uniformizing parameter $t$ or $\tau$.
  - Expansion coefficients: $A_0, A_1, A_2, \dots$, $a_0, a_1, \dots$, $c_n$.
  - Convergence radius: $r$, $r_0$, $R$.

## 2. Orthography and Prose Typography

- **Orthography**:
  - Follow the 1913 Teubner print faithfully: `Weierstraß'` (with final apostrophe), `daß`, `muß`, `läßt`, `Schluß`, `konvergiert`, `Koeffizienten`.
  - Do not modernize spelling or silently regularize author syntax.

- **Emphasis**:
  - Letterspaced emphasis (*Sperrung*) in the original print is rendered via `\emph{...}` (R20).
  - Both technical terms in Sperrung and author names in Sperrung use `\emph{...}`.

- **Quotation Marks**:
  - German low/high quotation marks are rendered as literal Unicode `„...“` (R22).

## 3. Formulas and Display Math

- **Display Math Wrapping (R16)**:
  - All standalone display formulas must be wrapped in `\[ ... \]`.
  - Multiline display equations must be enclosed in `\[ \begin{gathered} ... \end{gathered} \]` or `\[ \begin{aligned} ... \end{aligned} \]`. Never bare `\begin{align*}` or `\begin{gather*}`.

- **Equation Numbering (R5)**:
  - Tags are set on the right via `\tag{n}`, matching the original print: `\tag{1}`, `\tag{2}`, `\tag{3*}`.

- **Punctuation in Math**:
  - Preserved exactly as in the print: periods or commas ending displayed equations go inside the display math delimiters before `\]`.

## 4. Footnotes and Page Furniture (R15)

- In-text footnote calls use superscript: `${}^{1)}$`, `${}^{2)}$`.
- Footnotes are placed at the end of the text on the page where they appear, formatted as a paragraph starting with `\textbf{1)}`.
- Running heads, headers, and page signatures (`Weyl: Die Idee der Riemannschen Fläche`, `1`) are omitted.
