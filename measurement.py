"""Optional GA4 integration and durable Search Console verification assets."""
import html
import json
import re
from urllib.parse import urlsplit


def validate(config):
    analytics = config.get('analytics', {})
    measurement_id = analytics.get('measurement_id', '')
    if measurement_id and not re.fullmatch(r'G-[A-Z0-9]{6,20}', measurement_id):
        raise ValueError('Use the real GA4 web stream measurement ID (G-...).')
    if analytics.get('enabled') and not measurement_id:
        raise ValueError('Create the PLAYER’S CODEX GA4 web stream before enabling analytics.')
    verification = config.get('search_console', {}).get('verification_file', '')
    if verification and not re.fullmatch(r'google[a-f0-9]{16}\.html', verification):
        raise ValueError('Use the exact Google HTML verification filename.')


def head(config, base):
    if not config.get('analytics', {}).get('enabled'):
        return ''
    payload = json.dumps({
        'measurementId': config['analytics']['measurement_id'],
        'base': base,
        'origin': '{0.scheme}://{0.netloc}'.format(urlsplit(config['url'])),
    }).replace('<', '\\u003c')
    return (f'<script type="application/json" id="pc-analytics-config">{payload}</script>'
            f'<link rel="stylesheet" href="{base}assets/analytics.css?v=1">'
            f'<script defer src="{base}assets/analytics.js?v=1"></script>')


def controls(config, language, base):
    if not config.get('analytics', {}).get('enabled'):
        return ''
    ko = language == 'ko'
    label = '방문 통계 설정' if ko else 'Analytics preferences'
    title = '공략을 더 유용하게 만드는 데 도움을 주세요' if ko else 'Help improve these guides'
    copy = ('허용하면 Google Analytics가 방문 페이지와 도구 이용을 측정합니다. 플래너 내용과 검색어는 보내지 않습니다. 거절해도 모든 기능을 이용할 수 있습니다.' if ko else
            'If you allow analytics, Google Analytics measures page visits and tool use. We do not send planner text or search terms. All features work if you decline.')
    privacy = ('ko/' if ko else '') + 'privacy/'
    return f'''<div class="pc-analytics-preferences"><button type="button" class="btn" data-analytics-settings>{label}</button><span role="status" data-analytics-status></span></div>
<section class="pc-consent" data-analytics-banner hidden aria-labelledby="pc-consent-title"><h2 id="pc-consent-title">{title}</h2><p>{copy} <a href="{html.escape(base + privacy)}">{'개인정보 안내' if ko else 'Privacy notice'}</a></p><div><button type="button" class="btn" data-analytics-decline>{'거절' if ko else 'Decline'}</button><button type="button" class="btn" data-analytics-accept>{'분석 허용' if ko else 'Allow analytics'}</button></div></section>'''


def write_verification(config, out):
    filename = config.get('search_console', {}).get('verification_file')
    if filename:
        # Account-specific public verification file already used at the parent host.
        # The Search Console account must still confirm the URL-prefix property.
        (out / filename).write_text('google-site-verification: ' + filename)
