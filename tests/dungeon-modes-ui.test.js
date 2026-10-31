'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require('playwright');
const root=path.resolve('docs');
const server=http.createServer((req,res)=>{
 let name=new URL(req.url,'http://local').pathname.replace(/^\/Aion2-Daeva-Atlas\//,'');
 if(name.endsWith('/'))name+='index.html';
 const file=path.resolve(root,name);
 if(!file.startsWith(root+path.sep)||!fs.existsSync(file)){res.writeHead(404).end();return;}
 res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'})[path.extname(file)]||'application/octet-stream');
 fs.createReadStream(file).pipe(res);
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_EXECUTABLE?{executablePath:process.env.CHROMIUM_EXECUTABLE}:{})});
 try{
 for(const lang of ['en','ko'])for(const slug of ['urugugu-canyon','vakron-island'])for(const width of [320,390,768,1280]){
 const page=await browser.newPage({viewport:{width,height:900},reducedMotion:'reduce'}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));await page.route('https://**/*',r=>r.abort());
 await page.goto(`http://127.0.0.1:${server.address().port}/Aion2-Daeva-Atlas/${lang==='ko'?'ko/':''}dungeons/${slug}/`);
 const section=page.locator('[data-dungeon-modes]');assert.equal(await section.count(),1);
 assert.equal(await section.getAttribute('data-region'),'NA');assert.equal(await section.evaluate(n=>getComputedStyle(n).borderTopStyle),'solid');assert.equal(await section.locator('tbody tr').count(),8);
 assert.ok((await section.textContent()).includes('2,700'));
 assert.ok((await section.textContent()).includes(slug==='vakron-island'?'Ariel Fragment: Vakron':'Ariel Fragment: Urugugu'));
 await section.locator('.mode-pending summary').click();assert.ok(await section.locator('.mode-pending p').isVisible());
 assert.ok(await page.locator('.boss-lab [data-animation]').count()>0);
 const sizes=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));assert.ok(sizes.scroll<=width+1,JSON.stringify({lang,slug,...sizes}));
 const link=section.locator('a[href*="updates/na-"]');assert.equal((await page.request.get(new URL(await link.getAttribute('href'),page.url()).href)).status(),200);
 assert.deepEqual(errors,[]);
 if(width===390){await page.screenshot({path:`/tmp/${slug}-${lang}-mobile.png`,fullPage:true});}
 await page.close();
 }
 console.log('16 bilingual/dungeon/viewport combinations passed; no overflow or page errors; legacy animations and source links present.');
 }finally{await browser.close();server.close();}
})().catch(e=>{console.error(e);process.exitCode=1;server.close();});
