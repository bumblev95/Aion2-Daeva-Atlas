# Boss scene review — 2026-10-08

All 16 lessons now link to a specific publisher-hosted scene and the relevant article section. The KR Conquest articles and their media associations were reviewed; the response descriptions are our own bilingual summaries. No source images, loops, thumbnails or video files were copied or embedded. `fieldnotes.py` holds each cue, response, position, mistake and success condition; `bossmedia.py` holds its attribution and verification status.

## Primary evidence

| Source | Author and date | Scope |
| --- | --- | --- |
| [Krao / Draupnir](https://www.inven.co.kr/board/aion2/6444/458) | Nirr · Inven · 2025-11-25 | KR Conquest |
| [Urugugu / Vakron](https://www.inven.co.kr/board/aion2/6444/521) | Nirr · Inven · 2025-11-28 | KR Conquest |
| [Fire Temple](https://www.inven.co.kr/board/aion2/6444/655) | Nirr · Inven · 2025-12-05 | KR Conquest, not a later Trial encounter |
| [Fierce Horn](https://www.inven.co.kr/board/aion2/6444/803) | Nirr · Inven · 2025-12-15 | KR Conquest |
| [Expedition observations](https://gamechosun.co.kr/webzine/article/view.php?no=219539) | 이시영 · GameChosun · 2026-01-15 | KR normal Conquest |

## Pattern association and resulting lesson

| Pattern | Original scene | Explanation / visual correction |
| --- | --- | --- |
| Berk · cover | [Screenshot](https://www.gamechosun.co.kr/dataroom/article/20260115/219539/862663_1768469037.jpg) | Arrive early and check protection, including during the blast. |
| Berk · spin | [Screenshot](https://static.inven.co.kr/column/2025/11/25/news/i1777704511.png) | Red-particle cue; a chasing spin has no stationary safe circle. |
| Berk · stagger | [Screenshot](https://static.inven.co.kr/column/2025/11/25/news/i1861547977.png) | Reserve skills; empty the unlocked bar. |
| Bakarma · wave | [Loop](https://static.inven.co.kr/column/2025/11/25/news/i0156339433.webp) | Jump before contact, then close for stagger; avoid later tornadoes. |
| Bakarma · dive | [Loop](https://www.gamechosun.co.kr/dataroom/article/20260115/219539/986304_1768470217.webp) | Observe heading and silhouette; remove the invented underwater route. |
| Auldor · stack | [Screenshot](https://static.inven.co.kr/column/2025/11/28/news/i1581418761.png) | Airborne boss and red mark; gather for the shared landing. |
| Auldor · feathers | [Loop](https://static.inven.co.kr/column/2025/11/28/news/i0307490781.webp) | Leave the frontal attack; shock removal if caught. |
| Vakron · bind | [Loop](https://static.inven.co.kr/column/2025/11/28/news/i0197422466.webp) | Green health bar; keep clear before rescuing the bound ally. |
| Vakron · prison | [Screenshot](https://static.inven.co.kr/column/2025/11/28/news/i1924459847.png) | Destroy red rock before exiting through that opening; stagger stays locked. |
| Vakron · rings | [Loop](https://static.inven.co.kr/column/2025/11/28/news/i0459863811.webp) | Sidestep lines, jump three rings, then the separate binding follow-up. |
| Kromede · bow | [Loop](https://static.inven.co.kr/column/2025/12/05/news/i0386436973.webp) | Leave boss-centred fire; show both low-HP bursts. |
| Kromede · clones | [Loop](https://static.inven.co.kr/column/2025/12/05/news/i0117366601.webp) | Stay spread through both hits. |
| Kromede · walls | [Screenshot](https://static.inven.co.kr/column/2025/12/05/news/i1427011434.png) | Match each new opening; the player fits each illustrated gap. |
| Nuakum · intercept | [Loop](https://static.inven.co.kr/column/2025/12/15/news/i0464660879.webp) | Eligible ally intercepts for the immobilised target; rotate. |
| Nuakum · circles | [Screenshot](https://static.inven.co.kr/column/2025/12/15/news/i1372398522.png) | Large: target alone; small: share. |
| Nuakum · orb | [Screenshot](https://static.inven.co.kr/column/2025/12/15/news/i1834589360.png) | Re-align each shot; three hits within four opportunities; avoid the dark zone. |

## Optional video navigation and limits

[Couga54's chapter index](https://couga54.github.io/aion2-guides/en/dungeons/) links BIGSKALA's `mMjaSbaVTjc`, identified there as TW footage with Russian narration. It supplies Auldor 4:30 / 4:45, Vakron 7:03 / 7:15 / 7:45, and Kromede 8:44 / 9:30 / 10:12. These are index-reported navigation points, not independently verified scenes. The Kromede bow chapter covers a broader bow phase; the Bakarma dive chapter is not confirmation of the heading observation. Existing 김호러 Horror and 만두집아들 links remain available.

YouTube playback encountered a human-verification wall. No cast durations, distances, movement speeds, fixed boss routes or frame timings were measured. The animation pace, geometry and party size remain teaching examples; article-supported response order and counts do not establish a measured replay. Current Global equivalence, other difficulties and loop timing remain unverified. These limits appear beside the lessons, not only here.

## Verification

Python regressions cover all 16 associations in both languages, original-host links, verification claims, readable steps, accessible controls, no-JavaScript content and generated pages. Node regressions exercise the shipped renderer across all lessons, repeated attacks, prison exit geometry, wall openings, playback rate, visibility and reduced motion. Existing site and analytics checks remain in CI. No network media is loaded by the tests.

The responsive layout, wrapping and touch controls are retained. Browser/on-device visual QA was not completed during this review; these checks do not claim it. Future gameplay verification must identify server, difficulty and source date before upgrading the verification status.

## Vakron full-run supplement — 2026-10-13

The existing six bosses and 16 KR patterns, scene references and bookmark parameters remain intact. `vakron.py` adds nine bilingual lessons in six native disclosure sections on the existing Vakron permalink. `assets/vakron.js` draws original response-order SVGs through the existing player controls; it illustrates party movement and retained hazards without presenting geometry or pace as measured gameplay.

Sources: [Vi.ki, updated 2026-10-12](https://aion2.vi.ki/vakron-sky-island-guide) and [NoBS Game Guides, 2026-10-04](https://www.youtube.com/watch?v=jYqmiyFEdk8). Article text and YouTube title/description were inspected. These article-reported navigation points are linked beside the relevant lesson:

| Locator | Supplement |
| --- | --- |
| 0:05 | Debuff management |
| 0:49 / 1:13 | First boss and party movement |
| 1:48 | Jump/glide route |
| 2:50 | Thamon |
| 3:40 | Element/altar route |
| 3:50 / 4:33 | Final boss |

The YouTube player stayed at 0:05 with a black buffering screen. One reload reached a buffering advertisement; no target gameplay frames were inspected. Transcript export returned a remote file locator inaccessible to this workspace, so it was not used as reviewed evidence. No complete playback, exact scene timing, physical/magic damage tests, or current-server equivalence was verified. These limitations travel with each source link. No source video, screenshot, thumbnail or transcript is committed or rehosted. Vi.ki and our adapted notes are attributed as CC BY-SA 4.0; the original teaching drawings are independently authored.

The Global-source three-jump lesson does not overwrite the KR archive’s separate binding follow-up. PC key references are labelled as such. First boss localised name, grab safe side, exact altar coordinates and Hard-mode behaviour are not invented. Stones/party rescue, first boss hands and flowers, traversal, petrify/shield, altar route and final escape are reachable through the full-run navigation and searchable in both languages.

Validation: static link/anchor/language checks and all existing boss regressions; new evidence-claim gates; real mobile Chromium tests at 320, 390 and 768 CSS pixels in KO/EN. Browser tests cover touch controls (44px minimum), initial reduced motion, scrubbing, pause/replay, speed selection, source flags, retained puddles/red-rock removal, section anchors, reload/language switching, legacy mechanic bookmarks/tabs and all 16 overview references. No-JavaScript tests retain native disclosure and hide ineffective playback controls. Screenshots are emitted as CI artifacts for visual inspection. This is browser emulation, not physical-phone or live-game testing.
