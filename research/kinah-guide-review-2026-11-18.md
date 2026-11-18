# 북미 키나 공략 수정안 · 2026-11-18

상태: 사용자가 2026-11-18 수정안 배포를 승인함. PR CI 검증 후 병합·배포 진행. 인게임 실측 없음.

## 대조 근거

- 기준 main: `067635237a045c9519081b4a515aa3bc7d1881e2`.
- [PR #91](https://github.com/bumblev95/Aion2-Daeva-Atlas/pull/91): 2026-11-18 08:56:12 UTC 병합 확인. 패치 요약에는 화폐 변경이 있지만 `kinah_guide()`에는 누락.
- [NC 북미 공식 패치](https://aion2.plaync.com/en-us/board/update/view?articleId=6afd5b00ebccad0e4b5bad8b).
- [공식 Steam 공지 재확인](https://steamcommunity.com/app/3393110/allnews/?l=koreana): 영문 Nov. 18 공지의 field-monster Kina / daily acquisition limit 문단 확인. Steam 표시 언어는 한국 서버 적용 근거가 아님.
- 저장소의 `data/patch-reviews.json`에 묶인 원문 해시: `f4f6e5541d26a74131f6b84001379bcd5e366270558dce78b22a2657341f0d8e`. 이번 작업에서 NC 원문 API에 직접 접근하지 못했으므로 해시를 새로 계산했다고 주장하지 않음.

## 유지·수정 판단

| 항목 | 기존 공략 | 수정안과 검증 수준 |
| --- | --- | --- |
| 필드 몬스터 직접 키나 | 최신 귀속 전환 설명 누락 | 모든 필드 몬스터의 직접 키나는 귀속. 북미 공식 확인 사실 추가 |
| 일일 한도 | 설명 누락 | 일일 1,000,000 획득 한도도 귀속 키나로 변경. 상한이며 보장 수입 아님 |
| 다른 보상과 한도 합산 | 설명 없음 | 계정/캐릭터 범위·리셋·다른 보상 합산·한도 이후 다른 전리품은 직접 확인 대기 |
| 사명 | 1회 귀속 50,000, 5회 250,000 | 수치·조건 유지. 10월 자료이며 이번 패치로 인게임 재검증한 값이 아님 |
| 비밀 보관소 | 10,000점 최대 300,000, 공통 일일 던전 횟수 | 수치·점수·공통 횟수 조건 유지 |
| 봉인 던전·퀘스트 | 15,000 귀속 참고 보상·미완료 성장 경로 | 수치·일회성 조건 유지 |
| 기존 550,000 예시 | 사명 5회 + 보관소 1만점 | 조건부 산술 예시 유지. 필드 100만을 더한 하루 보장 총액 계산 금지 |
| 거래 가능 자금 | 거래 가능한 던전 재료·채집·가공 재료 판매 | 경로 유지. 실제 아이템 거래 가능 여부·판매 성사·정산 비용 확인. 루드라 귀속 변형은 판매 재고에서 제외 |
| 장비 강화 | 귀속과 거래 가능 잔액으로 비용 예산 | 해당 강화 화면이 귀속을 받는지 확인 후 예산 반영. 모든 강화 비용 사용 가능·우선 차감이라고 단정하지 않음 |
| 거래소 구매 | 거래 가능한 자금 필요 | 기존 구분 유지. 북미 필드 직접 키나는 이 예산에 포함하지 않음. 이번 패치가 모든 기존 결제 규칙을 재검증한 것으로 표현하지 않음 |
| 사용 계산기 | 귀속 먼저 사용을 단정 | 산술 로직 유지. 귀속 우선 차감은 계산 가정, 북미 사용 가능 비용·차감 우선순위는 직접 검증 대기로 명시 |
| 한국 서버·시세·시간당 수익 | 별도 범위·실측 없음 | 규칙·수익 수치 새로 만들지 않음 |
| 검토일 | 공통 2026-10-12 | 키나 페이지 메타·사이트맵만 2026-11-18. 기존 보상표의 10월 검토일과 다른 공략 날짜 유지 |

## 한국어 핵심 안내 수정안

북미 전용 · 2026년 11월 18일: 모든 필드 몬스터의 키나 보상이 귀속 키나로 바뀝니다. 일일 1,000,000 키나 획득 한도도 귀속 키나로 변경됩니다. 이는 획득 상한이며 보장 수입이 아닙니다. 필드 몬스터가 직접 지급하는 키나는 거래소 구매 자금으로 계산하지 마세요. 이 북미 공지를 한국 서버 규칙으로 적용하지 않습니다.

기존 사명·비밀 보관소·봉인 던전·퀘스트 보상은 10월 자료의 조건부 참고값을 유지합니다. 필드 100만을 더해 하루 보장 총액으로 안내하지 않습니다. 거래 가능한 던전 제작 재료·채집물·가공품 판매는 해당 아이템의 거래 가능 여부와 실제 판매 정산을 조건으로 유지합니다. 귀속 변형은 판매용 재고에서 제외합니다.

귀속 키나는 결제 미리보기에서 허용하는 강화 비용에만 반영하세요. 거래소 구매는 거래 가능한 자금으로 계획합니다. 계정·캐릭터 범위, 초기화 시각, 다른 보상과 한도 합산 여부, 한도 이후 전리품, 귀속 사용처·차감 우선순위는 인게임 검증 대기입니다.

전체 한국어·영어 문구는 `progression.py`의 `kinah_guide()`와 `growthvisuals.py`의 `wallet()` 및 생성 HTML에 포함합니다. 최신 안내는 주제 탭 밖에 항상 표시합니다.

## English proposed guidance

NA only · November 18, 2026: All field-monster Kina rewards become Bound Kina. The daily 1,000,000 Kina acquisition limit likewise changes to Bound Kina; this is an acquisition ceiling, not a guaranteed payout. Do not count direct field-monster currency as Market purchasing funds. This NA notice does not establish KR rules.

Retain the dated October references for duties, the depository, sealed dungeons and unfinished quests with their original conditions. Do not add the field cap to the 550,000 example as a guaranteed daily total. Sales of dungeon materials, gathered goods and processed inputs remain conditional on the exact item being tradable and the sale settling. Bound variants are not sale stock.

Budget Bound Kina for enhancement only where the payment preview accepts it. Plan Market purchases with unbound funds. Account versus character scope, reset time, cap sharing with other rewards, other loot at the cap, accepted costs and debit priority still require in-game checks. The calculator's bound-first allocation is a budgeting assumption, not live NA verification.

## 회귀 검증

- `python build.py`: 726 indexable pages 생성 성공.
- `python validate.py`: 731 HTML 문서, 내부 링크·앵커·언어쌍·JSON·사이트맵 통과.
- `python -m unittest discover -s tests -p 'test_*.py'`: 99개 통과. 새 키나 테스트 5개 포함.
- 새 테스트: 공식 검토본과 일치하는 귀속/100만 한도, 북미 범위와 보장수익 금지, 주제 변환 이후 안내 보존, 기존 조건부 보상·판매 경로, 미확인 항목, 계산 가정, 양 언어 생성 파일·메타/사이트맵 날짜 검사.
- Node: analytics, DPS, DPS math/rankings, patchbook, rotation-learning, battle 통과. DPS/학습 산출물 `--verify` 통과. 변경 JavaScript 문법 검사 통과.
- 결정적 재빌드: 생성 파일 전체 경로·SHA-256 일치.
- 범위 검사: 기존 `data/`, 한국 규칙/루드라/공통 숙제 자료, 역사적 DPS 변경 없음.
- 로컬 브라우저 테스트: 환경 제한으로 Chromium 프로세스가 `socket() failed: Operation not permitted`에서 종료. UI 통과로 보고하지 않음. 기존 `progression-ui.test.js`에 한국어/영어, JS/무JS, 320px, 탭 전환 후 공지 유지 검증 추가. 로컬 브라우저 검증 한계는 PR CI에서 확인한다.

## 실제 북미 클라이언트 검증 절차 (미실행)

1. 지역·서버·클라이언트 버전·시각을 기록하고 귀속/거래 가능 잔액과 필드 획득 카운터를 캡처한다. 필드 몬스터 처치 전후 변화량을 분리한다.
2. 일일 100만에 가까운 카운터에서 처치 전후 증가·경고를 기록한다. 한도 도달 후 화폐와 재료 드롭을 따로 관찰한다. 판매 한도라고 해석하지 않는다.
3. 사명·던전·퀘스트를 각각 1회 전후 비교해 어느 카운터가 증가하는지 기록한다. 다른 캐릭터와 리셋 전후도 비교하되 확인 전 계정·캐릭터 단위를 확정하지 않는다.
4. 잔액 두 종류를 보유한 상태에서 강화 미리보기의 허용 화폐·차감 순서를 확인한다. 실제 강화 소비는 별도 사용자 선택으로 남긴다.
5. 재료의 귀속/거래 가능 변형과 거래소 등록 가능 여부, 거래소 구매 시 허용 화폐를 미리보기로 확인한다. 구매·판매 체결은 이 문서 검증으로 수행하지 않는다.
6. 전투 시간, 이동·대기, 판매 소요와 수수료가 포함된 실측 없이는 시간당 수익을 게시하지 않는다.
