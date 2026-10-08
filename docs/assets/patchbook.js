(function (root) {
  'use strict';
  function classify(changes) {
    const types=new Set(changes.map(c=>c.type));
    if(types.has('adjustment')||(types.has('buff')&&types.has('nerf')))return 'adjustment';
    return ['buff','nerf','fix','tooltip'].find(x=>types.has(x))||'system';
  }
  function groups(item,classes) {
    const buckets={};
    (item.changes||[]).forEach(c=>{if(Object.hasOwn(classes,c.classId))(buckets[c.classId]??=[]).push(c);});
    return Object.keys(classes).filter(id=>buckets[id]).map(id=>({classId:id,info:classes[id],rows:buckets[id],type:classify(buckets[id])}));
  }
  function detailPath(item) {
    if(!['NA','KR'].includes(item.region)||! /^[a-zA-Z0-9_-]{1,64}$/.test(item.id))throw new Error('Invalid patch identity');
    return 'updates/'+item.region.toLowerCase()+'-'+item.id+'/';
  }
  const api={classify,groups,detailPath};
  if(typeof module==='object'&&module.exports)module.exports=api;
  else root.CodexPatch=api;
})(typeof globalThis!=='undefined'?globalThis:this);
