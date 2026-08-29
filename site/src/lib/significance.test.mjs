// Unit tests for the significance-note renderer (significance.js), run with `node --test`.
// The field is authored as plain prose, so the guard here is that its two bracket markers turn
// into the shared popover apparatus — and that everything else reaches the page as literal text.
import { test } from "node:test";
import assert from "node:assert/strict";
import { renderSignificance } from "./significance.js";

const SOURCES = [{ citation: "MacTutor, \"Gustav Roch\"", url: "https://example.org/roch" },
                 { citation: "An unlinked citation" }];
const NOTES = [{ label: "In modern notation",
                 text: "Roch's count is $\\ell(D)-\\ell(K-D)=\\deg D-p+1$." }];

test("a [n] marker becomes a superscript citation popover, linked when the source has a url", () => {
  const html = renderSignificance("Riemann had shown this.[1]", SOURCES, NOTES);
  assert.match(html, /<span class="pop cite" data-pagefind-ignore>/);
  assert.match(html, /<button type="button" class="pop-marker" aria-label="Citation 1">1<\/button>/);
  assert.match(html, /<a href="https:\/\/example\.org\/roch" rel="noopener">/);
});

test("a citation without a url renders its text with no link", () => {
  const html = renderSignificance("Stated here.[2]", SOURCES, NOTES);
  assert.match(html, /<span class="pop-content" role="note">An unlinked citation<\/span>/);
});

test("a [note n] marker becomes a labelled chip whose popover carries the note", () => {
  const html = renderSignificance("counts the same constants. [note 1]", SOURCES, NOTES);
  assert.match(html, /<span class="pop signote" data-pagefind-ignore>/);
  assert.match(html, /aria-label="Note: In modern notation">In modern notation<\/button>/);
  assert.match(html, /Roch's count is \$\\ell\(D\)-\\ell\(K-D\)=\\deg D-p\+1\$\./,
               "math is passed through untouched for the page's KaTeX pass");
});

test("markers with no matching entry are left as the literal text", () => {
  const html = renderSignificance("nothing here.[9] or [note 4]", SOURCES, NOTES);
  assert.match(html, /nothing here\.\[9\] or \[note 4\]/);
});

test("both marker kinds coexist in one paragraph", () => {
  const html = renderSignificance("A result.[1] [note 1] And on it goes.", SOURCES, NOTES);
  assert.equal((html.match(/class="pop cite"/g) || []).length, 1);
  assert.equal((html.match(/class="pop signote"/g) || []).length, 1);
});

test("prose is HTML-escaped, including inside a note and a citation", () => {
  const html = renderSignificance("a < b & <em>not markup</em>[1]",
    [{ citation: "<script>x</script>" }], NOTES);
  assert.match(html, /a &lt; b &amp; &lt;em&gt;not markup&lt;\/em&gt;/);
  assert.match(html, /&lt;script&gt;x&lt;\/script&gt;/);
  assert.ok(!html.includes("<script>"), "no raw tag may survive from the source text");
});

test("no significance renders as nothing at all", () => {
  assert.equal(renderSignificance(undefined, SOURCES, NOTES), "");
  assert.equal(renderSignificance("", SOURCES, NOTES), "");
});

test("markers still render when the lists are omitted entirely", () => {
  const html = renderSignificance("plain prose.[1] [note 1]");
  assert.match(html, /plain prose\.\[1\] \[note 1\]/);
});
