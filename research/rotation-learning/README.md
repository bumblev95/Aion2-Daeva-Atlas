# 공략 기반 회전 학습 / Guide-informed policy learning

이 연구는 인벤 원본 글의 스킬 순서·우선순위를 사람이 검토해 [claims.json](claims.json)에 주석 처리하고, 조건 검사 엔진 안에서 공격 정책을 탐색합니다. [출처 기록](../gameplay-evidence.json)에 작성자·날짜·관찰 상태가 연결됩니다. 영상이 없어도 텍스트를 회전 후보로 사용할 수 있습니다.

## 무엇을 학습했는가

각 후보는 모든 입력 기술의 우선순위와 가까운 쿨타임을 기다릴 수 있는 시간 값으로 구성됩니다. 선택할 때마다 엔진이 상태·연계·쿨타임·동작 시간·MP·원소 조건을 검사합니다. 정책은 그 검사를 통과한 기술을 고르거나 대기할 수 있으며, 피해나 자원을 직접 바꿀 수 없습니다.

학습은 categorical cross-entropy policy search로 구현했습니다. 후보를 샘플링하고 학습 시나리오의 eDPS가 좋은 후보를 골라, 기술별 우선순위 위치와 대기 값의 확률 분포를 반복 갱신합니다. 공략에 나온 순서는 시작 후보로만 사용합니다. 각 글의 버프 지속 시간·모션·피해·발동 확률은 입력하지 않습니다. 특정 공략의 주장과 연구자의 해석을 규칙 문맥에 표시합니다.

선택 기준은 같은 직업에서 기존 우선순위보다 얼마나 개선됐는지입니다. 서로 다른 직업의 스펙이나 피해를 학습 정답으로 혼합하지 않습니다. 학습 시드 3개를 보존하고, 선택에는 학습 점수만 사용합니다. 별도 검증·테스트 시나리오는 선택한 정책을 평가하며, 음수 변화도 그대로 기록합니다. 가능한 정책 수가 작을 때 전수 비교해 **제한된 학습 공간**에서 얼마나 최적값에 가까운지도 확인합니다.

**현재는 실측 전투 로그가 없는 부분 시뮬레이션 학습입니다.** 직접 피해 초기값은 72/96개입니다. 나머지는 직접 공격이 없는 회복/해제/버프 13개, 차징 입력이 필요한 4개, 소환·덫·장판의 빈도/발동이 필요한 7개로 구분합니다. 기본 동작은 임시 1초입니다. 정령성의 직접 공격은 7개로 늘었지만 실제 소환 공격·원소 획득 시간축은 없으므로 정령·융합 최적 회전을 확인한 결과가 아닙니다.

송곳 화살·협공 저주·약화의 낙인·고통의 연쇄의 직접 피해와 지속 피해를 분리했습니다. 각 틱은 전투 종료까지의 시간축과 공격 불가 구간을 따라 계산합니다. 첫 틱·치명·갱신 규칙은 확인되지 않아 라이브 계산기의 기본값은 지속 피해 제외이며 사용자가 가정을 선택합니다. 연구는 첫 틱이 한 주기 후, 치명 없음, 재적용 시 기존 효과 교체로 선언합니다. 협공 저주의 5초는 Curse 공통 효과 문구의 해석이므로 별도 지속 시간 검증이 필요합니다. 문양 0–5중첩 피해표와 맹수의 포효의 10초 중첩을 사용하지만 개별 만료·폭발 시 전체 소모는 연구 가정입니다. 파티 버프/방어·증폭 합성, 평타 연속/캔슬 시간, 스킬 레벨 상승, 차징, 확률 초기화는 아직 불완전합니다.

