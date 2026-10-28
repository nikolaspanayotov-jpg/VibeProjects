/**
 * Execute the page's real inline script against LinkeDOM and dispatch DOM events.
 * Run: npm install --prefix tests && npm test --prefix tests
 * Offline: LINKEDOM_WORKER_PATH=/path/to/linkedom/worker.js node tests/control_runtime.mjs
 *
 * This is a DOM/event regression test, not a browser or visual test. LinkeDOM
 * supplies parsing, selectors, nodes and event dispatch. The small adapters below
 * model missing browser APIs: location/hash changes, form state, focus/selection,
 * reflected details.open, animation frames, clipboard and the print lifecycle.
 * Native click defaults, keyboard activation, layout and OS dialogs are NOT tested.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath, pathToFileURL} from 'node:url';

const {parseHTML} = await import(process.env.LINKEDOM_WORKER_PATH
  ? pathToFileURL(path.resolve(process.env.LINKEDOM_WORKER_PATH)).href
  : 'linkedom/worker');
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const html = fs.readFileSync(process.env.RFRM_HTML_PATH || path.join(root, 'index.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(script, 'The generated page contains its inline application script');
const passed = [];
function pass(label) { passed.push(label); console.log('PASS ' + label); }

function harness(initialHash = '', baseURL = 'https://example.test/rfrm-debunked/') {
  const {document, window: domWindow} = parseHTML(html);
  const location = new URL(baseURL + initialHash);
  const window = new domWindow.EventTarget();
  const navigator = {};
  let activeElement = document.body;
  const frames = [];
  const scrolls = [];
  Object.defineProperty(document, 'activeElement', {get: () => activeElement});
  for (const el of document.querySelectorAll('*')) {
    el.focus = () => { activeElement = el; };
    el.scrollIntoView = () => { scrolls.push(el.id); };
    if (el.localName === 'details') Object.defineProperty(el, 'open', {
      get: () => el.hasAttribute('open'),
      set: value => el.toggleAttribute('open', !!value)
    });
    if (el.localName === 'select') Object.defineProperty(el, 'value', {
      get: () => el.querySelector('option[selected]')?.value || el.querySelector('option')?.value || '',
      set: value => el.querySelectorAll('option').forEach(option => option.toggleAttribute('selected', option.value === value))
    });
    if (el.localName === 'a') Object.defineProperty(el, 'hash', {
      get: () => new URL(el.getAttribute('href'), location).hash
    });
    if (el.localName === 'input') el.select = () => {
      el.selectionStart = 0;
      el.selectionEnd = el.value.length;
    };
  }
  const sandbox = {document, window, location, navigator, URL,
    requestAnimationFrame: callback => { frames.push(callback); }, console};
  vm.runInNewContext(script, sandbox, {filename: 'index.html:inline-script'});
  const $ = selector => {
    const el = document.querySelector(selector);
    assert.ok(el, 'Expected element: ' + selector);
    return el;
  };
  const all = selector => Array.from(document.querySelectorAll(selector));
  const event = (el, type) => {
    const e = new domWindow.Event(type, {bubbles: true, cancelable: true});
    el.dispatchEvent(e);
    return e;
  };
  const flush = () => { while (frames.length) frames.shift()(); };
  const hash = value => {
    location.hash = value;
    event(window, 'hashchange');
    flush();
  };
  const click = selector => event(typeof selector === 'string' ? $(selector) : selector, 'click');
  const search = value => { $('#query').value = value; event($('#query'), 'input'); };
  const visible = () => all('.policy:not([hidden])').map(el => el.id);
  const tick = () => new Promise(resolve => setImmediate(resolve));
  const snapshot = () => JSON.stringify({
    query: $('#query').value,
    topic: $('#topic-select').value,
    evidence: $('#evidence-select').value,
    shortcuts: all('button[data-shortcut][aria-pressed="true"]').map(el => el.dataset.shortcut),
    visible: visible(),
    details: all('details').map(el => el.open)
  });
  flush();
  return {$, all, event, flush, hash, click, search, visible, tick, snapshot,
    document, window, location, navigator, scrolls};
}

const h = harness();
assert.equal(h.visible().length, 101);
assert.equal(h.$('#filters').hidden, false);
assert.ok(h.all('.copy-link').every(el => !el.hidden));
assert.equal(h.$('#print-page').hidden, false);
pass('Initialisation exposes enhanced controls and all 101 entries');
assert.equal(h.all('#biggest-problems > .headline-grid > .headline-card').length, 3);
assert.equal(h.all('#more-findings .headline-card').length, 5);
assert.equal(h.$('#more-findings').open, false);
assert.equal(h.$('#number-index-panel').open, false);
assert.equal(h.all('#number-index-panel .number-grid a').length, 64);
assert.equal(h.click('#number-index-panel > summary').defaultPrevented, false);
assert.equal(h.click('#more-findings > summary').defaultPrevented, false);
for (const panel of h.all('.evidence-panel,.dependencies')) {
  assert.ok(panel.closest('details.analysis'), 'Supplementary evidence belongs inside native analysis');
}
assert.equal(h.all('.back-results').length, 101);
pass('Overview has three initial and five expandable findings; number index and all supplementary analyses use native disclosures');

const shortcutCases = {
  pay: {topics: ['tax-cuts-and-household-bills', 'reducing-the-cost-of-hiring-british-workers', 'welfare-claims'], ids: []},
  energy: {topics: ['unlocking-the-north-sea', 'reindustrialising-britain'], ids: ['claim-energy-bills', 'claim-net-zero-spending']},
  housing: {topics: ['getting-homes-built-in-cities', 'building-critical-national-infrastructure'], ids: []},
  services: {topics: ['spending-and-services', 'welfare-claims'], ids: []}
};
for (const [key, {topics, ids}] of Object.entries(shortcutCases)) {
  const button = h.$('button[data-shortcut="' + key + '"]');
  h.click(button);
  const expected = h.all('.policy').filter(el => topics.includes(el.dataset.topic) || ids.includes(el.id)).map(el => el.id);
  assert.deepEqual(h.visible(), expected, key + ' shortcut collects its curated categories and claims');
  assert.equal(button.getAttribute('aria-pressed'), 'true');
  assert.equal(h.document.activeElement.id, 'explorer-heading');
  assert.equal(h.scrolls.at(-1), 'explorer-heading');
  assert.ok(h.$('#current-topic').textContent.includes(button.textContent));
  h.search('#12');
  assert.deepEqual(h.visible(), expected.includes('measure-12') ? ['measure-12'] : []);
  h.search('');
  h.click('.topic-nav a[data-topic="welfare-claims"]');
  assert.deepEqual(h.visible(), expected.filter(id => h.document.getElementById(id).dataset.topic === 'welfare-claims'));
  h.click('#reset');
  assert.equal(h.visible().length, 101);
  assert.ok(h.all('button[data-shortcut]').every(el => el.getAttribute('aria-pressed') === 'false'));
  h.click(button); h.click(button);
  assert.equal(h.visible().length, 101, 'Repeating a shortcut removes that filter');
}
h.click('button[data-shortcut="energy"]');
h.search('no-matching-policy');
h.click('#empty-reset');
assert.equal(h.visible().length, 101);
assert.ok(h.all('button[data-shortcut]').every(el => el.getAttribute('aria-pressed') === 'false'));
h.click('button[data-shortcut="energy"]');
h.hash('#measure-12');
assert.equal(h.visible().length, 101, 'Policy navigation clears shortcut filters too');
h.$('#measure-12 details').open = false;
h.hash('#' + h.$('#more-findings .headline-card').id);
assert.equal(h.$('#more-findings').open, true, 'Links to an extra finding reveal its native disclosure');
h.$('#more-findings').open = false;
h.click('#change-topic');
assert.equal(h.document.activeElement.id, 'topic-select');
h.click('#jump-search');
assert.equal(h.document.activeElement.id, 'query');
h.click('button[data-shortcut="pay"]');
h.hash('#explorer-heading');
assert.ok(h.visible().length < 101, 'Back-to-results fragment preserves filters');
h.click('#reset');
pass('All four everyday shortcuts combine with search/topic, toggle, clear and reveal targets; reading controls focus without clearing results');

assert.equal(h.click('#measure-01 summary').defaultPrevented, false, 'Analysis summary click must keep its native disclosure default');
assert.equal(h.click('#measure-01 .article-sources a').defaultPrevented, false, 'Source links must keep their native navigation default');
assert.equal(h.$('#topic-select').value, 'all', 'Clicking an article must not filter the page');
for (const article of h.all('.policy')) {
  for (const selector of ['summary', '.article-actions a', '.article-sources a']) {
    const control = article.querySelector(selector);
    assert.equal(h.click(control).defaultPrevented, false, article.id + ' ' + selector + ' keeps its native default');
    assert.equal(h.$('#topic-select').value, 'all', article.id + ' control does not change topic');
  }
}
pass('All 101 summaries, permanent links and source links preserve native defaults without changing topic');

// Invoke the real submit listener; native button-to-submit dispatch is a browser test.
assert.equal(h.$('#filters button[type="submit"]').textContent, 'Search');
h.$('#query').value = 'ROSEBANK';
assert.equal(h.event(h.$('#filters'), 'submit').defaultPrevented, true);
assert.ok(h.visible().includes('measure-01'));
assert.ok(h.visible().length < 101);
h.search('#12');
assert.deepEqual(h.visible(), ['measure-12']);
h.click('.topic-nav a[data-topic="unlocking-the-north-sea"]');
assert.deepEqual(h.visible(), []);
assert.equal(h.$('#no-results').hidden, false);
h.click('#empty-reset');
assert.equal(h.visible().length, 101);
assert.equal(h.document.activeElement.id, 'query');
h.search('£218.70');
assert.ok(h.visible().includes('claim-personal-allowance'));
h.$('#query').value = '';
h.event(h.$('#query'), 'search');
assert.equal(h.visible().length, 101);
pass('Search submit, exact number, evidence text, combined filter and empty reset');

for (const link of h.all('.topic-nav a[data-topic]')) {
  h.click(link);
  const topic = link.dataset.topic;
  assert.equal(h.document.activeElement.id, 'explorer-heading', topic + ' topic link focuses results');
  assert.equal(h.scrolls.at(-1), 'explorer-heading', topic + ' topic link scrolls to results');
  const expected = h.all('.policy').filter(el => topic === 'all' || el.dataset.topic === topic).map(el => el.id);
  assert.deepEqual(h.visible(), expected);
  assert.equal(h.$('#topic-select').value, topic);
  assert.deepEqual(h.all('.topic-nav a[data-topic][aria-current="true"]').map(el => el.dataset.topic), [topic]);
}
for (const option of h.all('#topic-select option')) {
  h.$('#topic-select').value = option.value;
  h.event(h.$('#topic-select'), 'change');
  assert.ok(h.visible().length > 0);
  assert.ok(h.all('.policy:not([hidden])').every(el => option.value === 'all' || el.dataset.topic === option.value));
}
h.click('#reset');
assert.equal(h.visible().length, 101);
assert.equal(h.$('#query').value, '');
assert.equal(h.$('#topic-select').value, 'all');
pass('Every topic link and select option synchronises; clear-all restores entries');
for (const option of h.all('#evidence-select option')) {
  h.$('#evidence-select').value = option.value;
  h.event(h.$('#evidence-select'), 'change');
  const expected = h.all('.policy').filter(el => !option.value || el.querySelector('.evidence-label').textContent.trim() === option.value).map(el => el.id);
  assert.deepEqual(h.visible(), expected);
  assert.equal(h.all('#active-filters button').length, option.value ? 1 : 0);
}
h.click('#reset');
h.click('button[data-shortcut="housing"]');
h.click('.topic-nav a[data-topic="getting-homes-built-in-cities"]');
h.search('#12');
const measure12Label = h.$('#measure-12 .evidence-label').textContent.trim();
h.$('#evidence-select').value = measure12Label;
h.event(h.$('#evidence-select'), 'change');
assert.deepEqual(h.visible(), ['measure-12']);
assert.equal(h.all('#active-filters button').length, 4);
h.click('#active-filters button[data-clear-filter="evidence"]');
assert.equal(h.$('#evidence-select').value, '');
assert.equal(h.$('#topic-select').value, 'getting-homes-built-in-cities');
assert.equal(h.$('#query').value, '#12');
assert.equal(h.document.activeElement.id, 'evidence-select');
h.$('#evidence-select').value = measure12Label; h.event(h.$('#evidence-select'), 'change');
h.click('#active-filters button[data-clear-filter="query"]');
assert.equal(h.$('#query').value, '');
assert.equal(h.$('#evidence-select').value, measure12Label);
assert.equal(h.document.activeElement.id, 'query');
h.search('#12');
h.click('#active-filters button[data-clear-filter="topic"]');
assert.equal(h.$('#topic-select').value, 'all');
assert.equal(h.$('#evidence-select').value, measure12Label);
assert.equal(h.document.activeElement.id, 'explorer-heading');
h.click('.topic-nav a[data-topic="getting-homes-built-in-cities"]');
h.click('#active-filters button[data-clear-filter="shortcut"]');
assert.equal(h.all('button[data-shortcut][aria-pressed="true"]').length, 0);
assert.equal(h.$('#topic-select').value, 'getting-homes-built-in-cities');
assert.equal(h.$('#query').value, '#12');
assert.equal(h.document.activeElement.id, 'explorer-heading');
h.click('#reset');
const hostileQuery = '<img src=x onerror=alert(1)>';
h.search(hostileQuery);
assert.ok(h.$('#active-filters button[data-clear-filter="query"]').textContent.includes(hostileQuery));
assert.equal(h.all('#active-filters img').length, 0, 'Query chip is literal text, never markup');
h.click('#reset');
assert.equal(h.$('#active-filters').hidden, true);
h.$('#evidence-select').value = 'Legal obstacle'; h.event(h.$('#evidence-select'), 'change');
h.hash('#measure-12');
assert.equal(h.$('#evidence-select').value, '', 'Policy hashes clear evidence filtering');
h.$('#evidence-select').value = 'Legal obstacle'; h.event(h.$('#evidence-select'), 'change');
h.search('no-such-entry'); h.click('#empty-reset');
assert.equal(h.$('#evidence-select').value, '');
assert.equal(h.$('#active-filters').hidden, true);
pass('All six evidence labels combine with other filters; chips remove only one filter, restore logical focus and treat queries as text');

const routeIds = ['measure-35','measure-34','claim-fiscal-timing'];
assert.deepEqual(h.all('#funding-route li a').map(el => el.hash), routeIds.map(id => '#' + id));
for (const id of routeIds) {
  h.search('no-such-entry');
  h.hash('#' + id);
  assert.equal(h.document.getElementById(id).hidden, false);
  assert.equal(h.$('#' + id + ' details').open, true);
  assert.ok(h.$('#' + id + ' .route-steps'));
}
for (const id of ['headroom','marginal-pricing','ets','cbam','ni','uc']) {
  const term = h.$('#term-' + id);
  term.open = false;
  h.hash('#term-' + id);
  assert.equal(term.open, true);
  assert.equal(h.document.activeElement.id, 'term-' + id);
  assert.equal(h.click(term.querySelector('summary')).defaultPrevented, false);
}
assert.ok(h.all('.term-links a').every(link => h.document.getElementById(link.hash.slice(1))));
h.click('#reset');
pass('Static funding route and contextual glossary links resolve; term fragments open native definitions without cancelling summary defaults');

for (const link of h.all('a.report-error')) {
  const report = new URL(link.getAttribute('href'));
  assert.equal(report.origin, 'https://github.com');
  assert.equal(report.pathname, '/nikolaspanayotov-jpg/VibeProjects/issues/new');
  const body = report.searchParams.get('body');
  assert.ok(body.includes('Article: https://example.test/rfrm-debunked/' + (link.dataset.article ? '#' + link.dataset.article : '')));
  assert.ok(body.includes('Evidence / source URL'));
}
const offline = harness('', 'file:///private-reader/secret/index.html');
for (const link of offline.all('a.report-error')) {
  const body = new URL(link.getAttribute('href')).searchParams.get('body');
  assert.ok(body.includes('https://github.com/nikolaspanayotov-jpg/VibeProjects/blob/main/rfrm-debunked/index.html'));
  assert.ok(!body.includes('private-reader') && !body.includes('file:'), 'Reports never include local file paths');
}
pass('Correction links are prefilled GitHub issue drafts with evidence prompts; file readers retain public repository references');


for (const link of h.all('.number-grid a')) {
  h.search('no-matching-policy');
  h.hash(link.hash);
  const article = h.document.getElementById(link.hash.slice(1));
  assert.equal(article.hidden, false);
  assert.equal(article.querySelector('details').open, true);
  assert.equal(h.document.activeElement.id, article.id + '-heading');
}
h.hash('#measure-12');
h.search('no-matching-policy');
h.click('.number-grid a[href="#measure-12"]');
h.flush();
assert.equal(h.visible().length, 101);
assert.equal(h.document.activeElement.id, 'measure-12-heading');
pass('All 64 measure fragments and repeated same-fragment click reveal the target');

h.search('no-matching-policy');
h.$('#measure-12 details').open = false;
h.hash('#measure-12-source-1');
assert.equal(h.$('#measure-12').hidden, false);
assert.equal(h.$('#measure-12 details').open, true);
assert.equal(h.document.activeElement.id, 'measure-12-source-1');
h.search('no-matching-policy');
h.hash('#measure-12-heading');
assert.equal(h.document.activeElement.id, 'measure-12-heading');
h.search('no-matching-policy');
h.hash('#topic-unlocking-the-north-sea');
assert.equal(h.$('#topic-unlocking-the-north-sea').hidden, false);
h.click('.topic-nav a[data-topic="unlocking-the-north-sea"]');
h.flush();
assert.equal(h.$('#topic-select').value, 'unlocking-the-north-sea');
assert.ok(h.visible().length < 101);
for (const audit of h.all('.audit-item')) {
  audit.open = false;
  h.hash('#' + audit.id);
  assert.equal(audit.open, true);
  assert.equal(h.document.activeElement.id, audit.id);
}
for (const link of h.all('.top-links a')) {
  h.hash(link.hash);
  assert.equal(h.document.activeElement.id, link.hash.slice(1));
}
const initial = harness('#measure-12-source-1');
assert.equal(initial.document.activeElement.id, 'measure-12-source-1');
assert.equal(initial.$('#measure-12 details').open, true);
h.hash('#%E0%A4%A'); // malformed percent encoding must not break the page
h.click('#reset');
assert.equal(h.visible().length, 101);
pass('Nested source/heading, initial, topic, main-nav and all 20 audit fragments recover safely');

let copied;
h.navigator.clipboard = {writeText: value => { copied = value; return Promise.resolve(); }};
for (const button of h.all('.copy-link')) {
  h.click(button);
  await h.tick();
  const id = button.closest('.policy').id;
  assert.equal(copied, 'https://example.test/rfrm-debunked/#' + id);
  assert.equal(button.textContent, 'Link copied');
  assert.equal(button.closest('.policy').querySelector('.copy-fallback').hidden, true);
}
h.navigator.clipboard = {writeText: () => Promise.reject(new Error('Permission denied'))};
for (const button of h.all('.copy-link')) {
  h.click(button);
  await h.tick();
  const article = button.closest('.policy');
  const input = article.querySelector('.copy-fallback input');
  assert.equal(button.textContent, 'Copy link');
  assert.equal(article.querySelector('.copy-fallback').hidden, false);
  assert.equal(input.value, 'https://example.test/rfrm-debunked/#' + article.id);
  assert.equal(h.document.activeElement.id, input.id);
  assert.equal(input.selectionStart, 0);
  assert.equal(input.selectionEnd, input.value.length);
  assert.equal(h.all('.copy-fallback:not([hidden])').length, 1);
}
h.navigator.clipboard = undefined;
h.click('#measure-12 .copy-link');
await h.tick();
assert.equal(h.$('#measure-12 .copy-fallback').hidden, false);
pass('All 101 copy handlers succeed, recover on denied retry, select a fallback and close older fallbacks');

h.click('button[data-shortcut="housing"]');
h.search('#12');
h.$('#evidence-select').value = h.$('#measure-12 .evidence-label').textContent.trim();
h.event(h.$('#evidence-select'), 'change');
h.all('details').forEach((el, index) => { el.open = index % 3 === 0; });
const beforePrint = h.snapshot();
let printCalls = 0;
h.window.print = () => {
  printCalls += 1;
  assert.equal(h.visible().length, 101);
  assert.ok(h.all('details').every(el => el.open));
  h.event(h.window, 'beforeprint');
};
h.click('#print-page');
assert.equal(printCalls, 1);
assert.equal(h.visible().length, 101, 'Non-blocking print stays prepared until afterprint');
h.event(h.window, 'afterprint');
assert.equal(h.snapshot(), beforePrint);
h.event(h.window, 'beforeprint');
h.event(h.window, 'beforeprint');
assert.equal(h.visible().length, 101);
h.event(h.window, 'afterprint');
assert.equal(h.snapshot(), beforePrint);
h.window.print = () => { throw new Error('Print unavailable'); };
h.click('#print-page');
assert.equal(h.snapshot(), beforePrint);
assert.equal(h.$('#print-status').hidden, false);
assert.match(h.$('#print-status').textContent, /browser.*Print/);
h.window.print = () => {};
h.click('#print-page');
assert.equal(h.$('#print-status').hidden, true);
h.event(h.window, 'afterprint');
assert.equal(h.snapshot(), beforePrint);
pass('Print button prepares all content, waits for afterprint, restores exact state and handles unavailable printing');

const report = {passed, environment: 'Node + LinkeDOM 0.18.12',
  limitations: ['No browser rendering or native click/keyboard defaults',
    'Focus, selection, details reflection, location, clipboard and print APIs are modelled',
    'Real browser/OS clipboard, print dialogs, overflow and accessibility need browser verification']};
fs.mkdirSync(path.join(root, 'tests/artifacts'), {recursive: true});
fs.writeFileSync(path.join(root, 'tests/artifacts/control-runtime-results.json'), JSON.stringify(report, null, 2) + '\n');
console.log('DOM/event regression checks passed; browser behaviour and layout remain unverified.');
