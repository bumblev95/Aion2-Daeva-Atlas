# October 15, 2026: scoped combat-source review

## Published changes

- JaMeter's current reviewed period advances to [October 14–21](https://jameter.net/report/week/2026-10-14). The source explicitly marks it in progress. Eight launch classes meet the existing 50-record index floor; equal 1.13 indices share a place. This remains a provisional publisher index with an unspecified service region.
- The completed same-CP-band comparison advances to [October 7–14](https://jameter.net/report/week/2026-10-07). All eight launch classes have at least 20 records (59–186 per class). Its band is **750.0K–850.0K**, different from the prior report's 850.0K–950.0K. Neither different bands nor the two different metrics are combined into a trend or a class tier.
- Each dataset now carries its own collection and review dates in JSON, CSV and the bilingual page. A successful JaMeter refresh cannot advance AionFlex's October 9 review date.
- Patch warnings compare the official patch date with the underlying regional coverage, rather than the latest editorial review date. Re-reading old data does not establish current-patch DPS.

## Source boundaries

The Global and KR [AionFlex class pages](https://aionflex.gg/meta/classes?region=global&window=30d) still reported coverage at **2026-10-07 14:25 UTC**. The KR comparison still lacks sufficient shared coverage. Their values and all three historical KR boss snapshots remain unchanged.

The requested [Turgen](https://aionflex.gg/rankings/boss/2301721-willful-turgen?region=kr) and [Griosa](https://aionflex.gg/rankings/boss/2301722-forbidden-hexbeast-griosa?region=kr) pages redirected to Basilus, including a sequential retry. Their returned title identified the wrong boss. A full refresh would correctly fail the existing redirect/identity checks. The new explicit `--weekly-only` mode updates JaMeter while preserving AionFlex's values, hashes and original dates. No redirected boss values were imported.

No private APIs, player identities, raw-fight estimates, healing additions, synthetic builds, current-patch class tiers or pooled service regions are introduced. The new week is not relabelled complete based on the calendar alone.

Reviewed source HTML SHA-256:

- October 14: `9f255178b9ba6c13084b960524b8027e9a6c65c4616f64a114a04b1548af443b`
- October 7: `0fc00f3d11a29f3548e83c895d141e5c726b3ace33035391e7369c41c5353c60`

Publisher HTML was inspected in temporary review storage and is not republished.

## Same-day official KR hotfix

The [October 14 temporary-maintenance notice](https://aion2.plaync.com/ko-kr/board/notice/view?articleId=6acf3680263e537d356d1155), updated at **2026-10-14T10:31:58.662Z**, supersedes the morning patch's defensive cooldown value: **0.3s → 0.1s**. It also fixes the effect applying to passive attacks. This is KR-only and does not quantify total DPS.

The original regular-patch history is preserved and links prominently to a separate, hash-bound bilingual hotfix summary. The collector recognizes only the explicitly reviewed article on its exact notice feed as a patch; ordinary notices remain ordinary notices. A changed official body withdraws the old hotfix claims until re-reviewed.
