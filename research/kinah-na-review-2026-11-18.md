# 북미 키나 공략 수정 검토 — 2026-11-18

상태: 승인 전 수정안. 병합·공개 배포 없음. 직접 게임 플레이 검증 없음.

## 근거와 범위

- 공식 원문: https://aion2.plaync.com/en-us/board/update/view?articleId=6afd5b00ebccad0e4b5bad8b
- 공식 공개 API의 현재 본문을 다시 읽어 PR #91의 SHA-256 `f4f6e5541d26a74131f6b84001379bcd5e366270558dce78b22a2657341f0d8e`와 일치함을 확인했다. 조회 시각·기준 커밋은 동반 JSON에 기록했다.
- 비교 대상: `progression.py::kinah_guide()`, `growthvisuals.py::wallet()`, 한영 생성 페이지. 10월의 외부 자료를 이번 북미 클라이언트 실측으로 격상하지 않는다.
- 게임 한국어 번역과 한국 서버 규칙은 별개다. 한국어 공략에 북미 변경을 표시하되 한국 서버 규칙으로 확장하지 않는다.

## 유지·수정 비교

| 항목 | 기존 상태 | 수정안 | 근거 수준 |
|---|---|---|---|
| 필드 몬스터 직접 키나 | 변경·한도 설명 누락 | 북미 모든 필드 몬스터 직접 지급 키나는 귀속으로 표시 | 11/18 북미 공식 패치 |
| 일일 1,000,000 획득 한도 | 누락 | 귀속 키나 규칙 적용. 상한을 보장 수입으로 표시하지 않음 | 11/18 북미 공식 패치 |
| 한도의 상세 범위 | 설명 없음 | 계정/캐릭터, 초기화 시각, 타 보상과의 카운터 공유, 도달 후 동작 확인 대기 | 직접 검증 전 |
| 사명·보관소·봉인·퀘스트 | 10월 글로벌 보상 참고 | 수치·조건·경로 유지, 현재 북미 재검증 전임을 명시 | 기존 날짜가 있는 외부 자료 |
| 550,000 귀속 예시 | 사명 50,000 × 5 + 보관소 최대 300,000 | 계산 유지. 필드 한도 1,000,000과 합산한 보장 일수입을 만들지 않음 | 기존 조건부 산술 예시 |
| 거래소용 자금 | 거래 가능 제작·채집 재료 판매 | 경로 유지. 개별 귀속·등록·수수료·정산 화폐 확인 후 실제 판매분만 수입 계산 | 기존 자료 + 권고, 판매 실측 전 |
| 장비 강화 | 귀속분 우선 합산 계산 예시 | 계산 방식 유지. 해당 비용이 Kina (All)을 허용하는지·차감 순서 확인 안내 | 기존 화폐 자료, 11/18 패치가 새로 보장한 규칙 아님 |
| 거래소 구매 | 거래 가능 잔액으로만 구매 계산 | 유지. 직접 필드 키나를 거래소 자금에 넣지 않도록 명확화 | 기존 화폐 자료에 새 북미 보상 유형을 적용한 계획상 해석 |
| 검토일 | 성장 공략 공통 2026-10-12 | 키나 페이지 메타데이터·사이트맵만 11/18, 기존 보상표의 10월 날짜 유지 | 편집 검토일 |
| 한국 규칙·DPS·루드라 | 기존 별도 출처 | 데이터·공략 수치 변경 없음 | 변경 범위 보존 |

## 실제 반영할 한영 안내

아래는 새 북미 안내 카드의 코드 렌더링에서 추출했다. 게임 규칙의 신규 확정, 기존 자료에 따른 계획 권고, 미검증 항목을 구분했다.

### 한국어

북미 · 2026년 11월 18일: 필드 수입 귀속 전환

공식 패치 사실·계획 권고·인게임 확인 대기를 구분합니다. 10월 글로벌 참고는 원래 날짜와 범위를 유지합니다.

공식 · 필드 몬스터 보상

북미에서는 모든 필드 몬스터의 키나 보상이 귀속 키나로 바뀝니다. 일일 1,000,000 키나 획득 한도에도 귀속 키나 규칙이 적용됩니다. 획득 상한이며 보장 지급액이 아닙니다.

계획 · 강화 비용과 거래소 자금

필드 몬스터가 직접 지급하는 키나는 이제 거래소용 거래 가능 자금의 획득 경로가 아닙니다. 기존 화폐 자료에서는 Kina (All) 비용에 귀속분을 먼저 쓰고 거래소 구매에는 거래 가능분이 필요합니다. 실제 강화 비용의 화폐 표시·차감 순서는 인게임에서 확인해야 하며, 이번 패치가 이 사용 규칙을 새로 정한 것은 아닙니다.

유지 · 거래 가능한 재료 판매

이번 화폐 변경이 모든 제작 재료 판매를 무효화했다는 뜻은 아닙니다. 던전·채집·가공 판매 경로는 날짜가 있는 참고로 유지하고, 실제 아이템 귀속·등록 가능 여부·수수료·정산 화폐를 확인한 뒤 판매 완료분을 거래소 자금으로 계산하세요.

