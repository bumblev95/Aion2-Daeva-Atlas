# 실전 스킬 조합 조사 / Gameplay rotation evidence

조사일: 2026-10-08. 이 기록은 eDPS의 다음 개선을 위한 연구 자료입니다. PR #17은 사용 가능한 조건을 검사하지만 고수의 실제 회전을 재현하거나 최적 회전을 찾은 모델은 아닙니다. 아래 자료를 계산 기본값으로 가져오지 않았습니다.

Reviewed 2026-10-08. These records support future rotation work. PR #17 validates availability; it does not reproduce an expert rotation or optimize a build. None of these observations seeds the simulator.

## 직접 본 것과 아직 확인하지 못한 것

- 컷트라이의 치유성 연습 MP4 두 개에서 각각 영상 시작부터 4.75초까지 명목상 0.25초 간격으로 선택한 원본 장면을 확인했습니다. 원본은 15 FPS이므로 선택된 실제 프레임 시각과 이 간격은 정확히 일치하지 않을 수 있습니다. 허수아비 앞에서 짧은 공격 모션과 다음 효과가 반복되는 모습을 볼 수 있습니다. 고통의 연쇄·대지의 응보, 치유의 빛·대지의 응보라는 기술 식별은 작성자 설명에 근거합니다. 작은 HUD만으로 매 입력의 기술 이름·성공 적중·MP 변화량을 확정하지 않았습니다.
- 주요 YouTube 영상의 제목·작성자·설명·챕터는 확인했지만 본영상 스트림에 접근하지 못했습니다. 링크 확보나 챕터 확인을 전체 전투 시청으로 표시하지 않습니다. 보스 영상은 **전체 전투 미검증**, 공략의 순서는 **작성자 설명 확인** 상태입니다.
- 확보한 자료는 한국 서버의 서로 다른 시기·빌드입니다. 현재 한국판이나 Global의 동일 스킬 레벨·특화·쿨타임에 그대로 적용할 수 있는지는 확인되지 않았습니다. 공식 순위나 같은 조건의 로그로 작성자들의 현재 상위권 지위를 검증하지 않았으므로 모두를 검증된 랭커라고 부르지 않습니다.

Two Cleric practice clips were inspected through sampled original frames (nominal sample times 0–4.75 seconds, every 0.25 seconds; native 15 FPS frames need not align exactly). Skill identification comes from the accompanying author explanation; the small HUD does not establish every cast, hit or MP gain. YouTube metadata and chapters were accessible, but full video streams were unavailable. Author-reported rotations, full-fight verification and sampled-frame observations remain separate. These historical KR builds do not establish current KR/Global equivalence or independently verified player rankings.

## 직업별로 확보한 자료와 구체적인 조사 대상

