# DPS comparison correction · 2026-10-09

The former public ranking used attack 1000, all known active skills at level 20, no specialization/Stigma/passive damage, unlimited unverified MP and one-second actions. Its Cleric result was 7284.85 DPS, with 61.7% of modeled damage periodic. Assassin passive damage and Spiritmaster pet attacks were absent. Ranger and Sorcerer charged attacks were excluded while other known damage was counted. Conservative omissions differed by class, so a common input profile did not create a valid class comparison. Training and held-out simulator tests only established reproducibility of the same incomplete assumptions.

That ranking, training profile and production policy were withdrawn. The factual tooltip models and offline condition-aware rotation experiment remain for research. They cannot publish a class tier. No arbitrary healer penalty, class order or fitted multiplier was introduced.

Reviewed public sources:

- [AionFlex Hall of Champions](https://aionflex.gg/hall-of-champions): record holders span bosses and equipment, so the overall maximum bars are not a class balance table.
- [AionFlex methodology](https://aionflex.gg/meta/methodology): per-character-week medians, regional separation, matched boss/CP indices and explicit sample floors. Summons without owner attribution may be missing; healer damage is measured while healing.
- [AionFlex Global 30-day class comparison](https://aionflex.gg/meta/classes?region=global&window=30d) and [KR comparison](https://aionflex.gg/meta/classes?region=kr&window=30d): preserve each scope independently. KR does not have a usable matched comparison in this review. Do not substitute Global for KR.
- KR Citadel Hard record tables for [Turgen](https://aionflex.gg/rankings/boss/2301721-willful-turgen?region=kr), [Griosa](https://aionflex.gg/rankings/boss/2301722-forbidden-hexbeast-griosa?region=kr) and [Basilus](https://aionflex.gg/rankings/boss/2301723-basilus-the-false?region=kr): review only the highest posted value per launch class and the posted count. Ignore the separate TW+KR percentile table on each page. K/M values are rounded; do not invent additional precision, damage totals or elapsed times.
- [JaMeter metrics](https://jameter.net/metrics) and [nDPS](https://jameter.net/guide/ndps): individual damage, party contribution, CP-relative efficiency and external-buff-neutral nDPS are different metrics. Unobserved buff attribution is not inferred.
- [JaMeter 10/7 weekly report](https://jameter.net/report/week/2026-10-07): in-progress, same-boss DPS-per-CP indices, at least 50 records. [Completed 9/30 report](https://jameter.net/report/week/2026-09-30): common 850–950K CP band, median DPS, at least 20 records per class. Boss/party composition still differs. The public reports do not explicitly identify a service region, so the snapshot marks it unspecified.
- [AIONING stats](https://aion.ing/aion2/stats.php): a manual cross-check link only. No database or private API is copied.
- [MetaBot client dungeon names](https://metabot.gg/ko_KR/aion-2/dungeons/citadel-of-the-fallen-daeva): bilingual boss identity cross-check, not a Korean combat balance source.

Only numeric public summaries are reviewed into `data/dps-observations.json`, with each page's SHA-256, URL and source precision. Builds compute publication order and enforce coverage gates, without network requests or visitor-supplied stats. Public summaries are attributed to their publishers; they are not independently verified raw logs, simulated legal endgame builds, representative server populations or final current-patch tiers.

A useful raw-log backend would require exact damage ownership (including pets/procs), full encounter time, actual equipment/build, patch/region, buff events, resource/cast timing and repeated encounters. Until these exist, a plausible-looking simulated tier would repeat the original error.
