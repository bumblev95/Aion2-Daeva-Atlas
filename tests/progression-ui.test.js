/* Follow real discovery → reward → growth routes, with and without scripts. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '../docs');
const prefix = '/Aion2-Daeva-Atlas/';
const artifacts = process.env.PROGRESSION_QA_ARTIFACTS || path.resolve(__dirname, '../../progression-qa-artifacts');
fs.mkdirSync(artifacts, {recursive: true});
const server = http.createServer((req, res) => {
  const route = decodeURIComponent(new URL(req.url, 'http://local').pathname);
  if (!route.startsWith(prefix)) {res.writeHead(404).end(); return;}
  let relative = route.slice(prefix.length);
  if (!relative || relative.endsWith('/')) relative += 'index.html';
  const file = path.resolve(root, relative);
  if (!file.startsWith(root + path.sep) || !fs.existsSync(file)) {res.writeHead(404).end(); return;}
  const mime = {'.html':'text/html', '.js':'text/javascript', '.css':'text/css', '.json':'application/json', '.svg':'image/svg+xml', '.webp':'image/webp'};
  res.writeHead(200, {'Content-Type': mime[path.extname(file)] || 'application/octet-stream'});
  fs.createReadStream(file).pipe(res);
});
const routes = ['pet-growth','gear-targets','dungeon-rewards','kinah-farming'];

async function auditGuideLinks(page) {
  const links = await page.locator('.progress-guide a').evaluateAll(nodes => nodes.map(n => n.href));
  for (const link of links) {
    const u = new URL(link);
    if (u.origin !== new URL(page.url()).origin || !u.pathname.startsWith(prefix)) continue;
    const file = path.join(root, decodeURIComponent(u.pathname.slice(prefix.length)), 'index.html');
    assert(fs.existsSync(file), 'Missing destination: ' + link);
    if (u.hash) assert(fs.readFileSync(file,'utf8').includes('id="' + decodeURIComponent(u.hash.slice(1)) + '"'), 'Missing target fragment: ' + link);
  }
}

async function contained(page, label) {
  const box = await page.evaluate(() => ({width:innerWidth, scroll:document.documentElement.scrollWidth}));
  assert(box.scroll <= box.width + 1, label + ': horizontal overflow ' + JSON.stringify(box));
}

(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = 'http://127.0.0.1:' + server.address().port + prefix;
  let browser;
  try {
    browser = await chromium.launch({headless:true});
    for (const lang of ['en','ko']) for (const javascript of [true,false]) {
      console.log('Progression:',lang,javascript ? 'JS' : 'no-JS');
      const context = await browser.newContext({viewport:{width:1440,height:1000},javaScriptEnabled:javascript,reducedMotion:'reduce'});
      await context.route('https://**/*', route => route.abort());
      const page = await context.newPage(), errors = [];
      page.on('pageerror', error => errors.push(error.message));
      const local = base + (lang==='ko' ? 'ko/' : '');
      await page.goto(local);
      await page.locator('[data-growth-guide="pet-growth"]').click();
      await page.waitForURL('**/guides/pet-growth/');
      await page.locator('.progress-jumps a[href="#pet-asmodian"]').click();
      assert.equal(await page.locator('#pet-mumu').isVisible(), true);
      await page.locator('#pet-asmodian a[href*="zone=Altgard"]').click();
      await page.waitForURL('**/maps/?zone=Altgard');
      if (javascript) assert.equal(await page.locator('[data-world-zone]').inputValue(), 'Altgard');

      for (const slug of routes) {
        await page.goto(local + 'guides/' + slug + '/');
        await auditGuideLinks(page);
        assert.equal(await page.locator('.progress-series [aria-current="page"]').getAttribute('href'),prefix+(lang==='ko'?'ko/':'')+'guides/'+slug+'/');
        for (const width of [320,390,768,1440]) {
          await page.setViewportSize({width,height:844});
          await contained(page,lang+'/'+slug+'/'+width+'/'+javascript);
          if (width <= 600) for (const heading of await page.locator('.progress-table tbody th').all()) {
            const size = await heading.evaluate(node => ({cell:node.getBoundingClientRect().width,row:node.closest('tr').getBoundingClientRect().width}));
            assert(size.cell >= size.row * .8, 'Mobile row title must use the card width: '+JSON.stringify(size));
          }
          await page.locator('#growth-sources').evaluate(node => {node.open = true;});
          await contained(page,lang+'/'+slug+'/open-sources/'+width);
          await page.locator('#growth-sources').evaluate(node => {node.open = false;});
        }
        // Cross-page language switch keeps the same guide, not the guide index.
        const other = lang==='ko' ? '' : 'ko/';
        assert.equal(await page.locator('.navtools a.lang').getAttribute('href'),prefix+other+'guides/'+slug+'/');
        if (javascript) {
          await page.setViewportSize({width:390,height:844});
          await page.goto(local+'guides/'+slug+'/');
          await page.screenshot({path:path.join(artifacts,'growth-'+slug+'-'+lang+'-phone.png')});
        }
      }

      await page.goto(local+'guides/gear-targets/');
      await page.locator('#gear-tier-86 a[href$="dungeon-rewards/#dungeon-fire-temple"]').click();
      await page.waitForURL('**/guides/dungeon-rewards/#dungeon-fire-temple');
      const plan=page.locator('#dungeon-fire-temple');
      assert((await plan.textContent()).includes('2,100'));
      assert((await plan.textContent()).includes('Enraged Kromede Claymore'));
      assert((await plan.locator('.dungeon-response').textContent()).includes(lang==='ko'?'한국':'KR'));
      await plan.locator('a[href$="dungeons/fire-temple/"]').click();
      await page.waitForURL('**/dungeons/fire-temple/');
      assert.equal(await page.locator('.dungeon-reward-brief').isVisible(),true);
      await page.locator('.dungeon-reward-brief a').click();
      await page.waitForURL('**/guides/dungeon-rewards/#dungeon-fire-temple');

      await page.locator('.progress-series a[href$="kinah-farming/"]').click();
      await page.locator('#kinah-fixed a[href$="routines/#routine-duties"]').click();
      await page.waitForURL('**/routines/#routine-duties');
      assert.equal(await page.locator('#routine-duties').isVisible(),true);
      await page.locator('#reward-pet a[href$="guides/pet-growth/"]').click();
      await page.waitForURL('**/guides/pet-growth/');
      await page.locator('.progress-cite a[href="#growth-source-pet-system"]').first().click();
      assert.equal(await page.locator('#growth-source-pet-system').isVisible(),true);
      assert((await page.locator('#growth-source-game8').textContent()).includes('402'));

      for (const route of ['endgame/','guides/']) {
        await page.goto(local+route);
        assert.equal(await page.locator('[data-growth-guide="pet-growth"]').isVisible(),true);
      }
      await page.goto(local+'gear/');
      await page.locator('.growth-gateway').click();
      await page.waitForURL('**/guides/gear-targets/');
      if (javascript) {
        for (const [query, destination] of [[lang==='ko'?'무무 일꾼':'Mumu Worker','pet-growth/#pet-mumu'],['Enraged Kromede Claymore','dungeon-rewards/#dungeon-fire-temple']]) {
          await page.goto(local+'search/?q='+encodeURIComponent(query));
          await page.locator('[data-search-results] a[href$="guides/'+destination+'"]').click();
          await page.waitForURL('**/guides/'+destination);
        }
        await page.setViewportSize({width:1440,height:1100});
        await page.goto(local+'guides/gear-targets/#gear-ladder');
        await page.screenshot({path:path.join(artifacts,'growth-gear-ladder-'+lang+'-desktop.png')});
        await page.goto(local+'guides/dungeon-rewards/#dungeon-vakron-island');
        await page.screenshot({path:path.join(artifacts,'growth-vakron-'+lang+'-desktop.png')});
        await page.setViewportSize({width:390,height:1000});
        for (const [slug, anchor] of [['pet-growth','pet-asmodian'],['gear-targets','gear-tier-70'],['kinah-farming','kinah-fixed']]) {
          await page.goto(local+'guides/'+slug+'/#'+anchor);
          await page.screenshot({path:path.join(artifacts,'growth-'+anchor+'-'+lang+'-phone.png')});
        }
      }
      assert.deepEqual(errors,[]);
      await context.close();
    }
    console.log('PASS: growth guides, regional sources, reward/gear/boss routes, pet map routing, search, cross-page anchors, language switches and mobile/no-script layout.');
  } finally {if (browser) await browser.close(); await new Promise(resolve => server.close(resolve));}
})().catch(error => {console.error(error);server.close();process.exitCode=1;});
