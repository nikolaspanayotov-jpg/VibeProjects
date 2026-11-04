# CodingScore

A personal scorebook for using Codex in everyday work. Log actual uses, document your work XP, and build a trail of useful results.

Open `index.html` in a modern browser. No installation, account, build step, or backend is needed. For a stable browser-storage origin, serve this folder with any static server, for example:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000/`. The live page is [CodingScore](https://nikolaspanayotov-jpg.github.io/VibeProjects/CodingScore/). Preserve the project folder's case in the URL.

## What you can do

- Record and edit dated Codex uses, categories, results, manually assigned work XP, and optional minutes or references.
- Earn 20 daily XP, up to 30 documented work XP, 5 learning XP, 5 next-task XP, and a consecutive-day bonus capped at 25. The page explains the full receipt; 85 XP is the daily maximum.
- Explore the seven-day track, activity calendar, XP history/table, category counts, levels, and milestone badges.
- Record the remaining percentage and next reset shown by Codex for the five-hour and seven-day limits. Expired readings require an update; timers never refill quota automatically.
- Pick a five-hour mission, link a timed actual use to bank a stamp, and carry an unfinished mission to a later observed window.
- Configure an actual seven-day usage period, earn cosmetic 3/5/7-date and variety stamps, and save a period review to the journal.
- Save the next task or copy a practical starter prompt. Planning alone does not create an active day.
- Filter the journal, delete a use with undo, change your weekly target, and export/import your whole scorebook.

## More ways to make progress

- **Project quests:** Create a project with four named steps, defaulting to Investigate, Build, Test, and Finish. Log actual Codex work against a step; explicitly mark it complete when ready. All four completed steps earn a quest badge and workshop tools. Edit labels without losing links, archive old projects, and filter active/completed/archived quests. Delete an empty quest after confirmation.
- **Weekly highlight reel:** Pick a date to review its Monday–Sunday week. See active days, XP, useful results, estimated minutes saved, a highlighted result, and first-time categories/workflow uses. A current-week recap compares the same elapsed weekdays with the previous week. Download a shareable PNG card, with SVG fallback, or copy the text summary. Cards stay local until you choose where to share them.
- **A growing workshop:** Seven illustrated items unlock from real milestones: 1/3/7/14/30 active dates, the first completed project quest, and a seven-day consecutive streak. Select an item to see its requirement and progress. Everything is cosmetic; nothing costs XP.
- **Personal challenges:** Each calendar week suggests two historically less-used task categories and a three-category variety challenge. Accept a challenge, then earn its stamp through logged work. Category challenges require a useful result. Suggestions use activity before the week so they remain stable as you log new work. Previous challenges stay visible in their history.
- **Practical payoff:** Add optional before/after notes and estimated minutes saved to any use. See them in the journal, weekly recap, and lifetime payoff summary. Missing estimates stay unrecorded; zero is a valid estimate. Estimates are self-reported, can overlap, and do not affect XP.
- **Workflow library:** Save a successful prompt from a journal entry or create a workflow directly. Keep its result, context, category, and favorite status. Search/filter it, copy the prompt, and log its actual reuse. Deleting a template preserves its historical uses, saved prompts, title snapshots, XP, and reuse badge.

Creating quests, accepting challenges, saving/copying prompts, and downloading recaps do not create an active day or award XP. Quest, challenge, and workshop rewards derive from source records and recalculate when history changes.

## Illustrated quests and rewards

- Choose a rocket, robot, toolbox, compass, bug, or lightbulb emblem when creating or editing a quest. Existing quests receive the compass emblem automatically; step IDs and progress stay intact.
- Follow illustrated Investigate/Build/Test/Finish markers with explicit step status. Connected completed neighbors show the journey. The path becomes vertical on narrow screens so its order stays clear.
- Browse twelve collectible achievement illustrations. Streak artwork grows from a spark to a flame, campfire, sun, and starburst. Locked rewards retain a faded preview of their actual art, a progress ring, and the requirement.
- Filter the collection by All, Earned, or Next. Select any badge for details. Earned badges show the first qualifying local date and explain the source work; **Revisit that day** opens the actual daily record. Correcting history recalculates this evidence.
- New unlocks can briefly stamp into place with a glint, respecting the celebration preference and reduced-motion setting. Previously earned badges do not animate on every visit.
- The Today area features an unfinished active quest and the closest unfinished achievement beside daily logging. Saved next-task notes and prompt suggestions remain available under **Saved next task and prompt ideas**. The full reward collection stays in Progress.

All artwork is self-contained inline SVG, using the existing blue/peach/navy visual language. No image requests or dependencies are needed. Quest emblems are included in normal backup/export. The JSON format remains version 2, and the storage key and XP rules are unchanged.

## Explore your work

- **Clickable workshop:** The desk opens your active quest, books lead to workflows, the trophy visits earned achievements, the plant opens activity history, the lamp opens task cards, tools lead to projects, and the window opens the practice map. Objects have mouse/touch targets and keyboard controls. Locked decorations never prevent access to features; the item buttons still explain unlock requirements.
- **Win cards:** Useful results and before/after notes become flippable cards. See the task on one side and the actual recorded result on the other, including optional estimated savings. Filter by category, browse three cards at a time, and open the full daily record. Missing outcomes remain explicitly missing.
- **Growing quest stories:** Each of the six emblems has five illustrated stages, from a faint blueprint to a complete scene. Distinct completed steps advance the artwork. Select a quest illustration for the larger story, its step status, logging, and precisely filtered linked work. A newly completed quest can show a dismissible celebration; historical corrections recalculate the scene.
- **Personal badge showcase:** Open an earned badge and pin it near the top of Today. You can keep up to three favorites, unpin them, and download individual achievement cards as PNG with SVG fallback. Cards include the real earned date and recorded story and are never shared automatically. If a correction removes the earning condition, a previous pin remains visibly locked until the work qualifies again or you unpin it.
- **Practice islands:** Explore six illustrated routes for Build, Debug, Review, Automate, Learn, and Plan. Each shows actual uses, useful results, distinct dates, recent work, prompt ideas, and 1/5/15/30-use milestones. These describe practice, not a skill assessment. You can log a category use or browse its journal records directly.
- **Task deck:** Open **Saved next task and prompt ideas**, flip a bug/robot/lightbulb card, and copy its full starter prompt. Draw more cards or filter the category. The logging control starts an empty use record with the matching category; it never invents or saves an activity for you.
- **Weekly replay:** Choose a week in the recap and select **Replay my week**. Browse actual daily work, first completed quest steps, project completions, first-earned badges, and workshop unlocks in local-date order. Play, pause, restart, seek, or step manually. Playback stops on close, hidden tabs, source changes, and the final moment. Reduced-motion preference uses manual navigation. Empty weeks show no invented events.

The only new saved preference is `settings.pinnedAchievements`; older backups default to an empty list. Card flips, map navigation, replay controls, and task draws are temporary interface state. None of these interactions award XP, consume Codex quota, or create active days.

## Your data

All personal records stay in browser storage under **`codingScore.v1`**. The current JSON format is version 2; existing version 1 data/backups migrate without changing their original records or scores. The storage key is unchanged. This is manual tracking, not a connection to your Codex usage. Fonts load from Google Fonts when available; system fonts work offline. No application data is sent to a server.

Export a JSON backup in Settings before clearing browser data or switching devices. Import validates the backup, previews its contents, and asks before replacing current records. Unreadable stored data is preserved for download; blocked/full storage falls back to memory with a visible notice. File URLs and different hosts may have separate storage, so export before moving to a hosted copy.

Activity dates retain their recorded local labels. Known occurrence timestamps determine mission/campaign attribution, including exact start/end boundaries. Backdated records without a time still count for daily XP and streaks. Days use calendar arithmetic across daylight-saving changes. A missed date starts a new streak, while the best run remains visible.

## Checks

No test dependencies are required. From this directory:

```sh
node tests/core.test.cjs
TZ=America/New_York node tests/core.test.cjs
TZ=UTC node tests/ui.test.cjs
python3 tests/static_audit.py
```

The first suite checks the real inline scoring/date engine. The second command repeats those checks across a daylight-saving timezone. The UI suite runs the complete inline script against a small DOM adapter to exercise its actual event handlers, storage, and backup flows. It does not simulate browser layout or native focus/validation behavior.

See [verification.md](./tests/verification.md) for the checks completed and browser QA still outstanding. The initial brief is [plan-and-design.md](./plan-and-design.md).
