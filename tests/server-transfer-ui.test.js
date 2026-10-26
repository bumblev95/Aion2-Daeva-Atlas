'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const http=require('node:http');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'../docs'),prefix='/Aion2-Daeva-Atlas/';
const artifacts=process.env.TRANSFER_QA_ARTIFACTS||path.resolve(__dirname,'../../transfer-qa-artifacts');
fs.mkdirSync(artifacts,{recursive:true});
const server=http.createServer((req,res)=>{
  const u=new URL(req.url,'http://local');
  if(!u.pathname.startsWith(prefix)){res.writeHead(404).end();return;}
  let relative=decodeURIComponent(u.pathname.slice(prefix.length));
  if(!relative||relative.endsWith('/'))relative+='index.html';
  const file=path.resolve(root,relative);
  if(!file.startsWith(root+path.sep)||!fs.existsSync(file)){res.writeHead(404).end();return;}
  res.writeHead(200,{'Content-Type':({'.html':'text/html','.css':'text/css','.js':'text/javascript','.json':'application/json','.svg':'image/svg+xml','.webp':'image/webp'})[path.extname(file)]||'application/octet-stream'});
  fs.createReadStream(file).pipe(res);
});
(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const base='http://127.0.0.1:'+server.address().port+prefix;
  let browser;
  try{
    browser=await chromium.launch({headless:true});
    for(const lang of ['en','ko'])for(const scripts of [true,false]){
      console.log('Transfer:',lang,scripts?'JS':'no-JS');
      const context=await browser.newContext({viewport:{width:390,height:844},javaScriptEnabled:scripts,reducedMotion:'reduce'});
      await context.route('https://**/*',route=>route.abort());
      const page=await context.newPage(),errors=[];
      page.on('pageerror',error=>errors.push(error.message));
      const local=base+(lang==='ko'?'ko/':'');
      await page.goto(local);
      await page.locator('[data-growth-guide="server-transfer"]').click();
      await page.waitForURL('**/guides/server-transfer/');
      assert((await page.locator('.transfer-badge').innerText()).includes(lang==='ko'?'중단':'on hold'));
      await page.locator('.transfer-checklist input').first().check();
      assert.equal(await page.locator('.transfer-checklist input').first().isChecked(),true);
      await page.reload();
      assert.equal(await page.locator('.transfer-checklist input').first().isChecked(),false);
      for(const width of [320,390,768,1440]){
        await page.setViewportSize({width,height:844});
        await page.locator('.transfer-section').evaluateAll(nodes=>nodes.forEach(n=>n.open=true));
        const box=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
        assert(box.scroll<=box.width+1,lang+'/'+scripts+'/'+width+' overflow '+JSON.stringify(box));
      }
      await page.setViewportSize({width:390,height:844});
      await page.locator('.transfer-section').evaluateAll(nodes=>nodes.forEach(n=>n.open=n.id==='checklist'));
      await page.evaluate(()=>{document.activeElement.blur();window.scrollTo(0,0);});
      await page.screenshot({path:path.join(artifacts,'transfer-'+lang+'-'+scripts+'-viewport.png')});
      await page.screenshot({path:path.join(artifacts,'transfer-'+lang+'-'+scripts+'-phone.png'),fullPage:true});
      await page.locator('#storage>summary').click();
      assert.equal(await page.locator('#storage').getAttribute('open'),'');
      await page.locator('#storage').screenshot({path:path.join(artifacts,'transfer-storage-'+lang+'-'+scripts+'.png')});
      // Cross-page fragments must reveal native details and survive language switch.
      await page.goto(local+'guides/pet-growth/');
      await page.locator('.transfer-gateway a').click();
      await page.waitForURL('**/guides/server-transfer/#pets');
      if(!scripts && !(await page.locator('#pets').evaluate(n=>n.open))) await page.locator('#pets>summary').click();
      assert.equal(await page.locator('#pets h3').first().isVisible(),true);
      await page.locator('.navtools .lang').click();
      await page.waitForURL('**/guides/server-transfer/*');
      assert.equal(new URL(page.url()).pathname.includes('/ko/'),lang!=='ko');
      if(scripts){
        assert.equal(new URL(page.url()).hash,'#pets');
        await page.goto(local+'search/?q='+encodeURIComponent(lang==='ko'?'서버 이전':'server transfer'));
        const result=page.locator('[data-search-results] a[href$="guides/server-transfer/#checklist"]');
        await result.click();
        await page.waitForURL('**/server-transfer/#checklist');
      }
      assert.deepEqual(errors,[]);
      await context.close();
    }
    console.log('PASS: bilingual discovery/search, checked-state reset, language/deep links, native disclosure and 320–1440px containment.');
  }finally{if(browser)await browser.close();server.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
