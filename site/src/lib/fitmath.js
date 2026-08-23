// The rule that decides how a display equation shares its line with its \tag{n}.
//
// Extracted from the measuring pass in works/[id].astro so the arithmetic can be unit-tested:
// the pass itself reads real layout geometry, which no DOM stub can supply (jsdom reports zero
// for every getBoundingClientRect), but the decision made *from* those numbers is pure.
//
// The two outcomes are styled in global.css:
//   wide       - the formula is wider than its column, so it is left-aligned and the equation's
//                own horizontal scroll starts at the beginning of the formula rather than with
//                its left half already cut off.
//   tag-below  - the number cannot sit beside the formula, so it drops to its own right-aligned
//                line underneath.

// Gap kept between a formula and its equation number, in px.
const TAG_GUTTER = 8;

/**
 * @param {number} room     Available width of the equation box (its clientWidth).
 * @param {number} math     Width of the rendered formula, excluding its tag.
 * @param {number|null} tagWidth  Width of the `\tag{n}` element, or null when the equation has none.
 * @returns {{wide: boolean, tagBelow: boolean}}
 */
export function decideFit(room, math, tagWidth) {
  // A centred formula needs the number's width clear on *both* sides to stay centred, hence 2x:
  // the tag is pinned at one edge, and the same amount has to stay free at the opposite edge.
  const tagW = tagWidth === null ? 0 : tagWidth + TAG_GUTTER;
  return {
    wide: math > room,
    tagBelow: tagWidth !== null && math + 2 * tagW > room,
  };
}
