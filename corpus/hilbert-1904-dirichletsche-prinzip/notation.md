# Mathematical notation and typography decisions: hilbert-1904-dirichletsche-prinzip

These decisions are binding across the entire transcription of David Hilbert's
*Über das Dirichletsche Prinzip* (Mathematische Annalen, Band 59, 1904, pp. 161–186).
Treat this document as authoritative alongside `corpus/HOUSESTYLE.md`.

---

## Mathematical Symbols and Operators

- **Partial derivatives (`\partial`):**
  - Write `\frac{\partial u}{\partial x}`, `\frac{\partial u}{\partial y}`, `\frac{\partial^2 u}{\partial x^2}`, `\frac{\partial^2 u}{\partial y^2}`, `\frac{\partial^2 u}{\partial x \partial y}`.
  - The 1904 print uses the standard curved partial derivative symbol `\partial` throughout.
  - *Forbidden:* Do not write ordinary `d` for partial derivatives.

- **Laplace operator (`\Delta`):**
  - Write `\Delta u = 0`.

- **Limit operator (`L` / Limes):**
  - Hilbert writes an italic capital $L$ with the index condition underneath: `\underset{h=\infty}{L}` or `\underset{\substack{\varepsilon=0 \\ \eta=0}}{L}`.
  - *Forbidden:* Do not modernize to `\lim` or `\lim_{h \to \infty}`. The print sets $L$ and uses an equals sign `$h=\infty$`, never an arrow `\to`.

- **Natural logarithm (`l`):**
  - Hilbert writes an italic letter $l$ for the natural logarithm: e.g. `$a + a l r$`, `$A l \frac{r'}{r}$`, `$2 A l \frac{1}{r} + B$`.
  - Transcribe faithfully as `$l$` (e.g. `a + a l r` or `A l \frac{r'}{r}`).
  - *Forbidden:* Do not modernize to `\log` or `\ln`.

- **Difference operators (`d_x^{(\alpha)}`):**
  - Hilbert defines and uses finite difference operators: `$d_x^{(\alpha)}$`, `$d_x^{(\alpha')}$`, `$d_x^{(\alpha'')}$`, `$d_y^{(\beta)}$`, `$d_y^{(\beta')}$`, `$d_y^{(\beta'')}$`.
  - The variable is set as a subscript and the step parameter in parentheses as a superscript on italic $d$.

- **Integrals and double integrals:**
  - Iterated integrals with separate bounds: `\int_a^{a+l} \int_b^{b+l'}` or `\int_a^x \int_b^y`.
  - Double integrals over a region: `\int\!\!\int_{(G)}`, `\int\!\!\int_{(R)}`, `\int\!\!\int_{(F)}`, `\int\!\!\int_{(P_{\xi\eta})}`.
  - The domain of integration is enclosed in parentheses and placed below the integral signs: `_{(G)}`, `_{(R)}`, `_{(F)}`.
  - Inline integrals must include `\displaystyle\int` per HOUSESTYLE R2/R16.
  - Differentials carry a thin space `\,dx`, `\,dy`, `\,ds`, `\,d\xi`, `\,d\eta`. Where the print explicitly sets a multiplication dot before a differential (e.g. `\dots \cdot dx \cdot dy`), preserve `\cdot`.

- **Greek letters:**
  - **Theta:** The print uses curved theta $\vartheta$: write `\vartheta`, `\vartheta'`, `\vartheta''`, `\vartheta^*`, `\vartheta^{**}`. *Forbidden:* `\theta`.
  - **Kappa:** The parameter introduced on page 176 is curved kappa $\varkappa$: write `\varkappa` and `\varkappa\varrho`. *Forbidden:* Do not confuse with `$x$` or plain `$k$` or `\kappa`.
  - **Rho:** The auxiliary constant on pp. 175–176 is curved rho $\varrho$: write `\varrho`. *Forbidden:* Do not modernize to plain `\rho`.
  - **Phi:** Angle variable on pp. 185–186 is curved phi $\varphi$: write `\varphi`. *Forbidden:* `\phi`.
  - **Omega:** Auxiliary function $\omega_h = u_h - u$: write `\omega_h`.

- **Inequalities (`\leqq` and `\geqq`):**
  - The print predominantly uses double-barred inequalities $\leqq$ and $\geqq$: write `\leqq` and `\geqq`.
  - Where the print sets a single bar (e.g. top of page 165, and $p > 0$ on page 184), transcribe faithfully as printed (`\le`, `<`).

- **Equation numbering:**
  - Standard numbered equations: `\tag{1}`, `\tag{2}`, ..., `\tag{14}` inside `\[ ... \]`.
  - Roman-numeral equations in Hilfssatz 1: `\tag{I}`, `\tag{II}`, `\tag{III}`.

---

## Typography and Orthography

- **Antiqua German orthography:**
  - The text is printed in Antiqua (Roman) type, not Fraktur.
  - Preserves standard German `ß`: `daß`, `muß`, `Schlußweise`, `schließen`, `gleichmäßig`, `Größe`.
  - Archaic German spelling is preserved verbatim: `Variabeln` (with el), `differentiierbar`, `willkürlicher`, `Konstante`.

- **Headings:**
  - Paper title: `\section*{Über das Dirichletsche Prinzip.}`
  - Sections: `\subsection*{\S~1. \\ Darlegung des Problems.}` through `\S~10.`.
  - Preserves exact punctuation of section headings (e.g. final period).

- **Editorial annotations (`\ednote`):**
  - Document all compositor errors with `\ednote{...}` per HOUSESTYLE R4.
  - Strictly observe R18: no curly braces inside `\ednote` prose.
