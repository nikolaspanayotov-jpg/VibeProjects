# CodingScore

A personal scorebook for using Codex in everyday work. Log actual uses, document your work XP, and build a trail of useful results.

Open `index.html` in a modern browser. No installation, account, build step, or backend is needed. For a stable browser-storage origin, serve this folder with any static server, for example:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000/`. The app's GitHub Pages path, after this branch is merged and Pages deploys, is `/VibeProjects/CodingScore/` on the repository's default GitHub Pages host. A custom domain can change the prefix; the project folder's case must be preserved.

## What you can do

- Record and edit dated Codex uses, categories, results, manually assigned work XP, and optional minutes or references.
- Earn 20 daily XP, up to 30 documented work XP, 5 learning XP, 5 next-task XP, and a consecutive-day bonus capped at 25. The page explains the full receipt; 85 XP is the daily maximum.
- Explore the seven-day track, activity calendar, XP history/table, category counts, levels, and milestone badges.
- Record the remaining percentage and next reset shown by Codex for the five-hour and seven-day limits. Expired readings require an update; timers never refill quota automatically.
- Pick a five-hour mission, link a timed actual use to bank a stamp, and carry an unfinished mission to a later observed window.
- Configure an actual seven-day usage period, earn cosmetic 3/5/7-date and variety stamps, and save a period review to the journal.
- Save the next task or copy a practical starter prompt. Planning alone does not create an active day.
- Filter the journal, delete a use with undo, change your weekly target, and export/import your whole scorebook.

## Your data

All personal records stay in browser storage under **`codingScore.v1`**. This is manual tracking, not a connection to your Codex usage. Fonts load from Google Fonts when available; system fonts work offline. No application data is sent to a server.

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
