'use strict';
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const http=require('node:http'),fs=require('node:fs'),path=require('node:path');
const audit=require('../research/map-spatial-audit.json');
const root=path.resolve(__dirname,'../docs'),prefix='/Aion2-Daeva-Atlas';
const artifacts=process.env.MAP_QA_ARTIFACTS||'/tmp/aion-map-spatial-qa';fs.mkdirSync(artifacts,{recursive:true});
const server=http.createServer((q,r)=>{
 let p=decodeURIComponent(q.url.split('?')[0]).replace(prefix,'');if(p.endsWith('/'))p+='index.html';
 try{r.setHeader('Content-Type',({'.js':'text/javascript','.css':'text/css','.json':'application/json','.webp':'image/webp'})[path.extname(p)]||'text/html');
  // Optional, exact fetched public JS for reproducing the pre-fix gesture failure.
  r.end(fs.readFileSync(process.env.MAP_QA_BASELINE_JS&&p==='/assets/deep-guide.js'?process.env.MAP_QA_BASELINE_JS:root+p));
 }catch{r.writeHead(404).end();}
});
const frame=p=>p.evaluate(()=>new Promise(requestAnimationFrame));
const matrix=p=>p.locator('[data-map-world]').evaluate(w=>{const m=new DOMMatrix(getComputedStyle(w).transform);return {scale:m.a,x:m.e,y:m.f};});
(async()=>{
 await new Promise(r=>server.listen(0,r));const base='http://localhost:'+server.address().port+prefix;let browser;
 try{
  browser=await chromium.launch({headless:true,...(process.env.MAP_QA_CHROMIUM?{executablePath:process.env.MAP_QA_CHROMIUM}:{})});
  for(const lang of ['ko/','']){
   let page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true,reducedMotion:'reduce'}),errors=[];
   await page.route('https://**',r=>r.abort());page.on('pageerror',e=>errors.push(e.message));
   for(const sample of audit.samples){
    const query=new URLSearchParams({zone:sample.region,type:sample.type,point:sample.stableId});
    await page.goto(base+'/'+lang+'maps/?'+query,{waitUntil:'domcontentloaded'});
    await page.waitForFunction(()=>document.querySelector('[data-map-terrain]').naturalWidth===2048);
    const pin=page.locator('.world-pin[data-point-id="'+sample.stableId+'"]');
    const xy=await pin.evaluate(b=>[parseFloat(b.style.left),parseFloat(b.style.top)]);
    xy.forEach((v,i)=>assert.ok(Math.abs(v-sample.expectedLocalPixel[i])<.001,`${sample.region}/${sample.stableId} coordinate ${i}`));
    assert.equal(await pin.getAttribute('aria-pressed'),'true');
    const offset=await pin.evaluate(b=>{const r=b.getBoundingClientRect(),v=document.querySelector('[data-map-viewport]').getBoundingClientRect();return [r.x+r.width/2-(v.x+v.width/2),r.y+r.height/2-(v.y+v.height/2)];});
    offset.forEach(v=>assert.ok(Math.abs(v)<.1,`${sample.region}/${sample.stableId}: selected marker offset ${offset}`));
    const u=new URL(await page.locator('[data-map-source]').getAttribute('href'));assert.equal(u.searchParams.get('center'),sample.position.slice(0,2).join(','));
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
   }
   await page.goto(base+'/'+lang+'maps/?zone=Verteron&type=sealed_dungeon');
   await page.locator('.world-pin').first().waitFor();
   const id=new URL(page.url()).searchParams.get('point');
   await page.locator('[data-map-complete]').click();
   const checks=await page.evaluate(()=>JSON.parse(localStorage.getItem('players-codex-map-v1')));
   assert.ok(checks.includes('Verteron:'+id));
   await page.reload();assert.equal(await page.locator('[data-map-complete]').getAttribute('aria-pressed'),'true');
   const other=await page.locator('a.lang').getAttribute('href');assert.equal(new URL(other).searchParams.get('point'),id);
   await page.goto(other);assert.equal(await page.locator('[data-map-complete]').getAttribute('aria-pressed'),'true');
   assert.equal(await page.locator('[data-world-zone]').inputValue(),'Verteron');
   assert.equal(new URL(page.url()).searchParams.get('point'),id);
   await page.goto(base+'/'+lang+'maps/?zone=Verteron&type=sealed_dungeon');
   for(const width of [320,390]){
    await page.close();page=await browser.newPage({viewport:{width,height:844},isMobile:true,hasTouch:true,reducedMotion:'reduce'});
    await page.route('https://**',r=>r.abort());page.on('pageerror',e=>errors.push(e.message));
    await page.goto(base+'/'+lang+'maps/?zone=Verteron&type=sealed_dungeon');
    const pin=page.locator('.world-pin[aria-pressed="true"]');await pin.tap();
    assert.ok((await matrix(page)).scale>=2,'touch tap selects and centres a location');
    await page.locator('[data-map-viewport]').scrollIntoViewIfNeeded();await frame(page);
    const viewport=page.locator('[data-map-viewport]'),box=await viewport.boundingBox(),cdp=await page.context().newCDPSession(page);
    const point=(id,x,y)=>({id,x:box.x+x,y:box.y+y});
    const touches=d=>[point(1,box.width/2-d,130),point(2,box.width/2+d,130)];
    const pinBox=await pin.boundingBox(),pinStartScale=(await matrix(page)).scale;
    const onPin=d=>[{id:8,x:pinBox.x+pinBox.width/2-d,y:pinBox.y+pinBox.height/2},{id:9,x:pinBox.x+pinBox.width/2+50+d,y:pinBox.y+pinBox.height/2}];
    await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:onPin(0)});
    await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:onPin(25)});await frame(page);
    assert.ok((await matrix(page)).scale>pinStartScale*1.9,'pinch can start over a marker despite implicit capture transfer');
    await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await frame(page);
    await page.locator('[data-world-fit]').click();await viewport.scrollIntoViewIfNeeded();await frame(page);
    const initial=await matrix(page),selection=new URL(page.url()).searchParams.get('point');
    await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:touches(25)});
    await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:touches(60)});await frame(page);
    const enlarged=await matrix(page);assert.ok(enlarged.scale>initial.scale*2,'two-finger spread zooms terrain');
    // Pinch midpoint stays at the same world position, including an off-centre Y anchor.
    const anchor={x:box.width/2,y:130};
    for(const k of ['x','y'])assert.ok(Math.abs((anchor[k]-initial[k])/initial.scale-(anchor[k]-enlarged[k])/enlarged.scale)<.01,'pinch anchor stable');
    await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:touches(35)});await frame(page);
    assert.ok((await matrix(page)).scale<enlarged.scale,'two-finger close zooms out');
    await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await frame(page);
    assert.equal(new URL(page.url()).searchParams.get('point'),selection,'gesture never selects another marker');
    // A new single-finger gesture after pinching must pan, and may be cancelled.
    const start=await matrix(page);
    await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[point(1,30,40)]});
    await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[point(1,60,60)]});await frame(page);
    await cdp.send('Input.dispatchTouchEvent',{type:'touchCancel',touchPoints:[]});await frame(page);
    assert.ok(Math.abs((await matrix(page)).x-start.x-30)<.1);
    const beforeZoom=(await matrix(page)).scale;await page.locator('[data-world-zoom="in"]').click();assert.ok((await matrix(page)).scale>beforeZoom);
    await page.locator('[data-world-zoom="out"]').click();assert.ok(Math.abs((await matrix(page)).scale-beforeZoom)<.0001);
    await page.locator('[data-world-fit]').click();await viewport.scrollIntoViewIfNeeded();await frame(page);
    await page.locator('.map-place').first().click();await viewport.scrollIntoViewIfNeeded();await frame(page);
    await page.setViewportSize({width:width===320?390:320,height:844});await frame(page);await frame(page);
    const centered=await pin.evaluate(b=>{const r=b.getBoundingClientRect(),v=document.querySelector('[data-map-viewport]').getBoundingClientRect();return [r.x+r.width/2-v.x-v.width/2,r.y+r.height/2-v.y-v.height/2];});
    centered.forEach(v=>assert.ok(Math.abs(v)<.1,'viewport resize preserves selected location centre'));
    await page.setViewportSize({width,height:844});await frame(page);await viewport.scrollIntoViewIfNeeded();await page.screenshot({path:path.join(artifacts,`map-spatial-${lang?'ko':'en'}-${width}.png`)});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
    await cdp.detach();
   }
   assert.deepEqual(errors,[]);await page.close();
  }
  console.log(`PASS: ${audit.samples.length} independent source-coordinate samples in both languages; touch pinch/anchor, pinch followed by pan, cancellation, selection, buttons, 320/390px containment and persisted checks across reload/language change.`);
 }finally{if(browser)await browser.close();server.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
