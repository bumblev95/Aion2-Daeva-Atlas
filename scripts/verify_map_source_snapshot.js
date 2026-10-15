'use strict';
// Offline replay of the independent review. Runtime/build/CI never import CBOR.
// npm install --prefix /tmp/map-review cbor-x --no-save --package-lock=false
// NODE_PATH=/tmp/map-review/node_modules node scripts/verify_map_source_snapshot.js CACHE PROVIDER_TILES_JSON
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),crypto=require('node:crypto');
const {decode}=require('cbor-x');
const [cache,providerFile]=process.argv.slice(2);
assert.ok(cache&&providerFile,'Pass downloaded source cache and tilesConfig JSON independently extracted from TH.GL.');
const root=path.resolve(__dirname,'..'),read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const maps=read(path.join(root,'data/maps.json')),review=read(path.join(root,'research/map-spatial-audit.json')),provider=read(providerFile),ctx={window:{}};
for(const file of ['map-collectibles.js','map-resources.js'])vm.runInNewContext(fs.readFileSync(path.join(root,'assets',file),'utf8'),ctx);
let count=0;
for(const [region,map]of Object.entries(maps)){
 const record=review.sourceCoordinates.find(r=>r.region===region),bytes=fs.readFileSync(path.join(cache,map.key+'.raw'));
 assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),record.sha256,'Reviewed source bytes changed; perform a new review rather than blessing a different snapshot.');
 const source=decode(bytes),byId=new Map(),byPosition=new Set();
 for(const group of source)for(const node of group.spawns){if(node.id)byId.set(node.id,node);byPosition.add(group.type+':'+JSON.stringify(node.p));}
 const all=[...map.markers];
 for(const groups of [ctx.window.CODEX_MAP_COLLECTIBLES[region]||{},ctx.window.CODEX_MAP_RESOURCES.regions[region]||{}])for(const [type,rows]of Object.entries(groups))for(const [id,p]of rows)all.push({id,p,type});
 for(const point of all){assert.ok(byPosition.has(point.type+':'+JSON.stringify(point.p)),region+':'+point.id);if(!point.type.startsWith('gather_'))assert.equal(JSON.stringify(byId.get(record.preservedStableIds[point.id]||point.id)?.p),JSON.stringify(point.p));count++;}
 assert.equal(all.length,record.checked);
 assert.deepEqual(map.transformation,provider[map.key].transformation);assert.deepEqual(map.bounds,provider[map.key].options.bounds);
 for(const sample of review.samples.filter(s=>s.region===region)){
  const [a,b,c,d]=provider[map.key].transformation,p=byId.get(sample.sourceId).p;
  assert.deepEqual(p,sample.position);assert.deepEqual([2*(a*p[1]+b),2*(c*p[0]+d)],sample.expectedLocalPixel);
 }
}
console.log(`PASS: ${count} imported coordinates match reviewed provider bytes; stable IDs, source transforms and ${review.samples.length} independent display anchors verified.`);
