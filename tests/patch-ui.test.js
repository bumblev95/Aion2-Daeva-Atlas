/* Exercise the published HTML and real refresh script, including phone layout. */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const http=require('node:http');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'../docs'),prefix='/Aion2-Daeva-Atlas/';
const feed=require('../docs/data/news.json');
const reviews=require('../data/patch-reviews.json');
const items=new Map(feed.sources.flatMap(s=>s.items||[]).map(item=>[item.id,item]));
const artifacts=process.env.PATCH_QA_ARTIFACTS||path.resolve(__dirname,'../../patch-qa-artifacts');
fs.mkdirSync(artifacts,{recursive:true});
const server=http.createServer((req,res)=>{
  let relative=decodeURIComponent(new URL(req.url,'http://local').pathname);
  if(!relative.startsWith(prefix)){res.writeHead(404).end();return;}
  relative=relative.slice(prefix.length);if(relative.endsWith('/')||!relative)relative+='index.html';
  const file=path.resolve(root,relative);
  if(!file.startsWith(root+path.sep)||!fs.existsSync(file)){res.writeHead(404).end();return;}
  const type={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.webp':'image/webp'}[path.extname(file)]||'application/octet-stream';
  res.writeHead(200,{'Content-Type':type});
  // Commit navigation before the real detail HTML finishes parsing. The old
  // click -> count assertion read 0 here while document.readyState was loading.
  if(/(?:^|\/)updates\/(?:na|kr)-[^/]+\/index\.html$/.test(relative)){
    const html=fs.readFileSync(file);res.write(html.subarray(0,256));
    const timer=setTimeout(()=>res.end(html.subarray(256)),250);
    res.on('close',()=>clearTimeout(timer));
  }else fs.createReadStream(file).pipe(res);
});

async function follow(page,link){
  const target=new URL(await link.getAttribute('href'),page.url()).href;
  await Promise.all([
    page.waitForURL(target,{waitUntil:'domcontentloaded'}),
    link.click(),
  ]);
  assert.equal(page.url(),target);
}

async function refresh(page){
  // A health message can already be present (especially on a second refresh).
  // Observe this request and the old card's replacement, not a reused string.
  const previous=await page.locator('[data-news-items]>.patch-summary').first().elementHandle();
  try{
    const [response]=await Promise.all([
      page.waitForResponse(r=>new URL(r.url()).pathname===prefix+'data/news.json'&&r.request().method()==='GET'),
      page.locator('[data-news-refresh]').click(),
    ]);
    assert.equal(response.status(),200);await response.finished();
    await page.waitForFunction(card=>!card.isConnected,previous);
    assert((await page.locator('[data-news-status]').textContent()).includes(feed.checkedAt));
  }finally{await previous.dispose();}
}

async function assertDetail(page,id,lang){
  const item=items.get(id);assert.ok(item,'Missing patch fixture: '+id);
  const ready=item.reviewState==='reviewed'&&['complete','highlights'].includes(item.detail?.coverage);
  if(!ready){
    assert.equal(await page.locator('[data-news-detail]').count(),0);
    assert.ok(await page.locator('.patch-review-notice').isVisible());return false;
  }
  assert.equal(item.contentHash,reviews[id].contentHash,'Feed must match its reviewed source');
  assert.deepEqual(item.changes,reviews[id].changes,'Feed must preserve the reviewed changes');
  const detail=page.locator('[data-news-detail]');await detail.waitFor({state:'visible'});
  assert.equal(await detail.getAttribute('data-item-id'),id);
  assert.equal(await detail.getAttribute('data-lang'),lang);
  assert.equal(await detail.getAttribute('data-content-hash'),item.contentHash);
  assert.ok(await page.locator('[data-detail-content]').isVisible());
  assert.equal(await page.locator('[data-detail-revision]').isVisible(),false);
  const classes=[...new Set(item.changes.map(row=>row.classId))].sort();
  assert.deepEqual(await page.locator('.patch-class-card').evaluateAll(cards=>cards.map(c=>c.id.slice(6)).sort()),classes);
  for(const cid of classes){
    const rows=item.changes.filter(row=>row.classId===cid),list=page.locator('#class-'+cid+' .patch-skill-change');
    assert.equal(await list.count(),rows.length,lang+' '+id+' '+cid);
    assert.deepEqual((await list.locator('h3').allTextContents()).map(s=>s.trim()),rows.map(row=>row.subject[lang]));
    const values=await list.locator('.patch-before-after').evaluateAll(nodes=>nodes.map(node=>
      [...node.querySelectorAll(':scope>span')].map(span=>span.lastChild.textContent)));
    assert.deepEqual(values,rows.filter(row=>row.before&&row.after).map(row=>[row.before[lang],row.after[lang]]));
    for(const type of ['buff','nerf','adjustment','fix','tooltip','system']){
      assert.equal(await list.locator('.change-badge.'+type).count(),rows.filter(row=>row.type===type).length);
    }
  }
  assert.equal(await page.locator('.patch-impact-note').count(),item.changes.filter(row=>row.impact).length);
  assert.equal(await page.locator('.patch-detail-head>a').getAttribute('href'),item.url);
  return true;
}

async function contain(page,lang,widths=[320,390,768,1440]){
  for(const width of widths){
    await page.setViewportSize({width,height:844});
    const sizes=await page.evaluate(()=>({viewport:innerWidth,page:document.documentElement.scrollWidth}));
    assert.ok(sizes.page<=sizes.viewport+1,JSON.stringify({lang,...sizes}));
  }
}

(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const base='http://127.0.0.1:'+server.address().port+prefix;
  const browser=await chromium.launch({headless:true});
  let activePage;
  try{
    for(const lang of ['en','ko']){
      const local=base+(lang==='ko'?'ko/':''),context=await browser.newContext({viewport:{width:1440,height:1000}});
      await context.route('https://**/*',route=>route.abort());
      const page=activePage=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
      // Notices have no fake review queue; current summaries survive live refresh.
      await page.goto(local+'updates/?region=NA&kind=all');
      const newPatch=page.locator('.patch-summary[data-kind="patch"]').filter({has:page.locator('a[href*="na-6acf20d007b77e214688a7ac/"]')});
      assert.equal(await newPatch.isVisible(),true);
      assert.equal(await newPatch.locator('.review-badge').textContent(),lang==='ko'?'요약 검토 완료':'Summary reviewed');
      assert.equal(await page.locator('.patch-summary[data-kind="news"]').first().locator('.review-badge').textContent(),lang==='ko'?'공식 공지':'Official notice');
      await refresh(page);
      assert.equal(await newPatch.locator('.review-badge').textContent(),lang==='ko'?'요약 검토 완료':'Summary reviewed');
      assert.equal(await page.locator('.patch-summary[data-kind="news"]').first().locator('.review-badge').textContent(),lang==='ko'?'공식 공지':'Official notice');
      await follow(page,newPatch.locator('.patch-read-link'));
      await assertDetail(page,'6acf20d007b77e214688a7ac',lang);
      assert.equal(await page.locator('#class-sorcerer .patch-skill-change').count(),3);
      assert.equal(await page.locator('#class-spiritmaster .patch-skill-change').count(),1);
      assert.equal(await page.locator('.patch-impact-note').count(),5);
      assert.equal(await page.locator('#class-brawler').count(),0);
      assert.equal(await page.locator('.change-badge.nerf').count(),0);
      await contain(page,lang);
      await page.setViewportSize({width:390,height:844});
      await page.screenshot({path:path.join(artifacts,'oct14-na-mobile-'+lang+'.png')});
      // Refresh the detail document with a class fragment, then change languages.
      await follow(page,page.locator('.patch-class-jump[href="#class-sorcerer"]'));
      await page.reload({waitUntil:'domcontentloaded'});
      assert.equal(new URL(page.url()).hash,'#class-sorcerer');
      await assertDetail(page,'6acf20d007b77e214688a7ac',lang);
      await follow(page,page.locator('.lang'));
      await assertDetail(page,'6acf20d007b77e214688a7ac',lang==='en'?'ko':'en');
      await follow(page,page.locator('.lang'));
      await assertDetail(page,'6acf20d007b77e214688a7ac',lang);
      await page.goto(local+'updates/kr-6ace86b86cfe4756db5b8d81/');
      await assertDetail(page,'6ace86b86cfe4756db5b8d81',lang);
      const followup=page.locator('.patch-followup a');
      assert.equal(await followup.count(),1);
      assert((await followup.getAttribute('href')).includes('kr-6acf3680263e537d356d1155/'));
      assert.equal(await page.locator('#class-templar>header .change-badge.adjustment').count(),1);
      assert.equal(await page.locator('#class-all .change-badge.nerf').count(),2);
      assert.equal(await page.locator('.patch-impact-note').count(),34);
      await follow(page,followup);
      await assertDetail(page,'6acf3680263e537d356d1155',lang);
      assert((await page.locator('.patch-before-after').textContent()).includes('0.1'));
      assert((await page.locator('.patch-detail-head>a').getAttribute('href')).includes('articleId=6acf3680263e537d356d1155'));
      await page.reload({waitUntil:'domcontentloaded'});
      await assertDetail(page,'6acf3680263e537d356d1155',lang);
      await contain(page,lang);
      await page.setViewportSize({width:1440,height:1000});
      await page.goto(local+'updates/');
      assert.equal(await page.locator('[data-news-kind]').inputValue(),'patch');
      assert.equal(await page.locator('.patch-skill-change,.patch-fact-table').count(),0);
      await page.locator('[data-news-region]').selectOption('KR');
      await page.locator('[data-news-class]').selectOption('templar');
      const card=page.locator('.patch-summary').filter({has:page.locator('a[href*="kr-6a9727b8fa34c1011d627551/"]')});
      assert.equal(await card.isVisible(),true);
      await refresh(page);await refresh(page);
      await page.reload({waitUntil:'domcontentloaded'});
      assert.equal(await page.locator('[data-news-region]').inputValue(),'KR');
      assert.equal(await page.locator('[data-news-class]').inputValue(),'templar');
      for(const width of [320,390]){
        await page.setViewportSize({width,height:844});
        const sizes=await page.evaluate(()=>({viewport:innerWidth,page:document.documentElement.scrollWidth}));
        assert.ok(sizes.page<=sizes.viewport+1,JSON.stringify({lang,...sizes}));
      }
      await follow(page,card.locator('a[href$="#class-templar"]'));
      const ready=await assertDetail(page,'6a9727b8fa34c1011d627551',lang);
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
        await page.reload({waitUntil:'domcontentloaded'});
        assert.equal(new URL(page.url()).hash,'#class-templar');
        await assertDetail(page,'6a9727b8fa34c1011d627551',lang);
      }
      await follow(page,page.locator('.patch-bottom-nav .btn,.patch-breadcrumb a').first());
      assert.equal(page.url(),local+'updates/?region=KR&kind=patch');
      assert.equal(await page.locator('[data-news-region]').inputValue(),'KR');
      await follow(page,page.locator('.patch-title-link[href*="kr-6aa062386b722c561dc6a46c/"]'));
      if(await assertDetail(page,'6aa062386b722c561dc6a46c',lang)){
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
      if(items.get('6a9727b8fa34c1011d627551').reviewState==='reviewed'){
        await page.locator('[data-detail-content]').waitFor({state:'hidden'});
        assert.ok(await page.locator('[data-detail-revision]').isVisible());
        assert.equal(await page.locator('.patch-detail-head>p').isVisible(),false);
      }
      assert.deepEqual(errors,[]);await context.close();activePage=null;
      // The published detail content is static and must also survive reloads
      // on phones when JavaScript is unavailable.
      const offline=await browser.newContext({javaScriptEnabled:false,viewport:{width:320,height:844}});
      await offline.route('https://**/*',route=>route.abort());
      const staticPage=activePage=await offline.newPage();
      for(const id of ['6acf20d007b77e214688a7ac','6ace86b86cfe4756db5b8d81','6acf3680263e537d356d1155']){
        const item=items.get(id);
        await staticPage.goto(local+'updates/'+item.region.toLowerCase()+'-'+id+'/');
        await assertDetail(staticPage,id,lang);
        await staticPage.reload({waitUntil:'domcontentloaded'});
        await assertDetail(staticPage,id,lang);
        await contain(staticPage,lang,[320,390]);
      }
      await offline.close();activePage=null;
    }
    console.log('PASS: EN/KO delayed HTML navigation, exact reviewed class rows, repeated live refresh, filter/hash reloads, language switches, official portraits/tables, JS/no-JS at 320/390/768/1440px and stale-source removal.');
  }catch(error){
    if(activePage&&!activePage.isClosed()){
      fs.writeFileSync(path.join(artifacts,'patch-failure.html'),await activePage.content());
      fs.writeFileSync(path.join(artifacts,'patch-failure.json'),JSON.stringify({url:activePage.url(),message:error.message,readyState:await activePage.evaluate(()=>document.readyState)},null,2));
      await activePage.screenshot({path:path.join(artifacts,'patch-failure.png'),fullPage:true});
    }
    throw error;
  }finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
