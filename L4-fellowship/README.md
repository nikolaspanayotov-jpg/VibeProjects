# Data Fellowship study desk

A personal study page for the Level 4 Data Analyst apprenticeship, covering all 37 Knowledge, Skills and Behaviours.

Open `index.html` in a browser, keeping `curriculum.js` and `gamification.js` beside it. There is no installation, build step, account or backend. For a local server, run from this folder:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8000/`. The same relative paths work under the GitHub Pages project subpath, `VibeProjects/L4-fellowship/`.

## What is included

- A distinct illustrated memory cue and mnemonic sentence for every KSB, repeated consistently through lessons and practice. Browse or print all 37 from the visual memory map at `#visual-map`.
- All 37 complete answer guides, each with a concise 60-second explanation, a worked example, a common mistake and a probing question. Expand the full definitions/calculations when needed; use the mobile Learn / Worked example / My answer / Practise navigation to jump between tasks.
- A six-stage fictional service-capacity project with eight annotated artefacts, reproducible SQL, an interactive join comparison, numerical/qualitative dashboard views and a downloadable portfolio. Its artefacts map to every KSB and never count as personal evidence automatically.
- A readiness matrix separating recall, explicitly self-checked personal examples and evidence. Its next three actions open the relevant explanation, probing practice, personal response or evidence form.
- Search and combined filters; learning, confidence, recall and evidence tracked separately; local-date review scheduling.
- Evidence references with per-KSB rationales, review notes, editable reflections, draft recovery and deletion undo.
- Quick recall, follow-ups, probing questions, project walkthroughs, weak-topic review and mixed discussion, with answer reveal, an optional timer and resumable sessions.
- Three interactive analysis labs under Practice: outliers/missing values, joins/unions and forecast windows/baselines. Controls change the actual calculations and exact-value tables using synthetic data.
- Three branching workplace scenarios with required justifications, consequences, alternative routes, saved drafts and reflection prompts.
- Thirty misconception questions with explanations after submission, a previously-missed queue, review dates and resumable question sets. Question results stay separate from KSB recall and evidence.
- S12 stakeholder worksheets, an S13 forecast/mining worksheet and an accessible synthetic forecast plot/table.
- Six practical exercises and four downloadable synthetic CSV datasets with data dictionaries, worked approaches and self-checks.
- Four “find and fix” challenges with diagnoses, decision impacts and explained corrections.
- Six method-selection decisions covering t-tests, association, regression and forecasting, with assumptions and alternatives.
- An answer workshop for all 37 KSBs: three annotated example structures, independent drafts and six self-review checks.
- A private organisation notebook for policy references, tools, architecture and stakeholder context, displayed in related lessons.
- Nine interactive KSB connections covering all 37 topics, with combined discussion prompts and your matching evidence rationales.
- A statistical uncertainty lab with computed intervals, p-values, practical thresholds and 100 simulated samples.
- Confidence-versus-accuracy review using optional pre-feedback quiz ratings.
- Three “what changes if…?” cases, a two-audience briefing studio and evidence retrieval rehearsal for every KSB.
- An installable offline page with verified matching releases and a reminder of your last JSON backup download request.
- A three-block daily mission board: Recall, Apply and Explain, with 20 XP each and a 40 XP daily trio bonus.
- Local-date study/trio streaks, configurable three-window check-ins, eleven illustrated badges and a growing clickable study desk.
- Three weekly quest packs, an optional mixed rehearsal, dated completion history, weekly replay and local recap/card downloads.
- Downloadable calendar reminders for three daily practice visits; completed practice and rewards are included in normal backups.
- A weekly study plan, optional assessment settings, conditional AP03 route filters, JSON backup/restore, a Markdown study summary and print styles.

New tools open at `#repairs`, `#methods`, `#workshop`, `#organisation` and `#connections`. Focused links include `#repairs-duplicate-join`, `#methods-paired-change`, `#workshop-k8`, `#organisation-policies` and `#connections-quality`.

