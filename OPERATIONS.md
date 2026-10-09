# PLAYER’S CODEX 운영 전략

## 2026-10-07 디자인 개편

브랜드를 여러 게임을 담을 수 있는 PLAYER’S CODEX로 변경했다. 첫 게임 허브는 AION 2다. 첫 화면은 6개 바로가기와 8개 직업 선택 버튼, PvE/PvP 전환, 전투 위치 도식으로 구성한다. 설명 글은 단계별 그림과 펼침 메뉴로 제공한다. 전투 도식은 편집상 역할 설명이며 특정 보스 공략이나 실측 거리가 아니다. 커뮤니티 스킬 빌드는 Questlog 외부 링크임을 표시한다. 기존 GitHub Pages URL은 링크 호환성을 위해 유지한다.

## 포지셔닝

영문 독자를 우선 대상으로 하는 한국 정보 해설형 아이온 2 가이드. 핵심 가치는 한국 공략의 내용을 그대로 번역하는 것이 아니라, 글로벌 버전에서 적용할 수 있는 범위와 실제 행동을 설명하는 것이다. 현재 에디션은 플레이스타일과 판단 방법을 제공하며 실측 빌드 사이트로 소개하지 않는다.

## 성장 순서

1. **첫 방문:** 구체적인 검색 질문에 답하는 완성된 글을 만든다. 직업 선택, 한국어 직업명, 글로벌과 한국 공략의 호환 조건, 첫 파티 준비가 시작점이다. 검색량이 확인됐다고 주장하지 않는다.
2. **재방문:** 비교 링크, 브라우저 저장 플래너, 용어 검색을 유지한다. 게임 데이터가 확보되면 실제 지역별 리셋·보상·스킬 자료를 확인한 후 도구를 확장한다.
3. **차별화:** 실제 플레이를 확인할 수 있는 스크린샷·실험 조건·전투 영상이 확보되면 한 직업과 한 콘텐츠부터 깊게 다룬다. 보스별 패턴, 조건을 고정한 세팅 비교, 한국 패치의 글로벌 적용 여부가 다음 우선순위다.
4. **수익화:** 사이트 품질과 사용자 경험을 확인한 후 AdSense를 연결한다. 광고는 읽기 흐름을 해치지 않는 본문 위치부터 시작하고 실제 수익·속도·재방문 영향을 본다. 광고 클릭 유도, 트래픽 구매, 대량 자동 번역을 하지 않는다.

처음부터 10개 언어, 커뮤니티 계정, 댓글 서버, 자동 티어 생성, 수백 개의 빈 빌드 페이지를 추가하지 않는다. 이는 확정된 성공 공식이 아니라 현재 자원과 차별점을 고려한 운영 가설이다.

## 다음 콘텐츠의 발행 조건

| 주제 | 발행에 필요한 근거 |
| --- | --- |
| 특정 직업 PvE 빌드 | 지역·패치·장비·스킬 설명·반복 가능한 실측 |
| 보스 패턴 공략 | 실제 보스·난도·영상/스크린샷·확인한 패턴 |
| KR → Global 변경 해설 | 양쪽 공지의 정확한 출처와 적용 날짜 |
| 강화/재료 계산기 | 공식 확률·비용·실패/보호/천장 규칙 |
| 일일·주간 활동표 | 지역별 리셋 시각과 현재 게임의 이용 제한 |

## 검색·측정

