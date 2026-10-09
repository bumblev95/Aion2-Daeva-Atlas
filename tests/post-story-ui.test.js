/* Follow generated guide links, preserve saved progress and exercise real map filters. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '../docs');
const prefix = '/Aion2-Daeva-Atlas/';
const artifacts = process.env.POST_STORY_QA_ARTIFACTS || path.resolve(__dirname, '../../post-story-qa-artifacts');
fs.mkdirSync(artifacts, {recursive: true});
const server = http.createServer((req, res) => {
  let relative = decodeURIComponent(new URL(req.url, 'http://local').pathname);
  if (!relative.startsWith(prefix)) { res.writeHead(404).end(); return; }
  relative = relative.slice(prefix.length);
  if (relative.endsWith('/') || !relative) relative += 'index.html';
  const file = path.resolve(root, relative);
  if (!file.startsWith(root + path.sep) || !fs.existsSync(file)) { res.writeHead(404).end(); return; }
  const type = {'.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json',
    '.css': 'text/css', '.svg': 'image/svg+xml', '.webp': 'image/webp'}[path.extname(file)] || 'application/octet-stream';
  res.writeHead(200, {'Content-Type': type});
  fs.createReadStream(file).pipe(res);
});

async function contained(page, label) {
  const sizes = await page.evaluate(() => ({viewport: innerWidth, page: document.documentElement.scrollWidth}));
  assert.ok(sizes.page <= sizes.viewport + 1, JSON.stringify({label, ...sizes}));
}

(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = 'http://127.0.0.1:' + server.address().port + prefix;
  let browser;
  try {
    browser = await chromium.launch({headless: true});
    for (const lang of ['en', 'ko']) {
      const local = base + (lang === 'ko' ? 'ko/' : '');
      const context = await browser.newContext({viewport: {width: 1440, height: 1000}});
      await context.route('https://**/*', route => route.abort());
      await context.addInitScript(() => {
        if (localStorage.getItem('players-codex-start-v1') === null) {
          localStorage.setItem('players-codex-start-v1', JSON.stringify(['story']));
        }
      });
      const page = await context.newPage(), errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.goto(local);
      assert.equal(await page.locator('[data-rpg-goal]').count(), 3);
      for (const width of [320, 390, 768, 1440]) {
        await page.setViewportSize({width, height: 844});
        await contained(page, lang + ' RPG home');
      }
      await page.setViewportSize({width: 390, height: 844});
      await page.locator('.rpg-home-goals').scrollIntoViewIfNeeded();
      await page.screenshot({path: path.join(artifacts, 'rpg-goals-home-' + lang + '.png')});
      await page.locator('[data-rpg-goal="boss"]').click();
      await page.waitForURL('**/endgame/#boss-guides');
      assert.equal(await page.locator('#boss-guides').isVisible(), true);
      const bossLink = page.locator('.endgame-boss').first();
      const bossUrl = new URL(await bossLink.getAttribute('href'), local).href;
      await bossLink.click();
      await page.waitForURL(bossUrl);
      await page.goto(local);
      await page.locator('[data-rpg-goal="enhancement"]').click();
      await page.waitForURL('**/gear/#upgrade');
      assert.equal(await page.locator('#enhancement-heading').isVisible(), true);
      assert.equal(await page.locator('#enhancement-process > li').count(), 4);
      assert.equal(await page.locator('#enhancement-materials tbody tr').count(), 3);
      for (const width of [320, 390, 768, 1440]) {
        await page.setViewportSize({width, height: 844});
        await contained(page, lang + ' enhancement');
      }
      await page.setViewportSize({width: 390, height: 844});
      await page.locator('#enhancement-materials').scrollIntoViewIfNeeded();
      await page.screenshot({path: path.join(artifacts, 'enhancement-materials-' + lang + '.png')});
      await page.locator('.rpg-guide-nav a[href="#upgrade-decisions"]').click();
      await page.waitForURL('**/gear/#upgrade-decisions');
      assert.equal(await page.locator('#upgrade-decisions').isVisible(), true);
      await page.goto(local);
      await page.locator('.home-stage.endgame').click();
      await page.waitForURL('**/endgame/#after-story');
      assert.equal(await page.locator('#after-story-heading').isVisible(), true);
      assert.equal(await page.locator('.growth-route > li').count(), 5);
      assert.equal(await page.locator('#use-rewards tbody tr').count(), 5);
      const feather = page.locator('#after-story-feathers .reference-links a');
      assert.equal(await feather.getAttribute('href'), 'https://www.inven.co.kr/webzine/news/?news=311568&site=aion2');
      assert.equal(await feather.getAttribute('target'), '_blank');
      for (const width of [320, 390, 768, 1440]) {
        await page.setViewportSize({width, height: 844});
        await contained(page, lang + ' post-story');
      }
      await page.setViewportSize({width: 390, height: 844});
      await page.locator('#after-story-heading').scrollIntoViewIfNeeded();
      await page.screenshot({path: path.join(artifacts, 'post-story-mobile-' + lang + '.png')});
      await page.locator('#use-rewards').scrollIntoViewIfNeeded();
      await page.screenshot({path: path.join(artifacts, 'post-story-rewards-' + lang + '.png')});
      await page.setViewportSize({width: 1440, height: 1000});
      // Both faction links must open the correct real sealed-dungeon marker set.
      for (const zone of ['Verteron', 'Altgard']) {
        await page.goto(local + 'endgame/#after-story-field-rewards');
        await page.locator('#after-story-field-rewards a[href*="zone=' + zone + '"]').click();
        await page.waitForURL(url => url.pathname.endsWith('/maps/') && url.searchParams.get('type') === 'sealed_dungeon' && url.searchParams.get('zone') === zone);
        assert.equal(await page.locator('[data-world-zone]').inputValue(), zone);
        assert.equal(await page.locator('[data-map-type="sealed_dungeon"]').getAttribute('aria-pressed'), 'true');
        assert.ok(await page.locator('[data-map-pins] [data-point-id]').count() > 0);
        assert.ok((await page.locator('[data-map-reward]').textContent()).includes(lang === 'ko' ? '지혜의 돌' : 'Wisdom Stones'));
        assert.ok((await page.locator('[data-map-reward]').textContent()).includes(lang === 'ko' ? '데바니온 결정' : 'Daevanion Crystals'));
        await page.locator('a[href$="endgame/#use-rewards"]').click();
        await page.waitForURL('**/endgame/#use-rewards');
        assert.equal(await page.locator('#use-rewards').isVisible(), true);
      }
      await page.goto(local + 'start/');
      assert.equal(await page.locator('.post-story-gateway').isVisible(), true);
      await page.locator('.post-story-gateway').click();
      await page.waitForURL('**/endgame/#after-story');
      await page.goto(local + 'start/?view=growth&step=after-story');
      assert.equal(await page.locator('[data-journey-stage="after-story"]').getAttribute('aria-pressed'), 'true');
      assert.equal(await page.locator('[data-journey-panel="after-story"]').isVisible(), true);
      assert.equal(await page.locator('[data-start-task="story"]').isChecked(), true);
      await page.locator('[data-start-task="post-points"]').check();
      await page.reload();
      assert.equal(await page.locator('[data-start-task="post-points"]').isChecked(), true);
      assert.equal(await page.locator('[data-start-task="story"]').isChecked(), true);
      assert.deepEqual(await page.evaluate(() => JSON.parse(localStorage.getItem('players-codex-start-v1'))), ['story', 'post-points']);
      for (const width of [320, 390, 768, 1440]) {
        await page.setViewportSize({width, height: 844});
        await contained(page, lang + ' journey');
      }
      await page.setViewportSize({width: 390, height: 844});
      await page.locator('[data-journey-panel="after-story"] > .journey-heading').scrollIntoViewIfNeeded();
      await page.screenshot({path: path.join(artifacts, 'post-story-checklist-' + lang + '.png')});
      await page.locator('.lang').click();
      await page.waitForURL(url => url.searchParams.get('step') === 'after-story' && url.pathname !== new URL(local + 'start/').pathname);
      assert.equal(await page.locator('[data-journey-panel="after-story"]').isVisible(), true);
      assert.equal(await page.locator('[data-start-task="post-points"]').isChecked(), true);
      assert.deepEqual(errors, []);
      await context.close();
      const noScript = await browser.newContext({javaScriptEnabled: false, viewport: {width: 390, height: 844}});
      await noScript.route('https://**/*', route => route.abort());
      const staticPage = await noScript.newPage();
      await staticPage.goto(local + 'endgame/#after-story');
      assert.equal(await staticPage.locator('#after-story-heading').isVisible(), true);
      assert.equal(await staticPage.locator('#use-rewards tbody tr').count(), 5);
      await contained(staticPage, lang + ' no-script');
      await staticPage.goto(local + 'gear/#upgrade');
      assert.equal(await staticPage.locator('#enhancement-heading').isVisible(), true);
      assert.equal(await staticPage.locator('#enhancement-process > li').count(), 4);
      await contained(staticPage, lang + ' enhancement no-script');
      await noScript.close();
    }
    console.log('PASS: EN/KR three-goal home → growth / boss / enhancement, material routes, both faction map filters, reward use, saved legacy checks, language deep links, no-script guides and 320/390/768/1440px layout.');
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
