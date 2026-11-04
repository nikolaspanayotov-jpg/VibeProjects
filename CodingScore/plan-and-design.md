# CodingScore — plan and design

Date: 2026-11-04  
Status: Implemented as a static page; see [README.md](./README.md) and [verification notes](./tests/verification.md) for usage and validation limits.  
Location: `VibeProjects/CodingScore/`

## 1. Purpose

Make daily Codex use feel rewarding and easy to repeat. CodingScore is a personal scorebook: document a real use of Codex, collect points, extend a streak, and see the useful work accumulating. A short session that solves a small problem should feel like progress.

The page should answer three questions immediately:

- What have I achieved with Codex?
- What small task could I use it for today?
- How can I plan my next task around the five-hour and seven-day usage limits?

The first deliverable is this combined plan and design file. The next phase is a working static page, following the scope below.

## 2. Repository and design guidance

This plan applies the repository's [root instructions](../AGENTS.md), [frontend-design skill](../.agents/skills/frontend-design/SKILL.md), and its [design reference](../.agents/skills/frontend-design/references/anthropic-design.md).

- Keep the project self-contained. The initial app will be one `index.html` containing vanilla HTML, CSS, and JavaScript, with no build step, framework, backend, or required account.
- Store personal records locally and support JSON backup and restore.
- Design at 390px first, then expand to desktop. Use semantic controls, visible focus, readable contrast, and reduced-motion support.
- Use a coherent visual direction, one memorable interaction, and plain interface language.
- Keep the exact requested folder name, `CodingScore`. This follows the user's explicit naming request over the repository's lowercase-folder default. Its eventual URL path is case-sensitive.

Nearby projects demonstrate the repository's independent static-page pattern. CodingScore gets its own visual identity and imports no code or assets from another project.

## 3. Core experience: a Codex arcade scorebook

**Direction:** a bright, tactile arcade scorebook with a seven-day combo track. Daily work becomes a trail of completed date tiles; choosing a tile reveals what Codex helped with that day. The personality comes from the track, useful writing, and responsive feedback.

The surrounding page stays calm: one clear logging action, a compact score line, a work journal, and two practical usage-limit meters. Avoid a wall of identical statistic cards.

### The daily loop

1. Open the page. See today's status, the current streak, and one suggested task.
2. Use Codex on something useful in normal work.
3. Choose **Log Codex use**, add a short note, and document the points for the work.
4. Save. Today's tile fills, the score updates, and a concise receipt explains the points.
5. Optionally write the next task, making tomorrow easier to start.

Logging a basic use should take under 30 seconds. Usage-limit readings, minutes, and detailed reflections are optional.

### Useful task suggestions

Rotate a small local library of prompts, with **Try another idea** and **Copy prompt** controls. Suggestions should produce useful work, for example:

- Explain a function or unfamiliar part of a codebase.
- Find the cause of an error and suggest a small fix.
- Review a change for edge cases.
- Turn a repeated manual task into a script.
- Draft tests for a risky behavior.
- Break a task into steps or improve technical documentation.

Let the user choose a category: Build, Debug, Review, Automate, Learn, or Plan. Copying a prompt earns no points; the user records the actual use afterward.

## 4. Points and progression

Call points **XP** throughout the page. All work is self-reported; the app does not verify Codex activity.

| Action | XP | Rule |
| --- | ---: | --- |
| Use Codex on a day | 20 | Once per local calendar date, with a short note about the use |
| Document work | 0–30 | Manually assign 0–10 XP per entry; show 5 and 10 XP shortcuts; cap the sum at 30 per day |
| Record something learned | 5 | Once per active day; include a short learning note |
| Write the next task | 5 | Once per active day; include an actionable task |
| Consecutive-day bonus | 0–25 | `min(5 × (streakLengthOnThatDate − 1), 25)` |

`dailyXP = 20 + min(30, sum(entryXP)) + learningXP + nextTaskXP + streakBonus`

Apply the formula only on days with at least one recorded Codex use. The maximum is 85 XP per active day. The first entry secures the day's base points; further entries document more work without repeating the base award. Minutes are optional context and never multiply XP.

Examples:

- First day: use Codex, document a 10 XP win, record a lesson and next task: **40 XP**.
- Second consecutive day: use Codex, document 20 XP of work, record a lesson: **50 XP** including a 5 XP streak bonus.
- Seventh consecutive day, with every daily category filled: **85 XP** including a 25 XP streak bonus.