- 제목과 본문이 일치하도록 유지하고, 번역판은 `/ko/`에서 제공한다.
- 각 글은 독립된 정적 HTML, canonical, `hreflang`, Article JSON-LD를 가진다.
- sitemap: `https://bumblev95.github.io/Aion2-Daeva-Atlas/sitemap.xml`
- Search Console 프로젝트 URL-prefix 소유권 확인과 사이트맵 제출을 완료했다. 영문 홈페이지, 한국어 홈페이지, 영문 입문 가이드의 색인 요청도 접수됐다. 사이트맵 처리와 검색 색인 완료는 별도로 확인한다.
- 실제 측정 후 볼 지표: 색인된 원문 글, 검색 노출·클릭·질의, 도움이 된 도구 이용, 재방문, 페이지당 광고 수익과 페이지 속도.
- Google Analytics 4 전용 속성과 웹 스트림을 만들고 `G-S45PCCH32Y`를 배포했다. 방문자가 분석을 허용한 뒤에만 태그를 실행하며 거절·철회를 지원한다. 자동 향상된 측정은 꺼져 있다. 비교 링크의 URL 파라미터와 로컬 체크리스트는 방문 분석이 아니다.
- 광고 수익의 기본 계산은 `페이지뷰 / 1,000 × 실제 Page RPM`이다. 지금은 트래픽과 RPM 자료가 없어 수익 예측을 제공하지 않는다.

## AdSense 연결 전 실제 남은 일

1. 사이트 내용을 운영자가 읽고, 특히 플레이 경험이 필요한 부분을 검토한다. 현재 글은 AI 도움으로 작성되었으며 실측이 아니다. 개인정보 보호 안내와 연락 창구가 실제 운영 방식과 맞는지도 확인한다.
2. 장기 브랜드용 도메인을 선택한다. 구매나 DNS 변경은 이번 작업에 포함되지 않았다. GitHub 코드 저장소는 그대로 두고 호스팅은 필요에 따라 옮길 수 있다.
3. 기존 AdSense 게시자 ID `ca-pub-9723666081819297`를 확인해 적용했다. 추가 AdSense 계정은 만들지 않는다. 확인용 메타 태그와 `ads.txt`는 공개돼 있다.
4. GitHub 프로젝트 URL의 `/Aion2-Daeva-Atlas/ads.txt`나 `robots.txt`는 도메인 루트 파일이 아니다. 이 경로만으로 루트 광고 판매자 파일을 설정했다고 주장하지 않는다. 독립 도메인을 쓰면 이 사이트를 루트에 두고 `site.json.url`을 변경해 다시 빌드한다. 아이온2 검색 등록 요청에 따라 루트 robots.txt에는 아이온2 sitemap 선언만 추가한다. 기존 루트 홈페이지와 주식 통계 설정은 유지한다.
5. AdSense의 기존 `bumblev95.github.io` 사이트는 소유권 확인과 심사 요청이 접수돼 검토 중이다. 화면에 표시된 요청 시간은 2026-10-04 02:01이다. 삭제·재신청하지 않는다. 사이트 승인은 Google의 결정이며 글 수, 특정 기간, 트래픽 수가 승인을 보장하지 않는다.
6. 글로벌 광고 서비스에 맞는 Google 인증 CMP와 관련 지역의 개인정보 메시지를 설정한다. 현재 페이지에는 가짜 동의 배너가 없다. 단순히 `consent_reviewed`를 켜는 것은 CMP 설치가 아니다.
7. 실제 개인정보 안내와 필요한 선택/철회 UI를 구현한 뒤 수동 광고 단위의 슬롯 ID를 추가한다. 그때만 `enabled`와 `consent_reviewed`를 활성화한다. 현재 본문 광고 위치는 3번째 절 이후 한 곳이다. 새로운 상태를 반영해 현재 About/Privacy의 '광고 비활성' 문구도 수정한다.
8. 공개 URL에서 검증용 메타 태그와 루트 ads.txt 응답을 확인했다. 광고 활성화 시에는 동의 전후 네트워크, 실제 광고 배치, 휴대폰 화면을 추가 검증한다. 현재 광고 실행은 꺼져 있다.

## 호스팅

현재는 공개 정보성 팬 간행물을 GitHub Pages에 배포한다. GitHub는 Pages를 전자상거래·상업 거래·SaaS 중심 서비스의 무료 호스팅으로 쓰는 것을 제한한다. 유료 상품, 결제 또는 서비스를 추가할 때는 [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)를 다시 검토하고 목적에 맞는 호스팅으로 이전한다. GitHub 문서가 모든 광고 형태의 허용을 보장한다고 해석하지 않는다.

