# CodingScore project notes

Follow the repository's root instructions and frontend-design skill alongside these notes.

## Overview and running

CodingScore is a personal, browser-local scorebook for daily Codex use. The app is `index.html`, with inline CSS and JavaScript. Open it directly or serve this folder with `python3 -m http.server 8000`. Keep this project self-contained and build-free. Preserve the exact folder name and URL case, `CodingScore`.

## Architecture

- The inline `Core` object contains pure local-date, scoring, streak, level, badge, campaign, mission, and schema-validation functions.
- The UI IIFE handles rendering, native dialogs, forms, storage, JSON backups, and event delegation through `data-action`.
- Source records contain entries, daily notes, manual quota observations, campaigns, missions, and settings. Scores and rewards are derived; they are never independent saved counters.
- The persistent key is **`codingScore.v1`**. Preserve it after release. Wrap reads/writes; unreadable source data must survive for recovery until explicit replacement or clearing.
- `tests/core.test.cjs` extracts and exercises the actual inline `Core`. `tests/ui.test.cjs` executes the actual full script with a small DOM adapter. It is not browser QA. `tests/static_audit.py` checks static IDs, labels, icon targets, and DOM references.

## Rules that matter

- A recorded actual use earns one base award per stored local date. Work XP caps at 30/day, daily notes award once, and streak bonus caps at 25/day. Minutes and quota consumption never increase XP.
- Dates use local calendar arithmetic. Keep the original date label when a user travels. Precise quota-period attribution uses occurrence instants and half-open intervals `[start, end)`.
- Preserve seconds for an untouched occurrence time. Truncating a newly logged time to the displayed minute can place it before its mission's start.
- Unknown readings stay unknown. Expired readings stay unverified. A short-window reset cannot override weekly exhaustion. Never infer remaining quota from elapsed time, minutes, prompts, or XP.
- Mission and campaign stamps are cosmetic. Offline preparation never creates an active day.
- Validate imported records completely before changing current state. Confirm replacement/clearing, offer backup, escape all user content in generated markup, and allow only HTTP(S) reference URLs.

## Design

Bright arcade scorebook: pale blue `#EAF2FF`, cobalt `#2449D8`, navy `#172647`, white, muted slate `#596982`, and peach `#FFB782`. Outfit headings, Source Sans 3 body, system fallbacks. The seven-day track is the distinctive interaction; surrounding sections stay quiet. At narrow widths it wraps four tiles then three. CSS variables own the palette. Respect reduced motion and the optional celebration preference.

Native dialogs provide modal focus behavior. Preserve labels, visible focus, Escape/close controls, text equivalents for visual progress, and keyboard access. Check actual mobile/desktop rendering when browser tools become available; the initial environment did not provide the supported preview route.

## Validation

Run the commands in README after scoring, persistence, date, or interaction changes. Include browser QA for rendering/focus changes when available. Keep verification notes accurate; do not describe the DOM adapter as browser or accessibility testing.
