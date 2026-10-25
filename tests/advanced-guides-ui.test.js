/* Verify the published guide journey and numerical boundary/error cases. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '../docs'), prefix = '/Aion2-Daeva-Atlas/';
const artifacts = process.env.ADVANCED_GUIDE_QA_ARTIFACTS || path.resolve(__dirname, '../../advanced-guide-qa');
const slugs = ['gear-options', 'shugo-festival', 'stigma-growth', 'endgame-crafts', 'kr-pendant', 'kr-bitan'];
fs.mkdirSync(artifacts, {recursive:true});
const server = http.createServer((req,res) => {
  const route=decodeURIComponent(new URL(req.url,'http://local').pathname);
  if(!route.startsWith(prefix)){res.writeHead(404).end();return;}
  let relative=route.slice(prefix.length);if(!relative||relative.endsWith('/'))relative+='index.html';
  const file=path.resolve(root,relative);
  if(!file.startsWith(root+path.sep)||!fs.existsSync(file)){res.writeHead(404).end();return;}
  const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.webp':'image/webp'};
  res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});
  fs.createReadStream(file).pipe(res);
});
async function contained(page,label) {
  const sizes=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
  assert(sizes.scroll<=sizes.width+1,label+': '+JSON.stringify(sizes));
}
async function screenshot(page, options) {
  // Topic changes schedule scrolling; capture after it settles at the page top.
  if (options.fullPage) await page.evaluate(() => scrollTo({top:0,behavior:'instant'}));
  await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
  await page.waitForFunction(() => {
    const header=document.querySelector('.masthead').getBoundingClientRect();
    const dock=document.querySelector('.mobile-dock');
    return Math.abs(header.top)<1 && (getComputedStyle(dock).display==='none' || Math.abs(dock.getBoundingClientRect().bottom-innerHeight)<1);
  });
  if (options.fullPage) {
    await page.evaluate(() => scrollTo({top:0,behavior:'instant'}));
    await page.waitForFunction(() => scrollY===0);
  }
  await page.screenshot(options);
}
async function panel(page,key) {
  await page.waitForFunction(()=>document.querySelector('[data-topic-reader]')?.dataset.readerReady==='true');
  await page.locator('[data-reader-tab="'+key+'"]').click();
  assert.equal(await page.locator('[data-reader-panel]:visible').count(),1);
  assert.equal(await page.locator('[data-reader-panel="'+key+'"]').isVisible(),true);
}
(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const base='http://127.0.0.1:'+server.address().port+prefix;
  const browser=await chromium.launch({headless:true});
  try {
    for(const lang of ['ko','en']) {
      const context=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});
      await context.route('https://**/*',route=>route.abort());
      const page=await context.newPage(),errors=[];
      page.on('pageerror',error=>errors.push(error.message));
      const local=base+(lang==='ko'?'ko/':'');
      await page.goto(local+'gear/');
      await page.locator('[data-practical-guide="gear-options"]').click();
      await page.waitForURL('**/guides/gear-options/');
      for(const mode of ['reset','bind','sync']) {
        await page.locator('[data-option-mode="'+mode+'"]').click();
        assert.equal(await page.locator('[data-option-panel]:visible').getAttribute('data-option-panel'),mode);
      }
      await panel(page,'transfer');
      assert.equal(await page.locator('#transfer-route .ag-note').isVisible(),true);
      await page.locator('.navtools .lang').click();
      await page.waitForURL('**/guides/gear-options/#transfer-route');
      assert.equal(new URL(page.url()).pathname.includes('/ko/'),lang!=='ko');
      assert.equal(await page.locator('[data-reader-panel="transfer"]').isVisible(),true);
      await page.goto(local+'routines/');
      await page.locator('[data-practical-guide="shugo-festival"]').click();
      assert.equal(await page.locator('.ag-game-grid>article').count(),9);
      await panel(page,'keys');await contained(page,'festival keys '+lang);
      await panel(page,'shop');
      await page.locator('#festival-shop a[href$="stigma-growth/"]').click();
      await panel(page,'levels');
      await page.locator('[data-stigma-from]').selectOption('10');
      await page.locator('[data-stigma-to]').selectOption('20');
      assert.match(await page.locator('[data-stigma-result]').textContent(),/60/);
      await page.locator('[data-stigma-from]').selectOption('20');
      await page.locator('[data-stigma-to]').selectOption('10');
      assert.equal(await page.locator('[data-stigma-to]').getAttribute('aria-invalid'),'true');
      await panel(page,'kr-shop');
      assert.equal(await page.locator('.ag-table tbody tr').count(),5);
      await screenshot(page,{path:path.join(artifacts,'stigma-shop-'+lang+'-390.png'),fullPage:true});
      await page.goto(local+'guides/endgame-crafts/');
      assert.equal(await page.locator('[data-ludra-scope]').isVisible(),true);
      assert.match(await page.locator('#craft-bracelet').textContent(),/3 Ludra Gear Vouchers|3개/);
      assert.match(await page.locator('#craft-bracelet').textContent(),/5,000,000/);
      assert.match(await page.locator('#craft-bracelet').textContent(),/NA applicability remains unverified|북미 적용은 미확인/);
      await page.locator('[data-ludra-scope] a[href="#craft-na-ludra"]').click();
      assert.equal(await page.locator('[data-reader-panel="na-ludra"]').isVisible(),true);
      const preparation=await page.locator('#craft-na-ludra').textContent();
      for(const token of ['2,800','3,000','102','PST']) assert(preparation.includes(token));
      assert.match(preparation,/not published|공개하지 않았/);
      await screenshot(page,{path:path.join(artifacts,'na-ludra-preparation-'+lang+'-390.png'),fullPage:true});
      await page.locator('.navtools a.lang').click();
      await page.waitForURL('**/guides/endgame-crafts/#craft-na-ludra');
      assert.equal(new URL(page.url()).pathname.includes('/ko/'),lang!=='ko');
      assert.equal(await page.locator('#craft-na-ludra').isVisible(),true);
      await page.goto(local+'guides/kr-pendant/');
      await page.locator('[data-pendant-failures]').fill('2');
      assert.equal(await page.locator('[data-pendant-chance]').textContent(),'85%');
      await page.locator('[data-pendant-level]').selectOption('19');
      assert.equal(await page.locator('[data-pendant-failures]').inputValue(),'0');
      assert.equal(await page.locator('[data-pendant-chance]').textContent(),'1%');
      await page.locator('[data-pendant-failures]').fill('50');
      assert.equal(await page.locator('[data-pendant-chance]').textContent(),'100%');
      for(const invalid of ['', '-1', '1.5', '101']) {
        await page.locator('[data-pendant-failures]').fill(invalid);
        assert.equal(await page.locator('[data-pendant-failures]').getAttribute('aria-invalid'),'true');
        assert.equal(await page.locator('[data-pendant-chance]').textContent(),'—');
      }
      await page.locator('[data-pendant-failures]').fill('1');
      assert.equal(await page.locator('[data-pendant-chance]').textContent(),'3%');
      await screenshot(page,{path:path.join(artifacts,'pendant-'+lang+'-390.png'),fullPage:true});
      await page.goto(local+'guides/kr-bitan/#bitan-movement');
      const raid=page.locator('[data-raid-lesson="movement"]');
      assert.equal(await raid.getAttribute('data-playing'),'false');
      await raid.locator('[data-raid-next]').click();
      assert.equal(await raid.getAttribute('data-phase'),'1');
      await raid.locator('[data-raid-next]').click();
      assert.equal(await raid.getAttribute('data-phase'),'2');
      await screenshot(page,{path:path.join(artifacts,'bitan-'+lang+'-390.png'),fullPage:true});
      await page.goto(local+'search/?q='+encodeURIComponent(lang==='ko'?'계승':'Soul Binding'));
      await page.locator('[data-search-results] a[href$="guides/gear-options/"]').click();
      for(const width of [320,390,768,1440]) {
        await page.setViewportSize({width,height:900});
        for(const slug of slugs) {
          await page.goto(local+'guides/'+slug+'/');
          await contained(page,slug+'/'+lang+'/'+width);
          const tabs=await page.locator('[data-reader-tab]').count();
          for(let i=0;i<tabs;i++) {
            await page.locator('[data-reader-tab]').nth(i).click();
            await contained(page,slug+' panel '+i+'/'+lang+'/'+width);
          }
          if(width===1440) {
            await page.locator('[data-reader-tab]').first().click();
            await screenshot(page,{path:path.join(artifacts,slug+'-'+lang+'-1440.png'),fullPage:true});
          }
        }
      }
      assert.deepEqual(errors,[]);
      await context.close();
      const native=await browser.newContext({javaScriptEnabled:false,viewport:{width:320,height:800}});
      await native.route('https://**/*',route=>route.abort());
      const fallback=await native.newPage();
      for(const slug of slugs) {
        await fallback.goto(local+'guides/'+slug+'/');
        await fallback.locator('.reader-panel').last().locator('summary.reader-fallback').click();
        assert.equal(await fallback.locator('.reader-panel').last().getAttribute('open'),'');
        await contained(fallback,'no-script '+slug+'/'+lang);
        assert.equal(await fallback.locator('a[href^="https://"]').count()>0,true);
        if(slug==='endgame-crafts') {
          await fallback.locator('[data-reader-panel="na-ludra"] > summary').click();
          assert.equal(await fallback.locator('#craft-na-ludra').isVisible(),true);
          await contained(fallback,'no-script NA preparation/'+lang);
        }
      }
      await native.close();
    }
    const motion=await browser.newContext({viewport:{width:1000,height:950},reducedMotion:'no-preference'});
    await motion.route('https://**/*',route=>route.abort());
    const page=await motion.newPage();
    await page.goto(base+'ko/guides/kr-bitan/');
    const raid=page.locator('[data-raid-lesson="orbs"]');
    await raid.scrollIntoViewIfNeeded();
    await page.waitForFunction(()=>document.querySelector('[data-raid-lesson="orbs"]').dataset.phase!=='0',{},{timeout:6500});
    await raid.locator('[data-raid-play]').click();
    const phase=await raid.getAttribute('data-phase');
    assert.equal(await raid.getAttribute('data-playing'),'false');
    assert.equal(await raid.locator('.ag-cold').first().evaluate(n=>getComputedStyle(n).animationPlayState),'paused');
    await page.waitForTimeout(3300);
    assert.equal(await raid.getAttribute('data-phase'),phase);
    await motion.close();
    console.log('Advanced guides: bilingual navigation, six routes, 9 games, cost/probability boundaries, autoplay/pause, no-script and 320–1440px verified.');
  } finally {await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(error=>{console.error(error);process.exitCode=1;server.close();});
