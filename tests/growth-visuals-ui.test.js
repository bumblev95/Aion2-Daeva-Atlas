/* Exercise actual reward decisions, including no-script and narrow layouts. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '../docs');
const prefix = '/Aion2-Daeva-Atlas/';
const artifacts = process.env.GROWTH_VISUAL_QA_ARTIFACTS || path.resolve(__dirname, '../../growth-visual-qa');
fs.mkdirSync(artifacts, {recursive:true});
const server = http.createServer((req,res) => {
  const route = decodeURIComponent(new URL(req.url, 'http://local').pathname);
  if (!route.startsWith(prefix)) {res.writeHead(404).end();return;}
  let relative = route.slice(prefix.length);
  if (!relative || relative.endsWith('/')) relative += 'index.html';
  const file = path.resolve(root,relative);
  if (!file.startsWith(root+path.sep) || !fs.existsSync(file)) {res.writeHead(404).end();return;}
  const mime={'.html':'text/html','.css':'text/css','.js':'text/javascript','.json':'application/json','.svg':'image/svg+xml','.webp':'image/webp'};
  res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});
  fs.createReadStream(file).pipe(res);
});

async function contained(page, label) {
  const dimensions = await page.evaluate(() => ({width:innerWidth,scroll:document.documentElement.scrollWidth}));
  assert(dimensions.scroll <= dimensions.width+1, label+': overflow '+JSON.stringify(dimensions));
}

(async () => {
  await new Promise(resolve => server.listen(0,'127.0.0.1',resolve));
  const base='http://127.0.0.1:'+server.address().port+prefix;
  let browser;
  try {
    browser = await chromium.launch({headless:true});
    for (const lang of ['ko','en']) for (const javascript of [true,false]) {
      console.log('Visual growth:',lang,javascript?'JS':'no-JS');
      const context = await browser.newContext({viewport:{width:1440,height:1000},javaScriptEnabled:javascript,reducedMotion:'reduce'});
      await context.route('https://**/*',route=>route.abort());
      const page=await context.newPage(),errors=[];
      page.on('pageerror',error=>errors.push(error.message));
      const local=base+(lang==='ko'?'ko/':'');

      await page.goto(local+'endgame/#growth-visual');
      if (javascript) {
        await page.locator('[data-viz-choice="wisdom"]').click();
        assert.equal(await page.locator('#growth-v-wisdom-3').evaluate(n=>n.classList.contains('is-selected')),true);
        assert.equal(await page.locator('[data-viz-panel="feathers"]').isVisible(),false);
        assert.equal(await page.locator('.viz-edges>path.is-selected').first().evaluate(n=>getComputedStyle(n).animationName),'none');
        await page.locator('[data-viz-panel="wisdom"] a').click();
        await page.waitForURL('**/skills/');
      } else assert.equal(await page.locator('#growth-visual [data-viz-panel]:visible').count(),3);
      await page.goto(local+'endgame/#growth-visual');
      await page.setViewportSize({width:390,height:1000});
      assert.equal(await page.locator('#growth-visual .viz-node:visible').count(),javascript?3:9);
      await page.setViewportSize({width:1440,height:1000});

      await page.goto(local+'guides/pet-growth/#pet-visual');
      if (javascript) {
        await page.locator('[data-viz-choice="surplus"]').focus();
        await page.keyboard.press('Space');
        assert.equal(await page.locator('#pet-v-crystal').evaluate(n=>n.classList.contains('is-selected')),true);
        assert.equal(await page.locator('#pet-v-insight').evaluate(n=>n.classList.contains('is-selected')),false);
        await page.locator('[data-viz-panel="surplus"] a').click();
        await page.waitForURL('**/#pet-spending');
      } else assert.equal(await page.locator('#pet-visual [data-viz-panel]:visible').count(),2);

      await page.goto(local+'guides/gear-targets/#gear-visual');
      if (javascript) {
        const cases=[['700','weapon','krao-cave','54'],['700','armor','draupnir','54'],['1400','weapon','urugugu-canyon','70'],['1400','armor','vakron-island','70'],['2100','weapon','fire-temple','86'],['2100','armor','fierce-horn','86']];
        for (const [gate,slot,slug,tier] of cases) {
          await page.locator(`[data-viz-filter="gate"][data-value="${gate}"]`).click();
          await page.locator(`[data-viz-filter="slot"][data-value="${slot}"]`).click();
          const panel=page.locator('[data-dungeon-panel]:visible');
          assert.equal(await panel.count(),1);
          assert.equal(await panel.locator('.viz-target>strong').textContent(),tier);
          assert.equal(await panel.locator(`a[href$="dungeons/${slug}/"]`).count(),1);
          assert.equal(await panel.locator('.viz-entry>strong').textContent(),Number(gate).toLocaleString('en-US'));
        }
        await page.locator('[data-dungeon-panel]:visible a[href$="dungeons/fierce-horn/"]').click();
        await page.waitForURL('**/dungeons/fierce-horn/');
        assert.equal(await page.locator('.dungeon-reward-brief').isVisible(),true);
        // Existing links to a tier and direct links to a hidden choice stay usable.
        await page.goto(local+'guides/gear-targets/#gear-tier-70');
        assert.equal(await page.locator('[data-dungeon-panel]:visible').getAttribute('data-gate'),'1400');
        await page.goto(local+'guides/gear-targets/#gear-pick-vakron');
        assert.equal(await page.locator('[data-dungeon-panel]:visible').getAttribute('data-slot'),'armor');
        await page.locator('[data-dungeon-panel]:visible a[href*="dungeon-rewards/"]').click();
        await page.waitForURL('**/guides/dungeon-rewards/#dungeon-vakron-island');
      } else assert.equal(await page.locator('[data-dungeon-panel]:visible').count(),6);

      await page.goto(local+'guides/kinah-farming/#kinah-visual');
      const value=key=>page.locator(`[data-wallet-value="${key}"]`).textContent();
      assert.equal(await value('leftUnbound'),'150,000');
      if (javascript) {
        await page.locator('[data-viz-choice="market"]').click();
        assert((await page.locator('[data-wallet-status]').textContent()).includes('400,000'));
        assert.equal(await value('leftUnbound'),'200,000'); // A rejected cost does not spend funds.
        assert.equal(await value('usedBound'),'0');
        await page.locator('#wallet-cost').fill('150000');
        assert.equal(await value('leftUnbound'),'50,000');
        assert.equal(await value('leftBound'),'550,000');
        await page.locator('[data-viz-choice="all"]').click();
        assert.equal(await value('leftBound'),'400,000');
        assert.equal(await value('leftUnbound'),'200,000');
        await page.locator('#wallet-cost').fill('0');
        assert.equal(await value('usedBound'),'0');
        await page.locator('#wallet-cost').fill('-1');
        assert.equal(await page.locator('[data-wallet-error]').isVisible(),true);
        assert.equal(await value('usedBound'),'—');
        await page.locator('#wallet-cost').fill('');
        assert.equal(await page.locator('#wallet-cost').getAttribute('aria-invalid'),'true');
        await page.locator('#wallet-cost').fill('1000000000000');
        await page.setViewportSize({width:320,height:844});
        await contained(page,'large amount');
        await page.locator('#wallet-cost').fill('600000');
      } else assert.equal(await page.locator('[data-viz-controls]:visible').count(),0);

      for (const [route,id] of [['endgame/','growth-visual'],['guides/pet-growth/','pet-visual'],['guides/gear-targets/','gear-visual'],['guides/dungeon-rewards/','dungeon-visual'],['guides/kinah-farming/','kinah-visual']]) {
        await page.goto(local+route+'#'+id);
        for (const width of [320,390,768,1440]) {
          await page.setViewportSize({width,height:1000});
          await contained(page,lang+'/'+id+'/'+width+'/'+javascript);
          // Verify all visual nodes keep their own text inside their cards.
          for (const node of await page.locator('.growth-viz .viz-node:visible').all()) {
            assert(await node.evaluate(n=>n.scrollWidth<=n.clientWidth+1),'Node overflow: '+id);
          }
        }
        if (javascript && id!=='dungeon-visual') {
          for (const width of [1440,390]) {
            await page.setViewportSize({width,height:1600});
            await page.addStyleTag({content:'html{scroll-behavior:auto!important}'});
            await page.locator('#'+id).screenshot({path:path.join(artifacts,`visual-${id}-${lang}-${width}.png`)});
          }
        }
      }
      assert.deepEqual(errors,[]);
      await context.close();
    }
    console.log('PASS: visual reward routes, keyboard decisions, all six loot targets, boss links, deep links, wallet limits, reduced motion and mobile/no-script layouts.');
  } finally {if(browser) await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
