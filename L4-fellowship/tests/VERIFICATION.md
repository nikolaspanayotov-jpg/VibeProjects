# Implementation verification

Date: 3 November 2026. Result: **passed** in Playwright Chromium.

The page was exercised from a localhost server scoped to `L4-fellowship`, and separately by opening `index.html` directly from disk. All runtime content is local; no required external network requests or JavaScript page errors were observed.

## Browser checks performed

- Clean first visit: all 37 index links, no fabricated completion, no assumed assessment date.
- Search by topic/identifier, combined filters, clearing filters and empty results.
- All 37 complete lesson views, answer guides, personal response forms, preparation targets and source links.
- Response, confidence, learning and coverage persistence through reload; text containing HTML remains plain text.
- Review scheduling: help/partial/independent outcomes, seven-to-fourteen-day progression and manual dates. A Pacific/Kiritimati browser at a UTC date boundary confirmed local calendar dates.
- S12's two stakeholder slots and S13's forecast/mining worksheet persist; the S13 plot has an accessible description and the documented exact-value table.
- Evidence validation, two-KSB rationales, linked/reviewed states, edit, delete/undo and unfinished draft recovery.
- Practice: guidance hidden before reveal, pause/reload/resume, timer expiry preserves the response, ratings schedule reviews and mixed discussion contains K/S/B topics.
- Study plan, priority topics and conditional AP03 filters, reconciling 17 project-route and 20 discussion-route KSBs.
- Six practical exercises and all four CSV downloads. Fixtures reconcile to 300 requests, 30 missing completion dates, four missing service IDs, eight unmatched S99 records and 357 rows after the deliberately flawed join. Monthly series: 12 observations; feedback: 36 comments.
- JSON export; malformed, unsupported-version and unknown-KSB import rejection; import preview; default conflict retention; non-conflicting additions; explicit replacement confirmation.
- Corrupt storage remains untouched and downloadable. Simulated quota failure leaves an exportable temporary session.
- All main views checked for horizontal page overflow at 320, 390, 768 and 1280px. Desktop screenshots use 1440px. The tablet KSB index breakpoint was corrected after an observed overflow.
- Keyboard entry through the skip link, focus into main content and the next study action; reduced-motion mode and print navigation suppression.
- Direct file opening loads the full curriculum and synthetic forecast without `fetch()` or a server.

JavaScript syntax checks passed for the application and curriculum. The curriculum compiler checks the 37-item set and preserves the complete answers, examples, templates, evidence prompts and follow-ups. The source hash is embedded in `curriculum.js`.

## Visual inspection and limits

Desktop and mobile screenshots were inspected for hierarchy, legibility, reading surfaces, index layout and overflow. Test output and screenshots are saved under `/tmp/l4-qa` during this session and are not application data or committed assets.

This is focused browser verification, not a complete WCAG conformance audit or cross-browser certification. Provider-specific assessment requirements and detailed current-law/source verification remain as described in `solutions.md`. No real workplace evidence, model result or stakeholder feedback is asserted by the synthetic examples. Hosted-page offline reload and cloud synchronisation are not implemented; direct file opening and JSON transfer are supported.

## Guided lessons, worked project and readiness — 3 November 2026

Both the existing smoke check and `browser_enhancements.py` passed after the improvements. No page errors were observed. Enhancement screenshots/results are kept under `/tmp/l4-enhancements-qa`; the regression output is under `/tmp/l4-regression-qa` in this session.

- All 37 KSBs contain the short explanation, worked example, common mistake and probing question, while retaining the complete original guide and evidence prompts.
- Mobile Learn / Worked example / My answer / Practise jumps open and focus the correct content. Detailed guidance remains expandable, and sticky navigation does not cover the response field.
- Genuine-personal-example confirmation persists, clears on edits and stays separate from evidence and confidence. A legacy v1 record retains its response, confidence, gap note and settings while defaulting the new confirmation to false.
- The readiness matrix filters correctly. A seeded combination of partial recall, a draft example and missing evidence produces the expected three distinct actions and routes each to the matching KSB. User-entered markup stays plain text.
- Probing practice questions use their own question type, preserve responses across pause/reload and remain compatible with backup validation.
- The worked project has six navigable stages, eight annotated artefacts, links covering all 37 KSBs and a downloadable Markdown portfolio. Its approved example lookup downloads five unique reference rows.
- The portfolio's four SQL queries execute against the actual downloaded fixtures: duplicate S2 count two, flawed join 357 rows, approved join 300 rows, and missing/unmatched counts four/eight.
- The dashboard derives 300 requests, 270 completed, 30 open and median eight days from the same fixture generator as the CSV downloads. Service counts reconcile to 300. Feedback totals are 42 theme assignments across 36 comments, with explicit multiple-theme and sampling caveats.
- Project navigation/downloads do not create personal evidence, mark learning complete or copy fictional experience into a personal response. “Write my own example” opens the relevant empty/previously saved response without filling it from the case.
- New views reflow without page overflow at 320, 390, 768 and 1280px; enlarged reading text, keyboard jumps and direct file opening also work. Phone/desktop screenshots were inspected for the short lesson, readiness and project layouts.

