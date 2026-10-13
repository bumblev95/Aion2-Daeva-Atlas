/* Goal discovery, focused reading and preserved deep links on real generated pages. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '../docs');
const prefix = '/Aion2-Daeva-Atlas/';
const artifacts = process.env.FIND_GUIDE_QA_ARTIFACTS || path.resolve(__dirname, '../../find-guide-qa');
fs.mkdirSync(artifacts, {recursive:true});
const server = http.createServer((req,res) => {
  const route=decodeURIComponent(new URL(req.url,'http://local').pathname);
  if(!route.startsWith(prefix)){res.writeHead(404).end();return;}
  let relative=route.slice(prefix.length);
  if(!relative||relative.endsWith('/'))relative+='index.html';
  const file=path.resolve(root,relative);
  if(!file.startsWith(root+path.sep)||!fs.existsSync(file)){res.writeHead(404).end();return;}
  const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.webp':'image/webp'};
  res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});
  fs.createReadStream(file).pipe(res);
});
async function contained(page,label){
  const sizes=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
  assert(sizes.scroll<=sizes.width+1,label+': '+JSON.stringify(sizes));
}
async function selected(page,key){
  await page.waitForFunction(() => document.querySelector('[data-topic-reader]')?.dataset.readerReady === 'true');
  const panels=await page.locator('[data-reader-panel]').evaluateAll(nodes=>nodes.map(node=>({key:node.dataset.readerPanel,hidden:node.hidden,display:getComputedStyle(node).display,tag:node.tagName})));
  assert.equal(await page.locator('[data-reader-panel]:visible').count(),1,JSON.stringify(panels));
  assert.equal(await page.locator('[data-reader-panel="'+key+'"]').isVisible(),true);
  assert.equal(panels.filter(panel=>!panel.hidden).length,1);
  assert.equal(await page.locator('[data-reader-tab="'+key+'"]').getAttribute('aria-selected'),'true');
}
(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const base='http://127.0.0.1:'+server.address().port+prefix;
  const browser=await chromium.launch({headless:true});
  try{
    for(const lang of ['ko','en']){
      const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
      await context.route('https://**/*',route=>route.abort());
      const page=await context.newPage(),errors=[];
      page.on('pageerror',error=>errors.push(error.message));
      const local=base+(lang==='ko'?'ko/':'');
      for(const width of [320,390,768,1440]){
        await page.setViewportSize({width,height:900});
        await page.goto(local);
        assert.equal(await page.locator('[data-rpg-goal]').count(),4);
        await contained(page,'home '+lang+'/'+width);
        if(width===390||width===1440)await page.screenshot({path:path.join(artifacts,'find-home-'+lang+'-'+width+'.png'),fullPage:true});
      }
      await page.locator('#home-query').fill(lang==='ko'?'오디움':'Odylium');
      await page.locator('.find-search button').click();
      await page.waitForURL('**/search/?q=*');
      await page.locator('[data-search-results] a[href$="routines/#daily-choice-odium"]').click();
      await selected(page,'dungeons');
      assert.equal(await page.locator('#daily-choice-odium').isVisible(),true);
      await page.locator('[data-reader-tab="weekly"]').click();
      await selected(page,'weekly');
      await page.goBack();
      await selected(page,'dungeons');
      await page.goForward();
      await selected(page,'weekly');
      const weekly=page.locator('[data-reader-tab="weekly"]');
      await weekly.focus();await page.keyboard.press('End');
      await selected(page,'rewards');
      assert.equal(await page.locator('[data-reader-tab="rewards"]').evaluate(node=>node===document.activeElement),true);
      await page.keyboard.press('Home');await selected(page,'daily');
      await page.keyboard.press('ArrowLeft');await selected(page,'rewards');
      await page.keyboard.press('ArrowRight');await selected(page,'daily');
      await page.keyboard.press('Space');await selected(page,'daily');
      await page.keyboard.press('Enter');await selected(page,'daily');
      await page.keyboard.press('Tab');
      assert.equal(await page.locator('[data-reader-panel="daily"]').evaluate(node=>node===document.activeElement),true);
      await page.locator('[data-reader-tab="weekly"]').click();
      await page.locator('.navtools .lang').click();
      await page.waitForURL('**/routines/#routine-group-weekly');
      await selected(page,'weekly');
      assert.equal(new URL(page.url()).pathname.includes('/ko/'),lang!=='ko');

      await page.goto(local+'guides/');
      await page.locator('[data-directory-filter="boss"]').click();
      assert.equal(await page.locator('[data-directory-group]:visible').count(),1);
      assert.equal(new URL(page.url()).searchParams.get('topic'),'boss');
      await page.reload();
      assert.equal(await page.locator('[data-directory-group="boss"]').isVisible(),true);
      await page.locator('[data-directory-filter="growth"]').click();
      await page.goBack();
      assert.equal(await page.locator('[data-directory-group="boss"]').isVisible(),true);
      await page.setViewportSize({width:390,height:844});
      await page.screenshot({path:path.join(artifacts,'find-directory-'+lang+'-390.png')});
      await page.locator('[data-directory-filter="all"]').click();
      await page.locator('[data-growth-guide="pet-growth"]').click();
      await page.locator('[data-reader-tab="farm"]').click();
      await selected(page,'farm');
      await page.screenshot({path:path.join(artifacts,'find-pet-farm-'+lang+'-390.png')});
      await page.goto(local+'endgame/#after-story-field-rewards');
      assert.equal(await page.locator('#after-story-field-rewards details').getAttribute('open'),'');
      assert.equal(await page.locator('#after-story-field-rewards a[href*="zone=Altgard"]').isVisible(),true);
      await page.goto(local+'guides/dungeon-rewards/#dungeon-fire-temple');
      assert.equal(await page.locator('#dungeon-fire-temple').getAttribute('open'),'');
      assert.equal(await page.locator('#dungeon-fire-temple .dungeon-loot').isVisible(),true);
      await page.goto(local+'endgame/');
      assert.equal(await page.locator('.growth-route details[open]').count(),1);
      await page.screenshot({path:path.join(artifacts,'find-growth-'+lang+'-390.png'),fullPage:true});
      for(const width of [320,390,768,1440]){
        await page.setViewportSize({width,height:844});
        for(const route of ['guides/','endgame/','gear/','routines/']){
          await page.goto(local+route);await contained(page,route+lang+'/'+width);
        }
      }
      await page.setViewportSize({width:390,height:844});
      await page.goto(local);
      assert.equal(await page.locator('.mobile-dock').isVisible(),true);
      assert.equal(await page.locator('.mobile-dock a').count(),5);
      assert.equal(await page.locator('#main-nav').evaluate(node=>node.inert),true);
      await page.locator('[data-menu]').click();
      assert.equal(await page.locator('#main-nav').evaluate(node=>node.inert),false);
      await page.locator('.nav-reference>summary').click();
      await page.screenshot({path:path.join(artifacts,'find-menu-'+lang+'-390.png')});
      await page.keyboard.press('Escape');
      assert.equal(await page.locator('[data-menu]').getAttribute('aria-expanded'),'false');
      assert.equal(await page.locator('[data-menu]').evaluate(node=>node===document.activeElement),true);
      await page.locator('.mobile-dock a[href$="routines/"]').click();
      await selected(page,'daily');
      await page.locator('[data-reader-tab="weekly"]').click();
      await page.screenshot({path:path.join(artifacts,'find-weekly-'+lang+'-390.png')});
      assert.deepEqual(errors,[]);
      await context.close();
    }
    for(const lang of ['ko','en']) for(const width of [320,390,768,1440]){
    const local=base+(lang==='ko'?'ko/':'');
    const context=await browser.newContext({javaScriptEnabled:false,viewport:{width,height:844},reducedMotion:'reduce'});
    await context.route('https://**/*',route=>route.abort());
    const page=await context.newPage();
    await page.goto(local+'routines/');
    await page.locator('[data-reader-panel="weekly"]>.reader-fallback').click();
    assert.equal(await page.locator('#routine-daily-dungeon').isVisible(),true);
    await page.goto(local+'guides/dungeon-rewards/#dungeon-fire-temple');
    assert.equal(await page.locator('#dungeon-fire-temple .dungeon-loot').isVisible(),true);
    await contained(page,'native disclosure');
    await page.goto(local+'guides/');
    assert.equal(await page.locator('[data-directory-group]:visible').count(),5);
    assert.equal(await page.locator('[data-directory-controls]').isVisible(),false);
    await context.close();
    }
    console.log('PASS: task-first discovery, search, topic keyboard navigation, history, bilingual deep links, filtering, mobile dock/menu and native disclosure.');
  }finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