Show a receipt such as: “20 daily + 10 work + 5 learning + 10 streak = 45 XP.” Make **How points work** available beside the total and in the logging form. Preview points before saving; editing an entry recalculates the receipt.

### Levels and rewards

Use cumulative XP thresholds, with a progress bar showing the next threshold:

| Total XP | Title |
| ---: | --- |
| 0 | New explorer |
| 100 | Daily starter |
| 300 | Problem solver |
| 700 | Workflow builder |
| 1,500 | Codex regular |
| 3,000 | Everyday maker |

After 3,000 XP, add a numbered level every 1,000 XP. Levels change the scorebook emblem; they grant no extra scoring multipliers.

Badges reward clear milestones: first logged use; 3-, 7-, 14-, 30-, and 100-day streaks; first automation; ten documented wins; and use across all six task categories. A documented win is an entry explicitly marked **Useful result**, independent of its manually assigned points. Badges and limit-challenge stamps are cosmetic and add no XP. Every badge shows its requirement and progress; an unlock requires no manual claim button.

## 5. Consecutive days and streaks

- An active day contains at least one actual Codex use with a nonempty note. An unsuccessful debugging attempt or learning session still counts. Opening CodingScore, planning without using Codex, and updating a limit meter do not count.
- Multiple entries on the same date count as one active day. Backdated entries are allowed for correcting missed logs, up to today; future activity is rejected.
- Group entries by the local `YYYY-MM-DD` chosen when logging. Do not derive a displayed activity date from UTC.
- Current streak is the consecutive run ending today, or ending yesterday while today remains unlogged. If neither date is active, current streak is zero. Preserve the longest streak and lifetime progress.
- A missed date breaks the consecutive-day run. Use warm copy: “Your next run starts with one useful task.” Keep missed days visually neutral.
- At 3, 7, 14, 30, and 100 consecutive days, award the corresponding badge and briefly celebrate. The daily bonus reaches its cap on day six.
- Recalculate all streak bonuses, XP, levels, and badges from the dated records after edits, deletion, backfilling, or import. Explain that correcting history can change later streak bonuses. Never increment permanent counters separately from the records.

Do not add streak freezes to the first version: the consecutive-day number should always mean actual consecutive use. Add a separate optional weekly active-day target, defaulting to five, so a useful workweek is visible alongside the everyday streak. This target does not preserve or change the streak.

## 6. Gamifying the five-hour and seven-day limits

### What these meters mean

Treat five hours and seven days as **usage-limit windows**, not allowances of five hours or seven days of continuous work. Actual quotas, shared pools, and reset behavior depend on the user's current Codex plan. CodingScore has no live Codex usage connection in version one.

For each meter, the user can enter the remaining percentage and next reset date/time shown by Codex. Display **Manually entered**, the observation time, and the reset time. Keep optional named pools separate if needed later; the MVP starts with one five-hour and one seven-day meter. An unknown value must appear as **Not recorded**, never as a full allowance.

Do not calculate remaining quota from minutes, prompts, sessions, XP, or a timer. Reaching an entered reset time changes the message to **Reset time reached — update reading**; it does not refill a meter or assert that Codex is available. If the weekly limit is exhausted, a shorter-window reset must not imply restored access.

### Five-hour idea: the mission tray

Give each observed five-hour window a small tray with three optional actions:

| Action | Interaction | Reward |
| --- | --- | --- |
| Pick a mission | Choose one task before starting; keep its scope small enough to finish or learn something useful | Mission appears beside the meter |
| Bank a win | Link a logged Codex use to this mission and write what changed | A completed mission stamp |
| Prepare the next run | Save one next task, especially when quota is low | A ready-to-start task for the next visit |

The stamp requires a linked activity note, not reaching a consumption threshold. Allow unfinished missions to carry forward. The tray records which observed window it belongs to; reset-time changes or duplicate readings must not duplicate completed missions.

When a user marks a limit reached or records 0% remaining, show **Recharge mode**: review previous wins, organize the task queue, or prepare context for the next run. These offline actions do not count as Codex use. A next-task note can earn its normal 5 XP only if that date already contains actual Codex use; there is no extra limit-related award.

### Seven-day idea: the weekly campaign

Tie a campaign to a user-entered seven-day limit period, with explicit start and end times. An optional start-time suggestion may be seven days before the entered reset, clearly labeled for confirmation; do not silently infer an actual provider window.

