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
let reducedMotion = true;
const focusOptions = [];
Object.defineProperty(document, 'activeElement', {get: () => activeEl});
domWindow.HTMLElement.prototype.focus = function (options) {
  focused = this.id; activeEl = this; focusCount++; focusOptions.push(options);
};
domWindow.HTMLElement.prototype.scrollIntoView = function () { scrolled++; };
const window = {
  matchMedia: () => ({matches: reducedMotion}),
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
assert(!$('bridgeControls').hidden);

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
    assert.equal($('comparison').dataset.kind, index < 2 ? 'shared' : 'repaired');
    assert.match($('comparisonTitle').textContent, index < 2 ? /Both versions behave the same/ : /repair changes/);
    if (index < 2) assert.match($('comparisonDescription').textContent, /step three/);
    if (index >= 2) {
      assert.notEqual($('workspace').innerHTML, originalScene);
      assert.notEqual($('stepTitle').textContent, originalTitle);
      assert.match($('outcome').className, /safe/);
    }
    click('original');
    assertVersion(false);
    assert.equal($('comparison').dataset.kind, index < 2 ? 'shared' : 'original');
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
for (const id of ['copySizer', 'workspaceSizer', 'outcomeSizer', 'comparisonSizer', 'primarySizer', 'bridgeSizer', 'storyMotion']) {
  assert.equal($(id).getAttribute('aria-hidden'), 'true');
  assert($(id).hasAttribute('inert'));
}

// Exercise actual transition logic as well as the reduced-motion path.
reducedMotion = false;
click('stale');
click('next');
const retainedNote = $('workspace').querySelector('.sticky');
assert(retainedNote.classList.contains('reference-arrives'));
click('next');
assert.equal($('workspace').querySelector('.sticky'), retainedNote, 'The note must stay while the folder leaves');
assert($('storyMotion').querySelector('.folder'), 'The removed folder must have an exit illustration');
assert(!$('storyMotion').querySelector('.sticky'), 'The retained note must not leave with the folder');
$('storyMotion').querySelector('.folder').dispatchEvent(new domWindow.Event('animationend', {bubbles: true}));
assert.equal($('storyMotion').children.length, 0);
click('next');
assert.equal($('workspace').querySelector('.sticky'), retainedNote);
assert($('workspace').querySelector('.folder').classList.contains('object-arrives'));
click('repaired');
assert(!$('workspace').querySelector('.sticky'));
assert($('storyMotion').querySelector('.sticky'), 'The repair must clear the old note visibly');
for (let index = 0; index < 30; index++) {
  click(index % 2 ? 'original' : 'repaired');
  assert($('storyMotion').children.length <= 1, 'Rapid changes must replace old animations');
}
reducedMotion = true;
click('original');
assert.equal($('storyMotion').children.length, 0, 'Reduced motion must omit departure animations');

// Every definition opens, closes, restores focus and leaves story state intact.
for (const key of ['request', 'server', 'memory', 'worker', 'reference', 'cleanup', 'runtime', 'use-after-free']) {
  const termEl = [...document.querySelectorAll('.term')].find(el => el.dataset.term === key && !el.closest('[inert]'));
  assert(termEl, `Missing definition trigger: ${key}`);
  const before = $('counter').textContent;
  termEl.click();
  assert(!$('definitionPanel').hidden);
  assert.equal(termEl.getAttribute('aria-expanded'), 'true');
  assert.equal(activeEl, $('definitionClose'));
  assert($('definitionText').textContent.length > 70);
  assert.equal($('definitionTitle').textContent.toLowerCase(), key);
  click('definitionClose');
  assert($('definitionPanel').hidden);
  assert.equal(termEl.getAttribute('aria-expanded'), 'false');
  assert.equal(activeEl, termEl);
  assert.equal($('counter').textContent, before);
}
const termEl = $('stepText').querySelector('.term');
termEl.click();
const escape = new domWindow.Event('keydown', {bubbles: true, cancelable: true});
Object.defineProperty(escape, 'key', {value: 'Escape'});
document.dispatchEvent(escape);
assert(escape.defaultPrevented);
assert($('definitionPanel').hidden);
assert.equal(activeEl, termEl);
termEl.click();
$('storiesTitle').click();
assert($('definitionPanel').hidden, 'Clicking outside must dismiss the definition');
termEl.click();
click('reset');
assert($('definitionPanel').hidden, 'Changing a story must dismiss its old definition');

for (const path of ['prepared', 'ordinary', 'prepared', 'ordinary']) {
  click(path);
  assert.equal($('bridgeState').dataset.path, path);
  assert.equal($(path).getAttribute('aria-pressed'), 'true');
  assert.equal($(path === 'ordinary' ? 'prepared' : 'ordinary').getAttribute('aria-pressed'), 'false');
  assert.equal($('bridgeState').querySelectorAll('li').length, 3);
  assert.match($('bridgeState').querySelector('li:last-child h4').textContent, path === 'prepared' ? /attacker redirects/ : /may crash/);
}
assert.equal(scrolled, 0, 'New interactions must never invoke scrolling');
assert(focusOptions.every(options => options?.preventScroll === true), 'Definition focus must also prevent scrolling');

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
console.log('PASS: both stories, repair explanations, retained sticky note and folder departures, rapid transitions, reduced motion, all eight definitions/close/Escape/outside dismissal, both attack paths, zero scroll API calls, safe focus, every existing control, quiz path, copy/print, anchors and initial no-JavaScript state.');
