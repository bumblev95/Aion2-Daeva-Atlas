/* Browser regression for the real generated bilingual calculator. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {chromium} = require('playwright');
const root = path.resolve(__dirname,'../docs');
const db = require('../docs/data/dps.json');
const prefix = '/Aion2-Daeva-Atlas/';
const artifacts = process.env.DPS_QA_ARTIFACTS || path.resolve(__dirname,'../../dps-qa-artifacts');
fs.mkdirSync(artifacts,{recursive:true});
const server = http.createServer((req,res)=>{
  let relative = decodeURIComponent(new URL(req.url,'http://local').pathname);
  if(!relative.startsWith(prefix)){res.writeHead(404).end();return;}
  relative = relative.slice(prefix.length);if(relative.endsWith('/')||!relative)relative+='index.html';
  const file = path.resolve(root,relative);
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
      const context=await browser.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});
      await context.route('https://**/*',route=>route.abort());
      const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
      await page.goto(base+(lang==='ko'?'ko/':'')+'tools/dps/');
      await page.waitForSelector('[data-dps-results] tbody tr');
      const param=k=>page.locator('[data-param="'+k+'"]');
      const skill=id=>page.locator('[data-dps-skills] tr[data-id="'+id+'"]');
      const name=id=>db.classes.flatMap(c=>c.candidates).find(x=>x.id===id)[lang];
      const casts=async id=>page.locator('[data-dps-results] tbody tr').evaluateAll((rows,n)=>{
        const row=rows.find(r=>r.querySelector('th').textContent===n);return row?Number(row.cells[1].textContent):null;
      },name(id));
      const selectClass=async id=>{
        await page.locator('[data-dps-class]').selectOption(id);
        assert.equal(await page.locator('[data-dps-error]').isVisible(),false,id+' should calculate');
      };
      const showWindows=()=>page.locator('.condition-windows').evaluate(el=>el.open=true);
      const showResources=()=>param('resourceMode').evaluate(el=>el.closest('details').open=true);
      for(const c of db.classes)await selectClass(c.id);
      await selectClass('ranger');await param('duration').fill('30');
      assert.equal(await casts('burst-arrow'),0);
      await param('targetControl').selectOption('susceptible');assert.ok(await casts('burst-arrow')>0);
      await skill('snare-shot').locator('[data-enabled]').uncheck();assert.equal(await casts('burst-arrow'),0);
      await showWindows();await page.locator('[data-state-window="root"]').fill('0-5');assert.ok(await casts('burst-arrow')>0);
      // Save two builds in identical environments, then refuse a changed environment.
      await page.locator('[data-dps-clear]').click();await param('name').fill('Same A');await page.locator('[data-dps-compare]').click();
      await param('attack').fill('1000');await param('name').fill('Same B');await page.locator('[data-dps-compare]').click();
      assert.equal(await page.locator('.dps-ranking').count(),2);
      await param('targetControl').selectOption('immune');await param('name').fill('Different');await page.locator('[data-dps-compare]').click();
      assert.equal(await page.locator('.dps-ranking').count(),0);
      // A real Blob/download contains the condition inputs, not [object Object].
      const downloadPromise=page.waitForEvent('download');await page.locator('[data-dps-export]').click();
      const download=await downloadPromise;const csvPath=path.join(artifacts,'inputs-'+lang+'.csv');await download.saveAs(csvPath);
      const csv=fs.readFileSync(csvPath,'utf8');assert.ok(csv.includes('stateWindows'));assert.ok(csv.includes('requires_any'));assert.ok(!csv.includes('[object Object]'));
      await param('targetControl').selectOption('unknown');
      await selectClass('cleric');assert.equal(await casts('condemnation'),0);
      await page.locator('[data-state-window="chain-of-torment"]').fill('0-10');assert.ok(await casts('condemnation')>0);
      await showResources();await param('resourceMode').selectOption('budget');
      await param('mpStart').fill('100');assert.equal(await casts('condemnation'),0);
      await skill('condemnation').locator('[data-skill-param="mpCost"]').fill('200');
      await skill('chain-of-torment').locator('[data-enabled]').uncheck();assert.equal(await casts('condemnation'),0);
      await param('mpStart').fill('300');assert.equal(await casts('condemnation'),1);
      await param('resourceMode').selectOption('unverified');
      await selectClass('spiritmaster');await param('duration').fill('10');
      await page.locator('[data-dps-source-skill]').selectOption('elemental-fusion');await page.locator('[data-dps-add-source]').click();
      await skill('cold-shock').locator('[data-enabled]').uncheck();await skill('elemental-fusion').locator('[data-skill-param="flat"]').fill('100');
      assert.equal(await casts('elemental-fusion'),0);
      await param('elementEvents').fill('0,1,2,3');assert.equal(await casts('elemental-fusion'),1);
      await param('elementEvents').fill('');await param('elementsStart').fill('4');assert.equal(await casts('elemental-fusion'),1);
      await selectClass('sorcerer');await page.locator('[data-dps-clear]').click();await param('name').fill('Fire restore');
      await page.locator('[data-dps-compare]').click();assert.ok(await casts('blaze')>0);
      await param('fireMarkEnabled').selectOption('no');assert.equal(await casts('blaze'),0);
      await page.locator('[data-dps-restore="0"]').click();assert.ok(await casts('blaze')>0);
      assert.ok(await skill('blaze').locator('.skill-condition').textContent());
      // Inspect actual layout at phone widths; only table containers may scroll.
      for(const width of [390,320]){
        await page.setViewportSize({width,height:844});
        const sizes=await page.evaluate(()=>({viewport:innerWidth,page:document.documentElement.scrollWidth,
          table:document.querySelector('.dps-table-scroll').scrollWidth,container:document.querySelector('.dps-table-scroll').clientWidth}));
        assert.ok(sizes.page<=sizes.viewport+1,JSON.stringify(sizes));assert.ok(sizes.table>sizes.container);
      }
      await page.setViewportSize({width:390,height:844});await page.screenshot({path:path.join(artifacts,'mobile-'+lang+'.png'),fullPage:true});
      await page.setViewportSize({width:1440,height:1000});await page.screenshot({path:path.join(artifacts,'desktop-'+lang+'.png'),fullPage:true});
      assert.deepEqual(errors,[]);await context.close();
    }
    // Legacy saved input is loaded under current gates and cannot preserve an
    // unconditional Blaze or inherit the current page's MP/environment settings.
    const context=await browser.newContext();await context.route('https://**/*',r=>r.abort());
    const blaze=db.classes.find(c=>c.id==='sorcerer').skills.find(s=>s.id==='blaze');
    const legacy={classId:'sorcerer',region:'NA',name:'Legacy',patch:'test',duration:'10',attack:'100',crit:'0',critMultiplier:'1.5',accuracy:'100',factor:'1',downtime:'',
      sourceHash:'old',sourceDate:'2026-10-07',model:'conditional-rotation-v1',skills:[{id:'blaze',name:blaze.en,enabled:true,flat:100,coefficient:0,hits:1,cast:1,cooldown:5,afterCooldown:5,delta:0}]};
    await context.addInitScript(saved=>localStorage.setItem('players-codex-dps-v1',JSON.stringify([{input:saved}])),legacy);
    const page=await context.newPage();await page.goto(base+'tools/dps/');await page.waitForSelector('[data-dps-restore="0"]');
    await page.locator('[data-dps-restore="0"]').click();
    const count=await page.locator('[data-dps-results] tbody tr').first().locator('td').first().textContent();assert.equal(Number(count),0);
    assert.equal(await page.locator('[data-param="resourceMode"]').inputValue(),'unverified');
    assert.equal(await page.locator('.dps-ranking').count(),0);
    await context.close();
    console.log('PASS: bilingual source gates, timed states, MP/stack budgets, comparison, saved/legacy restore, actual CSV download, mobile 320/390px layout and desktop screenshots.');
  }finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
