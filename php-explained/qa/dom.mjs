// Fast interaction regression check. Focus and scrolling are instrumented.
import {parseHTML} from 'linkedom';
import {fileURLToPath} from 'node:url';
import vm from 'node:vm';
import fs from 'node:fs';
import assert from 'node:assert/strict';

const file = fileURLToPath(new URL('../index.html', import.meta.url));
const html = fs.readFileSync(file, 'utf8');
const {document, window: domWindow} = parseHTML(html);
let focused = '', scrolled = 0, printed = false, focusCount = 0;
let activeEl = null;
const focusOptions = [];
Object.defineProperty(document, 'activeElement', {get: () => activeEl});
domWindow.HTMLElement.prototype.focus = function (options) {
  focused = this.id; activeEl = this; focusCount++; focusOptions.push(options);
};
domWindow.HTMLElement.prototype.scrollIntoView = function () { scrolled++; };
const window = {
  matchMedia: () => ({matches: true}),
  scroll() { scrolled++; }, scrollTo() { scrolled++; }, scrollBy() { scrolled++; },
  print() { printed = true; }
};
const navigator = {clipboard: {async writeText(text) { navigator.copied = text; }}};
const $ = id => document.getElementById(id);
function select(id, value) {
  for (const option of $(id).querySelectorAll('option')) option.removeAttribute('selected');
  $(id).querySelector('option[value="' + value + '"]').setAttribute('selected', '');
  $(id).onchange();
}
function click(id) {
  assert(!$(id).disabled, `${id} unexpectedly disabled`);
  assert(!$(id).hidden, `${id} unexpectedly hidden`);
  activeEl = $(id);
  focused = id;
  $(id).click();
}
function assertVersion(repaired) {
  assert.equal($('badge').textContent, repaired ? 'Repaired PHP' : 'Original PHP');
  assert.equal($('storyStage').dataset.version, repaired ? 'repaired' : 'original');
  assert.equal($('original').getAttribute('aria-pressed'), String(!repaired));
  assert.equal($('repaired').getAttribute('aria-pressed'), String(repaired));
  assert.equal($('badgeDetail').textContent, repaired ? 'After the security update' : 'Before the security update');
}

assert($('storyLab').hidden);
assert($('quizPanel').hidden);
assert($('copyActions').hidden);
assert(!$('interactiveNotice').hidden);
// LinkeDOM does not select the first option automatically as browsers do.
for (const selectEl of document.querySelectorAll('select')) selectEl.querySelector('option').selected = true;
vm.runInNewContext(html.match(/<script>([\s\S]*?)<\/script>/)[1], {document, window, navigator});
assert(!$('storyLab').hidden);
assert(!$('quizPanel').hidden);
assert(!$('copyActions').hidden);
assert($('interactiveNotice').hidden);

for (const story of ['oom', 'stale']) {
  click(story);
  assert($('back').disabled);
  assert.equal($(story).getAttribute('aria-pressed'), 'true');
  assert.equal($(story === 'oom' ? 'stale' : 'oom').getAttribute('aria-pressed'), 'false');
  for (let index = 0; index < 4; index++) {
    assertVersion(false);
    const originalScene = $('workspace').innerHTML;
    const originalTitle = $('stepTitle').textContent;
    const beforeToggle = focusCount;
    click('repaired');
    assertVersion(true);
    assert.equal(focusCount, beforeToggle, 'Version comparison must not steal focus');
    assert.match($('counter').textContent, new RegExp(`STEP ${index + 1} OF 4`));
    if (index >= 2) {
      assert.notEqual($('workspace').innerHTML, originalScene);
      assert.notEqual($('stepTitle').textContent, originalTitle);
      assert.match($('outcome').className, /safe/);
    }
    click('original');
    assertVersion(false);
    assert.equal($('workspace').innerHTML, originalScene);
    if (index < 3) {
      assert($('patch').hidden);
      click('next');
      assert.equal(focused, index === 2 ? 'patch' : 'next');
      assert.notEqual($('workspace').innerHTML, originalScene);
    }
  }
  assert($('next').hidden);
  assert(!$('patch').hidden);
  assert.equal(focused, 'original');
  assert.match($('outcome').className, /danger/);
  click('back');
  assert(!$('next').hidden);
  assert($('patch').hidden);
  click('back');
  click('back');
  assert($('back').disabled);
  assert.equal(focused, 'next');
  for (let index = 0; index < 3; index++) click('next');
  click('patch');
  assert.equal(focused, 'next');
  assertVersion(true);
  assert.match($('counter').textContent, /STEP 1 OF 4/);
  for (let index = 0; index < 3; index++) click('next');
  assert.match($('outcome').className, /safe/);
  assert.match($('workspace').textContent, story === 'oom' ? /No invalid cleanup/ : /Fresh, valid state/);
  click('patch');
  assertVersion(false);
  click('next');
  click('repaired');
  click('reset');
  assertVersion(true);
  assert.match($('counter').textContent, /STEP 1 OF 4/);
  assert($('back').disabled);
}
assert.equal(scrolled, 0, 'Story controls must never scroll the page');
assert(focusOptions.length > 0, 'Final-step focus transfers should be exercised');
assert(focusOptions.every(options => options?.preventScroll === true), 'Story focus transfers must prevent scrolling');
assert.equal(document.querySelectorAll('.chapter-number, .story-card-number, .flow-index').length, 0);
for (const id of ['copySizer', 'workspaceSizer', 'outcomeSizer']) {
  assert.equal($(id).getAttribute('aria-hidden'), 'true');
  assert($(id).hasAttribute('inert'));
}

