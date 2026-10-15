# Project change history

## 2026-10-15 — independent map review and mobile gestures

- Compared four local terrains with 64 freshly fetched TH.GL tiles; checked 9,738 imported positions and recorded 47 display anchors. Cross-checked growth-region terrain and visible samples against historical KR player screenshots, retaining explicit gaps in object/current-client verification.
- Fixed missing touch pinch zoom and initial/resize observations overriding a shared-location view. Preserved map IDs, saved completion and language deep links.
- Clarified the provider's 559 traces versus historical KR guides' 560; no guessed position or unsupported region was added.
- Added touch/coordinate regressions and source-snapshot replay. Build/link checks, 58 Python tests and both map browser suites pass locally. PR CI remains separate from deployment.

[Review evidence and limits](research/map-audit-2026-10-15.md)

## 2026-10-15 — weekly DPS refresh and same-day KR correction

- Refreshed JaMeter's provisional October 14–21 index and completed October 7–14 comparison; labelled the changed 750–850K CP band and retained source precision and sample gates.
- Preserved AionFlex's earlier review, figures and hashes when two boss URLs redirected to a different boss. Added per-dataset dates and a safe weekly-only review mode.
- Kept older regional patch warnings visible when only the review date advances.
- Added the official October 14 KR hotfix (0.3s → 0.1s defensive cooldown reduction and passive-attack fix), with a separate summary and links from the preserved morning patch.
- Validation: static build/link validation, Python unit suite, DPS/math/ranking/rotation/patch/analytics/battle tests, provenance regeneration and JavaScript syntax checks. Browser coverage is run by the repository CI; local Chromium could not start because the executor blocks process sockets.
- Backup: exact pre-update main `c6665f61a3f4ad298ceb49dc6869f7aa2dd58e71` saved as a private Library ZIP with rollback instructions. File: `Aion2-Daeva-Atlas-before-20261015-c6665f61a3f4.zip`; SHA-256 `34880bbb3cb9bdf74f059f37eec12cbee2c42a8d473ea1a2860cf6fb68c3ae62`. ZIP CRC and original DPS source bytes verified.
- Deployment: pending PR checks and the existing GitHub Pages publication workflow. Release verification will be recorded after publication.

[Source review and boundaries](research/dps-review-2026-10-15.md)
