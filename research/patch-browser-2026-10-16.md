# Patch browser navigation regression — October 16, 2026

The [October 15 failed browser run](https://github.com/bumblev95/Aion2-Daeva-Atlas/actions/runs/38798980485)
read zero Sorcerer changes immediately after clicking the North America October
14 summary link. The expected count remains **3**.

## Evidence

- Failed commit: `d77c38def391ddd935aa8f77d3c3ad100ca7bec3`.
  Latest snapshot inspected: `dcfbb54bb6e88e58cb98bd7882c6c35ba3d76b8a`.
- At both commits, article `6acf20d007b77e214688a7ac` is reviewed with source
  hash `db9bde10552df0a16256346f008c8b32d3babf65a2efe6e79e7f9f14511c4b29`.
  It has 3 Sorcerer changes, 1 Spiritmaster change and 1 all-class change.
  `data/patch-reviews.json`, the feed and generated EN/KO detail HTML agree.
- The unmodified test passed with a normal local response. Streaming the **same
  detail HTML** in two chunks, 500 ms apart, reproduced the failure: immediately
  after `click()`, the URL was correct, `document.readyState` was `loading` and
  `.count()` returned 0. After `DOMContentLoaded`, the count was 3.
- The public EN/KO detail pages were also inspected in Chromium at 390 px:
  both displayed 3 Sorcerer changes and 1 Spiritmaster change, with matching
  source hashes, visible reviewed content and no horizontal page overflow.

This reproduces a test synchronization error. No patch data, reviewed values,
source hashes, rendering code or generated HTML needs changing.

## Regression coverage

`tests/patch-ui.test.js` now deliberately streams detail HTML in two chunks
250 ms apart and waits for the target URL **and** `DOMContentLoaded` before
asserting. No sleep is added to the assertion path. Each reviewed page must
match its item ID, language, source hash, reviewed rows, class subjects, change
types and before/after values. The explicit 3/1/5 and KR 34-item assertions remain.

List refresh waits for its own feed response and replacement of the old card.
An existing source-health message can no longer satisfy a later refresh.
Repeated refresh, filter persistence after reload, class-fragment reload,
language switching, KR correction links, complete tables, stale-source hiding,
JS/no-JS detail pages and 320/390/768/1440 px layouts are covered. Failures retain
HTML, URL/readiness metadata and a screenshot alongside existing CI evidence.

The browser workflow's main-branch path filter includes this test so a test-only
fix also runs after merge. The separate PR triggers the full browser workflow
and the complete build/unit/static-validation workflow.
