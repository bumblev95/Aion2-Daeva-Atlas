# eDPS activation audit / 발동 조건 조사

Reviewed 2026-10-08 against the repository's 2026-10-07 Global base-1 skill snapshot and individually published client-derived tooltips. These are tooltip references via MetaBot, not NC-certified combat measurements or verified KR rules. `dpsrules.py` holds the reviewed activation rules and `dpsmath.py` holds the expanded damage formulas; the generated catalog contains an audit for every one of the 96 active entries.

후속 피해 조사에서 직접 피해 초기값을 26개에서 72/96개로 확대했습니다. 방패 강타·타격쇄·고통의 연쇄도 준비 동작과 실제 직접 피해를 함께 반영합니다. 나머지 24개는 비공격 기술 13개, 차징 4개, 소환·장판·덫의 미확인 시간축 7개로 구분합니다. 지속 피해 4개는 별도 틱 시간축으로 지원하되 첫 틱·치명·갱신은 명시적 가정이며 기본값은 제외입니다. 문양 0–5중첩 피해표를 지원하지만 중첩 만료·소모 방식은 가정입니다. 패시브 추가 피해, 스티그마, 특화, 장비·고레벨 효과와 실제 소환 공격 빈도를 완성했다고 주장하지 않습니다. 차징과 미확인 시간축은 확인한 사용자 입력 없이 피해를 지급하지 않습니다. 세부 수학·공통 조건 재학습과 남은 한계는 [보고서](rotation-learning/REPORT.md)를 참고하십시오.

## Activation gates / 사용 가능 여부