| 직업 | 원본 자료 | 확인한 설명 / 다음에 영상에서 확인할 것 |
| --- | --- | --- |
| 치유성 | [컷트라이 · 2025-11-28](https://m.inven.co.kr/board/aion2/6452/408?vtype=mobile), [소티메리 · 2026-04-16](https://www.inven.co.kr/board/aion2/6452/16524), [소티의 가이드](https://www.youtube.com/watch?v=-iELblTrN1k) | 디버프를 유지하고 대지의 응보와 단죄를 짝지어 사용하며, 단죄가 기다리는 동안 심판의 번개나 보조기를 넣는다는 설명. 평타 적중과 MP 회복, 단죄 활성 구간·초기화, 치유 때문에 중단하는 시점을 따로 기록해야 합니다. |
| 마도성 | [나형임 · 2026-04-23](https://www.inven.co.kr/board/aion2/6453/10552), [나형이의 회전 영상](https://www.youtube.com/watch?v=hFTAb0JDTVU) | 첫 회전과 다음 회전의 순서가 다르며, 집중의 기원과 원소 강화에 맞추기 위해 지옥의 화염을 잠시 보류하는 설명. 쿨이 돌아왔다는 이유만으로 즉시 사용하는 회전과 구분해야 합니다. 불의 표식 확인, 차징 단계, 장판 안의 대상 체류도 조사 대상입니다. |
| 호법성 | [하구의 계속 수정되는 가이드 · 최초 2025-11-24](https://m.inven.co.kr/board/aion2/6451/116), [무스펠 보스전](https://www.youtube.com/watch?v=wvkgeSN_QPY) | 질풍의 권능 등 준비 후 평타와 백열격/암격쇄를 잇고, 암격쇄가 열렸을 때 먼저 쓰도록 배치한다는 설명. 타격쇄 등 선행 기술, 활성 아이콘, 접근·이탈, 버프·치유 유지로 공격을 멈추는 구간을 확인해야 합니다. 가이드의 최종 수정일은 미확인입니다. |
| 궁성 | [빵호빵 · 2025-11-27](https://m.inven.co.kr/board/aion2/6450/214?vtype=mobile), [원본 가이드](https://www.youtube.com/watch?v=WOEGlqV7uJc), [지옥햄스터의 반복 허수 실험 · 2026-04-26](https://www.inven.co.kr/board/aion2/6450/11715) | 영상 안내는 화살난사의 쿨타임 감소와 버프, 표적화살, 송곳/파열의 확률 초기화를 나눠 다룹니다. 초기 가이드는 작성자가 일주일차라고 명시한 후보 자료입니다. 반복 허수 실험도 개인 빌드 결과입니다. 둔화·속박 실제 성공, 조건부 기술 활성화, 초기화 여부를 확인하기 전에는 고수 회전으로 확정하지 않습니다. |
| 정령성 | [Sha2co · 2026-08-13](https://m.inven.co.kr/board/aion2/6454/9216?stype=nickname&svalue=Sha2co), [김바보의 불의 신전 정복 솔로 자료 · 2025-12-14](https://www.inven.co.kr/board/aion2/6454/634), [원본 보스 영상](https://www.youtube.com/watch?v=G1szvt7KwNA) | 파티 버프를 확인한 뒤 소환·융합을 맞추고, 원소 융합을 우선한다는 설명. 원소 4개 생성·소모, 정령 교체로 끊기는 공격, 초기화와 이동 중 공격 유지가 조사 대상입니다. 소환 횟수와 정령 기술 성공 횟수를 같은 값으로 취급하지 않습니다. |
| 살성 | [멍쮸야 · 2026-03-03](https://www.inven.co.kr/board/aion2/6449/5183) | 두 플레이어의 평타 섞기 방식과 피해 지분을 비교한 실전 자료. 장판을 밖에 놓는 역할도 달랐다고 작성자가 보완했으므로 우열을 확정할 수 없습니다. 치명타 후 심장 찌르기 활성화, 문양 생성·폭발, 후방 유지와 이동 역할을 실제 시간축으로 확인해야 합니다. 영상 회전은 확보하지 못했습니다. |
| 검성 | [김판금갑옷 · 2026-01-16](https://www.inven.co.kr/board/aion2/6448/3461), [수호굿의 사용 횟수·세팅 공유 · 2026-06-18](https://www.inven.co.kr/board/aion2/6448/21060), [원본 연습 영상](https://www.youtube.com/watch?v=J5GJ9w3zKdM) | 내려찍기가 열리지 않았을 때 대체 기술을 사용한다는 설명과 연습 기록을 확보했습니다. 넘어짐/면역 대상 발동, 평타 연계, 초기화, 실제 사용 횟수를 구분해야 합니다. 작성자 제목의 횟수를 현재 시뮬레이터의 동작 시간으로 역산하지 않습니다. |
| 수호성 | [멍덕팝 · 2026-01-08](https://www.inven.co.kr/board/aion2/6438/4572), [Jinsiwooe의 사나운 뿔 암굴 탐험 솔로 자료 · 2025-12-11](https://www.inven.co.kr/board/aion2/6438/1153), [원본 보스 영상](https://www.youtube.com/watch?v=hxDpOjMpsYs) | 도발·보호·격앙과 공격을 보스 패턴에 맞춰 배치한다는 설명. 심판을 여는 선행 기술, 막기·버프 발동, 탱킹 위치와 공격 중단을 확인해야 합니다. 첫 글은 자기 회전에 피드백을 구하는 자료이고, 탐험 솔로는 정복/성역 회전과 별도 조건입니다. |

English reading notes: Cleric mixes basic attacks with Condemnation and fills its downtime; Sorcerer sometimes holds a ready attack for a buff/reset; Chanter prioritizes an available follow-up while maintaining party support; Ranger needs independently observed control/reset events; Spiritmaster aligns summons/Fusion with party buffs; Assassin needs a real critical/mark/position timeline; Gladiator needs an unavailable-skill fallback; Templar needs tanking, block and prerequisite timing. These are author-reported behaviors or research questions, not measured optimal presets.

## 바로 찾아볼 수 있는 영상 구간

아래 시각은 작성자가 제공한 챕터입니다. 직접 검증한 스킬 이벤트 시각이 아닙니다.

| 원본 영상 | 구간 | 볼 내용 |
| --- | --- | --- |
| [빵호빵 궁성](https://www.youtube.com/watch?v=WOEGlqV7uJc&t=38s) | 00:38 / 01:24 / 06:45 | 스킬 운용 설명 / 쿨감과 버프 / 확률 초기화 |
| [하구 카이시넬 10단계](https://www.youtube.com/watch?v=_1S-5JZdgyI&t=174s) | 00:45 / 02:54 / 09:22 | 스킬 활용 / 해설 플레이 / 무편집 구간 |
| [하구 무스펠](https://www.youtube.com/watch?v=wvkgeSN_QPY&t=450s) | 01:07 / 02:46 / 07:30 | 신호등 / 비행 / 풀영상 구간. 회피·회복 후 딜 복귀를 확인할 후보 |

These timestamps are creator-provided navigation points, not independently observed cast times. Full-fight labels come from the creator, and the relevant difficulty/build still needs verification.

## 계산에 반영하려면 필요한 전투 기록

각 기록에 원본 링크·영상 시각과 전투 시작 기준 시각을 함께 남깁니다. 서버/패치, 보스/난도, 장비·스킬 레벨·특화·패시브·스티그마, 파티 버프와 스킬 예약 설정을 연결합니다. 확인되지 않는 값은 빈칸/미검증으로 유지합니다.

기술 입력, 사용 가능 아이콘, 실제 적중, 피해, 상태 시작·종료, MP/원소 변화, 쿨 초기화, 이동·치유·공격 불가 시간을 별도 이벤트로 기록해야 합니다. 버튼을 눌렀다는 사실을 피해가 성공한 사실로 바꾸지 않습니다. 같은 회전도 전투속도와 입력 환경이 다르면 모션이 달라질 수 있습니다.

그 자료로 오프닝, 지속 딜 우선순위, 버프 대기, 그로기 집중, 회피 후 재개를 구분합니다. 먼저 실제 입력 순서를 재생하는 모델로 관측 사용 횟수와 상태·자원을 대조하고, 이후 조건별 우선순위 모델을 비교할 수 있습니다. 시뮬레이터의 현재 공유 시간축·쿨타임·피해 수학을 바꾸기 전에 재생 회귀 자료가 필요합니다.

For a measured replay, retain video and fight-relative timestamps alongside server/patch, encounter/difficulty, build, party buffs and input settings. Separate input, availability, landed hit, damage, state start/end, resources, resets and downtime. Validate a recorded-action replay before deriving opening/sustained/burst/recovery policies. Unknown values remain unknown; a single successful proc does not establish its probability, and media FPS does not establish game action frames.

현재 회전 기본값과 직업별 최종 티어를 확정할 실측 근거는 부족합니다. 원본 영상·이미지를 배포 파일에 복제하지 않았으며, [연구 상태 JSON](gameplay-evidence.json)은 계산 데이터와 분리돼 있습니다.