## Analysis labs, branching scenarios and misconception quizzes — 4 November 2026

The existing smoke and guided-study checks passed with the new tools. The focused `browser_learning_tools.py` check also passed; its results and screenshots are under `/tmp/l4-learning-tools-qa` for this session. These are Chromium checks, not a complete accessibility or cross-browser certification.

- The statistics lab's outlier, observed-value exclusion and three missing-value treatments agree with independent Python mean/median calculations. Keyboard range interaction, reload persistence and lab-only reset were exercised.
- All four join types, with and without a duplicate lookup key, agree with actual SQLite output counts, distinct request IDs and sums. UNION/UNION ALL retain their different duplicate semantics and use compatible request tables.
- Twenty-four forecast configurations agree with independent regressions and RMSE calculations. Only available post-training observations enter error; beyond-history projections stay separate. Narrow-screen axis labels were simplified after visual inspection found an overlap; the check asserts visible month-label bounds do not overlap.
- All three scenarios follow their authored decision graphs. The check exercises risky and defensible routes, validates nonempty justifications, recovers drafts/outcomes through reload and verifies that imported paths cannot invent transitions. Restart affects one scenario only.
- The 30-question bank covers all KSB identifiers as conceptual revision material. Feedback is hidden until submission, recorded once through reload, and includes an explanation. The previously-missed and due queues, next-day incorrect review, correct-answer spacing and paused-set recovery were exercised.
- Lab, scenario and quiz work does not modify KSB recall, learning, confidence, personal-example confirmation or evidence automatically.
- JSON backups include new tool progress and unfinished sets. Merge preserves conflicting current settings and adds new records; old v1 imports preserve newer tool work. Invalid identifiers (including prototype-like keys), values and graph paths are rejected without changing state. Explicit replacement restores the complete tool state.
- New views reflow at 320, 390, 768 and 1280px, with enlarged reading text and direct file opening supported. Phone and desktop screenshots were inspected for lab results, question feedback and scenario choices. No JavaScript page errors were observed.

Question answers are canonical in the `solutions.md` appendix. The compiler validates 30 stable question IDs, KSB coverage, scenario reachability, acyclic paths, the saved-route length limit and the third authored-source hash. The question counts are practice information, not an EPA Pass prediction or verified workplace competence.

## 5 November 2026 — reasoning tools, notebook and connections

All four browser suites passed against the updated local page in headless Chromium (Playwright 1.64.1). JavaScript syntax checks passed for the application and curriculum. The authoring compiler passed ID, choice, KSB reference, annotation and coverage checks; all four source hashes were verified alongside the 37 lessons and 30 misconception questions.

Commands used in this environment:

```bash
PYTHONPATH=/tmp/l4-authoring python3 tests/compile_curriculum.py
node --check /tmp/extend-app.js
node --check curriculum.js
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_smoke.py --url http://127.0.0.1:8000/ --output /tmp/l4-core-regression
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_enhancements.py --url http://127.0.0.1:8000/ --output /tmp/l4-guided-regression-new
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_learning_tools.py --url http://127.0.0.1:8000/ --output /tmp/l4-learning-regression-new
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_reasoning_tools.py --url http://127.0.0.1:8000/ --output /tmp/l4-reasoning-qa
```

`/tmp/extend-app.js` was extracted from the shipped inline script. The new suite exercises all four correction challenges and six method decisions, required justifications, feedback hiding/reveal and reload persistence. Its SQLite calculation independently confirms the join example's five rows / total 90 versus source total 60. It checks six-part K/S/B example annotations, per-KSB drafts, clearing self-checks on edit, cancellation/acceptance of personal-response replacement and preservation of evidence/recall/coverage.

Notebook summaries, approved reference strings and manual verification dates persist and appear in the linked lessons and workshop. Malicious-looking note HTML and `javascript:` reference text stay inert. All nine connections collectively cover 37 KSBs, filter correctly and display actual matching evidence with its rationales. Combined responses save separately.

Synthetic records round-trip in JSON and the Markdown summary. Conflicts keep current records unless imported records are chosen. Old v1 backups retain the new sections on merge. Unknown/prototype-like IDs, invented choices, incomplete revealed responses, duplicate self-checks and impossible dates are rejected without changing saved state. The original three suites also passed their existing recovery, cross-device restore, lifecycle, data reconciliation and legacy compatibility checks.

