'use strict';
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const http=require('node:http'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../docs'),prefix='/Aion2-Daeva-Atlas';
const artifacts=process.env.MAP_QA_ARTIFACTS||'/tmp/aion-map-qa';fs.mkdirSync(artifacts,{recursive:true});
const server=http.createServer((q,r)=>{
 let p=decodeURIComponent(q.url.split('?')[0]).replace(prefix,'');if(p.endsWith('/'))p+='index.html';
 try{r.setHeader('Content-Type',({'.js':'text/javascript','.css':'text/css','.json':'application/json','.webp':'image/webp'})[path.extname(p)]||'text/html');r.end(fs.readFileSync(root+p));}catch{r.writeHead(404).end();}
});
(async()=>{
 await new Promise(r=>server.listen(8768,r));let browser;
 try{
  browser=await chromium.launch({headless:true});
  for(const lang of ['ko/','']){
   const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
   await page.route('https://**',r=>r.abort());page.on('pageerror',e=>errors.push(e.message));
   await page.goto('http://localhost:8768'+prefix+'/'+lang+'maps/',{waitUntil:'domcontentloaded'});
   await page.waitForSelector('.world-pin');
   assert.equal(await page.locator('[data-world-zone]').inputValue(),'Verteron');
   assert.equal(await page.locator('[data-map-resource]').inputValue(),'gather_odyle');
   assert.match(await page.locator('[data-map-summary]').textContent(),/706/);
   assert.match(await page.locator('[data-resource-use]').textContent(),lang?/오드 에너지/:/Odyle Energy/);
   assert.equal(await page.locator('.map-toolbar').evaluate(node=>Boolean(node.compareDocumentPosition(document.querySelector('.resource-finder'))&Node.DOCUMENT_POSITION_FOLLOWING)),true);
   for(const width of [390,1440]){
    await page.setViewportSize({width,height:1000});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
    await page.screenshot({path:path.join(artifacts,'map-entry-'+(lang?'ko':'en')+'-'+width+'.png')});
   }
   await page.setViewportSize({width:390,height:844});
   await page.locator('[data-map-resource]').selectOption('gather_ruby');assert.match(await page.locator('[data-map-summary]').textContent(),/196/);
   await page.locator('.map-place').first().click();assert.match(await page.locator('[data-map-reward]').textContent(),lang?/세공/:/Handicrafting/);
   await page.locator('[data-map-complete]').click();await page.locator('[data-map-hide-done]').check();assert.match(await page.locator('[data-map-summary]').textContent(),/195/);
   await page.locator('[data-resource-reset]').click();assert.match(await page.locator('[data-map-summary]').textContent(),/196/);await page.locator('[data-map-hide-done]').uncheck();
   await page.locator('[data-map-resource]').selectOption('gather_aria');await page.locator('button[data-faction="asmodian"]').click();
   assert.equal(await page.locator('[data-map-resource]').inputValue(),'gather_azpha');assert.match(await page.locator('[data-map-summary]').textContent(),/150/);
   await page.locator('button[data-faction="elyos"]').click();
   await page.locator('[data-map-resource]').selectOption('gather_all');assert.match(await page.locator('[data-map-summary]').textContent(),/2733/);
   await page.locator('[data-map-goal="dungeons"]').click();assert.equal(await page.locator('.map-place').count(),61);await page.locator('a[href$="endgame/#use-rewards"]').click({trial:true});
   await page.waitForFunction(()=>document.querySelector('[data-map-terrain]').naturalWidth===2048);
   await page.locator('[data-map-type="empyrean_trace"]').click();
   assert.match(await page.locator('[data-map-summary]').textContent(),/559/);
   assert.equal(await page.locator('.map-place').count(),100);
   assert.ok(await page.locator('.world-cluster').count()>0);
   await page.locator('[data-map-more]').click();assert.equal(await page.locator('.map-place').count(),200);
   await page.locator('[data-map-type="hidden_cube"]').click();assert.match(await page.locator('[data-map-summary]').textContent(),/1440/);
   assert.match(await page.locator('[data-map-purpose]').textContent(),lang?/후보/:/Possible/);
   await page.locator('button[data-faction="asmodian"]').click();
   assert.equal(await page.locator('[data-world-zone]').inputValue(),'Altgard');
   assert.match(await page.locator('[data-map-summary]').textContent(),/1371/);
   await page.locator('[data-world-zone]').selectOption('Ishalgen');
   assert.equal(await page.locator('.map-place').count(),11);
   assert.match(await page.locator('[data-map-region-title]').textContent(),lang?/마족/:/Asmodian/);
   await page.locator('[data-map-type="hidden_cube"]').click();
   assert.equal(await page.locator('[data-map-empty-box]').isVisible(),true);
   await page.locator('[data-map-next-region]').click();assert.equal(await page.locator('[data-world-zone]').inputValue(),'Altgard');
   await page.locator('[data-world-zone]').selectOption('Ishalgen');
   await page.locator('[data-map-type="quest_episode"]').click();await page.locator('[data-map-search]').fill('Andre');
   assert.equal(await page.locator('.map-place').count(),1);
   // Independent reference: provider zoom-2 coordinate for Andre is (1351.15796,1033.45606), displayed at half size.
   const xy=await page.locator('.world-pin').evaluate(b=>[parseFloat(b.style.left),parseFloat(b.style.top)]);
   assert.ok(Math.abs(xy[0]-675.5789803921568)<.001);assert.ok(Math.abs(xy[1]-516.728031372549)<.001);
   await page.waitForFunction(()=>document.querySelector('[data-map-terrain]').naturalWidth===2048);
   await page.locator('.map-place').click();assert.equal(await page.locator('[data-map-selection]').isVisible(),true);
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);assert.deepEqual(errors,[]);
   await page.locator('[data-map-purpose]').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(artifacts,'map-'+(lang?'ko':'en')+'.png')});
   await page.locator('button[data-faction="elyos"]').click();
   await page.locator('[data-map-goal="gather"]').click();
   await page.locator('[data-map-resource]').selectOption('gather_odyle');
   await page.locator('[data-world-zone]').selectOption('Poeta');
   assert.equal(await page.locator('.map-place').count(),8);
   assert.equal(await page.locator('[data-map-empty-box]').isVisible(),false);
   assert.match(await page.locator('[data-map-region-title]').textContent(),lang?/포에타.*천족/:/Poeta.*Elyos/);
   assert.match(await page.locator('[data-map-region-description]').textContent(),lang?/NPC 7곳·이동 거점 1곳/:/7 story NPC.*1 travel/);
   await page.waitForFunction(()=>document.querySelector('[data-map-terrain]').naturalWidth===2048);
   await page.locator('[data-map-type="gather_all"]').click();
   await page.locator('[data-map-show-story]').click();assert.equal(await page.locator('.map-place').count(),8);
   await page.locator('[data-map-region-farming]').click();assert.equal(await page.locator('[data-world-zone]').inputValue(),'Verteron');
   assert.equal(await page.locator('[data-map-resource]').inputValue(),'gather_odyle');
   // Shared explicit filters stay intact; provide recovery on direct entry too.
   await page.goto('http://localhost:8768'+prefix+'/'+lang+'maps/?zone=Poeta&type=gather_odyle');
   assert.equal(await page.locator('[data-map-empty-box]').isVisible(),true);
   await page.locator('[data-map-show-story]').click();assert.equal(await page.locator('.map-place').count(),8);
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);assert.deepEqual(errors,[]);
   await page.close();
  }
  console.log('PASS: EN/KR phone map, same-origin 2048px terrain with external hosts blocked, source coordinate alignment, material counts/uses, faction herbs, temporary visit checks, collectibles/candidate counts, clustering, pagination, empty tutorial recovery, selection and overflow.');
 }finally{if(browser)await browser.close();server.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
