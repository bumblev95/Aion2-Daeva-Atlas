"""Optional Korean source footage; the primary lesson is the local animation."""
from html import escape as e
GUIDE_URLS={'berk':'458','bakarma':'458','auldor':'521','vakron':'521','kromede':'655','nuakum':'803'}
VIDEOS={'berk':('3OXxi7f1coQ','김호러 Horror'),'bakarma':('3OXxi7f1coQ','김호러 Horror'),'nuakum':('Hl0Ky59z8jg','만두집아들')}
POSTERS={key:'https://i.ytimg.com/vi/'+value[0]+'/hqdefault.jpg' for key,value in VIDEOS.items()}
def media(boss,m,lang):
 t=lambda a,b:b if lang=='ko' else a;v=VIDEOS.get(boss['id']);video=''
 if v:
  video=f'<a class="source-video-link" href="https://www.youtube.com/watch?v={v[0]}" target="_blank" rel="noopener noreferrer"><img src="https://i.ytimg.com/vi/{v[0]}/mqdefault.jpg" alt="" loading="lazy" width="160" height="90"><span>▶ {t("Korean creator walkthrough","한국어 공략 영상")}<small>{e(v[1])} · {t("KR footage · full dungeon guide","한국판 촬영 · 던전 전체 공략")}</small></span></a>'
 return f'<details class="source-footage"><summary>{t("Original Korean footage & screenshots","실제 한국어 영상·움짤 보기")} ↗</summary>{video}<a href="https://www.inven.co.kr/board/aion2/6444/{GUIDE_URLS[boss["id"]]}" target="_blank" rel="noopener noreferrer">Nirr · Inven · {t("KR screenshots and loops","한국어 설명·실제 장면")} ↗</a><p class="tiny muted">{t("The animation above teaches the response in your selected language. These originals show the actual KR encounter and may differ from Global.","위 애니메이션은 대응 순서를 설명해요. 원본은 한국판 실제 전투 자료로, 글로벌판과 차이가 있을 수 있어요.")}</p></details>'
