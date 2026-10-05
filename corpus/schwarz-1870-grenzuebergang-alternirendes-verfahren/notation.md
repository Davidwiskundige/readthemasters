# Mathematical notation and typography decisions: schwarz-1870-grenzuebergang-alternirendes-verfahren

These decisions are binding across the entire transcription of Hermann Amandus Schwarz's
*Ueber einen Grenzübergang durch alternirendes Verfahren*
(Vierteljahrsschrift der Naturforschenden Gesellschaft in Zürich, 15. Jahrgang, 3. Heft, 1870, pp. 272–286).
Treat this document as authoritative alongside `corpus/HOUSESTYLE.md`.

---

## Mathematical Symbols and Operators

- **Laplace operator (`\Delta`):**
  - Write `\Delta u = 0`.
  - The print sets an open triangle $\Delta$.

- **Partial derivatives (`\partial`):**
  - Write `\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} = 0`, `\frac{\partial u}{\partial x}`, `\frac{\partial u}{\partial y}`.
  - The 1870 print uses curved partial derivative symbols `\partial`.

- **Multiplication dot (`\cdot`):**
  - The print sets explicit centered dots in expressions such as `$g \cdot q$`, `$G \cdot q_1$`, `$G \cdot (q_1 \cdot q_2)^{n-1}$`.
  - Preserve `\cdot` faithfully wherever printed.

- **Domains, Boundaries, and Geometric Labels:**
  - Regions/domains: Italic capitals `$T$`, `$T_1$`, `$T_2$`, `$T^*$`.
  - Boundary arcs/curves: Italic `$L$`, `$L_0$`, `$L_1$`, `$L_2$`, `$L_3$`.
  - Points: Italic `$P$`.
  - Multi-letter boundary pieces/combinations are set as plain math-mode letters per HOUSESTYLE R1.

- **Indices and Sequences:**
  - Functions in the alternating sequence: `$u_1, u_2, \dots, u_{2n-1}, u_{2n}, u_{2n+1}$`.
  - Subscripts use standard math italics / numerals.

- **Elliptic Functions and Integrals (p. 285):**
  - Amplitude sine: `\sin\mathrm{am}\, Kz`, with modulus `$k = i$`.
  - Upper-bound indefinite integral: `\int^{Z_1} \frac{\sqrt{1 - Z_1^4}}{Z_1^2} \, dZ_1`.
  - Definite integral: `\int_0^{\frac{\pi}{2}} \sqrt{\sin \varphi} \, d\varphi`.
  - Inline integrals must include `\displaystyle\int` per HOUSESTYLE R2/R16.
  - Differentials carry a thin space: `\,dx`, `\,dy`, `\,ds`, `\,dz`, `\,dZ_1`, `\,d\varphi`.

- **Greek Letters:**
  - Phi: Curved phi `\varphi`. *Forbidden:* `\phi`.
  - Delta: Capital `\Delta`.

- **Formulas and Displays:**
  - Standalone displays use `\[ ... \]` per HOUSESTYLE R16.
  - Multiline aligned displays are wrapped as `\[ \begin{aligned} ... \end{aligned} \]` or `\[ \begin{gathered} ... \end{gathered} \]`.
  - Periods and commas at the end of displayed equations are placed according to the print.

---

## Typography and Orthography

- **Antiqua Typeface:**
  - The journal is printed in Roman (Antiqua) typeface, not Fraktur.
  - Standard 19th-century German orthography is preserved verbatim:
    - `Ueber`, `alternirendes`, `convergirt`, `Constante`, `Theil`, `Werthe`, `daß`, `giebt`, `Cursivschrift`.
    - Do not modernize spellings.

- **Spaced Type (Sperrdruck):**
  - Proper names and emphasized terms set in spaced type (*Riemann*, *Dirichlet*, *Kronecker*, *Weber*, *Neumann*, *Weierstrass*, *Christoffel*, *Green*) are set with `\emph{...}`.

- **Em-dashes:**
  - Dashes in running text are transcribed as `---`.

- **Figures (HOUSESTYLE R30):**
  - The woodcut on p. 277 stands beside the paragraph beginning *"Es seien gegeben zwei Bereiche..."*.
  - Per R30, it is inserted before that paragraph:
    `\rmfigure{figures/fig-01.png}{}{Schematische Figur zweier sich überlappender Bereiche T_1 (Kreis) und T_2 (Quadrat) mit Schnittbereich T* und Randstücken L_0, L_1, L_2, L_3.}`

- **Page Markers:**
  - Every page transition carries `\origpage{N}` at the very beginning of text from that page.
