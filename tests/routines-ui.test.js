/* Readable rewards, native disclosure, discovery and mobile containment. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '../docs');
const prefix = '/Aion2-Daeva-Atlas/';
const artifacts = process.env.ROUTINES_QA_ARTIFACTS || path.resolve(__dirname, '../../routines-qa-artifacts');
fs.mkdirSync(artifacts, {recursive: true});
const server = http.createServer((req, res) => {
  const route = decodeURIComponent(new URL(req.url, 'http://local').pathname);
  if (!route.startsWith(prefix)) { res.writeHead(404).end(); return; }
  let relative = route.slice(prefix.length);
  if (!relative || relative.endsWith('/')) relative += 'index.html';
  const file = path.resolve(root, relative);
  if (!file.startsWith(root + path.sep) || !fs.existsSync(file)) { res.writeHead(404).end(); return; }
  const type = {'.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json',
    '.css': 'text/css', '.svg': 'image/svg+xml', '.webp': 'image/webp'}[path.extname(file)] || 'application/octet-stream';
  res.writeHead(200, {'Content-Type': type}); fs.createReadStream(file).pipe(res);
});

async function contained(page, label) {
  const box = await page.evaluate(() => ({width: innerWidth, scroll: document.documentElement.scrollWidth}));
  assert(box.scroll <= box.width + 1, label + ': page overflow ' + JSON.stringify(box));
}

(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = 'http://127.0.0.1:' + server.address().port + prefix;
  const browser = await chromium.launch({headless: true});
  try {
    for (const lang of ['en', 'ko']) for (const javascript of [true, false]) {
      console.log('Verify routines:', lang, javascript ? 'JS' : 'no-JS');
      // Native fragment navigation starts a smooth scroll under the site's default CSS.
      // Honor reduced motion so pointer checks and screenshots wait on a fixed layout.
      const context = await browser.newContext({viewport: {width: 1440, height: 1000}, javaScriptEnabled: javascript, reducedMotion: 'reduce'});
      await context.route('https://**/*', route => route.abort());
      const page = await context.newPage(), errors = [];
      page.on('pageerror', error => errors.push(error.message));
      const local = base + (lang === 'ko' ? 'ko/' : '');
      await page.goto(local);
      await page.locator('.home-stage-nav a[href$="routines/"]').click();
      await page.waitForURL('**/routines/');
      assert.equal(await page.locator('[data-routine-guide]').count(), 1);
      assert.equal(await page.locator('.routine-choice').count(), 3);
      assert.equal(await page.locator('#routine-group-daily tbody tr').count(), 2);
      assert.equal(await page.locator('#routine-group-banked tbody tr').count(), 5);
      assert.equal(await page.locator('#routine-daily-dungeon').locator('xpath=ancestor::section').getAttribute('id'), 'routine-group-weekly');
      assert((await page.locator('#routine-daily-dungeon').textContent()).includes('14'));
      assert((await page.locator('#routine-conquest').textContent()).includes('21'));
      assert((await page.locator('#routine-ascension').textContent()).includes('3'));
      for (const [id, amount] of [['bio', lang === 'ko' ? '1만' : '10,000'], ['odium', '80'], ['kinah', lang === 'ko' ? '30만' : '300,000']]) {
        const card = page.locator('#daily-choice-' + id);
        assert((await card.textContent()).includes(amount));
        assert((await card.textContent()).includes(lang === 'ko' ? '점 기준' : 'score'));
      }
      assert((await page.locator('#daily-dungeon-choices > header').textContent()).includes(lang === 'ko' ? '공유' : 'same'));
      assert((await page.locator('#routine-subjugation').textContent()).includes(lang === 'ko' ? '한국 공략' : 'KR guide'));
      await page.locator('#routine-conquest summary').click();
      assert.equal(await page.locator('#routine-conquest details').getAttribute('open'), '');
      await page.locator('#routine-conquest a[href="#routine-source-global"]').click();
      await page.waitForURL('**/#routine-source-global');
      assert.equal(await page.locator('#routine-source-global').isVisible(), true);
      assert.equal(await page.locator('#routine-sources li').count(), 14);
      await page.locator('.rpg-guide-nav a[href="#reward-uses"]').click();
      await page.waitForURL('**/#reward-uses');
      assert.equal(await page.locator('#reward-ap').isVisible(), true);
      await page.locator('#reward-stone a[href*="gear/#upgrade"]').click();
      await page.waitForURL('**/gear/#upgrade');
      assert.equal(await page.locator('#enhancement-heading').isVisible(), true);

      for (const width of [320, 390, 768, 1440]) {
        await page.setViewportSize({width, height: 844});
        await page.goto(local + 'routines/');
        await contained(page, lang + '/' + javascript + '/' + width);
        await page.locator('#routine-daily-dungeon summary').click();
        await contained(page, lang + '/open-details/' + width);
      }
      if (javascript) {
        await page.setViewportSize({width: 390, height: 844});
        await page.goto(local + 'routines/');
        await page.screenshot({path: path.join(artifacts, 'routines-' + lang + '-phone.png')});
        await page.locator('#daily-dungeon-choices').scrollIntoViewIfNeeded();
        await page.screenshot({path: path.join(artifacts, 'daily-choices-' + lang + '-phone.png')});
        await page.setViewportSize({width: 1440, height: 1000});
        await page.goto(local + 'routines/#routine-group-weekly');
        await page.screenshot({path: path.join(artifacts, 'weekly-' + lang + '-desktop.png')});
        await page.goto(local + 'search/?q=' + encodeURIComponent(lang === 'ko' ? '오디움' : 'Odylium'));
        const result = page.locator('[data-search-results] a[href$="routines/#daily-choice-odium"]');
        await result.waitFor({state: 'visible'});
        await result.click();
        await page.waitForURL('**/routines/#daily-choice-odium');
        assert.equal(await page.locator('#daily-choice-odium').isVisible(), true);
      }
      for (const route of ['endgame/', 'tools/planner/', 'guides/']) {
        await page.goto(local + route);
        assert.equal(await page.locator('.routine-gateway').isVisible(), true);
      }
      assert.deepEqual(errors, []);
      await context.close();
    }
    // Also exercise the default motion preference with a real native anchor jump.
    const motionContext = await browser.newContext({viewport: {width: 1440, height: 1000}});
    await motionContext.route('https://**/*', route => route.abort());
    const motionPage = await motionContext.newPage();
    await motionPage.goto(base + 'ko/routines/');
    await motionPage.locator('.rpg-guide-nav a[href="#reward-uses"]').click();
    await motionPage.waitForURL('**/#reward-uses');
    await motionPage.waitForFunction(() => {
      const top = document.querySelector('#reward-uses').getBoundingClientRect().top;
      return top >= 60 && top <= 130;
    });
    await motionPage.locator('#reward-stone a[href*="gear/#upgrade"]').click();
    await motionPage.waitForURL('**/gear/#upgrade');
    await motionContext.close();
    console.log('PASS: EN/KR daily/weekly separation, shared scored dungeon choices, regional rewards, source disclosure, search and upgrade routes; JS/no-JS at 320/390/768/1440px.');
  } finally { await browser.close(); await new Promise(resolve => server.close(resolve)); }
})().catch(error => { console.error(error); server.close(); process.exitCode = 1; });