Further activities open at `#uncertainty`, `#calibration`, `#changes`, `#briefing` and `#retrieval`. Use `#offline` for offline readiness, updates and home-screen installation instructions.

Practice rewards open at `#habits`, `#rewards` and `#quests`. Use `#habit-settings` for check-in windows, reminder times, calendar download and the celebration preference.

## Daily practice

Start a suggested mission on Today. Recall outcomes and five-question quiz reviews record their completion automatically. For labs, scenarios, challenges and writing tasks, choose **Track this activity**, work through it, then **Finish practice block** with a reflection and self-review. This awards practice XP and leaves KSB/evidence status separate.

Daily XP is capped at 100. More practice still contributes to history, check-ins and relevant badges. A three-check-in date requires completed blocks in three chosen windows; a daily trio requires the three block types. Schedules apply to future completions. Badges link to their qualifying practice records. Existing answers are retained; dated habit history begins with newly completed blocks.

The calendar download creates three local-time daily events with alarms for 90 days. Import the .ics file into your calendar; the website does not send background alerts. Badge and weekly cards are local SVG downloads, with a Markdown recap available too.

## Personal progress

Progress stays in browser storage under `l4-fellowship.v1`. Storage is specific to the device, browser and origin: opening the file, using localhost and visiting GitHub Pages can have different saved progress. Use the JSON backup and restore controls to move it. Merge retains conflicting current records by default and lets you choose imported records explicitly; replacement requires confirmation.

When storage fails, the page retains an exportable in-memory session. Corrupt saved data is left untouched and can be downloaded for recovery. If another tab changes the same progress, the current tab stops writing so it cannot silently overwrite those changes.

Use sanitised reflections and approved reference IDs. This public repository and browser storage are not approved storage for sensitive workplace evidence. Keep original material in its authorised location. Model answers, synthetic tasks and self-recorded coverage do not constitute assessor approval or a guaranteed Pass. Confirm your applicable assessment plan with the provider.

## Offline study

On the hosted HTTPS page, open **Plan and sources → Offline and installation** and wait for offline availability to be confirmed before disconnecting. The browser can then reload the app, lessons, activities and public source guides without a network. External reference websites still need a connection. Use the browser’s install or home-screen option when available. Browser storage and cached files can be cleared or evicted; keep JSON backups separately. Installation does not sync progress across devices.

An update waits for you to apply it or close older tabs. The app saves before reloading. Temporary-memory sessions must be exported before a reload; a failed or mismatched update retains the previous complete copy. Direct file opening remains available without service-worker installation.

## Files and content maintenance

`ksb-visuals.json` contains the 37 public cue names, captions and SVG illustrations. The compiler validates their shape markup and embeds them into the existing curriculum records with `visualSha256`. There is no extra runtime image dependency. Visual cues are mnemonic aids, separate from earned reward badges and personal progress. Library search also matches their names and captions.

`solutions.md` is the canonical public answer bank, including the short explanations, examples, mistakes and probes. `worked-project.md` is the fictional portfolio source; `design.md` records the page specification. `curriculum.js` contains the authored sources compiled into browser-ready records with source hashes and stable KSB anchors. `index.html` contains the application HTML, CSS and JavaScript. `gamification.js` provides the independent date/scoring functions, badge definitions and SVG artwork; it is a required relative script, with no package or runtime service. No runtime Markdown parser, external fonts, chart library or analytics service is used.

`solutions.md` also contains the human-readable misconception answer key. `learning-activities.json` is the authored lab/scenario source; the compiler validates its decision graphs and embeds it with the questions into the same local curriculum file. Learning tools are available at `#labs`, `#scenarios` and `#quiz`, with focused links such as `#labs-forecast`.

`reasoning-activities.json` is the canonical authored source for the five further tools. It is compiled into the same curriculum, validated for KSB/choice links and covered by `reasoningSha256`. The additive `studyTools` section holds each exercise, workshop draft, organisation note and connected explanation. Backups include these records; merge retains conflicting current work by default. The workshop only copies a draft into a KSB response when you choose that action, and confirms replacement of an existing different answer.

