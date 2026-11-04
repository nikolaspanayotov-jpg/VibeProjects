# CodingScore verification

Date: 2026-11-04

## Completed

- **15 core test cases**, run in UTC and America/New_York: scoring examples and caps, date arithmetic through leap/year boundaries and DST, open streaks ending yesterday, missed dates, historical corrections, levels, exact campaign boundaries, eight date-label periods, independent expired/exhausted quotas, mission attribution, schema/import validation, badge requirements, and travel with preserved local dates.
- **13 UI handler cases**, run with `TZ=UTC`: complete script boot, honest empty state, logging and reload, edit/delete/undo, backfill, invalid entries, immediate mission completion with preserved seconds, weekly exhaustion, campaign setup/review, escaped user text, denied storage, retained corrupt data, export, validated/confirmed import, and confirmed clearing.
- **Static HTML audit:** unique IDs, form names, label/icon/DOM targets, viewport/reduced-motion declarations, one inline app script with no script dependencies.
- **JavaScript syntax:** extracted inline script checked with `node --check`.

No application packages or browser dependencies were added.

## Six-feature expansion

The expanded suite now has **26 core cases and 27 UI handler cases (53 total)**. Core checks run in UTC and America/New_York; UI handler checks use UTC. The original checks remain in place.

Additional coverage includes v1-to-v2 migration without changed scores, four-step quest completion/correction and stable IDs, quest archiving/deletion, accepted challenges and weekly boundaries, recommendations stable during a week, missing versus zero payoff estimates, equivalent-period recap comparisons, first-time workflow/category detection, workshop milestones, workflow save/favorite/filter/reuse/removal, historical title snapshots after removal, escaped prompts and exported SVG, all-feature backup restoration, and complete clearing.

Representative recap SVG exports and locked/unlocked workshop illustrations were generated from the actual rendering functions and rasterized with installed SVG renderers. The exported recap and workshop artwork were visually inspected. These are asset checks, not a review of the full page's browser layout. The native browser PNG conversion path still requires browser verification; its self-contained SVG output and fallback download are covered.

## Illustrated quest and achievement update

The suite now includes **35 core cases and 35 UI handler cases (70 total)**. The added checks cover safe quest-emblem defaults and round trips, invalid artwork keys, partial-quest reward progress, accurate first-earned dates for streaks/results/categories/projects/challenges/workflows, corrections that revoke rewards, daily focus selection, the fully completed collection, selectable emblem focus, step-path connections, locked previews, earned details and day links, collection filters, and disabled celebrations.

All six quest emblems, twelve achievement images, and four step illustrations were rendered from the actual `Art` module into a contact sheet. The nested SVG parsed as XML and was rasterized with Inkscape; the rendered artwork was visually inspected for legibility, clipping, and consistency with the workshop palette. JavaScript syntax and the static HTML audit pass. This does not establish full-page browser rendering, native focus trapping, or animation behavior.

## Browser verification limit

The supported browser-preview tool was unavailable in this environment. No screenshots, visual viewport review, browser console inspection, native form-validation exercise, focus-trap assessment, or accessibility audit is claimed. The UI handler suite uses a DOM adapter; it cannot establish these properties.

Before describing the app as visually/browser verified, open it at 390px and desktop, inspect 320px and 200% zoom, use long journal notes, complete logging and import/export, tab through dialogs and chart points, test Escape/focus return, and check reduced-motion behavior and console errors. The responsive styles, native dialogs, labels, escaped rendering, and text/table alternatives are implemented but require that browser review.
