// Unit tests for the formula index's page attribution (mathindex.js), run with `node --test`.
import { test } from "node:test";
import assert from "node:assert/strict";
import { extractFormulas } from "./mathindex.js";

const doc = (body) => `\\begin{document}\n${body}\n\\end{document}`;

test("a formula takes the page of the last marker before it, arabic as a number", () => {
  const f = extractFormulas(doc("\\origpage{12}\nSei $x^{2}$ gleich."));
  assert.equal(f.length, 1);
  assert.equal(f[0].page, 12);
});

test("a formula on a roman front-matter page keeps the page as printed", () => {
  const f = extractFormulas(doc("\\origpage{vii}\nvon $x + iy$.\n\n\\origpage{1}\n\\[ w = f(z) \\]"));
  assert.deepEqual(f.map((x) => x.page), ["vii", 1]);
});
