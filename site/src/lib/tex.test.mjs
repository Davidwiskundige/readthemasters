// Unit tests for the reader's LaTeX-body -> HTML transform (tex.js), run with `node --test`.
// Zero dependencies (Node's built-in test runner). These guard the text-level niceties — the
// class of bug where a LaTeX control sequence leaks into the rendered prose as a literal backslash.
import { test } from "node:test";
import assert from "node:assert/strict";
import { texToHtml } from "./tex.js";

// The transform keeps only what is between \begin{document}...\end{document}; wrap a bare body.
const render = (body) => texToHtml(`\\begin{document}\n${body}\n\\end{document}`);

test("control space \\ after an abbreviation renders as a plain space, no backslash", () => {
  const html = render("dum scil.\\ spatiolum describit.");
  assert.match(html, /scil\. spatiolum/);
  assert.ok(!html.includes("scil.\\"), "the backslash must not leak into the text");
});

test("control space resolves inside \\emph and next to ~ and \\&", () => {
  const html = render("[Vide \\emph{Apr.\\ pag.}~198, \\& 1690]");
  assert.match(html, /<em>Apr\. pag\.<\/em>/); // \ inside \emph resolved
  assert.match(html, /198, &amp; 1690/);       // ~ -> space, \& -> &
  assert.ok(!html.includes("\\"), "no stray backslash anywhere");
});

test("several control spaces on one line (v.\\ g.\\ ) all resolve", () => {
  const html = render("determinentur. Sit, v.\\ g.\\ tunc sequitur.");
  assert.match(html, /Sit, v\. g\. tunc/);
});

test("a control space inside math is preserved for KaTeX, not collapsed by the text pass", () => {
  const html = render("the spacing $a\\ b$ is math");
  assert.match(html, /\$a\\ b\$/); // math span passes through verbatim
});

test("em-dash, curly quotes and \\& still work alongside the control-space rule", () => {
  const html = render("Leibnitius---quem ``Auctor'' \\& Amicus vocat.");
  assert.match(html, /Leibnitius—quem “Auctor” &amp; Amicus/);
});

test("\\S renders as the section sign §, in a heading and a cross-reference", () => {
  const html = render("\\subsection*{\\S.~I. Ueber die Form.}\n\nNach (\\S.~II.) folgt das.");
  assert.match(html, /<h3[^>]*>§\. I\. Ueber die Form\.<\/h3>/); // ~ -> space, \S -> §
  assert.match(html, /Nach \(§\. II\.\) folgt/);
  assert.ok(!html.includes("\\S"), "the \\S backslash must not leak into the text");
});

test("\\S does not eat a following control word or math \\Sigma", () => {
  const html = render("value $\\Sigma x$ and \\S 4 following.");
  assert.match(html, /\$\\Sigma x\$/); // math \Sigma untouched (stashed)
  assert.match(html, /§ 4 following/); // text \S -> §
});
