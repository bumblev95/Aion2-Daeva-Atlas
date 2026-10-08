# PLAYER’S CODEX — game guides and tools

An independent English/Korean game guide platform. AION 2 is the first game hub.

**Website:** https://bumblev95.github.io/Aion2-Daeva-Atlas/

**PLAYER’S CODEX** contains 16 video-linked mechanics across six dungeon bosses, 21 attributed Korean community notes from 15 sources, six original decision and practice guides, eight class playstyle profiles, a two-class comparison, 32 Korean/English glossary entries, full-text site search and a personal session planner. Both language editions are generated as real HTML, with matching language links, canonical URLs and a sitemap.

## Visual interface

The hub separates practical early-game and endgame guides, with direct settings references and attributed original screenshot previews; a complete 280-skill bilingual reference with game icons, class learning paths, and level-aware specialization choices; a 2D map with 384 real quest/travel/dungeon markers, search, panning, zoom, nearest travel points and saved completion; and 16 automatically animated boss lessons. Players can pause, scrub and change animation speed. Reduced motion is respected. Optional source footage is Korean. Existing class comparison, community insights, progression checklist and public URLs are retained. Source-era KR recommendations are separated from Global client facts.

## Develop

Python 3.12+ and Node 22+ are sufficient. There are no package dependencies.

```sh
python build.py
python validate.py
node --check assets/app.js
node --check assets/explorer.js
node --check assets/encounters.js
node --check assets/learn.js
node --check assets/analytics.js
node tests/analytics.test.js
```

Edit `content.py`, `fieldnotes.py`, `encounters.py`, `visuals.py`, `onboarding.py`, `skillbook.py`, `bossmedia.py`, `assets/` and `site.json`, then regenerate and commit `docs/`. GitHub Pages serves `main` → `/docs`. CI rejects a mismatch between the sources and generated pages.

## Editorial scope

- The guides contain original editorial advice and cite the background sources used.
- Class roles are qualitative orientation, not a damage benchmark or current tier list.
- No live boss mechanics, current skill coefficients or enhancement probabilities are invented.
- The first release is AI-assisted and does not claim human gameplay testing.
- Source review dates change only after a substantive review.
- The banner is an NC promotional screenshot from its Steam listing; see assets/credits.json. Class icons and schematics are original illustrations. Boss diagrams summarise cited KR mechanics; positions, distances and timings are not measured. Linked English skill names and base tooltips come from individual MetaBot Global database entries. KR build claims are kept separate from Global tooltip facts. Scales (천칭) remains an explicitly literal Arcana translation, not an asserted client name.

## Privacy and monetization

The planner stores its list in browser local storage; the class explorer can also save one preferred class. Existing planner data keeps its original storage key. It does not have a backend or accounts. Ad delivery is off. The existing publisher verification tag and Google HTML ownership file are installed. GA4 is connected to the dedicated PLAYER’S CODEX web stream and loads only after the visitor allows analytics. No external font scripts are installed. Beginner completion is local to the browser. Inven source links open additional loops; TH.GL hosts terrain previews and optional marker maps; YouTube hosts thumbnails and on-demand videos and may serve its own ads/storage. Media are not downloaded or republished in the repository. The public contact channel is GitHub Issues.

AdSense is configured **off**. See [OPERATIONS.md](OPERATIONS.md) before enabling it. This project is a path under the existing bumblev95.github.io AdSense site, not a separately registrable AdSense domain. Check the existing host’s review status in AdSense; do not remove and resubmit an in-progress site. This project does not claim AdSense approval or guaranteed revenue.

## Structure

| Path | Purpose |
| --- | --- |
| `content.py` | Bilingual articles, class profiles, glossary and source register |
| `visuals.py` | Interactive class explorer, visual dashboard and guide diagrams |
| `assets/explorer.js` | Class/mode/tab state, saved preference and accessible keyboard navigation |
| `fieldnotes.py` | Attributed bilingual boss mechanics, player insights and source metadata |
| `encounters.py` | Original SVG schematics, boss views, source disclosures and insight cards |
| `assets/encounters.js` | Mechanic/stage selection, share links and insight filters |
| `assets/encounters.css` | Responsive boss and insight layouts |
| `onboarding.py` | Beginner priorities, item anatomy, stats and embedded maps |
| `skillbook.py` | 280 client-derived skill entries, icons, build paths, linked dialogs and static documents |
| `bossmedia.py` | Optional Korean source videos and Inven footage links |
| `assets/learn.js` / `assets/learn.css` | Legacy checklist, tooltip and accessible skill dialog behavior |
| `build.py` | Static templates, metadata and sitemap generator |
| `assets/style.css` | Responsive design, accessibility and print styles |
| `assets/app.js` | Search, filtering, comparison and local planner |
| `validate.py` | Local links, language pairs, JSON and ad-state checks |
| `docs/` | Generated site deployed by GitHub Pages |

AION 2 and related marks belong to their owners. This project is not affiliated with or endorsed by NC.

New implementation: `firststeps.py`, `growth.py`, `worldmap.py`, `battlelab.py`, `assets/deep-guide.js`, `assets/battle.js` and `assets/deep-guide.css`. Versioned facts are in `data/skills.json` and `data/maps.json`.

Map projection follows the provider’s transform: coordinates are `[vertical, horizontal, altitude]`; source tiles stay on TH.GL CDN and attribution remains visible. Map completion is browser-local and does not change the game. Base skills are 12 active + 10 passive + 13 Stigma per launch class; chain effects live under their parent skill. Point investment stops at level 10; higher target skill levels include equipment, Daevanion and Arcana.

## Google connection status (2026-10-08)

- Existing publisher: `ca-pub-9723666081819297`, confirmed against the current host root. Root `ads.txt` already lists this publisher. The project emits the matching metadata without requesting ads.
- The account-specific verification file `google722860ebc63f523b.html` is preserved by every build, ready for the project URL-prefix property. This is preparation, not a claim that Search Console has confirmed the property.
- GA4 property `558027990` (PLAYER’S CODEX · AION 2), web stream `16065115962`, measurement ID `G-S45PCCH32Y` were created in the existing account `410587266`. Reporting uses America/Regina and CAD. The stream URL is the project URL, and enhanced measurement is off. `site.json` enables the existing consent-based integration in `measurement.py` and `assets/analytics.js`.
- Search Console submission and the current AdSense review status are tracked separately from Analytics activation.
- On changing the GA4 stream, keep enhanced measurement off (including automatic form/site-search/history events). This integration sends controlled page views and public interaction categories. Rebuild, validate, deploy, and verify opt-in traffic in Realtime.
- When enabled, the bilingual analytics controls allow refusal/withdrawal; before consent there is no Google tag request. URLs are sent without query strings/fragments, and planner/form values are never collected by this integration. Consent is separate from an advertising CMP.
