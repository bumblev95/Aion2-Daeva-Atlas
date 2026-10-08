# eDPS activation audit / 발동 조건 조사

Reviewed 2026-10-08 against the repository's 2026-10-07 Global base-1 skill snapshot and individually published client-derived tooltips. These are tooltip references via MetaBot, not NC-certified combat measurements or verified KR rules. `dpsrules.py` holds the reviewed rules; the generated catalog contains an audit for every one of the 96 active entries.

직접 피해 초기값은 기존 26개를 유지합니다. 나머지 70개, 패시브 피해, 스티그마, 특화, 장비·고레벨 효과는 채웠다고 주장하지 않습니다. 선행 기술 3개는 피해 0인 준비 동작으로 추가했습니다. 별도 피해 입력 없이 DoT·펫·발동 피해를 만들어내지 않습니다.

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

Each catalog audit links its individual source. The 26 active entries with an activation or stack-resource gate are distinct from the 26 entries with seeded direct damage; these are different coverage counts.

## Effects that are not base activation gates / 기본 발동 조건과 별개인 효과

- **Fire Mark:** the 20% additional-damage proc is separate from mark application. Do not multiply mark uptime by that proc or add its damage to Blaze. Passive proc damage remains excluded.
- **Drill Dart:** the snapshot attaches critical-hit wording to MP restoration. We therefore do not infer a critical-hit prerequisite for its direct hit. The disputed broader activation interpretation needs gameplay confirmation; crit-dependent MP recovery and its DoT remain excluded.
- **Ambush:** the back-attack damage bonus is not permission to cast the base skill.
- **Suppressing Arrow / Deadshot:** Precision-dependent CC or extra damage is recorded as a conditional effect. The snapshot does not establish an unconditional base-hit activation gate. These unseeded terms must be entered and verified separately.
- Specialization multi-hit, cooldown resets, chain additions, Stigma effects and Insignia damage scaling remain unmodeled. Having reviewed a tooltip does not mean all its effects were added to the damage formula.

## Resources / 자원

`data/dps-resources.json` records the base-1 MP table cell, URL, review date and exact skill-snapshot hash for all 96 active skills. 43 cells contain a number; 53 contain a dash. A dash is **unknown**, not verified zero. If the source skill snapshot changes, all stale MP defaults become unknown until re-reviewed; the condition-snapshot guard also blocks calculations until the activation audit is renewed.

MP limits are explicitly **unverified / omitted** by default. The optional budget requires user-supplied starting MP, capacity and regeneration. Known costs are editable for the actual build; blank costs block their skills when the budget is enabled. MP is spent before an action, restores after completion, and regenerates in downtime. Expected hit probability is not credited as a successful MP restoration. Costs and restoration from unselected specializations are excluded.

원소 4중첩은 MP 설정과 독립적으로 검사합니다. 회피의 스태미나 소모와 문양 중첩에 따른 피해·소모는 검증되지 않았으며 계산에 포함하지 않습니다. 사용자가 입력한 발동 구간도 실측 자료가 자동으로 검증됐다는 뜻은 아닙니다.

## Timeline and compatibility

- Existing expected-hit arithmetic, whole-fight eDPS denominator, shared action timeline, cooldown-at-start convention and downtime exclusion remain intact.
- Deterministic prerequisite effects appear at action completion; requirements are checked at cast start. Windows use `[start, end)`. These timing conventions and chain consumption are model assumptions, not measured game timings.
- Chance-based effects, uncertain duration/probability and Global providers in KR builds are blocked from automatic application. Use confirmed timed windows instead. No stochastic proc model or final class tier is claimed.
- Comparisons require the same external windows, target control, automatic-condition policy, resource mode/budget, initial elements and Spirit timestamps in addition to the existing common inputs and matching source/model versions.
- Saved version-1 inputs are not ranked as current. Restoring a known source skill attaches its current reviewed gates, resets missing new environmental fields, and requires review before marking the version current. Custom skill IDs cannot collide on restore.
- CSV retains existing damage/cooldown columns and adds state windows, gates, provider metadata, chain mode, costs, gains, casts and blocked reasons. JSON objects are serialized explicitly; formula-like cell labels remain escaped.

Validation covers missing and alternative states, expiry, chains and downtime, uncertain hits/procs, MP exhaustion/restoration/regeneration, four-stack consumption, KR separation, source changes, same-condition keys, safe CSV, bilingual controls and original DPS mathematics. Browser interaction results are recorded in the PR after verification.
