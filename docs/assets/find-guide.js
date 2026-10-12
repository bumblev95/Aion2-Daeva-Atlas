/* Short topic views with native disclosure fallback and stable deep links. */
(() => {
  'use strict';
  const list=(root,selector)=>[...root.querySelectorAll(selector)];
  const getTarget=()=>{
    try {return document.getElementById(decodeURIComponent(location.hash.slice(1)));}
    catch {return null;}
  };
  function reveal(target) {
    if (!target) return;
    for (let node=target;node;node=node.parentElement) if(node.tagName==='DETAILS') node.open=true;
    list(target,':scope > details[data-reader-expand]').forEach(node=>{node.open=true;});
  }
  function languageLink() {
    const link=document.querySelector('.navtools .lang');
    if(link) {const u=new URL(link.href);u.search=location.search;u.hash=location.hash;link.href=u.href;}
  }
  const readers=list(document,'[data-topic-reader]').map(root=>{
    const tabs=list(root,'[data-reader-tab]');
    // Keep native details without scripts; use proper tabpanels when enhanced.
    const panels=list(root,'[data-reader-panel]').map(detail=>{
      const section=document.createElement('section');
      section.id=detail.id;section.className=detail.className;section.dataset.readerPanel=detail.dataset.readerPanel;
      section.setAttribute('role','tabpanel');section.setAttribute('aria-labelledby',detail.id+'-tab');
      section.append(...detail.children);detail.replaceWith(section);return section;
    });
    root.dataset.readerReady='true';
    root.querySelector('[data-reader-tabs]').setAttribute('role','tablist');
    tabs.forEach(tab=>{tab.setAttribute('role','tab');tab.setAttribute('aria-controls',panels.find(p=>p.dataset.readerPanel===tab.dataset.readerTab).id);});
    let current=panels[0].dataset.readerPanel;
    function choose(key) {
      if(!panels.some(p=>p.dataset.readerPanel===key)) return;
      current=key;
      panels.forEach(p=>{p.hidden=p.dataset.readerPanel!==key;});
      tabs.forEach(tab=>{const selected=tab.dataset.readerTab===key;tab.setAttribute('aria-selected',String(selected));tab.tabIndex=selected?0:-1;});
    }
    function activate(tab) {
      choose(tab.dataset.readerTab);
      const u=new URL(location.href);u.hash=tab.hash;
      if(u.href!==location.href)history.pushState(null,'',u);
      const target=getTarget();reveal(target);languageLink();
      requestAnimationFrame(()=>root.querySelector('[data-reader-tabs]').scrollIntoView({block:'start',behavior:'instant'}));
    }
    tabs.forEach((tab,i)=>{
      tab.addEventListener('click',event=>{if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey||event.button!==0)return;event.preventDefault();activate(tab);});
      tab.addEventListener('keydown',event=>{
        const move={ArrowRight:(i+1)%tabs.length,ArrowLeft:(i+tabs.length-1)%tabs.length,Home:0,End:tabs.length-1};
        if(event.key in move){event.preventDefault();const next=tabs[move[event.key]];next.focus();activate(next);}
        if(event.key===' '){event.preventDefault();activate(tab);}
      });
    });
    choose(current);
    return {root,choose,first:panels[0].dataset.readerPanel};
  });
  function syncHash(scroll=true) {
    const target=getTarget();
    readers.forEach(({root,choose,first})=>{
      const panel=target?.closest('[data-reader-panel]');
      if(panel&&root.contains(panel))choose(panel.dataset.readerPanel);
      else if(!location.hash)choose(first);
    });
    reveal(target);languageLink();
    if(target&&scroll)requestAnimationFrame(()=>target.scrollIntoView({block:'start',behavior:'instant'}));
  }
  window.addEventListener('hashchange',()=>syncHash());
  window.addEventListener('popstate',()=>syncHash());
  syncHash(Boolean(location.hash));
  // A same-fragment link can point to a panel that was closed since the last visit.
  document.addEventListener('click',event=>{
    const link=event.target.closest('a[href]');
    if(!link||event.defaultPrevented||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey||event.button!==0)return;
    const u=new URL(link.href);
    if(u.origin===location.origin&&u.pathname===location.pathname&&u.search===location.search&&u.hash&&u.hash===location.hash){event.preventDefault();syncHash();}
  });
  list(document,'[data-guide-directory]').forEach(root=>{
    const buttons=list(root,'[data-directory-filter]'),groups=list(root,'[data-directory-group]');
    function select(key) {
      if(!buttons.some(b=>b.dataset.directoryFilter===key))key='all';
      groups.forEach(group=>{group.hidden=key!=='all'&&group.dataset.directoryGroup!==key;});
      buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.directoryFilter===key)));
    }
    buttons.forEach(b=>b.addEventListener('click',()=>{
      const key=b.dataset.directoryFilter;select(key);
      const u=new URL(location.href);key==='all'?u.searchParams.delete('topic'):u.searchParams.set('topic',key);
      history.pushState(null,'',u);languageLink();
    }));
    window.addEventListener('popstate',()=>select(new URLSearchParams(location.search).get('topic')||'all'));
    select(new URLSearchParams(location.search).get('topic')||'all');
    root.querySelector('[data-directory-controls]').hidden=false;
  });
})();