| Skill(s) | Required condition | Simulation treatment |
| --- | --- | --- |
| [Burst Arrow](https://metabot.gg/en/aion-2/skills/burst-arrow) | Slow **or** Root | OR gate. Snare Shot provides a 5s Slow only under a declared susceptible-target assumption and 100% hit chance; otherwise enter observed windows. |
| [Condemnation](https://metabot.gg/en/aion-2/skills/condemnation) | Chain of Torment | Block without a confirmed prerequisite window. The provider's 10s DoT is documented but is not treated as an independently verified availability duration. |
| [Blaze](https://metabot.gg/en/aion-2/skills/blaze) | Fire Mark | Gate on the mark. Its passive tooltip supplies a 5s mark on a Fire hit; model this only when enabled, using Global references and 100% hit chance. A gated skill cannot bootstrap its own mark. |
| [Judgment](https://metabot.gg/en/aion-2/skills/judgment) | A preceding Shield Smite, Warding Strike or Shield Rush | Provider tooltips open a 2s window on skill use. Single-use consumption is a conservative editable model assumption, not asserted game behavior. |
| [Dark Crush](https://metabot.gg/en/aion-2/skills/dark-crush) | Impactful Crush or Spinning Strike | Providers open a 2s window. Stigma alternatives are unseeded. Single-use consumption is an editable assumption. |
| [Heart Gore](https://metabot.gg/en/aion-2/skills/heart-gore) | A landed critical hit | Trigger identity is known, availability lifetime is not. Require observed trigger windows; do not turn expected critical damage into a guaranteed unlock. |
| [Dimensional Control](https://metabot.gg/en/aion-2/skills/dimensional-control) | A Spirit uses its skill | The word “briefly” is not a duration. Require observed availability windows; no pet cadence is invented. |
| [Elemental Fusion](https://metabot.gg/en/aion-2/skills/elemental-fusion) | Four Elements after four Spirit skill events | Require four stacks, cap at four, spend all four at cast start. Initial stacks and event timestamps are explicit inputs. Do not infer pet attacks or specialization refunds. |
| Overhead Slam, Aerial Snare, Annihilate, Shadow Fall, Frost Burst, Wave Blow | Appropriate Knockdown / Stun / Frost, or the skill's immunity-target proc | Check named state. The 5%/7% immunity exception does not guarantee availability. Its confirmed trigger window must be entered separately. |
| Sword Aura Rampage, Flash Rampage, Storm Rampage, Arrow Scattershot, Flame Scattershot, Rapid Scattershot, Lightning Strike Scattershot, Gust Rampage | Stagger | No gauge formula, accumulation rate or Stagger duration is invented. Require observed Stagger windows. |
| Rush Strike, Shield Rush, Infiltrate, Tremor Crush | After Dodge **or** flying | Require supplied windows. The post-Dodge window and Stamina expenditure are unverified. |

Each catalog audit links its individual source. The 26 active entries with an activation or stack-resource gate are distinct from the 72 entries with audited base-1 direct damage; these are different coverage counts.

## Effects that are not base activation gates / 기본 발동 조건과 별개인 효과

- **Fire Mark:** the 20% additional-damage proc is separate from mark application. Do not multiply mark uptime by that proc or add its damage to Blaze. Passive proc damage remains excluded.
- **Drill Dart:** the snapshot attaches critical-hit wording to MP restoration. We therefore do not infer a critical-hit prerequisite for its direct hit. The disputed broader activation interpretation needs gameplay confirmation; crit-dependent MP recovery remains excluded. Its source-backed Bleed formula is available only when explicit periodic-damage assumptions are enabled.
- **Ambush:** the back-attack damage bonus is not permission to cast the base skill.
- **Suppressing Arrow / Deadshot:** Precision-dependent CC or extra damage is recorded as a conditional effect. The snapshot does not establish an unconditional base-hit activation gate. Audited base direct terms are handled separately from Precision-dependent effects. Conditional bonuses and charge/action timing still need verified inputs; a tooltip proc does not grant unconditional bonus damage.
- Specialization multi-hit, cooldown resets, chain additions and Stigma effects remain unmodeled. Insignia Explosion uses its source-backed 0–5-stack damage table; stack expiry/refresh and consume/retain behavior are declared assumptions, and its chance-based Stun is not made guaranteed. Having reviewed a tooltip does not mean all its effects were added to the damage formula.

## Resources / 자원

`data/dps-resources.json` records the base-1 MP table cell, URL, review date and exact skill-snapshot hash for all 96 active skills. 43 cells contain a number; 53 contain a dash. A dash is **unknown**, not verified zero. If the source skill snapshot changes, all stale MP defaults become unknown until re-reviewed; the condition-snapshot guard also blocks calculations until the activation audit is renewed.

MP limits are explicitly **unverified / omitted** by default. The optional budget requires user-supplied starting MP, capacity and regeneration. Known costs are editable for the actual build; blank costs block their skills when the budget is enabled. MP is spent before an action, restores after completion, and regenerates in downtime. Expected hit probability is not credited as a successful MP restoration. Costs and restoration from unselected specializations are excluded.

원소 4중첩은 MP 설정과 독립적으로 검사합니다. 회피의 스태미나 소모는 계산하지 않습니다. 문양 중첩별 피해 수치는 포함하되 만료·갱신·소모는 사용자 선택 가정으로 구분합니다. 사용자가 입력한 발동 구간도 실측 자료가 자동으로 검증됐다는 뜻은 아닙니다.

## Timeline and compatibility

- Existing expected-hit arithmetic, whole-fight eDPS denominator, shared action timeline, cooldown-at-start convention and downtime exclusion remain intact.
- Deterministic prerequisite effects appear at action completion; requirements are checked at cast start. Windows use `[start, end)`. These timing conventions and chain consumption are model assumptions, not measured game timings.
- Chance-based effects are not automatically guaranteed. A source-declared 100% NPC CC effect can apply only under the declared NPC/susceptible-target assumptions, certain hits and any required state; player-target probabilities remain separate. Effects with uncertain duration/probability and Global providers in KR builds stay blocked from automatic application. Use confirmed timed windows instead. No stochastic proc model or final class tier is claimed.
- Comparisons require the same external windows, target type/control, automatic-condition policy, resource mode/budget, initial elements, Spirit timestamps, periodic mode/critical/refresh rules and Insignia consumption assumptions in addition to the existing common inputs and matching source/model versions.
- Saved version-1 inputs are not ranked as current. Restoring a known source skill attaches its current reviewed gates, resets missing new environmental fields, and requires review before marking the version current. Custom skill IDs cannot collide on restore.
- CSV retains existing damage/cooldown columns and adds state windows, gates, provider metadata, chain mode, costs, gains, casts, blocked reasons, periodic-damage contributions and the periodic/charge/Insignia inputs. JSON objects are serialized explicitly; formula-like cell labels remain escaped.

Validation covers missing and alternative states, expiry, chains and downtime, uncertain hits/procs, MP exhaustion/restoration/regeneration, four-stack consumption, KR separation, source changes, same-condition keys, safe CSV, bilingual controls and original DPS mathematics. Analytical damage tests also cover exact tick times, refresh/overlap, fight-end truncation, invulnerability suppression, charge/timing confirmation, Insignia expiry and target-specific CC. Successful English/Korean Chromium runs, saved/legacy restore, actual CSV downloads and 320px/390px containment are linked in PR #18.