All new views were checked at 320, 390, 768 and 1280 pixels, with enlarged text, keyboard radio selection and direct file opening. No page errors were recorded. Desktop connections and correction feedback, the mobile connection flow and the mobile answer workshop were visually inspected. Test screenshots, downloads and synthetic personal progress stay outside the repository. These browser checks are not a full accessibility conformance audit.

## 5 November 2026 — six further additions and offline lifecycle

All six browser suites passed on the final application in headless Chromium with Playwright 1.64.1. JavaScript syntax checks passed for the inline application, curriculum and service worker. Five content hashes, 37 KSB records, 30 quiz IDs and every precached public-asset hash were independently verified.

The four established suites passed again with outputs in `/tmp/l4-final-core`, `/tmp/l4-final-guided`, `/tmp/l4-final-learning` and `/tmp/l4-final-reasoning`. They retain the earlier coverage of storage failure, corrupt-data recovery, legacy backups, evidence status, numerical fixtures and guided study. The initial keyboard check caught the backup reminder preceding the primary study action; the reminder was moved below that action and the final check passed.

New commands (alongside the four existing suite commands):

```bash
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_rehearsal.py --url http://127.0.0.1:8000/ --output /tmp/l4-final-rehearsal
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_offline.py --url http://127.0.0.1:8001/L4-fellowship/ --fixture /tmp/l4-pwa-fixture/L4-fellowship --output /tmp/l4-offline-qa
```

The offline suite used a second localhost server rooted at `/tmp/l4-pwa-fixture`; it only changed its copied fixture to simulate releases. The test accounts for SimpleHTTPServer's whole-second Last-Modified validation when changing worker files. This fixture timing adjustment does not weaken the production SHA-256 asset checks.

Activity results:

- Eight combinations of n, known standard deviation, difference and confidence level matched independent Python `NormalDist` intervals and `math.erfc` p-values. All 100 interval rows reconciled with their displayed coverage and width; settings and simulation seed persisted.
- Confidence ratings survived unfinished quizzes, were recorded once before feedback and did not change KSB states. Unrated attempts were excluded; revisiting a question preserved an unfinished quiz.
- All three changed-condition cases required a choice/reason, explained changed versus retained assumptions and retained drafts/review state.
- Briefing drafts remained separate by scenario/audience, displayed tailored examples, escaped untrusted preview text and downloaded the actual draft and reference.
- Evidence rehearsal required support, contribution and limits, displayed saved rationales after review, supported explicit gaps and preserved explanations when an evidence reference was removed.
- New state round-tripped through JSON; conflicting imports retained current records by default; older v1 data retained new records during merge. Invalid IDs, confidence labels and numerical controls were rejected without mutation.

Offline results:

- Manifest scope/start URL and 192/512 PNG dimensions were checked. Registration and all cached URLs stayed under the project subpath; the cache contained only public assets.
- Actual offline reloads succeeded across lessons and new activities, public source guides were fetchable offline and edits survived disconnection/reload.
- A deliberately mismatched HTML/curriculum release failed installation. The previous complete copy and progress remained available.
- A valid release waited for explicit application. Simulated storage failure blocked reload; the temporary draft could be exported and restored, then survived activation and another offline reload.

New views were checked at 320, 390, 768 and 1280 pixels, with mobile activity selection, enlarged text and direct file opening. No page errors were recorded. Desktop briefing/statistics views and mobile statistics/offline views were visually inspected; the interval plot's mobile labels were enlarged and spaced for legibility. Screenshots and synthetic backups remain under `/tmp`. Headless Chromium does not test native OS installation dialogs, and these checks are not a complete WCAG conformance audit.

## 5 November 2026 — daily missions, dated rewards and quest history

All seven browser suites passed on the release application, plus `node tests/gamification_core.cjs`. JavaScript syntax checks passed for the inline app, `gamification.js`, curriculum and service worker. The five curriculum source hashes, 37 KSB records, 30 misconception IDs and all 12 cached public-asset hashes were verified. The new reward helper is included in the atomic offline release.

Release commands used:

```bash
node tests/gamification_core.cjs
node --check /tmp/habit-app.js
node --check gamification.js
node --check curriculum.js
node --check sw.js
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_smoke.py --output /tmp/l4-habit-release-core
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_enhancements.py --output /tmp/l4-habit-release-guided
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_learning_tools.py --output /tmp/l4-habit-release-learning
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_reasoning_tools.py --output /tmp/l4-habit-release-reasoning
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_rehearsal.py --output /tmp/l4-habit-release-rehearsal
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_gamification.py --output /tmp/l4-habit-release-game
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_offline.py --output /tmp/l4-habit-release-offline
```

`/tmp/habit-app.js` was extracted from the shipped inline script. The app suites used the project-local server on port 8000; the offline lifecycle suite used the disposable project-subpath fixture on port 8001. All test dates, reflections, backups and screenshots are synthetic and remain outside the project.

