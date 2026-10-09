/* Browser regression for authoritative backend results, including no-JS use. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {chromium} = require('playwright');
const root = path.resolve(__dirname,'../docs');
const results = JSON.parse(fs.readFileSync(path.join(root,'data/dps-rankings.json'),'utf8'));
const expectedCSV = fs.readFileSync(path.join(root,'data/dps-rankings.csv'),'utf8');
const prefix = '/Aion2-Daeva-Atlas/';
const artifacts = process.env.DPS_QA_ARTIFACTS || path.resolve(__dirname,'../../dps-qa-artifacts');
fs.mkdirSync(artifacts,{recursive:true});
const server=http.createServer((req,res)=>{
  const route=decodeURIComponent(new URL(req.url,'http://local').pathname);
  if(!route.startsWith(prefix)){res.writeHead(404).end();return;}
  let relative=route.slice(prefix.length);if(!relative||relative.endsWith('/'))relative+='index.html';
  const file=path.resolve(root,relative);
  if(!file.startsWith(root+path.sep)||!fs.existsSync(file)){res.writeHead(404).end();return;}
  const type={'.html':'text/html','.js':'text/javascript','.json':'application/json','.csv':'text/csv',
    '.css':'text/css','.svg':'image/svg+xml','.webp':'image/webp'}[path.extname(file)]||'application/octet-stream';
  res.writeHead(200,{'Content-Type':type});fs.createReadStream(file).pipe(res);
});

(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const base='http://127.0.0.1:'+server.address().port+prefix;
  const browser=await chromium.launch({headless:true});
  try{
    for(const lang of ['en','ko'])for(const javascript of [true,false]){
      const context=await browser.newContext({viewport:{width:1440,height:1000},javaScriptEnabled:javascript,acceptDownloads:true});
      await context.route('https://**/*',route=>route.abort());
      const page=await context.newPage(),errors=[],engineRequests=[];
      page.on('pageerror',error=>errors.push(error.message));
      page.on('request',request=>{if(/\/assets\/dps(?:-engine)?\.js/.test(request.url()))engineRequests.push(request.url());});
      if(javascript)await context.addInitScript(()=>localStorage.setItem('players-codex-dps-v1',JSON.stringify([
        {input:{name:'Injected visitor build',attack:99999999,skills:[{flat:99999999}]}}
      ])));
      await page.goto(base+(lang==='ko'?'ko/':'')+'tools/dps/?attack=999999999&class=assassin');
      const desk=page.locator('[data-dps-rankings]');
      assert.equal(await desk.getAttribute('data-computed-by'),'backend');
      assert.equal(await desk.locator('form,input,select,textarea').count(),0);
      assert.equal(await desk.locator('[data-class-detail]').count(),8);
      assert(!(await desk.textContent()).includes('Injected visitor build'));

      const checkRows=async(locator,expected)=>{
        const rows=await locator.evaluateAll(rows=>rows.map(row=>({id:row.dataset.rankClass,
          dps:Number(row.dataset.dps),place:Number(row.cells[0].textContent),value:row.cells[2].querySelector('strong').textContent,
          name:row.cells[1].querySelector('a').textContent.trim()})));
        assert.equal(rows.length,8);
        rows.forEach((row,i)=>{
          assert.equal(row.id,expected[i].classId);assert.equal(row.place,expected[i].rank);
          assert(Math.abs(row.dps-expected[i].dps)<1e-6);
          assert.equal(row.value,expected[i].dps.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}));
          assert.equal(row.name,expected[i][lang]);
        });
      };
      await checkRows(desk.locator('.rank-overall [data-rank-class]'),results.overall);
      for(const scenario of results.scenarios){
        const panel=desk.locator('[data-rank-scenario="'+scenario.id+'"]');
        await panel.locator('summary').click();
        assert.equal(await panel.getAttribute('open'),'');
        await checkRows(panel.locator('[data-rank-class]'),scenario.rows);
      }
      const cleric=desk.locator('[data-class-detail="cleric"]');
      await cleric.locator('summary').click();
      assert.equal(await cleric.locator('.rank-breakdown tbody tr').count(),results.classes.find(c=>c.classId==='cleric').policy.order.length);
      assert((await cleric.textContent()).includes(lang==='ko'?'미확인 피해':'Unresolved damage'));
      const json=await page.request.get(base+'data/dps-rankings.json');
      assert.deepEqual(await json.json(),results);

      const downloadPromise=page.waitForEvent('download');
      await desk.locator('a[download]').click();
      const download=await downloadPromise;
      const csvPath=path.join(artifacts,'results-'+lang+'-'+(javascript?'js':'nojs')+'.csv');
      await download.saveAs(csvPath);assert.equal(fs.readFileSync(csvPath,'utf8'),expectedCSV);

      for(const width of [390,320]){
        await page.setViewportSize({width,height:844});
        const sizes=await page.evaluate(()=>({viewport:innerWidth,page:document.documentElement.scrollWidth,
          table:document.querySelector('.rank-overall .rank-table-scroll').scrollWidth,
          container:document.querySelector('.rank-overall .rank-table-scroll').clientWidth}));
        assert(sizes.page<=sizes.viewport+1,JSON.stringify(sizes));assert(sizes.table>sizes.container);
      }
      await page.setViewportSize({width:390,height:844});
      await page.screenshot({path:path.join(artifacts,'rankings-mobile-'+lang+'-'+(javascript?'js':'nojs')+'.png'),fullPage:true});
      await page.setViewportSize({width:1440,height:1000});
      await page.screenshot({path:path.join(artifacts,'rankings-desktop-'+lang+'-'+(javascript?'js':'nojs')+'.png'),fullPage:true});
      assert.deepEqual(engineRequests,[],'The page must never fetch a client DPS engine');
      assert.deepEqual(errors,[]);await context.close();
    }
    console.log('PASS: backend ranks match JSON/CSV, visitor/query inputs ignored, no client simulation, bilingual native details, no-JS access and 320/390px containment.');
  }finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