`rehearsal-activities.json` provides the changed cases and audience-specific briefing examples, with `rehearsalSha256` in the curriculum. The additive `rehearsal` state stores uncertainty controls, latest rated quiz comparisons, case/briefing/retrieval drafts and the backup request date. Ratings and rehearsal outcomes do not change KSB competence or evidence.

Lab assumptions, scenario routes and quiz records use an additive `learningTools` section inside the existing version-1 backup. Older progress remains readable. Merge keeps existing conflicting tool records unless you choose otherwise; replacement still requires confirmation. Wrong quiz answers are suggested for the following day, correct answers for seven days, or fourteen after consecutive correct responses. These are study defaults, not assessment rules.

When changing the answer bank, the optional authoring utility regenerates the checked-in curriculum:

```bash
python3 -m pip install Markdown
python3 tests/compile_curriculum.py
python3 tests/build_offline.py
```

This utility is for maintainers; the shipped page runs directly without it. Preserve the KSB identifiers, solution anchors, project path and storage key. Re-run `tests/build_offline.py` after changing any cached public file, including `design.md`, and commit the generated `sw.js` with those files. Its SHA-256 checks prevent mixed releases from activating. `manifest.webmanifest` and the PNG icons are relative to this project.

The additive `game` section holds dated completion records, schedule/preferences, one tracked block and removed record IDs. XP, streaks, badges and quests recalculate from that history. Imports validate known activities, timestamps/local dates and recorded window boundaries, merge identical IDs once, and retain conflicting current records by default. Removed IDs prevent deleted practice from returning through an older merged backup.

## Verification