Pure calculations covered: 20/20/20 plus 40 daily XP and its cap; first qualifying badge dates; quest receipts; removal recalculation; current/best streaks across gaps; local dates and both sides of a DST fallback; exact time-window boundaries; supporting quiz-review prerequisites; same-day versus later-day mistake recovery; explicit 37-topic coverage; two audiences for the same scenario; and three linked discussion attempts.

The new browser suite completed real Recall, Apply and Explain tasks at three controlled local times, earning exactly 100 XP and the quality quest. It verified that unfinished reflections survive reload, a block cannot finish before interaction/source completion, and application/evidence-gap practice leaves KSB/evidence state separate. Further practice respected the daily cap. Badges showed their qualifying day, pinned correctly and exported local SVG cards; the desk's lamp unlocked. Selecting another quest changed actual mission suggestions.

Five reviewed quiz questions created one supported block; reloading did not duplicate records. The optional mixed rehearsal recorded three distinct K/S/B attempts and its cosmetic milestone. Time settings rejected invalid boundaries, retained historical window assignments and exported three 90-day calendar recurrences with alarms, stable IDs, floating local times and RFC-style folded lines of at most 75 bytes. The structural calendar checks do not assert delivery by an external calendar application.

Removal/undo recalculated XP and badges. Merging an older backup preserved removal IDs, identical imports did not duplicate rewards, and conflicting practice records required explicit imported-record selection. Older v1 data retained the new history during merge. Duplicate IDs, unknown/prototype-like types, invalid dates/offsets/windows, invalid schedules and unsupported tracked contexts were rejected without mutation. Full reward history round-tripped into a fresh browser context.

Weekly replay used actual records. Normal-motion playback advanced and paused when the document became hidden; reduced motion retained manual controls. Markdown recaps and SVG weekly cards reconciled with the recorded week. All new routes reflowed at 320, 390, 768 and 1280 pixels, enlarged text fit, and direct file opening loaded the required helper without page errors. Desktop reward/mission views and mobile missions/quest paths were visually inspected. The initial regression run exposed a hidden Resume practice button in the collapsed broader study plan; unfinished sessions now open that section and both existing resume checks passed.

The offline suite additionally earned a new practice record while disconnected and verified that the same game events survived temporary-memory recovery, verified service-worker activation and offline reload. It retained its checks for project scope, public-only caches and rejection of mismatched releases. These checks are not a complete accessibility audit and do not cover native OS installation dialogs or calendar alert delivery.

## 5 November 2026 — distinct visual memory cues for every KSB

All eight browser suites passed, alongside the scoring/date checks and JavaScript syntax checks. The new compiler validation passed for exactly 37 known IDs, unique names and SVG bodies, bounded captions and an SVG shape/attribute allowlist. All six content-source hashes, 37 guided records, 30 quiz IDs and 13 offline asset hashes were verified.

The existing core, guided, learning-tools, reasoning, rehearsal and gamification suites passed against the icon-enabled application, with outputs under `/tmp/l4-visual-core`, `guided`, `learning`, `reasoning`, `rehearsal` and `game`. The added suite and final offline check used:

```bash
PYTHONPATH=/tmp/l4-authoring python3 tests/compile_curriculum.py
python3 tests/build_offline.py
node --check /tmp/visual-app.js
node --check curriculum.js
node --check sw.js
node tests/gamification_core.cjs
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_visual_cues.py --output /tmp/l4-visual-release-cues
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_offline.py --output /tmp/l4-visual-release-offline
```

`/tmp/visual-app.js` was extracted from the shipped inline script. The visual suite inspected every cue in the map and index, then opened all 37 lessons and checked that each used exactly the same artwork and caption as its map card. Names and geometry were distinct. Browsing all pictures left personal KSB state, evidence and reward records unchanged. SVGs were decorative/non-focusable, with visible ID/title/caption text and keyboard-accessible links.

Library search located B2 through its “roadblock” cue. Readiness contained all 37 matching topic illustrations; the quality connection used K8/S6/B5; discussion practice showed the correct K1 picture and mnemonic; related-topic chips used the same art. Native text selects and existing KSB-ID text remained usable. The 37-picture memory map worked by opening the file directly, printed with all images present and generated a substantial A4 PDF through the browser print engine.

The new route, index, library, lesson headings, practice, readiness, connections and quests were checked at 320, 390, 768 and 1280 pixels, including enlarged text. No page errors were recorded. The complete desktop gallery was visually inspected for all 37 associations, along with desktop K1 and mobile S13/gallery layouts. Pictures retained readable sizes in the map and scaled down consistently for repeated cues. The K4 caption explicitly notes that data types can overlap and sensitivity is a separate question.

The offline suite reloaded `#visual-map` while disconnected and verified all 37 cards, in addition to its source-guide, scope, mismatch rejection, safe update and personal-progress preservation checks. The canonical visual JSON and the matching new curriculum version are covered by the atomic cache manifest. No new personal-data fields or reward rules were introduced. Test screenshots/PDFs remain under `/tmp`; these checks are not a complete accessibility conformance audit.