- **Show up:** log Codex use on 3 distinct local dates in the campaign to earn a bronze stamp.
- **Build rhythm:** reach 5 active dates for silver.
- **Full combo:** reach 7 active dates for gold, alongside the separate seven-day streak badge when the dates are consecutive.
- **Mix it up:** use Codex in three task categories to earn a variety stamp.
- **Close the loop:** write a short review of the campaign's most useful outcome; display it in the journal without extra XP.

Count only qualifying activity whose recorded occurrence timestamp falls in `[campaignStart, campaignEnd)`. Require a local occurrence time when explicitly linking backdated activity to a campaign or mission near a boundary. Map qualifying activity to its stored local date and count each date once. A campaign crossing eight local date labels still caps the active-date challenge at seven; a streak uses full local calendar dates independently.

Keep the **last seven calendar days** habit view separate from the provider's seven-day limit period. Label the former “Last 7 days” and the latter “Usage period,” with dates. A Monday–Sunday summary is a calendar view, not a claim about quota resets.

### Quota-aware prompts

Offer editable guidance bands based on the last manual reading: more than 50% remaining suggests a substantial task; 20–50% suggests a focused task; 1–19% suggests a small targeted question; 0% suggests preparation. Call these suggestions and show when the reading was recorded.

The points system has no reward for exhausting quota, hitting a limit, using every reset, or staying awake for one. Reset countdowns help plan a return; they do not create expiring rewards. There is no points penalty for unused allowance.

## 7. Information architecture and interactions

Use one page with anchors for **Today**, **Progress**, and **Journal**, plus **Settings** opening a dialog. Keep the logging button visible near the current-day status.

### Today

- Seven-day combo track: dated, selectable tiles showing use/no record, a connection only between consecutive active dates, and a marked current date.
- Current streak, best streak, total XP, and next-level progress in one compact score line.
- **Log Codex use**, today's point receipt, and one task suggestion or the saved next task.
- Five-hour and seven-day usage meters with **Update reading** controls and the mission tray.

### Progress

- Contribution calendar with distinct active-day patterns and a text legend. Selecting a day opens its records.
- Active days out of the last seven, this calendar week's target, and cumulative documented wins.
- A cumulative XP chart with date and XP axes, values on keyboard focus, and an equivalent text/table view. Show a flat line on inactive days; never invent activity.
- Badge shelf and a compact category breakdown that reveals useful ways Codex is entering everyday work.

### Journal

List actual records newest first. Filter by date, category, or text. Each entry shows its note, manually documented XP, optional result, optional minutes, and **Edit** / **Delete**. Provide a brief undo opportunity after deletion; editing points or dates previews the revised daily total.

### Logging form

Required: date, category, short use note, and documented work XP (default 5, editable 0–10). Optional: useful-result checkbox and outcome, learning note, next task, minutes, and link/reference. Expose occurrence time only for precise window attribution. A recorded use earns the day's 20 XP even when work XP is zero.

Use a bottom sheet on mobile and a dialog on desktop. Support Escape, focus trapping, return focus to the opener, and an explicit close button. Save updates the page without a reload. Announce the result through a polite status region; keep the success message and any undo control available long enough to use.

### Settings and ownership

Settings covers weekly active-day target, celebration preference, usage-period setup, JSON export/import, and a clear-data action with explicit confirmation. Export includes all records and settings. Preview import counts and date range; version one supports validated replacement after confirmation and a backup offer, avoiding ambiguous merges. Never replace current data on an invalid import.

No notifications, calendar connections, public leaderboard, or automated Codex telemetry are in the first version.

## 8. Visual design

### Palette

| Token | Color | Role |
| --- | --- | --- |
| `--bg` | `#EAF2FF` | Pale blue page background |
| `--surface` | `#FFFFFF` | Journal and form surfaces |
| `--ink` | `#172647` | Main text, track outlines, chart labels |
| `--muted` | `#596982` | Supporting text; verify contrast on each surface |
| `--accent` | `#2449D8` | Primary actions and completed track tiles |
| `--reward` | `#FFB782` | Milestone stamps and streak highlights, with dark text |

Status always includes words or an icon pattern. Use dark text on the peach reward color; do not use peach text on white. Validate all final foreground/background combinations during implementation.

### Type and spacing

