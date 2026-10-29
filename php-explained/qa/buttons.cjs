// Run from any directory: node /path/to/php-explained/qa/buttons.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');

const pageUrl = process.env.PHP_GUIDE_URL || pathToFileURL(path.resolve(__dirname, '../index.html')).href;
const launchOptions = {headless: true};
if (process.env.CHROMIUM_EXECUTABLE) {
  launchOptions.executablePath = process.env.CHROMIUM_EXECUTABLE;
}

async function run() {
  const artifacts = await fs.mkdtemp(path.join(os.tmpdir(), 'php-explained-qa-'));
  const browser = await chromium.launch(launchOptions);
  try {
    for (const width of [320, 390, 1280]) {
      const context = await browser.newContext({viewport: {width, height: 900}});
      const page = await context.newPage();
      page.setDefaultTimeout(5000);
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.goto(pageUrl);
      const text = selector => page.locator(selector).innerText();
      const assertNoOverflow = async () => assert(await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth
      ), `Horizontal overflow at ${width}px`);
      async function clickStory(id) {
        const control = page.locator('#' + id);
        // Position the control before recording, so Playwright's own scrolling
        // cannot be mistaken for scrolling caused by the application.
        await control.evaluate(element => element.scrollIntoView({block: 'center', behavior: 'instant'}));
        const before = await page.evaluate(() => ({
          scrollY: window.scrollY,
          navigationY: document.querySelector('.story-navigation').getBoundingClientRect().top
        }));
        await control.click();
        await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
        const after = await page.evaluate(() => ({
          scrollY: window.scrollY,
          navigationY: document.querySelector('.story-navigation').getBoundingClientRect().top
        }));
        assert(Math.abs(after.scrollY - before.scrollY) <= 1, `${id} scrolled the page at ${width}px`);
        assert(Math.abs(after.navigationY - before.navigationY) <= 1, `${id} moved the controls at ${width}px`);
      }
      assert(await page.locator('#interactiveNotice').isHidden());
      assert(await page.locator('#storyLab').isVisible());
      assert(await page.locator('#quizPanel').isVisible());
      assert(await page.locator('#copyActions').isVisible());
      assert(await page.locator('#bridgeControls').isVisible());
      assert.equal(await page.locator('html').getAttribute('lang'), 'en-GB');
      assert.equal(await page.locator('.chapter-number, .story-card-number, .flow-index').count(), 0);
      await assertNoOverflow();

      for (const story of ['oom', 'stale']) {
        await clickStory(story);
        assert.equal(await page.locator('#' + story).getAttribute('aria-pressed'), 'true');
        assert.equal(await page.locator('#' + (story === 'oom' ? 'stale' : 'oom')).getAttribute('aria-pressed'), 'false');
        assert(await page.locator('#back').isDisabled());
        assert.match(await text('#counter'), /STEP 1 OF 4/);
        for (let index = 0; index < 4; index++) {
          const originalScene = await text('#workspace');
          const originalTitle = await text('#stepTitle');
          await clickStory('repaired');
          assert.equal(await text('#badge'), 'Repaired PHP');
          assert.equal(await page.locator('#storyStage').getAttribute('data-version'), 'repaired');
          assert.equal(await page.locator('#repaired').getAttribute('aria-pressed'), 'true');
          assert.equal(await page.locator('#original').getAttribute('aria-pressed'), 'false');
          assert.equal(await page.evaluate(() => document.activeElement.id), 'repaired');
          assert.match(await text('#counter'), new RegExp(`STEP ${index + 1} OF 4`));
          assert.equal(await page.locator('#comparison').getAttribute('data-kind'), index < 2 ? 'shared' : 'repaired');
          assert.match(await text('#comparisonTitle'), index < 2 ? /Both versions behave the same/ : /repair changes/);
          if (index < 2) assert.match(await text('#comparisonDescription'), /step three/);
          if (index >= 2) {
            assert.notEqual(await text('#workspace'), originalScene);
            assert.notEqual(await text('#stepTitle'), originalTitle);
          }
          await clickStory('original');
          assert.equal(await text('#badge'), 'Original PHP');
          assert.equal(await page.locator('#storyStage').getAttribute('data-version'), 'original');
          assert.equal(await page.locator('#original').getAttribute('aria-pressed'), 'true');
          assert.equal(await page.locator('#repaired').getAttribute('aria-pressed'), 'false');
          assert.equal(await text('#workspace'), originalScene);
          assert.equal(await page.locator('#comparison').getAttribute('data-kind'), index < 2 ? 'shared' : 'original');
          if (index < 3) {
            assert(await page.locator('#patch').isHidden());
            await clickStory('next');
            assert.notEqual(await text('#workspace'), originalScene);
          }
          await assertNoOverflow();
        }
        assert(await page.locator('#next').isHidden());
        assert.equal(await page.evaluate(() => document.activeElement.id), 'original');
        assert.match(await page.locator('#outcome').getAttribute('class'), /danger/);
        await clickStory('back');
        assert.match(await text('#counter'), /STEP 3 OF 4/);
        assert(await page.locator('#next').isVisible());
        assert(await page.locator('#patch').isHidden());
        await clickStory('back');
        await clickStory('back');
        assert(await page.locator('#back').isDisabled());
        assert.equal(await page.evaluate(() => document.activeElement.id), 'next');
        for (let index = 0; index < 3; index++) await clickStory('next');
        assert.equal(await page.evaluate(() => document.activeElement.id), 'patch');
        await clickStory('patch');
        assert.equal(await text('#badge'), 'Repaired PHP');
        assert.match(await text('#counter'), /STEP 1 OF 4/);
        for (let index = 0; index < 3; index++) await clickStory('next');
        assert.match(await page.locator('#outcome').getAttribute('class'), /safe/);
        assert.match(await text('#workspace'), story === 'oom' ? /No invalid cleanup/ : /Fresh, valid state/);
        await clickStory('patch');
        assert.equal(await text('#badge'), 'Original PHP');
        await clickStory('next');
        await clickStory('reset');
        assert.match(await text('#counter'), /STEP 1 OF 4/);
        assert(await page.locator('#back').isDisabled());
      }

      // The note remains the same element while its folder is taken away.
      await clickStory('stale');
      await clickStory('next');
      await page.evaluate(() => {window.retainedNote = document.querySelector('#workspace .sticky');});
      await clickStory('next');
      assert(await page.evaluate(() => window.retainedNote === document.querySelector('#workspace .sticky')));
      await clickStory('next');
      assert(await page.evaluate(() => window.retainedNote === document.querySelector('#workspace .sticky')));

      // All definitions open above the page without changing its scroll position.
      for (const term of ['request', 'server', 'memory', 'worker', 'reference', 'cleanup', 'runtime', 'use-after-free']) {
        const control = page.locator(`button.term[data-term="${term}"]:visible`).first();
        await control.evaluate(element => element.scrollIntoView({block: 'center', behavior: 'instant'}));
        const before = await page.evaluate(() => window.scrollY);
        await control.click();
        assert(await page.locator('#definitionPanel').isVisible());
        assert.equal((await text('#definitionTitle')).toLowerCase(), term);
        assert((await text('#definitionText')).length > 70);
        assert.equal(await control.getAttribute('aria-expanded'), 'true');
        assert(Math.abs((await page.evaluate(() => window.scrollY)) - before) <= 1);
        await page.locator('#definitionClose').click();
        assert(await page.locator('#definitionPanel').isHidden());
        assert.equal(await control.getAttribute('aria-expanded'), 'false');
        assert(await control.evaluate(element => document.activeElement === element));
      }
      const keyboardTerm = page.locator('#stepText .term').first();
      await keyboardTerm.focus();
      await page.keyboard.press('Enter');
      assert(await page.locator('#definitionPanel').isVisible());
      await page.keyboard.press('Escape');
      assert(await keyboardTerm.evaluate(element => document.activeElement === element));
      await keyboardTerm.click();
      await page.locator('#storiesTitle').click();
      assert(await page.locator('#definitionPanel').isHidden());

      for (const path of ['prepared', 'ordinary', 'prepared', 'ordinary']) {
        await page.locator('#' + path).evaluate(element => element.scrollIntoView({block: 'center', behavior: 'instant'}));
        const before = await page.evaluate(() => ({scroll: window.scrollY, bottom: document.querySelector('#attackBridge').getBoundingClientRect().bottom}));
        await page.locator('#' + path).click();
        assert.equal(await page.locator('#bridgeState').getAttribute('data-path'), path);
        assert.equal(await page.locator('#' + path).getAttribute('aria-pressed'), 'true');
        assert.equal(await page.locator('#bridgeState li').count(), 3);
        assert.match(await text('#bridgeState li:last-child h4'), path === 'prepared' ? /attacker redirects/ : /may crash/);
        const after = await page.evaluate(() => ({scroll: window.scrollY, bottom: document.querySelector('#attackBridge').getBoundingClientRect().bottom}));
        assert(Math.abs(after.scroll - before.scroll) <= 1);
        assert(Math.abs(after.bottom - before.bottom) <= 1, 'Changing the attack path must not shift the page');
        await assertNoOverflow();
      }
      // Supporting diagram labels remain readable at every tested width.
      for (const selector of ['#badgeDetail', '.desk-edge', '.worker', '.story-card .eyebrow']) {
        assert(await page.locator(selector).first().evaluate(element => parseFloat(getComputedStyle(element).fontSize) >= 12));
      }

      await page.evaluate(() => Object.defineProperty(navigator, 'clipboard', {
        configurable: true, value: {writeText: async text => {window.copiedText = text;}}
      }));
      const baseAddress = page.url();
      const momentLinks = [];
      for (const story of ['oom', 'stale']) {
        await clickStory(story);
        for (const version of ['original', 'repaired']) {
          await clickStory(version);
          for (const index of [3, 0, 2, 1]) {
            await clickStory('storyStep' + index);
            assert.match(await text('#counter'), new RegExp(`STEP ${index + 1} OF 4`));
            assert.equal(await page.locator('#dots [aria-current="step"]').count(), 1);
            assert.equal(await page.locator('#storyStep' + index).getAttribute('aria-current'), 'step');
            assert.equal(await page.evaluate(() => document.activeElement.id), 'storyStep' + index);
            await page.locator('#shareStep').click();
            const copied = await page.evaluate(() => window.copiedText);
            const url = new URL(copied);
            assert.equal(url.searchParams.get('story'), story);
            assert.equal(url.searchParams.get('step'), String(index + 1));
            assert.equal(url.searchParams.get('php'), version);
            assert.equal(url.hash, '#storyStage');
            assert.equal(page.url(), baseAddress, 'Sharing must not change the current URL');
            momentLinks.push({url: copied, story, version, step: index + 1});
          }
        }
        await page.locator('#predict').evaluate(element => element.scrollIntoView({block: 'center', behavior: 'instant'}));
        const before = await page.evaluate(() => window.scrollY);
        const counter = await text('#counter');
        await page.locator('#predict').click();
        assert(await page.locator('#predictionPanel').isVisible());
        for (const index of [0, 1]) {
          await page.locator('.prediction-answer').nth(index).click();
          assert.equal(await page.locator('.prediction-answer').nth(index).getAttribute('aria-pressed'), 'true');
          assert.match(await text('#predictionFeedback'), index === (story === 'oom' ? 0 : 1) ? /^Exactly/ : /^Think about/);
        }
        await page.locator('#predictionClose').click();
        assert(await page.locator('#predictionPanel').isHidden());
        assert.equal(await page.evaluate(() => document.activeElement.id), 'predict');
        assert.equal(await text('#counter'), counter);
        assert(Math.abs((await page.evaluate(() => window.scrollY)) - before) <= 1);
        await page.keyboard.press('Enter');
        assert.equal(await page.locator('.prediction-answer').nth(1).getAttribute('aria-pressed'), 'true');
        await page.keyboard.press('Escape');
        assert.equal(await page.evaluate(() => document.activeElement.id), 'predict');
        await page.locator('#predict').click();
        await page.mouse.click(5, 5);
        assert(await page.locator('#predictionPanel').isHidden());
      }
      await page.evaluate(() => Object.defineProperty(navigator, 'clipboard', {
        configurable: true, value: {writeText: async () => {throw new Error('Clipboard denied');}}
      }));
      await page.locator('#shareStep').click();
      assert.match(await text('#shareStatus'), /Select the link/);
      assert.equal(await page.evaluate(() => document.activeElement.id), 'shareLink');
      assert(await page.locator('#shareLink').evaluate(element => element.selectionStart === 0 && element.selectionEnd === element.value.length));
      for (const [id, title] of Object.entries({journeyRequest: /visitor sends/, journeyPhp: /login check comes later/, journeyLogin: /password protects/})) {
        await page.locator('#' + id).evaluate(element => element.scrollIntoView({block: 'center', behavior: 'instant'}));
        const before = await page.evaluate(() => ({scroll: window.scrollY, bottom: document.querySelector('#loginJourney').getBoundingClientRect().bottom}));
        await page.locator('#' + id).click();
        assert.equal(await page.locator('.journey-stop[aria-pressed="true"]').count(), 1);
        assert.equal(await page.locator('#' + id).getAttribute('aria-pressed'), 'true');
        assert.match(await text('#journeyState h4'), title);
        const after = await page.evaluate(() => ({scroll: window.scrollY, bottom: document.querySelector('#loginJourney').getBoundingClientRect().bottom}));
        assert(Math.abs(after.scroll - before.scroll) <= 1);
        assert(Math.abs(after.bottom - before.bottom) <= 1);
      }
      await page.selectOption('#role', 'owner');
      assert(await page.locator('#ownerPlan').isVisible());
      const tasks = ['hostAsked', 'hostUpdated', 'hostVerified'];
      for (const [index, id] of tasks.entries()) {
        await page.locator('#' + id).check();
        assert.match(await text('#hostProgress'), new RegExp(`${index + 1} of 3`));
      }
      assert.deepEqual(await page.evaluate(() => JSON.parse(localStorage.getItem('php-explained.v1'))), {version: 1, hostTasks: [true, true, true]});
      await page.evaluate(() => Object.defineProperty(navigator, 'clipboard', {
        configurable: true, value: {writeText: async text => {window.copiedText = text;}}
      }));
      await page.locator('#copyHost').click();
      const message = await page.evaluate(() => window.copiedText);
      assert.equal(message, await page.locator('#hostMessage').inputValue());
      for (const cve of ['CVE-2026-109618', 'CVE-2026-109619', 'CVE-2026-115560']) assert(message.includes(cve));
      await page.evaluate(() => Object.defineProperty(navigator, 'clipboard', {
        configurable: true, value: {writeText: async () => {throw new Error('Clipboard denied');}}
      }));
      await page.locator('#copyHost').click();
      assert.match(await text('#hostCopyStatus'), /Select the message/);
      assert.equal(await page.evaluate(() => document.activeElement.id), 'hostMessage');
      assert(await page.locator('#hostMessage').evaluate(element => element.selectionEnd === element.value.length));
      if (width === 1280) {
        const linkedPage = await context.newPage();
        for (const moment of momentLinks) {
          await linkedPage.goto(moment.url);
          assert.equal(await linkedPage.locator('#' + moment.story).getAttribute('aria-pressed'), 'true');
          assert.equal(await linkedPage.locator('#badge').innerText(), moment.version === 'repaired' ? 'Repaired PHP' : 'Original PHP');
          assert.match(await linkedPage.locator('#counter').innerText(), new RegExp(`STEP ${moment.step} OF 4`));
        }
        await linkedPage.goto(pageUrl);
        await linkedPage.selectOption('#role', 'owner');
        for (const id of tasks) assert(await linkedPage.locator('#' + id).isChecked());
        await linkedPage.reload();
        await linkedPage.selectOption('#role', 'owner');
        for (const id of tasks) assert(await linkedPage.locator('#' + id).isChecked());
        for (const params of ['story=__proto__&step=9', 'step=2.5', 'step=-1', 'step=2junk', 'story=unknown&step=0&php=bad']) {
          const invalidUrl = new URL(pageUrl);
          invalidUrl.search = params;
          await linkedPage.goto(invalidUrl.href);
          assert.equal(await linkedPage.locator('#oom').getAttribute('aria-pressed'), 'true');
          assert.match(await linkedPage.locator('#counter').innerText(), /STEP 1 OF 4/);
        }
        await linkedPage.close();
      }
      for (const id of tasks) await page.locator('#' + id).uncheck();
      await assertNoOverflow();

      const roles = {visitor: 'server operator', owner: 'hosting provider', admin: 'Inventory, update'};
      for (const [value, result] of Object.entries(roles)) {
        await page.selectOption('#role', value);
        assert((await text('#roleResult')).includes(result));
        await assertNoOverflow();
      }
      const branches = {'8.5': '8.5.12', '8.4': '8.4.27', '8.3': '8.3.36', '8.2': '8.2.35'};
      for (const [value, fixed] of Object.entries(branches)) {
        await page.selectOption('#branch', value);
        assert(await page.locator('#level').isEnabled());
        for (const level of ['before', 'fixed']) {
          await page.selectOption('#level', level);
          assert((await text('#versionResult')).includes(fixed));
          assert((await text('#versionResult')).includes(level === 'before' ? 'need the repair' : 'has deployed the update'));
        }
      }
      for (const value of ['old', 'unknown']) {
        await page.selectOption('#branch', value);
        assert(await page.locator('#level').isDisabled());
        assert((await text('#versionResult')).includes(value === 'old' ? 'outside upstream support' : 'Ask your host'));
      }
      await page.selectOption('#branch', '8.5');
      assert(await page.locator('#level').isEnabled());

      for (const summary of await page.locator('summary').all()) {
        const details = summary.locator('..');
        const initial = await details.evaluate(element => element.open);
        await summary.click();
        assert.equal(await details.evaluate(element => element.open), !initial);
        await assertNoOverflow();
        await summary.click();
        assert.equal(await details.evaluate(element => element.open), initial);
      }

      // Each of the nine answer buttons is exercised, plus all-correct scoring.
      for (const answers of [[0, 0, 0], [1, 1, 1], [2, 2, 2], [1, 0, 2]]) {
        const correct = [1, 0, 2];
        let score = 0;
        assert(await page.locator('#quizNext').isDisabled());
        for (const [index, answer] of answers.entries()) {
          await page.locator('#answers button').nth(answer).click();
          if (answer === correct[index]) score++;
          assert((await text('#feedback')).length > 40);
          for (const button of await page.locator('#answers button').all()) assert(await button.isDisabled());
          assert.equal(await page.locator('#progress').getAttribute('value'), String(index + 1));
          assert(await page.locator('#quizNext').isEnabled());
          await page.locator('#quizNext').click();
          assert.equal(await page.evaluate(() => document.activeElement.id), 'question');
        }
        assert((await text('#question')).includes(`${score} out of 3`));
        assert(await page.locator('#quizNext').isHidden());
        await page.locator('#quizReset').click();
        assert.equal(await page.locator('#answers button').count(), 3);
        assert.equal(await page.locator('#progress').getAttribute('value'), '0');
      }

      // Stub OS integrations so results are deterministic without clipboard grants or a printer.
      await page.evaluate(() => Object.defineProperty(navigator, 'clipboard', {
        configurable: true, value: {writeText: async text => {window.copiedText = text;}}
      }));
      await page.locator('#copy').click();
      assert.equal(await text('#copyStatus'), 'Explanation copied.');
      assert.equal(await page.evaluate(() => window.copiedText), await page.locator('#explanation').textContent());
      await page.evaluate(() => Object.defineProperty(navigator, 'clipboard', {
        configurable: true, value: {writeText: async () => {throw new Error('Permission denied');}}
      }));
      await page.locator('#copy').click();
      assert.match(await text('#copyStatus'), /Select the explanation text/);
      await page.evaluate(() => {window.print = () => {window.printCalled = true;};});
      await page.locator('#print').click();
      assert(await page.evaluate(() => window.printCalled));

      for (const link of await page.locator('a[href^="#"]:not(.skip-link)').all()) {
        await link.evaluate(element => {
          for (let parent = element.parentElement; parent; parent = parent.parentElement) {
            if (parent.tagName === 'DETAILS') parent.open = true;
          }
        });
        const href = await link.getAttribute('href');
        await link.click();
        if (href !== '#') assert.equal(new URL(page.url()).hash, href);
      }
      await page.locator('.skip-link').focus();
      await page.keyboard.press('Enter');
      assert.equal(new URL(page.url()).hash, '#explore');
      // Exercise the keyboard path and reduced-motion setting too.
      await page.emulateMedia({reducedMotion: 'reduce'});
      await page.locator('#oom').focus();
      await page.keyboard.press('Enter');
      await page.locator('#next').focus();
      await page.keyboard.press('Space');
      assert.match(await text('#counter'), /STEP 2 OF 4/);
      assert(await page.locator('#workspace .folder').evaluate(element => getComputedStyle(element).animationName === 'none'));
      if (width === 390) {
        await page.locator('#repaired').focus();
        await page.keyboard.press('Enter');
        assert.equal(await text('#badge'), 'Repaired PHP');
      }
      await assertNoOverflow();
      assert.deepEqual(errors, []);
      await page.locator('#storyLab').screenshot({path: path.join(artifacts, `story-${width}.png`), style: 'header, .skip-link { visibility: hidden !important; }'});
      await page.locator('#prepared').click();
      await page.locator('#attackBridge').screenshot({path: path.join(artifacts, `attack-${width}.png`)});
      await page.locator('#loginJourney').screenshot({path: path.join(artifacts, `login-${width}.png`)});
      await page.selectOption('#role', 'owner');
      await page.locator('#ownerPlan').screenshot({path: path.join(artifacts, `host-${width}.png`)});
      await page.selectOption('#role', 'visitor');
      await page.locator('#predict').click();
      await page.locator('.prediction-answer').first().click();
      await page.locator('#predictionPanel').screenshot({path: path.join(artifacts, `prediction-${width}.png`)});
      await page.locator('#predictionClose').click();
      await page.screenshot({path: path.join(artifacts, `page-${width}.png`), fullPage: true});
      console.log(`PASS: stable story viewport/control positions, all interactions, keyboard focus and no overflow at ${width}px`);
      await context.close();
    }

    const noJsContext = await browser.newContext({javaScriptEnabled: false});
    const noJsPage = await noJsContext.newPage();
    await noJsPage.goto(pageUrl);
    assert(await noJsPage.locator('#interactiveNotice').isVisible());
    assert(await noJsPage.locator('#storyLab').isHidden());
    assert(await noJsPage.locator('#quizPanel').isHidden());
    assert(await noJsPage.locator('#copyActions').isHidden());
    assert(await noJsPage.locator('#bridgeControls').isHidden());
    assert(await noJsPage.locator('#bridgeState').isVisible());
    assert(await noJsPage.locator('#journeyState').isVisible());
    for (const button of await noJsPage.locator('.journey-stop').all()) assert(await button.isDisabled());
    assert(await noJsPage.locator('#basics').isVisible());
    await noJsContext.close();

    // Unavailable or corrupt storage cannot stop the guide or its checklist.
    for (const denied of [true, false]) {
      const storageContext = await browser.newContext();
      await storageContext.addInitScript(blocked => {
        if (blocked) Object.defineProperty(window, 'localStorage', {get() {throw new DOMException('Storage denied', 'SecurityError');}});
        else localStorage.setItem('php-explained.v1', '{invalid JSON');
      }, denied);
      const storagePage = await storageContext.newPage();
      const storageErrors = [];
      storagePage.on('pageerror', error => storageErrors.push(error.message));
      await storagePage.goto(pageUrl);
      await storagePage.selectOption('#role', 'owner');
      await storagePage.locator('#hostAsked').check();
      assert.match(await storagePage.locator('#hostProgress').innerText(), /1 of 3/);
      if (denied) assert.match(await storagePage.locator('#hostSaveHint').innerText(), /while this page is open/);
      assert.deepEqual(storageErrors, []);
      await storageContext.close();
    }
    console.log(`PASS: no-JavaScript fallback. Screenshots: ${artifacts}`);
  } finally {
    await browser.close();
  }
}

run().catch(error => {console.error(error); process.exitCode = 1;});