## 5 November 2026 — visible shortcuts and fading success feedback

All eight existing browser suites passed against the updated page, along with the scoring/date checks and JavaScript syntax checks. Outputs are under `/tmp/l4-feedback-core`, `guided`, `learning`, `reasoning`, `rehearsal`, `game`, `visuals` and `offline`. The additional `tests/browser_feedback.py` suite passed with output under `/tmp/l4-feedback-qa`.

The focused suite exercised all four shortcut destinations by keyboard, visible focus, touch targets and responsive layouts at 320, 390, 768 and 1440 pixels without changing saved progress. It submitted unanswered, incorrect and correct quiz questions; checked that focus stayed on the answer feedback; observed the actual CSS fade and eventual hiding; and verified repeat correct answers and no replay after reload. Correction, method and changed-assumption questions also received success feedback only after the authored correct choice and required explanation.

The same three-step weekly quest was completed through real Recall, correction and retrieval workflows in two separate weeks. Both completions displayed congratulations, including the second week after the original badge had already been earned. Incomplete quests and reloads did not display congratulations. The suite also checked static reduced-motion feedback, saved opt-out/re-enable behaviour and ordinary status toasts above the success message. The existing offline checks passed through disconnected use, rejection of a mismatched release, explicit verified update and preservation of personal records.

Desktop shortcut and correct-answer screenshots and phone shortcut/quest-completion screenshots were visually inspected. The buttons are prominent and the success message fits near the bottom with readable contrast. Synthetic screenshots and exported data remain outside the project under `/tmp`. No personal state schema or reward rules changed. These checks are not a complete accessibility audit.

## 5 November 2026 — seven guided-study improvements

All ten browser suites passed. The existing core, guided-learning, learning-tools, reasoning, rehearsal, gamification, visual-cue and feedback outputs are under `/tmp/l4-seven-core`, `guided`, `learning`, `reasoning`, `rehearsal`, `game`, `visuals` and `feedback`. The final expanded offline suite passed under `/tmp/l4-seven-offline-final`; the added `tests/browser_guided_study.py` passed under `/tmp/l4-seven-new`. The compiler regenerated 37 guided records, the complete project and activities with all six verified source hashes. JavaScript syntax checks passed for the inline app, curriculum, reward helper and generated worker. The pure scoring/date checks passed. All 13 cached-asset hashes matched the final offline manifest.

The new suite verified that the phone shortcuts fit in the first viewport with 44px touch targets and keyboard activation; all 13 original activities remain reachable from the grouped practice navigation; the recommended recall session lasts five minutes; and a completed tracked activity has a visible nearby finish action which uses the original reflection dialog. It exercised ten-row readiness paging, KSB search, disclosure expansion, all-37 mode and inert search markup. During development it caught a blur/change rerender which could swallow disclosure activation; the duplicate change handler was removed and the complete flow then passed.

Visual sessions for K1, S8 and B5 were completed through actual UI. Unfinished visual text survived reload and restoration in a separate browser context; the new question type retained existing strict v1 validation. The guide stayed hidden until reveal, and independent evidence/personal-example checks were not completed automatically. All 37 KSBs retain their authored scenarios, with the shared memory-cue suite verifying the existing illustrations. Lifecycle, join and statistics diagrams were checked.

A saved assessment date of 20 November 2026, preferred Monday/Wednesday/Friday study days and K13 priority produced the expected first day and topic, paged across weeks and stopped on the deadline. Past dates produced an actionable empty state and browsing did not change KSB records. Every new application challenge was answered, explanation-gated, revealed and reloaded. Chart tables matched their authored values. The weighted-mean and held-out RMSE keys were independently calculated. Backups restored all eight new records and the selected new quest in a separate context. All six quests were present and selectable.

The expanded offline suite reloaded the new chart/calculation routes, readiness, plan and quests while disconnected, alongside its original guide, scope, mismatched-release rejection, explicit update, memory-recovery and persistence checks. Responsive checks covered 320, 390, 768 and 1440 pixels and direct file opening of a new chart challenge. Desktop and phone screenshots of navigation, recommendations, readiness, charts and planning were visually inspected. Test data and screenshots remain synthetic and outside the project under `/tmp`. These checks are not a full accessibility audit or a prediction of EPA success.

## 5 November 2026 — seven preparation tools

The final release passed all eleven browser suites: the ten existing suites (including the expanded offline lifecycle suite) and `browser_preparation.py`. Logs are in `/tmp/l4-preparation-final`; the focused suite's screenshots, synthetic audio exports and result report are under `/tmp/l4-preparation-qa`. Both pure Node checks (`preparation_core.cjs` and `gamification_core.cjs`) passed, as did syntax checks for the inline app, new preparation modules, vendored SQLite engine and generated service worker. All eighteen cached public-file hashes matched the generated offline manifest. The core curriculum and its six canonical sources were unchanged.

