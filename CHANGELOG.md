# Project change history

## 2026-10-15 — weekly DPS refresh and same-day KR correction

- Refreshed JaMeter's provisional October 14–21 index and completed October 7–14 comparison; labelled the changed 750–850K CP band and retained source precision and sample gates.
- Preserved AionFlex's earlier review, figures and hashes when two boss URLs redirected to a different boss. Added per-dataset dates and a safe weekly-only review mode.
- Kept older regional patch warnings visible when only the review date advances.
- Added the official October 14 KR hotfix (0.3s → 0.1s defensive cooldown reduction and passive-attack fix), with a separate summary and links from the preserved morning patch.
- Validation: static build/link validation, Python unit suite, DPS/math/ranking/rotation/patch/analytics/battle tests, provenance regeneration and JavaScript syntax checks. Browser coverage is run by the repository CI; local Chromium could not start because the executor blocks process sockets.
- Backup: exact pre-update main `c6665f61a3f4ad298ceb49dc6869f7aa2dd58e71` saved as a private Library ZIP with rollback instructions. File: `Aion2-Daeva-Atlas-before-20261015-c6665f61a3f4.zip`; SHA-256 `34880bbb3cb9bdf74f059f37eec12cbee2c42a8d473ea1a2860cf6fb68c3ae62`. ZIP CRC and original DPS source bytes verified.
- Deployment: pending PR checks and the existing GitHub Pages publication workflow. Release verification will be recorded after publication.

[Source review and boundaries](research/dps-review-2026-10-15.md)
