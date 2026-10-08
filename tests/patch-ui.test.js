/* Exercise the published HTML and real refresh script, including phone layout. */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const http=require('node:http');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'../docs'),prefix='/Aion2-Daeva-Atlas/';
const feed=require('../docs/data/news.json');
const artifacts=process.env.PATCH_QA_ARTIFACTS||path.resolve(__dirname,'../../patch-qa-artifacts');
fs.mkdirSync(artifacts,{recursive:true});
const server=http.createServer((req,res)=>{
  let relative=decodeURIComponent(new URL(req.url,'http://local').pathname);
  if(!relative.startsWith(prefix)){res.writeHead(404).end();return;}
  relative=relative.slice(prefix.length);if(relative.endsWith('/')||!relative)relative+='index.html';
  const file=path.resolve(root,relative);
  if(!file.startsWith(root+path.sep)||!fs.existsSync(file)){res.writeHead(404).end();return;}
  const type={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.webp':'image/webp'}[path.extname(file)]||'application/octet-stream';
  res.writeHead(200,{'Content-Type':type});fs.createReadStream(file).pipe(res);
});

(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const base='http://127.0.0.1:'+server.address().port+prefix;
  const browser=await chromium.launch({headless:true});
  try{
    for(const lang of ['en','ko']){
      const local=base+(lang==='ko'?'ko/':''),context=await browser.newContext({viewport:{width:1440,height:1000}});
      await context.route('https://**/*',route=>route.abort());
      const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
      await page.goto(local+'updates/');
      assert.equal(await page.locator('[data-news-kind]').inputValue(),'patch');
      assert.equal(await page.locator('.patch-skill-change,.patch-fact-table').count(),0);
      await page.locator('[data-news-region]').selectOption('KR');
      await page.locator('[data-news-class]').selectOption('templar');
      const card=page.locator('.patch-summary').filter({has:page.locator('a[href*="kr-6a9727b8fa34c1011d627551/"]')});
      assert.equal(await card.isVisible(),true);
      await page.locator('[data-news-refresh]').click();
      await page.waitForFunction(()=>document.querySelector('[data-source-health]').textContent.includes('Last success:')||document.querySelector('[data-source-health]').textContent.includes('마지막 정상 확인:'));
      assert.equal(await page.locator('[data-news-region]').inputValue(),'KR');
      assert.equal(await page.locator('[data-news-class]').inputValue(),'templar');
      for(const width of [320,390]){
        await page.setViewportSize({width,height:844});
        const sizes=await page.evaluate(()=>({viewport:innerWidth,page:document.documentElement.scrollWidth}));
        assert.ok(sizes.page<=sizes.viewport+1,JSON.stringify({lang,...sizes}));
      }
      await card.locator('a[href$="#class-templar"]').click();
      await page.waitForURL('**/kr-6a9727b8fa34c1011d627551/#class-templar');
      const ready=await page.locator('[data-news-detail]').count();
      if(ready){
        assert.equal(await page.locator('#class-templar>header .change-badge.adjustment').count(),1);
        assert.ok(await page.locator('#class-templar .change-badge.buff').count()>0);
        assert.equal(await page.locator('#class-templar .change-badge.nerf').count(),2);
        await page.waitForFunction(()=>document.querySelector('#class-templar .patch-portrait').naturalWidth>0);
        for(const width of [320,390,768,1440]){
          await page.setViewportSize({width,height:844});
          const sizes=await page.evaluate(()=>({viewport:innerWidth,page:document.documentElement.scrollWidth}));
          assert.ok(sizes.page<=sizes.viewport+1,JSON.stringify({lang,...sizes}));
        }
        await page.setViewportSize({width:390,height:844});
        await page.screenshot({path:path.join(artifacts,'patch-class-mobile-'+lang+'.png')});
      }else assert.ok(await page.locator('.patch-review-notice').isVisible());
      await page.locator('.patch-bottom-nav .btn,.patch-breadcrumb a').first().click();
      await page.waitForURL('**/updates/?region=KR&kind=patch');
      assert.equal(await page.locator('[data-news-region]').inputValue(),'KR');
      await page.locator('.patch-title-link[href*="kr-6aa062386b722c561dc6a46c/"]').click();
      await page.waitForURL('**/kr-6aa062386b722c561dc6a46c/');
      if(await page.locator('[data-news-detail]').count()){
        assert.ok(await page.locator('.patch-fact-table tbody tr').count()>100);
        for(const width of [320,390]){
          await page.setViewportSize({width,height:844});
          const sizes=await page.evaluate(()=>({viewport:innerWidth,page:document.documentElement.scrollWidth,
            table:document.querySelector('.patch-fact-table').scrollWidth,container:document.querySelector('.patch-fact-table').clientWidth}));
          assert.ok(sizes.page<=sizes.viewport+1,JSON.stringify({lang,...sizes}));
          assert.ok(sizes.table>sizes.container);
        }
      }
      // A changed official source must remove stale class claims while the page is open.
      const revised=JSON.parse(JSON.stringify(feed));
      for(const source of revised.sources)for(const item of source.items)if(item.id==='6a9727b8fa34c1011d627551'){item.contentHash='changed';item.reviewState='revised';}
      await context.route('**/data/news.json?*',route=>route.fulfill({json:revised}));
      await page.goto(local+'updates/kr-6a9727b8fa34c1011d627551/');
      if(await page.locator('[data-news-detail]').count()){
        await page.locator('[data-detail-content]').waitFor({state:'hidden'});
        assert.ok(await page.locator('[data-detail-revision]').isVisible());
        assert.equal(await page.locator('.patch-detail-head>p').isVisible(),false);
      }
      assert.deepEqual(errors,[]);await context.close();
    }
    console.log('PASS: bilingual summary → class detail → list, refresh/filter continuity, official portraits, complete tables, 320/390/768px layout and stale-source removal.');
  }finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
