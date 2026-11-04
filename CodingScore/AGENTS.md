# CodingScore project notes

Follow the repository's root instructions and frontend-design skill alongside these notes.

## Overview and running

CodingScore is a personal, browser-local scorebook for daily Codex use. The app is `index.html`, with inline CSS and JavaScript. Open it directly or serve this folder with `python3 -m http.server 8000`. Keep this project self-contained and build-free. Preserve the exact folder name and URL case, `CodingScore`.

## Architecture

- The inline `Core` object contains pure local-date, scoring, streak, level, badge, campaign, mission, and schema-validation functions.
- The UI IIFE handles rendering, native dialogs, forms, storage, JSON backups, and event delegation through `data-action`.
- Source records contain entries, daily notes, manual quota observations, campaigns, missions, quests, workflows, accepted weekly challenges, and settings. Scores and rewards are derived; they are never independent saved counters.
- The persistent key is **`codingScore.v1`**. Preserve it after release. Wrap reads/writes; unreadable source data must survive for recovery until explicit replacement or clearing.
- The JSON format is now **version 2**. `Core.validate` also accepts version 1, fills new optional fields/collections, and normalizes to version 2 without changing XP. Keep this migration path and include every feature in backup/import/clear flows.
- `tests/core.test.cjs` extracts and exercises the actual inline `Core`. `tests/ui.test.cjs` executes the actual full script with a small DOM adapter. It is not browser QA. `tests/static_audit.py` checks static IDs, labels, icon targets, and DOM references.

## Rules that matter

- A recorded actual use earns one base award per stored local date. Work XP caps at 30/day, daily notes award once, and streak bonus caps at 25/day. Minutes and quota consumption never increase XP.
- Dates use local calendar arithmetic. Keep the original date label when a user travels. Precise quota-period attribution uses occurrence instants and half-open intervals `[start, end)`.
- Preserve seconds for an untouched occurrence time. Truncating a newly logged time to the displayed minute can place it before its mission's start.
- Unknown readings stay unknown. Expired readings stay unverified. A short-window reset cannot override weekly exhaustion. Never infer remaining quota from elapsed time, minutes, prompts, or XP.
- Mission and campaign stamps are cosmetic. Offline preparation never creates an active day.
- Quests have four stable step IDs. A step completes only through an actual linked entry with `stepComplete: true`; multiple logs on one step cannot finish another. Archive quests with history; only empty quests can be deleted. Recalculate the quest badge and workshop tools from the entries.
- Personal challenges are accepted per local Monday–Sunday week. Suggestions use prior-week history, not this week's changing counts. Category challenges need a useful matching result; variety counts distinct categories. Creating or accepting one adds no XP.
- Payoff fields (`before`, `after`, `minutesSaved`) and kept prompts are optional entry metadata. A missing estimate is `null`, while zero is meaningful. Label all savings as estimates and never multiply them automatically or convert them into XP.
- Workflow reuse is a logged actual use, not a copy action. Preserve `workflowId`, `workflowTitle`, and the entry's prompt when a template is removed. A missing template is allowed only with a title snapshot; journal history and reuse badges must survive removal.
- Weekly recap comparisons use equivalent elapsed weekdays for the current week. Earlier weeks use complete Monday–Sunday periods. Share cards escape user text into a self-contained SVG, rasterized locally to PNG with SVG fallback; never upload or share automatically.
- Workshop objects are derived cosmetic rewards. Keep text requirements and accessible item buttons alongside the illustration. Preserve keyboard focus when redrawing the selected item.
- `quest.emblem` is optional in older v2 backups and normalizes to `compass`. Restrict it to the six `Core.EMBLEMS` values. Preserve it through editing/import/export without changing quest or step IDs.
- Badge progress includes partial project steps. `Core.achievementDetails` derives the first qualifying local date and its evidence; never invent or persist a separate earned timestamp. `Core.dailyFocus` chooses an active unfinished quest and the closest unfinished achievement, with a complete-collection fallback.
- Validate imported records completely before changing current state. Confirm replacement/clearing, offer backup, escape all user content in generated markup, and allow only HTTP(S) reference URLs.

## Design

Bright arcade scorebook: pale blue `#EAF2FF`, cobalt `#2449D8`, navy `#172647`, white, muted slate `#596982`, and peach `#FFB782`. Outfit headings, Source Sans 3 body, system fallbacks. The seven-day track is the distinctive interaction; surrounding sections stay quiet. At narrow widths it wraps four tiles then three. CSS variables own the palette. Respect reduced motion and the optional celebration preference.

Native dialogs provide modal focus behavior. Preserve labels, visible focus, Escape/close controls, text equivalents for visual progress, and keyboard access. Check actual mobile/desktop rendering when browser tools become available; the initial environment did not provide the supported preview route.

The added quests, recap, workshop, and workflow library keep the existing palette and typography. The original mobile step grid has been replaced by a vertical illustrated quest path; challenge and library cards stack. Workshop art is inline SVG with a textual equivalent. The recap export uses system sans-serif fonts and contains no remote images or scripts.

The illustrated redesign now uses the inline `Art` module for six quest emblems, four step illustrations, category artwork, and twelve reward designs. Desktop quest paths run horizontally; mobile paths run vertically. Only completed neighboring steps get a colored connection. Keep visible status text alongside artwork and progress rings.

Achievements are native buttons with All/Earned/Next filters and a native detail dialog. Locked badges preview their real artwork; they remain interactive. A new earned badge can animate once after an actual qualifying change, respecting both reduced motion and `settings.celebrations`. Art helpers accept fixed keys only and never interpolate user text into SVG. Global `[hidden]` handling must continue to hide styled buttons correctly.

The Today layout places daily focus beside logging, with ideas/next-task content in an expandable panel below. Keep the logging action prominent on mobile. Restore focus after rebuilding emblem choices and collection filters. The artwork contact sheet was visually inspected; full browser layout remains an explicitly unverified environment limitation.

## Validation

Run the commands in README after scoring, persistence, date, or interaction changes. Include browser QA for rendering/focus changes when available. Keep verification notes accurate; do not describe the DOM adapter as browser or accessibility testing.
