# 공통 조건 재학습 / Controlled-profile rotation learning

공략 후보를 이용해 **부분 시뮬레이터 안에서** 다시 학습했습니다. 실제 고수의 전투 로그 학습이나 검증된 최적 DPS·직업 티어가 아닙니다.

## 동일한 입력 조건 / Common build profile

전 직업 공격력 1000·치명 25%·치명 배율 1.5·적중 100%·사용자 배율 1, 액티브 기본 1레벨·특화/스티그마 없음. 실제 동일 장비가 아닌 공통 능력치 실험입니다. 불의 표식은 발동 조건 제공만 반영합니다.

All classes use attack 1000, critical chance 25%, critical multiplier 1.5, hit chance 100%, factor 1 and base-1 active skills without specializations/Stigmas. This is a shared stat-input experiment, not measured identical equipment. Fire Mark only provides an activation condition.

모든 기술 동작은 1초인 합성 입력입니다. MP 제한은 미검증 모드이며 파티 버프·방어/증폭 합성·실측 장비는 없습니다. 지속 피해는 첫 틱이 한 주기 후, 치명 없음, 재적용 시 기존 효과 교체로 가정합니다. 문양은 각 중첩의 개별 10초 만료와 폭발 시 전체 소모를 가정합니다. 고통의 연쇄 사용 구간은 명시한 합성 외부 구간이며 지속 피해 시간으로 자동 대체하지 않습니다.

## 보완한 피해 수학 / Damage coverage

직접 피해 초기값은 26개에서 72/96개로 늘었습니다. 별도 확률 효과·MP 회복·지속 피해 문구 때문에 직접 피해를 버리던 필터를 제거했습니다. 방패 강타·타격쇄·고통의 연쇄의 준비 기술도 실제 직접 피해를 계산합니다.

- 직접 공격이 없는 회복/해제/버프: 13개. 누락된 공격 피해로 계산하지 않습니다.
- 차징: 4개. 최소/최대 피해만 확인했으며 중간 단계·충전 시간은 미검증입니다. 학습에 넣지 않았습니다.
- 정령/신성한 기운/혹한의 바람/덫: 7개. 공격 빈도·발동 시각이 확인될 때까지 자동 피해를 지급하지 않습니다.
- 지속 피해: 4개. 송곳 화살·협공 저주·약화의 낙인·고통의 연쇄의 수치/주기를 별도 시간축으로 계산합니다. 협공 저주의 5초는 공통 Curse 효과 문구에서 해석한 입력이며 별도 지속 시간 검증이 필요합니다.

각 틱은 전투 종료까지만 계산합니다. 공격 불가 구간에도 효과 시간은 흐르며 그 구간의 피해는 사라집니다. 같은 스킬의 갱신 방식과 치명 규칙은 입력 가정이며 적중률 100% 미만에서는 확률적 적용·갱신을 임의로 지급하지 않습니다. 문양 0–5중첩 피해표를 적용하되 소모·갱신 방식은 아직 가정입니다. 원문과 전 항목 조사는 [생성 카탈로그](../../docs/data/dps.json) 및 [계산 규칙](../../dpsmath.py)에 연결됩니다.

## 학습 결과 / Learned policies

각 변화율은 같은 직업·같은 입력에서 기존 우선순위와 비교한 값입니다. 다른 직업끼리 실제 전투력을 비교한 순위가 아닙니다. 학습 시드 3개와 분리한 학습/검증/테스트를 사용하며 학습 점수로만 정책과 시드를 선택합니다. 원문은 사람이 주석 처리한 정성적 순서 후보로만 사용합니다.

| 직업 | 직접 피해 수치 | 검증 평균 변화 | 테스트 평균 변화 | 학습 공간 전수 비교 |
| --- | --- | --- | --- | --- |
| 검성 | 11/12 | 20.52% | 19.41% | 공간이 커서 미실시 |
| 수호성 | 10/12 | 14.44% | 13.94% | 공간이 커서 미실시 |
| 살성 | 11/12 | 18.78% | 20.31% | 공간이 커서 미실시 |
| 궁성 | 9/12 | 8.62% | 7.52% | 공간이 커서 미실시 |
| 마도성 | 8/12 | 10.65% | 11.91% | 공간이 커서 미실시 |
| 정령성 | 7/12 | 10.05% | 10.62% | 공간이 커서 미실시 |
| 치유성 | 6/12 | 14.07% | 14.87% | 0.00000000 |
| 호법성 | 10/12 | 62.27% | 58.08% | 공간이 커서 미실시 |