- **Outfit** for headings and score numerals: a rounded geometric voice suited to the arcade track. **Source Sans 3** for readable body text and forms. Load fonts sparingly, with system sans-serif fallbacks and no functional dependency on the download.
- Body 16px, line-height about 1.55; supporting text at least 14px. Heading scale roughly 24/32/48px, with fluid sizing. Use tabular numerals for scores and countdowns.
- Sentence-case headings and labels; left-align the interface. Keep explanatory lines around 65–75 characters.
- Spacing tokens: 4, 8, 12, 16, 24, 32, 48px. Use 8px corners for controls and 16px for dialogs; make completed day tiles visibly distinct from ordinary surfaces. Avoid shadows under every section.

### Layout sketches

Desktop, maximum content width about 1,120px:

```text
CodingScore                    Today   Progress   Journal   Settings

Your week with Codex
[Thu]---[Fri]---[Sat]---[Sun]---[Mon]---[Tue]---[Today]
6-day streak   Best 12   640 XP   [level progress]

[Log Codex use]                 Next task: simplify the weekly report
Today's receipt                [Copy prompt] [Try another idea]

5-hour usage                   7-day usage period
[meter + observed reset]       [meter + observed reset]
Mission tray                   Campaign stamps

Progress: calendar and XP history
Journal: dated work, results, and lessons
```

Mobile at 390px:

```text
CodingScore                       Settings
Today       Progress       Journal

Your week with Codex
[Thu]  [Fri]  [Sat]  [Sun]
       [Mon]  [Tue]  [Today]
6-day streak · Best 12
640 XP [next-level progress]
[       Log Codex use       ]
Next task + copy control

5-hour usage + mission tray
7-day usage + campaign stamps
Progress
Journal
```

These labels and numbers illustrate layout only; the real first visit starts empty. On mobile the track wraps into a chronological list of four then three tiles; do not draw ambiguous connecting lines across rows. A text streak summary remains available. Below 390px, reduce gaps and use fluid tiles without horizontal page scrolling.

### Motion and feedback

The memorable moment is the saved day tile snapping into the combo track, accompanied by a 150–200ms score update. A milestone can show one short, dismissible stamp animation. Ordinary page load is still. Respect `prefers-reduced-motion` and the celebration toggle; communicate every reward in text even when animation is disabled. Avoid continuous flashing, countdown urgency, or repeated confetti.

## 9. Data and implementation outline

Persistence key: **`codingScore.v1`**. Store one versioned JSON object. Preserve the key after release; migrate intentionally if the schema changes.

| Collection | Essential fields |
| --- | --- |
| Root | `version`, `createdAt`, `updatedAt`, settings, entries, daily notes, quota observations, campaigns, missions |
| Entry | Stable ID, `localDate`, recorded local occurrence time/offset when known, `createdAt`, `updatedAt`, category, use note, work XP, useful result/outcome, optional minutes/reference, optional campaign/mission IDs |
| Daily notes | Local date, learning note, next-task note; one record per date |
| Quota observation | ID, window type, remaining percentage, `observedAt`, entered `resetAt`, optional campaign ID |
| Campaign | Stable ID, explicit start/end timestamps, review note |
| Mission | Stable ID, title, associated observed window, optional completion entry ID |
| Settings | Weekly active-day target, celebrations preference, display preferences |

Store timestamps with an offset or UTC instant for comparisons, alongside the chosen local activity date. Preserve historical date labels when the device timezone changes; default new logs to the device's current local date. Show the timezone beside reset-time entry fields. Handle local calendar arithmetic across month/year boundaries and daylight-saving changes; do not treat every day as exactly 24 hours.

Compute scores, streaks, charts, badge state, and campaign counts from source records. Do not store separate authoritative totals. Unattributed historical entries still count toward daily XP and streaks but stay out of precise usage-period challenges until the user supplies a valid occurrence time.

Keep scoring/date functions separate from rendering within the initial inline script. Useful boundaries: `getLocalDate`, `calculateDailyScore`, `calculateStreaks`, `calculateCampaignProgress`, `loadState`, `saveState`, and view-rendering helpers. Render user-provided text as text, and accept only safe web URL schemes for references.

Wrap every storage read/write and JSON parse in `try/catch`. If persistence fails, keep the page usable in memory and show “Changes are saved for this visit only. Export a backup.” Preserve malformed saved data for recovery rather than silently overwriting it. No data is sent to a server; the browser profile holds the records. Clearing browser data or changing devices requires a backup/import. Google Fonts, if used, is a separate external resource request.