The new browser suite completed a mixed K/S/B mock, reloaded an unfinished answer, verified that model guidance stayed hidden until completion, saved self-checks/next steps and exported the actual review. The pre-existing discussion draft, KSB evidence/recall fields and reward history remained independent. Notebook drafts and quiz-seeded reasoning persisted; scenario/probe revisits required a written explanation and explicitly recorded a future review date. Tagged course notes appeared in the right lessons, incomplete URL drafts survived reload, HTML-like personal text stayed inert, and inline definitions opened/closed by keyboard with focus restored. All twelve visual-comparison applications were answered with authored feedback and new-answer celebrations.

Each of the six authored SQL solutions ran in both independent Python SQLite and the browser's real sql.js engine with matching columns and rows. An arbitrary query returned its actual result. Tests exercised syntax errors, mutation rejection by the read-only database, multiple-statement rejection and termination of an unbounded recursive query after eight seconds. Saved drafts, progressive hints and direct `file://` execution worked. The unmodified sql.js 1.13.0 asm distribution has SHA-256 `c83beac167ae9c1af075449555b1db68b24b5280d0fc65c1f7ac4d1cd103459d`; its license is shipped locally.

A synthetic browser microphone exercised the actual MediaRecorder API: explicit start/stop, playback with advancing audio time, IndexedDB persistence through reload, a real downloadable audio file, stop/save on navigation, the selected one-minute limit and ended media tracks. Explicit deletion removed the stored blob. Denied permission produced actionable feedback; cancelling a pending permission request stopped late-arriving tracks. A simulated IndexedDB quota failure retained playable, exportable temporary audio. A fresh profile restoring JSON correctly showed recording reviews without inventing missing audio files. Real microphone hardware, mobile browser codecs and OS permission dialogs were not tested.

Backup checks covered old-v1 merges, per-record keep/import choices, deletion tombstones, rejection of unsafe saved URLs and malformed dates/IDs/queues, and preservation of current state on invalid import. Text remained exportable after simulated localStorage failure. Pure validation tests also covered bounded fields, duplicate KSB tags, reserved object keys and invalid revealed answers. The offline suite loaded every new route without a network connection, ran SQLite offline, saved a tagged note, rejected a deliberately mismatched release and preserved the new records through the existing explicit verified update flow.

All new routes and integrated lessons fit 320, 390, 768 and 1440 pixel widths. Testing caught an intrinsic select-width overflow on narrow recording screens; constrained grid columns and full-width styled controls fixed it. Desktop studio/SQL and phone comparison/recording screenshots were visually inspected, including the refined heading layout and flow diagrams. Tests and exported audio contain synthetic material only and remain outside the repository. These checks are not a full accessibility audit or an EPA pass prediction.

## 7 November 2026 — resumed publication and bounded SQL packaging

The release was recovered from the saved workspace after interrupted large connector uploads. A small license blob and a 64,889-byte vendor chunk uploaded successfully with matching Git hashes. Publication now uses individual Git blobs, a local hash checkpoint and a final tree/commit assembled from those hashes. No specific GitHub file-size limit was reported; the stalled large requests are an observed failure, not proof of a GitHub limit. The local `.release-local/` checkpoint and original authoring source are excluded from the release.

The pinned sql.js 1.13.0 distribution is now packaged into 22 small scripts under `vendor/`. `tests/pack_sql.py` rejects any source whose checksum differs. The pure preparation suite reconstructs all fragments, verifies the original byte count and SHA-256, and parses the complete original engine. Both Node suites, JavaScript syntax checks and all 40 offline asset hashes passed. The final generated offline release is `2026-11-07-ac44df1e75d8`.

All eleven browser suites passed across two Chromium builds. The ten online/feature suites (smoke, enhancements, learning tools, reasoning tools, rehearsal, gamification, visual cues, feedback, guided study and preparation) passed unchanged with Playwright's bundled Chromium 151.0.7922.34. Their reports and screenshots are in `/tmp/l4-release-20261107-bundled`. These cover actual SQL from the reconstructed engine, direct-file operation, synthetic audio capture/export, backup validation/merges and phone layouts. Desktop studio/SQL and phone comparison/recording screenshots were inspected.

The unchanged full offline suite passed with system Chromium 154 using a temporary harness that selects that browser executable; its report is `/tmp/l4-offline-release-system-final/results.json`. It verified all new routes and real SQL while disconnected, saved course notes, rejection of a mismatched cache release, explicit application of a valid update and preservation of both existing progress and the new preparation records. The system browser restricts file URLs by administrator policy, so direct-file checks used the bundled test browser without altering those policies.