See [the verification record](./tests/VERIFICATION.md). The browser smoke check exercises the main user flows, storage recovery, imports and responsive layouts. To run it with Playwright installed and a local server running:

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
python3 tests/browser_smoke.py --url http://127.0.0.1:8000/ --output /tmp/l4-qa
python3 tests/browser_enhancements.py --url http://127.0.0.1:8000/ --output /tmp/l4-enhancements-qa
python3 tests/browser_learning_tools.py --url http://127.0.0.1:8000/ --output /tmp/l4-learning-tools-qa
python3 tests/browser_reasoning_tools.py --url http://127.0.0.1:8000/ --output /tmp/l4-reasoning-qa
python3 tests/browser_rehearsal.py --url http://127.0.0.1:8000/ --output /tmp/l4-rehearsal-qa
python3 tests/browser_gamification.py --url http://127.0.0.1:8000/ --output /tmp/l4-gamification-qa
python3 tests/browser_visual_cues.py --url http://127.0.0.1:8000/ --output /tmp/l4-visual-cues-qa
node tests/gamification_core.cjs
```

The output folder contains screenshots and a JSON result report; it is not committed. Browser testing is not a complete WCAG conformance audit. For direct file opening, keep all the public files together in this project folder.

For the offline lifecycle check, start another localhost server rooted at a disposable `/tmp/l4-pwa-fixture` directory on port 8001, then run `python3 tests/browser_offline.py`. The test creates its `L4-fellowship/` fixture there, modifies only that copy to simulate releases and tests actual offline reloads. Native OS install dialogs are not covered by headless tests.

### Guided practice and assessment planning

On a phone, Practice, Quests and Rewards are available at the top of Today. Practice offers Recall, Apply and Explain recommendations; expand Browse all activities to reach the full tool collection. Select Picture → concept → scenario in discussion practice, or use Practise with the picture in any KSB lesson. Your unfinished visual responses use the same local save and JSON backup as other discussion sessions.

Readiness starts with ten expandable KSB records. Search by code, title or visual cue, filter gaps, page through results or show all 37. Plan and sources includes a weekly EPA roadmap based on your saved assessment date, study days, priorities and preparation gaps. Set these preferences below the roadmap. Planning itself does not mark anything complete.

The application collection now includes 14 decisions, calculation and chart challenges; quests include six themed packs. After a tracked activity, Review and finish this block appears beside the feedback and opens the existing reflection review. Today then offers your next quest step.

### Preparation studio

Open **Practice → Open preparation tools**. The new studio contains:

- **Mock EPA:** three or six mixed K/S/B questions, an advisory elapsed clock, saved answers and a final self-review. Guidance stays hidden until the set ends. A mock has its own draft and does not overwrite discussion practice. Completed reviews can be downloaded as Markdown.
- **Mistake notebook:** record what you thought, why it was wrong or incomplete, and what you will remember. Quiz feedback can seed an entry with your own reasoning. Revisit through a KSB scenario or decision probe; explicitly choose tomorrow or seven days after writing a new explanation.
- **SQL challenges:** six real SQLite exercises covering filtering, missing values, grouping, left/inner joins and HAVING. The fictional database resets on each run. Queries execute in a disposable Web Worker with a read-only database, a 32 MiB SQLite heap cap, a 100-row result limit and an eight-second timeout. Results are compared with authored expected output; matching a fixture does not prove a query is universally correct. Drafts and hints save locally; imported queries run only after pressing Run query.
- **Visual comparisons:** six paired concepts, each with two application questions, an explanation field and contextual feedback.
- **Spoken answers:** optional microphone recording for one or two minutes. Press Start to request permission, Stop to save, then play back and self-review. Leaving the tool or hiding the tab stops capture. Audio is stored in this browser's IndexedDB. If persistent storage fails, export the temporary clip before closing. JSON and Markdown backups include review text and metadata **but not the audio files**; use each clip's Export audio file button. Imported reviews on another device show that the original audio is absent. Explicit deletion removes the reference and attempts to delete the local blob. Clearing site data removes locally stored audio.
- **Course materials:** approved http/https links or pasted plain-text notes, tagged with one or more KSBs. Tagged resources appear in those lessons. Nothing fetches, imports or uploads external content automatically.
- **Terminology:** sixteen concise definitions with visual examples and common mistakes. Dotted terms in lesson prose open a keyboard-accessible dialog and return focus when closed.

These practice records use the additive `preparation` section of `l4-fellowship.v1`. Older backups default it safely, merges retain current conflicts unless explicitly replaced, and removal IDs prevent old merged backups from resurrecting deleted entries. Unfinished notebook and resource drafts are included. Recall, evidence, personal examples and quest rewards stay independent of these exercises.

Keep the complete project folder when downloading for direct file opening. New required assets are `preparation.js`, `preparation-data.js`, `preparation.css` and the complete `vendor/` folder; the offline worker verifies and caches them alongside the existing curriculum. Microphone support depends on the browser and secure context; HTTPS and localhost are supported environments. SQL, notes and other essential study tools also work from local files in Chromium.

The SQL engine is the pinned **sql.js 1.13.0 asm.js distribution**, downloaded from `https://cdn.jsdelivr.net/npm/sql.js@1.13.0/dist/sql-asm.js`. It is packaged in 22 small scripts under `vendor/`; these reconstruct the unmodified engine byte-for-byte inside the SQL worker. `vendor/sql-manifest.json` records the version and original checksum. Its MIT license and dependency notices are in [sql-LICENSE.txt](./sql-LICENSE.txt). There is no runtime CDN dependency. Authored fixtures and explanations live in `preparation-data.js`; this file is public learning content, never a place for personal notes.

Run `python3 tests/browser_preparation.py` and `node tests/preparation_core.cjs` with the existing checks. The browser test uses a synthetic microphone and disposable browser profiles, not real personal recordings.

The smaller vendor files avoid large publishing requests. To reproduce them during authoring, run `python3 tests/pack_sql.py /path/to/original/sql-asm.js`; it rejects a source with a different checksum. The shipped site needs no build, decompressor or runtime network dependency. `.release-local/` is a local recovery/checkpoint directory and must never be published.