[scenarios.json](scenarios.json)의 `sharedBuild`가 모든 직업의 공통 능력치·스킬 레벨·특화 조건을 고정합니다. 공격력 1000, 치명 25%, 치명 배율 1.5, 적중 100%, 사용자 배율 1, 기본 1레벨, 특화/스티그마 없음입니다. 패시브 추가 피해는 제외하고 불의 표식은 발동 조건 제공만 사용합니다. 시나리오가 공통 능력치나 계산 가정을 몰래 덮어쓰거나 직업의 스킬 레벨/동작 시간이 달라지면 학습을 거부합니다. **실제 동일 장비를 측정한 비교가 아닌 공통 수치 입력 실험**입니다. MP 제한과 장비 검증은 미완성입니다.

모든 분할에 같은 불완전한 엔진을 사용하므로 검증 시나리오가 실제 게임 정확도를 입증하지 않습니다. 선택이 끝난 정책을 그대로 두고 지속 피해 중첩·치명·문양 미소모·직접 피해만의 가정을 평가하여 민감도를 저장합니다. 이 값은 학습과 시드 선택에 사용하지 않습니다. [REPORT.md](REPORT.md)에 결과와 티어 차단 이유가 함께 있습니다.

## 재현

저장소 루트에서 실행합니다. Node 22+ 이외의 패키지나 외부 API가 필요하지 않습니다.

```sh
node tests/dps-math.test.js
node tests/rotation-learning.test.js
node research/rotation-learning/train.js --allow-unverified-guide-priors
node research/rotation-learning/train.js --verify
```

기본 실행에서 `--allow-unverified-guide-priors`를 빼면 공략 기반 시작 후보를 사용하지 않습니다. 명시한 옵션은 KR/Global 이름 대응이 미검증인 순서 후보의 연구 사용만 허용합니다. 계산 기본값이나 발동 규칙을 바꾸는 옵션이 아닙니다. 결과는 저장된 [model.json](model.json), [results.json](results.json), 보고서를 덮어씁니다. 실행은 재현 가능한 고정 시드이며 입력·엔진·학습 코드의 SHA-256을 저장합니다. 저장 결과를 검증할 때 해시가 달라졌으면 재학습 전까지 실패합니다.

`scenarios.json`은 전투 길이·공격 중단·상태 구간을 명시한 **인공 시나리오**입니다. 장비 수치, 고통의 연쇄 유지 구간과 조건별 성공률을 측정한 자료가 아닙니다. 학습에서 사용하는 최대 2초 대기 격자도 연구 설정이며 공략 작성자의 최적 시간으로 취급하지 않습니다. 본 연구 결과는 라이브 비교 순위나 티어 화면으로 가져오지 않습니다.

## 실제 DPS·티어까지 필요한 입력

동일 장비 예산·스킬 레벨·특화·파티 조건의 프로필, 기술별 직접 피해·DoT·정령 공격, 실제 동작/적중 시간, MP 수지와 상태·버프 유지 시간, 반복 초기화 기록이 필요합니다. 출처마다 다른 서버·패치를 유지하고, 그 프로필을 회전 재생에서 검증한 뒤 학습해야 합니다. 확률 효과가 추가되면 동일한 난수 시나리오에서 평균·분산을 비교해야 하며, 한 번의 최고 피해를 평균 DPS로 삼지 않습니다.

English: a common synthetic stat profile and base-1/no-specialization/Stigma selection are enforced across classes; this is not measured identical equipment. Source-backed direct/DoT and Insignia formulas are extended with explicitly declared timing/critical/refresh/consumption assumptions. Unresolved charges, pet/ground-effect frequency and trap triggers stay outside training. Fixed-policy held-out sensitivity tests never affect selection. Original guide prose is manually annotated into contextual hypotheses, not copied as a training corpus or used for language-model fine-tuning. A categorical proposal distribution learns priority orders and bounded cooldown holds from synthetic simulator rewards. Guide priors require an explicit research opt-in; reported mechanics/timings are never imported. Availability and damage stay owned by the existing engine. Deterministic seeds, input hashes, training-only selection and untouched held-out splits make the experiment reproducible. This does not learn measured expert performance, optimize complete builds or authorize class tiers.
