// Verify the privacy boundary without sending real analytics or loading Google.
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const source = fs.readFileSync('assets/analytics.js', 'utf8');
function visit(choice, options = {}) {
  const elements = new Map(), scripts = [], handlers = {}, stored = new Map();
  if (choice) stored.set('players-codex-analytics-consent-v1', JSON.stringify({value:choice,time:Date.now()}));
  for (const name of ['banner', 'status', 'settings', 'accept', 'decline']) elements.set('[data-analytics-' + name + ']', {hidden:true,textContent:'',addEventListener(type, fn){this[type]=fn;},focus(){}});
  const config = {measurementId:'G-ABC1234567',base:'/Aion2-Daeva-Atlas/',origin:'https://bumblev95.github.io'};
  const document = {
    documentElement:{lang:'en'}, referrer:'https://example.org/article?private=value#private', cookie:'',
    getElementById:() => ({textContent:JSON.stringify(config)}), querySelector:s=>elements.get(s),
    createElement:()=>({}),head:{append:s=>scripts.push(s)},addEventListener:(type,fn)=>handlers[type]=fn
  };
  const context = {document,window:{},navigator:{globalPrivacyControl:options.gpc || false},URL,Date,encodeURIComponent,
    location:{origin:config.origin,pathname:config.base+'ko/',href:config.origin+config.base+'ko/?q=private#private'},
    localStorage:{getItem:k=>{if(options.blocked) throw Error('blocked');return stored.get(k)||null;},setItem:(k,v)=>{if(options.blocked) throw Error('blocked');stored.set(k,v);}}
  };
  vm.runInNewContext(source, context);
  return {context, scripts, elements, handlers};
}
let run=visit(null);
assert.equal(run.scripts.length,0,'No consent must make no Google request');
assert.equal(run.elements.get('[data-analytics-banner]').hidden,false);
run.elements.get('[data-analytics-decline]').click();
assert.equal(run.scripts.length,0,'Declining must make no Google request');
run=visit('denied');
assert.equal(run.scripts.length,0,'Persisted refusal must make no Google request');
run=visit('granted');
assert.equal(run.scripts.length,1);
const commands=run.context.window.dataLayer.map(args=>Array.from(args));
const config=commands.find(c=>c[0]==='config')[2];
assert.equal(config.page_location,'https://bumblev95.github.io/Aion2-Daeva-Atlas/ko/');
assert.equal(config.page_referrer,'https://example.org/article');
assert.equal(config.cookie_path,'/Aion2-Daeva-Atlas/');
assert.equal(config.allow_google_signals,false);
run.elements.get('[data-analytics-accept]').click();
assert.equal(run.scripts.length,1,'Repeated acceptance must not double-install');
run.elements.get('[data-analytics-decline]').click();
assert.equal(run.context.window['ga-disable-G-ABC1234567'],true,'Withdrawal must disable collection');
const count=run.context.window.dataLayer.length;
run.handlers.click({target:{closest:()=>{throw Error('Refused clicks must not be inspected');}}});
assert.equal(run.context.window.dataLayer.length,count);
assert.equal(visit('granted',{gpc:true}).scripts.length,0,'GPC must override previous consent');
assert.equal(visit(null,{blocked:true}).scripts.length,0,'Storage errors must not imply consent');
console.log('PASS: no-consent, refusal, opt-in, withdrawal, URL redaction, single install, GPC and unavailable storage.');
