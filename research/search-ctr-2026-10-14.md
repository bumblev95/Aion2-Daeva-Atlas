# Search click review — October 14, 2026

## What the supplied evidence actually shows

The supplied Search Console screenshot shows the first 10 of 13 query rows. The date range, property-wide totals, matching landing pages, average positions, countries and devices are outside the crop. These rows cannot establish the whole site's CTR or prove a ranking, indexing, mobile or title problem.

| Visible query | Impressions | Clicks |
| --- | ---: | ---: |
| aion 2 what does 3b mean | 25 | 0 |
| aion codex | 24 | 0 |
| aion 2 what is 3b | 8 | 0 |
| aion 2 commend player | 8 | 0 |
| aion2index | 5 | 0 |
| what does 3b mean in aion 2 | 4 | 0 |
| aion 2 codex | 2 | 0 |
| aion2 3b | 2 | 0 |
| aion 2 3b | 1 | 0 |
| aion2codex | 1 | 0 |
| **Visible rows only** | **80** | **0** |

The five 3b variants account for 40/80 impressions. Codex/index-name variants account for 32/80; these may be navigation to existing databases, so their intent is uncertain. Commendation accounts for 8/80. Search impressions are not unique people.

The user clarified that **3b means a party run that clears all three bosses**. The original Inven author also defines it this way. It is a party recruitment convention, not an item or a build.

## Findings, with confidence separated

- **Observed:** At the starting commit, the maps title was “Find your next destination.” and the skills title “Know the skill behind the name.” Several other hubs lacked AION 2 in their titles. These do not clearly communicate the game and topic in a search result. The homepage description also omitted much of the site's newer progression and boss content.
- **Observed:** The existing 3b answer was a short definition deep in the beginner settings panel. No dedicated party-question guide existed. Commendations were explained in dated patch detail, rather than a task-oriented guide.
- **Observed:** Real static HTML, canonical URLs, en/ko alternates, a sitemap and indexable hub pages were already present. This review found no reason to replace those mechanisms.
- **Hypothesis:** Question-to-title mismatch may reduce relevance and the reason to click. The actual Google title/snippet shown for these impressions is not available; a public search index is not proof of the historical Google listing.
- **Hypothesis:** Some codex/index searches are navigational and unlikely to convert to an independent guide. Do not imitate another site's name or fill pages with its brand keywords.
- **Unresolved:** Low positions, a small/new sample, in-result answers and country/device differences could explain some or all zero-click observations. No causal CTR improvement is claimed.

A redesign after arrival cannot by itself explain why someone did not click a search result. The immediate changes target search relevance and a useful destination, while preserving the focused guide layout.

## Published changes

1. Descriptive game/topic titles for the homepage, beginner/progression/routine/gear/map/skill/dungeon/community hubs, guide directory, eight class profiles and six boss pages, in English and Korean. Homepage description and heading now reflect actual progression, boss, reward and map content.
2. `/guides/3b-meaning/` and its Korean counterpart: direct answer, three-boss diagram, 200k+/3b/tp recruitment example, run-plan advice, reward guide and six boss guide links.
3. `/guides/commend-player/` and its Korean counterpart: post-boss selection flow, eligibility and missing-popup checks. The official KR source scope is explicit; Global eligibility and exact labels are not asserted. September 23 alliance eligibility supersedes the initial KR party-only rule.
4. Native links from home, guide directory, beginner party terminology and glossary, plus bilingual search entries and sitemap entries. New pages are complete without JavaScript; no new account, external script or tracking event is introduced.
5. “Popular growth guides” renamed “Growth guides”: no popularity data was available.

## How to evaluate the change

After Google recrawls the pages, use Search Console for the new URLs and the matching query groups. Keep Search type = Web and compare equivalent date windows, country and device. Inspect clicks, impressions, CTR and position together. Record which URL appears for each query. Include all 13 rows or export the full query/page data; do not reuse the cropped 80 as a property total.

- If the page is far down the results, investigate relevance, distinctive content and ranking before blaming snippet copy alone.
- If comparable positions gain impressions but no clicks, inspect the actual Google title/snippet and whether the question is already answered in the result.
- If visitors arrive, inspect aggregate guide engagement separately. Analytics consent means its visits need not equal Search Console clicks.
- Retain one stable title per review window; do not promise or infer a lift from a few impressions.

No Search Console submission or indexing request was performed in this change. Publication does not guarantee indexing or immediate replacement of Google's title/snippet.

## Sources

- Google title-link guidance: https://developers.google.com/search/docs/appearance/title-link
- Google snippet guidance: https://developers.google.com/search/docs/appearance/snippet
- Search Console metric definitions and filtering: https://developers.google.com/search/blog/2022/10/performance-data-deep-dive
- Original party terminology: https://m.inven.co.kr/board/aion2/6444/2116 (author 구원의노래, July 20, 2026)
- Official commendation rules: https://aion2.plaync.com/ko-kr/board/update/view?articleId=6aa062386b722c561dc6a46c
- Official Trial popup fix: https://aion2.plaync.com/ko-kr/board/update/view?articleId=6aa99cb8a279104f7d9d5c34
- Official alliance eligibility and popup fixes: https://aion2.plaync.com/ko-kr/board/update/view?articleId=6ab2d738a279104f7d9d5d5b

The three official article bodies were checked through NC's public article API on October 14. Normalized content hashes match the previously reviewed originals; see `party-guide-source-review.json`. No publisher body HTML is republished.