북미 인게임 확인 · 한도 세부 사항

캐릭터·계정 단위, 초기화 시각, 다른 보상과의 카운터 공유 여부, 한도 도달 후 동작은 미검증입니다. 모든 수입의 상한으로 확대하거나 거래소 판매가 포함·제외된다고 단정하지 마세요. 기존 550,000 예시에 1,000,000을 더해 일일 보장 수입으로 안내하지 않습니다. 한국 서버 규칙·시간당 실측 수익은 변경하지 않습니다.

### English

NA · November 18, 2026: bound field income

Official patch facts, planning advice and open client checks are separated below. October Global references retain their original date and scope.

Official · field-monster rewards

In NA, Kina rewards from all field monsters become Bound Kina. The daily 1,000,000 Kina acquisition limit also changes to Bound Kina. This is an acquisition cap, not a promised payout.

Planning · enhancement versus the Market

Direct field-monster Kina is no longer a route to unbound Market funds. The older currency reference says Kina (All) costs use bound funds first and Market purchases require unbound funds. Check the live enhancement cost label and debit order; the patch does not redefine those spending rules.

Keep · eligible material sales

This currency change does not establish that all crafting-material sales are invalid. Keep dungeon, gathering and processing routes as dated references; check the actual item binding, listing eligibility, fees and settlement currency before counting a completed sale as Market funds.

Verify in the NA client · cap details

Per-character or per-account scope, reset time, which other rewards share the counter, and behavior after reaching the cap remain unverified. Do not treat this as a cap on all income or assume Market sales are included or exempt. Do not add 1,000,000 to the older 550,000 example as guaranteed daily income. No KR rule or measured Kinah-per-hour is changed here.

## 회귀 테스트와 검증 결과

- `python build.py`: 통과, 색인 가능 페이지 726개 생성.
- `python validate.py`: 통과, HTML 731개·내부 링크/앵커·언어 대응·JSON·사이트맵 검사.
- `python -m unittest discover -s tests -p 'test_*.py'`: 98개 통과. 신규 4개는 공식 북미 해시 연결, 한영 안내·확인 대기·탭 밖 배치, 기존 보상 산술·판매 경로 보존, 한영 생성물·페이지별 날짜를 검사한다.
- 모든 JavaScript 구문·공백 오류 검사 통과. 재빌드한 전체 docs 바이트 동일성 확인. data·한국 규칙·DPS·기존 보상 및 지갑 계산 코드 변경 없음 확인.
- Node: DPS·수학·순위·순위 재현성·rotation-learning·학습 산출물 재현성·patchbook·analytics·battle 검사 통과.
- 브라우저 테스트 두 개(`progression-ui.test.js`, `growth-visuals-ui.test.js`)를 확장했다. 탭/직접 링크/스크립트 미사용에서 새 안내를 확인하고, 귀속 1,000,000·거래 가능 0으로 거래소 비용 1을 결제할 수 없는 경우를 검사하도록 했다.
- 이 환경에서 브라우저 테스트 두 개는 Chromium 실행 단계의 `socket() failed: Operation not permitted`로 차단되어 화면 검사 결과를 얻지 못했다. 위 두 브라우저 검사를 통과했다고 간주하지 않는다. PR CI 또는 Chromium 실행 가능 환경에서 확인해야 한다.

## 북미 인게임 검증 절차 — 아직 실행하지 않음

1. 서버·클라이언트 버전·캐릭터·계정과 두 화폐 잔액, 획득 카운터를 기록한다. 일반 필드 몬스터 처치 전후 귀속/거래 가능 잔액·카운터·드롭 로그를 대조한다.
2. 자연스러운 플레이 중 한도 근처와 도달 뒤 변화를 기록한다. 다른 캐릭터·동일 계정에서 카운터가 공유되는지 확인한다. 다른 계정의 한도는 별도 관찰한다.
3. 초기화 전후 서버 표시 시각·시간대·카운터를 기록한다. 임의의 05:00 또는 타 지역 규칙을 대입하지 않는다.
4. 사명·보관소·퀘스트 보상을 종류별로 따로 받아 잔액·카운터를 대조한다. 거래소 판매 대금도 정산 전후 따로 기록해 합산 여부를 확정한다.
5. 실제 강화 확인 화면의 화폐 이름·비용을 기록한다. 원래 계획한 강화가 있을 때에만 전후 잔액으로 귀속 허용·차감 순서를 확인한다.
6. 제작/채집 재료는 아이템별 귀속과 등록 가능 여부를 먼저 확인한다. 소량 거래 후 수수료·정산 화폐·실제 판매대금을 기록한다. 실패·미판매 재고는 수입으로 잡지 않는다.

검증 전에는 한도 배수에 따른 부캐 수익, 시간당 수익, 거래소 전체 수익 한도, 필드 외 보상 포함/제외를 확정하지 않는다. 병합과 공개 배포는 사용자 승인 이후 별도로 진행한다.
