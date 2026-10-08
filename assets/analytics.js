/* Basic consent mode: no Google request before an affirmative analytics choice. */
(() => {
  'use strict';
  const configNode = document.getElementById('pc-analytics-config');
  if (!configNode) return;
  const config = JSON.parse(configNode.textContent);
  const id = config.measurementId;
  if (!/^G-[A-Z0-9]{6,20}$/.test(id) || location.origin !== config.origin || !location.pathname.startsWith(config.base)) return;
  const key = 'players-codex-analytics-consent-v1';
  const lifetime = 180 * 24 * 60 * 60 * 1000;
  const banner = document.querySelector('[data-analytics-banner]');
  const status = document.querySelector('[data-analytics-status]');
  const ko = document.documentElement.lang === 'ko';
  const text = (en, kr) => ko ? kr : en;
  let choice = null, loaded = false, active = false;
  try {
    const saved = JSON.parse(localStorage.getItem(key));
    if (saved && ['granted', 'denied'].includes(saved.value) && saved.time <= Date.now() && Date.now() - saved.time < lifetime) choice = saved.value;
  } catch { /* A blocked store must not grant consent. */ }
  const cleanUrl = value => {
    try { const url = new URL(value); return ['https:', 'http:'].includes(url.protocol) ? url.origin + url.pathname : ''; }
    catch { return ''; }
  };
  const defaults = {analytics_storage:'denied', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'};
  function start() {
    if (loaded || navigator.globalPrivacyControl === true) return;
    loaded = active = true;
    window['ga-disable-' + id] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', defaults);
    window.gtag('consent', 'update', {...defaults, analytics_storage:'granted'});
    window.gtag('js', new Date());
    window.gtag('config', id, {
      send_page_view:true,
      page_location:cleanUrl(location.href),
      page_referrer:cleanUrl(document.referrer),
      cookie_domain:'none', cookie_path:config.base, cookie_prefix:'pcx', cookie_expires:15552000,
      allow_google_signals:false, allow_ad_personalization_signals:false,
      content_group:'players_codex_aion2', language:document.documentElement.lang
    });
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
    document.head.append(script);
  }
  function clearCookies() {
    for (const cookie of document.cookie.split(';')) {
      const name = cookie.trim().split('=')[0];
      if (name.startsWith('pcx_')) document.cookie = name + '=; Max-Age=0; Path=' + config.base + '; SameSite=Lax; Secure';
    }
  }
  function apply(value, save = true) {
    choice = value;
    if (navigator.globalPrivacyControl === true) choice = 'denied';
    if (save) { try { localStorage.setItem(key, JSON.stringify({value:choice,time:Date.now()})); } catch { /* Visit-only choice. */ } }
    if (choice === 'granted') {
      if (!loaded) start();
      else if (!active) {
        window['ga-disable-' + id] = false;
        active = true;
        window.gtag('consent', 'update', {...defaults, analytics_storage:'granted'});
      }
    } else {
      active = false;
      window['ga-disable-' + id] = true;
      if (loaded) window.gtag('consent', 'update', defaults);
      clearCookies();
    }
    banner.hidden = true;
    status.textContent = choice === 'granted' ? text('Analytics allowed.', '방문 통계 허용됨.') : text('Analytics off.', '방문 통계 꺼짐.');
  }
  document.querySelector('[data-analytics-settings]').addEventListener('click', () => {
    banner.hidden = false;
    document.querySelector('[data-analytics-decline]').focus();
  });
  document.querySelector('[data-analytics-accept]').addEventListener('click', () => apply('granted'));
  document.querySelector('[data-analytics-decline]').addEventListener('click', () => apply('denied'));
  if (navigator.globalPrivacyControl === true) apply('denied', false);
  else if (choice) apply(choice, false);
  else banner.hidden = false;
  // Collect only fixed public action categories and clean link paths, never form values.
  document.addEventListener('click', event => {
    if (!active || navigator.globalPrivacyControl === true) return;
    const target = event.target.closest('a[href], [data-skill], [data-map-complete], [data-world-zoom], [data-library-class]');
    if (!target) return;
    const params = {send_to:id, page_location:cleanUrl(location.href), content_group:'players_codex_aion2'};
    if (target.matches('a[href]')) {
      const url = new URL(target.href, location.href);
      if (!['http:', 'https:'].includes(url.protocol)) return;
      params.link_domain = url.hostname;
      if (url.origin === location.origin && url.pathname.startsWith(config.base)) params.link_path = url.pathname;
      params.action_type = url.origin === location.origin ? 'navigation' : 'external_link';
    } else {
      params.action_type = target.hasAttribute('data-skill') ? 'skill_open' : target.hasAttribute('data-library-class') ? 'class_filter' : 'map_use';
    }
    window.gtag('event', 'guide_interaction', params);
  });
})();
