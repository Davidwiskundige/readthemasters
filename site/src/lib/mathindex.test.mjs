// Unit tests for the formula index's page attribution (mathindex.js), run with `node --test`.
import { test } from "node:test";
import assert from "node:assert/strict";
import { extractFormulas, buildIndex, expandEntry } from "./mathindex.js";

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

const work = {
  url: "/works/w/",
  title: "Opus",
  language_label: "Latin",
  original_tex: doc("$a$\n\\origpage{3}\nSit $x^{2}$ et $x^2$.\n\\[ y = 1 \\]"),
  translations: { en: { label: "English", tex: doc("\\origpage{3}\nLet $x^{2}$.") } },
};

test("the index stores each work once and expands a hit to its URL, title and label", () => {
  const idx = buildIndex([work]);
  assert.equal(idx.works.length, 1);
  const hits = idx.entries.map((e) => expandEntry(idx, e));
  assert.deepEqual(hits.map((h) => [h.url, h.where]), [
    ["/works/w/#original", "Original (Latin)"],
    ["/works/w/#p-3", "Original (Latin) · page 3"],
    ["/works/w/#p-3", "Original (Latin) · page 3"],
    ["/works/w/#en-p-3", "English translation · page 3"],
  ]);
  assert.equal(hits[1].title, "Opus");
  assert.equal(hits[2].display, true);
  assert.deepEqual(hits[2].tokens, ["y", "=", "1"]);
});

test("the same formula twice on one page of one artifact is indexed once", () => {
  const idx = buildIndex([work]);
  const xs = idx.entries.filter((e) => e[5].join(" ") === "x ^ 2");
  assert.deepEqual(xs.map((e) => [e[1], e[2]]), [["original", 3], ["en", 3]]);
});
