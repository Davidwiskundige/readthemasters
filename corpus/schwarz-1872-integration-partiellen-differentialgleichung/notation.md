# Mathematical notation and typography decisions: schwarz-1872-integration-partiellen-differentialgleichung

These decisions are binding across the entire transcription of Hermann Amandus Schwarz's
*Zur Integration der partiellen Differentialgleichung $\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} = 0$*
(Journal für die reine und angewandte Mathematik, Band 74, 1872, pp. 218–253).
Treat this document as authoritative alongside `corpus/HOUSESTYLE.md`.

---

## Mathematical Symbols and Operators

- **Laplace operator (`\Delta`):**
  - Write `\Delta u = 0`.
  - The print sets an open triangle $\Delta$.

- **Partial derivatives (`\partial`):**
  - Write `\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} = 0`, `\frac{\partial u}{\partial x}`, `\frac{\partial u}{\partial y}`, `\frac{\partial u}{\partial r}`, `\frac{\partial u}{\partial \varphi}`.
  - The 1872 print uses curved partial derivative symbols `\partial`.

- **Greek Letters:**
  - Phi: Curved phi `\varphi`. *Forbidden:* `\phi`.
  - Psi: `\psi`.
  - Theta: `\vartheta`.
  - Delta: `\Delta`.
  - Pi: `\pi`.

- **Multiplication dot (`\cdot`):**
  - The print sets explicit centered dots in expressions such as `$r^\mu \cdot [u(r, \varphi)]$`, `$2 \cdot \pi$`.
  - Preserve `\cdot` faithfully wherever printed.

- **Absolute Values / Brackets:**
  - The print frequently denotes the absolute value of a function using square brackets, e.g. `$[u(r, \varphi)] < g$`.
  - Transcribe faithfully with brackets `$[u(r, \varphi)]$` exactly as printed; do not modernize to vertical bars.

- **Integrals and Differentials:**
  - Definite integrals carry explicit limits: `\int_0^{2\pi}`.
  - Inline integrals must include `\displaystyle\int` per HOUSESTYLE R2/R16.
  - Differentials carry a thin space: `\,dx`, `\,dy`, `\,dr`, `\,d\varphi`, `\,d\psi`, `\,ds`.

- **Formulas and Displays:**
  - Standalone displays use `\[ ... \]` per HOUSESTYLE R16.
  - Multiline aligned displays are wrapped as `\[ \begin{aligned} ... \end{aligned} \]` or `\[ \begin{gathered} ... \end{gathered} \]`.
  - Periods and commas at the end of displayed equations are placed according to the print.
  - Numbered equations use `\tag{...}` matching printed labels `(1.)`, `(2.)`, `(I.)`, etc.

---

## Typography and Orthography

- **Antiqua Typeface:**
  - The journal is printed in Roman (Antiqua) typeface, not Fraktur.
  - Standard 19th-century German orthography is preserved verbatim:
    - `Function`, `Theil`, `theilweise`, `Werthe`, `Curven`, `Constante`, `convergirt`, `Reellen`, `Grenz- und Unstetigkeitsbedingungen`, `Mittheilung`, `Hülfs-`, `giebt`, `daß`/`dass`.
    - Do not modernize spellings.

- **Spaced Type (Sperrdruck):**
  - Proper names and emphasized terms set in spaced type (*Riemann*, *Dirichlet*, *Weierstrass*, *Prym*, *Neumann*, *Heine*, *Christoffel*, *Gauss*, *Poisson*, *Clebsch*) are set with `\emph{...}`.

- **Em-dashes:**
  - Dashes in running text are transcribed as `---`.

- **Footnotes:**
  - Footnotes use standard `\footnote{...}`.
  - Footnote markers in the original (*), **), etc. are converted to standard LaTeX footnotes.

- **Page Markers:**
  - Every page transition carries `\origpage{N}` at the very beginning of text from that page.
  - A page opening mid-sentence must have no blank line following `\origpage{N}`.
