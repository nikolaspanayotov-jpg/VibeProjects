// Run from any directory: node /path/to/php-explained/qa/buttons.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');

const pageUrl = pathToFileURL(path.resolve(__dirname, '../index.html')).href;
const launchOptions = {headless: true};
if (process.env.CHROMIUM_EXECUTABLE) {
  launchOptions.executablePath = process.env.CHROMIUM_EXECUTABLE;
}

async function run() {
  const artifacts = await fs.mkdtemp(path.join(os.tmpdir(), 'php-explained-qa-'));
  const browser = await chromium.launch(launchOptions);
  try {
    for (const width of [390, 1280]) {
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
      assert(await page.locator('#interactiveNotice').isHidden());
      assert(await page.locator('#storyLab').isVisible());
      assert(await page.locator('#quizPanel').isVisible());
      assert(await page.locator('#copyActions').isVisible());
      assert.equal(await page.locator('html').getAttribute('lang'), 'en-GB');
      await assertNoOverflow();

      for (const story of ['oom', 'stale']) {
        await page.locator('#' + story).click();
        assert.equal(await page.locator('#' + story).getAttribute('aria-pressed'), 'true');
        assert.equal(await page.locator('#' + (story === 'oom' ? 'stale' : 'oom')).getAttribute('aria-pressed'), 'false');
        assert(await page.locator('#back').isDisabled());
        assert.match(await text('#counter'), /STEP 1 OF 4/);
        for (let index = 0; index < 4; index++) {
          const originalScene = await page.locator('#workspace').innerHTML();
          const originalTitle = await text('#stepTitle');
          await page.locator('#repaired').click();
          assert.equal(await text('#badge'), 'Repaired PHP');
          assert.equal(await page.locator('#storyStage').getAttribute('data-version'), 'repaired');
          assert.equal(await page.locator('#repaired').getAttribute('aria-pressed'), 'true');
          assert.equal(await page.locator('#original').getAttribute('aria-pressed'), 'false');
          assert.equal(await page.evaluate(() => document.activeElement.id), 'repaired');
          assert.match(await text('#counter'), new RegExp(`STEP ${index + 1} OF 4`));
          if (index >= 2) {
            assert.notEqual(await page.locator('#workspace').innerHTML(), originalScene);
            assert.notEqual(await text('#stepTitle'), originalTitle);
          }
          await page.locator('#original').click();
          assert.equal(await text('#badge'), 'Original PHP');
          assert.equal(await page.locator('#storyStage').getAttribute('data-version'), 'original');
          assert.equal(await page.locator('#original').getAttribute('aria-pressed'), 'true');
          assert.equal(await page.locator('#repaired').getAttribute('aria-pressed'), 'false');
          assert.equal(await page.locator('#workspace').innerHTML(), originalScene);
          if (index < 3) {
            assert(await page.locator('#patch').isHidden());
            await page.locator('#next').click();
            assert.notEqual(await page.locator('#workspace').innerHTML(), originalScene);
          }
          await assertNoOverflow();
        }
        assert(await page.locator('#next').isHidden());
        assert.equal(await page.evaluate(() => document.activeElement.id), 'original');
        assert.match(await page.locator('#outcome').getAttribute('class'), /danger/);
        await page.locator('#back').click();
        assert.match(await text('#counter'), /STEP 3 OF 4/);
        assert(await page.locator('#next').isVisible());
        assert(await page.locator('#patch').isHidden());
        await page.locator('#next').click();
        assert.equal(await page.evaluate(() => document.activeElement.id), 'stepTitle');
        await page.locator('#patch').click();
        assert.equal(await text('#badge'), 'Repaired PHP');
        assert.match(await text('#counter'), /WITH THE REPAIR.*STEP 1 OF 4/);
        for (let index = 0; index < 3; index++) await page.locator('#next').click();
        assert.match(await page.locator('#outcome').getAttribute('class'), /safe/);
        assert.match(await text('#workspace'), story === 'oom' ? /No invalid cleanup/ : /Fresh, valid state/);
        await page.locator('#patch').click();
        assert.equal(await text('#badge'), 'Original PHP');
        await page.locator('#next').click();
        await page.locator('#reset').click();
        assert.match(await text('#counter'), /STEP 1 OF 4/);
        assert(await page.locator('#back').isDisabled());
      }

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
      if (width === 390) {
        await page.locator('#repaired').focus();
        await page.keyboard.press('Enter');
        assert.equal(await text('#badge'), 'Repaired PHP');
      }
      await assertNoOverflow();
      assert.deepEqual(errors, []);
      await page.locator('#storyLab').screenshot({path: path.join(artifacts, `story-${width}.png`)});
      await page.screenshot({path: path.join(artifacts, `page-${width}.png`), fullPage: true});
      console.log(`PASS: all controls, resulting states, keyboard focus and no overflow at ${width}px`);
      await context.close();
    }

    const noJsContext = await browser.newContext({javaScriptEnabled: false});
    const noJsPage = await noJsContext.newPage();
    await noJsPage.goto(pageUrl);
    assert(await noJsPage.locator('#interactiveNotice').isVisible());
    assert(await noJsPage.locator('#storyLab').isHidden());
    assert(await noJsPage.locator('#quizPanel').isHidden());
    assert(await noJsPage.locator('#copyActions').isHidden());
    assert(await noJsPage.locator('#basics').isVisible());
    await noJsContext.close();
    console.log(`PASS: no-JavaScript fallback. Screenshots: ${artifacts}`);
  } finally {
    await browser.close();
  }
}

run().catch(error => {console.error(error); process.exitCode = 1;});