The bundled browser's offline suite exposed a test-emulation discrepancy: `navigator.onLine` became true after reload while an uncached request outside the service-worker scope still failed with a TypeError. An isolated probe established normal 200 responses before emulation, blocked requests while offline before/after SQL and reload, and correct restoration of the indicator through the supported CDP `Network.overrideNetworkState` command. No product code or assertions were changed to hide that discrepancy; the complete unchanged offline suite was verified in the second browser. Synthetic test data and audio exports remain outside the published tree. These checks are not a full accessibility audit.

## 7 November 2026 — source-referenced assessment content

All twelve browser suites passed: the eleven existing suites and the new `browser_assessment.py`. The ten existing online suites passed with bundled Chromium 151.0.7922.34; their reports are in `/tmp/l4-assessment-complete`. The final assessment suite passed in `/tmp/l4-assessment-content-final`. The expanded offline suite passed with system Chromium 154 in `/tmp/l4-assessment-offline-final`, using the browser split explained above. The final offline release is `2026-11-07-6815f2cc6215`. JavaScript syntax checks, all three pure Node suites, the compiler/structural checks and all 43 cached-asset hashes passed.

All 30 grading rows and 254 source prompts were compared with the supplied Markdown cells. The 30 groups cover exactly 37 unique KSBs, split into 13 AM1 and 17 AM2 groups. Only the eight source distinction rows contain distinction criteria. Provider Meets/Exceeds guidance, uncertain table boundaries and derived learning remain separately labelled. All four evidence packs retain their exact required/optional mappings. The supplied Markdown checksum and all seven compiled-source hashes were verified. The original 37 IDs, ordered numeric coverage targets and 30 existing quiz records are unchanged.

The focused browser checks exercised shared filters, exact criterion rendering, saved group notes and independent self-checks, all six evaluation exercises and six new misconception keys, reveal gating and idempotent success feedback. A source-question mock resumed answers, withheld rubrics until completion and exported its actual conversation. Question snapshots retained their revision. Source links opened the correct spoken-practice KSB without starting the microphone. Evidence templates created unfinished drafts only; explicit pack links and safe review metadata persisted separately from approval.

Old-v1 imports preserved current assessment records. Conflict choices, removed-mock tombstones, invalid identifiers/dates/methods, inert personal markup, changed-source recheck notices and export after failed storage were verified. Actual offline reloads covered the three new routes; a source answer survived disconnection and a verified update. Mismatched releases were rejected, unsafe updates stayed blocked and existing progress survived activation.

Responsive checks covered 320, 390, 768 and 1440 pixels, direct file opening and keyboard focus. Desktop and phone criteria, evidence-pack and chart-comparison screenshots were visually inspected. Both chart representations use the same synthetic weekly values, exact table, common zero baseline and non-colour line styles. A final wording check aligned the derived comparison prompt with its displayed three-series line chart. Screenshots, synthetic responses and private source/checkpoint files remain outside the public release. These checks are not a complete accessibility audit, verification of the original workbook or confirmation that the provider's assessment arrangements apply to this learner.

## 11 November 2026 — clearer reading, memory artwork and assessment study

The initial review opened 40 primary views with no page errors or desktop page overflow. Phone/desktop screenshots of the library, lessons, memory map and recent assessment content informed `page-review-improvement-plan.md`.

All thirteen browser suites passed. The eleven existing online suites ran with bundled Chromium 151.0.7922.34; reports are under `/tmp/l4-review-tests`. Final reruns of enhancements, visual cues and the new page-review suite are in their `*-final` folders. The expanded offline suite passed with system Chromium 154 in `/tmp/l4-review-tests/offline`, using the previously documented browser split. Three pure Node suites, JavaScript syntax, structural/compiler validation and all 43 public asset hashes passed. The final offline release is `2026-11-11-e2c62acdd112`.

The focused `browser_page_review.py` opened all 37 lessons and used keyboard activation to open/focus each detailed guide and native disclosure toggling to close it. Each guide directly follows its original 60-second explanation. Browsing left KSB progress, evidence and rewards unchanged. The highlighted button's hover contrast was checked. Actual in-page print handling expanded the guide, a real A4 PDF was generated, and the app's after-print handler restored the original disclosure state. OS print dialogs were not tested.

All 30 assessment groups displayed topic names and source-linked Explain/Show/Discuss coaching, with exact pass wording and only the eight existing distinction rows. The complete provenance text and limitations remained available through its disclosure. The 254 source question records, four pack mappings, source revision, numeric coverage targets, original quiz records and 37 existing lesson answers were independently compared with the baseline. All remain unchanged. All 37 SVG bodies changed while their established mnemonic names, captions and topic associations stayed exact; trusted SVG validation and matching compiled source hashes passed.