## 10. Empty, error, and special states

| Situation | Required behavior |
| --- | --- |
| First visit | “Start with one useful task.” Empty track, zero XP, no invented streak or usage reading |
| Today already logged | “Today is logged.” Show the receipt and offer **Add another use** |
| Streak ended | Preserve best streak and lifetime results; invite a new use |
| Unknown quota | “Add a reading from Codex.” All logging stays available |
| Entered reset time passed | Mark reading as needing an update; retain its observation history |
| Limit reached | Show recharge tasks and the entered reset time; allow logging earlier real use |
| Invalid entry | Inline reason, preserved input, focus on the affected field |
| Storage unavailable or full | Visible session-only notice with export available |
| Invalid backup | Explain the validation failure; preserve existing records |
| No journal matches | Explain the filter and offer **Clear filters** |

## 11. Build sequence and acceptance criteria

### Phase 1 — daily logging and honest progress

Build the one-file static page, initial visual system, empty state, add/edit/delete flow, daily scoring, local-date streaks, combo track, levels, journal, and storage fallback. Add JSON export/import in this phase so personal progress has a recovery path.

Done when a real use can be logged in under 30 seconds; reload retains it; a second use on the same day does not repeat daily or streak bonuses; correcting an old date recomputes progress; and the page works by opening `index.html` or using a static server.

### Phase 2 — usage windows and motivation

Add manual quota readings, observed reset countdowns, mission tray, explicitly configured seven-day campaigns, task suggestions, badge shelf, contribution calendar, category breakdown, and accessible XP history.

Done when an unknown or expired reading cannot look like available quota, the two limit meters remain independent, campaign boundaries are respected, and offline preparation cannot create an active Codex day. Saving a completed mission creates one stamp regardless of repeated readings or edits.

### Phase 3 — verification and polish

Exercise the full logging and backup flows at 390px and desktop, then inspect 320px, long notes, 200% zoom, keyboard navigation, focus return, and reduced motion. Review screenshots for hierarchy, track order, form usability, readable data, and overflow. Check browser console errors.

Use meaningful scoring/date checks for duplicate same-day entries, a missed day, today still unlogged after yesterday, midnight, month/year boundaries, DST, historical corrections, deletion, import, daily point caps, precise campaign boundaries, and a short-window reset while weekly quota remains exhausted. Check storage-denied/corrupt-data states and invalid imports. No application tests or browser results are claimed by this planning document.

## 12. Review against the brief

- **Fun and interactive:** selecting past tiles reveals real work; recording today's use visibly extends the track; badges celebrate milestones.
- **Everyday motivation:** a saved next task and practical prompt suggestions remove friction at the start of a workday.
- **Progress:** documented wins, active dates, current/best streaks, XP history, and categories make the habit visible beyond a single score.
- **Manual ownership:** entries and work points are editable, calculations are explained, and backups keep the record portable.
- **Usage-limit ideas:** the mission tray and weekly campaign make the two windows actionable while accurately labeling manual readings.
- **Consecutive-day rewards:** an increasing daily bonus and milestone badges make returning tomorrow valuable.
- **Design critique:** replaced the default dashboard-card hero with the interactive seven-day track. Kept the meters and journal simple so the track remains the distinctive element. The palette, typography, and motion support a personal scorebook rather than a generic analytics page.

Defaults chosen for the first build: XP values above, five active days as the calendar-week target, no streak freezes, browser-local storage, manual quota readings, and no live integrations. Actual plan-specific quota behavior remains user-configurable through observed readings and explicit period dates.

## 13. Implemented extensions

The next iteration adds project quests, weekly highlight recaps with downloadable cards, a milestone-driven illustrated workshop, personal weekly challenges, optional before/after and estimated time-saved notes, and a reusable workflow library. See [README.md](./README.md) for each interaction and [verification notes](./tests/verification.md) for coverage and remaining browser QA. These additions preserve the original XP rules and storage key. JSON version 1 migrates to version 2; rewards and summaries continue to derive from actual dated records.

## 14. Illustrated quest and achievement direction

Carry the workshop's navy outlines and blue/peach fills into selectable quest emblems, a four-illustration step journey, category emblems, and twelve collectible reward designs. Locked achievements retain their real art with a progress ring and readable requirement. Earned badges gain a raised border and optional brief stamp/glint on first unlock. A selectable detail view explains when and how each earned reward qualified, using derived local dates from source records.

