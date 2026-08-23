// Unit tests for the display-math fitting rule (fitmath.js), run with `node --test`.
// Zero dependencies (Node's built-in test runner). The measuring pass that feeds this function
// cannot be tested here — it needs a real layout engine — so these pin the arithmetic instead,
// including the boundary comparisons, which is where a "harmless" refactor would silently drift.
import { test } from "node:test";
import assert from "node:assert/strict";
import { decideFit } from "./fitmath.js";

const COL = 1000; // stand-in text-column width

test("a formula narrower than the column with no tag gets neither class", () => {
  assert.deepEqual(decideFit(COL, 400, null), { wide: false, tagBelow: false });
});

test("a formula wider than the column is marked wide", () => {
  assert.deepEqual(decideFit(COL, 1400, null), { wide: true, tagBelow: false });
});

test("a formula with no tag never gets tag-below, however wide it is", () => {
  // No number to collide with, so the tag rule must not fire even far past the column.
  assert.equal(decideFit(COL, 99999, null).tagBelow, false);
});

test("a formula that fits but cannot share its line with the tag gets tag-below only", () => {
  // 700 fits in 1000, but 700 + 2*(100+8) = 916 ... still fits. Push the formula to 850:
  // 850 + 216 = 1066 > 1000, so the number drops below while the formula stays un-wide.
  const fit = decideFit(COL, 850, 100);
  assert.deepEqual(fit, { wide: false, tagBelow: true });
});

test("a formula can be both wide and tag-below", () => {
  assert.deepEqual(decideFit(COL, 1400, 100), { wide: true, tagBelow: true });
});

test("the tag allowance counts twice, keeping a centred formula centred", () => {
  // math + 2*(tagWidth + 8) is the threshold: the number is pinned at one edge, and the same
  // width has to stay clear at the opposite edge or the formula is no longer centred.
  const tagWidth = 100;
  const allowance = 2 * (tagWidth + 8); // 216
  assert.equal(decideFit(COL, COL - allowance - 1, tagWidth).tagBelow, false);
  assert.equal(decideFit(COL, COL - allowance + 1, tagWidth).tagBelow, true);
});

test("boundary: math exactly equal to the column is not wide (strictly greater)", () => {
  assert.equal(decideFit(COL, COL, null).wide, false);
  assert.equal(decideFit(COL, COL + 0.5, null).wide, true);
});

test("boundary: math + 2*(tag+gutter) exactly equal to the column is not tag-below", () => {
  const tagWidth = 100;
  const math = COL - 2 * (tagWidth + 8); // exactly fills the column with both allowances
  assert.equal(decideFit(COL, math, tagWidth).tagBelow, false);
  assert.equal(decideFit(COL, math + 0.5, tagWidth).tagBelow, true);
});

test("a zero-width tag still costs the gutter on both sides", () => {
  // An empty tag element is not the same as no tag: it is present, so it reserves the gutter.
  assert.equal(decideFit(COL, COL - 16, 0).tagBelow, false); // 2*8 = 16, exactly fills
  assert.equal(decideFit(COL, COL - 15, 0).tagBelow, true);
  assert.equal(decideFit(COL, COL - 15, null).tagBelow, false); // no tag at all: never fires
});

test("fractional widths from getBoundingClientRect are compared, not rounded", () => {
  assert.equal(decideFit(1000, 1000.4, null).wide, true);
  assert.equal(decideFit(1000, 999.6, null).wide, false);
});