Question navigation saved two different responses, returned to each correctly and retained them through reload. Search kept keyboard focus/caret, combined with AM2/S13 filters, returned a useful no-match/reset state and treated markup as inert text. Opening another question or filtering did not change evidence or reward state. The existing assessment suite separately verified strict imports, old-v1 preservation, conflicts, source snapshots, quota failure/export, independent mocks and objective-only celebrations.

The focused layouts covered 320, 390, 768 and 1440 pixels, including clearance below both rows of sticky phone lesson controls, enlarged content in the existing suites, and direct-file detailed reading/search. Desktop and phone full-answer cards/open guides, the complete three-category gallery and new study briefs were visually inspected. The artwork retains blue Knowledge, green Skills and amber Behaviours and is reused consistently in the index and study tools. Testing caught and fixed a full-answer hover contrast issue and a duplicate navigation action on a redundant return button.

The expanded offline suite opened a detailed answer and the new artwork while disconnected, searched/navigated the bank, opened a coaching brief, and retained source-answer state through a verified update. It also exercised real offline SQL, mismatch rejection, safe update gating and existing progress recovery. Private source/checkpoint files, screenshots, synthetic responses, PDFs and audio remain outside the public release. These checks are not a full accessibility audit or a new verification of the provider's assessment applicability or current legislation.

## 12 November 2026 — ten multiple-choice study tests

All fourteen browser suites passed: the thirteen existing suites and the new `browser_multiple_choice.py`. Existing online reports are in `/tmp/l4-tests-qa`; the final focused report is `/tmp/l4-tests-qa/multiple_choice-final/results.json`. The online suites used bundled Chromium 151.0.7922.34. The expanded actual offline lifecycle suite passed with system Chromium 154.0.8037.57 under `/tmp/l4-tests-qa/offline`, using the previously documented browser split. All four pure Node suites and JavaScript syntax checks passed. All 47 cached public asset hashes match release `2026-11-12-57a2428536e7`.

The new compiler validated ten tests, ten distinct questions each, eight options per question, 3–4 correct choices and every one of the 37 KSBs appearing at least twice. All 800 options have specific explanations. Each question's exact guide excerpt, source anchor and SHA-256 were checked against the existing detailed answer, with the full solutions hash retained. The original curriculum, solutions, source criteria and memory artwork are byte-for-byte unchanged. Independent standard-library calculations reproduced the synthetic regression coefficients, held-out forecasts, RMSE, future projections and descriptive figures. Numerical integration of the t distribution independently confirmed the guide's rounded p-value of 0.08052.

The focused suite completed all ten tests through 100 actual checkbox questions. It checked withheld keys, all eight controls, exact-set marking, the first deliberately missed-plus-extra answer, explanatory feedback and the score for each test. A retake selecting all eight options in every question scored zero and did not celebrate. Each of the 100 authored keys also passed pure scoring checks with every single missing-required and extra-incorrect option, plus order independence. Scores are computed from validated choices; imported score fields fail validation.

Main-menu entry was verified on desktop and in the mobile selector; no Today, library, project, Practice, Readiness, evidence, plan or preparation body introduces a Tests link. Keyboard checkbox selection, independent drafts, saved question position, reload, retakes and earlier history worked. Result export contained actual selections and explanations, and a source link opened/focused the existing Definitions and detailed answer. KSB progress, evidence, reward history and discussion drafts remained unchanged. Correct-answer success feedback occurs only on a new eligible submission, without automatic competence or XP claims.

Old-v1 imports preserved test records; conflicts required per-draft choices; malformed option/question IDs, bounds and forged scores were rejected before mutation. Deletion tombstones blocked restoration from older backups. Pure checks also verified that an already submitted/deleted draft cannot reappear from an old backup. A fresh profile restored real JSON test history and drafts. Simulated storage failure retained the real selected answer in an exported temporary backup. A separate browser check filled the 100-result history, verified that blocked submission preserved the complete draft, and confirmed that removing one old review allowed that unchanged draft to submit (`/tmp/l4-tests-qa/capacity.json`).

Responsive checks covered 320, 390, 768 and 1440 pixels, touch-sized options, keyboard focus, an actual A4 review PDF and direct-file operation. Desktop catalogue/question/results, the complete-answer callout and phone question/results were visually inspected. Disclosure controls explicitly say Show/Hide explanation; choice labels remain usable without colour. No page errors were recorded. Test development corrected two harness issues: a storage-failure stub needed a function wrapper, and a phone backup check needed the visible recovery control rather than the hidden desktop sidebar button.

While disconnected, the expanded offline suite resumed a two-question draft, submitted a complete ten-question test, started another draft and retained both submitted and unfinished test state through a verified update. It also retained its existing real SQL, source-question, workshop, mismatch rejection and safe-update recovery checks. Public question banks and scripts alone are cached; personal selections stay in guarded local state. Private release/source files, screenshots, synthetic backups, PDFs and recordings remain outside the public tree. These checks are not a full accessibility audit or validation of official EPA grading.