## 공식 참고

- [AdSense 사이트 연결과 심사](https://support.google.com/adsense/answer/7584263?hl=en)
- [콘텐츠·탐색 품질과 승인 문제](https://support.google.com/adsense/answer/81904?hl=en)
- [EEA·영국·스위스의 CMP 요구사항](https://support.google.com/adsense/answer/13554116?hl=en)

이 문서는 실행 계획이며 미래 유지보수 자동화를 예약한 것은 아니다.


## 2026-10-07 실제로 눌러 배우는 가이드

- `/start/`: 초반 육성 핵심 요약·편의 설정·스토리 이후를 포함한 4구간 성장 우선순위. `/endgame/#after-story`: 보상 아이템 사용·미완료 봉인 던전·깃털 반납·장신구·반복 콘텐츠를 실제 투자로 연결하는 성장 순서. 글로벌 아이템 자료와 한국 필드 공략을 구분하고 깃털 위치는 원본 인벤 공략으로 연결한다. 기존 던전/보스 공략·장비 투자·파티 준비와 실제 성장 체크리스트 저장은 유지한다.
- `/skills/`: 출시 8직업의 280개 기본 습득 스킬, 실제 아이콘, 한영 이름, 1레벨 효과, 모든 특화. 직업당 액티브 12·패시브 10·스티그마 13. 파생 연계는 부모 스킬 문서 안에 설명.
- `growth.py`: 입문용 PvE 편집 제안. 기본 포인트 10과 장비 등을 더한 합계 목표를 구분. 특화 선택은 합계 레벨과 슬롯 수를 적용. 한국 원문을 글로벌 실측 최적 세팅으로 제시하지 않는다.
- `/maps/`: TH.GL 공개 게임 타일·실제 좌표 기반 2D 지도. 4지역의 퀘스트·키벨리스크·봉인 던전 384곳. 검색·마커·확대·이동·근처 거점·완료 숨기기·위치 공유. WebGL 불필요. 직선거리 가까운 거점은 길찾기 경로가 아니다. 출처 표시는 유지.
- 보스 16개 패턴은 직접 작성한 SVG 애니메이션으로 자동 재생. 재생/일시정지·스크럽·속도·다시 보기, 화면 밖 중지, 동작 줄이기 지원. 거리·속도·인원 배치는 실제 측정치가 아니다.
- 러시아어 기본 영상은 제거. 김호러 Horror와 만두집아들의 한국어 원본, Nirr의 인벤 실제 장면을 보조 링크로 연결. 외부 표시가 제한된 인벤 이미지는 우회하지 않는다.
- `data/skills.json`: MetaBot EN/KO 스킬 DB에서 기본 효과·특화·게임 아이콘·이름을 확인. 누락된 호법성 생존 의지 아이콘만 Aion2t.com 원 게임 아이콘 사용.
- 새로운 백엔드·광고·분석·자동화를 추가하지 않았다. 저장 키는 `players-codex-lessons-v1`, `players-codex-map-v1`; 개인정보 화면의 기기 데이터 삭제에 포함.


## 2026-10-08 독자 제보 실전 팁

- 구원의노래의 인벤 글 <https://m.inven.co.kr/board/aion2/6444/2116> (표시 작성일 2026-07-20)을 읽고 후방 마커, 채팅 시간, 자동 사용, 추출 설정의 실제 캡처를 확인했다. 원문 링크를 유지하고 초보용 설명은 짧게 다시 작성했다.
- `fieldtips.py`는 한국 원문 메뉴와 출처를 표시한 외부 원본 이미지 미리보기·링크를 제공한다. 스크린샷을 저장소에 복제하지 않는다. 영어 메뉴명은 이해용 번역이며 글로벌 클라이언트의 정확한 표기를 검증했다고 주장하지 않는다. 설정 위치와 활용 맥락은 정적 공략으로 보여주며 모의 조작 버튼은 사용하지 않는다.
- 원문에서 이미지의 외부 재게시 허락은 확인되지 않았다. 원본 이미지는 다운로드·재게시하거나 img/iframe으로 삽입하지 않는다. 스크린샷 버튼은 원본 파일을 새 탭에서 여는 일반 링크다. 캡처 4개 모두 구원의노래/Inven 표기와 원문 링크를 함께 제공한다. 추가 허락 없이 작성자에게 연락하거나 요청을 발송하지 않았다.
- 추후 스크린샷을 사이트에 직접 싣는 경우 작성자 허락 또는 재사용 라이선스, 해당 원문, 적용 범위(상업적 사용·번역·표시 가공 포함)를 기록하고 출처·원본 맥락을 유지한다. 인벤 약관 15조의 게시물 권리 규정을 외부 사이트에 대한 포괄적 허락으로 해석하지 않는다.
- 자동 사용 연습의 생명력 45% 및 기준값은 설명용 수치다. 추천값·실제 물약 발동 테스트가 아니다. 추출은 선택 목록의 검토만 가르치고 게임 내 삭제를 수행하지 않는다.
- 모집글 약어는 예시 해독이며 200k를 권장 전투력으로 제시하지 않는다. 원문 수수료, 초기화 일정, 입장 컷, 신석 성능·가격은 글로벌 현재값으로 옮기지 않았다.

## 2026-10-08 Google 연결 상태

- GA4 계정 `410587266` 안에 별도 `PLAYER’S CODEX · AION 2` 속성 `558027990`, 웹 스트림 `16065115962`, 측정 ID `G-S45PCCH32Y`를 만들었다. 보고 시간대는 America/Regina, 통화는 CAD다. 기존 주식 사이트 속성은 수정하지 않았다.
- PR #9로 측정 ID를 연결했고 GitHub Pages 배포가 성공했다. 실제 한국어 페이지에서 동의 전 Google 태그 없음, 거절 시 통계 꺼짐, 허용 후 전용 태그 실행을 확인했다. 철회 후 새로고침에서도 통계 꺼짐과 Google 태그 없음을 확인했다. 동의·철회와 입력값 제외는 기존 자동 검사를 통과했다. Realtime에서 테스트 활성 사용자 1명, 페이지 조회 2건, `guide_interaction` 1건을 확인했다.
- 스트림 생성 화면에서 자동 향상된 측정을 끄려 했으나 생성 후 켜져 있는 것을 실제 수신 점검에서 발견했다. 웹 스트림 세부정보에서 '사용 안함'을 적용하고 새로고침 후에도 꺼진 설정을 확인했다. 초기 테스트의 `scroll` 이벤트는 최종 설정 이전에 실행된 태그에서 수신됐다. 정리된 페이지 URL과 정해진 기능 이용 이벤트만 전송하며 검색어·플래너 입력값·URL 파라미터·해시는 보내지 않는다.
- Search Console URL-prefix `https://bumblev95.github.io/Aion2-Daeva-Atlas/`는 기존 상위 속성 소유권으로 자동 확인됐다. HTML 확인 파일도 공개돼 있지만 이번 확인 방식은 상위 속성이다.
- 634개 URL을 담은 `sitemap.xml`을 제출했다. 공개 파일은 HTTP 200, XML 문법 정상이다. Google 검사 도구 스마트폰의 실제 테스트에서도 크롤링 허용 '예', 페이지 가져오기 '성공'을 확인하고 재제출했다. Sitemaps 보고서는 여전히 '가져올 수 없음', 발견된 페이지 0을 표시하므로 처리 성공으로 표기하지 않는다. Google의 다음 가져오기/처리 결과가 남아 있다.
- 영문 홈페이지 `/`, 한국어 홈페이지 `/ko/`, 영문 입문 가이드 `/start/`의 '색인 생성 요청됨' 화면을 확인했다. 요청 접수는 검색 색인 완료를 뜻하지 않는다.
- AdSense의 기존 `bumblev95.github.io` 사이트는 심사 중이다. 프로젝트 경로는 별도 신청 대상으로 추가하지 않았다. 루트 `https://bumblev95.github.io/ads.txt`는 요구된 게시자 행을 HTTP 200으로 제공한다. AdSense 목록의 ads.txt 상태는 아직 '찾을 수 없음'이다.
- 광고는 `enabled=false`, `consent_reviewed=false`, 슬롯 미설정으로 유지한다. 승인 후 Google 인증 CMP와 지역별 메시지, 실제 광고 단위를 설정하고 검증해야 한다. 분석 선택 UI는 광고용 CMP를 대체하지 않는다.

## Layout update · 2026-10-08

The home page leads with three player goals: growth, boss fights and equipment
enhancement. Early-game and full endgame links remain below those entries;
skill/location references and compact class links support the main guides.
Detailed class exploration, progression checklists and boss lessons
remain on their dedicated pages. Shared navigation groups beginner, character,
adventure and reference links; the mobile drawer closes with Escape or its
backdrop and keeps keyboard focus inside while open.

The beginner page progressively enhances three readable sections into tabs:
`view=basics`, `view=settings` and `view=growth`. Existing `lesson`, `step`,
`#field-tips` and `#tip-*` links remain supported. Hash targets reveal their
containing panel and tip disclosure. Browser Back/Forward restores the selected
section, and language links retain the current view. All three sections remain
in the HTML without JavaScript. Mobile lessons use a labeled native selector.
The screenshot links and all source/region caveats are retained. `gearsteps.py`
adds a static enhancement procedure and material/source table at `/gear/#upgrade`.
`tests/post-story-ui.test.js` follows all three home routes in English/Korean and
checks phone containment, material links and legacy completion storage.

Visual rules for this hierarchy live in `assets/layout.css`, loaded after the
existing component styles. Update its cache version when changing those rules.


## 2026-10-08 공식 패치 데스크와 DPS 모델

- `/updates/`와 `/ko/updates/`: 한국·북미 공식 공지 4채널을 분리 수집하고 변경 유형(버프·너프·조정·오류 수정·시스템)을 표시한다. 미국·캐나다는 북미 피드를 함께 사용한다. 공지 수집은 내용 검토와 다르다. 요약은 직접 작성하고 전체 원문은 복제하지 않는다. `data/patch-reviews.json`은 원문 내용 해시에 묶여 있으며 원문 수정 시 이전 요약을 표시하지 않는다.
- `scripts/collect_updates.py`: 인증 없는 공개 NC 게시판 API를 사용한다. 원문 본문은 해시 계산에만 사용하고 저장·재게시하지 않는다. 실패·429 시 재시도나 우회 없이 마지막 성공 항목과 날짜를 유지하고 실패 상태를 게시한다. `.github/workflows/refresh-updates.yml`은 매시간 13분에 실행되며 실제 실행은 GitHub 스케줄 지연이 있을 수 있다. 검증 후 뉴스 데이터와 해당 페이지만 일반 push로 반영하고 기존 main/docs Pages 빌드를 명시적으로 요청한다. 원격 브랜치가 바뀌면 push가 실패하며 강제 덮어쓰기를 하지 않는다.
- `/tools/dps/`와 `/ko/tools/dps/`: 방문자 입력 없는 서버 계산 순위. `data/dps-benchmark.json`의 공통 20레벨·공격력 1000·치명 25%·적중 100%·동작 1초 가정으로 8개 직업을 계산한다. 3개 학습 시드에서 학습 전투의 누적 피해/시간으로 사이클을 선택하고, 별도 180초·240초 보스 전투에서 평가한다. 종합 순위는 두 전투의 피해 합/전체 시간 합이며 개선율·반올림 값으로 정렬하지 않는다.
- `data/dps-skill-levels.json`: 96개 액티브의 기본·20레벨 직접/지속 피해와 문양별 수치를 출처와 툴팁 해시에 묶는다. 선형 레벨 배율을 추정하지 않는다. 보스 면역·공격 불가·선행 조건·원소 중첩·문양 만료를 검사한다. 고통의 연쇄가 적중한 뒤 지속 피해 시간만 선행 상태를 제공하는 가정은 화면에 명시한다. 미확인 차징 시간·펫 주기·덫/바닥 발동을 임의로 보완하지 않는다.
- 서버 계산: `node scripts/build_dps_rankings.js --train`으로 검토된 공식/프로필에서 학습 정책을 갱신한다. `python build.py`는 `--build`로 순위 JSON/CSV를 먼저 계산하고 HTML에 넣는다. 수식·데이터·정책 해시가 달라지면 학습 정책 검증에 실패하므로 재학습 없이 이전 결과를 새 기준으로 게시할 수 없다. `--verify`가 정책·수치·CSV의 재현성을 검증한다.
- 실제 동일 장비·동작 실측·특화·스티그마·자원 지속 가능성·일부 확률 연계가 미완성이므로 공통 글로벌 모델 순위로 표시하며, 한국 패치나 현재 최종빌드 티어로 확정하지 않는다. 방문자 기기 상태와 URL 매개변수는 점수에 영향을 주지 않는다. 매시간 서버 빌드에서 결과를 재계산하고 더 새로운 북미 패치가 수집되면 재검토 안내를 렌더링한다. 수치 조정을 자동 추정하지 않는다.
- `/screenshots/`: NC가 Steam에 공개한 실제 인게임 홍보 장면 3개를 공식 CDN에서 표시한다. 전투·대형 적·비행 이미지를 초반·엔드게임·지도 공략에 연결한다. HUD 없는 공식 이미지이며 빌드 실측이나 확인되지 않은 보스명의 증거로 쓰지 않는다. 커뮤니티 이미지의 재사용 상태는 기존 원본 링크 정책을 유지한다.
- `data/coverage-audit.json`: 실제 검토한 공략 보강 항목과 출처. 최종빌드 입력, 지역별 패치 차이, 같은 조건의 실측 순위가 현재 보강 대상이다. 검토 완료일은 수집 시간과 별도로 관리한다.

검증: Python 수집·캐시·원문 변경 테스트, Node DPS 수학/시간축 테스트, 기존 방문 분석 테스트, 정적 링크·언어·JSON·SEO 검사.


## Full patch pages

`patchbook.py` renders compact cards and a stable `updates/<region>-<articleId>/`
page for each collected patch in both languages. `data/patch-reviews.json` now
stores original editorial facts for every section, all numeric reward/schedule
rows and each class-specific change. Publisher article HTML is not republished.
The seven source patches present at rollout have complete section coverage.

Class impact is aggregated per class. A buff and a nerf together produce
`adjustment`; fixes and tooltip-only edits keep their own labels. A percentage
change is relative to the named skill, not to the class's total DPS. Next-week
plans remain in their own clearly marked section. Korea's 권성 is retained as a
Korea-only entry; it is not added to the Global class selector.

A reviewed `detail.coverage: complete` requires source-hash equality, bilingual
editorial notes, matching `sourceSections` and complete factual tables. On a
source revision, the collector clears detail, summary and class claims until
reviewed again. New unreviewed detail routes still link to the publisher. The
open detail page also checks for revisions without silently retaining changed
class claims. When reviewing a new patch, update the full section list together
with the summary and class rows before marking coverage complete.

Hourly publication may change only news data, home strips, patch index/detail
pages, DPS patch-review notices and their sitemap/search registrations. The scheduled whitelist cannot modify ranking source data or trained policies. Its whitelist checks tracked and
untracked files; new detail routes are staged for the existing Pages build.
Portrait attribution is in `assets/classes/credits.json` and on detail pages.
