# PLAYER’S CODEX — game guides and tools

An independent English/Korean game guide platform. AION 2 is the first game hub.

**Website:** https://bumblev95.github.io/Aion2-Daeva-Atlas/

**PLAYER’S CODEX** contains 16 video-linked mechanics across six dungeon bosses, 21 attributed Korean community notes from 15 sources, six original decision and practice guides, eight class playstyle profiles, a two-class comparison, 32 Korean/English glossary entries, full-text site search and a personal session planner. Both language editions are generated as real HTML, with matching language links, canonical URLs and a sitemap.

## Visual interface

The hub opens with six navigation tiles, a four-stage beginner checklist and an eight-class selector. New `/start/`, `/maps/`, `/gear/` and `/skills/` routes explain progression, four zoomable starting maps, item anatomy, six base stats and 17 bilingual skills. Clicking a skill in a community tip opens an accessible dialog with a static full-page fallback. Overview, combat practice, gear checks and Korean community tips share a class panel, with PvE/PvP context and an illustrative positioning diagram. Bosses have timestamped gameplay, eight optional KR gameplay loops, accessible mechanic tabs and shareable links. Original position sketches are secondary disclosures. YouTube uses its own pause/speed controls; switching mechanics unloads hidden players. Community cards filter by class, topic and text, with author/date/source disclosures. Guide pages use step illustrations and expandable sections. The name is game-independent; no additional game hub is advertised before it exists. Existing public URLs are retained.

## Develop

Python 3.12+ and Node 22+ are sufficient. There are no package dependencies.

```sh
python build.py
python validate.py
node --check assets/app.js
node --check assets/explorer.js
node --check assets/encounters.js
node --check assets/learn.js
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

The planner stores its list in browser local storage; the class explorer can also save one preferred class. Existing planner data keeps its original storage key. It does not have a backend or accounts. No site-owned ad, analytics or external font scripts are installed. Beginner completion is local to the browser. Inven hosts screenshot previews and optional loops; TH.GL hosts the maps; YouTube hosts on-demand videos and may serve its own ads/storage. Media are not downloaded or republished in the repository. The public contact channel is GitHub Issues.

AdSense is configured **off**. See [OPERATIONS.md](OPERATIONS.md) before enabling it. A new website still needs its own site review even when its publisher already has an AdSense account. This project does not claim AdSense approval or guaranteed revenue.

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
| `skillbook.py` | 17 sourced skill definitions, translated inline links and static documents |
| `bossmedia.py` | Original media URLs and timestamp provenance |
| `assets/learn.js` / `assets/learn.css` | Checklists, map selection, skill dialog and media lifecycle |
| `build.py` | Static templates, metadata and sitemap generator |
| `assets/style.css` | Responsive design, accessibility and print styles |
| `assets/app.js` | Search, filtering, comparison and local planner |
| `validate.py` | Local links, language pairs, JSON and ad-state checks |
| `docs/` | Generated site deployed by GitHub Pages |

AION 2 and related marks belong to their owners. This project is not affiliated with or endorsed by NC.
