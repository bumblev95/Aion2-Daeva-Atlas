/* Real generated bilingual guides on mobile Chromium; no third-party requests. */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require('playwright');
const root=path.resolve('docs'),prefix='/Aion2-Daeva-Atlas/';
const artifacts=process.env.VAKRON_QA_ARTIFACTS||path.resolve('../vakron-qa');
fs.mkdirSync(artifacts,{recursive:true});
const server=http.createServer((req,res)=>{
 const url=new URL(req.url,'http://local');
 if(!url.pathname.startsWith(prefix)){res.writeHead(404).end();return;}
 let relative=decodeURIComponent(url.pathname.slice(prefix.length));if(relative.endsWith('/')||!relative)relative+='index.html';
 const file=path.resolve(root,relative);
 if(!file.startsWith(root+path.sep)||!fs.existsSync(file)){res.writeHead(404).end();return;}
 res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'})[path.extname(file)]||'application/octet-stream');
 fs.createReadStream(file).pipe(res);
});
const ids=['debuff','hands','flowers','glide','petrify','shield','elements','jumps','rock'];
async function seek(box,value){await box.locator('[data-animation-seek]').evaluate((node,value)=>{node.value=value;node.dispatchEvent(new Event('input',{bubbles:true}));},value);}
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const base='http://127.0.0.1:'+server.address().port+prefix;
 const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_EXECUTABLE?{executablePath:process.env.CHROMIUM_EXECUTABLE}:{})});
 try{
 for(const lang of ['en','ko'])for(const width of [320,390,768]){
  const context=await browser.newContext({viewport:{width,height:844},isMobile:true,hasTouch:true,reducedMotion:'reduce'});
  await context.route('https://**/*',r=>r.abort());
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  const local=base+(lang==='ko'?'ko/':'');
  await page.goto(local+'dungeons/vakron-island/');
  assert.equal(await page.locator('.vk-stage').count(),6);
  assert.equal(await page.locator('.vk-guide [data-animation]').count(),9);
  assert.equal(await page.locator('.boss-lab [data-animation]').count(),3);
  assert.equal(await page.locator('.vk-guide [data-animation][data-playing="false"]').count(),9);
  for(const id of ids){
   const lesson=page.locator('#vakron-lesson-'+id),box=lesson.locator('[data-animation]');
   await lesson.evaluate(n=>{n.closest('details').open=true;});
   for(const p of [0,330,500,700,990]){
    await seek(box,p);
    const markup=await box.locator('svg').innerHTML();
    assert.ok(!/NaN|undefined|Infinity/.test(markup),id);
    assert.ok(markup.includes('<circle')||markup.includes('<path'));
   }
   assert.equal(await lesson.locator('[data-video-verified="false"][data-timing-verified="false"][data-global-verified="false"]').count(),1);
   const original=await lesson.locator('a[href*="youtube.com"]').getAttribute('href');
   assert.ok(original.includes('jYqmiyFEdk8')&&/t=\d+s/.test(original));
   await box.locator('.battle-transcript summary').click();
   assert.equal(await box.locator('.battle-transcript li:visible').count(),3);
   const sizes=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
   assert.ok(sizes.scroll<=sizes.width+1,lang+'/'+width+'/'+id+JSON.stringify(sizes));
   const controls=await box.locator('.battle-controls button,.battle-controls select').evaluateAll(nodes=>nodes.map(n=>({w:n.getBoundingClientRect().width,h:n.getBoundingClientRect().height})));
   assert.ok(controls.every(n=>n.w>=44&&n.h>=44),JSON.stringify(controls));
  }
  const flower=page.locator('#vakron-lesson-flowers [data-animation]');await seek(flower,900);
  assert.ok(await flower.locator('[data-puddle]').count()>0);
  const rock=page.locator('#vakron-lesson-rock [data-animation]');await seek(rock,500);
  assert.equal(await rock.locator('[data-vk-rock="red"]').count(),1);await seek(rock,900);
  assert.equal(await rock.locator('[data-vk-rock="red"]').count(),0);
  const shield=page.locator('#vakron-lesson-shield [data-animation]');await seek(shield,400);
  assert.ok((await shield.locator('svg').textContent()).includes(lang==='ko'?'물리 공격 중단':'STOP PHYSICAL'));
  await seek(shield,900);assert.ok((await shield.locator('svg').textContent()).includes(lang==='ko'?'마법 공격 중단':'STOP MAGIC'));
  await seek(flower,0);await flower.locator('[data-animation-speed]').selectOption('2');
  await flower.locator('[data-animation-toggle]').click();
  await page.waitForFunction(()=>Number(document.querySelector('#vakron-lesson-flowers [data-animation-seek]').value)>0);
  await flower.locator('[data-animation-toggle]').click();
  const stopped=await flower.locator('[data-animation-seek]').inputValue();
  await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
  assert.equal(await flower.locator('[data-animation-seek]').inputValue(),stopped);
  await flower.locator('[data-animation-replay]').click();assert.equal(await flower.getAttribute('data-playing'),'true');
  await flower.locator('[data-animation-toggle]').click();
  await page.locator('.vk-route a[href="#vakron-thamon"]').tap();
  assert.equal(await page.locator('#vakron-thamon').getAttribute('open'),'');
  await page.reload();assert.equal(await page.locator('#vakron-thamon').getAttribute('open'),'');
  await page.locator('.navtools .lang').click();
  await page.waitForURL(local===base?'**/ko/dungeons/vakron-island/**':'**/Aion2-Daeva-Atlas/dungeons/vakron-island/**');
  await page.waitForFunction(()=>document.querySelector('[data-vakron-guide]')?.dataset.ready==='true');
  assert.equal(await page.locator('#vakron-thamon').getAttribute('open'),'');
  assert.equal(new URL(page.url()).hash,'#vakron-thamon');
  // Preserve the existing per-pattern bookmark and real accessible tabs.
  await page.goto(local+'dungeons/vakron-island/?mechanic=prison#mechanic-vakron-prison');
  assert.equal(await page.locator('#mechanic-vakron-prison').isVisible(),true);
  await page.locator('#pick-vakron-prison').focus();await page.keyboard.press('ArrowRight');
  assert.equal(await page.locator('#mechanic-vakron-rings').isVisible(),true);
  assert.equal(await page.locator('.boss-lab [data-scene-reference]').count(),3);
  if(width===390){
   await page.goto(local+'dungeons/vakron-island/#vakron-first');
   await page.locator('#vakron-first .vk-lesson').last().scrollIntoViewIfNeeded();
   await seek(page.locator('#vakron-lesson-flowers [data-animation]'),800);
   await page.screenshot({path:path.join(artifacts,'vakron-'+lang+'-390.png')});
  }
  await page.goto(local+'dungeons/');assert.equal(await page.locator('[data-scene-reference]').count(),16);
  const duplicate=await page.locator('[id]').evaluateAll(nodes=>nodes.map(n=>n.id).filter((id,i,ids)=>ids.indexOf(id)!==i));
  assert.deepEqual(duplicate,[]);assert.deepEqual(errors,[]);await context.close();
 }
 for(const lang of ['en','ko']){
  const context=await browser.newContext({viewport:{width:320,height:844},javaScriptEnabled:false});
  await context.route('https://**/*',r=>r.abort());const page=await context.newPage();
  await page.goto(base+(lang==='ko'?'ko/':'')+'dungeons/vakron-island/');
  for(const stage of await page.locator('.vk-stage>summary').all())if(await stage.locator('..').getAttribute('open')===null){await stage.evaluate(n=>n.scrollIntoView({block:'center',behavior:'instant'}));await stage.click();}
  assert.equal(await page.locator('.vk-lesson:visible').count(),9);
  assert.equal(await page.locator('[data-scene-reference]:visible').count(),3);
  assert.equal(await page.locator('.battle-controls:visible').count(),0);
  await context.close();
 }
 console.log('PASS: KO/EN 320/390/768 mobile layouts, 9 scenes, touch controls, reduced motion, scrub/pause/replay/speed, source flags, hash reload/language switching, legacy tabs/16 references and no-JS.');
 }finally{await browser.close();await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