0%는 개선을 찾지 못했다는 뜻이고 음수는 테스트 입력에서 손해를 봤다는 뜻입니다. 모든 실패도 그대로 보존합니다. 현재 6–11개 기술의 정적 우선순위를 탐색합니다. 전수 비교 한도(6개)를 넘는 공간은 전수 검증하지 않으며 최적해를 보장하지 않습니다.

고통의 연쇄의 직접/지속 피해를 넣었으므로 이전 보고서의 “피해 0 준비기를 건너뛰어 얻은 개선”을 그대로 재사용하지 않습니다. 신규 결과에는 기존/학습 회전의 사용 횟수·직접 피해·지속 피해·틱 수가 모두 보존됩니다. 정령성은 직접 공격 7개가 들어갔지만 소환 공격 및 실제 원소 획득 시간축은 없어서 융합을 자동 사용할 수 없습니다.

## 미검증 규칙의 민감도 / Assumption sensitivity

아래는 학습한 정책을 그대로 두고 가정만 바꾼 테스트 평균 변화입니다. 재학습이나 시드 선택에는 쓰지 않았습니다. 가정에 따라 변화율이 크게 바뀌면 실제 최적 패턴으로 확정할 수 없습니다.

| 직업 | 직접 피해만 | 지속 피해 독립 중첩 | 지속 피해 치명 허용 | 문양 소모 없음 |
| --- | --- | --- | --- | --- |
| 검성 | 19.41% | 19.41% | 19.41% | 19.41% |
| 수호성 | 13.94% | 13.94% | 13.94% | 13.94% |
| 살성 | 11.59% | 20.31% | 20.31% | 20.31% |
| 궁성 | 8.72% | 7.23% | 7.41% | 7.52% |
| 마도성 | 11.91% | 11.91% | 11.91% | 11.91% |
| 정령성 | 23.37% | 10.62% | 9.94% | 10.62% |
| 치유성 | 54.59% | 14.87% | 13.63% | 14.87% |
| 호법성 | 58.08% | 58.08% | 58.08% | 58.08% |

English: source-backed base-1 direct terms increased from 26 to 72. Four DoT formulas have real tick scheduling, fight-end truncation and invulnerability suppression. First-tick phase, critical behavior, refresh and Insignia consumption are explicit research assumptions. Charges/summons/traps stay unavailable without verified timing inputs; non-attacks are separately classified. All eight classes share the declared stat and skill-level profile. Categorical proposal distributions are fitted only to training rewards; held-out and sensitivity results never select policies. No independent combat targets, measured gear loadouts or complete damage/animation models exist, so class tiers remain blocked.

## 최종 티어가 아직 차단되는 이유 / Tier blockers

- 직접 피해 수치 72/96개를 반영했습니다. 나머지는 비공격 기술·차징·소환·덫으로 구분했으며 미확인 피해를 0인 실측 값으로 취급하지 않습니다. / 72/96 active direct terms are modeled; remaining non-attacks, charges, summons and trap triggers are separately audited rather than measured zero damage.
- 기본 동작 시간은 임시 값으로, 실제 모션과 평타 캔슬을 측정하지 않았습니다. / Default action durations are placeholders, not measured animation/cancel times.
- 공통 능력치·기본 1레벨·특화/스티그마 없음으로 통일했지만 실제 동일 장비의 최종빌드를 측정하지 않았습니다. / A common stat budget, base-1 level and no-specialization/Stigma profile is enforced; actual identical equipment/endgame builds are not measured.
- 확인한 지속 피해 수치는 포함했고 첫 틱·치명·갱신·문양 소모는 연구 가정입니다. 정령 공격·버프/방어·차징·확률 초기화는 아직 미완성입니다. / Known DoT numbers are included with explicit tick/crit/refresh and Insignia consumption assumptions; pets, buff/defense composition, charges and resets remain incomplete.
- MP는 미검증 모드이며, 제공한 상태 구간은 실제 유지율을 측정한 값이 아닙니다. / MP mode is explicitly unverified; synthetic availability windows are not measured uptime.
- 한국 공략과 현재 Global의 조건 대응이 미검증이고, 실전 피해 정답 데이터가 없습니다. / KR guide mapping to current Global rules remains unverified; no measured combat target labels exist.
- 검증·테스트에도 같은 불완전한 엔진을 쓰므로 실제 게임의 정확도가 검증된 것은 아닙니다. / Held-out simulator scenarios share the same incomplete engine; they cannot validate live-game damage.

재현과 출처: [README](README.md), [claims](claims.json), [공통 입력](scenarios.json), [model](model.json), [results](results.json). 코드와 입력 SHA-256이 바뀌면 저장 결과를 재학습해야 검증을 통과합니다.
