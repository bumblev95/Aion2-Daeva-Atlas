# 공략 기반 회전 학습 연구 / Guide-informed rotation learning

이 결과는 공략의 우선순위 후보를 이용해 **부분 시뮬레이터 안에서** 학습한 회전입니다. 실제 전투 로그를 학습하거나 검증된 최적 DPS·직업 티어를 얻은 결과가 아닙니다.

현재 직접 피해 입력은 26/96 액티브이며 70개가 빠져 있습니다. 동작 시간도 임시 입력입니다. 아래 개선률은 같은 직업·같은 입력에서 기존 우선순위와 비교한 값이며, 서로 다른 직업의 실제 전투력 차이가 아닙니다.

텍스트는 사람이 검토해 규칙으로 주석 처리했습니다. 원문을 대량 복제하거나 언어 모델을 미세조정하지 않았습니다. 선택적 공략 후보로 탐색을 시작하고, 좋은 후보를 낸 우선순위 위치·대기 값의 확률을 반복 갱신했습니다. 학습 시드 3개와 별도 검증/테스트 시나리오를 사용했습니다. 모델·결과 JSON에 코드와 입력 파일의 SHA-256을 기록합니다.

| 직업 | 직접 피해 범위 | 검증 시나리오 평균 변화 | 테스트 시나리오 평균 변화 | 학습 공간 최적값과의 차이 |
| --- | --- | --- | --- | --- |
| 검성 | 4/12 | 0.00% | 0.00% | 0.00000000 |
| 수호성 | 4/12 | 1.37% | 0.63% | 0.00000000 |
| 살성 | 3/12 | 0.00% | 0.00% | 0.00000000 |
| 궁성 | 5/12 | 0.40% | 0.00% | 0.00000000 |
| 마도성 | 4/12 | 0.00% | 0.00% | 0.00000000 |
| 정령성 | 1/12 | 0.00% | 0.00% | 0.00000000 |
| 치유성 | 2/12 | 4.69% | 5.52% | 0.00000000 |
| 호법성 | 3/12 | 0.00% | 0.00% | 0.00000000 |

0%는 개선을 찾지 못했다는 뜻이며 최적의 실제 직업이라는 뜻이 아닙니다. 정령성은 현재 피해 입력이 냉기 충격 한 개뿐이어서 기술 간 순서를 배울 수 없습니다. 테스트 변화가 음수이면 그대로 실패 결과로 남깁니다.

치유성 개선에는 외부에서 합성 고통의 연쇄 구간이 주어진 상황에서, 피해 0으로 처리된 고통의 연쇄 준비기를 덜 써서 시간을 절약하는 효과가 포함됩니다. 실제 고통의 연쇄의 피해·직접 유지·디버프 가치가 빠져 있으므로 이를 실제 최적 회전이나 향상률로 해석할 수 없습니다. 결과 JSON은 기존/학습 회전의 사용 횟수를 함께 보존해 이 효과를 드러냅니다.

전수 비교의 범위는 현재 들어 있는 기술의 고정 우선순위와 선언된 쿨타임 대기 값뿐입니다. 버프 배율·평타 캔슬·상황별 오프닝·정령 공격·확률 초기화를 포함한 전체 게임의 최적해를 보장하지 않습니다. 살성의 버프 정렬이나 마도성의 차징 대기는 주장 데이터에 기록했지만 현재 보상 함수에 구현하지 않았습니다.

These are learned policies in a partial synthetic simulator, not measured expert rotations or live-game tiers. Text was manually annotated; categorical proposal probabilities were fitted to training rewards. Three seeds and distinct validation/test conditions are retained, including regressions. Exhaustive comparison certifies only the declared static-priority/cooldown-hold family on training scenarios. The same incomplete engine generates every split, so this is robustness testing, not independent combat validation.

## 최종 티어가 아직 차단되는 이유 / Tier blockers

- 액티브 96개 중 70개의 기본 직접 피해가 없으며, 준비 기술의 0 피해는 실측 결과가 아닙니다. / 70/96 active skills have no default direct-damage seed; helper zero damage is not a measured total.
- 기본 동작 시간은 임시 값으로, 실제 모션과 평타 캔슬을 측정하지 않았습니다. / Default action durations are placeholders, not measured animation/cancel times.
- 동일 장비 예산·스킬 레벨·특화·패시브를 갖춘 실제 빌드를 비교하지 않았습니다. / Equipment, skill levels, specializations and passives are not calibrated to comparable real builds.
- 지속 피해·정령 공격·파티 버프·차징 단계·확률 초기화가 보상 모델에서 빠져 있습니다. / DoT, pet attacks, party buffs, charge stages and reset probabilities remain outside this partial reward model.
- MP는 미검증 모드이며, 제공한 상태 구간은 실제 유지율을 측정한 값이 아닙니다. / MP mode is explicitly unverified; synthetic availability windows are not measured uptime.
- 한국 공략과 현재 Global의 조건 대응이 미검증이고, 실전 피해 정답 데이터가 없습니다. / KR guide mapping to current Global rules remains unverified; no measured combat target labels exist.
- 검증·테스트에도 같은 불완전한 엔진을 쓰므로 실제 게임의 정확도가 검증된 것은 아닙니다. / Held-out simulator scenarios share the same incomplete engine; they cannot validate live-game damage.

다음 입력은 직업별 동일 장비 예산·스킬 레벨·특화, 실제 동작/적중 시각, MP 수지, 버프·DoT·정령의 공격 시간축, 초기화 반복 실험입니다. 그 입력으로 공략 후보를 다시 학습하고 실제 로그의 사용 횟수·피해 분포를 재현한 뒤 티어를 평가해야 합니다.

Full inputs and independently measured replay targets are required before comparing class tiers. See [claims](claims.json), [model](model.json), [results](results.json), and [reproduction instructions](README.md).