for (const [value, result] of Object.entries({visitor: 'server operator', owner: 'hosting provider', admin: 'Inventory, update'})) {
  select('role', value);
  assert($('roleResult').textContent.includes(result));
}
for (const [branch, fixed] of Object.entries({'8.5': '8.5.12', '8.4': '8.4.27', '8.3': '8.3.36', '8.2': '8.2.35'})) {
  select('branch', branch);
  for (const level of ['before', 'fixed']) {
    select('level', level);
    assert($('versionResult').textContent.includes(fixed));
    assert($('versionResult').textContent.includes(level === 'before' ? 'need the repair' : 'has deployed the update'));
  }
}
for (const branch of ['old', 'unknown']) {
  select('branch', branch);
  assert($('level').disabled);
}
select('branch', '8.5');
assert(!$('level').disabled);

for (const answers of [[0, 0, 0], [1, 1, 1], [2, 2, 2], [1, 0, 2]]) {
  let score = 0;
  assert($('quizNext').disabled);
  for (const [index, answer] of answers.entries()) {
    if (answer === [1, 0, 2][index]) score++;
    $('answers').children[answer].click();
    assert([...$('answers').children].every(element => element.disabled));
    assert.equal($('answers').querySelectorAll('.is-correct').length, 1);
    assert.equal($('answers').querySelectorAll('.answer-result').length, 1);
    assert($('feedback').textContent.length > 40);
    click('quizNext');
    assert.equal(focused, 'question');
  }
  assert($('question').textContent.includes(`${score} out of 3`));
  assert($('quizNext').hidden);
  const beforeReset = focusCount;
  click('quizReset');
  assert.equal(focusCount - beforeReset, 1);
  assert.equal($('answers').children.length, 3);
  assert.equal($('progress').value, 0);
}

await $('copy').onclick();
assert.equal(navigator.copied, $('explanation').textContent);
assert.equal($('copyStatus').textContent, 'Explanation copied.');
navigator.clipboard.writeText = async () => { throw Error('Denied'); };
await $('copy').onclick();
assert.match($('copyStatus').textContent, /Select the explanation text/);
click('print');
assert(printed);
for (const anchor of document.querySelectorAll('a[href^="#"]')) {
  const id = anchor.getAttribute('href').slice(1);
  if (id) assert($(id), `Missing anchor ${id}`);
}
const ids = [...document.querySelectorAll('[id]')].map(element => element.id);
assert.equal(new Set(ids).size, ids.length);
assert.equal(document.documentElement.lang, 'en-GB');
console.log('PASS: no story scrolling, stable control focus, unnumbered sections, both stories, version comparison at every step, replay/back/restart, all audience/version choices, all nine quiz answers, scoring/reset, copy success/denial, print dispatch, anchors and initial no-JavaScript state.');