Give Today a compact focus panel for the active unfinished quest and closest reward, while keeping the main logging action prominent. Place saved tasks and prompt ideas in an expandable panel below; keep the complete reward collection in Progress with All/Earned/Next filters. Preserve the current fonts, palette, storage key, scores, and quest-step identities. The new emblem field is optional for old backups and uses a safe default.

## 15. Explore the artwork and the work behind it

Make the existing workshop an accessible navigation surface. Add actual before/after win cards, evolving five-stage illustrations for every quest emblem, three favorite badge slots with local achievement-card downloads, a six-island practice map, flippable task prompts, and a manually started weekly replay. These views reuse actual records and their first qualifying local dates. They do not create new scoring rules, live telemetry, or automatic sharing.

Pin preferences extend the existing v2 settings and default safely for older backups. All other exploration state is temporary. Empty views invite actual work; missing results remain missing; reduced motion preserves manual controls. See README for the final interactions and the verification notes for automated coverage and the remaining browser review.

## 16. A personal daily home and workshop

The next iteration implements all eight accepted ideas in the existing bright arcade style. Today keeps the logging action and current quest first, followed by a continuation capsule, companion, seven-day trail, and expandable prompt deck. Explore provides an illustrated directory to the larger collection. Existing section links and workshop shortcuts switch to the appropriate view before navigation; the lamp returns to Today’s prompt ideas.

- **Companions:** Orbit, Sprig, and Bolt are local SVG robots with ready, welcoming, and celebrating expressions. Choose or hide them. Clicking asks for a task idea and opens the existing ideas panel. Returning after a gap gets a welcome; no penalty or invented progress. Personal-best feedback obeys celebrations and reduced motion.
- **Decorations:** six earned decorations can occupy the wall, desk, or floor. A native dialog shows unlock requirements, placement, clearing, and two earned badge frames. Requirements derive from existing achievements. Historical corrections preserve chosen preferences while hiding art whose requirement is no longer met.
- **Mission packs:** Automate the Boring Stuff, Bug Detective, and Documentation Hero each contain three stable tasks. Explicitly accept a pack, link actual work to a task, and mark the result useful in the matching category. Distinct tasks earn stamps and a complete patch; repeated logs on one task never finish another.
- **Prompt lab:** start from scratch or a saved workflow. Keep up to thirty stable prompt versions per experiment, copy each, log the exact version actually used, and record personal observations and verdicts. Logged use and useful-result counts are derived independently of observations. A version tried from a current workflow also counts as an actual workflow reuse. Deleting a workflow retains experiment and entry history.
- **Continuation capsules:** save an action, context, category, optional prompt, and HTTP(S) link. The newest unfinished capsule appears on Today. Copy the starter to resume in Codex, then log real work and explicitly check completion. The result appears next to the original intention. Put aside/restore capsules without deleting their history. Editing or deleting completion work makes the next action available again.
- **Personal records:** four illustrated medals show the best streak, most consistent calendar month, most reused workflow, and completed project count. Details show actual supporting records (up to twenty) and derived dates. New personal bests receive short optional feedback after actual logged changes.
- **Personal rewards:** wrap a self-chosen treat behind total active days, a consecutive streak, a particular four-step quest, or a three-task pack. Eligibility is derived and can be revoked by historical corrections. Claiming is a separate user action, never a purchase. A claimed fact survives a correction and visibly explains if the milestone changed.
- **Today/Explore:** native view buttons keep the home focused. The existing project, progress, library, journal, and achievement links remain usable; Explore is an illustrated index to all old and new features. Source order and visual order match for keyboard navigation.

Persistence stays under `codingScore.v1`, JSON version 2. The optional `personal` object defaults safely for older backups and contains companion, decor, accepted packs, capsules, experiments, and rewards. Entries optionally link to a capsule/completion, pack/task, and experiment/version. Full validation precedes replacement, all content is escaped, and backup/import/clear includes every addition. Cosmetic interactions and offline preparation add neither XP nor active days. Existing XP rules and quota readings are preserved.

The new artwork is self-contained SVG. All three companions in three expressions, all six decorations, and both gift states were XML-validated, rasterized, and visually inspected. No example progress is installed. Automated core and UI-handler coverage includes migration, source correction, safe links, linked progression, claim limits, focus targets, navigation, and all-feature backup/clear. Full browser layout and native behavior remain pending because the supported preview tool is unavailable.
