import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lintMath } from './lint-math.mjs';

test('valid inline and display math passes with zero violations', () => {
  const tex = `
Here is inline math $x^2 + y^2 = z^2$ and another $\\frac{a}{b}$.
\\[
  \\begin{aligned}
    a &= b + c \\\\
    d &= e
  \\end{aligned}
\\]
`;
  const vios = lintMath(tex);
  assert.equal(vios.length, 0);
});

test('catches KaTeX syntax errors in inline and display math', () => {
  const inlineBad = 'Formula $\\frac{1}$ is missing an argument.';
  const inlineVios = lintMath(inlineBad);
  assert.equal(inlineVios.length, 1);
  assert.equal(inlineVios[0].type, 'inline-math');
  assert.match(inlineVios[0].error, /KaTeX parse error/i);

  const displayBad = '\\[ \\sqrt[ {x} \\]';
  const displayVios = lintMath(displayBad);
  assert.equal(displayVios.length, 1);
  assert.equal(displayVios[0].type, 'display-math');
  assert.match(displayVios[0].error, /KaTeX parse error/i);
});

test('catches unbalanced/unclosed dollar delimiters', () => {
  const tex = 'This formula $x + y = z was never closed.';
  const vios = lintMath(tex);
  assert.equal(vios.length, 1);
  assert.equal(vios[0].type, 'delimiter-unbalanced');
  assert.match(vios[0].error, /unclosed/i);
});

test('escaped dollars in prose do not trigger delimiter violations', () => {
  const tex = 'It cost \\$5 to buy $x$ items and \\$10 for the rest.';
  const vios = lintMath(tex);
  assert.equal(vios.length, 0);
});

test('catches bare display math environments outside \\[ ... \\] (HOUSESTYLE R16)', () => {
  const texAlign = `
\\begin{align*}
  a &= b \\\\
  c &= d
\\end{align*}
`;
  const viosAlign = lintMath(texAlign);
  assert.ok(viosAlign.length >= 1);
  assert.equal(viosAlign[0].type, 'display-wrap');
  assert.match(viosAlign[0].error, /R16/);

  const texGather = `
\\begin{gather*}
  x + y = z
\\end{gather*}
`;
  const viosGather = lintMath(texGather);
  assert.ok(viosGather.length >= 1);
  assert.equal(viosGather[0].type, 'display-wrap');
  assert.match(viosGather[0].error, /R16/);
});

test('catches apparatus macros inside math mode', () => {
  const apparatusCases = [
    { tex: 'Here is $\\uncertain{x}$ in inline math.', macro: '\\uncertain' },
    { tex: 'Here is $\\origpage{42}$ in inline math.', macro: '\\origpage' },
    { tex: 'Here is $\\ednote{misprint}$ in inline math.', macro: '\\ednote' },
    { tex: 'Here is $\\illegible$ in inline math.', macro: '\\illegible' },
    { tex: '\\[ x + \\rmfigure{fig.png}{1}{alt} = y \\]', macro: '\\rmfigure' },
  ];

  for (const tc of apparatusCases) {
    const vios = lintMath(tc.tex);
    assert.ok(vios.length >= 1, `Expected violation for ${tc.macro}`);
    assert.equal(vios[0].type, 'apparatus-in-math');
    assert.match(vios[0].error, /Apparatus macro/);
  }
});

test('ignores commented-out LaTeX lines', () => {
  const tex = `
% Here is a broken formula $\\frac{1}$
% And a bare environment:
% \\begin{align*}
%   x = 1
% \\end{align*}
Real prose with clean math $x = 1$.
`;
  const vios = lintMath(tex);
  assert.equal(vios.length, 0);
});
